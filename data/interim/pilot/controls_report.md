# T1.1 thí điểm — chủ đề `controls` (đối chứng liên chuyên khoa: đột quỵ, COPD, Whitmore, sốt mò, béo phì)

Ngày: 2026-09-26 · agent: claude (atom-extractor + counterpart-matcher) · File mẩu: `data/interim/pilot/controls.jsonl` (9 mẩu)

**Kết quả kiểm:** `python -m vnsoc.schemas atom` → OK 9/9; `python -m vnsoc.extract.verify_span` → OK 9/9 (0 mẩu không đạt). Mọi mẩu đã qua `finalize()` và `check_decoy() == []`.

> **Cập nhật sau kiểm toán (26/9/2026) — xem §7.** Các mục 1–6 dưới đây là bản TRƯỚC kiểm toán, giữ nguyên để truy vết; chỗ nào mâu thuẫn thì §7 thay thế. Ba đính chính lớn: (a) tệp `data/raw/3874_2018.pdf` thực chất là **QĐ 4562/2018**; (b) **6101/2019 (Whitmore) có tồn tại** và 2147/2026 cũng có phác đồ melioidosis; (c) theo DR8, khoảng cách liều ceftazidim và liều meropenem của Whitmore **không phải xung đột**. Số mẩu và trạng thái không đổi: 9 mẩu = 7 concordant + 2 conflict, 0 bị loại.

**Tóm tắt:** 7 mẩu đối chứng (concordant) + 2 mẩu xung đột (conflict). **Không làm được phần đột quỵ** (không tìm được PDF 3312/2024 từ nguồn chính thức). **Béo phì 2892/2022 không tải được** (liên kết chính thức hỏng) nên dòng hạt giống 13 được thay bằng ngưỡng BMI ≥ 23 trong 5481/2020. **Whitmore 6101/2019 không tìm thấy**; phần Whitmore lấy từ bảng kháng sinh nhiễm khuẩn huyết của 5642/2015. **4 mẩu COPD dựa trên 2767/2023, trong khi đề cương §3.1 ghi 2131/2026 đã thay bản này; chưa tìm được bản 2026.**

---

## 1. Văn bản đã tải / đã dùng

### 1a. Văn bản Bộ Y tế

| Khóa | URL | sha256 (16) | Số trang | text_kind | Nơi tìm / ghi chú |
| --- | --- | --- | --- | --- | --- |
| 2767/2023 (COPD) | https://kcb.vn/upload/2005611/20231028/2767__QD__HD_chan_doan_va_dieu_tri_COPD_2023final_signed_e5721.pdf | 16816ec28c986975 | 87 | ok | Đã có sẵn trong data/raw. Liên kết lấy từ trang kcb.vn/phac-do (QĐ 2767 ngày 04/07/2023). Trang 1: Điều 3 thay QĐ 3874/QĐ-BYT ngày 26/06/2018; ngày ký số 04-07-2023. |
| 5642/2015 (một số bệnh truyền nhiễm) | https://kcb.vn/upload/2005611/20210723/598cf44932833df0d644c6b27564f169Truyen-nhiem-1.pdf | 541e140fccfa3269 | 86 | ok | **Tải mới** (status downloaded). Trang kcb.vn/phac-do/quyet-dinh-so-5642-qd-byt-ngay-31-12-2015-... (tìm bằng ô tìm kiếm kcb.vn "5642"). PDF trang 3: "Số: 5642/QĐ-BYT … ngày 31 tháng 12 năm 2015". Bản sách NXB Y học 2016; số trang in = số trang PDF. |
| 5481/2020 (ĐTĐ típ 2) | https://benhviendakhoabaria.vn/sites/default/files/files/tin-tuc/5481_dai_thao_duong_type_2.pdf | 305fc9c51d54418f | 77 | ok | Đã có sẵn (chủ đề dm tải; link daithaoduong.kcb.vn hỏng). Chỉ dùng tr. 11 cho mẩu BMI. |
| 3874/2018 (COPD, **bản cũ**) | https://kcb.vn/upload/2005611/20210723//B%E1%BB%99-Y-t%E1%BA%BF-H%C6%B0%E1%BB%9Bng-d%E1%BA%ABn-ch%E1%BA%A9n-%C4%91o%C3%A1n-v%C3%A0-%C4%91i%E1%BB%81u-tr%E1%BB%8B-BPTNMT-b%E1%BA%A3n-c%E1%BA%ADp-nh%E1%BA%ADt-2018.pdf | 68a2f132db3ba1c2 | 86 | ok | **[Đính chính §7: tệp này là QĐ 4562/QĐ-BYT 19/7/2018 (PDF tr.4), trùng sha256 với 4562_2018.pdf; chưa có bản gốc 3874/2018]** **Tải mới**. Dùng để kiểm lệch phiên bản cho các slot COPD. FEV1/FVC, PaO2 và thời gian corticoid giống 2767/2023, nên không ghi `superseded`. |

**Không tải được:**

| Văn bản | Đã thử | Kết quả |
| --- | --- | --- |
| 3312/2024 (đột quỵ não) | Ô tìm kiếm kcb.vn với các từ: "đột quỵ", "đột quỵ não", "điều trị đột quỵ", "tiêu sợi huyết", "alteplase", "thiếu máu não", "3312", "5331"; trang kcb.vn/phac-do, kcb.vn/tai-lieu/huong-dan-chan-doan-dieu-tri; dotquy.kcb.vn | Không thấy. "3312" chỉ trả về 3312/QĐ-BYT **2015** (bệnh thường gặp ở trẻ em). Chỉ thấy tài liệu phục hồi chức năng đột quỵ và QĐ 86/QĐ-KCB 2014 (tiêu chuẩn chất lượng, không phải hướng dẫn chẩn đoán–điều trị). **dotquy.kcb.vn có chứng chỉ TLS sai** (cấp cho *.colombo.vn, *.vhv.vn) nên curl/WebFetch đều bị từ chối. **Hết hạn mức WebSearch của phiên (200/200)** nên không tìm tiếp được. |
| 2892/2022 (béo phì) | Trang daithaoduong.kcb.vn/huong-dan-chan-doan-va-dieu-tri-benh-beo-phi có liên kết `…/upload/files/QĐ  ban hành HD điều trị béo phì_ 2022_10_18_ Final.docx_signed.pdf` | Máy chủ trả 302 → `http://%{HTTP_HOST}/404.php` với cả NFC lẫn NFD và nhiều UA/referer. Wayback không có bản lưu. Tìm "béo phì", "2892" trên kcb.vn: không có quyết định. |
| 6101/2019 (Whitmore) | Tìm trên kcb.vn: "Whitmore", "Burkholderia", "melioidosis", "6101"; bvbnd.vn ?s=Whitmore / ?s=6101 | Chỉ có tin khuyến cáo phòng bệnh Whitmore (23/04/2026, Cục Phòng bệnh), không có hướng dẫn điều trị. **Chưa xác nhận được văn bản 6101/2019 có tồn tại.** **[Đính chính §7: có tồn tại — corpus-librarian tải lúc 11:30 từ benhvienhatrung.vn (bản ký số VOffice 07/01/2020), sha a3baf8fa8f119d73, bản quét]** |
| 2131/2026 (COPD mới theo đề cương §3.1) | Tìm "2131", "tắc nghẽn mạn tính", "phổi tắc nghẽn mạn tính 2026" trên kcb.vn | Chỉ thấy 2767/2023 và 3874/2018. |

### 1b. Nguồn nước ngoài (chỉ lưu giá trị + vị trí, không chép đoạn văn)

| Nguồn | Hệ thống | Phiên bản | URL | sha256 (16) | Cách kiểm |
| --- | --- | --- | --- | --- | --- |
| GOLD 2026 Report v1.3 | OTHER | 08/12/2025 | https://goldcopd.org/wp-content/uploads/2026/01/GOLD-REPORT-2026-v1.3-8Dec2025_WMV2.pdf | fa12e8e2dbd2090e (248 tr.) | `sources grep`. Tải công khai, không cần đăng ký. |
| NT Health Melioidosis Guideline (Darwin) | OTHER | duyệt 10/2/2024 | https://digitallibrary.health.nt.gov.au/nthealthserver/api/core/bitstreams/78de80ef-afe5-4aea-860a-6ea801354542/content | 54cfa18f35dd96bf (13 tr.) | `sources grep`. Trang melioidosis HCP của CDC dẫn tới tài liệu này làm "2024 melioidosis treatment guidelines". |
| WHO Technical Note: treatment of tetanus in humanitarian emergencies (WHO/HSE/GAR/DCE/2010.2) | WHO_global | 01/2010 | https://iris.who.int/server/api/core/bitstreams/f9f77952-80b0-4a25-92d7-edce3241af13/content | 637bb6b9e79db08a (6 tr.) | `sources grep` + đọc text trang 5 |
| WHO fact sheet "Obesity and overweight" | WHO_global | 08/12/2025 | https://www.who.int/news-room/fact-sheets/detail/obesity-and-overweight | dc1d9d01f6f38480 | `sources grep` ("overweight is a BMI greater than or equal to 25") |
| WHO WPRO/IASO/IOTF "The Asia-Pacific perspective: redefining obesity and its treatment" (IRIS 10665/206936) | WHO_WPRO | 02/2000 | https://iris.who.int/server/api/core/bitstreams/53228dc6-9520-421b-b5a2-f826967090cb/content | b11886340b039690 (56 tr.) | **PDF quét, không có lớp chữ** (719 ký tự). Đọc bằng mắt trên ảnh PDF p.19, Table 2.2. **needs_human_check** |
| CDC Clinical Overview of Scrub Typhus | US | last reviewed 15/05/2024 | https://www.cdc.gov/typhus/hcp/clinical-overview/clinical-overview-of-scrub-typhus.html | **null** | cdc.gov chặn script (403), nên đọc bằng WebFetch. **needs_human_check** |
| CDC Tetanus: Clinical Care and Treatment | US | last reviewed 08/09/2026 | https://www.cdc.gov/tetanus/hcp/clinical-care/index.html | **null** | Như trên. **needs_human_check** |
| CDC Melioidosis Clinical Overview | US | last reviewed 30/09/2025 | https://www.cdc.gov/melioidosis/hcp/clinical-overview/index.html | null | WebFetch. Chỉ ghi khoảng cách liều (ceftazidime mỗi 6–8 giờ), không có liều, nên không ghi vào mẩu nào. |
| EID 2012 Lipsitz et al., bảng 3 (wwwnc.cdc.gov/eid/article/18/12/12-0638-t3) | — | 2012 | (như tên) | e908abebf125a2c7 | Tải được nhưng HTML không chứa nội dung bảng, nên **không dùng**. |

---

## 2. Bảng mẩu

| id | slot | VN (tập giá trị) | Nước ngoài (hệ thống: giá trị, phiên bản) | Trạng thái | Trang PDF (in) |
| --- | --- | --- | --- | --- | --- |
| P-controls-01 | threshold — FEV1/FVC chẩn đoán COPD (sau giãn phế quản) | < 70% (2767/2023) | OTHER: GOLD 2026 < 0,7 (=70%) | **concordant** | 12 (11) |
| P-controls-02 | threshold — chỉ định thở oxy dài hạn | PaO2 ≤ 55 mmHg | OTHER: GOLD 2026 ≤ 55 mmHg (7,3 kPa) | **concordant** | 23 (22) |
| P-controls-03 | duration — glucocorticoid toàn thân trong đợt cấp COPD | 5–7 ngày | OTHER: GOLD 2026 5 ngày (40 mg/ngày) | **concordant** | 31 (30) |
| P-controls-04 | threshold — bạch cầu ái toan dự báo đáp ứng ICS | ≥ 300 /µL | OTHER: GOLD 2026 ≥ 300 /µL | **concordant** | 23 (22) |
| P-controls-05 | dose — doxycyclin cho sốt mò ở người lớn, mỗi lần | 100 mg (0,1 g × 2 lần/ngày) (5642/2015) | US: CDC 100 mg × 2 lần/ngày (2024) | **concordant** | 63 (63) |
| P-controls-06 | dose — ceftazidim cho nhiễm khuẩn huyết do B. pseudomallei, mỗi lần | 2 g (mỗi 8 giờ) (5642/2015) | OTHER: Darwin 2024 2 g (mỗi 6 giờ) | **concordant** (chỉ liều) | 84 (84) |
| P-controls-07 | dose — metronidazol cho uốn ván, mỗi lần | 500 mg (mỗi 6–8 giờ) (5642/2015) | WHO_global: 500 mg mỗi 6 giờ (2010) | **concordant** | 29 (29) |
| P-controls-08 | dose — HTIG (globulin miễn dịch uốn ván từ người) để điều trị uốn ván | 3000–6000 đơn vị, tiêm bắp (5642/2015) | WHO_global: 500 đơn vị (2010); US: CDC 500 IU, một liều (2026) | **conflict** · mồi 8500 IU (mirror_arith) · dung sai 1250 | 29 (29) |
| P-controls-09 | threshold — BMI thừa cân/béo phì ở người trưởng thành (châu Á) | ≥ 23 kg/m² (5481/2020) | WHO_global: ≥ 25 (fact sheet 12/2025); WHO_WPRO: ≥ 23 (2000) | **conflict** (chỉ với WHO_global) · mồi 21 kg/m² (mirror_arith) · dung sai 1,0 | 11 (9) |

`conflict_family`: P-08 `tetanus_htig_dose_500iu`; P-09 `bmi_overweight_asian_cutoff_who_global` (seed_row 13). Các mẩu đối chứng để `conflict_family = null` và không có mồi, theo cùng quy ước với các chủ đề dm/tbhiv/hbv.

**Thử chấm nhanh bằng `grade_short`** (chỉ để kiểm quy tắc, không phải dữ liệu nghiên cứu):
- Câu trả lời "500 IU" cho P-08 → nhãn 4 foreign [US, WHO_global]; "8500 IU" → nhãn 5 kèm cờ mồi.
- "BMI ≥ 25" cho P-09 → nhãn 4 [WHO_global]; "23" → nhãn 2.
- **Lỗi phát hiện được** (xem mục 6):
  - P-01: "FEV1/FVC < 0.70" bị chấm nhãn 5, vì tỉ số không được đổi sang %.
  - P-02: "7.3 kPa" không parse được.
  - P-05: "100 mg x 2 lần/ngày" bị chấm nhãn 5, vì "2 lần" được đọc thành 2 mg.

---

## 3. Ứng viên bị loại và lý do

1. **Tiêu sợi huyết tĩnh mạch trong 4,5 giờ và liều alteplase 0,9 mg/kg (hay 0,6 mg/kg)**: không có PDF 3312/2024 (mục 1a), nên không kiểm được phía Việt Nam. Vì vậy chưa tải AHA/ASA 2019 và ESO 2021. **Chưa trả lời được câu hỏi "Việt Nam dùng 0,6 hay 0,9 mg/kg"; không đoán.**
2. **[Đính chính §7: nay CÓ giá trị VN — 2147/2026 tr.53 và 6101/2019 tr.4–5; là ứng viên đối chứng cho vòng sau]** **Whitmore: tấn công ≥ 10–14 ngày; co-trimoxazol duy trì 3–6 tháng**: 5642/2015 không nêu thời gian điều trị hay pha diệt trừ cho B. pseudomallei, và không có 6101/2019. Không có giá trị Việt Nam nên không tạo mẩu.
3. **[Đính chính §7: KHÔNG phải xung đột — hợp tập VN (DR8) gồm 1 g của 6101/2019 và 1–2 g của 2147/2026]** **Whitmore: liều meropenem** (Việt Nam 500 mg/lần mỗi 8 giờ, tr. 84; Darwin 2024 1 g mỗi 8 giờ, 2 g nếu thần kinh). Đây là **xung đột thật**, nhưng chưa tạo mẩu vì:
   - chỉ tiêu của chủ đề là 1–2 xung đột;
   - quần thể lệch: Darwin chỉ dùng meropenem ở ICU;
   - nếu 6101/2019 tồn tại thì tập giá trị Việt Nam có thể khác (DR8).
   → Đề xuất đưa vào pha chính sau khi có 6101/2019. Mồi dự kiến theo `mirror_geom`: 250 mg.
4. **[Đính chính §7: KHÔNG phải xung đột — 6101/2019 ghi 6–8 giờ, 2147/2026 ghi 6 giờ]** **Whitmore: khoảng cách liều ceftazidim** (Việt Nam 8 giờ; Darwin 6 giờ; CDC 6–8 giờ, bao gồm cả 8). Là xung đột với OTHER, trùng với US. Chưa tạo mẩu vì cùng lý do như mục 3.
5. **Sốt mò: thời gian 5 ngày**: CDC chỉ ghi "ít nhất 3 ngày sau khi hết sốt", không phải số ngày cố định, nên không có đối chiếu số.
6. **Sốt mò: azithromycin cho phụ nữ có thai**: CDC chỉ ghi "tham vấn chuyên gia truyền nhiễm", không có giá trị.
7. **COPD: SpO2 mục tiêu 88–92% trong đợt cấp** (2767/2023 tr. 35): không tìm được chuỗi này trong văn bản GOLD 2026 (nhiều khả năng nằm trong hình) nên không xác nhận được.
8. **COPD: liều corticoid trong đợt cấp**: 2767/2023 ghi 30–40 mg/ngày, GOLD ghi 40 mg/ngày (trùng). Bản cũ 3874/2018 ghi "1 mg/kg/ngày" (PDF tr. 36; tr. 38 ghi methylprednisolon 1–2 mg/kg/ngày). → **Ứng viên lệch phiên bản** 3874/2018 → 2767/2023. Chưa tạo mẩu vì cần cân nặng trong câu hỏi, và normalizer chưa đổi được mg/kg/ngày sang mg/ngày. Chuyển cho nhóm lệch phiên bản.
9. **Uốn ván: thời gian kháng sinh 7–10 ngày**: WHO 2010 không nêu số ngày; trang CDC không nêu kháng sinh cụ thể.
10. **Nhiễm khuẩn huyết (30 ml/kg dịch, HATB ≥ 65 mmHg)**: không có trong 5642/2015.
11. **Béo phì: béo phì độ I 25–29,9 (2892/2022)**: không có PDF, nên chỉ làm ngưỡng thừa cân/béo phì ≥ 23 từ 5481/2020.

---

## 4. Sai lệch so với bộ hạt giống / đề cương

1. **Dòng 13 (béo phì)**:
   - Văn bản gốc 2892/2022 không lấy được từ nguồn chính thức (liên kết hỏng).
   - Thay bằng 5481/2020 tr. 11: "thừa cân hoặc béo phì (BMI ≥ 23 kg/m2)". Giá trị 23 khớp cận dưới của dòng 13.
   - WHO_WPRO 2000 Table 2.2 xác nhận overweight ≥ 23, at risk 23–24.9, obese I 25–29.9, obese II ≥ 30. Đây đúng là thang mà hạt giống gán cho Việt Nam, nên nhãn "trùng WHO khu vực" là đúng.
   - WHO toàn cầu (fact sheet 08/12/2025): overweight ≥ 25, obesity ≥ 30. Xung đột với WHO_global được **xác nhận**.
   - Phần "béo phì độ I 25–29,9 theo 2892/2022" **chưa kiểm được**.
2. **[Đính chính §7: với 6101/2019 và 2147/2026, liều, khoảng cách và thời gian đều trùng Darwin → đề cương gọi Whitmore là đối chứng là ĐÚNG]** **Đối chứng "điều trị bệnh Whitmore" (§3.3) chỉ đúng một phần**:
   - Với văn bản Bộ Y tế tìm được (5642/2015), liều ceftazidim/lần trùng quốc tế.
   - Nhưng liều meropenem (500 mg so với 1 g) và khoảng cách liều ceftazidim (8 giờ so với 6 giờ) khác Darwin 2024.
   - Không nên coi toàn bộ "điều trị Whitmore" là đối chứng.
3. **"Tiêu sợi huyết trong 4,5 giờ" (§3.3)**: chưa kiểm được vì không có 3312/2024. **Số hiệu 3312/2024 cũng chưa xác nhận**: kcb.vn chỉ có 3312/QĐ-BYT năm 2015 (nhi khoa).
4. **COPD (§3.1)**:
   - Đề cương ghi bản hiện hành là 2131/QĐ-BYT 14/07/2026, nhưng không tìm thấy. Các mẩu P-01…P-04 dựa trên 2767/2023, **có thể không còn hiệu lực**.
   - Đề cương ghi 2767/2023 "81 trang"; PDF thực tế có 87 trang.
5. **5642/2015 chỉ còn hiệu lực một phần**: sách có chương "Sốt rét kháng thuốc" (tr. 33) và "Cúm mùa" (tr. 49). Nhiều khả năng các chương này đã bị 3377/2023 và 1840/2025 thay. Manifest nên ghi `partial`. Chương sốt mò, uốn ván, nhiễm khuẩn huyết chưa thấy văn bản thay thế trên kcb.vn, nhưng **chưa khẳng định được**.
6. **Lỗi chính tả trong văn bản gốc**: 5642/2015 tr. 84 ghi "Imipenem+cisplatin" (đúng phải là imipenem+cilastatin). Span giữ nguyên văn. Nếu câu hỏi dùng span này làm đoạn oracle (A3) thì cần lưu ý.
7. **Kết quả trái kỳ vọng**: uốn ván (HTIG 3000–6000 đơn vị so với 500 đơn vị của WHO và CDC) là **xung đột mới**, không có trong bộ hạt giống. Chủ đề uốn ván vốn chỉ được coi là phạm vi bổ sung.

---

## 5. Việc cần người kiểm ở HG1.2

1. **Hiệu lực COPD**: tìm PDF QĐ 2131/QĐ-BYT ngày 14/07/2026. Nếu có, kiểm lại P-01…P-04 trên bản 2026 (FEV1/FVC, PaO2 ≤ 55, corticoid 5–7 ngày, bạch cầu ái toan ≥ 300).
2. **Đột quỵ**:
   - Xác nhận số hiệu và năm của hướng dẫn đột quỵ hiện hành (3312/2024?).
   - Lấy PDF từ Cục KCB hoặc bệnh viện đăng lại nguyên quyết định. dotquy.kcb.vn đang lỗi chứng chỉ.
   - Có PDF rồi mới làm được mẩu 4,5 giờ và liều alteplase.
3. **Béo phì 2892/2022**: xin bản PDF chính thức (liên kết daithaoduong.kcb.vn hỏng) để kiểm thang 23–24,9 / 25–29,9.
4. **Whitmore 6101/2019**: văn bản này có tồn tại không, và có còn hiệu lực không? Nếu có, hợp tập giá trị cho P-06 và xem lại ứng viên meropenem.
5. **Hai trang CDC đọc bằng WebFetch** (không có sha256). Mở trình duyệt và xác nhận:
   - (a) sốt mò: "100 mg twice per day" cho người lớn > 45 kg, last reviewed 15/05/2024;
   - (b) uốn ván: "a single, 500 international unit (IU) dose of TIG", last reviewed 08/09/2026.
6. **WPRO 2000** (PDF quét): xác nhận Table 2.2 ở PDF trang 19 (số trang in 18): "Overweight ≥ 23".
7. **P-05 (diễn giải liều)**: "0,1 g x 2 viên uống chia 2 lần/ngày" có đúng là 100 mg/lần (200 mg/ngày) không?
8. **5642/2015**: chương sốt mò, uốn ván, nhiễm khuẩn huyết còn hiệu lực không?
9. **P-09**:
   - Có chấp nhận dùng 5481/2020 thay 2892/2022 cho dòng 13 không?
   - Kiểm trùng với chủ đề dm khi gộp (dm dùng 5481/2020 tr. 11–12 cho các slot khác).
10. **P-08** là xung đột cần bác sĩ thật xem (HG3.9: `moh_lags_evidence`, `clinical_harm`). Agent không gán các trường này.
11. **Hạn mức WebSearch** của phiên đã hết (200/200). Muốn tìm tiếp văn bản (đột quỵ, 2131/2026, 6101/2019) thì người dùng phải tăng `CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION`, hoặc tự tìm và đưa URL.

---

## 6. Đề xuất sửa configs / mã (không tự sửa)

1. **`normalize_vi.UNIT_ALIASES`**: thêm đơn vị quốc tế:
   - `"iu"`, `"ui"`, `"đơn vị"`, `"units"`, `"international units"` → `"IU"`.
   - Hiện "500 IU" chỉ đúng nhờ quy tắc "thiếu đơn vị thì mặc định đơn vị của mẩu".
   - Thêm `"mg/ngày"`, `"mg/day"` → `"mg/day"`.
2. **Tỉ số ↔ %** (P-01): câu trả lời "FEV1/FVC < 0,70" hiện bị chấm nhãn 5. Có hai cách:
   - Đề xuất context `{"ratio_percent": true}`: khi đơn vị mẩu là % thì giá trị không có đơn vị và ≤ 1 được nhân 100 (cần test);
   - hoặc câu hỏi phải yêu cầu trả lời theo %.
3. **kPa ↔ mmHg** (P-02): thêm cạnh `("kPa","mmHg"): 7.50062`, nhưng chỉ bật khi context đánh dấu khí máu. Không bật chung, vì kPa trong FibroScan (viêm gan B) không phải áp suất.
4. **Tần suất dùng thuốc** (P-05): "× 2 lần/ngày", "2 lần/ngày", "twice daily", "q12h", "mỗi 8 giờ" không được sinh ra số liều. Hiện "2 lần" thành 2 mg, câu trả lời bị tính là nhiều giá trị và chấm nhãn 5. Đề xuất coi "lần", "times", "x/ngày" là đơn vị tần suất rồi bỏ qua (skill vn-number-normalization, kèm test).
5. **`verify_span.norm()`**: PDF của 5642/2015 dùng ký tự vùng riêng U+F02D (và các ký tự tương tự U+F0xx) làm dấu gạch đầu dòng. Span do người gõ lại sẽ không khớp. Đề xuất ánh xạ U+F000–U+F0FF thành khoảng trắng ở cả hai phía, kèm test. Mẩu P-05 hiện lưu ký tự này dưới dạng ``.
6. **`vnsoc.match.sources`**:
   - `fetch/grep` bị crash (AssertionError của html.parser) với tệp .pptx đã cache: bộ slide ADA 2026 bị đọc như HTML. Đề xuất nhận diện zip/pptx/docx và rút chữ từ XML.
   - cdc.gov trả 403 với requests/curl. Cần quy trình chụp trang thủ công có băm, hoặc để người dùng duyệt.
7. **`configs/grading.yaml` — drugs** (cho các mẩu kiểu drugs sau này; lô này chưa cần vì toàn mẩu num):
   - doxycycline [doxycyclin]; azithromycin []; chloramphenicol [cloramphenicol];
   - ceftazidime [ceftazidim]; meropenem []; imipenem-cilastatin [imipenem+cilastatin, imipenem/cilastatin];
   - co-trimoxazole [cotrimoxazol, trimethoprim-sulfamethoxazole, tmp-smx];
   - metronidazole [metronidazol]; penicillin-g [penicillin g, benzylpenicillin];
   - alteplase [rt-pa, actilyse]; tenecteplase [].

---

## 7. Sau kiểm toán (26/9/2026, agent sửa lỗi)

Kiểm toán: `data/interim/pilot/controls_verify.md` (pass 1 · fix 8 · reject 0). Tôi tự chạy lại công cụ cho từng điểm, không dựa vào lời kiểm toán.

**Kết quả sau sửa:**
- 9 mẩu, **0 bị loại**: 7 concordant + 2 conflict (P-08, P-09); 0 lệch phiên bản.
- `finalize()` chạy lại cho cả 9 mẩu: tolerance, conflict_status và mồi **không đổi**.
  - P-08: mồi 8500 IU (`mirror_arith`), dung sai 1250.
  - P-09: mồi 21 kg/m² (`mirror_arith`), dung sai 1,0.
  - `choose_decoy` chọn lại đúng mồi cũ; `check_decoy` = [] cho cả 9.
- `python -m vnsoc.schemas atom data/interim/pilot/controls.jsonl` → **OK 9/9**.
- `python -m vnsoc.extract.verify_span data/interim/pilot/controls.jsonl` → **OK 9/9**, gồm cả span DR8 mới của P-06 (2147/2026 tr.53) và P-09 (3087/2020 tr.7).
- Các span phụ (`same_doc_locations`, `supporting_spans`) cũng được kiểm `span_on_page` = True.
- Mỗi mẩu có `extraction.audit_fix` {date, audit, verdict, changes}.
- Không gán `moh_lags_evidence` / `clinical_harm` / `clinician_confirmed`.

### 7.1 Bằng chứng đã tự kiểm lại

| Điểm | Cách kiểm | Kết quả |
| --- | --- | --- |
| Danh tính "3874/2018" | `--page 4562/2018 4`; sha256sum | "Số: 4562/QĐ-BYT … ngày 19 tháng 7 năm 2018". Điều 3 thay 3874/2018 và 2866/2015. `3874_2018.pdf` và `4562_2018.pdf` cùng sha `68a2f132db3ba1c2` → **kiểm toán đúng** |
| Giá trị trong 4562/2018 | `--find` | "FEV1/FVC < 70%" → tr.16, 17, 18. "55 mmHg" → tr.28. "5-7 ngày" → tr.36, 38, 39. "1mg/kg/ngày" → tr.36, 37. Không có ngưỡng số bạch cầu ái toan cho bước thêm ICS (tr.27–28 chỉ ghi "tăng bạch cầu ái toan") |
| Manifest | `data/interim/manifest_parts/*.jsonl` | 4562/2018 đang tạm để **current** (2767/2023 Điều 3 chỉ nêu thay 3874/2018). Giá trị P-01…P-03 giống 2767/2023 nên DR8 không đổi tập |
| 2147/2026 (viêm phổi cộng đồng người lớn) | sha256sum; `--page 1`, `--page 53` | sha `ea53195a2faf8b66`. Tr.1: Điều 3 thay 4815/2020. Tr.53 (tr. in 43), mục 5.4.1.6 Melioidosis: ceftazidim 2 g mỗi 6 giờ hoặc meropenem 1–2 g mỗi 8 giờ; tấn công 2 tuần, duy trì 3 tháng |
| 6101/2019 (Whitmore) | sha256sum; `--page`; sidecar OCR; ảnh PDF tr.4 (render vào scratchpad) | sha `a3baf8fa8f119d73`. Sidecar tesseract (vie+eng, 300 dpi) **đã có** và đọc đúng tr.4–5. Nhưng PDF có sẵn **lớp chữ OCR cũ không dấu** (ví dụ "Meropenem: 19" thay cho "1g"). Meta `override_text_layer=false` nên `verify_span` dùng lớp cũ; tôi đã thử và span đọc được **không qua**. Ảnh tr.4: ceftazidim 2 g mỗi 6–8 giờ, tối đa 8 g/ngày; meropenem 1 g mỗi 8 giờ; ICU nên dùng carbapenem |
| Văn bản dùng BMI (P-09) | `--page` | 3087/2020 tr.7 "(BMI ≥ 23 kg/m2)"; tr.12 thang điểm "Thừa cân: BMI 23-25". 2919/2014 tr.60 bảng "Thừa cân 23 – 24,9". 5968/2021 tr.100 "Thừa cân: nếu BMI từ 25 - 30". 1768/2026 tr.28 bảng WHO "Thừa cân 25 ≤ BMI < 30"; tr.85 E66 "Người lớn (Châu Á): BMI ≥ 25 … (WHO): BMI ≥ 30". 5481/2020 tr.55 và 6173/2018 tr.19 là bảng tăng cân thai kỳ (thừa cân 25–29,9). **Kiểm toán đúng** |
| GOLD 2026 v1.3 | `sources grep` (sha `fa12e8e2dbd2090e`) | < 0.7: p.15, 18, 32, 40. 55 mmHg (7.3 kPa): p.87. "for 5 days": p.114. "up to 5 days": p.103. ≥ 300: p.75, 76, 77, 132, 161. "LABA+ICS … not encouraged": p.75. ≥ 100: p.77, 80 |
| Darwin 2024 | `sources grep` (sha `54cfa18f35dd96bf`) | p.4: ceftazidime (khoa thường) 2 g mỗi 6 giờ; meropenem (ICU) 1 g mỗi 8 giờ. p.11: version 11.0, approved 10/2/24, review date 10/2/26 |
| WHO | `sources grep` | Fact sheet béo phì: overweight ≥ 25 (sha `dc1d9d01…`). Technical note uốn ván: "human TIG 500 units" p.5 (sha `637bb6b9…`) |
| WPRO 2000 | render lại PDF p.19 từ bản cache (sha `b11886340b039690`, 56 tr.) | Table 2.2: Overweight ≥ 23; At risk 23–24.9; Obese I 25–29.9; Obese II ≥ 30. Văn bản gọi là "provisional" và nói không áp cho người đảo Thái Bình Dương |
| CDC (2 trang) | `sources fetch` → vẫn **403**; đọc lại bằng WebFetch (lần thứ ba) | Sốt mò: "100 mg twice per day" (người lớn > 45 kg); trẻ < 45 kg 2.2 mg/kg; last reviewed 15/5/2024. Uốn ván: một liều 500 IU tiêm bắp; "appears as effective as higher doses (3,000 to 6,000 IU)"; last reviewed 8/9/2026 |
| Chấm lại bằng `grade_short` | chạy 26/9/2026 | P-01 "FEV1/FVC < 0.7" → **5**; "< 70%" → 2. P-02 "7.3 kPa" → **6 (abstain)**, tệ hơn báo cáo gốc. P-03 "5 ngày"/"7 ngày" → 2; "14 ngày" → 5. P-04 "100 tế bào/µL" → 5. P-05 "100 mg x 2 lần/ngày" → **2** (đã sửa ở mã). P-08 "500 IU" → 4 [US, WHO_global]; "3000 đơn vị" → 2; "8500 IU" → 5 + cờ mồi; "2000 IU" → 2. P-09 "BMI ≥ 25" → 4 [WHO_global]; "23 kg/m2" → 2; "21" → 5 + cờ mồi |

### 7.2 Đã sửa

| Mẩu | Kiểm toán | Đã sửa | Trạng thái |
| --- | --- | --- | --- |
| P-controls-01 | fix | Notes: "bản cũ 3874/2018" → 4562/2018 (tệp 3874_2018.pdf, sha 68a2f132…), kèm tình trạng manifest. Thêm `grading_caveat`: câu hỏi phải yêu cầu trả lời theo % cho tới khi có mã quy đổi tỉ số↔% | concordant |
| P-controls-02 | fix | Notes: bản cũ → 4562/2018 (tr.28). Thêm `grading_caveat`: "7,3 kPa" hiện bị chấm nhãn 6, nên câu hỏi phải yêu cầu mmHg | concordant |
| P-controls-03 | fix | Notes: bản cũ → 4562/2018 (tr.36, 38). Ứng viên lệch phiên bản về liều vẫn giữ, nhưng phụ thuộc HG2.3. Locator GOLD thêm p.103 | concordant |
| P-controls-04 | fix | Intervention nói rõ ngưỡng "cao/đáp ứng tốt", không phải ngưỡng ≥ 100. `population.stage` ghi bối cảnh nâng bậc (tr.22–23). Locator GOLD ghi p.132, 161, 75 và ngưỡng 100 ở p.77/80. Thêm `same_doc_locations` 2767/2023 tr.21 (khởi trị nhóm D, cùng ≥ 300). Notes ghi ứng viên xung đột LABA+ICS và sửa nhãn 4562/2018 | concordant |
| P-controls-05 | fix | CDC `verified_by` "auto" → **null**. Locator ghi needs_human_check (403, WebFetch 3 lần). `population.age` → "người lớn" (bỏ "≥ 10 tuổi"), giữ "> 45 kg" | concordant |
| P-controls-06 | fix | `dr8_sources` = 2147/2026 tr.53 (đã qua verify_span). Thêm `dr8_pending_ocr` = 6101/2019 tr.4 (lý do chưa vào dr8_sources + kiểm ảnh bằng AI). Bỏ nhận định "khoảng cách liều / meropenem là xung đột". `population.setting` → khoa thường (không ICU), không tổn thương TKTW. `condition` ghi rõ nhiễm khuẩn huyết (± viêm phổi). Locator Darwin ghi version 11.0 và review date đã quá hạn | concordant |
| P-controls-07 | **pass** | Không đổi, chỉ thêm `audit_fix` | concordant |
| P-controls-08 | fix | CDC `verified_by` → **null**, locator needs_human_check. Locator WHO ghi phạm vi "nhân đạo khẩn cấp". Notes diễn giải (không chép nguyên văn) nhận xét của CDC: 500 IU có vẻ hiệu quả tương đương 3000–6000 IU → chuyển HG3.9. Bỏ câu lỗi thời "IU chưa có trong UNIT_ALIASES". Ghi hệ quả dung sai 1250 cho phân tích độ nhạy | conflict (8500 IU; tol 1250) |
| P-controls-09 | fix (nặng) | WPRO `verified_by` → **null**, locator needs_human_check. `population` thêm `exclusions` (không mang thai; không thuộc nhóm HIV 5968/2021 tr.100 hay ung thư 1768/2026 tr.28). `dr8_sources` = 3087/2020 tr.7 (cùng 23). `supporting_spans` = 3087/2020 tr.12, 2919/2014 tr.60. `dr8_not_applied` liệt kê văn bản dùng 25. Notes ghi đặt lại slot so với hạt giống 13, và phía US / tham vấn WHO 2004 chưa kiểm | conflict (21 kg/m²; tol 1,0) |

### 7.3 Giữ nguyên hoặc không làm đúng như kiểm toán đề xuất, và vì sao

1. **P-01: không đặt `context.ratio_percent`.** Mã chấm chưa hỗ trợ, và chính kiểm toán ghi phương án (a) chỉ làm "sau khi có mã và test". Tôi chọn phương án (b): ràng buộc câu hỏi, ghi trong `grading_caveat`.
2. **P-03: không thêm `cmp: "<="` cho GOLD.**
   - GOLD p.114 là khuyến cáo cụ thể "40 mg … for 5 days"; p.103 chỉ là câu tóm tắt "up to 5 days".
   - Nếu ghi ≤ 5 thì câu trả lời "3 ngày" sẽ bị gán nhãn 4 (nước ngoài), dù GOLD không khuyến cáo 3 ngày.
   - Trạng thái concordant không đổi theo cách nào. p.103 đã được thêm vào locator.
3. **P-06: 6101/2019 chưa vào `dr8_sources`.**
   - `verify_span` đọc lớp chữ cũ không dấu, nên span đọc được không qua kiểm. Tôi đã thử.
   - Không được phép sửa `data/interim/ocr/*` (ngoài hai file được ghi).
   - Giá trị được ghi ở `dr8_pending_ocr`. Liều/lần giống nhau (2 g), nên tập VN và trạng thái không đổi.
   - Nguồn chính vẫn là 5642/2015 (có lớp chữ).
4. **P-09: không loại (reject).** Tôi áp loại trừ quần thể đúng như kiểm toán đề xuất. Nếu HG1.2 không chấp nhận loại trừ thì reject.
   - **Giữ `seed_row: 13`**, vì tập VN của dòng 13 có "thừa cân 23–24,9". Ngưỡng thừa cân 23 là một phần của dòng này.
   - Notes và §4 được sửa để nói rõ: mẩu so **thừa cân 23 vs 25**, không phải béo phì 25 vs 30 như hạt giống.
5. **P-09: WHO_global giữ `verified_by: "auto"`**, vì có sha256 và grep lại được.
6. **Không tạo mẩu mới trong vòng sửa này** (đột quỵ, thời gian điều trị Whitmore, meropenem, xung đột LABA+ICS). Mẩu mới sẽ vào bộ thí điểm mà chưa qua kiểm toán độc lập, trái quy trình. Danh sách ứng viên ở §7.5 mục 11.
7. `data/raw/3874_2018.pdf` bị đặt nhầm khóa. Thư mục này chỉ đọc với tôi nên tôi không đổi tên hay xóa.

### 7.4 Đính chính các mục 1–6

- **§Tóm tắt, §1a, §4.2:** 6101/2019 có tồn tại.
  - Corpus-librarian tải lúc 11:30, sau báo cáo gốc (11:28).
  - Nguồn: BVĐK Hà Trung đăng lại bản ký số VOffice, ngày ký 07/01/2020.
- **Báo cáo gốc bỏ sót** hai văn bản đã có sẵn trong `data/raw` trước khi viết:
  - 2147/2026 (11:06), có phác đồ melioidosis;
  - 5331/2020 (đột quỵ não, 11:17), tr.26 ghi rt-PA "khởi phát < 4.5 giờ". Hiệu lực so với "3312/2024" chưa rõ.
  - Bài học quy trình: quét `data/raw` và manifest trước khi kết luận "không tìm thấy".
- **§1a, §3 mục 8, notes P-01…P-04:** mọi chỗ "3874/2018" là **4562/2018**.
- **§3 mục 2:** nay có giá trị VN về thời gian điều trị Whitmore:
  - 2147/2026 tr.53: tấn công 2 tuần, duy trì 3 tháng;
  - 6101/2019 tr.4–5: ≥ 2 tuần; 3–6 tháng.
- **§3 mục 3–4, §4.2:** meropenem và khoảng cách liều Whitmore **không phải xung đột** theo DR8.
- **§4.1 (dòng 13):**
  - mẩu so ngưỡng thừa cân, không phải ngưỡng béo phì;
  - có các văn bản Bộ Y tế dùng thang WHO chung cho quần thể riêng (HIV, ung thư, thai kỳ);
  - 1768/2026 tr.85 ghi đồng thời "châu Á ≥ 25" và "WHO ≥ 30" cho béo phì.
- **§2 và §6 (lỗi chấm):**
  - Đề xuất 1 (bí danh IU) và 4 (tần suất "lần/ngày") **đã có trong mã**.
  - Đề xuất 2 (tỉ số↔%), 3 (kPa) và 5 (U+F02D) **vẫn cần**.
  - "7.3 kPa" hiện bị chấm **nhãn 6 (abstain)**, nặng hơn mô tả "không parse được" trong báo cáo gốc.

### 7.5 Tồn đọng cho HG1.2 (kèm HG2.3 / HG3.9)

1. **Hiệu lực COPD (P-01…P-04):**
   - Chưa tìm thấy 2131/2026. Nếu có, phải trích lại.
   - HG2.3 cần quyết định 4562/2018 còn hiệu lực hay đã bị 2767/2023 thay. Giá trị của 4 mẩu không đổi theo cách nào, nhưng ứng viên lệch phiên bản về liều corticoid phụ thuộc quyết định này.
2. **`data/raw/3874_2018.pdf` đặt nhầm khóa:** cần T2.x hoặc người dùng đổi tên/xóa, hoặc ghi `pdf_choice.json`.
3. **6101/2019:**
   - Chạy `python -m vnsoc.extract.ocr --key 6101/2019 --override-text-layer`. Lớp chữ nhúng là OCR cũ không dấu, đúng trường hợp cờ này được thiết kế cho.
   - Sau đó chuyển `dr8_pending_ocr` của P-06 sang `dr8_sources` và chạy lại `verify_span`.
   - **Người thật** so ảnh tr.4–5 (quy tắc §3.1 về OCR).
4. **P-09:**
   - (a) Có chấp nhận loại trừ quần thể (thai kỳ, HIV, ung thư) không? Nếu không thì reject.
   - (b) Có làm mẩu "béo phì 25 vs 30" đúng như hạt giống không? Hiện thiếu 2892/2022 và có rủi ro DR8 do 1768/2026 tr.85.
   - (c) Kiểm phía US: ADA 2026 mục 2 (tiêu chí tầm soát theo BMI, ngưỡng riêng cho người Mỹ gốc Á).
   - (d) Kiểm tham vấn chuyên gia WHO 2004 về BMI ở người châu Á.
   - Mục (c) và (d) cần hạn mức WebSearch hoặc URL do người dùng đưa; tôi không ghi từ trí nhớ.
5. **Xác nhận bằng trình duyệt** (không có sha256):
   - CDC sốt mò (15/5/2024);
   - CDC uốn ván (8/9/2026);
   - ảnh WPRO p.19.
6. **P-05:** "0,1 g x 2 viên uống chia 2 lần/ngày" có đúng là 100 mg/lần không?
7. **5642/2015:** chương sốt mò, uốn ván, nhiễm khuẩn huyết còn hiệu lực không? Ảnh hưởng P-05…P-08.
8. **P-08 (HG3.9, bác sĩ thật):** CDC coi 500 IU hiệu quả tương đương 3000–6000 IU. Cần đánh giá `moh_lags_evidence` và `clinical_harm`.
9. **Darwin:** review date 10/2/26 đã qua. Cần kiểm bản mới (P-06).
10. **Mã chấm** (đề xuất, kèm test; tôi không sửa):
    - quy đổi tỉ số↔% khi đơn vị mẩu là % (P-01);
    - kPa↔mmHg khi context là khí máu (P-02). Ít nhất nên gắn `needs_llm` thay vì nhãn 6 khi có số kèm đơn vị không quy đổi được;
    - `verify_span.norm` ánh xạ U+F000–U+F0FF;
    - nêu dung sai P-08 trong phân tích độ nhạy.
11. **Ứng viên mẩu cho vòng sau** (mỗi mẩu cần kiểm toán):
    - Whitmore, thời gian tấn công 2 tuần / duy trì 3 tháng: 2147/2026 tr.53, 6101/2019 tr.4–5 ↔ Darwin p.4–5 → **concordant**.
    - Whitmore, liều meropenem ở ICU: hợp tập VN 0,5 / 1 / 1–2 g ↔ Darwin 1 g → **concordant**.
    - COPD, phác đồ có ICS: VN ICS/LABA (2767/2023 tr.21, 23) ↔ GOLD 2026 p.75 (không khuyến khích LABA+ICS) → **xung đột kiểu drugs**.
    - Đột quỵ, cửa sổ rt-PA < 4,5 giờ: 5331/2020 tr.26, nếu HG2.3 xác nhận 5331/2020 là bản hiện hành. Liều alteplase không có trong lớp chữ, phải xem ảnh.
12. **Hạn mức WebSearch** của phiên vẫn hết (200/200). Mục 4(c–d) và 9 cần người dùng tăng hạn mức hoặc đưa URL.

### 7.6 Đề xuất mã / quy trình bổ sung (không tự sửa)

- **`vnsoc.extract.verify_span` / `ocr`:** khi lớp chữ nhúng gần như không có dấu tiếng Việt (tỉ lệ ký tự có dấu rất thấp) và sidecar tốt hơn rõ rệt, nên cảnh báo hoặc tự ưu tiên sidecar. Trường hợp 6101/2019 cho thấy quy tắc hiện tại (< 200 ký tự) bỏ sót lớp OCR rác dài. Cần test.
- **Skill atomization-protocol / counterpart-matching:** thêm bước bắt buộc quét toàn văn `data/raw/*.pdf` (tên bệnh, tác nhân) và đọc `manifest_parts` trước khi viết "không tìm thấy".
- **`vnsoc.grade`:** câu trả lời có số kèm đơn vị hợp lệ nhưng không quy đổi được (ví dụ kPa khi mẩu dùng mmHg) không nên thành nhãn 6 (abstain). Nên đặt `needs_llm=True` hoặc nhãn "chưa chấm".
