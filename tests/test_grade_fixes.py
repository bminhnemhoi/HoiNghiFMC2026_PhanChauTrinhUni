"""Grader 1.1.0 fixes (26/9/2026, pre-freeze) from the T1.3 pilot question reviews (data/interim/pilot/qdrafts/
*_review.md). Answer strings are the reviewers' self-written probes (no model output); atoms are TEST FIXTURES
modelled on the pilot atoms they cite (P-anaphylaxis-03, P-htn-01, P-immunization-02, P-tbhiv-01/02/05, P-hbv-06),
not data."""
import pytest

from vnsoc.grade import compute_tolerance, grade_mcq, grade_short, parse_values
from vnsoc.normalize_vi import drugs_cover, parse_drugs


def atom(**kw):
    a = {"atom_id": "t", "foreign": [], "superseded": [], "decoy": []}
    a.update(kw)
    a["tolerance"] = compute_tolerance(a)
    return a


def lab(out, a, lang="vi", **kw):
    return grade_short(out, a, lang, **kw)


# ------------------------------------------------------------------ G1: ml/kg, ml, ống (P-anaphylaxis-03)
CTX = {"weight_kg": 6, "mg_per_ml": 1, "mg_per_ampoule": 1}
INFANT_ADR = atom(value_kind="num", unit="ug", context=CTX,
                  vn=[{"lo": 200, "hi": 200, "unit": "ug"}, {"lo": 200, "hi": 1000 / 3, "unit": "ug"},
                      {"lo": 0.01, "hi": 0.01, "unit": "mg/kg"}],
                  foreign=[{"system": "EU_UK", "values": [{"lo": 100, "hi": 150, "unit": "ug"}]},
                           {"system": "WHO_global", "values": [{"lo": 0.15, "hi": 0.15, "unit": "mg"}]}],
                  decoy=[{"lo": 400, "hi": 450, "unit": "ug"}])


@pytest.mark.parametrize("out,lang,label,value", [
    ("ĐÁP ÁN: 0,01 ml/kg", "vi", "correct", (60, 60)),          # was 10 µg (the /kg was dropped) -> decoy side
    ("ANSWER: 0.01 mL/kg", "en", "correct", (60, 60)),
    ("ĐÁP ÁN: 0,01 mg/kg", "vi", "correct", (60, 60)),
    ("ĐÁP ÁN: 0,2 ml", "vi", "correct", (200, 200)),
    ("ĐÁP ÁN: 1/5 ống", "vi", "correct", (200, 200)),
    ("ĐÁP ÁN: 1⁄3 ống", "vi", "correct", (1000 / 3, 1000 / 3)),   # U+2044 fraction slash (OCR / typeset text)
    ("ĐÁP ÁN: 1/5-1/3 ống", "vi", "correct", (200, 1000 / 3)),
    ("ĐÁP ÁN: 1/5 – 1/3 ống", "vi", "correct", (200, 1000 / 3)),
    ("ĐÁP ÁN: ½ ống", "vi", "unattributed", (500, 500)),
    ("ANSWER: 1/2 amp", "en", "unattributed", (500, 500)),
    ("ĐÁP ÁN: 0,3-0,5 ml", "vi", "unattributed", (300, 500)),
    ("ĐÁP ÁN: 150 µg", "vi", "foreign", (150, 150)),
    ("ĐÁP ÁN: 0,15 mg", "vi", "foreign", (150, 150)),
])
def test_ml_per_kg_and_ampoule_fractions(out, lang, label, value):
    g = lab(out, INFANT_ADR, lang)
    assert g.label_name == label
    vals = parse_values(g.answer_text, INFANT_ADR, lang)
    assert [f for f, _ in vals] == ["ok"]
    assert (vals[0][1].lo, vals[0][1].hi, vals[0][1].unit) == (pytest.approx(value[0]), pytest.approx(value[1]), "ug")


def test_ml_per_kg_without_context_is_not_guessed():
    no_conc = dict(INFANT_ADR, context={"weight_kg": 6})            # no mg_per_ml -> ml/kg cannot become µg
    g = lab("ĐÁP ÁN: 0,01 ml/kg", no_conc)
    assert (g.label_name, g.parse_method, g.parsed) == ("unattributed", "unit_mismatch", [])
    no_amp = dict(INFANT_ADR, context={"weight_kg": 6, "mg_per_ml": 1})
    assert lab("ĐÁP ÁN: 1/5 ống", no_amp).parse_method == "unit_mismatch"


# ------------------------------------------------------------------ G2: split blood pressure (P-htn-01)
HTN = atom(value_kind="bp", unit="mmHg", vn=[{"sys": 140, "dia": 90}],
           foreign=[{"system": "US", "values": [{"sys": 130, "dia": 80}]},
                    {"system": "EU_UK", "values": [{"sys": 140, "dia": 90}]}],
           decoy=[{"sys": 150, "dia": 100}])


@pytest.mark.parametrize("out,lang,label", [
    ("ĐÁP ÁN: HA tâm thu ≥ 140 mmHg và/hoặc HA tâm trương ≥ 90 mmHg", "vi", "correct"),
    ("ĐÁP ÁN: huyết áp tâm thu ≥140 và/hoặc tâm trương ≥90 mmHg", "vi", "correct"),
    ("ĐÁP ÁN: HATT ≥ 140 mmHg và HATTr ≥ 90 mmHg", "vi", "correct"),
    ("ANSWER: SBP ≥140 and/or DBP ≥90 mmHg", "en", "correct"),
    ("ANSWER: systolic ≥ 130 mm Hg or diastolic ≥ 80 mm Hg", "en", "foreign"),
    ("ANSWER: ≥130 mmHg systolic or ≥80 mmHg diastolic", "en", "foreign"),
    ("ĐÁP ÁN: ≥ 140/90 mmHg (tâm thu ≥ 140 và/hoặc tâm trương ≥ 90)", "vi", "correct"),   # same value twice
])
def test_split_blood_pressure_is_one_value(out, lang, label):
    g = lab(out, HTN, lang)
    assert g.label_name == label and len(g.parsed) == 1 and "cmp='>='" in g.parsed[0]


# ------------------------------------------------------------------ G3: compound age (P-immunization-02)
BOOSTER = atom(value_kind="num", unit="year", vn=[{"lo": 7, "hi": 7, "unit": "year"}],
               foreign=[{"system": "US", "values": [{"lo": 4, "hi": 6, "unit": "year"}]},
                        {"system": "EU_UK", "values": [{"lo": 40, "hi": 40, "unit": "month"}]}],
               decoy=[{"lo": 8, "hi": 10, "unit": "year"}])


@pytest.mark.parametrize("out,lang", [
    ("ĐÁP ÁN: 3 tuổi 4 tháng", "vi"), ("ĐÁP ÁN: 3 năm 4 tháng", "vi"), ("ANSWER: 3 years 4 months", "en"),
    ("ANSWER: 3 years and 4 months", "en"), ("ĐÁP ÁN: 40 tháng", "vi"),
])
def test_compound_age_is_one_value(out, lang):
    g = lab(out, BOOSTER, lang)
    assert (g.label_name, g.foreign_systems, g.multi) == ("foreign", ["EU_UK"], False)


# ------------------------------------------------------------------ G4: drug aliases, regimens, classes
SYN = {"bedaquiline": ["bedaquilin", "bdq"], "pretomanid": [], "linezolid": ["lzd"], "moxifloxacin": ["mfx"],
       "delamanid": ["dlm"], "clofazimine": ["clofazimin", "cfz"], "cycloserine": ["cycloserin"], "amikacin": [],
       "levofloxacin": ["lfx"], "prothionamide": ["prothionamid", "pto"],
       "tenofovir-disoproxil": ["tenofovir disoproxil", "tdf"], "tenofovir-alafenamide": ["tenofovir alafenamide", "taf"],
       "lamivudine": ["lamivudin", "3tc"], "emtricitabine": ["ftc"], "dolutegravir": ["dtg"], "efavirenz": ["efv"],
       "bictegravir": ["bic"], "nevirapine": ["nvp"], "entecavir": ["etv"],
       "bedaquiline+pretomanid+linezolid": ["bpal"], "bedaquiline+pretomanid+linezolid+moxifloxacin": ["bpalm"],
       "bedaquiline+delamanid+linezolid+clofazimine": ["bdlc"],
       "tenofovir-disoproxil+lamivudine+dolutegravir": ["tld"], "tenofovir-disoproxil+lamivudine+efavirenz": ["tle"],
       "bictegravir+emtricitabine+tenofovir-alafenamide": ["biktarvy"],
       "tenofovir-disoproxil|tenofovir-alafenamide": ["tenofovir"]}
# BPaL listed BEFORE BPaLM on purpose: collapsing must not depend on dict order
COMBOS = {"BPaL": ["bedaquiline", "pretomanid", "linezolid"],
          "BPaLM": ["bedaquiline", "pretomanid", "linezolid", "moxifloxacin"]}
TDF, TAF = "tenofovir-disoproxil", "tenofovir-alafenamide"
CLASS = f"{TDF}|{TAF}"


@pytest.mark.parametrize("text,names", [
    ("BPaL", {"BPaL"}),
    ("bedaquilin + pretomanid + linezolid", {"BPaL"}),
    ("BPaLM", {"BPaLM"}),
    ("BPaL + moxifloxacin", {"BPaLM"}),
    ("BDLC", {"bedaquiline", "delamanid", "linezolid", "clofazimine"}),   # expands, never collapses
    ("Bdq-Lfx-Pto-E-Z-Hh-Cfz", {"bedaquiline", "levofloxacin", "prothionamide", "clofazimine"}),
    ("TLD", {TDF, "lamivudine", "dolutegravir"}),
    ("TLE", {TDF, "lamivudine", "efavirenz"}),
    ("Biktarvy", {"bictegravir", "emtricitabine", TAF}),
    ("BIC/FTC/TAF", {"bictegravir", "emtricitabine", TAF}),
    ("bictegravir/emtricitabine/tenofovir alafenamide", {"bictegravir", "emtricitabine", TAF}),
    ("tenofovir disoproxil + lamivudine + dolutegravir", {TDF, "lamivudine", "dolutegravir"}),
    ("Tenofovir", {CLASS}),
    ("tenofovir (TDF) + 3TC", {TDF, "lamivudine"}),            # the class word adds nothing when the form is named
    ("TDF + 3TC + NVP", {TDF, "lamivudine", "nevirapine"}),
])
def test_parse_drugs_regimens_and_classes(text, names):
    assert parse_drugs(text, SYN, COMBOS).names == frozenset(names)


def test_class_token_covers_one_member():
    assert drugs_cover({CLASS}, [TDF]) == (True, True)
    assert drugs_cover({CLASS}, [TDF, TAF]) == (False, True)
    assert drugs_cover({CLASS, TAF}, [TDF, TAF]) == (True, True)
    assert drugs_cover({"lamivudine"}, [TDF]) == (False, False)


TB_FQ = atom(value_kind="drugs", vn=[{"key_drugs": ["BPaL"]}],
             foreign=[{"system": "WHO_global", "values": [{"key_drugs": ["BPaL"]}, {"key_drugs": ["delamanid", "clofazimine"]}]}],
             superseded=[{"guideline": "2760/2021", "values": [{"key_drugs": ["cycloserine"]}]}],
             decoy=[{"key_drugs": ["pretomanid", "moxifloxacin", "pyrazinamide"]}])
TB_SHORT = atom(value_kind="drugs", vn=[{"key_drugs": ["bedaquiline"]}],
                foreign=[{"system": "WHO_global", "version_date": "2026", "values": [{"key_drugs": ["bedaquiline"]}]},
                         {"system": "WHO_global", "version_date": "2019", "values": [{"key_drugs": ["amikacin"]}]}],
                superseded=[{"guideline": "1314/2020", "values": [{"key_drugs": ["amikacin"]}]}])
PEP = atom(value_kind="drugs", vn=[{"key_drugs": [TDF, "dolutegravir"]}],
           foreign=[{"system": "US", "values": [{"key_drugs": ["bictegravir"]}, {"key_drugs": [TDF, "dolutegravir"]},
                                                {"key_drugs": [TAF, "dolutegravir"]}]}],
           decoy=[{"key_drugs": ["nevirapine"]}])
HBV_NA = atom(value_kind="drugs", vn=[{"key_drugs": [TDF]}, {"key_drugs": [TAF]}, {"key_drugs": ["entecavir"]}],
              foreign=[{"system": "WHO_global", "values": [{"key_drugs": [TDF]}, {"key_drugs": ["entecavir"]}]}])


@pytest.mark.parametrize("a,out,label,extra", [
    (TB_FQ, "ĐÁP ÁN: BPaL", "correct", {}),
    (TB_FQ, "ĐÁP ÁN: BDLC", "foreign", {"foreign_systems": ["WHO_global"]}),
    (TB_FQ, "ĐÁP ÁN: BPaLM", "unattributed", {}),
    (TB_SHORT, "ĐÁP ÁN: Bdq-Lfx-Pto-E-Z-Hh-Cfz", "correct", {}),
    (TB_SHORT, "ĐÁP ÁN: amikacin, levofloxacin, prothionamide, clofazimine", "temporal", {"superseded": ["1314/2020"]}),
    (PEP, "ĐÁP ÁN: BIC/FTC/TAF", "foreign", {"foreign_systems": ["US"]}),
    (PEP, "ĐÁP ÁN: Biktarvy", "foreign", {"foreign_systems": ["US"]}),
    (PEP, "ĐÁP ÁN: tenofovir disoproxil + lamivudine + dolutegravir", "correct", {}),
    (PEP, "ĐÁP ÁN: TLD", "correct", {}),
    (PEP, "ĐÁP ÁN: TAF + FTC + DTG", "foreign", {}),
    (PEP, "ĐÁP ÁN: TDF + 3TC + NVP", "unattributed", {"decoy_match": True}),
    (HBV_NA, "ĐÁP ÁN: Tenofovir", "correct", {}),                  # was abstain (label 6)
    (HBV_NA, "ĐÁP ÁN: tenofovir hoặc entecavir", "correct", {}),
])
def test_drug_answers(a, out, label, extra):
    g = grade_short(out, a, "vi", SYN, COMBOS)
    assert g.label_name == label
    for k, v in extra.items():
        assert getattr(g, k) == v


def test_real_config_reads_reviewer_strings():
    from vnsoc.extract.verify_span import drug_tables

    syn, combos = drug_tables()
    for text, want in [("BPaL", {"BPaL"}), ("BDLC", {"bedaquiline", "delamanid", "linezolid", "clofazimine"}),
                       ("Biktarvy", {"bictegravir", "emtricitabine", TAF}), ("TLD", {TDF, "lamivudine", "dolutegravir"}),
                       ("amikacin + prothionamide", {"amikacin", "prothionamide"}), ("Tenofovir", {CLASS}),
                       ("NVP", {"nevirapine"}), ("Mfx", {"moxifloxacin"}),
                       # WHO ACTs of the malaria atoms (no entry before 1.1.0 -> those foreign values never matched)
                       ("artesunat + amodiaquin", {"artesunate-amodiaquine"}), ("AS-MQ", {"artesunate-mefloquine"}),
                       ("artesunat + sulfadoxin-pyrimethamin", {"artesunate+sulfadoxine-pyrimethamine"})]:
        assert parse_drugs(text, syn, combos).names == frozenset(want), text


# ------------------------------------------------------------------ G5: MCQ roles with several sources
ROLES = {"A": "vn", "B": "superseded:3310/2019|foreign:US", "C": "foreign:US+WHO_global", "D": "decoy",
         "E": "filler", "F": "foreign:EU_UK|decoy"}


@pytest.mark.parametrize("out,label,vn,foreign,sup,decoy", [
    ("ĐÁP ÁN: A", "correct", True, [], [], False),
    ("ĐÁP ÁN: B", "temporal", False, ["US"], ["3310/2019"], False),   # same precedence as grade_short
    ("ĐÁP ÁN: C", "foreign", False, ["US", "WHO_global"], [], False),
    ("ĐÁP ÁN: D", "unattributed", False, [], [], True),
    ("ĐÁP ÁN: E", "unattributed", False, [], [], False),
    ("ĐÁP ÁN: F", "foreign", False, ["EU_UK"], [], True),
])
def test_mcq_multi_source_roles(out, label, vn, foreign, sup, decoy):
    g = grade_mcq(out, ROLES)
    assert (g.label_name, g.vn_match, g.foreign_systems, g.superseded, g.decoy_match) == (label, vn, foreign, sup, decoy)


def test_mcq_vn_token_wins():
    g = grade_mcq("ANSWER: A", {"A": "superseded:x|vn", "B": "decoy"})
    assert (g.label_name, g.vn_match, g.superseded) == ("correct", True, ["x"])


# ------------------------------------------------------------------ G6: drug-list conflict is tested per value
def test_concordant_record_not_vetoed_by_conflicting_record_of_same_system():
    # WHO 2026 = MoH (bedaquiline); WHO 2019 = amikacin. 'bedaquiline' used to get label 5 (system-name test).
    g = grade_short("ĐÁP ÁN: bedaquilin", TB_SHORT, "vi", SYN, COMBOS)
    assert (g.label_name, g.multi) == ("correct", False)
    both = grade_short("ĐÁP ÁN: bedaquilin + amikacin", TB_SHORT, "vi", SYN, COMBOS)
    assert (both.label_name, both.multi) == ("unattributed", True)   # both regimens, unattributed


def test_class_name_is_underspecified_not_a_second_regimen():
    # 'tenofovir' fits TDF (MoH) and TAF (US conflicting value). Neutral rule (review of 1.1.0): graded once per
    # member, 2 vs 4 -> label 5, underspecified; no source credited (it used to be 2 by MoH-first precedence).
    g = grade_short("ĐÁP ÁN: tenofovir + lamivudin + dolutegravir", PEP, "vi", SYN, COMBOS)
    assert (g.label_name, g.multi, g.underspecified) == ("unattributed", False, True)
    assert (g.vn_match, g.foreign_systems, g.decoy_match) == (False, [], False)
    assert g.parsed == [f"Drugs(names=frozenset({{'dolutegravir', 'lamivudine', '{CLASS}'}}))"]   # the class kept


# ================================================================== independent review of 1.1.0 (26/9/2026)
def _real():
    from vnsoc.extract.verify_span import drug_tables

    return drug_tables()


# ------------------------------------------------------------------ R1: one value restated with a comparator
DM_AGE = atom(value_kind="num", unit="year", vn=[{"lo": 45, "hi": 45, "cmp": ">="}],
              foreign=[{"system": "US", "values": [{"lo": 35, "hi": 35, "cmp": ">="}]}], decoy=[{"lo": 55, "hi": 55}])


@pytest.mark.parametrize("out,a,label,cmp", [
    ("ĐÁP ÁN: 130/80 mmHg (tâm thu ≥ 130 hoặc tâm trương ≥ 80)", HTN, "foreign", ">="),     # was 5 (two BPs)
    ("ĐÁP ÁN: 140/90 mmHg (tâm thu ≥ 140 hoặc tâm trương ≥ 90)", HTN, "correct", ">="),
    ("ĐÁP ÁN: 35 tuổi (từ 35 tuổi trở lên)", DM_AGE, "foreign", ">="),                      # was 5
    ("ĐÁP ÁN: 45 tuổi (từ 45 tuổi trở lên)", DM_AGE, "correct", ">="),
    ("ĐÁP ÁN: 0,15 mg (150 µg)", INFANT_ADR, "foreign", None),                              # same value, two units
    ("ĐÁP ÁN: 0,01 ml/kg (0,06 mg)", INFANT_ADR, "correct", None),
])
def test_restated_value_is_one_value(out, a, label, cmp):
    g = lab(out, a)
    assert (g.label_name, g.multi, len(g.parsed)) == (label, False, 1)
    assert f"cmp={cmp!r}" in g.parsed[0]                                                   # the comparator is kept


def test_different_comparators_stay_two_values():
    g = lab("ĐÁP ÁN: ≥ 35 tuổi hoặc < 35 tuổi", DM_AGE)
    assert (g.label_name, g.multi, len(g.parsed)) == ("unattributed", True, 2)


# ------------------------------------------------------------------ R2: Vietnamese INN spelling of TAF/TDF
@pytest.mark.parametrize("out,label", [
    ("ĐÁP ÁN: tenofovir alafenamid + lamivudin + dolutegravir", "foreign"),          # was 2 via the class name
    ("ĐÁP ÁN: tenofovir-alafenamid fumarat + 3TC + DTG", "foreign"),
    ("ĐÁP ÁN: tenofovir disoproxil fumarat + lamivudin + dolutegravir", "correct"),
    ("ĐÁP ÁN: tenofovir (TDF) + 3TC + DTG", "correct"),                               # the class word adds nothing
])
def test_vietnamese_tenofovir_forms(out, label):
    syn, combos = _real()
    g = grade_short(out, PEP, "vi", syn, combos)
    assert (g.label_name, g.underspecified) == (label, False)


# ------------------------------------------------------------------ R3: decoy regimen abbreviation (symmetry)
def test_decoy_regimen_abbreviation_is_read_like_the_foreign_one():
    syn, combos = _real()
    assert parse_drugs("BPaMZ", syn, combos).names == {"bedaquiline", "pretomanid", "moxifloxacin", "pyrazinamide"}
    decoy = grade_short("ĐÁP ÁN: BPaMZ", TB_FQ, "vi", syn, combos)                     # was 6 (not read)
    assert (decoy.label_name, decoy.decoy_match) == ("unattributed", True)
    assert grade_short("ĐÁP ÁN: BDLC", TB_FQ, "vi", syn, combos).label_name == "foreign"


# ------------------------------------------------------------------ R4: per-kg and per-time phrases
@pytest.mark.parametrize("out,lang", [
    ("ANSWER: 0.01 mg per kg", "en"), ("ANSWER: 0.01 mL per kg", "en"), ("ANSWER: 10 mcg per kg", "en"),
    ("ANSWER: 10 micrograms per kilogram", "en"), ("ĐÁP ÁN: 0,01 mg cho mỗi kg", "vi"), ("ĐÁP ÁN: 0,01 mg/1 kg", "vi"),
    ("ĐÁP ÁN: 0,01 ml / kg", "vi"), ("ĐÁP ÁN: 0,01 mg / kg", "vi"), ("ĐÁP ÁN: 0,01 ml/kg", "vi"),
])
def test_per_kg_is_not_dropped(out, lang):
    # the /kg used to be dropped: 10 µg, inside the decoy range at 6 kg -> decoy_match
    g = lab(out, INFANT_ADR, lang)
    assert (g.label_name, g.decoy_match, g.parsed) == ("correct", False, ["Num(lo=60.0, hi=60.0, unit='ug', cmp=None)"])


FLUID = atom(value_kind="num", unit="ml/kg/h", vn=[{"lo": 15, "hi": 15}],
             foreign=[{"system": "WHO_global", "values": [{"lo": 5, "hi": 10}]}], decoy=[{"lo": 20, "hi": 25}])
PQ_DAY = atom(value_kind="num", unit="mg/kg/day", context={"weight_kg": 60}, vn=[{"lo": 0.5, "hi": 0.5}],
              foreign=[{"system": "WHO_global", "values": [{"lo": 1, "hi": 1}]}])


@pytest.mark.parametrize("out,a,lang,label", [
    ("ANSWER: 5-7 mL/kg per hour", FLUID, "en", "foreign"),                          # was unit_mismatch (5)
    ("ĐÁP ÁN: 15 ml/kg mỗi giờ", FLUID, "vi", "correct"),
    ("ANSWER: 0.5 mg/kg per day", PQ_DAY, "en", "correct"),
    ("ĐÁP ÁN: 0,5 mg/kg cân nặng/ngày", PQ_DAY, "vi", "correct"),
    ("ĐÁP ÁN: 1 mg/kg mỗi ngày", PQ_DAY, "vi", "foreign"),
])
def test_per_time_phrases(out, a, lang, label):
    assert lab(out, a, lang).label_name == label


def test_amount_over_a_time_is_not_a_rate():
    g = lab("ĐÁP ÁN: 15 ml/kg trong 1 giờ", FLUID)                                   # unchanged (not rewritten)
    assert (g.label_name, g.parse_method) == ("unattributed", "unit_mismatch")


# ------------------------------------------------------------------ R5: neutral rule for a drug class name
NO_TNF = atom(value_kind="drugs", vn=[{"key_drugs": ["entecavir"]}],
              foreign=[{"system": "US", "values": [{"key_drugs": [TAF]}]}])


def test_class_name_never_credits_one_side():
    # MoH has no tenofovir: 'tenofovir' is TDF (no source) or TAF (US) -> 5, not a full foreign match
    g = grade_short("ĐÁP ÁN: Tenofovir", NO_TNF, "vi", SYN, COMBOS)
    assert (g.label_name, g.underspecified, g.foreign_systems) == ("unattributed", True, [])
    assert grade_short("ĐÁP ÁN: TAF", NO_TNF, "vi", SYN, COMBOS).label_name == "foreign"
    # every member is MoH (P-hbv-06): still correct, and no member-specific source is credited
    h = grade_short("ĐÁP ÁN: Tenofovir", HBV_NA, "vi", SYN, COMBOS)
    assert (h.label_name, h.underspecified, h.foreign_systems) == ("correct", False, [])


# ------------------------------------------------------------------ R6: malformed MCQ roles fail loudly
@pytest.mark.parametrize("role", ["VN", "foreign:", "foreign", "foregin:US", "superseded", "", "vn|", "foreign:US+"])
def test_mcq_malformed_role_raises(role):
    with pytest.raises(ValueError):
        grade_mcq("ĐÁP ÁN: A", {"A": "vn", "B": role})                                # checked even if not chosen


# ------------------------------------------------------------------ R7: product concentrations are not doses
@pytest.mark.parametrize("out,lang", [
    ("ĐÁP ÁN: 0,01 ml/kg dung dịch 1:1000", "vi"), ("ANSWER: 0.01 mL/kg of 1 mg/mL epinephrine", "en"),
    ("ĐÁP ÁN: adrenalin 1‰ 0,01 ml/kg", "vi"), ("ĐÁP ÁN: 0,01 ml/kg (ống 1 mg/1 ml)", "vi"),
])
def test_concentration_is_not_a_second_value(out, lang):
    g = lab(out, INFANT_ADR, lang)
    assert (g.label_name, g.multi) == ("correct", False)


def test_concentration_only_is_a_value_not_an_abstention():
    g = lab("ĐÁP ÁN: adrenalin 1:1000", INFANT_ADR)
    assert (g.label_name, g.parse_method) == ("unattributed", "unit_mismatch")


# ------------------------------------------------------------------ R8: minor readings
@pytest.mark.parametrize("out,label", [
    ("ĐÁP ÁN: HA tâm trương ≥ 90 mmHg và/hoặc HA tâm thu ≥ 140 mmHg", "correct"),    # reversed order
    ("ĐÁP ÁN: HATTh ≥ 140 mmHg và HATTr ≥ 90 mmHg", "correct"),
    ("ĐÁP ÁN: HA ≥ 130 mmHg (tâm thu) và/hoặc ≥ 80 mmHg (tâm trương)", "foreign"),
])
def test_split_blood_pressure_more_forms(out, label):
    assert lab(out, HTN).label_name == label


@pytest.mark.parametrize("out,lang", [("ANSWER: 3 years, 4 months", "en"), ("ĐÁP ÁN: 3 tuổi, 4 tháng", "vi"),
                                      ("ANSWER: 3 yrs 4 mos", "en")])
def test_compound_age_with_comma(out, lang):
    assert lab(out, BOOSTER, lang).label_name == "foreign"


@pytest.mark.parametrize("out,label", [("ĐÁP ÁN: 1/5 ống (0,2 ml)", "correct"),
                                       ("ANSWER: 1/5 to 1/3 of an ampoule", "correct"),
                                       ("ĐÁP ÁN: nửa ống", "unattributed")])       # 'nửa ống' was abstain (6)
def test_dose_form_words(out, label):
    g = lab(out, INFANT_ADR, "en" if out.startswith("ANSWER") else "vi")
    assert (g.label_name, g.multi, g.parse_method) == (label, False, "answer_line")


def test_tb_chain_codes_read_the_old_regimen():
    syn, combos = _real()
    g = grade_short("ĐÁP ÁN: Bdq Lzd Cfz Cs", TB_FQ, "vi", syn, combos)               # was 5 (Cs not read)
    assert (g.label_name, g.superseded) == ("temporal", ["2760/2021"])
    s = grade_short("ĐÁP ÁN: 4-6 Am Lfx Pto Cfz Z H liều cao E / 5 Lfx Cfz Z E", TB_SHORT, "vi", syn, combos)
    assert (s.label_name, s.superseded) == ("temporal", ["1314/2020"])


def test_parsed_drugs_are_reproducible():
    g = grade_short("ĐÁP ÁN: TDF + 3TC + NVP", PEP, "vi", SYN, COMBOS)
    assert g.parsed == ["Drugs(names=frozenset({'lamivudine', 'nevirapine', 'tenofovir-disoproxil'}))"]


def test_day_to_hour_is_exact():
    a = atom(value_kind="num", unit="h", vn=[{"lo": 24, "hi": 24}],
             foreign=[{"system": "US", "values": [{"lo": 48, "hi": 48}]}])
    assert lab("ĐÁP ÁN: 1 ngày", a).label_name == "correct"                          # was unit_mismatch
    assert lab("ĐÁP ÁN: 2 ngày", a).label_name == "foreign"


# ---------------------------------------------------------------- log-scale quantities (viral load), grader 1.1.0
def _vl_atom(**kw):
    a = {"atom_id": "T-vl", "value_kind": "num", "unit": "IU/mL",
         "vn": [{"lo": 2000, "hi": 2000, "unit": "IU/mL", "cmp": ">"}],
         "foreign": [{"system": "US", "source": "x", "version_date": "2025",
                      "values": [{"lo": 20000, "hi": 20000, "unit": "IU/mL", "cmp": ">"}]}]}
    a.update(kw)
    from vnsoc.grade import compute_tolerance
    return dict(a, tolerance=compute_tolerance(a))


def test_log_scale_tolerance_is_in_decades():
    import math

    from vnsoc.grade import _gap, grade_short, log_scale
    a = _vl_atom()
    assert log_scale(a) and math.isclose(a["tolerance"], 0.5)          # 10-fold gap = 1 decade -> half of it
    assert math.isclose(_gap(a["vn"][0], a["foreign"][0]["values"][0], a), 1.0)
    assert grade_short("ĐÁP ÁN: > 2.000 IU/mL", a).label == 2
    assert grade_short("ĐÁP ÁN: > 3.000 IU/mL", a).label == 2           # inside the 2000..6325 log window
    assert grade_short("ĐÁP ÁN: > 10.000 IU/mL", a).label == 4          # nearer 20000 on the log scale
    assert grade_short("ĐÁP ÁN: > 20.000 IU/mL", a).label == 4


def test_log_scale_geometric_decoy_is_accepted_again():
    from vnsoc.match.decoys import check_decoy, choose_decoy
    a = _vl_atom()
    d, rule = choose_decoy(a)
    assert d is not None and rule == "mirror_geom" and d["lo"] == 200
    assert check_decoy(dict(a, decoy=[d])) == []


def test_linear_units_unchanged():
    from vnsoc.grade import _gap, log_scale
    a = _vl_atom(unit="U/L")
    a["vn"][0]["unit"] = a["foreign"][0]["values"][0]["unit"] = "U/L"
    assert not log_scale(a) and _gap(a["vn"][0], a["foreign"][0]["values"][0], a) == 18000
