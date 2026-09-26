import pytest

from vnsoc.normalize_vi import BP, Num, convert, parse_bps, parse_cats, parse_drugs, parse_number, parse_nums, parse_schedules


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


def test_daily_dose_converts_with_weight():
    # malaria OCR audit (26/9/2026): "30 mg/ngày" at 60 kg is 0,5 mg/kg/ngày, not "30 mg"
    assert parse_nums("30 mg/ngày")[0].unit == "mg/day"
    assert convert(30, "mg/day", "mg/kg/day", {"weight_kg": 60}) == pytest.approx(0.5)
    assert convert(30, "mg/day", "mg/kg/day", {}) is None


# Grader 1.1.0 (26/9/2026, pre-freeze): parse-level cases from the T1.3 pilot question reviews.
def test_ml_per_kg_unit_and_conversion():
    assert parse_nums("0,01 ml/kg") == [Num(0.01, 0.01, "ml/kg")]
    assert parse_nums("0.01 mL/kg", "en") == [Num(0.01, 0.01, "ml/kg")]
    assert parse_nums("10 ml/kg/giờ")[0].unit == "ml/kg/h"                  # the rate unit still wins
    assert convert(0.01, "ml/kg", "ug", {"weight_kg": 6, "mg_per_ml": 1}) == pytest.approx(60)
    assert convert(0.01, "ml/kg", "ug", {"weight_kg": 6}) is None          # no concentration: not guessed
    assert convert(0.01, "ml/kg", "ug", {"mg_per_ml": 1}) is None          # no weight: not guessed


@pytest.mark.parametrize("text,lo,hi,unit", [
    ("1/2 ống", 0.5, 0.5, "ampoule"), ("½ ống", 0.5, 0.5, "ampoule"), ("1/3 ống", 1 / 3, 1 / 3, "ampoule"),
    ("1⁄3 ống", 1 / 3, 1 / 3, "ampoule"), ("1/5-1/3 ống", 0.2, 1 / 3, "ampoule"), ("1/5 đến 1/3 ống", 0.2, 1 / 3, "ampoule"),
    ("1/2 – 1 ống", 0.5, 1.0, "ampoule"), ("1/2 amp", 0.5, 0.5, "ampoule"), ("0,3-0,5 ml", 0.3, 0.5, "ml"),
    ("1/2 viên", 0.5, 0.5, "tablet"),
])
def test_dose_form_fractions(text, lo, hi, unit):
    n = parse_nums(text)
    assert len(n) == 1 and (n[0].lo, n[0].hi, n[0].unit) == (pytest.approx(lo), pytest.approx(hi), unit)


def test_fractions_do_not_touch_blood_pressure():
    assert parse_bps("HA 140/90 mmHg; adrenalin 1/5 ống") == [BP(140, 90)]
    assert all(n.unit != "ampoule" for n in parse_nums("HA 140/90 mmHg"))


@pytest.mark.parametrize("text", [
    "HA tâm thu ≥ 140 mmHg và/hoặc HA tâm trương ≥ 90 mmHg", "huyết áp tâm thu ≥140 và/hoặc tâm trương ≥90 mmHg",
    "HATT ≥ 140 mmHg và HATTr ≥ 90 mmHg", "SBP ≥140 and/or DBP ≥90 mmHg", "systolic ≥ 140 mm Hg or diastolic ≥ 90 mm Hg",
    "≥140 mmHg systolic or ≥90 mmHg diastolic", "systolic blood pressure ≥ 140 mmHg and/or diastolic blood pressure ≥ 90 mmHg",
    "huyết áp tâm thu từ 140 mmHg trở lên và/hoặc huyết áp tâm trương từ 90 mmHg trở lên",
    "SBP of 140 mmHg or higher and/or DBP of 90 mmHg or higher", "HA tâm thu ≥ 140 mmHg; HA tâm trương ≥ 90 mmHg",
])
def test_split_blood_pressure(text):
    assert parse_bps(text) == [BP(140, 90, ">=")]


def test_split_blood_pressure_needs_both_parts():
    assert parse_bps("HA tâm thu ≥ 140 mmHg") == []
    assert parse_bps("tâm thu 1400 và tâm trương 90") == []


@pytest.mark.parametrize("text,lang,months", [
    ("3 tuổi 4 tháng", "vi", 40), ("3 năm 4 tháng", "vi", 40), ("3 years 4 months", "en", 40),
    ("3 years and 4 months", "en", 40), ("1 năm 6 tháng", "vi", 18),
])
def test_compound_age_is_one_value(text, lang, months):
    assert parse_nums(text, lang) == [Num(months, months, "month")]


def test_compound_age_guards():
    assert len(parse_nums("3 năm 18 tháng")) == 2                          # 18 months is not a remainder
    assert parse_nums("≥ 3 tuổi 4 tháng")[0].cmp == ">="


# Grader 1.1.0, independent review round (26/9/2026, pre-freeze): parse-level cases.
@pytest.mark.parametrize("text,lang,want", [
    ("0.01 mg per kg", "en", Num(0.01, 0.01, "mg/kg")), ("0,01 mg cho mỗi kg", "vi", Num(0.01, 0.01, "mg/kg")),
    ("0,01 mg/1 kg", "vi", Num(0.01, 0.01, "mg/kg")), ("0,01 ml / kg", "vi", Num(0.01, 0.01, "ml/kg")),
    ("10 micrograms per kilogram", "en", Num(10, 10, "ug/kg")), ("10 mcg per kg", "en", Num(10, 10, "ug/kg")),
    ("5-7 mL/kg per hour", "en", Num(5, 7, "ml/kg/h")), ("15 ml/kg mỗi giờ", "vi", Num(15, 15, "ml/kg/h")),
    ("0,5 mg/kg mỗi ngày", "vi", Num(0.5, 0.5, "mg/kg/day")), ("0,5 mg/kg cân nặng/ngày", "vi", Num(0.5, 0.5, "mg/kg/day")),
    ("60mg/kg cân nặng/24 giờ", "vi", Num(60, 60, "mg/kg/day")), ("10 - 15mg/kg cân nặng/lần", "vi", Num(10, 15, "mg/kg")),
    ("10 mg/kg/h", "en", Num(10, 10, "mg/kg/h")),                   # grader 1.3.1: mg/kg/h is a unit (was mg/kg)
])
def test_unit_phrases_in_words(text, lang, want):
    assert parse_nums(text, lang)[0] == want


def test_amount_over_time_and_mg_per_day_untouched():
    assert parse_nums("15 ml/kg trong 1 giờ") == [Num(15, 15, "ml/kg"), Num(1, 1, "h")]
    assert parse_nums("10 mg mỗi ngày") == [Num(10, 10, "mg")]              # a daily dose of a per-dose atom: unchanged


@pytest.mark.parametrize("text,kept", [
    ("0,01 ml/kg dung dịch 1:1000", [Num(0.01, 0.01, "ml/kg")]),
    ("0.01 mL/kg of 1 mg/mL epinephrine", [Num(0.01, 0.01, "ml/kg")]),
    ("adrenalin 1‰ 0,01 ml/kg", [Num(0.01, 0.01, "ml/kg")]),
    ("1 ống 1mg/1ml", [Num(1, 1, "ampoule")]),
    ("dung dịch 1/10.000 1 ml/kg", [Num(1, 1, "ml/kg")]),
    ("0,5 mg in 0,5 mL", [Num(0.5, 0.5, "mg"), Num(0.5, 0.5, "ml")]),     # a dose and its volume: kept
    ("ép tim/thổi ngạt 30:2", [Num(30, 30), Num(2, 2)]),                  # other ratios: kept
])
def test_concentrations_dropped_only_on_request(text, kept):
    assert parse_nums(text, "en" if " of " in text else "vi", drop_concentrations=True) == kept
    assert len(parse_nums(text, "en" if " of " in text else "vi")) >= len(kept)   # default: unchanged


@pytest.mark.parametrize("text,lo,hi,unit", [
    ("nửa ống", 0.5, 0.5, "ampoule"), ("half an ampoule", 0.5, 0.5, "ampoule"), ("nửa ống đến 1 ống", 0.5, 1, "ampoule"),
    ("1/5 to 1/3 of an ampoule", 0.2, 1 / 3, "ampoule"), ("1 1/2 ống", 1.5, 1.5, "ampoule"), ("1½ ống", 1.5, 1.5, "ampoule"),
    ("3 years, 4 months", 40, 40, "month"), ("3 tuổi, 4 tháng", 40, 40, "month"), ("3 yrs 4 mos", 40, 40, "month"),
    ("3 tuổi rưỡi", 3.5, 3.5, "year"), ("3 tuổi 4 tháng – 5 tuổi", 40, 60, "month"),
    ("từ 3 tuổi 4 tháng đến 5 tuổi", 40, 60, "month"), ("18 tháng - 3 tuổi 4 tháng", 18, 40, "month"),
])
def test_more_one_value_forms(text, lo, hi, unit):
    n = parse_nums(text, "en" if text[0].isascii() and "tuổi" not in text and "tháng" not in text else "vi")
    assert len(n) == 1 and (n[0].lo, n[0].hi, n[0].unit) == (pytest.approx(lo), pytest.approx(hi), unit)


def test_plain_age_range_still_a_plain_range():
    assert parse_nums("4-6 tuổi") == [Num(4, 6, "year")]


@pytest.mark.parametrize("text,bp", [
    ("HA tâm trương ≥ 90 mmHg và/hoặc HA tâm thu ≥ 140 mmHg", BP(140, 90, ">=")),
    ("HATTh ≥ 140 mmHg và HATTr ≥ 90 mmHg", BP(140, 90, ">=")),
    ("HA ≥ 140 mmHg (tâm thu) và/hoặc ≥ 90 mmHg (tâm trương)", BP(140, 90, ">=")),
    ("≥80 mmHg diastolic or ≥130 mmHg systolic", BP(130, 80, ">=")),
])
def test_split_blood_pressure_more_forms(text, bp):
    assert parse_bps(text) == [bp]


def test_convert_day_hour():
    assert convert(1, "day", "h") == 24 and convert(48, "h", "day") == 2
    assert convert(1, "month", "day") is None                            # inexact: never guessed


SYN_TB = {"bedaquiline": ["bdq"], "linezolid": ["lzd"], "clofazimine": ["cfz"], "levofloxacin": ["lfx"],
          "prothionamide": ["pto"], "cycloserine": ["cycloserin", "~cs"], "amikacin": ["~am"], "ethambutol": ["~e"],
          "pyrazinamide": ["pza", "~z"], "isoniazid": ["inh", "~h", "~hh"],
          "tenofovir-disoproxil": ["tdf"], "lamivudine": ["3tc"], "dolutegravir": ["dtg"],
          "tenofovir-alafenamide": ["tenofovir alafenamid", "taf"]}


@pytest.mark.parametrize("text,names", [
    ("Bdq Lzd Cfz Cs", {"bedaquiline", "linezolid", "clofazimine", "cycloserine"}),
    ("4-6 Am(Km)-Lfx-Pto-Cfz-Z-H", {"amikacin", "levofloxacin", "prothionamide", "clofazimine", "pyrazinamide",
                                    "isoniazid"}),
    ("Bdq[6]-Lfx-Pto-E-Z-Hh-Cfz", {"bedaquiline", "levofloxacin", "prothionamide", "ethambutol", "pyrazinamide",
                                   "isoniazid", "clofazimine"}),
    ("Lfx Cfz Am", {"levofloxacin", "clofazimine"}),                     # only 2 other drugs: 'Am' not read
    ("Am", set()), ("Cs", set()),
    ("Lfx-Cfz-Pto âm tính", {"levofloxacin", "clofazimine", "prothionamide"}),   # 'âm' is never 'Am'
    ("HIV âm tính: TDF-3TC-DTG", {"tenofovir-disoproxil", "lamivudine", "dolutegravir"}),
    ("tenofovir-alafenamid", {"tenofovir-alafenamide"}),                 # space and hyphen interchangeable
])
def test_tb_chain_codes_and_alias_separators(text, names):
    assert parse_drugs(text, SYN_TB).names == frozenset(names)


def test_drug_repr_is_sorted():
    d = parse_drugs("DTG + 3TC + TDF", SYN_TB)
    assert repr(d) == "Drugs(names=frozenset({'dolutegravir', 'lamivudine', 'tenofovir-disoproxil'}))"


# ================================================================== grader 1.2.0 (26/9/2026, pre-freeze): parse level
def test_clean_keeps_powers_of_ten():
    from vnsoc.normalize_vi import clean

    assert clean("2×10³ IU/mL") == "2×10^3 IU/mL" and clean("10⁻³") == "10^-3"
    assert clean("23 kg/m²") == "23 kg/m2" and clean("1000 mm³") == "1000 mm3"   # unit exponents unchanged


@pytest.mark.parametrize("text,lang,want", [
    ("2 x 10^3 IU/mL", "en", Num(2000, 2000, "IU/mL")), ("2×10³ IU/mL", "en", Num(2000, 2000, "IU/mL")),
    ("2 · 10^3 IU/mL", "en", Num(2000, 2000, "IU/mL")), ("> 10^4 IU/mL", "en", Num(1e4, 1e4, "IU/mL", ">")),
    ("2.10^4 IU/mL", "vi", Num(2e4, 2e4, "IU/mL")), ("2,5.10^4 IU/mL", "vi", Num(2.5e4, 2.5e4, "IU/mL")),
    ("2,5 x 10^4 IU/mL", "vi", Num(2.5e4, 2.5e4, "IU/mL")), ("2.5 x 10^4 IU/mL", "en", Num(2.5e4, 2.5e4, "IU/mL")),
    ("2e3 IU/mL", "en", Num(2000, 2000, "IU/mL")), ("2E+03 IU/mL", "en", Num(2000, 2000, "IU/mL")),
    ("10^4 copies/mL", "en", Num(1e4, 1e4, "copies/mL")),             # own unit, never converted to IU/mL
    ("100 x 10^9/L", "en", Num(100, 100, "10^9/L")),                  # still the platelet unit
    ("150 × 10³/µL", "en", Num(1.5e5, 1.5e5, "/uL")),
])
def test_powers_of_ten(text, lang, want):
    assert parse_nums(text, lang) == [want]


def test_copies_are_not_iu():
    assert convert(1e4, "copies/mL", "IU/mL") is None


@pytest.mark.parametrize("text", ["23 kg/m^2", "23 kg/m²", "23 kg/m 2", "23 kg / m2", "23 kg per m2", "23 kg per m^2",
                                  "23 kg per square metre", "23 kg/sq m", "23 kg·m-2", "23 kg m−2"])
def test_bmi_unit_spellings(text):
    assert parse_nums(text, "en") == [Num(23, 23, "kg/m2")]


@pytest.mark.parametrize("text,lang,want", [
    ("0.5 mg base/kg/day", "en", Num(0.5, 0.5, "mg/kg/day")), ("0,5 mg base/kg/ngày", "vi", Num(0.5, 0.5, "mg/kg/day")),
    ("0.5 mg base/kg daily", "en", Num(0.5, 0.5, "mg/kg/day")), ("15 mg base", "en", Num(15, 15, "mg")),
    ("10 mg/kg once daily", "en", Num(10, 10, "mg/kg/day")), ("10 mg/kg once a day", "en", Num(10, 10, "mg/kg/day")),
    ("10 mg/kg 1 lần/ngày", "vi", Num(10, 10, "mg/kg/day")), ("10 mg/kg một lần mỗi ngày", "vi", Num(10, 10, "mg/kg/day")),
    ("18-month", "en", Num(18, 18, "month")), ("5-year-old", "en", Num(5, 5, "year")),
    ("7-day course", "en", Num(7, 7, "day")), ("30-minute", "en", Num(30, 30, "min")),
])
def test_unit_spellings_1_2_0(text, lang, want):
    assert parse_nums(text, lang) == [want]


@pytest.mark.parametrize("text,lang,want", [
    ("ba ngày", "vi", Num(3, 3, "day")), ("bảy ngày", "vi", Num(7, 7, "day")), ("hai tuần", "vi", Num(2, 2, "week")),
    ("mười lăm phút", "vi", Num(15, 15, "min")), ("hai mươi bốn giờ", "vi", Num(24, 24, "h")),
    ("hai mươi mốt ngày", "vi", Num(21, 21, "day")), ("ba mươi phút", "vi", Num(30, 30, "min")),
    ("một trăm năm mươi phút", "vi", Num(150, 150, "min")), ("năm ngày", "vi", Num(5, 5, "day")),
    ("mười năm", "vi", Num(10, 10, "year")), ("hai năm", "vi", Num(2, 2, "year")),
    ("three days", "en", Num(3, 3, "day")), ("seven days", "en", Num(7, 7, "day")), ("two weeks", "en", Num(2, 2, "week")),
    ("fifteen minutes", "en", Num(15, 15, "min")), ("twenty-four hours", "en", Num(24, 24, "h")),
    ("one hundred and fifty minutes", "en", Num(150, 150, "min")),
])
def test_numbers_in_words(text, lang, want):
    assert parse_nums(text, lang) == [want]


@pytest.mark.parametrize("text,lang,want", [
    ("100 mg twice daily", "en", [Num(100, 100, "mg"), Num(2, 2, "times/day")]),   # a frequency, never a dose
    ("10 mg/kg twice daily", "en", [Num(10, 10, "mg/kg"), Num(2, 2, "times/day")]),  # per dose: not a daily dose
    ("hai lần mỗi ngày", "vi", [Num(2, 2, "times/day")]),                # a frequency unit (dropped by the grader)
    ("(năm tuổi)", "vi", []),                                            # 'năm' = year here, not 5
    ("7 năm tuổi", "vi", [Num(7, 7, "year")]),
    ("15 phút, sau một giờ", "vi", [Num(15, 15, "min")]),                # 'một'/'one'/'a' yield to a real value
    ("15 minutes, after an hour", "en", [Num(15, 15, "min")]),
    ("một tuần", "vi", [Num(1, 1, "week")]), ("a week", "en", [Num(1, 1, "week")]),   # alone: read
    ("sau một tuần", "vi", [Num(1, 1, "week")]), ("Not sure; consult a doctor within a day", "en", []),  # hedge
    ("Không rõ, nên tái khám trong vòng một ngày", "vi", []),
    ("half an ampoule", "en", [Num(0.5, 0.5, "ampoule")]),               # not '1 ampoule'
])
def test_number_word_guards(text, lang, want):
    assert parse_nums(text, lang) == want


@pytest.mark.parametrize("text,lang,want", [
    ("9 tháng (mũi 1)", "vi", [Num(9, 9, "month")]), ("mũi 1 lúc 9 tháng", "vi", [Num(9, 9, "month")]),
    ("mũi thứ 2: 18 tháng", "vi", [Num(18, 18, "month")]), ("lần 1, 2 và 3 lúc 2, 3, 4 tháng", "vi",
                                                          [Num(2, 2), Num(3, 3), Num(4, 4, "month")]),
    ("Tiêm nhắc lại lần 2 sau 5 phút", "vi", [Num(5, 5, "min")]),
    ("9 months (MMR dose 1)", "en", [Num(9, 9, "month")]), ("Dose #2 at 4-6 years", "en", [Num(4, 6, "year")]),
    ("4–6 years (after the 18-month visit)", "en", [Num(4, 6, "year")]),
    ("7 tuổi (sau mũi 18 tháng)", "vi", [Num(7, 7, "year")]),
    ("At the 18-month visit", "en", [Num(18, 18, "month")]),             # a name alone is still read
    ("mũi 18 tháng", "vi", [Num(18, 18, "month")]),
    ("liều 2 mg", "vi", [Num(2, 2, "mg")]), ("2 liều", "vi", [Num(2, 2)]), ("liều 1-2 viên", "vi", [Num(1, 2, "tablet")]),
    ("liều 0,5 ml", "vi", [Num(0.5, 0.5, "ml")]), ("liều 2", "vi", [Num(2, 2)]),
])
def test_ordinals_yield_to_values(text, lang, want):
    assert parse_nums(text, lang) == want


@pytest.mark.parametrize("text,bp", [
    ("140 over 90 mmHg", BP(140, 90)), ("at least 130 over 80 mmHg", BP(130, 80, ">=")), ("140 trên 90 mmHg", BP(140, 90)),
    ("≥140/≥90 mmHg", BP(140, 90, ">=")), ("140/≥90", BP(140, 90, ">=")),
    ("140 và 90 mmHg", BP(140, 90)), ("HA 140 và 90", BP(140, 90)), ("≥ 130 and/or ≥ 80 mmHg", BP(130, 80, ">=")),
    ("130–139/80–89 mmHg", BP(130, 80, ">=")), ("140-159/90-99", BP(140, 90, ">=")),
    ("130-139 systolic or 80-89 diastolic", BP(130, 80, ">=")),
    ("tâm thu 140–159 và/hoặc tâm trương 90–99", BP(140, 90, ">=")),
    ("HA tâm thu ≥ 140 và/hay tâm trương ≥ 90", BP(140, 90, ">=")), ("tâm thu ≥ 140 hay tâm trương ≥ 90", BP(140, 90, ">=")),
    ("tâm thu ≥ 140 hoặc là tâm trương ≥ 90", BP(140, 90, ">=")),
])
def test_blood_pressure_forms_1_2_0(text, bp):
    assert parse_bps(text) == [bp]


@pytest.mark.parametrize("text", ["140 và 130 mmHg", "140 và 90", "140 hoặc 90 mmHg", "tâm thu 140-90 và tâm trương 90"])
def test_blood_pressure_word_guards(text):
    assert parse_bps(text) == []


CAT_OPTS = {"colloid": ["cao phan tu", r"\bcolloid", r"\bhes\b"], "crystalloid": ["ringer", r"\bnacl\b", r"\bsaline\b", "crystalloid"],
            "HRE": [r"(?<![a-z])hre(?![a-z])"], "HR": [r"(?<![a-z])hr(?![a-z])"]}


@pytest.mark.parametrize("text,labels", [
    ("Ringer lactate hoặc cao phân tử", {"colloid", "crystalloid"}),                    # both named: both kept
    ("Ringer lactate; nếu không đáp ứng chuyển cao phân tử", {"colloid", "crystalloid"}),
    ("cao phân tử, không dùng Ringer lactate", {"colloid"}), ("Ringer lactate, không dùng cao phân tử", {"crystalloid"}),
    ("cao phân tử thay vì Ringer", {"colloid"}), ("Ringer thay vì cao phân tử", {"crystalloid"}),
    ("colloid rather than crystalloid", {"colloid"}), ("crystalloid rather than colloid", {"crystalloid"}),
    ("colloid, not crystalloid", {"colloid"}), ("avoid colloid; use crystalloid", {"crystalloid"}),
    ("cao phân tử; Ringer lactate không được dùng", {"colloid"}), ("colloid; Ringer's lactate is not recommended", {"colloid"}),
    ("HES 6% in 0.9% saline", {"colloid"}), ("HES 6% pha trong NaCl 0,9%", {"colloid"}),   # a vehicle is no choice
    ("a 10 ml/kg bolus in Ringer lactate", {"crystalloid"}),                   # ... but only after another category
    ("4HRE chứ không phải 4HR", {"HRE"}), ("không dùng 4HR; dùng 4HRE", {"HRE"}),
    ("không có kháng thuốc: 4HRE", {"HRE"}), ("nếu không kháng isoniazid thì 4HR", {"HR"}),
    ("4HR, không dùng ethambutol", {"HR"}),
])
def test_cats_negated_or_vehicle_mentions(text, labels):
    assert parse_cats(text, CAT_OPTS).labels == labels


SYN_PA = dict(SYN_TB, pretomanid=["~Pa@2"], moxifloxacin=["mfx"], **{
    "bedaquiline+pretomanid+linezolid": ["bpal"], "bedaquiline+pretomanid+pyrazinamide": ["bpaz"],
    "bedaquiline+pretomanid+linezolid+moxifloxacin": ["bpalm"]})
BPAL = {"bedaquiline", "pretomanid", "linezolid"}


@pytest.mark.parametrize("text,names", [
    ("Bdq, Pa, Lzd", BPAL), ("Bdq-Pa-Lzd-Mfx", BPAL | {"moxifloxacin"}), ("B-Pa-L", BPAL), ("B Pa L", BPAL),
    ("B + Pa + L + M", BPAL | {"moxifloxacin"}), ("B-Pa-Z", {"bedaquiline", "pretomanid", "pyrazinamide"}),
    ("Or B-Pa-L", BPAL),
    ("Bdq Pa", {"bedaquiline"}), ("Pa", set()), ("X-quang PA, Bdq, Lzd", {"bedaquiline", "linezolid"}),
    ("H R Z E", set()),                                                   # spelled letters that are no regimen alias
])
def test_pretomanid_code_and_spelled_regimens(text, names):
    assert parse_drugs(text, SYN_PA).names == frozenset(names)


# ============================================ grader 1.2.0 after the independent grader review (26/9/2026, blind)
# Self-written strings only; each case is a regression test for one review finding (CHẶN-1..5, NÊN SỬA).
@pytest.mark.parametrize("text,lang,want", [
    # frequencies are one value in times/day|week (never a duration): digits, words and adverbs alike
    ("once a day", "en", [Num(1, 1, "times/day")]), ("once daily", "en", [Num(1, 1, "times/day")]),
    ("twice a day", "en", [Num(2, 2, "times/day")]), ("3 times a day", "en", [Num(3, 3, "times/day")]),
    ("three times daily", "en", [Num(3, 3, "times/day")]), ("3x/day", "en", [Num(3, 3, "times/day")]),
    ("twice weekly", "en", [Num(2, 2, "times/week")]),
    ("ngày một lần", "vi", [Num(1, 1, "times/day")]), ("ngày 1 lần", "vi", [Num(1, 1, "times/day")]),
    ("mỗi ngày uống 2 lần", "vi", [Num(2, 2, "times/day")]), ("1 lần/ngày", "vi", [Num(1, 1, "times/day")]),
    ("một lần mỗi ngày", "vi", [Num(1, 1, "times/day")]), ("2 lần mỗi tuần", "vi", [Num(2, 2, "times/week")]),
    # ... so 'a day' of 'once a day' is not 1 day, and the opening 'a week' is still read
    ("Primaquine once a day for a week", "en", [Num(1, 1, "times/day"), Num(1, 1, "week")]),
    ("Primaquin ngày một lần trong một tuần", "vi", [Num(1, 1, "times/day"), Num(1, 1, "week")]),
    ("3 days, once daily", "en", [Num(3, 3, "day"), Num(1, 1, "times/day")]),
    ("3 ngày 1 lần", "vi", [Num(3, 3, "day"), Num(1, 1, "times")]),          # 'every 3 days': not 'ngày 1 lần'
    # a bare count is a count in both languages; 'once' / 'một lần' alone are adverbs
    ("Repeat twice", "en", [Num(2, 2, "times")]), ("Nhắc lại hai lần", "vi", [Num(2, 2, "times")]),
    ("Repeat two times", "en", [Num(2, 2, "times")]), ("Nhắc lại 2 lần", "vi", [Num(2, 2, "times")]),
    ("Repeat once", "en", []), ("Nhắc lại một lần", "vi", []), ("once stable", "en", []),
    # a number word used as the unit of the number before it is not read again
    ("mười năm ngày", "vi", [Num(10, 10, "year")]),
])
def test_frequencies_and_counts(text, lang, want):
    assert parse_nums(text, lang) == want


@pytest.mark.parametrize("text,lang,want", [
    # CHẶN-4: a dose named by its age is a value unless it is introduced as a reference point
    ("the 9-month dose; some countries give it at 12 months", "en", [Num(9, 9, "month"), Num(12, 12, "month")]),
    ("mũi 9 tháng; một số nước tiêm lúc 12 tháng", "vi", [Num(9, 9, "month"), Num(12, 12, "month")]),
    ("9 months vaccine, or 12-15 months", "en", [Num(9, 9, "month"), Num(12, 15, "month")]),
    ("Mũi 18 tháng, hoặc 15 tháng", "vi", [Num(18, 18, "month"), Num(15, 15, "month")]),
    ("Booster at 7 years (after the 18-month dose)", "en", [Num(7, 7, "year")]),
    ("Mũi nhắc lại 7 tuổi (sau mũi 18 tháng)", "vi", [Num(7, 7, "year")]),
    ("7 years, following the 18 month booster", "en", [Num(7, 7, "year")]),
    ("7 tuổi, kể từ mũi 18 tháng", "vi", [Num(7, 7, "year")]),
])
def test_age_named_doses(text, lang, want):
    assert parse_nums(text, lang) == want


@pytest.mark.parametrize("text,lang,want", [
    # powers of ten: '*' as the times sign (was '210', the decoy 200 on a log scale); a range of powers; copies spellings
    ("> 2*10^3 IU/mL", "en", [Num(2000, 2000, "IU/mL", ">")]),
    ("HBV DNA 10^4–10^5 copies/mL", "en", [Num(1e4, 1e5, "copies/mL")]),      # was 10^4 read in the atom's IU/mL
    ("từ 10^4 đến 10^5 bản sao/mL", "vi", [Num(1e4, 1e5, "copies/mL")]),
    ("10^3 IU/mL - 10^4 IU/mL", "en", [Num(1e3, 1e4, "IU/mL")]),
    ("10^5 cps/mL", "en", [Num(1e5, 1e5, "copies/mL")]), ("10^5 copies per mL", "en", [Num(1e5, 1e5, "copies/mL")]),
    ("2000 IU per mL", "en", [Num(2000, 2000, "IU/mL")]),
    # English adjective between number and unit = Vietnamese adjective after the unit
    ("three consecutive days", "en", [Num(3, 3, "day")]), ("3 consecutive days", "en", [Num(3, 3, "day")]),
    ("ba ngày liên tiếp", "vi", [Num(3, 3, "day")]), ("a hundred days", "en", [Num(100, 100, "day")]),
    # 'năm' is 5 except in a unit hint or 'năm tuổi thứ N' ("năm tuổi" = "five years")
    ("năm tuổi", "vi", [Num(5, 5, "year")]), ("năm năm", "vi", [Num(5, 5, "year")]), ("(năm tuổi)", "vi", []),
    ("lúc 7 tuổi (năm tuổi thứ 7)", "vi", [Num(7, 7, "year"), Num(7, 7)]),
    # a source name before the opening 'một/one' does not count as words of its clause
    ("Theo Bộ Y tế: một tuần", "vi", [Num(1, 1, "week")]), ("According to the Vietnam MoH, one week", "en",
                                                          [Num(1, 1, "week")]),
    # 'đợt 1' = 'round 1', 'chu kỳ 1' = 'cycle 1' are ordinals
    ("9 months (round 1)", "en", [Num(9, 9, "month")]), ("9 tháng (đợt 1)", "vi", [Num(9, 9, "month")]),
    ("21 ngày (chu kỳ 1)", "vi", [Num(21, 21, "day")]), ("21 days (cycle 1)", "en", [Num(21, 21, "day")]),
])
def test_value_spellings_after_review(text, lang, want):
    assert parse_nums(text, lang) == want


@pytest.mark.parametrize("text", [
    "120–129/<80 mmHg", "Elevated BP 120-129/<80", "≥140/<90 mmHg",                  # range end; opposite comparators
    "tâm thu ≥ 140 và tâm trương < 90 mmHg", "SBP ≥ 140 and DBP < 90", "≥ 140 và < 90 mmHg"])
def test_blood_pressure_not_a_threshold_pair(text):
    assert parse_bps(text) == []


def test_fold_keeps_accents_aligned():
    from vnsoc.normalize_vi import _fold

    free, kept = _fold("Phác đồ CHỨA HRE; nó là 4HR (Bộ Y tế)")
    assert free == "phac do chua hre; no la 4hr (bo y te)" and len(kept) == len(free)
    assert kept == "phác đồ chứa hre; nó là 4hr (bộ y tế)"


FLUID_OPTS = {"colloid": [r"(?s)^(?!.*(?:khong dung|not)\s+(?:cao phan tu|colloid|dextran|\bhes\b))"
                          r".*(?:cao phan tu|colloid|dextran|\bhes\b|starch|gelatin)"],        # anchored, whole answer
              "crystalloid": ["ringer", r"\bnacl\b", r"\bsaline\b", "crystalloid"]}
YES_NO_OPTS = {"no": [r"^\s*(?:khong|no)\b"], "yes": [r"^\s*(?:co|yes)\b"]}


@pytest.mark.parametrize("text,opts,labels", [
    # CHẶN-1: a yes/no answer word is never negated by what follows (P-dengue-04)
    ("Không - metamizol không nên dùng", YES_NO_OPTS, {"no"}), ("No — metamizole is not recommended", YES_NO_OPTS, {"no"}),
    ("Không vì metamizol không được dùng", YES_NO_OPTS, {"no"}), ("No metamizole should be avoided", YES_NO_OPTS, {"no"}),
    ("Có - gelatin có thể dùng", YES_NO_OPTS, {"yes"}),
    # CHẶN-2: an anchored whole-answer pattern across clauses stands unless its only mention is dismissed
    ("Colloid (dextran 40); HES is not recommended", FLUID_OPTS, {"colloid"}),
    ("Dextran 40 (HES không được khuyến cáo)", FLUID_OPTS, {"colloid"}),
    ("Cao phân tử, HES không nên dùng", FLUID_OPTS, {"colloid"}),
    ("Colloid such as gelatin; starches should be avoided", FLUID_OPTS, {"colloid"}),
    ("Dextran 40 không được khuyến cáo", FLUID_OPTS, set()), ("Ringer lactate không được khuyến cáo", FLUID_OPTS, set()),
    ("Truyền dịch; HES không được dùng", FLUID_OPTS, set()),
    ("Truyền dịch; Ringer lactate không được dùng", FLUID_OPTS, set()),
    ("HES không được dùng; dùng Ringer lactate", FLUID_OPTS, {"crystalloid"}),
    ("Ringer lactate không được dùng; dùng HES", FLUID_OPTS, {"colloid"}),
    # CHẶN-3: accents are kept for the negation words ('chứa' is not 'chưa', 'nó' is not 'no')
    ("Phác đồ chứa HRE", CAT_OPTS, {"HRE"}), ("Phác đồ duy trì chứa 4HR", CAT_OPTS, {"HR"}),
    ("Dung dịch có chứa Ringer lactate", CAT_OPTS, {"crystalloid"}),
    ("Truyền Ringer lactate vì nó là dịch đẳng trương", CAT_OPTS, {"crystalloid"}),
    ("chưa dùng 4HR; dùng 4HRE", CAT_OPTS, {"HRE"}), ("4HRE, bỏ 4HR", CAT_OPTS, {"HRE"}),
    ("khong dung 4HR; dung 4HRE", CAT_OPTS, {"HRE"}), ("Phac do chua HRE", CAT_OPTS, {"HRE"}),   # no diacritics
    ("Bo Y te: 4HRE", CAT_OPTS, {"HRE"}),
    # mention patterns read one sentence or ';'-clause (P-dengue-06 not_used crossed a ';')
    ("gelatin có thể dùng; không dùng albumin", {"sub": ["gelatin[^.]{0,40}co the dung"],
                                               "not": ["gelatin[^.]{0,40}khong dung"]}, {"sub"}),
    # the vehicle's clause keeps parentheses
    ("Cao phân tử (Dextran 40) pha trong NaCl 0,9%", CAT_OPTS | {"colloid": ["cao phan tu", "dextran"]}, {"colloid"}),
])
def test_cat_mentions_after_review(text, opts, labels):
    assert parse_cats(text, opts).labels == labels


def test_anchored_pattern_reread_is_bounded():
    # a degenerate (repeated) output: at most _MAX_CLAUSES clauses are re-read, then the pattern's reading stands
    from vnsoc.normalize_vi import _MAX_CLAUSES

    assert parse_cats("Truyền dịch; " + "HES không được dùng; " * 10, FLUID_OPTS).labels == set()
    assert parse_cats("Truyền dịch; " + "HES không được dùng; " * (_MAX_CLAUSES + 5), FLUID_OPTS).labels == {"colloid"}


# ================================================================== grader 1.3.0 (27/9/2026, pre-freeze; self-written)
from vnsoc.normalize_vi import cat_mentioned, clean, drug_leaves, join_tb_letters  # noqa: E402


@pytest.mark.parametrize("text,want", [
    ("5 <unit>", "5"), ("0,5 <đơn vị> mg", "0,5 mg"), ("<giá trị> 20 ml/kg/giờ", "20 ml/kg/giờ"),
    ("<b>140</b>/<b>90</b>", "140 / 90"), ("3 <times> /ULN", "3 x ULN"),
    ("1 /ULN", "1 x ULN"), ("2 lần /ULN", "2 x ULN"), ("2x/ULN", "2 x ULN"), ("2 times / ULN", "2 x ULN"),
    ("1,5 /ULN", "1,5 x ULN"),
    # untouched: comparisons, numbers inside brackets, a ratio without a number, ranges with '<'
    ("< 140 và > 90", "< 140 và > 90"), ("<5 tuổi>", "<5 tuổi>"), ("120-129/<80", "120-129/<80"),
    ("ALT/ULN 2", "ALT/ULN 2"), ("tuổi <5 hoặc >10", "tuổi <5 hoặc >10"),
])
def test_clean_placeholders_and_uln_slash(text, want):
    assert clean(text) == want


@pytest.mark.parametrize("text,bp", [
    ("140 mmHg / 90 mmHg", BP(140, 90)), ("≥ 130 mmHg/≥ 80 mmHg", BP(130, 80, ">=")), ("140 mmHg over 90", BP(140, 90)),
    ("140 90 mmHg", BP(140, 90)), ("130 mmHg 80 mmHg", BP(130, 80)), ("HA 150 100", BP(150, 100)),
    ("BP ≥ 140 ≥ 90", BP(140, 90, ">=")), ("blood pressure 130 80", BP(130, 80)),
])
def test_blood_pressure_unit_per_part_and_space_1_3_0(text, bp):
    assert parse_bps(text) == [bp]


@pytest.mark.parametrize("text", [
    "140 90",                                   # no mmHg, no BP word: two numbers, not read
    "130-139 80-89 mmHg", "140 90-99 mmHg",     # range ends
    "130 120 mmHg", "160 140 mmHg",             # implausible pair (difference < 20, diastolic > 130)
    "≥ 140 < 90 mmHg",                          # opposite comparators
    "tuổi 60 80 mmHg",
])
def test_blood_pressure_space_guards(text):
    assert parse_bps(text) == []


def test_blood_pressure_words_between_numbers_unchanged():
    assert parse_bps("140 over 90 mmHg") == [BP(140, 90)]                   # BP_RE, no comparator
    assert parse_bps("140 hoặc 90 mmHg") == []


@pytest.mark.parametrize("text,want", [
    ("R H E", "RHE"), ("4 R H E", "4 RHE"), ("R-H-E", "RHE"), ("H R Z E", "HRZE"), ("2HRZE/4R H E", "2HRZE/4RHE"),
    ("r h e", "r h e"),                          # capitals only
    ("vitamin E", "vitamin E"), ("HR 80", "HR 80"), ("HA R", "HA R"), ("E. coli", "E. coli"),
])
def test_join_tb_letters(text, want):
    assert join_tb_letters(text) == want


def test_tb_letters_in_cats():
    opts = {"HRE": [r"(?<![a-z0-9])(?:hre|rhe)(?![a-z])"], "HR": [r"(?<![a-z0-9])(?:hr|rh)(?![a-z])"]}
    assert parse_cats("R H E", opts).labels == {"HRE"}
    assert parse_cats("R H", opts).labels == {"HR"}
    assert parse_cats("không dùng R H E", opts).labels == frozenset()       # negation reads the joined code too


def test_cat_mentioned_reads_negated_mentions():
    opts = {"colloid": [r"\bhes\b", "dextran"], "crystalloid": ["ringer"]}
    assert cat_mentioned("Dextran 40 không được khuyến cáo", opts)
    assert cat_mentioned("HES", opts) and not cat_mentioned("500 ml/giờ", opts)


def test_drug_leaves():
    combos = {"BPaL": ["bedaquiline", "pretomanid", "linezolid"], "artemether-lumefantrine": ["artemether", "lumefantrine"]}
    cls = "tenofovir-disoproxil|tenofovir-alafenamide"
    assert drug_leaves({"BPaL", "quinine+clindamycin"}, combos) == {"bedaquiline", "pretomanid", "linezolid", "quinine",
                                                                   "clindamycin"}
    assert drug_leaves({"artemether-lumefantrine"}, combos) == {"artemether", "lumefantrine"}
    assert drug_leaves({cls}, combos) == {cls}
    assert drug_leaves({cls}, combos, classes="members") == {"tenofovir-disoproxil", "tenofovir-alafenamide"}


# ------------------------------------------------------------------ grader 1.3.0 after the independent review
SYN_MINI = {"tenofovir-disoproxil": ["tdf"], "lamivudine": ["3tc"], "dolutegravir": ["dtg"], "efavirenz": ["efv"],
            "nevirapine": ["nvp"], "entecavir": ["etv"], "emtricitabine": ["ftc"], "pyrazinamide": ["pyrazinamid"],
            "ethambutol": [], "tenofovir-disoproxil+lamivudine+dolutegravir": ["tld"],
            "tenofovir-disoproxil+lamivudine+efavirenz": ["tle"]}


@pytest.mark.parametrize("text,names,joined", [
    ("TDF + 3TC + DTG (không dùng EFV)", {"tenofovir-disoproxil", "lamivudine", "dolutegravir"}, True),
    ("TDF + 3TC + DTG, not EFV", {"tenofovir-disoproxil", "lamivudine", "dolutegravir"}, True),
    ("TLD instead of TLE", {"tenofovir-disoproxil", "lamivudine", "dolutegravir"}, False),
    ("TLE instead of TLD", {"tenofovir-disoproxil", "lamivudine", "efavirenz"}, False),
    ("không dùng EFV hoặc NVP; TDF + 3TC + DTG", {"tenofovir-disoproxil", "lamivudine", "dolutegravir"}, True),
    ("EFV or NVP should be avoided", set(), False),
    ("không dùng EFV, TDF + 3TC + DTG", {"tenofovir-disoproxil", "lamivudine", "dolutegravir"}, True),
    ("stop pyrazinamide and ethambutol", set(), False), ("ngừng pyrazinamid và ethambutol", set(), False),
    ("TDF + ETV", {"tenofovir-disoproxil", "entecavir"}, True), ("TDF hoặc ETV", {"tenofovir-disoproxil", "entecavir"}, False),
    ("TDF, ETV", {"tenofovir-disoproxil", "entecavir"}, False), ("TDF and ETV", {"tenofovir-disoproxil", "entecavir"}, False),
    ("TDF + 3TC (hoặc FTC) + DTG", {"tenofovir-disoproxil", "lamivudine", "emtricitabine", "dolutegravir"}, False),
    ("TDF + 3TC. DTG", {"tenofovir-disoproxil", "lamivudine", "dolutegravir"}, False),
    ("chứa TDF", {"tenofovir-disoproxil"}, False),                     # 'chứa' (contains) is not 'chưa'
])
def test_stated_drugs_text(text, names, joined):
    from vnsoc.normalize_vi import stated_drugs_text

    stated, j = stated_drugs_text(text, SYN_MINI)
    assert (set(parse_drugs(stated, SYN_MINI).names), j) == (names, joined)


@pytest.mark.parametrize("text,codes", [
    ("HRZE", ["HRZE"]), ("E H R", ["EHR"]), ("2HRZE/4HR", ["2HRZE", "4HR"]), ("RHZ", ["RHZ"]),
    ("HR", []), ("HRR", []), ("HER2", []), ("không dùng HRZE", []), ("hrze", []), ("ESR", ["ESR"]),
])
def test_tb_codes(text, codes):
    from vnsoc.normalize_vi import tb_codes

    assert [m.group(0) for m in tb_codes(text)[1]] == codes


@pytest.mark.parametrize("text,bp", [
    ("≥140 mmHg or ≥90 mmHg", BP(140, 90, ">=")), ("≥ 130 mmHg hoặc ≥ 80 mmHg", BP(130, 80, ">=")),
    ("140 by 90 mmHg", BP(140, 90)), ("130-139 mmHg / 80-89 mmHg", BP(130, 80, ">=")),
    ("SBP 140 mmHg, 90 mmHg DBP", BP(140, 90)), ("90 mmHg DBP, SBP 140 mmHg", BP(140, 90)),
])
def test_blood_pressure_forms_after_review(text, bp):
    assert parse_bps(text) == [bp]


@pytest.mark.parametrize("text", ["140 mmHg hoặc 150 mmHg", "140 or 90", "≥ 140 mmHg or < 90 mmHg",
                                  "HA tâm thu ≥ 140 mmHg 30 phút sau nghỉ", "SBP 140 mmHg, 150 mmHg DBP"])
def test_no_blood_pressure_after_review(text):
    assert parse_bps(text) == []


# ================================================================== grader 1.3.1: reader inventory of the corpus
# Strings are SELF-WRITTEN, modelled on the wording of the 25 corpus documents (source in the comment); no model output.
# Inventory: review/extraction_calibration/reader_inventory.md.
@pytest.mark.parametrize("text,want", [
    ("Thở oxy cannula 2-6 lít/phút", Num(2, 6, "L/min")),                                   # 1019/2025 tr.15
    ("oxy 8-10l/ph", Num(8, 10, "L/min")), ("6 l/min", Num(6, 6, "L/min")),                  # 3610/2015
    ("Áp lực: 4 - 6 cm H2O", Num(4, 6, "cmH2O")), ("tối đa 10 cmH2O", Num(10, 10, "cmH2O", "<=")),
    ("PEEP 5 cmH₂O", Num(5, 5, "cmH2O")),                                                     # subscript digit
    ("IgG < 3g/L", Num(3, 3, "g/L", "<")), ("albumin < 30 g/L", Num(30, 30, "g/L", "<")),    # 1019/2025, 2388/2024
    ("Hb < 13,0 g/dL", Num(13, 13, "g/dL", "<")), ("CRP > 100 mg/L", Num(100, 100, "mg/L", ">")),
    ("đường huyết > 160 mg%", Num(160, 160, "mg/dL", ">")),                                   # 292/2024
    ("creatinin 26,5 µmol/L", Num(26.5, 26.5, "umol/L")), ("26,5 umol/l", Num(26.5, 26.5, "umol/L")),
    ("Natri máu < 125mEq/l", Num(125, 125, "mEq/L", "<")),                                    # 2760/2023
    ("không quá 0,5 mEq/l/giờ", Num(0.5, 0.5, "mEq/L/h", "<=")),                              # 1019/2025 tr.15
    ("tăng 8 - 10 mmol/L/24 giờ", Num(8, 10, "mmol/L/day")), ("0,5 mmol/L/giờ", Num(0.5, 0.5, "mmol/L/h")),
    ("sốt > 38,5oC", Num(38.5, 38.5, "°C", ">")), ("trên 39°C", Num(39, 39, "°C", ">")),     # 1019/2025, 162/2024
    ("37,5 - 38 độ C", Num(37.5, 38, "°C")), ("Đầu cao 30°", Num(30, 30, "°")),              # 2760/2023
    ("nằm đầu cao 30 độ", Num(30, 30, "°")), ("39 °F", Num(39, 39, "°F")),
    ("Dobutamine 2 – 20 µg/kg/min", Num(2, 20, "ug/kg/min")),                                  # 1857/2022 Bảng 8
    ("0,1 - 0,3 µg/kg/phút", Num(0.1, 0.3, "ug/kg/min")), ("0,1 mcg/kg/ph", Num(0.1, 0.1, "ug/kg/min")),
    ("0,05 mcg/kg/phút", Num(0.05, 0.05, "ug/kg/min")), ("1 µg/kg/giờ", Num(1, 1, "ug/kg/h")),
    ("20 mg/kg/giờ", Num(20, 20, "mg/kg/h")), ("5 mg/phút", Num(5, 5, "mg/min")), ("10 mg/giờ", Num(10, 10, "mg/h")),
    ("truyền 20 ml/giờ", Num(20, 20, "ml/h")), ("nước tiểu ≥ 100 mL/h", Num(100, 100, "ml/h", ">=")),
    ("5 ml/kg/phút", Num(5, 5, "ml/kg/min")), ("20 giọt/phút", Num(20, 20, "drops/min")),
    ("0,1 đơn vị/kg/giờ", Num(0.1, 0.1, "IU/kg/h")), ("0,1 UI/kg/h", Num(0.1, 0.1, "IU/kg/h")),  # 5481/2020 DKA
    ("insulin 4 đơn vị/giờ", Num(4, 4, "IU/h")), ("50 UI/kg", Num(50, 50, "IU/kg")),
    ("nhịp thở trên 30 lần/phút", Num(30, 30, "/min", ">")), ("> 70 ck/phút", Num(70, 70, "/min", ">")),
    ("nhịp tim 60 nhịp/phút", Num(60, 60, "/min")),                                           # 162/2024, 1857/2022
    ("MLCT < 30 ml/phút/1,73m2", Num(30, 30, "mL/min/1.73m2", "<")),                          # 2388/2024
    ("eGFR ≥ 60 ml/phút/1,73 m2", Num(60, 60, "mL/min/1.73m2", ">=")),
    ("eGFR < 30 mL/min/1.73 m2", Num(30, 30, "mL/min/1.73m2", "<")), ("CrCl < 50 ml/ph", Num(50, 50, "ml/min", "<")),
    ("giảm > 5 ml/phút/năm", Num(5, 5, "mL/min/year", ">")),
    ("CD4 < 200 tế bào/mm3", Num(200, 200, "/uL", "<")), ("CD4 dưới 100 tb/mm3", Num(100, 100, "/uL", "<")),
    ("Tiểu cầu < 100 G/L", Num(100, 100, "10^9/L", "<")), ("Bạch cầu < 4 G/l", Num(4, 4, "10^9/L", "<")),  # 3312, 5642
    ("QRS ≥ 150 ms", Num(150, 150, "ms", ">=")), ("nín thở 10 giây", Num(10, 10, "s")),
    ("UACR ≥ 30 mg/g", Num(30, 30, "mg/g", ">=")), ("ACR > 3 mg/mmol", Num(3, 3, "mg/mmol", ">")),
    ("NT-proBNP ≥ 125 pg/mL", Num(125, 125, "pg/mL", ">=")), ("ferritin < 100 µg/L", Num(100, 100, "ug/L", "<")),
    ("áp lực thẩm thấu > 320 mOsm/kg", Num(320, 320, "mOsm/kg", ">")),
    ("giảm ≥ 1 log10 IU/mL", Num(1, 1, "log10 IU/mL", ">=")),
    ("10 - 15 kcal/kg", Num(10, 15, "kcal/kg")), ("25 kcal/kg/ngày", Num(25, 25, "kcal/kg/day")),
    ("giảm 2 - 3 kg/tháng", Num(2, 3, "kg/month")),                                           # 2892/2022
    ("tối thiểu 5 ngày/tuần", Num(5, 5, "days/week", ">=")), ("150 phút/tuần", Num(150, 150, "min/week")),
    ("30 phút/ngày", Num(30, 30, "min/day")),
    ("tăng 1 lần/năm", Num(1, 1, "times/year")), ("2 liều/ngày", Num(2, 2, "times/day")),
    ("1‰", Num(1, 1, "‰")), ("xịt 2 nhát", Num(2, 2, "puff")), ("1 gói", Num(1, 1, "sachet")),
    ("vòng bụng ≥ 90 cm", Num(90, 90, "cm", ">=")), ("hạt Koplik 0,5 - 1 mm", Num(0.5, 1, "mm")),
    ("≥ 95th percentile", Num(95, 95, "percentile", ">=")),
    ("IVIG 0,25 g/kg/ngày", Num(0.25, 0.25, "g/kg/day")), ("0,5 - 1 g/kg", Num(0.5, 1, "g/kg")),
    ("muối dưới 5g/ngày", Num(5, 5, "g/day", "<")), ("2 g/24 giờ", Num(2, 2, "g/day")),        # 2892/2022
    ("NVP 200 mg/m2", Num(200, 200, "mg/m2")), ("700 mg/m2/24h", Num(700, 700, "mg/m2/day")),
    ("vitamin A 200.000 UI/ngày", Num(200000, 200000, "IU/day")),
    ("2 viên/ngày", Num(2, 2, "tablet/day")), ("2 viên/ ngày", Num(2, 2, "tablet/day")),
    ("Benzathin penicillin 2,4 triệu đơn vị", Num(2.4, 2.4, "MIU")), ("2,4 triệu U", Num(2.4, 2.4, "MIU")),  # 678, 5968
    ("Penicilin G 2 MIU", Num(2, 2, "MIU")),                                                  # 2147/2026
    ("1 lan/ngay", Num(1, 1, "times/day")), ("< 12 tuôi", Num(12, 12, "year", "<")),           # no diacritics / OCR
    ("2 vién/ngay", Num(2, 2, "tablet/day")),                                                 # 3377/2023 OCR
])
def test_units_of_the_corpus(text, want):
    got = parse_nums(text, "vi")
    assert got[0] == want, got


@pytest.mark.parametrize("variants,want", [
    (["60mg/ngày", "60mg/ ngày", "60 mg /ngày", "60 mg / ngày", "60 mg/ngày"], Num(60, 60, "mg/day")),    # 1840/2025
    (["10 mg/kg/ngày", "10 mg/kg/ ngày", "10 mg / kg / ngày"], Num(10, 10, "mg/kg/day")),
    (["2 lần/ngày", "2 lần/ ngày", "2 lần /ngày"], Num(2, 2, "times/day")),
    (["1 lần/tuần", "1 lần/ tuần"], Num(1, 1, "times/week")),
    (["5 ml/giờ", "5 ml/ giờ", "5 ml / giờ"], Num(5, 5, "ml/h")),
])
def test_space_around_slash_is_read(variants, want):
    for v in variants:
        assert parse_nums(v, "vi") == [want], v


@pytest.mark.parametrize("text,lang,want", [
    ("500 mg/lần", "vi", Num(500, 500, "mg")), ("10 mg/kg/lần", "vi", Num(10, 10, "mg/kg")),   # per dose
    ("15 mg/kg/liều", "vi", Num(15, 15, "mg/kg")), ("100 mcg/liều", "vi", Num(100, 100, "ug")),
    ("75mg/ngày", "vi", Num(75, 75, "mg/day")), ("0,125 mg/24h", "vi", Num(0.125, 0.125, "mg/day")),  # per day
    ("8 giờ/lần", "vi", Num(8, 8, "h")), ("3 tháng/lần", "vi", Num(3, 3, "month")),              # an interval
    ("500 mg/12h", "vi", Num(500, 500, "mg")),                                                  # dose + interval
    ("50 mg daily", "en", Num(50, 50, "mg")),     # known limitation (unchanged): 'daily' alone does not make mg/day
])
def test_per_dose_and_per_day_forms(text, lang, want):
    assert parse_nums(text, lang)[0] == want


@pytest.mark.parametrize("frm,to,ctx,value,want", [
    ("g/L", "mmol/L", {"analyte": "glucose"}, 1.26, 1260 / 10 / 18.016),        # glucose 1,26 g/l = 7 mmol/L
    ("mg/dL", "umol/L", {"analyte": "creatinine"}, 1.0, 88.4),                  # creatinine 113.12 g/mol
    ("mEq/L", "mmol/L", {"analyte": "sodium"}, 125, 125), ("mEq/L/h", "mmol/L/h", {"analyte": "sodium"}, 0.5, 0.5),
    ("mEq/L", "mmol/L", {"analyte": "magnesium"}, 4, 2),                        # divalent
    ("g/dL", "g/L", {}, 13, 130), ("mg/L", "mg/dL", {}, 100, 10), ("ug/mL", "mg/L", {}, 5, 5),
    ("ng/mL", "ug/L", {}, 100, 100), ("pg/mL", "ng/L", {}, 125, 125), ("umol/L", "mmol/L", {}, 300, 0.3),
    ("L/min", "ml/min", {}, 2, 2000), ("ml/min", "ml/h", {}, 1, 60), ("ml/day", "ml/h", {}, 2400, 100),
    ("ug/kg/min", "mg/kg/h", {}, 5, 0.3), ("ug/kg/min", "ug/min", {"weight_kg": 70}, 0.1, 7),
    ("mg/kg/h", "mg/kg/day", {}, 1, 24), ("g/day", "mg/day", {}, 2, 2000), ("mmol/L/day", "mmol/L/h", {}, 12, 0.5),
    ("mg", "mg/day", {"doses_per_day": 1}, 75, 75), ("mg", "mg/day", {"doses_per_day": 2}, 500, 1000),
    ("tablet/day", "mg/day", {"mg_per_tablet": 300}, 2, 600), ("MIU", "IU", {}, 2.4, 2.4e6),
    ("‰", "%", {}, 1, 0.1), ("°", "°C", {}, 38.5, 38.5), ("mm", "cm", {}, 10, 1), ("s", "min", {}, 30, 0.5),
    ("ms", "s", {}, 150, 0.15),
])
def test_exact_conversion_edges(frm, to, ctx, value, want):
    assert convert(value, frm, to, ctx) == pytest.approx(want, rel=1e-3)


@pytest.mark.parametrize("frm,to,ctx", [
    ("mg", "mg/day", {}),                          # per dose -> per day only with the atom's doses_per_day
    ("mEq/L", "mmol/L", {}),                       # valence depends on the analyte
    ("mg/dL", "umol/L", {}),                       # molar mass depends on the analyte
    ("cmH2O", "mmHg", {}), ("°F", "°C", {}),       # not a factor / affine scale
    ("ml/min", "mL/min/1.73m2", {}),               # clearance vs eGFR normalised to 1.73 m2: different quantities
    ("days/week", "times/week", {}), ("min/day", "min/week", {}), ("kg/month", "kg/week", {}),
    ("mL/min/1.73m2/year", "mL/min/1.73m2", {}),   # a slope is not a level
    ("drops/min", "ml/h", {}), ("mg/g", "mg/mmol", {}), ("IU/day", "IU", {}),
])
def test_no_inexact_conversion(frm, to, ctx):
    assert convert(1.0, frm, to, ctx) is None


@pytest.mark.parametrize("text,want", [
    ("0,0625 mg", [Num(0.0625, 0.0625, "mg")]),                                  # 1857/2022: digoxin 62,5 µg
    ("Sacubitril/valsartan 49/51 mg", [Num(49, 49, "mg"), Num(51, 51, "mg")]),     # 1857/2022 Bảng 6
    ("Hydralazine/ISDN 37.5mg/20mg", [Num(37.5, 37.5, "mg"), Num(20, 20, "mg")]),
    ("TDF/3TC/DTG 300/300/50 mg", [Num(300, 300, "mg"), Num(300, 300, "mg"), Num(50, 50, "mg")]),
    ("co-trimoxazol 800/160 mg", [Num(800, 800, "mg"), Num(160, 160, "mg")]),
    ("250 mg/5 ml", [Num(250, 250, "mg")]),                                        # a concentration: not a pair
    ("Tăng huyết áp 140/90 mmHg", [Num(140, 140, None)]),                          # not a dose pair (parse_bps)
    ("liều 3.125 mg", [Num(3125, 3125, "mg")]),     # known limitation: Vietnamese '.' + 3 digits = thousands
    ("có 4 triệu chứng", [Num(4, 4, None)]),                                       # bare 'triệu' is not a unit
])
def test_numbers_and_dose_pairs(text, want):
    assert parse_nums(text, "vi") == want


def test_units_of_the_pilot_style_are_unchanged():
    """Readings that existed before 1.3.1 stay (regression)."""
    for text, want in [("15 ml/kg/giờ", Num(15, 15, "ml/kg/h")), ("0,01 mg/kg", Num(0.01, 0.01, "mg/kg")),
                       ("100.000/mm3", Num(100000, 100000, "/uL")), ("2 lần/ngày", Num(2, 2, "times/day")),
                       ("≥ 7,0 mmol/L", Num(7, 7, "mmol/L", ">=")), ("100 × 10^9/L", Num(100, 100, "10^9/L")),
                       ("25 kg/m2", Num(25, 25, "kg/m2")), ("2.000 IU/mL", Num(2000, 2000, "IU/mL")),
                       ("3 tuổi 4 tháng", Num(40, 40, "month")), ("0,15 mg", Num(0.15, 0.15, "mg"))]:
        assert parse_nums(text, "vi")[0] == want, text


# ------------------------------------------------------------------ 1.3.1 drug table (configs/grading.yaml)
def _cfg_tables():
    from vnsoc.extract.verify_span import drug_tables

    return drug_tables()


@pytest.mark.parametrize("text,names", [
    ("Kháng sinh ban đầu: Amoxicillin hoặc Amoxicillin-acid clavulanic uống", {"amoxicillin", "amoxicillin-clavulanate"}),
    ("Amoxicillin – acid clavulanic (Uống) hoặc Cefotaxim hoặc Ceftriaxon (TM)",
     {"amoxicillin-clavulanate", "cefotaxime", "ceftriaxone"}),                                   # 1019/2025 tr.14
    ("amoxicillin + acid clavulanic", {"amoxicillin-clavulanate"}),                               # combos collapse
    ("co-amoxiclav", {"amoxicillin-clavulanate"}), ("Amx-Clv", {"amoxicillin-clavulanate"}),
    ("Ciprofloxacin hoặc Ofloxacin hoặc Levofloxacin", {"ciprofloxacin", "ofloxacin", "levofloxacin"}),
    ("Oxacillin (TM) hoặc Cloxacillin (TM) hoặc Vancomycin (TM)", {"oxacillin", "cloxacillin", "vancomycin"}),
    ("Nystatin uống", {"nystatin"}), ("Chống co giật: Diazepam", {"diazepam"}),
    ("Natriclorua 3% hoặc Mannitol 20%", {"sodium-chloride", "mannitol"}),
    ("Paracetamol hoặc Ibuprofen", {"paracetamol", "ibuprofen"}), ("Oresol", {"oral-rehydration-salts"}),
    ("sacubitril/valsartan", {"sacubitril-valsartan"}), ("sacubitril + valsartan", {"sacubitril-valsartan"}),
    ("ARNI", {"sacubitril-valsartan"}), ("valsartan", {"valsartan"}),
    ("dapagliflozin hoặc empagliflozin", {"dapagliflozin", "empagliflozin"}),                     # 1857/2022 tr.12
    ("carvedilol, metoprolol succinat, bisoprolol, nebivolol", {"carvedilol", "metoprolol", "bisoprolol", "nebivolol"}),
    ("furosemid", {"furosemide"}), ("Noradrenalin ưu thế hơn dopamin", {"noradrenaline", "dopamine"}),
    ("orlistat và liraglutide 3,0 mg", {"orlistat", "liraglutide"}),                              # 2892/2022 tr.16
    ("Oseltamivir hoặc zanamivir hoặc baloxavir marboxil", {"oseltamivir", "zanamivir", "baloxavir"}),  # 1840/2025
    ("sulfamethoxazol + trimethoprim", {"co-trimoxazole"}), ("Cotrimoxazole", {"co-trimoxazole"}),
    ("Ipm-Cln hoặc Mpm", {"imipenem", "meropenem"}), ("imipenem/cilastatin", {"imipenem"}),
    ("4-6 Km-Lfx-Pto-Cfz-Z-H", {"kanamycin", "levofloxacin", "prothionamide", "clofazimine", "pyrazinamide",
                                "isoniazid"}),
    ("Magie sulphat 4 g", {"magnesium-sulfate"}), ("MgSO4 15%", {"magnesium-sulfate"}),           # 1154/2024
    ("labetalol hoặc nifedipin hoặc hydralazin", {"labetalol", "nifedipine", "hydralazine"}),
    ("Calcium gluconate 10%", {"calcium-gluconate"}), ("kali chloride (KCl)", {"potassium-chloride"}),
    ("natri bicarbonate uống", {"sodium-bicarbonate"}),
    ("than hoạt + sorbitol", {"activated-charcoal", "sorbitol"}), ("PAM và atropin", {"pralidoxime", "atropine"}),
    ("N-acetylcystein", {"acetylcysteine"}), ("Naloxon 0,4mg", {"naloxone"}),
    ("xanh methylen", {"methylthioninium-chloride"}), ("huyết thanh kháng nọc rắn", {"snake-antivenom"}),
    ("CaNa2EDTA", {"sodium-calcium-edetate"}), ("Vitamin A", {"retinol"}), ("vitamin K1", {"phytomenadione"}),
    ("Pyridoxine (vitamin B6)", {"pyridoxine"}),
    ("SOF/VEL", {"sofosbuvir", "velpatasvir"}), ("SOF/DAC", {"sofosbuvir", "daclatasvir"}),       # 2855/2024
    ("SOF/LED", {"sofosbuvir", "ledipasvir"}), ("Epclusa", {"sofosbuvir", "velpatasvir"}),
    ("3HP", {"isoniazid", "rifapentine"}), ("Berodual", {"fenoterol", "ipratropium"}),
    ("Insulin glargine", {"insulin"}), ("insulin NPH", {"insulin"}), ("Penicillin G", {"benzylpenicillin"}),
    ("Benzathin penicilin G", {"benzathine-benzylpenicillin"}), ("Procain penicillin", {"procaine-benzylpenicillin"}),
    ("Heparin không phân đoạn", {"heparin"}), ("heparin trọng lượng phân tử thấp", {"enoxaparin|nadroparin"}),
    ("LMWH", {"enoxaparin|nadroparin"}), ("enoxaparin", {"enoxaparin"}),
    ("ABC + 3TC + DTG", {"abacavir", "lamivudine", "dolutegravir"}),
    ("TDF + 3TC + RAL", {"tenofovir-disoproxil", "lamivudine", "raltegravir"}),
    ("Glucagon 1 mg tiêm bắp", {"glucagon"}), ("IVIG", {"human-normal-immunoglobulin"}),
    ("HBIG", {"hepatitis-b-immunoglobulin"}),
])
def test_drugs_of_the_corpus(text, names):
    syn, combos = _cfg_tables()
    assert set(parse_drugs(text, syn, combos).names) == names


@pytest.mark.parametrize("text", [
    "Đánh giá ABC, adrenalin",               # 'ABC' (airway) next to one drug is not abacavir
    "GLP-1 RA (glucagon-like peptide-1)",    # a drug name inside a non-drug term
    "tình trạng kháng insulin", "đề kháng insulin", "insulin resistance", "tiết insulin",
    "kali máu < 3,5 mmol/L", "calci máu", "magie máu", "glucose máu", "albumin máu < 30 g/L",   # analytes
    "đậm đặc", "kém", "sắt", "nấc cụt", "4 triệu chứng", "thuốc chẹn beta", "statin",           # words, classes
])
def test_not_drugs(text):
    syn, combos = _cfg_tables()
    names = set(parse_drugs(text, syn, combos).names)
    assert names <= {"adrenaline"}, (text, names)


def test_new_aliases_are_no_vietnamese_word():
    """No alias of one token is an accent-free Vietnamese word ('đặc' -> 'dac', 'kẽm' -> 'kem', 'nấc' -> 'nac' would
    read ordinary words as drugs)."""
    from vnsoc.normalize_vi import _norm_drug_text

    syn, _ = _cfg_tables()
    vn = {"dac", "kem", "nac", "sat", "than", "kali", "calci", "canxi", "magie", "natri", "dung", "can", "mau", "la",
          "co", "cho", "tu", "vi", "sau", "da", "an", "ho", "hoa", "son", "tien", "phan", "hat", "bot", "tim", "gan"}
    single = {_norm_drug_text(a) for c, al in syn.items() for a in [c, *al] if not a.startswith("~")}
    assert not single & vn
