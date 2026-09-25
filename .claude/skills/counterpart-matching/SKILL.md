---
name: counterpart-matching
description: Dựng kho đối chiếu nước ngoài có phiên bản, gắn giá trị nước ngoài / bản cũ / mồi cho mẩu, tính dung sai và trạng thái xung đột, đo độ nhạy và độ chính xác ghép (T2.6, T3.3, HG3.7).
---
# Ghép giá trị đối chiếu (đề cương §3.3, §4.2)

## Kho nước ngoài (`data/interim/foreign_values.jsonl`)
Mỗi dòng: chủ đề, `system` (US | EU_UK | WHO_global | WHO_WPRO | OTHER), `source` (tên hướng dẫn + năm), `version_date`, `url`, `locator` (mục/bảng/trang), `fetched_at` (ngày mở trang), `page_sha256` (băm nội dung trang/PDF đã mở — bằng chứng giá trị lấy từ nguồn chứ không từ trí nhớ), `values` (ValueItem). Trang bị chặn trong chế độ tự động (domain chưa trong danh sách cho phép) → block task, ghi domain để người dùng duyệt. **Không lưu đoạn văn** của ADA/ESC/AHA/GINA/GOLD. Ghi cả bản WHO hiện hành và bản trước (ví dụ WHO 2009 dengue → hướng dẫn arbovirus WHO 7/2025), RCUK và WAO/EAACI cho phản vệ.

## Ghép
1. Truy xuất đoạn liên quan trong nguồn nước ngoài và bản Bộ Y tế cũ (theo bệnh + slot + quần thể).
2. LLM đề xuất giá trị + vị trí; chỉ nhận khi giá trị có trong trang nguồn (kiểm bằng code với bản HTML/PDF mở).
3. So sánh bằng quy tắc: số sau quy đổi; thuốc theo INN; lịch theo dãy ngày. `vnsoc.grade.conflict_status(atom)` và `compute_tolerance(atom)` là định nghĩa duy nhất.
4. **Giá trị mồi** (`decoy`): cùng kiểu/đơn vị, khoảng cách tới giá trị Việt Nam ≈ khoảng cách của giá trị nước ngoài, phía còn lại nếu hợp lý lâm sàng, không trùng nguồn nào; kiểm bằng code rằng mẩu không thành `indistinguishable`. Với lịch/thuốc: một phác đồ có thật nhưng không phải của nguồn nào trong mẩu.
5. `conflict_family`: nhãn cho các mẩu cùng một khác biệt gốc (ví dụ `htn_threshold_us`).

## Đo chất lượng
- **Độ nhạy** trên bộ hạt giống: bao nhiêu dòng xác nhận trong `seed_conflicts.yaml` được pipeline tìm lại.
- **Độ chính xác** (HG3.7): 100 cặp ghép ngẫu nhiên → người dùng kiểm → Clopper–Pearson.
- **Độ nhạy theo kho đối chiếu**: báo cáo quy nguồn khi bỏ từng hệ thống (US/EU_UK/WHO).
- DR2: < 400 mẩu xung đột hoặc < 25 nhóm → mở rộng bệnh giàu xung đột trước ngày đóng băng câu hỏi; không hạ chuẩn xung đột.
