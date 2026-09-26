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


# ---------------------------------------------------------------- CLI of the merge (--only / --out / --no-checklist)
def _mini(aid: str, guideline: str, vn: float, foreign: list[dict], decoy: list[dict], unit: str) -> dict:
    """Minimal schema-valid pilot atom (TEST FIXTURE, not data)."""
    return {"atom_id": aid, "guideline": guideline, "section": "s", "page": 1, "span": "x", "disease": "d",
            "condition": "c", "population": {"age": "người lớn"}, "slot_type": "dose", "intervention": "i",
            "value_kind": "num", "unit": unit, "vn": [{"lo": vn, "hi": vn}], "pilot": True, "decoy": decoy,
            "foreign": [{"system": "US", "source": "src", "version_date": "2020", "url": "https://example.org",
                         "fetched_at": "2026-09-01", "values": foreign}]}


@pytest.fixture
def mini_root(tmp_path, monkeypatch):
    from vnsoc.extract import pilot_merge as pm
    from vnsoc.match import sources

    d = tmp_path / "data" / "interim" / "pilot"
    d.mkdir(parents=True)
    # a: a hand-set decoy that differs from the rule decoy (20–25) is replaced
    a = _mini("A-1", "1/2020", 15, [{"lo": 5, "hi": 10}], [{"lo": 30, "hi": 30}], "ml/kg/h")
    # b: no rule decoy is valid (10 vs 20 mg); a hand-set decoy (40 mg) that would pass check_decoy is NOT kept
    b = _mini("B-1", "5904/2019__9e6bbe13", 10, [{"lo": 20, "hi": 20}], [{"lo": 40, "hi": 40}], "mg")
    (d / "a.jsonl").write_text(json.dumps(a, ensure_ascii=False) + "\n", encoding="utf-8")
    (d / "b.jsonl").write_text(json.dumps(b, ensure_ascii=False) + "\n", encoding="utf-8")
    monkeypatch.setenv("VNSOC_ROOT", str(tmp_path))
    monkeypatch.setattr(pm, "drug_tables", lambda root=None: ({}, {}))
    monkeypatch.setattr(pm, "verify_atom", lambda *args, **kw: {"ok": True})     # no PDF in the fixture root
    monkeypatch.setattr(pm, "source_warnings", lambda *args, **kw: [])
    monkeypatch.setattr(sources, "block_hashes", lambda root=None: set())
    return tmp_path


def _read(p):
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]


def _shared(root):
    return {"atoms": root / "data" / "interim" / "pilot_atoms.jsonl",
            "rejects": root / "data" / "interim" / "pilot_merge_rejects.jsonl",
            "pdf_choice": root / "data" / "interim" / "pdf_choice.json",
            "checklist": root / "state" / "gates" / "HG1.2_checklist.md"}


def test_merge_only_one_topic_writes_no_shared_file(mini_root):
    from vnsoc.extract.pilot_merge import main

    out = mini_root / "scratch" / "a_sim.jsonl"
    assert main(["--only", "a", "--out", str(out)]) == 0
    got = _read(out)
    assert [x["atom_id"] for x in got] == ["A-1"]
    assert got[0]["decoy"][0]["lo"] == 20 and got[0]["decoy_rule"] == "mirror_arith" and got[0]["roundness_ok"]
    assert got[0]["extraction"]["decoy_rule"] == "mirror_arith (đặt lại khi gộp)" and got[0]["tolerance"] == 2.5
    assert got[0]["extraction"]["decoy_rounding"] == "none"
    assert (mini_root / "scratch" / "a_sim_rejects.jsonl").exists()
    assert not any(p.exists() for p in _shared(mini_root).values())
    with pytest.raises(SystemExit):
        main(["--only", "a"])                                       # would overwrite pilot_atoms.jsonl with one topic
    with pytest.raises(SystemExit):
        main(["--only", "nope", "--out", str(out)])


def test_merge_no_checklist_all_topics(mini_root):
    from vnsoc.extract.pilot_merge import main

    out = mini_root / "scratch" / "all.jsonl"
    assert main(["--out", str(out), "--no-checklist"]) == 0
    got = {x["atom_id"]: x for x in _read(out)}
    assert set(got) == {"A-1", "B-1"} and got["B-1"]["guideline"] == "5904/2019"
    assert got["B-1"]["decoy"] == [] and got["B-1"]["decoy_rule"] is None
    assert got["B-1"]["extraction"]["decoy_rule"].startswith("none — ")
    assert got["B-1"]["conflict_status"] == "conflict"             # kept, without decoy (excluded from H1/H2)
    assert not any(p.exists() for p in _shared(mini_root).values())


def test_enforce_decoy_rule_keeps_the_rule_name_and_records_the_rounding():
    # review 2026-09-26 (blocker): 'mirror_arith+round' dropped rounded arithmetic mirrors from the registered S2 set
    # (decoy_rule == "mirror_arith"); the rounding now goes to extraction.decoy_rounding
    from vnsoc.extract.pilot_merge import enforce_decoy_rule

    a = _mini("R-1", "1/2020", 250, [{"lo": 150, "hi": 150}], [], "ug")
    a["vn"].append({"lo": 200, "hi": 333.3333333333333})
    a["extraction"] = {"decoy_rounding": "stale"}
    got = enforce_decoy_rule(a)
    assert got["decoy"][0]["lo"] == 390 and got["decoy_rule"] == "mirror_arith"
    assert got["extraction"]["decoy_rounding"] == "step 10" and got["roundness_ok"] is False
    # no valid rule decoy: no rounding recorded, a stale one is removed
    b = enforce_decoy_rule(dict(_mini("R-2", "1/2020", 10, [{"lo": 20, "hi": 20}], [], "mg"),
                                extraction={"decoy_rounding": "stale"}))
    assert b["decoy"] == [] and "decoy_rounding" not in b["extraction"]
    # a hand-set num decoy on an atom with tol0 = 0 (it would set the tolerance itself) is dropped
    c = _mini("R-3", "1/2020", 10, [{"lo": 10, "hi": 10}], [{"lo": 30, "hi": 30}], "mg")
    got = finalize(enforce_decoy_rule(c))
    assert got["decoy"] == [] and got["tolerance"] == 0.0 and got["conflict_status"] == "concordant"


def test_merge_default_keeps_shared_outputs(mini_root):
    from vnsoc.extract.pilot_merge import main

    assert main([]) == 0
    sh = _shared(mini_root)
    assert all(p.exists() for p in sh.values())
    assert len(_read(sh["atoms"])) == 2 and "A-1" in sh["checklist"].read_text(encoding="utf-8")
    assert json.loads(sh["pdf_choice"].read_text(encoding="utf-8"))["5904/2019"]["file"] == "5904_2019__9e6bbe13.pdf"
