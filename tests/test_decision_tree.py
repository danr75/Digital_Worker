from pathlib import Path

from src.decision_tree import (
    branch_completeness,
    load_ruleset,
    merge_rulesets,
    resolve_next,
    Session,
)
from src.engine import load_case

CONTENT_DIR = Path(__file__).resolve().parent.parent / "content"


def test_outer_ruleset_loads():
    outer = load_ruleset(CONTENT_DIR / "rules" / "outer_layer.yaml")
    assert outer.entry_step == "step_1_role"
    assert "step_9_output" in outer.step_ids()


def test_outer_branch_completeness():
    outer = load_ruleset(CONTENT_DIR / "rules" / "outer_layer.yaml")
    errs = branch_completeness(outer)
    assert errs == [], errs


def test_merged_warehouse_branch_completeness():
    case = load_case("warehouse_pick_rate")
    errs = branch_completeness(case.ruleset)
    assert errs == [], errs


def test_warehouse_inner_overrides_seam():
    case = load_case("warehouse_pick_rate")
    seam = case.ruleset.get("step_4a_case_branch")
    # Inner layer replaces the compute pass-through with a multi_choice step.
    assert seam.kind == "multi_choice"


def test_role_branching_in_step_6():
    case = load_case("warehouse_pick_rate")
    step = case.ruleset.get("step_6_notice")
    assert step.kind == "compute"
    # rules include per-role emissions
    role_ids = [r.get("when", {}).get("role") for r in step.data["rules"]]
    assert {"eph", "pcbu", "hsr", "inspector"} <= set(role_ids)


def test_resolve_next_string_and_branches():
    case = load_case("warehouse_pick_rate")
    step = case.ruleset.get("step_2_system")
    session = Session()
    assert resolve_next(step, session) == "step_3_risks"
