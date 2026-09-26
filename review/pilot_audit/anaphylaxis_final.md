# HG1.2 — Kiểm toán tự động, chủ đề anaphylaxis: phán quyết trọng tài

Người kiểm: **AI (Claude)**, gồm 2 kiểm toán viên độc lập A, B và trọng tài. **Không phải người, không phải bác sĩ.** Ngày 26/9/2026. Không đọc `data/runs/`.

Phạm vi: checklist chỉ có một mẩu `P-anaphylaxis-` là **P-anaphylaxis-03**. Hai mẩu -01 và -02 đã bị pilot_merge loại có chủ đích từ trước (trùng P-anaphylaxis_ocr-03/-04), nên không kiểm ở đây.

| Mẩu | (a) nguyên văn | (b) giá trị | (c) quần thể | (d) nước ngoài | A/B đồng ý | Phán quyết | Loại? |
|---|---|---|---|---|---|---|---|
| P-anaphylaxis-03 | pass | pass | pass | pass | 4/4 | **fix** (đã sửa, không đổi giá trị) | không |

**Tổng:** 0 ok · 1 đã sửa · 0 loại · 0 chưa rõ.

## Bằng chứng chính (trọng tài tự so lại)
- **(a)** Ảnh TT51 trang PDF 9: «a) Trẻ sơ sinh hoặc trẻ < 10kg: 0,2ml (tương đương 1/5 ống).» khớp span từng ký tự.
- **(b)** Các giá trị Bộ Y tế đều khớp ảnh trang:
  - 200 µg: TT51 trang 9.
  - 1/5–1/3 ống = 200–333,3 µg: TT51 trang 20, ô «TIÊM BẮP». Lớp chữ OCR ghi "TIEM BAP". Cùng giá trị có ở trang 19.
  - 0,01 mg/kg = 60 µg: 3312/2015 trang PDF 106 và 3942/2014 trang PDF 13. Trang 13 của 3942 có số in 8.
- **(c)** Câu hỏi VI/EN khớp quần thể của mẩu: 4 tháng, 6 kg (< 10 kg), độ II–III, sau tiêm kháng sinh, tiêm bắp, ống 1 mg/1 ml, tại cơ sở y tế, liều đầu tiên. Áp mặc định A.5 (DR8 không phụ thuộc nguyên nhân) không thêm giá trị nào:
  - 3942 tr.77 (côn trùng) cũng là 0,01 mg/kg, trùng giá trị đã có.
  - 3942 tr.48 (thức ăn) không có mức cho trẻ < 10 kg.
  - 3312 tr.81 (ong đốt) ghi 0,3 ml **TDD** (tiêm dưới da), khác đường tiêm của mẩu.
  - 3610 là liều không nêu tuổi hoặc liều người lớn. Theo (a), đây là quần thể lân cận, không vào tập giá trị của mẩu.
- **(d)** Các nguồn nước ngoài được mở trên bản đệm, sha khớp:
  - RCUK 2021, trang PDF 29, dòng "< 6 months": 100–150 µg.
  - WHO Pocket Book 2013, trang PDF 133: 0,15 ml 1:1000 = 150 µg.
  - WAO 2020 và AAAAI/ACAAI: 0,01 mg/kg (A và B cùng xác nhận). Bản đệm AAAAI/ACAAI là bản in trước 2023. Crossref xác nhận bản in chính thức là 2024;132(2):124–176.

## Thay đổi dữ liệu (`data/interim/pilot/anaphylaxis.jsonl`, chỉ mẩu -03)
Chỉ sửa ghi chú và nguồn gốc. Không đổi giá trị, span, trang, quần thể, dung sai, trạng thái xung đột hay mồi.
- `dr8_sources[0]`:
  - thêm `image_text` ghi "TIÊM BẮP" theo ảnh; span vẫn giữ "TIEM BAP" theo lớp chữ để verify_span qua;
  - thêm `ocr_note`;
  - thêm vị trí cùng giá trị ở trang 19.
- `dr8_sources[1]`: thêm `printed_page` 106 và các vị trí cùng giá trị 10 µg/kg ở 3312 tr.29/30/32/55.
- `dr8_sources[2]`: thêm `printed_page` 8, `page_note` và `manifest_note`.
- `vn[1].text`, `vn[2].text`: ghi rõ số trang PDF và số trang in.
- `foreign[US].locator`: ghi bản đệm là bản in trước, kèm DOI.
- Nối ghi chú vào `ocr_visual_check` và `dr8_not_applied`. Thêm `decision_default` (A.5) và `audit_fix`.

Tự kiểm bằng `pilot_merge --only anaphylaxis`: vẫn giữ 1 mẩu (conflict), dung sai 20, mồi rỗng. Danh sách loại giống hệt lượt chạy trước khi sửa. verify_span và schema đều OK. File gốc đã sao lưu ở `scratchpad/audit/anaphylaxis_before.jsonl`.

## Đề xuất ngoài mẩu (chưa làm)
1. **Đoạn oracle A3** (`data/interim/pilot_passages.jsonl`, P-anaphylaxis-03#A3) là chữ OCR có lỗi, đã xác nhận: "Img" (đúng là "1mg"), "1⁄2 - ]" (đúng là "1/2 - 1 ống"), dấu ">" (đúng là "≥"), "phúVlần", "on dinh", "nước cat". Cần sửa theo ảnh trang 9 trước khi đóng băng bộ v1, và không xem đầu ra mô hình khi sửa.
2. **Manifest:** thêm dòng cho QĐ 3942/2014. Giá trị 60 µg vẫn có nguồn hiện hành là 3312/2015.
3. **Cho HG3.9 (bác sĩ thật):**
   - dải 1/5–1/3 ống của Phụ lục X áp cho trẻ 6 kg;
   - áp DR8 từ văn bản viết cho "sốc phản vệ" vào phản vệ độ II;
   - 200 µg/6 kg ≈ 33 µg/kg.
