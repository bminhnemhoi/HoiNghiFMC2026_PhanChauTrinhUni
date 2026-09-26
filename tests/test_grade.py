"""Golden cases from the seed conflicts (proposal §3.3). Values here are TEST FIXTURES, not data."""
import pytest

from vnsoc.grade import compute_tolerance, conflict_status, grade_mcq, grade_short

SYN = {"artemether-lumefantrine": ["artemether-lumefantrin", "coartem"], "artemether": [], "lumefantrine": ["lumefantrin"],
       "quinine": ["quinin"], "clindamycin": [], "dihydroartemisinin-piperaquine": []}
COMBOS = {"artemether-lumefantrine": ["artemether", "lumefantrine"], "quinine+clindamycin": ["quinine", "clindamycin"]}


def atom(**kw):
    a = {"atom_id": "t", "foreign": [], "superseded": [], "decoy": []}
    a.update(kw)
    a["tolerance"] = compute_tolerance(a)
    return a


DENGUE = atom(value_kind="num", unit="ml/kg/h", vn=[{"lo": 15, "hi": 15}],
              foreign=[{"system": "WHO_global", "values": [{"lo": 5, "hi": 10}]}], decoy=[{"lo": 20, "hi": 25}])
HTN = atom(value_kind="bp", vn=[{"sys": 140, "dia": 90}],
           foreign=[{"system": "US", "values": [{"sys": 130, "dia": 80}]}, {"system": "EU_UK", "values": [{"sys": 140, "dia": 90}]}],
           decoy=[{"sys": 150, "dia": 100}])
RABIES = atom(value_kind="schedule", vn=[{"seq": [0, 3, 7, 14, 28]}],
              foreign=[{"system": "US", "values": [{"seq": [0, 3, 7, 14]}]}], decoy=[{"seq": [0, 7, 21, 28]}])
ADRENALINE = atom(value_kind="num", unit="mg", vn=[{"lo": 0.5, "hi": 1.0}],
                  foreign=[{"system": "EU_UK", "values": [{"lo": 0.5, "hi": 0.5}]}])
MALARIA_PREG = atom(value_kind="drugs", vn=[{"key_drugs": ["quinine+clindamycin"]}],
                    foreign=[{"system": "US", "values": [{"key_drugs": ["artemether-lumefantrine"]}]}],
                    decoy=[{"key_drugs": ["dihydroartemisinin-piperaquine"]}])
HBV = atom(value_kind="num", unit="U/L", vn=[{"lo": 30, "hi": 30}],
           foreign=[{"system": "US", "values": [{"lo": 70, "hi": 70}]}],
           superseded=[{"guideline": "3310/2019", "values": [{"lo": 40, "hi": 40}]}], decoy=[{"lo": 50, "hi": 50}])
PEDS_ADR = atom(value_kind="num", unit="ug", context={"mg_per_ml": 1, "weight_kg": 10}, vn=[{"lo": 250, "hi": 250}],
                foreign=[{"system": "EU_UK", "values": [{"lo": 150, "hi": 150}]}], decoy=[{"lo": 350, "hi": 350}])


def g(out, a, **kw):
    return grade_short(out, a, synonyms=SYN, combos=COMBOS, **kw)


def test_status():
    assert conflict_status(DENGUE) == "conflict"
    assert conflict_status(ADRENALINE) == "concordant"          # seed row 14: 0.5 mg inside 0.5–1 mg
    assert conflict_status(HTN) == "conflict"                   # US only
    assert conflict_status(atom(value_kind="num", unit="mg", vn=[{"lo": 1, "hi": 1}])) == "no_counterpart"
    clash = atom(value_kind="num", unit="mg", vn=[{"lo": 10, "hi": 10}], foreign=[{"system": "US", "values": [{"lo": 5, "hi": 5}]}],
                 superseded=[{"guideline": "x", "values": [{"lo": 5, "hi": 5}]}])
    assert conflict_status(clash) == "indistinguishable"
    assert DENGUE["tolerance"] == pytest.approx(2.5) and HTN["tolerance"] == pytest.approx(5)


@pytest.mark.parametrize("out,label,extra", [
    ("ĐÁP ÁN: 15 ml/kg/giờ", "correct", {}),
    ("ĐÁP ÁN: 10 ml/kg/giờ", "foreign", {"foreign_systems": ["WHO_global"]}),
    ("ĐÁP ÁN: 5–10 ml/kg/h", "foreign", {}),
    ("ĐÁP ÁN: 12 ml/kg/h", "foreign", {}),                      # within tolerance of WHO 5–10
    ("ĐÁP ÁN: 20 ml/kg/giờ", "unattributed", {"decoy_match": True}),
    ("ĐÁP ÁN: 15 ml/kg/giờ (Bộ Y tế); WHO 2009 là 5–10 ml/kg/giờ", "correct_aware", {"multi": True}),
    ("Tôi không chắc chắn.", "abstain", {}),
    ("Bạn đang hỏi theo hướng dẫn của quốc gia nào?", "abstain", {}),       # no condition given -> not credited
])
def test_dengue(out, label, extra):
    r = g(out, DENGUE)
    assert r.label_name == label
    for k, v in extra.items():
        assert getattr(r, k) == v


def test_ask_country_only_aware_without_cue():
    q = "Bạn hỏi theo hướng dẫn của quốc gia nào?"
    assert g(q, DENGUE, condition="A0").label_name == "correct_aware"
    assert g(q, DENGUE, condition="A1").label_name == "abstain"


def test_needs_llm_when_ambiguous():
    r = g("Có thể truyền 10 hoặc 20 ml/kg/giờ tùy đáp ứng", DENGUE)
    assert r.label is None and r.needs_llm


def test_htn_rabies_adrenaline_malaria_hbv():
    assert g("ĐÁP ÁN: 130/80 mmHg", HTN).label_name == "foreign"
    assert g("ĐÁP ÁN: 130/80 mmHg", HTN).foreign_systems == ["US"]
    assert g("ĐÁP ÁN: ≥ 140/90 mmHg", HTN).label_name == "correct"
    assert g("ĐÁP ÁN: ngày 0, 3, 7, 14", RABIES).label_name == "foreign"
    assert g("ĐÁP ÁN: N0-3-7-14-28", RABIES).label_name == "correct"
    assert g("ĐÁP ÁN: 0,5 mg", ADRENALINE).label_name == "correct"
    assert g("ĐÁP ÁN: quinin + clindamycin 7 ngày", MALARIA_PREG).label_name == "correct"
    assert g("ANSWER: artemether-lumefantrine", MALARIA_PREG, lang="en").label_name == "foreign"
    assert g("ANSWER: quinine plus clindamycin; the CDC recommends artemether-lumefantrine", MALARIA_PREG,
             lang="en").label_name == "correct_aware"
    assert g("ĐÁP ÁN: ALT > 40 U/L", HBV).label_name == "temporal"
    assert g("ĐÁP ÁN: ALT > 30 U/L", HBV).label_name == "correct"
    assert g("ĐÁP ÁN: 0,25 ml", PEDS_ADR).label_name == "correct"          # ml -> µg via 1 mg/ml
    assert g("ĐÁP ÁN: 0,15 mg", PEDS_ADR).label_name == "foreign"


def test_think_block_and_unit_mismatch():
    assert g("<think>maybe 10</think>\nĐÁP ÁN: 15 ml/kg/giờ", DENGUE).label_name == "correct"
    r = g("ĐÁP ÁN: 3 viên", DENGUE)
    assert r.label_name == "unattributed" and r.parse_method == "unit_mismatch"


def test_mcq():
    roles = {"A": "vn", "B": "foreign:US", "C": "decoy", "D": "superseded:3310/2019"}
    assert grade_mcq("ĐÁP ÁN: B", roles).label_name == "foreign"
    assert grade_mcq("C", roles).decoy_match
    assert grade_mcq("ĐÁP ÁN: D", roles).label_name == "temporal"
    assert grade_mcq("không biết", roles).label_name == "abstain"


def test_drug_regimens_conflict_unless_identical():
    # _gap for drugs must agree with the value-set idea: a regimen differing by any drug is outside the MoH set
    vn = {"key_drugs": ["tenofovir-disoproxil", "lamivudine", "dolutegravir"]}
    other = {"key_drugs": ["tenofovir-alafenamide", "emtricitabine", "dolutegravir"]}
    a = atom(value_kind="drugs", vn=[vn], foreign=[{"system": "US", "values": [other]}])
    assert conflict_status(a) == "conflict"
    same = atom(value_kind="drugs", vn=[vn], foreign=[{"system": "WHO_global", "values": [dict(vn)]}])
    assert conflict_status(same) == "concordant"


def test_footnote_digits_after_abbreviations():
    from vnsoc.normalize_vi import parse_drugs

    syn = {"dolutegravir": ["dtg"], "tenofovir-alafenamide": ["taf"], "lamivudine": ["3tc"]}
    assert parse_drugs("TAF2 + 3TC + DTG1", syn).names == frozenset({"tenofovir-alafenamide", "lamivudine", "dolutegravir"})


def test_grading_config_aliases_unambiguous():
    import yaml

    from vnsoc.normalize_vi import _norm_drug_text
    from vnsoc.paths import paths

    cfg = yaml.safe_load((paths().configs / "grading.yaml").read_text(encoding="utf-8"))
    seen, chain = {}, {}
    for inn, aliases in cfg["drugs"].items():
        for a in [inn, *aliases]:
            if a.startswith("~"):                # TB chain code (1–2 letters), read only inside a regimen chain
                code, _, n = a[1:].partition("@")   # '~Pa@2': minimum of other drugs (grader 1.2.0), default 3
                # grader 1.3.1: a 3-letter code only in capitals (case-sensitive) with a minimum of ≥ 2 other drugs
                # ('~ABC@2', '~RAL@2', '~PAS@2': 'ABC' of airway assessment is not abacavir)
                three = len(code) == 3 and code.isupper() and n.isdigit() and int(n) >= 2
                assert code.isalpha() and (len(code) <= 2 or three) and "+" not in inn and "|" not in inn, a
                assert not n or (n.isdigit() and int(n) >= 2), a
                assert chain.setdefault(code.lower(), inn) == inn, f"{a} trỏ tới {chain[code.lower()]} và {inn}"
                continue
            k = _norm_drug_text(a)
            assert len(k) >= 3, f"bí danh quá ngắn: {a}"
            assert seen.setdefault(k, inn) == inn or k == _norm_drug_text(inn), f"{a} trỏ tới {seen[k]} và {inn}"
    for combo, parts in cfg["combos"].items():
        assert all(p in cfg["drugs"] for p in parts), combo
    for key in cfg["drugs"]:                     # named regimens 'a+b' and classes 'a|b' are made of known INNs
        members = key.split("+") if "+" in key else key.split("|") if "|" in key else []
        assert all(m in cfg["drugs"] and "+" not in m and "|" not in m for m in members), key
        assert "+" not in key or "|" not in key, key
