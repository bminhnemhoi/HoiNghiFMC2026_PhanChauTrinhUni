# Phản biện độc lập — câu hỏi thí điểm chủ đề dengue

- Người phản biện: agent AI đóng vai rev-clinician + rev-methods (**không phải bác sĩ thật**; mọi nhận định lâm sàng cần bác sĩ xác nhận ở HG4.2).
- Ngày: 2026-09-26. Đầu vào: `dengue.jsonl` (bản nháp), `pilot_atoms.jsonl` (P-dengue-01..06, 08..10; không có 07), `dengue_q.jsonl`, `dengue_p.jsonl`, `dengue_qc.csv`, đề cương §1.2/§3.5/§4.2–4.5/§5.7, SKILL question-generation, `configs/conditions.yaml`, `src/vnsoc/qgen/*.py`, `src/vnsoc/run/prompts.py`, `src/vnsoc/grade.py`, `src/vnsoc/schemas.py`. Văn bản gốc 2760/2023 được đối chiếu lại bằng `page_text` (p.9, 12, 14, 15, 16, 18, 28, 30, 38, 46, 50).
- Chống rò rỉ: KHÔNG xem đầu ra của mô hình nào được kiểm tra. Mọi câu trả lời dùng để thử bộ chấm dưới đây do người phản biện tự viết.
- Kiểm bằng mã: chạy lại `vnsoc.qgen.build --only-drafted` trên bản nháp hiện tại (34 câu, 3 mục QC lỗi — đúng như người viết báo). Các sửa đề xuất ở bản nháp cho mẩu 01, 02, 04 và 06 được chạy thử trong scratchpad, không ghi vào dự án. Kết quả: 34 câu, vẫn chỉ 3 mục QC lỗi, đều do dữ liệu mẩu ("mẩu không có mồi" của 05, 06, 08); các sửa đề xuất không tạo lỗi QC mới.

## Tổng hợp

| atom_id | verdict | Ai sửa | Lý do chính |
| --- | --- | --- | --- |
| P-dengue-01 | **fix** | bản nháp (filler) + mẩu | Filler do mã sinh là "27,5–32,5 ml/kg/giờ": số lẻ lộ vai trò. Khoảng WHO 5–10 chứa 10 ml/kg/giờ, là bước 2 của chính Bộ Y tế, nên nhầm bước bị chấm "trùng nước ngoài" |
| P-dengue-02 | **fix** | bản nháp (câu + filler) + mẩu | "Bước tiếp theo" chưa tách bước 2 (10) khỏi các bước giảm dần 6 → 3 → 1,5 của Bộ Y tế. WHO 5–7 chứa 6 của Bộ Y tế; filler 1–3 phủ 3 và 1,5 của Bộ Y tế |
| P-dengue-03 | **fix** | mã (hiển thị trắc nghiệm) | Câu ngắn đạt. Trắc nghiệm hiển thị nguyên văn `text`: lộ "(mồi)", "(khuyến cáo có điều kiện)"; bản EN có phương án tiếng Việt |
| P-dengue-04 | **fix** | mã (hiển thị trắc nghiệm) + bản nháp (filler) | Câu ngắn đạt. Trắc nghiệm có phương án "**WHO** gợi ý dùng…", "(mồi)", phương án Bộ Y tế dài và lộ "chỉ dùng paracetamol"; bản EN có phương án tiếng Việt |
| P-dengue-05 | **fix** | mẩu/mã (quyết định trắc nghiệm) | Câu ngắn đạt. Trắc nghiệm lệch phiên bản không dựng được vì mẩu không có mồi; dung sai 22,5 phút làm mồi < 37,5 phút bị chấm là đúng Bộ Y tế |
| P-dengue-06 | **fix** | bản nháp (câu ngắn) + mẩu/mã (trắc nghiệm) | "Có dùng…/should gelatin be used" là câu hỏi chuẩn tắc, trong khi Bộ Y tế chỉ nói "có thể thay thế". Câu trả lời "Không, ưu tiên HES 130" bị chấm **nhãn 3 (lệch phiên bản) sai**. Trắc nghiệm nhị phân không có nước ngoài hay mồi |
| P-dengue-08 | **pass** | mã (bỏ trắc nghiệm) | Câu ngắn đạt. Trắc nghiệm vô nghĩa vì bản cũ = Bộ Y tế = WHO; mã cần miễn trắc nghiệm khi giá trị bản cũ nằm trong tập Bộ Y tế |
| P-dengue-09 | **pass** | — | Ghi chú: đoạn A3 có dấu chữ ký số |
| P-dengue-10 | **pass** | — | Ghi chú: sơ đồ 2760 (p.46, p.50) viết "HA kẹt 25 mmHg: xử trí như sốc", nên "25" là giá trị Bộ Y tế lân cận (bác sĩ HG xem) |

Tổng: **pass 3 / fix 6 / drop 0**.

- Không mẩu nào phải loại vì mơ hồ quần thể. Với quần thể đã nêu, cả 9 câu ngắn đều có **một** đáp án Bộ Y tế, và không giá trị nước ngoài xung đột nào cũng đúng theo Bộ Y tế.
- Không câu nào (ngắn hay câu dẫn trắc nghiệm) nhắc Việt Nam, Bộ Y tế, WHO, Mỹ hay số quyết định. Không câu nào chứa đáp án hay giá trị nước ngoài/mồi/bản cũ. Mọi câu ≤ 60 từ, có đơn vị mong đợi (num), và bản EN trung thành về số, đơn vị, phủ định và quần thể.
- Vấn đề nằm ở **phương án trắc nghiệm** (mã hiển thị và filler) và ở **cách chấm** các giá trị Bộ Y tế lân cận (dữ liệu mẩu).

### Vấn đề nghiêm trọng (xếp theo mức độ)

1. **[Chặn, mã — cả bộ] Trắc nghiệm kiểu `cat` hiển thị nguyên văn `ValueItem.text`.**
   - `render.render_value` với `value_kind == "cat"` trả về `item.get("text") or item["label"]`, không có bản EN và không lọc chú thích nội bộ. Kết quả trong `dengue_q.jsonl` (8 câu: 03 và 04 × VI/EN × 2 thứ tự):
     - phương án mồi mang chữ **"(mồi)"**: "albumin 5% (mồi)", "chỉ dùng khi không đáp ứng paracetamol (mồi)";
     - phương án nước ngoài **nêu tên nguồn**: "WHO gợi ý dùng metamizol (dipyrone) … (khuyến cáo có điều kiện)". Ở A0 điều này phá tính trung tính. Ở A1, mô hình được bảo "theo Bộ Y tế" chỉ cần loại phương án có chữ WHO, nên P(nước ngoài) bị kéo xuống và phép so với mồi lệch về phía **không** ủng hộ H1;
     - phương án Bộ Y tế **khác hẳn về độ dài và độ cụ thể**: "cao phân tử (dextran/HES) 10–15 ml/kg/giờ" là phương án duy nhất có liều; "Không dùng analgin (metamizol); chỉ dùng paracetamol đơn chất" lộ thêm thông tin;
     - **bản EN hiển thị phương án tiếng Việt**: `P-dengue-03|mcq|en|*` và `P-dengue-04|mcq|en|*`.
   - QC không bắt được lỗi này vì `build_all` chỉ chạy `leak_issues` trên câu dẫn, không kiểm phương án. Cột `ok=True` của 8 câu này trong `dengue_qc.csv` vì vậy **không đáng tin**.
   - **Không được dùng 8 câu này trong lượt chạy thí điểm** cho tới khi sửa mã.
   - Hiện dengue là chủ đề duy nhất có trắc nghiệm `cat`, nhưng lỗi sẽ lặp lại ở mọi mẩu `cat` của bộ đầy đủ.
   - Đề xuất (người giữ mã quyết định; phản biện không sửa `src/`):
     - (a) thêm bảng hiển thị theo nhãn, hai ngôn ngữ, ví dụ trường mẩu `cat_display: {label: {vi, en}}`, và cho filler `cat` mang `{"label", "vi", "en"}`;
     - (b) `render_value` cho `cat` dùng bảng này và báo lỗi nếu thiếu;
     - (c) thêm QC phương án: không chứa tên nguồn hay vai trò (`WHO|CDC|NICE|ESC|Bộ Y tế|BYT|mồi|decoy|khuyến cáo`); phương án EN không có dấu tiếng Việt; tỉ lệ độ dài dài nhất/ngắn nhất ≤ khoảng 2.

   Văn bản hiển thị đề xuất cho 03 và 04 nằm trong mục từng mẩu bên dưới.

2. **[Phương pháp, dữ liệu mẩu — H1] Giá trị nước ngoài của 01/02 chứa giá trị Bộ Y tế ở bước lân cận, và bộ chấm không biết điều này.**
   - 2760 p.28 ghi phác đồ sốc người lớn là 15 → 10 (×2 giờ) → 6 → 3 → 1,5 ml/kg/giờ. WHO 5–10 (mẩu 01) chứa 10 và 6; WHO 5–7 (mẩu 02) chứa 6.
   - Thử bộ chấm bằng câu trả lời tự viết:
     - 01: "ĐÁP ÁN: 10 ml/kg/giờ" → **nhãn 4 (trùng WHO)**;
     - 02: "ĐÁP ÁN: 6 ml/kg/giờ" → **nhãn 4 (trùng WHO)**.
   - Như vậy, một mô hình **nhớ đúng phác đồ Bộ Y tế nhưng nhầm bước** bị tính là "trùng chuẩn nước ngoài". Sai lệch này **thiên về phía ủng hộ H1** (anti-conservative).
   - Chiều ngược lại: mồi 20–25 (01) chứa 20 ml/kg/giờ, là giờ đầu của trẻ em/thiếu niên 13–16 tuổi theo Bộ Y tế; mồi 13–15 (02) chứa 15, là bước 1 của chính phác đồ. Nhầm bước hay nhầm quần thể vì vậy cũng làm tăng P(mồi), tức sai lệch bảo thủ.
   - Hai lệch không triệt tiêu nhau một cách kiểm soát được.
   - `Atom.moh_neighbour` có trong schema nhưng: các mẩu dengue chỉ ghi `extraction.neighbor_values` (01 thiếu 10/6/3/1,5 người lớn; 02 thiếu 6/3/1,5); `grade_short` không dùng `moh_neighbour` (chỉ `passage_alt_values` dùng).
   - Đề xuất:
     - (a) điền `moh_neighbour` cho 01 (10, 6, 3, 1,5 ml/kg/giờ người lớn; 20 ml/kg/giờ trẻ em/thiếu niên) và 02 (15, 6, 3, 1,5);
     - (b) đăng ký trước một phân tích độ nhạy: câu trả lời trùng giá trị lân cận Bộ Y tế được tách khỏi nhãn 4 và khỏi "trùng mồi". Hoặc xếp 01/02 vào "không phân biệt được nguồn" theo §1.2 nếu HG thấy chồng lấn quá lớn;
     - (c) nếu phải cắt còn một mẩu trong họ `dengue_adult_compensated_shock_crystalloid_rate_who` thì giữ 01 (bỏ 02), như ghi chú mẩu đã nêu.
   - Cách diễn đạt câu hỏi (giờ đầu / ngay sau giờ đầu) giảm nhưng không loại được nhầm bước.

3. **[Dữ liệu mẩu / quy tắc mã — trắc nghiệm] 3 mục QC lỗi "mẩu không có mồi" không sửa được ở bản nháp.** Mỗi mẩu cần một quyết định khác nhau:
   - **05** (lệch phiên bản 15 → 60 phút, nước ngoài trùng Bộ Y tế): trắc nghiệm có ý nghĩa cho RQ lệch phiên bản nhưng cần mồi + filler.
     - Dung sai 22,5 phút làm mọi mồi hay filler trong (0; 37,5) phút bị chấm là đúng Bộ Y tế (thử: "ĐÁP ÁN: 30 phút" → nhãn 2). Mồi phải ≥ 37,5 phút và cách 60 đủ xa (ví dụ 120 phút), nên không đối xứng quanh giá trị Bộ Y tế.
     - Đề xuất: người giữ `counterpart-matching` chọn một trong hai: (a) thêm mồi, ghi `decoy_rule` riêng cho mẩu lệch phiên bản; (b) miễn trắc nghiệm cho mẩu lệch phiên bản không có xung đột nước ngoài và ghi vào DECISIONS.md.
   - **06** (nhị phân: được dùng / không dùng; không có nước ngoài): trắc nghiệm 4 phương án cho câu có/không phải bịa 2 nhãn. Đề xuất miễn trắc nghiệm (hoặc cho phép trắc nghiệm 2 phương án nếu đề cương muốn).
   - **08** (bản cũ = Bộ Y tế = WHO): trắc nghiệm vô nghĩa. Đề xuất sửa quy tắc ở `build_all`: chỉ bắt buộc trắc nghiệm khi `conflict_status == "conflict"` **hoặc** có giá trị bản cũ nằm **ngoài** tập Bộ Y tế (`_gap > 0`).

   Nếu áp dụng quy tắc này, 08 hết lỗi; 05 và 06 vẫn cần quyết định.

4. **[Bản nháp — nhãn lệch phiên bản giả] Mẩu 06 hỏi dạng chuẩn tắc.**
   - "Có dùng gelatin… hay không" / "should gelatin be used" mời mô hình chọn giữa HES 130 và gelatin.
   - Thử: "ĐÁP ÁN: Không, nên ưu tiên HES 130 6%" → **nhãn 3 (lệch phiên bản)**. Câu trả lời này không đến từ bản 3705 mà từ việc hiểu câu hỏi theo nghĩa "có nên".
   - Sửa thành câu hỏi về **sự cho phép** (xem mục 06). Câu sửa đã chạy QC sạch.

---

## Nhận xét từng mẩu

Ký hiệu 6 tiêu chí: (1) đáp án Bộ Y tế duy nhất và giá trị nước ngoài không "cũng đúng"; (2) không lộ đáp án hay nguồn/quốc gia; (3) EN trung thành về nghĩa; (4) diễn đạt tự nhiên, bác sĩ Việt Nam hiểu ngay; (5) trắc nghiệm hiển thị hợp lệ; (6) đơn vị mong đợi rõ.

### P-dengue-01 — verdict: **fix** (bản nháp: filler; mẩu: `moh_neighbour`)

- (1) Đạt.
  - Đáp án Bộ Y tế: 15 ml/kg/giờ (2760 C.2.1.2, p.28).
  - Quần thể loại được mọi nhánh khác của Bộ Y tế: người lớn, sốc còn bù không phải sốc nặng (loại C.2.2 bolus 15 phút), vào viện vì sốc và chưa truyền dịch (loại nhánh B2 → cao phân tử, p.15), BMI < 25 (cân nặng thực).
  - WHO 5–10 (sốc còn bù, người lớn) không đúng theo Bộ Y tế cho quần thể này.
  - Ghi chú biên tuổi: 2760 vừa dùng "người lớn (≥ 16 tuổi)" vừa có "trẻ thiếu niên 13 - 16 tuổi" (p.18, Phụ lục 11 p.50, giờ đầu 20 ml/kg/giờ). Người đúng 16 tuổi thuộc cả hai nhóm, nên mồi 20–25 "cũng đúng" về lý thuyết cho riêng trường hợp này. Không sửa câu (quy tắc giữ nguyên số quần thể; mô hình không suy luận ở biên), nhưng bác sĩ HG ghi nhận.
- (2) Đạt: không có số tốc độ nào; "giờ đầu" không ghi thành số.
- (3) Đạt: "nhập cấp cứu" = "admitted to the emergency department"; "HA kẹt" = "narrow pulse pressure".
- (4) Đạt; "HA" viết tắt thông dụng.
- (6) Đạt: (ml/kg/giờ).
- (5) Chưa đạt:
  - Phương án hiển thị: 5–10 (WHO) / 15 (Bộ Y tế) / 20–25 (mồi) / **27,5–32,5 (filler, `rule_filler`)**. Cùng đơn vị, không phương án nào đúng theo Bộ Y tế cho người lớn.
  - Filler có số lẻ ",5" mà không hướng dẫn nào viết, nên phương án tự lộ là "nhân tạo" (cùng lỗi phản biện immunization đã nêu ở P-immunization-01).
  - Phương án WHO 5–10 chứa 10 ml/kg/giờ là bước 2 của Bộ Y tế (xem vấn đề nghiêm trọng 2).
- **Sửa cụ thể (bản nháp):** `"filler": {"lo": 30, "hi": 30, "unit": "ml/kg/h"}`.
  - Giữ đúng tâm 30 của filler mã sinh, đọc tự nhiên.
  - 30 ml/kg/giờ không có trong Bộ Y tế (người lớn: 15, 10, 6, 3, 1,5; trẻ em/thiếu niên 20), WHO 2009/2012 (người lớn 5–10, 5–7, 3–5, 2–3) hay CDC (bolus 20 mL/kg).
  - Đã chạy thử: trắc nghiệm hiển thị "20–25 / 30 / 15 / 5–10 ml/kg/giờ", QC sạch.
- **Sửa cụ thể (mẩu):** điền `moh_neighbour` (10, 6, 3, 1,5 ml/kg/giờ người lớn — 2760 p.28; 20 ml/kg/giờ trẻ em/thiếu niên — p.15, p.18/50).
- Đoạn A3 (p.28) chứa 10 và 6 ml/kg/giờ (bước sau), nên bị gắn cờ `foreign:WHO_global`. Loại khỏi phân tích H3 chính theo phân tích độ nhạy đã đăng ký; kiểm tay trước khi đóng băng.

### P-dengue-02 — verdict: **fix** (bản nháp: câu + filler; mẩu: `moh_neighbour`)

- (1) Đạt nhưng mong manh.
  - Đáp án Bộ Y tế: 10 ml/kg/giờ × 2 giờ (p.28, bước ngay sau giờ đầu khi cải thiện). WHO 5–7 không đúng cho bước này.
  - Tuy vậy 2760 viết tiếp: "Nếu người bệnh cải thiện lâm sàng và hematocrit giảm, giảm tốc độ … 6 ml/kg/giờ trong 2 giờ, sau đó 3 ml/kg/giờ trong 5 - 7 giờ, sau đó 1,5 ml/kg/giờ". "Bước tiếp theo" chưa neo rõ vào mốc thời gian, và 6 (Bộ Y tế, bước 3) nằm trong WHO 5–7.
- (2) Đạt: tốc độ giờ đầu đã được bỏ đúng cách (15 thuộc mồi 13–15).
- (3), (4), (6) Đạt. Riêng VI "bước tiếp theo truyền dịch này tốc độ bao nhiêu" hơi cụt; bản sửa tự nhiên hơn.
- (5) Chưa đạt:
  - Phương án hiển thị: 10 / 5–7 / **1–3 (filler, `rule_filler`)** / 13–15.
  - Filler 1–3 chứa 3 và 1,5 ml/kg/giờ của chính Bộ Y tế (bước 4–5, cùng quần thể) và 2–3 của WHO. Như vậy nó vi phạm SKILL bước 3 ("nhiễu hợp lý không thuộc nguồn nào").
  - Với câu dẫn "ngay sau giờ đầu", filler này không đúng theo Bộ Y tế, nhưng là giá trị thật của phác đồ.
- **Sửa cụ thể (bản nháp, đã chạy QC sạch; VI 59 từ, EN 57 từ):**
  - `short_vi`: "Ở người lớn (≥ 16 tuổi) nhập viện vì sốc sốt xuất huyết Dengue còn bù (chưa phải sốc nặng), đã truyền Ringer lactate hoặc NaCl 0,9% trong giờ đầu chống sốc, nay cải thiện (mạch giảm, HA bình thường, hiệu áp > 20 mmHg), ngay sau giờ đầu cần truyền tiếp dịch này tốc độ bao nhiêu (ml/kg/giờ)?"
  - `short_en`: "In an adult (≥ 16 years) admitted with compensated dengue shock (not profound shock) who received Ringer's lactate or 0.9% NaCl during the first hour of shock resuscitation and has now improved clinically (slower pulse, normal blood pressure, pulse pressure > 20 mmHg), at what rate should this fluid be continued immediately after the first hour (mL/kg/hour)?"
  - `mcq_stem_vi` / `mcq_stem_en`: tương tự, kết thúc "…ngay sau giờ đầu cần truyền tiếp dịch này với tốc độ nào?" / "…at which rate should this fluid be continued immediately after the first hour?"
  - `"filler": {"lo": 12, "hi": 12, "unit": "ml/kg/h"}`: không có trong Bộ Y tế, WHO người lớn/trẻ em hay CDC; khác 10 là 2 > dung sai 1,5; khác mồi 13–15. Nhược điểm: gần hai phương án khác. Nếu HG thấy không hợp lý, có thể giữ 1–3 và ghi rõ trong báo cáo, nhưng không có filler "sạch" nào trong khoảng 1,5–10 vì mọi giá trị ở đó đều là một bước của Bộ Y tế hoặc WHO.
- **Sửa cụ thể (mẩu):** điền `moh_neighbour` (15, 6, 3, 1,5 ml/kg/giờ — 2760 p.28; 15 ml/kg/giờ bước 2 sốc nặng — p.30).
- Đoạn A3 bị gắn cờ `decoy;foreign:WHO_global` (chứa 15 và 6), nên cần kiểm tay.
- Cùng họ xung đột với 01 (không độc lập).

### P-dengue-03 — verdict: **fix** (mã hiển thị trắc nghiệm; câu ngắn đạt)

- (1) Đạt, có cảnh báo cho HG.
  - Bối cảnh B2 (đang truyền dịch vì dấu hiệu cảnh báo, chưa bolus, chuyển sốc còn bù, Hct tăng) cho đúng một đáp án Bộ Y tế: cao phân tử (2760 p.15, Phụ lục 6).
  - Dịch tinh thể (WHO 2009/2012/2025, CDC) không đúng cho **đúng quần thể này** theo Bộ Y tế.
  - "Chưa nhận bolus nào" loại đúng ngoại lệ WHO 2012 (ưu tiên dịch keo sau bolus dịch tinh thể).
  - Cảnh báo: 2760 **tự mâu thuẫn một phần**. Người lớn vào viện vì sốc dùng dịch tinh thể trước (C.2.1.2, p.28), nên bác sĩ hoặc mô hình trả lời "dịch tinh thể" có thể đang dựa vào chính Bộ Y tế (nhánh khác). Câu hỏi đã giữ đúng bối cảnh B2; bác sĩ HG cần xác nhận mẩu này còn là "xung đột sạch".
- (2) Đạt: không nêu tên dịch đang truyền (tránh khớp nhãn tinh thể).
- (3), (4) Đạt.
- (6) Không áp dụng (cat).
- (5) **Không đạt:**
  - Hiển thị: "cao phân tử (dextran/HES) 10–15 ml/kg/giờ" / "dịch tinh thể thay vì dịch keo (khuyến cáo có điều kiện)" / "huyết tương tươi đông lạnh" / "albumin 5% (mồi)".
  - Có đủ các lỗi của vấn đề nghiêm trọng 1: lộ vai trò mồi, cụm GRADE của WHO, chỉ phương án Bộ Y tế có liều, bản EN tiếng Việt.
  - Thêm: "albumin 5%" là dịch keo, nên nếu phương án Bộ Y tế ghi chung "cao phân tử/dịch keo" thì albumin thành tập con của nó. Phương án Bộ Y tế phải ghi rõ **tổng hợp (dextran hoặc HES)**.
  - Filler "huyết tương tươi đông lạnh" chấp nhận được: có thật, không nguồn nào khuyến cáo làm liều chống sốc đầu; dễ loại, nhưng filler không phải mồi.
- **Sửa cụ thể (mã/mẩu — văn bản hiển thị đề xuất):**

  | nhãn | vai trò | VI | EN |
  | --- | --- | --- | --- |
  | colloid | vn | Dung dịch cao phân tử tổng hợp (dextran hoặc HES) | Synthetic colloid (dextran or HES) |
  | crystalloid | foreign | Dịch tinh thể đẳng trương (Ringer lactate hoặc NaCl 0,9%) | Isotonic crystalloid (Ringer's lactate or 0.9% NaCl) |
  | albumin | decoy | Dung dịch albumin 5% | 5% albumin solution |
  | (filler) | filler | Huyết tương tươi đông lạnh | Fresh frozen plasma |

- Đoạn A3 (p.15) mở đầu bằng mảnh "14 24 giờ." (số trang + đuôi câu trang trước) và chứa danh mục dịch tinh thể của phần trẻ em (C1.1.1). Đã bị gắn cờ `foreign:US;foreign:WHO_global`, cần kiểm tay.

### P-dengue-04 — verdict: **fix** (mã hiển thị trắc nghiệm; bản nháp: filler; câu ngắn đạt)

- (1) Đạt.
  - Bộ Y tế: không dùng analgin (p.12, mọi người bệnh SXHD). WHO 2025: gợi ý dùng (có điều kiện). "Có" không đúng theo Bộ Y tế.
- (2) Đạt: tránh khéo mọi cụm khớp `cat_options`.
- (3) Đạt: "có nên dùng" = "should … be used".
- (4) Đạt.
- (6) (có/không) rõ.
- Ghi chú diễn giải: metamizol không được phép lưu hành ở Mỹ/Anh. Ở A0 tiếng Anh, câu trả lời "No" có thể phản ánh tình trạng cấp phép ở Mỹ chứ không phải kiến thức Bộ Y tế, nên "đúng" ở A0-EN mẩu này nên đọc thận trọng. WHO 2025 (7/2025) có thể nằm sau mốc dữ liệu huấn luyện của một số mô hình.
- (5) **Không đạt:**
  - Hiển thị: "**WHO** gợi ý dùng metamizol (dipyrone) cho đau và/hoặc sốt (khuyến cáo có điều kiện)" / "Không dùng analgin (metamizol); chỉ dùng paracetamol đơn chất" / "chỉ dùng khi không đáp ứng paracetamol (**mồi**)" / "chỉ dùng cho người lớn, không dùng cho trẻ em".
  - Lộ nguồn, lộ vai trò, phương án Bộ Y tế dài và kèm "chỉ dùng paracetamol", bản EN tiếng Việt.
  - Filler giới hạn tuổi mâu thuẫn với câu dẫn "ở bất kỳ lứa tuổi nào", nên dễ loại.
- **Sửa cụ thể (bản nháp, đã chạy QC sạch):** `"filler": {"label": "dùng xen kẽ với paracetamol"}`. Đây là thực hành có thật (xen kẽ thuốc hạ sốt) nhưng không nguồn nào trong mẩu khuyến cáo cho SXHD, và không mâu thuẫn câu dẫn.
- **Sửa cụ thể (mã/mẩu — văn bản hiển thị đề xuất):**

  | nhãn | vai trò | VI | EN |
  | --- | --- | --- | --- |
  | not_allowed | vn | Không dùng metamizol | Metamizole should not be used |
  | allowed | foreign | Có thể dùng metamizol để hạ sốt hoặc giảm đau | Metamizole may be used for fever or pain |
  | second_line_only | decoy | Chỉ dùng metamizol khi paracetamol không hiệu quả | Use metamizole only if paracetamol is ineffective |
  | (filler) | filler | Dùng metamizol xen kẽ với paracetamol | Alternate metamizole with paracetamol |

### P-dengue-05 — verdict: **fix** (mẩu/mã: quyết định trắc nghiệm; câu ngắn đạt)

- (1) Đạt.
  - Bộ Y tế 2760 C.2.2 (p.30): 15 ml/kg trong 15 phút. WHO/CDC 15 hay 15–30 phút là trùng (concordant). Bản cũ 3705: 60 phút (suy bằng phép tính).
  - "Sốc … nặng (mạch không bắt được, huyết áp không đo được)" + "nhập cấp cứu" khớp đúng điều kiện "nhập viện trong tình trạng sốc nặng".
- (2) Đạt về quy tắc. Ghi chú: "15 ml/kg" trong câu cùng số với đáp án "15 phút", nên mô hình có thể lặp lại số (neo số).
  - Giữ thể tích vì thời gian bolus phụ thuộc thể tích, và vì dung sai 22,5 phút làm 15/20/30 phút đều chấm đúng. Neo số chủ yếu ảnh hưởng tỉ lệ trả lời 60 phút (lệch phiên bản).
  - Ghi vào hạn chế; không sửa.
- (3), (4), (6) Đạt.
- (5) Không dựng được ("mẩu không có mồi"). Xem vấn đề nghiêm trọng 3: cần quyết định (a) thêm mồi ≥ 37,5 phút, hoặc (b) miễn trắc nghiệm cho mẩu lệch phiên bản không xung đột. Câu dẫn trắc nghiệm của người viết đã dùng được.
- Đoạn A3 (p.30) mở đầu giữa công thức cân nặng ("50,0 + 0,91 x (chiều cao…") do ranh giới trang, không phải do cắt câu. Đoạn này chứa "15ml/kg/giờ x 1 giờ" (bước sau), nên bị gắn cờ `superseded`, cần kiểm tay.

### P-dengue-06 — verdict: **fix** (bản nháp: câu ngắn; mẩu/mã: trắc nghiệm)

- (1) Đạt về quần thể: trẻ < 16 tuổi, sốc không cải thiện sau giờ đầu, Hct còn cao hoặc ≥ 40%, có chỉ định cao phân tử, **không có** Dextran 40/70 hay HES 200 6%. Đây đúng là điều kiện để 2760 p.16 cho "có thể thay thế bằng 6% HES 130 hoặc Gelatin".
- (4) Chưa đạt về **thể thức câu hỏi**:
  - "Có dùng gelatin … hay không" (VI) và "should gelatin be used" (EN) là câu chuẩn tắc, trong khi Bộ Y tế chỉ **cho phép** (ngang với HES 130, kèm theo dõi sát).
  - Câu trả lời hợp lý "Không, nên ưu tiên HES 130" bị chấm nhãn 3 (lệch phiên bản) dù không đến từ 3705 (đã thử bằng câu tự viết, VI và EN).
- (2), (3), (6) Đạt.
- **Sửa cụ thể (bản nháp, đã chạy QC sạch; VI 60 từ, EN 50 từ):**
  - `short_vi`: "Ở trẻ em (< 16 tuổi) nằm viện vì sốc sốt xuất huyết Dengue không cải thiện sau giờ đầu, hematocrit còn tăng cao hoặc ≥ 40%, có chỉ định truyền cao phân tử nhưng cơ sở không có Dextran 40, Dextran 70 hay HES 200 6%, có được phép dùng gelatin làm dung dịch cao phân tử không (có/không)?"
  - `short_en`: "In a child (< 16 years) hospitalised with dengue shock not improving after the first hour, haematocrit still high or ≥ 40%, with an indication for colloid infusion but no Dextran 40, Dextran 70 or 6% HES 200 available at the facility, is gelatin permitted as the colloid solution (yes/no)?"
  - Giữ nguyên `mcq_stem_vi/en` (bản dài hơn sẽ vượt 60 từ).
- (5) Không dựng được. Mẩu nhị phân không có nước ngoài hay mồi; đề xuất miễn trắc nghiệm (vấn đề nghiêm trọng 3).

### P-dengue-08 — verdict: **pass** (mã: miễn trắc nghiệm)

- (1) Đạt: 10–15 mg/kg/lần (p.12); WHO 2025 10–15, WHO 2012 10 (nằm trong tập Bộ Y tế). Hỏi đúng liều **mỗi lần**, không lẫn khoảng cách hay tổng liều/ngày.
- (2), (3), (4) Đạt.
- (6) (mg/kg/lần) rõ.
- (5) Trắc nghiệm vô nghĩa vì bản cũ = Bộ Y tế. Mục QC lỗi sẽ hết khi mã chỉ bắt buộc trắc nghiệm cho bản cũ **khác** Bộ Y tế (vấn đề nghiêm trọng 3). Không cần sửa bản nháp; giữ câu dẫn trong nháp không gây hại.

### P-dengue-09 — verdict: **pass**

- (1) Đạt: AST hoặc ALT ≥ 1000 U/L (Phụ lục 2 p.38). "Nặng do suy tạng gan" tách đúng khỏi dấu hiệu cảnh báo AST/ALT ≥ 400 U/L (cùng trang).
- (2), (3) Đạt.
- (6) (U/L) rõ.
- (4) Đạt; "(áp dụng cho mọi lứa tuổi)" hơi hành chính, có thể viết "ở cả trẻ em và người lớn". Không bắt buộc.
- Đoạn A3 kết thúc bằng dấu chữ ký số "syt_hochiminh_vt_Van thu SYT TP.Ho Chi Minh_04/07/2023 10:26:33 2760 04 7" (không ảnh hưởng chấm U/L). Nên cắt ở bước dựng đoạn A3 cho mọi văn bản có dấu này.

### P-dengue-10 — verdict: **pass**

- (1) Đạt: định nghĩa huyết áp kẹt ≤ 20 mmHg (p.9; Phụ lục 11 p.50 "kẹt ≤ 20 mmHg"). Trẻ em để WHO 2009/2012 áp dụng.
- (2), (4) Đạt.
- (6) (mmHg) rõ.
- Ghi chú cho HG:
  - Sơ đồ 2760 p.46 và p.50 viết "(*): Mạch nhanh, HA kẹt 25 mmHg: xử trí như sốc SXH Dengue"; p.14 viết "hiệu áp = 25 mmHg: điều trị như sốc".
  - Như vậy chính văn bản gọi 25 mmHg là "HA kẹt" trong bối cảnh xử trí. Câu trả lời "25 mmHg" bị chấm nhãn 5 (đã thử) dù có căn cứ trong Bộ Y tế.
  - Cụm "được định nghĩa là" trong câu hỏi là cách xử lý đúng. Đề xuất điền `moh_neighbour` (25 mmHg, p.14/46/50) để báo cáo riêng.
- (3) Đạt. Có thể làm tiếng Anh tự nhiên hơn (không bắt buộc): "…at or below what pulse pressure (systolic minus diastolic blood pressure) is the pulse pressure defined as narrowed (mmHg)?"

---

## Việc cần làm (theo người phụ trách)

- **question-writer (bản nháp `dengue.jsonl`):**
  - Thay 4 dòng 01, 02, 04, 06 theo các sửa ở trên. Bản đầy đủ đã chạy thử nằm ở scratchpad của phiên phản biện (`…/scratchpad/dengue_rev/dengue_rev.jsonl`).
  - Chạy lại `vnsoc.qgen.build --only-drafted`. Kết quả mong đợi vẫn là 3 mục lỗi dữ liệu cho tới khi các mục dưới được xử lý.
- **Người giữ mã (`src/vnsoc/qgen`):**
  - (i) hiển thị `cat` hai ngôn ngữ từ bảng nhãn + QC phương án (vấn đề 1);
  - (ii) chỉ bắt buộc trắc nghiệm khi `conflict` hoặc bản cũ ngoài tập Bộ Y tế (vấn đề 3);
  - (iii) cân nhắc làm tròn `rule_filler` về số nguyên hoặc số có trong thực hành, để khỏi phải viết filler tay (01; immunization-01).
- **counterpart-matching (mẩu):**
  - `moh_neighbour` cho 01, 02, 10;
  - bảng hiển thị `cat` cho 03, 04;
  - quyết định mồi hoặc miễn trắc nghiệm cho 05, 06.
- **HG / prereg:**
  - phân tích độ nhạy "trùng giá trị Bộ Y tế lân cận" cho H1 (vấn đề 2);
  - xác nhận của bác sĩ về mâu thuẫn nội tại 2760 (03), biên tuổi 16 (01), và "HA kẹt 25 mmHg" (10).

---

## Trạng thái sau vòng sửa qfix (26/9, agent atom-extractor + question-writer; không phải bác sĩ)

Kiểm bằng mã (lặp tới khi sạch): `pilot_merge --only dengue --no-checklist` giữ 9/9 mẩu, loại 0; `qgen.build --only-drafted` ra 30 câu (short 18, mcq 12), 0 mục QC không đạt, 6 mẩu bỏ trắc nghiệm có chủ đích; chấm thử 34 câu trả lời TỰ VIẾT (không phải đầu ra mô hình) và mọi chữ cái của 12 câu trắc nghiệm đều ra đúng nhãn. Sao lưu bản trước ở scratchpad phiên (`qfix/dengue_atoms_before.jsonl`, `qfix/dengue_drafts_before/`).

| Mục phản biện | Trạng thái |
| --- | --- |
| 1. Hiển thị trắc nghiệm `cat` (03, 04) | **Đã sửa**: mã render từ `option_text` + QC phương án; bản nháp 03/04 có `option_text` VI/EN, mỗi văn bản đọc lại bằng `cat_options` ra đúng nhãn vai trò; 8 câu trắc nghiệm 03/04 dùng được |
| 2. Giá trị Bộ Y tế lân cận (01, 02) | **Đã điền `moh_neighbour`** (nguyên văn 2760): 01 = 10/6/3/1,5 (p.28), 20 (p.18 thiếu niên, p.15 trẻ em); 02 = 15 (p.28 giờ đầu; p.30 sốc nặng), 6/3/1,5 (p.28). `neighbour_overlap` = True cho cả hai → `status_with_neighbours` = indistinguishable (phương án (b)). Bộ chấm KHÔNG đổi: "10 ml/kg/giờ" ở 01 và "6 ml/kg/giờ" ở 02 vẫn nhãn 4 → **chờ HG/prereg** chọn phân tích độ nhạy N1 hay loại khỏi phân tích chính |
| 2'. Mồi theo quy tắc khi có lân cận | 01: 20–25 chạm 20 → mirror_geom **28–32 ml/kg/giờ** (roundness_ok False). 02: 13–15 / 16–18 / 17–19 đều cách 15 < 3 → **không còn mồi** → bỏ trắc nghiệm, ngoài H1/H2 (DECISIONS 2026-09-26) |
| 3. Trắc nghiệm 05, 06, 08 | Mã mới bỏ có chủ đích (không mồi; 08 không có giá trị ngoài tập). 05/06 vẫn chờ HG nếu muốn trắc nghiệm lệch phiên bản |
| 4. 06 câu chuẩn tắc | Đã sửa ở vòng trước ("có được phép dùng") |
| 01 filler | Filler tay 30 bỏ (nằm trong mồi 28–32); filler theo quy tắc **43–48 ml/kg/giờ**. Mồi và filler đều "không tròn" cạnh 15 và 5–10 → người giữ mã xem (`_mirror` làm tròn nửa-chẵn 27,5→28, 32,5→32 rồi bỏ qua lưới tròn; `rule_filler` 2 chữ số có nghĩa) |
| 09 đoạn A3 dấu ký số | Đã hết (mã cắt) |
| 03 đoạn A3 mở đầu "14 24 giờ." | Còn (mã dựng đoạn A3), kiểm tay trước khi đóng băng |
| 10 "HA kẹt 25 mmHg" | Đã điền `moh_neighbour` 25 mmHg (p.14, p.46, p.50); "25 mmHg" vẫn nhãn 5 |
| population chứa ghi chú người trích (01, 02, 03, 10) | Đã rút gọn; ghi chú chuyển vào `extraction.notes` |
| Mồi cat 03/04 | `decoy_rule` = agent_proposed, bỏ "(mồi)" trong text; lý do ở `extraction.notes`; `decoy_plausible` để trống (HG3.5) |

Còn chờ người (bác sĩ HG): mâu thuẫn nội tại 2760 ở 03 (vào viện vì sốc → tinh thể; đang truyền vì cảnh báo → cao phân tử); biên tuổi 16 ở 01; albumin (mồi 03) có ở bối cảnh khác khe (C.2.3 albumin phối hợp khi sốc kéo dài, p.30) — nếu coi là lân cận thì phải đổi mồi.

---

## Trạng thái sau vòng sửa qfix 2 (26/9, theo kiểm độc lập rev-methods + rev-clinician — AI, không phải bác sĩ)

Kiểm bằng mã (lặp tới khi sạch): `pilot_merge --only dengue --no-checklist` giữ 9/9, loại 0; đầu ra giống từng byte `data/interim/pilot/dengue.jsonl` (sha256 f7585307…). Mồi, dung sai, trạng thái của cả 9 mẩu không đổi. `qgen.build --only-drafted`: 30 câu (short 18, mcq 12), 0 mục QC không đạt, 6 mẩu bỏ trắc nghiệm có chủ đích. Câu hỏi và đoạn A3 giống hệt vòng 1; chỉ cột `passage_has_alt_value` của `P-dengue-03#A3` thêm `neighbour`. Chấm thử: 139 câu TỰ VIẾT cho 03/04 (không phải đầu ra mô hình) → 0 sai nhãn (trước khi sửa 45 sai); 48 chữ cái của 12 câu trắc nghiệm → đúng vai trò. Script: scratchpad phiên `qfix/dengue_r2_cats.py`, `dengue_r2_fix_atoms.py`, `dengue_r2_fix_drafts.py`, `dengue_r2_cat_try.py`; sao lưu trước vòng 2: `qfix/dengue_atoms_before_round2.jsonl`, `qfix/dengue_drafts_before_round2/`.

| Mục kiểm độc lập | Trạng thái |
| --- | --- |
| 03 crystalloid bỏ sót cách viết (nhãn 6) | **Đã sửa**: 'dung dịch mặn đẳng trương' (chữ của 2760 C1.1.1), 'dịch đẳng trương', 'NaCl đẳng trương', 'saline', 'isotonic fluid(s)/solution', 'balanced salt/crystalloid', 'Hartmann', 'Plasma-Lyte', 'Sterofundin', 'natri clorid', 'sodium chloride' → nhãn 4. Colloid thêm Gelofusine, Voluven, Volulyte, Tetraspan, Haemaccel, HAES → nhãn 2 |
| 03 'dich keo' bắt 'dịch kéo dài' | **Đã sửa**: `dich keo(?!\s*dai)`; 'dịch kéo dài' → 6; 'Ringer lactate; tránh truyền dịch kéo dài' → 4 |
| Câu cat nhiều nhãn luôn ra 2 (mã/prereg) | **Giảm một phần ở dữ liệu, phần còn lại chờ quyết**. Không đọc nhãn colloid khi lần nhắc dịch keo DUY NHẤT bị phủ định ('không dùng/không phải/tránh/thay vì cao phân tử', 'not/no/avoid/without/instead of/rather than colloid') và câu có dịch tinh thể; hoặc khi dịch tinh thể nêu trước và dịch keo chỉ được nhắc kèm giới hạn ('only if refractory', 'chỉ khi kháng trị', 'not recommended'). Đã thử đối kháng: 21 câu đúng Bộ Y tế (có nhắc/phủ định dịch tinh thể, hoặc phủ định một loại dịch keo khác) vẫn nhãn 2. **Bác bỏ có chủ đích** cho 'Ringer lactate; nếu không đáp ứng chuyển cao phân tử' (vẫn 2): cùng dạng chữ nói đúng logic B2 của Bộ Y tế cho quần thể này (đang truyền dịch tinh thể duy trì, chuyển sốc → cao phân tử); ép thành 4 sẽ sinh nhãn 4 giả, nghiêng về H1. 'Ringer lactate hoặc cao phân tử' vẫn 2. Quy tắc chung (tương tự quy tắc 7 §6.3 cho cat, hoặc bộ tách LLM) là việc của mã + đăng ký trước |
| 03 câu chỉ nêu huyết tương tươi đông lạnh/truyền máu ra 6 | **Đã sửa**: nhãn không nguồn `blood_product` → nhãn 5 (giá trị không khớp nguồn). Không bắt 'huyết tương' trơn ('bù lượng huyết tương mất đi' vẫn 6). Phương án filler đọc ra `blood_product`, QC filler đạt; nhãn máy filler của bản nháp đổi thành `blood_product`. Người kiểm ghi 'truyền máu' → 6; vòng này chọn 5 vì là một giá trị (sai) chứ không phải từ chối |
| 03 mâu thuẫn nội tại 2760 | **Đã ghi `moh_neighbour`** (nguyên văn 2760 C.2.1.2, PDF p.28, span_on_page True): người lớn vào viện vì sốc → Ringer lactate/NaCl 0,9% giờ đầu (nhãn crystalloid). `neighbour_overlap` = True → `status_with_neighbours` = indistinguishable (phân tích độ nhạy N1). Bác sĩ HG vẫn cần xác nhận mẩu có còn là "xung đột sạch" ở phân tích chính |
| 04 lỗ hổng cat_options | **Đã sửa**: 'Not recommended', 'Metamizol không được khuyến cáo…', 'not advised' → 2; 'Được', 'metamizol dùng được' → 4; 'Không, trừ khi paracetamol không hiệu quả', 'No, unless paracetamol fails' → 5 có cờ mồi; 'Chỉ paracetamol được dùng; không dùng analgin' không còn đọc thêm nhãn allowed |
| Nhãn 3 | Không xảy ra ở 01/02/03/04/10: bản cũ 3705/2019 trùng giá trị Bộ Y tế, nên câu trả lời theo bản cũ được nhãn 2 (ưu tiên Bộ Y tế) |

Còn chờ người: (1) quy tắc chung cho câu cat nhiều nhãn (mã + addendum đăng ký trước); (2) bác sĩ HG: mâu thuẫn nội tại 2760 ở 03, biên tuổi 16 ở 01, albumin mồi 03 (albumin phối hợp C.2.3 p.30); (3) kiểm ngữ cảnh của sinh viên: `moh_scope` (03, 04), `context_checked`, `conflict_family` theo quy tắc cơ học, `decoy_plausible` (HG3.5) — `atom_flags check` báo 13 vấn đề trước đóng băng, đều thuộc nhóm này; (4) giá trị CDC ở 02 ('10mg/kg for 1-2 hrs', verified_by null) cần người đọc lại; (5) `data/interim/pilot_atoms.jsonl` chưa gộp lại (ngoài phạm vi vòng này).
