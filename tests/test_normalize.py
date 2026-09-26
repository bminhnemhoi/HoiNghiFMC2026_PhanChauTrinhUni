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
    ("10 mg/kg/h", "en", Num(10, 10, "mg/kg")),                          # no mg/kg/h unit: not rewritten
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
