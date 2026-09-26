"""Seed-row outcomes come from atoms (code-computed status) or evidenced notes, never from the seed table itself."""
from vnsoc.analysis.seed_check import outcomes

SEED = {"rows": [{"row": 1, "topic": "a", "status": "confirmed"}, {"row": 2, "topic": "b", "status": "confirmed"},
                 {"row": 3, "topic": "c", "status": "confirmed"}, {"row": 4, "topic": "d", "status": "confirmed"},
                 {"row": 5, "topic": "e", "status": "removed"}]}


def test_outcomes():
    atoms = [{"atom_id": "P-x-01", "seed_row": 1, "conflict_status": "conflict"},
             {"atom_id": "P-x-02", "seed_row": 2, "conflict_status": "concordant"}]
    notes = [{"row": 3, "outcome": "no_official_text", "evidence": "r.md §4"}]
    o = {r["row"]: r["outcome"] for r in outcomes(SEED, atoms, notes)}
    assert o == {1: "confirmed_conflict", 2: "not_clean", 3: "blocked", 4: "not_checked", 5: "not_checked"}
