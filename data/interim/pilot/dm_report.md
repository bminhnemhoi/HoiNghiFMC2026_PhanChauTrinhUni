# Báo cáo T1.1 (thí điểm tuần 0) — chủ đề `dm`: Đái tháo đường típ 2 và thai kỳ

Ngày: 2026-09-26 · Người làm: agent atom-extractor + counterpart-matcher (Claude) · File mẩu: `data/interim/pilot/dm.jsonl` (8 mẩu)

> **Cập nhật sau kiểm toán (xem mục 8).** Mục 1–7 là bản gốc trước kiểm toán, giữ lại để truy vết; chỗ sai đã được đánh dấu "[Sửa sau kiểm toán]". Trạng thái hiện hành: **2 xung đột** (P-dm-01, P-dm-03) và **6 đối chứng** (P-dm-02, 04, 05, 06, 07, 08). P-dm-04 (trước là xung đột) và P-dm-05 (trước là indistinguishable) nay là **concordant theo DR8**. Lý do: 3879/2014 có hai bài chưa bị bãi bỏ. Bài THA ở người ĐTĐ chẩn đoán THA từ ≥ 130/80. Bài ĐTĐ thai kỳ nêu cả tầm soát 1 bước lẫn 2 bước.

**Tóm tắt.** Có 8 mẩu, đều qua `vnsoc.schemas atom` và `vnsoc.extract.verify_span`. Trong đó có 3 xung đột (P-dm-01, 03, 04) và 1 lệch phiên bản. Mẩu lệch phiên bản (P-dm-05) có trạng thái **indistinguishable** vì giá trị của Mỹ trùng giá trị bản cũ. Còn lại 4 đối chứng (P-dm-02, 06, 07, 08).

**Hai dòng hạt giống không còn là xung đột** khi áp quy tắc hợp tập giá trị (DR8), nên không tạo mẩu:
- dòng 9 (mục tiêu HA): 5904/2019 đặt mục tiêu < 130/80 cho người THA + ĐTĐ.
- dòng 10 (LDL-C): chính 5481/2020 có ngưỡng < 55 mg/dL ở mục 6.2.

Chi tiết ở mục 4.

---

## 1. Văn bản đã tải

### 1a. Văn bản Bộ Y tế (tải bằng `vnsoc.extract.fetch_pdf` → `data/raw/`)

| Khóa | Nguồn (URL) | sha256 (16) | Số trang | text_kind | Nơi tìm / ghi chú |
|---|---|---|---|---|---|
| 5481/2020 | https://benhviendakhoabaria.vn/sites/default/files/files/tin-tuc/5481_dai_thao_duong_type_2.pdf | 305fc9c51d54418f | 77 | ok | Link chính thức trên daithaoduong.kcb.vn (trang "Hướng dẫn chẩn đoán và điều trị ĐTĐ típ 2") bị hỏng: 302 → `http://%{HTTP_HOST}/404.php` (cả mã hóa NFC lẫn NFD). Bản dùng là bản BV Đa khoa Bà Rịa đăng lại nguyên quyết định. Danh tính: tiêu đề, Điều 3 "thay thế Quyết định số 3319/QĐ-BYT ngày 19/07/2017", dấu ký số "5481 30 12". Lớp chữ để trống số hiệu ("Số: /QĐ-BYT"). |
| 1353/2021 | https://benhviendakhoabaria.vn/sites/default/files/files/tin-tuc/quyet_dinh_1353_dai_thao_duong_type_2.pdf | 404beba5811b8894 | 1 | ok | Cùng nguồn. Văn bản chỉ bổ sung một người biên soạn và sửa "điểm b, mục 3, trang 37" (chế độ insulin cho bệnh nặng không nguy kịch). Không ảnh hưởng mẩu nào. |
| 3319/2017 (bản cũ) | http://benhvienninhphuoc.vn/vanbanphapluat/detail/Quyet-dinh-so-3319-QD-BYT-ngay-19-7-2017-ve-viec-ban-hanh-tai-lieu-chuyen-mon-Huong-dan-chan-doan-va-dieu-tri-dai-thao-duong-tip-2-7/?download=1&id=1 | b5df6fd56fc2c4d5 | 37 | ok | Trang văn bản pháp quy của TTYT/BV Ninh Phước. File là phần tài liệu "Ban hành kèm theo Quyết định số 3319/QĐ-BYT ngày 19 tháng 7 năm 2017". Trang quyết định (id=0) không tải. |
| 1470/2024 | https://bvdkbaclieu.gov.vn/upload/1000079/20240622/387_Quyet_dinh-1470-QD-BYT_d07fdf47d7.pdf | 9e86a45fd39ffc62 | 31 | **scanned_or_empty** | BV Đa khoa Bạc Liêu (.gov.vn). **Không dùng để tạo mẩu** vì máy chưa có OCR. Đã thử thêm: (i) bản Google Drive do BV Sa Đéc liên kết, cũng chỉ là ảnh quét (chỉ đọc thử trong scratchpad, không lưu vào data/raw); (ii) bvgialai.vn không phân giải DNS; (iii) syt.bacgiang.gov.vn không phân giải DNS; (iv) trang tin moh.gov.vn trả 404. Danh tính xác nhận bằng ảnh trang 1: QĐ 1470/QĐ-BYT ngày 29/5/2024, thay QĐ 6173/QĐ-BYT ngày 12/10/2018. |
| 5904/2019 | (đã có sẵn trong data/raw, do agent khác tải) | `5904_2019.pdf` 7cb7cd93fd30cf64 (22 tr.); bản trùng `5904_2019__9e6bbe13.pdf` 9e6bbe13d5705fc8 (68 tr.) | 22 / 68 | xem ghi chú | `5904_2019.pdf` là bản quét đã OCR, chữ rác (ví dụ "BQYTE… QUYETDINH"), có vẻ thiếu trang. `verify_span` đọc đúng file này, nên **không kiểm span được**. Bản 68 trang có lớp chữ nhưng dùng glyph cũ "Ƣ/ƣ" thay "Ư/ư". Tôi chỉ đọc bản 68 trang để kiểm DR8, không tạo mẩu từ đó. **[Sửa sau kiểm toán: sai.]** Khóa `5904/2019__9e6bbe13` đọc được bằng `verify_span`, và `norm()` đã đổi Ƣ→Ư. P-dm-04 nay dùng khóa này trong `dr8_sources`. |

Không truy cập trang thư viện pháp luật tư nhân. Kết quả tìm kiếm từ luatvietnam.vn và hieuluat.vn cũng bị bỏ qua (không phải nguồn chính thức).

### 1b. Nguồn nước ngoài (tải bằng `vnsoc.match.sources`)

| Nguồn | URL | sha256 (16) | Ghi chú |
|---|---|---|---|
| ADA Standards of Care in Diabetes—2026: bộ slide toàn bộ khuyến cáo (ADA phát hành, 2025-12-08) | https://professional.diabetes.org/sites/dpro/files/2025-12/2026-ADA-SOC-Slide-Deck-all-recommendations-12-8-25.pptx | 034f66ea0fda2bab | Là bản ADA **hiện hành** tại 10/2026. Chữ trong slide được trích bằng zipfile (thẻ `a:t`). Bảng 2.1 và 2.8 là ảnh, tôi đọc bằng mắt nên `verified_by: null`. **Lỗi công cụ:** file đã ghi vào cache (`034f66ea0fda2bab1012.html`) nhưng `sources.py` bị lỗi ở bước HTMLParser (pptx không phải HTML/PDF). Mục của nó cũng không có trong `index.json`, có lẽ do agent khác ghi đè cùng lúc. sha256 tính lại trực tiếp từ file. |
| WHO/IDF 2006: Definition and diagnosis of diabetes mellitus and intermediate hyperglycaemia | https://iris.who.int/server/api/core/bitstreams/ef6a81ae-5db3-4c5c-9136-c047bd8f8344/content | ae658daa4370559b | 50 trang. `grep` thấy "7.0mmol/l (126mg/dl)" ở tr. 7 và 9. |
| WHO 2011: Use of glycated haemoglobin (HbA1c) in the diagnosis of diabetes mellitus | https://iris.who.int/server/api/core/bitstreams/db9b9d3d-f95e-4797-9d2b-c78dcef0133f/content | 5a7d55740b4215d9 | 25 trang. `grep` thấy "6.5%" ở tr. 3 và 6. |
| WHO 2013: Diagnostic criteria and classification of hyperglycaemia first detected in pregnancy | https://iris.who.int/server/api/core/bitstreams/612e0faa-04b5-4984-abcb-5fe3b1703677/content | 70afa6fb83a23557 | 62 trang. `grep` thấy "5.1-6.9 mmol/l (92 -125 mg/dl)" ở tr. 5 và 37. |
| WHO fact sheet Hypertension | https://www.who.int/news-room/fact-sheets/detail/hypertension | 2779af89d3929cb2 | Lấy từ cache chung (agent khác đã tải cùng ngày). `grep` thấy "≥140 mmhg … ≥90 mmhg". Ngày phiên bản ghi "2025": trang có nhiều ngày, nhiều khả năng ngày của fact sheet là 25/9/2025, **cần người kiểm**. |

Các nguồn bị chặn hoặc không đọc được:
- diabetesjournals.org (cả trang bài lẫn PDF ADA 2025/2026) trả 403.
- PMC (pmc.ncbi.nlm.nih.gov, www.ncbi.nlm.nih.gov/pmc) trả trang reCAPTCHA.
- Europe PMC: fullTextXML trả 500, PDF trả 403.
- E-utilities efetch chỉ trả siêu dữ liệu (NXB không cho XML toàn văn).
- PubMed (trang tìm kiếm) bị challenge.
- ACOG Practice Bulletin 190: trang chỉ có mục lục (nội dung trả phí). Trang ghi "Reaffirmed 2026" và "July 2024 Clinical Practice Update". Chưa lấy được giá trị.
- ADA 2025 §9 (PMC11635045) đọc được qua WebFetch: Rec 9.23 "A1C >10% … hoặc glucose ≥300 mg/dL". Không có sha256 nên không ghi vào `foreign`. Giá trị trùng ADA 2026, nên theo quy tắc cũng không cần ghi bản trước.

---

## 2. Bảng mẩu

| id | slot | VN (5481/2020) | Nước ngoài (hệ thống: giá trị, phiên bản) | Trạng thái | Trang PDF (in) |
|---|---|---|---|---|---|
| P-dm-01 | threshold: HbA1c để cân nhắc insulin sớm (ĐTĐ típ 2) | ≥ 9% | US: A1C > 10% (ADA 2026 Rec 9.20) | **conflict** (tol 0,5; mồi 8%) | 25 (23) |
| P-dm-02 | threshold: glucose để cân nhắc insulin sớm | ≥ 300 mg/dL (16,7 mmol/L) | US: ≥ 300 mg/dL (ADA 2026 Rec 9.20) | concordant | 25 (23) |
| P-dm-03 | threshold: tuổi bắt đầu tầm soát cho mọi người | từ 45 tuổi | US: từ 35 tuổi (ADA 2026 Rec 2.12b) | **conflict** (tol 5; mồi 55 tuổi) | 12 (10) |
| P-dm-04 | threshold: HA tâm thu để chẩn đoán THA ở người ĐTĐ (mẩu mới) | ≥ 140 mmHg | US: ≥ 130 mmHg (ADA 2026 Rec 10.1); WHO_global: ≥ 140 (fact sheet) | **conflict** (tol 5; mồi 150 mmHg) | 34 (32) |
| P-dm-05 | procedure: chiến lược tầm soát ĐTĐ thai kỳ tuần 24–28 | một bước (NPDNG 75 g) | US: một bước **hoặc** hai bước (ADA 2026 slide 44, Bảng 2.8) | **indistinguishable** (bản cũ 3319/2017 cho phép cả 2 bước) — lệch phiên bản | 12 (10); bản cũ 3319/2017 tr. 4 |
| P-dm-06 | threshold: glucose đói chẩn đoán ĐTĐ | ≥ 7,0 mmol/L (126 mg/dL) | WHO_global: 7,0 (WHO/IDF 2006); US: 7,0/126 (ADA 2026 Bảng 2.1, đọc từ ảnh) | concordant | 11 (9) |
| P-dm-07 | threshold: HbA1c chẩn đoán ĐTĐ | ≥ 6,5% | WHO_global: 6,5% (WHO 2011); US: 6,5% (ADA 2026 Bảng 2.1, đọc từ ảnh) | concordant | 11 (9) |
| P-dm-08 | threshold: glucose đói NPDNG 75 g chẩn đoán ĐTĐ thai kỳ | ≥ 5,1 mmol/L (92 mg/dL) | WHO_global: 5,1–6,9 (WHO 2013); US: 92 mg/dL (ADA 2026 Bảng 2.8, một bước, đọc từ ảnh) | concordant | 12 (10) |

Ghi chú kỹ thuật:
- Mồi của mẩu num tạo bằng `mirror_decoy` (quy tắc `mirror_arith`). `check_decoy` = [] ở cả 8 mẩu. `tolerance` và `conflict_status` tính bằng `finalize()`.
- Mẩu đối chứng có đơn vị kép (mg/dL và mmol/L): tập `vn` và `foreign` ghi cả hai dạng như văn bản gốc. Lý do: đối chứng không có mồi nên dung sai gần 0, và 126 mg/dL = 6,994 mmol/L sẽ bị chấm là "không khớp 7,0" nếu chỉ ghi một đơn vị.
- Đã chạy thử `grade_short` trên đáp án giả:
  - P-dm-01: "A1C > 10%" → foreign US; "8%" → decoy.
  - P-dm-03: "35 tuổi" → foreign US.
  - P-dm-04: "130/80 mmHg" → foreign US.
  - P-dm-05: "hai bước (50 g rồi 100 g)" → temporal + US (đúng như dự kiến vì mẩu indistinguishable).
  - Các đáp án đúng đều được nhãn `correct`.
  - Lỗi phát hiện được: xem mục 6.

---

## 3. Ứng viên bị loại và lý do

1. **Dòng hạt giống 9 (mục tiêu HA < 140/90 vs ADA < 130/80): không tạo mẩu xung đột.**
   - 5481/2020 Bảng 4 (tr. 21): "Huyết áp Tâm thu <140 mmHg, Tâm trương <90 mmHg Nếu đã có biến chứng thận, hoặc có yếu tố nguy cơ tim mạch do xơ vữa cao: Huyết áp <130/80 mmHg".
   - Nhưng 5904/2019, Phần 3 "lồng ghép THA và ĐTĐ tại trạm y tế xã" (bản 68 trang, tr. PDF 28, số in 19) ghi mục tiêu "Huyết áp mmHg < 130/80*". Chú thích ghi HA tâm thu 120 đến < 130 mmHg với người < 65 tuổi, và 130 đến < 140 với người cao tuổi (văn bản ghi nhầm "(người <65 tuổi)" lần hai).
   - Theo DR8 (hợp các văn bản hiện hành cho cùng quần thể), ADA < 130/80 nằm **trong** tập Việt Nam. Vậy mẩu không thỏa điều kiện "giá trị nước ngoài không đồng thời đúng theo Bộ Y tế".
   - Ngoài ra, 5481 tr. 34 (6.1.2) tự cho phép "<130/90-80 mmHg" ở BN trẻ và "<130/80-85" nếu có bệnh thận mạn.
   - Không thể đưa 5904 vào mẩu kiểm span được, vì file chuẩn `5904_2019.pdf` là bản OCR rác. **[Sửa sau kiểm toán: sai.]** Khóa `5904/2019__9e6bbe13` kiểm span được. Kết luận "không phải xung đột theo DR8" vẫn đúng.
2. **Dòng hạt giống 10 (LDL-C khi có bệnh tim mạch xơ vữa): không phải xung đột; chưa tạo mẩu đối chứng.**
   - Bảng 4 (tr. 21): "LDL cholesterol <70 mg/dL (1,8 mmol/L) nếu đã có bệnh tim mạch vữa xơ, hoặc có thể thấp hơn <50 mg/dL nếu có yếu tố nguy cơ xơ vữa cao".
   - Nhưng mục 6.2.2 cùng văn bản (tr. 36) ghi: "BN đái tháo đường nguy cơ rất cao (có bệnh tim mạch xơ vữa, …) cần hạ LDL-C ≥50% hoặc dưới 1.4 mmol/L (55 mg/dL)".
   - Tập VN hợp lệ vì thế là {< 70, < 55, < 50}. ADA 2026 Rec 10.27 (< 55 mg/dL, slide 214) nằm trong tập → **concordant**. Đây là một mâu thuẫn nội bộ của 5481 (kết quả phụ theo §1.2).
   - Không tạo mẩu vì schema chỉ có một `span` trên một trang, không chứa đủ cả ba giá trị. Nếu chỉ ghi {70, 50} thì `finalize` sẽ báo sai là conflict. Nếu chỉ ghi {55} thì đáp án "70" sẽ bị chấm nhầm là lệch phiên bản (3319/2017 tr. 7 cũng ghi < 70). Đề xuất mở rộng schema ở mục 6.
3. **Dòng 12 (GLP-1 RA/SGLT2i):** đã bị loại theo đề cương, không làm.
4. **Ngưỡng dưới của rối loạn glucose lúc đói (IFG)** là ứng viên xung đột tốt với WHO nhưng chưa làm được.
   - VN: 5,6 mmol/L. Chỉ thấy trong 5904/2019 (bản 68 trang): "5,6 đến 6,9 mmol/L (100 đến 125 mg/dL)". 5481 không định nghĩa tiền ĐTĐ.
   - WHO 2006: 6,1 mmol/L (tr. 8–9, đã `grep`). ADA: 5,6 (trùng VN).
   - Chưa làm vì không kiểm span 5904 được. Sẽ thành mẩu xung đột với WHO_global khi 5904 có bản chuẩn đọc được.
   - **[Sửa sau kiểm toán]** Lý do hoãn này sai, vì 5904 đọc được (khóa `__9e6bbe13`). Nhưng ứng viên này **chưa sạch**: 3280/2011 tr. 3 ghi IFG từ 6,1 mmol/L (110 mg/dL), mà hiệu lực của 3280/2011 chưa được xác nhận. Xem mục 8.4.
5. **Mục tiêu HbA1c/HA ở người cao tuổi, bệnh thận mạn:** không tạo mẩu.
   - Chồng lấn với khoảng 130–< 140 của 5904.
   - ADA khuyến khích tâm thu < 120 mmHg (Rec 10.4/11.5) chỉ là mục tiêu phụ, và mồi phản chiếu sẽ trùng chính mục tiêu < 140 của VN.
6. **Aspirin phòng ngừa thứ phát:** không tạo mẩu. VN 75–160 mg/ngày (5481 tr. 36), ADA 75–162 mg/ngày (ADA 2026 Rec 10.33, trong slide). Khác biệt 2 mg là giả do quy cách viên 81 mg của Mỹ, không có ý nghĩa lâm sàng.
7. **ACOG (hai bước):** không ghi được giá trị, vì trang trả phí và PubMed bị chặn.

---

## 4. Sai lệch so với bộ hạt giống (§3.3)

| Dòng | Bảng hạt giống | Kết quả đối chiếu văn bản | Hệ quả |
|---|---|---|---|
| 8 | 45 vs ADA 2025: 35; confirmed_low_stakes | Khớp. ADA **2026** Rec 2.12b vẫn 35. 3319/2017 cũng 45 (không lệch phiên bản). | P-dm-03, conflict |
| 9 | < 140/90; < 130/80 nếu biến chứng thận/nguy cơ cao vs ADA < 130/80; confirmed | Giá trị 5481 khớp. **Nhưng** 5904/2019 (hiện hành, trạm y tế xã, người THA + ĐTĐ) ghi < 130/80. 5481 tr. 34 cũng cho phép < 130/80 ở BN trẻ hoặc có bệnh thận mạn. | **Không còn là xung đột theo DR8.** Không tạo mẩu. Cần quyết định ở HG1.2. |
| 10 | < 70, có thể < 50 vs ADA < 55; fixed | Bảng 4 khớp. **Nhưng** 5481 tr. 36 (6.2.2) có < 55 mg/dL cho ASCVD / nguy cơ rất cao. | **Không phải xung đột** (ADA < 55 ∈ tập VN). Là mâu thuẫn nội bộ 5481. Chưa tạo mẩu vì giới hạn schema. |
| 11 | A1C ≥ 9% hoặc glucose ≥ 300 vs ADA > 10% hoặc ≥ 300 | Khớp nguyên văn (tr. 25). ADA 2026 Rec 9.20, ADA 2025 Rec 9.23. | Đã tách: P-dm-01 conflict, P-dm-02 concordant. Seed ghi `unit: "%"` cho cả dòng; mẩu glucose dùng mg/dL. |
| 25 | 1470/2024 "75 g một bước" vs "ACOG ưu tiên hai bước"; confirmed_low_stakes_not_rechecked | 5481 và 1470 (đọc bằng mắt) đều chỉ nêu một bước. **Không kiểm được "ACOG ưu tiên hai bước"**. ADA 2026 chấp nhận cả hai. **Phát hiện mới:** bản cũ 3319/2017 (tr. 4) cho phép cả 1 bước và 2 bước. | P-dm-05 là mẩu lệch phiên bản, nhưng **indistinguishable**: giá trị "hai bước" của Mỹ trùng bản cũ. Không dùng cho kiểm định xác nhận. |
| Đối chứng (danh sách hạt giống) | "tiêu chuẩn chẩn đoán ĐTĐ", "ngưỡng ĐTĐ thai kỳ 5,1/10,0/8,5" | Khớp với WHO 2006/2011/2013 và ADA 2026. | P-dm-06, 07, 08 |

Mẩu thêm ngoài bảng hạt giống: **P-dm-04** (ngưỡng chẩn đoán THA ở người ĐTĐ: VN ≥ 140 vs ADA ≥ 130). Cùng gốc khác biệt với dòng 6, nên cần thống nhất `conflict_family` với agent chủ đề THA (tôi đặt `htn_dx_threshold_us`). Theo hiểu biết chung (chưa kiểm bằng nguồn đã tải), văn bản 5481 giống cấu trúc ADA các năm trước khi đổi định nghĩa (130/80 để đo lại, 140/90 để chẩn đoán). Nếu đúng vậy thì Mỹ đã đổi định nghĩa, còn Bộ Y tế giữ nguyên. Cần kiểm ADA bản cũ trước khi viết điều này vào bài.

---

## 5. Việc cần người kiểm ở HG1.2

1. So span và trang của 8 mẩu với PDF 5481/2020.
   - Nên đối chiếu bản BV Bà Rịa với bản ký số trên kcb.vn khi link kcb.vn hoạt động lại.
   - Trang PDF khác số trang in: PDF 11/12/25/34 tương ứng số in 9/10/23/32.
2. Các giá trị ADA đọc từ ảnh bảng (P-dm-06, 07, 08; `verified_by: null`): kiểm lại Bảng 2.1 (slide 19) và Bảng 2.8 (slide 45) trong file pptx đã tải (sha256 034f66ea…).
3. P-dm-04: mồi 150 mmHg (quy tắc cố định) trùng ngưỡng "khởi trị hai thuốc" của ADA Rec 10.7 (≥ 150/90, đã thấy ở slide 206). Theo hiểu biết chung (chưa kiểm nguồn), nó có thể trùng cả ngưỡng JNC8 cho người ≥ 60 tuổi. Cần quyết định giữ hay loại mẩu khỏi phân tích mồi. Câu hỏi cũng phải hỏi rõ "ngưỡng **chẩn đoán**", vì cùng đoạn văn có 130/80 là ngưỡng đo lại.
4. Quyết định về dòng 9 và DR8 với 5904/2019. Hai lựa chọn:
   - (a) bỏ hẳn;
   - (b) giới hạn quần thể theo tuyến (bệnh viện, không áp dụng 5904). Cách này dễ bị phản biện vì mô hình không biết tuyến.

   Tôi đề nghị (a) và báo cáo đây là mâu thuẫn nội bộ Bộ Y tế.
5. Dòng 10: đồng ý xếp là mâu thuẫn nội bộ 5481 (Bảng 4 so với mục 6.2.2) và chọn cách biểu diễn (xem đề xuất schema).
6. 1470/2024: cần OCR hoặc người đọc tr. PDF 13–14 để xác nhận và thêm vào hợp tập giá trị.
   - Tôi đọc bằng mắt: tr. 13 (in 8) ghi "Thực hiện tầm soát ĐTĐTK cho mọi thai phụ từ tuần thứ 24 - 28 … với nghiệm pháp dung nạp 75gram glucose".
   - Tr. 14 (in 9), Bảng 3: ≥ 92 / ≥ 180 / ≥ 153 mg/dL (5,1 / 10,0 / 8,5 mmol/L), "Nếu có từ 1 giá trị lớn hơn hay bằng là chẩn đoán ĐTĐTK".
   - Khớp 5481, nhưng chưa phải bằng chứng kiểm được bằng máy.
7. 5904/2019: corpus-librarian cần chọn bản chuẩn. Bản 68 trang (9e6bbe13…) đầy đủ hơn hẳn bản 22 trang OCR rác. Khi xong có thể thêm mẩu IFG (xung đột với WHO) và làm lại dòng 9.
8. Ngày phiên bản của WHO fact sheet Hypertension (đang ghi "2025").
9. ACOG: nếu có quyền truy cập, ghi giá trị ACOG (Practice Bulletin 190, reaffirmed; Clinical Practice Update 7/2024) cho P-dm-05.
10. P-dm-01: kiểm xem AACE (Mỹ) các bản cũ có dùng ngưỡng ~9% hay không. Nếu có, giá trị VN trùng một nguồn Mỹ cũ. Hiện chưa kiểm, không ghi vào dữ liệu.

---

## 6. Đề xuất bổ sung config và mã (không tự sửa)

1. `normalize_vi.UNIT_ALIASES`:
   - Thêm `"mmol/mol"` (HbA1c IFCC) như một đơn vị riêng, để số "48 mmol/mol" không bị gán nhầm đơn vị mặc định "%". Hiện đáp án "HbA1c ≥ 9% (75 mmol/mol)" bị tách thành 2 giá trị (multi → unattributed), và "48 mmol/mol" bị chấm sai.
   - Nếu cần quy đổi: %NGSP = 0,09148 × IFCC + 2,152. Đây là quan hệ affine, `convert()` hiện chỉ hỗ trợ nhân hệ số.
   - Thêm `"mg%"` → `mg/dL` (1470/2024 ghi "mg/dl hay mg%").
   - Thêm `"gam"` → `g`.
2. `grade`: đặt sàn dung sai tương đối (ví dụ 1%) khi so sánh giá trị đã quy đổi đơn vị, để mẩu đối chứng không phụ thuộc cách ghi đơn vị kép.
3. `schemas.Atom`: cho phép nhiều span (ví dụ `vn_spans: [{page, span, value_idx}]`) để ghi hợp tập giá trị từ nhiều trang hoặc văn bản (DR8, dòng 10), và `verify_span` kiểm từng span.
4. `match/sources.py`:
   - Ghi `index.json` có khóa file hoặc ghi nguyên tử theo kiểu đọc-sửa-ghi có lock. Hiện nhiều agent ghi cùng lúc làm mất mục (mục pptx ADA bị mất).
   - Không gọi HTMLParser cho nội dung nhị phân (zip/pptx). Nên trích chữ pptx (thẻ `a:t`) và ghi số slide như `[[page n]]`.
5. `extract/verify_span.norm`: map glyph cũ `Ƣ→Ư`, `ƣ→ư` (bản 5904 68 trang).
6. `configs/grading.yaml`: không cần thêm thuốc cho các mẩu này.

---

## 7. Lệnh đã chạy để kiểm

```
PYTHONUTF8=1 .venv/bin/python -m vnsoc.schemas atom data/interim/pilot/dm.jsonl        → OK 8 dòng hợp lệ (atom)
PYTHONUTF8=1 .venv/bin/python -m vnsoc.extract.verify_span data/interim/pilot/dm.jsonl → OK: 0 mẩu không đạt
finalize() tính lại khớp giá trị ghi trong file; check_decoy() = [] cho cả 8 mẩu
```

---

## 8. Sau kiểm toán (2026-09-26, agent sửa lỗi)

Đầu vào: `data/interim/pilot/dm_verify.md` (6 pass, 2 fix, 0 reject).

Tôi tự kiểm lại mọi bằng chứng bằng công cụ của dự án. Tôi chỉ ghi `dm.jsonl` và file này. Không chạy OCR. Không ghi vào `data/raw`, `data/cache` hay `state/`. Ảnh trang chỉ dựng trong scratchpad.

### 8.1 Kết quả sau khi sửa

| id | Trước kiểm toán | Sau khi sửa | Thay đổi chính |
|---|---|---|---|
| P-dm-01 | conflict (tol 0,5; mồi 8%) | **conflict**, không đổi | — |
| P-dm-02 | concordant | concordant, không đổi | — |
| P-dm-03 | conflict (tol 5; mồi 55) | **conflict**, không đổi | Thêm `dr8_sources`: 3087/2020 tr. 7 cũng 45 tuổi |
| P-dm-04 | conflict (tol 5; mồi 150 mmHg) | **concordant (DR8)** | Tập VN = {≥ 140 (5481), ≥ 130 (3879/2014)}; family `htn_us_130_80`; WHO 2025-09-25; bỏ mồi |
| P-dm-05 | indistinguishable | **concordant (DR8)** | Nhãn loại trừ nhau `one_step_only` / `two_step_allowed` (sửa lỗi chấm); tập VN thêm `two_step_allowed` từ 3879/2014 |
| P-dm-06, 07, 08 | concordant | concordant, không đổi | — |

- **Tổng:** 8 mẩu, gồm 2 xung đột và 6 đối chứng. Không mẩu nào bị loại. Không còn mẩu lệch phiên bản dùng được.
  - P-dm-05 vẫn có `superseded` 3319/2017 (cho phép 2 bước). Nhưng theo DR8, giá trị đó nằm trong tập VN hiện hành.
- **Kiểm tra lại cả 8 mẩu:**
  - `vnsoc.schemas atom` → OK 8 dòng.
  - `vnsoc.extract.verify_span` → OK: 0 mẩu không đạt. Mọi span trong `dr8_sources` cũng được công cụ kiểm nguyên văn.
  - `finalize()` cho lại đúng `tolerance` và `conflict_status` đã ghi.
  - `check_decoy()` = [] cho cả 8 mẩu.
  - Không có trường chỉ-bác-sĩ.
- **Kiểm tay:** `span_on_page` = True cho 2 span bản cũ 3319/2017 tr. 4 và 2 span 6173/2018 tr. 12–13 (`supporting_spans`).

### 8.2 Phát hiện mới khi tự kiểm lại: kiểm toán chưa xét 3879/2014

**Văn bản.** 3879/2014 là "Hướng dẫn chẩn đoán và điều trị bệnh nội tiết – chuyển hóa":
- nguồn kcb.vn; `data/raw/3879_2014.pdf`, sha256 `d7565fdb81be2b85`; 275 trang, có lớp chữ;
- manifest ghi `current`.

Chương 4 có nhiều bài riêng (mục lục tr. 8):
- "Bệnh đái tháo đường typ 2" (tr. 174–187);
- "Tăng huyết áp ở người bệnh đái tháo đường" (tr. 212–213);
- "Bệnh đái tháo đường và thai kỳ" (tr. 228);
- "Đái tháo đường thai kỳ" (tr. 234–235).

**Phạm vi bãi bỏ.** Tôi tải trang quyết định 3319/2017 từ kcb.vn vào scratchpad (1 trang quét ký, sha256 `ca840b6dd0c5853a…`, khớp manifest) và đọc ảnh.
- Điều 3 chỉ "Bãi bỏ nội dung 'Hướng dẫn chẩn đoán và điều trị đái tháo đường típ 2'" trong 3879/2014. Tức là chỉ bài tr. 174.
- 5481/2020 Điều 3 chỉ thay 3319/2017 (tr. 1, lớp chữ).
- 6173/2018 tr. 2 không có điều khoản thay thế.
- 1470/2024 Điều 3 chỉ thay 6173/2018. Tôi xem ảnh tr. 1 trong scratchpad; bản quét nên chưa kiểm bằng máy.

→ Theo quy tắc hiệu lực (chỉ dựa trên điều khoản thay thế/bãi bỏ; đề cương §1.2 và prompt mục 4), hai bài sau của 3879/2014 **còn hiệu lực**, nên phải vào hợp tập giá trị (DR8):

1. **Tr. 213, bài THA ở người ĐTĐ:** "THA ở người bệnh ĐTĐ được chẩn đoán khi huyết áp (HA) tâm thu ≥ 130 mmHg và/ hoặc huyết áp tâm trương ≥ 80mmHg sau hai lần đo ở hai ngày khác nhau".
   - Giá trị này trùng ADA 2026 Rec 10.1.
   - → **P-dm-04 không còn là xung đột.**
2. **Tr. 235, bài ĐTĐ thai kỳ:**
   - mục 2.1 "Tầm soát một bước" (75 g);
   - mục 2.2 "Tầm soát hai bước" (50 g → 100 g), cho thai phụ tuần 24–28.
   - → **P-dm-05: chiến lược "một hoặc hai bước" của ADA nằm trong tập VN.**

**Nguồn gốc mâu thuẫn nội bộ của 5481.** Đây là giải thích bằng văn bản cho phát hiện số 3 của kiểm toán; kiểm toán chỉ đoán là "giống ADA cũ".
- 5481 tr. 34–35, mục 6.1.3a ("130–139 / 80–89 … thay đổi lối sống … tối đa 3 tháng … thuốc") gần như chép từ 3879/2014 tr. 213. Ở 3879, THA ở người ĐTĐ bắt đầu từ 130/80, nên đoạn đó nhất quán.
- 3319/2017 (tr. 14) đổi ngưỡng chẩn đoán thành ≥ 140/90 nhưng giữ đoạn điều trị cũ. 5481 chép lại nguyên cả hai.

**Hai cách hiểu, cùng một hệ quả.** Nếu HG1.2 kết luận hai bài của 3879/2014 đã hết hiệu lực trên thực tế (dù không có điều khoản bãi bỏ):
- giá trị 130/80 và "hai bước" thành giá trị Bộ Y tế **cũ** trùng giá trị Mỹ;
- P-dm-04 và P-dm-05 thành **indistinguishable**.

Trong cả hai cách hiểu, **không mẩu nào trong hai mẩu này dùng được cho kiểm định xác nhận (H1)**. Tôi mã hóa theo quy tắc đã đăng ký: DR8, dùng trạng thái `current` của manifest. Tôi ghi rõ cách chuyển sang cách hiểu kia trong `extraction.notes`.
- Đã chạy thử cách hiểu hẹp cho P-dm-05 (bỏ `two_step_allowed` khỏi `vn`, thêm 3879 vào `superseded`): `finalize` → indistinguishable. Các đáp án "hoặc" → temporal, đúng như kiểm toán muốn.

### 8.3 Từng mục kiểm toán: đã sửa, giữ, và lý do

**P-dm-04**

| Mục kiểm toán | Xử lý | Lý do |
|---|---|---|
| 1. `conflict_family` → `htn_us_130_80` | **Đã sửa** | Cùng cụm với P-htn-01/03. |
| 2. Đổi sang `value_kind: bp`, mồi 150/100 | **Không áp dụng; giữ `num` (HA tâm thu)** | Theo DR8, tập VN có 130/80 từ 3879 tr. 213. `parse_bps` chỉ đọc dạng "x/y", nên không đọc lại được câu "≥ 130 mmHg và/ hoặc … ≥ 80mmHg" (3879) hay "≥140 mmHg và/hay … ≥90 mmHg" (5481). Với `bp`, `verify_span` sẽ báo thiếu giá trị VN. Tôi không lấy câu *mục tiêu* "< 130/80" để lách bộ kiểm. Mẩu đã concordant nên không cần mồi; lo ngại "mồi 150 trùng ADA 10.7" không còn. Đề xuất mở rộng `parse_bps` (8.6), sau đó chuyển sang `bp`. |
| 3. Ghi chú mâu thuẫn nội bộ mục 6.1.3 | **Đã sửa, mở rộng** | Thêm nguồn gốc từ 3879 tr. 213 (8.2). Câu hỏi phải hỏi đúng "ngưỡng CHẨN ĐOÁN"; đã thêm `population.setting`. |
| 4. WHO `version_date` → 2025-09-25 | **Đã sửa** | `sources grep` thấy "hypertension 25 september 2025" ở đầu trang (sha `2779af89…`). |
| 5. Thay fact sheet bằng WHO 2021 | **Giữ fact sheet** | WHO 2021 là ngưỡng khởi trị, không phải định nghĩa (agent THA cũng ghi như vậy). Trạng thái không đổi. |
| Thêm | `dr8_sources` | 3879/2014 tr. 213 (130/80); 5904 (`__9e6bbe13`) tr. 11 ("≥ 140/90" và bảng phân độ: 130–139/85–89 là "bình thường cao"). Mọi span đều được `verify_span` kiểm. |
| Thêm | ADA Rec 10.1 | Kiểm lại bằng trích XML slide 200 từ bản đệm pptx (sha256 `034f66ea…` khớp). `sources grep` vẫn lỗi `AssertionError` với pptx (đã tái hiện). Giữ `verified_by: "auto"` như mẩu đã pass. |

**P-dm-05**

| Mục kiểm toán | Xử lý | Lý do / bằng chứng |
|---|---|---|
| 1. Lỗi chấm: "1 bước hoặc 2 bước" → correct | **Đã sửa** theo hướng (a), đổi tên nhãn | Hai nhãn loại trừ nhau, viết bằng regex có lookahead (P-tbhiv-03/04 cũng dùng lookahead trong `cat_options`). `one_step_only` = có dấu hiệu 1 bước và không có dấu hiệu 2 bước, trừ khi 2 bước bị phủ định ngay trước (≤ 3 từ: "không dùng phương pháp 2 bước", "rather than the two-step"). `two_step_allowed` = có 2 bước / 50 g / 100 g và không bị phủ định. Tôi dùng tên `two_step_allowed` thay cho `one_or_two_step` vì đáp án chỉ nêu "2 bước" cũng thuộc tập của ADA và 3319, không thuộc "chỉ 1 bước". |
| 2. Chưa dẫn 1470/2024 | **Đã kiểm thêm; chưa thể thành span** | Tôi xem ảnh tr. 1 và tr. 13 (số in 8) trong scratchpad: tầm soát mọi thai phụ tuần 24–28 bằng "nghiệm pháp dung nạp 75gram glucose". Chưa có sidecar OCR chính thức → không đưa vào `dr8_sources`, không đổi `guideline`. |
| 3. Chưa kiểm 6173/2018 | **Đã kiểm** | `data/raw/6173_2018.pdf` (sha `52857b966d71181b`, có lớp chữ, agent khác tải 11:39). Tr. 12–13: chỉ NPDNG 75 g một bước; `--find` "2 bước", "hai bước", "50 g", "100 g" → []. Không lệch phiên bản trên nhánh 6173→1470. Ghi vào `supporting_spans`, không ghi vào `superseded` vì giá trị trùng bản hiện hành. |
| 4. `seed_row` 25 (ACOG) | Giữ | ACOG vẫn chưa kiểm được (trang trả phí). |
| Thêm | DR8 3879/2014 tr. 235 | Tập VN = {`one_step_only`, `two_step_allowed`} → **concordant**. Hệ quả: mọi đáp án nêu một chiến lược đều "đúng", nên mẩu **không có giá trị làm đối chứng**. Đề nghị loại khỏi bộ đối chứng, trừ khi HG1.2 chọn cách hiểu hẹp. |

**Chấm thử `grade_short` sau khi sửa P-dm-05** (tập VN theo DR8 / cách hiểu hẹp):

| Đáp án | Nhãn | DR8 | Hẹp |
|---|---|---|---|
| "phương pháp 1 bước: NPDNG 75 g" | one_step_only | correct | correct |
| "2 bước (50 g rồi 100 g)" | two_step_allowed | correct | temporal (+US) |
| "có thể dùng 1 bước (75 g) hoặc 2 bước (50 g/100 g)" | two_step_allowed | correct | temporal (+US) |
| "Either the one-step 75-g OGTT or the two-step approach" | two_step_allowed | correct | temporal (+US) |
| "1 bước 75 g, không dùng phương pháp 2 bước" | one_step_only | correct | correct |
| "one-step 75 g OGTT rather than the two-step approach" | one_step_only | correct | correct |
| "không nhất thiết 1 bước, có thể 2 bước" | two_step_allowed | correct | temporal |
| "glucose lúc đói" / "không rõ" | — | abstain | abstain |

- Giới hạn còn lại: một dòng đáp án nêu cả hai hệ thống mà không phủ định (ví dụ "ADA: một hoặc hai bước; Việt Nam: một bước") sẽ bị gán `two_step_allowed`. Cần xử lý ở `grade.matches` (8.6).

**P-dm-04, chấm thử (`num`, DR8):**
- "≥ 140 mmHg" và "≥ 140/90" → correct (WHO);
- "130/80" và "≥ 130" → correct (US);
- "135" và "150" → unattributed.

**Các mẩu pass (01, 02, 03, 06, 07, 08):** giữ nguyên giá trị và trạng thái. Chỉ P-dm-03 được thêm một `dr8_sources` (3087/2020 tr. 7, mục 3.1.3 "Tất cả mọi người từ tuổi 45 trở lên"). Tôi đã rà các bài chưa bị bãi bỏ của 3879/2014 và 3280/2011 cho từng mẩu:
- **P-dm-01:** 3280/2011 tr. 5 và 7 ghi insulin khi "HbA1C trên 9,0% mà … lúc đói trên 15,0 mmol/l". Vẫn là 9%, nên ADA > 10% vẫn nằm ngoài tập. Xung đột đứng vững.
- **P-dm-03:** 3280 tr. 2 ghi "Tuổi ≥ 45 và có một trong các yếu tố nguy cơ" (nhóm khác). Bài ĐTĐ típ 2 của 3879 đã bị bãi bỏ. Xung đột đứng vững.
- **P-dm-06, 07:** không có giá trị mâu thuẫn.
- **P-dm-08:** 3879 tr. 235 cũng ghi một bước "≥ 92 mg/dL (5,1 mmol/L)", khớp. Cùng trang có bảng tham khảo "theo WHO và EASD" (75 g: lúc đói ≥ 7 và ≥ 6 mmol/L). Tôi coi đó là thông tin về tổ chức khác, không phải khuyến cáo của Bộ Y tế (cần người xác nhận). Nếu tính theo DR8 thì tập chỉ rộng thêm; mẩu vẫn concordant.

### 8.4 Những điểm tôi không đồng ý với kiểm toán (có bằng chứng)

1. **"P-dm-04 conflict tol 5 ✓", "P-dm-05 indistinguishable đúng".** Kiểm toán không xét 3879/2014. Với bằng chứng ở 8.2, cả hai là concordant theo DR8, hoặc indistinguishable nếu HG1.2 coi hai bài của 3879 đã hết hiệu lực. Không cách hiểu nào cho trạng thái conflict.
2. **"Ứng viên IFG là mẩu xung đột sạch với WHO_global (tạo P-dm-09)".** Chưa sạch, nên **tôi chưa tạo P-dm-09**.
   - VN hiện hành: 3087/2020 tr. 7 (Bảng 1: "5,6 – 6,9 mmol/L (100 – 125 mg/dL)", kcb.vn, sha `c329ac9fa2f0162a`) và 5904 tr. 18. Cả hai đều 5,6.
   - Nhưng 3280/2011 tr. 3 ghi IFG "từ 6,1 mmol/l (110 mg/dl) đến 6,9 mmol/l", trùng WHO 2006. Manifest ghi 3280/2011 là `current` tạm thời, "hiệu lực chưa xác nhận", và tệp có dấu hiệu xuất từ trang thư viện pháp luật tư nhân (siêu dữ liệu "LawSoft"). Nếu 3280 còn hiệu lực thì DR8 cho tập VN {5,6; 6,1} → concordant.
   - Lưu đồ 3879/2014 tr. 177 cũng dùng 6,1, nhưng nằm trong bài ĐTĐ típ 2 đã bị bãi bỏ.
   - → Chỉ tạo P-dm-09 (span 3087/2020 tr. 7) sau khi HG1.2 quyết hiệu lực của 3280/2011.
3. **Đổi sang `bp`:** không làm được mà vẫn qua `verify_span` (8.3). Đây là giới hạn của bộ đọc, không phải bất đồng về nội dung.

### 8.5 Tồn đọng cho HG1.2 (người thật)

1. **Hiệu lực các bài ĐTĐ còn lại của 3879/2014** (tr. 188–245; đặc biệt tr. 212–213 THA ở người ĐTĐ và tr. 234–235 ĐTĐ thai kỳ).
   - Còn hiệu lực → giữ mã hóa hiện tại (P-dm-04, 05 concordant; đếm là mâu thuẫn nội bộ, kết quả phụ §1.2).
   - Hết hiệu lực trên thực tế → cần căn cứ bằng văn bản. Khi đó chuyển P-dm-04 và P-dm-05 sang indistinguishable theo hướng dẫn trong `extraction.notes`.
   - Manifest nên đổi 3879/2014 thành `partial` và thêm `partially_amended_by: ["3319/2017"]`. Việc này của corpus-librarian.
2. **Hiệu lực và nguồn gốc 3280/2011** (quyết định cho IFG / P-dm-09). Không ảnh hưởng 8 mẩu hiện có.
3. **P-dm-05:** giữ trong bộ đối chứng hay loại? Theo DR8, mọi đáp án đều đúng. Tôi đề nghị loại khỏi bộ đối chứng.
4. **1470/2024:** cần sidecar OCR chính thức (`vnsoc.extract.ocr --key 1470/2024 --pages 12-14`) và người đối chiếu ảnh tr. 13–14.
5. **P-dm-04:** câu hỏi phải nói rõ "ngưỡng chẩn đoán", đo tại phòng khám, đo lại vào ngày khác.
6. **Liên chủ đề (agent THA):** P-htn-01 ("người trưởng thành", chẩn đoán ≥ 140/90) chưa loại người ĐTĐ khỏi quần thể. Với người ĐTĐ, tập VN có 130/80 (3879 tr. 213). Đề nghị thêm "không ĐTĐ" vào `population` của P-htn-01, như P-htn-03 đã làm.
7. Các mục cũ còn nguyên:
   - ACOG cho P-dm-05;
   - ADA Living Standards 2026 (có sửa Rec 2.12b, 9.20, 10.1 hay Bảng 2.8 giữa năm hay không);
   - xác nhận 5481/2020 còn hiện hành trước ngày đóng băng 15/10/2026;
   - `verified_by` của giá trị đọc từ ảnh bảng ADA (P-dm-06, 07, 08).
8. **Tổng mẩu chủ đề dm giảm:** còn 2 xung đột thật và 0 mẩu lệch phiên bản dùng được (trước: 3 xung đột, 1 lệch phiên bản). Mẩu thay thế tiềm năng: IFG với WHO (mục 2).

### 8.6 Đề xuất mã/config (không tự sửa)

1. **`normalize_vi.parse_bps`:** đọc được dạng "tâm thu ≥ X mmHg và/hoặc (huyết áp) tâm trương ≥ Y mmHg" (và "SBP ≥ X … DBP ≥ Y"). Sau đó chuyển P-dm-04 sang `bp`, cùng dạng với P-htn-01/03.
2. **`grade.matches` / `grade_short` cho kind `cat`:** khi tập nhãn của đáp án lớn hơn tập VN và nhãn thừa thuộc một giá trị nước ngoài hoặc bản cũ xung đột, xử lý như nhánh `drugs` (multi → 1 hoặc 5). Nhãn loại trừ bằng regex của P-dm-05 chỉ là cách chữa tạm trong dữ liệu.
3. **`match/sources.py`:** đọc được pptx (zip, thẻ `a:t`, `[[page n]]` theo số slide). Hiện ADA 2026 và ESC 2024 đều là pptx; slide ESC là ảnh EMF.
4. **`data/interim/pdf_choice.json`:** chọn `5904_2019__9e6bbe13.pdf` cho khóa `5904/2019`. Việc này của corpus-librarian.
5. **Manifest:** 3879/2014 → `partial` (3319/2017 Điều 3); ghi quyết định về 3280/2011.
6. **Kế hoạch phân tích:** đếm số mẩu đổi trạng thái vì DR8 (ở dm: P-dm-04, P-dm-05) như kết quả phụ "mâu thuẫn nội bộ Bộ Y tế".

### 8.7 Văn bản đã đọc thêm ở bước này

| Khóa | sha256 (16) | Trang đã đọc | Ghi chú |
|---|---|---|---|
| 3879/2014 | d7565fdb81be2b85 | 3, 8, 174, 177, 208, 212–213, 228, 230, 233–235 | kcb.vn, có lớp chữ |
| 3319/2017, trang quyết định | ca840b6dd0c5853a | 1 (ảnh, scratchpad) | kcb.vn; không lưu vào `data/raw` |
| 6173/2018 | 52857b966d71181b | 2, 12, 13 (+ `--find`) | Có lớp chữ |
| 3087/2020 | c329ac9fa2f0162a | 1, 7, 8 | kcb.vn, có lớp chữ |
| 3280/2011 | 5f66da370601976a | 1, 2, 3, 5, 6, 7 | Hiệu lực và nguồn gốc chưa xác nhận; chỉ đọc để kiểm DR8 |
| 1470/2024 | 9e86a45fd39ffc62 | 1, 13 (ảnh, scratchpad) | Bản quét |
| 5481/2020 | 305fc9c51d54418f | 1, 34, 35 | — |
| 5904/2019__9e6bbe13 | 9e6bbe13d5705fc8 | 11, 18, 27 | — |

```
PYTHONUTF8=1 .venv/bin/python -m vnsoc.schemas atom data/interim/pilot/dm.jsonl        → OK 8 dòng hợp lệ (atom)
PYTHONUTF8=1 .venv/bin/python -m vnsoc.extract.verify_span data/interim/pilot/dm.jsonl → OK: 0 mẩu không đạt
finalize() khớp giá trị ghi trong file; check_decoy() = [] cho cả 8 mẩu
```
