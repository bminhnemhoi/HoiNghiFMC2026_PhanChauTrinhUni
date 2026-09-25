---
name: tripod-llm-manuscript
description: Cấu trúc và quy tắc viết abstract FMC, slide, bản thảo JMIR Medical Informatics/IJMI theo TRIPOD-LLM, supplement S1–S6, thư nộp; số qua registry (T1.6, T4.8, T7.x, T8.1).
---
# Viết bài

## Abstract FMC (T1.6, tiếng Việt)
Theo mục 7.3 đề cương: tên 131 ký tự; bản ngắn (≤ giới hạn ô 500 — ký tự hay từ theo trả lời của ban tổ chức) và bản đầy đủ ~340 từ cho file đính kèm DOCX/PDF ≤ 1 MB. Ô `[n] [k] [a] [b] [c] [d] [e] [f]` điền bằng `{{pilot.*}}` từ registry (bản thiết kế dùng `{{design.*}}` do `src/vnsoc/analysis/design_counts.py` tính từ `data/seed/seed_conflicts.yaml`); `$PY -m vnsoc.numbers render` tạo `manuscript/build/fmc/*.md` đã điền số; DOCX tạo từ bản build; người dùng chỉ nộp bản build. Không kịp thí điểm → phương án “chỉ thiết kế” (mô tả bộ xung đột đã xác minh, thì tương lai). Ghi rõ mẫu chọn tay, chưa có bác sĩ duyệt. Tạo DOCX bằng python-docx hoặc pandoc; kiểm dung lượng.

## Bản thảo (tiếng Anh, `manuscript/main.md`)
Cấu trúc JMIR (Original Paper): Abstract có cấu trúc (Background, Objective, Methods, Results, Conclusions ≤ 450 từ) · Introduction · Methods (Guideline corpus; Recommendation atoms; Foreign and superseded counterparts; Question sets; Models and conditions; Rule-based grading; Statistical analysis; Certified abstention; Preregistration and deviations; Ethics) · Results · Discussion (principal findings, comparison with prior work, implications for medical education in Vietnam, limitations) · Conclusions · Data/code availability · AI use disclosure (ICMJE) · CRediT.
- Hình: F1 quy trình; F2 quy nguồn ở A1 theo mô hình × ngôn ngữ (nhãn 1–6, vạch mồi); F3 bậc thang ngữ cảnh A0→A4; F4 lệch phiên bản theo số tháng; F5 cận chứng nhận RQ3 theo mức trả lời. Bảng: T1 kho hướng dẫn; T2 mô hình; T3 kết quả giả thuyết H1–H4; T4 phân rã lỗi truy xuất vs cố chấp.
- Supplement: S1 danh mục văn bản + chuỗi thay thế; S2 quy tắc trích và QC; S3 prompt và điều kiện; S4 quy tắc chấm + kiểm bộ tách; S5 phân tích độ nhạy; S6 checklist TRIPOD-LLM điền đủ.
- Mọi số: `{{khóa}}`; hằng số thiết kế `{{=…}}`; `make verify` xanh; `$PY -m vnsoc.numbers render` → `manuscript/build/`.
- Giọng điệu: tuyên bố đúng mức (mục 2.4 đề cương); nêu rõ giới hạn (một quốc gia, kho 25–35 văn bản, mô hình 7–8B lượng tử, bảo đảm RQ3 không áp dụng cho hướng dẫn mới). Không gọi agent phản biện là người.
- Thư nộp (T8.1): 1 trang — vấn đề, đóng góp, vì sao hợp tạp chí, dữ liệu/mã công khai, không nộp nơi khác, đăng ký trước (link OSF), xung đột lợi ích.
