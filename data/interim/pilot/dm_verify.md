# Kiểm toán độc lập: thí điểm Đái tháo đường (típ 2 và thai kỳ), ID = dm

- **Ngày:** 2026-09-26
- **Người kiểm:** integrity-auditor. Đây là AI kiêm góc nhìn bác sĩ lâm sàng Việt Nam do AI đóng vai, **không phải bác sĩ thật**.
- **Đối tượng:** `data/interim/pilot/dm.jsonl` (8 mẩu) và `data/interim/pilot/dm_report.md`. Cả hai được ghi lúc 11:16.
- **Nguyên tắc:**
  - Không tin báo cáo; tự chạy lại mọi kiểm tra.
  - Chỉ đọc dữ liệu; chỉ ghi file này.
  - OCR 1470/2024 và trích chữ slide ADA chỉ làm trong scratchpad của phiên, không ghi vào `data/`.

## 0. Kết luận nhanh

| atom_id | verdict | Lý do chính |
|---|---|---|
| P-dm-01 | **pass** | Span, giá trị VN và ADA 2026 Rec 9.20 đều đúng. Bản cũ 3319/2017 (kể cả Hình 1–2) không có ngưỡng HbA1c khởi trị insulin, nên `superseded: []` là đúng. Mồi 8% đúng quy tắc. |
| P-dm-02 | **pass** | Mẩu đối chứng thật: VN và ADA đều ≥ 300 mg/dL (16,7 mmol/L). |
| P-dm-03 | **pass** | VN ≥ 45 (5481 tr. 12), ADA 2026 Rec 2.12b 35 tuổi cho "all other people". Bản cũ 3319 cũng 45, nên không lệch phiên bản. Mồi 55 đúng quy tắc. |
| P-dm-04 | **fix** | Nội dung đúng, nhưng biểu diễn chưa thống nhất với mẩu THA. Mồi "150" trùng số ADA Rec 10.7 (≥150/90, ô khác). Còn thiếu ghi chú về mâu thuẫn nội bộ ở mục 6.1.3 của 5481. |
| P-dm-05 | **fix** | Trạng thái indistinguishable là đúng. Nhưng (i) bộ chấm cho đáp án "một bước **hoặc** hai bước" (đúng kiểu ADA) là **correct**; (ii) chưa dẫn 1470/2024, văn bản hiện hành chuyên biệt về ĐTĐ thai kỳ; (iii) chưa kiểm 6173/2018. |
| P-dm-06 | **pass** | VN, WHO 2006 và ADA Bảng 2.1 đều 7,0 mmol/L / 126 mg/dL. |
| P-dm-07 | **pass** | VN, WHO 2011 và ADA Bảng 2.1 đều 6,5%. |
| P-dm-08 | **pass** | VN (5481, 1470), WHO 2013 và ADA Bảng 2.8 (một bước) đều 5,1 mmol/L / 92 mg/dL. |

**Tổng: 6 pass · 2 fix · 0 reject.**

Kết quả chạy lại:
- `vnsoc.schemas atom` → "OK 8 dòng hợp lệ".
- `vnsoc.extract.verify_span` → "OK: 0 mẩu không đạt".
- `finalize()` tính lại `tolerance` và `conflict_status` khớp từng mẩu.
- `mirror_decoy` và `choose_decoy` cho đúng mồi đã ghi (8 %, 55 year, 150 mmHg).
- `check_decoy` = [] cho cả 8 mẩu.

**Phát hiện mới mà báo cáo chưa nêu:**
1. **Lỗi chấm (nghiêm trọng về thiết kế) ở mẩu `cat` P-dm-05.** Đáp án "có thể dùng 1 bước (75 g) hoặc 2 bước (50 g/100 g)" bị chấm `correct`. `parse_cats` trả cả hai nhãn, và `matches()` coi là khớp chỉ cần nhãn VN nằm trong tập. Đây chính là câu trả lời theo ADA 2026 và theo bản cũ 3319/2017.
2. **Báo cáo nói sai rằng 5904/2019 không kiểm span được.** Khóa `5904/2019__9e6bbe13` (bản 68 trang) đọc được bằng `verify_span`, và mẩu THA (P-htn-01..04) đang dùng khóa này. Tôi đã đọc tr. 11, 17–20, 27–28. Vì vậy ứng viên IFG (VN 5,6 so với WHO 6,1) **làm được ngay** (mục 3.4).
3. **5481/2020 mục 6.1.3 mâu thuẫn nội bộ với 6.1.1** về ngưỡng THA ở người ĐTĐ (xem P-dm-04).
4. **`conflict_family` của P-dm-04 (`htn_dx_threshold_us`) khác mẩu THA cùng gốc** (`htn_us_130_80`, value_kind `bp`).
5. **`vnsoc.match.sources grep` vẫn lỗi với file pptx của ADA.** Tôi đã tái hiện: `AssertionError` trong `_markupbase`. Hệ quả: nhãn `verified_by: "auto"` của mọi giá trị lấy từ bộ slide ADA không tái lập được bằng công cụ chuẩn của dự án. Tôi đã tự tái lập bằng cách trích XML slide.

---

## 1. Kiểm lại văn bản và nguồn

| Mục | Kiểm bằng | Kết quả |
|---|---|---|
| 5481/2020 (danh tính) | `verify_span --page 5481/2020 1` và `2` | Tiêu đề đúng. Điều 3 "thay thế Quyết định số 3319/QĐ-BYT ngày 19/07/2017". Dấu ký số "5481 30 12", năm 2020. Lớp chữ để trống số ✓ |
| 5481/2020: số trang in | `--page` 11/12/25/34 | Số in 9/10/23/32, khớp `printed_page` ✓ |
| 1353/2021 | `--page 1353/2021 1` | Chỉ (1) bổ sung người biên soạn và (2) sửa "điểm b, mục 3, trang 37" (insulin cho bệnh nặng không nguy kịch). Không chạm mẩu nào ✓ |
| 5481/2020 còn hiện hành? | WebFetch kcb.vn/phac-do, kcb.vn/tai-lieu, daithaoduong.kcb.vn | Không thấy văn bản ĐTĐ típ 2 mới. Trang phac-do hiện mục từ 07/2020 đến 08/2024; trang tai-lieu hiện mục từ 06/2026 đến 25/09/2026. **Không loại trừ hoàn toàn được** vì ngân sách WebSearch đã hết (200/200). Corpus-librarian cần xác nhận trước ngày đóng băng 15/10/2026. |
| 3319/2017 (bản cũ) | `--page`, `--find`, ảnh tr. 8 (Hình 1), ảnh tr. 10 | Tr. 3 "≥ 45 tuổi" ✓. Tr. 4: hai `superseded_spans` của P-dm-05 đều khớp (tôi chạy `span_on_page` → True) ✓. **Không có** ngưỡng HbA1c khởi trị insulin, cả trong lớp chữ lẫn trong Hình 1 (ảnh sơ đồ tôi đã xem). Tr. 10 chỉ có "Nếu A1C <8%, xem xét ↓liều insulin nền" (ô khác) ✓ |
| 1470/2024 (hiện hành, ĐTĐ thai kỳ) | Ảnh trang và OCR tesseract vie+eng 300 dpi **trong scratchpad** (không lưu vào data/) | Tr. 1: QĐ 1470/QĐ-BYT ngày 29/5/2024, "Hướng dẫn quốc gia về sàng lọc và quản lý đái tháo đường thai kỳ", thay 6173/QĐ-BYT ngày 12/10/2018. Tr. 13 (số in 8): tầm soát mọi thai phụ tuần 24–28 bằng "nghiệm pháp dung nạp 75gram glucose". Tr. 14 (số in 9), Bảng 3: ≥92/≥180/≥153 mg/dL (≥5.1/≥10.0/≥8.5 mmol/L). OCR cả 31 trang **không có** "50 g", "100 g" hay "2 bước" → không có phương pháp hai bước ✓. Báo cáo đọc bằng mắt đúng. |
| 5904/2019 bản 68 trang | `verify_span --page "5904/2019__9e6bbe13"` 11, 17–20, 27–28 | Đọc tốt, glyph Ƣ đã được chuẩn hóa. Tr. 11: THA ở người ≥ 18 tuổi khi HA ≥ 140/90. Tr. 18: chẩn đoán ĐTĐ 7,0/126; 6,5%/48; tiền ĐTĐ IFG "5,6 đến 6,9mmol/L". Tr. 28: mục tiêu HA "< 130/80*" cho THA+ĐTĐ; chú thích ghi "(người <65 tuổi)" hai lần (lỗi văn bản) ✓ |
| ADA 2026 pptx | sha256sum của `data/cache/foreign/034f66ea0fda2bab1012.html` | `034f66ea…cc4f122b`, khớp `page_sha256` ✓. File là zip (PK), 347 slide, thứ tự trình chiếu trùng số file. Mục đã **có lại** trong `index.json`, dù báo cáo ghi là mất (index sửa lúc 11:42). |
| ADA: kiểm chuỗi | `sources grep` → **lỗi** `AssertionError: expected name token` (HTMLParser đọc nhị phân). Tôi tự trích `<a:t>` trong XML slide và xem ảnh bảng. | Slide 29: 2.12b "…screening should begin at age 35 years" ✓. Slide 44: "either of two strategies" ✓. Slide 176: 9.20 "A1C >10% … ≥300 mg/dL" ✓. Slide 200: 10.1 "systolic … ≥130 mmHg or … ≥80" ✓. Slide 206: 10.7 "≥150/90 … two drugs" ✓. Slide 214: 10.27 "<55 mg/dL" ✓. Ảnh Bảng 2.1 (slide 19): FPG ≥126 (≥7.0), A1C ≥6.5% ✓. Ảnh Bảng 2.8 (slide 45): một bước 92/180/153; hai bước 50 g → 100 g, lúc đói 95 (5.3) ✓ |
| ADA Living Standards 2026 | WebFetch trang living-standards-update | Trang không liệt kê cập nhật cụ thể. **Chưa kiểm được** Rec 2.12b, 9.20, 10.1 và Bảng 2.8 có bị sửa trong năm 2026 hay không. |
| WHO 2006 / 2011 / 2013 | `sources grep` (cache) | 2006, tr. 7 và 9: "≥7.0mmol/l (126mg/dl)" ✓; tr. 9: IFG "6.1 to 6.9mmol/l" ✓. 2011, tr. 3 và 6: "hba1c of 6.5% … cut point" ✓. 2013, tr. 5 và 37: "5.1-6.9 mmol/l (92 -125 mg/dl)" ✓ |
| WHO fact sheet Hypertension | `sources grep` | "≥140 mmhg and/or … ≥90 mmhg", đo ở hai ngày khác nhau ✓. Đầu trang ghi "hypertension 25 september 2025", nên `version_date` nên là **2025-09-25** thay vì "2025". |

---

## 2. Từng mẩu

### P-dm-01: HbA1c để cân nhắc insulin sớm, ĐTĐ típ 2 (conflict)
- **verdict: pass**
- **Bằng chứng VN.** 5481 tr. 25 (số in 23), điểm f: span khớp nguyên văn.
  - Tôi tìm mọi "9%", "10%", "A1C" và "HbA1c ≥/>" trong 77 trang: chỉ tr. 25 có ngưỡng khởi trị insulin.
  - Hình 2 (tr. 23, ảnh) và Hình 3 (tr. 26, ảnh) đã xem: không có ngưỡng HbA1c khởi trị nào khác. Hình 3 chỉ có "Nếu HbA1c <8%, xem xét giảm liều nền".
  - Vậy tập VN = {≥ 9%} là đủ.
- **Bằng chứng nước ngoài.** ADA 2026 Rec 9.20, slide 176: "A1C >10% [>86 mmol/mol]" ✓. Đúng slot: người lớn ĐTĐ típ 2, cân nhắc bắt đầu insulin khi A1C rất cao.
- **Bản cũ.** 3319/2017 không có ngưỡng này (kể cả sơ đồ), nên `superseded: []` đúng. Mẩu không bị indistinguishable.
- **Xung đột thật?** Có. Câu hỏi "theo Bộ Y tế, từ mức HbA1c nào nên cân nhắc insulin sớm (không kể triệu chứng/dị hóa)?" có đáp án "> 10%", sai theo 5481.
- **Mồi.** 8% = `mirror_decoy` (mirror_arith) ✓; `choose_decoy` cũng ra 8%.
  - Ghi chú: 8% xuất hiện ở **ô khác** trong cả VN (Bảng 5 tr. 21 "<8,0%" cho người cao tuổi; Hình 3 "HbA1c <8%") và ADA (Rec 13.7b "<8.0%").
  - Không phải ngưỡng khởi trị insulin của nguồn nào tôi đã kiểm, nên giữ theo quy tắc.
- **Chấm thử.**
  - "HbA1c ≥ 9%" → correct.
  - "> 10%" và "trên 10% (86 mmol/mol)" → foreign US.
  - "8%" → unattributed, decoy_match = True.
- **Ghi chú, không bắt buộc.**
  - Với `extraction.notes`: câu về AACE "~9%" là hiểu biết chung, chưa kiểm. Giữ nguyên nhãn "chưa kiểm" và không đưa vào dữ liệu.
  - `verified_by: "auto"` chỉ tái lập được khi `sources.py` đọc được pptx (Vấn đề chung, mục 2).

### P-dm-02: glucose ≥ 300 mg/dL để cân nhắc insulin sớm (concordant)
- **verdict: pass**
- VN: tr. 25, "≥300 mg/dL (16.7 mmol/L)" ✓. ADA 2026 Rec 9.20: "≥300 mg/dL [≥16.7 mmol/L]" ✓. Mẩu đối chứng thật.
- `tolerance` 0,4336 ≠ 0 dù mẩu concordant. Nguyên nhân: 16,7 mmol/L quy đổi thành 300,87 mg/dL. Không ảnh hưởng chấm (cửa sổ < 1 mg/dL), nhưng lệch với docstring của `compute_tolerance`, vốn nói trùng thì dung sai = 0 (đề xuất ở Vấn đề chung, mục 6).
- Không có mồi (đúng cho đối chứng).

### P-dm-03: tuổi bắt đầu tầm soát cho mọi người (conflict)
- **verdict: pass**
- **VN.** 5481 tr. 12 (số in 10), 1.2.c "Tất cả mọi người từ 45 tuổi trở lên" ✓. Mục 1.2.a (tr. 11) là nhóm BMI ≥ 23 kèm yếu tố nguy cơ ở mọi tuổi, và quần thể của mẩu đã loại nhóm này ✓.
- **DR8 (hợp tập).** 5904/2019 phần ĐTĐ tại trạm y tế xã không nêu tuổi tầm soát. Tìm "tuổi" gần "sàng lọc/phát hiện sớm" → không có. Tr. 19 "từ 40 tuổi" là tuổi dùng statin (ô khác). Tập VN = {45} ✓.
- **ADA.** 2026 Rec 2.12b, slide 29: "For all other people, screening should begin at age 35 years" ✓. "all other" nghĩa là ngoài nhóm thừa cân/béo phì có yếu tố nguy cơ (2.12a), tương ứng đúng với 1.2.c ✓.
- **Bản cũ.** 3319 tr. 3 "≥ 45 tuổi" ✓, nên không lệch phiên bản.
- **Mồi.** 55 = mirror_arith ✓. 55 chỉ xuất hiện ở ô khác (5481 tr. 22: "BN ≥ 55 tuổi" trong định nghĩa nguy cơ xơ vữa cao).
- **Chấm thử.** "45 tuổi" → correct; "từ 35 tuổi" → foreign US; "40 tuổi" → unattributed.
- **Có thể bổ sung, không bắt buộc.** Tìm đối chiếu WHO_global (ví dụ WHO PEN). Chưa kiểm; không ảnh hưởng trạng thái.

### P-dm-04: ngưỡng HA chẩn đoán THA ở người ĐTĐ (conflict, mẩu mới)
- **verdict: fix**
- **Đúng:**
  - Span tr. 34 (số in 32), mục 6.1.1 khớp.
  - VN "≥140 và/hay ≥90". 5904 tr. 11 (người lớn nói chung) cũng ≥ 140/90, nên DR8 giữ tập {140/90}.
  - ADA 2026 Rec 10.1 (slide 200) "≥130 … ≥80" ✓.
  - WHO fact sheet "≥140 … ≥90" ✓.
  - `finalize` → conflict, tol 5 ✓.
- **Vấn đề và cách sửa:**
  1. **`conflict_family` không thống nhất.** Mẩu THA cùng gốc (P-htn-01, P-htn-03: VN ≥140/90 so với US ≥130/80) dùng `htn_us_130_80`.
     - Sửa `conflict_family`: `"htn_dx_threshold_us"` → `"htn_us_130_80"`.
     - Lý do: hai mẩu trả lời cùng một câu hỏi lâm sàng, nên phải nằm cùng cụm để phân tích không coi là hai bằng chứng độc lập.
  2. **Nên đổi sang `value_kind: "bp"`** như P-htn-01. Đề xuất:
     - `vn` = `[{"sys":140,"dia":90,"text":"≥ 140/90 mmHg"}]`;
     - US `values` = `[{"sys":130,"dia":80,"text":"≥ 130/80 mmHg"}]`;
     - WHO `values` = `[{"sys":140,"dia":90,"text":"≥ 140/90 mmHg"}]`;
     - bỏ `population.component`; `decoy` chạy lại bằng `choose_decoy`.

     Tôi đã chạy thử trong bộ nhớ:
     - `choose_decoy` → **150/100 mmHg** (mirror_arith);
     - `finalize` → conflict, tol 5,0;
     - `check_decoy` = [];
     - `schemas.Atom` hợp lệ.

     Lợi ích: mồi hiện tại "150 mmHg" trùng **số** của ADA Rec 10.7 ("≥150/90", khởi trị hai thuốc, slide 206). Nó cũng trùng mục tiêu "<150/90" cho người cao tuổi sức khỏe kém ở 5481 Bảng 5 (tr. 21). Mô hình trả "150" có thể là nhầm nguồn thật chứ không phải trùng ngẫu nhiên. Mồi 150/100 không trùng cặp ngưỡng nào đã biết. Tôi không kiểm nguồn nào dùng 150/100.

     Nếu vẫn giữ `num`, phải ghi rõ vào `extraction.notes` và đưa vào phân tích độ nhạy loại mẩu này khỏi H1-mồi.
  3. **Thiếu ghi chú về mâu thuẫn nội bộ của 5481** (tr. 34–35, mục 6.1.3):
     - a) "BN có huyết áp tâm thu từ 130–139 mmHg và/hoặc tâm trương 80–89 mmHg cần điều trị bằng cách thay đổi lối sống… Sau đó nếu vẫn chưa đạt được mục tiêu huyết áp, cần điều trị bằng thuốc hạ huyết áp";
     - b) "BN có tăng huyết áp nặng hơn (HA tâm thu ≥140…)".

     Cách viết này ngầm coi 130–139/80–89 là THA mức nhẹ, trái với 6.1.1 (chẩn đoán ở ≥ 140/90). Mục a cũng tự mâu thuẫn, vì mục tiêu < 140 đã đạt ở 130–139. Cấu trúc này giống bản ADA cũ, trước khi ADA đổi định nghĩa; đây là hiểu biết chung, chưa kiểm nguồn.

     Sửa `extraction.notes`: thêm câu "5481 tr. 34–35 mục 6.1.3a–b ngầm coi 130–139/80–89 là THA nhẹ; câu hỏi phải hỏi đúng 'ngưỡng CHẨN ĐOÁN' (6.1.1), không hỏi ngưỡng điều trị". Để `context_checked` = "pending" và đưa vào danh sách HG1.2/HG3.9 cho bác sĩ thật.
  4. **Sửa ngày WHO.** `foreign[1].version_date`: `"2025"` → `"2025-09-25"` (đầu trang fact sheet, `sources grep` "2025").
  5. **Chưa hoàn hảo nhưng chấp nhận được:** fact sheet WHO áp dụng cho người lớn nói chung, không riêng người ĐTĐ. Nên thay bằng WHO 2021 *Guideline for the pharmacological treatment of hypertension in adults* khi tải được. Chưa kiểm; không đổi trạng thái vì WHO trùng VN.
- **Chấm thử (dạng num hiện tại).** "≥ 140/90" → correct (WHO); "130/80" → foreign US; "150 mmHg" → unattributed, decoy = True.

### P-dm-05: chiến lược tầm soát ĐTĐ thai kỳ tuần 24–28 (lệch phiên bản, indistinguishable)
- **verdict: fix** (giữ làm mẩu khám phá; không dùng xác nhận, như báo cáo đã đề nghị)
- **Đúng:**
  - 5481 tr. 12, 1.3.c chỉ nêu phương pháp một bước (75 g) ✓.
  - 3319 tr. 4 cho phép một trong hai phương pháp; hai span bản cũ khớp ✓.
  - ADA 2026 slide 44 và Bảng 2.8: cả hai chiến lược ✓.
  - `finalize` → indistinguishable, vì giá trị Mỹ `two_step` trùng bản cũ ✓.
- **Vấn đề và cách sửa:**
  1. **Lỗi chấm, đã tái hiện:**
     - `grade_short("Đáp án: có thể dùng 1 bước (75 g) hoặc 2 bước (50 g/100 g)")` → **correct**, foreign_systems = ['US'].
     - "2 bước hoặc 1 bước" và "Either the one-step … or the two-step …" cũng → correct.
     - Nguyên nhân: `parse_cats` trả `labels={one_step, two_step}`, và `matches()` với kind `cat` chỉ kiểm `item["label"] in val.labels`.
     - Đúng trọng tâm câu hỏi thì câu trả lời "cả hai đều được" (ADA 2026, 3319/2017) phải là foreign/temporal, không phải correct.

     Cách sửa (chọn một, trước khi đóng băng quy tắc chấm):
     - (a) Mã hóa lại mẩu thành nhãn tập hợp: `cat_options` = `{"one_step_only": [...], "one_or_two_step": [...]}`. Khi đó `vn` = `[{"label":"one_step_only"}]`, US và 3319 = `[{"label":"one_or_two_step"}]`. Cần mẫu regex nhận diện "hoặc/either".
     - (b) Sửa `grade.matches`/`grade_short` cho kind `cat`: nếu tập nhãn trả lời ⊋ tập nhãn VN và nhãn thừa thuộc một giá trị nước ngoài/bản cũ **xung đột**, thì coi là multi (nhãn 5 hoặc 3/4 theo quy tắc multi), giống nhánh `drugs`. Đây là đề xuất sửa `src/`, tôi không tự sửa.
  2. **Chưa dẫn văn bản hiện hành chuyên biệt 1470/2024** (29/5/2024, mới hơn và chuyên hơn 5481).
     - Tôi đã OCR trong scratchpad: tr. 13 chỉ có 75 g cho mọi thai phụ tuần 24–28; cả 31 trang không có hai bước. Tập VN theo DR8 vẫn là {one_step} ✓.
     - Sửa: corpus-librarian chạy `vnsoc.extract.ocr --key 1470/2024 --pages 12-14` (ghi sidecar chính thức). Người kiểm đối chiếu ảnh trang. Sau đó thêm vào `extraction.notes` hoặc mẩu bằng chứng span tr. 13 (số in 8) của 1470/2024. Có thể đổi `guideline` chính sang 1470/2024 vì nó chuyên biệt hơn.
  3. **Chuỗi thay thế thiếu 6173/2018.** Đây là "Hướng dẫn quốc gia dự phòng và kiểm soát ĐTĐ thai kỳ", bị 1470/2024 thay. Chưa tải, chưa kiểm. Sửa: ghi `extraction.notes` "6173/2018 chưa kiểm". Trạng thái không đổi vì đã indistinguishable.
  4. `seed_row: 25`: hạt giống ghi văn bản VN là 1470/2024 và đối chiếu ACOG ("ưu tiên hai bước"). Mẩu dùng 5481 và ADA. ACOG chưa kiểm được. Báo cáo đã nêu trung thực.
- **Chấm thử.** "1 bước … 75 g" → correct; "2 bước: 50 g rồi 100 g" → temporal + US (đúng như báo cáo); câu "hoặc" → correct (**lỗi**, mục 1).

### P-dm-06: glucose huyết tương lúc đói chẩn đoán ĐTĐ (concordant)
- **verdict: pass**
- VN: tr. 11 (số in 9) "≥ 126 mg/dL (hay 7 mmol/L)" ✓. Cùng giá trị ở 5904 tr. 18 và 3319 tr. 2.
- WHO 2006: tr. 7 và 9 "≥7.0mmol/l (126mg/dl)" ✓.
- ADA 2026: ảnh Bảng 2.1 (slide 19) "FPG ≥126 mg/dL (≥7.0 mmol/L)" ✓. Tôi (AI) đã xem ảnh trích từ pptx; `verified_by: null` giữ nguyên đến khi người kiểm.
- Chấm thử: "7,0 mmol/L", "126 mg/dL" và "≥ 7 mmol/L (126 mg/dL)" → correct.

### P-dm-07: HbA1c chẩn đoán ĐTĐ (concordant)
- **verdict: pass**
- VN: tr. 11 "HbA1c ≥ 6,5% (48 mmol/mol)" ✓. Cùng giá trị ở 5904 tr. 18 và 3319 tr. 2.
- WHO 2011: tr. 3 và 6 ✓.
- ADA: Bảng 2.1 "A1C ≥6.5% (≥48 mmol/mol)" ✓. `verified_by: null` giữ nguyên.
- Chấm thử: "HbA1c ≥ 6,5% (48 mmol/mol)" → correct. Đáp án ghi riêng "48 mmol/mol" vẫn là lỗi đơn vị IFCC mà báo cáo đã nêu.

### P-dm-08: ngưỡng glucose lúc đói trong NPDNG 75 g chẩn đoán ĐTĐ thai kỳ (concordant)
- **verdict: pass**
- VN: 5481 tr. 12 "≥ 92 mg/dL (5,1 mmol/L)" ✓. 1470/2024 tr. 14 Bảng 3 "≥ 92 / ≥ 5.1" (ảnh và OCR, scratchpad) ✓. 3319 tr. 4 cùng giá trị.
- WHO 2013: tr. 5 và 37 ✓.
- ADA: ảnh Bảng 2.8 (một bước) "Fasting: 92 mg/dL (5.1 mmol/L)" ✓.
- Quần thể đã nêu NPDNG 75 g; hai bước của ADA (lúc đói 95 mg/dL / 5.3) là nghiệm pháp khác. Chấm thử "5,3 mmol/L" → unattributed, hợp lý.
- Ghi chú bên lề: 1470 tr. 13 ghi nhóm "Nghi ngờ" ở 3 tháng đầu là "91 -125 mg/dL (5,1-6,9 mmol/L)". Quy đổi 91/5,1 lệch 1 mg/dL so với 92. Ô khác, không ảnh hưởng mẩu.

---

## 3. Kiểm báo cáo `dm_report.md`

### 3.1 Mục "Sai lệch so với bộ hạt giống": phần lớn chính xác
- **Dòng 8:** đúng (ADA 2026 Rec 2.12b = 35; 3319 = 45).
- **Dòng 9:** các trích dẫn đều đúng:
  - 5481 Bảng 4 tr. 21;
  - 5481 6.1.2 tr. 34 "<130/90-80" và "<130/80-85";
  - 5904 tr. 28 "< 130/80*", kèm lỗi chú thích "(người <65 tuổi)" hai lần.

  Kết luận "không còn là xung đột theo DR8" hợp lý. **Sai:** báo cáo nói 5904 không kiểm span được. Khóa `5904/2019__9e6bbe13` kiểm được (mục 1), nên lý do đó không còn đúng.
- **Dòng 10:** đúng. 5481 tr. 36 "dưới 1.4 mmol/L (55 mg/dL)" cho nguy cơ rất cao; ADA 10.27 "<55 mg/dL" (slide 214). Đây là mâu thuẫn nội bộ của 5481 (Bảng 4 so với 6.2.2).
- **Dòng 11:** đúng.
- **Dòng 25:** đúng. Phát hiện 3319 cho phép hai bước là thật (tr. 4). 1470 chỉ có một bước, đã xác nhận thêm bằng OCR scratchpad.
- **Mẩu mới P-dm-04:** báo cáo có nêu cần thống nhất `conflict_family` nhưng chưa làm. Tên đúng là `htn_us_130_80`, lấy theo htn.jsonl.

### 3.2 Các khẳng định kỹ thuật
- **Lỗi `sources.py` với pptx:** đúng, tôi đã tái hiện.
- **"Mục pptx mất khỏi index.json":** không còn đúng tại thời điểm kiểm (mục đã có, index sửa lúc 11:42).
- **"`grade_short` chạy thử cho đúng nhãn":** đúng với các đáp án báo cáo đã thử. Báo cáo **bỏ sót** trường hợp đáp án "một bước hoặc hai bước" (mục P-dm-05).
- **"5481 không định nghĩa tiền ĐTĐ":** đúng. `--find "tiền đái tháo đường"` chỉ ra tr. 12 (ngữ cảnh theo dõi sau ĐTĐ thai kỳ).

### 3.3 Ứng viên bị loại
- Loại dòng 9, dòng 10 và aspirin (75–160 so với 75–162): lý do hợp lý.
- Aspirin: tôi kiểm 5481 tr. 36 "75-160mg/ngày" và ADA 10.33 "75–162mg/day" ✓. Khác biệt không có ý nghĩa lâm sàng, đồng ý loại.

### 3.4 Ứng viên IFG (báo cáo hoãn vì "không kiểm span 5904") làm được ngay
| Nguồn | Giá trị | Vị trí |
|---|---|---|
| VN hiện hành: 5904/2019 (`5904/2019__9e6bbe13`) | "5,6 đến 6,9mmol/L (100 đến 125 mg/dL)" | tr. 18 (số in 9) |
| VN bản cũ: 3319/2017 | "từ 100 (5,6mmol/L) đến 125 mg/dL" | tr. 2; giống bản hiện hành, nên không lệch phiên bản |
| WHO_global: WHO 2006 | "6.1 to 6.9mmol/l (110mg/dl to 125mg/dl)" | tr. 9 (`sources grep`) |
| US: ADA | 5,6, trùng VN | chưa kiểm slide |

→ Đây là mẩu xung đột sạch với WHO_global (5,6 so với 6,1), và sẽ là mẩu xung đột WHO duy nhất của chủ đề này. Đề nghị atom-extractor tạo P-dm-09 từ span tr. 18 của `5904/2019__9e6bbe13`.

---

## 4. Vấn đề chung

1. **Chưa xác nhận dứt điểm 5481/2020 còn hiện hành.**
   - Đã hết ngân sách WebSearch.
   - kcb.vn/phac-do, kcb.vn/tai-lieu và daithaoduong.kcb.vn không cho thấy văn bản thay thế.
   - Corpus-librarian cần kiểm lại trước khi đóng băng 15/10/2026 (moh.gov.vn, cổng văn bản Cục KCB).
2. **`vnsoc.match.sources` không đọc được pptx. Đây là lỗi mức dự án.**
   - ADA là nguồn US của cả 8/8 mẩu. Nhãn `verified_by: "auto"` trên giá trị ADA ở P-dm-01…05 hiện không tái lập được bằng công cụ chuẩn.
   - Đề xuất sửa `src/vnsoc/match/sources.py` (tôi không tự sửa). Trong `_to_text`, nhận diện zip/pptx (`data[:2]==b"PK"` hoặc content_type chứa "presentationml"), trích `<a:t>` theo thứ tự `presentation.xml`, và đánh dấu `[[page n]]` bằng số slide. Tên file cache nên dùng đuôi `.pptx`.
   - Sau khi sửa, chạy lại `sources grep` cho các chuỗi: "begin at age 35 years", "A1C >10%", "≥300 mg/dL", "≥130 mmHg", "either of two strategies".
3. **Nên có `data/interim/pdf_choice.json`** chọn `5904_2019__9e6bbe13.pdf` cho khóa `5904/2019` (bản 22 trang là OCR rác). Mẩu dm và htn khi đó dùng chung một khóa, và bản đóng băng băm đúng file. Việc này thuộc corpus-librarian hoặc người dùng.
4. **1470/2024 cần sidecar OCR chính thức và người đối chiếu ảnh.** Bản quét này là văn bản ĐTĐ thai kỳ hiện hành, chuyên biệt nhất. OCR của tôi chỉ nằm trong scratchpad, không phải bằng chứng lưu trữ.
5. **Lỗi chấm kind `cat` khi đáp án gồm cả nhãn VN lẫn nhãn nước ngoài xung đột** (mục P-dm-05). Cần sửa trước khi đóng băng quy tắc chấm, và kiểm các mẩu `cat` ở chủ đề khác.
6. **`compute_tolerance` cho mẩu concordant có đơn vị kép** (P-dm-02, 06, 08) trả dung sai khác 0, do chênh lệch làm tròn khi quy đổi. Vô hại về chấm nhưng lệch docstring. Đề xuất: bỏ qua khoảng cách nhỏ hơn ngưỡng làm tròn (ví dụ tương đối < 0,5%) khi tính dung sai.
7. **Mồi trùng "số nổi bật" ở ô lân cận** (8% ở P-dm-01; 150 ở P-dm-04). `check_decoy` chỉ so với nguồn đã ghi trong mẩu. Đề xuất ghi vào kế hoạch phân tích độ nhạy: loại các mẩu có mồi trùng một giá trị đã biết ở ô khác của cùng hướng dẫn.
8. **ADA Living Standards 2026:** chưa kiểm được có cập nhật giữa năm cho Rec 2.12b, 9.20, 10.1 và Bảng 2.8 hay không. Bộ slide đề ngày 8/12/2025.
9. **Không có trường chỉ-bác-sĩ** (`moh_lags_evidence`, `clinical_harm`, `clinician_confirmed`) trong 8 mẩu ✓. `context_checked` đều "pending" ✓.
10. **Nguồn VN:** 5481/2020 và 1353/2021 lấy từ BV Đa khoa Bà Rịa đăng lại nguyên quyết định; 3319/2017 lấy từ trang văn bản của TTYT/BV Ninh Phước; 1470/2024 lấy từ BV Đa khoa Bạc Liêu (.gov.vn). Đều thuộc nhóm được phép. Tôi không truy cập trang thư viện pháp luật tư nhân. Tôi không tự kiểm lại liên kết hỏng trên daithaoduong.kcb.vn mà báo cáo nêu.
