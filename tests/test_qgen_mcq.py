"""MCQ construction after the pilot review of 26/9/2026 (Q1-Q8): eligibility, slot 3 = superseded or filler (never a
second foreign value), multi-source role tokens, distinctness from the whole value set, rule filler, same comparator
on planted options, writer option texts for cat atoms with option QC, order 1 = rotation by two. Values are FIXTURES."""
import pytest

from vnsoc.grade import grade_mcq
from vnsoc.match.decoys import finalize
from vnsoc.qgen import build, mcq
from vnsoc.qgen.qc import (drug_fragment_issues, option_distinct_issues, option_hint_issues, option_issues,
                           option_script_issues, option_text_issues)


def _atom(**kw):
    base = {"atom_id": "T-x", "value_kind": "num", "unit": "%", "slot_type": "threshold", "foreign": [],
            "superseded": [], "decoy": []}
    return finalize({**base, **kw})


# conflict: MoH >= 9 %, US > 10 %, decoy 8 % (tolerance 0.5)
THR = _atom(atom_id="T-thr", vn=[{"lo": 9, "hi": 9, "cmp": ">="}],
            foreign=[{"system": "US", "values": [{"lo": 10, "hi": 10, "cmp": ">"}]}], decoy=[{"lo": 8, "hi": 8}])
# two conflicting foreign values, no superseded value (tolerance 1.5)
TWO_F = _atom(atom_id="T-2f", unit="month", slot_type="schedule", vn=[{"lo": 9, "hi": 9}],
              foreign=[{"system": "US", "values": [{"lo": 12, "hi": 15}]},
                       {"system": "EU_UK", "values": [{"lo": 24, "hi": 24}]}],
              decoy=[{"lo": 3, "hi": 6}])
# foreign value = superseded value (hbv-like; indistinguishable but a superseded value lies outside the MoH set)
SAME = _atom(atom_id="T-same", unit="U/L", vn=[{"lo": 30, "hi": 30}],
             foreign=[{"system": "US", "values": [{"lo": 35, "hi": 35}]},
                      {"system": "WHO_global", "values": [{"lo": 30, "hi": 30}]}],
             superseded=[{"guideline": "3310/2019", "values": [{"lo": 35, "hi": 35}]}], decoy=[{"lo": 26, "hi": 26}])
# no conflicting foreign value, superseded values outside the MoH set (version drift only)
DRIFT = _atom(atom_id="T-drift", unit="kPa", vn=[{"lo": 12.5, "hi": 12.5, "cmp": ">"}],
              foreign=[{"system": "WHO_global", "values": [{"lo": 12.5, "hi": 12.5, "cmp": ">"}]}],
              superseded=[{"guideline": "1/2019", "values": [{"lo": 11, "hi": 11, "cmp": ">="}]}],
              decoy=[{"lo": 16, "hi": 16}])
STEMS = {"vi": "Ngưỡng nào sau đây?", "en": "Which threshold?"}


def test_skip_reasons_and_unit_twins():
    """Q1: an MCQ only for a planted value outside the MoH set + a decoy + one distinct MoH item."""
    assert mcq.skip_reasons(THR) == [] and mcq.skip_reasons(DRIFT) == [] and mcq.skip_reasons(SAME) == []
    assert mcq.skip_reasons(dict(THR, decoy=[])) == [mcq.NO_DECOY]
    assert mcq.skip_reasons(dict(THR, vn=THR["vn"] + [{"lo": 10.5, "hi": 10.5}])) == [mcq.MULTI_VN]
    inside = _atom(vn=[{"lo": 7, "hi": 7, "cmp": ">"}], decoy=[{"lo": 5, "hi": 5}],
                   foreign=[{"system": "WHO_global", "values": [{"lo": 7, "hi": 7, "cmp": ">"}]}],
                   superseded=[{"guideline": "1/2019", "values": [{"lo": 7, "hi": 7, "cmp": ">="}]}])
    assert inside["conflict_status"] == "concordant" and mcq.skip_reasons(inside) == [mcq.NO_OUTSIDE]
    # one glucose threshold written in two units is ONE MoH item (not a DR8 set)
    glu = _atom(unit="mmol/L", context={"analyte": "glucose"},
                vn=[{"lo": 7.0, "hi": 7.0, "cmp": ">="}, {"lo": 126, "hi": 126, "unit": "mg/dL", "cmp": ">="}],
                foreign=[{"system": "US", "values": [{"lo": 6.5, "hi": 6.5, "cmp": ">="}]}],
                decoy=[{"lo": 7.5, "hi": 7.5}])
    assert len(mcq.distinct_vn(glu)) == 1 and mcq.skip_reasons(glu) == []


def test_build_all_skips_on_purpose_and_requires_stems(monkeypatch):
    """Q1 + Q11: skipped MCQ -> QC ok=True with a note (null stems valid); eligible atom without stems -> QC error."""
    monkeypatch.setattr(build, "atom_passage", lambda a, root=None, *w: "Đoạn trích giả.")
    monkeypatch.setattr(build, "passage_ocr", lambda a, root=None: False)
    meta = {"guideline": "9999/2099", "section": "s", "page": 1}
    draft = {"short_vi": "Ngưỡng HbA1c (%) là bao nhiêu?", "short_en": "What is the HbA1c threshold (%)?",
             "mcq_stem_vi": None, "mcq_stem_en": None}
    no_decoy = dict(THR, atom_id="T-a", decoy=[], **meta)
    _, _, qc = build.build_all([no_decoy], {"T-a": dict(draft, atom_id="T-a")}, 1, (150, 300))
    row = next(r for r in qc if r["question_id"] == "T-a|mcq")
    assert row["ok"] is True and row["note"] == build.SKIP_NOTE + mcq.NO_DECOY
    _, _, qc = build.build_all([dict(THR, atom_id="T-b", **meta)], {"T-b": dict(draft, atom_id="T-b")}, 1, (150, 300))
    row = next(r for r in qc if r["question_id"] == "T-b|mcq")
    assert row["ok"] is False and row["issues"] == "thiếu stem trắc nghiệm"


def test_third_option_superseded_else_filler_never_second_foreign():
    """Q2: slot 3 = a superseded value outside the MoH set, else a filler; never a second foreign value."""
    with_sup = dict(THR, superseded=[{"guideline": "1/2019", "values": [{"lo": 7, "hi": 7, "cmp": ">="}]}])
    assert [r for _, r, _ in mcq.options(with_sup)[0]] == ["vn", "foreign:US", "superseded:1/2019", "decoy"]
    assert [r for _, r, _ in mcq.options(THR)[0]] == ["vn", "foreign:US", "filler", "decoy"]
    with pytest.raises(ValueError, match="filler"):     # old code filled slot 3 with EU_UK 24 months
        mcq.options(TWO_F)
    opts, notes = mcq.options(TWO_F, filler={"lo": 30, "hi": 30, "unit": "month"})
    assert [r for _, r, _ in opts] == ["vn", "foreign:US", "filler", "decoy"] and notes == [mcq.HAND_FILLER]
    # no conflicting foreign value: slots 2-3 hold superseded values, then a filler
    assert [s for s, _, _ in mcq.options(DRIFT)[0]] == ["vn", "superseded", "filler", "decoy"]


def test_option_equal_to_foreign_and_superseded_carries_both_tokens():
    """Q2 + shared contract: one option, every token in grading priority; grade_mcq -> label 3 with the system."""
    opts, _ = mcq.options(SAME)
    assert [r for _, r, _ in opts] == ["vn", "superseded:3310/2019|foreign:US", "filler", "decoy"]
    g = grade_mcq("ĐÁP ÁN: B", {"A": "vn", "B": opts[1][1], "C": "filler", "D": "decoy"})
    assert g.label == 3 and g.superseded == ["3310/2019"] and g.foreign_systems == ["US"]
    two_sup = dict(SAME, superseded=SAME["superseded"] + [{"guideline": "5448/2014", "values": [{"lo": 45, "hi": 45}]}])
    assert [r for _, r, _ in mcq.options(two_sup)[0]] == ["vn", "superseded:3310/2019|foreign:US",
                                                          "superseded:5448/2014", "decoy"]


def test_options_differ_from_the_whole_value_set():
    """Q3: a superseded value inside ANY MoH item is never planted; a filler must clear every recorded value."""
    a = _atom(vn=[{"lo": 9, "hi": 9}, {"lo": 11, "hi": 11}], decoy=[{"lo": 5, "hi": 5}],
              superseded=[{"guideline": "1/2019", "values": [{"lo": 11, "hi": 11}]},
                          {"guideline": "2/2019", "values": [{"lo": 13, "hi": 13}]}])
    assert mcq.superseded_outside(a) == [{"lo": 13, "hi": 13}] and mcq.role_of({"lo": 11, "hi": 11}, a) == "vn"
    with pytest.raises(ValueError, match="trùng"):
        mcq.options(TWO_F, filler={"lo": 24, "hi": 24, "unit": "month"})
    with pytest.raises(ValueError, match="dung sai"):                 # 25 is 1 month from EU_UK 24 (< 2 x 1.5)
        mcq.options(TWO_F, filler={"lo": 25, "hi": 25, "unit": "month"})
    drugs = finalize({"atom_id": "T-d", "value_kind": "drugs", "vn": [{"key_drugs": ["bedaquiline"]}],
                      "foreign": [{"system": "WHO_global", "values": [{"key_drugs": ["amikacin"]},
                                                                      {"key_drugs": ["cycloserine"],
                                                                       "derived": True}]}],
                      "superseded": [], "decoy": [{"key_drugs": ["linezolid"]}]})
    with pytest.raises(ValueError, match="trùng"):                    # derived values count for the filler
        mcq.options(drugs, filler={"key_drugs": ["cycloserine"]})
    assert mcq.options(drugs, filler={"key_drugs": ["delamanid"]})[0][2][1] == "filler"


def test_rule_filler_order_rounding_and_hand_filler():
    """Q4: reflection through the foreign value, then through the decoy, then 'far' on both sides; nicely rounded,
    same width as the foreign value; a draft num filler only when no rule candidate qualifies."""
    age = _atom(unit="year", vn=[{"lo": 45, "hi": 45, "cmp": ">="}], decoy=[{"lo": 55, "hi": 55}],
                foreign=[{"system": "US", "values": [{"lo": 35, "hi": 35, "cmp": ">="}]}])
    assert mcq.rule_filler(age, age["foreign"][0]["values"][0], age["decoy"][0]) == {"lo": 25, "hi": 25, "unit": "year"}
    iu = _atom(unit="IU", vn=[{"lo": 3000, "hi": 6000}], decoy=[{"lo": 8500, "hi": 8500}],
               foreign=[{"system": "US", "values": [{"lo": 500, "hi": 500}]}])      # through foreign < 0 -> decoy
    assert mcq.rule_filler(iu, {"lo": 500, "hi": 500}, iu["decoy"][0])["lo"] == 13000       # 12500 -> 2 digits
    rate = _atom(unit="ml/kg/h", vn=[{"lo": 15, "hi": 15}], decoy=[{"lo": 20, "hi": 25}],
                 foreign=[{"system": "WHO_global", "values": [{"lo": 5, "hi": 10}]}])     # only 'far' qualifies
    opts, notes = mcq.options(rate, filler={"lo": 30, "hi": 30})                      # draft filler ignored
    assert opts[2][2] == {"lo": 35, "hi": 40, "unit": "ml/kg/h"} and notes == [mcq.DRAFT_FILLER_UNUSED]
    months = _atom(unit="month", vn=[{"lo": 9, "hi": 9}], decoy=[{"lo": 3, "hi": 6}],
                   foreign=[{"system": "US", "values": [{"lo": 12, "hi": 15}]}])
    assert mcq.options(months)[0][2][2] == {"lo": 21, "hi": 24, "unit": "month"}      # 22.5 +- 1.5 -> 21-24
    dose = _atom(unit="mg/kg", vn=[{"lo": 3, "hi": 3}], decoy=[{"lo": 3.6, "hi": 3.6}],
                 foreign=[{"system": "US", "values": [{"lo": 2.4, "hi": 2.4}]}])
    assert mcq.options(dose)[0][2][2]["lo"] == 1.8                                    # exactly 2 x tol: accepted
    # MoH neighbour values block candidates; when every candidate is blocked the draft filler is used ("filler tay")
    nb = dict(THR, moh_neighbour=[{"context": "k", "values": [{"lo": 11, "hi": 11}]}])
    assert mcq.options(nb)[0][2][2]["lo"] == 7                                        # 11 blocked -> through decoy
    blocked = dict(THR, moh_neighbour=[{"context": "k", "values": [{"lo": x, "hi": x} for x in (7, 11, 12, 6)]}])
    with pytest.raises(ValueError):
        mcq.options(blocked)
    opts, notes = mcq.options(blocked, filler={"lo": 14, "hi": 14})
    assert opts[2][2] == {"lo": 14, "hi": 14} and notes == [mcq.HAND_FILLER]


def test_planted_options_take_the_foreign_comparator():
    """Q5: decoy and filler are displayed with the comparator of the foreign option (else of the MoH option); a range
    never takes one; comparators that differ in the recorded values themselves are noted, not hidden."""
    opts, _ = mcq.options(THR, side="anchor")
    assert mcq.option_texts(THR, opts, "vi")[0] == ["≥ 9 %", "> 10 %", "> 11 %", "> 8 %"]
    qs, _ = mcq.build(THR, STEMS, 7)
    assert all(t[0] in "≥>" for q in qs for t in q["options"].values())
    assert "cmp" not in THR["decoy"][0]                                               # atom values untouched
    opts, _ = mcq.options(DRIFT, side="anchor")
    assert mcq.option_texts(DRIFT, opts, "en")[0] == ["> 12.5 kPa", "≥ 11 kPa", "> 9.5 kPa", "> 16 kPa"]
    rng = _atom(vn=[{"lo": 9, "hi": 9, "cmp": ">="}], decoy=[{"lo": 5, "hi": 7}],
                foreign=[{"system": "US", "values": [{"lo": 12, "hi": 12, "cmp": ">="}]}])
    opts, _ = mcq.options(rng, side="anchor")
    assert mcq.option_texts(rng, opts, "vi")[0][3] == "5–7 %"                        # not "≥ 5–7 %"
    odd = _atom(vn=[{"lo": 9, "hi": 9, "cmp": ">="}], decoy=[{"lo": 8, "hi": 8}],
                foreign=[{"system": "US", "values": [{"lo": 10, "hi": 10}]}])
    _, meta = mcq.build(odd, STEMS, 7)
    assert any(n.startswith(mcq.CMP_MISMATCH) for n in meta["notes"])


def test_filler_side_is_a_seeded_coin_and_the_numeric_rank_is_recorded():
    """Review 26/9 (H1 symmetry): the decoy lies beyond the MoH value from the foreign value, so a filler always tried
    beyond the foreign value put the foreign option inside and the decoy at the numeric edge. The side tried first is a
    coin seeded by atom_id (about half each way); the realised order of the options is recorded."""
    ids = [f"P-x-{i:03d}" for i in range(400)]
    share = sum(mcq.filler_side(i, 20260926) == "decoy" for i in ids) / len(ids)
    assert 0.44 <= share <= 0.56 and mcq.filler_side("P-x-001", 5) == mcq.filler_side("P-x-001", 5)
    a, _ = mcq.options(THR, side="anchor")
    d, _ = mcq.options(THR, side="decoy")
    assert mcq.option_rank(THR, a) == "decoy<vn<foreign<filler" and a[2][2]["lo"] == 11
    assert mcq.option_rank(THR, d) == "filler<decoy<vn<foreign" and d[2][2]["lo"] == 7
    assert mcq.edge_slots(mcq.option_rank(THR, a)) == {"decoy", "filler"}
    assert mcq.edge_slots(mcq.option_rank(THR, d)) == {"filler", "foreign"}
    _, meta = mcq.build(THR, STEMS, 7)
    assert meta["side"] == mcq.filler_side("T-thr", 7) and meta["rank"] == mcq.option_rank(THR, meta["opts"])
    assert mcq.option_rank(CAT, mcq.options(CAT, filler={"label": "plasma"})[0]) == ""
    # viral load (log scale) is reflected by ratio, as its decoy is: 2,000 via 20,000 -> 200,000 (not 38,000)
    vl = _atom(atom_id="T-vl", unit="IU/mL", vn=[{"lo": 2000, "hi": 2000, "cmp": ">"}], decoy=[{"lo": 200, "hi": 200}],
               foreign=[{"system": "US", "values": [{"lo": 20000, "hi": 20000, "cmp": ">"}]}])
    assert mcq.rule_filler(vl, vl["foreign"][0]["values"][0], vl["decoy"][0])["lo"] == 200000


def test_moh_option_is_the_item_in_the_atom_unit_and_unit_twins_are_refused():
    """The MoH option shows the item written in the atom's unit (not '≥ 6,994 mmol/L'); a planted value that is the
    MoH threshold in another unit is a data error; an indistinguishable atom gets its own skip reason."""
    glu = _atom(unit="mmol/L", context={"analyte": "glucose"},
                vn=[{"lo": 126, "hi": 126, "unit": "mg/dL", "cmp": ">="}, {"lo": 7.0, "hi": 7.0, "cmp": ">="}],
                foreign=[{"system": "US", "values": [{"lo": 6.5, "hi": 6.5, "cmp": ">="}]}], decoy=[{"lo": 7.5, "hi": 7.5}])
    assert mcq.vn_item(glu) == {"lo": 7.0, "hi": 7.0, "cmp": ">="}
    assert mcq.build(glu, STEMS, 7)[1]["texts"]["vi"][0] == "≥ 7 mmol/L"
    twin = _atom(unit="mmol/L", context={"analyte": "glucose"}, vn=[{"lo": 7.0, "hi": 7.0, "cmp": ">="}],
                 foreign=[{"system": "US", "values": [{"lo": 126, "hi": 126, "unit": "mg/dL", "cmp": ">="}]}],
                 superseded=[{"guideline": "1/2019", "values": [{"lo": 7.8, "hi": 7.8, "cmp": ">="}]}],
                 decoy=[{"lo": 6.5, "hi": 6.5}])
    with pytest.raises(ValueError, match="đơn vị khác"):
        mcq.options(twin)
    ind = _atom(vn=[{"lo": 10, "hi": 10}], foreign=[{"system": "US", "values": [{"lo": 12, "hi": 12}]}],
                decoy=[{"lo": 12.5, "hi": 12.5}])
    assert ind["conflict_status"] == "indistinguishable" and mcq.skip_reasons(ind) == [mcq.NOT_SEPARABLE]


CAT = finalize({"atom_id": "T-cat", "value_kind": "cat", "slot_type": "first_line",
                "cat_options": {"colloid": ["cao phan tu", "colloid"], "crystalloid": ["tinh the", "crystalloid"],
                                "albumin": ["albumin"], "plasma": ["huyet tuong", "plasma"]},
                "vn": [{"label": "colloid", "text": "cao phân tử 10–15 ml/kg/giờ"}],
                "foreign": [{"system": "WHO_global", "values": [{"label": "crystalloid", "text": "WHO gợi ý tinh thể"}]}],
                "superseded": [], "decoy": [{"label": "albumin", "text": "albumin (mồi)"}]})
GOOD_TEXT = {"vn": {"vi": "dung dịch cao phân tử", "en": "colloid solution"},
             "foreign": {"vi": "dung dịch tinh thể", "en": "crystalloid solution"},
             "decoy": {"vi": "dung dịch albumin", "en": "albumin solution"},
             "filler": {"vi": "huyết tương tươi", "en": "fresh plasma"}}


def test_cat_options_need_writer_text_and_pass_option_qc():
    """Q7: cat atoms need the writer's option_text (ValueItem.text leaked '(mồi)', 'WHO…', Vietnamese in EN);
    option texts are checked for source/role words, role read-back by the grader, length and script."""
    with pytest.raises(ValueError, match="option_text"):
        mcq.build(CAT, STEMS, 7, filler={"label": "plasma"})
    qs, meta = mcq.build(CAT, STEMS, 7, filler={"label": "plasma"}, option_text=GOOD_TEXT)
    assert meta["texts"]["en"] == ["colloid solution", "crystalloid solution", "fresh plasma", "albumin solution"]
    for lang in ("vi", "en"):
        assert option_issues(meta["opts"], meta["texts"][lang], meta["by_writer"][lang], CAT, lang) == []
    bad = dict(GOOD_TEXT, vn={"vi": "cao phân tử theo khuyến cáo Bộ Y tế, truyền nhanh trong giờ đầu tiên",
                              "en": "dung dịch cao phân tử"},
               foreign={"vi": "dung dịch cao phân tử", "en": "crystalloid solution"})
    _, meta = mcq.build(CAT, STEMS, 7, filler={"label": "plasma"}, option_text=bad)
    vi = " | ".join(option_issues(meta["opts"], meta["texts"]["vi"], meta["by_writer"]["vi"], CAT, "vi"))
    en = " | ".join(option_issues(meta["opts"], meta["texts"]["en"], meta["by_writer"]["en"], CAT, "en"))
    assert "gợi nguồn" in vi and "độ dài" in vi and "phương án foreign (vi)" in vi      # (i), (iii), (ii)
    assert "chữ tiếng Việt" in en                                                     # (iv)
    # drugs: option_text is optional, per slot
    mal = finalize({"atom_id": "T-m", "value_kind": "drugs", "vn": [{"key_drugs": ["quinine+clindamycin"]}],
                    "foreign": [{"system": "US", "values": [{"key_drugs": ["artemether-lumefantrine"]}]}],
                    "decoy": [{"key_drugs": ["atovaquone-proguanil"]}], "superseded": []})
    _, meta = mcq.build(mal, STEMS, 7, filler={"key_drugs": ["mefloquine"]},
                        option_text={"vn": {"vi": "quinin + clindamycin 7 ngày", "en": "quinine + clindamycin"}})
    assert meta["by_writer"]["vi"] == {"vn"} and meta["texts"]["vi"][1] == "artemether-lumefantrin"


def test_cat_filler_may_be_unreadable_but_must_not_name_a_source():
    """Review 26/9: a cat atom's cat_options hold only the labels of its sources, so no filler text can be parsed;
    an unreadable filler passes (it matches no source), a filler that reads as a source label fails."""
    src_only = dict(CAT, cat_options={k: v for k, v in CAT["cat_options"].items() if k != "plasma"})
    _, meta = mcq.build(src_only, STEMS, 7, filler={"label": "plasma"}, option_text=GOOD_TEXT)
    for lang in ("vi", "en"):
        assert option_issues(meta["opts"], meta["texts"][lang], meta["by_writer"][lang], src_only, lang) == []
    named = dict(GOOD_TEXT, filler={"vi": "dịch tinh thể pha loãng", "en": "diluted crystalloid"})
    _, meta = mcq.build(src_only, STEMS, 7, filler={"label": "plasma"}, option_text=named)
    assert any("filler (vi) được bộ chấm xếp vào một nguồn" in x for x in
               option_issues(meta["opts"], meta["texts"]["vi"], meta["by_writer"]["vi"], src_only, "vi"))


SCHED = finalize({"atom_id": "T-s", "value_kind": "schedule", "slot_type": "schedule",
                  "vn": [{"seq": [0, 3, 7, 14, 28], "unit": "day"}], "superseded": [],
                  "foreign": [{"system": "US", "values": [{"seq": [0, 3, 7, 14], "unit": "day"}]}],
                  "decoy": [{"seq": [0, 7, 21], "unit": "day"}]})


def test_writer_option_text_is_read_back_for_every_kind_that_allows_it():
    """Review 26/9: num/bp options are always rendered (option_text refused); schedule texts are read back like
    drugs/cat (a swapped or copied text no longer passes silently); the four texts must differ."""
    num = _atom(unit="ml/kg/h", vn=[{"lo": 15, "hi": 15}], decoy=[{"lo": 20, "hi": 25}],
                foreign=[{"system": "WHO_global", "values": [{"lo": 5, "hi": 10}]}])
    with pytest.raises(ValueError, match="num/bp"):
        mcq.build(num, STEMS, 7, option_text={"vn": {"vi": "5–10 ml/kg/giờ", "en": "5–10 mL/kg/h"}})
    copied = {"vn": {"vi": "ngày 0, 3, 7, 14", "en": "days 0, 3, 7, 14"}}
    _, meta = mcq.build(SCHED, STEMS, 7, filler={"seq": [0, 7, 28], "unit": "day"}, option_text=copied)
    issues = " | ".join(option_issues(meta["opts"], meta["texts"]["vi"], meta["by_writer"]["vi"], SCHED, "vi"))
    assert "phương án vn (vi) được bộ chấm xếp" in issues and "hai phương án hiển thị giống nhau" in issues
    ok = {"vn": {"vi": "ngày 0, 3, 7, 14 và 28", "en": "days 0, 3, 7, 14 and 28"}}
    _, meta = mcq.build(SCHED, STEMS, 7, filler={"seq": [0, 7, 28], "unit": "day"}, option_text=ok)
    assert option_issues(meta["opts"], meta["texts"]["en"], meta["by_writer"]["en"], SCHED, "en") == []
    # the same printed text for two values (rounding) is caught too
    assert option_distinct_issues(["0,1235 mg", "0,1235 mg ", "1 mg", "2 mg"])


def test_option_text_parallel_in_both_languages():
    assert option_text_issues(GOOD_TEXT) == []
    bad = {"vn": {"vi": "truyền 5 ngày", "en": "7 days"}, "decoy": {"vi": "albumin"}}
    assert option_text_issues(bad) == ["option_text vn: số khác nhau VI [5.0] ≠ EN [7.0]",
                                       "option_text decoy thiếu bản en"]


FRAG_SYN = {d: [] for d in ("bedaquiline", "pretomanid", "linezolid", "delamanid", "clofazimine", "moxifloxacin",
                            "pyrazinamide", "levofloxacin")}
FRAG_COMBOS = {"BPaL": ["bedaquiline", "pretomanid", "linezolid"]}
FRAG = finalize({"atom_id": "T-bpal", "value_kind": "drugs", "superseded": [],
                 "vn": [{"key_drugs": ["BPaL"], "text": "BPaL (bedaquiline + pretomanid + linezolid), 6 tháng"}],
                 "foreign": [{"system": "WHO_global", "values": [
                     {"key_drugs": ["delamanid", "clofazimine"],
                      "text": "BDLC: bedaquiline + delamanid + linezolid + clofazimine"}]}],
                 "decoy": [{"key_drugs": ["pretomanid", "moxifloxacin", "pyrazinamide"],
                            "text": "bedaquiline + pretomanid + moxifloxacin + pyrazinamide"}]})


def test_drug_options_rendered_from_key_fragments_need_writer_text():
    """Review 26/9 (tbhiv-01): key_drugs is only the discriminating part of a regimen; an option rendered from it
    ('delamanid + clofazimine' for BDLC) is a fragment told apart by its form, so option_text is required."""
    _, meta = mcq.build(FRAG, STEMS, 7, FRAG_SYN, FRAG_COMBOS, filler={"key_drugs": ["levofloxacin"]})
    issues = option_issues(meta["opts"], meta["texts"]["en"], meta["by_writer"]["en"], FRAG, "en", FRAG_SYN,
                           FRAG_COMBOS)
    assert [x.split(" tự render")[0] for x in issues] == ["phương án foreign", "phương án decoy"]
    full = {"foreign": {"vi": "bedaquilin + delamanid + linezolid + clofazimin",
                        "en": "bedaquiline + delamanid + linezolid + clofazimine"},
            "decoy": {"vi": "bedaquilin + pretomanid + moxifloxacin + pyrazinamid",
                      "en": "bedaquiline + pretomanid + moxifloxacin + pyrazinamide"},
            "filler": {"vi": "bedaquilin + levofloxacin + linezolid + clofazimin",
                       "en": "bedaquiline + levofloxacin + linezolid + clofazimine"},
            "vn": {"vi": "bedaquilin + pretomanid + linezolid", "en": "bedaquiline + pretomanid + linezolid"}}
    _, meta = mcq.build(FRAG, STEMS, 7, FRAG_SYN, FRAG_COMBOS, filler={"key_drugs": ["levofloxacin"]},
                        option_text=full)
    assert option_issues(meta["opts"], meta["texts"]["en"], meta["by_writer"]["en"], FRAG, "en", FRAG_SYN,
                         FRAG_COMBOS) == []
    # a class token covering the key ('tenofovir' for TDF) is not an extra drug
    cls_syn = {"tenofovir-disoproxil": ["tdf"], "tenofovir-disoproxil|tenofovir-alafenamide": ["tenofovir"]}
    tdf = {"value_kind": "drugs"}
    assert drug_fragment_issues("vn", {"key_drugs": ["tenofovir-disoproxil"], "text": "tenofovir"}, tdf, cls_syn) == []


def test_option_hint_words():
    for t in ("5 mg (WHO)", "theo 2760/2023", "khuyến cáo chính", "liều của Anh", "US dose", "phương án mồi",
              "recommended dose", "Bộ Y tế", "Vietnamese protocol", "Ministry of Health dose", "Europe", "England",
              "EU label", "NHS dose", "khuyến nghị", "phác đồ cũ", "previous regimen", "QĐ 3310", "Quyết định 2760",
              "Hoa Kì", "nước ngoài"):
        assert option_hint_issues(t), t
    for t in ("140/90 mmHg", "ưu tiên tiêm bắp", "20.000 IU/mL", "đơn vị quốc tế", "adrenalin 1/1000",
              "pha loãng 1/2000", "cũng dùng được", "international units"):
        assert option_hint_issues(t) == [], t
    assert option_script_issues("Guillain-Barré syndrome", "en") == []
    assert option_script_issues("dung dịch tinh thể", "en") and option_script_issues("có là", "en")


def test_order_one_rotates_order_zero_by_two():
    """Q8: position i of order 0 -> (i+2) mod 4 in order 1: every option changes letter, middle and edge swap."""
    for aid in ("P-a-01", "P-b-02", "P-c-03", "P-d-04", "P-e-05"):
        first, second = mcq.orders(aid, 4, 7)
        for opt in range(4):
            p0, p1 = first.index(opt), second.index(opt)
            assert p1 == (p0 + 2) % 4 and ({p0, p1} & {0, 3}) and ({p0, p1} & {1, 2})
