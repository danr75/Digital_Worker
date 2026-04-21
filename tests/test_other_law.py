from src.artefact_registry import load_registry
from src.other_law import active_flags, load_flags


def test_flags_load():
    flags = load_flags()
    ids = [f.id for f in flags]
    assert {
        "privacy_act",
        "ppipa",
        "hripa",
        "workplace_surveillance_act",
        "fair_work_act",
        "commonwealth_override",
        "legal_professional_privilege",
        "commercial_in_confidence",
        "cross_border_data",
    } <= set(ids)


def test_flags_trigger_on_records_and_location_data():
    flags = load_flags()
    reg = load_registry()
    surfaced = reg.filter_for_case_and_types(
        "warehouse_pick_rate", ["data_logs", "records"]
    )
    assert surfaced
    active = active_flags(
        system_types=["predictive_ml"],
        artefact_types=["data_logs", "records"],
        surfaced_artefacts=surfaced,
        flags=flags,
    )
    active_ids = {f.id for f in active}
    assert "privacy_act" in active_ids
    # Workplace Surveillance Act should fire via data_logs or the
    # workplace_surveillance_act sensitivity on location-tracking artefacts.
    assert "workplace_surveillance_act" in active_ids


def test_flags_trigger_on_platform_system_type():
    flags = load_flags()
    active = active_flags(
        system_types=["online_platform"],
        artefact_types=[],
        surfaced_artefacts=[],
        flags=flags,
    )
    ids = {f.id for f in active}
    assert "fair_work_act" in ids
    assert "commonwealth_override" in ids
