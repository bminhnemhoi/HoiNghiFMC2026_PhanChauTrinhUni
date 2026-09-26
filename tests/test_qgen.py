"""Question generation: rendering, oracle passages, planted MCQ roles/orders, and code QC. Values are FIXTURES."""
import pytest

from vnsoc.grade import grade_mcq
from vnsoc.match.decoys import finalize
from vnsoc.qgen import mcq
from vnsoc.qgen.passages import oracle_passage
from vnsoc.qgen.qc import leak_issues, numbers, population_issues, translation_issues
from vnsoc.qgen.render import fmt_num, render_value

DENGUE = finalize({"atom_id": "P-t-01", "value_kind": "num", "unit": "ml/kg/h", "vn": [{"lo": 15, "hi": 15}],
                   "foreign": [{"system": "WHO_global", "values": [{"lo": 5, "hi": 10}]}],
                   "superseded": [], "decoy": [{"lo": 20, "hi": 25}],
                   "population": {"age": "người lớn ≥ 16 tuổi", "setting": "sốc SXHD"}})
MAL = finalize({"atom_id": "P-t-02", "value_kind": "drugs", "vn": [{"key_drugs": ["quinine+clindamycin"]}],
                "foreign": [{"system": "US", "values": [{"key_drugs": ["artemether-lumefantrine"]}]}],
                "decoy": [{"key_drugs": ["atovaquone-proguanil"]}], "superseded": []})
SYN = {"quinine": ["quinin"], "clindamycin": [], "artemether-lumefantrine": ["artemether-lumefantrin"]}
COMBOS = {"quinine+clindamycin": ["quinine", "clindamycin"]}


def test_render():
    assert fmt_num(5000.25, "vi") == "5.000,25" and fmt_num(0.5, "en") == "0.5"
    assert render_value({"lo": 5, "hi": 10}, DENGUE, "vi") == "5–10 ml/kg/giờ"
    assert render_value({"lo": 5, "hi": 10}, DENGUE, "en") == "5–10 mL/kg/h"
    assert render_value({"sys": 140, "dia": 90, "cmp": ">="}, {"value_kind": "bp"}, "vi") == "≥ 140/90 mmHg"
    assert render_value({"seq": [0, 3, 7, 14, 28]}, {"value_kind": "schedule"}, "en") == "days 0, 3, 7, 14, 28"
    assert render_value({"key_drugs": ["quinine+clindamycin"]}, MAL, "vi", SYN, COMBOS) == "quinin + clindamycin"


def test_oracle_passage_keeps_span_and_cuts_at_sentences():
    filler = " ".join(f"Câu thứ {i} nói về chăm sóc chung cho người bệnh." for i in range(60))
    page = filler + " Truyền Ringer lactat 15 ml/kg/giờ trong giờ đầu. " + filler
    p = oracle_passage(page, "Ringer lactat 15 ml/kg/giờ", 150, 300)
    assert "Ringer lactat 15 ml/kg/giờ" in p and 150 <= len(p.split()) <= 300 and p.endswith(".")
    with pytest.raises(ValueError):
        oracle_passage(page, "không có câu này", 150, 300)


def test_mcq_roles_orders_and_grading():
    qs = mcq.build(DENGUE, {"vi": "Tốc độ dịch?", "en": "Fluid rate?"}, 7)
    assert len(qs) == 4 and {q["order_variant"] for q in qs} == {0, 1}
    roles = [q["option_roles"] for q in qs if q["language"] == "vi"]
    assert sorted(roles[0].values()) == sorted(["vn", "foreign:WHO_global", "filler", "decoy"])
    inv0 = {r: letter for letter, r in roles[0].items()}
    inv1 = {r: letter for letter, r in roles[1].items()}
    assert all(inv0[r] != inv1[r] for r in inv0)                      # every option moves between orders
    letter = inv0["foreign:WHO_global"]
    assert grade_mcq(f"ĐÁP ÁN: {letter}", roles[0]).label == 4
    assert mcq.build(DENGUE, {"vi": "x"}, 7)[0]["options"] == mcq.build(DENGUE, {"vi": "x"}, 7)[0]["options"]


def test_mcq_needs_filler_for_drugs():
    with pytest.raises(ValueError):
        mcq.options(MAL)
    opts = mcq.options(MAL, filler={"key_drugs": ["mefloquine"]})
    assert [r for r, _ in opts] == ["vn", "foreign:US", "filler", "decoy"]


def test_qc_checks():
    assert leak_issues("Truyền 15 ml/kg/giờ có đúng không?", DENGUE, "vi") == ["lộ giá trị Bộ Y tế"]
    assert leak_issues("Người lớn ≥ 16 tuổi bị sốc SXHD: tốc độ dịch ban đầu (ml/kg/giờ)?", DENGUE, "vi") == []
    assert population_issues("Người lớn bị sốc SXHD?", DENGUE, "vi") == ["thiếu số của quần thể [16.0]"]
    assert numbers("0,5 mg và 5.000 IU", "vi") == numbers("0.5 mg and 5,000 IU", "en") == [0.5, 5000.0]
    assert translation_issues("Trẻ 10 kg không sốc", "A 10 kg child without shock") == []
    assert translation_issues("Trẻ 10 kg", "A 12 kg child") and translation_issues("Trẻ không sốc", "A child in shock")
