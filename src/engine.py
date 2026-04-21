"""Session orchestrator — ties taxonomies, rules, registry, flags, and output
together for a single user session.

Kept separate from ``decision_tree`` so the rule engine remains a pure data
transformer and the orchestration (I/O, audit logging, LLM calls) is
isolated.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from src.artefact_registry import ArtefactEntry, ArtefactRegistry, load_registry
from src.audit import AuditLogger
from src.decision_tree import (
    Ruleset,
    Session,
    branch_completeness,
    load_ruleset,
    merge_rulesets,
    resolve_next,
)
from src.other_law import OtherLawFlag, active_flags, load_flags
from src.output import render, template_for_role
from src.roles import ROLES, Role, get_role
from src.taxonomy import Taxonomy, load_all_taxonomies

CONTENT_DIR = Path(__file__).resolve().parent.parent / "content"


@dataclass
class CaseBundle:
    """A merged ruleset + scenario for a specific case."""

    case_id: str
    ruleset: Ruleset
    scenario: dict


def load_case(
    case_id: str,
    outer_ruleset_path: Path = CONTENT_DIR / "rules" / "outer_layer.yaml",
    inner_ruleset_path: Path | None = None,
    scenario_path: Path | None = None,
) -> CaseBundle:
    import yaml

    inner_ruleset_path = (
        inner_ruleset_path or CONTENT_DIR / "rules" / f"{case_id}.yaml"
    )
    scenario_path = scenario_path or CONTENT_DIR / "scenarios" / f"{case_id}.yaml"

    outer = load_ruleset(outer_ruleset_path)
    inner = load_ruleset(inner_ruleset_path)
    merged = merge_rulesets(outer, inner)
    errors = branch_completeness(merged)
    if errors:
        raise ValueError(
            "Rule completeness errors for case "
            + case_id
            + ":\n  - "
            + "\n  - ".join(errors)
        )
    with scenario_path.open("r", encoding="utf-8") as f:
        scenario = yaml.safe_load(f)
    return CaseBundle(case_id=case_id, ruleset=merged, scenario=scenario)


@dataclass
class EngineState:
    taxonomies: dict[str, Taxonomy]
    registry: ArtefactRegistry
    other_law_flags: list[OtherLawFlag]
    roles: tuple[Role, ...] = ROLES


def load_engine_state() -> EngineState:
    return EngineState(
        taxonomies=load_all_taxonomies(),
        registry=load_registry(),
        other_law_flags=load_flags(),
    )


# -- automatic-step execution ------------------------------------------------

def run_compute_step(step_data: dict, session: Session) -> None:
    """Execute a ``compute`` step. Applies declarative rules to state."""
    rules = step_data.get("rules", [])
    for rule in rules:
        when = rule.get("when") or {}
        when_any = rule.get("when_any") or {}
        if when and _match_all(when, session):
            _apply_emit(rule.get("emit", {}), session)
        if when_any and _match_any(when_any, session):
            _apply_emit(rule.get("emit", {}), session)

    if step_data.get("finalise_access"):
        include_explain = session.get("access_mode_include_explain", False)
        include_inspect = session.get("access_mode_include_inspect", False)
        if include_explain and include_inspect:
            mode = "both (inspect and explain)"
        elif include_explain:
            mode = "explain (walkthrough under confidentiality)"
        elif include_inspect:
            mode = "inspect"
        else:
            mode = "to be scoped"
        session.set("access_mode", mode)

    # Flat emit (no conditional) — used for pass-through seams.
    if "emit" in step_data and not rules:
        _apply_emit(step_data.get("emit", {}), session)


def _match_all(cond: dict, session: Session) -> bool:
    for key, expected in cond.items():
        actual = session.role if key == "role" else session.get(key)
        if actual != expected:
            return False
    return True


def _match_any(cond: dict, session: Session) -> bool:
    for key, expected in cond.items():
        actual = session.role if key == "role" else session.get(key)
        actual_set = set(actual) if isinstance(actual, list) else {actual}
        expected_set = set(expected) if isinstance(expected, list) else {expected}
        if actual_set.intersection(expected_set):
            return True
    return False


def _apply_emit(emit: dict, session: Session) -> None:
    for key, value in emit.items():
        session.set(key, value)


def run_artefact_lookup(
    step_data: dict,
    session: Session,
    engine: EngineState,
    case_id: str,
) -> list[ArtefactEntry]:
    types = session.get("artefact_types", []) or []
    surfaced = engine.registry.filter_for_case_and_types(case_id, types)
    session.set("surfaced_artefacts", [a.artefact_id for a in surfaced])
    return surfaced


def run_other_law_check(
    step_data: dict,
    session: Session,
    engine: EngineState,
    surfaced_artefacts: list[ArtefactEntry],
) -> list[OtherLawFlag]:
    flags = active_flags(
        system_types=session.get("system_types", []) or [],
        artefact_types=session.get("artefact_types", []) or [],
        surfaced_artefacts=surfaced_artefacts,
        flags=engine.other_law_flags,
    )
    session.set("other_law_flag_ids", [f.id for f in flags])
    return flags


def run_render_output(
    step_data: dict,
    session: Session,
    *,
    engine: EngineState,
    case: CaseBundle,
    surfaced_artefacts: list[ArtefactEntry],
    flags: list[OtherLawFlag],
    ai_assisted: bool = False,
    extra_context: dict | None = None,
) -> str:
    role = session.role
    assert role is not None, "role must be selected before rendering output"
    template_name = template_for_role(role)
    role_obj = get_role(role)

    system_types = [
        engine.taxonomies["system_types"].get(s).name
        for s in session.get("system_types", []) or []
    ]
    risk_types = [
        engine.taxonomies["risk_types"].get(r).name
        for r in session.get("risk_types", []) or []
    ]

    artefact_ctx = [
        {
            "artefact_name": a.artefact_name,
            "artefact_type": a.artefact_type,
            "proposed_access_method": ", ".join(a.typical_access_methods),
            "proportionality_notes": a.proportionality_notes,
            "evidentiary_value": a.evidentiary_value,
            "eph_overlap": "To confirm with EPH",
        }
        for a in surfaced_artefacts
    ]

    flag_ctx = [
        {"name": f.name, "guidance": f.guidance} for f in flags
    ]

    subcomponents_ids = session.get("warehouse_subcomponents", []) or []
    sub_patterns_ids = session.get("warehouse_sub_patterns", []) or []

    # Translate sub-component and sub-pattern ids to readable labels via the
    # case's inner ruleset options if present.
    def _label(step_id: str, option_id: str) -> str:
        try:
            step = case.ruleset.get(step_id)
        except KeyError:
            return option_id
        for opt in step.data.get("options", []) or []:
            if opt["id"] == option_id:
                return opt["name"]
        return option_id

    subcomponents = [_label("step_4a_case_branch", s) for s in subcomponents_ids]
    sub_patterns = [_label("step_4b_sub_patterns", s) for s in sub_patterns_ids]

    context = {
        "role": role_obj.name,
        "scenario_title": case.scenario.get("title", case.case_id),
        "system_types": system_types,
        "risk_types": risk_types,
        "artefacts": artefact_ctx,
        "other_law_flags": flag_ctx,
        "access_mode": session.get("access_mode", "to be scoped"),
        "notice_period_guidance": session.get(
            "notice_period_guidance", "To be confirmed."
        ),
        "warehouse_subcomponents": subcomponents,
        "warehouse_sub_patterns": sub_patterns,
        "grounds": case.scenario.get("eph_grounds", []),
        "suspected_contraventions": case.scenario.get(
            "suspected_contraventions", []
        ),
        "ai_assisted": ai_assisted,
    }
    if extra_context:
        context.update(extra_context)

    # PCBU defaults: translate surfaced artefacts into a starter 'provided'
    # list. The user edits in the UI.
    if role == "pcbu":
        context["artefacts_provided"] = [
            {
                "artefact_name": a.artefact_name,
                "artefact_type": a.artefact_type,
                "access_mode_offered": ", ".join(a.typical_access_methods),
                "form_of_disclosure": "To be confirmed",
                "requires_undertaking": (
                    "commercial_in_confidence" in a.sensitivity_flags
                    or "intellectual_property" in a.sensitivity_flags
                ),
            }
            for a in surfaced_artefacts
        ]
        context.setdefault("artefacts_withheld", [])

    return render(template_name, context)
