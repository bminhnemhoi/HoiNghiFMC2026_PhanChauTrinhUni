---
name: vn-number-normalization
description: Cách dùng và mở rộng src/vnsoc/normalize_vi.py (số kiểu Việt/Anh, khoảng, dấu so sánh, đơn vị, huyết áp, lịch tiêm, thuốc, phân loại). Dùng khi trích mẩu, ghép giá trị, chấm điểm, hoặc khi test chấm thất bại.
---
# Chuẩn hóa giá trị tiếng Việt

- Số: tiếng Việt dấu phẩy thập phân (`0,5`), dấu chấm + đúng 3 chữ số là hàng nghìn (`5.000`); `0.500` và `2.5` hiểu là thập phân; `2,000` (phẩy + `000`) là hàng nghìn. Tiếng Anh ngược lại. Hàm: `parse_number(tok, lang)`.
- Giá trị: `parse_nums(text, lang)` → `Num(lo, hi, unit, cmp)`; khoảng (`10 - 15`, `từ … đến …`, `0,5–1`), dấu so sánh (≥, trên, dưới, tối đa, at least…). Trích dẫn văn bản (`QĐ 2760/QĐ-BYT`, `1740/2026`) và năm đứng riêng (`ADA 2025`) bị loại trước khi đọc số.
- Đơn vị chuẩn trong `UNIT_ALIASES` (ví dụ `ml/kg/giờ`→`ml/kg/h`, `µg|mcg`→`ug`, `/mm3`→`/uL`). Quy đổi `convert(v, from, to, ctx)`; ngữ cảnh mẩu (`Atom.context`): `weight_kg`, `mg_per_ml`, `mg_per_tablet`, `mg_per_ampoule`, `analyte` (glucose/ldl/triglyceride cho mg/dL↔mmol/L).
- Huyết áp `parse_bps` (loại cặp không hợp lý như `30/19 U/L`); lịch `parse_schedules` (`N0-3-7-14-28`, `ngày 0, 3, 7, 14`, `2, 3, 4 tháng`); thuốc `parse_drugs` theo `configs/grading.yaml` (bí danh INN + tổ hợp); phân loại `parse_cats` theo `cat_options` của mẩu.

## Khi thêm quy tắc
1. Viết test trong `tests/test_normalize.py` trước (ca gốc lấy từ văn bản thật, ghi nguồn trong comment).
2. Sửa tối thiểu; chạy toàn bộ `make test`.
3. Sau khi đóng băng câu hỏi (T4.3): mọi thay đổi ảnh hưởng chấm điểm → tăng `grader_version` trong configs/grading.yaml (tạo bản mới, không sửa bản đóng băng), ghi DECISIONS, chấm lại toàn bộ và báo cả hai.
