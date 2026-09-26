"""Design counts come from the seed table / pilot atoms, never typed by hand."""
from vnsoc.analysis.design_counts import pilot_counts, seed_counts


def test_seed_counts_on_real_seed():
    import yaml

    from vnsoc.paths import paths

    seed = yaml.safe_load((paths().root / "data" / "seed" / "seed_conflicts.yaml").read_text(encoding="utf-8"))
    c = seed_counts(seed)
    assert c["seed_rows"] == 25
    assert c["seed_conflict_rows"] == 20          # excludes removed (12, 14), no_counterpart (3), unverified (21), drift (22)
    assert c["seed_version_drift_pairs"] == 3 and c["seed_concordant_topics"] == 9
    assert 0 < c["seed_us_only_rows"] < c["seed_conflict_rows"]


def test_pilot_counts_only_verified():
    atoms = [
        {"guideline": "2760/2023", "span_verified": True, "conflict_status": "conflict", "conflict_family": "f1",
         "seed_row": 1, "foreign": [{"system": "WHO_global"}], "superseded": []},
        {"guideline": "2760/2023", "span_verified": True, "conflict_status": "concordant", "foreign": [{"system": "US"}],
         "superseded": [{"guideline": "3705/2019"}]},
        {"guideline": "1740/2026", "span_verified": False, "conflict_status": "conflict", "conflict_family": "f2"},
    ]
    c = pilot_counts(atoms)
    assert (c["pdf_atoms"], c["pdf_conflicts"], c["pdf_concordant"], c["pdf_version_drift"]) == (2, 1, 1, 1)
    assert c["pdf_guidelines"] == 1 and c["pdf_conflict_families"] == 1 and c["pdf_foreign_systems"] == 2
