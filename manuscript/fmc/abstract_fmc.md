# Abstract FMC 2026 — bản có kết quả thí điểm (T1.7)

Theo mẫu hướng dẫn viết abstract của hội nghị và trả lời của Ban tổ chức (HG1.0): giới hạn và độ dài khuyến khích ở src/vnsoc/fmc.py, mỗi file một ngôn ngữ. Mọi số lấy từ registry (results/numbers.json) qua `vnsoc.numbers render`; DOCX dựng bằng `vnsoc.fmc` từ bản đã điền số trong manuscript/build/fmc/. Thí điểm: mẫu chọn tay; kiểm trích dẫn và kiểm bộ chấm bằng AI (người dùng làm một mình, không có bác sĩ); chạy cục bộ Qwen3-8B bản lượng tử hóa (docs/DECISIONS.md).

## Ô TÓM TẮT

LLM có thể trả lời theo hướng dẫn nước ngoài hoặc bản cũ thay vì hướng dẫn hiện hành của Bộ Y tế. Thí điểm trên {{pilot.n_atoms}} khuyến cáo đối chiếu PDF chính thức: khi hỏi "theo Bộ Y tế", Qwen3-8B đúng {{pilot.a1_vi_conflict_correct}}/{{pilot.a1_vi_conflict_n}} khuyến cáo xung đột với chuẩn nước ngoài, trùng giá trị nước ngoài {{pilot.a1_vi_conflict_foreign}} lần; lỗi chủ yếu là giá trị không có nguồn. Kèm đoạn hướng dẫn, số đúng tăng lên {{pilot.a3_vi_conflict_correct}}/{{pilot.a3_vi_conflict_n}}.

## VI

### TIÊU ĐỀ

Chuẩn điều trị của ai? Sai lệch theo chuẩn nước ngoài và theo phiên bản cũ của LLM so với hướng dẫn chuyên môn của Bộ Y tế Việt Nam

### ĐẶT VẤN ĐỀ

Sinh viên và nhân viên y tế dùng mô hình ngôn ngữ lớn (LLM) để tra cứu, nhưng LLM có thể trả lời theo hướng dẫn nước ngoài hoặc bản đã bị thay thế, trong khi hướng dẫn của Bộ Y tế khác về liều, ngưỡng, thuốc và lịch tiêm.

### MỤC TIÊU

Xây dựng phương pháp đo sai lệch của LLM so với hướng dẫn hiện hành của Bộ Y tế, truy mỗi lỗi tới một hướng dẫn nước ngoài hoặc bản cũ có tên, và thử trên một mô hình mở chạy cục bộ.

### PHƯƠNG PHÁP NGHIÊN CỨU

Thí điểm trên {{pilot.n_atoms}} khuyến cáo có giá trị cụ thể từ {{pilot.n_guidelines}} hướng dẫn hiện hành, trích nguyên văn từ PDF chính thức và được hai kiểm toán viên AI độc lập đối chiếu. Mỗi khuyến cáo gắn giá trị WHO, Mỹ, châu Âu có phiên bản, giá trị bản cũ và một giá trị mồi sinh theo quy tắc để đối chứng trùng hợp ngẫu nhiên. Qwen3-8B (bản lượng tử hóa, chạy trên laptop) trả lời bằng tiếng Việt và tiếng Anh ở ba điều kiện: không nêu quốc gia, hỏi "theo Bộ Y tế", và kèm đúng đoạn hướng dẫn. Câu trả lời được chấm bằng quy tắc so giá trị định trước; hai người chấm AI độc lập kiểm lại toàn bộ {{pilot.grader_n}} câu.

### KẾT QUẢ

Bộ chấm quy tắc khớp nhãn tham chiếu {{pilot.grader_agree_pct}} (kappa {{pilot.grader_kappa_rule_final}}). Khi hỏi "theo Bộ Y tế" bằng tiếng Việt, trên {{pilot.a1_vi_conflict_n}} khuyến cáo xung đột với chuẩn nước ngoài, mô hình đúng {{pilot.a1_vi_conflict_correct}} ({{pilot.a1_vi_conflict_correct_pct}}; KTC {{pilot.ci_level}} {{pilot.a1_vi_conflict_correct_ci}}), trùng giá trị nước ngoài {{pilot.a1_vi_conflict_foreign}}, và {{pilot.a1_vi_conflict_unattributed}} câu đưa giá trị không khớp nguồn nào; trên {{pilot.a1_vi_h1_n}} khuyến cáo có mồi, trùng nước ngoài {{pilot.a1_vi_h1_foreign}} lần so với trùng mồi {{pilot.a1_vi_decoy}} lần. Khi kèm đoạn hướng dẫn, số câu đúng tăng lên {{pilot.a3_vi_conflict_correct}}/{{pilot.a3_vi_conflict_n}} (khuyến cáo xung đột) và {{pilot.a3_vi_concordant_correct}}/{{pilot.a3_vi_concordant_n}} (khuyến cáo trùng chuẩn quốc tế).

### KẾT LUẬN

Ở mô hình mở nhỏ này, lỗi chủ yếu là giá trị không có nguồn hơn là mặc định theo chuẩn nước ngoài, và cung cấp đúng văn bản Bộ Y tế cải thiện rõ độ chính xác. Đây là kết quả sơ bộ trên mẫu chọn tay, kiểm bằng AI, chưa có bác sĩ duyệt; nghiên cứu chính sẽ kiểm định trên toàn kho hướng dẫn và nhiều mô hình mở.

### TỪ KHÓA

mô hình ngôn ngữ lớn; hướng dẫn điều trị; bộ y tế; đánh giá mô hình; giáo dục y khoa

## EN

### TITLE

Whose Standard of Care? Foreign-Guideline and Outdated-Version Deviations of LLMs from Vietnamese Ministry of Health Guidelines

### BACKGROUND

Students and health workers use large language models (LLMs) for clinical reference, but LLMs may answer with the values of foreign or superseded guidelines, whereas Vietnamese Ministry of Health (MoH) guidelines differ in doses, thresholds, first-line drugs and schedules.

### OBJECTIVE

To build a method that measures how LLM answers deviate from current MoH guidelines, traces each error to a named foreign guideline or superseded MoH version, and to pilot it on a locally run open model.

### METHODS

Pilot on {{pilot.n_atoms}} recommendations with specific values from {{pilot.n_guidelines}} current guidelines, quoted verbatim from official PDFs and cross-checked by two independent AI auditors. Each recommendation carries versioned WHO, US and European values, superseded values and a rule-generated decoy value that controls for chance matches. Qwen3-8B (quantized, run on a laptop) answered in Vietnamese and English under three conditions: no country cue, "according to the MoH", and with the correct guideline passage. Answers were graded by pre-specified value-comparison rules; two independent AI graders re-labelled all {{pilot.grader_n}} answers.

### RESULTS

The rule-based grader matched the reference labels in {{pilot.grader_agree_pct}} of answers (kappa {{pilot.grader_kappa_rule_final}}). Under the MoH cue in Vietnamese, on {{pilot.a1_vi_conflict_n}} recommendations that conflict with foreign guidelines, the model was correct in {{pilot.a1_vi_conflict_correct}} ({{pilot.a1_vi_conflict_correct_pct}}; {{pilot.ci_level}} CI {{pilot.a1_vi_conflict_correct_ci}}), matched a foreign value in {{pilot.a1_vi_conflict_foreign}}, and gave a value matching no source in {{pilot.a1_vi_conflict_unattributed}}; on {{pilot.a1_vi_h1_n}} recommendations with a decoy, foreign matches were {{pilot.a1_vi_h1_foreign}} versus {{pilot.a1_vi_decoy}} decoy matches. With the guideline passage, correct answers rose to {{pilot.a3_vi_conflict_correct}} of {{pilot.a3_vi_conflict_n}} conflict recommendations and {{pilot.a3_vi_concordant_correct}} of {{pilot.a3_vi_concordant_n}} recommendations concordant with international guidelines.

### CONCLUSION

For this small open model, errors were mostly unsourced values rather than foreign defaults, and supplying the MoH text clearly improved accuracy. These are preliminary results on a hand-picked sample, checked by AI without clinician review; the main study will test them across the guideline corpus and several open models.

### KEYWORDS

large language models; clinical practice guidelines; ministry of health; model evaluation; medical education

## GHI CHÚ

Bài chưa được đăng trên tạp chí khoa học trong nước hoặc quốc tế. Hình thức báo cáo: Oral.

## NOTE

This work has not been published in any national or international journal. Presentation format: Oral.

## ABSTRACT BOX

LLMs may answer with foreign or outdated guideline values instead of current Vietnamese Ministry of Health (MoH) guidelines. In a pilot on {{pilot.n_atoms}} recommendations checked against official PDFs, Qwen3-8B asked "according to the MoH" was correct on {{pilot.a1_vi_conflict_correct}}/{{pilot.a1_vi_conflict_n}} conflict recommendations and matched a foreign value {{pilot.a1_vi_conflict_foreign}} times; most errors were unsourced values. With the guideline passage, correct answers rose to {{pilot.a3_vi_conflict_correct}}/{{pilot.a3_vi_conflict_n}}.
