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


# Drug items carry their recorded `text` as the pilot atoms do (key_drugs is only the discriminating part of the
# regimen; since grader 1.3.0 the other drugs of an answer must belong to the regimen: key drugs + drugs of the text).
TB_FQ = atom(value_kind="drugs", vn=[{"key_drugs": ["BPaL"], "text": "BPaL (bedaquiline + pretomanid + linezolid)"}],
             foreign=[{"system": "WHO_global", "values": [
                 {"key_drugs": ["BPaL"], "text": "BPaL"},
                 {"key_drugs": ["delamanid", "clofazimine"],
                  "text": "BDLC: bedaquiline + delamanid + linezolid + clofazimine"}]}],
             superseded=[{"guideline": "2760/2021", "values": [
                 {"key_drugs": ["cycloserine"], "text": "Bdq Lzd Cfz Cs + 1 thuốc nhóm C"}]}],
             decoy=[{"key_drugs": ["pretomanid", "moxifloxacin", "pyrazinamide"],
                     "text": "BPaMZ: bedaquiline + pretomanid + moxifloxacin + pyrazinamide"}])
TB_SHORT = atom(value_kind="drugs", vn=[{"key_drugs": ["bedaquiline"], "text": "4-6 Bdq-Lfx-Pto-E-Z-Hh-Cfz / 5 Lfx-Cfz-Z-E"}],
                foreign=[{"system": "WHO_global", "version_date": "2026", "values": [
                    {"key_drugs": ["bedaquiline"], "text": "4-6 Bdq-Lfx-Eto-E-Z-Hh-Cfz / 5 Lfx-Cfz-Z-E"}]},
                         {"system": "WHO_global", "version_date": "2019", "values": [
                             {"key_drugs": ["amikacin"], "text": "4-6 Am-Mfx-Cfz-Eto-Z-E-Hh / 5 Mfx-Cfz-Z-E"}]}],
                superseded=[{"guideline": "1314/2020", "values": [
                    {"key_drugs": ["amikacin"], "text": "4-6 Am Lfx Pto Cfz Z H liều cao E / 5 Lfx Cfz Z E"}]}])
PEP = atom(value_kind="drugs", vn=[{"key_drugs": [TDF, "dolutegravir"], "text": "TDF + 3TC (hoặc FTC) + DTG"}],
           foreign=[{"system": "US", "values": [
               {"key_drugs": ["bictegravir"], "text": "BIC/FTC/TAF"},
               {"key_drugs": [TDF, "dolutegravir"], "text": "DTG + TDF + (FTC hoặc 3TC)"},
               {"key_drugs": [TAF, "dolutegravir"], "text": "DTG + TAF + (FTC hoặc 3TC)"}]}],
           decoy=[{"key_drugs": ["nevirapine"], "text": "TDF + 3TC + NVP"}])
HBV_NA = atom(value_kind="drugs", vn=[{"key_drugs": [TDF], "text": "TDF"}, {"key_drugs": [TAF], "text": "TAF"},
                                      {"key_drugs": ["entecavir"], "text": "ETV"}],
              foreign=[{"system": "WHO_global", "values": [{"key_drugs": [TDF], "text": "TDF"},
                                                           {"key_drugs": ["entecavir"], "text": "ETV"}]}])


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
    both = grade_short("ĐÁP ÁN: bedaquilin hoặc amikacin", TB_SHORT, "vi", SYN, COMBOS)
    assert (both.label_name, both.multi) == ("unattributed", True)   # both regimens listed, unattributed (rule 7)
    # grader 1.3.0: joined by '+' the two key drugs are ONE combined regimen, recorded nowhere: 5, not two values
    joined = grade_short("ĐÁP ÁN: bedaquilin + amikacin", TB_SHORT, "vi", SYN, COMBOS)
    assert (joined.label_name, joined.multi, joined.partial) == ("unattributed", False, True)


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


# ================================================================== grader 1.2.0 (26/9/2026, pre-freeze)
# Blind to the sealed pilot outputs: every answer below is self-written; atoms are fixtures modelled on P-dengue-03,
# P-tbhiv-03, P-htn-01, P-controls-09, P-hbv-03/06, P-tbhiv-01, P-immunization-01/02, P-malaria_ocr-04/05/06.

# ------------------------------------------------------------------ R1: a cat answer naming several categories
FLUID_CAT = atom(value_kind="cat", vn=[{"label": "colloid"}], foreign=[{"system": "WHO_global", "values": [
    {"label": "crystalloid"}]}], decoy=[{"label": "albumin"}],
    cat_options={"colloid": ["cao phan tu", r"\bcolloid", "dextran", r"\bhes\b"],
                 "crystalloid": ["ringer", r"\bnacl\b", "crystalloid", "tinh the", r"\bsaline\b"],
                 "albumin": ["albumin"]})
HRE_CAT = atom(value_kind="cat", vn=[{"label": "HRE"}], foreign=[{"system": "US", "values": [{"label": "HR"}]}],
               decoy=[{"label": "RE"}],
               cat_options={"HRE": [r"(?<![a-z])(?:hre|rhe)(?![a-z])"], "HR": [r"(?<![a-z])(?:hr|rh)(?![a-z])"],
                            "RE": [r"(?<![a-z])re(?![a-z])"]})


@pytest.mark.parametrize("a,out,lang,label,multi", [
    (FLUID_CAT, "ĐÁP ÁN: Dung dịch cao phân tử (dextran)", "vi", "correct", False),
    (FLUID_CAT, "ĐÁP ÁN: Ringer lactate", "vi", "foreign", False),
    (FLUID_CAT, "ĐÁP ÁN: Ringer lactate hoặc cao phân tử", "vi", "unattributed", True),      # was 2 (MoH first)
    (FLUID_CAT, "ANSWER: Ringer's lactate or a colloid", "en", "unattributed", True),
    # a conditional next step is two values, whichever comes first (neither reading is credited)
    (FLUID_CAT, "ĐÁP ÁN: Ringer lactate; nếu không đáp ứng chuyển cao phân tử", "vi", "unattributed", True),  # was 2
    (FLUID_CAT, "ĐÁP ÁN: Cao phân tử; nếu không đáp ứng chuyển Ringer lactate", "vi", "unattributed", True),
    (FLUID_CAT, "ANSWER: Ringer's lactate; if no response, switch to a colloid", "en", "unattributed", True),
    (FLUID_CAT, "ĐÁP ÁN: Theo Bộ Y tế Việt Nam: cao phân tử; theo WHO: Ringer lactate", "vi", "correct_aware", True),
    (HRE_CAT, "ĐÁP ÁN: 4HR hoặc 4HRE", "vi", "unattributed", True),                          # was 2
    (HRE_CAT, "ANSWER: 4HR; 4HRE if high isoniazid resistance", "en", "unattributed", True),
    (HRE_CAT, "ĐÁP ÁN: 2RHZE/4RHE", "vi", "correct", False),
])
def test_cat_several_categories_are_several_values(a, out, lang, label, multi):
    g = lab(out, a, lang)
    assert (g.label_name, g.multi) == (label, multi)


def test_cat_all_moh_categories_is_correct():
    both = atom(value_kind="cat", vn=[{"label": "one_step"}, {"label": "two_step"}],
                foreign=[{"system": "US", "values": [{"label": "two_step"}]}],
                cat_options={"one_step": ["mot buoc", "one-step"], "two_step": ["hai buoc", "two-step"]})
    g = lab("ĐÁP ÁN: một bước hoặc hai bước", both)
    assert (g.label_name, g.multi, len(g.parsed)) == ("correct", False, 2)


def test_cat_decoy_among_several_is_flagged():
    g = lab("ĐÁP ÁN: cao phân tử hoặc albumin", FLUID_CAT)
    assert (g.label_name, g.multi, g.decoy_match) == ("unattributed", True, True)


@pytest.mark.parametrize("a,out,lang,label", [
    # a negated or vehicle mention is not a second category — the same rule for every label (symmetric pairs)
    (FLUID_CAT, "ĐÁP ÁN: Cao phân tử, không dùng Ringer lactate", "vi", "correct"),
    (FLUID_CAT, "ĐÁP ÁN: Ringer lactate, không dùng cao phân tử", "vi", "foreign"),
    (FLUID_CAT, "ĐÁP ÁN: Dùng cao phân tử thay vì Ringer lactate", "vi", "correct"),
    (FLUID_CAT, "ĐÁP ÁN: Ringer lactate thay vì cao phân tử", "vi", "foreign"),
    (FLUID_CAT, "ĐÁP ÁN: Cao phân tử (không phải dịch tinh thể)", "vi", "correct"),
    (FLUID_CAT, "ANSWER: A colloid, not crystalloid", "en", "correct"),
    (FLUID_CAT, "ANSWER: Colloid rather than Ringer's lactate", "en", "correct"),
    (FLUID_CAT, "ANSWER: Crystalloid rather than colloid", "en", "foreign"),
    (FLUID_CAT, "ĐÁP ÁN: Cao phân tử; Ringer lactate không được khuyến cáo", "vi", "correct"),
    (FLUID_CAT, "ĐÁP ÁN: Ringer lactate; cao phân tử không được khuyến cáo", "vi", "foreign"),
    (FLUID_CAT, "ANSWER: Colloid; Ringer's lactate is not recommended", "en", "correct"),
    (FLUID_CAT, "ĐÁP ÁN: HES 6% pha trong NaCl 0,9%", "vi", "correct"),
    (FLUID_CAT, "ANSWER: 6% HES in 0.9% saline", "en", "correct"),
    (HRE_CAT, "ĐÁP ÁN: 4HRE, không phải 4HR", "vi", "correct"),
    (HRE_CAT, "ĐÁP ÁN: 4HRE thay vì 4HR", "vi", "correct"),
    (HRE_CAT, "ANSWER: 4HR rather than 4HRE", "en", "foreign"),                           # was 2
    (HRE_CAT, "ĐÁP ÁN: 4HR, không dùng ethambutol", "vi", "foreign"),                     # the negation is not on HR
    (HRE_CAT, "ĐÁP ÁN: Không có kháng thuốc: 4HRE", "vi", "correct"),                     # other clause
])
def test_cat_negated_mention_is_not_a_value(a, out, lang, label):
    g = lab(out, a, lang)
    assert (g.label_name, g.multi) == (label, False)


def test_cat_real_pilot_atoms():
    import json

    from vnsoc.paths import paths

    f = paths().root / "data" / "interim" / "pilot_atoms.jsonl"
    atoms = {}
    if f.exists():
        atoms = {json.loads(x)["atom_id"]: json.loads(x) for x in f.read_text(encoding="utf-8").splitlines() if x}
    if not {"P-dengue-03", "P-tbhiv-03"} <= set(atoms):
        pytest.skip("pilot atoms absent")
    d, t = atoms["P-dengue-03"], atoms["P-tbhiv-03"]
    for out, a, lang, want in [("ĐÁP ÁN: Ringer lactate hoặc cao phân tử", d, "vi", (5, True)),
                               ("ĐÁP ÁN: Ringer lactate; nếu không đáp ứng chuyển cao phân tử", d, "vi", (5, True)),
                               ("ĐÁP ÁN: Cao phân tử, không dùng Ringer lactate", d, "vi", (2, False)),
                               ("ANSWER: 6% HES in 0.9% saline", d, "en", (2, False)),
                               ("ĐÁP ÁN: Ringer lactate", d, "vi", (4, False)),
                               ("ĐÁP ÁN: 4HR hoặc 4HRE", t, "vi", (5, True)),
                               ("ANSWER: 4HR rather than 4HRE", t, "en", (4, False)),
                               ("ĐÁP ÁN: 2RHZE/4RHE", t, "vi", (2, False))]:
        g = grade_short(out, a, lang, condition="A1")
        assert (g.label, g.multi) == want, out


# ------------------------------------------------------------------ R2 + R5: blood pressure forms and joiners
@pytest.mark.parametrize("out,lang,label", [
    ("ANSWER: 140 over 90 mmHg", "en", "correct"), ("ANSWER: at least 130 over 80 mmHg", "en", "foreign"),
    ("ĐÁP ÁN: 140 trên 90 mmHg", "vi", "correct"),
    ("ANSWER: ≥140/≥90 mmHg", "en", "correct"), ("ĐÁP ÁN: ≥130/≥80 mmHg", "vi", "foreign"),
    ("ĐÁP ÁN: 140 và 90 mmHg", "vi", "correct"), ("ANSWER: 130 and 80 mmHg", "en", "foreign"),
    ("ĐÁP ÁN: HA ≥ 140 và/hoặc ≥ 90 mmHg", "vi", "correct"),
    # a range is read at its lower bounds (every pilot bp atom is a threshold), the same way for every source
    ("ANSWER: 130–139/80–89 mmHg", "en", "foreign"), ("ĐÁP ÁN: 140–159/90–99 mmHg", "vi", "correct"),
    ("ANSWER: 130-139 systolic or 80-89 diastolic", "en", "foreign"),
    ("ĐÁP ÁN: tâm thu 140–159 và/hoặc tâm trương 90–99 mmHg", "vi", "correct"),
    # R5: 'hay', 'và/hay', 'hoặc là' join the split form
    ("ĐÁP ÁN: HA tâm thu ≥ 140 mmHg hay HA tâm trương ≥ 90 mmHg", "vi", "correct"),
    ("ĐÁP ÁN: HA tâm thu ≥ 140 và/hay tâm trương ≥ 90 mmHg", "vi", "correct"),
    ("ĐÁP ÁN: tâm thu ≥ 130 mmHg hoặc là tâm trương ≥ 80 mmHg", "vi", "foreign"),
])
def test_blood_pressure_forms_1_2_0(out, lang, label):
    g = lab(out, HTN, lang)
    assert (g.label_name, len(g.parsed)) == (label, 1)


def test_two_bare_systolic_values_are_not_a_blood_pressure():
    # no BP is read (unchanged); since grader 1.3.0 numbers that are no BP value are label 5 (unit_mismatch), not 6
    for out in ("ĐÁP ÁN: 140 và 130 mmHg", "ĐÁP ÁN: 140 và 90"):                  # two systolic values; no context
        g = lab(out, HTN)
        assert (g.label_name, g.parse_method, g.parsed) == ("unattributed", "unit_mismatch", []), out


# ------------------------------------------------------------------ R3: units and powers of ten
BMI = atom(value_kind="num", unit="kg/m2", vn=[{"lo": 23, "hi": 23, "cmp": ">="}],
           foreign=[{"system": "WHO_global", "values": [{"lo": 25, "hi": 25, "cmp": ">="}]}],
           decoy=[{"lo": 21, "hi": 21}])


@pytest.mark.parametrize("out,lang,label", [
    ("ANSWER: BMI ≥ 23 kg/m^2", "en", "correct"), ("ANSWER: 25 kg/m^2", "en", "foreign"),   # was unit_mismatch
    ("ĐÁP ÁN: 23 kg/m²", "vi", "correct"), ("ĐÁP ÁN: 23 kg/m 2", "vi", "correct"),
    ("ANSWER: 23 kg per m2", "en", "correct"), ("ANSWER: 25 kg per square metre", "en", "foreign"),
    ("ANSWER: 23 kg·m-2", "en", "correct"),
])
def test_bmi_unit_spellings(out, lang, label):
    g = lab(out, BMI, lang)
    assert (g.label_name, g.parse_method) == (label, "answer_line")


@pytest.mark.parametrize("out,lang,label,method", [
    ("ANSWER: > 2 x 10^3 IU/mL", "en", "correct", "answer_line"),                       # was 5 (2 and 10)
    ("ANSWER: > 2×10³ IU/mL", "en", "correct", "answer_line"),
    ("ĐÁP ÁN: > 2.10^3 IU/mL", "vi", "correct", "answer_line"),                         # Vietnamese dot = times
    ("ĐÁP ÁN: > 2,0.10^3 IU/mL", "vi", "correct", "answer_line"),
    ("ANSWER: > 2e3 IU/mL", "en", "correct", "answer_line"),
    ("ANSWER: > 2 x 10^4 IU/mL", "en", "foreign", "answer_line"),
    ("ANSWER: > 10^4 IU/mL", "en", "foreign", "answer_line"),                           # nearer 20.000 in log10
    # copies/mL is not converted to IU/mL (assay-dependent factor): an unconvertible unit, as for every source
    ("ANSWER: > 10^4 copies/mL", "en", "unattributed", "unit_mismatch"),                # was 10 IU/mL
    ("ĐÁP ÁN: > 10.000 copies/mL", "vi", "unattributed", "unit_mismatch"),
])
def test_powers_of_ten_and_copies(out, lang, label, method):
    g = lab(out, _vl_atom(), lang)
    assert (g.label_name, g.parse_method) == (label, method)


# ------------------------------------------------------------------ R4: drugs
def test_new_drugs_and_regimen_spellings():
    syn, combos = _real()
    hbv = grade_short("ĐÁP ÁN: adefovir", HBV_NA, "vi", syn, combos)
    assert (hbv.label_name, hbv.parse_method) == ("unattributed", "answer_line")      # was abstain (not read)
    assert parse_drugs("adefovir dipivoxil (ADV)", syn, combos).names == {"adefovir"}
    assert parse_drugs("LdT", syn, combos).names == {"telbivudine"}
    tb = atom(value_kind="drugs", vn=[{"key_drugs": ["BPaL"], "text": "BPaL (bedaquiline + pretomanid + linezolid)"}],
              foreign=[{"system": "WHO_global", "values": [
                  {"key_drugs": ["delamanid", "clofazimine"], "text": "BDLC: bedaquiline + delamanid + linezolid + clofazimine"}]}],
              decoy=[{"key_drugs": ["pretomanid", "pyrazinamide"], "text": "BPaZ: bedaquiline + pretomanid + pyrazinamide"}])
    for out in ("ĐÁP ÁN: BPaZ", "ĐÁP ÁN: B-Pa-Z", "ANSWER: B + Pa + Z"):
        g = grade_short(out, tb, "vi", syn, combos)
        assert (g.label_name, g.decoy_match) == ("unattributed", True), out
    for out in ("ĐÁP ÁN: Bdq, Pa, Lzd", "ĐÁP ÁN: B-Pa-L", "ANSWER: B Pa L", "ĐÁP ÁN: Bdq + Pa + Lzd (6 tháng)"):
        assert grade_short(out, tb, "vi", syn, combos).label_name == "correct", out   # was 5 (Pa not read)
    # 'PA' (chest X-ray view) is not pretomanid: the code is matched case-sensitively
    assert "pretomanid" not in parse_drugs("X-quang PA, Bdq, Lzd", syn, combos).names
    assert parse_drugs("Pa", syn, combos).names == frozenset()                        # never alone


# ------------------------------------------------------------------ R6: ordinals and dose/visit names
MEASLES = atom(value_kind="num", unit="month", vn=[{"lo": 9, "hi": 9}],
               foreign=[{"system": "US", "values": [{"lo": 12, "hi": 15}]}], decoy=[{"lo": 3, "hi": 6}])
DTP18 = atom(value_kind="num", unit="month", vn=[{"lo": 18, "hi": 18}],
             foreign=[{"system": "US", "values": [{"lo": 15, "hi": 18}]},
                      {"system": "WHO_global", "values": [{"lo": 12, "hi": 23}]}])


@pytest.mark.parametrize("a,out,lang,label", [
    (MEASLES, "ĐÁP ÁN: 9 tháng (mũi 1)", "vi", "correct"),                                 # was 5 (9 and 1)
    (MEASLES, "ĐÁP ÁN: mũi 1 lúc 9 tháng tuổi", "vi", "correct"),
    (MEASLES, "ĐÁP ÁN: mũi thứ 1: 9 tháng", "vi", "correct"),
    (MEASLES, "ANSWER: 9 months (MMR dose 1)", "en", "correct"),
    (MEASLES, "ANSWER: Dose 1 at 12–15 months", "en", "foreign"),
    (MEASLES, "ĐÁP ÁN: lần 1 lúc 12-15 tháng", "vi", "foreign"),
    (BOOSTER, "ANSWER: 4–6 years (after the 18-month visit)", "en", "foreign"),           # was 5 (18 years)
    (BOOSTER, "ĐÁP ÁN: 7 tuổi (sau mũi 18 tháng)", "vi", "correct"),
    (BOOSTER, "ANSWER: 7 years (after the 18 month dose)", "en", "correct"),
    (DTP18, "ANSWER: At the 18-month visit", "en", "correct"),                            # a name alone is read
    (DTP18, "ĐÁP ÁN: mũi 18 tháng", "vi", "correct"),
])
def test_ordinals_and_visit_names_are_not_values(a, out, lang, label):
    g = lab(out, a, lang)
    assert (g.label_name, g.multi) == (label, False)


def test_real_values_next_to_dose_words_are_kept():
    mg = atom(value_kind="num", unit="mg", vn=[{"lo": 2, "hi": 2}],
              foreign=[{"system": "US", "values": [{"lo": 4, "hi": 4}]}])
    assert lab("ĐÁP ÁN: liều 2 mg", mg).label_name == "correct"
    assert lab("ĐÁP ÁN: liều 2", mg).label_name == "correct"                              # alone: still the value
    tab = atom(value_kind="num", unit="tablet", vn=[{"lo": 1, "hi": 2}],
               foreign=[{"system": "US", "values": [{"lo": 4, "hi": 4}]}])
    assert lab("ĐÁP ÁN: liều 1-2 viên", tab).label_name == "correct"                     # a range, not 'liều 1'


# ------------------------------------------------------------------ R7: numbers in words, 'daily', 'mg base'
DAYS3 = atom(value_kind="num", unit="day", vn=[{"lo": 3, "hi": 3}],
             foreign=[{"system": "US", "values": [{"lo": 5, "hi": 5}]}], decoy=[{"lo": 1, "hi": 1}])
DAYS7 = atom(value_kind="num", unit="day", vn=[{"lo": 7, "hi": 7}],
             foreign=[{"system": "US", "values": [{"lo": 14, "hi": 14}]}])
MIN15 = atom(value_kind="num", unit="min", vn=[{"lo": 15, "hi": 15}],
             foreign=[{"system": "US", "values": [{"lo": 30, "hi": 30}]}])


@pytest.mark.parametrize("a,out,lang,label", [
    (DAYS3, "ĐÁP ÁN: ba ngày", "vi", "correct"), (DAYS3, "ANSWER: three days", "en", "correct"),   # were 6
    (DAYS3, "ĐÁP ÁN: năm ngày", "vi", "foreign"), (DAYS3, "ANSWER: five days", "en", "foreign"),
    (DAYS3, "ĐÁP ÁN: một ngày", "vi", "unattributed"), (DAYS3, "ANSWER: one day", "en", "unattributed"),
    (DAYS7, "ĐÁP ÁN: bảy ngày", "vi", "correct"), (DAYS7, "ANSWER: seven days", "en", "correct"),
    (DAYS7, "ĐÁP ÁN: một tuần", "vi", "correct"), (DAYS7, "ANSWER: one week", "en", "correct"),
    (DAYS7, "ANSWER: a week", "en", "correct"),
    (DAYS7, "ĐÁP ÁN: hai tuần", "vi", "foreign"), (DAYS7, "ANSWER: two weeks", "en", "foreign"),
    (MIN15, "ĐÁP ÁN: mười lăm phút", "vi", "correct"), (MIN15, "ANSWER: fifteen minutes", "en", "correct"),
    (MIN15, "ĐÁP ÁN: ba mươi phút", "vi", "foreign"), (MIN15, "ANSWER: thirty minutes", "en", "foreign"),
    # 'một'/'one'/'a' before a unit yield to a real value (articles), in both languages
    (MIN15, "ĐÁP ÁN: 15 phút, đánh giá lại sau một giờ", "vi", "correct"),
    (MIN15, "ANSWER: 15 minutes, reassess after an hour", "en", "correct"),
    (MIN15, "ANSWER: 15 minutes, reassess after one hour", "en", "correct"),
    # ... and are read alone only when they open the answer: a hedge is not a value (DAYS3's decoy is 1 day)
    (DAYS3, "ANSWER: Not sure; consult a doctor within a day", "en", "abstain"),
    (DAYS3, "ĐÁP ÁN: Không rõ, nên tái khám trong vòng một ngày", "vi", "abstain"),
    (DAYS3, "ANSWER: within a day", "en", "unattributed"),
])
def test_numbers_in_words(a, out, lang, label):
    g = lab(out, a, lang)
    assert (g.label_name, g.multi) == (label, False)


@pytest.mark.parametrize("out,lang,label", [
    ("ANSWER: 0.5 mg base/kg/day", "en", "correct"),            # was unit_mismatch (VI 'mg base/kg/ngày' was 2)
    ("ANSWER: 0.5 mg base/kg daily", "en", "correct"),
    ("ĐÁP ÁN: 0,5 mg base/kg/ngày", "vi", "correct"),
    ("ANSWER: 0.5 mg/kg once daily", "en", "correct"),
    ("ĐÁP ÁN: 0,5 mg/kg 1 lần/ngày", "vi", "correct"),
    ("ANSWER: 1 mg/kg once a day", "en", "foreign"),
])
def test_daily_and_mg_base(out, lang, label):
    assert lab(out, PQ_DAY, lang).label_name == label


def test_twice_daily_is_not_a_value_nor_a_daily_dose():
    per_dose = atom(value_kind="num", unit="mg", vn=[{"lo": 100, "hi": 100}],
                    foreign=[{"system": "US", "values": [{"lo": 200, "hi": 200}]}])
    g = lab("ANSWER: 100 mg twice daily", per_dose, "en")
    assert (g.label_name, g.multi) == ("correct", False)
    g = lab("ANSWER: 0.25 mg/kg twice daily", PQ_DAY, "en")         # 0.25 mg/kg per dose is not 0.25 mg/kg/day
    assert (g.label_name, g.parse_method) == ("unattributed", "unit_mismatch")


# ------------------------------------------------------------------ R8: recorded, NOT changed
def test_threshold_target_with_point_answer_is_unchanged():
    # known limitation (DECISIONS 1.1.0 and 1.2.0): '135' against a '< 140' target is not read as inside it
    target = atom(value_kind="num", unit="mmHg", vn=[{"lo": 140, "hi": 140, "cmp": "<"}],
                  foreign=[{"system": "US", "values": [{"lo": 130, "hi": 130, "cmp": "<"}]}])
    assert lab("ĐÁP ÁN: 135 mmHg", target).label_name == "unattributed"


# ============================================ grader 1.2.0 after the independent grader review (26/9/2026, blind)
# Regression tests for the review findings (CHẶN-1..5 and NÊN SỬA). Self-written answers; fixtures modelled on
# P-dengue-03/04/06, P-tbhiv-03, P-immunization-01/04, P-malaria_ocr-05/06, P-htn-01. Every case that concerns one
# source has its mirror for the other source (the rule must not lean towards the MoH or the foreign value).
NSAID = atom(value_kind="cat", vn=[{"label": "not_allowed"}], foreign=[{"system": "WHO_global", "values": [
    {"label": "allowed"}]}], cat_options={
    "not_allowed": [r"(?s)^(\s*(?:khong|no)\b|.*metamizol\w*[^.]{0,40}(?:khong (?:duoc |nen )?dung|not recommended))"],
    "allowed": [r"(?s)^(\s*(?:co|yes)\b|.*metamizol\w*[^.]{0,40}(?<!khong )(?:co the dung|can be used))"]})


@pytest.mark.parametrize("out,lang,label", [
    # CHẶN-1: the answer word 'Không'/'No' is not negated by the clause that explains it (was abstain)
    ("ĐÁP ÁN: Không - metamizol không nên dùng", "vi", "correct"),
    ("ĐÁP ÁN: Không – metamizol không được dùng trong sốt xuất huyết", "vi", "correct"),
    ("ĐÁP ÁN: Không vì metamizol không được dùng", "vi", "correct"),
    ("ANSWER: No — metamizole is not recommended", "en", "correct"),
    ("ANSWER: No - metamizole should not be used in dengue", "en", "correct"),
    ("ANSWER: No - it is not recommended", "en", "correct"),
    ("ANSWER: No metamizole should be avoided", "en", "correct"),
    ("ĐÁP ÁN: Có - metamizol có thể dùng", "vi", "foreign"), ("ANSWER: Yes - metamizole can be used", "en", "foreign"),
])
def test_yes_no_answer_is_not_negated_by_its_explanation(out, lang, label):
    g = lab(out, NSAID, lang)
    assert (g.label_name, g.multi) == (label, False)


FLUID_ANCHORED = atom(value_kind="cat", vn=[{"label": "colloid"}], foreign=[{"system": "WHO_global", "values": [
    {"label": "crystalloid"}]}], cat_options={
    "colloid": [r"(?s)^(?!.*(?:khong dung|not|avoid)\s+(?:cao phan tu|colloid|dextran|\bhes\b))"
                r".*(?:cao phan tu|colloid|dextran|\bhes\b|starch|gelatin)"],
    "crystalloid": ["ringer", r"\bnacl\b", "crystalloid", r"\bsaline\b"]})


@pytest.mark.parametrize("out,lang,label", [
    # CHẶN-2: a whole-answer (anchored) pattern is not dismissed by a negation of its LAST mention only (was abstain)
    ("ĐÁP ÁN: Dung dịch cao phân tử (Dextran 40); HES không được dùng", "vi", "correct"),
    ("ĐÁP ÁN: Dextran 40 (HES không được khuyến cáo)", "vi", "correct"),
    ("ANSWER: Colloid (dextran 40); HES is not recommended", "en", "correct"),
    ("ANSWER: Colloid such as gelatin; starches should be avoided", "en", "correct"),
    ("ĐÁP ÁN: Cao phân tử, HES không nên dùng", "vi", "correct"),
    ("ĐÁP ÁN: Ringer lactate, NaCl 0,9% không nên dùng", "vi", "foreign"),                  # mirror (simple pattern)
    # ... but a single mention, or the only accepted one, is checked like any mention (mirrors give the same label)
    ("ĐÁP ÁN: Dextran 40 không được khuyến cáo", "vi", "abstain"),
    ("ĐÁP ÁN: Ringer lactate không được khuyến cáo", "vi", "abstain"),
    ("ĐÁP ÁN: Truyền dịch; HES không được dùng", "vi", "abstain"),
    ("ĐÁP ÁN: Truyền dịch; Ringer lactate không được dùng", "vi", "abstain"),
    ("ĐÁP ÁN: HES không được dùng; dùng Ringer lactate", "vi", "foreign"),
    ("ĐÁP ÁN: Ringer lactate không được dùng; dùng HES", "vi", "correct"),
])
def test_anchored_whole_answer_pattern(out, lang, label):
    g = lab(out, FLUID_ANCHORED, lang)
    assert (g.label_name, g.multi) == (label, False)


@pytest.mark.parametrize("a,out,label", [
    # CHẶN-3: 'chứa' (contains) is not 'chưa' (not yet); 'nó' is not 'no' (was abstain)
    (HRE_CAT, "ĐÁP ÁN: Phác đồ chứa HRE", "correct"), (HRE_CAT, "ĐÁP ÁN: Phác đồ duy trì chứa 4HR", "foreign"),
    (FLUID_CAT, "ĐÁP ÁN: Dung dịch chứa natri clorid 0,9% (NaCl)", "foreign"),
    (FLUID_CAT, "ĐÁP ÁN: Dung dịch có chứa Ringer lactate", "foreign"),
    (FLUID_CAT, "ĐÁP ÁN: Dịch keo chứa HES 6%", "correct"),
    (FLUID_CAT, "ĐÁP ÁN: Truyền Ringer lactate vì nó là dịch đẳng trương", "foreign"),
    (HRE_CAT, "ĐÁP ÁN: chưa dùng 4HR; dùng 4HRE", "correct"),                   # accented negation still read
    (HRE_CAT, "ĐÁP ÁN: khong dung 4HR; dung 4HRE", "correct"),                  # unaccented answer: unaccented words
    (HRE_CAT, "ĐÁP ÁN: Phac do chua HRE", "correct"),                          # 'chua' is ambiguous: not a negation
])
def test_accents_of_negation_words(a, out, label):
    g = lab(out, a)
    assert (g.label_name, g.multi) == (label, False)


# NÊN SỬA: every negation phrase has its English (Vietnamese) counterpart; each pair gets the same label, and the
# mirror (MoH negated instead of foreign) gets the mirrored label.
NEG_PAIRS = [
    ("4HRE; 4HR không còn được khuyến cáo", "4HRE; 4HR is no longer recommended"),
    ("4HRE; 4HR không phải lựa chọn đầu tay", "4HRE; 4HR is not first-line"),
    ("4HRE; 4HR không phải là lựa chọn đầu tiên", "4HRE; 4HR is not the first choice"),
    ("4HRE; không khuyến cáo 4HR", "4HRE; do not recommend 4HR"),
    ("4HRE; 4HR không khuyến cáo", "4HRE; 4HR not recommended"),
    ("4HRE; 4HR không được khuyến khích", "4HRE; 4HR is discouraged"),
    ("4HRE, bỏ 4HR", "4HRE, dropping 4HR"),
    ("4HRE; 4HR không cần thiết", "4HRE; 4HR is not necessary"),
    ("4HRE; 4HR nên tránh", "4HRE; 4HR should be avoided"),
    ("4HRE; 4HR bị chống chỉ định", "4HRE; 4HR is contraindicated"),
    ("4HRE; 4HR bị cấm", "4HRE; 4HR is prohibited"),
    ("4HRE, không bao giờ dùng 4HR", "4HRE, never use 4HR"),
    ("4HRE thay cho 4HR", "4HRE in place of 4HR"),
    ("4HRE thay vì 4HR", "4HRE instead of 4HR"),
    ("4HRE chứ không phải 4HR", "4HRE, not 4HR"),
    ("4HR không được ưu tiên; 4HRE", "4HR is not preferred; 4HRE"),
    ("4HRE; 4HR hiện không còn dùng", "4HRE; 4HR is currently no longer used"),
    ("4HRE; 4HR không nên", "4HRE; 4HR should not"),
    ("4HRE; tránh dùng 4HR", "4HRE; avoid using 4HR"),
    ("4HRE, ngoại trừ 4HR", "4HRE, except 4HR"),
    ("4HRE, không kèm 4HR", "4HRE, without 4HR"),
    ("4HRE - không dùng 4HR", "4HRE - do not use 4HR"),
    ("Không dùng 4HR vì nguy cơ kháng; dùng 4HRE", "Do not use 4HR because of resistance; use 4HRE"),
]


def _mirror(text: str) -> str:
    return text.replace("4HRE", "@").replace("4HR", "4HRE").replace("@", "4HR")


@pytest.mark.parametrize("vi,en", NEG_PAIRS)
def test_negation_pairs_are_symmetric(vi, en):
    for v, e, want in ((vi, en, "correct"), (_mirror(vi), _mirror(en), "foreign")):
        gv, ge = lab("ĐÁP ÁN: " + v, HRE_CAT, "vi"), lab("ANSWER: " + e, HRE_CAT, "en")
        assert (gv.label_name, gv.multi) == (ge.label_name, ge.multi) == (want, False), (v, e)


@pytest.mark.parametrize("vi,en,label", [
    # NÊN SỬA (vehicle): 'trong' and 'in' alike, and only after ANOTHER category in the same clause
    ("HES 6% trong NaCl 0,9%", "6% HES in 0.9% saline", "correct"),
    ("Dextran 40 pha trong NaCl 0,9%", "Dextran 40 diluted in 0.9% saline", "correct"),
    ("Cao phân tử (Dextran 40) pha trong NaCl 0,9%", "Colloid (dextran 40) diluted in 0.9% saline", "correct"),
    ("Bolus 10 ml/kg trong Ringer lactate", "A 10 mL/kg bolus in Ringer's lactate", "foreign"),     # was abstain
    ("Ringer lactate không phải lựa chọn đầu tiên; dùng cao phân tử", "Normal saline is not first-line; use colloid",
     "correct"),
    ("Cao phân tử không phải lựa chọn đầu tiên; dùng Ringer lactate", "Colloid is not first-line; use normal saline",
     "foreign"),
])
def test_vehicle_and_first_line_pairs(vi, en, label):
    gv, ge = lab("ĐÁP ÁN: " + vi, FLUID_CAT, "vi"), lab("ANSWER: " + en, FLUID_CAT, "en")
    assert (gv.label_name, gv.multi) == (ge.label_name, ge.multi) == (label, False)


@pytest.mark.parametrize("colloid_first,crystalloid_first,lang", [
    # CHẶN-5 (grader side): a conditional or fallback mention is a second value for EVERY category, in both orders
    ("Cao phân tử; Ringer lactate chỉ dùng khi sốc kháng trị", "Ringer lactate; cao phân tử chỉ dùng khi sốc kháng trị",
     "vi"),
    ("Cao phân tử; nếu không đáp ứng chuyển Ringer lactate", "Ringer lactate; nếu không đáp ứng chuyển cao phân tử", "vi"),
    ("Colloid; crystalloid only if colloid is unavailable", "Crystalloid; colloid only if refractory", "en"),
    ("Colloid first; Ringer's lactate if no response", "Ringer's lactate first; colloid if no response", "en"),
])
def test_conditional_mentions_are_second_values_both_ways(colloid_first, crystalloid_first, lang):
    pre = "ĐÁP ÁN: " if lang == "vi" else "ANSWER: "
    for out in (colloid_first, crystalloid_first):
        g = lab(pre + out, FLUID_CAT, lang)
        assert (g.label_name, g.multi) == ("unattributed", True), out


def _pilot_atoms() -> dict:
    import json

    from vnsoc.paths import paths

    f = paths().root / "data" / "interim" / "pilot_atoms.jsonl"
    if not f.exists():
        pytest.skip("pilot atoms absent")
    return {json.loads(x)["atom_id"]: json.loads(x) for x in f.read_text(encoding="utf-8").splitlines() if x}


@pytest.mark.parametrize("aid,out,lang,want", [
    # the reviewer's reproductions on the real pilot atoms (self-written answers): (label, multi)
    ("P-dengue-04", "ĐÁP ÁN: Không - metamizol không nên dùng", "vi", (2, False)),
    ("P-dengue-04", "ĐÁP ÁN: Không vì metamizol không được dùng", "vi", (2, False)),
    ("P-dengue-04", "ANSWER: No — metamizole is not recommended", "en", (2, False)),
    ("P-dengue-04", "ANSWER: No metamizole should be avoided", "en", (2, False)),
    ("P-dengue-03", "ANSWER: Colloid (dextran 40); HES is not recommended", "en", (2, False)),
    ("P-dengue-03", "ĐÁP ÁN: Dextran 40 (HES không được khuyến cáo)", "vi", (2, False)),
    ("P-dengue-03", "ĐÁP ÁN: Cao phân tử, HES không nên dùng", "vi", (2, False)),
    ("P-dengue-03", "ĐÁP ÁN: Dung dịch có chứa Ringer lactate", "vi", (4, False)),
    ("P-dengue-03", "ĐÁP ÁN: HES 6% trong NaCl 0,9%", "vi", (2, False)),
    ("P-dengue-03", "ANSWER: Give a 10 mL/kg bolus in Ringer's lactate", "en", (4, False)),
    ("P-dengue-03", "ĐÁP ÁN: Ringer lactate không phải lựa chọn đầu tiên; dùng cao phân tử", "vi", (2, False)),
    ("P-dengue-03", "ĐÁP ÁN: Truyền dịch; HES không được dùng", "vi", (6, False)),
    ("P-dengue-06", "ĐÁP ÁN: Có, gelatin có thể dùng thay thế; không dùng albumin", "vi", (2, False)),
    ("P-tbhiv-03", "ĐÁP ÁN: Phác đồ chứa HRE", "vi", (2, False)),
    ("P-tbhiv-03", "ĐÁP ÁN: Phác đồ duy trì chứa 4HR", "vi", (4, False)),
    ("P-tbhiv-03", "ANSWER: 4HRE; 4HR is no longer recommended", "en", (2, False)),
    ("P-tbhiv-03", "ĐÁP ÁN: 4HRE; 4HR không khuyến cáo", "vi", (2, False)),
    ("P-tbhiv-03", "ĐÁP ÁN: 4HRE (4HR chỉ dùng khi ...)", "vi", (5, True)),
    ("P-tbhiv-03", "ANSWER: 4HRE (4HR only if ...)", "en", (5, True)),
    ("P-tbhiv-04", "ĐÁP ÁN: Phác đồ chứa HR", "vi", (2, False)),
    ("P-hbv-04", "ANSWER: ALT above the ULN; 2×ULN is no longer required", "en", (2, False)),
    ("P-hbv-04", "ĐÁP ÁN: ALT > ULN; mức > 2 lần ULN không còn được yêu cầu", "vi", (2, False)),
    ("P-immunization-01", "ANSWER: the 9-month dose; some countries give it at 12 months", "en", (5, True)),
    ("P-immunization-01", "ĐÁP ÁN: mũi 9 tháng; một số nước tiêm lúc 12 tháng", "vi", (5, True)),
    ("P-immunization-04", "ĐÁP ÁN: Mũi 18 tháng, hoặc 15 tháng", "vi", (5, True)),
    ("P-immunization-04", "ANSWER: The 18-month booster, or 15 months", "en", (5, True)),
    ("P-immunization-02", "ĐÁP ÁN: Mũi nhắc lại 7 tuổi (sau mũi 18 tháng)", "vi", (2, False)),
    ("P-malaria_ocr-05", "ANSWER: Primaquine once a day for a week", "en", (2, False)),
    ("P-malaria_ocr-05", "ĐÁP ÁN: Primaquin ngày một lần trong một tuần", "vi", (2, False)),
    ("P-htn-01", "ANSWER: 120–129/<80 mmHg", "en", (5, False)),                # 1.3.0: no BP value, a number (5)
    ("P-hbv-03", "ANSWER: HBV DNA 10^4–10^5 copies/mL", "en", (5, False)),    # was 3 (10^4 read in IU/mL)
    ("P-hbv-03", "ANSWER: > 2*10^3 IU/mL", "en", (2, False)),                  # was 5 with decoy_match (210)
    ("P-immunization-02", "ĐÁP ÁN: năm tuổi", "vi", (4, False)), ("P-immunization-02", "ANSWER: five years", "en",
                                                                  (4, False)),
    ("P-malaria_ocr-05", "ĐÁP ÁN: Theo Bộ Y tế: một tuần", "vi", (2, False)),
    ("P-malaria_ocr-05", "ANSWER: Per MoH: one week", "en", (2, False)),
    ("P-malaria_ocr-06", "ANSWER: three consecutive days", "en", (2, False)),
    ("P-malaria_ocr-06", "ĐÁP ÁN: ba ngày liên tiếp", "vi", (2, False)),
])
def test_review_reproductions_on_pilot_atoms(aid, out, lang, want):
    g = grade_short(out, _pilot_atoms()[aid], lang, condition="A1")
    assert (g.label, g.multi) == want


@pytest.mark.parametrize("out,lang", [("ANSWER: ACT once a day", "en"), ("ĐÁP ÁN: Uống ngày một lần", "vi"),
                                      ("ĐÁP ÁN: Uống ngày 1 lần", "vi"), ("ANSWER: twice daily", "en")])
def test_frequency_is_not_the_one_day_decoy(out, lang):
    # NÊN SỬA (WEAK_ONE): 'a day' of 'once a day' is no duration; P-malaria_ocr-06's decoy is 1 day. A frequency
    # alone is a value in an unconvertible unit, like '1 lần/ngày' in 1.1.0 (label 5, no decoy flag)
    for a in (DAYS3, _pilot_atoms().get("P-malaria_ocr-06", DAYS3)):
        g = lab(out, a, lang)
        assert (g.label_name, g.parse_method, g.decoy_match) == ("unattributed", "unit_mismatch", False)


@pytest.mark.parametrize("a,out,label", [
    (DAYS7, "ANSWER: Primaquine once a day for a week", "correct"),                     # was 5 ('a day' = 1 day)
    (DAYS7, "ĐÁP ÁN: Primaquin ngày một lần trong một tuần", "correct"),
    (DAYS3, "ANSWER: 3 days, once daily", "correct"), (DAYS3, "ĐÁP ÁN: 3 ngày, ngày 1 lần", "correct"),
    (DAYS3, "ANSWER: 5 days, twice a day", "foreign"), (DAYS3, "ĐÁP ÁN: 5 ngày, ngày 2 lần", "foreign"),
])
def test_duration_next_to_a_frequency(a, out, label):
    g = lab(out, a, "en" if out.startswith("ANSWER") else "vi")
    assert (g.label_name, g.multi, g.decoy_match) == (label, False, False)


INTERVAL = atom(value_kind="num", unit="min", vn=[{"lo": 5, "hi": 15}], foreign=[{"system": "EU_UK", "values": [
    {"lo": 5, "hi": 5}]}])


@pytest.mark.parametrize("out,lang,label,method", [
    # a count is a count in both languages ('twice' = 'hai lần' = '2 lần'); 'once' / 'một lần' alone are adverbs
    ("ANSWER: Repeat twice", "en", "unattributed", "unit_mismatch"),
    ("ANSWER: Repeat two times", "en", "unattributed", "unit_mismatch"),
    ("ĐÁP ÁN: Nhắc lại hai lần", "vi", "unattributed", "unit_mismatch"),
    ("ĐÁP ÁN: Nhắc lại 2 lần", "vi", "unattributed", "unit_mismatch"),                  # as in 1.1.0
    ("ANSWER: Repeat once", "en", "abstain", "answer_line"), ("ĐÁP ÁN: Nhắc lại một lần", "vi", "abstain", "answer_line"),
    ("ĐÁP ÁN: 5–15 phút, tối đa hai lần", "vi", "correct", "answer_line"),
    ("ANSWER: every 5-15 minutes, up to twice", "en", "correct", "answer_line"),
])
def test_counts_read_alike(out, lang, label, method):
    g = lab(out, INTERVAL, lang)
    assert (g.label_name, g.parse_method) == (label, method)


@pytest.mark.parametrize("a,out,label,multi", [
    # CHẶN-4: a dose named by its age is a value (was masked: the foreign 12 months was left alone -> label 4)
    (MEASLES, "ANSWER: the 9-month dose; some countries give it at 12 months", "unattributed", True),
    (MEASLES, "ĐÁP ÁN: mũi 9 tháng; một số nước tiêm lúc 12 tháng", "unattributed", True),
    (MEASLES, "ANSWER: 9 months vaccine, or 12-15 months", "unattributed", True),
    (MEASLES, "ĐÁP ÁN: mũi 12 tháng; một số nước tiêm lúc 9 tháng", "unattributed", True),      # mirror
    (DTP18, "ĐÁP ÁN: Mũi 18 tháng, hoặc 15 tháng", "unattributed", True),
    (DTP18, "ANSWER: The 18-month booster, or 15 months", "unattributed", True),
    (DTP18, "ANSWER: The 15-month booster, or 18 months", "unattributed", True),                  # mirror
    (MEASLES, "ANSWER: the 9-month dose", "correct", False), (MEASLES, "ĐÁP ÁN: mũi 12 tháng", "foreign", False),
    # ... unless it is introduced as a reference point ("sau", "kể từ", "after", "following", "since")
    (BOOSTER, "ĐÁP ÁN: Mũi nhắc lại 7 tuổi (sau mũi 18 tháng)", "correct", False),                 # was 5
    (BOOSTER, "ANSWER: Booster at 7 years (after the 18-month dose)", "correct", False),
    (BOOSTER, "ANSWER: 4–6 years, following the 18 month booster", "foreign", False),
])
def test_age_named_doses_are_values(a, out, label, multi):
    g = lab(out, a, "en" if out.startswith("ANSWER") else "vi")
    assert (g.label_name, g.multi) == (label, multi)


@pytest.mark.parametrize("out,lang", [
    ("ANSWER: 120–129/<80 mmHg", "en"), ("ANSWER: Elevated BP 120-129/<80", "en"),     # was 4 (read as 129/80)
    ("ANSWER: ≥140/<90 mmHg", "en"), ("ĐÁP ÁN: tâm thu ≥ 140 và tâm trương < 90 mmHg", "vi"),
])
def test_bp_category_is_not_a_threshold(out, lang):
    g = lab(out, HTN, lang)                    # no BP value is read; since 1.3.0 a number that is no BP value is 5, not 6
    assert (g.label_name, g.parse_method, g.parsed) == ("unattributed", "unit_mismatch", [])


def test_pilot_conditional_mentions_symmetric():
    """P-dengue-03: a conditional mention is a second value whichever source comes first (atom colloid branch fixed
    2026-09-26, blind to outputs; DECISIONS grader 1.2.0)."""
    d3 = _pilot_atoms()["P-dengue-03"]
    for x, y, lang in [("Cao phân tử; Ringer lactate chỉ dùng khi sốc kháng trị",
                        "Ringer lactate; cao phân tử chỉ dùng khi sốc kháng trị", "vi"),
                       ("Colloid; crystalloid only if colloid is unavailable", "Crystalloid; colloid only if refractory",
                        "en")]:
        pre = "ĐÁP ÁN: " if lang == "vi" else "ANSWER: "
        assert grade_short(pre + x, d3, lang).label == grade_short(pre + y, d3, lang).label == 5




# ================================================================== grader 1.3.0 (27/9/2026, pre-freeze)
# From the AI check of the pilot grading (review/pilot_grading: 41 grader_error rows). Every answer below is SELF-WRITTEN
# to reproduce one error TYPE (no model output is copied); atoms are fixtures modelled on the pilot atoms, or the real
# pilot atoms where the atom's own patterns matter (skipped when absent). The main study is graded with 1.3.0; the
# pilot stays reported with 1.2.0.
from vnsoc.grade import classify_value, extra_drugs  # noqa: E402
from vnsoc.normalize_vi import Drugs  # noqa: E402

TB_CAT = atom(value_kind="cat", vn=[{"label": "HRE"}], foreign=[{"system": "US", "values": [{"label": "HR"}]}],
              decoy=[{"label": "RE"}],
              cat_options={"HRE": [r"(?<![a-z0-9])(?:hre|rhe)(?![a-z])",
                                   r"rifampi\w*,? (?:and |va )?isoniazid\w*,? (?:and |va )?ethambutol"],
                           "HR": [r"(?<![a-z0-9])(?:hr|rh)(?![a-z])"], "RE": [r"(?<![a-z0-9])(?:re|er)(?![a-z])"]})


# ------------------------------------------------------------------ E1a: a number that is no value of the atom's kind
@pytest.mark.parametrize("a,out,lang", [
    (FLUID_CAT, "ĐÁP ÁN: 500 ml/giờ", "vi"), (FLUID_CAT, "ANSWER: 20 mL/kg", "en"),        # cat: a rate, no fluid type
    (NSAID, "ĐÁP ÁN: 0 viên", "vi"), (NSAID, "ANSWER: 0 tablets", "en"),                   # cat yes/no: a dose
    (TB_CAT, "ĐÁP ÁN: 6 tháng", "vi"), (TB_CAT, "ANSWER: 6 months", "en"),                 # cat: the phase length
    (PEP, "ĐÁP ÁN: 3 thuốc", "vi"), (PEP, "ANSWER: 3 drugs", "en"),                         # drugs: a count
    (TB_FQ, "ĐÁP ÁN: 400 mg / 200 mg", "vi"),                                              # drugs: doses only
    (HTN, "ĐÁP ÁN: 150 mmHg", "vi"), (HTN, "ANSWER: 150 mmHg", "en"),                      # bp: systolic only
])
def test_number_of_another_kind_is_a_value_every_kind(a, out, lang):
    g = lab(out, a, lang, synonyms=SYN, combos=COMBOS) if a["value_kind"] == "drugs" else lab(out, a, lang)
    assert (g.label_name, g.parse_method, g.parsed, g.needs_llm) == ("unattributed", "unit_mismatch", [], False)


@pytest.mark.parametrize("out,lang", [("ĐÁP ÁN: Không rõ", "vi"), ("ANSWER: I do not know", "en"),
                                      ("ĐÁP ÁN: theo QĐ 1740/QĐ-BYT", "vi")])      # a citation is not a number
def test_no_number_is_still_an_abstention(out, lang):
    for a in (FLUID_CAT, PEP, HTN):
        assert lab(out, a, lang, synonyms=SYN, combos=COMBOS).label_name == "abstain"


@pytest.mark.parametrize("colloid,crystalloid", [
    ("ĐÁP ÁN: HES 6% không được dùng", "ĐÁP ÁN: NaCl 500 ml không được dùng"),
    ("ANSWER: avoid dextran 40", "ANSWER: avoid Ringer's lactate 500 mL")])
def test_negated_mention_with_a_number_is_unchanged_and_symmetric(colloid, crystalloid):
    # a number inside a product name must not tell a negated colloid from a negated crystalloid (both 6, as in 1.2.0).
    # Known, NOT changed in 1.3.0: a decimal concentration between the negation and the category ("avoid 0.9% saline",
    # "NaCl 0,9% không được dùng", "avoid 6% HES") defeats the negation reading, for every category (DECISIONS).
    lang = "en" if colloid.startswith("ANSWER") else "vi"
    for out in (colloid, crystalloid):
        g = lab(out, FLUID_CAT, lang)
        assert (g.label_name, g.parse_method) == ("abstain", "answer_line"), out


# ------------------------------------------------------------------ E1b: no answer line -> LLM extractor, not 6
@pytest.mark.parametrize("a,out", [
    (FLUID_CAT, "Truyền 20 ml/kg trong giờ đầu, sau đó đánh giá lại."),
    (TB_CAT, "The continuation phase lasts 4 months."),
    (PEP, "Uống trong 28 ngày, bắt đầu trong vòng 72 giờ."),
    (FLUID, "Có thể cho 3 viên mỗi ngày."),                                                   # num: unconvertible unit
    (TB_CAT, "Dùng rifampicin và pyrazinamid."),                                              # cat: drugs, no category
])
def test_fallback_with_numbers_or_drugs_goes_to_the_extractor(a, out):
    g = lab(out, a, "vi", synonyms=SYN, combos=COMBOS) if a["value_kind"] == "drugs" else lab(out, a)
    assert (g.label, g.needs_llm, g.parse_method) == (None, True, "fallback")


def test_fallback_without_value_like_text_is_still_an_abstention():
    for a in (FLUID_CAT, TB_CAT, FLUID):
        g = lab("Tôi không chắc, cần hỏi bác sĩ.", a)
        assert (g.label_name, g.needs_llm) == ("abstain", False)


def test_llm_extracted_answer_follows_the_answer_line_rule():
    g = grade_short("Không có dòng đáp án ở đây.", TB_CAT, "vi", extracted="6 tháng")
    assert (g.label_name, g.parse_method) == ("unattributed", "unit_mismatch")
    assert grade_short("…", TB_CAT, "vi", extracted="HRE").label_name == "correct"


# ------------------------------------------------------------------ E2: blood pressure with a unit on each part / a space
@pytest.mark.parametrize("out,lang,label,decoy", [
    ("ĐÁP ÁN: ≥ 140 mmHg / ≥ 90 mmHg", "vi", "correct", False),
    ("ANSWER: 130 mmHg / 80 mmHg", "en", "foreign", False), ("ANSWER: 150 mmHg/100 mmHg", "en", "unattributed", True),
    ("ĐÁP ÁN: 130 80 mmHg", "vi", "foreign", False), ("ANSWER: 140 90 mm Hg", "en", "correct", False),
    ("ĐÁP ÁN: HA 150 100", "vi", "unattributed", True), ("ANSWER: 130 mmHg 80 mmHg", "en", "foreign", False),
])
def test_blood_pressure_unit_per_part_and_space(out, lang, label, decoy):
    g = lab(out, HTN, lang)
    assert (g.label_name, g.decoy_match, g.multi, len(g.parsed)) == (label, decoy, False, 1)


# ------------------------------------------------------------------ E3: template placeholders, multiples of ULN
def test_placeholders_are_not_text():
    assert lab("ĐÁP ÁN: 15 <đơn vị>", FLUID).label_name == "correct"                     # read in the atom's unit
    assert lab("ANSWER: 5 <unit> mL/kg/h", FLUID, "en").label_name == "foreign"
    assert lab("ĐÁP ÁN: <giá trị> 20 ml/kg/giờ", FLUID).decoy_match


@pytest.mark.parametrize("out,lang,label", [
    ("ĐÁP ÁN: 1 <đơn vị> /ULN", "vi", 2), ("ANSWER: 1 x/ULN", "en", 2),                  # MoH > ULN
    ("ANSWER: 2 <value> times/ULN", "en", 3), ("ĐÁP ÁN: 2 lần/ ULN", "vi", 3),           # superseded 2×ULN
    ("ANSWER: 3 <times> /ULN", "en", 5), ("ĐÁP ÁN: 3 x /ULN", "vi", 5),                  # decoy 3×ULN
])
def test_uln_multiple_with_a_slash_on_the_pilot_atom(out, lang, label):
    g = grade_short(out, _pilot_atoms()["P-hbv-04"], lang, condition="A1")
    assert (g.label, g.multi, g.decoy_match) == (label, False, label == 5)


# ------------------------------------------------------------------ E4: a regimen with an extra drug is another regimen
SYM = atom(value_kind="drugs",
           vn=[{"key_drugs": ["linezolid"], "text": "linezolid + clofazimine"}],
           foreign=[{"system": "US", "values": [{"key_drugs": ["delamanid"], "text": "delamanid + clofazimine"}]}],
           superseded=[{"guideline": "old/2019", "values": [{"key_drugs": ["amikacin"],
                                                             "text": "amikacin + clofazimine"}]}],
           decoy=[{"key_drugs": ["pretomanid"], "text": "pretomanid + clofazimine"}])
ROLE_LABEL = {"linezolid": (2, [], [], False), "delamanid": (4, ["US"], [], False),
              "amikacin": (3, [], ["old/2019"], False), "pretomanid": (5, [], [], True)}


@pytest.mark.parametrize("key", sorted(ROLE_LABEL))
def test_extra_drug_rule_is_the_same_for_every_source(key):
    label, foreign, sup, decoy = ROLE_LABEL[key]
    for out in (f"ĐÁP ÁN: {key}", f"ĐÁP ÁN: {key} + clofazimin"):              # key alone, or the recorded regimen
        g = grade_short(out, SYM, "vi", SYN, COMBOS)
        assert (g.label, g.foreign_systems, g.superseded, g.decoy_match, g.multi) == (label, foreign, sup, decoy, False)
    g = grade_short(f"ANSWER: {key} + clofazimine + levofloxacin", SYM, "en", SYN, COMBOS)   # a drug of no regimen
    assert (g.label, g.foreign_systems, g.superseded, g.decoy_match) == (5, [], [], False)
    assert g.partial == (key == "linezolid")                                   # partial: an MoH key drug is named
    assert extra_drugs(Drugs(frozenset({key, "clofazimine", "levofloxacin"})), SYM, SYN, COMBOS) == ["levofloxacin"]


@pytest.mark.parametrize("a,out,label,partial", [
    (HBV_NA, "ĐÁP ÁN: TDF + lamivudin", 5, True),                 # monotherapy asked: a combination is another value
    (HBV_NA, "ANSWER: entecavir plus 3TC", 5, True),
    (HBV_NA, "ĐÁP ÁN: TDF hoặc ETV", 2, False),                   # two MoH alternatives: every drug belongs to one
    (PEP, "ANSWER: TDF + 3TC + DTG + NVP", 5, True),              # joined: ONE 4-drug regimen, recorded nowhere
    (PEP, "ANSWER: TDF + 3TC + DTG or TDF + 3TC + NVP", 5, False),  # listed: MoH + decoy regimen (rule 7), multi
    (PEP, "ĐÁP ÁN: TDF + FTC + DTG", 2, False),                   # FTC: background of the atom (a text names it)
    (PEP, "ĐÁP ÁN: BIC/FTC/TAF + EFV", 5, False),                 # a foreign regimen plus a drug of no regimen
    (TB_FQ, "ANSWER: BPaL + clofazimine", 5, True),
    (TB_SHORT, "ĐÁP ÁN: amikacin, levofloxacin, linezolid", 5, False),   # superseded chain + a drug it does not hold
])
def test_extra_drugs_examples(a, out, label, partial):
    g = grade_short(out, a, "en" if out.startswith("ANSWER") else "vi", SYN, COMBOS)
    assert (g.label, g.partial) == (label, partial)


@pytest.mark.parametrize("out,label,multi,decoy", [
    ("ĐÁP ÁN: linezolid hoặc amikacin", 5, True, False),           # MoH + superseded regimen (new in 1.3.0; was 2)
    ("ĐÁP ÁN: linezolid, pretomanid", 5, True, True),              # MoH + decoy regimen (new in 1.3.0; was 2)
    ("ĐÁP ÁN: linezolid hoặc delamanid", 5, True, False),          # MoH + conflicting foreign regimen (rule 7, 1.1.0)
    # joined by '+': ONE combined regimen recorded nowhere (review of 1.3.0): 5, not two values, no source flag
    ("ĐÁP ÁN: linezolid + amikacin", 5, False, False), ("ĐÁP ÁN: linezolid + pretomanid", 5, False, False),
    ("ĐÁP ÁN: linezolid + delamanid", 5, False, False),
    ("ĐÁP ÁN: Theo Bộ Y tế: linezolid. Theo Mỹ (US): delamanid", 1, True, False),      # attributed (rule 7)
    ("ĐÁP ÁN: Theo Bộ Y tế: linezolid. Theo quyết định cũ: amikacin", 5, True, False),  # superseded is not foreign
])
def test_two_recorded_regimens_in_one_list_are_two_values(out, label, multi, decoy):
    g = grade_short(out, SYM, "vi", SYN, COMBOS)
    assert (g.label, g.multi, g.decoy_match) == (label, multi, decoy)


def test_same_value_texts_are_pooled():
    # WHO 2026 (ethionamide) = MoH C1a (prothionamide) at gap 0: the WHO spelling of the regimen is still the MoH value
    syn, combos = _real()
    for out in ("ĐÁP ÁN: 4-6 Bdq-Lfx-Eto-E-Z-Hh-Cfz", "ĐÁP ÁN: 4-6 Bdq-Lfx-Pto-E-Z-Hh-Cfz"):
        g = grade_short(out, TB_SHORT, "vi", syn, combos)
        assert (g.label, g.foreign_systems) == (2, ["WHO_global"]), out
    g = grade_short("ĐÁP ÁN: 4-6 Bdq-Lfx-Pto-Cfz + rifampicin", TB_SHORT, "vi", syn, combos)   # rifampicin: no regimen
    assert (g.label, g.partial) == (5, True)


def test_item_without_text_reads_its_key_drugs_only():
    bare = atom(value_kind="drugs", vn=[{"key_drugs": [TDF]}],
                foreign=[{"system": "US", "values": [{"key_drugs": [TAF]}]}])
    assert grade_short("ĐÁP ÁN: TDF", bare, "vi", SYN, COMBOS).label == 2
    assert grade_short("ĐÁP ÁN: TDF + 3TC", bare, "vi", SYN, COMBOS).label == 5          # strict: nothing recorded
    assert grade_short("ĐÁP ÁN: TAF + 3TC", bare, "vi", SYN, COMBOS).label == 5


def test_class_named_in_a_recorded_text_names_the_items_own_member():
    # 'Tenofovir 300 mg' recorded for a TDF item names TDF (review of 1.3.0: before, every member, so 'TDF + TAF' fitted
    # the TDF regimen); a class in a text of an item keyed on neither member names every member
    old = atom(value_kind="drugs", vn=[{"key_drugs": ["entecavir"], "text": "ETV"}],
               superseded=[{"guideline": "5448/2014", "values": [{"key_drugs": [TDF], "text": "Tenofovir 300 mg/ngày"}]}])
    assert grade_short("ĐÁP ÁN: TDF", old, "vi", SYN, COMBOS).label == 3
    c = classify_value(Drugs(frozenset({TDF, "lamivudine"})), old, SYN, COMBOS)
    assert (c["superseded"], c["extra"]) == ([], ["lamivudine"])
    assert grade_short("ĐÁP ÁN: TDF + TAF", old, "vi", SYN, COMBOS).label == 5
    from vnsoc.grade import regimen_drugs

    other = atom(value_kind="drugs", vn=[{"key_drugs": ["dolutegravir"], "text": "DTG + tenofovir + 3TC"}])
    assert regimen_drugs(other["vn"][0], other, SYN, COMBOS) >= {TDF, TAF, "lamivudine", "dolutegravir"}


def test_containment_helpers_unchanged_for_span_checks():
    # verify_span.missing_vn_values reads a whole MoH span with `matches` (containment): extra drugs there are fine
    from vnsoc.grade import matches

    assert matches(Drugs(frozenset({TDF, "lamivudine", "dolutegravir", "efavirenz"})), PEP["vn"][0], PEP)[0]


# ------------------------------------------------------------------ E5: drug names, TB letters written apart
@pytest.mark.parametrize("text,names", [
    ("Truvada", {TDF, "emtricitabine"}), ("Descovy", {TAF, "emtricitabine"}),
    ("DRV/r", {"darunavir", "ritonavir"}), ("darunavir/ritonavir", {"darunavir", "ritonavir"}),
    ("LPV/r", {"lopinavir", "ritonavir"}), ("ATV/r", {"atazanavir", "ritonavir"}),
    ("Kaletra", {"lopinavir", "ritonavir"}), ("rifabutin", {"rifabutin"}), ("streptomycin", {"streptomycin"}),
    ("kanamycin", {"kanamycin"}), ("Moxyfloxacin", {"moxifloxacin"}),
    ("bedaquiline, pretomanid, linezolid and moxyfloxacin", {"BPaLM"}),
])
def test_new_drug_names_1_3_0(text, names):
    syn, combos = _real()
    assert parse_drugs(text, syn, combos).names == frozenset(names)


@pytest.mark.parametrize("out,lang,label", [
    ("ANSWER: Truvada plus dolutegravir", "en", 2), ("ĐÁP ÁN: Descovy + DTG", "vi", 4),
    ("ANSWER: TDF/FTC + LPV/r", "en", 5), ("ĐÁP ÁN: Truvada + rifabutin", "vi", 5),      # were 6 (not read)
])
def test_new_drug_names_are_graded(out, lang, label):
    syn, combos = _real()
    assert grade_short(out, PEP, lang, syn, combos).label == label


def test_misspelled_moxifloxacin_is_not_dropped():
    syn, combos = _real()
    assert grade_short("ANSWER: BPaL plus moxyfloxacin", TB_FQ, "en", syn, combos).label == 5   # BPaLM, not BPaL
    assert grade_short("ĐÁP ÁN: bedaquilin, pretomanid, linezolid", TB_FQ, "vi", syn, combos).label == 2


@pytest.mark.parametrize("out,lang,label,decoy", [
    ("ĐÁP ÁN: 4 R-H-E", "vi", "correct", False), ("ANSWER: H R", "en", "foreign", False),
    ("ĐÁP ÁN: R E /tháng", "vi", "unattributed", True), ("ANSWER: R H", "en", "foreign", False),
    ("ANSWER: E H R", "en", "correct", False),                   # 'EHR': read in the order the patterns read (HRE)
])
def test_tb_letters_written_apart(out, lang, label, decoy):
    g = lab(out, TB_CAT, lang)
    assert (g.label_name, g.decoy_match) == (label, decoy)


# ------------------------------------------------------------------ E6: a drug outside a closed category set
@pytest.mark.parametrize("a,out,lang", [
    (TB_CAT, "ĐÁP ÁN: isoniazid + pyrazinamid", "vi"), (TB_CAT, "ANSWER: ethambutol and pyrazinamide", "en"),
    (TB_CAT, "ANSWER: rifampicin, isoniazid, pyrazinamide and ethambutol", "en"),      # all four, no category
    (FLUID_CAT, "ĐÁP ÁN: adrenalin", "vi"),                                            # any drug, any cat atom
])
def test_drug_outside_the_categories_is_a_value(a, out, lang):
    g = lab(out, a, lang)
    assert (g.label_name, g.parse_method, g.decoy_match) == ("unattributed", "unlisted", False)


def test_category_named_by_drugs_still_wins():
    assert lab("ANSWER: rifampicin, isoniazid, ethambutol", TB_CAT, "en").label_name == "correct"


# ------------------------------------------------------------------ global regression on the 65 pilot atoms
KNOWN_RENDER_EXCEPTIONS = {("P-dengue-03", "foreign")}   # US text 'crystalloid; colloid only if refractory' = 2 values


def test_rendered_values_of_pilot_atoms_get_their_role():
    """Every recorded value of every pilot atom, rendered as an option (qgen.render, VI and EN), is graded with its own
    role; conflict_status and tolerance recomputed equal the stored ones (unchanged by 1.3.0)."""
    from vnsoc.grade import _gap, conflict_status
    from vnsoc.qgen.render import render_value

    syn, combos = _real()
    bad = set()
    for a in _pilot_atoms().values():
        assert conflict_status(a) == a["conflict_status"] and compute_tolerance(a) == pytest.approx(a["tolerance"])
        fr = [y for f in a.get("foreign") or [] for y in f["values"] if not y.get("derived")]
        sup = [y for s in a.get("superseded") or [] for y in s["values"] if not y.get("derived")]
        items = [("vn", it) for it in a["vn"]] + [("foreign", it) for it in fr] + [("superseded", it) for it in sup]
        for role, it in items + [("decoy", it) for it in a.get("decoy") or []]:
            def same(xs, it=it, a=a):
                return any(_gap(it, x, a) == 0 for x in xs)
            ok = {"vn": {2}, "superseded": {3} | ({2} if same(a["vn"]) else set()),
                  "foreign": {4} | ({3} if same(sup) else set()) | ({2} if same(a["vn"]) else set()),
                  "decoy": {5}}[role]
            for lang, pre in (("vi", "ĐÁP ÁN: "), ("en", "ANSWER: ")):
                g = grade_short(pre + render_value(it, a, lang, syn, combos), a, lang, syn, combos, condition="A1")
                if g.label not in ok or (role == "decoy" and not g.decoy_match):
                    bad.add((a["atom_id"], role))
    assert bad == KNOWN_RENDER_EXCEPTIONS


# ================================================================== grader 1.3.0 after the independent review (27/9/2026)
# Regression tests for the review of the first 1.3.0 draft (4 CHẶN, NÊN SỬA, THẤP). Every answer is SELF-WRITTEN (no
# model output copied); fixtures are modelled on the pilot atoms, or are the real pilot atoms where their own records
# matter (skipped when absent). Each rule is tested with its mirror for the other source.

# ------------------------------------------------------------------ CHẶN E1: abstention / asking back before rule 5
STEM_CAT = atom(value_kind="cat", vn=[{"label": "HRE"}], foreign=[{"system": "US", "values": [{"label": "HR"}]}],
                decoy=[{"label": "RE"}], cat_options=TB_CAT["cat_options"],
                condition="Lao phổi mới — phác đồ chuẩn 6 tháng", intervention="Thuốc giai đoạn duy trì 4 tháng",
                population={"age": "người lớn ≥ 18 tuổi", "window": "trong 72 giờ", "ga": "tuần 24–28"})
STEM_PEP = dict(PEP, population={"exposure": "phơi nhiễm trong 72 giờ", "age": "≥ 14 tuổi"})


@pytest.mark.parametrize("out,lang,unit", [
    ("ĐÁP ÁN: Không rõ, cần hỏi bác sĩ trong 24 giờ", "vi", True),
    ("ANSWER: I don't know; see a doctor within 24 hours", "en", True),
    ("ANSWER: Insufficient information (depends on age ≥ 14 years)", "en", True),
    ("ĐÁP ÁN: Không đủ thông tin để trả lời (tùy cân nặng > 35 kg)", "vi", True),
    ("ANSWER: Unable to determine; it varies with 3 factors", "en", False),
    ("ĐÁP ÁN: Chưa rõ, cần thêm 2 xét nghiệm", "vi", False),
])
def test_abstention_with_an_incidental_number_is_label_6_every_kind(out, lang, unit):
    # num atoms: a number WITHOUT a unit is read in the atom's unit (registered rule 3, unit_assumed), so only the
    # unit-bearing variants reach rule 5 there (known limitation, DECISIONS)
    for a in (FLUID_CAT, TB_CAT, NSAID, PEP, HTN, TB_FQ) + ((FLUID,) if unit else ()):
        g = lab(out, a, lang, synonyms=SYN, combos=COMBOS)
        assert (g.label_name, g.needs_llm) == ("abstain", False), (out, a["value_kind"])
    g = grade_short("…", PEP, lang, SYN, COMBOS, extracted=out.split(": ", 1)[1])      # LLM-extracted: same rule
    assert g.label_name == "abstain"


def test_a_hedged_value_is_still_a_value():
    # the abstention rule applies only when no value of the atom's kind is read
    assert lab("ĐÁP ÁN: Không chắc, có lẽ 15 ml/kg/giờ", FLUID).label_name == "correct"
    assert lab("ANSWER: Not sure, probably 5-10 mL/kg/h", FLUID, "en").label_name == "foreign"
    assert lab("ANSWER: not sure — TDF + 3TC + DTG", PEP, "en", synonyms=SYN, combos=COMBOS).label_name == "correct"


@pytest.mark.parametrize("out,lang", [
    ("ANSWER: Which guideline? It differs between the 2 systems", "en"),
    ("ĐÁP ÁN: Theo quốc gia nào? (mỗi nước có 1 ngưỡng khác)", "vi"),
    ("ANSWER: Which country? US and Vietnam differ by 10 mmHg", "en"),
])
def test_asking_back_in_the_answer_line_is_label_1_under_a0_only(out, lang):
    for a in (HTN, PEP, TB_CAT, FLUID_CAT):
        g = lab(out, a, lang, synonyms=SYN, combos=COMBOS, condition="A0")
        assert g.label_name == "correct_aware", (out, a["value_kind"])
        g1 = lab(out, a, lang, synonyms=SYN, combos=COMBOS, condition="A1")         # not A0: rule 5 as before
        assert g1.label_name in ("unattributed", "abstain")


@pytest.mark.parametrize("a,out,lang", [
    (STEM_CAT, "ANSWER: standard 6-month regimen", "en"), (STEM_CAT, "ĐÁP ÁN: phác đồ 6 tháng chuẩn", "vi"),
    (STEM_CAT, "ANSWER: an adult (≥ 18 years) regimen", "en"), (STEM_CAT, "ANSWER: OGTT at weeks 24-28", "en"),
    (STEM_PEP, "ANSWER: PEP within 72 hours", "en"), (STEM_PEP, "ĐÁP ÁN: dự phòng trong vòng 72 giờ", "vi"),
    (TB_CAT, "ANSWER: first-line (bậc 1) regimen", "en"), (PEP, "ĐÁP ÁN: ARV bậc 1 ưu tiên", "vi"),
    (PEP, "ANSWER: a 2nd-line regimen", "en"),
])
def test_stem_numbers_in_a_phrase_and_ordinal_labels_are_not_values(a, out, lang):
    g = lab(out, a, lang, synonyms=SYN, combos=COMBOS)
    assert (g.label_name, g.parse_method) == ("abstain", "answer_line")


@pytest.mark.parametrize("a,out,lang", [
    (STEM_CAT, "ĐÁP ÁN: 4 tháng", "vi"), (STEM_CAT, "ANSWER: 6 months", "en"),        # a bare quantity is an answer
    (STEM_PEP, "ANSWER: 72 hours", "en"), (STEM_CAT, "ANSWER: an 8-month regimen", "en"),   # not in the stem
])
def test_bare_quantity_or_new_number_is_still_rule_5(a, out, lang):
    g = lab(out, a, lang, synonyms=SYN, combos=COMBOS)
    assert (g.label_name, g.parse_method) == ("unattributed", "unit_mismatch")


def test_fallback_abstention_with_numbers_still_goes_to_the_extractor():
    g = lab("Tôi không chắc. Hãy đến cơ sở y tế trong 24 giờ.", PEP, synonyms=SYN, combos=COMBOS)
    assert (g.label, g.needs_llm) == (None, True)


@pytest.mark.parametrize("out,lang", [("ĐÁP ÁN: Không rõ", "vi"), ("ĐÁP ÁN: Không biết", "vi"),
                                      ("ANSWER: No information available", "en"), ("ANSWER: Not sure", "en"),
                                      ("ĐÁP ÁN: Không có đủ thông tin (cần 2 lần xét nghiệm)", "vi")])
def test_abstention_is_not_the_answer_no_of_a_yes_no_atom(out, lang):
    assert lab(out, NSAID, lang).label_name == "abstain"                    # was 'correct' ('không'/'no' = No)


@pytest.mark.parametrize("out,lang,label", [
    ("ĐÁP ÁN: Không, không rõ lợi ích nên không dùng metamizol", "vi", "correct"),
    ("ANSWER: No - unknown benefit, metamizole is not recommended", "en", "correct"),
    ("ĐÁP ÁN: Có, dù chưa rõ cơ chế", "vi", "foreign"), ("ANSWER: Yes, though the mechanism is unknown", "en", "foreign"),
])
def test_yes_no_answer_with_an_abstention_word_keeps_its_answer(out, lang, label):
    assert lab(out, NSAID, lang).label_name == label


# ------------------------------------------------------------------ NÊN SỬA E1: correct BP forms that were not read
@pytest.mark.parametrize("out,lang,label", [
    ("ANSWER: ≥140 mmHg or ≥90 mmHg", "en", "correct"), ("ĐÁP ÁN: ≥ 140 mmHg hoặc ≥ 90 mmHg", "vi", "correct"),
    ("ANSWER: ≥130 mmHg or ≥80 mmHg", "en", "foreign"), ("ĐÁP ÁN: ≥ 130 mmHg hay ≥ 80 mmHg", "vi", "foreign"),
    ("ANSWER: 140 by 90 mmHg", "en", "correct"), ("ANSWER: 130 by 80 mmHg", "en", "foreign"),
    ("ANSWER: 140-159 mmHg / 90-99 mmHg", "en", "correct"), ("ANSWER: 130-139 mmHg / 80-89 mmHg", "en", "foreign"),
    ("ANSWER: SBP 140 mmHg, 90 mmHg DBP", "en", "correct"), ("ANSWER: SBP 130 mmHg, 80 mmHg DBP", "en", "foreign"),
    ("ĐÁP ÁN: 140 mmHg tâm thu, tâm trương 90", "vi", "correct"), ("ĐÁP ÁN: tâm trương 80, 130 mmHg tâm thu", "vi", "foreign"),
])
def test_blood_pressure_forms_after_review(out, lang, label):
    g = lab(out, HTN, lang)
    assert (g.label_name, g.multi, len(g.parsed)) == (label, False, 1)


@pytest.mark.parametrize("out", ["ĐÁP ÁN: 140 mmHg hoặc 150 mmHg", "ANSWER: 140 or 90", "ANSWER: ≥ 140 mmHg or < 90 mmHg",
                                 "ĐÁP ÁN: HA tâm thu ≥ 140 mmHg 30 phút sau nghỉ"])
def test_no_blood_pressure_is_invented(out):
    assert lab(out, HTN, "vi").parsed == []


# ------------------------------------------------------------------ CHẶN E3: a filled slot keeps its text
@pytest.mark.parametrize("text,cleaned", [
    ("4 <weeks>", "4 weeks"), ("<TDF>", "TDF"), ("ĐÁP ÁN:<Không>", "ĐÁP ÁN: Không"), ("15 <mL/kg/h>", "15 mL/kg/h"),
    ("<isoniazid and rifampicin>", "isoniazid and rifampicin"), ("2 <times> /ULN", "2 x ULN"),
    ("<value> <unit>", ""), ("<giá trị> 20 <đơn vị>", "20"), ("<b>ALT > ULN</b>", "ALT > ULN"), ("<chữ cái>", ""),
    ("ALT<ULN>", "ALT<ULN>"), ("< 140 và > 90", "< 140 và > 90"), ("<5 tuổi", "<5 tuổi"), ("120–129/<80", "120-129/<80"),
    ("ALT<ULN và DNA>2000 IU/mL", "ALT<ULN và DNA>2000 IU/mL"),
])
def test_template_slots(text, cleaned):
    from vnsoc.normalize_vi import clean

    assert clean(text) == cleaned


@pytest.mark.parametrize("a,out,lang,label", [
    (HBV_NA, "ANSWER: <TDF>", "en", 2), (HBV_NA, "ĐÁP ÁN: <Entecavir>", "vi", 2),
    (NSAID, "ĐÁP ÁN: <Không>", "vi", 2), (NSAID, "ANSWER: <Yes>", "en", 4),
    (TB_CAT, "ANSWER: <RHE>", "en", 2), (TB_CAT, "ANSWER: <HR>", "en", 4),
    (FLUID_CAT, "ĐÁP ÁN: <cao phân tử>", "vi", 2), (FLUID_CAT, "ANSWER: <Ringer lactate>", "en", 4),
    (FLUID, "ANSWER: 15 <mL/kg/h>", "en", 2), (FLUID, "ANSWER: 20 <mL/kg/h>", "en", 5),
])
def test_filled_slot_is_graded_like_the_plain_answer(a, out, lang, label):
    g = lab(out, a, lang, synonyms=SYN, combos=COMBOS)
    plain = lab(out.replace("<", "").replace(">", ""), a, lang, synonyms=SYN, combos=COMBOS)
    assert g.label == plain.label == label


def test_unit_written_in_a_slot_is_that_unit():
    days = atom(value_kind="num", unit="day", vn=[{"lo": 28, "hi": 28}],
                foreign=[{"system": "US", "values": [{"lo": 30, "hi": 30}]}])
    assert lab("ANSWER: 4 <weeks>", days, "en").label_name == "correct"             # 28 days (was 4 days: 5)
    assert lab("ANSWER: 30 <days>", days, "en").label_name == "foreign"
    assert lab("ANSWER: 4 <value> <unit>", days, "en").unit_assumed                  # a template word adds nothing


# ------------------------------------------------------------------ CHẶN E4: one background per atom (symmetry)
ACT = atom(value_kind="drugs",
           vn=[{"key_drugs": ["pyronaridine-artesunate"], "text": "pyronaridin-artesunat 3 ngày + primaquin liều duy nhất"}],
           foreign=[{"system": "WHO_global", "values": [{"key_drugs": ["artemether-lumefantrine"],
                                                         "text": "artemether-lumefantrin"}]}],
           decoy=[{"key_drugs": ["artesunate-mefloquine"], "text": "artesunat-mefloquin"}])
ACT_MIRROR = atom(value_kind="drugs",
                  vn=[{"key_drugs": ["pyronaridine-artesunate"], "text": "pyronaridin-artesunat"}],
                  foreign=[{"system": "WHO_global", "values": [{"key_drugs": ["artemether-lumefantrine"],
                                                                "text": "artemether-lumefantrin + primaquin liều duy nhất"}]}],
                  decoy=[{"key_drugs": ["artesunate-mefloquine"], "text": "artesunat-mefloquin"}])


@pytest.mark.parametrize("a", [ACT, ACT_MIRROR], ids=["moh_text_names_pq", "who_text_names_pq"])
@pytest.mark.parametrize("act,label,decoy", [("pyronaridine-artesunate", 2, False),
                                             ("artemether-lumefantrine", 4, False), ("artesunate-mefloquine", 5, True)])
def test_backbone_drug_is_allowed_whichever_text_records_it(a, act, label, decoy):
    syn, combos = _real()
    for tail in ("", " + primaquine", " plus single-dose primaquine"):
        g = grade_short(f"ANSWER: {act}{tail}", a, "en", syn, combos)
        assert (g.label, g.decoy_match) == (label, decoy), tail
    g = grade_short(f"ANSWER: {act} + doxycycline", a, "en", syn, combos)            # a drug no text names
    assert (g.label, g.decoy_match, g.foreign_systems) == (5, False, [])


def test_background_of_the_pilot_drug_atoms():
    from vnsoc.grade import background_drugs

    syn, combos = _real()
    atoms = _pilot_atoms()
    want = {"P-hbv-06": set(), "P-malaria_ocr-01": set(), "P-malaria_ocr-02": {"primaquine"},
            "P-tbhiv-05": {"lamivudine", "emtricitabine"}}
    for aid, bg in want.items():
        assert background_drugs(atoms[aid], syn, combos) == bg, aid


def test_pilot_drug_atoms_symmetric_under_background_and_extra_drugs():
    """Every recorded regimen of every pilot drug atom (VI and EN): adding a background drug of the atom keeps the
    label and flags (unless the addition forms another named regimen, e.g. BPaL + moxifloxacin = BPaLM); adding a drug
    no record names gives 5 with no source and no decoy flag, for every source alike."""
    from vnsoc.grade import background_drugs
    from vnsoc.qgen.render import drug_display, render_value

    syn, combos = _real()
    disp = drug_display()
    for a in _pilot_atoms().values():
        if a["value_kind"] != "drugs":
            continue
        bg = sorted(background_drugs(a, syn, combos))
        items = [it for it in a["vn"]] + [it for f in a["foreign"] for it in f["values"] if not it.get("derived")]
        items += [it for s in a.get("superseded") or [] for it in s["values"] if not it.get("derived")]
        for it in items + list(a.get("decoy") or []):
            for lang, pre in (("vi", "ĐÁP ÁN: "), ("en", "ANSWER: ")):
                base = render_value(it, a, lang, syn, combos)
                g0 = grade_short(pre + base, a, lang, syn, combos, condition="A1")
                for b in bg:
                    out = f"{pre}{base} + {disp[b][lang]}"
                    if parse_drugs(out, syn, combos).names != parse_drugs(pre + base, syn, combos).names | {b}:
                        continue                                            # forms another named regimen
                    g = grade_short(out, a, lang, syn, combos, condition="A1")
                    assert (g.label, g.decoy_match, g.foreign_systems, g.superseded) == (
                        g0.label, g0.decoy_match, g0.foreign_systems, g0.superseded), out
                g = grade_short(f"{pre}{base} + raltegravir", a, lang, syn, combos, condition="A1")
                assert (g.label, g.decoy_match, g.foreign_systems, g.superseded) == (5, False, [], []), base


@pytest.mark.parametrize("out,label,decoy,foreign", [
    ("ANSWER: TDF + FTC + EFV", 5, True, []), ("ANSWER: TDF + 3TC + EFV", 5, True, []),      # decoy, either backbone
    ("ANSWER: TAF + FTC + DTG", 4, False, ["US"]), ("ANSWER: TAF + 3TC + DTG", 4, False, ["US"]),
    ("ANSWER: TDF + FTC + DTG", 2, False, ["US", "WHO_global"]),
    ("ANSWER: TDF + 3TC + DTG + raltegravir", 5, False, []), ("ANSWER: TDF + 3TC + zidovudine", 5, False, []),
])
def test_pilot_pep_backbone_is_symmetric(out, label, decoy, foreign):
    syn, combos = _real()
    g = grade_short(out, _pilot_atoms()["P-tbhiv-05"], "en", syn, combos, condition="A1")
    assert (g.label, g.decoy_match, g.foreign_systems) == (label, decoy, foreign)


# ------------------------------------------------------------------ CHẶN E4: a drug the answer excludes is not read
@pytest.mark.parametrize("out,lang,label,decoy", [
    ("ĐÁP ÁN: TDF + 3TC + DTG (không dùng EFV)", "vi", 2, False), ("ANSWER: TDF + 3TC + DTG, not EFV", "en", 2, False),
    ("ANSWER: TLD instead of TLE", "en", 2, False), ("ANSWER: TLE instead of TLD", "en", 5, True),     # mirror
    ("ANSWER: TAF + FTC + DTG (avoid TDF)", "en", 4, False), ("ĐÁP ÁN: TDF + 3TC + DTG (tránh TAF)", "vi", 2, False),
    ("ANSWER: TDF + 3TC + DTG (avoid nevirapine)", "en", 2, False),
    ("ANSWER: TDF/3TC/DTG for 28 days; co-trimoxazole is not needed", "en", 2, False),
    ("ĐÁP ÁN: không dùng EFV hoặc NVP; dùng TDF + 3TC + DTG", "vi", 2, False),
    ("ANSWER: EFV or NVP should be avoided; TDF + 3TC + DTG", "en", 2, False),
    ("ĐÁP ÁN: không dùng EFV, TDF + 3TC + DTG", "vi", 2, False),        # a comma ends the negated list
])
def test_negated_drugs_are_not_part_of_the_regimen(out, lang, label, decoy):
    syn, combos = _real()
    g = grade_short(out, _pilot_atoms()["P-tbhiv-05"], lang, syn, combos, condition="A1")
    assert (g.label, g.decoy_match, g.multi) == (label, decoy, False)


@pytest.mark.parametrize("out,lang,label", [
    ("ĐÁP ÁN: TDF hoặc ETV (không dùng lamivudin vì dễ kháng)", "vi", 2),
    ("ANSWER: Entecavir or TDF; adefovir is no longer recommended", "en", 2),
    ("ANSWER: TDF + lamivudine (not entecavir)", "en", 5),                 # the negation does not rescue the combination
    ("ĐÁP ÁN: ETV (không phối hợp TDF)", "vi", 2),
])
def test_negated_drugs_hbv(out, lang, label):
    syn, combos = _real()
    assert grade_short(out, _pilot_atoms()["P-hbv-06"], lang, syn, combos, condition="A1").label == label


@pytest.mark.parametrize("out,lang,label", [
    ("ANSWER: BPaL (bedaquiline, pretomanid, linezolid); moxifloxacin is omitted", "en", 2),
    ("ĐÁP ÁN: BPaL, không kèm moxifloxacin do kháng FQ", "vi", 2),
    ("ĐÁP ÁN: BDLC (không dùng pretomanid)", "vi", 4),
    ("ANSWER: BPaL + moxifloxacin", "en", 5),                                 # BPaLM: stated, a different regimen
])
def test_negated_drugs_tb(out, lang, label):
    syn, combos = _real()
    assert grade_short(out, _pilot_atoms()["P-tbhiv-01"], lang, syn, combos, condition="A1").label == label


@pytest.mark.parametrize("out,lang", [("ĐÁP ÁN: Không dùng pyrazinamid", "vi"), ("ANSWER: pyrazinamide is not continued", "en"),
                                      ("ANSWER: stop pyrazinamide and ethambutol", "en"),
                                      ("ĐÁP ÁN: ngừng pyrazinamid và ethambutol", "vi")])
def test_negated_drug_is_not_an_unlisted_value(out, lang):
    assert lab(out, TB_CAT, lang).label_name == "abstain"


# ------------------------------------------------------------------ E4: a '+' combination is one regimen
@pytest.mark.parametrize("out,lang,label,partial,multi", [
    ("ĐÁP ÁN: TDF + ETV", "vi", 5, True, False), ("ANSWER: TDF plus TAF", "en", 5, True, False),
    ("ĐÁP ÁN: TDF phối hợp ETV", "vi", 5, True, False),
    ("ĐÁP ÁN: TDF hoặc ETV", "vi", 2, False, False), ("ANSWER: TDF, TAF or ETV", "en", 2, False, False),
    ("ANSWER: TDF and ETV", "en", 2, False, False),                          # 'and' lists the preferred drugs
])
def test_moh_alternatives_joined_by_plus_are_a_combination(out, lang, label, partial, multi):
    syn, combos = _real()
    g = grade_short(out, _pilot_atoms()["P-hbv-06"], lang, syn, combos, condition="A1")
    assert (g.label, g.partial, g.multi) == (label, partial, multi)


@pytest.mark.parametrize("out,label", [
    ("ANSWER: artemether-lumefantrine + artesunate-amodiaquine", 5),          # foreign alternatives joined: mirror
    ("ANSWER: artemether-lumefantrine or artesunate-amodiaquine", 4),
])
def test_foreign_alternatives_joined_by_plus_are_a_combination(out, label):
    syn, combos = _real()
    g = grade_short(out, _pilot_atoms()["P-malaria_ocr-02"], "en", syn, combos, condition="A1")
    assert g.label == label


# ------------------------------------------------------------------ NÊN SỬA E4: attribution read piece by piece
@pytest.mark.parametrize("aid,out,lang,label", [
    ("P-tbhiv-05", "ĐÁP ÁN: Theo Bộ Y tế: TDF + 3TC + DTG. Theo CDC (US): TDF/FTC + DRV/r", "vi", 1),
    ("P-tbhiv-05", "ANSWER: Vietnam MoH: TLD. WHO: TLD or TAF/FTC/DTG. US: Biktarvy", "en", 1),
    ("P-hbv-06", "ANSWER: Vietnam MoH: TDF or ETV or TAF. EASL also lists TDF plus lamivudine.", "en", 1),
    ("P-malaria_ocr-02", "ANSWER: MoH: Pyramax. WHO (international): artemether-lumefantrine plus primaquine", "en", 1),
    ("P-tbhiv-05", "ĐÁP ÁN: TDF + 3TC + DTG. Hoặc TDF/FTC + DRV/r", "vi", 5),          # not attributed: 5, multi
    ("P-tbhiv-05", "ANSWER: Per CDC: TDF/FTC + DRV/r. Per the MoH: TLD + EFV", "en", 5),  # no MoH regimen stated
])
def test_drug_attribution_is_read_piece_by_piece(aid, out, lang, label):
    syn, combos = _real()
    g = grade_short(out, _pilot_atoms()[aid], lang, syn, combos, condition="A1")
    assert g.label == label
    if label == 1:
        assert g.multi and g.vn_match


# ------------------------------------------------------------------ THẤP: TB codes, dictionary, units
@pytest.mark.parametrize("out,lang,label,method", [
    ("ANSWER: E H R", "en", "correct", "answer_line"), ("ĐÁP ÁN: EHR", "vi", "correct", "answer_line"),
    ("ANSWER: HRZE", "en", "unattributed", "unlisted"), ("ANSWER: H R Z E", "en", "unattributed", "unlisted"),
    ("ANSWER: RHZ", "en", "unattributed", "unlisted"), ("ĐÁP ÁN: ZEH", "vi", "unattributed", "unlisted"),
    ("ĐÁP ÁN: không dùng HRZE", "vi", "abstain", "answer_line"), ("ANSWER: HR", "en", "foreign", "answer_line"),
])
def test_tb_phase_codes(out, lang, label, method):
    g = lab(out, TB_CAT, lang)
    assert (g.label_name, g.parse_method) == (label, method)


def test_tb_codes_are_only_read_on_tb_atoms():
    assert lab("ANSWER: HRZE", FLUID_CAT, "en").label_name == "abstain"


@pytest.mark.parametrize("text,names", [
    ("raltegravir", {"raltegravir"}), ("AZT", {"zidovudine"}), ("zidovudin", {"zidovudine"}), ("abacavir", {"abacavir"}),
    ("RPV", {"rilpivirine"}), ("DHA-piperaquine", {"dihydroartemisinin-piperaquine"}),
])
def test_more_drug_names_after_review(text, names):
    syn, combos = _real()
    assert parse_drugs(text, syn, combos).names == frozenset(names)


def test_regimen_listed_with_a_superseded_regimen_after_review():
    syn, combos = _real()
    g = grade_short("ANSWER: pyronaridine-artesunate or DHA-piperaquine", _pilot_atoms()["P-malaria_ocr-02"], "en",
                    syn, combos, condition="A1")
    assert (g.label, g.multi) == (5, True)                                   # was 2: DHA-piperaquine not read


@pytest.mark.parametrize("text,value", [("0.1 grams", (0.1, "g")), ("100 milligrams", (100.0, "mg")),
                                        ("75 gam", (75.0, "g"))])
def test_plural_mass_units(text, value):
    from vnsoc.normalize_vi import parse_nums

    (n,) = parse_nums(text, "en")
    assert (n.lo, n.unit) == value
