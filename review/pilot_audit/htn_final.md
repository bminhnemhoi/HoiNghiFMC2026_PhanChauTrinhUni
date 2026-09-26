# HG1.2 tự động: trọng tài chủ đề htn (tăng huyết áp)

Ngày 26/9/2026. **Kiểm bởi AI (Claude), không phải người, không phải bác sĩ.** Kiểm toán viên A, B và trọng tài đều là AI.
Đầu vào: `htn_A.json`, `htn_B.json`. Kết quả máy đọc: `htn_final.json`.

**Kết quả: 2 ok, 1 đã sửa (lỗi giá trị nước ngoài, sửa từ nguồn đã mở), 0 loại, 0 chưa rõ.**

A và B chỉ khác nhau ở một chỗ: tiêu chí (d) của P-htn-04 (A pass, B uncertain). Không có tiêu chí nào fail. Không đọc `data/runs/`.

| Mẩu | a | b | c | d | A/B | Chốt | Thay đổi |
|---|---|---|---|---|---|---|---|
| P-htn-01 | pass | pass | pass | pass | ok/ok | **ok** | — |
| P-htn-03 | pass | pass | pass | pass | ok/ok | **ok** | — |
| P-htn-04 | pass | pass | pass | **fail → đã sửa** | ok/uncertain | **error (đã sửa)** | `foreign[1]` 2018 ESC/ESH: thêm 120–129 mmHg (< 65 tuổi), đổi sang nguồn gốc 2018 |

## Chỗ bất đồng: P-htn-04, tiêu chí (d)

Bản ghi EU_UK "2018 ESC/ESH" chỉ trích lại khuyến cáo chung qua slide 31 của bộ slide ESC 2024. B nghi bản 2018 có mục tiêu riêng cho người dưới 65 tuổi.

Trọng tài mở bộ slide chính thức 2018 ESC/ESH do European Society of Hypertension đăng: `eshonline.org/.../2018/10/Download-1.pdf`, bản đệm sha256 `60b18b7c…`, băm lại khớp. File có lớp chữ nên grep được. Trọng tài đã xem ảnh các slide 6, 62, 76, 77 và 116.

- **Slide 62:** người < 65 tuổi đang dùng thuốc hạ áp, đích tâm thu 120–129 mmHg ở đa số (I-A).
- **Slide 116:** cùng khuyến cáo trên, ghi là "120 đến < 130". Slide này cũng có mục tiêu đầu tiên < 140/90 cho mọi người bệnh, sau đó 130/80 hoặc thấp hơn nếu dung nạp (I-A).
- **Slide 6, 76, 77:** nhất quán. Nhóm 18–65 tuổi đặt đích 130 hoặc thấp hơn nếu dung nạp, không xuống dưới 120.

**Kết luận: B đúng.** Bản ghi cũ bỏ sót giá trị áp dụng cho đúng quần thể của mẩu (18–59 tuổi). Việc sửa dựa chắc chắn vào nguồn đã mở:
- thêm giá trị 120–129 mmHg;
- giữ hai giá trị < 140 và ≤ 130, vì cả hai đều được xác nhận ở slide 116;
- chuyển nguồn, url, sha256 và locator sang bộ slide 2018;
- đổi `verified_by` từ null sang auto.

Trạng thái xung đột vẫn là **concordant**, vì 120–129 giao với tập {120 đến < 130} của 5904. Mồi và dung sai không đổi.

## Thay đổi dữ liệu (`data/interim/pilot/htn.jsonl`)

Bản sao lưu nằm ở `scratchpad/audit/htn_before.jsonl`. Script sửa là `scratchpad/audit/fix_htn04.py`; nó kiểm rằng chỉ `foreign[1]` và `extraction.audit_fix` của P-htn-04 thay đổi, còn hai mẩu kia giữ nguyên từng byte.

- P-htn-04 `foreign[1].values`: thêm 120–129 mmHg (người < 65 tuổi).
- P-htn-04 `foreign[1]`: đổi source, url, fetched_at, page_sha256, locator và verified_by.
- P-htn-04 `extraction.audit_fix`: thêm mới, ghi rõ việc kiểm do AI làm, không phải người.

## Đề xuất loại

Không có.

## Không sửa dữ liệu, chỉ ghi lại

- **P-htn-01 (cho điều phối viên).**
  - Trọng tài đã tự xem ảnh 5904 tr. PDF 16 (Phụ lục 1.2). Ảnh ghi "HA tại phòng khám đo đúng quy trình ≥ 140/90 mmHg" và "Tự đo tại nhà ≥ 135/85 mmHg".
  - Như vậy cặp 135/85 của `moh_neighbour_pending` được một văn bản Bộ Y tế thứ hai xác nhận. Cặp 130/80 (Holter) chỉ suy ra bằng loại trừ.
  - Nhánh "≥ 180/110 → THA" trong cùng sơ đồ là một bước khác, không làm đổi đáp án.
  - Mặc định A.6 vẫn áp dụng: bối cảnh lân cận chỉ đưa vào độ nhạy N1.
- **P-htn-03.** Hai điểm, đều không đổi đáp án:
  - Tùy chọn cho question-writer (làm trước khi đóng băng và không xem đầu ra): câu "nam 56–59 tuổi không có yếu tố nguy cơ khác" mâu thuẫn với 3192 tr. 7 (nam > 55 tuổi đã là yếu tố nguy cơ). Có thể thu hẹp thành 41–55 tuổi hoặc ghi "nữ".
  - Ô "≥ 160/100 → dùng thuốc ngay" ở 5904 tr. 12 chỉ có trong ảnh. Điểm này để người chấm HG3.5 xem.
- **P-htn-04.**
  - Ghi chú (3) trong notes nay chỉ còn đúng với WHO 2021 và JNC8.
  - Lỗi bộ chấm với cmp "<" là việc của điều phối viên trước khi đóng băng.
- **Giá trị ESC 2024 ở các mẩu 01, 03, 04.** Slide ở dạng ảnh EMF. A và B đã tự dựng ảnh và đọc, trọng tài xem lại slide 53, 92, 93; cả ba khớp. `verified_by` vẫn để null vì người đọc là AI, không phải người.
- Cảnh báo "không thấy 140/90" của pilot_merge ở mẩu 01 và 03 là do `cached_text` không đọc được EMF trong pptx, không phải lỗi giá trị.
- Checklist HG1.2 sẽ được cập nhật khi chạy pilot_merge có checklist lúc gộp.

## Tự kiểm

- `vnsoc.schemas atom`: OK 3/3.
- `pilot_merge --only htn --no-checklist`:
  - trước khi sửa: giữ 3 (2 conflict, 1 concordant), loại 0;
  - sau khi sửa: giữ 3 (2 conflict, 1 concordant), loại 0.
- Cảnh báo của P-htn-04 đã hết. Cảnh báo pptx ở mẩu 01 và 03 có từ trước.
