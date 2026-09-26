# Abstract FMC 2026 — bản có kết quả thí điểm (T1.7, sửa theo hội đồng M1)

Theo mẫu hướng dẫn viết abstract của hội nghị và trả lời của Ban tổ chức (HG1.0): giới hạn và độ dài khuyến khích ở src/vnsoc/fmc.py, mỗi file một ngôn ngữ. Mọi số lấy từ registry (results/numbers.json) qua `vnsoc.numbers render` (bản tiếng Anh dùng `|en` để in dấu chấm thập phân); DOCX dựng bằng `vnsoc.fmc`. Thí điểm: mẫu chọn tay; kiểm trích dẫn và kiểm bộ chấm bằng AI (người dùng làm một mình, không có bác sĩ); chạy cục bộ Qwen3-8B bản lượng tử hóa (docs/DECISIONS.md). Sửa theo các báo cáo trong review/M1.

## Ô TÓM TẮT

LLM có thể trả lời theo hướng dẫn nước ngoài hoặc bản cũ thay vì hướng dẫn hiện hành của Bộ Y tế. Thí điểm (mẫu chọn tay, kiểm bằng AI, chưa có bác sĩ duyệt) trên {{pilot.n_atoms_analysed}} khuyến cáo: hỏi "theo Bộ Y tế" bằng tiếng Việt, Qwen3-8B đúng {{pilot.a1_vi_conflict_correct}}/{{pilot.a1_vi_conflict_n}} khuyến cáo khác chuẩn nước ngoài, trùng giá trị nước ngoài {{pilot.a1_vi_conflict_foreign}} lần (không vượt mức trùng mồi); phần lớn lỗi không khớp nguồn nào. Kèm đoạn hướng dẫn: đúng {{pilot.a3_vi_conflict_correct}}/{{pilot.a3_vi_conflict_n}}.

## VI

### TIÊU ĐỀ

Chuẩn điều trị của ai? Sai lệch theo chuẩn nước ngoài và theo phiên bản cũ của LLM so với hướng dẫn chuyên môn của Bộ Y tế Việt Nam

### ĐẶT VẤN ĐỀ

Người học và nhân viên y tế dùng mô hình ngôn ngữ lớn (LLM) để tra cứu, nhưng LLM có thể trả lời theo hướng dẫn nước ngoài hoặc bản đã bị thay thế, vốn có thể khác hướng dẫn Bộ Y tế về liều, ngưỡng và thuốc.

### MỤC TIÊU

Đo sai lệch của LLM so với hướng dẫn hiện hành của Bộ Y tế và phân loại mỗi lỗi theo nguồn (nước ngoài có tên, bản cũ, hay không khớp nguồn nào).

### PHƯƠNG PHÁP NGHIÊN CỨU

Thí điểm trên {{pilot.n_atoms}} khuyến cáo có giá trị cụ thể, trích nguyên văn từ PDF chính thức; {{pilot.n_atoms_analysed}} khuyến cáo từ {{pilot.n_guidelines_analysed}} văn bản còn hiệu lực được phân tích. Trích dẫn được hai lượt AI (Claude) kiểm riêng, mù, có trọng tài. Khuyến cáo được gắn giá trị WHO, Mỹ, châu Âu có phiên bản, giá trị bản cũ và giá trị mồi sinh theo quy tắc (khi có) để đối chứng trùng hợp ngẫu nhiên. Qwen3-8B (chạy cục bộ trên laptop) trả lời bằng tiếng Việt và tiếng Anh ở ba điều kiện: không nêu quốc gia, hỏi "theo Bộ Y tế", và kèm đúng đoạn hướng dẫn. Câu trả lời được chấm bằng quy tắc so giá trị định trước và được kiểm lại bằng hai lượt chấm AI mù có trọng tài.

### KẾT QUẢ

Với câu trả lời ngắn, bộ chấm quy tắc khớp nhãn do AI phân xử ở {{pilot.grader_short_agree_pct}} (kappa {{pilot.grader_short_kappa}}). Hỏi "theo Bộ Y tế" bằng tiếng Việt, trên {{pilot.a1_vi_conflict_n}} khuyến cáo khác ít nhất một hướng dẫn nước ngoài có tên, mô hình đúng {{pilot.a1_vi_conflict_correct}} ({{pilot.a1_vi_conflict_correct_pct}}; KTC {{pilot.ci_level}} {{pilot.a1_vi_conflict_correct_ci}}), trùng giá trị nước ngoài {{pilot.a1_vi_conflict_foreign}}, không khớp giá trị đối chiếu nào {{pilot.a1_vi_conflict_unattributed}}, không trả lời {{pilot.a1_vi_conflict_abstain}}. Trên {{pilot.n_conflict_h1_atoms}} khuyến cáo có mồi: trùng nước ngoài {{pilot.a1_vi_h1_foreign}}, trùng mồi {{pilot.a1_vi_decoy}} (trả lời ngắn); trắc nghiệm {{pilot.mcq_a1_vi_foreign}} và {{pilot.mcq_a1_vi_decoy}} trên {{pilot.mcq_a1_vi_n}} câu. Trên {{pilot.a1_vi_drift_n}} khuyến cáo có bản cũ, {{pilot.a1_vi_drift_stale}} câu trùng giá trị bản cũ. Khi kèm đoạn hướng dẫn, số câu đúng là {{pilot.a3_vi_conflict_correct}}/{{pilot.a3_vi_conflict_n}} với khuyến cáo xung đột ({{pilot.a1a3_vi_conflict_improved}} câu tốt lên, {{pilot.a1a3_vi_conflict_worsened}} câu xấu đi; p = {{pilot.a1a3_vi_conflict_p}}) và {{pilot.a3_vi_concordant_correct}}/{{pilot.a3_vi_concordant_n}} với khuyến cáo trùng chuẩn quốc tế (không kèm: {{pilot.a1_vi_concordant_correct}}/{{pilot.a1_vi_concordant_n}}).

### KẾT LUẬN

Ở mô hình mở nhỏ này, phần lớn lỗi là giá trị không khớp nguồn nào đã ghi nhận; chưa thấy khuynh hướng theo chuẩn nước ngoài vượt mức trùng ngẫu nhiên. Kèm văn bản Bộ Y tế làm tăng số câu đúng nhưng vẫn còn sai. Kết quả sơ bộ trên mẫu chọn tay, kiểm bằng AI, chưa có bác sĩ duyệt; nghiên cứu chính sẽ kiểm định trên toàn kho hướng dẫn và nhiều mô hình mở.

### TỪ KHÓA

mô hình ngôn ngữ lớn; hướng dẫn điều trị; bộ y tế; đánh giá mô hình; giáo dục y khoa

## EN

### TITLE

Whose Standard of Care? Foreign-Guideline and Outdated-Version Deviations of LLMs from Vietnamese Ministry of Health Guidelines

### BACKGROUND

Students and health workers use large language models (LLMs) for clinical reference, but LLMs may answer with the values of foreign or superseded guidelines, whereas Vietnamese Ministry of Health (MoH) guidelines may differ in doses, thresholds and drugs.

### OBJECTIVE

To build a method that measures how LLM answers deviate from current MoH guidelines and classifies each error by source (a named foreign guideline, a superseded MoH version, or no recorded source), and to pilot it on a locally run open model.

### METHODS

Pilot on {{pilot.n_atoms}} recommendations with specific values quoted verbatim from official PDFs; {{pilot.n_atoms_analysed}} recommendations from {{pilot.n_guidelines_analysed}} documents still in force were analysed. Quotations were checked by two separate, blinded AI passes (Claude) with an AI referee. Recommendations carry versioned WHO, US and European values (when available), superseded values (when available) and a rule-generated decoy value (when the rule allows) to control for chance matches. Qwen3-8B (quantized, run on a laptop) answered in Vietnamese and English under three conditions: no country cue, "according to the MoH", and with the correct guideline passage. Answers were graded by pre-specified value-comparison rules, and all labels were re-checked by two blinded AI passes with an AI referee.

### RESULTS

For short answers, the rule-based grader matched the AI-adjudicated labels in {{pilot.grader_short_agree_pct|en}} (kappa {{pilot.grader_short_kappa|en}}). Under the MoH cue in Vietnamese, on {{pilot.a1_vi_conflict_n}} recommendations whose MoH value differs from at least one named foreign guideline, the model was correct in {{pilot.a1_vi_conflict_correct}} ({{pilot.a1_vi_conflict_correct_pct|en}}; {{pilot.ci_level}} CI {{pilot.a1_vi_conflict_correct_ci|en}}), matched a foreign value in {{pilot.a1_vi_conflict_foreign}}, matched no value in the reference set in {{pilot.a1_vi_conflict_unattributed}}, and {{pilot.a1_vi_conflict_abstain}} were graded as non-answers. On {{pilot.n_conflict_h1_atoms}} recommendations with a decoy, foreign versus decoy matches were {{pilot.a1_vi_h1_foreign}} versus {{pilot.a1_vi_decoy}} (short answers) and {{pilot.mcq_a1_vi_foreign}} versus {{pilot.mcq_a1_vi_decoy}} of {{pilot.mcq_a1_vi_n}} multiple-choice answers. On {{pilot.a1_vi_drift_n}} recommendations with a superseded version, {{pilot.a1_vi_drift_stale}} answers matched the superseded value. On recommendations concordant with international guidelines, {{pilot.a1_vi_concordant_correct}} of {{pilot.a1_vi_concordant_n}} were correct. With the guideline passage, correct answers were {{pilot.a3_vi_conflict_correct}} of {{pilot.a3_vi_conflict_n}} for conflict recommendations ({{pilot.a1a3_vi_conflict_improved}} improved, {{pilot.a1a3_vi_conflict_worsened}} worsened; p = {{pilot.a1a3_vi_conflict_p|en}}) and {{pilot.a3_vi_concordant_correct}} of {{pilot.a3_vi_concordant_n}} for concordant ones.

### CONCLUSION

For this small open model, most errors were values matching no recorded source, with no sign of foreign defaults beyond the decoy (chance) level. Supplying the MoH text increased correct answers, but errors remained. These are preliminary results on a hand-picked sample, checked by AI without clinician review; the main study will test them across the guideline corpus and several locally run open models.

### KEYWORDS

large language models; clinical practice guidelines; ministry of health; model evaluation; medical education

## GHI CHÚ

Bài chưa được đăng trên tạp chí khoa học trong nước hoặc quốc tế. Hình thức báo cáo: Oral.

## NOTE

This work has not been published in any national or international journal. Presentation format: Oral.

## ABSTRACT BOX

LLMs may answer with foreign or outdated guideline values instead of current Vietnamese Ministry of Health (MoH) guidelines. Pilot (hand-picked, AI-checked, no clinician review) on {{pilot.n_atoms_analysed}} recommendations: asked "according to the MoH" in Vietnamese, Qwen3-8B was correct on {{pilot.a1_vi_conflict_correct}}/{{pilot.a1_vi_conflict_n}} recommendations that differ from foreign guidelines and matched a foreign value {{pilot.a1_vi_conflict_foreign}} times (not above decoy level); most errors matched no source. With the guideline passage: {{pilot.a3_vi_conflict_correct}}/{{pilot.a3_vi_conflict_n}}.
