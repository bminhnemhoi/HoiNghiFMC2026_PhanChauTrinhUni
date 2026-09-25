---
name: grading-protocol
description: Chấm đầu ra bằng vnsoc.grade theo quy tắc đăng ký trước (6 nhãn, dung sai, nhiều giá trị, mồi), LLM tách đáp án dự phòng, kiểm tay bộ tách, DR9 (T1.5, T6.1, HG6.2).
---
# Chấm bằng quy tắc (đề cương §1.2, §4.5)

1. `grade_short(raw_output, atom, lang, synonyms, combos, condition=...)` cho trả lời ngắn và A6 (hỏi lại “quốc gia nào?” chỉ là nhãn 1 ở A0; ở A1–A6 là nhãn 6); `grade_mcq(output, option_roles)` cho trắc nghiệm. Tham số thuốc từ `configs/grading.yaml` (bản đóng băng).
2. Thứ tự nhãn: 1 đúng + biết bối cảnh → 2 đúng → 3 lệch phiên bản → 4 trùng nước ngoài (ghi hệ thống) → 5 không quy được nguồn (cờ `decoy_match`) → 6 từ chối. Đúng một phần / liệt kê nhiều giá trị không chỉ rõ giá trị Việt Nam → sai, báo cáo riêng (`partial`, `multi`).
3. Thiếu dòng `ĐÁP ÁN:`/`ANSWER:` và có > 1 giá trị ứng viên → `needs_llm`: gọi LLM tách đáp án (prompt cố định, API rẻ, Batch), chấm lại với `extracted=`; `parse_method: llm`.
4. **Kiểm bộ tách** (HG6.2): mẫu phân tầng 500 câu (đề cương §4.5; gồm mọi câu `parse_method=llm` nếu ≤ 250, phần còn lại phân tầng theo parse_method × mô hình × ngôn ngữ) → người dùng kiểm → báo cáo độ chính xác bộ tách kèm Clopper–Pearson. Lỗi tách > 5% hoặc tỉ lệ `needs_llm` > 5% ở một mô hình → DR9 (sửa bộ tách, tăng `grader_version`, chấm lại toàn bộ, báo cả hai).
5. Mẩu `indistinguishable` và `concordant` không vào kiểm định xác nhận H1–H3 (vẫn báo cáo mô tả).
6. Đầu ra: `data/processed/grades_v<grader_version>.parquet` (schema GradeRecord + khóa run).
