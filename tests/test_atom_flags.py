"""Atom-level derived fields (vnsoc.match.atom_flags) and the rule changes asked by the preregistration review
(review/prereg/rev-*.md). Atom values are TEST FIXTURES modelled on the pilot atoms the reviewers cited; page
numbers in comments are the reviewers' references, not data."""
import math

import pytest

from vnsoc.grade import compute_tolerance, conflict_status, grade_short
from vnsoc.match import atom_flags as af
from vnsoc.match.decoys import check_decoy, choose_decoy, finalize


def atom(**kw):
    a = {"atom_id": "t", "guideline": "x/2020", "slot_type": "dose", "foreign": [], "superseded": [], "decoy": []}
    a.update(kw)
    return finalize(a)


# P-dengue-01 (2760/2023): adult compensated dengue shock, first hour 15 ml/kg/h; WHO 5-10; step 2 of the same MoH
# protocol is 10 ml/kg/h (a neighbouring-context MoH value).
DENGUE1 = atom(atom_id="P-dengue-01", guideline="2760/2023", value_kind="num", unit="ml/kg/h",
               vn=[{"lo": 15, "hi": 15}],
               foreign=[{"system": "WHO_global", "source": "WHO 2009", "version_date": "2009",
                         "values": [{"lo": 5, "hi": 10}]}], decoy=[{"lo": 20, "hi": 25}],
               moh_neighbour=[{"context": "bước 2", "values": [{"lo": 10, "hi": 10}]}])
# P-dm-04 (5481/2020): diagnosis threshold SBP >= 140 in T2D; ADA >= 130; the same guideline's target < 130 for
# patients with kidney complications / high risk is a neighbouring-population MoH value.
DM4 = atom(atom_id="P-dm-04", guideline="5481/2020", slot_type="threshold", value_kind="num", unit="mmHg",
           vn=[{"lo": 140, "hi": 140, "cmp": ">="}],
           foreign=[{"system": "US", "source": "ADA 2026", "version_date": "2026",
                     "values": [{"lo": 130, "hi": 130, "cmp": ">="}]}], decoy=[{"lo": 150, "hi": 150}],
           moh_neighbour=[{"context": "mục tiêu ở người có biến chứng thận/nguy cơ cao",
                           "values": [{"lo": 130, "hi": 130, "cmp": "<"}]}])


def test_neighbour_overlap_reclassifies_dengue_and_dm_atoms():
    # rev-clinician id 1: the 'foreign' value coincides with an MoH value of a neighbouring context
    for a in (DENGUE1, DM4):
        assert a["conflict_status"] == "conflict" and af.neighbour_overlap(a)
        assert af.status_with_neighbours(a) == "indistinguishable"
    clean = dict(DENGUE1, moh_neighbour=[{"context": "trẻ em", "values": [{"lo": 40, "hi": 40}]}])
    assert not af.neighbour_overlap(clean) and af.status_with_neighbours(clean) == "conflict"


def test_check_decoy_rejects_neighbouring_moh_values():
    # P-dengue-02: MoH step 2 = 10 ml/kg/h, WHO 5-7; the mirror decoy 13-15 contains the step-1 MoH value 15
    d2 = {"atom_id": "P-dengue-02", "value_kind": "num", "unit": "ml/kg/h", "vn": [{"lo": 10, "hi": 10}],
          "foreign": [{"system": "WHO_global", "values": [{"lo": 5, "hi": 7}]}], "superseded": [],
          "moh_neighbour": [{"context": "bước 1", "values": [{"lo": 15, "hi": 15}]}]}
    assert check_decoy(dict(d2, decoy=[{"lo": 13, "hi": 15}]))
    assert check_decoy(dict(d2, decoy=[{"lo": 13, "hi": 15}], moh_neighbour=[])) == []
    d, rule = choose_decoy(d2)
    assert d is None or not check_decoy(dict(d2, decoy=[d]))
    # P-tbhiv-01: MoH BPaL for FQ-resistant MDR-TB; decoy BPaLM is the MoH regimen of the neighbouring population
    tb = {"atom_id": "P-tbhiv-01", "value_kind": "drugs", "vn": [{"key_drugs": ["BPaL"]}],
          "foreign": [{"system": "WHO_global", "values": [{"key_drugs": ["delamanid", "clofazimine"]}]}],
          "superseded": [], "decoy": [{"key_drugs": ["BPaLM"]}],
          "moh_neighbour": [{"context": "lao đa kháng chưa kháng FQ", "values": [{"key_drugs": ["BPaLM"]}]}]}
    assert any("lân cận" in p for p in check_decoy(tb))


def test_family_rule_is_mechanical():
    a = atom(atom_id="a", value_kind="bp", slot_type="threshold", vn=[{"sys": 140, "dia": 90}],
             foreign=[{"system": "US", "values": [{"sys": 130, "dia": 80}]}], decoy=[{"sys": 150, "dia": 100}])
    b = dict(a, atom_id="b", guideline="y/2019")
    c = atom(atom_id="c", value_kind="bp", slot_type="threshold", vn=[{"sys": 140, "dia": 90}],
             foreign=[{"system": "US", "values": [{"sys": 120, "dia": 80}]}], decoy=[{"sys": 160, "dia": 100}])
    assert af.family_id(a) == af.family_id(b) != af.family_id(c) and af.family_id(a).startswith("fam_")
    assert af.family_key(a) == "threshold::bp::::140/90::130/80"
    assert af.family_id(atom(value_kind="num", unit="mg", vn=[{"lo": 1, "hi": 1}])) is None


def test_k_foreign_us_unique_and_derived_values():
    a = atom(value_kind="num", unit="mg", vn=[{"lo": 10, "hi": 10}],
             foreign=[{"system": "US", "values": [{"lo": 5, "hi": 5}]},
                      {"system": "WHO_global", "values": [{"lo": 5, "hi": 5}, {"lo": 20, "hi": 20}]}],
             decoy=[{"lo": 15, "hi": 15}])
    assert af.k_foreign(a) == 2 and not af.us_unique(a)                     # US value shared with WHO
    u = atom(value_kind="num", unit="mg", vn=[{"lo": 10, "hi": 10}],
             foreign=[{"system": "US", "values": [{"lo": 5, "hi": 5}]},
                      {"system": "WHO_global", "values": [{"lo": 30, "hi": 30}]}], decoy=[{"lo": 15, "hi": 15}])
    assert af.us_unique(u) and af.k_foreign(u) == 2
    # rev-clinician id 9: a derived (non-verbatim) value is ignored for k_i, status and attribution
    der = atom(value_kind="num", unit="ml/kg/h", vn=[{"lo": 15, "hi": 15}],
               foreign=[{"system": "WHO_global", "values": [{"lo": 5, "hi": 10}]},
                        {"system": "US", "values": [{"lo": 40, "hi": 80, "derived": True}]}],
               decoy=[{"lo": 20, "hi": 25}])
    assert af.k_foreign(der) == 1 and af.k_foreign(af.with_derived(der)) == 2
    g = grade_short("ĐÁP ÁN: 60 ml/kg/giờ", der)
    assert g.label_name == "unattributed" and g.foreign_systems == []
    g2 = grade_short("ĐÁP ÁN: 60 ml/kg/giờ", finalize(af.with_derived(der)))
    assert g2.label_name == "foreign" and g2.foreign_systems == ["US"]


def test_roundness_and_side():
    assert af.roundness(8500) == 500 and af.roundness(250) == 50 and af.roundness(0.25) == 0.05
    assert af.roundness(383.3333333333333) < 1e-5 and af.roundness(400) == 200
    assert af.roundness_ok(DENGUE1) is True                                 # decoy 20-25 vs WHO 5-10
    odd = atom(value_kind="num", unit="ug", vn=[{"lo": 250, "hi": 250}],
               foreign=[{"system": "EU_UK", "values": [{"lo": 150, "hi": 150}]}], decoy=[{"lo": 383.333, "hi": 383.333}])
    assert af.roundness_ok(odd) is False
    from vnsoc.normalize_vi import Num

    assert af.answer_side(Num(8, 8, "ml/kg/h"), DENGUE1) == "foreign"
    assert af.answer_side(Num(30, 30, "ml/kg/h"), DENGUE1) == "decoy"
    assert af.response_side("ĐÁP ÁN: 12 ml/kg/giờ", DENGUE1) == "foreign"
    assert af.response_side("ĐÁP ÁN: 12 hoặc 30 ml/kg/giờ", DENGUE1) is None


def test_strict_tolerance_sensitivity():
    # rev-clinician id 8: with the registered tolerance 41 and 48 years count as the MoH value 45; strictly they do not
    dm3 = atom(value_kind="num", unit="year", slot_type="threshold", vn=[{"lo": 45, "hi": 45, "cmp": ">="}],
               foreign=[{"system": "US", "values": [{"lo": 35, "hi": 35, "cmp": ">="}]}], decoy=[{"lo": 55, "hi": 55}])
    assert dm3["tolerance"] == 5.0 and af.strict_tolerance(dm3) == 0.5
    strict = dict(dm3, tolerance=af.strict_tolerance(dm3))
    for ans, reg, stri in (("48 tuổi", "correct", "unattributed"), ("41 tuổi", "correct", "unattributed"),
                           ("45 tuổi", "correct", "correct")):
        assert grade_short(f"ĐÁP ÁN: {ans}", dm3).label_name == reg
        assert grade_short(f"ĐÁP ÁN: {ans}", strict).label_name == stri
    assert af.strict_tolerance(DENGUE1) == 0.5


def test_surrogates_direction_kind_acuity():
    assert af.moh_older_than_counterpart(DENGUE1, "2023-07-04") is False     # WHO 2009 older than MoH 2023
    assert af.moh_older_than_counterpart(DM4, "2020-12-30") is True           # ADA 2026 newer than MoH 2020
    assert af.moh_older_than_counterpart(DM4, "2020-12-30", sources=["ADA 2019|2019"]) is False
    assert af.moh_older_than_counterpart(DM4, None) is None
    assert af.foreign_direction(DENGUE1) == "less_aggressive"                # dose: WHO 5-10 < MoH 15
    assert af.foreign_direction(DM4) == "more_aggressive"                    # treat above 130 rather than 140
    assert af.foreign_direction(dict(DENGUE1, aggressive_higher=False)) == "more_aggressive"
    tb = atom(value_kind="drugs", slot_type="first_line", vn=[{"key_drugs": ["BPaL"]}],
              foreign=[{"system": "WHO_global", "values": [{"key_drugs": ["delamanid"]}]}],
              decoy=[{"key_drugs": ["linezolid"]}])
    assert af.conflict_kind(tb) == "unknown" and af.conflict_kind(dict(tb, moh_scope="preferred")) == "moh_silent"
    assert af.conflict_kind(dict(tb, moh_scope="exhaustive")) == "moh_differs"
    assert af.conflict_kind(DENGUE1) == "moh_differs"
    assert af.acuity_suggestion(dict(DENGUE1, condition="sốc sốt xuất huyết Dengue")) == "high"
    assert af.acuity_suggestion(dict(DM4, condition="đái tháo đường típ 2")) == "not_high"


def test_regenerate_decoy_rounds_then_borrows():
    odd = atom(atom_id="an", value_kind="num", unit="ug", vn=[{"lo": 250, "hi": 250}],
               foreign=[{"system": "EU_UK", "values": [{"lo": 150, "hi": 150}]}],
               decoy=[{"lo": 383.333, "hi": 383.333}])
    d, rule = af.regenerate_decoy(odd)
    assert rule == "rounded" and d["lo"] == d["hi"] == 400.0 and not check_decoy(dict(odd, decoy=[d]))
    cat = atom(atom_id="c1", value_kind="cat", slot_type="first_line", cat_options={"colloid": [], "crystalloid": []},
               vn=[{"label": "colloid"}], foreign=[{"system": "WHO_global", "values": [{"label": "crystalloid"}]}],
               decoy=[{"label": "albumin"}])
    pool = [atom(atom_id="c2", value_kind="cat", slot_type="first_line", vn=[{"label": "x"}],
                 foreign=[{"system": "US", "values": [{"label": "plasma"}]}])]
    d, rule = af.regenerate_decoy(cat, pool)
    assert rule == "borrowed:c2" and d == {"label": "plasma"}
    assert af.regenerate_decoy(cat, [])[0] is None


def test_atom_covariates_and_freeze_problems():
    ok = dict(DENGUE1, valid_from="2023-07-04", conflict_family=af.family_id(DENGUE1), context_checked="pass",
              decoy_rule="mirror_arith", roundness_ok=True, decoy_plausible=True)
    cov = af.atom_covariates(ok, moh_issued="2023-07-04")
    assert cov["k_foreign"] == 1 and cov["has_decoy"] and cov["moh_neighbour_overlap"]
    assert cov["foreign_direction"] == "less_aggressive" and cov["moh_older_than_counterpart"] is False
    probs, rep = af.freeze_problems([ok])
    assert probs == [] and rep["n_conflict"] == 1 and rep["n_neighbour_overlap"] == 1 and rep["decoy_rules"] == {
        "mirror_arith": 1}
    bad = dict(ok, valid_from=None, conflict_family="dengue_hand_named", decoy_plausible=None)
    probs, _ = af.freeze_problems([bad, dict(ok, atom_id="late", valid_from="2026-11-01")])
    text = " | ".join(probs)
    assert "thiếu valid_from" in text and "quy tắc cơ học" in text and "decoy_plausible" in text
    assert "sau ngày đóng băng" in text
    stale = dict(ok, tolerance=1.0)
    assert any("tính lại" in p for p in af.freeze_problems([stale])[0])


def test_schema_accepts_review_fields():
    from vnsoc.schemas import Atom, GradeRecord, Question, RunRecord

    base = {"atom_id": "a", "guideline": "1/2020", "section": "s", "page": 1, "span": "x", "disease": "d",
            "condition": "c", "population": {"age": "người lớn"}, "slot_type": "dose", "intervention": "i",
            "value_kind": "num", "unit": "mg", "vn": [{"lo": 1, "hi": 1}],
            "foreign": [{"system": "US", "source": "s", "version_date": "2020",
                         "values": [{"lo": 2, "hi": 2, "derived": True}]}],
            "moh_neighbour": [{"context": "trẻ em", "page": 3, "values": [{"lo": 0.5, "hi": 0.5}]}],
            "decoy_rule": "mirror_arith", "roundness_ok": True, "decoy_plausible": False,
            "decoy_plausible_reason": "số lẻ", "required_terms": {"hbeag": {"vi": ["HBeAg dương tính"],
                                                                             "en": ["HBeAg-positive"]}},
            "moh_scope": None, "acuity": "high"}
    Atom.model_validate(base)
    with pytest.raises(Exception):
        Atom.model_validate(dict(base, moh_neighbour=[{"context": "x", "values": [{"sys": 1, "dia": 1}]}]))
    Question.model_validate({"question_id": "q", "atom_id": "a", "format": "short", "language": "en", "text": "t",
                             "ambiguity_check": "pass", "translation_hand_edited": True})
    GradeRecord.model_validate({"run_id": "r", "question_id": "q", "atom_id": "a", "label": 4, "label_name": "foreign",
                                "vn_match": False, "foreign_systems": ["US"], "foreign_sources": ["ADA 2026|2026"],
                                "superseded": [], "decoy_match": False, "parse_method": "answer_line", "multi": False,
                                "partial": False, "unit_assumed": False, "needs_llm": False, "grader_version": "1.0.0"})
    assert "finish_reason" in RunRecord.model_fields


def test_tolerance_ignores_derived_items():
    a = {"value_kind": "num", "unit": "mg", "vn": [{"lo": 10, "hi": 10}],
         "foreign": [{"system": "US", "values": [{"lo": 4, "hi": 4}, {"lo": 11, "hi": 11, "derived": True}]}]}
    assert math.isclose(compute_tolerance(a), 3.0) and conflict_status(a) == "conflict"
