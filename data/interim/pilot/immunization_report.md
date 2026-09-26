# Báo cáo T1.1 thí điểm — chủ đề `immunization` (Tiêm chủng mở rộng trẻ em)

Người làm: agent atom-extractor + counterpart-matcher (Claude), ngày 26/09/2026.
Kết quả: **4 mẩu, cả 4 đã kiểm span (`verify_span` OK) và qua schema** — 2 xung đột (chỉ với Mỹ), 2 đối chứng.

> **Phát hiện quan trọng nhất:** văn bản mà bảng hạt giống và task nêu (TT 10/2024) **không còn hiệu lực**.
> Chuỗi văn bản: TT 38/2017 → **TT 10/2024** (hiệu lực 01/8/2024) → **TT 52/2025** (ký 31/12/2025, hiệu lực 15/02/2026, bãi bỏ TT 10/2024)
> → **TT 13/2026/TT-BYT** "Quy định về hoạt động tiêm chủng" (ký 16/5/2026, hiệu lực **01/7/2026**; Điều 27 khoản 2 điểm d bãi bỏ TT 52/2025).
> TT 13/2026 **không ghi lịch tiêm**. Điều 5 khoản 4 giao lịch tiêm cho "hướng dẫn chuyên môn của Cục Phòng bệnh", và tôi **chưa tìm thấy** văn bản hướng dẫn đó.
> Vì vậy 4 mẩu dưới đây lấy span từ **TT 52/2025**, văn bản cuối cùng có lịch tiêm, có lớp chữ và kiểm span được. Mỗi mẩu ghi `valid_to: 2026-06-30`, và cần người quyết ở HG1.2 trước khi dùng làm "chuẩn hiện hành".
> Giá trị không đổi giữa TT 10/2024 và TT 52/2025 (TT 10/2024 là bản quét, tôi đọc bằng mắt). Riêng liều sơ sinh viêm gan B "trong vòng 24 giờ sau sinh" vẫn có trong TT 13/2026, Điều 26 khoản 1 (bản quét, đọc bằng mắt).
>
> **[Cập nhật sau kiểm toán, 26/09/2026 — xem mục 7]:** Máy đã có OCR. Mẩu 03 nay neo vào **TT 13/2026 (đang hiệu lực) trang 18**, span lấy từ OCR và đã qua `verify_span`. Mẩu 01, 02, 04 vẫn neo vào TT 52/2025 và **bị chặn ở HG1.2**. Cả 4 mẩu đã có thêm hệ EU_UK (UKHSA 9/2026) ở những chỗ có giá trị tương ứng, và thêm bản CDC 2025 gốc.

---

## 1. Văn bản đã tải

### 1a. Văn bản Việt Nam (qua `vnsoc.extract.fetch_pdf`, lưu `data/raw/`)

| Khóa | URL | sha256 (16) | Số trang | text_kind | Nơi tìm / xác nhận danh tính |
|---|---|---|---|---|---|
| `TT10/2024` | https://datafiles.chinhphu.vn/cpp/files/vbpq/2024/6/10-byt.pdf | `cb760684d3fb7e09` | 5 | **scanned_or_empty** | Hệ thống văn bản, Cổng TTĐT Chính phủ (vanban.chinhphu.vn, docid=210413). Bản "SAO Y", ký số Bộ Y tế 13/06/2024. Tôi đọc bằng mắt: tiêu đề, Điều 1 (bảng lịch), Điều 4 (hiệu lực 01/8/2024, bãi bỏ TT 38/2017). **Không kiểm span được, không tạo mẩu.** |
| `TT52/2025` | https://cmsapi.tiemchungmorong.vn/assets/e5510aa2-618f-499a-8da6-7f4bbe05f33e | `fbaa37ef7d626c4f` | 10 | **ok** | Trang tài liệu của Văn phòng Tiêm chủng Quốc gia, Viện VSDT Trung ương (tiemchungmorong.vn/document/thong-tu-52-2025-tt-byt-ngay-31-12-2025-…). Lớp chữ để trống số và ngày ("Số: /2025/TT-BYT"). Dấu ký số chèn số "52", ngày "31 12" (trang 1) và "15 02" (ngày hiệu lực, Điều 4, trang 9). Tiêu đề đúng. Người ký: Thứ trưởng Nguyễn Thị Liên Hương. Điều 4 khoản 2 bãi bỏ TT 10/2024. **Dùng để tạo mẩu.** |
| `TT13/2026` | https://bcp.cdnchinhphu.vn/334894974524682240/2026/5/20/tt-13-2026-byt-quy-dinh-ve-hoat-dong-tiem-chung-17792452503061057865388.pdf | `8328ae009d5eae4a` | 19 | **scanned_or_empty** | Link PDF toàn văn trong bài của Báo điện tử Chính phủ (baochinhphu.vn, 20/5/2026). Bản quét (HP Scan), số 13/2026/TT-BYT, ngày 16/5/2026. Tôi đọc bằng mắt: Điều 3 (14 bệnh, có HPV), Điều 5 khoản 4 (lịch tiêm theo hướng dẫn Cục Phòng bệnh, trang 3), Điều 26 khoản 1 (viêm gan B trong 24 giờ sau sinh, trang 18), Điều 27 (hiệu lực 01/7/2026, bãi bỏ TT 24/2018, 34/2018, 05/2020, 52/2025, trang 18). ~~Không kiểm span được.~~ **[Sau kiểm toán: đã OCR đủ 19 trang, sidecar `data/interim/ocr/TT13_2026`, nên nay kiểm span được. Mẩu 03 dùng trang 18.]** |

Không tìm được bản TT 52/2025 hay TT 13/2026 trên kcb.vn, moh.gov.vn hoặc vncdc.gov.vn (vncdc.gov.vn bị lỗi chứng chỉ khi mở). Thử đoán đường dẫn datafiles.chinhphu.vn cho TT 52/2025 và TT 13/2026 đều trả 404. Không truy cập trang thư viện pháp luật tư nhân. Một số kết quả tìm kiếm chỉ trỏ tới trang đó.

### 1b. Nguồn nước ngoài (qua `vnsoc.match.sources fetch`, chỉ lưu giá trị, vị trí và băm)

| Hệ thống | Nguồn | URL | sha256 (16) | Ghi chú |
|---|---|---|---|---|
| US | CDC/ACIP Child & Adolescent Immunization Schedule, **2025 (revised 07/02/2025)**, PDF 18 trang | https://www.cdc.gov/vaccines/hcp/imz-schedules/downloads/child/0-18yrs-child-combined-schedule.pdf | `96159043a4ebc044` | Trang HTML `child-adolescent-age.html` trả 403 với bộ tải. PDF ở đúng URL này hiện vẫn là bản 2025. |
| US (bối cảnh) | Congressional Research Service R48982 "The 2026 Childhood Immunization Schedule" (11/6/2026) | https://www.congress.gov/crs_external_products/R/PDF/R48982/R48982.1.pdf | `66d7d66dc7095b31` | Chỉ dùng để xác định bản CDC nào đang có hiệu lực. Không lấy giá trị từ đây. |
| WHO_global | WHO Table 1 – Summary of WHO Position Papers, Recommendations for Routine Immunization (**updated December 2025**), 13 trang | https://cdn.who.int/media/docs/default-source/immunization/immunization_schedules/immunization-summary-table-1.pdf?sfvrsn=2e112cea_16&download=true | `9861c483644986f4` | Bản hiện hành. |
| WHO_global | Measles vaccines: WHO position paper – April 2017, bản tóm tắt chính thức, 2 trang | https://cdn.who.int/media/docs/default-source/immunization/position_paper_documents/measles/who-pp-measles-vaccine-summary-2017.pdf?sfvrsn=e546119a_2 | `704cfe534804547e` | PDF WER 92(17) trên IRIS (iris.who.int/bitstream/…/WER9217.pdf) trả HTML rỗng, nên không dùng. |

**Bản CDC nào đang có hiệu lực (9/2026):** ngày 05/01/2026, HHS/CDC ban hành lịch trẻ em sửa đổi. Viêm gan B, viêm gan A, cúm, COVID-19 và não mô cầu chuyển sang "quyết định lâm sàng chung" hoặc chỉ cho nhóm nguy cơ. Liều sơ sinh viêm gan B cho trẻ có mẹ HBsAg âm tính chuyển sang quyết định cá nhân, theo phiếu ACIP 12/2025. Ngày **16/3/2026**, Tòa Liên bang quận Massachusetts (AAP v. Kennedy) **đình chỉ** bản sửa đổi và đưa lịch về ~~bản trước tháng 6/2025~~ **"the version as of May 2025"** (CRS R48982 trang 5). Chính phủ Mỹ kháng cáo ngày 29/4/2026. ~~Theo tin tìm kiếm, Tòa phúc thẩm Khu vực 1 sẽ nghe tranh luận ngày 06/10/2026, trước ngày đóng băng kho 15/10/2026.~~ **[Sửa sau kiểm toán: tuyên bố về ngày 06/10/2026 không có trong nguồn nào đã băm, nên đã xóa khỏi mẩu. Nguồn đã băm mới nhất là CRS R48982 ngày 11/6/2026, cả bản .1 lẫn .2. Tình trạng sau ngày đó chưa kiểm.]** ~~Vì vậy mẩu ghi CDC 2025 (revised 07/02/2025) là bản Mỹ đang có hiệu lực~~ **[Sửa: mẩu nay ghi cả hai bản CDC 2025, bản gốc và bản sửa 07/02/2025. Hai bản có giá trị giống nhau. Chưa xác định được bản nào đúng là "version as of May 2025", xem mục 7.]** Không phải "bản 2026". Với sởi và DTaP, bản 2026 không đổi giá trị. Với viêm gan B sơ sinh, bản 2026 khác (xem mục 5).

---

## 2. Bảng mẩu

> Bảng dưới là bản **trước kiểm toán**. Bảng hiện hành ở **mục 7.2**.

| id | slot | Việt Nam (TT 52/2025) | Nước ngoài (hệ thống: giá trị, phiên bản) | Trạng thái (`finalize`) | Trang PDF | Mồi |
|---|---|---|---|---|---|---|
| P-immunization-01 (hạt giống dòng 23) | Tuổi tiêm mũi 1 vắc xin sởi (MCV1), tiêm thường xuyên | **9 tháng** ("khi trẻ đủ 9 tháng tuổi") | US: 12–15 tháng (CDC 2025, Notes MMR p.10). WHO_global: 9 tháng cho nước còn lây truyền (Table 1 12/2025 p.8; PP sởi 2017) | **conflict** (chỉ Mỹ), tol 1,5 | 7 | 3–6 tháng (mirror_arith) |
| P-immunization-02 (mẩu mới) | Tuổi mũi nhắc lại lần 2 vắc xin có thành phần bạch hầu | **7 tuổi** ("Tiêm nhắc lại lần 2 khi trẻ đủ 7 tuổi", bạch hầu giảm liều) | US: 4–6 tuổi (DTaP liều 5; CDC 2025 p.8). WHO_global: 4–7 tuổi (Td/DT; Table 1 p.1, p.6) | **conflict** (chỉ Mỹ), tol 0,5 | 3 | 8–10 tuổi (mirror_arith) |
| P-immunization-03 | Thời hạn tiêm liều sơ sinh viêm gan B (mẹ HBsAg âm tính, ≥ 2000 g) | **trong vòng 24 giờ** sau sinh | US: trong 24 giờ (CDC 2025 p.9, mẹ HBsAg âm tính, ≥ 2000 g). WHO_global: "ideally within 24 hours" (Table 1 p.5) | **concordant** | 1 | — |
| P-immunization-04 | Tuổi mũi nhắc lại lần 1 vắc xin DTP (dòng ho gà) | **18 tháng** | US: 15–18 tháng (DTaP liều 4; CDC 2025 p.8). WHO_global: 12–23 tháng (Table 1 p.1) | **concordant** | 3 | — |

`conflict_family`: `measles_mcv1_age_us`, `dtp_booster2_age_us`, `hepb_birth_dose_timing`, `dtp_booster1_age`.

Tôi đã chấm thử bằng `grade_short`, đúng như kỳ vọng:
- Mẩu 01: "12–15 tháng", "12 months" và "1 tuổi" được chấm là foreign US; "9 tháng" được chấm là đúng; "3–6 tháng" và "6 tháng" trùng mồi.
- Mẩu 02: "4–6 tuổi" và "5 years" được chấm foreign, nhưng **trùng cả US lẫn WHO_global** (xem mục 5).
- Mẩu 03: "1 ngày" bị chấm là không quy được nguồn, vì chưa có quy đổi ngày ↔ giờ (xem mục 6).

---

## 3. Ứng viên bị loại và lý do

1. **Hạt giống dòng 24, DTP cơ bản "2, 3, 4 tháng" so với CDC "2, 4, 6 tháng": loại.** Cả TT 10/2024 (đọc bằng mắt) và TT 52/2025 (trang 2–4) chỉ ghi: mũi 1 khi trẻ đủ 2 tháng, mũi 2 và mũi 3 mỗi mũi "ít nhất 1 tháng" sau mũi trước. Văn bản **không ghi** 3 và 4 tháng. Lịch 2, 4, 6 tháng của CDC vẫn thỏa khoảng cách tối thiểu của Việt Nam, nên xét theo văn bản thì đây không phải xung đột. `verify_span` cũng không thể đọc ra dãy [2, 3, 4] từ span.
2. **Tuổi mũi 1 DTP (Việt Nam 2 tháng, CDC 2 tháng, WHO "sớm nhất từ 6 tuần"): không tạo mẩu.** Giá trị WHO là mức tối thiểu chứ không phải một điểm, nên mơ hồ. Chỉ tiêu đối chứng đã đủ.
3. **Mũi 2 sởi–rubella: Việt Nam 18 tháng, CDC MMR liều 2 lúc 4–6 tuổi, WHO MCV2 15–18 tháng.** Đây là xung đột sạch, chỉ với Mỹ, và quy nguồn rõ hơn mẩu 02. Tôi không đưa vào vì `mirror_decoy` trả "phản chiếu cho giá trị ≤ 0" (không tạo được mồi) và vì đã đủ chỉ tiêu 2 xung đột. Nên thêm nếu quy tắc mồi được mở rộng (mục 6).
4. **Liều sơ sinh viêm gan B khi mẹ HBsAg dương tính hoặc không rõ (CDC: trong 12 giờ, kèm HBIG):** TT 52/2025 không tách quần thể này. Nó thuộc hướng dẫn chuyên đề viêm gan B, ngoài phạm vi chủ đề này.
5. **MCV1 lúc 12 tháng (WHO, nước lây truyền thấp):** quần thể khác nên không ghi làm giá trị. Chỉ ghi chú.
6. **Ứng viên cho vòng sau, chưa làm:**
   - IPV: Việt Nam 5 và 9 tháng, CDC 2, 4, 6–18 tháng và 4–6 tuổi.
   - Uốn ván cho phụ nữ có thai: Việt Nam theo tiền sử, tối đa 5 liều; Mỹ tiêm Tdap mỗi thai kỳ.
   - BCG: Việt Nam trong 1 tháng sau sinh, WHO lúc sinh, Mỹ không tiêm thường quy (không có tương ứng).
   - Viêm não Nhật Bản: Mỹ không có trong lịch thường quy.
   Tất cả phụ thuộc việc xác định văn bản lịch tiêm hiện hành.

---

## 4. Sai lệch so với bộ hạt giống (bảng §3.3, `data/seed/seed_conflicts.yaml`)

| Dòng | Hạt giống ghi | Thực tế kiểm được | Đề xuất |
|---|---|---|---|
| 23 và 24 (văn bản) | `vn_doc: TT 10/2024` | TT 10/2024 hết hiệu lực từ 15/02/2026 (bị TT 52/2025 thay). TT 52/2025 hết hiệu lực từ 01/7/2026 (bị TT 13/2026 bãi bỏ). TT 13/2026 không có lịch tiêm. | Sửa `vn_doc`. Thêm TT 10/2024 và TT 52/2025 vào manifest với trạng thái superseded, TT 13/2026 với trạng thái current (bản quét). |
| 23 (giá trị) | Việt Nam 9 tháng; CDC 12–15 tháng; WHO "giống Việt Nam" | Đúng. Riêng WHO chỉ là 9 tháng cho **nước còn lây truyền**; nước lây truyền thấp là 12 tháng. | Ghi rõ quần thể WHO; giữ `confirmed_us_only`, kèm cảnh báo văn bản. |
| 24 (giá trị và trạng thái) | "2, 3, 4 tháng" so với CDC "2, 4, 6", `confirmed_low_stakes` | "2, 3, 4" **không có nguyên văn**. Văn bản ghi 2 tháng + khoảng cách ≥ 1 tháng, và CDC 2, 4, 6 thỏa điều kiện đó. | Đổi trạng thái thành *không phải xung đột theo văn bản* (loại). |
| Nguồn Mỹ | ~~"CDC (bản 2026)"~~ **[Sửa sau kiểm toán: hạt giống chỉ ghi "CDC", không ghi năm (`seed_conflicts.yaml` dòng 68–72; đề cương dòng 208–209). Chữ "2026" lấy từ đề bài task.]** | Bản 2026 đang bị tòa đình chỉ. Lịch được đưa về "version as of May 2025". Mẩu ghi bản CDC 2025 gốc và bản sửa 07/02/2025; hai bản cùng giá trị. | Ghi phiên bản vào kho đối chiếu; theo dõi phán quyết phúc thẩm. |
| 23 (trạng thái) | "chỉ xung đột với Mỹ" | **[Sau kiểm toán]** Mẩu cũng xung đột với **EU_UK**: UKHSA 9/2026 tiêm MMRV lúc 1 tuổi. | Đổi thành "xung đột với US và EU_UK". `conflict_family` đổi thành `measles_mcv1_age`. |

---

## 5. Việc cần người kiểm ở HG1.2

1. **(Chặn) Xác định văn bản lịch TCMR hiện hành tại 15/10/2026.** Cần tìm "hướng dẫn chuyên môn của Cục Phòng bệnh" về lịch tiêm (theo TT 13/2026 Điều 5 khoản 4), trên vncdc.gov.vn, moh.gov.vn hoặc hỏi Viện VSDT. Nếu có: tải về, tạo lại span và sửa `guideline`. Nếu chưa có: quyết định có coi giá trị TT 52/2025 là "chuẩn Bộ Y tế đang áp dụng trên thực tế" cho thí điểm hay không, và ghi vào `docs/DECISIONS.md`. Hiện cả 4 mẩu đều có `valid_to: 2026-06-30`.
2. **Duyệt nguồn:** tiemchungmorong.vn (Văn phòng TCQG, Viện VSDT TƯ), datafiles.chinhphu.vn, vanban.chinhphu.vn và bcp.cdnchinhphu.vn (Cổng/Báo điện tử Chính phủ) đều chưa có trong `official_hosts`.
3. **Danh tính TT 52/2025:** lớp chữ PDF để trống số và ngày; danh tính dựa trên tiêu đề, người ký, dấu ký số và trang danh mục. Cần người xác nhận.
4. **Bản quét TT 13/2026 và TT 10/2024:** tôi chỉ đọc bằng mắt (TT 13/2026 trang 3, 4, 18). Cần người đối chiếu lại Điều 5 khoản 4, Điều 26 khoản 1 và Điều 27 khoản 2 điểm d.
5. **Mẩu 03 (viêm gan B sơ sinh) có thể đổi trạng thái:** nếu Tòa Khu vực 1 gỡ lệnh đình chỉ trước 15/10/2026, khuyến cáo Mỹ cho trẻ có mẹ HBsAg âm tính sẽ thành quyết định cá nhân, có thể bắt đầu từ ≥ 2 tháng. Khi đó mẩu không còn là đối chứng. Cần kiểm lại ngay trước khi đóng băng. AAP 2026 vẫn khuyến cáo trong 24 giờ, nhưng tôi chưa tải nguồn này.
6. **Mồi:**
   - Mẩu 01: mồi 3–6 tháng chạm mốc 6 tháng. Đó là tuổi của liều sớm trước du lịch (CDC 6–11 tháng) và liều bổ sung khi có dịch (WHO từ 6 tháng); cả hai là quần thể khác. Việc này làm tỉ lệ trùng mồi cao hơn, tức là thiên về bảo thủ cho H1.
   - Mẩu 02: mồi 8–10 tuổi chồng lên khoảng tuổi mũi nhắc thứ 3 của WHO (9–15 tuổi, Td), là một liều khác.
   Cần quyết định có chấp nhận hai mồi này không.
7. **Quy nguồn mẩu 02:** khoảng WHO 4–7 tuổi chứa cả khoảng Mỹ 4–6, nên câu trả lời theo Mỹ được chấm trùng cả US và WHO_global. H1 (bất kỳ nguồn nước ngoài) vẫn dùng được, nhưng phân tích theo hệ thống thì không tách được. Có thể thay bằng mẩu mũi 2 sởi (mục 3.3) nếu có quy tắc mồi thay thế.
8. **Ràng buộc khi viết câu hỏi:**
   - 01: nói rõ tiêm chủng thường xuyên, không du lịch, không có dịch.
   - 02: hỏi tuổi của mũi nhắc lần 2, sau mũi 18 tháng.
   - 03: mẹ HBsAg âm tính, trẻ ≥ 2000 g, ổn định; hỏi **thời hạn tối đa** tính bằng giờ.
   - 04: mũi nhắc lại sau khi đủ 3 mũi cơ bản.
9. Không điền `moh_lags_evidence`, `clinical_harm`, `clinician_confirmed`. Các trường này chờ bác sĩ thật.

---

## 6. Đề xuất bổ sung mã và config (chưa sửa, theo quy tắc 4)

1. **`src/vnsoc/normalize_vi.py` STATIC_EDGES:** thêm cạnh `("day", "h"): 24`, để "1 ngày" / "1 day" quy đổi được về giờ cho mẩu 03. Nên thêm cả `("month", "day"): 30.4375` hoặc `("week", "month")`, vì câu trả lời kiểu "6 tuần" cho các mẩu tính bằng tháng hiện không quy đổi được. Kèm test trong `tests/`.
2. **`src/vnsoc/match/decoys.py`:** khi `mirror_arith` và `mirror_geom` đều cho giá trị ≤ 0 (trường hợp mũi 2 sởi 18 tháng so với 4–6 tuổi), cần một quy tắc dự phòng cố định. Ví dụ: phản chiếu hình học với độ rộng co theo cùng tỉ lệ, `w_d = w_f · c_d / c_f`. Có như vậy mới giữ được mẩu xung đột có mồi.
3. **`configs/project.yaml` `corpus.official_hosts`:** thêm `tiemchungmorong.vn`, `chinhphu.vn` (gồm datafiles., vanban.) và `cdnchinhphu.vn` (bcp.), sau khi người dùng duyệt ở mục 5.2.
4. **Manifest:** thêm các dòng TT 10/2024 (superseded_by TT 52/2025), TT 52/2025 (superseded_by TT 13/2026) và TT 13/2026 (current, OCR cần thiết). Khóa file theo quy ước: `TT10_2024.pdf`, `TT52_2025.pdf`, `TT13_2026.pdf`.
5. `configs/grading.yaml`: không cần thêm thuốc. Chủ đề này không có value_kind drugs.

---

## 7. Sau kiểm toán (26/09/2026)

Làm theo `immunization_verify.md`, trong đó kiểm toán cho kết quả: **4 fix, 0 reject, 0 pass**. Tôi kiểm lại từng điểm bằng công cụ trước khi sửa.

Kết quả: vẫn **4 mẩu**, gồm 2 xung đột và 2 đối chứng, không có mẩu lệch phiên bản.
- Mẩu 03 đã sửa xong và neo vào văn bản **đang hiệu lực**.
- Mẩu 01, 02, 04 đã sửa các trường nhưng **vẫn bị chặn ở HG1.2**, vì văn bản nguồn đã hết hiệu lực. Mỗi mẩu này có trường `extraction.hg_block`.
- `finalize()` cho lại đúng tolerance và trạng thái đã ghi. `check_decoy` = [] cho cả 4 mẩu. Mồi của mẩu 01 và 02 đúng bằng `mirror_decoy(atom)`.
- `vnsoc.schemas atom`: **OK 4 dòng**.
- `verify_span`: **OK 4/4**. Mẩu 03 có `ocr: True`.
- `source_warnings` (hàm kiểm nguồn của `pilot_merge`): không có cảnh báo.

### 7.1 Tôi đã kiểm lại những gì

**1. OCR TT 13/2026**
- Tôi chạy `vnsoc.extract.ocr --key TT13/2026 --pages 18`, sau đó chạy lại không giới hạn trang.
- Cả hai lần đều trả `new_pages: []`, vì sidecar `data/interim/ocr/TT13_2026/` đã có sẵn đủ 19 trang. Sidecar này do một tiến trình khác tạo lúc 11:48–12:01. `meta.json` ghi `pdf_sha256` = `8328ae009d5eae4a…`, trùng với PDF; engine Tesseract 5.4.0, tessdata_best, vie+eng, 300 dpi.
- Tôi tự xem ảnh trang 18 (130 dpi) và trang 3 (110 dpi) trong scratchpad:
  - Điều 26 khoản 1 ghi "…có phòng sinh: tổ chức thực hiện việc tiêm chủng vắc xin viêm gan B trong vòng 24 giờ sau sinh…". Khớp từng chữ với đoạn OCR dùng làm span.
  - Đoạn OCR ngay sau span có lỗi ("sinh pham"). Tôi cắt span trước chỗ đó và **không sửa chữ nào**.
  - Điều 5 khoản 4 (trang 3) ghi lịch tiêm theo "hướng dẫn chuyên môn của Cục Phòng bệnh". Điều 27 (trang 18) ghi hiệu lực 01/7/2026 và điểm d bãi bỏ TT 52/2025. Cả hai đúng như kiểm toán nêu.

**2. TT 13/2026 có chứa lịch tiêm theo tuổi không**
- Tôi dùng `verify_span --find` trên OCR 19 trang.
- "tuổi", "tuôi", "tháng tuổi", "sơ sinh": **không trang nào có**.
- "24 giờ" có ở các trang 6, 7, 9 và 18. Trang 6 nói về theo dõi tại nhà ≥ 24 giờ; trang 7 và 9 nói về báo cáo tai biến. Chỉ trang 18 nói về viêm gan B.
- Kết luận: TT 13/2026 **không chứa giá trị lịch tiêm theo tuổi nào**. Mẩu 01, 02, 04 không thể neo lại vào văn bản này.

**3. Tìm "hướng dẫn chuyên môn của Cục Phòng bệnh"**
- `tiemchungmorong.vn/documents` (WebFetch): văn bản mới nhất vẫn là TT 52/2025. Tin trong nước trên trang chủ kéo tới 30/6/2026, không có lịch mới.
- `vncdc.gov.vn`: WebFetch báo "certificate has expired".
  - Tôi tải trang chủ bằng curl bỏ qua chứng chỉ, chỉ vào scratchpad và không dùng làm dữ liệu.
  - Tiêu đề trang vẫn là "Cục Y tế dự phòng", mục mới nhất là năm 2024 hoặc đầu 2025. Trang này không còn được cập nhật, nên không phải nơi đăng văn bản của Cục Phòng bệnh.
- Một URL đoán trên moh.gov.vn trả 404.
- **WebSearch của phiên đã hết hạn mức (200/200)**, nên tôi không tìm rộng hơn được.
- Kết luận: **chưa tìm thấy, nhưng chưa loại trừ** khả năng văn bản tồn tại.

**4. Nguồn nước ngoài mới** (tải bằng `vnsoc.match.sources fetch`, chỉ lưu giá trị, vị trí và băm)

| Hệ thống | Nguồn | URL | sha256 (16) | Dùng cho |
|---|---|---|---|---|
| US | CDC Child & Adolescent Schedule 2025, **bản gốc 2025** (kho lưu CDC, 17 trang, không có dấu "revised") | https://www.cdc.gov/vaccines/hcp/imz-schedules/downloads/past/2025-child.pdf | `30712f928cd4327e` | MMR trang 10 (12–15 tháng); DTaP trang 7 (15–18 tháng, 4–6 tuổi); VGB trang 8 (mẹ HBsAg âm tính, ≥ 2.000 g: trong 24 giờ). **Trùng giá trị bản sửa 07/02/2025.** |
| EU_UK | UKHSA *Complete routine immunisation schedule from 1 September 2026* (trang HTML, "Updated 24 September 2026") | https://www.gov.uk/government/publications/the-complete-routine-immunisation-schedule/complete-routine-immunisation-schedule-from-1-july-2026 | `61db065b3d2f0683` | MMRV lúc "One year old"; 6-trong-1 lúc 18 tháng (trẻ sinh từ 01/7/2024); dTaP/IPV lúc "three years four months"; VGB lúc sinh chỉ cho trẻ có mẹ nhiễm |
| EU_UK (phiên bản) | Trang danh mục UKHSA (bản cập nhật 24/9/2026) | https://www.gov.uk/government/publications/the-complete-routine-immunisation-schedule | `9b3aa362b1a18caf` | Chỉ để xác định bản hiện hành |
| US (bối cảnh) | CRS R48982 **bản .2** | https://www.congress.gov/crs_external_products/R/PDF/R48982/R48982.2.pdf | `ceef92164ba5b246` | Vẫn đề ngày 11/6/2026. Nội dung về lệnh đình chỉ giống bản .1 (trang 5 và 27). **Không có thông tin sau 11/6/2026.** |

Tôi cũng grep lại các nguồn cũ:
- CDC bản sửa, trang 14: Tdap "age 11-12 years".
- CDC bản sửa, trang 8: "dose 5 is not necessary if dose 4 was administered at age 4 years or older".
- WHO Table 1, trang 1: "9-15 yrs (td)".
- Tất cả đều đúng như ghi chú trong mẩu.

### 7.2 Bảng mẩu hiện hành

| id | slot | Việt Nam (văn bản, trang PDF) | Nước ngoài (hệ thống: giá trị, phiên bản) | Trạng thái | tol | Mồi | HG1.2 |
|---|---|---|---|---|---|---|---|
| P-immunization-01 | Tuổi tiêm mũi 1 vắc xin có chứa thành phần sởi | 9 tháng (TT 52/2025, tr.7; hết hiệu lực) | US: 12–15 tháng (CDC 2025, bản gốc tr.10 và bản sửa tr.10). **EU_UK: 12 tháng (UKHSA 9/2026)**. WHO: 9 tháng (Table 1 12/2025 tr.8; PP 2017) | conflict (US + EU_UK) | 1,5 | 3–6 tháng (mirror_arith) | **chặn** |
| P-immunization-02 | Tuổi mũi nhắc lại lần 2 vắc xin có chứa thành phần bạch hầu (sau mũi nhắc lại lúc 18 tháng) | 7 tuổi (TT 52/2025, tr.3; hết hiệu lực) | US: 4–6 tuổi (CDC 2025, bản gốc tr.7 và bản sửa tr.8). **EU_UK: 40 tháng = 3 tuổi 4 tháng (UKHSA 9/2026)**. WHO: 4–7 tuổi | conflict (US + EU_UK) | 0,5 | 8–10 tuổi (mirror_arith) | **chặn** |
| P-immunization-03 | Thời hạn tối đa tiêm liều sơ sinh VGB (mẹ HBsAg âm tính, ≥ 2.000 g, sinh tại cơ sở có phòng sinh) | ≤ 24 giờ (**TT 13/2026, tr.18, OCR, đang hiệu lực**) | US: ≤ 24 giờ (CDC 2025, bản gốc tr.8 và bản sửa tr.9). WHO: ≤ 24 giờ (tr.5). EU_UK: không có liều sơ sinh thường quy cho quần thể này, nên không có giá trị tương ứng | concordant | 0 | — | chỉ cần kiểm OCR |
| P-immunization-04 | Tuổi mũi nhắc lại đầu tiên (mũi 4) vắc xin có thành phần ho gà | 18 tháng (TT 52/2025, tr.3; hết hiệu lực) | US: 15–18 tháng. WHO: 12–23 tháng. **EU_UK: 18 tháng (trẻ sinh từ 01/7/2024)** | concordant | 0 | — | **chặn** |

`conflict_family`: `measles_mcv1_age` (đổi từ `…_us`), `dtp_booster2_age` (đổi từ `…_us`), `hepb_birth_dose_timing`, `dtp_booster1_age`.

### 7.3 Đã sửa gì, giữ gì và vì sao

**P-immunization-03 (sửa trọn)**
- **Đã sửa theo kiểm toán:**
  - `guideline` → `TT13/2026`; `page` → 18.
  - `section` → "Điều 26 khoản 1…".
  - `span` → đoạn OCR nguyên văn (có kiểm ảnh trang); `vn.text` → "trong vòng 24 giờ sau sinh".
  - `valid_from` → 2026-07-01; `valid_to` → null.
  - `extraction.ocr` → true, kèm `ocr_check`; `printed_page` → "18".
  - `population.setting` → "trẻ sinh tại cơ sở khám bệnh, chữa bệnh có phòng sinh".
  - Ghi chú rằng giới hạn "mẹ HBsAg âm tính" và "≥ 2.000 g" lấy theo CDC.
  - `intervention` bỏ chữ "đơn giá", vì TT 13 chỉ ghi "vắc xin viêm gan B".
- **Đã xóa** tuyên bố "phúc thẩm 6/10/2026". Thay bằng câu có nguồn: kháng cáo ngày 29/4/2026 (CRS trang 5), tình trạng sau 11/6/2026 chưa kiểm, bắt buộc kiểm trước 15/10/2026.
- TT 52/2025 (trang 1) và TT 10/2024 được ghi vào `extraction.prior_versions_same_value`, **không** ghi vào `superseded`. Lý do: cùng giá trị nên không phải lệch phiên bản, và đưa vào `superseded` sẽ làm sai phân tích phiên bản.
- **Thêm:** US bản CDC 2025 gốc; ghi chú EU_UK không có giá trị tương ứng.

**P-immunization-01**
- **Đã sửa:**
  - `intervention` → "vắc xin có chứa thành phần sởi – mũi 1 (MCV1), tiêm chủng thường xuyên". Ghi chú: câu hỏi không nêu loại vắc xin.
  - Nhãn CDC sửa đúng như kiểm toán.
  - **Thêm EU_UK: 12 tháng.** Vì vậy đổi `conflict_family` thành `measles_mcv1_age` (kiểm toán điểm 4).
- **Giữ:**
  - Span, giá trị, `valid_to` 2026-06-30 (trung thực).
  - Mồi 3–6 tháng theo quy tắc đăng ký trước. Tôi chạy lại: mirror_geom 4,5–7,5 và mirror_far ≤ 0 đều không sạch hơn.
- **Phát hiện mới:** US 12–15 và EU_UK 12 cách giá trị Việt Nam đúng bằng nhau (3 tháng). Khi đó `mirror_decoy` chọn nguồn nào **đứng trước trong danh sách**, ở đây là US. Nếu đặt UK trước, mồi sẽ là 6 tháng. Đề xuất ở mục 7.6.

**P-immunization-02**
- **Đã sửa:**
  - `intervention` → "vắc xin có chứa thành phần bạch hầu – mũi nhắc lại lần 2 (sau mũi nhắc lại lúc 18 tháng)".
  - Ghi ràng buộc: câu hỏi không nêu dạng bào chế.
  - Nhãn CDC.
  - **Thêm EU_UK: 40 tháng.** Giá trị này suy ra từ chữ "three years four months". Số "40" không có nguyên văn trong nguồn. Kiểm tra token của `source_warnings` vẫn qua, nhưng chỉ do **trùng ngẫu nhiên** với "40/100,000" ở dòng BCG.
- Giá trị EU_UK nằm ngoài khoảng WHO 4–7, nên phần quy nguồn theo hệ thống **tách được một phần**:
  - "40 tháng" được chấm là EU_UK.
  - "4–6 tuổi" vẫn bị chấm [US, WHO_global].
- **Giữ:** mồi 8–10 tuổi theo quy tắc, và ghi rõ giới hạn chồng lên mũi Td 9–15 tuổi của WHO.

**P-immunization-04**
- **Giữ span dòng ho gà (593 ký tự). Sửa `intervention` → "mũi nhắc lại (mũi thứ 4, sau 3 mũi cơ bản)".** Đây là phương án 2 của kiểm toán.
- **Không theo phương án 1** (span ngắn ở dòng uốn ván trang 4), vì hai lý do:
  - Chuỗi "Trẻ em - Tiêm nhắc lại lần 1 khi trẻ đủ 18 tháng tuổi." không chứa tên vắc xin hay bệnh, nên thiếu ngữ cảnh quần thể theo quy tắc span.
  - Span đủ ngữ cảnh ở dòng bạch hầu (trang 2) dài 626 ký tự, ở dòng uốn ván (trang 4) dài 625 ký tự, đều vượt 600.
- **Thêm EU_UK: 18 tháng.** Mẩu nay là đối chứng với cả 3 hệ.

**Chỗ tôi khác kiểm toán**
- Kiểm toán ghi "1 ngày" (mẩu 03) bị chấm `unit_mismatch` (nhãn 5). Tôi chạy thử thì ra **nhãn 6 (abstain), `parsed=[]`**. Bộ tách không đọc được "ngày" với mẩu tính bằng giờ, nên lỗi nặng hơn kiểm toán nêu. Xem đề xuất ở mục 7.6.
- Kiểm toán đề nghị giữ bản CDC sửa 07/02/2025 và chỉ sửa nhãn. Tôi **ghi thêm bản CDC 2025 gốc** vì hai lý do:
  - Lệnh tòa đưa lịch về "version as of May 2025", có thể là bản trước lần sửa 07/02/2025.
  - Lệnh tòa cũng đình chỉ các phiếu ACIP năm 2025 (CRS trang 5).
  - Hai bản có cùng giá trị cho cả 4 slot, nên kết luận không đổi.

### 7.4 Chấm thử (`grade_short`, sau khi sửa)

- **01:**
  - "9 tháng" → nhãn 2.
  - "12 tháng" / "1 tuổi" → nhãn 4 [EU_UK, US].
  - "12–15 tháng" → nhãn 4 [US].
  - "6 tháng" / "3–6 tháng" → nhãn 5, `decoy_match`.
- **02:**
  - "7 tuổi" → nhãn 2.
  - "4–6 tuổi" / "5 years" → nhãn 4 [US, WHO_global].
  - "40 tháng" → nhãn 4 [EU_UK].
  - "9 tuổi" → nhãn 5, `decoy_match`.
  - **"3 tuổi 4 tháng" → `needs_llm`** (bộ tách ra 2 giá trị: 3 năm và 0,33 năm).
- **03:**
  - "trong vòng 24 giờ" / "24 giờ" → nhãn 2.
  - "12 giờ" / "48 giờ" → nhãn 5.
  - **"1 ngày" → nhãn 6 (abstain, không tách được)**.
- **04:**
  - "18 tháng" → nhãn 2.
  - "15–18 tháng" → nhãn 4 [US, WHO_global].
  - "12 tháng" → nhãn 4 [WHO_global].

### 7.5 Tồn đọng cho HG1.2 (xếp theo mức ưu tiên)

1. **(Chặn mẩu 01, 02, 04) Văn bản lịch TCMR hiện hành.** Người dùng cần chọn một trong ba hướng:
   - **(a)** Lấy "hướng dẫn chuyên môn của Cục Phòng bệnh" về lịch tiêm (TT 13/2026 Điều 5 khoản 4): hỏi Cục Phòng bệnh hoặc Viện VSDT TƯ, hoặc tìm trang web mới của Cục, vì vncdc.gov.vn đã ngừng cập nhật và hết chứng chỉ.
   - **(b)** Quyết định dùng TT 52/2025 như "lịch Bộ Y tế công bố gần nhất". Khi đó ghi vào `docs/DECISIONS.md` và nêu giới hạn trong bài.
   - **(c)** Bỏ ba mẩu này. Chủ đề chỉ còn mẩu 03 (đối chứng) và mất 2 mẩu xung đột.
   - Tôi, như kiểm toán, không khuyến nghị (b) khi chưa thử (a).
2. **Trước 15/10/2026: kiểm tình trạng vụ AAP v. Kennedy ở Tòa phúc thẩm Khu vực 1.**
   - Nếu lịch CDC 2026 có hiệu lực, mẩu 03 có thể thành **xung đột với Mỹ**, và nhãn US ở cả 4 mẩu phải đổi.
   - Tuyên bố của báo cáo gốc rằng "bản 2026 không đổi giá trị với sởi và DTaP" **chưa được kiểm bằng nguồn đã băm**, vì tôi chưa tải được bản CDC 2026.
3. **Kiểm OCR bằng mắt (đề cương §3.1):** TT 13/2026 trang 18 (span mẩu 03, và Điều 27 điểm d dùng làm bằng chứng chặn) và trang 3 (Điều 5 khoản 4).
4. **Duyệt nguồn:** thêm `tiemchungmorong.vn`, `chinhphu.vn`, `cdnchinhphu.vn` vào `official_hosts`, như đã đề xuất ở mục 5.2.
5. **Mồi nhiễm khuyến cáo lân cận:** mẩu 01 chạm 6 tháng; mẩu 02 chồng mũi Td 9–15 tuổi. Nên chấp nhận như một giới hạn (thiên về bảo thủ cho H1), không sửa quy tắc sau khi đã đăng ký.
6. **Mẩu 03, quần thể:**
   - Giới hạn HBsAg và cân nặng lấy theo CDC.
   - Cần kiểm hướng dẫn khám sàng lọc trước tiêm chủng của Bộ Y tế cho trẻ < 2.000 g trước khi đóng băng.
   - Câu hỏi phải nêu đủ: mẹ HBsAg âm tính, ≥ 2.000 g, ổn định, sinh tại cơ sở có phòng sinh; hỏi **thời hạn tối đa tính bằng giờ**.
7. **Hạn mức OCR:**
   - Hiện đã có sidecar OCR cho **8/10** văn bản: 1327_2014, 1470_2024, 292_2024, 3377_2023, 4121_2009, 6101_2019, TT13_2026, TT51_2017.
   - Không nên OCR TT 10/2024, vì nó cùng giá trị với TT 52/2025 và không cần cho `superseded`.
8. **Ứng viên mẩu mới neo vào TT 13/2026 (chưa làm vì ngoài phạm vi sửa lỗi):**
   - Điều 12 (trang 6) ghi "theo dõi đối tượng tiêm chủng tại điểm tiêm chủng ít nhất 30 phút", và theo dõi tại nhà ít nhất 24 giờ.
   - Đây là giá trị Việt Nam **đang hiệu lực** của chủ đề. Để tạo mẩu cần tải nguồn nước ngoài tương ứng; tôi không nêu giá trị nước ngoài vì chưa tải nguồn.
9. **Ràng buộc câu hỏi (cập nhật):**
   - 01: không nêu loại vắc xin; nêu tiêm thường xuyên, không du lịch, không có dịch.
   - 02: không nêu dạng bào chế; hỏi tuổi mũi nhắc lần 2 sau mũi 18 tháng, đúng lịch.
   - 03: như điểm 6.
   - 04: mũi nhắc đầu tiên sau đủ 3 mũi cơ bản.

### 7.6 Đề xuất mã và config bổ sung (chưa sửa, theo quy tắc 4)

1. **`normalize_vi` / `grade`:**
   - "1 ngày" với mẩu đơn vị `h` hiện **không tách được giá trị nào** (nhãn 6). Cần thêm cạnh quy đổi `("day","h"): 24` và bảo đảm "ngày" được nhận là đơn vị.
   - Tuổi ghép "3 tuổi 4 tháng" cần gộp thành một giá trị (40 tháng).
   - Kèm test cho cả hai.
2. **`pilot_merge`:** hiện gộp mẩu mà không xét `valid_to` hay `extraction.hg_block`. Nên loại hoặc gắn cờ các mẩu có `valid_to` < ngày đóng băng, hoặc có `hg_block`, rồi liệt kê trong checklist HG1.2.
3. **`decoys.mirror_decoy`:** cần quy tắc phá hòa cố định khi hai nguồn xung đột cách giá trị Việt Nam bằng nhau (ví dụ theo thứ tự hệ cố định, hoặc chọn khoảng rộng nhất), để mồi không phụ thuộc thứ tự ghi `foreign`. Việc này phải đăng ký trước khi có đầu ra mô hình.
4. **`pilot_merge.source_warnings`:** cho phép đánh dấu giá trị suy ra (ví dụ `derived: "3 years 4 months = 40 months"`), để việc kiểm token không qua nhờ trùng ngẫu nhiên.

### 7.7 File đã ghi hoặc chạm tới

- **Tôi ghi:** `data/interim/pilot/immunization.jsonl` và `data/interim/pilot/immunization_report.md`.
- **Công cụ dự án tự ghi:**
  - `vnsoc.extract.ocr` chạy nhưng không tạo trang mới (`new_pages: []`); chỉ ghi lại `meta.json`.
  - `vnsoc.match.sources` thêm 4 bản đệm vào `data/cache/foreign/`: CDC 2025 gốc, UKHSA HTML, trang danh mục UKHSA, CRS R48982.2.
- **Ảnh trang và trang vncdc.gov.vn:** chỉ lưu trong scratchpad của phiên.
