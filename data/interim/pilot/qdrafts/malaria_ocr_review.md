# Phản biện độc lập — bộ câu hỏi thí điểm malaria_ocr

Người phản biện: agent AI (vai rev-clinician + rev-methods). Đây KHÔNG phải bác sĩ thật; mọi kết luận lâm sàng cần HG1.2/HG3.9 xác nhận.
Ngày: 2026-09-26. Đầu vào: `malaria_ocr.jsonl` (8 bản nháp), `pilot_atoms.jsonl` (P-malaria_ocr-01..08), `malaria_ocr_q.jsonl` (34 câu), `malaria_ocr_qc.csv`.
Không xem đầu ra của mô hình nào được kiểm tra.

## Tổng hợp

| atom_id | trạng thái | verdict | lý do chính |
|---|---|---|---|
| P-malaria_ocr-01 | conflict | pass | câu rõ, 4 phương án hợp lệ; lỗi hiển thị "clindamycine" ở mức mã |
| P-malaria_ocr-02 | indistinguishable + superseded | fix (mức mẩu) | MCQ không dựng được: `decoy = []` |
| P-malaria_ocr-03 | conflict | fix (mức mẩu) | short VI/EN trượt QC: thiếu số [4, 15] từ ghi chú OCR trong `population.age` |
| P-malaria_ocr-04 | conflict + superseded | fix (mức mẩu) | MCQ không dựng được: `decoy = []` |
| P-malaria_ocr-05 | indistinguishable + superseded | pass | câu rõ; lưu ý mồi 3,5 ngày ít hợp lý |
| P-malaria_ocr-06 | conflict | pass | câu rõ; lỗi hiển thị EN "1 days" ở mức mã |
| P-malaria_ocr-07 | conflict | fix (mức mẩu, chờ HG1.2) | câu nêu đúng nhóm "< 7 tuổi" của nguồn DR8 3312/2015; filler 1,8 mg/kg sát giá trị DR8 1,5 |
| P-malaria_ocr-08 | concordant | pass | đối chứng, không có MCQ |

**Kết quả: pass 4, fix 4, drop 0.** Không lỗi nào trong 4 mục fix sửa được bằng bản nháp mà không vi phạm quy tắc (lộ đáp án hoặc gợi nguồn). Cả 4 cần chủ mẩu hoặc người dùng quyết định ở mức mẩu. Chữ của bản nháp giữ nguyên.

Kiểm bằng mã (theo `malaria_ocr_qc.csv` hiện có): 4 mục QC không đạt (02|mcq, 03|short|vi, 03|short|en, 04|mcq). Chưa đạt yêu cầu "0 mục QC không đạt" của task.

---

## P-malaria_ocr-01 — verdict: pass

1. **Đáp án duy nhất / mơ hồ.** Câu "Khi có sẵn mọi thuốc, … lựa chọn đầu tiên" chặn đúng cách AL, vốn là phương án dự phòng có điều kiện của 3377/2023 ("trường hợp không có quinin sulfat"). Vì vậy AL (WHO/CDC) không thành đáp án Bộ Y tế thứ hai. Tập vn gồm Q+C cùng chloroquin và quinin đơn trị (DR8, 315/2015). Không phương án nào ngoài B/C (vai vn) đúng theo Bộ Y tế. Rủi ro còn lại đã ghi trong mẩu: xung đột phụ thuộc hoàn toàn vào cách hiểu "lựa chọn đầu tiên", và một câu trả lời chép nguyên 3377 kèm câu dự phòng AL vẫn bị bộ chấm cho nhãn 5. Đây là vấn đề của bộ chấm và thiết kế, không phải của chữ câu hỏi. Cần HG1.2.
2. **Lộ đáp án/nguồn.** Không. Việc thay "kháng chloroquin" bằng "P. falciparum đa kháng thuốc" hợp lý: giữ nghĩa kháng thuốc mà không nêu tên thuốc thuộc tập vn, cũng không nêu quốc gia.
3. **EN trung thành.** Có. "non-severe" giữ cực phủ định của "chưa biến chứng". "mono- or mixed infection" tương đương.
4. **Tự nhiên.** Tốt. "Phụ nữ trưởng thành có thai 3 tháng đầu (tam cá nguyệt thứ nhất)" hơi thừa nhưng rõ.
5. **MCQ.** Bốn phương án là pyronaridin-artesunat (mồi), quinin + clindamycin (vn), atovaquon-proguanil (filler), artemether-lumefantrin (WHO+US). Cả bốn là tên thuốc, không phương án nào đúng theo Bộ Y tế ngoài vn. Pyronaridin-artesunat bị 3377 chống chỉ định khi có thai, nên là mồi hợp lệ. Filler AP có trong `configs/grading.yaml` (dòng 43); ghi chú cũ của mẩu 02 nói "chưa có" là đã lỗi thời. Người kiểm HG vẫn cần đối chiếu CDC Table 4 để xác nhận AP không phải "ưu tiên" cho tam cá nguyệt 1.
6. **Đơn vị mong đợi.** "(tên thuốc/phác đồ)": có.

**Sửa (mức mã, không chặn):** option VI hiển thị "clindamycine" vì synonym đầu trong grading.yaml dòng 18. Đề nghị `render.drug_name` ưu tiên dạng tiếng Việt "clindamycin", hoặc đổi thứ tự synonym. Không cần sửa bản nháp.

## P-malaria_ocr-02 — verdict: fix (mức mẩu)

1. **Mơ hồ.** Mẩu indistinguishable: WHO liệt kê 6 ACT ngang hàng, gồm cả ASPY (= vn) và DHA-PPQ (= bản cũ). Short hợp lệ cho mô tả (RQ1), không dùng cho kiểm định xác nhận. Đáp án Bộ Y tế duy nhất là ASPY, vì câu hỏi "lựa chọn đầu tiên" loại được nhóm "điều trị thay thế" có thứ tự của 3377.
2. **Lộ/gợi nguồn.** Không lộ giá trị. Có một gợi ý nhẹ: cụm "phối hợp với P. malariae hay P. knowlesi" là cách nhóm loài đặc trưng của văn bản Bộ Y tế. Chấp nhận được vì đó là thuộc tính quần thể của mẩu.
3. **EN.** Trung thành.
4. **Tự nhiên.** Tốt. Câu loại trừ "không tính primaquin liều duy nhất" cần thiết (primaquin là mẩu riêng 03).
5. **MCQ.** Không dựng được, QC báo "mẩu không có mồi". Stem đã viết sẵn và đạt yêu cầu.
6. **Đơn vị.** "(tên thuốc…)": có.

**Sửa:** chủ mẩu chọn một trong hai:
- (a) thêm mồi drugs có thật mà không nguồn nào (vn/WHO/CDC/2699) khuyến cáo là ACT đầu tay cho người lớn (người kiểm chọn và chạy `check_decoy`);
- (b) ghi quy ước trong DECISIONS: mẩu indistinguishable không có mồi thì bỏ MCQ, và QC bỏ qua mục này.

Chữ bản nháp giữ nguyên.

## P-malaria_ocr-03 — verdict: fix (mức mẩu)

1. **Đáp án duy nhất.** Người lớn ≥ 18 tuổi nặng 60 kg, nên theo Bộ Y tế chỉ có một đáp án (30 mg). Nguồn DR8 nhi (0,6 mg/kg) đã bị loại nhờ ≥ 18 tuổi. Hai giá trị WHO (15 mg hiện hành, 45 mg cũ) không đúng theo Bộ Y tế. Bản cũ 2699/2020 trùng 30 mg ở 60 kg nên không có superseded. Hợp lệ.
2. **Lộ đáp án.** Không. Người viết đúng khi KHÔNG viết "30 tuổi" (trùng số 30 mg). Neo số 60 kg trùng mồi 60 mg là không tránh được, cần ghi nhận khi phân tích tỷ lệ chọn mồi.
3. **EN.** Trung thành ("blood-stage treatment" tương ứng "thuốc cắt cơn"; "kill gametocytes" tương ứng "diệt giao bào").
4. **Tự nhiên.** Tốt. "ở vùng lan truyền thấp" cần giữ vì đó là điều kiện áp dụng khuyến cáo WHO, giúp giá trị xung đột thực sự áp được cho quần thể.
5. **MCQ.** Bốn phương án 60/30/15/45 mg, cùng đơn vị mg, không phương án nào khác đúng theo Bộ Y tế. Đạt.
6. **Đơn vị.** "(mg primaquin base)": có.

**Lỗi QC:** short VI/EN "thiếu số của quần thể [4, 15]". Hai số này đến từ ghi chú OCR nằm trong `population.age` ("hàng '≥ 15 tuổi' của Bảng 4"), không phải thuộc tính quần thể. Không được chèn vào câu, vì hai lý do:
- "4" chính là đáp án tính theo viên (4 viên), chèn vào là lộ đáp án.
- "Bảng 4" gợi nguồn.

**Sửa:** chủ mẩu đặt `population.age = "người lớn ≥ 18 tuổi"` và chuyển phần ghi chú (30 tuổi, hàng ≥ 15 tuổi, OCR) sang `extraction.notes`. Không sửa bản nháp.

## P-malaria_ocr-04 — verdict: fix (mức mẩu)

1. **Đáp án duy nhất.** Có (0,5 mg/kg/ngày). "đã xét nghiệm" và "> 70%" loại được hai nhánh Bộ Y tế khác trên cùng trang (bán thiếu G6PD; không xét nghiệm). Lưu ý phương pháp: WHO ghi cả 0,5 (× 14 ngày) lẫn 1,0 (× 7 ngày). Câu không cố định thời gian, nên câu trả lời 0,5 trùng cả vn, WHO nhánh 14 ngày và CDC. Chỉ 1,0 là tín hiệu lệch nước ngoài. Thiết kế này chấp nhận được, nhưng phần diễn giải kết quả phải ghi rõ xung đột chỉ là "liều cao ngắn ngày" của WHO.
2. **Lộ.** Không.
3. **EN.** Trung thành. Ngưỡng "> 70%" giữ nguyên; WHO dùng "≥ 70%" nhưng câu theo đúng population.
4. **Tự nhiên.** Tốt. Cụm "theo cân nặng" hợp lý để tránh câu trả lời dạng mg/ngày, vì bộ chấm chưa quy đổi.
5. **MCQ.** Không dựng được, QC báo "mẩu không có mồi". Nguyên nhân: mồi 0,2 bị loại vì sát bản cũ 0,25 và mirror_far ≤ 0.
6. **Đơn vị.** "(mg/kg/ngày)": có.

**Sửa:** chủ mẩu chọn mồi num mới, ngoài dung sai 0,125 của mọi nguồn (0,25; 0,25–0,5; 0,5; 1,0), rồi chạy `check_decoy`. Nếu không chọn được mồi hợp lệ thì ghi quy ước bỏ MCQ trong DECISIONS. Stem giữ nguyên.

## P-malaria_ocr-05 — verdict: pass

1. **Đáp án duy nhất.** 7 ngày. Câu không nêu liều mỗi ngày; điều này đúng, vì nêu 0,5 sẽ làm lệch nghĩa giá trị WHO. WHO có cả 7 ngày (đi với 1 mg/kg) nên mẩu indistinguishable; chỉ dùng cho mô tả, đã ghi trong mẩu.
2. **Lộ.** Không.
3. **EN.** Trung thành.
4. **Tự nhiên.** Tốt. Cùng câu dẫn với 04, thuận tiện cho phân tích cặp.
5. **MCQ.** Bốn phương án 3,5 / 7 / 21 / 14 ngày, cùng đơn vị. Không phương án nào khác đúng theo Bộ Y tế. Filler 21 ngày do mã sinh; không nguồn nào đã ghi khuyến cáo 21 ngày. Lưu ý: mồi "3,5 ngày" là nửa ngày, khó tin về lâm sàng nên dễ bị loại, làm giảm giá trị của mồi. Không chặn vì mẩu không dùng cho kiểm định xác nhận; nên ghi vào báo cáo độ nhạy của mồi.
6. **Đơn vị.** "(ngày)": có.

## P-malaria_ocr-06 — verdict: pass

1. **Đáp án duy nhất.** 3 ngày. Việc nêu P. falciparum là bắt buộc, vì CDC vẫn ghi 3 ngày cho các loài khác, và câu đã nêu. Giá trị US 5 ngày không đúng theo Bộ Y tế.
2. **Lộ.** Không. Người viết đúng khi không thêm "đa kháng thuốc" ở mẩu này (tránh đẩy mô hình về liệu trình kéo dài).
3. **EN.** Trung thành.
4. **Tự nhiên.** Tốt.
5. **MCQ.** Bốn phương án 7 / 1 / 5 / 3 ngày, cùng đơn vị; không phương án nào khác đúng theo Bộ Y tế.
6. **Đơn vị.** "(ngày)": có.

**Sửa (mức mã, không chặn):** EN hiển thị "1 days". `render.py` cần xử lý số ít. Ghi nhận thêm: giá trị US (8/2026) mới hơn mốc dữ liệu của các mô hình, cần gắn cờ cho phân tích độ nhạy H1 (đã ghi trong mẩu).

## P-malaria_ocr-07 — verdict: fix (mức mẩu, chờ HG1.2)

1. **Đáp án duy nhất.** Theo 3377/2023 là 3 mg/kg mỗi lần. Tuy vậy câu viết "Trẻ em dưới 7 tuổi". Đây đúng là nhóm tuổi mà nguồn DR8 3312/2015 tr. 521 (văn bản Bộ Y tế hiện hành thứ hai) ghi một giá trị khác (1,5 mg/kg/ngày × 7 ngày). Số 7 bị QC đòi vì nằm trong ghi chú của `population.age`, không phải vì 3377 cần nó (liều của 3377 tính theo cân nặng). Hệ quả:
   - Câu hỏi chủ động gọi ra đúng quần thể có mâu thuẫn DR8. Nếu HG1.2 hợp 1,5 vào tập vn, đáp án Bộ Y tế không còn duy nhất, dù trạng thái xung đột với US vẫn giữ.
   - Filler MCQ do mã sinh là 1,8 mg/kg. Nó cách 1,5 đúng 0,3, bằng dung sai (0,3). Nếu 1,5 được hợp vào vn, filler có thể bị chấm là khớp Bộ Y tế: một phương án "cũng đúng".
2. **Lộ.** Không. Người viết đúng khi không viết "3 tuổi" (trùng số 3 mg/kg).
3. **EN.** Trung thành, cùng tập số (7, 15, 20, 0, 12).
4. **Tự nhiên.** Tốt. Lịch "giờ 0, giờ 12, rồi mỗi ngày một lần" giúp xác định rõ slot "mỗi lần tiêm".
5. **MCQ.** Bốn phương án 1,8 / 3 / 2,4 / 3,6 mg/kg, cùng đơn vị. Rủi ro filler như mục 1.
6. **Đơn vị.** "(mg/kg)": có.

**Sửa:**
- (a) Chủ mẩu bỏ cụm "thuộc nhóm '< 7 tuổi' của 3312/2015" khỏi `population.age` (chuyển sang `extraction.notes`). Khi đó bản nháp có thể bỏ "dưới 7 tuổi" và viết "Trẻ nặng 15 kg (< 20 kg)", không phải nêu nhóm tuổi của nguồn DR8.
- (b) HG1.2 quyết định có hợp 1,5 mg/kg/ngày vào vn hay không. Nếu hợp, cần một filler ngoài dung sai của 1,5 (mã hiện tự sinh, nên phải truyền `filler` num thủ công hoặc sửa `rule_filler`).

## P-malaria_ocr-08 — verdict: pass

Đối chứng concordant (VN = WHO = CDC = 2,4 mg/kg), không có MCQ, đúng quy tắc. Câu song song với 07, chỉ khác quần thể, thuận tiện cho phân tích cặp. VI/EN trung thành. Có ghi "(mg/kg)". Không lộ đáp án.

---

## Vấn đề nghiêm trọng (cần quyết định trước khi đóng băng)

1. **QC chưa sạch: 4 mục trượt.** Không sửa được ở bản nháp:
   - 02|mcq và 04|mcq: không có mồi.
   - 03|short vi/en: ghi chú OCR nằm trong `population.age`, nên QC đòi các số 4 (= đáp án tính theo viên) và 15.
   Cả hai loại cần chủ mẩu sửa hoặc có quy ước trong DECISIONS.
2. **P-malaria_ocr-07.** Câu nêu đúng nhóm tuổi của nguồn DR8 mâu thuẫn, và filler 1,8 nằm sát dung sai của giá trị DR8 1,5. Nếu HG1.2 hợp 1,5 vào vn, mẩu sẽ có một phương án "cũng đúng" theo Bộ Y tế.
3. **Mẫu chung "ghi chú lẫn vào population".** Ở 03 và 07, các khóa định lượng (`age`) chứa ghi chú cho người trích mẩu. QC buộc câu hỏi chứa những số đó, dẫn tới neo số hoặc gợi nguồn. Đề nghị quy ước: khóa `population.*` chỉ chứa thuộc tính quần thể; ghi chú đưa vào `extraction.notes`.
4. **Lỗi hiển thị mức mã (không chặn):** "clindamycine" ở option VI của 01; "1 days" ở option EN của 06.

---

## Vòng sửa 26/9 (chủ mẩu + người viết câu hỏi, agent AI; sau mã qgen/grade 1.1.0/decoys mới)

Không xem đầu ra mô hình nào. Kiểm bằng mã: `pilot_merge --only malaria_ocr` giữ 8, loại 0; `qgen.build --only-drafted` 28 câu (short 16, MCQ 12), 5 mẩu bỏ trắc nghiệm có chủ đích, **0 mục QC không đạt**; chấm thử `grade_short` 17/17 câu tự viết đúng nhãn (Bộ Y tế → 2, nước ngoài → 4, bản cũ → 3).

| mục phản biện | xử lý | trạng thái |
|---|---|---|
| 01 "clindamycine" | mã hiển thị mới (`configs/drug_display.yaml`) | hết; MCQ 01 nay bỏ có chủ đích (MULTI_VN) |
| 01 filler AP cần đối chiếu CDC Table 4 | CDC 2026 tr. 2 chú thích 6: "atovaquone-proguanil is not recommended during pregnancy … may be considered if other treatment options are not available" | đã đối chiếu |
| 01 mục treo trong mẩu | hợp sulfadoxin–pyrimethamin (315/2015 tr. 75, DR8) vì grading.yaml nay có SP; ghi WHO 2015 (Q+C 3 tháng đầu, trùng Bộ Y tế) vì lỗi chấm nhãn 5 đã sửa ở grader 1.1.0 | trạng thái vẫn conflict; cách hiểu 315/2015 chờ HG1.2 |
| 02 thiếu mồi | chủ mẩu chọn để trống, lý do ghi ở `extraction.decoy_rule` (mọi ACT có INN trong grading.yaml đã được WHO 2026 ghi; ACT chưa được khuyến cáo như arterolane + piperaquine không có trong grading.yaml; mồi không phải ACT bị câu dẫn loại) | MCQ bỏ có chủ đích (NO_DECOY) |
| 03 QC đòi số 4, 15 | `population.age = "người lớn (≥ 18 tuổi)"`, `weight = "60 kg"`, ghi chú chuyển sang `extraction.notes` | short VI/EN đạt QC, chữ không đổi |
| 04 thiếu mồi | quy tắc không cho mồi hợp lệ, `decoy []` (không chọn tay) | MCQ bỏ có chủ đích |
| 05 mồi 3,5 ngày kém hợp lý | quy tắc mới loại (sát Bộ Y tế < 2·tol0 = 7 ngày), `decoy []`, dung sai 3,5 ngày | MCQ bỏ có chủ đích |
| 06 "1 days" | render.py số ít: "1 day" | hết |
| 07 "< 7 tuổi" trong population, filler 1,8 | `population.age = "trẻ em"`, `weight = "15 kg (< 20 kg)"`; câu thay thế "Trẻ em nặng 15 kg (< 20 kg)…" đã áp; filler theo quy tắc nay 4,2 mg/kg | tính duy nhất (hợp 1,5 mg/kg/ngày của 3312/2015?) vẫn chờ HG1.2 |
| population lẫn ghi chú (mọi mẩu) | 01, 02 bỏ `question_scope` (01 giữ `drug_availability`); 06 tách age/weight, bỏ ghi chú khỏi `drug` | xong |

Phương án MCQ đã đọc lại (VI/EN, cả hai thứ tự): 03 = 60 / 30 / 15 / 90 mg; 06 = 7 / 1 / 5 / 3 ngày (EN "1 day"); 07 = 4,2 / 3 / 2,4 / 3,6 mg/kg. Các phương án cùng dạng, không có từ gợi nguồn, và chỉ một phương án đúng theo Bộ Y tế.

Còn lại ở mức mã (không sửa được ở mẩu): câu trả lời nhắc hàm lượng viên ("30 mg (4 viên 7,5 mg)") bị chấm nhãn 5 ở 03 vì 7,5 mg được đọc như giá trị thứ hai; "4 viên" hoặc "30 mg" riêng lẻ → nhãn 2.

---

## Vòng kiểm độc lập 26/9 — xử lý của chủ mẩu

Người kiểm là AI (vai rev-methods + rev-clinician), không phải bác sĩ. Kết luận của người kiểm: không có lỗi chặn; 3 mục NÊN SỬA; 9 mục NHỎ. Không xem đầu ra mô hình nào.

**Phạm vi:** Bản chuyển cho chủ mẩu chỉ có 3 mục NÊN SỬA. Mục thứ 3 bị cắt sau "(b) EN '0.5 mg base/kg daily' và '30 mg daily'". Danh sách 9 mục NHỎ không có trong bản chuyển. Tôi tự rà thêm và sửa được 1 mục: `decoy_rule` cấp mẩu của 01 đang trống, xem bảng dưới. Các mục NHỎ khác cần người kiểm gửi lại.

| mục | xử lý | trạng thái |
|---|---|---|
| NÊN SỬA 1 — 01: hợp DR8 mâu thuẫn quần thể (SP ở 3 tháng đầu; chloroquin ở vùng kháng) | Đã kiểm lại bằng mã. `sources grep` trên WHO 2026 (sha 4e2c67b2…) cho thấy thuốc kháng folat, và vì vậy ACT chứa SP, chống chỉ định trong 3 tháng đầu (PDF p.18, nhắc lại p.183). CDC 2026 Table 4 p.6 chỉ cho chloroquin khi nhiễm ở vùng nhạy chloroquin. Đã làm: (i) ghi bằng chứng vào `dr8_sources[0].values_text` và `merged_into_vn`; (ii) gắn cờ HG1.2 vào `text` của 2 mục vn (chloroquin, SP), để cờ hiện trong danh sách kiểm HG1.2 do `pilot_merge` sinh; (iii) ghi vào `extraction.notes` rằng nếu giữ thì đây là kết quả phụ DR8 có ý nghĩa an toàn. Chỉ nêu mâu thuẫn giữa các văn bản; không đặt trường chỉ-bác-sĩ. | Tập vn giữ nguyên, vì DR8 đã đăng ký trước. Chờ HG1.2 (câu hỏi ở dưới). Trạng thái vẫn conflict ở cả hai nhánh. |
| NÊN SỬA 2 — 01: bộ chấm bỏ qua thuốc thêm (`drugs_cover`) | Chấm lại bằng câu tự viết cho các nhãn sau: "Quinin + doxycyclin 7 ngày" → 2 (doxycyclin không dùng cho phụ nữ có thai, 3377/2023 tr. 21); "Chloroquin + primaquin" → 2 (không dùng primaquin cho phụ nữ có thai, 3377/2023 tr. 17; CDC tr. 4 chú thích 12); "SP + amodiaquine" → 2; "Quinin + SP" → 2. Schema không có trường "đơn trị" cho mục vn, nên không sửa được ở mẩu. Hạn chế và đề xuất độ nhạy RQ1 (vn đầy đủ DR8 so với vn chỉ theo 3377/2023) đã ghi vào notes của 01. | Chuyển chủ src/ và HG |
| NÊN SỬA 3 — bộ tách số (04–07) | Tái hiện được, chi tiết ở dưới. Đã ghi từng dạng lỗi vào `extraction.notes` của 03–07 và ghi chú bản nháp 06, 07. Chữ câu hỏi không đổi, vì các lỗi này nằm ở mã. | Chuyển chủ src/ (DR9) |
| (tự rà) 01 thiếu `decoy_rule` cấp mẩu | Đặt `decoy_rule = "agent_proposed"` như các chủ đề khác. `atom_flags check` hết báo "có mồi nhưng thiếu decoy_rule" (24 → 23 vấn đề; 23 vấn đề còn lại là việc chung của lúc đóng băng: valid_from, conflict_family cơ học, context_checked, HG3.5, moh_scope). | xong |

**Câu hỏi cho HG1.2 (mẩu 01).** Hướng dẫn 315/2015 (sản phụ khoa 2015, mục "Sốt trong khi có thai — 2.1.4 Sốt rét", trang PDF 75) có áp dụng cho sốt rét P. falciparum chưa biến chứng ở phụ nữ có thai 3 tháng đầu, nhiễm ở vùng P. falciparum kháng chloroquin hoặc đa kháng thuốc, không? Ba phương án của văn bản (chloroquin; sulfadoxin–pyrimethamin 3 viên liều duy nhất; muối quinin 7 ngày) là ba lựa chọn ngang hàng, hay chỉ áp dụng cho loài hoặc vùng còn nhạy thuốc?
- **Không áp dụng:** vn = {quinin + clindamycin}. Trắc nghiệm 01 tự dựng lại từ stem và filler hiện có. Đã mô phỏng trên bản sao trong scratchpad: 4 câu MCQ, 0 mục QC trượt. Các phương án là pyronaridin-artesunat, quinin + clindamycin, atovaquon-proguanil, artemether-lumefantrin.
- **Có áp dụng:** giữ tập hợp hiện tại và báo cáo là kết quả phụ DR8 có ý nghĩa an toàn.

**Lỗi bộ chấm grader 1.1.0 tái hiện bằng câu tự viết.** Các câu dưới đều dùng dòng ĐÁP ÁN/ANSWER như prompt yêu cầu:
- Số viết bằng chữ → nhãn 6 (từ chối). needs_llm = False, nên câu trả lời không được chuyển sang bộ tách LLM:
  - 05: "seven days", "one week", "bảy ngày";
  - 06: "three days", "ba ngày"; "five days" đáng lẽ là nhãn 4.
- Từ "daily" không được đọc là "/ngày":
  - "ANSWER: 30 mg daily" → 5 (unit_mismatch). Khi không có dòng ANSWER → 6 (parse_method 'none').
  - EN "0.5 mg base/kg/day" → 5, trong khi VI "0,5 mg base/kg/ngày" → 2.
- Số không đơn vị bị đọc theo đơn vị của mẩu, làm câu trả lời có nhiều giá trị → nhãn 5:
  - 06: "3 ngày (6 liều)" và "6 doses over 3 days". Với "over 3 days", phần này còn bị đọc thành "> 3". Đây là cách nói rất hay gặp với AL.
  - 07: "2.4 mg/kg at 0, 12 and 24 hours" → 5 thay vì 4. Làm mất nhãn 4 nghĩa là lỗi thiên về bảo thủ cho H1.
- Đơn vị không quy đổi được ở nhánh fallback → 6 thay vì 5 hoặc chuyển LLM: 07 "1,5 mg/kg/ngày" (giá trị DR8 của 3312/2015).
- 03: "ĐÁP ÁN: 30 mg (4 viên 7,5 mg)" → 5; khi không có dòng ĐÁP ÁN → needs_llm.
- Người kiểm cho rằng 04 "0.2 mg/kg/day" nên là 5. Tôi bác mục này: bộ chấm cho 3 là đúng thiết kế, vì 0,2 cách giá trị 0,25 của 2699/2020 ít hơn dung sai 0,125.

**Tự kiểm sau khi sửa:**
- `pilot_merge --only malaria_ocr`: giữ 8 mẩu, loại 0 (conflict 5, indistinguishable 2, concordant 1); mồi và dung sai không đổi.
- `qgen.build --only-drafted`: 28 câu, 5 mẩu bỏ trắc nghiệm có chủ đích, **0 mục QC không đạt**. q/p/qc giống từng byte với bản trước, vì chỉ đổi notes, cờ và `decoy_rule`.
- Schema hợp lệ: atom 8/8, question 28/28.
- `grade_short`, câu tự viết dạng ĐÁP ÁN: 34/34 đúng nhãn. Bộ Y tế → 2 (cả 4 mục vn của 01), nước ngoài → 4, bản cũ → 3, mồi → 5, từ chối → 6.
- Bộ 92 câu của người kiểm: 12 câu lệch. Cả 12 là các lỗi mức mã đã nêu ở trên, cộng câu 0,2 đã bác.
