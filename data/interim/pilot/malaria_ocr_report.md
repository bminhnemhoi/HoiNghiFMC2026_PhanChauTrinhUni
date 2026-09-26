# T1.1 thí điểm — Sốt rét từ OCR của QĐ 3377/2023 (ID = malaria_ocr) — báo cáo agent

Ngày: 2026-09-26 · agent: claude (atom-extractor + counterpart-matcher) · file mẩu: `data/interim/pilot/malaria_ocr.jsonl`
Tiếp nối: `malaria_report.md` (lượt trước, 0 mẩu vì 3377/2023 là bản quét) và `malaria_verify.md` (kiểm toán độc lập).

## Tóm tắt (đọc trước)

> **Sau kiểm toán (2026-09-26):** xem **mục 8**. Kết luận "không có nguồn DR8" ở §3.6 là **sai**. 315/2015 tr. 75 và
> 3312/2015 tr. 520–522 là nguồn DR8 thật; đã ghi vào mẩu 01 và 07. Trạng thái 8 mẩu không đổi (5 conflict, 2
> indistinguishable, 1 concordant), nhưng mồi của mẩu 04 vẫn hỏng nên 04 chưa dùng được cho phép so mồi của H1.

- **8 mẩu đã ghi.** Cả 8 đều từ trang OCR của 3377/2023 (`extraction.ocr = true`) và qua các kiểm tra máy:
  - `vnsoc.schemas atom`: **OK 8/8**;
  - `verify_span`: **OK 8/8**, cả 8 báo `ocr=True`;
  - mô phỏng `pilot_merge.check` + `enforce_decoy_rule` + `source_warnings`: 0 lỗi, 0 cảnh báo nguồn, mồi và trạng thái không đổi khi gộp.
- **Trạng thái** (tính bằng `finalize`):
  - **5 conflict**: 01 (hạt giống 17), 03 (18), 04 (19, liều/ngày), 06 (mới: số ngày dùng AL), 07 (mới: artesunat cho trẻ < 20 kg);
  - **2 indistinguishable**: 02 (hạt giống 16), 05 (19, thời gian);
  - **1 concordant**: 08 (đối chứng artesunat người lớn).
- **Lệch phiên bản** 2699/2020 → 3377/2023: 3 mẩu có giá trị bản cũ khác VN (02, 04, 05). Chỉ **04** vừa phân biệt được vừa là
  mẩu xung đột (0,25 mg/kg/ngày × 14 ngày → 0,5 mg/kg/ngày × 7 ngày). 02 và 05 thành indistinguishable.
- **Đã có CDC kèm sha256.** Trang HTML CDC trả 403 với script. Nhưng trang đó dẫn tới bản PDF chính thức
  `Malaria-Treatment-Tables-8-11-26.pdf`, và `vnsoc.match.sources fetch` tải được bản này (sha `7893052505772ec3`). Nhờ vậy mọi
  giá trị US ở lượt trước (chỉ đọc bằng WebFetch) nay có nguồn đã băm.
- **Đã có WHO 2015 (3rd ed.)**, bản văn bản do IRIS phát hành (sha `f1bab2b81e7429c3`). Dùng để ghi các phiên bản WHO cũ khi giá
  trị khác bản hiện hành.
- **Hai lỗi mã ảnh hưởng trực tiếp tới dữ liệu này** (mục 7): lỗi nhãn 5 khi một hệ thống vừa có bản trùng VN vừa có bản xung đột
  (mẩu thuốc), và mồi của mẩu 04 nằm sát giá trị bản cũ. **Chưa có mẩu nào được người kiểm.**
  Mọi con số trên trang OCR phải được người so với ảnh trang ở HG1.2.

---

## 1. Văn bản đã dùng

| Khóa | Vai trò | Tệp | sha256 (16) | Lớp chữ | Ghi chú |
|---|---|---|---|---|---|
| 3377/2023 | hiện hành | `data/raw/3377_2023.pdf` (23 tr.) | `aa1792688e9dda03` | **OCR**: sidecar `data/interim/ocr/3377_2023/` (tesseract 5.4.0, vie+eng, 300 dpi, `pdf_sha256` khớp) | Bản sao y của Sở Y tế Thanh Hóa, do BVĐK Hà Trung đăng lại (xem `malaria_report.md` §1) |
| 2699/2020 | bản cũ (bị 3377/2023 thay thế, Điều 1) | `data/raw/2699_2020.pdf` (30 tr.) | `8bc1a6b403476197` | lớp chữ (ký số VGCA) | Span bản cũ chép từ `--page` |
| 5642/2015 | kiểm DR8 | `data/raw/5642_2015.pdf` | `541e140fccfa3269` | lớp chữ | Chương "Bệnh sốt rét kháng thuốc" (tr. 33–37) chỉ nói điều trị **thất bại/kháng thuốc**: second line quinin + doxycyclin/clindamycin. Khác quần thể với 8 mẩu, nên **không có nguồn DR8** |

Nguồn nước ngoài (chỉ lưu giá trị, vị trí và băm; không lưu đoạn văn):

| Nguồn | URL | Ngày phiên bản | fetched_at | page_sha256 (16) |
|---|---|---|---|---|
| WHO guidelines for malaria (MAGICapp PDF, 494 tr.) | `https://iris.who.int/server/api/core/bitstreams/d3c6488b-3ee6-41cb-960f-ddf0202cd74d/content` | 2026-09-10 | 2026-09-26 | `4e2c67b2ec74124e` |
| WHO Guidelines for the treatment of malaria, 3rd ed. (bản văn bản IRIS) | `https://iris.who.int/server/api/core/bitstreams/999277b9-4aa3-4609-960f-b39d7283587b/content` | 2015 | 2026-09-26 | `f1bab2b81e7429c3` |
| CDC Malaria in the United States: Treatment Tables (PDF, 7 tr.) | `https://www.cdc.gov/malaria/media/pdfs/2026/06/Malaria-Treatment-Tables-8-11-26.pdf` | Table 1, 5: 2026-08-11 · Table 2–4: 2026-06-26 (ghi ở đầu từng trang) | 2026-09-26 | `7893052505772ec3` |

Ghi chú nguồn:

- **WHO 2015.** Trang item IRIS (`https://iris.who.int/handle/10665/162441`, sha `ed0fa8bb8e0dfca3`) xác nhận đây là "Guidelines for
  the treatment of malaria, 3rd ed.". Bitstream PDF (2,42 MB) tải quá 120 giây nên bị ngắt. Tôi dùng bitstream văn bản do IRIS
  trích ra. Bản này **không có số trang PDF**, nên locator ghi theo chương/phụ lục.
- **CDC.** URL PDF lấy từ liên kết trên trang HTML Appendix A (đọc bằng WebFetch). Trang HTML ghi "Updated August 17, 2026",
  còn các trang PDF ghi "Last Updated" 26/6/2026 và 11/8/2026.

---

## 2. Bảng mẩu

Số trang = trang PDF, đếm từ 1. Mọi span chép nguyên văn từ `verify_span --page` (giữ lỗi OCR). Ảnh trang nằm ở
`data/cache/page_images/3377_2023_pNNN.png`.

| id | Hạt giống | Slot · kiểu | VN (3377/2023) | Nước ngoài | Bản cũ 2699/2020 | Mồi | Trạng thái | Trang (in) | Kiểm ảnh (agent) |
|---|---|---|---|---|---|---|---|---|---|
| 01 | 17 | first_line · drugs — P. falciparum chưa biến chứng, **thai 3 tháng đầu**, lựa chọn đầu tiên | quinin sulfat 7 ngày + clindamycin 7 ngày | WHO 2026 (khuyến cáo 2022, mạnh): **AL** · US CDC Table 4: **AL (ưu tiên)** | trùng (Q+C, tr. 7), không ghi | pyronaridin–artesunat (agent đề xuất; check_decoy = []) | **conflict** (WHO + US) | 10 (9) | khớp ảnh tr. 10, không sai khác |
| 02 | 16 | first_line · drugs — P. falciparum chưa biến chứng, không có thai, ACT đầu tiên | pyronaridin–artesunat (Pyramax) 3 ngày + primaquin liều đơn | US CDC Table 1: AL (A), atovaquon–proguanil (B) · WHO 2026: 6 ACT ngang hàng (AL, AS+AQ, AS-MQ, **DHA-PPQ**, AS+SP, **AS-PY**) | **DHA-PPQ** 3 ngày + primaquin (tr. 6) | — | **indistinguishable** | 9 (8) | khớp số/tên thuốc; lỗi chữ không phải số ("Jalciparum", "uông 3 ngay", "Bang", "hoic") |
| 03 | 18 | dose · num (mg) — primaquin liều đơn cho P. falciparum, ≥ 15 tuổi, 60 kg | 4 viên × 7,5 mg base = **30 mg** | WHO 2026 (cập nhật 2026, mạnh, vùng lan truyền thấp): **0,25 mg/kg** (= 15 mg) · WHO trước 2015: 0,75 mg/kg (= 45 mg) | trùng (0,5 mg base/kg; ≥ 15 tuổi 4 viên), không ghi | 60 mg (mirror_geom; arith 45 mg bị loại vì trùng WHO cũ) | **conflict** (WHO) | 16 (PL tr. 2) | khớp ảnh; OCR đọc "≥ 15 tuổi" thành "> 15 tuổi" |
| 04 | 19 | dose · num (mg/kg/day) — P. vivax/ovale, G6PD không thiếu (đã xét nghiệm), người lớn 60 kg | **0,5 mg/kg/ngày** (× 7 ngày) | WHO 2026 (khuyến cáo 2024, mạnh): **1 mg/kg/ngày × 7** hoặc 0,5 × 14 · US CDC Table 2: 30 mg/ngày × 14 (= 0,5 mg/kg/ngày ở 60 kg) · WHO 2015: 0,25–0,5 × 14 | **0,25 mg base/kg/ngày × 14** (tr. 15) | 0,2 mg/kg/day (mirror_geom) ⚠ | **conflict** (WHO) + lệch phiên bản | 17 (PL tr. 3) | khớp ảnh, không sai khác |
| 05 | 19 | duration · num (day) — cùng quần thể 04 | **7 ngày** | WHO 2026: 14 hoặc 7 · US CDC: 14 · WHO 2015: 14 | **14 ngày** (tr. 15) | — | **indistinguishable** | 17 (PL tr. 3) | khớp ảnh |
| 06 | mới | duration · num (day) — AL cho P. falciparum chưa biến chứng, người lớn | **3 ngày** (2 lần/ngày) | **US CDC Table 1: 5 ngày** · WHO 2026 (khuyến cáo 2015): 3 ngày | không có AL | 1 day (mirror_arith) | **conflict** (US) | 19 (PL tr. 5) | khớp ảnh; "–" thành "—", "giờ" thành "gio" |
| 07 | mới (đối chứng cũ xếp sai) | dose · num (mg/kg) — artesunat tiêm, sốt rét ác tính, **trẻ < 20 kg** | **3 mg/kg/lần** | WHO 2026 (khuyến cáo 2015): 3 mg/kg · **US CDC Table 5: 2,4 mg/kg** (chú thích 2 nói rõ khác WHO) | trùng (3 mg/kg, tr. 8), không ghi | 3,6 mg/kg (mirror_arith) | **conflict** (US) | 11 (10) | khớp ảnh, không sai khác |
| 08 | đối chứng "artesunat cho sốt rét ác tính" | dose · num (mg/kg) — artesunat tiêm, người lớn 60 kg | **2,4 mg/kg** (giờ 0, giờ 12, rồi mỗi ngày) | WHO 2026: 2,4 · US CDC Table 5: 2,4 | trùng (tr. 8), không ghi | — | **concordant** | 11 (10) | khớp ảnh; "giờ đầu" thành "gio đầu" |

Tổng: 5 conflict, 2 indistinguishable, 1 concordant.

Theo hệ thống, 5 mẩu conflict chia như sau:

- chỉ WHO_global: 03, 04;
- chỉ US: 06, 07;
- cả hai: 01.

Mẩu 06 và 07 là **phát hiện mới**, không có trong bộ hạt giống.

Kiểm bằng bộ chấm (`vnsoc.grade.grade_short`, chạy thử trong bộ nhớ, không ghi file):

| Mẩu | Câu trả lời | Nhãn |
|---|---|---|
| 01 | "quinin sulfat + clindamycin" | 2 |
| 01 | "artemether-lumefantrin" | 4 [US, WHO_global] |
| 01 | "Pyramax" | 5 (decoy_match) |
| 02 | "dihydroartemisinin-piperaquin" | 3 (kèm WHO_global) → minh họa vì sao indistinguishable |
| 03 | "30 mg", "4 viên", "0,5 mg/kg" | 2 |
| 03 | "0,25 mg/kg", "15 mg" | 4 |
| 04 | "0,5 mg/kg/ngày" | 2 |
| 04 | "1 mg/kg/ngày" | 4 |
| 04 | "0,25 mg/kg/ngày" | 3 **và decoy_match = True** (xem mục 7.2) |
| 04 | "30 mg/ngày" | 5 (không quy đổi được, xem mục 7.3) |

---

## 3. Quyết định định nghĩa mẩu (cần người/bác sĩ xác nhận)

1. **01 — "lựa chọn đầu tiên" (slot first_line).**
   - Bảng 3377/2023 tr. 10 ghi quinin sulfat 7 ngày + clindamycin 7 ngày. Câu tiếp theo: "Trường hợp không có quinin sulfat, có thể
     dùng artemether - lumefantrin". Vì vậy AL là lựa chọn thay thế có điều kiện và **không** được tính vào `vn`.
   - Để đối xứng, phía nước ngoài cũng chỉ ghi lựa chọn ưu tiên. CDC Table 4 còn liệt kê quinin + clindamycin và mefloquin (khi
     không còn lựa chọn khác), nhưng chúng không phải lựa chọn ưu tiên.
   - **Độ nhạy:** nếu tính AL vào tập VN thì mẩu thành concordant. Kết quả xung đột phụ thuộc hoàn toàn vào việc câu hỏi nói rõ
     "lựa chọn đầu tiên / ưu tiên, khi có đủ thuốc".
2. **04 — không cố định thời gian trong slot liều/ngày**, theo khuyến nghị kiểm toán. Nếu hỏi "liệu trình 7 ngày" thì bản cũ
   (chỉ có 14 ngày) và CDC (14 ngày) không còn cùng slot.
   - Xung đột thật của mẩu này là với WHO 2024+ (1 mg/kg/ngày × 7; tổng liều cao 7 mg/kg). WHO ghi lợi ích của liều cao lớn hơn ở
     Đông Nam Á.
   - CDC không xung đột: 30 mg/ngày ≈ 0,5 mg/kg/ngày ở 60 kg.
   - Tafenoquin **không** phải xung đột: 3377/2023 tr. 9 cho dùng "Tafenoquine liều duy nhất (sử dụng sau khi được Bộ Y tế cấp
     phép lưu hành...)".
3. **03 — phụ thuộc cân nặng.** VN cho liều theo tuổi (4 viên, không kể cân nặng); WHO cho liều theo mg/kg. Câu hỏi phải nêu
   60 kg. Nếu cân nặng khác, giá trị WHO quy đổi và mồi cũng đổi theo.
4. **02 — giữ lại dù indistinguishable** để ghi kết quả thật của hạt giống 16. Mồi để trống: mọi mồi đều bị `check_decoy` báo
   "làm mẩu thành indistinguishable".
5. **Không ghi `superseded` khi giá trị bản cũ trùng VN** (01, 03, 07, 08). Span bản cũ vẫn được chép vào `extraction.notes` để
   người kiểm.
6. **DR8:** không có văn bản Bộ Y tế hiện hành thứ hai cho cùng quần thể trong `data/raw`.
   - 5642/2015 chỉ nói sốt rét kháng thuốc/thất bại điều trị.
   - **Chưa kiểm được** hướng dẫn nhi khoa của Bộ Y tế (có thể có chương sốt rét và liều artesunat cho trẻ em). Văn bản này không có
     trong `data/raw`, nên corpus-librarian cần kiểm trước khi đóng băng kho.
   - **[Sau kiểm toán: SAI.]** `data/raw/3312_2015.pdf` (nhi khoa, `current`) đã có trong kho trước khi viết báo cáo này.
     Chương "SỐT RÉT Ở TRẺ EM" nằm ở tr. 517–523. 315/2015 tr. 75 (sản phụ khoa, `current`) cũng có mục xử trí sốt rét
     khi có thai. Kết quả quét lại và cách áp DR8 ở mục 8.

---

## 4. Ứng viên bị loại / không lập + lý do

| Ứng viên | Lý do |
|---|---|
| Tafenoquin 300 mg (CDC) cho P. vivax | 3377/2023 cũng có tafenoquin liều duy nhất, với điều kiện được cấp phép lưu hành → không phải xung đột |
| P. vivax khi **không** xét nghiệm G6PD (VN 0,25 mg/kg/ngày × 14 ngày) | CDC bắt buộc xét nghiệm G6PD định lượng trước khi dùng. WHO chỉ nói cân nhắc lợi/hại → không có giá trị đối chiếu (no_counterpart) |
| Thuốc uống chuyển tiếp sau artesunat tiêm (VN: Pyramax 3 ngày) | 2699/2020 ghi "DHA-PPQ hoặc các ACT khác" (tập bản cũ bao trùm tập hiện hành). WHO: ACT bất kỳ 3 ngày → dự kiến indistinguishable/concordant; không lập |
| Thai > 3 tháng, P. falciparum (VN: AL / AS-MQ / DHA-PPQ / AS-AQ) | Dự kiến concordant: CDC ưu tiên AL, nằm trong tập VN. Chưa grep đủ khuyến cáo WHO cho tam cá nguyệt 2–3 → để lượt sau nếu cần thêm đối chứng thuốc |
| Primaquin liều đơn — đối chiếu US | CDC Table 1 không có primaquin liều đơn diệt giao bào → không ghi US ở mẩu 03 |
| Span Bảng 1 (tr. 15) cho artesunat | OCR đọc "2,4" thành "2 ,4" → **không dùng span này**, dùng span tr. 11 (đúng số) |
| Giá trị Bảng 3 Pyramax (tr. 16) | OCR đọc sai phân số ("1/3" thành "1⁄4", "2/3" thành "2/4") → không lập mẩu từ bảng này |
| Hàng "1½ viên/ngày" Bảng 4 | OCR đọc thành "11⁄2" → span mẩu 03 cố ý bắt đầu ở hàng "≥ 15 tuổi" để tránh ô này |
| WHO 2015 cho mẩu 01 (Q+C 7 ngày, trùng VN) và 02 (5 ACT, chưa có AS-PY) | Đã đọc nhưng **không ghi** vào `foreign`. Ghi vào sẽ làm `grade_short` chấm câu trả lời đúng VN thành nhãn 5 (lỗi 7.1, đã chạy lại). Mẩu 02 đã indistinguishable nên không đổi trạng thái. Đã ghi trong `extraction.notes` |

---

## 5. SAI LỆCH SO VỚI BỘ HẠT GIỐNG (§3.3 / `seed_conflicts.yaml`)

1. **Dòng 16** (`confirmed_us_only`) → thực tế là **indistinguishable**.
   - WHO 2026 không "chấp nhận cả hai" theo nghĩa xếp hạng. WHO liệt kê 6 ACT ngang hàng, trong đó có AS-PY (= VN) và DHA-PPQ.
     DHA-PPQ lại chính là giá trị ưu tiên của bản cũ 2699/2020.
   - 3377/2023 có AL làm thuốc thay thế thứ 2. Vì vậy khác biệt với CDC chủ yếu là **thứ tự ưu tiên**, cùng loại lý do đã khiến
     dòng 12 bị loại.
2. **Dòng 17** (`confirmed`, chỉ ghi CDC): xung đột (lựa chọn đầu tiên) là với **cả WHO_global** (khuyến cáo 2022, còn trong bản
   10/9/2026) **và US**.
   - 3377/2023 thêm AL làm lựa chọn dự phòng khi không có quinin; bảng hạt giống không nhắc chi tiết này.
   - CDC có một tập: AL (ưu tiên), Q+C, mefloquin.
   - WHO 2015 từng khuyến cáo Q+C cho 3 tháng đầu (trùng VN).
3. **Dòng 18** (`fixed`, `pilot: false`): giá trị VN đúng (30 mg). Mẩu lập được, trạng thái **conflict chỉ với WHO**.
   - 3377/2023 không còn ghi mg/kg cho liều đơn; bản 2699 ghi 0,5 mg base/kg.
   - WHO khẳng định lại 0,25 mg/kg trong bản cập nhật 2026.
   - CDC không có đối chiếu.
4. **Dòng 19** (`confirmed`, CDC "30 mg × 14 hoặc tafenoquin"): **mô tả nước ngoài sai.**
   - CDC 30 mg/ngày ≈ 0,5 mg/kg/ngày = VN về liều mỗi ngày.
   - Tafenoquin có trong 3377/2023.
   - Xung đột thật là với **WHO 2024+** (1 mg/kg/ngày × 7 ngày).
   - Tách thời gian (7 so với 14 ngày) → indistinguishable, vì 14 ngày trùng bản cũ.
   - Mẩu liều/ngày là mẩu **lệch phiên bản thật** (0,25 × 14 → 0,5 × 7).
5. **Đối chứng "artesunat cho sốt rét ác tính"**: đúng là trùng ở người lớn/trẻ > 20 kg (mẩu 08). Ở trẻ < 20 kg thì **không
   trùng**: CDC dùng 2,4 mg/kg, VN = WHO = 3 mg/kg (mẩu 07).
   - Báo cáo lượt trước xếp nhầm mục này là đối chứng; kiểm toán đã chỉ ra. Nay xác nhận trên PDF CDC đã băm.
6. **Mới:** CDC 2026 kéo dài AL cho P. falciparum lên **5 ngày**, còn VN và WHO là 3 ngày (mẩu 06).
7. **Ghi chú kho:** bảng hạt giống không nêu rằng 3377/2023 chỉ có bản quét. Toàn bộ mẩu sốt rét phụ thuộc OCR và việc người so ảnh.

---

## 6. Việc cho người ở HG1.2 (mọi mẩu đều từ trang OCR)

1. **So TỪNG con số và tên thuốc trong span với ảnh trang** (`verify_span --image 3377/2023 <trang>` → `data/cache/page_images/`),
   ở các trang 9, 10, 11, 16, 17, 19.
   - Với 03: xác nhận "4 viên" nằm ở **cột "P. falciparum, P. knowlesi, P. malariae điều trị 1 lần"**, hàng **"≥ 15 tuổi"**. Tiêu
     đề cột nằm ngoài span, và OCR đọc "≥" thành ">".
2. **01:** bác sĩ/người dùng quyết định cách đặt vấn đề "lựa chọn đầu tiên" (mục 3.1). Câu hỏi phải nói rõ "thuốc lựa chọn đầu
   tiên khi có đủ thuốc".
3. **CDC:** mở PDF (link ở mục 1) và kiểm các điểm sau:
   - Table 1: AL xếp thứ nhất, liệu trình 5 ngày;
   - Table 4: AL "(preferred)";
   - Table 2: primaquin 30 mg × 14;
   - Table 5: 2,4 mg/kg, và chú thích 2 về trẻ < 20 kg.

   Cũng ghi nhận độ vênh ngày giữa trang HTML (17/8/2026) và PDF (11/8/2026).
4. **WHO:** mở PDF 10/9/2026 và kiểm:
   - p.17: 6 ACT; ACT 3 ngày;
   - p.18: AL cho 3 tháng đầu; primaquin 0,25 mg/kg;
   - p.21: primaquin 7 mg/kg;
   - p.22: artesunat 3 / 2,4 mg/kg.

   Mục "WHO trước 2015" (0,75 mg/kg) ở mẩu 03 dựa trên câu "previously recommended dose" trong bản 2015. `version_date` đang là
   chuỗi "trước 2015", cần quyết định cách ghi.
5. **Tafenoquin đã được cấp phép lưu hành ở Việt Nam chưa?** Chỉ ảnh hưởng tới diễn giải, không ảnh hưởng mẩu liều primaquin.
6. **Danh tính 2699/2020** (file để trống số) và **tính hiện hành của 3377/2023** vẫn chờ người/corpus-librarian xác nhận
   (như `malaria_verify.md` §1).
7. Câu hỏi phải nêu:
   - 03: 60 kg, ≥ 15 tuổi, P. falciparum;
   - 04/05: G6PD đã xét nghiệm, bình thường;
   - 06: P. falciparum, đã chọn AL;
   - 07: trẻ 15 kg;
   - 08: người lớn 60 kg.

---

## 7. Đề xuất sửa mã / config (không tự sửa)

### 7.1 Lỗi chấm nhãn 5 cho câu trả lời đúng VN (`vnsoc.grade.grade_short`, khối "one drug list containing both")

- **Tái hiện.** Lấy mẩu 01 và thêm `foreign` WHO_global 2015 = Q+C (trùng VN). Khi đó
  `grade_short("ĐÁP ÁN: quinin sulfat + clindamycin trong 7 ngày")` cho **nhãn 5 (unattributed)**, vn_match = True.
- **Nguyên nhân.**
  - Danh sách `conflicting` được tính theo **mục foreign** (bản WHO 2026 toàn AL nên bị coi là conflicting).
  - Còn `c["foreign"]` được tính theo **hệ thống**: câu trả lời Q+C khớp WHO_global qua bản 2015.
  - Hai hệ thống giao nhau nên câu trả lời bị coi là "danh sách chứa cả VN lẫn phác đồ nước ngoài".
- **Đề xuất.** Chỉ vào nhánh này khi tập thuốc trả lời chứa `key_drugs` của một **mục** foreign xung đột mà mục đó *không* khớp VN.
  Nói cách khác: kiểm `matches(val, it)` với từng mục có `all(_gap(v, it) > 0 for v in vn)`. Thêm test cho trường hợp "cùng hệ
  thống, bản cũ trùng VN".
- **Hệ quả nếu chưa sửa:** không ghi được phiên bản cũ của nguồn nước ngoài khi bản đó trùng VN (tôi đã phải bỏ WHO 2015 ở 01/02).

### 7.2 Mồi sát nguồn đã ghi (`check_decoy`)

- **Tái hiện ở mẩu 04.** Mồi bắt buộc (mirror_geom) là 0,2, cách bản cũ 0,25 và cận dưới WHO 2015 (0,25) chỉ 0,05, trong khi
  2 × tol = 0,25. Kết quả: `grade_short("0,25 mg/kg/ngày")` cho nhãn 3 **và** decoy_match = True.
- **Hệ quả:** tỷ lệ trùng mồi bị thổi phồng bởi các câu trả lời theo bản cũ.
- **Đề xuất (lặp lại từ lượt trước, chưa sửa):**
  - loại mồi khi `_gap(mồi, nguồn) < 2 × tol`;
  - sau đó thử bước kế tiếp (mirror_far) hoặc để trống.

  Cần ghi quyết định vào `docs/DECISIONS.md` trước khi đóng băng mẩu. `pilot_merge.enforce_decoy_rule` hiện sẽ đặt lại mồi 0,2.

### 7.3 `normalize_vi`

- Thêm cạnh quy đổi `mg/day ↔ mg/kg/day` theo `weight_kg`. Hiện "30 mg/ngày" ở mẩu 04 cho nhãn 5.
- Thêm đơn vị: "mg base/kg/ngày" → mg/kg/day, "mg base/kg" → mg/kg, "mg base" → mg, "mg/kg/lần/tuần" → mg/kg/week, "gói".

### 7.4 `configs/grading.yaml`

- **drugs:** thêm `atovaquone-proguanil` (bí danh malarone, atovaquon-proguanil), `mefloquine` (mefloquin),
  `amodiaquine` (amodiaquin), `doxycycline` (doxycyclin), `sulfadoxine-pyrimethamine` (sp, fansidar).
- **combos:** thêm `artesunate-mefloquine`, `artesunate-amodiaquine`, `artesunate+sulfadoxine-pyrimethamine`,
  `quinine+doxycycline`.
- Mẩu 02 đã ghi các khóa này trong `key_drugs`, nhưng bộ chấm chưa đọc được.
- **[Sau kiểm toán]** `grading.yaml` sửa lúc 11:44 đã có mefloquine, atovaquone-proguanil, doxycycline. Còn thiếu:
  amodiaquine, sulfadoxine-pyrimethamine, và các combo AS-MQ, AS-AQ, AS+SP (mục 8.6).
- Cần test thứ tự gộp combo, vì "artesunate" có trong nhiều combo.

### 7.5 Schema và nguồn

- **`version_date`:** cần quy ước cho khuyến cáo cũ không có ngày chính xác (mẩu 03: "trước 2015").
- **`vnsoc.match.sources.fetch`:** cần timeout dài hơn hoặc tải dạng stream. Bitstream PDF IRIS 2,42 MB không tải xong trong
  120 giây; tôi đã dùng bitstream văn bản thay thế.

### 7.6 Manifest

Nhắc lại từ lượt trước: cần thêm dòng 3377/2023 (`text_layer: false`, `ocr: true`) và 2699/2020 (`superseded_by: [3377/2023]`).

---

## 8. Sau kiểm toán (agent sửa lỗi, 2026-09-26)

- **Đầu vào:** `data/interim/pilot/malaria_ocr_verify.md` (4 pass · 4 fix · 0 reject).
- **Cách làm:** tự kiểm lại từng điểm bằng công cụ trước khi sửa. Không bịa, không điền từ trí nhớ.
- **Chỉ ghi 2 file:** `malaria_ocr.jsonl` và báo cáo này. Script sửa nằm ngoài dự án (scratchpad), chạy thử trong bộ nhớ
  trước khi ghi.

### 8.1. Bằng chứng tự kiểm lại

| Điểm | Cách kiểm | Kết quả |
|---|---|---|
| Quét DR8 toàn kho | `verify_span` trên **52 văn bản `current`** của manifest, tìm 8 từ khóa: sốt rét, artesunat, primaquin, quinin, lumefantrin, chloroquin, plasmodium, falciparum | Chỉ **315/2015 tr. 75** và **3312/2015 tr. 520–522** có giá trị điều trị. 5642/2015 tr. 33–37 chỉ nói điều trị thất bại (second line) → khác quần thể. 3312/2015 tr. 169 chỉ ghi "Sốt rét: Artesunate (tiêm tĩnh mạch)", không có liều. 11 văn bản còn lại chỉ nhắc sốt rét như nguyên nhân, xét nghiệm hoặc tương tác thuốc (5968/2021 tr. 64 là primaquin cho viêm phổi PCP, khác bệnh) |
| Khác với kiểm toán | như trên | Kiểm toán viết 1493/2015 "không có sốt rét". Thực tế có ở tr. 46 ("cơn sốt rét run", triệu chứng) và tr. 101 (nguyên nhân suy gan), nhưng không có giá trị điều trị. Kết luận không đổi |
| 315/2015 tr. 75 (in 74), sha `8038358264cdbc64`, lớp chữ | `--page` và ảnh trang | Mục "2.1.4. Sốt rét", phần "Xử trí" có 3 gạch đầu dòng "+": chloroquin (10 mg/kg × 2 ngày, rồi 5 mg/kg ngày 3); sulfadoxin/pyrimethamin 3 viên liều duy nhất; muối quinine 10 mg/kg × 3 lần/ngày × 7 ngày. Áp cho **mọi** phụ nữ có thai bị sốt rét: không phân tam cá nguyệt, loài hay mức độ, không xếp thứ tự |
| 3312/2015 tr. 520, sha `a66c5e8bc460807c`, lớp chữ | ảnh trang | Bảng 1 ghi rõ "theo ... QĐ 3232/QĐ-BYT ngày 30/8/2013". Hàng "Phụ nữ có thai trong 3 tháng", cột P. falciparum = **Quinin + Clindamycin** (trùng 3377). Hàng "Từ 3 tuổi trở lên", cột P. falciparum = DHA-PPQ + Primaquin |
| 3312/2015 tr. 521 | ảnh trang | Mỗi thuốc trình bày theo mẫu "tên, rồi liều". Dòng "Trẻ em < 7 tuổi: 1,5 mg/kg/ngày, 7 ngày" là một dòng thụt lề riêng, **ngay dưới** đoạn "Artesunat tiêm tĩnh mạch hoặc tiêm bắp, lọ 60mg..." và trước mục Chloroquine → đọc theo vị trí là liều artesunat tiêm. Văn bản không ghi số lần/ngày, không có liều nạp, không có liều cho trẻ ≥ 7 tuổi. Cùng trang có dòng liều DHA-PPQ "Người lớn > 15 tuổi" |
| 3312/2015 tr. 522 | `--page` | Primaquin "Liều 0,6 mg base / kg / ngày": diệt giao bào P. falciparum thì uống 1 ngày cuối đợt; P. vivax/ovale thì dùng 14 ngày; không dùng cho trẻ < 4 tuổi |
| Mồi mẩu 04 | tự tính bằng `mirror_decoy` | mirror_arith = 2·0,5 − 1,0 = 0 (≤ 0) → mirror_geom = 0,5²/1,0 = **0,25, đúng bằng giá trị bản cũ 2699/2020**. Làm tròn 1 chữ số (round-half-even) cho ra 0,2. Vì vậy `check_decoy` (chỉ loại khi gap = 0) không bắt được. Chính câu trả lời "0,2" bị chấm nhãn 3 kèm `decoy_match` |
| `decoys.py` đổi trong phiên | `ls --full-time` | `src/vnsoc/match/decoys.py` và `tests/test_decoys.py` bị một tiến trình khác sửa lúc **12:20**, sau khi tôi đọc lúc 12:11. Bản mới chỉ báo "mồi làm mẩu thành indistinguishable" khi **chính mồi** gây ra. **Chưa** có quy tắc loại mồi cách nguồn < 2·tol. Hệ quả: 04 vẫn nhận mồi 0,2; mẩu 05 nay nhận mồi 3,5 ngày theo quy tắc bắt buộc |
| WHO 2nd ed. (2010) cho mẩu 03 và 07 | IRIS | **Không tải được.** API tìm kiếm của IRIS trả 403. Trang tìm kiếm dựng bằng JS. Hai handle thử là tài liệu khác (10665/44236 = sổ tay cảnh giác dược ARV; 10665/44653 = phương pháp đo phơi nhiễm thuốc sốt rét) nên không dùng. Liên kết whqlibdoc chuyển sang extranet. Trang khuyến cáo primaquin 2012 (URL do WHO 2015 trích) trả 404. Trong nguồn đã băm chỉ kiểm được hai điều: WHO 2015 gọi 0,75 mg/kg là "previously recommended dose", và trích "Single dose primaquine ... updated WHO policy recommendation. Geneva: WHO; 2012" |

### 8.2. Đã sửa gì

| Mẩu | Kiểm toán | Đã làm | Trạng thái (finalize) |
|---|---|---|---|
| 01 | fix | Thêm `dr8_sources` = [315/2015 tr. 75; 3312/2015 tr. 520]. Mỗi dòng có span nguyên văn từ `--page`, `values_text` và `merged_into_vn`. **Áp DR8:** `vn` += {chloroquine}, {quinine}, nên vn = {Q+C, chloroquin, quinin}. **Sulfadoxin–pyrimethamin chưa hợp** vì `grading.yaml` chưa có thuốc này: `verify_span` và bộ chấm không đọc được (mục 8.6). Ghi thêm vào `decoy_rule` rằng nguồn DR8 cũng không nêu Pyramax. Thêm notes | **conflict** (không đổi; AL nằm ngoài tập hợp) |
| 02 | pass | Chỉ sửa ghi chú: thêm kết quả quét DR8 (hàng "Từ 3 tuổi trở lên" của 3312 coi là ngoài quần thể người lớn). `decoy_rule` cũ viện dẫn báo động giả của `check_decoy`, đã lỗi thời sau bản sửa 12:20, nên viết lại. Vẫn không có mồi | indistinguishable |
| 03 | fix | `population.age` → "người lớn ≥ 18 tuổi (câu hỏi dùng người 30 tuổi, 60 kg)" để 3312/2015 (nhi, 0,6 mg base/kg) nằm ngoài quần thể. Mục WHO cũ: `version_date` "trước 2015" → **"chưa rõ (trước 2012)"**; `source`/`locator` ghi rõ chỉ mốc 2012 là kiểm được. Giữ mục này vì bỏ đi thì mồi thành 45 mg, trùng khuyến cáo cũ có thật của WHO | **conflict** (tol 7,5; mồi 60 mg) |
| 04 | fix | **Giữ mồi 0,2**: quy tắc bắt buộc `choose_decoy`, và `enforce_decoy_rule` cũng sẽ đặt lại 0,2. Ghi chẩn đoán vào notes: 0,25 đúng bằng bản cũ trước khi làm tròn. Ghi rõ 04 **chưa dùng được cho phép so trùng nước ngoài/trùng mồi (H1)** tới khi sửa `check_decoy`; khi đó mồi → None và `decoy = []`. Thêm notes DR8 (3312 tr. 522 là nhi, ngoài quần thể) | **conflict** (tol 0,125) — ⚠ mồi hỏng |
| 05 | pass | Mồi `[]` → **[3,5 ngày]** (mirror_geom = 7²/14) để khớp `decoys.py` bản 12:20; `enforce_decoy_rule` khi gộp cũng làm vậy. Không nguồn nào ghi primaquin 3,5 ngày. tol 3,5 → 1,75 | indistinguishable (không đổi) |
| 06 | pass | Chỉ thêm notes: không có nguồn DR8; "CDC đổi sang 5 ngày" đọc là "CDC 2026 ghi 5 ngày" (chưa có bản CDC cũ đã băm); cờ độ nhạy H1 | conflict (US) |
| 07 | fix | `population.age` → "trẻ em (câu hỏi dùng trẻ 3 tuổi, 15 kg — thuộc nhóm '< 7 tuổi' của 3312/2015)". Thêm `dr8_sources` = [3312/2015 tr. 521], span 268 ký tự, **`merged_into_vn: "không (chờ HG1.2)"`** (lý do ở 8.3). Notes ghi: chưa lấy được WHO bản cũ, nên "2,4 mg/kg" hiện chỉ quy cho US | **conflict** (US; tol 0,3; mồi 3,6) |
| 08 | pass | Chỉ thêm notes DR8 (không có nguồn cho người lớn) | concordant |

**Tổng sau sửa:** 5 conflict (01, 03, 04, 06, 07), 2 indistinguishable (02, 05), 1 concordant (08); không mẩu nào bị loại.
Mẩu 04 có mồi hỏng, nên số mẩu conflict dùng được cho phép so mồi của H1 là **4**.

**Kiểm tra cuối (file đã ghi):**

- `vnsoc.schemas atom` → **OK 8 dòng hợp lệ**.
- `vnsoc.extract.verify_span` → **OK: 0 mẩu không đạt**. Cả 8 mẩu có `ocr=True`; span DR8 cũng được kiểm nguyên văn đúng trang.
- `pilot_merge.check` → [] ×8; `source_warnings` → [] ×8.
- `enforce_decoy_rule` lũy đẳng ×8 (không đổi mồi hay trạng thái khi gộp).
- `finalize` lũy đẳng; không có trường chỉ-bác-sĩ.

**Chấm thử** (`grade_short`, nạp `grading.yaml`, chạy trong bộ nhớ):

| Mẩu | Câu trả lời | Nhãn | Ghi chú |
|---|---|---|---|
| 01 | "quinin sulfat + clindamycin" / "chloroquin" / "quinin" | 2 / 2 / 2 | chloroquin và quinin đúng nhờ DR8 |
| 01 | "artemether-lumefantrin" | 4 [US, WHO_global] | |
| 01 | "Pyramax" | 5, decoy | |
| 01 | "quinin + clindamycin; nếu không có quinin thì artemether-lumefantrin" | **5** | Chép đúng 3377 mà vẫn nhãn 5: lỗi bộ chấm/thiết kế câu hỏi, còn nguyên |
| 03 | "30 mg" / "4 viên" / "0,25 mg/kg" / "45 mg" / "60 mg" | 2 / 2 / 4 / 4 / 5 decoy | |
| 03 | "36 mg" (0,6 mg/kg × 60 theo 3312) | 2 | Nằm trong dung sai 30 ± 7,5 |
| 04 | "0,5 mg/kg/ngày" / "1 mg/kg/ngày" | 2 / 4 | |
| 04 | "0,25 mg/kg/ngày" và "0,2 mg/kg/ngày" | **3 kèm decoy = True** | Mồi hỏng, còn nguyên |
| 04 | "30 mg/ngày" | **5** (unit_mismatch) | Còn nguyên |
| 05 | "7 ngày" / "14 ngày" / "3,5 ngày" | 2 / 3 [US, WHO] / 5 decoy | |
| 07 | "3 mg/kg" / "2,4 mg/kg" / "3,6 mg/kg" | 2 / 4 [US] / 5 decoy | |
| 07 | "1,5 mg/kg" / "1,5 mg/kg/ngày" | 5 / 5 (unit_mismatch) | Theo 3312 (DR8), chưa hợp |

### 8.3. Chỗ tôi làm khác kiểm toán, và lý do

1. **01: đã áp DR8 ngay**, không chờ người.
   - Kiểm toán để người quyết định D-315 có "cùng quần thể, cùng slot" không. Tôi áp ngay vì:
     - 315/2015 là văn bản `current`, và mục xử trí áp cho mọi phụ nữ có thai bị sốt rét, tức bao trùm quần thể của mẩu;
     - ba phương án không xếp thứ tự, nên cả ba đều là lựa chọn đầu tiên trong văn bản đó;
     - DR8 đã đăng ký trước và không có ngoại lệ "văn bản chuyên ngành mới hơn thắng".
   - Trạng thái không đổi; mô phỏng không có DR8 cũng ra conflict.
   - Nếu người đọc "+" là phối hợp (không phải thay thế), cần sửa lại. Ghi ở 8.5.
2. **07: chưa hợp 1,5 vào `vn`, kể cả nếu người trả lời "có".** Hai lý do:
   - (i) slot của mẩu là liều **mỗi lần**, còn văn bản cho liều **theo ngày** và không ghi số lần. Liều mỗi lần không suy ra được.
   - (ii) `verify_span` không đọc lại được 1,5 mg/kg từ span: parser đọc "1,5 mg/kg/ngày" là mg/kg/day, không quy đổi được.
     Parser còn đọc "lọ 60mg" thành 4 mg/kg ở 15 kg.

   Vì vậy phương án "có → thêm {1,5 mg/kg}" của kiểm toán hiện chưa làm được nếu không sửa mã. Tôi đã ghi nguồn vào
   `dr8_sources` với `merged_into_vn: "không"`. Mô phỏng hợp {3; 1,5}: vẫn conflict, tol 0,3, mồi 3,6.
3. **03: không tải được WHO 2010, nên không ghi năm 2010.**
   - Kiểm toán cho phép hai đường: tải bản 2010, hoặc để người/DECISIONS định quy ước.
   - Tôi không tải được (8.1) nên không điền "2010" từ trí nhớ.
   - `version_date` = "chưa rõ (trước 2012)" theo quy tắc cứng "không biết → chưa rõ". Chuỗi này vẫn chưa theo dạng YYYY
     của schema: cần quy ước (8.6).
4. **05 (pass) có thay đổi dữ liệu:** thêm mồi 3,5 ngày. Đây không phải yêu cầu của kiểm toán. Việc này để khớp mã
   `decoys.py` đổi lúc 12:20 và quy tắc "num: bắt buộc choose_decoy".
5. **EU_UK:** chưa kiểm được (hạn mức WebSearch đã cạn; không có URL chính thức UKHSA/BIA trong bản đệm). **Cả 8 mẩu
   đều chưa có hệ EU_UK.**

### 8.4. Kết quả phụ DR8: các văn bản Bộ Y tế hiện hành mâu thuẫn nhau về sốt rét

Đếm và báo cáo theo DR8. Có 2 mẩu ghi nguồn DR8 có giá trị khác: 01 và 07. Có thêm 3 cặp "ngoài quần thể" đã ghi chú (02,
03, 04/05).

| Quần thể | 3377/2023 (chuyên đề) | Văn bản hiện hành khác | Mẩu |
|---|---|---|---|
| Thai 3 tháng đầu, P. falciparum | quinin + clindamycin (không có quinin thì AL) | 315/2015: chloroquin / SP / quinin đơn trị, không phân tam cá nguyệt. 3312/2015 (bảng theo 3232/2013): Q+C | 01 |
| Trẻ < 7 tuổi (< 20 kg), sốt rét ác tính, artesunat tiêm | 3 mg/kg/lần lúc 0, 12, 24 giờ, rồi mỗi ngày | 3312/2015: 1,5 mg/kg/ngày × 7 ngày | 07 |
| Trẻ em, primaquin | 3377 Bảng 4 theo tuổi; P. vivax 0,5 mg/kg/ngày × 7 hoặc 0,25 × 14 tùy G6PD | 3312/2015: 0,6 mg base/kg (liều đơn ngày cuối; P. vivax × 14 ngày) | 03, 04, 05 (chỉ ghi chú) |
| Trẻ ≥ 3 tuổi, P. falciparum | Pyramax + primaquin | 3312/2015: DHA-PPQ + primaquin | 02 (chỉ ghi chú) |

Nhận định (AI, không phải bác sĩ): 315/2015 và 3312/2015 phản ánh phác đồ cũ, lấy theo 3232/2013 hoặc trước đó. Cả hai
vẫn `current` trong manifest. Điều này đáng báo cáo trong bài như một bất cập của kho văn bản.

### 8.5. Việc cho người ở HG1.2 (bổ sung vào mục 6)

1. **DR8 (quyết định khoa học, ghi `docs/DECISIONS.md`):**
   - (a) 315/2015 tr. 75: ba gạch "+" là **ba phương án thay thế**, đúng như cách tôi đã hợp? Nếu đúng thì cũng thêm SP
     sau khi config có thuốc này.
   - (b) 3312/2015 tr. 521: "Trẻ em < 7 tuổi: 1,5 mg/kg/ngày, 7 ngày" có phải liều artesunat tiêm không, và mỗi lần là bao
     nhiêu? Nếu có, cần sửa mã (8.6) rồi mới hợp vào 07, hoặc lập thêm mẩu anh em "liều/ngày".
   - (c) Phạm vi của 3312/2015 có gồm người lớn không? Tr. 521 có dòng DHA-PPQ "Người lớn > 15 tuổi". Nếu **có**:
     - 02 → conflict (vn ∪ DHA-PPQ);
     - 03 → vn {30; 36} mg, vẫn conflict, tol 1,5, mồi 27 mg;
     - 04 → vn {0,5; 0,6}, vẫn conflict, mồi 0,2, tol 0,05;
     - 05 → **concordant**.

     Tất cả đã mô phỏng.
2. **So ảnh** (dù không phải trang OCR): 3312/2015 tr. 520 (ô hàng/cột), tr. 521 (vị trí dòng 1,5), tr. 522; 315/2015 tr. 75.
3. **03:** chọn quy ước ghi `version_date` cho khuyến cáo cũ không rõ năm. Nếu người có bản WHO 2010, xác nhận 0,75 mg/kg
   rồi đổi thành "2010" kèm url/sha của bản đó.
4. **04:** chọn một trong ba:
   - chấp nhận loại 04 khỏi phép so mồi tới khi sửa `check_decoy`;
   - đổi slot sang tổng liều (VN 3,5 mg/kg; WHO 7; CDC 7 ở 60 kg);
   - chấp nhận mồi 0,2 kèm phân tích độ nhạy.
5. **05:** xác nhận mồi 3,5 ngày (mirror_geom) chấp nhận được cho câu trắc nghiệm.
6. Mọi việc ở mục 6 vẫn còn, đặc biệt: so từng số với ảnh 3377 tr. 9, 10, 11, 16, 17, 19 (mọi mẩu đều từ OCR).

### 8.6. Đề xuất mã và config (cập nhật; không tự sửa)

1. **`decoys.check_decoy`.** Bản 12:20 chưa đủ. Cần thêm:
   - (a) loại mồi có `_gap(mồi, nguồn) < 2·tol` với mọi nguồn đã ghi (foreign, superseded);
   - (b) so cả **giá trị phản chiếu trước khi làm tròn** với nguồn, vì ở 04 mirror_geom chưa làm tròn = 0,25 = bản cũ.

   Kèm test ca 04. Sau khi sửa, 04 → `decoy = []`. Ghi DECISIONS vì đây là quy tắc mồi đã đăng ký.
2. **`grade.grade_short`**, nhánh thuốc:
   - lỗi 7.1: so theo **mục** foreign, không theo hệ thống;
   - câu trả lời "phác đồ VN + lựa chọn thay thế có điều kiện" (01) đang bị nhãn 5.
3. **`normalize_vi`:**
   - cạnh mg/ngày ↔ mg/kg/ngày theo `weight_kg` (04: "30 mg/ngày");
   - cạnh mg/kg/ngày ↔ mg/kg theo khóa context mới `doses_per_day` (07, nếu người chọn 8.5-1b);
   - không coi hàm lượng lọ/viên ("lọ 60mg") là liều.
4. **`configs/grading.yaml`:**
   - drugs: `sulfadoxine-pyrimethamine: [sulfadoxin-pyrimethamin, "sulfadoxin /pyrimethamin", sp, fansidar]` (315/2015
     viết "Sulfadoxin /pyrimethamin", có dấu cách trước "/"), `amodiaquine: [amodiaquin]`;
   - combos: `artesunate-mefloquine`, `artesunate-amodiaquine`, `artesunate+sulfadoxine-pyrimethamine`;
   - tăng `grader_version`.

   Khi có SP, thêm `{key_drugs:["sulfadoxine-pyrimethamine"]}` vào `vn` của 01.
5. **`schemas.ForeignValue.version_date`:** thêm validator và quy ước cho năm không rõ, ví dụ "YYYY | YYYY-MM | YYYY-MM-DD
   | chưa rõ (trước YYYY)".
6. **DR8 trong công cụ:**
   - chuẩn hóa trường `merged_into_vn` trong `extraction.dr8_sources`;
   - `pilot_merge.checklist` in cả nguồn DR8 cho HG1.2 (hiện không in);
   - thêm lệnh quét DR8 tự động trên mọi văn bản `current` (8.1), bắt buộc trước khi ghi `dr8_sources = []` (khuyến nghị 6
     của kiểm toán).
