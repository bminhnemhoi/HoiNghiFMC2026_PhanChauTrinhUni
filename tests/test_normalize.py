import pytest

from vnsoc.normalize_vi import Num, convert, parse_bps, parse_cats, parse_drugs, parse_number, parse_nums, parse_schedules


@pytest.mark.parametrize("tok,lang,val", [
    ("0,5", "vi", 0.5), ("5.000", "vi", 5000), ("1.500", "vi", 1500), ("0.5", "vi", 0.5), ("0.500", "vi", 0.5),
    ("2,000", "vi", 2000), ("2,5", "vi", 2.5), ("1.000.000", "vi", 1e6), ("1.000,5", "vi", 1000.5),
    ("2,000", "en", 2000), ("0.5", "en", 0.5), ("2.000", "en", 2000), ("0,5", "en", 0.5), ("½", "vi", 0.5),
])
def test_parse_number(tok, lang, val):
    assert parse_number(tok, lang) == pytest.approx(val)


def test_ranges_and_units():
    assert parse_nums("0,5–1 mg") == [Num(0.5, 1.0, "mg")]
    assert parse_nums("10 - 15mg/kg") == [Num(10, 15, "mg/kg")]
    assert parse_nums("từ 10 đến 15 ml/kg/giờ") == [Num(10, 15, "ml/kg/h")]
    assert parse_nums("from 10 to 15 mg", "en") == [Num(10, 15, "mg")]
    assert parse_nums("5 - 10 ml/kg/h")[0].unit == "ml/kg/h"


def test_comparators_and_citations():
    n = parse_nums("HBV DNA > 2.000 IU/mL (QĐ 1740/QĐ-BYT 2026)")
    assert n == [Num(2000, 2000, "IU/mL", ">")]
    assert parse_nums("HbA1c ≥ 9%") == [Num(9, 9, "%", ">=")]          # the 1 in A1c is not a value
    assert parse_nums("theo ADA 2025 là < 55 mg/dL") == [Num(55, 55, "mg/dL", "<")]
    assert parse_nums("từ 45 tuổi")[0].cmp == ">="
    assert parse_nums("2000 IU/mL")[0].lo == 2000                        # not stripped as a year


def test_convert():
    assert convert(250, "ug", "mg") == pytest.approx(0.25)
    assert convert(0.25, "ml", "ug", {"mg_per_ml": 1}) == pytest.approx(250)
    assert convert(4, "tablet", "mg", {"mg_per_tablet": 7.5}) == pytest.approx(30)
    assert convert(0.01, "mg/kg", "ug", {"weight_kg": 10}) == pytest.approx(100)
    assert convert(5.0, "mmol/L", "mg/dL", {"analyte": "glucose"}) == pytest.approx(90.08, rel=1e-3)
    assert convert(5000, "/uL", "10^9/L") == pytest.approx(5)
    assert convert(1, "mg", "ml/kg/h") is None


def test_bp():
    assert parse_bps("≥ 140/90 mmHg")[0].sys == 140
    assert parse_bps("ALT 30/19 U/L") == []
    assert parse_bps("QĐ 3192/2010: 140/90")[0].dia == 90


def test_schedules():
    assert parse_schedules("N0-3-7-14-28")[0].seq == (0, 3, 7, 14, 28)
    assert parse_schedules("ngày 0, 3, 7, 14")[0].seq == (0, 3, 7, 14)
    assert parse_schedules("2, 3, 4 tháng")[0].unit == "month"
    assert parse_schedules("QĐ 1622/QĐ-BYT 2014: N0-3-7-14-28")[0].seq == (0, 3, 7, 14, 28)


@pytest.mark.parametrize("text,seq,unit", [
    # unit is decided next to each sequence, not by any "tháng" elsewhere (found by the rabies pilot agent, 26/9/2026)
    ("Tiêm bắp các ngày 0, 3, 7, 14 và 28; theo dõi 3 tháng", (0, 3, 7, 14, 28), "day"),
    ("ĐÁP ÁN: ngày 0, 3, 7, 14 (trong vòng 1 tháng)", (0, 3, 7, 14), "day"),
    ("Ngày 0 Ngày 3 Ngày 7 Ngày 14 Ngày 28", (0, 3, 7, 14, 28), "day"),          # appendix-form style, space-separated
    ("DPT: tiêm lúc 2, 3, 4 tháng tuổi", (2, 3, 4), "month"),
    ("ANSWER: at 2, 4 and 6 months of age", (2, 4, 6), "month"),
    ("vaccinate on days 0, 3, 7 and 14", (0, 3, 7, 14), "day"),
    ("tháng thứ 2, 3, 4 sau sinh", (2, 3, 4), "month"),
])
def test_schedule_unit_is_local(text, seq, unit):
    s = parse_schedules(text)[0]
    assert (s.seq, s.unit) == (seq, unit)


SYN = {"artemether-lumefantrine": ["artemether-lumefantrin", "coartem"], "artemether": [], "lumefantrine": ["lumefantrin"],
       "pyronaridine-artesunate": ["pyronaridin-artesunat"], "artesunate": ["artesunat"], "primaquine": ["primaquin"],
       "quinine": ["quinin"], "clindamycin": []}
COMBOS = {"artemether-lumefantrine": ["artemether", "lumefantrine"], "quinine+clindamycin": ["quinine", "clindamycin"]}


def test_drugs():
    assert parse_drugs("Artemether–lumefantrine (Coartem)", SYN, COMBOS).names == {"artemether-lumefantrine"}
    assert parse_drugs("artemether + lumefantrin", SYN, COMBOS).names == {"artemether-lumefantrine"}
    assert parse_drugs("Pyronaridin-artesunat 3 ngày + primaquin", SYN, COMBOS).names == {"pyronaridine-artesunate", "primaquine"}
    assert parse_drugs("Quinin 7 ngày + clindamycin 7 ngày", SYN, COMBOS).names == {"quinine+clindamycin"}


def test_cats():
    opts = {"one_step": ["mot buoc", "one-step"], "two_step": ["hai buoc", "two-step"]}
    assert parse_cats("Nghiệm pháp 75 g một bước", opts).labels == {"one_step"}


# Grader fixes found by the pilot agents (26/9/2026) — cases taken from their reports, pre-freeze.
def _vals(text, **atom):
    from vnsoc.grade import parse_values

    return [(f, (round(v.lo, 3), round(v.hi, 3), v.unit)) for f, v in parse_values(text, atom, "vi")]


def test_weight_and_frequency_are_not_assumed_doses():
    a = {"value_kind": "num", "unit": "ug", "context": {"mg_per_ml": 1, "weight_kg": 10}}
    assert _vals("Trẻ 2 tuổi nặng 10 kg: tiêm bắp 0,25 mg", **a) == [("ok", (250.0, 250.0, "ug"))]
    b = {"value_kind": "num", "unit": "mg/kg"}
    assert _vals("Paracetamol 10–15 mg/kg/lần, 2 lần/ngày, cách 4–6 giờ", **b) == [("ok", (10.0, 15.0, "mg/kg"))]


def test_ifcc_international_units_and_index():
    assert _vals("HbA1c ≥ 9% (75 mmol/mol)", value_kind="num", unit="%") == [("ok", (9.0, 9.0, "%"))]
    assert _vals("HTIG 3000–6000 đơn vị tiêm bắp", value_kind="num", unit="IU") == [("ok", (3000.0, 6000.0, "IU"))]
    assert parse_nums("500 IU")[0].unit == "IU" and parse_nums("APRI 1,5 index")[0].unit == "index"
