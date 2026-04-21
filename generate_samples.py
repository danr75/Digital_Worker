"""Generate sample outputs for every role into samples/.

Used to demonstrate the prototype without running Streamlit. Outputs are
populated with the warehouse pick-rate case content.
"""

from __future__ import annotations

from pathlib import Path

from src.decision_tree import Session
from src.engine import (
    load_case,
    load_engine_state,
    run_artefact_lookup,
    run_compute_step,
    run_other_law_check,
    run_render_output,
)


SAMPLES_DIR = Path(__file__).resolve().parent / "samples"


def _build_session(role: str) -> Session:
    return Session(
        role=role,
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
            "warehouse_subcomponents": [
                "pick_rate_algorithm",
                "location_tracking",
                "supervisor_dashboard",
            ],
            "warehouse_sub_patterns": [
                "pace_forcing_countdown_timer",
                "dynamically_rising_targets",
                "continuous_location_tracking",
                "disparate_impact_by_age_or_pregnancy",
                "unpublished_thresholds",
            ],
        },
    )


def _render_for_role(role: str) -> str:
    engine = load_engine_state()
    case = load_case("warehouse_pick_rate")
    session = _build_session(role)
    run_compute_step(case.ruleset.get("step_5_access").data, session)
    run_compute_step(case.ruleset.get("step_5a_finalise_access").data, session)
    run_compute_step(case.ruleset.get("step_6_notice").data, session)
    surfaced = run_artefact_lookup(
        case.ruleset.get("step_8_artefact_registry").data,
        session,
        engine,
        case.case_id,
    )
    flags = run_other_law_check(
        case.ruleset.get("step_7_limits").data, session, engine, surfaced
    )
    return run_render_output(
        case.ruleset.get("step_9_output").data,
        session,
        engine=engine,
        case=case,
        surfaced_artefacts=surfaced,
        flags=flags,
    )


def main() -> None:
    SAMPLES_DIR.mkdir(exist_ok=True)
    for role, filename in [
        ("eph", "eph_notice.md"),
        ("pcbu", "pcbu_response.md"),
        ("hsr", "hsr_brief.md"),
        ("inspector", "inspector_plan.md"),
    ]:
        out_path = SAMPLES_DIR / filename
        out_path.write_text(_render_for_role(role), encoding="utf-8")
        print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
