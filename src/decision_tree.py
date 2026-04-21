"""Decision-tree engine (spec §4).

Rules are authored in YAML so a lawyer or policy officer can review and
revise them without reading code. The engine is deterministic: given a step
and the session state, the next step is a pure function of the rules. LLMs
are not involved in any decision computed here.

Step kinds
----------
- ``role_selection`` — user selects a role (spec §2).
- ``multi_choice`` — user selects one or more values from a referenced
  taxonomy or an enumerated option list.
- ``single_choice`` — user selects exactly one value.
- ``free_text_with_tags`` — user supplies free text plus structured tags.
- ``compute`` — applies declarative rules to existing state to produce new
  state values (e.g. proportionate access mode). No user input.
- ``artefact_lookup`` — surfaces artefacts from the registry whose
  ``artefact_type`` intersects the user's selected artefact types for the
  active case.
- ``other_law_check`` — raises flags from the other-law module based on
  selected artefact types and system types.
- ``render_output`` — renders the output document via a Jinja2 template.
- ``end`` — terminal.

Branching
---------
``next`` may be a string (single next step id) or a list of conditional
branches of the form::

    next:
      - when: {role: eph}
        goto: step_5_eph
      - when: {role: pcbu}
        goto: step_5_pcbu
      - default: step_5_generic

Conditions match on session state by key. Lists in ``when`` are interpreted
as "any of these values is present in the state key" (set intersection).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

CONTENT_DIR = Path(__file__).resolve().parent.parent / "content"
RULES_DIR = CONTENT_DIR / "rules"

STEP_KINDS = {
    "role_selection",
    "multi_choice",
    "single_choice",
    "free_text_with_tags",
    "compute",
    "artefact_lookup",
    "other_law_check",
    "render_output",
    "end",
}

AUTOMATIC_KINDS = {
    "compute",
    "artefact_lookup",
    "other_law_check",
    "render_output",
    "end",
}


@dataclass(frozen=True)
class Step:
    id: str
    kind: str
    title: str
    data: dict[str, Any]

    @property
    def next(self) -> Any:
        return self.data.get("next")


@dataclass(frozen=True)
class Ruleset:
    ruleset_id: str
    version: int
    description: str
    steps: tuple[Step, ...]
    entry_step: str

    def get(self, step_id: str) -> Step:
        for step in self.steps:
            if step.id == step_id:
                return step
        raise KeyError(f"No step with id={step_id!r} in ruleset {self.ruleset_id}")

    def step_ids(self) -> list[str]:
        return [s.id for s in self.steps]


@dataclass
class Session:
    """Per-user traversal state. Holds collected answers and history."""

    role: str | None = None
    state: dict[str, Any] = field(default_factory=dict)
    history: list[str] = field(default_factory=list)
    emissions: list[dict[str, Any]] = field(default_factory=list)
    current_step_id: str | None = None

    def set(self, key: str, value: Any) -> None:
        self.state[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self.state.get(key, default)


def load_ruleset(path: Path) -> Ruleset:
    with path.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    steps: list[Step] = []
    for entry in raw["steps"]:
        kind = entry["kind"]
        if kind not in STEP_KINDS:
            raise ValueError(
                f"Unknown step kind {kind!r} in ruleset {raw['ruleset_id']}, "
                f"step {entry['id']}"
            )
        steps.append(
            Step(
                id=entry["id"],
                kind=kind,
                title=entry.get("title", entry["id"]),
                data=entry,
            )
        )
    return Ruleset(
        ruleset_id=raw["ruleset_id"],
        version=raw["version"],
        description=raw.get("description", ""),
        steps=tuple(steps),
        entry_step=raw.get("entry_step", steps[0].id),
    )


def merge_rulesets(outer: Ruleset, inner: Ruleset) -> Ruleset:
    """Merge an inner-layer case ruleset into the outer scaffolding.

    Inner rulesets may add new steps or override existing step data by id.
    This is how a new case (spec §12) plugs its branches into the outer
    decision tree without rewriting the scaffolding.
    """
    merged: dict[str, Step] = {s.id: s for s in outer.steps}
    for step in inner.steps:
        merged[step.id] = step
    return Ruleset(
        ruleset_id=f"{outer.ruleset_id}+{inner.ruleset_id}",
        version=outer.version,
        description=(
            f"{outer.description} | merged inner: {inner.description}"
        ),
        steps=tuple(merged.values()),
        entry_step=outer.entry_step,
    )


# -- branch resolution -------------------------------------------------------

def _condition_matches(cond: dict[str, Any], session: Session) -> bool:
    """Check whether all keys in ``cond`` are satisfied by ``session``.

    Scalar values match equality. Lists in the condition match as set
    intersection with the session value (which should be list-valued).
    """
    for key, expected in cond.items():
        actual = session.role if key == "role" else session.get(key)
        if isinstance(expected, list):
            actual_set = set(actual) if isinstance(actual, list) else {actual}
            if not actual_set.intersection(expected):
                return False
        else:
            if actual != expected:
                return False
    return True


def resolve_next(step: Step, session: Session) -> str | None:
    nxt = step.next
    if nxt is None:
        return None
    if isinstance(nxt, str):
        return nxt
    if isinstance(nxt, list):
        for branch in nxt:
            if "default" in branch:
                continue
            if "when" in branch and _condition_matches(branch["when"], session):
                return branch["goto"]
        for branch in nxt:
            if "default" in branch:
                return branch["default"]
        return None
    raise TypeError(f"Unsupported 'next' format: {nxt!r}")


# -- validation --------------------------------------------------------------

def branch_completeness(ruleset: Ruleset) -> list[str]:
    """Return a list of completeness errors, empty if all branches terminate.

    This implements the success-criterion check from spec §11:
    "Decision-tree traversal logs show no branch has a dead end or a missing
    rule."
    """
    errors: list[str] = []
    ids = set(ruleset.step_ids())
    for step in ruleset.steps:
        if step.kind == "end":
            continue
        nxt = step.next
        if nxt is None:
            errors.append(f"Step {step.id!r} has no 'next' and is not an end step.")
            continue
        if isinstance(nxt, str):
            if nxt not in ids:
                errors.append(f"Step {step.id!r} points to unknown step {nxt!r}.")
        elif isinstance(nxt, list):
            has_default = False
            for branch in nxt:
                if "default" in branch:
                    has_default = True
                    target = branch["default"]
                elif "goto" in branch:
                    target = branch["goto"]
                else:
                    errors.append(
                        f"Step {step.id!r} has a branch with neither 'goto' "
                        f"nor 'default': {branch!r}"
                    )
                    continue
                if target not in ids:
                    errors.append(
                        f"Step {step.id!r} branch targets unknown step "
                        f"{target!r}."
                    )
            if not has_default:
                errors.append(
                    f"Step {step.id!r} has branches but no 'default' — "
                    f"dead end risk."
                )
    return errors
