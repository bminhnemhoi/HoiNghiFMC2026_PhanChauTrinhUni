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
