---
name: question-generation
description: Sinh bộ câu hỏi VI+EN (trả lời ngắn, trắc nghiệm gài đáp án, tình huống A6), kiểm quần thể, dịch và QC, gán split theo mẩu, chuẩn bị đoạn oracle cho A3 (T1.3, T4.1–T4.3).
---
# Sinh câu hỏi (đề cương §3.5, §4.3)

1. **Trả lời ngắn** (dạng chính): mẫu câu cố định theo `slot_type` (liều / ngưỡng / thời gian / lịch / thuốc đầu tay / mục tiêu / phân loại / quy trình) điền bệnh, quần thể, can thiệp; LLM chỉ diễn đạt lại cho tự nhiên (giữ nguyên số, đơn vị, quần thể — kiểm bằng code). Không chứa đáp án hay từ gợi ý nguồn. Câu hỏi A1 ghép tiền tố trong `configs/conditions.yaml`, không viết vào câu hỏi.
2. **Loại câu mơ hồ**: nếu với quần thể đã nêu, giá trị nước ngoài cũng đúng theo Bộ Y tế (ví dụ ngưỡng HA đo lưu động) → sửa quần thể hoặc loại. HA chẩn đoán phải ghi “đo tại phòng khám”.
3. **Trắc nghiệm**: lựa chọn = {Bộ Y tế, nước ngoài (hệ thống xung đột), bản cũ (nếu có), mồi}; nếu thiếu bản cũ thì 3 lựa chọn + 1 nhiễu hợp lý không thuộc nguồn nào; hai thứ tự (order_variant 0/1) sinh bằng seed cố định; `option_roles` ghi vai trò từng chữ cái.
4. **Tình huống A6**: ca bệnh ở bệnh viện huyện Việt Nam (tên địa danh chung chung), đủ dữ kiện quần thể, hỏi bước xử trí/giá trị tiếp theo; không nói “theo Bộ Y tế”. HG4.2: người dùng (hoặc bác sĩ nếu có) kiểm ≥ 100 câu.
5. **Tiếng Anh**: dịch máy (API rẻ, Batch) → dịch ngược → so bằng code: tập số và đơn vị giống hệt, phủ định giữ nguyên, quần thể giữ nguyên; lỗi → dịch lại hoặc sửa tay có ghi log. `translation_qc: pass|fail`.
6. **Đoạn oracle A3**: 150–300 từ quanh `span` trong PDF (không cắt giữa câu); `oracle_passage_id`. Chunk RAG A2: ≤ 500 token, ghi `gold_chunk_ids` (chunk chứa span).
7. **Split theo mẩu** cho RQ3: `ref` (lấy ngưỡng/lưới, ví dụ 20%), `cal` (chứng nhận), `test` (đánh giá chế độ a) — tỉ lệ và seed ghi trong prereg; chia bằng `vnsoc.ltt.split_by_atom` hai lần; mọi câu của một mẩu cùng phía.
8. **Đóng băng** (T4.3): `/freeze questions` (đóng băng cùng grading.yaml và conditions.yaml) + addendum OSF nếu có thay đổi so với bản đăng ký.

Kiểm tra xong: schema `question` OK; mỗi mẩu xung đột có đủ VI/EN × short + MCQ(2 thứ tự); tỉ lệ loại < 20% (nếu cao hơn → xem lại mẫu câu); báo cáo `results/tables/question_qc.csv`.
