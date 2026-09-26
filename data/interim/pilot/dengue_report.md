# Báo cáo T1.1 (thí điểm tuần 0) — chủ đề Sốt xuất huyết Dengue (ID `dengue`)

Người làm: agent atom-extractor + counterpart-matcher (Claude), ngày 2026-09-26.
> **Cập nhật sau kiểm toán (2026-09-26):** tệp hiện còn **9 mẩu** (P-dengue-07 bị loại); 7 mẩu đã sửa theo `dengue_verify.md`. Trạng thái hiện hành và lý do xem **mục (7)**. Các mục (1)–(6) giữ nguyên bản gốc, chỉ thêm ghi chú "[sau kiểm toán]" ở chỗ đã lỗi thời.

Tệp dữ liệu: `data/interim/pilot/dengue.jsonl` (bản gốc: 10 mẩu). Cả 10 mẩu qua `python -m vnsoc.schemas atom` (OK 10 dòng) và `python -m vnsoc.extract.verify_span` (0 mẩu lỗi), nên `span_verified: true`. `tolerance` và `conflict_status` do `vnsoc.match.decoys.finalize` tính; `check_decoy == []` với mọi mẩu. Mọi mẩu có `context_checked: "pending"`. Các trường chỉ bác sĩ được điền (moh_lags_evidence, clinical_harm, clinician_confirmed) để trống.

## Tóm tắt kết quả

| Loại (theo thiết kế) | Mẩu | Chỉ tiêu |
|---|---|---|
| Xung đột | P-dengue-01, 02, 03, 04 | 2–3 → **vượt 1** (xem thứ tự ưu tiên ở mục 3) |
| Lệch phiên bản 3705/2019 → 2760/2023 | P-dengue-05, 06, ~~07~~ [sau kiểm toán: 07 bị loại] | 2–4 |
| Đối chứng (trùng quốc tế) | P-dengue-08, 09, 10 | 2–3 |

Đếm theo `conflict_status` do máy tính: conflict 4 (01–04) · concordant 4 (05, 08, 09, 10) · no_counterpart 1 (06) · indistinguishable 1 (07).

**Phát hiện chính (cần báo người dùng):**
1. **Dòng hạt giống 1 ĐÚNG về giá trị Việt Nam, nhưng KHÔNG phải mẩu lệch phiên bản.** Bản 3705/2019 có cùng giá trị: 15 ml/kg/giờ, rồi 10 ml/kg/giờ × 2 giờ.
2. **WHO 2025 (hướng dẫn arbovirus, IRIS 3/7/2025) không có tốc độ dịch ml/kg/giờ nào.** Văn bản này chỉ có khuyến cáo định tính: ưu tiên dịch tinh thể hơn dịch keo, dùng thời gian đổ đầy mao mạch (CRT), lactate và nghiệm pháp nâng chân thụ động (PLR). Nó dẫn chiếu về các hướng dẫn WHO trước để lấy chi tiết. Vì vậy con số nước ngoài cho mẩu 01/02 vẫn phải lấy từ WHO 2009 và sổ tay WHO 2012.
3. **WHO 2025 xung đột trực tiếp với Bộ Y tế ở hai điểm định tính** (đã thành mẩu):
   - Bộ Y tế **cấm analgin (metamizol)**, còn WHO 2025 **gợi ý dùng metamizol** để hạ sốt/giảm đau (P-dengue-04).
   - Bộ Y tế cho **dịch keo (cao phân tử) làm liều chống sốc đầu tiên** ở người lớn có dấu hiệu cảnh báo chuyển sang sốc, còn WHO 2025, WHO 2009/2012 và CDC đều dùng **dịch tinh thể** (P-dengue-03).
4. **Bản 3705/2019 chính thức duy nhất tìm được là bản QUÉT** (lớp OCR không dấu), **có watermark LuatVietnam**, do một bệnh viện đăng lại. Giá trị bản cũ đọc bằng mắt từ ảnh trang, **chưa kiểm được bằng máy**. Cần người kiểm ở HG1.2.

## (1) Văn bản đã tải

### Văn bản Bộ Y tế (qua `vnsoc.extract.fetch_pdf`)

| Khóa | URL | sha256 (16) | Số trang | text_kind | Trạng thái | Nơi tìm và xác nhận danh tính |
|---|---|---|---|---|---|---|
| 2760/2023 | https://file.medinet.gov.vn/%2fdata%2fsoytehcm%5ctrungtamytebinhtan%5cattachments%2f2023_7%2f2760anngay24-5-2023trinhbanhanhdanhsotrangsigned_187202317.pdf | 5936c4e425a17db8 | 104 | ok | downloaded | Trang đăng: TTYT quận Bình Tân, trên nền medinet.gov.vn của Sở Y tế TP.HCM ([trang tin](https://trungtamytebinhtan.medinet.gov.vn/thong-bao/ban-hanh-huong-dan-chan-doan-dieu-tri-sot-xuat-huyet-dengue-vbct14533-107239.aspx), ghi số 2760/QĐ-BYT, ngày 4/7/2023, người ký Trần Văn Thuấn). Lớp chữ để trống số hiệu ("Số: /QĐ-BYT"). Danh tính xác nhận qua: chữ ký số "Ký bởi: Bộ Y tế … Ngày ký: 04-07-2023"; dấu văn thư SYT TP.HCM "2760 04 7"; Điều 1 ghi thay thế QĐ 3705/QĐ-BYT ngày 22/8/2019. |
| 3705/2019 | https://file.medinet.gov.vn//data/soytehcm%5Cbvquanphunhuan%5Cattachments/2022_11/quyet-dinh-3705-qd-byt-2019-huong-dan-chan-doan-dieu-tri-sot-xuat-huyet-dengue3_1611202215.pdf | fcd393c4ef07ad8c | 75 | **scanned_or_empty** | downloaded | Trang đăng: BV quận Phú Nhuận (medinet.gov.vn). Ảnh trang 1 cho thấy: "Số: 3705/QĐ-BYT", Hà Nội ngày 22/8/2019, KT. Bộ trưởng – Thứ trưởng Nguyễn Viết Tiến, có dấu; Điều 2 bãi bỏ QĐ 458/QĐ-BYT ngày 16/02/2011. **Mọi trang có watermark "LuatVietnam"**, tức bệnh viện đăng lại bản lấy từ một thư viện pháp luật tư nhân (không phải tên miền bị cấm). Lớp OCR không dấu, số bị đọc sai (ví dụ "ISmg"). |

Những nơi đã thử mà không lấy được:
- **kcb.vn:** trang /phac-do không có mục dengue; các URL tìm kiếm và tin cũ trả về 404.
- **Trang Sở Y tế:** Bình Định (lỗi SSL), Bắc Giang (lỗi DNS), Tuyên Quang (chứng chỉ hết hạn, trang chỉ trả JS), Thừa Thiên Huế (lỗi DNS).
- **TTYT Hóc Môn (medinet):** 404 cho cả 2760 và 3705.
- **BV Nhựt Thành:** chứng chỉ hết hạn.
- **Ngoài ra:** kết quả tìm kiếm cho 3705/2019 chỉ trỏ tới trang thư viện pháp luật tư nhân. Không truy cập các trang đó. Không tìm được bản 3705 có lớp chữ tốt trên nguồn chính thức.
- **Giới hạn công cụ:** hạn mức WebSearch của phiên đã hết (200/200) giữa chừng, nên không tìm thêm được.

### Nguồn nước ngoài (qua `vnsoc.match.sources`; mọi chuỗi giá trị đã kiểm bằng `grep`, có số trang PDF)

| Nguồn | Hệ thống | URL đã tải | sha256 (16) | Trang |
|---|---|---|---|---|
| WHO 2009 Dengue guidelines (ISBN 9789241547871) | WHO_global | IRIS REST bitstream b1db05d8-…/content | f6f48811df824c02 | 160 |
| WHO 2012 Handbook for clinical management of dengue | WHO_global | IRIS REST bitstream 825eb07b-…/content | b0ca16915451b163 | 124 |
| WHO 2025 guidelines for clinical management of arboviral diseases (ISBN 9789240111110; IRIS dc.date.issued 2025-07-03) | WHO_global | IRIS REST bitstream 634a55a5-…/content | cbbe4513ef91cc6b | 125 |
| CDC Dengue Clinical Management Pocket Guide (5/2024) | US | cdc.gov/dengue/media/pdfs/2024/05/…PocketGuideDCMC_UPDATE.pdf | 20dad79a31da86cc | 8 |

Ghi chú nguồn:
- **NCBI Bookshelf** (NBK616301) trả về trang reCAPTCHA. Không dùng được, nên đã tải PDF chính thức từ WHO IRIS.
- **Bộ nhớ đệm bị ghi rác:** `sources.fetch` đã lưu trang reCAPTCHA vào cache (`data/cache/foreign/81a34ccd….html`), và lưu trang HTML rỗng của IRIS cho URL `/bitstream/handle/10665/381804/9789240111110-eng.pdf` (`a859cc83….html`). Hai mục cache này là rác, **không được dùng làm bằng chứng** (xem đề xuất ở mục 6).
- **CDC:** các trang HTML của cdc.gov trả 403 với requests/curl. WebFetch chỉ được dùng để tìm link PDF pocket guide; không lưu giá trị nào lấy từ trang HTML.

## (2) Bảng mẩu

Ghi chú chung: "PDF p." là số trang PDF (1-based) của 2760/2023. Ô "Bản cũ 3705" ghi giá trị đọc bằng mắt từ ảnh trang quét.

| id | slot / quần thể | Việt Nam (2760/2023) | Nước ngoài (hệ thống: giá trị, phiên bản) | Bản cũ 3705/2019 | Trạng thái | PDF p. (in) |
|---|---|---|---|---|---|---|
| P-dengue-01 (hạt giống 1) | dose — người lớn ≥ 16 tuổi, sốc còn bù, **giờ đầu** | 15 ml/kg/giờ | WHO 2009: 5–10 ml/kg/giờ; WHO 2012 (người lớn): 5–10; US CDC 2024: 20 mL/kg trong 15–30 phút (≈ 40–80 ml/kg/giờ, **quy đổi**) [sau kiểm toán: mục CDC đã bỏ] | 15 (không đổi) | conflict; mồi 20–25 | 28 (27) |
| P-dengue-02 (tách hạt giống 1) | dose — người lớn, sốc còn bù đã cải thiện, **bước 2** | 10 ml/kg/giờ × 2 giờ | WHO 2009: 5–7; WHO 2012: 5–7; US CDC: 10 (nguồn in nhầm "mg/kg") | 10 (không đổi) | conflict; mồi 13–15 | 28 (27) |
| P-dengue-03 | first_line (cat) — người lớn có dấu hiệu cảnh báo đang truyền dịch, chuyển sang sốc **còn bù**: loại dịch cho liều chống sốc đầu | cao phân tử (colloid) 10–15 ml/kg/giờ | WHO 2025, WHO 2009, WHO 2012, CDC 2024: dịch tinh thể | colloid (không đổi) | conflict; mồi albumin | 15 (14) |
| P-dengue-04 | first_line (cat, Có/Không) — có được dùng analgin (metamizol) để hạ sốt? | Không (chỉ paracetamol đơn chất) | WHO 2025: có (gợi ý metamizol, khuyến cáo có điều kiện) | Không (không đổi) | conflict; mồi "chỉ khi paracetamol thất bại" | 12 (11) |
| P-dengue-05 | duration — người lớn **sốc nặng** (M = 0, HA = 0): thời gian truyền 15 ml/kg dịch tinh thể đầu | 15 phút | WHO 2009: 15 phút; WHO 2012: 15–30; CDC: 15–30 (**thể tích nước ngoài là 20 ml/kg**) | 60 phút (3705 gộp sốc và sốc nặng: 15 ml/kg/giờ trong giờ đầu) — **suy ra** | concordant (lệch phiên bản) | 30 (29) |
| P-dengue-06 | first_line (cat, Có/Không) — trẻ em sốc, Hct cao, không có Dextran/HES 200: dùng Gelatin thay thế? | Có (Gelatin hoặc HES 130, theo dõi sát) | — | Không ("không dùng Gelatin do hiệu quả kém") | no_counterpart (lệch phiên bản) | 16 (15) |
| P-dengue-07 | dose — trẻ thiếu niên 13–16 tuổi, sốc đã cải thiện: tốc độ duy trì cuối | 1,5 ml/kg/giờ × 12–18 giờ | WHO 2012 (trẻ em): 3; WHO 2009: 2–3; CDC: 2–4 | 3 ml/kg/giờ × 4–6 giờ (phác đồ trẻ em chung cho < 16 tuổi) | **indistinguishable** (bản cũ trùng WHO 2012) [sau kiểm toán: **BỊ LOẠI**, xem mục (3)] | 18 (17) |
| P-dengue-08 | dose — trẻ < 16 tuổi, paracetamol mỗi lần | 10–15 mg/kg | WHO 2025: 10–15 mg/kg; WHO 2012: 10 mg/kg/liều | 10–15 (không đổi) | concordant | 12 (11) |
| P-dengue-09 | classification — SXHD nặng do tổn thương gan | AST hoặc ALT ≥ 1000 U/L | WHO 2009: ≥ 1000; WHO 2012: ≥ 1000; CDC: ≥ 1000 IU | — | concordant | 38 (Phụ lục 2) |
| P-dengue-10 | threshold — trẻ em, huyết áp kẹt | hiệu áp ≤ 20 mmHg | WHO 2009 (trẻ em): ≤ 20; WHO 2012 (trẻ em): ≤ 20; CDC: < 20 | — | concordant | 9 (8) |

Họ xung đột (`conflict_family`):
- P-01 và P-02 chung họ `dengue_adult_compensated_shock_crystalloid_rate_who`, nên không độc lập.
- P-03: `dengue_colloid_vs_crystalloid_who2025`.
- P-04: `dengue_metamizole_who2025`.

Chạy thử `vnsoc.grade.grade_short` trên đáp án giả (không phải đầu ra mô hình) cho nhãn đúng như thiết kế:
- "5-10 ml/kg/hour" (P-01) → nhãn 4, WHO_global.
- "Có" (P-04) → nhãn 4, WHO_global.
- "1 giờ" (P-05) → nhãn 3, 3705/2019.
- "Không dùng gelatin" (P-06) → nhãn 3.
- "3 ml/kg/giờ" (P-07) → nhãn 3 nhưng trùng cả WHO/US, nên mới là indistinguishable.

## (3) Ứng viên bị loại và lý do

Thứ tự ưu tiên nếu cần cắt về 3 xung đột: giữ P-01 (hạt giống), P-04 và P-03 (hai mẩu dựa trên WHO 2025). P-02 có thể bỏ vì cùng họ với P-01.

| Ứng viên | Lý do loại |
|---|---|
| Trẻ em sốc có **tụt HA** (chưa phải sốc nặng): 20 ml/kg **trong 30 phút** (2760, PDF p.15). 3705 dùng 20 ml/kg/giờ. WHO 2009 dùng 15 phút. Đây vừa là lệch phiên bản vừa là xung đột. | `verify_span` thất bại. Trong chuỗi "20 ml/kg/30 phút", `NUM_RE` có lookbehind loại số đứng sau "/", nên không đọc được "30 phút". Mọi chỗ trong văn bản đều viết cùng kiểu này. Đã dựng mẩu rồi phải bỏ; xem đề xuất sửa bộ phân tích ở mục 6. |
| Thể tích bolus sốc nặng người lớn: 15 ml/kg (Việt Nam) so với 20 ml/kg (WHO 2009/2012, CDC). Là **xung đột rõ**. | `UNIT_ALIASES` không có "ml/kg", nên "15ml/kg" bị đọc thành "15 ml" và không kiểm được. |
| Trẻ em sốc nặng: 20 ml/kg trong 15 phút (trùng WHO) | Cùng lỗi đơn vị "ml/kg". |
| Ngưỡng albumin máu để truyền albumin khi sốc trẻ em: 3705 "< 2g/dL" → 2760 "< 2,5g/dL" (PDF p.20). Là **lệch phiên bản thật**. | Thiếu đơn vị "g/dL": "2,5g/dL" bị đọc thành "2,5 g". |
| Thể tích truyền máu: hồng cầu lắng 5–10 ml/kg, máu toàn phần 10–20 ml/kg (trùng WHO 2009) | Lỗi đơn vị "ml/kg". |
| Cân nặng dùng để tính dịch ở người lớn thừa cân. 2760: BMI ≥ 25 → cân nặng hiệu chỉnh (PDF p.29). WHO 2009 p.48 và WHO 2012 p.37: cân nặng lý tưởng. CDC p.6: IBW cho dịch duy trì. 3705: CN thực > 120% CN lý tưởng → hiệu chỉnh, 100–120% → CN lý tưởng. | Tạm hoãn vì đã đủ chỉ tiêu xung đột. Nguồn đã đủ. Nên dựng mẩu cat cho quần thể "CN thực > 120% CN lý tưởng": Việt Nam = hiệu chỉnh, WHO = lý tưởng, 3705 = hiệu chỉnh. |
| Truyền tiểu cầu (hạt giống dòng 2) | Theo chỉ thị: nhiều điều kiện. Ghi nhận thêm: WHO 2025 gợi ý **không** truyền tiểu cầu dự phòng khi < 50.000/µL mà không chảy máu; Việt Nam "< 5.000/mm3 (xem xét)". |
| Liều paracetamol tối đa/ngày (60 mg/kg, trùng WHO 2025) | WHO 2012 ghi "10 mg/kg/liều, không quá 3–4 lần/24 giờ", tương đương 30–40 mg/kg/ngày. Đây là giá trị suy ra, nếu ghi sẽ làm mẩu thành xung đột. Chọn mẩu liều mỗi lần (P-08) thay thế. |
| Trẻ em sốc còn bù, giờ đầu 20 ml/kg/giờ | WHO 2012 (trẻ em) 10–20 trùng, còn WHO 2009 5–10 là số chung cho mọi tuổi. Nguồn WHO đúng quần thể lại trùng Việt Nam, nên không phải xung đột sạch. |
| Tiêu chuẩn ra viện: hết sốt 2 ngày (Việt Nam) so với 48 giờ (WHO 2009 Textbox F) | Trùng nhau, nhưng `normalize_vi` không đổi được h ↔ day. |
| Dấu hiệu cảnh báo "AST/ALT ≥ 400 U/L" và "nôn ≥ 3 lần/1 giờ" | Riêng của Việt Nam, WHO 2009 không có (no_counterpart). Có thể thêm sau. **[Sau kiểm toán — SAI một nửa:** "nôn ≥ 3 lần/1 giờ hoặc ≥ 4 lần/6 giờ" (2760 PDF p.38) **trùng** CDC 2024 p.1 và WHO 2025 p.28 (đã grep) → là ứng viên **đối chứng**, không phải no_counterpart; chỉ khác WHO 2009. Chưa dựng được vì normalize_vi chưa có đơn vị "lần/giờ". "AST/ALT ≥ 400" vẫn là no_counterpart.] |
| **P-dengue-07** (sau kiểm toán) — thiếu niên 13–16 tuổi, tốc độ duy trì cuối: 1,5 ml/kg/giờ × 12–18 giờ (2760 p.18); bản cũ 3 ml/kg/giờ × 4–6 giờ (3705 p.9) | **Loại theo kiểm toán, đã tự kiểm lại:** (a) `conflict_status = indistinguishable` (bản cũ 3 trùng WHO 2012 trẻ em) → không dùng được cho kiểm định; (b) Phụ lục 11 của chính 2760 (p.50, lớp chữ) **vẫn có bước "RL hoặc NaCl 0.9% 3 ml/kg/giờ x 4-6 giờ"** trước bước 1,5 → câu trả lời "3" có thể là bước hiện hành áp chót, không phải bản cũ; lời văn p.18 ("bằng 1/2 trẻ nhỏ") mâu thuẫn với sơ đồ p.50; (c) WHO không có sàn: WHO 2009 p.61 "for adults with IBW >50 kg, 1.5-2 ml/kg" (dịch duy trì mỗi giờ), WHO 2012 p.41 "2-3 ml/kg/hour (or less)" → 1,5 có thể nằm trong WHO. Ví dụ "lệch phiên bản không đo được". |
| Phần phụ nữ có thai (tiểu cầu > 50.000 khi sinh thường, > 75.000 khi mổ) | Mới có ở 2760; 3705 không có, nên không phải lệch phiên bản. Chưa tìm đối chiếu. |
| WHO 2025: corticoid, immunoglobulin | Bộ Y tế không có giá trị tương ứng. |

## (4) Sai lệch so với bộ hạt giống (§3.3 / `seed_conflicts.yaml`)

1. **Dòng 1, trường `superseded` ("3705/2019: cần tra"):** đã tra (ảnh trang PDF p.19). 3705/2019 **giống hệt** 2760/2023 (15 ml/kg/giờ; rồi 10 ml/kg/giờ × 2 giờ). Dòng 1 **không** cho mẩu lệch phiên bản.
2. **Dòng 1, vị trí:** giá trị nằm ở mục **C.2.1.2** (PDF p.28, trang in 27). Mục C.2.1 chỉ là đề mục.
3. **Dòng 1, quần thể:** 2760 tách riêng **sốc nặng người lớn (M = 0, HA = 0)** ở mục C.2.2, với phác đồ 15 ml/kg trong 15 phút rồi cao phân tử. Vì vậy 15 ml/kg/giờ chỉ đúng cho sốc chưa phải sốc nặng. Câu hỏi phải ghi rõ điều này. Bước "10 ml/kg/giờ × 2 giờ" chỉ áp dụng khi đã cải thiện.
4. **Dòng 1, nước ngoài:** WHO 2009 "5–10 ml/kg/giờ trong 1 giờ" đã xác nhận (PDF p.48), nhưng WHO 2009 **không phân tuổi**. Sổ tay WHO 2012 mới ghi rõ 5–10 cho người lớn và 10–20 cho trẻ em.
5. **Ghi chú "đối chiếu thêm WHO 7/2025":** WHO 2025 **không có giá trị số** cho tốc độ dịch, nên không xác nhận cũng không bác bỏ dòng 1. Ngược lại, WHO 2025 cho ra hai xung đột định tính mới (P-03, P-04).
6. **`version_drift_pilot: Dengue 3705/2019 → 2760/2023`:** thay đổi giá trị ít hơn kỳ vọng. Hầu hết số liệu điều trị giữ nguyên, gồm:
   - dịch cho dấu hiệu cảnh báo trẻ em/người lớn;
   - sốc người lớn và trẻ em (nhánh chính);
   - paracetamol;
   - chỉ định truyền máu, tiểu cầu, huyết tương;
   - vitamin K1;
   - Hct nền 43%/38%;
   - tiêu chuẩn ra viện;
   - dấu hiệu cảnh báo.

   Các thay đổi thật tìm được:
   - Gelatin (P-06);
   - tách phác đồ sốc nặng người lớn (P-05);
   - mục thiếu niên 13–16 tuổi (P-07);
   - nhánh tụt HA trẻ em 20 ml/kg/30 phút (bị loại vì bộ phân tích);
   - ngưỡng albumin < 2 → < 2,5 g/dL (bị loại vì đơn vị);
   - tiêu chí cân nặng hiệu chỉnh người lớn (BMI ≥ 25 thay cho > 120% CN lý tưởng);
   - xét nghiệm NS1 thêm khung "ngày 1–7".
7. **Đối chứng "phân loại dengue và dấu hiệu cảnh báo":** tiêu chuẩn nặng (AST/ALT ≥ 1000) trùng WHO (P-09). Tuy vậy, danh sách dấu hiệu cảnh báo của Việt Nam **không trùng hoàn toàn** WHO 2009 (có thêm AST/ALT ≥ 400 U/L và định lượng số lần nôn).
8. **§3.3 ghi "WHO arbovirus (4/7/2025)":** metadata IRIS ghi dc.date.issued = 2025-07-03. Chênh lệch nhỏ, cần thống nhất khi trích dẫn.

## (5) Việc cần người kiểm ở HG1.2

1. **Bản 3705/2019:**
   - Đối chiếu bằng mắt mọi `extraction.superseded_spans` (PDF p.6, 8, 9, 11, 19) với ảnh trang.
   - Quyết định có chấp nhận bản quét mang watermark LuatVietnam do BV Phú Nhuận đăng lại hay không. Nếu được, hãy tìm bản sạch (lưu trữ kcb.vn / moh.gov.vn) hoặc chạy OCR có dấu.
   - Tất cả mẩu có superseded đều ghi `machine_verified: false`.
2. **Giá trị bản cũ là suy ra:**
   - P-05: 60 phút, suy từ "trong 1 giờ đầu … 15ml/kg/giờ" dưới đề mục "sốc SXHD, sốc SXHD nặng".
   - P-07: 3 ml/kg/giờ, vì trẻ 13–16 tuổi thuộc phác đồ trẻ em < 16 tuổi của 3705.
3. **Giá trị CDC cần diễn giải:**
   - P-01: 40–80 ml/kg/giờ là quy đổi từ "20 mL/kg trong 15–30 phút".
   - P-02: nguồn in "10mg/kg for 1-2 hrs", đã hiểu là mL/kg/giờ.
   - P-10: CDC dùng "< 20" chứ không phải "≤ 20".
4. **Mồi sinh bằng quy tắc `mirror_decoy` trùng giá trị Việt Nam của quần thể khác:**
   - P-01: mồi 20–25 ml/kg/giờ chứa 20 ml/kg/giờ, là tốc độ giờ đầu của **trẻ em** theo chính 2760. Chạy thử "20 ml/kg/giờ" → decoy_match.
   - P-02: mồi 13–15 chứa 15, là tốc độ giờ đầu người lớn.
   - Hệ quả: tỉ lệ trùng mồi có thể bị thổi phồng vì mô hình nhầm quần thể, không phải trùng ngẫu nhiên. Cần quyết định giữ nguyên, hay sửa quy tắc (xem mục 6).
5. **Quần thể của các mẩu cat:**
   - P-03: bệnh nhân đang truyền dịch vì có dấu hiệu cảnh báo rồi mới sốc. WHO 2012 cho phép ưu tiên dịch keo khi sốc **tụt HA**, nên đã giới hạn ở sốc còn bù.
   - P-04: xác nhận analgin = metamizol natri (dipyrone). Khuyến cáo WHO 2025 là có điều kiện, kèm ghi chú "hạn chế về tính sẵn có".
   - P-06: câu hỏi Có/Không.
6. **P-07 là indistinguishable:** không dùng cho kiểm định xác nhận. Cần xác nhận có giữ trong thí điểm hay không.
7. **Việc chỉ bác sĩ làm được:** `moh_lags_evidence`, `clinical_harm` (đặc biệt P-03 dịch keo so với tinh thể, và P-04 metamizol). Chưa có bác sĩ duyệt.

## (6) Đề xuất bổ sung configs / mã (không tự sửa)

1. **`configs/grading.yaml` → `drugs`:**
   - Thêm `metamizole: [metamizol, analgin, dipyrone, dipyron, novalgin]`, `paracetamol: [acetaminophen]`, `ibuprofen: []`, `aspirin: [acetylsalicylic acid, acid acetylsalicylic]`.
   - Thêm các dịch nếu muốn chấm dạng `drugs`: `ringer-lactate`, `sodium-chloride-0.9`, `dextran-40`, `hydroxyethyl-starch`, `gelatin`, `albumin`.
2. **`src/vnsoc/normalize_vi.py` → `UNIT_ALIASES`** (kèm test):
   - `"ml/kg": "ml/kg"`: phải khớp trước "ml" (khóa đã sắp theo độ dài nên chỉ cần thêm). Mở lại được 3 ứng viên ở mục 3.
   - `"g/dl": "g/dL"` và `"g/l": "g/L"`, kèm cạnh (g/L → g/dL) = 0,1. Mở lại được mẩu ngưỡng albumin (lệch phiên bản thật).
   - Cạnh (h, day) = 1/24. Mở lại được mẩu tiêu chuẩn ra viện 2 ngày = 48 giờ.
3. **`NUM_RE` / `parse_nums`:** hiện bỏ qua số đứng sau "/", nên không đọc được "20 ml/kg/30 phút" hay "15 - 20ml/kg/15 - 30 phút". Đề xuất một mẫu ghép "X ml/kg/Y phút|giờ". Có thể trả về cả thể tích (X ml/kg) lẫn thời gian (Y phút), hoặc quy đổi thành tốc độ X·60/Y ml/kg/h, kèm test.
4. **`vnsoc.match.sources.fetch`:**
   - Không ghi cache khi nội dung là trang thử thách hoặc rỗng (chars < ~500, có "recaptcha", hoặc HTML khi URL đuôi .pdf).
   - Dọn 2 mục rác hiện có: NBK616301 và `.../9789240111110-eng.pdf` trong `data/cache/foreign/index.json`.
   - Ghi chú: WHO IRIS tải được ổn định qua REST `https://iris.who.int/server/api/core/bitstreams/<uuid>/content`. Tra uuid bằng `/server/api/pid/find?id=hdl:<handle>`.
5. **`mirror_decoy`:** thêm bước loại (hoặc cảnh báo) mồi trùng giá trị Bộ Y tế của quần thể lân cận trong cùng văn bản (P-01, P-02). Với mẩu lệch phiên bản không có xung đột nước ngoài (P-05), có thể thêm quy tắc phản chiếu quanh giá trị bản cũ, để kiểm soát ngẫu nhiên cho H2. Cả hai đều là thay đổi quy tắc đăng ký trước, nên cần ghi DECISIONS và báo người dùng.
6. **Manifest:** thêm 2 dòng cho 2760/2023 (`current`, supersedes 3705/2019) và 3705/2019 (`superseded`, `ocr` cần thiết, ghi rõ nguồn có watermark tư nhân). T1.1 chỉ được ghi 2 tệp nên chưa thêm.

Không sửa docs/, configs/, src/, tests/, state/, .claude/. Chỉ ghi vào data/raw qua `fetch_pdf` (2760_2023.pdf, 3705_2019.pdf). Tệp tạm (văn bản trang, ảnh render, script dựng mẩu) nằm trong thư mục scratchpad của phiên.

## (7) Sau kiểm toán (2026-09-26)

**Đầu vào:** `data/interim/pilot/dengue_verify.md` (integrity-auditor, AI). Kết luận kiểm toán: pass 2 (P-06, P-08), fix 7 (P-01–05, P-09, P-10), reject 1 (P-07).

**Cách làm:** agent sửa (Claude, AI, **không phải bác sĩ**) tự kiểm lại bằng chứng bằng công cụ **trước** khi sửa. Mẩu được dựng lại bằng script trong scratchpad (`fix_dengue/build.py`: sửa → `finalize()` → `Atom.model_validate` → `mirror_decoy`/`check_decoy`), rồi chép vào `dengue.jsonl` bằng công cụ Write/Edit. Tệp cuối **trùng từng byte** với bản dựng (sha256 `11ae21b5d521af8a…`). Chỉ ghi `dengue.jsonl` và file này; không ghi `data/raw`, `src`, `configs`, `tests`, `data/seed`.

**Kiểm tra máy trên tệp cuối:**
- `vnsoc.schemas atom` → "OK 9 dòng hợp lệ (atom)".
- `vnsoc.extract.verify_span` → "OK: 0 mẩu không đạt" → `span_verified: true` giữ nguyên cho cả 9 mẩu.
- `finalize()` chạy lại khớp giá trị lưu; `check_decoy == []` cả 9 mẩu; `mirror_decoy` tái tạo đúng mồi P-01 (20–25) và P-02 (13–15).
- Không mẩu nào có `moh_lags_evidence`, `clinical_harm`, `clinician_confirmed`.

### 7.1 Bằng chứng agent sửa đã tự kiểm lại

| Nguồn | Cách kiểm | Kết quả |
|---|---|---|
| 2760/2023 (sha `5936c4e425a17db8`) | `verify_span --page` p.14, 15, 28, 29, 30, 34, 42, 46, 50, 55, 56; `--find` "lbumin" → [15, 16, 20, 21, 26, 27, 30, 51, 59]; "25 mmHg" → [14, 46, 50]; "4 lần/6 giờ" → [38, 39, 65] | Khớp kiểm toán: p.15 và Phụ lục 6 p.42 (nhánh B2: liều đầu CPT 10–15 ml/kg/giờ); p.14 phác đồ B2 người lớn 6 → 3 → 1,5 ml/kg/giờ và "hiệu áp = 25 mmHg: điều trị như sốc SXHD"; p.30 bước 2 sốc nặng 15 ml/kg/giờ x 1 giờ. **Mới:** p.30 (C.2.3) albumin 1 g/kg khi sốc kéo dài/tái sốc; p.34 PNCT "truyền dịch chống sốc tương tự phụ nữ không mang thai" |
| 3705/2019 (sha `fcd393c4ef07ad8c`, bản quét) | Ảnh p.19 và p.39 (PyMuPDF 130 dpi, scratchpad), đọc bằng mắt | p.19: đề mục "C.2.1. Điều trị sốc sốt xuất huyết Dengue, sốc sốt xuất huyết Dengue nặng", câu "Trong 1 giờ đầu … 15ml/kg/giờ …", a) "… 10ml/kg/giờ x 2 giờ". p.39 (Phụ lục 14, ghi tay "3705/QĐ-BYT ngày 22 tháng 8 năm 2019"): ô "SỐC SXHD hoặc SỐC SXHD NẶNG" → "Thở Oxy" → "RL hoặc NaCl 0,9% 15 ml/kg/giờ x 1 giờ" → (cải thiện) "RL hoặc NaCl 0,9% 10 ml/kg/giờ x 2 giờ". Watermark LuatVietnam ở chân trang |
| CDC 2024 (sha `20dad79a31da86cc`) | `sources grep` + **ảnh p.5** (260 dpi) | p.5: ô "Reduce IV crystalloid solution to 10mg/kg for 1-2 hrs" là nhánh YES ngay sau liều crystalloid đầu 20 mL/kg/15–30 phút, ô kế tiếp "5-7mL/kg/hr for 2-4 hrs" → cùng slot với P-02 nhưng đơn vị là diễn giải. p.1 "ALT or AST>1000 IU" (nhóm C); p.6 "≥1000" (tiêu chí nhập viện); p.2 "colloids (such as albumin) for refractory shock"; p.1 "≥3 episodes in 1 hr or ≥4 in 6 hrs" |
| WHO 2012 (sha `b0ca16915451b163`) | `sources grep` | p.39, 40, 42 "colloid is preferable if the patient has already received previous boluses of crystalloid"; p.34 tóm tắt: sốc còn bù 5-10 ml/kg/hr, sốc tụt HA "20 ml/kg as a bolus for 15 min"; p.38 "5-10 ml/kg/hour over one hour in adults"; p.41 "over 15-30 minutes", "2-3 ml/kg/hour (or less)"; "albumin" chỉ có trong ca bệnh minh họa |
| WHO 2009 (sha `f6f48811df824c02`) | `sources grep` | p.48 "5-10 ml/kg/hour over one hour"; p.49 "20 ml/kg as a bolus given over 15 minutes"; p.61 "IBW >50 kg, 1.5-2 ml/kg" (maintenance mỗi giờ); "albumin" = 0 kết quả |
| WHO 2025 (sha `cbbe4513ef91cc6b`) | `sources grep` + đọc p.15, 47–49 | p.15 tóm tắt metamizole (p.7 chỉ là danh mục bảng); p.47 §4.2.2; **p.49 coi metamizole là lựa chọn thay thế ("alternative to") paracetamol** ở nước đã phê duyệt, không đặt điều kiện paracetamol thất bại; p.60 ghi chú cá thể hóa "subsequent to the initial resuscitation"; p.28 chỉ dẫn chiếu "WHO 2009 definition", "AST or ALT" = 0 kết quả; p.62 hypertonic saline/albumin chỉ xuất hiện trong bảng đếm nghiên cứu |

Mọi phát hiện của kiểm toán mà agent sửa kiểm lại đều **đúng**. Không thấy chỗ nào kiểm toán sai về dữ kiện nguồn.

### 7.2 Đã sửa gì (theo mẩu)

| Mẩu | Kiểm toán | Đã sửa | Trạng thái sau sửa (finalize) |
|---|---|---|---|
| P-01 | fix | **Bỏ mục US/CDC** (40–80 ml/kg/giờ là quy đổi, không có trong nguồn). Thêm `population.history` "vào viện trong tình trạng sốc, CHƯA truyền dịch" (loại nhánh B2). Thêm span bản cũ Phụ lục 14 p.39. Thêm `extraction.neighbor_values`; ghi rõ lý do giữ mồi trong `decoy_rule` | conflict, tol 2,5, mồi 20–25 (không đổi) |
| P-02 | fix | CDC: `verified_by: null` + "needs_human_check" trong locator; `values[0].text` ghi rõ nguồn in "10mg/kg for 1-2 hrs". `population.severity` nêu "KHÔNG phải sốc nặng" (bước 2 sốc nặng = 15 ml/kg/giờ, p.30); thêm `history`. Thêm span bản cũ p.39 (ô 10 ml/kg/giờ x 2 giờ). Thêm `neighbor_values` | conflict, tol 1,5, mồi 13–15 (không đổi) |
| P-03 | fix | `population.severity`: đang truyền duy trì B2 (6 → 3 → 1,5), **CHƯA nhận bolus**. Locator WHO 2012 thêm ngoại lệ p.39/40/42; WHO 2025 thêm ghi chú p.60. `cat_options.colloid` thêm "dich keo", "starch". Nhãn mồi `albumin` chỉ gán khi câu trả lời **không** có từ dịch keo chung/tổng hợp. Ghi chênh lệch nội tại C.2.1.2 và B2 vào notes | conflict (không đổi) |
| P-04 | fix (nhẹ) | Locator WHO 2025 → p.47 + tóm tắt p.15 + bảng liều p.49. Viết lại `cat_options`: not_allowed bắt "chống chỉ định analgin", "contraindicated", "tránh dùng", "không nên/không sử dụng", "bị cấm"; allowed có điều kiện phủ định để câu "dùng khi paracetamol không hiệu quả" rơi vào `second_line_only` (ưu tiên mồi hơn allowed **ở mức dữ liệu**, không sửa mã); lookbehind `(?<!khong )` để "không được dùng" không lọt vào allowed. **Mới (ngoài kiểm toán):** chuyển "thay thế paracetamol" từ second_line_only sang allowed, vì WHO 2025 p.49 dùng đúng cách nói đó | conflict (không đổi) |
| P-05 | fix | `superseded_spans` thay bằng **3 span nguyên văn** (bỏ span có "…"): đề mục C.2.1 p.19; câu "Trong 1 giờ đầu…" p.19; ô Phụ lục 14 p.39 kèm `context_box` "SỐC SXHD hoặc SỐC SXHD NẶNG". `superseded[0].values[0].text` ghi rõ "(phép tính)"; thêm `extraction.derived_values`. Locator WHO 2012 thêm tóm tắt p.34 "bolus for 15 min" | concordant, tol 22,5 (không đổi); vẫn là mẩu lệch phiên bản (60 phút tách được) |
| P-06 | pass | Không đổi | no_counterpart |
| P-07 | **reject** | **Xóa khỏi jsonl**; thêm vào mục (3) kèm lý do đã tự kiểm | — |
| P-08 | pass | Không đổi | concordant |
| P-09 | fix (nhẹ) | CDC: `cmp` ">=" → ">", text "ALT hoặc AST > 1000 IU (nhóm C)", locator tách p.1 (phân độ) và p.6 (nhập viện). Không thêm WHO 2025 vì p.28 chỉ dẫn chiếu định nghĩa WHO 2009, không in giá trị (không grep được) | concordant (không đổi) |
| P-10 | fix (nhẹ) | `population.context` → "ĐỊNH NGHĨA huyết áp kẹt — KHÔNG phải ngưỡng 'xử trí như sốc' 25 mmHg (p.14, 46, 50)"; notes cấm question-writer hỏi ngưỡng "xử trí như sốc"; thêm `neighbor_values` | concordant (không đổi) |

### 7.3 Giữ gì, làm khác kiểm toán ở đâu, và vì sao

1. **`verified_by: "needs_human_check"` không hợp lệ theo schema.** `ForeignValue.verified_by` chỉ nhận `auto | student | clinician | null`. Vì vậy dùng `null` và ghi "needs_human_check" trong `locator`, giống cách `htn.jsonl` đã làm.
2. **P-01 — bỏ hẳn CDC** (phương án thứ nhất của kiểm toán), không giữ kèm `null`. Lý do:
   - giá trị không có trong nguồn;
   - câu trả lời kiểu CDC ("20 ml/kg trong 15–30 phút") vẫn bị chấm nhãn 5, dù có hay không có mục này (đã dò);
   - bỏ mục này không đổi tolerance, trạng thái hay mồi.
3. **P-02 — giữ CDC với `null`** (kiểm toán cho phép). Ảnh p.5 xác nhận ô này đúng là bước 2 sau liều đầu, nên cùng slot. Giá trị trùng Việt Nam, nên không ảnh hưởng trạng thái.
4. **P-03 — giữ mồi albumin, sửa nhãn chấm** (nhánh thứ hai của kiểm toán: "nếu giữ albumin, bộ chấm phải xếp 'colloid … albumin' vào một nhãn"). Lý do:
   - Đề cương §1.2 đòi mồi "hợp lý như nhau". Một phương án không phải dịch keo và không phải dịch tinh thể đẳng trương (ví dụ glucose 5%, NaCl 3%) kém hợp lý hơn rất nhiều so với đáp án nước ngoài "dịch tinh thể". Mồi như vậy sẽ hạ tỉ lệ trùng mồi và làm H1 **dễ xác nhận hơn thực tế** (thiên lệch không thận trọng).
   - **Nhưng** agent sửa phát hiện thêm: albumin là giá trị thật của **bước lân cận** (2760 p.30 C.2.3: albumin 1 g/kg khi sốc kéo dài hoặc tái sốc; CDC p.2: sốc kháng trị). Đây cùng loại vấn đề mà kiểm toán nêu cho P-01/P-02.
   - → Ghi vào `neighbor_values`. **Bác sĩ HG chọn** giữ albumin (thận trọng cho H1) hay đổi sang phương án không lân cận.
5. **P-03 — không thêm `\bkeo\b`** như kiểm toán đề xuất. Sau khi bỏ dấu, "kéo dài" cũng thành "keo", nên câu "Ringer lactate, tránh truyền kéo dài" sẽ bị gắn nhãn colloid và chấm đúng Bộ Y tế. Chỉ thêm "dich keo" (bao cả "dung dịch keo") và "starch".
6. **P-01/P-02 — giữ mồi theo quy tắc đăng ký trước** (đồng ý kiểm toán). Chỉ **thêm dữ liệu** `extraction.neighbor_values` (trường tự do trong `extraction`) để khi DECISIONS duyệt quy tắc mới thì `check_decoy` dùng được ngay. Không đổi quy tắc.
7. **P-06, P-08 (pass):** không đổi byte nào.

### 7.4 Dò bộ chấm bằng câu giả (không phải đầu ra mô hình)

Chạy `vnsoc.grade.grade_short(..., condition="A1")` trên câu giả, cùng bộ câu cho `cat_options` cũ và mới (script `fix_dengue/probe.py` trong scratchpad). Mỗi nhãn có ≥ 5 cách nói VI/EN, gồm cả phủ định đảo trật tự.

| Mẩu | Số câu | Sai với `cat_options` cũ | Sai với `cat_options` mới |
|---|---|---|---|
| P-03 | 17 (7 đúng Bộ Y tế, 5 nước ngoài, 5 mồi) | 4 | **0** |
| P-04 | 26 (12 đúng Bộ Y tế, 6 nước ngoài, 8 mồi) | 9 | **0** |

Ví dụ đã sửa được:
- "ĐÁP ÁN: dịch keo": 6 → 2.
- "dịch keo như albumin": 5 + mồi → 2.
- "a colloid such as albumin": 2 + mồi → 2, không mồi.
- "Chống chỉ định analgin": 6 → 2.
- "Có thể dùng metamizol khi paracetamol không hiệu quả": 4 → 5 + mồi.
- "Không dùng analgin trừ khi paracetamol thất bại": 2 → 5 + mồi.
- "Metamizol có thể dùng thay thế paracetamol": 5 + mồi → 4.

Giới hạn còn lại (đã dò, **chưa** sửa được ở mức dữ liệu):
- (a) Câu phủ định có mệnh đề "khi/nếu paracetamol không hiệu quả" (ví dụ "Không dùng analgin; nếu paracetamol không hiệu quả thì chườm mát") → nhãn **2 đúng**, nhưng `decoy_match` **bật sai**.
- (b) Câu trả lời lưỡng lự chứa hai phương án ("Ringer lactate hoặc dịch keo") → nhãn **2**. Nguyên nhân: `parse_cats` gộp mọi nhãn vào **một** giá trị, nên `grade_short` không coi là câu nhiều giá trị (khác với mẩu num). Đây là lỗi mã, xem đề xuất 7.7.
- (c) "albumin hoặc Ringer lactate" → 4 + mồi.
- Cần test chính thức trong `tests/` trước khi đóng băng quy tắc chấm. Có thể dùng 43 câu trong `probe.py` làm nền.

### 7.5 Số mẩu sau kiểm toán

| Loại (thiết kế) | Mẩu | Chỉ tiêu |
|---|---|---|
| Xung đột | P-01, 02, 03, 04 (**3 họ độc lập**: 01 và 02 cùng họ) | 2–3 → đạt; nếu cắt còn 3 thì bỏ P-02 |
| Lệch phiên bản | P-05, P-06 | 2–4 → đạt (sàn) |
| Đối chứng | P-08, 09, 10 | 2–3 → đạt |

Theo `conflict_status` máy tính: conflict 4, concordant 4 (gồm P-05, là mẩu lệch phiên bản trùng nước ngoài), no_counterpart 1 (P-06).

Hai mẩu lệch phiên bản đều phụ thuộc bản quét 3705/2019 (xem 7.6 mục 1). Nếu HG từ chối nguồn này, chủ đề dengue **mất cả hai** mẩu lệch phiên bản.

### 7.6 Tồn đọng cho HG1.2 (người/bác sĩ thật)

1. **Nguồn 3705/2019** — quyết định sống còn cho P-05, P-06.
   - Bản quét duy nhất mang watermark LuatVietnam, do BV quận Phú Nhuận đăng lại trên medinet.gov.vn.
   - Người dùng quyết định có chấp nhận hay không.
   - Nếu chấp nhận: chạy `vnsoc.extract.ocr --key 3705/2019 --override-text-layer` (tính vào trần 10 văn bản OCR). Sau đó đổi `machine_verified` theo kết quả thật. Mọi `superseded_spans` hiện vẫn là `false`.
   - Trong đó có 2 span mới ở p.39 (P-01, P-02, P-05): là ô chữ của **sơ đồ**, nên OCR có thể không khớp nguyên văn → cần người đối chiếu ảnh.
2. **P-02, CDC:** xác nhận cách đọc "10mg/kg for 1-2 hrs" (10 mL/kg/giờ hay 10 mL/kg trong 1–2 giờ). Mục này hiện có `verified_by: null`.
3. **P-03:**
   - chọn mồi (giữ albumin, là bước lân cận; hay đổi);
   - duyệt cách diễn đạt quần thể "đang truyền duy trì B2, chưa bolus";
   - nhận định lâm sàng về chênh lệch nội tại C.2.1.2 và B2 của 2760 (dịch tinh thể trước hay cao phân tử trước).
4. **P-01:** duyệt cách diễn đạt "vào viện trong tình trạng sốc, chưa truyền dịch".
5. **P-05:** xác nhận giá trị bản cũ 60 phút là phép tính hợp lệ (`extraction.derived_values`).
6. **Quyết định giữ P-02** nếu phải cắt còn 3 xung đột.
7. **Quy tắc mồi lân cận:** xem 7.7 mục 1. Cần DECISIONS và người dùng duyệt vì là quy tắc đăng ký trước.
8. **Tính hiện hành của 2760/2023:** WebSearch của phiên đã hết hạn mức. Giao corpus-librarian kiểm moh.gov.vn, vncdc.gov.vn và trang Sở Y tế trước khi đóng băng kho (15/10/2026).
9. **Trường chỉ-bác-sĩ** (`moh_lags_evidence`, `clinical_harm`, `clinician_confirmed`), đặc biệt cho P-03 và P-04: chưa điền, chờ bác sĩ.

### 7.7 Đề xuất mã / config (không tự sửa)

1. **`check_decoy` + `extraction.neighbor_values`:**
   - loại mồi trùng giá trị thật của quần thể hoặc bước lân cận (đã điền cho P-01, 02, 03, 10);
   - khi đó `choose_decoy` chuyển sang `mirror_geom` / `mirror_far` theo thứ tự đã định;
   - ghi DECISIONS và báo người dùng.
2. **`vnsoc.grade` với mẩu cat:** khi `Cat.labels` có ≥ 2 nhãn thuộc các nguồn khác nhau, xử lý như câu nhiều giá trị (`multi`). Hiện tại "Ringer lactate hoặc dịch keo" được nhãn 2.
3. **`normalize_vi.parse_cats` hạ chữ thường cả mẫu regex** (`p.lower()`), nên `\S`, `\D`, `\W`, `\B` sẽ lặng lẽ đổi nghĩa thành `\s`, `\d`, `\w`, `\b`.
   - Mẫu hiện có không dùng các ký hiệu này (agent sửa đã tránh; dùng `(?s)` thay cho `[\s\S]`).
   - Đề xuất: dùng `re.I` thay cho `lower()`, hoặc kiểm mẫu khi nạp.
4. **Schema `ForeignValue`:** thêm cờ `derived: bool` hoặc giá trị `needs_human_check` cho `verified_by`. `vnsoc.check` nên từ chối `verified_by: "auto"` khi `sources.grep(url, value)` rỗng.
5. **`normalize_vi`:** thêm đơn vị "ml/kg", "g/dL", "lần/giờ" và mẫu "X ml/kg/Y phút" (xem mục (6), ý 2–3). Việc này mở lại các ứng viên:
   - thể tích bolus sốc nặng 15 so với 20 ml/kg (xung đột);
   - ngưỡng albumin < 2 → < 2,5 g/dL (lệch phiên bản);
   - nôn ≥ 3 lần/1 giờ (đối chứng).
6. **Test** `tests/test_cat_options_dengue.py`: dùng 43 câu dò ở 7.4, cộng các giới hạn (a)–(c) làm `xfail`.
