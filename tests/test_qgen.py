"""Question generation: rendering, oracle passages, planted MCQ roles/orders, code QC, A3 section labels.
Values are FIXTURES; stamps and names below are made up (privacy regression tests use fake strings only)."""
import csv
import json

import pytest
import yaml

from vnsoc.grade import grade_mcq
from vnsoc.match.decoys import finalize
from vnsoc.paths import paths
from vnsoc.qgen import build, mcq
from vnsoc.qgen.passages import clean_page, oracle_passage, residual_furniture
from vnsoc.qgen.qc import leak_issues, numbers, population_issues, translation_issues
from vnsoc.qgen.render import drug_display, fmt_num, render_value
from vnsoc.run.prompts import messages, section_label

DENGUE = finalize({"atom_id": "P-t-01", "value_kind": "num", "unit": "ml/kg/h", "vn": [{"lo": 15, "hi": 15}],
                   "foreign": [{"system": "WHO_global", "values": [{"lo": 5, "hi": 10}]}],
                   "superseded": [], "decoy": [{"lo": 20, "hi": 25}],
                   "population": {"age": "người lớn ≥ 16 tuổi", "setting": "sốc SXHD"}})
MAL = finalize({"atom_id": "P-t-02", "value_kind": "drugs", "vn": [{"key_drugs": ["quinine+clindamycin"]}],
                "foreign": [{"system": "US", "values": [{"key_drugs": ["artemether-lumefantrine"]}]}],
                "decoy": [{"key_drugs": ["atovaquone-proguanil"]}], "superseded": []})
SYN = {"quinine": ["quinin"], "clindamycin": ["clindamycine"], "artemether-lumefantrine": ["artemether-lumefantrin"]}
COMBOS = {"quinine+clindamycin": ["quinine", "clindamycin"]}


def test_render():
    assert fmt_num(2.25, "vi") == "2,25" and fmt_num(0.5, "en") == "0.5" and fmt_num(20000, "vi") == "20.000"
    assert render_value({"lo": 5, "hi": 10}, DENGUE, "vi") == "5–10 ml/kg/giờ"
    assert render_value({"lo": 5, "hi": 10}, DENGUE, "en") == "5–10 mL/kg/h"
    assert render_value({"sys": 140, "dia": 90, "cmp": ">="}, {"value_kind": "bp"}, "vi") == "≥ 140/90 mmHg"
    assert render_value({"seq": [0, 3, 7, 14, 28]}, {"value_kind": "schedule"}, "en") == "days 0, 3, 7, 14, 28"
    # display names come from configs/drug_display.yaml, not from the first grading alias ("clindamycine")
    assert render_value({"key_drugs": ["quinine+clindamycin"]}, MAL, "vi", SYN, COMBOS) == "quinin + clindamycin"
    assert render_value({"key_drugs": ["quinine+clindamycin"]}, MAL, "en", SYN, COMBOS) == "quinine + clindamycin"
    fake = {"x-drug": {"vi": "x-thuoc", "en": "x-drug"}}
    assert render_value({"key_drugs": ["x-drug", "y-drug"]}, MAL, "vi", {}, {}, fake) == "x-thuoc + y-drug"  # fallback INN


def test_fmt_num_has_no_junk_decimals():
    """Q6d: at most 4 significant digits, trailing zeros dropped, the integer part never rounded."""
    assert fmt_num(3.3333333333333335, "vi") == "3,333" and fmt_num(383.3333333333333, "en") == "383.3"
    assert fmt_num(12345.5, "vi") == "12.346" and fmt_num(0.012345, "en") == "0.01235"
    assert fmt_num(150.00000000000003, "vi") == "150" and fmt_num(7.0, "en") == "7"


def test_render_years_ages_singulars_and_index():
    """Q6a-c: 'year' is 'năm' for durations and 'tuổi' otherwise; 40 months in a year atom is '3 tuổi 4 tháng';
    English singular for 1; dimensionless 'index' has no unit."""
    age = {"value_kind": "num", "unit": "year", "slot_type": "schedule"}
    dur = {"value_kind": "num", "unit": "year", "slot_type": "duration"}
    assert render_value({"lo": 7, "hi": 7}, age, "vi") == "7 tuổi"
    assert render_value({"lo": 3, "hi": 4, "cmp": ">="}, dur, "vi") == "≥ 3–4 năm"
    assert render_value({"lo": 40, "hi": 40, "unit": "month"}, age, "vi") == "3 tuổi 4 tháng"
    assert render_value({"lo": 40, "hi": 40, "unit": "month"}, dur, "vi") == "3 năm 4 tháng"
    assert render_value({"lo": 40, "hi": 40, "unit": "month"}, age, "en") == "3 years 4 months"
    assert render_value({"lo": 13, "hi": 13, "unit": "month"}, age, "en") == "1 year 1 month"
    assert render_value({"lo": 1, "hi": 1, "cmp": ">="}, dur, "en") == "≥ 1 year"
    assert render_value({"lo": 1, "hi": 1}, {"value_kind": "num", "unit": "day"}, "en") == "1 day"
    assert render_value({"lo": 1, "hi": 2}, {"value_kind": "num", "unit": "day"}, "en") == "1–2 days"
    assert render_value({"lo": 1, "hi": 1}, {"value_kind": "num", "unit": "h"}, "en") == "1 hour"
    apri = {"value_kind": "num", "unit": "index"}
    assert render_value({"lo": 0.5, "hi": 0.5, "cmp": ">"}, apri, "vi") == "> 0,5"
    assert render_value({"lo": 2, "hi": 2}, apri, "en") == "2"


def test_drug_display_covers_every_inn_of_grading_yaml():
    """Q6e: every single-INN key of configs/grading.yaml has a VI and an EN display name."""
    P = paths()
    drugs = yaml.safe_load((P.configs / "grading.yaml").read_text(encoding="utf-8"))["drugs"]
    table = drug_display()
    inns = [k for k in drugs if "+" not in k and "|" not in k]
    missing = [k for k in inns if not (table.get(k) or {}).get("vi") or not (table.get(k) or {}).get("en")]
    assert not missing, f"thiếu tên hiển thị trong configs/drug_display.yaml: {missing}"
    assert table["clindamycin"]["vi"] == "clindamycin" and table["tenofovir-disoproxil"]["vi"] != "tdf"


def test_oracle_passage_keeps_span_and_cuts_at_sentences():
    filler = " ".join(f"Câu thứ {i} nói về chăm sóc chung cho người bệnh." for i in range(60))
    page = filler + " Truyền Ringer lactat 15 ml/kg/giờ trong giờ đầu. " + filler
    p = oracle_passage(page, "Ringer lactat 15 ml/kg/giờ", 150, 300)
    assert "Ringer lactat 15 ml/kg/giờ" in p and 150 <= len(p.split()) <= 300 and p.endswith(".")
    with pytest.raises(ValueError):
        oracle_passage(page, "không có câu này", 150, 300)


def test_oracle_passage_sentence_rules():
    """Q9a-b: a lower-case Vietnamese word never starts a sentence (not even after ';'), and ':' never ends one."""
    head = " ".join(f"Mục {i} bàn về theo dõi người bệnh." for i in range(8))
    page = (head + " Khi kiểm soát kém; ưu tiên chọn thuốc nhóm A khi có bệnh tim mạch. Lịch tiêm như sau: "
            "Tiêm lần 1: khi trẻ đủ 2 tháng tuổi. Tiêm lần 2: sau lần 1 ít nhất 1 tháng. " + head)
    p = oracle_passage(page, "ưu tiên chọn thuốc nhóm A", 20, 60)
    assert p.startswith("Khi kiểm soát kém; ưu tiên") and not p.rstrip().endswith(":")
    q = oracle_passage(page, "Tiêm lần 1: khi trẻ", 5, 12)
    assert q.startswith("Lịch tiêm như sau: Tiêm lần 1") and q.endswith("tháng tuổi.")


def test_oracle_passage_drops_page_furniture_and_names():
    """Q9c-d: signature stamps with a person's name, signature blocks, watermarks, bare page numbers are removed
    outside the span; the span stays verbatim inside the passage (fake names only)."""
    body = " ".join(f"Đoạn {i} mô tả chăm sóc người bệnh." for i in range(10))
    page = ("12 Tiêu chuẩn điều trị cho người lớn. " + body + " Ký bởi: Co quan X Cơ quan: Co quan X Ngày ký: "
            "01-02-2025 09:30:36 +07:00 LuatVietnam www.kcb.vn/abc Điều trị khi ALT > ULN. " + body
            + " abcd.kcb_Nguyen Van Gia_01/02/2025 10:11:12 syt_tinhx_vt_Van thu So Y te X_03/04/2024 08:26:07"
            " 2760 04 7")
    text, i, j = clean_page(page, "Điều trị khi ALT > ULN", 13)
    assert text[i:j] == "Điều trị khi ALT > ULN"
    for bad in ("Nguyen Van Gia", "Van thu", "_vt_", "kcb", "LuatVietnam", "Ký bởi", "2760 04 7"):
        assert bad not in text, bad
    assert text.startswith("Tiêu chuẩn điều trị") and text.endswith("người bệnh.")
    # page number right before the span is dropped, the span itself untouched
    t2, i2, _ = clean_page("9 Tiêu chuẩn điều trị cho người lớn.", "Tiêu chuẩn điều trị", 20)
    assert t2 == "Tiêu chuẩn điều trị cho người lớn." and i2 == 0
    # not a page number: larger than the PDF page, a range, or a value with a unit
    assert clean_page("48 Tiêu chuẩn điều trị.", "điều trị", 20)[0].startswith("48 ")
    assert clean_page("1 - 2 triệu đơn vị mỗi ngày.", "đơn vị", 20)[0].startswith("1 - 2")
    assert clean_page("3 ngày đầu dùng thuốc.", "dùng thuốc", 20)[0].startswith("3 ngày")
    p = oracle_passage(page, "Điều trị khi ALT > ULN", 10, 40, page=13)
    assert "Điều trị khi ALT > ULN" in p and "Nguyen" not in p


def test_mcq_roles_orders_and_grading():
    qs, meta = mcq.build(DENGUE, {"vi": "Tốc độ dịch?", "en": "Fluid rate?"}, 7)
    assert len(qs) == 4 and {q["order_variant"] for q in qs} == {0, 1}
    roles = [q["option_roles"] for q in qs if q["language"] == "vi"]
    assert sorted(roles[0].values()) == sorted(["vn", "foreign:WHO_global", "filler", "decoy"])
    inv0 = {r: letter for letter, r in roles[0].items()}
    inv1 = {r: letter for letter, r in roles[1].items()}
    assert all(inv0[r] != inv1[r] for r in inv0)                      # every option moves between orders
    letter = inv0["foreign:WHO_global"]
    assert grade_mcq(f"ĐÁP ÁN: {letter}", roles[0]).label == 4
    assert mcq.build(DENGUE, {"vi": "x"}, 7)[0][0]["options"] == mcq.build(DENGUE, {"vi": "x"}, 7)[0][0]["options"]


def test_mcq_needs_filler_for_drugs():
    with pytest.raises(ValueError):
        mcq.options(MAL)
    opts, notes = mcq.options(MAL, filler={"key_drugs": ["mefloquine"]})
    assert [r for _, r, _ in opts] == ["vn", "foreign:US", "filler", "decoy"] and notes == []


def test_qc_checks():
    assert leak_issues("Truyền 15 ml/kg/giờ có đúng không?", DENGUE, "vi") == ["lộ giá trị Bộ Y tế"]
    assert leak_issues("Người lớn ≥ 16 tuổi bị sốc SXHD: tốc độ dịch ban đầu (ml/kg/giờ)?", DENGUE, "vi") == []
    assert population_issues("Người lớn bị sốc SXHD?", DENGUE, "vi") == ["thiếu số của quần thể [16.0]"]
    assert numbers("0,5 mg và 5.000 IU", "vi") == numbers("0.5 mg and 5,000 IU", "en") == [0.5, 5000.0]
    assert translation_issues("Trẻ 10 kg không sốc", "A 10 kg child without shock") == []
    assert translation_issues("Trẻ 10 kg", "A 12 kg child") and translation_issues("Trẻ không sốc", "A child in shock")


def test_render_converts_to_atom_unit():
    a = {"value_kind": "num", "unit": "ug", "context": {"weight_kg": 10}}
    assert render_value({"lo": 0.01, "hi": 0.01, "unit": "mg/kg"}, a, "vi") == "100 µg"


def test_section_label_drops_pointers_and_notes():
    """Q10: the A3 section label keeps the chapter/section path, drops the extractor's notes and answer pointers."""
    lab = section_label
    assert lab({"section": "Phụ lục III (Hướng dẫn xử trí), mục IV 'Tiêu đề mục', khoản 1 'Thuốc 1mg = 1 ống', "
                           "điểm a"}) == "Phụ lục III (Hướng dẫn xử trí), mục IV, khoản 1"
    assert lab({"section": "1. ĐỊNH NGHĨA (cùng trang: 3.1 Chẩn đoán, Bảng 1 — ngưỡng, dòng 'Đo đúng quy trình')"}) \
        == "1. ĐỊNH NGHĨA"
    assert lab({"section": "Phần III, 2.2.2 Phác đồ cho người lớn — Phác đồ XYZ"}) == "Phần III, 2.2.2 Phác đồ cho người lớn"
    assert lab({"section": "Phần III, 2.2.2 d) Phác đồ kháng H (6 R(H)ZE)"}) == "Phần III, 2.2.2 d) Phác đồ kháng H"
    assert lab({"section": "Mục 1.1 Chẩn đoán, tiêu chí c"}) == "Mục 1.1 Chẩn đoán"
    assert lab({"section": "Phụ lục X (Sơ đồ xử trí), II. Sơ đồ tóm tắt, ô 'TIÊM BẮP'"}) == \
        "Phụ lục X (Sơ đồ xử trí), II. Sơ đồ tóm tắt"
    assert lab({"section": "Phụ lục 2 – Phân độ (cột nặng: suy tạng)"}) == "Phụ lục 2 – Phân độ"
    assert lab({"section": "III.2.2.1(a) Phụ nữ có thai (điều trị ưu tiên)"}) == \
        "III.2.2.1(a) Phụ nữ có thai (điều trị ưu tiên)"
    assert lab({"section": "C.2.1"}) == "C.2.1"
    long = lab({"section": "Phần 2 " + " ".join(["Chẩn đoán và phân loại"] * 10)})
    assert len(long) <= 120 and long.endswith("…")
    atom = {"guideline": "2760/2023", "section": "C.2 Điều trị sốc, điểm b"}
    q = {"question_id": "x|short|vi", "format": "short", "language": "vi", "text": "Tốc độ dịch là bao nhiêu?"}
    a3 = messages(q, "A3", atom, "Đoạn văn.")[0]["content"]
    assert "mục C.2 Điều trị sốc:" in a3 and "điểm b" not in a3


def _write_jsonl(p, rows):
    p.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")


def test_build_qc_columns_note_and_ocr_flag(tmp_path, monkeypatch, capsys):
    """Q9e + Q11: passage records carry 'ocr'; the QC table has columns note and passage_ocr; the build summary
    counts MCQs skipped on purpose."""
    monkeypatch.setattr(build, "atom_passage", lambda a, root=None, *w: "Đoạn trích giả. Truyền dịch theo phác đồ.")
    monkeypatch.setattr(build, "passage_ocr", lambda a, root=None: True)
    atom = dict(DENGUE, guideline="9999/2099", section="C.2", page=3, decoy=[])        # no decoy: MCQ skipped
    draft = {"atom_id": "P-t-01", "short_vi": "Người lớn ≥ 16 tuổi bị sốc SXHD: tốc độ dịch (ml/kg/giờ)?",
             "short_en": "Adult ≥ 16 years with dengue shock: fluid rate (mL/kg/h)?", "mcq_stem_vi": None,
             "mcq_stem_en": None}
    _write_jsonl(tmp_path / "a.jsonl", [atom])
    _write_jsonl(tmp_path / "d.jsonl", [draft])
    out = [str(tmp_path / n) for n in ("q.jsonl", "p.jsonl", "qc.csv")]
    rc = build.main(["--atoms", str(tmp_path / "a.jsonl"), "--drafts", str(tmp_path / "d.jsonl"), "--out", out[0],
                     "--passages", out[1], "--qc", out[2]])
    assert rc == 0 and "1 mẩu bỏ trắc nghiệm có chủ đích" in capsys.readouterr().out
    rows = list(csv.DictReader(open(out[2], encoding="utf-8")))
    assert list(rows[0]) == build.QC_FIELDS
    by = {r["question_id"]: r for r in rows}
    assert by["P-t-01#A3"]["passage_ocr"] == "True"
    assert by["P-t-01|mcq"]["ok"] == "True" and by["P-t-01|mcq"]["note"].startswith("bỏ trắc nghiệm có chủ đích: ")
    assert json.loads(open(out[1], encoding="utf-8").readline())["ocr"] is True


def test_render_edge_cases_after_review():
    """Review 26/9: two ends that print alike are one value ('1 day', not '1–1 days'); EN singular in schedules;
    decimal comma in Vietnamese blood pressure; tiny numbers never print as '0'."""
    day = {"value_kind": "num", "unit": "day"}
    assert render_value({"lo": 1.0, "hi": 1.0000000001}, day, "en") == "1 day"
    assert render_value({"seq": [1], "unit": "month"}, {"value_kind": "schedule"}, "en") == "1 month"
    assert render_value({"seq": [0, 1, 6], "unit": "month"}, {"value_kind": "schedule"}, "en") == "0, 1, 6 months"
    assert render_value({"sys": 135, "dia": 85.5}, {"value_kind": "bp"}, "vi") == "135/85,5 mmHg"
    assert fmt_num(2.5e-11, "en") == "0.000000000025" and fmt_num(1000.4, "vi") == "1.000"


def test_passage_furniture_variants_are_removed(capsys):
    """Review 26/9 (privacy): stamp and signature shapes beyond the pilot corpus (login with a hyphen, d-m-yyyy and
    yyyy/m/d dates, no login, a signature block without a date or with an e-mail) leave no name. Fake names only."""
    body = " ".join(f"Đoạn {i} mô tả chăm sóc người bệnh." for i in range(4))
    span = "Điều trị khi ALT > ULN"
    stamps = ["nguyen-van.kcb_Xyz Abc_01-02-2025 10:11:12", "user01.kcb_Qwe Rty_2025/02/01 10:11:12",
              "kcb_Uio Pas_01/02/2025", "Ký bởi: Dfg Hjk Cơ quan: Co quan X",
              "Người ký: Lmn Opq Email: lmn@example.gov.vn Cơ quan: Co quan X Thời gian ký: 01.02.2025 10:11:12 +07:00"]
    for st in stamps:
        text, i, j = clean_page(body + " " + st + " " + span + ". " + body, span, 5)
        assert text[i:j] == span
        for name in ("Xyz", "Abc", "Qwe", "Uio", "Dfg", "Hjk", "Lmn", "Opq", "@", "nguyen"):
            assert name not in text, (st, name)
    # a count at the top of the page is not a page number; a page number right after a final span goes
    assert clean_page("15 người bệnh được theo dõi. " + span + ".", span, 20)[0].startswith("15 người")
    assert clean_page(body + " " + span + ". 12", span + ".", 13)[0].endswith(span + ".")
    # prose that mentions a signer keeps its words
    assert "Bộ trưởng" in clean_page("Văn bản được ký bởi Bộ trưởng. " + span, span, 5)[0]
    # safety net: a shape the filters miss fails the A3 QC row instead of reaching the model unseen
    assert residual_furniture("Người ký: Abc Def") and residual_furniture("x.y_Abc_01/02/2025")
    assert not residual_furniture("Văn bản được ký bởi Bộ trưởng, có hiệu lực từ ngày ký.")


def test_passage_never_adds_the_unfinished_sentences_of_the_page():
    """Review 26/9: a page's last sentence cut by the page end ('…các biểu hiện:') and a first sentence begun on the
    previous page are not added around the span (kept only when the span lies in them)."""
    head = "và theo dõi sát trong suốt quá trình điều trị."
    mid = " ".join(f"Mục {i} bàn về theo dõi người bệnh." for i in range(6))
    page = f"{head} {mid} Chỉ định thở oxy khi SaO2 ≤ 88%. {mid} Hoặc PaO2 thấp kèm một trong các biểu hiện:"
    p = oracle_passage(page, "Chỉ định thở oxy", 200, 300)          # wants more words than the page has
    assert p.startswith("Mục 0") and p.endswith("người bệnh.")
    q = oracle_passage(page, "kèm một trong các biểu hiện", 5, 30)
    assert q.endswith("biểu hiện:")
    r = oracle_passage("“Chú ý” khi dùng. " + mid, "Mục 1", 2, 8)
    assert r == "Mục 1 bàn về theo dõi người bệnh."


def test_section_label_keeps_titles_that_contain_pointer_words():
    """Review 26/9: 'Thời điểm …' and 'hàng đầu' are titles, not pointers; 'điểm a' without a comma is a pointer; an
    em-dash part that continues the path is kept."""
    lab = section_label
    assert lab({"section": "Phần 1 – Bước 5, mục 5 (Thời điểm khởi trị THA)"}) == \
        "Phần 1 – Bước 5, mục 5 (Thời điểm khởi trị THA)"
    assert lab({"section": "mục 4 (thuốc hàng đầu)"}) == "mục 4 (thuốc hàng đầu)"
    assert lab({"section": "mục 1.2 điểm a"}) == "mục 1.2"
    assert lab({"section": "Chương 3 — Điều trị, mục 3.2 Liều dùng"}) == "Chương 3 — Điều trị, mục 3.2 Liều dùng"
    assert lab({"section": "Bảng 3, cột 'Trẻ < 10 kg: 0,1 ml'"}) == "Bảng 3"


def test_build_records_option_rank_and_flags_a3_label_values(monkeypatch, capsys):
    """H1 symmetry and A3 label: num/bp MCQ rows carry option_rank, the summary counts edge positions; a section
    label that states a non-MoH value fails the A3 row."""
    monkeypatch.setattr(build, "atom_passage", lambda a, root=None, *w: "Đoạn trích giả. Truyền dịch theo phác đồ.")
    monkeypatch.setattr(build, "passage_ocr", lambda a, root=None: False)
    atom = dict(DENGUE, guideline="9999/2099", section="C.2 (sốc) — truyền 5–10 ml/kg/giờ, mục 2 Điều trị", page=3)
    draft = {"atom_id": "P-t-01", "short_vi": "Người lớn ≥ 16 tuổi bị sốc SXHD: tốc độ dịch (ml/kg/giờ)?",
             "short_en": "Adult ≥ 16 years with dengue shock: fluid rate (mL/kg/h)?",
             "mcq_stem_vi": "Người lớn ≥ 16 tuổi bị sốc SXHD: tốc độ dịch ban đầu?",
             "mcq_stem_en": "Adult ≥ 16 years with dengue shock: initial fluid rate?"}
    qs, _, qc = build.build_all([atom], {"P-t-01": draft}, 7, (150, 300))
    by = {r["question_id"]: r for r in qc}
    assert by["P-t-01#A3"]["ok"] is False and "nhãn mục A3" in by["P-t-01#A3"]["issues"]
    rank = by["P-t-01|mcq|vi|o0"]["option_rank"]
    assert sorted(rank.split("<")) == ["decoy", "filler", "foreign", "vn"]
    assert build.edge_summary(qc).startswith("trắc nghiệm num/bp có nước ngoài: 1 mẩu")
