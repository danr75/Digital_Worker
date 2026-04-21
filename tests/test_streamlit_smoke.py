"""Streamlit app smoke test.

Uses st.testing.v1.AppTest to render the app and walk through the full
flow as an EPH, asserting the output document appears.
"""

from __future__ import annotations

import pytest

pytest.importorskip("streamlit")

from streamlit.testing.v1 import AppTest


def test_app_boots_and_eph_flow_produces_output(tmp_path, monkeypatch):
    # Write audit logs to tmp so the test is hermetic.
    monkeypatch.setenv("HOME", str(tmp_path))
    at = AppTest.from_file("app.py", default_timeout=15)
    at.run()
    assert not at.exception, at.exception

    def click_button_containing(at_obj, label_fragment: str) -> bool:
        for b in at_obj.button:
            if label_fragment in b.label:
                b.click()
                return True
        return False

    def confirm_selection(at_obj, values):
        at_obj.multiselect[0].set_value(values)
        at_obj.run()
        assert not at_obj.exception, at_obj.exception
        clicked = click_button_containing(at_obj, "Confirm selection")
        assert clicked, "Confirm selection button not found"
        at_obj.run()
        assert not at_obj.exception, at_obj.exception

    # Step 1: select EPH role (radio is conditional — set value, run, then
    # click the button that now exists).
    at.radio[0].set_value("eph")
    at.run()
    assert not at.exception, at.exception
    assert click_button_containing(at, "Confirm role"), "Confirm role button absent"
    at.run()
    assert not at.exception, at.exception

    # Steps 2 through 4b.
    confirm_selection(at, ["predictive_ml", "rule_based"])
    confirm_selection(
        at,
        [
            "unreasonable_workloads",
            "unreasonable_monitoring",
            "unlawful_discrimination",
        ],
    )
    confirm_selection(
        at,
        [
            "code_and_logic",
            "performance_metrics",
            "records",
            "data_logs",
            "audit_trails",
            "training_data",
            "human_oversight",
        ],
    )
    confirm_selection(at, ["pick_rate_algorithm", "supervisor_dashboard"])
    confirm_selection(at, ["pace_forcing_countdown_timer"])

    # The app should now have run all automatic steps and rendered an output.
    # The rendered output is st.markdown — search for the notice heading.
    all_md = " ".join(
        getattr(m, "value", "") or getattr(m, "body", "") or ""
        for m in at.markdown
    )
    assert "Notice under s 118(1)(a1)" in all_md, (
        "expected rendered EPH notice in markdown output"
    )
    assert "Disclaimer" in all_md
