# Abstract FMC 2026 — bản rút gọn theo mức khuyến khích của mẫu (dự phòng)

Theo mẫu hướng dẫn viết abstract của hội nghị (manuscript/fmc/template/) và trả lời của Ban tổ chức (HG1.0): mỗi file một ngôn ngữ; độ dài theo mức khuyến khích của mẫu (giới hạn cứng ở src/vnsoc/fmc.py). Mọi số lấy từ registry (results/numbers.json) qua `vnsoc.numbers render` (bản tiếng Anh dùng `|en`); DOCX dựng bằng `vnsoc.fmc` từ chính file mẫu của hội nghị. Viết lại từ ba bản nháp, hai giám khảo và ba lượt kiểm đối kháng (agent AI), theo các báo cáo review/M1.

## Ô TÓM TẮT

Mô hình ngôn ngữ lớn có thể nêu liều, ngưỡng theo hướng dẫn nước ngoài hoặc bản cũ thay vì hướng dẫn hiện hành của Bộ Y tế. Thí điểm trên {{pilot.n_atoms_analysed}} khuyến cáo (chọn chủ đích, chỉ AI kiểm, chưa có bác sĩ duyệt): hỏi bằng tiếng Việt, nêu rõ Bộ Y tế, Qwen3-8B đúng {{pilot.a1_vi_conflict_correct}}/{{pilot.a1_vi_conflict_n}} khuyến cáo khác ít nhất một chuẩn nước ngoài; phần lớn câu sai không khớp nguồn đã ghi nhận; trùng chuẩn nước ngoài chưa rõ vượt mức trùng giá trị mồi. Kèm đoạn hướng dẫn: đúng {{pilot.a3_vi_conflict_correct}}/{{pilot.a3_vi_conflict_n}}, vẫn còn sai.

## VI

### TIÊU ĐỀ

Chuẩn điều trị của ai? Sai lệch của LLM theo chuẩn nước ngoài và phiên bản cũ so với hướng dẫn chuyên môn của Bộ Y tế Việt Nam

### ĐẶT VẤN ĐỀ

Mô hình ngôn ngữ lớn (LLM) có thể nêu liều, ngưỡng theo chuẩn nước ngoài hoặc bản cũ thay vì bản hiện hành của Bộ Y tế (BYT); mức độ, nguồn gốc chưa rõ.

### MỤC TIÊU

Thí điểm phương pháp đo và truy nguồn sai lệch.

### PHƯƠNG PHÁP NGHIÊN CỨU

Phân tích {{pilot.n_atoms_analysed}} khuyến cáo chọn chủ đích, trích nguyên văn từ {{pilot.n_guidelines_analysed}} văn bản BYT hiện hành. Đối chiếu: chuẩn nước ngoài có tên, bản BYT cũ (khi có), giá trị mồi (giá trị giả đặt trước, đo trùng ngẫu nhiên). Qwen3-8B (mô hình mở nhỏ) trả lời bằng tiếng Việt, tiếng Anh trong ba điều kiện: không nêu quốc gia, nêu BYT, kèm đoạn hướng dẫn. Chấm theo quy tắc định trước; chỉ AI kiểm lại đoạn trích, kết quả chấm.

### KẾT QUẢ

Hỏi bằng tiếng Việt, nêu BYT, trên {{pilot.a1_vi_conflict_n}} khuyến cáo khác ít nhất một chuẩn nước ngoài: đúng {{pilot.a1_vi_conflict_correct}} ({{pilot.a1_vi_conflict_correct_pct}}; KTC {{pilot.ci_level}}: {{pilot.a1_vi_conflict_correct_ci}}), trùng nước ngoài {{pilot.a1_vi_conflict_foreign}}, không khớp nguồn đã ghi nhận {{pilot.a1_vi_conflict_unattributed}}, bộ chấm không đọc được {{pilot.a1_vi_conflict_abstain}}. Trong đó {{pilot.n_conflict_h1_atoms}} có mồi: trùng nước ngoài {{pilot.a1_vi_h1_foreign}}, trùng mồi {{pilot.a1_vi_decoy}}. Trùng bản cũ: {{pilot.a1_vi_drift_stale}}/{{pilot.a1_vi_drift_n}} khuyến cáo khác có bản cũ. Kèm đoạn hướng dẫn: đúng {{pilot.a3_vi_conflict_correct}}/{{pilot.a3_vi_conflict_n}} (khám phá: McNemar p = {{pilot.a1a3_vi_conflict_p}}).

### KẾT LUẬN

Phần lớn câu sai không khớp nguồn đã ghi nhận; trùng chuẩn nước ngoài chưa rõ vượt mức ngẫu nhiên; kèm đoạn hướng dẫn vẫn còn sai. Kết quả sơ bộ, chưa có bác sĩ duyệt.

### TỪ KHÓA

mô hình ngôn ngữ lớn; hướng dẫn chẩn đoán và điều trị; bộ y tế; trí tuệ nhân tạo; đánh giá mô hình

## EN

### TITLE

Whose Standard of Care? Foreign-Guideline and Outdated-Version Deviations of LLMs from Vietnamese Ministry of Health Guidelines

### BACKGROUND

Large language models (LLMs) may state doses or thresholds from foreign or superseded guidelines instead of current Vietnamese Ministry of Health (MoH) guidelines; the extent and sources of such deviations are unclear.

### OBJECTIVE

To pilot a method for measuring these deviations and tracing their sources.

### METHODS

We analysed {{pilot.n_atoms_analysed}} purposively selected recommendations, quoted verbatim from {{pilot.n_guidelines_analysed}} MoH documents in force. Comparison values were named foreign guideline values, superseded MoH values (where available) and decoys (pre-specified false values for estimating chance matches). Qwen3-8B, a small open model, answered in Vietnamese and English under three conditions: no country cue, an explicit MoH cue, or the relevant MoH passage. Answers were graded using pre-specified rules; quotations and grades were rechecked by AI only.

### RESULTS

In Vietnamese with the MoH cue, for {{pilot.a1_vi_conflict_n}} recommendations differing from at least one named foreign guideline, {{pilot.a1_vi_conflict_correct}} answers were correct ({{pilot.a1_vi_conflict_correct_pct|en}}; {{pilot.ci_level}} CI {{pilot.a1_vi_conflict_correct_ci|en}}), {{pilot.a1_vi_conflict_foreign}} matched a foreign value, {{pilot.a1_vi_conflict_unattributed}} matched no recorded source, and in {{pilot.a1_vi_conflict_abstain}} the rule grader could not extract a value. Among the {{pilot.n_conflict_h1_atoms}} of these with a decoy, foreign versus decoy matches were {{pilot.a1_vi_h1_foreign}} versus {{pilot.a1_vi_decoy}}. For {{pilot.a1_vi_drift_n}} other recommendations with an older version, {{pilot.a1_vi_drift_stale}} answers matched the superseded value. With the MoH passage, {{pilot.a3_vi_conflict_correct}}/{{pilot.a3_vi_conflict_n}} were correct (exploratory McNemar p = {{pilot.a1a3_vi_conflict_p|en}}).

### CONCLUSION

Most errors matched no recorded source; foreign-guideline matches were not shown to exceed the chance (decoy) level; errors remained even with the MoH passage. These results are preliminary and have not been reviewed by clinicians.

### KEYWORDS

large language models; clinical practice guidelines; ministry of health; artificial intelligence; model evaluation

## GHI CHÚ

HÌNH THỨC BÁO CÁO: Oral
LĨNH VỰC: AI và Chuyển đổi số trong Y tế và Giáo dục Y khoa
GHI CHÚ: Bài chưa được đăng trên tạp chí khoa học trong nước hoặc quốc tế.

## NOTE

PRESENTATION FORMAT: Oral
TOPIC: AI and Digital Transformation in Healthcare and Medical Education
NOTE: This work has not been published in any national or international journal.

## ABSTRACT BOX

LLMs may give doses or thresholds from foreign or outdated guidelines instead of current Vietnamese Ministry of Health (MoH) guidelines. Pilot on {{pilot.n_atoms_analysed}} purposively selected recommendations (AI-checked only, no clinician review): asked in Vietnamese with an MoH cue, Qwen3-8B was correct on {{pilot.a1_vi_conflict_correct}}/{{pilot.a1_vi_conflict_n}} recommendations differing from a named foreign guideline; most errors matched no recorded source; foreign matches were not shown to exceed chance (decoy) level. With the MoH passage: {{pilot.a3_vi_conflict_correct}}/{{pilot.a3_vi_conflict_n}} correct.
