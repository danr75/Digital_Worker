"""End-to-end traversal of the decision tree for each role, asserting that
every path produces a rendered output and no branch dead-ends.
"""

from src.artefact_registry import load_registry
from src.decision_tree import Session, resolve_next
from src.engine import (
    load_case,
    load_engine_state,
    run_artefact_lookup,
    run_compute_step,
    run_other_law_check,
    run_render_output,
)


def _traverse(role: str) -> str:
    engine = load_engine_state()
    case = load_case("warehouse_pick_rate")
    session = Session(
        role=role,
        current_step_id=case.ruleset.entry_step,
        state={
            "system_types": ["predictive_ml", "rule_based"],
            "risk_types": [
                "unreasonable_workloads",
                "unreasonable_metrics",
                "unreasonable_monitoring",
                "unlawful_discrimination",
            ],
            "artefact_types": [
                "code_and_logic",
                "performance_metrics",
                "records",
                "data_logs",
                "audit_trails",
                "training_data",
                "human_oversight",
            ],
            "warehouse_subcomponents": ["pick_rate_algorithm", "supervisor_dashboard"],
            "warehouse_sub_patterns": [
                "pace_forcing_countdown_timer",
                "dynamically_rising_targets",
            ],
        },
    )
    surfaced = []
    flags = []
    output = None
    # Skip the role/multi-choice input steps — state is pre-seeded.
    input_kinds = {"role_selection", "multi_choice", "single_choice", "free_text_with_tags"}

    visited: list[str] = []
    session.current_step_id = "step_5_access"  # start past input steps
    guard = 0
    while session.current_step_id is not None and guard < 50:
        guard += 1
        step = case.ruleset.get(session.current_step_id)
        visited.append(step.id)
        if step.kind in input_kinds:
            # Shouldn't hit input steps in pre-seeded traversal
            session.current_step_id = resolve_next(step, session)
            continue
        if step.kind == "compute":
            run_compute_step(step.data, session)
        elif step.kind == "artefact_lookup":
            surfaced = run_artefact_lookup(step.data, session, engine, case.case_id)
        elif step.kind == "other_law_check":
            flags = run_other_law_check(step.data, session, engine, surfaced)
        elif step.kind == "render_output":
            output = run_render_output(
                step.data,
                session,
                engine=engine,
                case=case,
                surfaced_artefacts=surfaced,
                flags=flags,
            )
        elif step.kind == "end":
            break
        session.current_step_id = resolve_next(step, session)

    assert output is not None, f"no output for role={role}; visited={visited}"
    return output


def test_eph_end_to_end():
    out = _traverse("eph")
    assert "Notice under s 118(1)(a1)" in out
    assert "Disclaimer" in out
    assert "Pick-rate target-setting algorithm" in out


def test_pcbu_end_to_end():
    out = _traverse("pcbu")
    assert "Response to notice" in out
    assert "Disclaimer" in out


def test_hsr_end_to_end():
    out = _traverse("hsr")
    assert "Orientation brief" in out
    assert "Disclaimer" in out


def test_inspector_end_to_end():
    out = _traverse("inspector")
    assert "Proportionality check" in out
    assert "Disclaimer" in out


def test_access_mode_finalises_for_mixed_artefacts():
    engine = load_engine_state()
    case = load_case("warehouse_pick_rate")
    session = Session(
        role="eph",
        state={
            "artefact_types": ["code_and_logic", "data_logs"],
            "system_types": ["predictive_ml"],
            "risk_types": ["unreasonable_monitoring"],
        },
    )
    # step_5_access sets include_* flags, step_5a finalises.
    run_compute_step(case.ruleset.get("step_5_access").data, session)
    run_compute_step(case.ruleset.get("step_5a_finalise_access").data, session)
    assert "both" in session.get("access_mode", "")
