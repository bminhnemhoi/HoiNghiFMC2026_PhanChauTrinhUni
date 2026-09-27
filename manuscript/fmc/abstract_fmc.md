# Abstract FMC 2026 — bản đầy đủ theo mẫu hội nghị, trong giới hạn từ của Ban tổ chức

Theo mẫu hướng dẫn viết abstract của hội nghị (manuscript/fmc/template/) và trả lời của Ban tổ chức (HG1.0): mỗi file một ngôn ngữ; giới hạn tính theo số từ, mức trong mẫu chỉ là khuyến khích (giới hạn cứng ở src/vnsoc/fmc.py). Mọi số lấy từ registry (results/numbers.json) qua `vnsoc.numbers render` (bản tiếng Anh dùng `|en`); DOCX dựng bằng `vnsoc.fmc` từ chính file mẫu của hội nghị. Mở rộng từ bản rút gọn đã qua kiểm toán độc lập (agent AI), giữ các cách viết đã sửa; bổ sung theo các báo cáo review/M1: mốc đối chứng, trắc nghiệm có mồi kèm cảnh báo cắt cụt, kiểm định ghép cặp ở hai ngôn ngữ (khám phá), độ nhạy theo nhãn AI phân xử; bỏ độ khớp của bộ chấm cho vừa giới hạn (sẽ nêu trong slide và bài báo); hướng viết: ý nghĩa với lâm sàng và giáo dục y khoa.

## Ô TÓM TẮT

Mô hình ngôn ngữ lớn có thể nêu liều, ngưỡng theo hướng dẫn nước ngoài hoặc bản cũ thay vì hướng dẫn hiện hành của Bộ Y tế. Thí điểm trên {{pilot.n_atoms_analysed}} khuyến cáo (chọn chủ đích, chỉ AI kiểm, chưa có bác sĩ duyệt): hỏi bằng tiếng Việt, nêu rõ Bộ Y tế, Qwen3-8B đúng {{pilot.a1_vi_conflict_correct}}/{{pilot.a1_vi_conflict_n}} khuyến cáo khác ít nhất một chuẩn nước ngoài; phần lớn câu sai không khớp nguồn đã ghi nhận; chưa cho thấy trùng chuẩn nước ngoài vượt mức trùng giá trị mồi. Kèm đoạn hướng dẫn: đúng {{pilot.a3_vi_conflict_correct}}/{{pilot.a3_vi_conflict_n}}, vẫn còn sai.

## VI

### TIÊU ĐỀ

Chuẩn điều trị của ai? Sai lệch của LLM theo chuẩn nước ngoài và phiên bản cũ so với hướng dẫn chuyên môn của Bộ Y tế Việt Nam

### ĐẶT VẤN ĐỀ

Mô hình ngôn ngữ lớn (LLM) có thể nêu liều thuốc hoặc ngưỡng chẩn đoán theo chuẩn nước ngoài hoặc phiên bản cũ thay vì hướng dẫn hiện hành của Bộ Y tế (BYT). Con số có thật ở hướng dẫn khác nên khó nhận ra. Mức độ và nguồn gốc sai lệch chưa rõ.

### MỤC TIÊU

Thí điểm phương pháp đo tỉ lệ đúng và truy nguồn câu sai (đối chiếu mức trùng ngẫu nhiên), theo ngôn ngữ và điều kiện hỏi.

### PHƯƠNG PHÁP NGHIÊN CỨU

Thiết kế thí điểm: phân tích {{pilot.n_atoms_analysed}} khuyến cáo chọn chủ đích (trong {{pilot.n_atoms}}) thuộc {{pilot.n_guidelines_analysed}} văn bản BYT còn hiệu lực, trích nguyên văn kèm số trang. Ba nhóm: xung đột ({{pilot.n_conflict_atoms}}, khác ít nhất một chuẩn nước ngoài có tên; trong đó {{pilot.n_conflict_h1_atoms}} có mồi: giá trị sai đặt trước, để ước tính mức trùng ngẫu nhiên), phiên bản ({{pilot.n_drift_atoms}}, có bản BYT cũ), đối chứng ({{pilot.n_concordant_atoms}} khuyến cáo còn lại, trùng chuẩn nước ngoài). Qwen3-8B (mô hình mở nhỏ, lượng tử hóa bốn bit, chạy trên laptop) trả lời ngắn bằng tiếng Việt và tiếng Anh ở ba điều kiện: không nêu quốc gia, nêu BYT, kèm đoạn hướng dẫn. Chấm theo quy tắc định trước; chỉ AI (Claude) kiểm tra đoạn trích và {{pilot.grader_short_n}} câu trả lời ngắn (hai lượt chấm mù, AI phân xử, cho phân tích độ nhạy). Khoảng tin cậy (KTC) {{pilot.ci_level}} Clopper–Pearson; kiểm định McNemar chính xác ghép cặp giữa nêu BYT và kèm đoạn (khám phá, thêm sau khi mở kết quả).

### KẾT QUẢ

Tiếng Việt, nêu BYT: nhóm xung đột đúng {{pilot.a1_vi_conflict_correct}}/{{pilot.a1_vi_conflict_n}} (KTC {{pilot.ci_level}}: {{pilot.a1_vi_conflict_correct_ci}}); {{pilot.a1_vi_conflict_foreign}} trùng chuẩn nước ngoài, {{pilot.a1_vi_conflict_unattributed}} không khớp nguồn đã ghi nhận, {{pilot.a1_vi_conflict_abstain}} câu bộ chấm không đọc được giá trị (phân tích độ nhạy: đúng {{pilot.adj_a1_vi_conflict_correct}}/{{pilot.adj_a1_vi_conflict_n}}); nhóm đối chứng đúng {{pilot.a1_vi_concordant_correct}}/{{pilot.a1_vi_concordant_n}}; nhóm phiên bản {{pilot.a1_vi_drift_stale}}/{{pilot.a1_vi_drift_n}} trùng bản cũ. Ở {{pilot.n_conflict_h1_atoms}} khuyến cáo có mồi: {{pilot.a1_vi_h1_foreign}} trùng chuẩn nước ngoài, {{pilot.a1_vi_decoy}} trùng mồi. Nhóm xung đột, tiếng Việt: không nêu quốc gia đúng {{pilot.a0_vi_conflict_correct}}/{{pilot.a0_vi_conflict_n}}; kèm đoạn {{pilot.a3_vi_conflict_correct}}/{{pilot.a3_vi_conflict_n}}; so với nêu BYT: {{pilot.a1a3_vi_conflict_improved}} sai thành đúng, {{pilot.a1a3_vi_conflict_worsened}} đúng thành sai (McNemar, khám phá: p = {{pilot.a1a3_vi_conflict_p}}). Cùng nhóm, tiếng Anh, ba điều kiện, đúng: {{pilot.a0_en_conflict_correct}}/{{pilot.a0_en_conflict_n}}, {{pilot.a1_en_conflict_correct}}/{{pilot.a1_en_conflict_n}}, {{pilot.a3_en_conflict_correct}}/{{pilot.a3_en_conflict_n}} (McNemar, khám phá: p = {{pilot.a1a3_en_conflict_p}}).

### KẾT LUẬN

Phần lớn câu sai không khớp nguồn đã ghi nhận; chưa cho thấy trùng chuẩn nước ngoài vượt mức trùng mồi. Khi nêu BYT, nhóm đối chứng cũng đúng chưa đến một nửa. Kèm đoạn, đúng nhiều hơn nhưng vẫn còn sai; người học và thầy thuốc cần đối chiếu con số LLM đưa ra với hướng dẫn BYT hiện hành. Hạn chế: mẫu nhỏ chọn chủ đích, một mô hình, chỉ AI kiểm tra, chưa có bác sĩ duyệt, nhiều mồi kém hợp lý; câu đúng có thể trùng chuẩn nước ngoài khác. Tiếp theo: nghiên cứu chính (sẽ đăng ký trước) trên kho hướng dẫn BYT hiện hành, nhiều mô hình mở.

### TỪ KHÓA

mô hình ngôn ngữ lớn; hướng dẫn chẩn đoán và điều trị; bộ y tế; trí tuệ nhân tạo; đánh giá mô hình

## EN

### TITLE

Whose Standard of Care? Foreign-Guideline and Outdated-Version Deviations of LLMs from Vietnamese Ministry of Health Guidelines

### BACKGROUND

Large language models (LLMs) may give drug doses or diagnostic thresholds from foreign or superseded guidelines instead of current Vietnamese Ministry of Health (MoH) guidelines; because such values exist in other guidelines, learners and clinicians may not notice. The extent and sources of these deviations are unclear.

### OBJECTIVE

To pilot a method that measures how often an LLM gives the current MoH value, traces wrong answers to their sources, benchmarked against a chance-match level, and compares question languages and prompting conditions.

### METHODS

Pilot design: we analysed {{pilot.n_atoms_analysed}} purposively selected recommendations (of {{pilot.n_atoms}}) from {{pilot.n_guidelines_analysed}} MoH documents in force, quoted verbatim with page numbers. Three groups: conflict ({{pilot.n_conflict_atoms}}; differing from at least one named foreign guideline; {{pilot.n_conflict_h1_atoms}} of these had a decoy, a pre-specified false value for estimating chance matches), version ({{pilot.n_drift_atoms}}; each with an older MoH version) and concordant (the remaining {{pilot.n_concordant_atoms}}; matching foreign guidelines). Qwen3-8B (a small open model, four-bit quantised, run on a laptop) gave short answers in Vietnamese and English under three conditions: no country cue, an MoH cue and the relevant MoH passage. Answers were graded by pre-specified rules; only an AI (Claude) checked the quotations and all {{pilot.grader_short_n|en}} short answers (two blinded passes with an AI referee, used for a sensitivity analysis). Statistics: Clopper–Pearson {{pilot.ci_level|en}} confidence intervals (CIs); exact McNemar tests pairing the MoH-cue and passage conditions (exploratory; added post hoc, after the sealed outputs were opened).

### RESULTS

In Vietnamese with the MoH cue, {{pilot.a1_vi_conflict_correct}}/{{pilot.a1_vi_conflict_n}} conflict-group answers were correct ({{pilot.ci_level|en}} CI {{pilot.a1_vi_conflict_correct_ci|en}}); {{pilot.a1_vi_conflict_foreign}} matched a foreign value, {{pilot.a1_vi_conflict_unattributed}} matched no recorded source, and in {{pilot.a1_vi_conflict_abstain}} the rule grader could not read a value (sensitivity analysis with AI-adjudicated labels: {{pilot.adj_a1_vi_conflict_correct}}/{{pilot.adj_a1_vi_conflict_n}} correct). With the same cue, {{pilot.a1_vi_concordant_correct}}/{{pilot.a1_vi_concordant_n}} concordant answers were correct and {{pilot.a1_vi_drift_stale}}/{{pilot.a1_vi_drift_n}} version-group answers matched a superseded MoH value. Among the {{pilot.n_conflict_h1_atoms}} recommendations with a decoy, {{pilot.a1_vi_h1_foreign}} answers matched a foreign value and {{pilot.a1_vi_decoy}} matched the decoy. In the conflict group in Vietnamese, {{pilot.a0_vi_conflict_correct}}/{{pilot.a0_vi_conflict_n}} answers were correct without a country cue and {{pilot.a3_vi_conflict_correct}}/{{pilot.a3_vi_conflict_n}} with the passage; versus the MoH cue, {{pilot.a1a3_vi_conflict_improved}} changed from wrong to correct and {{pilot.a1a3_vi_conflict_worsened}} from correct to wrong (exploratory McNemar p = {{pilot.a1a3_vi_conflict_p|en}}). In the same group in English, the three conditions gave {{pilot.a0_en_conflict_correct}}/{{pilot.a0_en_conflict_n}}, {{pilot.a1_en_conflict_correct}}/{{pilot.a1_en_conflict_n}} and {{pilot.a3_en_conflict_correct}}/{{pilot.a3_en_conflict_n}} correct answers (exploratory McNemar p = {{pilot.a1a3_en_conflict_p|en}}).

### CONCLUSION

Most wrong answers matched no recorded source, and foreign-guideline matches were not shown to exceed the chance (decoy) level. With the MoH cue, the concordant group also had fewer than half of its answers correct. With the MoH passage, more answers were correct but errors remained; learners and clinicians should check any value an LLM states against the current MoH guideline. Limitations: small purposive sample, one model, AI-only checking, no clinician review, many decoys rated implausible by AI; a correct answer may also coincide with a foreign value. Next: a main study, to be pre-registered, on the current MoH guideline corpus with several open models.

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
