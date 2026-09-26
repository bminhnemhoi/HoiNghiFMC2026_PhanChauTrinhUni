# Kiểm toán độc lập — thí điểm `immunization` (Tiêm chủng mở rộng trẻ em)

Người kiểm: integrity-auditor (Claude), kiêm góc nhìn bác sĩ lâm sàng Việt Nam **do AI đóng vai, không phải bác sĩ thật**. Ngày 26/09/2026.
Phạm vi: `data/interim/pilot/immunization.jsonl` (4 mẩu) và `immunization_report.md`. Tôi chỉ đọc dữ liệu; chỉ ghi file này. Ảnh trang và OCR thử để trong scratchpad của phiên, không ghi vào `data/`.

## Kết luận nhanh

| atom_id | Loại | Verdict | Lý do chính |
|---|---|---|---|
| P-immunization-01 | xung đột (sởi MCV1) | **fix** (bị chặn) | Văn bản nguồn TT52/2025 hết hiệu lực từ 01/7/2026, chưa có văn bản hiện hành có lịch tiêm. Trường intervention "đơn giá" lệch slot với Mỹ. Nhãn phiên bản CDC chưa chính xác. Quy nguồn "chỉ Mỹ" chưa chắc. |
| P-immunization-02 | xung đột (bạch hầu nhắc lần 2) | **fix** (bị chặn) | Như trên. Thêm: nêu "giảm liều" thì slot Mỹ sai (Mỹ dùng Tdap 11–12 tuổi). Không tách được quy nguồn US/WHO. |
| P-immunization-03 | đối chứng (VGB sơ sinh) | **fix** (sửa được ngay) | Neo lại vào **TT13/2026 (đang hiệu lực) Điều 26 khoản 1, trang 18** qua OCR. Hạn chế quần thể lấy từ CDC. Một tuyên bố về phiên tòa phúc thẩm chưa có nguồn. |
| P-immunization-04 | đối chứng (DTP nhắc lần 1) | **fix** (bị chặn) | Văn bản hết hiệu lực. Span dài 593/600 ký tự. |

Không mẩu nào đạt "pass": cả 4 đều neo vào văn bản **không còn hiệu lực** tại ngày đóng băng kho (15/10/2026).

Phần kỹ thuật đều đạt:
- Schema: `OK 4 dòng hợp lệ (atom)`.
- `verify_span`: 4/4 OK.
- Giá trị Việt Nam đúng trang.
- Mọi giá trị nước ngoài có trong nguồn đã băm.
- Mồi đúng `mirror_decoy`.
- `finalize` cho lại đúng tolerance và trạng thái đã ghi.
- Không có trường chỉ bác sĩ được điền.

---

## Kiểm lại bằng công cụ (tóm tắt bằng chứng)

**1. Văn bản Việt Nam**
- `TT52/2025` (sha256 `fbaa37ef…`, 10 trang, có lớp chữ):
  - Tôi đọc lại `--page` các trang 1–10.
  - Giá trị: sởi đơn giá 9 tháng (trang 7); nhắc lại lần 1 lúc 18 tháng ở dòng bạch hầu (trang 2), ho gà (trang 3), uốn ván (trang 4); "bạch hầu giảm liều" nhắc lại lần 2 lúc 7 tuổi (trang 3); uốn ván nhắc lại lần 2 lúc 7 tuổi (trang 4); VGB sơ sinh "trong vòng 24 giờ sau khi sinh" (trang 1).
  - Tập giá trị `vn` đầy đủ: không trang nào ghi giá trị khác cho cùng quần thể.
  - Danh tính và hiệu lực: ảnh trang 9 có dấu số "15 02" ở Điều 4 (hiệu lực 15/02/2026). PDF có 7 trường chữ ký số. Danh mục tiemchungmorong.vn/documents (WebFetch hôm nay) ghi "Thông tư 52/2025/TT-BYT ngày 31/12/2025". TT13/2026 Điều 27 khoản 2 điểm d gọi đúng số, ngày và tên văn bản này.
- `TT13/2026` (sha256 `8328ae00…`, 19 trang, bản quét). Tôi đọc ảnh trang 1–4, 18, 19 và chạy OCR thử trang 3 và 18:
  - Trang 1: "Số: 13/2026/TT-BYT", ngày 16/5/2026, căn cứ Luật Phòng bệnh 114/2025/QH15.
  - Trang 2: Điều 3 có 14 nhóm bệnh (có HPV).
  - Trang 3: Điều 5 khoản 4 giao "Lịch tiêm chủng và cách dùng vắc xin, sinh phẩm" cho "hướng dẫn của nhà sản xuất, hướng dẫn chuyên môn của Cục Phòng bệnh".
  - Trang 4: Điều 6 và Điều 7 cũng giao cho Cục Phòng bệnh.
  - Trang 18: Điều 26 khoản 1 ghi "tổ chức thực hiện việc tiêm chủng vắc xin viêm gan B trong vòng 24 giờ sau sinh". Điều 27: hiệu lực 01/7/2026; điểm d bãi bỏ TT52/2025.
  - Trang 19: Thứ trưởng Nguyễn Thị Liên Hương ký.
  - **Mọi điều báo cáo nêu về TT13/2026 đều đúng.**
- `TT10/2024` (sha256 `cb760684…`, 5 trang, bản quét). Tôi đọc ảnh trang 1–3; giá trị trùng TT52/2025:
  - Trang 1: VGB "trong vòng 24 giờ sau khi sinh"; bạch hầu nhắc lại 18 tháng; "bạch hầu giảm liều" nhắc lại lúc 7 tuổi (TT10 không ghi "lần 2").
  - Trang 2: ho gà 18 tháng; uốn ván 18 tháng và 7 tuổi.
  - Trang 3: sởi, ghi "Vắc xin có chứa thành phần sởi" (không ghi "đơn giá"), 9 tháng.
  - Không có "3 tháng" hay "4 tháng" cho DTP. Chỉ có "khi trẻ đủ 02 tháng tuổi" và "ít nhất 01 tháng sau lần 1/lần 2".
- **Văn bản lịch tiêm hiện hành:** tôi cũng không tìm thấy "hướng dẫn chuyên môn của Cục Phòng bệnh" về lịch tiêm.
  - tiemchungmorong.vn/documents: văn bản mới nhất là TT52/2025.
  - Tin trong nước của trang này tới 30/6/2026 cũng không có.
  - vncdc.gov.vn: WebFetch báo "certificate has expired".
  - WebSearch của phiên đã hết hạn mức, nên không tìm rộng hơn được. Chưa loại trừ khả năng văn bản đó tồn tại mà chưa đăng công khai.

**2. Nguồn nước ngoài** (`vnsoc.match.sources grep`, dùng cache)
- CDC PDF (sha `96159043…`):
  - Trang 1 ghi "united states 2025 revised 07/02/2025".
  - Trang 10: MMR "2-dose series at age 12-15 months, age 4-6 years".
  - Trang 8: DTaP "booster doses at ages 15-18 months and 4-6 years".
  - Trang 9: VGB "mother is hbsag-negative" và "birth weight ≥2,000 grams: 1 dose within 24 hours of birth".
  - Tất cả khớp mẩu.
- WHO Table 1 (sha `9861c483…`):
  - Các trang ghi "(updated: december 2025)". Trang WHO hôm nay vẫn ghi "as of December 2025", không có bản 2026.
  - Trang 8: MCV1 "should be given at age 9 months" ở nước còn lây truyền.
  - Trang 1 và 6: nhắc lại "12-23 months (dtpcv) and 4-7 years (td/dt…)", thêm "9-15 yrs (td)".
  - Trang 5: VGB "as soon as possible after birth, ideally within 24 hours".
  - Tất cả khớp mẩu.
- WHO bản tóm tắt position paper sởi 2017 (sha `704cfe53…`), trang 1: MCV1 "at 9 months of age" ở nơi nguy cơ cao; "may be administered at 12 months" ở nơi gần loại trừ; liều bổ sung "from 6 months of age" khi có dịch.
- CRS R48982 (sha `66d7d66d…`), bằng chứng bối cảnh Mỹ:
  - Trang 5: "on march 16, 2026 … issued a stay"; lệnh này đưa lịch về "the version as of may 2025"; kháng cáo "april 29, 2026".
  - Trang 7: lá phiếu ACIP 12/2025 chuyển VGB sơ sinh (mẹ HBsAg âm tính) sang quyết định cá nhân.

**3. Mồi và trạng thái** (chạy lại bằng Python)
- `mirror_decoy(auto)`: mẩu 01 → 3–6 tháng (mirror_arith); mẩu 02 → 8–10 tuổi (mirror_arith). Cả hai trùng giá trị đã ghi; `check_decoy` = [].
- `finalize`: 01 → tol 1,5, conflict; 02 → tol 0,5, conflict; 03 và 04 → tol 0, concordant. Đều trùng giá trị đã ghi.

---

## P-immunization-01 — sởi, tuổi tiêm mũi 1 (MCV1)

- **verdict: fix** (bị chặn chờ HG1.2)
- **Đã đúng:**
  - Span trang 7 TT52/2025 đúng nguyên văn.
  - VN 9 tháng; US 12–15 tháng (CDC trang 10); WHO 9 tháng cho nước còn lây truyền (Table 1 trang 8; PP 2017 trang 1).
  - Xung đột có thật: hỏi "tiêm mũi 1 vắc xin sởi thường quy lúc mấy tháng tuổi" thì "12–15 tháng" sai theo Bộ Y tế.
  - Mồi đúng quy tắc.
- **Vấn đề và cách sửa:**
  1. **(Chặn) Văn bản không còn hiệu lực.** TT52/2025 hết hiệu lực từ 01/7/2026 (TT13/2026 trang 18, Điều 27 khoản 2 điểm d). TT13/2026 không có lịch sởi (Điều 5 khoản 4, trang 3).
     - Sửa: giữ `valid_to: 2026-06-30` (trung thực). Không đưa vào atoms v1 cho tới khi HG1.2 xong: hoặc (a) có văn bản hướng dẫn của Cục Phòng bệnh → tạo lại span và `guideline`; hoặc (b) người dùng quyết định dùng "lịch Bộ Y tế công bố gần nhất" và ghi `docs/DECISIONS.md`, kèm câu giới hạn trong bài.
  2. **Trường `intervention` gây lệch slot.** Hiện ghi "vắc xin sởi đơn giá (mũi 1, MCV1)". Mỹ không dùng vắc xin sởi đơn giá (chỉ MMR/MMRV, CDC trang 10). Nếu câu hỏi chép "đơn giá", giá trị Mỹ không còn tương ứng.
     - Sửa: `intervention` → "vắc xin có chứa thành phần sởi – mũi 1 (MCV1), tiêm chủng thường xuyên". Thêm vào `extraction.notes`: "câu hỏi không nêu loại vắc xin (đơn giá/MMR)".
  3. **Nhãn phiên bản CDC chưa chính xác.** `source` ghi bản "revised 07/02/2025" là "operative 9/2026". CRS trang 5 ghi lệnh đình chỉ đưa lịch về "the version as of may 2025", tức là trước bản sửa 07/02/2025. CRS đề ngày 11/6/2026, nên tình trạng tháng 9/2026 chưa được nguồn nào xác nhận.
     - Sửa `foreign[US].source`: "CDC/ACIP Child & Adolescent Schedule 2025 (PDF revised 07/02/2025). D. Mass. stay 16/3/2026 reverts to version as of May 2025 (CRS R48982 p.5, 11/6/2026). Status after 6/2026 not verified."
     - Nên tải thêm bản CDC 2025 gốc (tháng 1/2025) để xác nhận giá trị MMR không đổi. Tôi chưa kiểm bản đó.
  4. **Quy nguồn "chỉ Mỹ" chưa chắc.** "12 tháng" cũng là giá trị WHO cho nước gần loại trừ (Table 1 trang 8; PP 2017 trang 1 "may be administered at 12 months"), và có thể là giá trị EU_UK (chưa ghi hệ EU_UK; tôi **chưa tải nguồn** nên không nêu giá trị).
     - Sửa: tải lịch tiêm UKHSA hoặc ECDC bằng `vnsoc.match.sources fetch` rồi ghi hệ EU_UK nếu có. Nếu có, đổi `conflict_family` từ `measles_mcv1_age_us` sang nhãn không gắn một nước (ví dụ `measles_mcv1_age`).
     - Không ảnh hưởng H1 (bất kỳ nguồn nước ngoài), nhưng ảnh hưởng phân tích quy nguồn theo hệ thống.
  5. **Mồi 3–6 tháng chạm "6 tháng".** Đây là tuổi liều bổ sung khi có dịch hoặc đi vùng lưu hành (WHO Table 1 trang 8 "from 6 months of age") và liều trước du lịch của CDC 6–11 tháng (trang 10).
     - Các mồi dự phòng cũng không sạch hơn: `mirror_geom` 4,5–7,5 tháng vẫn chứa 6; `mirror_far` ≤ 0.
     - Giữ mồi theo quy tắc đăng ký trước. Ghi vào HG1.2 như một giới hạn (thiên về bảo thủ cho H1).
  6. Kiểm chấm: "11 tháng" bị chấm là foreign US, do dung sai 1,5 kéo khoảng Mỹ xuống 10,5. Đây là quy tắc chấm đã định, không phải lỗi mẩu. Chỉ ghi lại.

## P-immunization-02 — bạch hầu, mũi nhắc lại lần 2

- **verdict: fix** (bị chặn chờ HG1.2)
- **Đã đúng:**
  - Span trang 3 TT52/2025 đúng; dòng uốn ván trang 4 cùng giá trị 7 tuổi.
  - US: DTaP liều 5 lúc "4-6 years" (CDC trang 8, "booster doses at ages 15-18 months and 4-6 years").
  - WHO: mũi nhắc thứ 2 lúc 4–7 tuổi (Table 1 trang 1 và 6).
  - Xung đột với Mỹ có thật. WHO trùng Việt Nam (7 nằm trong 4–7).
  - Mồi 8–10 đúng mirror_arith.
- **Vấn đề và cách sửa:**
  1. **(Chặn) Văn bản không còn hiệu lực.** Như mẩu 01.
  2. **Slot phụ thuộc cách đặt câu hỏi.** `intervention` ghi "giảm liều, Td ở Việt Nam". Nếu câu hỏi nêu "vắc xin bạch hầu giảm liều (Td)", tương ứng ở Mỹ là liều Tdap vị thành niên "at age 11-12 years" (CDC trang 14). Khi đó giá trị Mỹ 4–6 tuổi (DTaP liều đầy đủ) sai slot.
     - Sửa: `intervention` → "vắc xin có chứa thành phần bạch hầu – mũi nhắc lại lần 2 (sau mũi nhắc 18 tháng)". Thêm ràng buộc vào `extraction.notes`: "không nêu dạng bào chế (giảm liều/Td/DTaP) trong câu hỏi".
  3. **Không tách được quy nguồn.** Chạy `grade_short` thử: "4–6 tuổi" và "5 tuổi" đều được chấm foreign **[US, WHO_global]**, vì khoảng WHO 4–7 chứa khoảng Mỹ. Báo cáo đã nêu đúng điều này.
     - Mẩu vẫn dùng được cho H1, nhưng gần như vô ích cho RQ quy nguồn theo hệ thống. Đề xuất HG1.2 cân nhắc giữ mẩu nhưng loại khỏi phân tích theo hệ thống.
  4. **Mồi 8–10 tuổi chồng mũi Td thứ 3 của WHO** ("9-15 yrs (td)", Table 1 trang 1). Chạy thử: "9 tuổi" được chấm trùng mồi.
     - Các mồi dự phòng còn tệ hơn: `mirror_geom` 8,8–10,8; `mirror_far` 10–12 chồng cả Tdap Mỹ 11–12 tuổi.
     - Giữ mồi theo quy tắc, ghi thành giới hạn ở HG1.2.
  5. (Phụ) CDC trang 8: "dose 5 is not necessary if dose 4 was administered at age 4 years or older…". Đây là trường hợp đặc biệt, không đổi giá trị thường quy; câu hỏi nên nói rõ "đúng lịch".

## P-immunization-03 — viêm gan B, liều sơ sinh

- **verdict: fix** (sửa được ngay, không cần chờ Cục Phòng bệnh)
- **Đã đúng:**
  - Span trang 1 TT52/2025 đúng.
  - US: "within 24 hours of birth", mẹ HBsAg âm tính, ≥ 2.000 g (CDC trang 9).
  - WHO: "ideally within 24 hours" (Table 1 trang 5).
  - Đối chứng có thật dưới lịch CDC đang được tòa khôi phục.
- **Vấn đề và cách sửa:**
  1. **Neo lại vào văn bản đang hiệu lực.** TT13/2026 Điều 26 khoản 1 (trang PDF 18) ghi "tổ chức thực hiện việc tiêm chủng vắc xin viêm gan B trong vòng 24 giờ sau sinh".
     - Tôi đã đọc ảnh trang và chạy OCR thử trong scratchpad (Tesseract 5.4, vie+eng, 300 dpi, tessdata dự án). Chữ ra sạch.
     - **Máy đã có OCR**: `vnsoc.extract.ocr` tìm thấy `C:\Program Files\Tesseract-OCR\tesseract.exe` và `data/cache/tessdata`. Báo cáo coi TT13/2026 là "không kiểm span được", điều này không còn đúng.
     - Sửa (việc của atom-extractor, tôi không tự ghi):
       1. Chạy `vnsoc.extract.ocr --key TT13/2026 --pages 18`, rồi `verify_span`.
       2. Sửa các trường: `guideline` → `TT13/2026`; `page` → 18; `section` → "Điều 26 khoản 1"; `span` → chuỗi OCR đã khớp; `valid_from` → 2026-07-01; `valid_to` → null; `extraction.ocr` → true.
       3. Đưa trang này vào danh sách người kiểm OCR theo ảnh (đề cương §3.1).
       4. Bổ sung `population.setting` → "trẻ sinh tại cơ sở khám bệnh, chữa bệnh có phòng sinh", vì điều khoản được viết như trách nhiệm của cơ sở.
       5. Giữ TT52/2025 trang 1 trong notes làm bằng chứng phụ (cùng giá trị; không phải lệch phiên bản).
  2. **Hạn chế quần thể lấy từ CDC.** Các giới hạn "mẹ HBsAg âm tính", "≥ 2000 g, ổn định" không có trong văn bản Việt Nam; cả TT52 và TT13 áp dụng cho mọi trẻ sơ sinh.
     - Chấp nhận được, vì đây là quần thể con để khớp slot Mỹ. Nhưng thêm vào `extraction.notes`: "giới hạn quần thể lấy theo CDC; văn bản Bộ Y tế không phân nhóm".
     - Chưa kiểm hướng dẫn khám sàng lọc trước tiêm chủng của Bộ Y tế có quy định riêng cho trẻ < 2000 g hay không. Cần kiểm trước khi đóng băng.
  3. **Tuyên bố chưa có nguồn trong `notes`.** Câu "phúc thẩm Tòa Khu vực 1 tranh luận 6/10/2026" không có trong nguồn nào đã băm (CRS chỉ tới 11/6/2026).
     - Sửa: xóa, hoặc ghi "(chưa kiểm, từ kết quả tìm kiếm)". Việc kiểm lại tình trạng lệnh đình chỉ trước 15/10/2026 là bắt buộc: nếu lịch CDC 2026 có hiệu lực, mẩu có thể thành xung đột.
  4. Nhãn phiên bản CDC: sửa như mẩu 01 mục 3.
  5. Kiểm chấm: "1 ngày" ra `unit_mismatch` (nhãn 5), vì chưa có cạnh quy đổi ngày ↔ giờ. Đồng ý với đề xuất `STATIC_EDGES ("day","h"): 24` trong báo cáo.

## P-immunization-04 — DTP, mũi nhắc lại lần 1

- **verdict: fix** (bị chặn chờ HG1.2)
- **Đã đúng:**
  - Span trang 3 TT52/2025 đúng; dòng bạch hầu (trang 2) và uốn ván (trang 4) cùng giá trị 18 tháng.
  - US 15–18 tháng (CDC trang 8); WHO 12–23 tháng (Table 1 trang 1).
  - Đối chứng thật so với US và WHO.
- **Vấn đề và cách sửa:**
  1. **(Chặn) Văn bản không còn hiệu lực.** Như mẩu 01.
  2. **Span dài 593/600 ký tự**, gần hết là lịch cơ bản. Dòng ho gà ghi "Tiêm nhắc lại" (không có "lần 1"), trong khi `intervention` ghi "nhắc lại lần 1".
     - Sửa (khuyến nghị): dùng span ngắn trên một trang ở dòng uốn ván trang 4, "Trẻ em - Tiêm nhắc lại lần 1 khi trẻ đủ 18 tháng tuổi." (khớp chữ "lần 1"), và đổi `section` tương ứng. Hoặc giữ span hiện tại và sửa `intervention` thành "mũi nhắc lại (18 tháng)".
  3. Tính "đối chứng" chỉ đúng so với US và WHO; chưa đối chiếu EU_UK. Ghi rõ trong notes.
  4. Kiểm chấm: "15–18 tháng" được chấm foreign [US, WHO_global], dù đây là mẩu đối chứng, vì khoảng trả lời không nằm trong tập Bộ Y tế (tol 0). Đây là thiết kế chấm, không phải lỗi mẩu. Nhóm chấm cần biết khi diễn giải đối chứng.

---

## Vấn đề chung

1. **(Chặn cả chủ đề) Không có văn bản lịch TCMR hiện hành kiểm được.**
   - Chuỗi TT38/2017 → TT10/2024 → TT52/2025 → TT13/2026 đã được xác nhận bằng ảnh trang (TT10 trang 1; TT52 trang 9; TT13 trang 3 và 18).
   - TT13/2026 bỏ bảng lịch và giao cho "hướng dẫn chuyên môn của Cục Phòng bệnh"; văn bản đó chưa tìm thấy.
   - HG1.2 cần người dùng chọn một trong ba hướng:
     - (a) tìm hoặc hỏi Cục Phòng bệnh / Viện VSDT TƯ để lấy văn bản hướng dẫn lịch tiêm;
     - (b) quyết định dùng TT52/2025 như "lịch Bộ Y tế công bố gần nhất, TT13/2026 không thay đổi giá trị", ghi `docs/DECISIONS.md` và nêu giới hạn trong bài (người phản biện Q1 có thể bắt lỗi "đối chiếu với thông tư đã bãi bỏ");
     - (c) chỉ giữ mẩu 03 (neo vào TT13/2026) cho v1.
   - Tôi không khuyến nghị (b) nếu chưa thử (a).
2. **Máy đã có OCR.** Tesseract và tessdata_best có trong dự án, sidecar đã có cho 3377_2023 và TT51_2017. TT13/2026 và TT10/2024 nên được OCR (trong hạn mức ≤ 10 văn bản OCR của §3.1), để neo mẩu 03 vào TT13 và để ghi `superseded_spans` TT10/2024 nếu cần.
3. **Nguồn cần duyệt (HG2.3).** Các host `cmsapi.tiemchungmorong.vn`, `datafiles.chinhphu.vn` và `bcp.cdnchinhphu.vn` không có trong `configs/project.yaml` `official_hosts` (hiện chỉ có kcb.vn, moh.gov.vn, vncdc.gov.vn). Danh tính TT52/2025 và TT13/2026 được đối chiếu chéo tốt: số, ngày, người ký, chữ ký số, và TT13 dẫn chiếu đúng TT52.
4. **Độ chính xác của báo cáo agent:**
   - Đúng: chuỗi văn bản; giá trị TT10 = TT52; lý do loại dòng hạt giống 24 ("2, 3, 4 tháng" không có nguyên văn); các giá trị CDC và WHO; kết quả chấm thử; bối cảnh lệnh đình chỉ ở Mỹ (khớp CRS trang 5).
   - **Sai một chỗ ở §4:** báo cáo nói hạt giống ghi "CDC (bản 2026)". Thực tế `data/seed/seed_conflicts.yaml` dòng 68–72 và bảng đề cương `docs/01_DE_CUONG.md` dòng 208–209 chỉ ghi "CDC", không ghi năm. Chữ "2026" đến từ đề bài task.
   - Không nhất quán nội bộ: báo cáo nói tòa "đưa lịch về bản trước tháng 6/2025", nhưng mẩu lại ghi bản "revised 07/02/2025" là bản đang hiệu lực.
   - Tuyên bố "phúc thẩm 6/10/2026" chưa có nguồn đã băm.
5. **Thiếu hệ EU_UK** ở cả 4 mẩu, nên phân tích quy nguồn theo hệ thống bị lệch về US. Đề xuất counterpart-matcher tải lịch UKHSA hoặc ECDC (tôi không nêu giá trị vì chưa tải).
6. **Mồi bị nhiễm khuyến cáo lân cận** (01: 6 tháng; 02: 9–15 tuổi), ở mọi quy tắc dự phòng. Không sửa quy tắc sau khi đã đăng ký. Ghi vào HG1.2 và phần giới hạn: tỉ lệ trùng mồi có thể cao hơn mức "trùng ngẫu nhiên", thiên về bảo thủ cho H1.
7. **Đề xuất mã** (không tự sửa, theo quy tắc 4), bổ sung cho §6 của báo cáo:
   - `normalize_vi`: xử lý tuổi ghép "3 tuổi 4 tháng". Chạy thử hiện tách thành 2 giá trị (3 năm và 0,33 năm), nên bị chấm multi/nhãn 5. Cần kèm test.
   - Đồng ý thêm cạnh quy đổi ngày ↔ giờ và tuần ↔ tháng.
8. **Không có trường chỉ bác sĩ** (`moh_lags_evidence`, `clinical_harm`, `clinician_confirmed`) trong 4 mẩu. Đúng quy tắc. `context_checked` = "pending" cho cả 4; giữ nguyên tới HG1.2.
