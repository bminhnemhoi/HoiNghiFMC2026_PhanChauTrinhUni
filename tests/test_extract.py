"""T3.1 pipeline: verbatim span check + value parse (verify_span), and the pilot re-find criterion (atomize)."""
from vnsoc.extract import atomize
from vnsoc.extract.verify_span import norm


def _a(aid, page, span, lo, g="2760/2023", unit="ml/kg/h"):
    return {"atom_id": aid, "guideline": g, "page": page, "span": span, "value_kind": "num", "unit": unit,
            "vn": [{"lo": lo, "hi": lo, "unit": unit}]}


def test_span_normalisation_is_what_is_compared():
    assert norm("Người  lớn  15ml/kg/giờ") == "Người lớn 15ml/kg/giờ"


def test_refind_by_value_or_span():
    pilot = [_a("P-1", 27, "Ringer lactate 15ml/kg/giờ trong 1 giờ đầu", 15),
             _a("P-2", 30, "một câu khác hoàn toàn", 99),
             _a("P-3", 5, "x", 1, g="9999/2026")]
    mains = [_a("A-1", 28, "bù dịch Ringer lactate 15 ml/kg/giờ", 15),          # same value, page +1
             _a("A-2", 40, "một câu khác hoàn toàn", 99)]                        # same span but page too far
    r = atomize.refind_rate(pilot, mains, in_corpus={"2760/2023"})
    assert r["n"] == 2 and r["refound"] == 1 and r["missing"] == ["P-2"] and r["matches"] == {"P-1": "A-1"}
    assert atomize.span_overlap("a b c d", "b c d e f") == 0.75
