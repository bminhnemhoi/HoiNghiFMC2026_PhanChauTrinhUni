# T1.1 thí điểm — Sốt rét (ID = malaria) — báo cáo agent

Ngày: 2026-09-26 · agent: claude (atom-extractor + counterpart-matcher) · file mẩu: `data/interim/pilot/malaria.jsonl`

## Tóm tắt (đọc trước)

- **Số mẩu đã ghi: 0.** Văn bản hiện hành QĐ 3377/QĐ-BYT (30/8/2023) chỉ có **bản quét không có lớp chữ**
  (`text_kind = scanned_or_empty`) ở cả 3 bản chính thức tìm được. Máy chưa có OCR, nên `verify_span` không kiểm
  được span nào. Theo quy tắc cứng của task, tôi **không tạo mẩu** từ văn bản này. `malaria.jsonl` để rỗng (0 dòng)
  và vẫn qua `vnsoc.schemas atom` và `verify_span` (0 dòng, 0 lỗi).
- Bản cũ QĐ 2699/QĐ-BYT (26/6/2020) **có lớp chữ** (ký số VGCA). Đã tải vào `data/raw/2699_2020.pdf` và kiểm được
  span cho các giá trị bản cũ (mục 2 và 4).
- Tôi đã **đọc bằng mắt** các trang quét của 3377/2023 (ảnh dựng từ PDF chính thức) để đối chiếu với bảng hạt giống.
  Tôi cũng đã tải và grep nguồn WHO hiện hành (WHO guidelines for malaria, **10/9/2026**). **CDC chặn tải bằng script
  (403)**, nên giá trị CDC chỉ đọc được bằng WebFetch (page_sha256 = null, needs_human_check).
- **Bảng hạt giống có sai lệch đáng kể** ở cả 4 dòng 16–19 (xem mục 4). Nói ngắn: (i) 3377/2023 có
  artemether–lumefantrin làm thuốc thay thế/dự phòng cho cả dòng 16 và 17; (ii) tafenoquin **có** trong 3377/2023,
  nên phương án tafenoquin của CDC ở dòng 19 không phải xung đột; (iii) xung đột thật của dòng 19 là với WHO 2024+
  (tổng liều cao 7 mg/kg), không phải về liều mỗi ngày của CDC. Ngoài ra, dòng 16 (có bản cũ) và thời gian điều trị
  ở dòng 19 sẽ thành `indistinguishable` theo `vnsoc.grade.conflict_status`.

---

## 1. Văn bản đã tải / đã kiểm

| Khóa | Vai trò | URL (nguồn) | sha256 (16) | Trang | text_kind | Trạng thái |
|---|---|---|---|---|---|---|
| 3377/2023 | hiện hành | https://benhvienhatrung.vn/wp-content/uploads/2023/09/Huong-dan-chan-doan-va-dieu-tri-benh-sot-ret.pdf (BVĐK Hà Trung đăng lại bản **sao y của Sở Y tế Thanh Hóa**, dấu "Sao y; Sở Y Tế; 31/08/2023") | `aa1792688e9dda03` | 23 | **scanned_or_empty** | downloaded → `data/raw/3377_2023.pdf` |
| 2699/2020 | bản cũ (bị thay) | http://quantri.impe-qn.org.vn//Data/impeqn/old/upload/info/attach/1593593404164_HDchandoandieutriSR2020.pdf (Viện Sốt rét–KST–CT Quy Nhơn, mục "Văn bản của Bộ Y tế") | `8bc1a6b403476197` | 30 | ok | downloaded → `data/raw/2699_2020.pdf` |

Xác nhận danh tính:
- **3377/2023:** trang PDF 1 (ảnh) ghi "Số: 3377 /QĐ-BYT", "Hà Nội, ngày 30 tháng 8 năm 2023", KT. Bộ trưởng – Thứ
  trưởng Trần Văn Thuấn. Điều 1: thay thế hướng dẫn ban hành kèm QĐ 2699/QĐ-BYT ngày 26/06/2020. Điều 2: hiệu lực từ
  ngày ký. Lớp chữ chỉ có dấu văn thư ("syt_thanhhoa_vt_So Y te Thanh Hoa_30/08/2023 10:10:01 3377 30 8 / Sao y…").
  Producer: ShinPFUPDF (máy quét) + iTextSharp.
- **2699/2020:** file hướng dẫn để trống số ("Số: /", "ngày tháng 6 năm 2020"), ký số VGCA lúc 26/06/2020 16:14:40.
  Trên cùng trang danh mục IMPE-QN có file quyết định kèm theo
  (…/1593593395504_2699QDBYT.pdf, 2 trang, có lớp chữ, "Số: 2699/QĐ-BYT … ngày 26 tháng 6 năm 2020", ký VGCA
  26/06/2020 16:14:20; sha256 `0eed96d3fef735b2`; chỉ lưu ở scratchpad, **không** đưa vào data/raw).

Các bản khác của 3377/2023 đã thử (không đưa vào data/raw):

| Nơi | Kết quả |
|---|---|
| Viện SR–KST–CT Quy Nhơn: http://quantri.impe-qn.org.vn//Data/impeqn/old/upload/info/attach/1701315127056_quyetdinh3377qdbyt2023huongdanchandoanvadieutribenhsotret.pdf | PDF 23 trang, **không có lớp chữ** (Foxit PhantomPDF Printer, 31/08/2023); sha256 `2034f0c5aee904a5` |
| BV Tân Bình (Sở Y tế TP.HCM chuyển): https://bvtb.org.vn/wp-content/uploads/2023/10/8224_SYT_NVD.pdf | 26 trang, bản quét RICOH, **không có lớp chữ**; sha256 `8f57ad31ae25f448` |
| Sở Y tế Quảng Ninh (congchuc.quangninh.gov.vn DownloadFile.aspx) | Phải **đăng nhập** mới tải được |
| binhphuoc.gov.vn | ECONNREFUSED |
| trungtamytehocmon.medinet.gov.vn (trang văn bản 3377) | 404 (trang đã đổi địa chỉ) |
| kcb.vn (/phac-do: 52 mục; tìm kiếm "sốt rét") | Không có mục sốt rét; tìm kiếm trả `totalItems: 0` |
| moh.gov.vn | Chỉ có bài tin/tuyên truyền, không có file quyết định |

Nhận định: Bộ Y tế phát hành 3377/2023 dưới dạng **ảnh quét** của bản ký tay. Có thể không tồn tại bản chính thức
có lớp chữ. Các trang thư viện pháp luật tư nhân có bản gõ lại, nhưng tôi **không dùng** vì không phải nguồn chính thức.

Nguồn nước ngoài:

| Nguồn | URL | fetched_at | page_sha256 (16) | Ghi chú |
|---|---|---|---|---|
| WHO guidelines for malaria, **10 September 2026** (MAGICapp PDF, 494 tr.) | https://iris.who.int/server/api/core/bitstreams/d3c6488b-3ee6-41cb-960f-ddf0202cd74d/content | 2026-09-26 | `4e2c67b2ec74124e` | bản hiện hành (doi 10.2471/B09879); bản trước: 13/8/2025 (B09514), 30/11/2024 (B09146) |
| WHO "Version updates to the WHO guidelines for malaria" | https://cdn.who.int/media/docs/default-source/malaria/version-updates-to-the-who-guidelines-for-malaria.pdf?sfvrsn=8a667008_5 | 2026-09-26 | `63a9f8775767f597` | xác nhận lịch sử phiên bản: 25/11/2022 (điều trị, liều chống tái phát), 30/11/2024 (G6PD, primaquin, tafenoquin), 10/9/2026 (primaquin liều đơn…) |
| CDC "Appendix A: Malaria in the United States Treatment Tables" | https://www.cdc.gov/malaria/hcp/clinical-guidance/appendix-a-treatment-tables.html | 2026-09-26 (WebFetch) | **null** | `vnsoc.match.sources fetch` → **403**; PDF bảng 2023 cũ → 404. Chỉ đọc qua WebFetch (trang ghi "Published July 9, 2026; Updated and Reviewed August 17, 2026") → **needs_human_check** |

---

## 2. Bảng mẩu

**Không có mẩu nào được ghi** (0/0). Bảng dưới là **mẩu dự thảo, CHƯA ghi vào JSONL**. Giá trị VN đọc bằng mắt từ
ảnh quét 3377/2023 (số trang = trang PDF 1-based). Giá trị bản cũ 2699/2020 đã kiểm span bằng
`verify_span --find`. Trạng thái dự kiến tính bằng `finalize()` trên dict trong bộ nhớ, không ghi file.

| Dự thảo | Hạt giống | Slot | VN 3377/2023 (trang PDF, đọc từ ảnh) | Nước ngoài | Bản cũ 2699/2020 (trang, span đã kiểm) | Trạng thái dự kiến |
|---|---|---|---|---|---|---|
| D1 | 16 | first_line, drugs — P. falciparum không biến chứng, không thai | pyronaridine-artesunate 3 ngày + primaquin liều duy nhất (tr. 9, mục III.2.1.a "Điều trị đặc hiệu ưu tiên"); thay thế theo thứ tự: AS-MQ, AL, AS-AQ, DHA-PPQ, quinin + clindamycin/doxycyclin (tr. 9, mục b) | US (CDC 2026, needs_human_check): AL ưu tiên; atovaquone-proguanil; quinine + doxycycline; mefloquine. WHO_global (10/9/2026, tr. 17): AL, AS+AQ, AS-MQ, DHA-PPQ, AS+SP, AS-PY (2022) | DHA-PPQ 3 ngày + primaquin liều duy nhất (tr. 6) | **indistinguishable** (WHO có DHA-PPQ = bản cũ). Bỏ bản cũ thì là conflict |
| D2 | 17 | first_line, drugs — P. falciparum không biến chứng, thai 3 tháng đầu | quinin sulfat 7 ngày + clindamycin 7 ngày; **"Trường hợp không có quinin sulfat, có thể dùng artemether - lumefantrin"** (tr. 10, mục 2.2.1.a) | US (CDC 2026, needs_human_check): AL (mọi tam cá nguyệt, ưu tiên), quinine + clindamycin, mefloquine (khi không có lựa chọn khác). WHO_global (tr. 18, khuyến cáo 2022): AL trong 3 tháng đầu | quinin sulfat 7 ngày + clindamycin 7 ngày, **không** có AL (tr. 7) | conflict. Tập VN chỉ gồm thuốc ưu tiên → xung đột US + WHO (AL). Tập VN gồm cả AL dự phòng → chỉ xung đột CDC (mefloquine) |
| D3 | 18 | dose, num (mg) — primaquin liều đơn cho P. falciparum, ≥ 15 tuổi (cần cân nặng, ví dụ 60 kg) | Bảng 4 "Primaquin (viên chứa 7,5 mg primaquin base)": ≥ 15 tuổi → 4 viên (= 30 mg) (tr. 16) | WHO_global (tr. 18/180, cập nhật **2026**): 0,25 mg/kg liều đơn kèm ACT ở vùng lan truyền thấp. US: CDC không có dòng liều đơn | 0,5 mg base/kg liều đơn; ≥ 15 tuổi 4 viên (tr. 15), trùng VN | conflict (WHO). Mồi tự động sai do lỗi mã (mục 6) |
| D4 | 19 | dose, num (mg/kg/day) — P. vivax, G6PD bình thường **đã xét nghiệm**, liệu trình 7 ngày | "Không thiếu G6PD: liều primaquin: 0,5 mg/kg/ngày x 7 ngày" (tr. 17) | WHO_global (tr. 20–21, 2024): tổng liều cao 7 mg/kg = 0,5 mg/kg/ngày × 14 ngày **hoặc 1 mg/kg/ngày × 7 ngày** (G6PD ≥ 70%); 0,5 × 7 là phương án 3,5 mg/kg. US (CDC, needs_human_check): 30 mg base/ngày × 14 ngày (≈ 0,5 mg/kg/ngày); trẻ em 0,5 mg/kg/ngày × 14 | **0,25 mg base/kg/ngày × 14 ngày** (tr. 15) | conflict (WHO 1 mg/kg/ngày) **kèm lệch phiên bản** (0,25 → 0,5). Mồi hình học 0,2 sát giá trị bản cũ 0,25 (mục 6) |
| D4b | 19 | duration, num (day) — cùng quần thể | 7 ngày (tr. 17) | US: 14 ngày; WHO: 14 hoặc 7 ngày | 14 ngày (tr. 15) | **indistinguishable** (CDC 14 = bản cũ 14) → loại |
| D5 | đối chứng | dose, num (mg/kg) — artesunat tiêm, sốt rét ác tính, trẻ > 20 kg và người lớn | 2,4 mg/kg giờ đầu, nhắc lại giờ 12, rồi mỗi ngày 1 liều (tr. 11, mục 2.3.b; Bảng 1 tr. 15) | WHO_global (tr. 22): 2,4 mg/kg (≥ 20 kg); US (CDC, needs_human_check): 2,4 mg/kg IV lúc 0, 12, 24 giờ | 2,4 mg/kg (tr. 8, 16) | concordant |
| D5b | đối chứng | dose — artesunat tiêm, trẻ < 20 kg | 3 mg/kg/lần (tr. 11) | WHO (tr. 22): 3 mg/kg; CDC: chưa rõ | 3 mg/kg (tr. 8) | concordant (chỉ WHO) |

Trích đoạn 3377/2023 **tôi tự chép từ ảnh, chưa kiểm tự động** (để OCR/người đối chiếu ở HG1.2; không dùng làm span):
- tr. 9: "Sốt rét do P. falciparum đơn thuần hoặc phối hợp P. falciparum với P. malariae hoặc P. knowlesi: Pyronaridin
  tetraphosphat - artesunat (Pyramax) uống 3 ngày (xem Bảng 2 hoặc 3) và primaquin liều duy nhất (xem Bảng 4)."
- tr. 9: "Sốt rét do P. vivax hoặc P. ovale: Chloroquin uống 3 ngày (xem Bảng 5) hoặc Pyronaridin tetraphosphat -
  artesunat (Pyramax) uống 3 ngày (xem Bảng 2 hoặc 3) và primaquin uống 7 ngày hoặc 14 ngày (xem Bảng 4) hoặc
  Tafenoquine liều duy nhất (sử dụng sau khi được Bộ Y tế cấp phép lưu hành, liều dùng theo hướng dẫn của nhà sản xuất)."
- tr. 10: "+ Thuốc điều trị là quinin sulfat 7 ngày (xem Bảng 6) + clindamycin 7 ngày (xem Bảng 7). + Trường hợp không
  có quinin sulfat, có thể dùng artemether - lumefantrin (xem Bảng 10)."
- tr. 11: "+ Trẻ em > 20 kg và người lớn: Liều giờ đầu 2,4 mg/kg, tiêm nhắc lại 2,4 mg/kg vào giờ thứ 12 (ngày đầu)."
- tr. 17: "- Không thiếu G6PD: liều primaquin: 0,5 mg/kg/ngày x 7 ngày." · "- Bán thiếu G6PD (hoạt độ G6PD từ 30 - 70%
  hoạt độ G6PD ở người bình thường), liều primaquin: 0,25 mg/kg/ngày x 14 ngày." · "b) Nếu không có xét nghiệm G6PD:
  liều pimaquin 0,25mg/kg/ngày x 14 ngày" (bản gốc viết sai chính tả "pimaquin").

Đánh số trang: trang PDF = số in + 1 ở phần chính (ví dụ PDF 9 = trang in 8). Phụ lục I đánh số lại từ đầu
(PDF 16 = PL tr. 2, PDF 17 = PL tr. 3).

---

## 3. Ứng viên bị loại + lý do

| Ứng viên | Lý do loại |
|---|---|
| Toàn bộ mẩu từ 3377/2023 (D1–D5b) | PDF chính thức là bản quét (`scanned_or_empty`), máy không có OCR → `verify_span` không kiểm được. Loại theo quy tắc cứng; chờ OCR/HG |
| D1 (hạt giống 16) | Kể cả khi có OCR: theo `conflict_status` là `indistinguishable` vì WHO liệt kê DHA-PPQ, trùng giá trị bản 2699/2020. Ngoài ra khác biệt với VN chỉ nằm ở **thứ tự ưu tiên** (AL là thuốc thay thế thứ 2 trong 3377) |
| D4b (thời gian primaquin P. vivax) | `indistinguishable`: 14 ngày của CDC trùng 14 ngày của bản 2699/2020 |
| P. vivax "không có xét nghiệm G6PD" (0,25 × 14) | WHO chỉ nói cân nhắc lợi/hại; CDC bắt buộc xét nghiệm → `no_counterpart` |
| Tafenoquin cho P. vivax | 3377 cũng có tafenoquin (sau khi được cấp phép) → không phải xung đột. WHO 2024 chỉ khuyến cáo tafenoquin cho Nam Mỹ |
| **Ứng viên mới (chưa kiểm)**: số ngày dùng AL | 3377 Bảng 10 (tr. 19): AL uống 2 lần/ngày × 3 ngày. WebFetch trang CDC 2026 ghi "Five-day course" (ngày 1: 2 liều; ngày 2–5: 2 lần/ngày). WHO: ACT 3 ngày. **Không kiểm được**, vì CDC 403 với script và kết quả WebFetch có thể do bộ tóm tắt đọc sai. Không dùng khi người chưa mở trang xác nhận |

---

## 4. SAI LỆCH SO VỚI BỘ HẠT GIỐNG (§3.3 / seed_conflicts.yaml)

1. **Dòng 16 (thuốc đầu tay P. falciparum):**
   - Giá trị VN đúng: pyronaridin–artesunat 3 ngày + primaquin liều duy nhất.
   - Nhưng 3377 liệt kê AL là thuốc **thay thế thứ 2** (khi không có Pyramax). Vậy khác biệt với CDC là về **thứ tự
     ưu tiên**, không phải về tập giá trị. Đây là cùng loại lý do đã khiến dòng 12 bị loại.
   - Nhãn "WHO chấp nhận cả hai → chỉ xung đột với Mỹ" chưa chính xác. WHO 2026 liệt kê 6 ACT (có AL và DHA-PPQ),
     nên câu trả lời AL khớp **cả US và WHO**. Câu trả lời DHA-PPQ khớp cả WHO lẫn bản cũ 2699/2020, vì vậy mẩu thành
     `indistinguishable` khi ghi bản cũ.
   - Trạng thái đề xuất: `confirmed_us_only` → **complex / indistinguishable**.
2. **Dòng 17 (3 tháng đầu thai kỳ):**
   - 3377 **thêm** "Trường hợp không có quinin sulfat, có thể dùng artemether - lumefantrin" (bảng hạt giống không
     nhắc tới).
   - WHO khuyến cáo AL cho 3 tháng đầu từ bản 25/11/2022 (khuyến cáo mạnh, còn trong bản 10/9/2026). Vậy xung đột
     (về lựa chọn ưu tiên) là với **cả WHO_global**, không chỉ CDC.
   - CDC có một **tập** giá trị: AL (ưu tiên), quinine + clindamycin (trùng VN), mefloquine (ngoài tập VN).
   - Cần quyết định có tính AL dự phòng vào tập VN hay không (mục 5).
3. **Dòng 18 (primaquin liều đơn, ≥ 15 tuổi):**
   - Giá trị VN đúng: 4 viên × 7,5 mg base = 30 mg (Bảng 4).
   - 3377 **không còn ghi mg/kg** cho liều đơn. Bản 2699 ghi "0,5 mg base/kg"; 3377 chỉ còn bảng theo tuổi.
   - WHO 0,25 mg/kg đã được **khẳng định lại trong bản 10/9/2026** (vùng lan truyền thấp).
   - CDC không có liều đơn → xung đột chỉ với WHO.
4. **Dòng 19 (P. vivax, G6PD bình thường):**
   - "0,5 mg/kg/ngày × 7 ngày" đúng, nhưng **chỉ khi đã xét nghiệm và G6PD bình thường**. Không xét nghiệm hoặc bán
     thiếu → 0,25 × 14.
   - "Tafenoquin 300 mg (CDC)" **không phải xung đột**, vì 3377 có tafenoquin liều duy nhất (sau khi được cấp phép).
   - CDC 30 mg/ngày ≈ 0,5 mg/kg/ngày → **trùng liều mỗi ngày** với VN. Xung đột CDC chỉ còn ở số ngày (14), mà
     14 ngày lại trùng bản 2699 → `indistinguishable`.
   - Xung đột rõ nhất là với **WHO 2024+**: tổng liều cao 7 mg/kg (1 mg/kg/ngày × 7 ngày hoặc 0,5 × 14). Hạt giống
     không ghi điểm này.
   - Mẩu này còn là mẩu **lệch phiên bản**: 2699/2020 dùng 0,25 mg/kg/ngày × 14 ngày.
5. **Đối chứng "artesunat cho sốt rét ác tính": xác nhận trùng** (2,4 mg/kg; trẻ < 20 kg 3 mg/kg = WHO).
   Có thay đổi phiên bản ở thuốc uống chuyển tiếp: DHA-PPQ (2699) → Pyramax (3377).
6. **Lệch phiên bản 2699/2020 → 3377/2023 (đã đọc cả hai):**
   - thuốc ưu tiên P. falciparum: DHA-PPQ → Pyramax;
   - primaquin P. vivax cho G6PD bình thường: 0,25 × 14 → 0,5 × 7;
   - bỏ ghi "0,5 mg base/kg" cho liều đơn;
   - thêm AL dự phòng cho 3 tháng đầu;
   - thêm tafenoquin;
   - thuốc uống sau artesunat tiêm: DHA-PPQ → Pyramax.
7. **Ghi chú kho:** bảng hạt giống và đề cương không nhắc rằng PDF 3377/2023 chỉ có bản quét. Phần sốt rét (4/13 dòng
   xung đột thí điểm, 1 đối chứng) vì thế phụ thuộc vào OCR.

---

## 5. Việc cần người kiểm ở HG1.2

1. **Quyết định cách xử lý PDF quét 3377/2023** (chặn toàn bộ mẩu sốt rét). Hai hướng:
   - (a) cài Tesseract + gói `vie` + ocrmypdf, tạo bản OCR, rồi **so tay mọi con số với ảnh trang** (đề cương §4.1);
   - (b) xin bản ký số có lớp chữ từ Cục QLKCB hoặc Viện SR–KST–CT Trung ương.

   Lưu ý: `data/raw/3377_2023.pdf` hiện là bản quét. Nếu tải được bản có chữ, `fetch_pdf` sẽ lưu thành
   `3377_2023__<sha8>.pdf` và `verify_span` sẽ **không** đọc tới file đó. Cần người hoặc corpus-librarian xử lý tên file
   (tôi không được xóa hay đổi tên trong data/raw).
2. **Kiểm CDC bằng tay** (trang 403 với script):
   - xác nhận AL "Five-day course" hay 3 ngày;
   - tập thuốc cho thai kỳ (AL / quinine + clindamycin / mefloquine; atovaquone-proguanil không có);
   - primaquin 30 mg × 14 ngày và quy tắc ≥ 70 kg (tổng 6 mg/kg);
   - liều artesunat cho trẻ < 20 kg;
   - ngày cập nhật 17/8/2026.
3. **Quyết định khoa học:** với dòng 16 và 17, khi VN cho phép AL làm thuốc thay thế hoặc dự phòng, ta (i) giữ slot
   "thuốc ưu tiên" với tập VN chỉ gồm lựa chọn thứ nhất, câu hỏi phải nói rõ "ưu tiên"; hay (ii) coi là khác biệt thứ tự
   ưu tiên và loại như dòng 12? Đề xuất: (i) cho dòng 17, ghi rõ ở báo cáo; dòng 16 để ngoài phân tích xác nhận vì
   `indistinguishable`.
4. **Tafenoquin đã được Bộ Y tế cấp phép lưu hành chưa?** Điều này quyết định tafenoquin có thuộc tập VN hiện hành
   (có điều kiện) hay không.
5. Đối chiếu các **trích đoạn tôi tự chép từ ảnh** (mục 2) với ảnh trang.
6. Xác nhận file hướng dẫn 2699/2020 (để trống số) đúng là phụ lục của QĐ 2699/QĐ-BYT. Cơ sở: cùng trang danh mục
   IMPE-QN, ký số VGCA cùng ngày 26/06/2020, file QĐ ký trước 20 giây.

---

## 6. Đề xuất bổ sung configs / mã (không tự sửa)

**configs/grading.yaml – drugs** (thiếu, cần cho sốt rét):
- `mefloquine: [mefloquin]`
- `amodiaquine: [amodiaquin]`
- `doxycycline: [doxycyclin, doxycyclin]`
- `atovaquone: [atovaquon]`
- `proguanil: []`
- `atovaquone-proguanil: [malarone]`
- `sulfadoxine-pyrimethamine: [sp, fansidar]`

**combos:**
- `artesunate-mefloquine: [artesunate, mefloquine]`
- `artesunate-amodiaquine: [artesunate, amodiaquine]`
- `quinine+doxycycline: [quinine, doxycycline]`
- `atovaquone-proguanil: [atovaquone, proguanil]`
- `artesunate+sulfadoxine-pyrimethamine: [artesunate, sulfadoxine-pyrimethamine]`

Lưu ý: `parse_drugs` gộp combo theo thứ tự khai báo. `artesunate` có mặt trong ≥ 3 combo nên cần test thứ tự.

**normalize_vi.UNIT_ALIASES** (đã thử bằng `parse_nums`):
- "0,25 mg base/kg/ngày" hiện bị đọc thành **0,25 mg** (sai đơn vị). Cần thêm `"mg base/kg/ngày"→mg/kg/day`,
  `"mg base/kg"→mg/kg`, `"mg base"→mg`.
- "0,75mg/kg/lần/tuần" bị đọc thành mg/kg (mất "tuần"). Cần đơn vị `mg/kg/week` với các alias
  "mg/kg/tuần", "mg/kg/lần/tuần".
- Thêm `"gói"→sachet` (Pyramax dạng bột).

**Lỗi mã phát hiện khi chạy thử trong bộ nhớ:**
1. `vnsoc.match.decoys.mirror_decoy` **không quy đổi đơn vị** của giá trị nước ngoài trước khi phản chiếu (dùng thẳng
   `f["lo"]`). Với D3: VN 30 mg, WHO 0,25 mg/kg (context weight_kg = 60) → mồi ra **59,75 mg** thay vì 45 mg. Sửa:
   đổi `f` và `v` sang `atom["unit"]` bằng `nv.Num(...).to(unit, context)` trước khi tính.
2. `check_decoy` chỉ loại mồi trùng đúng (gap = 0) với nguồn đã ghi, **không** loại mồi nằm trong 2 × dung sai của một
   giá trị bản cũ. Với D4: mồi `mirror_geom` 0,25 được làm tròn thành 0,2, cách giá trị bản cũ 0,25 chỉ 0,05 khi dung sai
   là 0,125 → đáp án "0,25" khớp cả bản cũ và mồi. Đề xuất: loại mồi khi `_gap(mồi, nguồn) < 2 × tol`.
3. `fetch_pdf`: bản tải đầu tiên chiếm khóa chuẩn **kể cả khi là bản quét**. Đề xuất: bản `scanned_or_empty` lưu thành
   `<key>__scan.pdf` (hoặc hỏi trước) để bản có chữ tải sau vẫn nằm ở khóa chuẩn. `verify_span` cũng nên hỗ trợ
   sidecar OCR (`<key>.ocr.pdf`) và ghi `ocr: true` vào manifest.

**Manifest:** chưa cập nhật (không thuộc quyền ghi của task này). Đề xuất corpus-librarian thêm hai dòng:
- `3377/2023`: current, `text_layer: false`, `ocr` cần làm;
- `2699/2020`: superseded, `superseded_by: [3377/2023]`, `text_layer: true`.
