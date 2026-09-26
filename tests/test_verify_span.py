"""Span verification: the span must be verbatim on the stated page and every MoH value must parse back from it.
The PDF here is generated in the test (ASCII text; Vietnamese normalisation is tested on strings)."""
import pytest

from vnsoc.extract.verify_span import find_pages, missing_vn_values, norm, pdf_path, span_on_page, verify_atom

SYN = {"quinine": ["quinin"], "clindamycin": [], "artemether-lumefantrine": ["artemether-lumefantrin"]}
COMBOS = {"quinine+clindamycin": ["quinine", "clindamycin"]}


@pytest.fixture
def pdf(proj):
    fitz = pytest.importorskip("fitz")
    doc = fitz.open()
    for text in ("Section A. General principles of care.",
                 "Shock in adults: Ringer lactate 15 ml/kg/h in the first hour,\nthen 10 ml/kg/h for 2 hours."):
        page = doc.new_page()
        page.insert_text((72, 72), text, fontsize=11)
    p = pdf_path("9999/2099", proj)
    p.parent.mkdir(parents=True, exist_ok=True)
    doc.save(p)
    return p


def atom(**kw):
    a = {"atom_id": "x", "guideline": "9999/2099", "page": 2, "value_kind": "num", "unit": "ml/kg/h",
         "span": "Ringer lactate 15 ml/kg/h in the first hour, then 10 ml/kg/h for 2 hours.", "vn": [{"lo": 15, "hi": 15}]}
    a.update(kw)
    return a


def test_norm_vietnamese():
    decomposed = "Bộ Y tế"          # NFD "Bộ Y tế"
    assert norm(decomposed) == "Bộ Y tế"
    assert norm("15 ml/kg/giờ\n  rồi\t10") == "15 ml/kg/giờ rồi 10"
    assert norm("ph­ác đồ") == "phác đồ"


def test_pdf_path_keys(proj):
    assert pdf_path("2760/2023", proj).name == "2760_2023.pdf"
    assert pdf_path("TT51/2017", proj).name == "TT51_2017.pdf"


def test_span_on_page(pdf):
    assert span_on_page(pdf, 2, "Ringer lactate 15 ml/kg/h in the first hour, then 10 ml/kg/h")   # crosses a line break
    assert not span_on_page(pdf, 1, "Ringer lactate 15 ml/kg/h")
    assert find_pages(pdf, "10 ml/kg/h for 2 hours") == [2]


def test_verify_atom(pdf, proj):
    assert verify_atom(atom(), proj, {}, {})["ok"]
    r = verify_atom(atom(page=1), proj, {}, {})
    assert not r["ok"] and "trang [2]" in r["reason"]
    r = verify_atom(atom(vn=[{"lo": 20, "hi": 20}]), proj, {}, {})
    assert not r["ok"] and r["missing_vn"] == [0]
    assert not verify_atom(atom(guideline="1/2000"), proj, {}, {})["pdf_exists"]


def test_missing_values_other_kinds():
    bp = {"value_kind": "bp", "span": "chẩn đoán THA khi HA ≥ 140/90 mmHg đo tại phòng khám", "vn": [{"sys": 140, "dia": 90}]}
    assert missing_vn_values(bp) == []
    sched = {"value_kind": "schedule", "span": "tiêm bắp vào các ngày N0, N3, N7, N14 và N28", "min_schedule_len": 3,
             "vn": [{"seq": [0, 3, 7, 14, 28]}]}
    assert missing_vn_values(sched) == []
    drugs = {"value_kind": "drugs", "span": "3 tháng đầu: quinin 7 ngày + clindamycin 7 ngày",
             "vn": [{"key_drugs": ["quinine+clindamycin"]}]}
    assert missing_vn_values(drugs, "vi", SYN, COMBOS) == []
    assert missing_vn_values(dict(drugs, span="artemether-lumefantrin"), "vi", SYN, COMBOS) == [0]
