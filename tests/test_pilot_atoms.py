"""T1.1 acceptance: every pilot atom is schema-valid, span-verified against its official PDF page (the PDF must be
present in data/raw/), its MoH values parse back from the span, its status is recomputed by code, foreign values
carry url + fetch date, and no clinician-only field is filled."""
import json

import pytest

from vnsoc.extract.verify_span import drug_tables, verify_atom
from vnsoc.match.decoys import check_decoy, finalize
from vnsoc.paths import paths
from vnsoc.schemas import Atom

F = paths().root / "data" / "interim" / "pilot_atoms.jsonl"
ATOMS = [json.loads(x) for x in F.read_text(encoding="utf-8").splitlines() if x.strip()] if F.exists() else []
SYN, COMBOS = drug_tables()


def test_file_present_and_sized():
    assert F.exists(), "chưa có data/interim/pilot_atoms.jsonl (chạy vnsoc.extract.pilot_merge)"
    assert len(ATOMS) >= 30 and sum(a["conflict_status"] == "conflict" for a in ATOMS) >= 12
    assert len({a["atom_id"] for a in ATOMS}) == len(ATOMS)


@pytest.mark.parametrize("atom", ATOMS, ids=[a["atom_id"] for a in ATOMS])
def test_atom(atom):
    Atom.model_validate(atom)
    assert atom["pilot"] and atom["span_verified"]
    r = verify_atom(atom, synonyms=SYN, combos=COMBOS)
    assert r["pdf_exists"], r["reason"]
    assert r["ok"], r["reason"]
    fin = finalize(atom)
    assert (fin["conflict_status"], fin["tolerance"]) == (atom["conflict_status"], atom["tolerance"])
    assert all(f.get("url") and f.get("fetched_at") for f in atom.get("foreign") or [])
    assert not any(atom.get(k) is not None for k in ("moh_lags_evidence", "clinical_harm", "clinician_confirmed"))
    assert check_decoy(atom) == []
