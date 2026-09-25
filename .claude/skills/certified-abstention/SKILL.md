---
name: certified-abstention
description: RQ3 — tín hiệu bất đồng, hai nhóm cố định, điểm tin cậy cross-fit, cận trên Clopper–Pearson đồng thời ở các mức trả lời cố định (kết quả chính), Learn-then-Test (phụ), hai chế độ chia, DR4/DR5 (T6.6). Dùng src/vnsoc/ltt.py.
---
# Từ chối có chứng nhận (đề cương §4.6, §4.7, §5.4)

## Tín hiệu và nhóm (cố định trước hiệu chỉnh, không dùng nhãn)
- Câu trả lời phục vụ: A2, cùng ngôn ngữ câu hỏi, nhiệt độ 0.
- Nhóm **bất đồng** nếu có ≥ 1: A1 ≠ A2 (so giá trị đã parse, không so chuỗi); VI ≠ EN ở A2; đoạn được trích dẫn (dòng NGUỒN/SOURCE) không chứa giá trị được trả lời. Còn lại: **đồng thuận**. G = 2.
- Điểm c(x): hồi quy logistic trên tín hiệu (các cờ trên, độ nhất quán 5 mẫu A2 T=0,7, log-prob câu trả lời của mô hình mở), huấn luyện cross-fit trên phần hướng dẫn tách riêng; cách tính giống hệt lúc triển khai.

## Kết quả chính: cận chứng nhận
1. Chia theo mẩu (`split_by_atom`, seed trong prereg): phần tham chiếu (lấy ngưỡng) / hiệu chỉnh / (chế độ a) đánh giá.
2. `thr = thresholds_from_reference(score_ref, group_ref, (1.0, .75, .5, .25))`.
3. `certified_bounds(score_cal, error_cal, group_cal, thr, delta=0.10)` → U_gk với độ tin cậy 1 − δ/(G·K). Báo cáo: “ở mức trả lời c, sai số nhóm g ≤ U”.
4. Phụ: `ltt_thresholds(..., make_grids(ref), alpha, delta)`; α = 0,10, trừ khi nhóm có < 300 mẩu hiệu chỉnh → α = 0,15 (DR4, quy tắc không dùng nhãn). Mức trả lời < 30% ở nhóm bất đồng → kết luận “lớp từ chối không hữu ích cho nhóm này” (DR5) — vẫn là kết quả.
5. So sánh: không từ chối; “từ chối mọi câu bất đồng”; LTT một nhóm; CRC trên rủi ro kết hợp; nhóm theo chuyên khoa.

## Đánh giá vi phạm
- (a) Chia ngẫu nhiên theo mẩu: so với sai số **toàn kho** (hiệu chỉnh ∪ kiểm tra), không so với nửa kiểm tra.
- (b) Chia theo hướng dẫn (hướng dẫn chưa thấy): 500 lần chia; tần suất vi phạm thực nghiệm; ngưỡng chấp nhận ≤ 2δ = 0,20. Không có bảo đảm lý thuyết — nói rõ.
- Báo cáo bảng chéo nhóm tín hiệu × trạng thái xung đột × loại lỗi (mô hình “cố chấp nhất quán” rơi vào nhóm đồng thuận).
- Kiểm tra mã: `$PY -m vnsoc.ltt` (mô phỏng) phải cho tỉ lệ cận bị vượt ≤ 0,10.
