"""Grader and question-QC rules changed before the freeze after the preregistration review (rev-clinician ids 2, 3,
5, 11; rev-methods id 4). The answer strings are the reviewer's probes rewritten as full outputs; atoms are TEST
FIXTURES modelled on the pilot atoms they cite, not data."""
from vnsoc.grade import compute_tolerance, conflict_status, grade_short
from vnsoc.qgen.qc import passage_alt_values, required_terms_issues


def atom(**kw):
    a = {"atom_id": "t", "foreign": [], "superseded": [], "decoy": []}
    a.update(kw)
    a["tolerance"] = compute_tolerance(a)
    return a


DENGUE = atom(value_kind="num", unit="ml/kg/h", vn=[{"lo": 15, "hi": 15}],
              foreign=[{"system": "WHO_global", "source": "WHO 2009 Dengue", "version_date": "2009",
                        "values": [{"lo": 5, "hi": 10}]}], decoy=[{"lo": 20, "hi": 25}])
DM3 = atom(value_kind="num", unit="year", vn=[{"lo": 45, "hi": 45, "cmp": ">="}],
           foreign=[{"system": "US", "values": [{"lo": 35, "hi": 35, "cmp": ">="}]}], decoy=[{"lo": 55, "hi": 55}])
DM1 = atom(value_kind="num", unit="%", vn=[{"lo": 9, "hi": 9, "cmp": ">="}],
           foreign=[{"system": "US", "values": [{"lo": 10, "hi": 10, "cmp": ">"}]}], decoy=[{"lo": 8, "hi": 8}])
HBV8 = atom(value_kind="num", unit="IU/mL", vn=[{"lo": 2000, "hi": 2000, "cmp": ">"}],
            foreign=[{"system": "WHO_global", "values": [{"lo": 20000, "hi": 20000, "cmp": ">"}]}],
            decoy=[{"lo": 200, "hi": 200}])


def lab(out, a, lang="vi"):
    return grade_short(out, a, lang).label_name


def test_label1_not_given_for_generic_words():
    # rev-clinician id 3: 'who', 'while', 'however', 'khác', 'đơn vị quốc tế' used to give label 1
    assert lab("Screening should begin at age 45 years; however, it may start earlier in patients who are "
               "overweight.\nANSWER: 45 years", DM3, "en") == "correct"
    assert lab("Start insulin early if A1C ≥ 9%, while considering patients who tolerate it.\nANSWER: 9%", DM1,
               "en") == "correct"
    assert lab("Điều trị khi HBV DNA > 2.000 đơn vị quốc tế/mL; các trường hợp khác cần theo dõi.\n"
               "ĐÁP ÁN: > 2.000 IU/mL", HBV8) == "correct"


def test_label1_same_in_both_languages_for_the_step_two_rate():
    en = "Give 15 mL/kg/h for the first hour, then reduce to 10 mL/kg/h while monitoring.\nANSWER: 15 mL/kg/h"
    vi = "Truyền 15 ml/kg/giờ trong giờ đầu, sau đó giảm còn 10 ml/kg/giờ trong khi theo dõi.\nĐÁP ÁN: 15 ml/kg/giờ"
    assert lab(en, DENGUE, "en") == lab(vi, DENGUE) == "correct"


def test_prompt_echo_with_two_values_is_hedging_not_awareness():
    # A1 echo: the MoH marker precedes BOTH values, so the WHO value is attributed to the MoH -> label 5
    assert lab("ĐÁP ÁN: Theo Bộ Y tế: 5-10 ml/kg/giờ hoặc 15 ml/kg/giờ", DENGUE) == "unattributed"


def test_label1_still_given_for_explicit_attribution():
    assert lab("Theo Bộ Y tế Việt Nam là 15 ml/kg/giờ, trong khi WHO khuyến cáo 5–10 ml/kg/giờ.\n"
               "ĐÁP ÁN: 15 ml/kg/giờ", DENGUE) == "correct_aware"
    assert lab("The Vietnamese MoH recommends 15 mL/kg/h, unlike WHO (5–10 mL/kg/h).\nANSWER: 15 mL/kg/h", DENGUE,
               "en") == "correct_aware"
    g = grade_short("ĐÁP ÁN: 15 ml/kg/giờ (Bộ Y tế); WHO 2009 là 5–10 ml/kg/giờ", DENGUE)
    assert g.label_name == "correct_aware" and g.foreign_sources == ["WHO 2009 Dengue|2009"]


def test_foreign_sources_recorded():
    # rev-clinician id 11: the matched source and version date are kept (latest-version analysis)
    g = grade_short("ĐÁP ÁN: 8 ml/kg/giờ", DENGUE)
    assert g.label_name == "foreign" and g.foreign_sources == ["WHO 2009 Dengue|2009"]


def test_comparison_signs_are_handled_consistently():
    # rev-clinician id 2: MoH target '130 to < 140'; US '< 130' and ESC '120-129' must both be non-MoH
    t = atom(value_kind="num", unit="mmHg", slot_type="target", vn=[{"lo": 130, "hi": 140}],
             foreign=[{"system": "US", "values": [{"lo": 130, "hi": 130, "cmp": "<"}]},
                      {"system": "EU_UK", "values": [{"lo": 120, "hi": 129}]}])
    assert conflict_status(t) == "conflict"
    assert grade_short("ĐÁP ÁN: < 130 mmHg", t).label_name == "foreign"
    assert grade_short("ĐÁP ÁN: < 130 mmHg", t).foreign_systems == ["US"]
    assert grade_short("ĐÁP ÁN: 120-129 mmHg", t).foreign_systems == ["EU_UK"]
    assert grade_short("ĐÁP ÁN: 135 mmHg", t).label_name == "correct"
    # with the conditional clause encoded ('< 140, may be lower if tolerated') both are inside the MoH set
    t2 = atom(value_kind="num", unit="mmHg", slot_type="target", vn=[{"lo": 0, "hi": 140, "cmp": "<"}],
              foreign=[{"system": "US", "values": [{"lo": 130, "hi": 130, "cmp": "<"}]},
                       {"system": "EU_UK", "values": [{"lo": 120, "hi": 129}]}])
    assert conflict_status(t2) == "concordant"
    assert {grade_short(x, t2).label_name for x in ("ĐÁP ÁN: < 130 mmHg", "ĐÁP ÁN: 120-129 mmHg")} == {"correct"}
    # point-against-point thresholds keep their equality ('> 2000' vs '>= 2000')
    h = atom(value_kind="num", unit="IU/mL", vn=[{"lo": 2000, "hi": 2000, "cmp": ">"}],
             foreign=[{"system": "US", "values": [{"lo": 2000, "hi": 2000, "cmp": ">="}]}])
    assert conflict_status(h) == "concordant"


def test_required_population_terms():
    # rev-clinician id 5: a question for P-hbv-03 without 'HBeAg dương tính' must fail QC in both languages
    hbv3 = {"required_terms": {"hbeag": {"vi": ["HBeAg dương tính", "HBeAg (+)"], "en": ["HBeAg-positive",
                                                                                         "HBeAg positive"]}}}
    assert required_terms_issues("Người lớn viêm gan B mạn, ALT tăng: ngưỡng HBV DNA để điều trị?", hbv3, "vi")
    assert required_terms_issues("Người lớn viêm gan B mạn HBeAg dương tính, ALT tăng: ngưỡng HBV DNA?", hbv3,
                                 "vi") == []
    assert required_terms_issues("Adults with HBeAg-positive chronic hepatitis B: HBV DNA threshold?", hbv3, "en") == []
    assert required_terms_issues("Adults with chronic hepatitis B: HBV DNA threshold?", hbv3, "en")
    assert required_terms_issues("anything", {"required_terms": {}}, "vi") == []


def test_a3_passage_alt_values():
    # rev-methods id 4(a), rev-clinician id 1(d): the dengue passage states the step-2 rate 10 ml/kg/h (= WHO value)
    a = dict(DENGUE, moh_neighbour=[{"context": "bước 2", "values": [{"lo": 10, "hi": 10}]}])
    p = ("Truyền Ringer lactat 15 ml/kg/giờ trong 1 giờ. Nếu cải thiện, giảm còn 10 ml/kg/giờ trong 2 giờ, "
         "sau đó giảm dần.")
    assert passage_alt_values(p, a) == ["foreign:WHO_global", "neighbour"]
    assert passage_alt_values("Truyền Ringer lactat 15 ml/kg/giờ trong 1 giờ.", a) == []
