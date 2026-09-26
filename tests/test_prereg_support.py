"""Registered procedures around the analysis (rev-editor ids 6, 9, 10): mechanical corpus order, blinded extractor
sheet, snapshot hashes of the registration package."""
from vnsoc.analysis.extractor_check import blind_output, check_sheet
from vnsoc.extract.corpus_priority import priority_order


def test_blinding_removes_citation_line_and_hides_model():
    raw = "<think>x</think>Theo đoạn [P2], liều là 15 ml/kg/giờ.\nNGUỒN: [P2]\nĐÁP ÁN: 15 ml/kg/giờ"
    b = blind_output(raw)
    assert "NGUỒN" not in b and "<think>" not in b and "ĐÁP ÁN: 15 ml/kg/giờ" in b
    assert "SOURCE" not in blind_output("Dose 15.\n**SOURCE:** [P1]\nANSWER: 15 mL/kg/h")
    rows = [{"run_id": f"r{i}", "model": "qwen3_8b", "condition": "A2", "question": "q", "reference": "15",
             "raw_output": raw, "parsed": "15"} for i in range(5)]
    sheet = check_sheet(rows)
    assert [r["item"] for r in sheet] == [1, 2, 3, 4, 5] and all("model" not in r and "condition" not in r
                                                              for r in sheet)
    assert [r["run_id"] for r in sheet] == [r["run_id"] for r in check_sheet(rows)]     # seeded order


def test_corpus_priority_is_mechanical():
    rows = [
        {"doc_key": "a/2026", "status": "current", "official_pdf": "True", "text_layer": "True", "issued": "2026-06-16"},
        {"doc_key": "b/2010", "status": "current", "official_pdf": "True", "text_layer": "True", "issued": "2010-08-31"},
        {"doc_key": "c/2023", "status": "current", "official_pdf": "True", "text_layer": "True", "issued": "2023-07-04"},
        {"doc_key": "d/2024", "status": "current", "official_pdf": "True", "text_layer": "False", "issued": "2024-01-19"},
        {"doc_key": "e/2025", "status": "current", "official_pdf": "True", "text_layer": "True", "issued": "2025-03-01"},
        {"doc_key": "f/2019", "status": "superseded", "official_pdf": "True", "text_layer": "True", "issued": "2019"},
        {"doc_key": "g/2026", "status": "current", "official_pdf": "True", "text_layer": "True", "issued": "2026-11-01"},
        {"doc_key": "h/2022", "status": "current", "official_pdf": "False", "text_layer": "", "issued": "2022-01-01"},
    ]
    order = priority_order(rows, seeded={"b/2010"}, max_docs=3)
    assert [r["doc_key"] for r in order] == ["b/2010", "a/2026", "e/2025", "c/2023", "d/2024"]
    assert [r["tier"] for r in order] == [1, 2, 2, 3, 4]
    assert [r["included"] for r in order] == [True, True, True, False, False]       # DR2 reserve in the same order
    capped = priority_order(rows, seeded=set(), max_docs=10, max_ocr=1, ocr_already=1)
    assert not next(r for r in capped if r["doc_key"] == "d/2024")["included"]


def test_priority_order_scope_keeps_out_of_scope_as_reserve():
    rows = [{"doc_key": k, "status": "current", "official_pdf": "True", "text_layer": "True", "issued": d}
            for k, d in (("new/2026", "2026-05-01"), ("hf/2022", "2022-01-01"), ("x/2025", "2025-01-01"))]
    order = priority_order(rows, seeded=set(), max_docs=2, scope={"hf/2022", "x/2025"}, excluded={"x/2025": "no values"})
    by = {r["doc_key"]: r for r in order}
    assert by["hf/2022"]["included"] and not by["new/2026"]["included"] and not by["x/2025"]["included"]
    assert by["x/2025"]["reason"] == "no values" and "DR2" in by["new/2026"]["reason"]
    assert [r["doc_key"] for r in order][0] == "hf/2022"                  # in-scope first, reserve after
