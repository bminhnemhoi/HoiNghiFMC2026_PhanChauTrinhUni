# HG1.2 — Kiểm toán tự động chủ đề dengue: phán quyết cuối (trọng tài)

Ngày 26/9/2026. **Kiểm bởi AI (Claude), không phải người, không phải bác sĩ.** Đầu vào: `dengue_A.json`, `dengue_B.json`.
Không đọc `data/runs/`. Nguồn nước ngoài chỉ ghi giá trị và vị trí.

**Kết quả: 5 ok · 4 đã sửa (không đổi giá trị) · 0 loại · 0 chưa rõ.**

| Mẩu | a | b | c | d | Cuối | A≠B ở | Trường đã sửa |
|---|---|---|---|---|---|---|---|
| P-dengue-01 | pass | pass | pass | pass | **ok** | — | — |
| P-dengue-02 | pass | pass | pass | uncertain | **sửa** | — | foreign[US/CDC 2024] (bỏ; chuyển sang extraction.removed_foreign); extraction.removed_foreign (mới); extraction.audit_fix (mới); extraction.notes (thêm) |
| P-dengue-03 | pass | pass | pass | pass | **ok** | — | — |
| P-dengue-04 | pass | pass | fail | pass | **sửa** | cd | population.severity; condition; foreign[WHO 2025].locator (thêm phạm vi p.15, p.27); extraction.audit_fix (mới, có pending_questions); extraction.notes (thêm) |
| P-dengue-05 | pass | pass | pass | pass | **sửa** | — | extraction.notes (thêm); extraction.audit_fix (mới) |
| P-dengue-06 | pass | pass | pass | pass | **ok** | — | — |
| P-dengue-08 | pass | pass | pass | pass | **ok** | — | — |
| P-dengue-09 | pass | pass | pass | pass | **ok** | — | — |
| P-dengue-10 | pass | pass | pass | pass | **sửa** | — | foreign[WHO 2009].locator; foreign[CDC 2024].locator (thêm p.7); extraction.audit_fix (mới); extraction.notes (thêm) |

## Quyết định chính

- **P-dengue-02**: CDC 2024 tr.5 in «10mg/kg for 1-2 hrs». Sai đơn vị và không có "/giờ", nên không xác nhận được giá trị. Trọng tài bỏ bản ghi CDC khỏi `foreign` (lưu ở `extraction.removed_foreign`). Còn WHO 2009 và 2012 (5–7 ml/kg/giờ), nên mẩu vẫn là xung đột.
- **P-dengue-04**: WHO 2025 tr.15 và tr.27 định nghĩa "non-severe" là người bệnh xử trí được ngoại trú; người phải nhập viện được xếp là "severe". Vì vậy quần thể của mẩu thu hẹp thành "SXHD chưa có dấu hiệu cảnh báo, điều trị ngoại trú". Giá trị giữ nguyên: Bộ Y tế "không dùng" (2760 tr.12), WHO "gợi ý dùng" (tr.47).
- **P-dengue-05**: bổ sung ghi chú, giá trị giữ nguyên. Cả 3705/2019 (Phụ lục 19, tr.45) và 2760/2023 (Phụ lục 21, tr.63) đều có ô "20 ml/kg/15 phút (M=0, HA=0)" ở tuyến cơ sở. Vì vậy việc đổi 60 → 15 phút chỉ đúng cho phác đồ người lớn tại bệnh viện.
- **P-dengue-10**: vị trí WHO 2009 sửa thành Chương 2 §2.1.4 (tr.40, số in 28). Thêm vị trí CDC tr.7 (≤ 20 mmHg, cột sốc tụt huyết áp).

## Tự kiểm
- `verify_span`: 9/9 OK. Schema: 9 dòng hợp lệ.
- `pilot_merge --only dengue`: giữ 9, loại 0. Trạng thái, dung sai, mồi và giá trị Bộ Y tế/bản cũ giống hệt trước khi sửa.
- Sao lưu: `C:/Users/Admin/AppData/Local/Temp/claude/d--phan-chau-trinh---y-khoa/1e1ea5eb-0832-473b-882a-b9921c8f5c59/scratchpad/audit/dengue_before.jsonl`.

## Còn việc (ngoài file mẩu)
- Sửa **6 câu hỏi P-dengue-04**: bỏ "hoặc nội trú" / "or inpatient", thay bằng "chưa có dấu hiệu cảnh báo, điều trị ngoại trú". Phải xong **trước khi đóng băng bộ câu hỏi v1**.
- Lượt thí điểm đã chạy P-dengue-04 với câu cũ. Cần ghi đây là hạn chế của thí điểm.
- Mục B trong HG1.2_decisions ("P-dengue-02: giá trị CDC") đã xử lý xong, không cần người mở nữa.
