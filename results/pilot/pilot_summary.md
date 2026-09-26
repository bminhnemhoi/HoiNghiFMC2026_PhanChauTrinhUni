# Thí điểm — kết quả chấm (tự sinh bởi src/vnsoc/analysis/pilot.py)

Mẫu chọn tay, chưa có bác sĩ duyệt. grader_version 1.2.0. Nhãn: 1 đúng+biết bối cảnh, 2 đúng, 3 lệch phiên bản, 4 trùng nước ngoài, 5 không quy được nguồn, 6 từ chối.

Loại khỏi phân tích (quyết trước khi chấm, data/interim/pilot_analysis_exclusions.yaml): mcq P-tbhiv-05: mồi hiển thị TDF+3TC+EFV trùng phương án thay thế của WHO 2014 (phát hiện sau khi dựng câu, trước khi chấm) — không phải mồi hợp lệ; descriptive P-immunization-01: neo TT 52/2025 đã hết hiệu lực 01/7/2026 — chuẩn tham chiếu chờ người dùng quyết (HG1.2 A1; mặc định (c)); descriptive P-immunization-02: như P-immunization-01; descriptive P-immunization-04: như P-immunization-01; descriptive P-controls-09: tập Bộ Y tế phụ thuộc cách đọc 3879/2014 Bảng 2 (HG1.2 A4); mặc định ngoài tập xung đột xác nhận.

| mô hình | điều kiện | ngôn ngữ | dạng | nhóm mẩu | n | L1 | L2 | L3 | L4 | L5 | L6 | trùng mồi | lỗi | cần LLM |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| qwen3_8b_local | A0 | en | short | concordant | 21 | 0 | 10 | 0 | 0 | 11 | 0 | 0 | 0 | 0 |
| qwen3_8b_local | A0 | en | short | conflict | 20 | 0 | 3 | 1 | 3 | 11 | 2 | 1 | 0 | 0 |
| qwen3_8b_local | A0 | en | short | descriptive | 4 | 0 | 0 | 0 | 1 | 3 | 0 | 1 | 0 | 0 |
| qwen3_8b_local | A0 | en | short | drift | 20 | 0 | 5 | 4 | 1 | 8 | 2 | 0 | 0 | 0 |
| qwen3_8b_local | A0 | vi | short | concordant | 21 | 0 | 11 | 0 | 0 | 9 | 1 | 0 | 0 | 0 |
| qwen3_8b_local | A0 | vi | short | conflict | 20 | 0 | 2 | 0 | 4 | 10 | 4 | 0 | 0 | 0 |
| qwen3_8b_local | A0 | vi | short | descriptive | 4 | 0 | 1 | 0 | 3 | 0 | 0 | 0 | 0 | 0 |
| qwen3_8b_local | A0 | vi | short | drift | 20 | 0 | 8 | 2 | 1 | 7 | 2 | 0 | 0 | 0 |
| qwen3_8b_local | A1 | en | mcq | concordant | 2 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| qwen3_8b_local | A1 | en | mcq | conflict | 26 | 0 | 7 | 1 | 3 | 6 | 9 | 4 | 0 | 0 |
| qwen3_8b_local | A1 | en | mcq | descriptive | 6 | 0 | 2 | 0 | 0 | 2 | 2 | 0 | 0 | 0 |
| qwen3_8b_local | A1 | en | mcq | drift | 10 | 0 | 3 | 2 | 0 | 3 | 2 | 1 | 0 | 0 |
| qwen3_8b_local | A1 | en | short | concordant | 21 | 0 | 10 | 0 | 0 | 10 | 1 | 0 | 0 | 0 |
| qwen3_8b_local | A1 | en | short | conflict | 20 | 0 | 5 | 2 | 1 | 8 | 4 | 0 | 0 | 0 |
| qwen3_8b_local | A1 | en | short | descriptive | 4 | 0 | 2 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |
| qwen3_8b_local | A1 | en | short | drift | 20 | 0 | 6 | 3 | 0 | 8 | 3 | 0 | 0 | 0 |
| qwen3_8b_local | A1 | vi | mcq | concordant | 2 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| qwen3_8b_local | A1 | vi | mcq | conflict | 26 | 0 | 14 | 1 | 5 | 6 | 0 | 4 | 0 | 0 |
| qwen3_8b_local | A1 | vi | mcq | descriptive | 6 | 0 | 0 | 0 | 5 | 1 | 0 | 0 | 0 | 0 |
| qwen3_8b_local | A1 | vi | mcq | drift | 10 | 0 | 3 | 4 | 0 | 3 | 0 | 0 | 0 | 0 |
| qwen3_8b_local | A1 | vi | short | concordant | 21 | 0 | 9 | 0 | 0 | 11 | 1 | 0 | 0 | 0 |
| qwen3_8b_local | A1 | vi | short | conflict | 20 | 0 | 7 | 0 | 2 | 7 | 4 | 0 | 0 | 0 |
| qwen3_8b_local | A1 | vi | short | descriptive | 4 | 0 | 1 | 0 | 3 | 0 | 0 | 0 | 0 | 0 |
| qwen3_8b_local | A1 | vi | short | drift | 20 | 0 | 9 | 3 | 1 | 4 | 3 | 0 | 0 | 0 |
| qwen3_8b_local | A3 | en | short | concordant | 21 | 0 | 19 | 0 | 0 | 1 | 1 | 0 | 0 | 0 |
| qwen3_8b_local | A3 | en | short | conflict | 20 | 0 | 13 | 0 | 1 | 3 | 3 | 0 | 0 | 0 |
| qwen3_8b_local | A3 | en | short | descriptive | 4 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| qwen3_8b_local | A3 | en | short | drift | 20 | 0 | 15 | 1 | 0 | 2 | 2 | 0 | 0 | 0 |
| qwen3_8b_local | A3 | vi | short | concordant | 21 | 0 | 19 | 0 | 0 | 1 | 1 | 0 | 0 | 0 |
| qwen3_8b_local | A3 | vi | short | conflict | 20 | 0 | 13 | 0 | 0 | 4 | 3 | 0 | 0 | 0 |
| qwen3_8b_local | A3 | vi | short | descriptive | 4 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| qwen3_8b_local | A3 | vi | short | drift | 20 | 0 | 18 | 1 | 0 | 0 | 1 | 0 | 0 | 0 |
