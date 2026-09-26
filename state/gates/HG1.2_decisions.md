# HG1.2 — Các quyết định cần bạn chốt (đi kèm `HG1.2_checklist.md`)

Soạn 26/9/2026, sau 2 vòng phản biện câu hỏi và mẩu thí điểm (AI; chưa có bác sĩ thật duyệt).
Mỗi mục có **mặc định**: nếu bạn không trả lời trước khi chấm thí điểm, tôi áp mặc định và ghi vào `docs/DECISIONS.md`.
Trả lời trong chat, ví dụ: `HG1.2 quyết định: 1b, 2 có, 3 không, ...` (không cần trả lời hết một lần).

**Thứ tự kiểm checklist nếu ít thời gian:** kiểm trước 24 mẩu **xung đột**, vì chúng quyết định H1 và abstract:
P-anaphylaxis-03, P-anaphylaxis_ocr-01/-05, P-controls-08/-09, P-dengue-01/-02/-03/-04, P-dm-01/-03, P-hbv-07,
P-htn-01/-03, P-immunization-01/-02, P-malaria_ocr-01/-03/-04/-06/-07, P-tbhiv-01/-03/-05.
Sau đó mới tới 41 mẩu đối chứng hoặc không phân biệt được.

## A. Quyết định về giá trị chuẩn (ảnh hưởng trực tiếp kết quả)

1. **Tiêm chủng — TT 52/2025 đã hết hiệu lực từ 01/7/2026** (TT 13/2026 thay thế nhưng không có lịch tiêm). Ba mẩu P-immunization-01/-02/-04 đang neo vào TT52. Chọn:
   (a) tìm văn bản hướng dẫn chuyên môn hiện hành của Cục Phòng bệnh (việc HG2.3);
   (b) dùng lịch công bố gần nhất và ghi rõ trong bài;
   (c) bỏ 3 mẩu.
   Manh mối: QĐ 1327/2014 tr.6 (mũi sởi đầu 9 tháng, chưa rõ hiệu lực); QĐ 1637/2015 (MR 18 tháng, chưa có trong kho).
   **Mặc định: (c) cho phân tích chính; vẫn báo cáo mô tả.**
2. **Sốt rét thai 3 tháng đầu (P-malaria_ocr-01).** QĐ 315/2015 (sản phụ khoa, trang PDF 75) có áp dụng cho sốt rét P. falciparum chưa biến chứng, nhiễm ở vùng kháng chloroquin, không?
   - Nếu KHÔNG: tập Bộ Y tế chỉ còn quinin + clindamycin.
   - Nếu CÓ: giữ tập hiện tại và báo cáo đây là mâu thuẫn giữa các văn bản. Không kết luận "gây hại" khi chưa có bác sĩ xác nhận.

   **Mặc định: KHÔNG.**
3. **P-malaria_ocr-07.** Có hợp giá trị 1,5 mg/kg/ngày của QĐ 3312/2015 tr.521 vào tập Bộ Y tế (DR8) không? **Mặc định: không** (văn bản không ghi số lần/ngày).
4. **P-controls-09 (BMI trong chỉ định tầm soát ĐTĐ).** Bảng 2 chương 5 của QĐ 3879/2014 (thang WHO, thừa cân 25–29,9) có phải giá trị Bộ Y tế hiện hành cho cùng câu hỏi không?
   - Nếu CÓ: mẩu thành đối chứng (concordant).
   - Nếu KHÔNG: giữ ≥ 23.

   **Mặc định: giữ ≥ 23, nhưng loại 09 khỏi tập xung đột xác nhận (chỉ mô tả).** Lưu ý: 3879/2014 bị QĐ 3319/2017 bãi bỏ một phần.
5. **Phản vệ — cách đọc DR8.** Có ba cách: theo nguyên nhân (do thuốc/thức ăn), không phụ thuộc nguyên nhân, hoặc chỉ theo TT 51/2017. Lựa chọn quyết định P-anaphylaxis_ocr-01/-05 là xung đột hay đối chứng. Kèm theo đó là phạm vi "quần thể lân cận":
   (a) gồm cả liều người lớn/không nêu tuổi → không có mồi;
   (b) không gồm → có lại mồi 390 µg.

   **Mặc định: không phụ thuộc nguyên nhân + (a).**
6. **Định nghĩa "bối cảnh lân cận"** — quyết một lần cho mọi chủ đề: có tính cách đo khác (Holter/tự đo tại nhà, P-htn-01), chất phân tích khác (AST, P-hbv-01/-02), nhóm phân loại khác (ngưỡng béo phì, P-controls-09) không? Nếu tính, câu trả lời 130/80 ở P-htn-01 có thể do nhầm cách đo chứ không chắc do hướng dẫn Mỹ. **Mặc định: không tính (theo câu chữ đăng ký); đưa vào phân tích độ nhạy N1.**
7. **Mồi trùng giá trị thật:**
   - **P-hbv-01:** mồi 25 U/L trùng ULN nữ của AASLD/3310. **Mặc định: loại khỏi phép so nước ngoài–mồi.**
   - **P-tbhiv-05:** mồi TDF + 3TC + EFV trùng phương án thay thế của WHO 2014. Chọn (a) đổi sang TDF + 3TC + doravirine, hoặc (b) giữ mồi và gắn cờ. **Mặc định: (a).** Trong lượt thí điểm đã chạy, câu trắc nghiệm của mẩu này được loại khỏi phép so H1.
8. **P-hbv-04.** "ALT > ULN ít nhất 2 lần" (không kèm khoảng thời gian) hiện được chấm là **bội số** (nhãn 3, bản cũ). Chấm là **số lần đo** (nhãn 2) thì phải báo trước khi đóng băng. **Mặc định: giữ cách chấm hiện tại.**
9. **P-dm-08.** Có ghi WHO 1999 (≥ 7,0 mmol/L) làm giá trị nước ngoài không? Nếu ghi, mẩu có thể vào H1 với mồi 3,0 mmol/L, một giá trị phi sinh lý. **Mặc định: không ghi.**

## B. Nguồn cần người mở (tôi không truy cập được)

- **P-hbv-07** (mẩu xung đột duy nhất của HBV): giá trị Mỹ "≥ 2 năm" mới chỉ thấy trên slide 33 của AASLD. Cần đối chiếu toàn văn Ghany 2025 (Hepatology, doi 10.1097/HEP.0000000000001549, bài trả phí).
- **Phản vệ:** RCUK "< 6 tháng: 100–150 µg" (tr.29) và WHO Pocket Book 150 µg (tr.133). Hai giá trị đang ở trạng thái `verified_by auto`.
- **P-dengue-02:** giá trị CDC "10 mg/kg for 1–2 hrs".
- **P-htn-01/-03:** 3 giá trị ESC lấy từ slide dạng EMF; cách ghép cột Bảng 1 của 3192 (130/80 là Holter, 135/85 là tự đo tại nhà).
- **Tải về `data/raw` (HG2.3, chỉ từ nguồn chính thức):**
  - QĐ 5456/2019 (vaac.gov.vn lỗi chứng chỉ TLS);
  - bản .doc của QĐ 1622/2014 (vncdc.gov.vn);
  - TT 08/1999, nếu muốn có giá trị bản cũ cho phản vệ.

## C. Kiểm tay chữ OCR

- **16 đoạn A3 lấy từ trang OCR** (cột `passage_ocr` trong `results/tables/pilot_question_qc.csv`). So với ảnh trang (lệnh `python -m vnsoc.extract.verify_span --image <văn bản> <trang>`). Đoạn không kiểm kịp được gắn cờ trong phân tích độ nhạy H3.
- **Span P-anaphylaxis_ocr-04** ("TIEM BAP") và **-05** ("1⁄3") chép lỗi OCR của TT 51 tr.9 và tr.20. Giá trị số đã được kiểm với ảnh, nhưng bạn cần so lại.

## D. Để sau (không chặn thí điểm)

- **HG3.5 (chấm mù, không xem đầu ra):** độ hợp lý của các mồi 21 kg/m² (controls-09), 8.500 IU (controls-08), 150/100 mmHg (htn-01/-03), BPaZ (tbhiv-01), RE (tbhiv-03), albumin (dengue-03).
- **HG3.9 (bác sĩ thật):**
  - tình huống lâm sàng của các câu hỏi;
  - 200 µg/6 kg ≈ 33 µg/kg (TT51);
  - mâu thuẫn nội tại của QĐ 2760 (dengue-03);
  - giới hạn tuổi mục trẻ em của 162/2024 (tbhiv-01).
- **HG2.9 (trước 7/10):** chốt D1–D16 trong `review/prereg/response.md`. D13–D16 là mới (định nghĩa k^MCQ, quy tắc lớp thuốc trung lập, dải làm tròn mồi, đồng xu chọn phía filler).
