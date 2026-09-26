"""Main-study atom merge: pilot atoms and atoms outside the corpus are rejected; a verified atom is kept."""
import json
from pathlib import Path

import pytest

from vnsoc.extract import atoms_merge


def _pilot_atom(aid):
    f = Path("data/interim/pilot_atoms.jsonl")
    if not f.exists() or not Path("data/raw").exists():
        pytest.skip("không có mẩu thí điểm/PDF")
    return next(json.loads(x) for x in f.read_text(encoding="utf-8").splitlines() if f'"{aid}"' in x)


def test_check_rules():
    from vnsoc.extract.verify_span import drug_tables

    syn, combos = drug_tables()
    a = dict(_pilot_atom("P-dengue-01"), atom_id="A-2760_2023-001", pilot=False)
    assert atoms_merge.check(a, syn, combos, set()) == []                     # corpus not selected yet: allowed
    assert atoms_merge.check(a, syn, combos, {a["guideline"]}) == []
    assert any("không thuộc kho" in p for p in atoms_merge.check(a, syn, combos, {"9999/2026"}))
    assert any("thí điểm" in p for p in atoms_merge.check(dict(a, pilot=True), syn, combos, set()))


def test_merge_writes_atoms_and_rejects(tmp_path):
    a = dict(_pilot_atom("P-dengue-01"), atom_id="A-2760_2023-001", pilot=False)
    parts = tmp_path / "parts"
    parts.mkdir()
    (parts / "2760_2023.jsonl").write_text(json.dumps(a, ensure_ascii=False) + "\n"
                                           + json.dumps(dict(a, atom_id="A-x", pilot=True), ensure_ascii=False) + "\n",
                                           encoding="utf-8")
    out = tmp_path / "atoms.jsonl"
    assert atoms_merge.main(["--parts", str(parts), "--out", str(out)]) == 0
    kept = [json.loads(x) for x in out.read_text(encoding="utf-8").splitlines() if x.strip()]
    rej = [json.loads(x) for x in (tmp_path / "atoms_rejects.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
    assert [k["atom_id"] for k in kept] == ["A-2760_2023-001"] and rej[0]["atom_id"] == "A-x"
    row = atoms_merge.audit_rows(kept, {})[0]
    assert row["page"] == a["page"] and row["span"] == a["span"] and "a_verbatim" not in row   # verdicts left empty
