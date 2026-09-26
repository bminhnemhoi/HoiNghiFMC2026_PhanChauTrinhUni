# Phản biện độc lập — bộ câu hỏi thí điểm `anaphylaxis_ocr`

- **Người phản biện:** Claude (AI), vai rev-clinician + rev-methods. **Không phải bác sĩ thật**: mọi nhận định lâm sàng dưới đây cần bác sĩ xác nhận ở HG3.9 trước khi đóng băng.
- **Ngày:** 2026-09-26. Không xem đầu ra của bất kỳ mô hình nào được kiểm tra.
- **Đã đọc:** `anaphylaxis_ocr.jsonl` (bản nháp), 6 mẩu `P-anaphylaxis_ocr-01..06` trong `data/interim/pilot_atoms.jsonl`, `anaphylaxis_ocr_q.jsonl`, `anaphylaxis_ocr_qc.csv`, `anaphylaxis_ocr_p.jsonl`; đề cương §1.2, §3.5, §4.2–4.4, §5.3, §5.7; SKILL `question-generation`; `configs/conditions.yaml`; `src/vnsoc/qgen/*.py`, `src/vnsoc/match/decoys.py`, `src/vnsoc/match/atom_flags.py`, `src/vnsoc/run/prompts.py`; `schemas.Question`, `schemas.NeighbourValue`.
- **Đối chiếu ảnh trang** TT51/2017 tr.9 và tr.20 (`data/cache/page_images/TT51_2017_p009.png`, `_p020.png`): mọi giá trị `vn` lấy từ TT51 của 6 mẩu khớp ảnh (0,2 / 0,25 / 0,3 / 0,5 / 0,5–1 ml; 1/2 ống; 1/5–1/3 ống; 3–5 phút/lần).
- **Tự kiểm bằng mã:** mọi câu thay thế đề xuất ở dưới đã chạy qua `vnsoc.qgen.build --only-drafted`, ghi ra thư mục nháp (không ghi vào dự án): 20 câu, 6 đoạn A3, **0 mục QC không đạt**, mã thoát 0; mỗi câu ≤ 60 từ.

## Kết luận

**pass 0 · fix 6 · drop 0**

| Mẩu | Trạng thái | Kết luận | Vấn đề chính |
| --- | --- | --- | --- |
| -01 | conflict (DR8 cách đọc a) | **fix, nặng** | S1 mồi hiển thị lộ là giả; S2 giá trị 150 µg trùng giá trị Bộ Y tế của quần thể lân cận nhưng chưa ghi `moh_neighbour`; S3 trắc nghiệm bị nhiễu bởi giá trị Bộ Y tế không hiển thị (100 µg); S4; S5; S7 |
| -02 | concordant | fix, nhẹ | S7 (diễn đạt); S5 (đoạn A3) |
| -03 | concordant | fix, nhẹ | S7; “độ II–III” đọc như một khoảng cho một bệnh nhân; S5 |
| -04 | concordant | fix, nhẹ | S7; S5 (đoạn A3 tr.20 lỗi OCR nặng nhất) |
| -05 | conflict (DR8 cách đọc a) | **fix, nặng** | S1 (2/4 phương án có 4 chữ số lẻ); S2; S3 (200 µg của Bộ Y tế gần 150 µg nhất); S4; S5; S7 |
| -06 | concordant | fix, nhẹ | S7; “not yet in puberty” → “prepubertal”; S5 |

- **Về nội dung lâm sàng:** câu hỏi của cả 6 mẩu đúng quần thể. Không câu nào lộ đáp án hay gợi ý quốc gia/nguồn, và bản tiếng Anh trung thành với bản tiếng Việt. Riêng -02/-03/-04/-06 chỉ phải sửa diễn đạt: nếu người điều phối chấp nhận dạng nhiều câu thì 4 mẩu này đạt **pass**.
- **Về -01/-05:** chưa được dùng cho H1, kể cả trắc nghiệm, cho tới khi (i) S1–S3 được xử lý và (ii) người dùng quyết định cách đọc DR8 (HG, ghi vào docs/DECISIONS.md), như ghi chú mẩu đã nêu.

## Vấn đề nghiêm trọng (xếp theo mức độ)

### S1. Mồi hiển thị lộ rõ là giá trị giả (-01, -05): mức cao, vi phạm §1.2 “hợp lý như nhau”

- **Hiện trạng:** mồi hiển thị là `383,3333 µg` (EN `383.3333 µg`). Giá trị này do `mirror_arith` sinh ra, phản chiếu 150 µg qua tâm khoảng 200–333,3 µg. Ở -05, phương án nhiễu do mã sinh (`rule_filler`, phản chiếu qua mồi) cũng lẻ: `466,6667 µg`. Các phương án còn lại đều tròn (50 / 150 / 250 / 300 µg).
- **Hậu quả:** mô hình có thể loại phương án chỉ vì cách viết số, nên P(mồi) thấp giả tạo. Đây là sai lệch về phía xác nhận H1 (hiệu P(nước ngoài) − P(mồi) bị thổi phồng).
  - Ở -05, 2/4 phương án trông giả, nên câu thực chất còn hai lựa chọn (Bộ Y tế hoặc nước ngoài).
- **Mã xác nhận:**
  - `atom_flags.roundness_ok(atom)` = **False** cho cả hai mẩu, tức chúng rơi vào tầng S3.
  - `decoy_plausible` chưa chấm, nên `freeze_problems` sẽ chặn đóng băng (“chưa chấm decoy_plausible (HG3.5)”).
- **Sửa cụ thể**, theo đúng đường đã đăng ký trước (HG3.5, không tự chế):
  1. Chấm `decoy_plausible = false`, `decoy_plausible_reason` = “hiển thị 4 chữ số lẻ, không đúng độ chia lâm sàng”.
  2. Chạy `atom_flags.regenerate_decoy`, ra `{"lo": 400, "hi": 400, "unit": "ug"}` với rule `rounded` (độ chia g = 50 µg). Đã kiểm bằng mã: `check_decoy` = [] và `roundness_ok` thành True.
  3. Phương án nhiễu của -05 tự thành **500 µg**.
  4. Phương án mới:
     - -01: {250 vn, 150 foreign, 50 filler, 400 decoy}
     - -05: {300 vn, 150 foreign, 500 filler, 400 decoy}
  5. Ghi vào notes của -05 rằng 500 µg là giá trị Bộ Y tế của quần thể lân cận (TT51 điểm d/e: trẻ > 30 kg, người lớn). Giá trị này chấp nhận được làm phương án nhiễu vì không đúng cho trẻ 20 kg, giống cách làm ở mẩu anh em P-anaphylaxis-03.
- **Không sửa bằng cách làm tròn khi hiển thị:** `render.py` không được gõ lại số.

### S2. 150 µg trùng giá trị Bộ Y tế của quần thể lân cận nhưng không được ghi vào `Atom.moh_neighbour` (-01, -05): mức cao, về toàn vẹn phân tích

- **Các giá trị trùng:**
  - QĐ 3942/2014, ch.5 “Dị ứng thức ăn”, tr.48: “Trẻ em nặng 10-25kg: adrenaline 0,15mg tiêm bắp” (sốc phản vệ do thức ăn), áp cho cả 10 kg lẫn 20 kg.
  - QĐ 3610/2015 tr.133: “EpiPen Jr. chứa 0.15 mg”.
- **Hiện trạng:** ghi chú mẩu đã mô tả điều này bằng chữ (“QUY NGUỒN… không quy riêng cho một hệ thống”), nhưng trường `moh_neighbour` để trống. Vì vậy `neighbour_overlap(atom)` = **False**, và phân tích độ vững N1 đã đăng ký (`analysis/confirmatory.py`, loại các mẩu có `moh_neighbour_overlap`) **sẽ không loại** hai mẩu này.
- **Đã kiểm bằng mã:** khi ghi `moh_neighbour` = {3942/2014 tr.48, 0,15 mg} thì `neighbour_overlap` = True, và mồi 400 µg vẫn qua `check_decoy`.
- **Sửa cụ thể** (bước mẩu, skill counterpart-matching; không phải bản nháp):
  - Thêm vào cả -01 và -05:
    ```json
    {"context": "sốc phản vệ do thức ăn, trẻ nặng 10–25 kg", "guideline": "3942/2014", "section": "Chương 5 Dị ứng thức ăn", "page": 48,
     "span": "Trẻ em nặng 10-25kg: adrenaline 0,15mg tiêm bắp", "values": [{"lo": 0.15, "hi": 0.15, "unit": "mg"}]}
    ```
  - Cân nhắc thêm mục cho 3610/2015 tr.133 sau khi kiểm span nguyên văn.

### S3. Trắc nghiệm -01/-05 bị nhiễu bởi giá trị Bộ Y tế không hiển thị: mức cao với phép so trắc nghiệm, không ảnh hưởng câu trả lời ngắn

- **Tập giá trị Bộ Y tế:** theo cách đọc (a), tập còn gồm 0,01 mg/kg (3312 tr.106; 3942 Bảng 3), tức **100 µg** ở -01 và **200 µg** ở -05. Đây cũng là quy tắc của WAO/Mỹ. Trắc nghiệm chỉ hiển thị `vn[0]` (TT51: 250 / 300 µg).
- **Mô hình tính theo cân nặng** (đúng theo Bộ Y tế) không tìm được phương án khớp:
  - -05: 200 µg gần **150 µg (nước ngoài, cách 50)** hơn 300 µg (cách 100).
  - -01: 100 µg cách đều 50 µg (nhiễu) và **150 µg (nước ngoài)**.
- **Hậu quả:** chọn “nước ngoài” khi đó không đo việc “áp khung tuổi của RCUK/WHO”. Nhiễu này ngược chiều với mồi (mồi 383/400 µg nằm phía bên kia), nên thiên về xác nhận H1.
  - Câu trả lời ngắn không bị ảnh hưởng, vì 100/200 µg được chấm là đúng theo Bộ Y tế.
  - Với -05, nhiễu vẫn còn theo cách đọc (c), vì 200 µg = 1/5 ống của PL X.
- **Sửa cụ thể:**
  - (i) **Ngay:** ở bước kiểm mơ hồ 100% mẩu xung đột, đặt `ambiguity_check = "fail"` cho 8 câu trắc nghiệm của -01/-05 (hoặc ghi loại khỏi phép so trắc nghiệm) và chỉ báo cáo mô tả.
  - (ii) **Quyết định của người dùng / statistician trước khi khóa OSF:** với mẩu có tập Bộ Y tế nhiều mục, có hiển thị mục Bộ Y tế gần giá trị nước ngoài nhất hay không. Ở -05 đó là 200 µg; ở -01 là 100 µg, nhưng khi đó phương án nhiễu tự sinh (phản chiếu 100 qua 150 = 200) rơi vào tập Bộ Y tế nên phải cấp nhiễu tay. Việc này chạm vào thứ tự ưu tiên hiển thị ở §1.2, nên cần một mục trong DECISIONS.

### S4. Trạng thái xung đột phụ thuộc cách đọc DR8; nguyên nhân “do thuốc” không được mã giữ (-01, -05; liên quan -02..-06)

- **Kết quả theo từng cách đọc** (đúng như `extraction.dr8_reading_sensitivity`):
  - -01, -05: (a) conflict · (b) concordant · (c) conflict.
  - -02: conflict theo (c).
  - -06: conflict theo (c).
- **Câu hỏi hiện nêu đủ “do thuốc”.** Nhưng các mẩu **không có `required_terms`**, và `population_issues` chỉ kiểm số tuổi/cân nặng. Nếu một lần sửa câu sau này bỏ mất “do thuốc”, câu vẫn qua QC trong khi 150 µg đã thành đúng theo Bộ Y tế (3942 ch.5).
- **Sửa cụ thể** (bước mẩu), thêm `required_terms`:
  - `cause`:
    - -01/-03/-04/-05/-06: `{"vi": ["do thuốc"], "en": ["caused by a drug", "drug-induced"]}`
    - -02: `{"vi": ["do thức ăn"], "en": ["caused by food"]}`
  - `severity`:
    - -01/-02/-04/-05/-06: `{"vi": ["độ III"], "en": ["grade III"]}`
    - -03: `{"vi": ["độ II"], "en": ["grade II"]}`
  - `setting`: `{"vi": ["cơ sở y tế"], "en": ["healthcare facility"]}`
  - Các câu thay thế ở dưới đều chứa những từ này.

### S5. Đoạn A3 là lớp chữ OCR chưa sửa (cả 6 mẩu): chặn đóng băng điều kiện A3

- **Nguồn:** `qgen.passages` đọc thẳng sidecar OCR `data/interim/ocr/TT51_2017/p009.txt` và `p020.txt`, không có lớp sửa tay.
- **Lỗi so với ảnh, trang 9** (đoạn của -01/-02/-03/-05/-06):

  | OCR | Đúng theo ảnh |
  | --- | --- |
  | Phác do | Phác đồ |
  | én định; on dinh | ổn định |
  | > 90mmHg; > 70mmHg | ≥ 90mmHg; ≥ 70mmHg |
  | hô hap; hô hâp | hô hấp |
  | rit | rít |
  | dau hiệu vê | dấu hiệu về |
  | **Img = 1ml** | **1mg = 1ml** (chính là quy tắc đổi ml↔mg mà câu -03 cần) |
  | 1⁄3 (U+2044) | 1/3 |
  | 1⁄2 - ] | 1/2 - 1 |
  | phut/lan; phúVlần | phút/lần |
  | Néu mach | Nếu mạch |
  | tiêm băp | tiêm bắp |
  | tuân hoàn | tuần hoàn |

  Đoạn còn kết thúc lơ lửng ở “a) Nếu chưa có đường truyền tĩnh mạch:”, trái tinh thần “không cắt giữa câu” của SKILL bước 6.
- **Lỗi so với ảnh, trang 20** (đoạn của -04):

  | OCR | Đúng theo ảnh |
  | --- | --- |
  | **A Ning (độ nm 4** | **Nặng (độ II)** |
  | (Cs thé chuyén độ | (Có thể chuyển độ |
  | (ong 1mg/1ml) | (ống 1mg/1ml) |
  | Img/kg | 1mg/kg |
  | TIEM BAP | TIÊM BẮP |
  | ký tự “6” thừa | (bỏ) |
  | Thiêt lập | Thiết lập |
  | dau hiệu | dấu hiệu |
  | 1m1 | 1ml |
  | 50-100ug | 50-100µg |
  | “Y Y” | (rác, bỏ) |

  Ngoài ra, việc duỗi sơ đồ thành một dòng làm mất quan hệ giữa các ô.
- **Hậu quả:** tỉ lệ cố chấp = P(nước ngoài | A3). Nhiễu trong đoạn oracle làm tăng giả lỗi “cố chấp/không quy được nguồn”. Nhiễu này lại chỉ có ở mẩu OCR, nên bị trộn với biến văn bản/chủ đề trong GLMM.
- **Sửa cụ thể** (người điều phối; không phải bản nháp): tạo lớp đoạn A3 sửa tay, hoặc sửa sidecar rồi chạy lại `verify_span`. Span của -04 (“TIEM BAP…”) và -05 (“1⁄3”) đang chép lỗi OCR: đã kiểm, chúng không còn khớp nguyên văn với bản sửa, nên phải cập nhật span cùng lúc. Bản chép lại từ ảnh ở **Phụ lục A** (đã chạy `passage_alt_values`: không cờ nào; 215 và 169 từ). Người thật phải so lại với ảnh trước khi đóng băng.

### S6. Nhãn mục của prompt A3 chỉ thẳng vào dòng đáp án: xuyên suốt, mức trung bình

- **Hiện trạng:** `run.prompts.short_prompt` điền `{section}` bằng nguyên `atom.section`. Ở đây nhãn kết thúc bằng “điểm b / c / d / e”, tức chỉ đúng hàng cân nặng chứa đáp án.
- **Phạm vi:** 14/65 mẩu thí điểm có nhãn chỉ tới điểm/dòng; các mẩu khác chỉ ghi mục. Mức gợi ý ở A3 vì thế không đều giữa các mẩu và tương quan với chủ đề (nhiễu cho H3).
- **Đề nghị:** trong prompt A3, cắt phần chỉ tới điểm/dòng (ví dụ “Phụ lục III, mục IV”), hoặc đăng ký rõ cách làm hiện tại.
- **Phụ:** prompt A3 tiếng Anh đang in chuỗi mục tiếng Việt.

### S7. Dạng câu tình huống nhiều câu, không theo mẫu một câu theo slot (cả 6 mẩu): mức trung bình, lý do chính của các “fix nhẹ”

- **Hiện trạng:** bản nháp viết 2 câu kể + 1 câu hỏi. Chỉ `anaphylaxis_ocr` (6) và `malaria_ocr` (8) làm vậy; 45/59 bản nháp còn lại, kể cả mẩu anh em P-anaphylaxis-03, dùng **một câu** theo mẫu slot (SKILL bước 1 “mẫu câu cố định theo slot_type”; quy tắc viết “MỘT câu hỏi”).
- **Hậu quả với A1:** tiền tố bám vào câu kể thay vì câu hỏi. Ví dụ: “Theo hướng dẫn … Bộ Y tế Việt Nam, trẻ 18 tháng … bị phản vệ độ III … tại cơ sở y tế. Nhân viên y tế tiêm … Liều … là bao nhiêu (µg)?”. A3 cũng vậy: “Dựa vào đoạn trích, trẻ 18 tháng … bị phản vệ …”.
  - Phạm vi của gợi ý quốc gia vì thế khác nhau giữa các chủ đề, và khác biệt này trùng đúng với nhóm mẩu OCR.
  - Nó cũng làm mờ ranh giới giữa câu trả lời ngắn và tình huống A6 (RQ4).
- **Sửa:** dùng các câu thay thế ở dưới (đã qua QC mã, ≤ 60 từ). Khi ghép tiền tố, chúng đọc thành “Theo hướng dẫn …, liều adrenalin tiêm bắp đầu tiên cho … là bao nhiêu (µg)?”.

## Từng mẩu

### P-anaphylaxis_ocr-01 — **fix (nặng)**
- **(1) Đáp án duy nhất / nước ngoài có “cũng đúng”?**
  - Theo (a), tập Bộ Y tế = {250; 200–333,3; 0,01 mg/kg = 100} µg. Tập nhiều mục là đúng thiết kế §1.2.
  - 150 µg nằm ngoài mọi mục một khoảng lớn hơn dung sai (cách 50 so với dung sai 25), nên không đúng theo (a)/(c). Theo (b) thì đúng (3942 ch.5 tr.48): chờ HG.
  - Quần thể đủ: 18 tháng (1–2 tuổi), 10 kg, độ III, do thuốc, cơ sở y tế, nhân viên y tế tiêm, ống 1 mg/1 ml, liều tiêm bắp đầu tiên.
- **(2) Lộ đáp án/nguồn?** Không. “Độ III” có định nghĩa trong ngoặc, trùng thang Ring–Messmer, không phải dấu hiệu quốc gia.
- **(3) Tiếng Anh:** trung thành.
- **(4) Diễn đạt:** tự nhiên. “18 tháng (1–2 tuổi)” hơi thừa nhưng bắt buộc theo `population.age`.
- **(5) Trắc nghiệm:** cùng đơn vị µg. Không phương án nào nằm trong tập Bộ Y tế (383,3 > 333,3 + 25; 50 < 100 − 25). Nhưng bị S1 và S3.
- **(6) Đơn vị:** có (µg).
- **Sửa:** thay dòng nháp như dưới (filler null, notes cập nhật). Bước mẩu: S1, S2, S3, S4. Giữ ngoài H1 cho tới quyết định DR8.
```json
{"atom_id": "P-anaphylaxis_ocr-01", "short_vi": "Liều adrenalin tiêm bắp đầu tiên cho trẻ 18 tháng (1–2 tuổi), nặng 10 kg, bị phản vệ độ III (tụt huyết áp, chưa ngừng tuần hoàn) do thuốc, xảy ra ngay sau tiêm kháng sinh tại cơ sở y tế, được nhân viên y tế tiêm từ ống 1 mg/1 ml (1:1.000), là bao nhiêu (µg)?", "short_en": "What is the initial intramuscular adrenaline dose (µg) for an 18-month-old child (aged 1–2 years) weighing 10 kg with grade III anaphylaxis (hypotension, without cardiac arrest) caused by a drug, occurring immediately after an antibiotic injection in a healthcare facility, given by a health worker from a 1 mg/1 mL (1:1,000) ampoule?", "mcq_stem_vi": "Phương án nào sau đây là liều adrenalin tiêm bắp đầu tiên cho trẻ 18 tháng (1–2 tuổi), nặng 10 kg, bị phản vệ độ III (tụt huyết áp, chưa ngừng tuần hoàn) do thuốc, xảy ra ngay sau tiêm kháng sinh tại cơ sở y tế, được nhân viên y tế tiêm từ ống 1 mg/1 ml (1:1.000)?", "mcq_stem_en": "Which of the following is the initial intramuscular adrenaline dose for an 18-month-old child (aged 1–2 years) weighing 10 kg with grade III anaphylaxis (hypotension, without cardiac arrest) caused by a drug, occurring immediately after an antibiotic injection in a healthcare facility, given by a health worker from a 1 mg/1 mL (1:1,000) ampoule?", "filler": null}
```

### P-anaphylaxis_ocr-02 — **fix (nhẹ, chỉ diễn đạt)**
- **(1)** Theo (a)/(b) là concordant: tập Bộ Y tế {250; 200–333,3; 100; 150 (3942 ch.5)} chứa mọi giá trị nước ngoài. Theo (c) là conflict. Thức ăn là lạc, không phải dứa (3610 tr.166), đúng như mẩu ghi.
- **(2)** Không lộ.
- **(3)** Trung thành.
- **(4)** Tự nhiên.
- **(5)** Không có trắc nghiệm.
- **(6)** Có đơn vị (µg).
- **Ghi chú:** cặp -01/-02 chỉ khác nguyên nhân, nên là phép thử tốt về độ nhạy với nguyên nhân. Nếu người dùng chọn (b), chỉ giữ một mẩu.
```json
{"atom_id": "P-anaphylaxis_ocr-02", "short_vi": "Liều adrenalin tiêm bắp đầu tiên cho trẻ 18 tháng (1–2 tuổi), nặng 10 kg, bị phản vệ độ III (tụt huyết áp, chưa ngừng tuần hoàn) do thức ăn, xảy ra ngay sau khi ăn lạc (đậu phộng), được nhân viên y tế tại cơ sở y tế tiêm từ ống 1 mg/1 ml (1:1.000), là bao nhiêu (µg)?", "short_en": "What is the initial intramuscular adrenaline dose (µg) for an 18-month-old child (aged 1–2 years) weighing 10 kg with grade III anaphylaxis (hypotension, without cardiac arrest) caused by food, occurring immediately after eating peanuts, given by a health worker in a healthcare facility from a 1 mg/1 mL (1:1,000) ampoule?", "mcq_stem_vi": null, "mcq_stem_en": null, "filler": null}
```

### P-anaphylaxis_ocr-03 — **fix (nhẹ, chỉ diễn đạt)**
- **(1)** Tập Bộ Y tế là một khoảng 0,5–1 mg; RCUK/WAO/Mỹ 0,5 mg nằm trong, nên concordant. Nêu “do thuốc” loại được 0,3–0,5 mg của chương côn trùng đốt (3942 ch.10).
- **(2)** Cố ý không ghi “1 mg/1 ml”, vì trùng cận trên 1 mg (QC báo lộ). Cách làm này đúng; câu sửa giữ nguyên.
- **(3)** Trung thành.
- **(4)** “Bị phản vệ độ II–III” đọc như một khoảng cho một bệnh nhân, nên sửa thành “phản vệ nặng (độ II) hoặc nguy kịch (độ III)”. “Dung dịch adrenalin 1:1.000 (dạng ống)” sửa thành “ống adrenalin 1:1.000”.
- **(6)** Có đơn vị (mg).
```json
{"atom_id": "P-anaphylaxis_ocr-03", "short_vi": "Liều adrenalin tiêm bắp đầu tiên cho người lớn (≥ 18 tuổi), nặng khoảng 60 kg (≥ 50 kg), bị phản vệ nặng (độ II) hoặc nguy kịch (độ III) do thuốc, xảy ra ngay sau tiêm kháng sinh tại cơ sở y tế, được nhân viên y tế tiêm từ ống adrenalin 1:1.000, là bao nhiêu (mg)?", "short_en": "What is the initial intramuscular adrenaline dose (mg) for an adult (≥ 18 years) weighing about 60 kg (≥ 50 kg) with severe (grade II) or critical (grade III) anaphylaxis caused by a drug, occurring immediately after an antibiotic injection in a healthcare facility, given by a health worker from a 1:1,000 adrenaline ampoule?", "mcq_stem_vi": null, "mcq_stem_en": null, "filler": null}
```

### P-anaphylaxis_ocr-04 — **fix (nhẹ, chỉ diễn đạt)**
- **(1)** Tập Bộ Y tế {3–5; 5–15} phút. RCUK 5 và WAO 5–15 đều nằm trong, nên concordant theo cả 3 cách đọc.
  - Là đối chứng yếu: hầu như mọi câu trả lời từ 3 đến 15 phút đều đúng. Điều này đã biết và chấp nhận được cho vai trò đối chứng.
  - Quần thể người lớn loại được “5–10 phút” của 3312 (chỉ trẻ em). “Chưa đáp ứng” đúng ngữ cảnh nhắc lại. Câu hỏi hỏi khoảng cách tiêm bắp, không nhầm với tần suất theo dõi huyết áp.
- **(2)** Không lộ.
- **(3)** Trung thành.
- **(4)** Tự nhiên.
- **(6)** Có đơn vị (phút).
- **Câu sửa:** vừa đúng 60 từ. Để vừa giới hạn, đã bỏ “(1:1.000)” và “ngay”; nồng độ vẫn nêu qua “ống 1 mg/1 ml”.
- **Đoạn A3:** trang 20 có lỗi OCR nặng nhất (S5).
```json
{"atom_id": "P-anaphylaxis_ocr-04", "short_vi": "Khoảng cách giữa các lần tiêm bắp nhắc lại adrenalin ống 1 mg/1 ml cho người lớn (≥ 18 tuổi) bị phản vệ độ III (tụt huyết áp, chưa ngừng tuần hoàn) do thuốc, sau tiêm kháng sinh tại cơ sở y tế, đã được nhân viên y tế tiêm liều đầu nhưng chưa đáp ứng, là bao nhiêu (phút)?", "short_en": "What is the interval (minutes) between repeat intramuscular injections of adrenaline from a 1 mg/1 mL ampoule for an adult (≥ 18 years) with grade III anaphylaxis (hypotension, without cardiac arrest) caused by a drug, after an antibiotic injection in a healthcare facility, who has received the first dose from a health worker but has not responded?", "mcq_stem_vi": null, "mcq_stem_en": null, "filler": null}
```

### P-anaphylaxis_ocr-05 — **fix (nặng)**
- **(1)** Tập Bộ Y tế = {300; 200–333,3; 0,01 mg/kg = 200} µg. 150 µg nằm ngoài (cách 50 so với dung sai 25), nên conflict theo (a)/(c); theo (b) là concordant (3942 tr.48, 10–25 kg). Khung tuổi RCUK 6 tháng–6 tuổi chứa trẻ 5 tuổi; khung WAO 1–5 tuổi thì 5 tuổi nằm đúng mép.
- **(2)** Không lộ.
- **(3)** Trung thành.
- **(4)** Tự nhiên.
- **(5)** Ca nặng nhất của S1 (2/4 phương án lẻ 4 chữ số) và của S3 (200 µg gần 150 µg nhất).
- **(6)** Có đơn vị (µg).
- **Sửa:** thay dòng nháp như dưới. Bước mẩu: S1, S2, S3, S4.
```json
{"atom_id": "P-anaphylaxis_ocr-05", "short_vi": "Liều adrenalin tiêm bắp đầu tiên cho trẻ 5 tuổi, nặng 20 kg, bị phản vệ độ III (tụt huyết áp, chưa ngừng tuần hoàn) do thuốc, xảy ra ngay sau tiêm kháng sinh tại cơ sở y tế, được nhân viên y tế tiêm từ ống 1 mg/1 ml (1:1.000), là bao nhiêu (µg)?", "short_en": "What is the initial intramuscular adrenaline dose (µg) for a 5-year-old child weighing 20 kg with grade III anaphylaxis (hypotension, without cardiac arrest) caused by a drug, occurring immediately after an antibiotic injection in a healthcare facility, given by a health worker from a 1 mg/1 mL (1:1,000) ampoule?", "mcq_stem_vi": "Phương án nào sau đây là liều adrenalin tiêm bắp đầu tiên cho trẻ 5 tuổi, nặng 20 kg, bị phản vệ độ III (tụt huyết áp, chưa ngừng tuần hoàn) do thuốc, xảy ra ngay sau tiêm kháng sinh tại cơ sở y tế, được nhân viên y tế tiêm từ ống 1 mg/1 ml (1:1.000)?", "mcq_stem_en": "Which of the following is the initial intramuscular adrenaline dose for a 5-year-old child weighing 20 kg with grade III anaphylaxis (hypotension, without cardiac arrest) caused by a drug, occurring immediately after an antibiotic injection in a healthcare facility, given by a health worker from a 1 mg/1 mL (1:1,000) ampoule?", "filler": null}
```

### P-anaphylaxis_ocr-06 — **fix (nhẹ, chỉ diễn đạt)**
- **(1)** Tập Bộ Y tế {500; 200–333,3; 350; 300} µg rất rộng, chứa mọi giá trị nước ngoài, nên concordant theo (a)/(b). Theo (c) là conflict (WAO 350 > 333,3 + 8,3).
  - WHO Pocket Book (150 µg) bị loại vì phạm vi sách là “young children”, bảng liều thuốc dừng ở 29 kg. Cần HG xác nhận: nếu tính vào thì mẩu thành conflict.
- **(2)** Không lộ.
- **(3)** “Not yet in puberty” sửa thành “prepubertal” cho tự nhiên.
- **(4)** Tự nhiên. “Chưa dậy thì” không liên quan liều, nhưng có trong `population.age`, nên giữ.
- **(6)** Có đơn vị (µg).
```json
{"atom_id": "P-anaphylaxis_ocr-06", "short_vi": "Liều adrenalin tiêm bắp đầu tiên cho trẻ 10 tuổi, chưa dậy thì, nặng 35 kg, bị phản vệ độ III (tụt huyết áp, chưa ngừng tuần hoàn) do thuốc, xảy ra ngay sau tiêm kháng sinh tại cơ sở y tế, được nhân viên y tế tiêm từ ống 1 mg/1 ml (1:1.000), là bao nhiêu (µg)?", "short_en": "What is the initial intramuscular adrenaline dose (µg) for a prepubertal 10-year-old child weighing 35 kg with grade III anaphylaxis (hypotension, without cardiac arrest) caused by a drug, occurring immediately after an antibiotic injection in a healthcare facility, given by a health worker from a 1 mg/1 mL (1:1,000) ampoule?", "mcq_stem_vi": null, "mcq_stem_en": null, "filler": null}
```

**Việc cho người viết:** thay 6 dòng trên (giữ và cập nhật trường `notes`), rồi chạy lại `vnsoc.qgen.build --only-drafted`. Kết quả mong đợi là 0 mục QC không đạt; phản biện đã chạy thử và cho kết quả này.

## Việc ngoài bản nháp (cho người điều phối / bước mẩu)

1. **HG3.5 cho -01/-05** (S1): chấm `decoy_plausible=false`, chạy `regenerate_decoy` để được mồi 400 µg (“rounded”), ghi `decoy_rule`/`roundness_ok`, rồi dựng lại câu hỏi.
2. **Ghi `moh_neighbour`** (3942 tr.48, 0,15 mg) cho -01/-05 (S2).
3. **Thêm `required_terms`** (cause / severity / setting) cho 6 mẩu (S4).
4. **Quyết định cho trắc nghiệm -01/-05** (S3): đặt `ambiguity_check=fail` ngay; quy tắc hiển thị mục Bộ Y tế gần nước ngoài nhất thì cần mục DECISIONS.
5. **Sửa đoạn A3** theo ảnh (S5, Phụ lục A) và cập nhật span -04/-05 nếu sửa sidecar.
6. **Nhãn mục trong prompt A3** (S6): áp dụng chung cho 14/65 mẩu.
7. **Quyết định DR8** (HG): -01/-05 chưa vào tập xác nhận H1.
8. **Lỗi đã biết, cần sửa ở `normalize_vi`:** chuỗi “0,01 ml/kg” đang bị đọc thành 10 µg. Câu hỏi đòi đơn vị µg nên giảm được rủi ro, nhưng vẫn cần sửa trước khi chấm.

## Phụ lục A — đoạn A3 chép lại từ ảnh trang (người thật phải so lại trước khi đóng băng)

**TT51/2017 tr.9: đoạn cho -01, -02, -03, -05, -06.** 215 từ, kết thúc trọn câu 4a); `passage_alt_values` = [] cho cả 5 mẩu.

> IV. Phác đồ sử dụng adrenalin và truyền dịch. Mục tiêu: nâng và duy trì ổn định HA tối đa của người lớn lên ≥ 90mmHg, trẻ em ≥ 70mmHg và không còn các dấu hiệu về hô hấp như thở rít, khó thở; dấu hiệu về tiêu hóa như nôn mửa, ỉa chảy. 1. Thuốc adrenalin 1mg = 1ml = 1 ống, tiêm bắp: a) Trẻ sơ sinh hoặc trẻ < 10kg: 0,2ml (tương đương 1/5 ống). b) Trẻ khoảng 10 kg: 0,25ml (tương đương 1/4 ống). c) Trẻ khoảng 20 kg: 0,3ml (tương đương 1/3 ống). d) Trẻ > 30kg: 0,5ml (tương đương 1/2 ống). e) Người lớn: 0,5-1ml (tương đương 1/2 - 1 ống). 2. Theo dõi huyết áp 3-5 phút/lần. 3. Tiêm nhắc lại adrenalin liều như khoản 1 mục IV 3-5 phút/lần cho đến khi huyết áp và mạch ổn định. 4. Nếu mạch không bắt được và huyết áp không đo được, các dấu hiệu hô hấp và tiêu hóa nặng lên sau 2-3 lần tiêm bắp như khoản 1 mục IV hoặc có nguy cơ ngừng tuần hoàn phải: a) Nếu chưa có đường truyền tĩnh mạch: Tiêm tĩnh mạch chậm dung dịch adrenalin 1/10.000 (1 ống adrenalin 1mg pha với 9ml nước cất = pha loãng 1/10).

Nếu muốn tránh hẳn nội dung tiêm tĩnh mạch, có thể dừng sau mục 3. Khi đó đoạn chỉ còn 146 từ, dưới mức 150 từ đã đăng ký, nên phải ghi là sai lệch.

**TT51/2017 tr.20: đoạn cho -04.** 169 từ; `passage_alt_values` = []. Các nhãn ô trong ngoặc vuông do người chép thêm để giữ cấu trúc sơ đồ; mũi tên trên ảnh đi từ “Nhẹ” xuống ô trái, từ “Nặng” xuống ô TIÊM BẮP, từ “Nguy kịch” xuống ô ĐƯỜNG TĨNH MẠCH. Cần người xác nhận.

> 1. ĐÁNH GIÁ MỨC ĐỘ (Có thể chuyển độ, nặng lên rất nhanh): Nhẹ (độ I); Nặng (độ II); Nguy kịch (độ III). 2. Xử trí ngay bằng ADRENALIN (ống 1mg/1ml) – Duy nhất cứu sống người bệnh. [Ô dưới 'Nhẹ (độ I)']: • Diphenhydramin: uống hoặc tiêm 1mg/kg • Methylprednisolon uống hoặc tiêm 1-2 mg/kg (hoặc các thuốc tương tự) • Theo dõi sát mạch, HA, ý thức... [Ô 'TIÊM BẮP']: - Người lớn: 1/2 ống - Trẻ em: 1/5-1/3 ống • Nhắc lại sau mỗi 3-5 phút cho đến khi hết các dấu hiệu về hô hấp và tiêu hóa, huyết động ổn định • Thiết lập sẵn đường truyền TM NaCl 0,9%. [Ô 'ĐƯỜNG TĨNH MẠCH']: Sau khi tiêm bắp adrenalin > 2 lần huyết áp không lên, các dấu hiệu hô hấp và tiêu hóa nặng lên: • Nếu chưa có đường truyền tĩnh mạch: Tiêm TM chậm adrenalin pha loãng 1/10 (0,1mg = 1ml), tiêm nhắc lại khi cần - Người lớn: 0,5-1ml (50-100µg).

## Trạng thái sau vòng 3 (atom-extractor + question-writer, 2026-09-26)

Không xem đầu ra mô hình nào. Kiểm bằng mã: `pilot_merge --only anaphylaxis_ocr` (vào scratchpad) giữ 6/6 mẩu, 0 loại. `qgen.build --only-drafted` cho 12 câu, 6 đoạn A3, 6 trắc nghiệm bỏ có chủ đích, 0 mục QC không đạt. Chấm thử bằng câu trả lời tự viết: 42/42 đúng nhãn mong đợi.

| Mục | Trạng thái |
| --- | --- |
| S1 mồi lẻ | Mồi nay do quy tắc sinh khi gộp: **390 µg** (mirror_arith, làm tròn step 10). Không chọn tay. `roundness_ok` = False (tầng S3). Việc chấm `decoy_plausible` và `regenerate_decoy` (400 µg) vẫn thuộc HG3.5. Phương án lẻ 383,3333 / 466,6667 µg không còn. |
| S2 `moh_neighbour` | **Xong** cho -01 và -05: 3942/2014 tr.48 “Trẻ em nặng 10-25kg: adrenaline 0,15mg tiêm bắp” và 3610/2015 tr.133 “EpiPen Jr. chứa 0.15 mg”. Nguyên văn đã kiểm trên trang lớp chữ. `neighbour_overlap` = True. |
| S3 trắc nghiệm -01/-05 | Mã bỏ có chủ đích (tập Bộ Y tế nhiều mục DR8), nên không còn phương án hiển thị. Nếu chọn DR8 cách đọc (c), mã sẽ sinh trắc nghiệm, và nhiễu 200 µg ở -05 quay lại: phải xét lại. |
| S4 `required_terms` | **Xong** cho 6 mẩu (cause / severity / setting, cùng dose = tiêm bắp). Thử phản chứng: QC bắt được khi bỏ từng khóa. |
| S5 đoạn A3 OCR | **Còn treo** (sửa sidecar theo ảnh, người điều phối). Mã mới đã cắt đoạn trọn câu. Đoạn -03 bắt đầu từ dòng “b)”, thiếu đầu mục “1. Thuốc adrenalin … tiêm bắp:”. Span -04 (“TIEM BAP”) và -05 (“1⁄3”) cố ý giữ theo lớp chữ OCR; khi sửa sidecar thì cập nhật cùng lúc. |
| S6 nhãn mục A3 | Mã `section_label` nay bỏ phần chỉ tới điểm/ô. Build kiểm nhãn: không cờ nào. |
| S7 dạng câu | Đã xong ở vòng 2. |
| Mục 8 “0,01 ml/kg” | Grader 1.1.0 đọc đúng: 100 µg ở 10 kg, 200 µg ở 20 kg. `vn_item_checks` đã tính lại; mọi nguồn khai báo đều đọc lại được. |
| population | Chỉ còn thuộc tính quần thể; ghi chú của người trích chuyển sang `extraction.notes`. |

## Trạng thái sau vòng 4 (sửa theo kiểm độc lập vòng 3, 2026-09-26)

Không xem đầu ra mô hình nào. Kiểm bằng mã: `pilot_merge --only anaphylaxis_ocr` giữ 6/6 mẩu, 0 loại (2 conflict, 4 concordant). `qgen.build --only-drafted` cho 12 câu, 6 đoạn A3, 6 trắc nghiệm bỏ có chủ đích, 0 mục QC không đạt. Chấm thử bằng câu trả lời tự viết (-01, -02, -05): 36/36 đúng nhãn mong đợi.

| Mục | Trạng thái |
| --- | --- |
| [CHẶN] mồi 390 µg nằm trong 0,3–0,5 mg của bối cảnh lân cận | **Đã sửa.** `moh_neighbour` của -01/-05 nay có đủ 17 mục. Cách làm: quét bằng mã 62 PDF trong data/raw, đọc từng trang trúng, kiểm từng span trên đúng trang. Trong đó có 3610 tr.133 (ong đốt nhiều nốt), 3610 tr.166 (dị ứng dứa), 3942 tr.77 (côn trùng đốt), 3942 tr.42 (phù Quincke), cùng các giá trị người lớn và các mức cân nặng khác. Quy tắc ghi và danh sách loại trừ có lý do nằm ở `extraction.notes`. Hệ quả do mã tính: mọi ứng viên của quy tắc (mirror_arith 380/390/383,3; mirror_geom 450–500/474,1; mirror_far 500) đều chạm giá trị lân cận, nên -01/-05 thành **mẩu xung đột không mồi**. Hai mẩu này nằm ngoài H1/H2 và được đếm trong addendum đóng băng. |
| Quyết định của người dùng | Mô phỏng: nếu coi liều người lớn và liều không nêu tuổi là KHÔNG thuộc “quần thể lân cận” của trẻ 10/20 kg, quy tắc lại cho mồi 390 µg. Cách hiểu này lệch câu chữ “another population” của prereg, nên phải ghi docs/DECISIONS.md kèm addendum. |
| [nhỏ] bản ghi lân cận chưa đủ (EpiPen 0,3 mg, TT51 a/c/d/e) | **Đã sửa** cùng lúc với mục CHẶN. |
| [nhỏ] -02 thiếu khóa loại thức ăn | **Đã sửa:** thêm `required_terms.food`. Thử phản chứng (bỏ “lạc (đậu phộng)”/“peanuts”) thì QC báo lỗi. |
| [nhỏ] QC không nhận phủ định; EN dose thiếu “IM” | Không sửa được trong dữ liệu (đây là mã `qgen.qc`). Đã ghi lưu ý vào notes của bản nháp. Câu hiện tại không bị ảnh hưởng. |
| [nhỏ] conflict_family lệch quy tắc cơ học | **Đã sửa:** -01 = `fam_19d7210de9`, -05 = `fam_e3d33e8a2e` (tính bằng `family_id`), nên thành hai nhóm. Tên đặt tay cũ ghi ở notes. |
| Nhãn 3 (bản cũ) | Không thử được: không mẩu nào có giá trị bản cũ, vì TT08/1999 chưa có bản chính thức trong kho. |
| S5 đoạn A3 OCR | Vẫn **còn treo** (người điều phối). Đoạn A3 -01/-05 nay có cờ `passage_has_alt_value = neighbour`. Đây là cờ để kiểm tay trước đóng băng, không phải lỗi QC. |
| `context_checked` = pending (-01, -05) | Việc của người dùng ở bước kiểm ngữ cảnh. Chưa đặt. |
