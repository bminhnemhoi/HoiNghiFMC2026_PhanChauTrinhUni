# Abstract FMC 2026 — bản "thiết kế" (dự phòng khi chưa có kết quả thí điểm)

Theo mẫu FMC2026_Huong-dan-viet-Abstract.docx (manuscript/fmc/template/). Chủ đề hội nghị: AI và chuyển đổi số trong Y tế và Giáo dục Y khoa. DOCX dựng bằng `vnsoc.fmc` từ bản đã điền số trong manuscript/build/fmc/.

## Ô TÓM TẮT

LLM có thể trả lời theo hướng dẫn nước ngoài hoặc bản cũ thay vì hướng dẫn hiện hành của Bộ Y tế. Chúng tôi xây bộ khuyến cáo đối chiếu được (giá trị Bộ Y tế trích nguyên văn từ PDF chính thức, giá trị WHO/Mỹ/châu Âu có phiên bản, giá trị bản cũ, giá trị mồi) và chấm câu trả lời của LLM bằng quy tắc so giá trị, bằng tiếng Việt và tiếng Anh. Đến nay {{design.pdf_conflicts}} khuyến cáo xung đột từ {{design.pdf_guidelines}} hướng dẫn đã được đối chiếu với văn bản gốc.

## VI

### TIÊU ĐỀ

Chuẩn điều trị của ai? Sai lệch theo chuẩn nước ngoài và theo phiên bản cũ của LLM so với hướng dẫn chuyên môn của Bộ Y tế Việt Nam

### ĐẶT VẤN ĐỀ

Sinh viên y khoa dùng mô hình ngôn ngữ lớn (LLM) để tra cứu, nhưng LLM có thể trả lời theo hướng dẫn nước ngoài hoặc bản cũ, trong khi hướng dẫn Bộ Y tế khác về liều, ngưỡng, thuốc và lịch tiêm.

### MỤC TIÊU

Đo sai lệch của LLM so với hướng dẫn hiện hành của Bộ Y tế và truy mỗi lỗi tới một hướng dẫn nước ngoài hoặc bản cũ có tên.

### PHƯƠNG PHÁP NGHIÊN CỨU

Trích khuyến cáo có giá trị từ {{=25}}–{{=35}} hướng dẫn hiện hành (PDF chính thức, khớp nguyên văn), gắn giá trị WHO, Mỹ, châu Âu, bản cũ và giá trị mồi. Hỏi LLM bằng tiếng Việt và tiếng Anh, có/không nêu "theo Bộ Y tế", có/không kèm đoạn hướng dẫn; chấm bằng quy tắc so giá trị thành {{design.n_labels}} nhãn. Giả thuyết chính (đăng ký trước): khi hỏi "theo Bộ Y tế", tỉ lệ trùng giá trị nước ngoài cao hơn trùng giá trị mồi.

### KẾT QUẢ

Đối chiếu PDF chính thức: {{design.seed_rows_confirmed}}/{{design.seed_rows_checked}} khác biệt hạt giống được xác nhận là xung đột; số còn lại không sạch (trùng văn bản hiện hành khác, trùng bản cũ, hoặc không phải khuyến cáo). Hiện có {{design.pdf_conflicts}} khuyến cáo xung đột ({{design.pdf_conflict_families}} nhóm, {{design.pdf_guidelines}} hướng dẫn) khớp nguyên văn; chưa có người và bác sĩ kiểm ngữ cảnh.

### KẾT LUẬN

Nếu được xác nhận, sai lệch theo chuẩn nước ngoài là rủi ro riêng cần đánh giá trước khi dùng LLM trong đào tạo và tra cứu lâm sàng tại Việt Nam.

### TỪ KHÓA

mô hình ngôn ngữ lớn; hướng dẫn điều trị; bộ y tế; đánh giá mô hình; giáo dục y khoa

## EN

### TITLE

Whose Standard of Care? Jurisdictional Defaults and Guideline Staleness of LLMs on Vietnamese Ministry of Health Guidelines

### BACKGROUND

Vietnamese medical students use large language models (LLMs) for reference. LLMs may answer with the values of foreign guidelines or of superseded versions, whereas Ministry of Health (MoH) guidelines differ in doses, thresholds, first-line drugs and schedules; an answer that is "right elsewhere" is hard to detect.

### OBJECTIVE

To measure how LLM answers deviate from current MoH guidelines and trace each error to a named foreign guideline or a named superseded MoH version.

### METHODS

We extract value-bearing recommendations from {{=25}}–{{=35}} current guidelines (official PDFs, verbatim-matched) and attach versioned WHO, US and European values, superseded values and a rule-generated decoy value. Open and commercial LLMs are queried in Vietnamese and English, with or without "according to the MoH", with or without the guideline passage. Answers are graded by value-comparison rules into {{design.n_labels}} labels: correct and context-aware, correct, outdated version, foreign match, unattributable, abstention. Preregistered primary hypothesis: under the MoH cue, foreign-value matches on conflict recommendations exceed decoy matches.

### RESULTS

Checking the seed set against official PDFs confirmed {{design.seed_rows_confirmed}} of {{design.seed_rows_checked}} candidate differences as conflicts; the rest were not clean (matching another current MoH document or a superseded version, or not a recommendation). So far {{design.pdf_conflicts}} conflict recommendations in {{design.pdf_conflict_families}} families from {{design.pdf_guidelines}} guidelines are verbatim-matched; human and clinician context review is still pending.

### CONCLUSION

If confirmed, foreign-standard deviation is a distinct risk to evaluate before LLMs are used in Vietnamese medical education and clinical reference.

### KEYWORDS

large language models; clinical practice guidelines; ministry of health; model evaluation; medical education

## GHI CHÚ

Bài chưa được đăng trên tạp chí khoa học trong nước hoặc quốc tế. This work has not been published in any national or international journal. Hình thức báo cáo: Oral.
