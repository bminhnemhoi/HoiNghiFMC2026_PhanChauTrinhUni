"""Prompts -> requests -> RunRecords -> grades, end to end on fixtures (no GPU, no API)."""
import json

import pytest

from vnsoc.analysis.pilot import cp, grade_all, register
from vnsoc.match.decoys import finalize
from vnsoc.run import collect, plan
from vnsoc.run.prompts import doc_label, messages, parse_request_id, request_id
from vnsoc.schemas import RunRecord

ATOM = finalize({"atom_id": "P-t-01", "guideline": "2760/2023", "section": "C.2.1", "page": 3, "value_kind": "num",
                 "unit": "ml/kg/h", "vn": [{"lo": 15, "hi": 15}], "superseded": [], "decoy": [{"lo": 20, "hi": 25}],
                 "foreign": [{"system": "WHO_global", "values": [{"lo": 5, "hi": 10}]}]})
Q_VI = {"question_id": "P-t-01|short|vi", "atom_id": "P-t-01", "format": "short", "language": "vi",
        "text": "Người lớn bị sốc SXHD: tốc độ dịch giờ đầu (ml/kg/giờ) là bao nhiêu?", "oracle_passage_id": "P-t-01#A3"}
Q_MCQ = {"question_id": "P-t-01|mcq|vi|o0", "atom_id": "P-t-01", "format": "mcq", "language": "vi",
         "text": "Tốc độ dịch giờ đầu?", "options": {"A": "15 ml/kg/giờ", "B": "5–10 ml/kg/giờ", "C": "20–25 ml/kg/giờ",
                                                  "D": "25–30 ml/kg/giờ"},
         "option_roles": {"A": "vn", "B": "foreign:WHO_global", "C": "decoy", "D": "filler"}}


def test_doc_label_and_request_ids():
    assert doc_label("2760/2023", "vi") == "Quyết định 2760/QĐ-BYT (2023)"
    assert doc_label("TT51/2017", "en") == "Circular 51/2017/TT-BYT"
    rid = request_id("P-t-01|short|vi", "A1", "qwen3_8b", 0)
    assert parse_request_id(rid) == ("P-t-01|short|vi", "A1", "qwen3_8b", 0)


def test_prompts_follow_config():
    a0 = messages(Q_VI, "A0")[0]["content"]
    a1 = messages(Q_VI, "A1")[0]["content"]
    a3 = messages(Q_VI, "A3", ATOM, "Đoạn văn ...")[0]["content"]
    assert a0.startswith("Người lớn") and a0.rstrip().endswith("ĐÁP ÁN: <giá trị> <đơn vị>")
    assert a1.startswith("Theo hướng dẫn chẩn đoán và điều trị hiện hành của Bộ Y tế Việt Nam, người lớn")
    assert "Quyết định 2760/QĐ-BYT (2023), mục C.2.1" in a3 and "Đoạn văn ..." in a3
    m = messages(Q_MCQ, "A1")[0]["content"]
    assert m.startswith("Theo hướng dẫn") and "\nA. 15 ml/kg/giờ\nB." in m and m.rstrip().endswith("<chữ cái>")
    with pytest.raises(ValueError):
        messages(Q_MCQ, "A3")


def test_plan_collect_grade():
    reqs, index, pl = plan.build([Q_VI, Q_MCQ], {"P-t-01": ATOM}, {"P-t-01#A3": "Đoạn văn ..."}, ["m1"])
    assert pl == {"m1|A0|vi|short": 1, "m1|A1|vi|short": 1, "m1|A3|vi|short": 1, "m1|A1|vi|mcq": 1}
    idx = {r["request_id"]: r for r in index}
    outs = {"A0": "ĐÁP ÁN: 10 ml/kg/giờ", "A1": "ĐÁP ÁN: 15 ml/kg/giờ", "A3": "ĐÁP ÁN: 22 ml/kg/giờ"}
    raw = [{"request_id": r["request_id"], "outputs": [outs[r["condition"]] if r["format"] == "short" else "ĐÁP ÁN: C"],
            "tokens_in": 50, "tokens_out": [6], "cum_logprob": [-0.5]} for r in index]
    recs = collect.records(idx, raw, "hf-commit-x", "vllm", "2026-09-28")
    assert len(recs) == 4 and all(RunRecord.model_validate(r) for r in recs)
    with pytest.raises(ValueError):
        collect.records(idx, [{"request_id": "nope|A1|m1|0", "raw_output": "x"}], "v", "vllm", "d")
    g = grade_all(recs, {Q_VI["question_id"]: Q_VI, Q_MCQ["question_id"]: Q_MCQ}, {"P-t-01": ATOM}, {}, {}, "1.0.0")
    lab = {(x["condition"], x["format"]): x for x in g}
    assert lab[("A0", "short")]["label"] == 4 and lab[("A1", "short")]["label"] == 2
    assert lab[("A3", "short")]["decoy_match"] and lab[("A1", "mcq")]["decoy_match"]
    reg = register(g, {"P-t-01": ATOM})
    assert reg["n_conflict_atoms"] == 1 and reg["a1_vi_conflict_n"] == 1 and reg["a0_vi_foreign"] == 1
    assert json.dumps(reg)


def test_clopper_pearson():
    lo, hi = cp(0, 10)
    assert lo == 0.0 and hi == pytest.approx(0.3085, abs=1e-3)
    lo, hi = cp(5, 10)
    assert lo == pytest.approx(0.1871, abs=1e-3) and hi == pytest.approx(0.8129, abs=1e-3)
