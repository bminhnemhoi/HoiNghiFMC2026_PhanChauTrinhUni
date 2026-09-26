# HG1.2 tự động: trọng tài chủ đề dm (đái tháo đường)

Ngày 26/9/2026. **Kiểm bởi AI (Claude), không phải người, không phải bác sĩ.** Kiểm toán viên A, B và trọng tài đều là AI.
Đầu vào: `dm_A.json`, `dm_B.json`. Kết quả máy đọc: `dm_final.json`.

**Kết quả: 5 ok, 3 đã sửa (fix, không đổi giá trị), 0 loại, 0 chưa rõ.**

A và B đồng thuận cả 4 tiêu chí ở cả 8 mẩu, không có fail hay uncertain. Trước khi sửa dữ liệu, trọng tài tự mở lại nguồn:
- WHO 2013: tr. PDF 4, 5, 36, 37;
- WHO/IDF 2006: tr. PDF 7, 9;
- ảnh 1470/2024: tr. PDF 13, 14;
- 5481/2020: tr. PDF 56.

Không đọc `data/runs/`.

| Mẩu | a | b | c | d | A/B | Chốt | Thay đổi |
|---|---|---|---|---|---|---|---|
| P-dm-01 | pass | pass | pass | pass | ok/ok | **ok** | — |
| P-dm-02 | pass | pass | pass | pass | ok/ok | **ok** | — |
| P-dm-03 | pass | pass | pass | pass | ok/ok | **ok** | — |
| P-dm-04 | pass | pass | pass | pass | ok/ok | **ok** | — (giữ cờ [concordant_by_union]) |
| P-dm-05 | pass | pass | pass | pass | ok/fix | **fix** | `vn[0].text`: 1470/2024 đã đối chiếu ảnh tr. PDF 13 (in 8), mục 1.2.2 |
| P-dm-06 | pass | pass | pass | pass | ok/ok | **fix** | `foreign[0].locator` WHO 2006: tr. 7 là Recommendation 1, tr. 9 là bảng |
| P-dm-08 | pass | pass | pass | pass | fix/fix | **fix** | `foreign[0].locator` WHO 2013: khuyến cáo **3** (tr. PDF 5 và 37), không phải khuyến cáo 2; ghi mặc định A.9 |
| P-dm-07 | pass | pass | pass | pass | ok/ok | **ok** | — |

## Chi tiết các thay đổi (`data/interim/pilot/dm.jsonl`)

Bản sao lưu nằm ở `scratchpad/audit/dm_before.jsonl`. Không thay đổi nào chạm tới giá trị, đơn vị, span, trang, quần thể, dung sai, mồi hay trạng thái xung đột; script sửa đã kiểm bất biến này.

- **P-dm-08.**
  - Khuyến cáo 2 của WHO 2013 là "Diabetes in pregnancy", ngưỡng FPG ≥ 7,0 mmol/L. Nó nằm ở phần tóm tắt tr. PDF 4 và mục 4.2 tr. PDF 36.
  - Khuyến cáo 3 là ĐTĐ thai kỳ, FPG 5,1–6,9 mmol/L (92–125 mg/dL). Nó nằm ở tr. PDF 5 và mục 4.3 tr. PDF 37.
  - Đã sửa locator. Giá trị 5,1 mmol/L / 92 mg/dL không đổi.
  - Thêm ghi chú: 5481/2020 tr. PDF 56 mục 2.3.1a "≥ 7 mmol/L" thuộc ĐTĐ mang thai, là khe khác nên không phải giá trị bị bỏ sót.
  - Áp mặc định HG1.2 mục A.9: **không** ghi WHO 1999.
- **P-dm-05.**
  - Thay ghi chú "chưa kiểm span" bằng vị trí đã đối chiếu ảnh. Ảnh ghi: tầm soát mọi thai phụ tuần 24–28 bằng nghiệm pháp 75 g, tức chỉ 1 bước.
  - OCR trang này sai chữ ("tằm soát", "chuyền hóa", "thai ky"). Vì vậy không ghi thành span để máy kiểm.
- **P-dm-06.** Locator WHO 2006 được tách rõ: tr. 7 là văn bản khuyến cáo, tr. 9 là bảng. Giá trị không đổi.

## Đề xuất loại

Không có.

## Không sửa dữ liệu, chỉ ghi lại

- **P-dm-01.** Ở câu trắc nghiệm, phương án Bộ Y tế "≥ 9 %" là phương án duy nhất dùng "≥", nên hình thức có thể lộ đáp án. question-writer nên đồng nhất ký hiệu so sánh trước khi đóng băng bộ câu hỏi v1, và không xem đầu ra thí điểm khi sửa.
- **P-dm-02.**
  - Cảnh báo "không thấy 16.7" là giới hạn của `cached_text` với tệp .pptx, không phải lỗi giá trị. Slide 176 ghi "≥16.7 mmol/L".
  - Tùy chọn: thêm "(điều trị ngoại trú)" vào câu hỏi.
- **P-dm-04 và P-dm-05.** Tập giá trị Bộ Y tế đang là hợp của 5481/2020 và bài tương ứng trong 3879/2014 (DR8).
  - Theo điều khoản, 3879/2014 còn hiệu lực: Điều 3 QĐ 3319/2017 chỉ bãi bỏ bài ĐTĐ típ 2.
  - Còn hiệu lực trên thực tế hay không là phán đoán khoa học, AI không quyết thay.
  - Giữ cờ [concordant_by_union]; không dùng hai mẩu này làm đối chứng sạch.
- **Giá trị ADA ở P-dm-06, -07, -08.** Các giá trị này lấy từ Bảng 2.1 và 2.8, vốn là ảnh trong slide. A và B đã xem ảnh và thấy khớp. `verified_by` vẫn để null vì người đọc là AI, không phải người.

## Tự kiểm

- `vnsoc.schemas atom`: OK 8/8.
- `pilot_merge --only dm --no-checklist`:
  - trước khi sửa: giữ 8 (2 conflict, 6 concordant), loại 0;
  - sau khi sửa: giữ 8 (2 conflict, 6 concordant), loại 0.
