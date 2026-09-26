"""T2.4: positioned text with heading paths, page furniture dropped, tables kept, OCR pages from the sidecar."""
import hashlib
import json

import pytest

from vnsoc.extract.pdf_to_text import extract, furniture, is_heading
from vnsoc.extract.verify_span import pdf_path


def test_heading_and_furniture_rules():
    assert is_heading("C.2.1. Treatment of shock in adults", bold=True) == "C.2.1"
    assert is_heading("2.2. Special groups", bold=False) == "2.2"
    assert is_heading("Chương 3 Điều trị", bold=True) == "Chương"
    assert is_heading("Phụ lục 16.1: Sơ đồ truyền dịch (tham chiếu trong thân bài)", bold=False) is None
    assert is_heading("15 ml/kg/h is the initial rate in adults with dengue shock and should be reassessed after one "
                      "hour of treatment in all cases", bold=False) is None
    assert furniture("syt_hochiminh_vt_Van thu SYT TP.Ho Chi Minh_04/07/2023 10:26:33") and furniture(" 27 ")
    assert not furniture("C.2. Treatment")
    assert is_heading("30 phút, lặp lại mỗi 8 giờ", bold=False) is None and is_heading("IV. Điều trị", bold=True) == "IV"


def test_extract_blocks_tables_and_ocr(proj):
    fitz = pytest.importorskip("pymupdf")
    pytest.importorskip("pdfplumber")
    doc = fitz.open()
    p1 = doc.new_page()
    p1.insert_text((72, 60), "syt_test_vt_stamp 01/01/2099", fontsize=8)
    p1.insert_text((72, 100), "C.2. Severe dengue in adults", fontname="hebo", fontsize=12)
    p1.insert_text((72, 130), "C.2.1. Shock", fontname="hebo", fontsize=12)
    p1.insert_text((72, 160), "Ringer lactate 15 ml/kg/h for the first hour.", fontsize=11)
    x0, y0, w, h = 72, 200, 150, 20                               # a 2 x 2 table with ruling lines
    for r in range(3):
        p1.draw_line((x0, y0 + r * h), (x0 + 2 * w, y0 + r * h))
    for c in range(3):
        p1.draw_line((x0 + c * w, y0), (x0 + c * w, y0 + 2 * h))
    for r, row in enumerate((("Group", "Dose"), ("Adult", "15 ml/kg/h"))):
        for c, cell in enumerate(row):
            p1.insert_text((x0 + c * w + 4, y0 + r * h + 14), cell, fontsize=9)
    doc.new_page()                                                # scanned page (no text layer)
    path = pdf_path("5555/2099", proj)
    path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(path)
    from vnsoc.extract.ocr import sidecar_dir

    d = sidecar_dir(path, proj)
    d.mkdir(parents=True)
    (d / "p002.txt").write_text("OCR page text: primaquine 0,25 mg/kg single dose. " * 3, encoding="utf-8")
    (d / "meta.json").write_text(json.dumps({"pdf_sha256": hashlib.sha256(path.read_bytes()).hexdigest()}), encoding="utf-8")
    recs, meta = extract("5555/2099", tables=True, root=proj)
    texts = [r for r in recs if r["kind"] == "text"]
    assert not any("syt_test" in r["text"] for r in recs)
    body = next(r for r in texts if "Ringer lactate" in r["text"])
    assert body["headings"][-1].startswith("C.2.1") and body["headings"][0].startswith("C.2.") and body["bbox"]
    tab = [r for r in recs if r["kind"] == "table"]
    assert tab and tab[0]["rows"][1] == ["Adult", "15 ml/kg/h"]
    ocr = [r for r in recs if r["kind"] == "ocr"]
    assert ocr and ocr[0]["page"] == 2 and "primaquine" in ocr[0]["text"] and meta["ocr_pages"] == [2]
