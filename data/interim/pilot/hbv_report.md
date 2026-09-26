# Báo cáo thí điểm T1.1 — Viêm gan vi rút B (ID = hbv)

Ngày: 2026-09-26 · Agent: atom-extractor + counterpart-matcher (claude) · File mẩu: `data/interim/pilot/hbv.jsonl` (10 mẩu)

Kiểm tra đã chạy:
- `python -m vnsoc.schemas atom data/interim/pilot/hbv.jsonl`: **OK 10 dòng**
- `python -m vnsoc.extract.verify_span data/interim/pilot/hbv.jsonl`: **OK, 0 mẩu không đạt**
- `tolerance` và `conflict_status` đều do `finalize()` tính. Tôi đã chạy lại và ra đúng các giá trị trong file.

**Tóm tắt trung thực.** Bộ hạt giống dòng 20 coi "30/19 U/L (Việt Nam) so với 35/25 U/L (AASLD)" là một xung đột đã xác nhận. Khi đọc bản 3310/2019 chính thức, tôi thấy chính Bộ Y tế đã dùng ULN = 35 U/L (nam) và 25 U/L (nữ). Bản 3310/2019 còn dùng ALT > 2×ULN và HBV DNA ≥ 20.000 IU/mL khi HBeAg dương tính. Cả ba giá trị này trùng AASLD 2025. Vì vậy mọi khác biệt Việt Nam–Mỹ của dòng 20 đều **không phân biệt được** với lệch phiên bản 3310/2019 → 1740/2026 (`indistinguishable`). Chúng không phải xung đột sạch. Đây là kết quả trái kỳ vọng của bảng §3.3, xem mục 4.

> **Cập nhật sau kiểm toán độc lập (2026-09-26).** Số liệu dưới đây đã sửa theo kiểm toán `hbv_verify.md`. Chi tiết đã sửa gì, giữ gì và vì sao ở **mục 7**. Các mục 1–6 giữ nội dung gốc; chỗ nào đã sai được đánh dấu "(sau kiểm toán: …)".

Kết quả 10 mẩu (sau kiểm toán):
- **1 mẩu `conflict`: P-hbv-07** (AASLD 2025, ≥ 2 năm). Mẩu này mong manh, xem mục 7.
- **6 mẩu `indistinguishable`**: 01, 02, 03, 04, 08, 10. P-hbv-08 trước là `conflict`. Nó đổi trạng thái vì 3310/2019 có nhánh 2 (> 30 tuổi, HBV DNA > 20.000), trùng giá trị WHO 2015.
- 3 mẩu `concordant`: 05, 06, 09.
- 6 mẩu có lệch phiên bản thật (giá trị bản cũ khác giá trị hiện hành): 01, 02, 03, 04, 09, 10. P-hbv-07 có thêm một giá trị 5448/2014 suy ra (≥ 1 năm).
- Trước kiểm toán, báo cáo ghi 2 mẩu `conflict`: 07, và 08 (chỉ xung đột với WHO 2015). Con số đó sai.

---

## 1. Văn bản đã tải

### Văn bản Bộ Y tế (qua `vnsoc.extract.fetch_pdf`)

**1740/2026 → `data/raw/1740_2026.pdf`**
- Nguồn: kcb.vn, https://kcb.vn/upload/2005611/20260617/BYT__QD_ban_hanh_HDCDT_viem_gan_vi_rut_B_-_final_2_signed_8c1b5.pdf
- sha256 (16): `e7723a0bda785a39` · 42 trang · text_kind `ok`
- Tìm thấy qua trang kcb.vn/tin-tuc "Quyết định 1740/QĐ-BYT ban hành tài liệu chuyên môn…" (đăng 17/6/2026).
- Lớp chữ để trống số hiệu ("Số: /QĐ-BYT"). Danh tính được xác nhận bằng: tiêu đề; dòng chữ ký số "tienph.kcb_…_17/06/2026 … 1740 16 6"; Điều 3 thay thế QĐ 3310/QĐ-BYT ngày 29/7/2019; và trang tin kcb.vn.
- Số trang in = số trang PDF − 11 (ví dụ tr.PDF 20 = tr. in 9).

**3310/2019, bản quét chính thức → `data/raw/3310_2019__c43006cb.pdf` (status `clash_kept_both`)**
- Nguồn: Sở Y tế TP.HCM (medinet), https://admin.medinet.gov.vn/%2fdata%2fsoytehcm%5csoytehcm%5cattachments%2f2019_8%2f07%2f4238-syt-nvy_78201920.pdf
- sha256 (16): `c43006cb69cb517f` · 18 trang · text_kind **`scanned_or_empty`**
- Tìm thấy qua trang medinet "V/v triển khai Hướng dẫn chẩn đoán, điều trị bệnh viêm gan vi rút B" (CV 4238/SYT-NVY ngày 07/8/2019).
- Trang 2 là QĐ 3310/QĐ-BYT ngày 29/7/2019, có dấu "ĐẾN 30-07-2019". Trang 3–18 là toàn văn hướng dẫn và phụ lục.
- Không có OCR, nên **không kiểm span bằng máy được**. Tôi chỉ dùng văn bản này cho giá trị bản cũ (`superseded`), chép tay từ ảnh trang, và đánh dấu `visual_transcription_scan`.

**"3310/2019", bản đăng lại của BVĐK Hà Trung → `data/raw/3310_2019.pdf`**
- Nguồn: https://benhvienhatrung.vn/wp-content/uploads/2022/06/3310-2019-hddt-viem-gan-b.pdf
- sha256 (16): `e2b720f885e9c262` · 8 trang · text_kind `ok`
- **SAI NHÃN — KHÔNG DÙNG.** Tiêu đề ghi "Ban hành kèm theo QĐ 3310/QĐ-BYT ngày 29/07/2019", nhưng nội dung là hướng dẫn 5448/2014. Bằng chứng:
  - Mọi câu then chốt (ALT "trên 2 lần giá trị bình thường", "HBV-DNA ≥ 105 copies/ml (20.000 IU/ml)", "Tenofovir (300mg/ngày) hoặc entecavir", "3 lần xét nghiệm liên tiếp cách nhau mỗi 6 tháng") đều có nguyên văn trong 5448/2014 tải từ kcb.vn.
  - Tỉ lệ giống văn bản là 0,835.
  - Cấu trúc hoàn toàn khác bản 3310 chính thức, vốn có mục 2.4.2, Bảng 1 có TAF, Phụ lục 1–2.

**5448/2014 → `data/raw/5448_2014.pdf`**
- Nguồn: kcb.vn/thu-vien-tai-lieu, https://kcb.vn/upload/2005611/20210723/Hướng-dẫn-chẩn-đoán-và-điều-trị-bệnh-viêm-gan-vi-rút-B.pdf (dạng mã hóa URL)
- sha256 (16): `67bc6b58cd69c3b8` · 10 trang · text_kind `ok`
- Tìm thấy qua trang kcb.vn "Hướng dẫn chẩn đoán, điều trị bệnh viêm gan vi rút B". Đây là bản trước 3310. Tôi tải về để đối chứng, và nó cũng là một bản Bộ Y tế đã bị thay (5448/2014 → 3310/2019 → 1740/2026).

Chuỗi thay thế đã xác nhận:
- 1740/2026 Điều 3 thay 3310/2019.
- 3310/2019 Điều 2 bãi bỏ 5448/2014 (đọc trên ảnh trang 2 của bản quét).

### Nguồn nước ngoài (qua `vnsoc.match.sources fetch`; chỉ lưu giá trị, vị trí và băm, không lưu đoạn văn)

**AASLD 2025 → dùng làm `US`**
- Tên: AASLD Practice Guideline on Treatment of CHB (Ghany et al., Hepatology 2025), bộ slide giáo dục "Practical Application of HBV Guidelines".
- URL: https://www.aasld.org/sites/default/files/2025-11/CHB%20Educational%20Slide%20Set%20Final%202.pdf
- sha256 (16): `763a79fe35c57c68` · PDF 46 trang (= 46 slide)

**WHO 2024 → dùng làm `WHO_global`**
- Tên: WHO Guidelines for the prevention, diagnosis, care and treatment for people with CHB infection (29/3/2024).
- URL: https://iris.who.int/server/api/core/bitstreams/34470cc8-af90-4d7b-a949-ef27e5d0726f/content
- sha256 (16): `e44231194db4a3c7` · 275 trang
- Link IRIS dạng `bitstream/handle/...` chỉ trả HTML rỗng. Link đúng lấy từ trang who.int/publications.

**WHO 2015 → dùng làm `WHO_global`, ghi là bản trước (chỉ ghi khi giá trị khác WHO 2024)**
- Tên: WHO Guidelines for the prevention, care and treatment of persons with CHB infection (3/2015).
- URL: https://iris.who.int/server/api/core/bitstreams/51bfba1f-fbbe-4ae3-a950-48cf39601916/content
- sha256 (16): `e8ef75c1e10b31d4` · 166 trang

**EASL 2025 → không dùng**
- Tên: EASL CPG on the management of HBV infection (J Hepatol 2025;83(2):502–583, doi 10.1016/j.jhep.2025.03.018).
- journal-of-hepatology.eu (fulltext, showPdf), sciencedirect.com và link chia sẻ authors.elsevier.com đều trả **403**. easl.eu yêu cầu đăng nhập MyEASL. Europe PMC báo "Subscription required". PubMed chặn (trang trả 129 ký tự). Tải qua WebFetch cũng bị 403.
- Kết quả: **không đọc được từ nguồn chính thức**, nên không ghi hệ thống EU_UK vào mẩu nào.

**Slide EASL do NATAP đăng lại → không dùng**
- URL: https://www.natap.org/2025/EASL/EASL_HBV%20Guidelines%202.pdf
- sha256 (16): `3286876ad6296109` · 34 trang
- Đây là bản đăng lại của bên thứ ba, không chính thức. Tôi chỉ dùng làm manh mối: slide ghi LSM ≥ 7 kPa cho Metavir ≥ F2 và LSM > 8 kPa cho Metavir ≥ F3; ngưỡng HBV DNA "thay đổi theo mức hoạt động"; ngừng NA cần HBsAg < 100 IU/mL ở người châu Á. **Không dùng trong dữ liệu.**

---

## 2. Bảng mẩu

Ký hiệu: VN = 1740/2026. "Bản cũ" = giá trị trong `superseded`. Trang = trang PDF 1-based của 1740_2026.pdf; "in" = số trang in trên văn bản.

**P-hbv-01 — ngưỡng (threshold): ULN của ALT, nam**
- VN: 30 U/L
- Nước ngoài: US AASLD 2025 = 35 U/L; WHO 2024 = 30 U/L
- Bản cũ: 3310/2019 = 35 U/L
- Mồi: 25 U/L (mirror_arith). **Sau kiểm toán:** đổi thành 26 U/L (mirror_geom), vì 25 U/L trùng ULN nữ có thật ở mẩu 02.
- Trạng thái: **indistinguishable** · trang 18 (in 7)

**P-hbv-02 — ngưỡng: ULN của ALT, nữ**
- VN: 19 U/L
- Nước ngoài: US AASLD 2025 = 25 U/L; WHO 2024 = 19 U/L
- Bản cũ: 3310/2019 = 25 U/L
- Mồi: 13 U/L (mirror_arith)
- Trạng thái: **indistinguishable** · trang 18 (in 7)

**P-hbv-03 — ngưỡng: HBV DNA để khởi trị, HBeAg dương tính, người lớn chưa xơ gan, ALT tăng**
- Quần thể sau kiểm toán: ALT ≥ 2×ULN, không có yếu tố nguy cơ nào của 1740 tr.PDF 20.
- VN: > 2.000 IU/mL
- Nước ngoài: US AASLD 2025 ≥ 20.000 IU/mL; WHO 2024 > 2.000 IU/mL; WHO 2015 > 20.000 IU/mL
- Bản cũ: 3310/2019 ≥ 20.000, và > 20.000 ở nhánh 2 (thêm sau kiểm toán); 5448/2014 ≥ 20.000
- Mồi: 200 IU/mL (mirror_geom)
- Trạng thái: **indistinguishable** · trang 20 (in 9)

**P-hbv-04 — ngưỡng (cat): mức ALT so với ULN để khởi trị**
- Quần thể sau kiểm toán: HBeAg dương tính, 18–30 tuổi, HBV DNA 20.000–10.000.000 IU/mL, chưa ≥ F2, không có yếu tố nguy cơ. Trước đó là "HBeAg bất kỳ, ≥ 18 tuổi".
- VN: ALT > ULN (`gt_1x_uln`)
- Nước ngoài: US AASLD 2025 = ALT ≥ 2×ULN; WHO 2024 = ALT > ULN
- Bản cũ: 3310/2019 và 5448/2014 = ALT > 2 lần ULN
- Mồi: không có (lý do ở mục 6)
- Trạng thái: **indistinguishable** · trang 20 (in 9)

**P-hbv-05 — ngưỡng: FibroScan cho xơ hóa đáng kể (≥ F2)**
- VN: > 7 kPa
- Nước ngoài: WHO 2024 > 7 kPa
- Bản cũ: 3310/2019 = 7,0 kPa (không đổi)
- Mồi: không có
- Trạng thái: **concordant** · trang 19 (in 8)

**P-hbv-06 — thuốc đầu tay (first_line): NA đơn trị ưu tiên**
- Quần thể sau kiểm toán: 18–60 tuổi, ≥ 50 kg, không có thai, không bệnh thận/loãng xương, không yếu tố nguy cơ thận.
- VN: TDF, TAF, ETV
- Nước ngoài: WHO 2024 = TDF, ETV. ~~US AASLD 2025 = ETV, TDF, TAF~~: **đã bỏ sau kiểm toán**, vì đó là bảng "Available Treatment Options" của AASLD 2018, không phải danh sách ưu tiên.
- Bản cũ: 3310/2019 = TDF, ETV (sau kiểm toán; TAF chỉ ưu tiên khi > 60 tuổi, loãng xương hoặc suy thận); 5448/2014 = tenofovir, entecavir
- Mồi: không có
- Trạng thái: **concordant** · trang 40 (in 29)

**P-hbv-07 — thời gian (duration): HBV DNA không phát hiện trước khi ngừng NA, HBeAg âm tính, không xơ gan**
- VN: ≥ 3–4 năm (kèm qHBsAg < 100 IU/mL)
- Nước ngoài: US AASLD 2025 ≥ 2 năm
- Bản cũ: 3310/2019 không nêu số năm (yêu cầu mất HBsAg). Thêm sau kiểm toán: 5448/2014 ≥ 1 năm, suy ra từ "3 lần xét nghiệm liên tiếp cách nhau mỗi 6 tháng".
- Mồi: 5 năm (mirror_arith)
- Trạng thái: **conflict**, mong manh (xem mục 7) · trang 24 (in 13)

**P-hbv-08 — ngưỡng: HBV DNA để khởi trị, HBeAg âm tính**
- VN: > 2.000 IU/mL
- Nước ngoài: US AASLD 2025 ≥ 2.000; WHO 2024 > 2.000; WHO 2015 > 20.000
- Bản cũ: 3310/2019 và 5448/2014 ≥ 2.000. **Sai, đã sửa sau kiểm toán:** 3310/2019 còn có nhánh 2, > 20.000 IU/mL cho người > 30 tuổi có ALT > ULN kéo dài, bất kể HBeAg.
- Mồi: 200 IU/mL (mirror_geom)
- Trạng thái: ~~conflict (chỉ với WHO 2015)~~ → **indistinguishable** · trang 20 (in 9)

**P-hbv-09 — ngưỡng: FibroScan cho xơ gan (F4)**
- VN: > 12,5 kPa
- Nước ngoài: WHO 2024 > 12,5 kPa
- Bản cũ: 3310/2019 ≥ 11 kPa; 5448/2014 > 14,6 kPa
- Mồi: không có
- Trạng thái: **concordant**, có lệch phiên bản · trang 19 (in 8)

**P-hbv-10 — ngưỡng: APRI cho xơ gan (F4)**
- VN: > 1
- Nước ngoài: WHO 2024 > 1; WHO 2015 > 2
- Bản cũ: 3310/2019 ≥ 2; 5448/2014 > 2
- Mồi: 0,5 (mirror_geom)
- Trạng thái: **indistinguishable** · trang 19 (in 8)

**Vị trí giá trị nước ngoài trong nguồn** (ghi đầy đủ trong trường `locator`):
- AASLD, ULN 35/25: slide 21 và slide 25 (chú thích Figure 2/3), slide 4.
- AASLD, giai đoạn "immune active" (ALT ≥ 2×ULN; DNA ≥ 20.000 khi HBeAg+ và ≥ 2.000 khi HBeAg−): slide 4 và slide 29.
- AASLD, tiêu chí ngừng thuốc: slide 33.
- AASLD, danh sách thuốc: slide 5–6.
- WHO 2024, khung khuyến cáo "Who to treat": PDF tr.35 (in xxix).
- WHO 2024, "First-line": PDF tr.36 (in xxx).
- WHO 2015, "Who to treat" và APRI > 2: PDF tr.22.

**Cách ghép quần thể.** 1740/2026 dùng **một** ngưỡng HBV DNA > 2.000 IU/mL, không phân biệt HBeAg. Vì vậy mẩu 03 (HBeAg+) và 08 (HBeAg−) cùng một span, nhưng khác quần thể, và giá trị nước ngoài được ghép theo đúng quần thể HBeAg của nguồn.

---

## 3. Ứng viên bị loại và lý do

**Dự phòng lây truyền mẹ–con: thời điểm bắt đầu thuốc (dòng hạt giống 21).**
- Bị loại khỏi thí điểm theo bảng §3.3/§5.7.
- Dữ kiện thu được, để dùng sau:
  - 1740/2026 tr.PDF 41 (Phụ lục 6): tenofovir "từ tuần thai thứ 14" khi HBV DNA ≥ 200.000 IU/mL hoặc HBeAg dương tính. Tr.PDF 26 và 35 dẫn chiếu QĐ 678/2025.
  - 3310/2019 (ảnh trang 14): TDF "từ tuần 24–28".
  - AASLD 2025: tuần 28 (slide 10).
  - WHO 2024: "ít nhất từ tam cá nguyệt 2".
- Chưa đọc QĐ 678/2025, nên chưa lập được tập giá trị Việt Nam (DR8). Nếu làm, mẩu này có khả năng indistinguishable, vì tuần 28 của Mỹ gần tuần 24–28 của bản cũ.

**Ngưỡng HBV DNA 200.000 IU/mL để dự phòng mẹ–con.** Mọi nguồn đều đồng thuận (3310 > 200.000; 1740 ≥ 200.000; AASLD > 200.000; WHO ≥ 200.000). Loại vì thuộc nhóm dòng 21. Có thể dùng làm đối chứng về sau.
- **(Sau kiểm toán: cần sửa khẳng định "WHO ≥ 200.000".)** Trang đính chính của WHO 2024 (PDF tr.6, cùng file sha `e44231194db4a3c7`) xóa cụm "with HBV DNA ≥200 000 IU/mL or positive HBeAg" khỏi khuyến cáo trang xxxi. Câu thay thế là: TDF cho **mọi** phụ nữ mang thai HBsAg dương tính.
- Trang đính chính ghi các sửa đổi "đã đưa vào bản điện tử". Nhưng PDF tr.37 (in xxxi) vẫn còn câu cũ.
- Hệ quả: nếu tính bản đính chính, WHO **không còn** ngưỡng 200.000. Ứng viên này có thể là xung đột (WHO: không ngưỡng) chứ không phải đối chứng. Cần người kiểm trước khi dùng.

**Thời gian củng cố sau chuyển đổi huyết thanh HBeAg.** 1740 = thêm 12 tháng; 3310 = 12 tháng; 5448 = 6–12 tháng (chồng lấn giá trị Việt Nam); WHO và AASLD = 1 năm. Đồng thuận, nhưng giá trị bản cũ 5448 chồng lấn nên nhãn lệch phiên bản không sạch. Chưa tạo mẩu; có thể thêm làm đối chứng.

**Thời gian dự phòng sau khi ngưng thuốc ức chế miễn dịch.** 1740 ghi "6–12 tháng (tùy trường hợp)" và "ít nhất 6 tháng" (≥ 12 tháng với thuốc làm suy yếu tế bào B); 3310 ghi ≥ 12 tháng. Hợp các giá trị hiện hành đã chứa 12 tháng, nên lệch phiên bản không phân biệt được.

**Thời gian Peg-IFN.** 1740 = 48 tuần; 5448 = 6–12 tháng (chồng lấn 48 tuần); 3310 = 48 tuần. Không có lệch phiên bản sạch.

**Ngưỡng HBV DNA để điều trị lại sau khi ngừng thuốc.** 1740 = > 10.000 IU/mL. AASLD chỉ có con số này trong một phương án trắc nghiệm của slide 37–38, không có câu khuyến cáo. EASL chỉ đọc được trên bản đăng lại NATAP. Không có giá trị nước ngoài chính thức nên loại.

**Tiêu chí điều trị trẻ 2–11 tuổi.** Nhiều điều kiện, khó ra một giá trị duy nhất. Loại.

**Đồng nhiễm HIV/HBV.** Về cấu trúc, 1740 dùng "HBV DNA trên ngưỡng phát hiện", còn 5448 dùng > 2.000 IU/mL. Không rõ đây là giá trị hay cách diễn đạt, và thiếu giá trị nước ngoài tương ứng. Loại.

**Dự phòng sau phơi nhiễm, HBIG 0,06 mL/kg** (1740 tr.PDF 35). Có thể là đối chứng với CDC, nhưng chưa tải nguồn CDC. Chưa làm.

**APRI > 0,5 cho xơ hóa đáng kể (F2).** Đồng thuận (3310: 0,5; WHO: 0,5). Không tạo mẩu riêng để tránh trùng lặp với P-hbv-05.

**Mọi giá trị EASL 2025.** Không đọc được bản chính thức (403 hoặc cần đăng nhập). Không ghi.

**Mức ULN theo slide AASLD.** Slide 29 ghi đơn vị "U/mL" (lỗi đánh máy của slide). Tôi lấy giá trị theo slide 4, 21 và 25, là các slide ghi "U/L".

---

## 4. Sai lệch so với bộ hạt giống (§3.3 và `data/seed/seed_conflicts.yaml`)

**1. Dòng 20 không phải xung đột sạch.**
- Bảng ghi "Xác nhận" cho khác biệt 30/19 U/L so với 35/25 U/L (AASLD 2025). Bản 3310/2019 chính thức (ảnh trang 4, tr. in 2, mục II.1) định nghĩa "ULN: 35 U/L đối với nam, 25 U/L đối với nữ". Như vậy giá trị Mỹ **trùng giá trị Bộ Y tế cũ**, và mẩu 01–02 thành `indistinguishable`.
- Tương tự, AASLD 2025 dùng ALT ≥ 2×ULN và HBV DNA ≥ 20.000 IU/mL khi HBeAg dương tính. Cả hai trùng 3310/2019 và 5448/2014, nên mẩu 03–04 cũng `indistinguishable`.
- Hệ quả cho H1: dòng 20 và các mẩu tách ra từ nó **không vào được kiểm định xác nhận**. Chúng vẫn có giá trị cho mô tả lệch phiên bản (nhãn 3). Khi mô hình trả lời 35 U/L, 2×ULN hay 20.000 IU/mL, không thể quy riêng cho "chuẩn Mỹ" hay "bản Bộ Y tế cũ".

**2. Dòng 20, ô `superseded: cần tra`.** Nay đã tra từ bản chính thức 3310/2019 (bản quét):
- ULN 35/25 U/L;
- ALT > 2 lần ULN;
- HBV DNA ≥ 20.000 IU/mL (HBeAg+) và ≥ 2.000 IU/mL (HBeAg−);
- FibroScan F4 ≥ 11 kPa;
- APRI F4 ≥ 2.
Thêm từ 5448/2014: FibroScan F4 > 14,6 kPa; APRI F4 > 2.

**3. Dòng 20, mô tả phía AASLD.** Mô tả "ALT ≥ 2×ULN (35/25) và HBV DNA theo HBeAg" **đúng** với slide AASLD 2025 (≥ 20.000 IU/mL khi HBeAg+, ≥ 2.000 IU/mL khi HBeAg−). Trạng thái "Xác nhận" cần sửa thành "trùng bản Bộ Y tế cũ, không phân biệt được".

**4. Dòng 20, tiêu chí xơ hóa (APRI > 0,5 hoặc FibroScan > 7 kPa).** Giá trị đúng (1740 tr.PDF 18–19). Tuy vậy, đây là **đối chứng** (trùng WHO 2024 và bản 3310), không phải xung đột. Lệch phiên bản đáng giá thật nằm ở **ngưỡng xơ gan F4** (mẩu 09 và 10), không ở ngưỡng F2.

**5. Kỳ vọng về lệch phiên bản (§5.7).** Cặp 3310/2019 → 1740/2026 có ít nhất 6 lệch phiên bản thật (01, 02, 03, 04, 09, 10). Nhưng 5/6 trong số đó trùng một nguồn nước ngoài: AASLD 2025, hoặc WHO 2015 với mẩu 10. Nên cân nhắc điều này khi ước tính số mẩu dùng được cho H1 và H2.
- *(Sau kiểm toán)* Mẩu 04 chỉ lệch phiên bản sạch ở người ≤ 30 tuổi, vì nhánh 2 của 3310 dùng ALT > ULN cho người > 30 tuổi. Quần thể đã được chốt lại là 18–30 tuổi.
- *(Sau kiểm toán)* Mục 2 ở trên bỏ sót nhánh 2 của 3310 mục 2.4.2. Đó là tiêu chí: > 30 tuổi, ALT > ULN kéo dài (≥ 3 lần trong 24–48 tuần) và HBV DNA > 20.000 IU/ml, bất kể HBeAg (ảnh tr.7).

**6. Dòng 21.** Ghi chú "có thể mâu thuẫn với 1740/2026" được chứng thực một phần: 1740 dẫn chiếu 678/2025 và tự ghi tuần thai 14 (Phụ lục 6), trong khi 3310 ghi tuần 24–28. Chưa đọc 678/2025.

**7. Lỗi kho văn bản.** `data/raw/3310_2019.pdf` là bản đăng lại **sai nhãn**, nội dung thực là 5448/2014. Mọi công cụ gọi `pdf_path("3310/2019")` sẽ trỏ vào file sai. Đề xuất cho corpus-librarian (tôi không được sửa `data/raw`):
- đánh dấu file này là không hợp lệ trong manifest;
- dùng `3310_2019__c43006cb.pdf` (bản quét chính thức, cần OCR, tính vào hạn mức `max_ocr_documents` = 10);
- ghi `5448/2014` vào manifest với trạng thái `superseded`, `superseded_by` = 3310/2019.

**8. Tài liệu tham khảo của 1740/2026** dẫn AASLD 2018 (Terrault) và EASL 2025, không dẫn AASLD 2025. Chỉ để tham khảo khi viết bài.

---

## 5. Việc cần người kiểm ở HG1.2

**1. Span 1740/2026.** Mở `data/raw/1740_2026.pdf`, kiểm các trang PDF 18, 19, 20, 24 và 40 (trang in 7, 8, 9, 13, 29). Công cụ đã khớp nguyên văn cả 10 mẩu. Người kiểm cần xác nhận quần thể và bối cảnh:
- 01–02: ULN theo giới.
- 03 và 08: tiêu chí dành cho người ≥ 12 tuổi, không phân biệt HBeAg.
- 06: là "phác đồ ưu tiên".
- 07: HBeAg âm tính, kèm qHBsAg < 100 IU/mL.

**2. Bản chép tay 3310/2019** (từ ảnh; **không kiểm bằng máy được**). Mở `data/raw/3310_2019__c43006cb.pdf` và đối chiếu `extraction.superseded_spans` ở các trang:
- tr.4 (in 2): ULN 35/25 U/L;
- tr.7 (in 5): mục 2.4.2;
- tr.8 (in 6): Bảng 1 thuốc;
- tr.9 (in 7): mục 2.6.1 ngừng thuốc;
- tr.16 (in 15): Phụ lục 2 (FibroScan F4 ≥ 11 KPa, APRI F4 ≥ 2).

Cần xác nhận thêm: ULN 35/25 được định nghĩa ở mục viêm gan B **cấp**. Tôi hiểu đó là định nghĩa ULN dùng cho toàn văn bản, vì mục 2.4.2 (viêm gan mạn) dùng "ULN" mà không định nghĩa lại. Việc hiểu này cần người duyệt.

**3. EASL 2025.** Cần truy cập qua thư viện hoặc tài khoản (J Hepatol 2025;83(2):502–583) để lấy: ULN của ALT, ngưỡng HBV DNA theo HBeAg, LSM cho F2 và F4, tiêu chí ngừng NA ở người HBeAg âm tính. Nếu người dùng cung cấp PDF chính thức, tôi sẽ bổ sung hệ thống EU_UK. Khả năng cao EASL sẽ làm thay đổi trạng thái của 01–04 và 07.

**4. AASLD.** Giá trị lấy từ bộ slide giáo dục chính thức của AASLD, không phải bài báo Hepatology 2025. Nên đối chiếu một lần với toàn văn bài báo (Ghany et al., 2025).

**5. Mẩu 07.** Khuyến cáo 5 của AASLD là **không ngừng NA cho tới khi mất HBsAg**. Mốc "≥ 2 năm" nằm trong tiêu chí dành cho người muốn ngừng (slide 33). Cần quyết định có chấp nhận quy "2 năm" cho AASLD hay không. Nếu không, mẩu thành `no_counterpart`, và thí điểm HBV chỉ còn 1 mẩu xung đột (08, với WHO bản cũ).
- *(Sau kiểm toán)* 08 không còn là xung đột. Nếu 07 bị loại, thí điểm HBV sẽ có **0** mẩu xung đột dùng được cho H1.

**6. Mồi cần duyệt.**
- Mẩu 01: mồi 25 U/L trùng ULN **nữ** của AASLD và 3310. Mô hình nhầm giới có thể bị tính là trùng mồi.
- Mẩu 10: mồi 0,5 trùng ngưỡng APRI cho **F2** của chính 1740.
- Cả hai do quy tắc mirror bắt buộc tạo ra, không tự sửa. Hệ quả là trùng mồi có xu hướng bị ước tính cao, tức bảo thủ cho H1.
- Mẩu 04: mồi đề xuất "ALT ≥ 3×ULN" **chưa đưa vào** trường `decoy`, lý do ở mục 6.

**7. Phân loại mẩu 08.** Mẩu này "xung đột" chỉ vì WHO 2015, một bản WHO đã bị thay. Cần quyết định có tính vào nhóm xung đột của thí điểm hay xếp riêng.
- *(Sau kiểm toán: đã giải quyết.)* Mẩu 08 là `indistinguishable`, vì nhánh 2 của 3310 cũng dùng > 20.000. Xem mục 7.

---

## 6. Đề xuất bổ sung configs và mã (không tự sửa)

**1. `src/vnsoc/normalize_vi.py` — `UNIT_ALIASES`**
- Thêm đơn vị không thứ nguyên cho chỉ số APRI và FIB-4, ví dụ `"index": "index"`, `"apri": "index"`. Mẩu 10 đang dùng `unit: "index"`.
- Cân nhắc thêm `"copies/ml"` với hệ số 1 IU/mL ≈ 5 copies/mL (theo quy ước của WHO 2015 và bản 3310). Lý do: văn bản cũ ghi "10^5 copies/ml", và lớp chữ PDF mất chỉ số trên, thành "105 copies/ml".

**2. `configs/grading.yaml` — mục `drugs` và `combos`**
- `emtricitabine: [ftc, emtricitabin]`
- `peginterferon-alfa-2a: [peg-ifn, peg-ifn-α-2a, peginterferon alfa-2a, pegasys]`
- `interferon-alfa-2b: [ifn-α-2b]`
- `adefovir: [adv]`
- `telbivudine: [ldt]`
- combos `TDF/3TC: [tenofovir-disoproxil, lamivudine]` và `TDF/FTC: [tenofovir-disoproxil, emtricitabine]`
- Quyết định cách chấm câu trả lời chỉ ghi "tenofovir" (không rõ TDF hay TAF). Hiện câu trả lời này không parse ra thuốc nào.

**3. `src/vnsoc/match/decoys.py::check_decoy`** trả `"mồi làm mẩu thành indistinguishable"` cả khi mẩu **đã** indistinguishable trước khi có mồi, vì giá trị bản cũ trùng nước ngoài. Đây là báo động giả; nó gặp ở mẩu 01, 02, 03, 10 và cả 04.
- Đề xuất: so `conflict_status` khi có mồi và khi không có mồi. Chỉ báo lỗi khi chính mồi làm đổi trạng thái.
- Vì báo động giả này mà mẩu 04 (kiểu cat) để trống `decoy` theo đúng quy tắc "check_decoy phải == []". Mồi đề xuất ghi trong `extraction.notes`.

**4. Kiểm span bản cũ bằng máy.** Nên mở rộng `verify_span` để kiểm `extraction.superseded_spans` khi văn bản cũ có lớp chữ. Với 5448/2014 tôi đã tự kiểm thủ công: các span nằm nguyên văn ở tr.4 và tr.9. Với bản quét, cần OCR (DR/§4.1).

**5. Manifest và kho văn bản:** xem mục 4 điểm 7. Cần sửa sai nhãn `3310_2019.pdf`, thêm `3310_2019__c43006cb.pdf` (cần OCR), và thêm `5448/2014`.

---

## 7. Sau kiểm toán (2026-09-26)

Đầu vào: `data/interim/pilot/hbv_verify.md` (pass 2 · fix 8 · reject 0). Tôi tự kiểm lại từng điểm bằng công cụ trước khi sửa. Chỉ ghi 2 file: `hbv.jsonl` và báo cáo này.

### 7.1. Bằng chứng tự kiểm lại (không dựa vào lời kiểm toán)

| Điểm | Cách kiểm | Kết quả |
|---|---|---|
| Nhánh 2 của 3310 mục 2.4.2 | Dựng ảnh tr.7 của `3310_2019__c43006cb.pdf` (sha `c43006cb69cb517f`) bằng PyMuPDF, 200 dpi, rồi đọc bằng mắt | **Có**: "Đối với các trường hợp chưa đáp ứng hai tiêu chuẩn trên… + Trên 30 tuổi với mức ALT cao hơn ULN kéo dài (ghi nhận ít nhất 3 lần trong khoảng 24 - 48 tuần) và HBV DNA > 20.000 IU/ml, bất kể tình trạng HBeAg". Các tiêu chí kế tiếp: tiền sử gia đình HCC/xơ gan; biểu hiện ngoài gan; tái phát sau ngưng thuốc |
| Chú thích ** của 3310 Bảng 1 | Ảnh tr.8 | TAF "được lựa chọn ưu tiên" khi > 60 tuổi, loãng xương, suy thận hoặc chạy thận |
| AASLD slide 4, 21, 24, 25, 32, 33 | `sources fetch` (sha `763a79fe35c57c68`), đọc toàn văn trang từ bản đã băm | Xác nhận: Figure 2 (HBeAg+, ALT 1–<2×ULN: theo dõi, cân nhắc nếu ≥ 40 tuổi hoặc ≥ F2); Rec 4 và Figure 3 (HBeAg−, ALT < 2×ULN: quyết định chung); Rec 5 (không ngừng NA tới khi mất HBsAg). Dòng trích "Ghany M., et al. … Hepatology 2025" (tìm trong lớp chữ) có ở slide 4, 7, 13, 17, 21, 25, 29, 43, 46. **Không** có ở slide 33, và cũng không có ở slide 32. Kiểm toán nói slide 32 có dòng trích: không đúng với lớp chữ. Tuy vậy slide 32 mang nhãn "Recommendation 5", tức là khuyến cáo chính thức của bài hướng dẫn |
| AASLD slide 5–6 | Như trên | Chú thích "Adapted from Table 1 in Terrault N… AASLD 2018"; tiêu đề "Available Treatment Options" |
| Metadata AASLD 2025 | `sources fetch` Europe PMC REST (sha `596b6ab3e979…`) | Tiêu đề Europe PMC ghi "AASLD ISDA Practice Guideline on treatment of chronic hepatitis B"; doi 10.1097/hep.0000000000001549; epub 2025-11-04; Hepatology 2026;83(4):974–997; PMID 41186418; không truy cập mở |
| WHO 2015 tr.22 | `sources` (sha `e8ef75c1e10b31d4`), đọc toàn văn trang | "aged more than 30 years (in particular)". Nhóm theo dõi gồm HBeAg âm ≤ 30 tuổi có HBV DNA dao động 2.000–20.000 |
| WHO 2024: tuổi áp dụng ngưỡng kPa/APRI | grep (sha `e44231194db4a3c7`) | tr.46, 48, 84 ghi "(adults)". Chú thích e (tr.47, 85) ghi chưa thẩm định ở trẻ em và vị thành niên. Đính chính tr.7 chỉ đổi ký hiệu chú thích d→e, vẫn giữ câu này. **tr.80 CÓ ">7.0 kPa"** |
| 1740 tr.15, 20, 22, 24 | `verify_span --page` | tr.15: ULN 30/19 ở mục viêm gan B cấp (cùng vị trí 3310 đặt 35/25). tr.20: danh sách yếu tố nguy cơ. tr.22: tránh TDF ở người tuổi cao, < 50 kg, tăng huyết áp, đái tháo đường, dùng thuốc độc thận. tr.24: tiêu chí ngừng thuốc |
| 5448 tr.4 | `verify_span --page 5448/2014 4` | Không có nhánh tuổi. Ngừng thuốc khi HBeAg (−): "3 lần xét nghiệm liên tiếp cách nhau mỗi 6 tháng" |
| check_decoy báo động giả | `finalize(dict(a, decoy=[]))` | 01, 02, 03, 08, 10 vẫn `indistinguishable` khi bỏ mồi. Cảnh báo là giả |
| Regex mẩu 04 | `nv.parse_cats` trên 14 câu mẫu | Mọi cách viết "gấp đôi / double / more than 2 times / >2ULN / trên hai lần / 2-fold / greater than two times" → `gt_2x_uln`. "> ULN / above the ULN" vẫn → `gt_1x_uln`. Không nhận nhầm chéo |

### 7.2. Đã sửa gì (theo từng mẩu)

| Mẩu | Kiểm toán | Đã làm | Trạng thái (finalize) |
|---|---|---|---|
| 01 | fix | Mồi 25 → **26 U/L** (`mirror_geom`, phương án dự phòng định trước trong `choose_decoy`). Lý do: 25 U/L là ULN nữ có thật của AASLD và 3310, tức giá trị của mẩu anh em 02. Thêm ghi chú về 1740 tr.15. Chuẩn hóa metadata AASLD | indistinguishable (tol 2,5 → 2,0) |
| 02 | pass | Chỉ chuẩn hóa metadata AASLD | indistinguishable |
| 03 | fix | Quần thể: ALT ≥ 2×ULN; ghi đủ yếu tố nguy cơ của 1740 tr.20. Thêm nhánh 2 của 3310 (> 20.000) vào `superseded` và `superseded_spans`. Locator AASLD → slide 21 | indistinguishable |
| 04 | fix | Quần thể: HBeAg+, **18–30 tuổi**, HBV DNA 20.000–10.000.000, chưa ≥ F2, không yếu tố nguy cơ. Thêm 6 regex cho `gt_2x_uln`. Locator AASLD → slide 21 (Figure 2). Mồi vẫn trống (xem 7.3) | indistinguishable |
| 05 | fix | Tuổi → người lớn (≥ 18). Locator WHO: thêm tr.34 và tr.46, **giữ** tr.80 | concordant |
| 06 | fix | **Bỏ mục AASLD** (bảng "Available options" 2018, không phải danh sách ưu tiên 2025). Tập 3310 → {TDF, ETV}, thêm span chú thích **. Quần thể: 18–60 tuổi, ≥ 50 kg, không bệnh thận/xương và không yếu tố nguy cơ thận (theo 1740 tr.22) | concordant |
| 07 | fix | Locator AASLD ghi rõ slide 33 là tiêu chí cho người muốn ngừng, và slide 32 Rec 5 là không ngừng tới khi mất HBsAg; có cờ needs_human_check. Thêm `population.preference` và `vn[0].cmp ">="`. Thêm 5448/2014 = **≥ 1 năm (giá trị suy ra)** vào `superseded` và span tr.4 | **conflict** (tol 0,5; khoảng cách AASLD–5448 = 1 = 2·tol, không nhỏ hơn) |
| 08 | fix | **Phương án A.** Thêm nhánh 2 của 3310 (> 20.000) vào `superseded`. `conflict_family` → `hbv_dna_threshold_20000_age30`. Quần thể ghi đủ yếu tố nguy cơ. Locator và giá trị AASLD ghi cả Rec 4. Sửa câu sai trong notes | **conflict → indistinguishable** |
| 09 | fix | Tuổi → người lớn (≥ 18). Locator WHO thêm tr.34 | concordant |
| 10 | pass | Chỉ thêm ghi chú: mồi 0,5 trùng ngưỡng F2 thật; không có mồi thay thế theo quy tắc | indistinguishable |

Metadata AASLD của 01, 02, 03, 04, 07, 08 nay ghi: `version_date` = 2025-11-04; `source` = tên, tạp chí, PMID, doi theo Europe PMC. `source` cũng ghi rõ giá trị lấy từ bộ slide giáo dục và toàn văn chưa đọc (403).

Kiểm tra cuối:
- `vnsoc.schemas atom data/interim/pilot/hbv.jsonl` → **OK 10 dòng hợp lệ**.
- `vnsoc.extract.verify_span data/interim/pilot/hbv.jsonl` → **OK: 0 mẩu không đạt**.
- `finalize()` chạy lại trên file đã ghi: tolerance và trạng thái không đổi (lũy đẳng).
- Không mẩu nào có trường chỉ-bác-sĩ.

### 7.3. Chỗ tôi không làm theo kiểm toán, và lý do

1. **Mẩu 08, phương án B, bị loại vì tiền đề của nó sai.**
   - Kiểm toán nói WHO 2015 "không có khuyến cáo điều trị cho ≤ 30 tuổi".
   - WHO 2015 tr.22 thực ra viết "aged more than 30 years (in particular)", tức là nhấn mạnh chứ không giới hạn cứng. Nhóm "theo dõi" của nó còn nêu riêng người HBeAg âm ≤ 30 tuổi có HBV DNA 2.000–20.000.
   - Vậy ở 18–30 tuổi, WHO 2015 vẫn là > 20.000. Không được bỏ WHO 2015 khỏi mẩu (quy tắc: ghi mọi hệ thống liên quan).
   - Nếu giữ WHO 2015, phương án B cho ra xung đột **chỉ với WHO 2015**. Nhưng 20.000 lại là ngưỡng HBeAg+ của 3310, 5448 và AASLD, tức quần thể lân cận. Quy nguồn quá mong manh.
   - Vì vậy tôi chọn phương án A (bảo thủ, cũng là mặc định của kiểm toán).
2. **Mẩu 05, locator tr.80:** kiểm toán nói tr.80 không chứa 7 kPa. Sai: `sources grep "7.0 kPa"` trả tr.80 (">7.0 kPa identifies most adults with significant fibrosis"). Tôi giữ tr.80 và thêm tr.34, tr.46.
3. **Mẩu 07, `verified_by` = "needs_human_check":** schema chỉ nhận `auto | student | clinician`. Tôi giữ `"auto"`, vì giá trị "minimum of 2 years" có nguyên văn trong trang slide đã băm. Cờ needs_human_check (quy slide 33 về Ghany 2025) được ghi trong `locator` và `notes`.
4. **Mẩu 06, xử lý mục AASLD:** kiểm toán cho chọn "bỏ" hoặc "đổi nhãn 2018".
   - Tôi chọn **bỏ**. "Available options" không phải cùng slot với "thuốc đầu tay ưu tiên".
   - Tôi đã thử lấy toàn văn AASLD 2018 (PMC5975958) để có giá trị "preferred" đúng nguồn, nhưng không được: PMC trả trang 131 ký tự, Europe PMC fullTextXML trả lỗi 500.
   - Kết quả: mẩu 06 không có hệ US.
5. **Mẩu 04, mồi:** giữ trống. Quy tắc bắt buộc `check_decoy == []` cho mẩu cat. Chừng nào `check_decoy` chưa được sửa, mọi mồi đều bị báo động giả. Mồi đề xuất `gt_3x_uln` ghi ở notes.

### 7.4. Tồn đọng cho HG1.2 (người kiểm)

1. **Ảnh 3310** (`visual_transcription_scan`, AI chép): 2 span mới cần đối chiếu.
   - tr.7: nhánh 2 của mục 2.4.2 (mẩu 03, 08);
   - tr.8: chú thích ** của Bảng 1 (mẩu 06).
   - Cùng các span cũ ở tr.4, 7, 8, 9, 16.
2. **Mẩu 07.**
   - (a) Có chấp nhận quy "≥ 2 năm" cho AASLD 2025 không? Lý do nghi ngờ: slide 33 không có dòng trích, và khuyến cáo chính Rec 5 là "không ngừng tới khi mất HBsAg". Nếu không chấp nhận, **thí điểm HBV không còn mẩu xung đột nào cho H1**.
   - (b) Có chấp nhận giá trị suy ra 5448 = ≥ 1 năm không?
   - (c) Có tạo mẩu cat anh em "điều kiện ngừng NA ở HBeAg−, không xơ gan" không? Mẩu này sẽ là: VN = {DNA dưới ngưỡng ≥ 3–4 năm + qHBsAg < 100}; 3310 = AASLD Rec 5 = {mất HBsAg}; dự kiến `indistinguishable`.
3. **Mẩu 08:** xác nhận phương án A. Nếu muốn có mẩu đối chứng sạch thay thế, cần một quyết định về WHO 2015 ("in particular").
4. **Mẩu 01:** mồi `mirror_geom` 26 U/L thay cho `auto` 25 U/L. Việc này **cần ghi `docs/DECISIONS.md`**, vì prereg §6.4 chỉ mô tả `auto`. Nếu không chấp nhận, trả về 25 U/L và ghi giới hạn trong QC trắc nghiệm.
5. **Mẩu 10:** mồi 0,5 là ngưỡng thật của F2. Cần ghi vào QC trắc nghiệm.
6. **Toàn văn AASLD 2025** (Hepatology 2026;83(4):974–997) và **EASL 2025**: cần người dùng cung cấp qua thư viện. EASL có thể biến 07 thành đồng thuận với EU nếu EASL ghi 3 năm. Hệ EU_UK hiện trống ở cả 10 mẩu.
7. **WHO 2024 và dự phòng mẹ–con:** trang đính chính (tr.6) xóa ngưỡng ≥ 200.000/HBeAg+, nhưng tr.37 vẫn còn câu cũ (mục 3). Cần người kiểm trước khi dùng ứng viên dòng 21.
8. **Chưa kiểm được** (hết hạn mức tìm kiếm ở phiên kiểm toán, và phiên này không có WebSearch): 1740/2026 có bị sửa hoặc thay sau 17/6/2026 không; WHO có bản HBV 2025/2026 không.
9. **Dòng hạt giống 20:** đề nghị đổi `status: confirmed` thành "indistinguishable (trùng 3310/2019)". Người dùng quyết định; tôi không sửa file hạt giống.

### 7.5. Đề xuất mã và cấu hình bổ sung (không tự sửa)

1. **`src/vnsoc/match/decoys.py::check_decoy`**
   - (a) Chỉ báo "mồi làm mẩu thành indistinguishable" khi trạng thái có mồi **khác** trạng thái không mồi.
   - (b) So mồi với giá trị của các mẩu **cùng span hoặc cùng `conflict_family`**, để bắt mồi trùng giá trị thật ở mẩu anh em (01 ↔ 02, 10 ↔ ngưỡng F2).
   - Nếu chỉ làm (a) mà không làm (b), `pilot_merge.enforce_decoy_rule` sẽ đặt lại mồi 01 về 25 U/L.
   - Chưa sửa thì `pilot_merge.check()` sẽ loại 01, 02, 03, 08, 10.
2. **`configs/grading.yaml` (mục drugs)** hiện chỉ có `tenofovir-disoproxil: [tdf, tenofovir disoproxil fumarate]` và `tenofovir-alafenamide: [taf]`. Cần thêm:
   - `tenofovir disoproxil`, `tenofovir disoproxil fumarat`, `viread`;
   - `tenofovir alafenamide`, `tenofovir alafenamid`, `tenofovir alafenamid fumarat`, `vemlidy`;
   - `entecavir`: `baraclude`.
   - Kiểm bằng test trước khi đóng băng câu hỏi.
3. **`src/vnsoc/schemas.py::ForeignValue.verified_by`:** cân nhắc thêm giá trị `needs_human_check`, cho trường hợp giá trị có trong nguồn đã băm nhưng việc quy phiên bản chưa kiểm được (mẩu 07).
4. **Prereg §6.4 và `docs/DECISIONS.md`:** thống nhất chuỗi dự phòng `auto → mirror_geom → mirror_far` mà `choose_decoy` đã cài. Thêm quy tắc "mồi không được trùng giá trị thật của quần thể lân cận". Báo cáo dengue cũng nêu vấn đề này.
5. Giữ các đề xuất ở mục 6: `UNIT_ALIASES` (`index`, `copies/ml`); sửa manifest cho `3310_2019.pdf` sai nhãn; OCR bản quét 3310.
