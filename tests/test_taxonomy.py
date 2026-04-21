from src.taxonomy import load_all_taxonomies


def test_all_three_taxonomies_present():
    tx = load_all_taxonomies()
    assert set(tx) >= {"system_types", "artefact_types", "risk_types"}


def test_system_types_contents():
    tx = load_all_taxonomies()
    ids = tx["system_types"].ids()
    assert {
        "rule_based",
        "predictive_ml",
        "generative_ai",
        "agentic_ai",
        "online_platform",
        "hybrid",
    } <= set(ids)


def test_artefact_types_contents():
    tx = load_all_taxonomies()
    ids = tx["artefact_types"].ids()
    assert {
        "code_and_logic",
        "performance_metrics",
        "records",
        "data_logs",
        "audit_trails",
        "training_data",
        "human_oversight",
    } == set(ids)


def test_risk_types_contents():
    tx = load_all_taxonomies()
    ids = tx["risk_types"].ids()
    assert {
        "unreasonable_workloads",
        "unreasonable_metrics",
        "unreasonable_monitoring",
        "unlawful_discrimination",
    } == set(ids)
