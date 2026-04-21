from src.artefact_registry import load_registry
from src.taxonomy import load_all_taxonomies


def test_registry_loads_and_has_warehouse_entries():
    reg = load_registry()
    ids = reg.all_ids()
    assert len(ids) >= 15, f"expected 15+ warehouse entries, got {len(ids)}"
    assert len(ids) <= 40
    wh = reg.filter_by_case("warehouse_pick_rate")
    assert len(wh) == len(ids)


def test_registry_artefact_types_are_valid():
    reg = load_registry()
    tx = load_all_taxonomies()
    valid_types = set(tx["artefact_types"].ids())
    for e in reg.entries:
        assert e.artefact_type in valid_types, (
            f"{e.artefact_id} has invalid artefact_type {e.artefact_type}"
        )


def test_registry_related_risks_are_valid():
    reg = load_registry()
    tx = load_all_taxonomies()
    valid_risks = set(tx["risk_types"].ids())
    for e in reg.entries:
        for r in e.related_risks:
            assert r in valid_risks, (
                f"{e.artefact_id} references unknown risk {r}"
            )


def test_registry_filter_by_types():
    reg = load_registry()
    logs = reg.filter_by_types(["data_logs"])
    assert logs
    for e in logs:
        assert e.artefact_type == "data_logs"
