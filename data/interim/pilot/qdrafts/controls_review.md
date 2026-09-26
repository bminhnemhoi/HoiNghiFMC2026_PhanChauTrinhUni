# Phản biện độc lập — bộ câu hỏi thí điểm chủ đề `controls`

- Người phản biện: agent AI đóng vai rev-clinician + rev-methods (không phải bác sĩ thật; mọi nhận định lâm sàng cần người/bác sĩ xác nhận ở HG4.2).
- Ngày: 2026-09-26.
- Đầu vào: `data/interim/pilot/qdrafts/controls.jsonl` (9 bản nháp), `data/interim/pilot_atoms.jsonl` (P-controls-01..09), `controls_q.jsonl` (26 câu), `controls_qc.csv`, `controls_p.jsonl` (9 đoạn A3, chỉ là văn bản Bộ Y tế).
- Chống rò rỉ: KHÔNG xem đầu ra của bất kỳ mô hình được kiểm tra nào. Các chuỗi dùng để chấm thử bên dưới là chuỗi do người phản biện tự viết.
- Kiểm bằng mã:
  - Dựng lại vào scratchpad: 26 câu, 9 đoạn A3, 0 mục QC không đạt, exit 0; kết quả giống hệt `controls_q.jsonl`.
  - Số từ: mọi câu ≤ 60 từ. P-controls-04 VI đúng 60 từ, sát trần.
  - Chấm thử `grade_short` trên chuỗi tự viết để xem đơn vị và cách quy nguồn (kết quả nêu ở từng mẩu).
  - Các bản sửa đề xuất cho 04 và 09 đã chạy qua `vnsoc.qgen.build` với tệp nháp tạm trong scratchpad: 0 mục QC không đạt. Tệp nháp của người viết chưa bị sửa.

## Tổng hợp

| atom_id | Loại | Kết luận | Vấn đề chính |
| --- | --- | --- | --- |
| P-controls-01 | đối chứng | **pass** | Diễn đạt hơi thừa (không bắt buộc sửa) |
| P-controls-02 | đối chứng | **pass** | Câu nối dài; nên sửa diễn đạt (không bắt buộc) |
| P-controls-03 | đối chứng | **pass** | — |
| P-controls-04 | đối chứng | **fix** | "còn đợt cấp" vẫn cho phép áp nhánh ≥ 100 tế bào/µL của cùng đoạn Bộ Y tế |
| P-controls-05 | đối chứng | **pass** | — |
| P-controls-06 | đối chứng | **pass** | — |
| P-controls-07 | đối chứng | **pass** | — |
| P-controls-08 | xung đột | **fix** (MCQ; câu ngắn VI/EN đạt) | Chỉ phương án VN là khoảng; giá trị UKHSA 10.000 IU và mồi 8.500 IU; 250 IU (liều dự phòng của Bộ Y tế) bị chấm nhãn 4 |
| P-controls-09 | xung đột | **fix** (phụ thuộc sửa mẩu và mã; không sửa được thì loại khỏi tập xác nhận) | Cụm "gốc châu Á" trùng ngưỡng Mỹ 23; 25 cũng là ngưỡng béo phì của Bộ Y tế; mồi 21 không hợp lý; dấu "≥" làm lộ phương án |

**Đếm: pass 6, fix 3, drop 0.**

---

## P-controls-01 — pass

- Câu hỏi: ngưỡng FEV1/FVC sau test hồi phục phế quản để chẩn đoán BPTNMT (tính theo %).
- (1) Đáp án Bộ Y tế duy nhất: < 70%. GOLD cũng < 0,7, nên mẩu đối chứng hợp lệ.
- (2) Không lộ đáp án. Không có dấu hiệu nguồn hay quốc gia.
- (3) Bản EN trung thành. Phủ định "không hồi phục hoàn toàn" ↔ "not fully reversible" khớp nhau.
- (4) Bác sĩ hiểu ngay. Cụm "đo hô hấp ký tại cơ sở y tế có máy đo chức năng hô hấp" thừa, vì đã đo hô hấp ký thì tất nhiên có máy. Đây là vấn đề văn phong, không ảnh hưởng tính duy nhất.
- (6) "(tính theo %)" là bắt buộc. Chấm thử: "0,7" và "0.70" nhận nhãn 5; "70%" và "70" nhận nhãn 2. Người viết đã xử lý đúng grading_caveat.
- Sửa (tùy chọn): "Ở người lớn được đo chức năng hô hấp (hô hấp ký) tại cơ sở y tế, tỉ số FEV1/FVC sau test hồi phục phế quản dưới ngưỡng nào thì xác định …". Phải giữ "cơ sở y tế có máy đo" nếu muốn bám sát population.setting.

## P-controls-02 — pass

- (1) Đã loại nhánh 56–59 mmHg bằng cách nêu "không tăng áp phổi, suy tim phải hay đa hồng cầu". Còn lại duy nhất ≤ 55 mmHg, trùng GOLD.
- (2) Không lộ đáp án. Không nhắc SaO2 88% (giá trị khác slot).
- (3) EN trung thành, cùng các số 2 và 3.
- (4) Câu VI nối liền "…đa hồng cầu, PaO2 lúc nghỉ, không thở oxy (…) từ ngưỡng nào trở xuống…" nên đọc như còn một mục liệt kê nữa. Vẫn hiểu được, nhưng không trơn. "khí máu" nên ghi "khí máu động mạch".
- (6) "(mmHg)" là bắt buộc. Chấm thử: "7.3 kPa" nhận nhãn 5 (unit_mismatch); "55 mm Hg" nhận nhãn 2.
- Sửa (tùy chọn, ≤ 60 từ): "Ở người lớn mắc bệnh phổi tắc nghẽn mạn tính ổn định, đã điều trị tối ưu, không có tăng áp phổi, suy tim phải hay đa hồng cầu, PaO2 đo lúc nghỉ khi không thở oxy (2 mẫu khí máu động mạch trong 3 tuần) từ ngưỡng nào trở xuống thì chỉ định thở oxy dài hạn tại nhà (mmHg)?" EN: đổi "not breathing oxygen" thành "while breathing room air" và "blood gas samples" thành "arterial blood gas samples".
- Ghi chú đoạn A3 (`P-controls-02#A3`): đoạn kết thúc bằng dấu chữ ký số của PDF, có họ tên và giờ ("ngoctlv.kcb_Truong Le Van Ngoc_27/10/2023 18:07:34"). Đoạn còn bị cắt ở cuối trang ngay sau "kèm thêm một trong các biểu hiện:". Đây là nhiễu trong prompt A3 và để lộ tên cá nhân. Đề xuất cho chủ mã `passages.py` lọc mẫu dấu ký số này. Việc này không làm đổi đáp án 55.

## P-controls-03 — pass

- (1) Tập Bộ Y tế 5–7 ngày (nội trú cũng 5–7) chứa 5 ngày của GOLD, nên là đối chứng. "Ngoại trú" và "đường uống" đủ xác định.
- (2) Không nêu liều 30–40 mg, nên không gợi ý.
- (3) EN trung thành.
- (4) Diễn đạt tự nhiên.
- (6) "(số ngày)" đủ rõ. Chấm thử: "5 ngày", "5-7 ngày", "5 to 7 days" nhận nhãn 2; "14 ngày" và "10-14 days" nhận nhãn 5.
- Ghi chú đoạn A3: đoạn bắt đầu bằng số trang trần "30". Nhiễu nhỏ.

## P-controls-04 — fix

- Vấn đề (tiêu chí 1): câu nêu "còn đợt cấp khi đơn trị LABA hoặc LAMA" nhưng không nói tần suất. Ngay sau câu ≥ 300, cùng đoạn Bộ Y tế (2767/2023 tr.23) ghi: "ICS/LABA có thể chỉ định cho … Bệnh nhân có ≥ 2 đợt cấp trung bình/năm hoặc ≥ 1 đợt cấp nhập viện, và bạch cầu ái toan ≥ 100 tế bào/µL". Quần thể trong câu hiện tại bao gồm cả người đợt cấp thường xuyên, nên 100 tế bào/µL cũng là một ngưỡng Bộ Y tế "khi cân nhắc thêm ICS". GOLD có quy tắc tương tự (≥ 100 khi còn đợt cấp).
  - Cụm "dự báo đáp ứng tốt" chỉ đúng 300, nhưng mô hình dễ trả lời 100. Chấm thử: "100 tế bào/µL" nhận nhãn 5.
  - Với mẩu đối chứng, điều này hạ tỉ lệ đúng ở nhóm đối chứng một cách giả tạo, nên làm lệch so sánh xung đột với đối chứng.
- (2), (3), (6) đạt. Đơn vị: "0.3 x 10^9/L" cũng được quy đổi đúng (nhãn 2).
- (4) Câu VI đúng 60 từ, sát trần.
- Sửa cụ thể: nêu tần suất đợt cấp dưới ngưỡng của nhánh 100 và rút gọn câu. Bản dưới đã chạy QC mã: 0 lỗi, VI 59 từ, EN 52 từ.
  - short_vi: "Ở người lớn mắc bệnh phổi tắc nghẽn mạn tính giai đoạn ổn định, đang đơn trị LABA hoặc LAMA, có 1 đợt cấp trung bình (không nhập viện) trong năm qua, khi cân nhắc thêm corticosteroid dạng hít (ICS), bạch cầu ái toan máu từ mức nào trở lên dự báo đáp ứng tốt với ICS (tế bào/µL)?"
  - short_en: "In an adult with stable chronic obstructive pulmonary disease on LABA or LAMA monotherapy who has had 1 moderate exacerbation (not requiring hospitalisation) in the past year and is being considered for an added inhaled corticosteroid (ICS), at or above what blood eosinophil count is a good response to ICS predicted (cells/µL)?"
  - Lý do: với 1 đợt cấp trung bình, không nhập viện, nhánh "≥ 2 đợt cấp trung bình/năm hoặc ≥ 1 đợt cấp nhập viện" (ngưỡng 100) không áp dụng. Còn lại duy nhất ngưỡng 300 cho đáp ứng tốt với ICS. GOLD cũng dùng 300 để nâng lên LABA+LAMA+ICS ở bệnh nhân LABA/LAMA đơn trị. Cần bác sĩ xác nhận (HG4.2).

## P-controls-05 — pass

- (1) 100 mg/lần, trùng CDC. Loại thai kỳ và chống chỉ định tetracyclin, nên nhánh azithromycin không áp dụng.
- (2) Không lộ đáp án. "> 45 kg" là ngưỡng cân nặng liều người lớn của CDC, nhưng đó là số quần thể bắt buộc và không phải đáp án.
- (3) EN trung thành. Phủ định khớp ("không mang thai", "không có chống chỉ định" ↔ "non-pregnant", "no contraindication").
- (4) Diễn đạt tự nhiên. Nêu "2 lần mỗi ngày" để tránh câu trả lời liều ngày 200 mg. Chấm thử: "200 mg" nhận nhãn 5; "100 mg twice daily" nhận nhãn 2.
- Còn tồn ở mức mẩu, không phải câu hỏi: cách hiểu "0,1 g x 2 viên uống chia 2 lần/ngày" và hiệu lực 5642/2015 cho sốt mò vẫn cần kiểm ở HG1.2/HG2.3.

## P-controls-06 — pass

- (1) 2 g/lần là giá trị chung của cả ba văn bản Bộ Y tế (DR8) và Darwin 2024. Giới hạn khoa thường, không tổn thương thần kinh trung ương, thận bình thường đã loại nhánh carbapenem/ICU và chỉnh liều.
- (2) Không nêu khoảng cách liều, nên không gợi ý.
- (3) EN trung thành.
- (4) Câu dài (57 từ) nhưng rõ.
- (6) Hỏi "(mg/lần)" dù lâm sàng quen ghi theo g. Chấm thử: "2 g" và "2000 mg/lần" đều nhận nhãn 2 (có quy đổi g→mg); "50 mg/kg" nhận nhãn 5 (unit_mismatch), chấp nhận được với câu hỏi người lớn.
- Ghi chú đoạn A3: đoạn có dòng của vi khuẩn liền trước ("Ceftazidime 3-6 g/ngày … 8 giờ/lần"), là giá trị theo ngày của tác nhân khác. Nhiễu nhỏ; passage_has_alt_value rỗng.

## P-controls-07 — pass

- (1) 500 mg/lần, trùng WHO 2010. Câu đã chỉ định metronidazol, nên nhánh penicillin G không áp dụng.
- (2), (3), (4), (6) đạt. Chấm thử: "500 mg every 6-8 hours" nhận nhãn 2.

## P-controls-08 — fix (câu ngắn VI/EN đạt; phần trắc nghiệm cần sửa)

Câu ngắn:
- (1) Đã nêu HTIG từ người (không phải SAT ngựa) và điều trị bệnh (không phải dự phòng vết thương). 500 IU không đúng theo 5642/2015 cho quần thể này. 3312/2015 có HTIG 250 UI nhưng đó là dự phòng, khác slot.
- (2) Không lộ đáp án. Cụm loại trừ SAT ngựa là dấu hiệu bối cảnh nước thu nhập thấp–trung bình rất yếu. Chấp nhận được vì cần để phân biệt sản phẩm.
- (3) EN trung thành. Phủ định khớp.
- (4) Tự nhiên, đúng thuật ngữ Bộ Y tế.
- (6) Chấm thử: "3000 đơn vị", "3,000–6,000 IU" nhận nhãn 2; "500 units" nhận nhãn 4 (US + WHO_global).

Trắc nghiệm (vấn đề):
1. Dấu hiệu hình thức: 4 phương án là "500 IU", "3.000–6.000 IU", "8.500 IU" và "12.500 IU". Chỉ phương án VN là khoảng; ba phương án còn lại là số đơn. Mô hình có thể chọn theo hình thức ("giống câu trong hướng dẫn") thay vì theo nội dung.
   - Nguyên nhân nằm ở mã: mồi `mirror_arith` và filler do `rule_filler` sinh đều có độ rộng 0.
   - Không sửa được trong bản nháp, vì quy tắc bắt filler = null với kiểu num.
2. Mồi 8.500 IU có thể không "sạch nguồn": UKHSA "Guidance on the management of suspected tetanus cases…" (gov.uk, cập nhật 12/8/2026) khuyến cáo điều trị uốn ván lâm sàng bằng IVIG theo cân nặng.
   - Nguyên văn: "for individuals less than 50kg, 5,000 IU" / "for individuals 50kg and over, 10,000 IU". Nguồn ghi TIG tĩnh mạch không còn ở Anh.
   - Tôi đọc bằng WebFetch ngày 26/9/2026, chưa có sha256 → needs_human_check qua quy trình counterpart-matching.
   - Hệ quả trắc nghiệm: mô hình quen hướng dẫn Anh có thể chọn 8.500 IU (gần 10.000 IU nhất), làm P(mồi) tăng. Sai lệch này đi về phía bảo thủ cho H1, nhưng phá vai trò "không thuộc nguồn nào" của mồi.
   - Hệ quả trả lời ngắn: chấm thử "10000 IU" nhận nhãn 5, nên câu trả lời quy được về chuẩn Anh bị tính là "không quy được nguồn".
3. Giá trị lân cận của Bộ Y tế bị quy sai: chấm thử "250 IU" nhận nhãn 4 (US + WHO_global) do dung sai 1250. Nhưng 250 IU chính là liều HTIG dự phòng của Bộ Y tế (3312/2015 tr.79). Lỗi nhầm slot nội bộ bị tính thành "lỗi trùng chuẩn nước ngoài".

Sửa cụ thể:
- Bản nháp: giữ nguyên short_vi, short_en, mcq_stem_vi, mcq_stem_en.
- Mã (chủ `src/vnsoc/qgen/mcq.py` và `vnsoc.match.decoys`; người phản biện không sửa src): mồi và filler kiểu num nên có cùng độ rộng tương đối với khoảng VN khi VN là khoảng (ví dụ 7.000–14.000 IU thay cho 8.500). Cách khác: đăng ký trước phân tích độ nhạy loại mẩu có phương án VN khác dạng.
- Mẩu (chủ counterpart-matching):
  - Quyết định giá trị UKHSA (IVIG, tĩnh mạch, 10.000 IU cho ≥ 50 kg) là cùng slot (thêm foreign EU_UK) hay khác slot (khác sản phẩm và đường dùng; ghi vào notes). Xem lại mồi 8.500 IU nếu nó nằm giữa VN 6.000 và UK 10.000.
  - Ghi `moh_neighbour` 250 IU (3312/2015, dự phòng vết thương) để phân tích độ nhạy tách được các câu trả lời 250 IU.

## P-controls-09 — fix (phụ thuộc sửa mẩu và mã; nếu không sửa được thì loại khỏi tập xung đột xác nhận)

1. **"gốc châu Á" làm yếu xung đột và gợi đáp án** (tiêu chí 1, 2).
   - USPSTF 2021 (Mỹ), đọc bằng WebFetch 26/9/2026, nguyên văn: "Data suggest that a BMI of 23 or greater may be an appropriate cut point in Asian American persons". Nguồn khuyên tầm soát người Mỹ gốc Á ở BMI thấp hơn (≥ 23). Theo ghi chú của mẩu, ADA mục 2 có lẽ cũng vậy nhưng chưa kiểm.
   - Hệ quả: với quần thể "người trưởng thành gốc châu Á, xét tầm soát ĐTĐ", hệ thống Mỹ cho đúng 23, trùng Bộ Y tế. WPRO 2000 cũng 23. Chỉ còn tờ thông tin WHO (định nghĩa chung, không theo sắc tộc) cho 25.
   - Bản EN gần như lặp lại câu chữ USPSTF/ADA. Câu hỏi vì thế đo "mô hình có biết ngưỡng cho người châu Á không" hơn là "mô hình có mặc định theo chuẩn nước ngoài không".
   - Văn bản gốc Bộ Y tế (5481/2020 tr.11; 3087/2020 tr.7) chỉ ghi "Người trưởng thành ở bất kỳ tuổi nào", không có sắc tộc. "(châu Á)" là cách đặt khung của người trích mẩu, và câu hỏi chỉ viết lại theo quy tắc "nêu đủ population".
2. **Giá trị nước ngoài 25 trùng một giá trị Bộ Y tế ở slot lân cận.**
   - Theo thang châu Á, 25 là ngưỡng béo phì của chính Bộ Y tế: 3087/2020 tr.12 "Béo phì: BMI ≥ 25-30"; 2919/2014 tr.60 "Béo độ 1 25 – 29,9".
   - Chấm thử: "25 kg/m²" nhận nhãn 4 (WHO_global). Nhưng câu trả lời này cũng có thể là nhầm thừa cân với béo phì ngay trong thang Bộ Y tế, nên quy nguồn bị nhiễu.
   - Tình huống này tương đương "không phân biệt được nguồn" ở đề cương §1.2.
3. **Mồi 21 kg/m² không hợp lý như các phương án khác** (§1.2 yêu cầu "hợp lý như nhau").
   - 21 nằm trong khoảng bình thường của cả thang châu Á (18,5–22,9) lẫn thang WHO (18,5–24,9). Bác sĩ hay mô hình biết chút ít đều loại được.
   - Hệ quả: P(mồi) bị ép gần 0, làm phần vượt (π_nước ngoài − π_mồi)/(1 − π_mồi) bị thổi phồng. Sai lệch này có lợi cho H1, tức là không bảo thủ.
4. **Dấu "≥" làm lộ phương án**, lỗi ở mã và có tính hệ thống.
   - 4 phương án là "≥ 23 kg/m2" (vn), "≥ 25 kg/m2" (WHO), "27 kg/m2" (filler), "21 kg/m2" (mồi). Câu dẫn hỏi "từ ngưỡng nào trở lên", mà chỉ phương án VN và nước ngoài mang "≥".
   - Mô hình có thể loại mồi và filler chỉ nhờ hình thức. P(mồi) giảm, nên sai lệch lại có lợi cho H1.
   - Mọi mẩu ngưỡng có `cmp` ở mọi chủ đề đều bị ảnh hưởng.

Các tiêu chí khác: (3) EN trung thành; (6) "(kg/m²)" rõ; (4) chuỗi loại trừ "(không mang thai, không nhiễm HIV, không mắc ung thư)" hơi gượng nhưng cần cho DR8.

Sửa cụ thể:
- Mẩu (chủ counterpart-matching, cần quyết định trước khi đóng băng):
  - (a) Đổi population.ethnicity thành ghi chú "ngầm định người Việt Nam qua tiền tố A1; không nêu trong câu hỏi". Căn cứ: văn bản Bộ Y tế không nêu sắc tộc.
  - (b) Thêm foreign US từ USPSTF 2021: thừa cân ≥ 25 cho quần thể chung; ghi ngưỡng 23 cho người Mỹ gốc Á vào notes (cần kiểm có sha).
  - (c) Ghi `moh_neighbour` 25 kg/m² (ngưỡng béo phì thang châu Á của Bộ Y tế). Đăng ký trước phân tích độ nhạy loại mẩu này, hoặc xếp mẩu vào nhóm không phân biệt được.
  - (d) Xem lại mồi 21 (không hợp lý lâm sàng).
  - Nếu giữ "châu Á" trong population, mẩu nên ra khỏi tập xung đột xác nhận: với quần thể đó, Mỹ và WPRO đều là 23, và WHO 2004 cũng có điểm hành động 23 cho người châu Á (chưa tải, cần kiểm).
- Câu hỏi (dùng nếu chọn (a); đã chạy QC mã, 0 lỗi):
  - short_vi: "Ở người trưởng thành không có triệu chứng (không mang thai, không nhiễm HIV, không mắc ung thư), khi xét chỉ định xét nghiệm tầm soát đái tháo đường hoặc tiền đái tháo đường, chỉ số khối cơ thể (BMI) từ ngưỡng nào trở lên được xếp là thừa cân hoặc béo phì (kg/m²)?"
  - short_en: "In an asymptomatic adult (not pregnant, without HIV infection or cancer) being assessed for screening tests for diabetes or prediabetes, at or above what body mass index (BMI) threshold is the person classified as overweight or obese (kg/m²)?"
  - mcq_stem_vi / mcq_stem_en: như trên, bỏ phần đơn vị trong ngoặc.
  - Lưu ý: khi bỏ "châu Á", ở A0 (không dấu hiệu quốc gia) 25 là đáp án đúng về y khoa cho người trưởng thành nói chung. A0 chỉ có vai trò mô tả (§4.4), nên với mẩu này chỉ diễn giải A1 và A3. Cần ghi rõ điều này trong phân tích.
- Mã (chủ `src/vnsoc/qgen/mcq.py` hoặc `render.py`): mồi và filler phải mang cùng `cmp` với phương án VN, hoặc bỏ `cmp` khỏi mọi phương án khi câu dẫn đã nói "trở lên/trở xuống". Sau khi sửa mã, cần dựng lại trắc nghiệm của mọi chủ đề.

---

## Vấn đề hệ thống (chuyển người điều phối)

1. **Hình thức phương án trắc nghiệm để lộ vai trò** (mcq.py/render.py): `cmp` chỉ có ở phương án VN và nước ngoài; mồi và filler là số đơn độ rộng 0 trong khi VN có thể là khoảng. Cả hai làm P(mồi) sai lệch trong phép so sánh P(nước ngoài) với P(mồi) của H1 phần trắc nghiệm, nên phải sửa trước `/freeze questions`.
2. **Giá trị Bộ Y tế ở slot lân cận trùng hoặc nằm trong dung sai của giá trị nước ngoài** (09: 25 kg/m²; 08: 250 IU): nên ghi `moh_neighbour` có hệ thống và đăng ký trước phân tích độ nhạy.
3. **Độ hợp lý của mồi `mirror_arith`**: khi phép phản chiếu rơi vào vùng "bình thường" hoặc vùng vô lý lâm sàng (09: 21 kg/m²), mồi không còn là đối chứng trùng ngẫu nhiên. Đề xuất một bước kiểm độ hợp lý của mồi (người hoặc bác sĩ) ở HG3.x.
4. **Nhiễu trong đoạn A3** (passages.py): dấu chữ ký số có tên người ở 2767/2023 (đoạn 02); số trang trần ở đầu đoạn 03 và 04.

## Kiểm lại theo 6 tiêu chí (tóm tắt)

| atom | (1) duy nhất / nước ngoài không đồng thời đúng | (2) không lộ | (3) EN trung thành | (4) tự nhiên | (5) trắc nghiệm | (6) đơn vị |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | đạt | đạt | đạt | đạt (thừa chữ) | — | đạt (%) |
| 02 | đạt | đạt | đạt | tạm (câu nối) | — | đạt (mmHg) |
| 03 | đạt | đạt | đạt | đạt | — | đạt |
| 04 | **không** (nhánh 100) | đạt | đạt | đạt (60 từ) | — | đạt |
| 05 | đạt | đạt | đạt | đạt | — | đạt |
| 06 | đạt | đạt | đạt | đạt | — | đạt |
| 07 | đạt | đạt | đạt | đạt | — | đạt |
| 08 | đạt | đạt | đạt | đạt | **không** (khoảng vs số đơn; mồi gần UKHSA) | đạt |
| 09 | đạt với Bộ Y tế, nhưng quy nguồn bị nhiễu (25 là ngưỡng béo phì của Bộ Y tế; Mỹ cho người châu Á = 23) | **gợi ý** ("gốc châu Á") | đạt | tạm | **không** (dấu "≥"; mồi 21 vô lý) | đạt |

---

## Phản hồi sửa (26/9/2026, atom-extractor + question-writer, agent AI)

Đã tự kiểm bằng mã: `pilot_merge --only controls` giữ 9/9 mẩu (7 concordant, 2 conflict), loại 0. `qgen.build --only-drafted` cho 26 câu, 9 đoạn A3, 7 mẩu bỏ trắc nghiệm có chủ đích (đối chứng: không có giá trị ngoài tập Bộ Y tế, không có mồi), 0 mục QC không đạt; dựng lại hai lần cho kết quả giống hệt. Chấm thử `grade_short` với 21 câu trả lời tự viết (không dùng đầu ra mô hình): cả 21 đúng kỳ vọng.

- **P-controls-09**
  - Đã bỏ `population.ethnicity`.
  - Viết lại `population.setting` và `population.exclusions` chỉ còn thuộc tính quần thể; phần ghi chú chuyển sang `extraction.notes`.
  - Thêm `foreign` US: USPSTF 2021-08-24, giá trị ≥ 25, sha256 c53c89e6…. Ngưỡng ≥ 23 cho người Mỹ gốc Á chỉ ghi trong notes.
  - Thêm `moh_neighbour` 25: 3087/2020 PDF tr.12, "Béo phì : BMI ≥ 25-30".
  - Không dùng 2919/2014 tr.60, vì trang này thuộc Phần 2 mà manifest ghi đã bị 5904/2019 bãi bỏ.
  - Mồi vẫn là 21, do quy tắc `mirror_arith` sinh, không chọn tay. Đánh giá độ hợp lý của mồi thuộc HG3.5.
  - Mã mới cho mọi phương án cùng dấu "≥" (≥ 23 / ≥ 25 / ≥ 27 / ≥ 21 kg/m2).
  - Cờ `moh_neighbour_overlap` = True, nên `status_with_neighbours` = indistinguishable.
- **P-controls-08**
  - UKHSA (IVIG tiêm tĩnh mạch) khác sản phẩm và đường dùng so với câu hỏi (tiêm bắp), nên xếp khác slot và không thêm vào `foreign`.
  - Thêm `moh_neighbour` 250 IU: 3312/2015 tr.79, trẻ em, dự phòng vết thương. Cờ `moh_neighbour_overlap` = True.
  - Mồi 8.500 IU do quy tắc sinh. Filler nay là 13.000 IU.
  - **Còn treo (mã):** chỉ phương án Bộ Y tế là khoảng; mồi và filler là số đơn.
- **P-controls-04**
  - `population.stage` viết lại cho khớp câu hỏi đã thu hẹp.
  - Thêm `moh_neighbour` ≥ 100 tế bào/µL (2767/2023 tr.23).
  - Lưu ý mã: "tế bào/µL" được hiểu là đơn vị giả định, nên QC đoạn A3 không cờ giá trị 100.
- **P-controls-02, 03, 05**
  - `population` chỉ còn thuộc tính quần thể. Riêng 03 trước đây có ghi chú chứa chính đáp án "5-7 ngày".
- **Đoạn A3**: đoạn 02 không còn dấu chữ ký số; đoạn 03 không còn số trang trần ở đầu.

---

## Phản hồi sửa vòng 3 — theo người kiểm độc lập (26/9/2026, atom-extractor + question-writer, agent AI)

Sao lưu trước khi sửa: `scratchpad/qfix/controls_atoms_before.jsonl` (mẩu, bản vòng 2) và `scratchpad/qfix/controls_before_round2/` (bản nháp, q, p, qc, review). Bản vòng 1 đổi tên thành `controls_atoms_before_round1.jsonl`. Script sửa: `scratchpad/qfix/fix_controls_r3.py` (chạy lại không tạo trùng; mọi span mới được kiểm nguyên văn bằng `verify_span.find_pages` trước khi ghi).

- **[CHẶN] P-controls-09, bỏ sót DR8 3879/2014**
  - **Xác nhận phát hiện.** 3879/2014 Chương 5 tr.247 có Bảng 2 theo TCYTTG ghi "Tăng cân 25 - 29,9"; tr.249 ghi "Áp dụng chỉ số BMI theo TCYTTG (bảng 2)".
  - **Quét DR8 lại toàn bộ `data/interim/text`.** Mọi văn bản hiện hành nói về *tiêu chí chỉ định tầm soát ĐTĐ theo BMI* đều cho 23:
    - 5481/2020 tr.11: "…(BMI ≥ 23 kg/m2) và có kèm một trong số các yếu tố nguy cơ sau:".
    - 3087/2020 tr.7.
    - Bảng hỏi 3087/2020 tr.12: "Thừa cân: BMI 23-25".
  - **Văn bản cùng giá trị 23 nhưng không dùng làm nguồn DR8:**
    - 3879/2014 tr.176 ("…sàng lọc bệnh đái tháo đường typ 2 … BMI trên 23"): phần ĐTĐ típ 2 của 3879/2014 bị 3319/2017 Điều 3 bãi bỏ (manifest).
    - 3280/2011 tr.2: hiệu lực chưa xác nhận.
  - **Giá trị 25 của Bộ Y tế chỉ gặp ở bối cảnh khác:**
    - Phân loại béo phì chung: 3879/2014 ch.5 Bảng 2; 3087/2020 tr.12 (ngưỡng béo phì).
    - Quần thể đã loại: HIV, ung thư, thai kỳ.
    - Ngưỡng *béo phì* trong thang nguy cơ bệnh khác: 2388/2024 tr.20; 3908/2023 tr.35.
  - **Sửa câu hỏi.** Câu cũ hỏi "BMI từ ngưỡng nào trở lên được *xếp là* thừa cân hoặc béo phì", tức phân loại chung, đúng chỗ Bảng 2 áp dụng. Câu mới hỏi "BMI *thấp nhất* là bao nhiêu thì đạt *tiêu chí* thừa cân hoặc béo phì *của chỉ định [tầm soát] này*". VI 59 từ, EN 37 từ.
  - **Sửa mẩu.**
    - Đổi `condition` và `intervention` sang slot tiêu chí tầm soát.
    - Thêm `moh_neighbour` 3879/2014 tr.247 Bảng 2 (≥ 25).
    - `dr8_not_applied` ghi lập luận: bối cảnh phân loại chung, không phải tiêu chí tầm soát; cùng chương dùng Bảng 1 châu Á ≥ 23 và lưu đồ tr.252 "BÉO PHÌ BMI > 23".
    - `supporting_spans` thêm tr.247 Bảng 1, tr.252, tr.176 (ghi rõ không hiện hành) và 5481/2020 tr.11 câu đầy đủ.
    - `vn` giữ {≥ 23}.
  - **Chưa kết luận, chuyển HG2.3.** Còn một rủi ro: tr.249 ghi áp dụng *cả hai* bảng. Nội dung cần quyết định ghi ở `extraction.dr8_pending`:
    - Nếu HG2.3 coi là cùng quần thể: thêm 25 vào `vn`, mẩu thành concordant và ra khỏi tập xung đột.
    - Cho đến khi HG2.3 quyết, áp mặc định an toàn: P-controls-09 không vào tập xung đột xác nhận, chỉ dùng để mô tả hoặc khám phá.
- **[NÊN SỬA] P-controls-09, câu trả lời hai ngưỡng bị chấm 5**
  - Câu mới hỏi một ngưỡng thấp nhất, nên ít gợi kiểu trả lời hai ngưỡng hơn.
  - Nếu mô hình vẫn trả lời "thừa cân ≥ 23; béo phì ≥ 25" thì vẫn nhận nhãn 5. Quy tắc chấm đã đăng ký trước, không đổi. Nhãn 5 không làm tăng π_foreign.
- **[NÊN SỬA] P-controls-08, đoạn A3 và H3**
  - Thêm `moh_neighbour`:
    - SAT 1500 đơn vị: 5642/2015 tr.32 (mục 6.2 dự phòng thụ động sau vết thương) và 3312/2015 tr.79 "SAT 1500UI" (gộp vào mục lân cận 3312/2015 đã có, cạnh HTIG 250 UI).
    - Test SAT 75 đơn vị: 5642/2015 tr.29, trong cùng span của mẩu.
  - "1.500 đơn vị/01 ống" là hàm lượng ống, không phải liều, nên không ghi riêng.
  - QC nay cờ `P-controls-08#A3` với passage_has_alt_value = `neighbour`.
  - Nhãn chấm không đổi: "1.500" và "75" vẫn nhãn 4. Hai giá trị này tách được ở N1; `moh_neighbour_overlap` vốn đã True.
- **[NÊN SỬA] P-controls-08, phương án khoảng so với số đơn: vẫn treo, lỗi mã**
  - `decoys.mirror_arith` giữ độ rộng của giá trị nước ngoài (bằng 0); `rule_filler` giữ độ rộng của anchor.
  - `option_text` bị từ chối với mẩu num, nên không sửa được trong mẩu hay bản nháp.
  - Cần sửa mã hoặc đăng ký trước phân tích độ nhạy trước `/freeze questions`.
- **Bộ chấm, chuyển chủ mã**: "Answer: 23 kg/m^2" vẫn nhận nhãn 5 (unit_mismatch) vì `normalize_vi` chưa đọc "m^2". Tôi không sửa src.
- **[NHỎ] P-controls-09, mồi**: nội dung mục này trong bản chuyển tới bị cắt nên tôi không đọc được đủ.
  - Mồi 21 kg/m2 vẫn do quy tắc `mirror_arith` sinh lại khi gộp; không chọn tay, không làm tròn. `roundness_ok` = False do mã tính.
  - Đánh giá độ hợp lý của mồi thuộc HG3.5.

**Tự kiểm bằng mã (vòng 3)**

| Bước | Kết quả |
| --- | --- |
| `pilot_merge --only controls` | Giữ 9/9 mẩu (7 concordant, 2 conflict), loại 0. Mồi 8500 IU và 21 kg/m2 do quy tắc sinh; dung sai 1250 và 1.0 không đổi. |
| `qgen.build --only-drafted` | 26 câu, 9 đoạn A3, 7 mẩu bỏ trắc nghiệm có chủ đích, 0 mục QC không đạt. Dựng lại lần hai giống từng byte. |
| Schema | Hợp lệ. |
| `verify_span` | 9/9 đạt. |
| Chấm thử | 20/20 câu tự viết có nhãn kỳ vọng ra đúng nhãn. 32/32 chữ cái trắc nghiệm ra đúng nhãn. |

Chi tiết chấm thử:
- **P-controls-08**:
  - Nhãn 2: "3.000–6.000 đơn vị", "3000 to 6000 IU", "5000 IU".
  - Nhãn 4: "500 IU", "500 đơn vị", "1.500 đơn vị", "75 đơn vị", "250 IU".
  - Nhãn 5: "8,500 IU" (cờ mồi), "13.000 IU".
  - Nhãn 6: "không rõ".
- **P-controls-09**:
  - Nhãn 2: "BMI ≥ 23 kg/m²", "23 kg/m2", "23 kg/m² or higher", "23".
  - Nhãn 4: "BMI ≥ 25 kg/m2", "25 kg/m²", "BMI of 25 or more".
  - Nhãn 5: "21 kg/m2" (cờ mồi), "30 kg/m²".
  - Nhãn 6: "I am not sure".
- **Nhãn 3**: không áp dụng, vì cả hai mẩu không có giá trị bản cũ.
