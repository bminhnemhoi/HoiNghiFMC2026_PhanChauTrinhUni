# Kiểm toán độc lập — thí điểm Sốt rét (ID = malaria)

Ngày: 2026-09-26 · Người kiểm: integrity-auditor (AI; có góc nhìn bác sĩ lâm sàng do AI đóng vai, **không phải bác sĩ thật**)
Đối tượng: `data/interim/pilot/malaria.jsonl` (0 dòng) và `data/interim/pilot/malaria_report.md`.
Nguyên tắc: không tin báo cáo, tự chạy lại mọi kiểm tra. Chỉ đọc dữ liệu; chỉ ghi file này.

## 0. Kết luận nhanh

- **JSONL có 0 mẩu nên không có mẩu nào để pass/fix/reject.**
  - `vnsoc.schemas atom` → "OK 0 dòng hợp lệ".
  - `verify_span` → "OK: 0 mẩu không đạt".
- **Lý do "0 mẩu" (không có OCR) đã HẾT HIỆU LỰC.** Sau khi báo cáo được viết (11:01), có sidecar OCR cho 3377/2023 tại
  `data/interim/ocr/3377_2023/`, tạo lúc 11:13–11:15:
  - tesseract 5.4.0, `vie+eng`, 300 dpi, đủ 23 trang;
  - `pdf_sha256` = `aa1792688e9dda03…`, khớp đúng `data/raw/3377_2023.pdf`.

  `verify_span` (sửa lúc 11:22) giờ đọc được sidecar này. Tôi chạy `verify_atom` trong bộ nhớ cho **cả 9 span ứng viên**
  (D1, D1b, D2, D2-AL, D3, D3-mg, D4, D5, D5b). **Tất cả đều `ok=True`, `ocr=True`** (mục 2).

  → Cần **chạy lại trích mẩu sốt rét**, gắn `extraction.ocr = true` và so từng con số với ảnh trang ở HG.
- Báo cáo **trung thực và phần lớn chính xác**:
  - mọi số trang và giá trị VN khớp OCR và ảnh trang tôi dựng;
  - mọi span bản cũ 2699/2020 khớp lớp chữ;
  - giá trị WHO khớp nguồn đã cache (sha `4e2c67b2…`).
- **Sai hoặc thiếu trong báo cáo:**
  1. **D5b (artesunat tiêm, trẻ < 20 kg) KHÔNG phải đối chứng trùng.** Chú thích ở bảng CDC (đọc bằng WebFetch) nói CDC
     dùng 2,4 mg/kg cho trẻ < 20 kg và ghi rõ WHO dùng 3 mg/kg. Vậy VN = WHO = 3 ≠ US = 2,4. `finalize` → **conflict**
     (tol 0,3). Báo cáo ghi "CDC: chưa rõ" và "concordant (chỉ WHO)".
  2. **Lỗi mã #1 (mirror_decoy không quy đổi đơn vị) không còn tái hiện.** `decoys.py` đã sửa lúc 11:17: D3 giờ ra mồi
     **45 mg**, không phải 59,75 mg.
  3. **Lỗi mã #2 (mồi sát giá trị bản cũ) VẪN CÒN**, đúng như báo cáo.
  4. **Đề xuất fetch_pdf/sidecar phần lớn đã có** (`pdf_choice.json` và sidecar OCR trong `verify_span`).
- **Vấn đề mới báo cáo chưa nêu:**
  - `grade._gap` trả `inf` khi không quy đổi được đơn vị, nên ghi CDC "30 mg/ngày" vào mẩu đơn vị mg/kg/day sẽ thành
    **conflict giả**. Dòng hạt giống 19 ghi đúng kiểu này.
  - OCR làm sai ký hiệu và phân số: "≥" → ">", "1/3" → "1⁄4", "2/3" → "2/4".
  - Ở D4, khi đặt slot "liệu trình 7 ngày", giá trị bản cũ (0,25 mg/kg × **14** ngày) không còn cùng slot.

---

## 1. Kiểm lại văn bản và nguồn

| Mục | Kiểm bằng | Kết quả |
|---|---|---|
| `data/raw/3377_2023.pdf` | sha256sum; pymupdf | sha `aa1792688e9dda03…` ✓. 23 trang. Lớp chữ mỗi trang chỉ 54–144 ký tự, toàn dấu văn thư Sở Y tế Thanh Hóa. Creator là PaperStream ClickScan (bản quét) ✓ |
| Danh tính 3377/2023 | `verify_span --page 3377/2023 1` (OCR) | "Số: 3377 /QĐ-BYT", "ngày 30 tháng 8 năm 2023". Điều 1 thay thế hướng dẫn kèm QĐ 2699/QĐ-BYT ngày 26/06/2020. Điều 2 có hiệu lực từ ngày ký ✓ |
| `data/raw/2699_2020.pdf` | sha256sum; pymupdf | sha `8bc1a6b403476197…` ✓. 30 trang. Producer VGCASignService, 2020-06-26 16:14:40 ✓. Trang 1 để trống số ("Số: /", "ngày tháng 6 năm 2020") ✓. Danh tính dựa vào tiêu đề, ngày ký và trang danh mục IMPE-QN → chờ xác nhận ở HG, như báo cáo đã nêu |
| Có bản VN mới hơn 3377/2023 không? | WebFetch kcb.vn/phac-do (trang 1) | Không có mục sốt rét. **Không loại trừ hoàn toàn được**: đã hết ngân sách WebSearch (200/200), nimpe.vn trả ECONNREFUSED, impe-qn.org.vn lỗi chứng chỉ. → Cần corpus-librarian xác nhận trước khi đóng băng kho (15/10/2026) |
| WHO guidelines for malaria | `sources grep` (cache) | "10 September 2026", doi 10.2471/B09879, 494 trang, sha `4e2c67b2ec74124e` ✓ |
| WHO version updates | `sources grep` | Các mốc 25/11/2022, 30/11/2024, 13/8/2025, 10/9/2026 ✓. Bản 30/11/2024 cập nhật primaquin, tafenoquin và xét nghiệm G6PD. Bản 10/9/2026 cập nhật primaquin liều đơn cho vùng lan truyền trung bình–cao ✓ |
| CDC Appendix A | `sources fetch` | **403** (tôi tự chạy lại) ✓. Đọc bằng WebFetch: Published 9/7/2026, Updated 17/8/2026 → `page_sha256 = null`, needs_human_check |

---

## 2. Từng mẩu (mẩu dự thảo của báo cáo; JSONL không có mẩu)

Ghi chú chung cho mục này:
- Verdict ở đây là **khuyến nghị cho lần trích lại**, không phải verdict trên dòng JSONL.
- "Span OCR" là chuỗi lấy nguyên văn từ `verify_span --page` (kể cả lỗi OCR). Tôi đã chạy `verify_atom` cho từng span:
  `ok=True`, `ocr=True`.

### D1 — hạt giống 16 · first_line, drugs · P. falciparum chưa biến chứng, không có thai
- **verdict: reject** (khỏi phân tích xác nhận). Đồng ý với báo cáo.
- Bằng chứng VN:
  - 3377 tr. 9 (OCR và ảnh): mục III.2.1.a "Điều trị đặc hiệu ưu tiên" ghi Pyramax 3 ngày + primaquin liều duy nhất.
  - Mục b "Điều trị thay thế … theo thứ tự ưu tiên": AS-MQ, **AL (thứ 2)**, AS-AQ, **DHA-PPQ (thứ 4)**, quinin + clindamycin/doxycyclin.
- Bằng chứng bản cũ: 2699 tr. 6 ghi DHA-PPQ 3 ngày + primaquin liều duy nhất (`--find` → [6]).
- Bằng chứng WHO: WHO 10/9/2026 tr. 17 liệt kê 6 ACT, trong đó có AL, DHA-PPQ và **artesunate-pyronaridine** (2022).
  Vậy lựa chọn ưu tiên của VN nằm trong tập WHO.
- `finalize` (trong bộ nhớ):
  - US + WHO + bản cũ → **indistinguishable**;
  - chỉ US + bản cũ → conflict;
  - bỏ bản cũ → conflict.

  Phải ghi cả WHO (không được bỏ bớt nguồn), nên trạng thái trung thực là indistinguishable.
- Thêm: DHA-PPQ vừa là giá trị bản cũ vừa là thuốc thay thế thứ 4 của bản hiện hành. Khác biệt với CDC chỉ là thứ tự ưu tiên.
- fix: không tạo mẩu xác nhận. Nếu cần mô tả, ghi làm mẩu khám phá.

### D2 — hạt giống 17 · first_line, drugs · P. falciparum chưa biến chứng, thai 3 tháng đầu
- **verdict: fix** (tạo mẩu; trạng thái đúng là conflict).
- Span OCR tr. 10: `Thuốc điều trị là quinin sulfat 7 ngày (xem Bảng 6) + clindamycin 7 ngày (xem Bảng 7).` → ok.
- Cùng trang có câu dự phòng: `+ Trường hợp không có quinin sulfat, có thể dùng artemether - lumefantrin (xem Bảng 10).`
  Câu này đã kiểm bằng `--find` → [10] và ảnh trang.
- Các trường nên đặt:
  - `population`: `{pregnancy: "3 tháng đầu", species: "P. falciparum hoặc nhiễm phối hợp có P. falciparum", severity: "chưa biến chứng"}`;
  - `slot_type = first_line`; `vn = [{key_drugs: ["quinine+clindamycin"]}]`;
  - câu hỏi phải hỏi rõ **lựa chọn ưu tiên**, và ghi câu dự phòng AL vào ghi chú ngữ cảnh.
- `foreign`:
  - WHO_global, "WHO guidelines for malaria", 2026-09-10, locator "Treatment in the first trimester of pregnancy (2022), PDF p.18",
    page_sha256 `4e2c67b2ec74124e…`. Giá trị AL. Đã grep "should be treated with artemether-lumefantrine during the first trimester".
  - US, CDC Appendix A (updated 2026-08-17). Giá trị: AL (ưu tiên), quinine + clindamycin, mefloquine (chỉ khi không còn lựa chọn khác).
    `page_sha256 = null`, `verified_by = null`, needs_human_check.
- `superseded`: 2699/2020 tr. 7 ghi quinin sulfat 7 ngày + clindamycin 7 ngày, **không có AL** (`--find lumefantrin` → []).
  Giá trị giống hiện hành nên không có lệch phiên bản ở slot này.
- `finalize`:
  - tập VN = {Q+C} → **conflict**;
  - tập VN = {Q+C, AL} → conflict chỉ nhờ mefloquine của CDC (lựa chọn cuối cùng, xung đột yếu);
  - tập VN = {Q+C, AL} và chỉ có WHO → concordant.

  Khuyến nghị: dùng tập VN = {Q+C} và ghi rõ lý do.
- Điều kiện chặn: `configs/grading.yaml` chưa có `mefloquine` → câu trả lời "mefloquine" sẽ không đọc được (mục Vấn đề chung).

### D3 — hạt giống 18 (seed `pilot: false`) · dose, num (mg) · primaquin liều đơn cho P. falciparum, ≥ 15 tuổi
- **verdict: fix.**
- Bằng chứng VN (3377 tr. 16):
  - ảnh Bảng 4, cột "P. falciparum, P. knowlesi, P. malariae điều trị 1 lần", hàng **"≥ 15 tuổi" → 4 viên**;
  - tiêu đề bảng ghi viên chứa 7,5 mg primaquin base → 30 mg.
- Lỗi OCR cần lưu ý: OCR đọc "≥ 15 tuổi" thành **"> 15 tuổi"**. Span phải chép đúng OCR (`> 15 tuổi 4 viên 4 viên/ngày 2 viên/ngày`
  → ok), nhưng `population.age` phải ghi **"≥ 15 tuổi"** theo ảnh.
- Span chỉ là một hàng bảng, tên cột nằm xa. Vì vậy `context_checked` phải xác nhận cột "điều trị 1 lần" bằng ảnh.
- 3377 **không còn** ghi mg/kg cho liều đơn: `--find "0,5 mg"` chỉ ra tr. 17 (P. vivax). Khớp báo cáo.
- WHO: tr. 18/180, khuyến cáo (2026) "in low-transmission areas, a single dose of 0.25 mg/kg bw". Việt Nam là vùng lan
  truyền thấp nên khuyến cáo áp dụng được.
- Các trường nên đặt:
  - `context = {weight_kg: 60, mg_per_tablet: 7.5}`;
  - `vn = 30 mg`; WHO 0,25 mg/kg (= 15 mg);
  - `superseded`: 2699 tr. 15 ghi "liều duy nhất 0,5 mg base/kg" (= 30 mg ở 60 kg, **trùng VN**, không lệch phiên bản).
- `finalize`: **conflict**, tol 7,5. `choose_decoy` → mirror_arith **45 mg**, `check_decoy` → [] (hợp lệ).
- CDC: WebFetch không thấy liều đơn cho giao bào → không có đối chiếu US (cần người kiểm).

### D4 — hạt giống 19 · dose, num (mg/kg/day) · P. vivax/P. ovale, G6PD đã xét nghiệm và không thiếu
- **verdict: fix.**
- Bằng chứng VN (3377):
  - tr. 16 có "a) Nếu có kết quả xét nghiệm G6PD";
  - tr. 17 span OCR `- Không thiếu G6PD: liều primaquin: 0,5 mg/kg/ngày x 7 ngày.` → ok. Ảnh trang xác nhận.
  - Không xét nghiệm hoặc bán thiếu (30–70 %) → 0,25 × 14; thiếu (< 30 %) → 0,75 mg/kg/tuần × 8. Báo cáo nêu đúng điều kiện này.
- Sửa 1 — slot và quần thể: **bỏ "liệu trình 7 ngày" khỏi slot.**
  - Lý do: bản cũ 2699 chỉ có phác đồ 0,25 mg base/kg/ngày × **14** ngày (tr. 15), không có phác đồ 7 ngày. Nếu giữ slot
    "7 ngày" thì giá trị bản cũ không cùng slot, và câu hỏi làm lộ thời gian của VN.
  - Slot nên là "liều primaquin mỗi ngày, người lớn, G6PD không thiếu (đã xét nghiệm), không có thai, không cho con bú".
- Sửa 2 — tập giá trị WHO: WHO 10/9/2026 tr. 21/207, "primaquine as anti-relapse therapy (2024)", tổng liều cao 7 mg/kg,
  tức 0,5 mg/kg/ngày × 14 **hoặc** 1 mg/kg/ngày × 7 (1 mg/kg chỉ khi G6PD ≥ 70 %).
  - Vậy WHO values = {0,5; 1,0} mg/kg/day. `finalize` → vẫn **conflict** (nhờ 1,0).
  - WHO chỉ cho phép tổng liều thấp 3,5 mg/kg (0,5 × 7) ở tiểu lục địa Ấn Độ và châu Mỹ. WHO ghi lợi ích liều cao lớn hơn ở
    Đông Nam Á. Điều này củng cố xung đột với VN.
- Sửa 3 — US: **không** ghi "30 mg/ngày" vào mẩu đơn vị mg/kg/day.
  - Nếu ghi như vậy, `_gap` trả `inf` → conflict giả (đã chạy: `finalize` → conflict).
  - Nên ghi hàng trẻ em của CDC "0.5 mg/kg base po qd x 14 days", hoặc quy đổi 30 mg ở 60 kg thành 0,5 mg/kg/day.
    Cả hai đều **trùng VN**, nên US không phải nguồn xung đột (needs_human_check).
- Tafenoquin 300 mg của CDC không phải xung đột: 3377 tr. 9 có "Tafenoquine liều duy nhất (sử dụng sau khi được Bộ Y tế cấp phép…)".
- Sửa 4 — mồi:
  - `choose_decoy` → mirror_geom 0,2, cách giá trị bản cũ 0,25 chỉ 0,05 trong khi 2 × tol = 0,25. `check_decoy` vẫn trả []
    (lỗi #2 còn tồn tại). mirror_far → None.
  - **Chưa có mồi số hợp lệ** theo quy tắc hiện hành. Để trống `decoy` và ghi quyết định (DECISIONS), hoặc sửa quy tắc mồi
    trước khi đóng băng.
- Lệch phiên bản 0,25 → 0,5 là thật (2699 tr. 15 span đã `--find`). Lưu ý bộ đọc số hiện đọc "0,25 mg base/kg/ngày" thành **mg**
  (mục Vấn đề chung).

### D4b — hạt giống 19 · duration (day)
- **verdict: reject.** Đồng ý với báo cáo.
- VN 7 ngày; CDC 14 ngày; WHO {14; 7}; bản cũ 14 ngày → `finalize` = **indistinguishable**.

### D5 — đối chứng "artesunat cho sốt rét ác tính" · dose, num (mg/kg) · trẻ > 20 kg và người lớn
- **verdict: fix** (tạo mẩu concordant; báo cáo đúng về trạng thái).
- Span OCR tr. 11: `Liều gio đầu 2,4 mg/kg, tiêm nhắc lại 2,4 mg/kg vào giờ thứ 12 (ngày đầu).` → ok.
  - Phải giữ nguyên lỗi OCR "gio". Chuỗi đúng chính tả "Liều giờ đầu 2,4 mg/kg" **không** tìm được (`--find` → []).
- Quần thể: ảnh ghi "Trẻ em **>** 20 kg và người lớn" và "Trẻ em **<** 20kg". VN bỏ ngỏ đúng 20 kg; WHO xếp 20 kg vào nhóm
  2,4 mg/kg. Câu hỏi nên dùng người lớn (ví dụ 60 kg).
- Nguồn đối chiếu: WHO tr. 22/218 ghi 2,4 mg/kg ✓. CDC ghi 2,4 mg/kg IV lúc 0, 12, 24 giờ (WebFetch, needs_human_check).
  Bản cũ 2699 tr. 8, 16 ghi 2,4 mg/kg.
- `finalize` → concordant ✓.

### D5b — artesunat tiêm, trẻ < 20 kg
- **verdict: fix — nhãn trong báo cáo SAI.**
- Span OCR tr. 11: `Trẻ em < 20kg liều sử dụng artesunat tiêm là 3mg/kg/lần` → ok. WHO tr. 22 ghi "children weighing < 20 kg … 3 mg/kg bw" ✓.
- **CDC** (WebFetch bảng Appendix A, đọc 2 lần): chú thích nói liều 2,4 mg/kg cho trẻ < 20 kg dựa trên mô hình dược động
  học của FDA, và ghi WHO khuyến cáo 3 mg/kg. Vậy US = 2,4 ≠ VN = 3.
- `finalize` (VN 3; WHO 3; US 2,4; bản cũ 3) → **conflict**, tol 0,3.
- fix:
  - đưa D5b ra khỏi nhóm đối chứng trùng;
  - xem như ứng viên **xung đột chỉ với US** (VN theo WHO), `page_sha256 = null`, needs_human_check;
  - báo cáo phải sửa dòng D5b (trạng thái dự kiến "concordant (chỉ WHO)" → "conflict (US), CDC cần người kiểm").

### Ứng viên: số ngày dùng AL (báo cáo mục 3)
- **verdict: giữ ngoài dữ liệu** (đúng cách xử lý của báo cáo).
- Lần WebFetch độc lập thứ hai của tôi cũng đọc CDC là "Five-day course: Day 1 … Days 2–5: BID dosing".
- VN 3377 Bảng 10 (tr. 19, OCR): "Uống 2 lần/ ngày, liên tục trong 3 ngày". WHO: ACT 3 ngày. 2699 không có AL.
- Nếu người kiểm xác nhận trên trang CDC, đây là xung đột chỉ với US (3 so với 5 ngày), không có bản cũ. Cần xác nhận
  **bằng mắt**, không dựa vào bộ tóm tắt.

---

## 3. Kiểm mục "SAI LỆCH SO VỚI BỘ HẠT GIỐNG" của báo cáo

| Mục báo cáo | Đánh giá |
|---|---|
| 1. Dòng 16 | **Chính xác.** VN đúng. AL là thuốc thay thế thứ 2. WHO tr. 17 liệt kê cả AL, DHA-PPQ và ASPY. Có bản cũ → indistinguishable (tôi đã chạy lại) |
| 2. Dòng 17 | **Chính xác.** Câu dự phòng AL có ở tr. 10. WHO AL 3 tháng đầu là khuyến cáo mạnh (2022) ở tr. 18. Tập CDC khớp WebFetch của tôi |
| 3. Dòng 18 | **Chính xác.** 4 viên × 7,5 mg; bỏ mg/kg; WHO 0,25 mg/kg (2026). Thiếu một ý: OCR đọc sai "≥ 15" |
| 4. Dòng 19 | **Chính xác** về tafenoquin, về liều CDC trùng VN và về WHO 7 mg/kg. Thiếu: slot "7 ngày" làm lệch slot của giá trị bản cũ; WHO 0,5 mg/kg/day cũng thuộc tập WHO; lưu ý vùng của WHO (Đông Nam Á) |
| 5. Đối chứng artesunat | **Một phần sai.** D5 (≥ 20 kg) trùng thật. D5b (< 20 kg) không trùng với CDC (2,4 mg/kg) |
| 6. Lệch phiên bản | **Chính xác cả 6 ý**, tôi đã tự kiểm: DHA-PPQ → Pyramax (2699 tr. 6 / 3377 tr. 9); 0,25 × 14 → 0,5 × 7 (tr. 15 / tr. 17); bỏ "0,5 mg base/kg"; thêm AL dự phòng (2699 không có "lumefantrin"); thêm tafenoquin (2699 không có); thuốc uống sau artesunat tiêm DHA-PPQ → Pyramax (2699 tr. 16 / 3377 tr. 11, 15) |
| 7. Ghi chú kho (bản quét) | Đúng lúc viết; nay đã có OCR |
| Mục 6 — lỗi mã #1 (mirror_decoy) | **Không còn tái hiện**: `decoys.py` dùng `in_atom_unit`; D3 → 45 mg |
| Mục 6 — lỗi mã #2 (check_decoy) | **Còn tồn tại**: D4 mồi 0,2 so với bản cũ 0,25, `check_decoy` = [], trạng thái vẫn "conflict" |
| Mục 6 — lỗi mã #3 (fetch_pdf / sidecar) | **Phần lớn đã có**: `verify_span.pdf_choice()` đọc `data/interim/pdf_choice.json` (chưa tạo file) và sidecar OCR |
| Mục 6 — UNIT_ALIASES | **Còn đúng** (đã chạy `parse_nums`): "0,25 mg base/kg/ngày" → 0,25 **mg**; "0,5 mg base/kg" → 0,5 **mg**; "0,75mg/kg/lần/tuần" → mg/kg (mất "tuần"); "1 gói" → unit None |
| Mục 6 — drugs/combos | **Còn đúng**: grading.yaml thiếu mefloquine, amodiaquine, doxycycline, atovaquone(-proguanil), SP và các combo. Lỗi nhỏ: đề xuất ghi `doxycycline: [doxycyclin, doxycyclin]` (lặp) |

Không phát hiện vi phạm quy tắc cứng trong báo cáo:
- không dùng trang thư viện pháp luật tư nhân;
- trích nguồn nước ngoài ngắn;
- không có trường chỉ bác sĩ mới được điền;
- không ghi mẩu thiếu span.

---

## 4. Vấn đề chung

1. **Chạy lại trích mẩu sốt rét (ưu tiên cao).** Với sidecar OCR, D2, D3, D4, D5, D5b tạo được mẩu có span kiểm tự động.
   - Mọi mẩu phải có `extraction.ocr = true`.
   - Người phải so **từng con số** với ảnh trang (§3.1), dùng `verify_span --image 3377/2023 <trang>`.
   - Báo cáo `malaria_report.md` cần cập nhật: lý do "không có OCR" không còn đúng.
2. **Lỗi OCR đã thấy** (so với ảnh):
   - "≥" → ">" (tr. 16);
   - Bảng 3 Pyramax "1/3 viên", "2/3 viên" → "1⁄4", "2/4" (tr. 16);
   - "Liều giờ đầu" → "Liều gio đầu" (tr. 11);
   - "uống 3 ngày" → "uông 3 ngay" (tr. 9);
   - "liều duy nhất" → "liêu duy nhất" (tr. 9);
   - "P. falciparum" → "P. Jalciparum" (tr. 9).

   Hệ quả:
   - span phải chép **từ OCR** (`--page`), không chép từ bản gõ lại bằng mắt. Nhiều trích đoạn "chép từ ảnh" trong báo cáo
     sẽ không khớp;
   - quần thể và dấu so sánh phải lấy từ ảnh;
   - **không** dùng giá trị trong Bảng 3 Pyramax nếu chưa so với ảnh.
3. **Conflict giả do đơn vị** (`vnsoc.grade._gap`). Hàm trả `inf` khi `Num.to()` không quy đổi được, nên `conflict_status`
   coi giá trị nước ngoài là "conflicting".
   - Ví dụ: CDC "30 mg/day" trong mẩu mg/kg/day → conflict, dù ở 60 kg thì bằng đúng 0,5 mg/kg/day.
   - Đề xuất (không tự sửa): `finalize` báo lỗi hoặc trả trạng thái "unit_unconvertible" thay vì conflict; thêm test.
   - Ảnh hưởng đến hạt giống 19 (CDC ghi "30 mg/ngày").
4. **Mồi sát giá trị bản cũ** (`check_decoy`). Cần loại mồi khi `_gap(mồi, nguồn bất kỳ) < 2 × tol`, không chỉ khi gap = 0.
   Lỗi này làm D4 không có mồi hợp lệ (mirror_far → None). Cần quyết định cách xử lý và ghi vào `docs/DECISIONS.md`.
5. **Bộ đọc số và đơn vị** (`normalize_vi`): thiếu "mg base/kg/ngày", "mg base/kg", "mg base", "mg/kg/tuần" / "mg/kg/lần/tuần"
   và "gói".
   - Hệ quả: câu trả lời của mô hình viết "0.25 mg base/kg/day" sẽ bị đọc thành mg và chấm sai.
   - Giá trị bản cũ 2699 (viết "mg base/kg") cũng không đọc lại được bằng bộ chấm.
6. **Bảng thuốc** (`configs/grading.yaml`): thiếu mefloquine, amodiaquine, doxycycline, atovaquone-proguanil,
   sulfadoxine-pyrimethamine và các combo (artesunate-mefloquine, artesunate-amodiaquine, quinine+doxycycline).
   Phải bổ sung (kèm test) **trước** khi chấm D1/D2.
7. **CDC chặn script (403).** Mọi giá trị US của sốt rét hiện chỉ có WebFetch, nên `page_sha256 = null`, `verified_by = null`,
   needs_human_check. Phải có người mở trang (cập nhật 17/8/2026) để xác nhận:
   - AL 5 ngày;
   - tập thuốc cho 3 tháng đầu;
   - primaquin 30 mg × 14 ngày và quy tắc ≥ 70 kg;
   - **artesunat 2,4 mg/kg cho trẻ < 20 kg**;
   - không có primaquin liều đơn.
8. **Tính hiện hành của 3377/2023** chưa được xác nhận độc lập (hết ngân sách WebSearch; nimpe.vn và impe-qn không truy cập
   được). corpus-librarian cần kiểm trước khi đóng băng kho.
9. **Manifest chưa có** dòng 3377/2023 và 2699/2020 (`data/interim/manifest_parts/` trống). Nên ghi:
   - 3377/2023: `text_layer: false`, `ocr: true` (sidecar tesseract 5.4, vie, 300 dpi);
   - 2699/2020: superseded_by 3377/2023.
10. **Hệ thống nguồn:** WHO_global là đúng cho WHO guidelines for malaria. Không cần WHO_WPRO: tôi không thấy khuyến cáo điều
    trị riêng của WPRO trong phạm vi đã kiểm.
