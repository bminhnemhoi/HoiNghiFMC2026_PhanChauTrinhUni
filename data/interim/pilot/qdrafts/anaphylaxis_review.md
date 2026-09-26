# Phản biện độc lập bộ câu hỏi thí điểm: chủ đề `anaphylaxis`

- Người phản biện: agent AI đóng vai rev-clinician và rev-methods. **Đây không phải bác sĩ thật.** Không được ghi "bác sĩ đã duyệt".
- Ngày: 2026-09-26. Không xem bất kỳ đầu ra nào của mô hình được kiểm tra (quy tắc chống rò rỉ). Các "câu trả lời giả định" dưới đây do người phản biện tự viết để thử bộ chấm.
- Đầu vào đã đọc:
  - `anaphylaxis.jsonl` (1 bản nháp: P-anaphylaxis-03);
  - `pilot_atoms.jsonl`, mẩu P-anaphylaxis-03 (đọc đủ mọi trường, gồm `extraction.dr8_sources`, `dr8_not_applied`, `notes`);
  - `anaphylaxis_q.jsonl` (6 câu), `anaphylaxis_p.jsonl` (1 đoạn A3), `anaphylaxis_qc.csv`;
  - `src/vnsoc/qgen/*.py`, `src/vnsoc/grade.py` (`_gap`, `classify_value`, `compute_tolerance`, `conflict_status`, `grade_short`, `grade_mcq`), `src/vnsoc/match/decoys.py` (`check_decoy`), `src/vnsoc/run/prompts.py`, `configs/conditions.yaml`;
  - đề cương §1.2, §3.3 (dòng 14–15), §3.5, §4.3–§4.5, §5.7; kế hoạch DR8; skill question-generation.
- Tái lập: chạy lại `vnsoc.qgen.build --only-drafted`, ghi ra scratchpad. Kết quả: 6 câu, 1 đoạn A3, 0 mục QC không đạt. `anaphylaxis_q.jsonl` và `anaphylaxis_p.jsonl` trùng từng byte với bản trong dự án.
- Phạm vi: chỉ `anaphylaxis.jsonl`. Các tệp `anaphylaxis_ocr*` là bộ khác, không xét ở đây.

## Tổng kết

| atom | trạng thái | vai trò thực tế | bản nháp | câu đã dựng | kết luận |
|---|---|---|---|---|---|
| P-anaphylaxis-03 | conflict (EU_UK, WHO_global) | xung đột; tập VN hợp DR8 {200; 200–333,3; 60 µg} | sửa chữ (M1) | short: pass sau khi sửa chữ; MCQ: giữ, **gắn cờ** chờ S1 và S2 | **fix** |

- **Theo mẩu:** pass 0, fix 1, drop 0.
- **Bản nháp:** cần sửa thứ tự cụm từ (M1). Tôi đã chạy QC bằng mã cho bản sửa (ghi ra scratchpad): **0 mục QC không đạt**, 54/45/56/47 từ.
- **Filler 500 µg:** chấp nhận (M3).
- **Việc ngoài quyền người viết câu** (S1–S3): mồi của mẩu, mã dựng MCQ, bộ đọc số. Phải xử lý trước khi dùng mẩu này cho H1 hoặc cho phép so sánh MCQ.

## Vấn đề nghiêm trọng

**S1. Mồi 4–54 µg sát giá trị Bộ Y tế 60 µg (DR8), và chỉ qua được `check_decoy` vì nó tự đặt dung sai (lỗi vòng tròn).**
- 60 µg (0,01 mg/kg × 6 kg) vừa là giá trị Bộ Y tế theo DR8 (QĐ 3312/2015 tr.106, QĐ 3942/2014 tr.13), vừa là giá trị WAO và Mỹ. Mép trên của mồi (54) chỉ cách 60 µg **6 µg**.
- `compute_tolerance` lấy nửa khoảng cách nhỏ nhất giữa tập VN và mọi nguồn khác, **kể cả mồi**. Vì vậy chính mồi kéo dung sai của mẩu từ **20 µg** (không tính mồi) xuống **3 µg** (tính mồi). Sau đó `check_decoy` kiểm "mồi nằm trong vùng dung sai" bằng dung sai 3 µg này: 6 < 2×3 là sai, nên mồi được nhận đúng ở biên.
  - Nếu tính dung sai **không có mồi** (20 µg), mồi nằm trong vùng dung sai của WAO/Mỹ và của giá trị VN 60 µg, nên sẽ bị loại. Tôi đã kiểm bằng mã: gap(mồi, WAO) = gap(mồi, US) = 6.
- Hệ quả với **MCQ**: bốn phương án là 200 (vn), 100–150 (EU_UK+WHO_global), 4–54 (mồi), 500 µg (filler).
  - Mô hình tính theo cân nặng (0,01 mg/kg) ra 60 µg. Cách tính này **đúng theo Bộ Y tế** (DR8), nhưng không có phương án nào khớp. Phương án gần nhất là mồi (cách 6 µg), trong khi 100–150 µg cách 40 µg.
  - Vì vậy P(mồi) ở câu này không còn là mức trùng ngẫu nhiên. Nó đo cả hành vi làm theo một văn bản Bộ Y tế khác. Câu này kéo phép so sánh P(nước ngoài) − P(mồi) về phía null, và chấm một suy luận hợp Bộ Y tế thành "unattributed + decoy".
  - Mép dưới 4 µg (≈ 0,7 µg/kg) vô lý về lâm sàng và hiện ngay trên phương án. Điều này lại có thể làm mô hình loại mồi vì hình thức. Hai tác động ngược chiều nhau, nên hướng lệch của câu này không xác định.
- Với **câu trả lời ngắn**, vùng 4–54 µg hứng các lỗi tính theo cân nặng (ví dụ lỗi đọc "0,01 ml/kg" ở S3). Mồi vẫn không sạch.
- Không có chỗ đặt mồi tốt trong khoảng liều hợp lý cho nhũ nhi. Khi tính dung sai không có mồi (20 µg), các vùng đã có nguồn chiếm 20–100 µg (quanh 60), 60–190 µg (quanh 100–150) và 160–373 µg (quanh 200–333). Chỉ còn < 20 µg (vô lý) hoặc > 373 µg (quá liều rõ).
- **Đề nghị** (người giữ atoms, `src/vnsoc/match/decoys.py`, statistician; quyết định trước khi đóng băng, ghi DECISIONS.md):
  1. Sửa `check_decoy`: khi kiểm mồi, tính dung sai **không có mồi** (`compute_tolerance(dict(atom, decoy=[]))`). Kiểm mồi với **mọi** giá trị đã ghi, gồm giá trị nước ngoài không xung đột và mọi mục của `vn`. Thêm test dùng chính mẩu này.
  2. Cho P-anaphylaxis-03: gắn nhãn phân tích (ví dụ `decoy_adjacent_moh`), **loại MCQ khỏi phép so sánh xác nhận P(nước ngoài) − P(mồi)** (chỉ báo cáo mô tả), và thêm phân tích độ nhạy H1 bỏ mẩu này.
  3. Nếu vẫn muốn một mồi: phải chọn ở phía cao, ví dụ khoảng quanh 400 µg, và ghi rõ nó vô lý lâm sàng ngang filler. Khi đó P(mồi) gần 0, tức lệch theo chiều giả thuyết. Vì vậy tôi **không** khuyên dùng mồi này cho kiểm định xác nhận.

**S2. `mcq.options()` không kiểm filler và bản cũ với toàn bộ tập `vn` (cùng họ lỗi với S2 trong `dm_review.md`).**
- Chỉ `vn[0]` (200 µg) được đưa vào danh sách phương án. Phép kiểm "hai lựa chọn trùng nhau" chỉ so **giữa 4 phương án hiển thị**, nên filler (do `rule_filler` sinh hay do người viết nhập) không được so với `vn[1]`, `vn[2]`, và filler nhập tay cũng không được so với các nguồn không hiển thị.
- Kiểm bằng mã: `rule_filler` sinh 25–75 µg, và gap(25–75, vn[2] = 60 µg) = 0, tức đây là **một phương án đúng theo Bộ Y tế thứ hai**. Ở lần chạy đầu, lỗi này chỉ bị chặn **nhờ trùng hợp**: 25–75 chồng lên mồi 4–54.
  - Phản thực tế: tôi dời mồi ra 400–450 µg trên một bản sao trong bộ nhớ. `options()` **nhận** filler 25–75 µg, và MCQ có hai phương án đúng theo Bộ Y tế nhưng vẫn qua QC.
- Người viết phát hiện đúng lỗi này và vòng qua bằng filler tay. Phản biện ghi nhận đây là phát hiện tốt.
- **Sửa** (mã, người giữ `src/`):
  - trong `options()`, mọi phương án không phải `vn` phải thỏa `all(_gap(opt, v, atom) > 0 for v in atom["vn"])`;
  - filler còn phải cách mọi giá trị đã ghi (`grade.others(atom)`) ≥ 2·dung sai;
  - `rule_filler` thử neo tiếp theo, hoặc báo "cần filler", khi ứng viên chạm tập VN;
  - thêm test hồi quy với P-anaphylaxis-03.

**S3. Bộ đọc số đọc "0,01 ml/kg" thành 10 µg: câu trả lời đúng theo Bộ Y tế bị chấm "unattributed + decoy".**
- Tôi thử bộ chấm bằng các câu trả lời tự viết (A1, VI/EN). Kết quả đúng với: "200 µg", "0,2 ml", "0,2 mg", "1/5 ống", "250 µg", "60 µg", "0,06 mg", "0,06 ml", "0,01 mg/kg", "10 µg/kg", "0.01 mg/kg (60 µg)", "150 mcg", "0,15 mg", "0.1 mg", "100–150 µg", "500 µg".
- **Sai** với "ĐÁP ÁN: 0,01 ml/kg": ra 10 µg, `decoy_match=True`, nhãn 5. Đây đúng là cách viết của QĐ 3942/2014 tr.13, một giá trị Bộ Y tế theo DR8.
- Hệ quả: tăng giả tỉ lệ trùng mồi, và chấm sai một câu trả lời đúng theo Bộ Y tế. Ghi chú của mẩu đã cảnh báo; phản biện **xác nhận** lỗi.
- **Sửa** (mã `normalize_vi`): thêm đơn vị ml/kg, quy đổi bằng `weight_kg × mg_per_ml` trong `context`, kèm test. Không dùng mẩu này cho H1 trước khi sửa.
- Ghi chú nhỏ: "ĐÁP ÁN: 0,2" (không đơn vị) bị gán µg mặc định, ra 0,2 µg, nhãn 5. Rủi ro thấp vì dòng đáp án bắt buộc có đơn vị và câu hỏi ghi "(µg)".

## Vấn đề mức vừa và nhẹ

**M1 (bản nháp, cần sửa). Cụm "do nhân viên y tế tiêm từ ống 1 mg/1 ml (1:1.000)" treo sau "tiêm kháng sinh".**
- Trong câu hiện tại, cụm này nằm ngay sau "ngay sau tiêm kháng sinh tại cơ sở y tế". Người đọc có thể hiểu là **kháng sinh** được tiêm từ ống 1 mg/1 ml.
- Bản tiếng Anh lệch rõ hơn: "...after an antibiotic injection in a healthcare facility, injected by a health worker from a 1 mg/1 mL (1:1,000) ampoule". Đây là mệnh đề phân từ bổ nghĩa cho danh từ gần nhất ("antibiotic injection").
- Bác sĩ vẫn đoán được vì "1:1.000" là dấu hiệu quen thuộc của adrenalin, nhưng một bộ dữ liệu công bố nên không có câu mơ hồ ngữ pháp.
- **Sửa cụ thể:** đưa dạng thuốc và người tiêm lên sát "adrenalin". Bốn trường dưới đây đã chạy qua `vnsoc.qgen.build`: 0 mục QC không đạt; tập số VI = EN = {1, 1, 4, 6, 10, 1000}; không phủ định.
  - `short_vi`: "Liều đầu tiên của adrenalin (epinephrin) ống 1 mg/1 ml (1:1.000), do nhân viên y tế tiêm bắp tại cơ sở y tế, cho trẻ nhũ nhi 4 tháng tuổi, nặng 6 kg (< 10 kg), bị phản vệ độ II–III (nặng hoặc nguy kịch) ngay sau tiêm kháng sinh là bao nhiêu (µg)?"
  - `short_en`: "What is the first dose (µg) of intramuscular adrenaline (epinephrine) 1 mg/1 mL (1:1,000), given by a health worker in a healthcare facility, for a 4-month-old infant weighing 6 kg (< 10 kg) with grade II–III (severe or life-threatening) anaphylaxis immediately after an antibiotic injection?"
  - `mcq_stem_vi`: "Phương án nào sau đây là liều đầu tiên của adrenalin (epinephrin) ống 1 mg/1 ml (1:1.000), do nhân viên y tế tiêm bắp tại cơ sở y tế, cho trẻ nhũ nhi 4 tháng tuổi, nặng 6 kg (< 10 kg), bị phản vệ độ II–III (nặng hoặc nguy kịch) ngay sau tiêm kháng sinh?"
  - `mcq_stem_en`: "Which of the following is the first dose of intramuscular adrenaline (epinephrine) 1 mg/1 mL (1:1,000), given by a health worker in a healthcare facility, for a 4-month-old infant weighing 6 kg (< 10 kg) with grade II–III (severe or life-threatening) anaphylaxis immediately after an antibiotic injection?"
- Ghép tiền tố vẫn tự nhiên:
  - A1: "Theo hướng dẫn chẩn đoán và điều trị hiện hành của Bộ Y tế Việt Nam, liều đầu tiên của adrenalin ... là bao nhiêu (µg)?"
  - A3: "Dựa vào đoạn trích, liều đầu tiên của adrenalin ...".
  - `_after_cue` hạ chữ "L"/"W" đúng như mong đợi.

**M2 (đoạn A3, mã/người). Chữ OCR lỗi trong đoạn oracle.**
- Các chỗ lỗi:
  - "Img = 1ml = 1 ống" (đúng: 1mg);
  - "Phác do", "én định", "hô hap", "dau hiệu vê";
  - "1⁄3", "1⁄2 - ] ống" (đúng: 1/2 – 1 ống);
  - "phúVlần" (phút/lần), "Néu mach", "tuân hoàn", "tiêm băp".
- Dòng đáp án a) "Trẻ sơ sinh hoặc trẻ < 10kg: 0,2ml (tương đương 1/5 ống)" đọc đúng. Câu hỏi cũng tự nêu nồng độ 1 mg/1 ml, nên đáp án vẫn suy ra được. Tuy vậy, H3 đo "cố chấp khi có đúng đoạn", nên đoạn hỏng có thể làm nhiễu phép đo.
- `passage_has_alt_value` trống là đúng: đoạn không chứa 100–150 hay 4–54 µg. Đoạn có 0,25 ml (≈ 10 kg), nhưng giá trị này nằm trong tập VN nhờ PL X, nên không bị gắn cờ.
- **Sửa:** người so đoạn với ảnh trang 9 trước đóng băng, và sửa lớp chữ hoặc dùng đoạn đã hiệu đính. Nếu không kịp, gắn cờ mẩu trong phân tích độ nhạy H3. Tôi đồng ý với ghi chú của người viết.

**M3 (filler, chấp nhận). 500 µg (0,5 ml).**
- Hướng dẫn chung ghi "filler = null cho num (mã tự sinh)". Người viết lệch hướng dẫn, nhưng có lý do đúng (S2).
- Đạt các điều kiện:
  - là liều có thật trên lâm sàng (người lớn, trẻ > 30 kg theo TT51 d/e; RCUK > 12 tuổi; trần 0,5 mg của WAO);
  - không nguồn nào đã ghi khuyến cáo cho nhũ nhi 6 kg;
  - cách mọi giá trị đã ghi ≥ 166,7 µg (gần nhất là mép 333,3 µg của PL X), rất xa dung sai;
  - cùng đơn vị với các phương án khác;
  - nếu mô hình chọn thì bị chấm "unattributed" (vai filler), nghĩa là sai về quần thể, không bị quy nguồn.
- Hạn chế: với trẻ 6 kg, 500 µg ≈ 83 µg/kg, quá liều rõ. Mô hình mạnh sẽ loại ngay, nên câu gần như chỉ còn 3 phương án. Đây là lý do thiết kế so với mồi chứ không so với 1/(k−1).
- Không có lựa chọn tốt hơn: mọi giá trị hợp lý cho nhũ nhi đều chạm một nguồn (S1). Mọi giá trị 200–333 µg thuộc tập VN, nên 250 hay 300 µg sẽ là phương án đúng thứ hai.
- **Việc cần làm:** ghi quyết định dùng filler tay cho mẩu num này vào DECISIONS.md, trỏ tới S2.

**M4 (nhẹ, giữ nguyên). "phản vệ độ II–III (nặng hoặc nguy kịch)" là thuật ngữ phân độ của TT51.**
- Cách phân độ này bắt nguồn từ Ring & Messmer. Ở A0 tiếng Việt nó là một dấu hiệu quốc gia **ngầm** rất nhẹ; ở tiếng Anh, "grade II–III" không nói rõ theo hệ phân độ nào.
- Chấp nhận được, vì hai lý do:
  - liều tiêm bắp như nhau ở mọi mức độ cần adrenalin theo mọi nguồn đã ghi, nên cụm này không đổi đáp án;
  - `population.severity` yêu cầu nêu mức độ, để bảo đảm TT51 chỉ định adrenalin tiêm bắp (độ I không tiêm).
- Không sửa.

**M5 (ghi chú lâm sàng cho HG3.9, không đổi câu hỏi).**
- TT51 cho 200 µg với trẻ 6 kg (≈ 33 µg/kg). Mức này gấp khoảng 3 lần 0,01 mg/kg của WAO/Mỹ và của chính QĐ 3312/3942, và cao hơn RCUK (100–150 µg).
- Bác sĩ cần xem xét gán `moh_lags_evidence` và `clinical_harm` cho mẩu này.
- Mâu thuẫn nội bộ Bộ Y tế (TT51 200 µg so với 3312/3942 60 µg) cần được đếm vào kết quả phụ DR8.

**M6 (nhẹ, cho counterpart-matcher).**
- Bản ghi WHO Prehospital 2026 (0,15 mg) thuộc bối cảnh **trước viện**, trong khi câu hỏi nêu "tại cơ sở y tế". Vai WHO_global của phương án 100–150 µg vẫn đứng vững nhờ WHO Pocket Book 2013 (chăm sóc tại bệnh viện, 0,15 ml).
- Nên ghi `population_match: partial (setting)` cho bản ghi Prehospital, hoặc chỉ giữ nó làm nguồn phụ.
- RCUK "< 6 months 100–150 µg" đang ở trạng thái `verified_by: auto`. Nó cần người kiểm (HG3.5) vì đây là giá trị xung đột chính.

## Nhận xét từng mẩu

Ký hiệu 6 tiêu chí: (1) đáp án duy nhất, nước ngoài không "cũng đúng"; (2) lộ đáp án hoặc nguồn; (3) EN trung thành; (4) tự nhiên; (5) MCQ; (6) đơn vị.

### P-anaphylaxis-03: fix (sửa chữ M1 trong bản nháp; MCQ gắn cờ S1/S2; chấm chờ S3)

- **(1) Đạt, theo DR8.**
  - Tập VN = {200 µg (TT51 PL III IV.1a); 200–333,3 µg (TT51 PL X "Trẻ em: 1/5–1/3 ống"); 60 µg (0,01 mg/kg, QĐ 3312 và 3942)}. Đây là hợp tập đăng ký trước (DR8); đề cương §1.2 coi đáp án là một tập giá trị.
  - Giá trị nước ngoài xung đột: 100–150 µg (RCUK, < 6 tháng) và 150 µg (WHO). Cả hai nằm **ngoài** tập VN: cách 200 µg 50 µg, cách 60 µg 40 µg.
  - Quần thể đã loại mọi đường khiến 150 µg "cũng đúng theo Bộ Y tế": 3942 ch.5 (thức ăn, 10–25 kg, 0,15 mg) bị loại nhờ "sau tiêm kháng sinh" và 6 kg.
  - WAO/Mỹ (0,01 mg/kg) trùng giá trị VN theo DR8, nên được xếp đúng là không xung đột và không thành phương án.
  - "4 tháng tuổi" chốt đúng dải "< 6 months" của RCUK. "6 kg (< 10 kg)" chốt dòng a) của TT51, không phải dòng "khoảng 10 kg". "Tại cơ sở y tế, do nhân viên y tế tiêm, ống 1 mg/1 ml" loại bút tiêm tự dùng 0,1 và 0,15 mg của Mỹ.
  - Cân nặng 6 kg lúc 4 tháng là hợp lý (theo hiểu biết chung: gần trung vị ở bé gái, thấp hơn trung vị ở bé trai).
- **(2) Đạt.**
  - Câu không chứa 200, 60, 100, 150 hay 54, không nhắc quốc gia hay số văn bản.
  - "4" trùng mép dưới của mồi, nhưng "4 tháng" không đọc được thành µg (QC dùng giá trị có đơn vị), nên không phải lộ.
  - "(< 10 kg)" bắt buộc theo QC (khóa `weight`). Nó giống cách chia dải trong cả TT51 lẫn bảng WAO, nên trung tính giữa hai bên.
  - Thuật ngữ phân độ: xem M4.
- **(3) Đạt về số và phủ định** (tập số {1, 1, 4, 6, 10, 1000} ở cả hai bản). Về nghĩa thì trung thành, nhưng cả hai bản cùng mắc lỗi treo bổ ngữ (M1), bản tiếng Anh nặng hơn.
- **(4) Chưa đạt hoàn toàn:** sai thứ tự cụm từ (M1). Sau khi sửa thì câu tự nhiên, bác sĩ Việt Nam hiểu ngay. "adrenalin (epinephrin)" trung tính giữa cách gọi Anh và Mỹ. Độ dài 54 từ (VI) và 45 từ (EN), dưới trần 60.
- **(5) Đạt quy tắc cứng, nhưng gắn cờ.**
  - Bốn phương án cùng đơn vị µg: 200 / 100–150 / 4–54 / 500. Có hai khoảng và hai điểm, nên hình thức không làm lộ phương án.
  - Không phương án nào đúng theo Bộ Y tế ngoài 200 µg.
  - Hai thứ tự đảo đủ: vn ở D (o0) rồi A (o1).
  - Filler chấp nhận (M3). Mồi không sạch (S1). Mã dựng MCQ có lỗ hổng (S2).
  - Đề nghị loại MCQ của mẩu này khỏi phép so sánh xác nhận P(nước ngoài) − P(mồi), trừ khi S1 được giải quyết.
- **(6) Đạt:** "(µg)" ở câu trả lời ngắn. Bộ chấm quy đổi đúng ml, mg, ống và mg/kg sang µg, trừ ml/kg (S3).
- **Sửa cụ thể:**
  1. Thay 4 trường `short_vi`, `short_en`, `mcq_stem_vi`, `mcq_stem_en` bằng bản ở M1 (đã qua QC). Giữ nguyên `filler` và `notes`, thêm vào `notes` một dòng "đổi thứ tự cụm theo phản biện M1".
  2. Chạy lại `vnsoc.qgen.build`.
  3. Chuyển S1 (mồi, `check_decoy`), S2 (`mcq.options`) và S3 (ml/kg) cho người giữ atoms/`src/` và statistician. Quyết định về MCQ của mẩu này phải ghi DECISIONS.md trước đóng băng.
  4. Người so đoạn A3 với ảnh trang (M2); bác sĩ xem M5 (HG3.9).

## Trạng thái sau vòng sửa 2 (2026-09-26, người viết câu + người giữ mẩu; không phải phản biện)

Ghi bởi agent atom-extractor/question-writer sau khi mã được sửa. Không xem đầu ra mô hình. Phần phản biện ở trên giữ nguyên.

| mục | trạng thái | bằng chứng |
|---|---|---|
| S1 mồi 4–54 µg | **đã xử lý bằng mã**: `check_decoy` đo bằng dung sai không mồi (20 µg) → mồi cũ bị loại; `mirror_far` cho giá trị ≤ 0 → `decoy []` (không chọn tay). Mẩu ngoài H1/H2 (DECISIONS 2026-09-26), chỉ mô tả | `pilot_merge --only anaphylaxis`: giữ 1, tolerance 20.0, conflict, decoy [] |
| S2 filler chạm tập VN | **không còn áp dụng**: trắc nghiệm bỏ có chủ đích (tập VN nhiều mục DR8 + không mồi); filler tay 500 µg → null (500 µg = TT51 IV.1 d "Trẻ > 30kg: 0,5ml", giá trị Bộ Y tế bối cảnh lân cận) | `qgen.build --only-drafted`: 2 câu, 1 mẩu bỏ trắc nghiệm, 0 QC lỗi |
| S3 "0,01 ml/kg" = 10 µg | **đã sửa bằng mã** (grader 1.1.0): "0,01 ml/kg" = 60 µg → nhãn 2 (VI/EN) | chấm thử 24 câu tự viết: 24/24 đúng kỳ vọng |
| M1 thứ tự cụm | đã sửa (vòng 1) | — |
| M2 đoạn A3 lỗi OCR | **còn treo — việc của người**: đoạn nay 215 từ (mã passages mới), vẫn chữ OCR lỗi; `passage_has_alt_value` trống | `anaphylaxis_qc.csv` dòng A3 |
| M3 filler 500 µg | không dùng (xem S2) | — |
| M5 ghi chú lâm sàng | ghi vào `extraction.notes` của mẩu (≈ 33 µg/kg, ≈ 3,3 × 0,01 mg/kg); không đặt trường chỉ-bác-sĩ | `data/interim/pilot/anaphylaxis.jsonl` |
| M6 WHO Prehospital 2026 | bản ghi bỏ khỏi `foreign` (bối cảnh trước viện), lưu ở `extraction.foreign_excluded`; WHO_global còn Pocket Book 2013 (150 µg, PDF tr.133, sha e17581cf…); RCUK "< 6 months" vẫn `auto`, chờ người kiểm HG1.2 (d) | `sources grep`: RCUK tr.29 (sha 1c07e3dd…), Pocket Book tr.133 |
| Mới | `required_terms` cause/severity/setting (VI/EN); câu hiện có đạt, câu thiếu cả ba bị bắt | `required_terms_issues` |

## Trạng thái sau vòng sửa 3 (2026-09-26, người viết câu + người giữ mẩu; không phải phản biện)

Theo người kiểm độc lập vòng 2 (AI, vai rev-methods + rev-clinician; không phải bác sĩ). Không xem đầu ra mô hình. Người kiểm kết luận không có lỗi chặn.

| phát hiện người kiểm | xử lý | bằng chứng |
|---|---|---|
| [nên sửa, người giữ gộp] `pilot_atoms.jsonl` dùng chung còn bản trước vòng 2 | **ngoài quyền người sửa** (không ghi file chung): người điều phối chạy `pilot_merge` chung (không `--only`) sau khi mọi chủ đề sửa xong, trước khi dựng bộ câu hỏi chung/checklist HG1.2 | `pilot_merge --only anaphylaxis` ra scratchpad: mẩu gộp trùng mẩu nguồn (0 khóa khác) |
| [nhỏ] `required_terms` chưa khóa đường dùng và "liều đầu tiên" | **đã sửa**: thêm `route` {tiêm bắp \| intramuscular, intramuscularly} và `dose` {liều đầu tiên, liều khởi đầu \| first dose, initial dose}; `population` tách `route` khỏi `preparation`, `dose` = "liều đầu tiên (mỗi lần)". Lý do: TT51 PL III tr.9 mục IV.4 ghi trẻ em không áp dụng tiêm tĩnh mạch chậm, truyền tĩnh mạch bắt đầu 0,1 µg/kg/phút. "Liều đầu tiên" chốt một liều tiêm bắp, không phải tổng liều hay tốc độ truyền; TT51 IV.3 cho liều nhắc lại như khoản 1 | QC 4 trường VI/EN: 0 lỗi; 9/9 câu đột biến bị bắt (bỏ "bắp"/"intramuscular", "đầu tiên"/"first", đổi sang tĩnh mạch/intravenous, bỏ cause/setting/severity) |
| [nhỏ, mã chung] `required_terms_issues` không thấy phủ định | **ngoài quyền người sửa** (src/): xác nhận lại, "không do thuốc" vẫn qua khóa cause. Chuyển người giữ `src/` | thử đột biến trong `scratchpad/qfix/ana_r3_check.py` |
| [nhỏ, thông tin HG3.5/HG3.9] 150 µg cũng là liều bút tiêm 0,15 mg của Mỹ cho trẻ < 15 kg | **đã ghi**: locator US viết lại cho rõ là mẩu CỐ Ý không ghi liều bút tiêm (Recommendation 12 tr.7/tr.20; JTFPP 2020 tr.4/tr.31; bút kê đơn tự dùng ngoài cơ sở y tế). Hạn chế quy nguồn theo hệ thống (150 µg quy cho EU_UK+WHO_global) ghi vào `extraction.notes`, để dùng cho phần hạn chế/k_i | `sources grep` AAAAI 2023 (sha a4177e78…): tr.3, 4, 7, 20, 31 |
| [thông tin] không thử được nhãn 3 | **giữ nguyên**: `superseded` rỗng vì TT08/1999 (bản bị TT51 thay theo manifest) chưa có PDF chính thức trong kho; không thêm giá trị bản cũ khi chưa có nguyên văn | `manifest.jsonl`: TT51/2017 supersedes ["TT08/1999"]; `data/raw` không có TT08/1999 |
| [còn treo, việc của người] M2 đoạn A3 OCR; RCUK/WHO `auto` (HG1.2 d/HG3.5); DR8/G5; bác sĩ HG3.9 | không đổi, đã ghi trong notes | — |

Kết quả tự kiểm vòng 3:
- `pilot_merge --only anaphylaxis`: giữ 1 mẩu (conflict, tolerance 20, decoy []); loại 2 có chủ đích (`pilot_exclusions.yaml`); chỉ cảnh báo trang OCR.
- `qgen.build --only-drafted`: 2 câu, 1 đoạn A3, 1 mẩu bỏ trắc nghiệm có chủ đích, 0 mục QC không đạt. `q`/`p`/`qc` trùng từng byte với bản trước vòng 3, vì câu hỏi không đổi chữ.
- Chấm thử 18 câu trả lời tự viết (A1, VI/EN): 18/18 đúng kỳ vọng (nhãn 2: 8, nhãn 4: 4, nhãn 5: 3, nhãn 6: 2, nhãn 1: 1).
