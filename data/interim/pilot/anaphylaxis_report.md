# T1.1 thí điểm — Phản vệ, adrenalin tiêm bắp (ID = anaphylaxis)

Ngày: 2026-09-26 · Người làm: agent atom-extractor + counterpart-matcher (Claude) · Trạng thái bản gốc (11:01): **KHÔNG ghi được mẩu nào (0/4 chỉ tiêu: 1–2 xung đột, 2 đối chứng)**

> **CẬP NHẬT SAU KIỂM TOÁN (xem mục 7 ở cuối file):** sau kiểm toán độc lập (`anaphylaxis_verify.md`: pass 0 · fix 3 · reject 3), `anaphylaxis.jsonl` nay có **3 mẩu** (1 conflict, 2 concordant): P-anaphylaxis-01 (= D2, người lớn), -02 (= D3, khoảng nhắc lại, trẻ em), -03 (= D6, nhũ nhi < 10 kg). D1, D4, D5 giữ loại. Hai lệnh kiểm bắt buộc OK với 3/3 mẩu. Mục 1–6 dưới đây là bản gốc, giữ nguyên để truy vết; chỗ nào lỗi thời đã được đánh dấu.

Bản gốc: `data/interim/pilot/anaphylaxis.jsonl` là **file rỗng (0 mẩu)**. Hai lệnh kiểm vẫn qua trên file rỗng (`vnsoc.schemas atom` → "OK 0 dòng"; `verify_span` → "OK: 0 mẩu không đạt"), nên chữ "OK" ở đây **không** có nghĩa là có mẩu đạt.

Tóm tắt:
1. **Bản PDF chính thức duy nhất của TT51/2017 (kcb.vn) là bản quét có ký số, không có lớp chữ** (`text_kind = scanned_or_empty`; `verify_span --page TT51/2017 9` trả về chuỗi rỗng). Máy chưa có OCR. Theo quy tắc, không tạo mẩu từ văn bản này. Tôi chỉ **đọc bằng mắt** ảnh trang để chuẩn bị bản nháp (mục 2b), và đánh dấu rõ là chưa kiểm được bằng máy.
2. **Phát hiện chính (trái với bảng hạt giống):** hai văn bản chuyên môn khác của Bộ Y tế vẫn đăng trên kcb.vn là QĐ 3942/QĐ-BYT (2014, dị ứng – miễn dịch lâm sàng) và QĐ 3312/QĐ-BYT (2015, bệnh thường gặp ở trẻ em). Chúng ghi liều adrenalin tiêm bắp cho trẻ là **0,01 mg/kg** (tức 0,01 ml/kg), và QĐ 3942 còn ghi **0,15 mg cho trẻ 10–25 kg** (chương dị ứng thức ăn). Đây đúng là giá trị của WAO và RCUK. TT51/2017 chỉ tuyên bố thay thế TT08/1999, không bãi bỏ hai văn bản này. Hệ quả: nếu áp quy tắc DR8 (§1.2, mọi văn bản Bộ Y tế hiện hành cho đúng quần thể đều tính là đúng), **dòng hạt giống 15 không còn là xung đột**. Nếu coi hai văn bản cũ đã bị TT51 thay, mẩu thành **indistinguishable** (giá trị nước ngoài trùng giá trị Bộ Y tế cũ). Dòng 15 chỉ là "xung đột sạch" khi bỏ qua hẳn hai văn bản đó. Đây là quyết định khoa học/pháp lý cho người dùng (mục 5).
3. Ngay trong TT51, sơ đồ tóm tắt ở Phụ lục X (trang 19–20) ghi "Trẻ em: 1/5–1/3 ống" (200–333 µg) và "Người lớn: 1/2 ống". Khoảng này chứa 300 µg của RCUK cho trẻ 6–12 tuổi, nên mẩu dự kiến "trẻ > 30 kg" cũng không còn là xung đột với RCUK (mục 3).
4. Phía nước ngoài đã kiểm có sha256: RCUK 2021 (sơ đồ và toàn văn), WAO 2020 (qua Europe PMC) và Mỹ AAAAI/ACAAI 2023. **EAACI 2021 bị chặn (403) ở cả 4 nguồn**, nên không ghi giá trị.
5. Phát hiện lỗi mã: `mirror_decoy` không quy đổi đơn vị trước khi phản chiếu. Kết quả là mồi sai "999.99 ug" mà `check_decoy` không bắt được (mục 6).

---

## 1. Văn bản đã tìm / tải

### 1a. Văn bản Việt Nam

| Khóa | URL / nơi tìm | Kết quả | sha256 (16) | Trang | text_kind |
|---|---|---|---|---|---|
| TT51/2017 | kcb.vn, trang văn bản `kcb.vn/van-ban/thong-tu-so-51-2017-tt-byt-ngay-29-12-2017-huong-dan-phong-chan-doan-va-xu-tri-phan-ve.html` (trạng thái trên trang: "Đã có hiệu lực"). PDF: `https://kcb.vn/upload/2005611/20210723/fda42ab303f0f256316b69ff98643f48tt-2017-51-1.pdf` | **Đã tải** qua fetch_pdf → `data/raw/TT51_2017.pdf` (status downloaded, 3.008.354 byte). Trang 1 chỉ có lớp chữ chữ ký số: "Chứng thư: Bộ Y tế · Ngày ký: 19/01/2018 · Hệ thống VOffice Bộ Y Tế". Đủ Điều 1–9 và Phụ lục I–X (xem ảnh trang). Số trang in trùng số trang PDF (trang 9 in số "9") | cab611be9dd14312 | 20 | **scanned_or_empty** |
| TT51/2017 (link thứ 2 trên cùng trang kcb.vn) | `.../df9b95d9ffbf23e085173d93d1337683tt-2017-51-1.pdf` | Tải thử về scratchpad: **cùng một file** (cùng sha256), cũng là bản quét. Không ghi vào data/raw | cab611be9dd14312 | 20 | scanned_or_empty |
| TT51/2017 (tìm bản có lớp chữ) | moh.gov.vn: không tìm thấy. emohbackup.moh.gov.vn `/publish/attach/getfile/406971`: HTTPS lỗi chứng chỉ (sai tên miền/hết hạn), HTTP trả thông báo lỗi 33 byte. vbpl.vn/boyte (ItemID=128248): trang tải động, không lấy được file. vbpl.yte.gov.vn và soytehaiphong.gov.vn: DNS không phân giải. syt.binhdinh.gov.vn: chỉ có poster. Nhiều kết quả khác chỉ trỏ tới trang thư viện pháp luật tư nhân hoặc trang tư nhân khác (luatvietnam, download.vn, studocu…) | **Không có bản chính thức nào có lớp chữ.** Các trang tư nhân không truy cập | — | — | — |
| TT51/2017 (bản đánh máy lại, để đối chiếu) | soyt.langson.gov.vn `/upload/105380/20241107/1_BAC_SI_HANG_III__Y_KHOA__e05ea.pdf` (tài liệu ôn thi của Sở Y tế Lạng Sơn, có đánh máy lại TT51) | Đọc trong scratchpad **chỉ để đối chiếu** với việc đọc bằng mắt. Các con số ở trang 7 khớp với ảnh trang 9 của bản chính thức. **Không** phải bản đăng lại nguyên quyết định nên không dùng làm nguồn mẩu và không ghi vào data/raw | 3d0dcd0d496c52a1 | 112 | ok |
| 3942/2014 (QĐ 3942/QĐ-BYT ngày 02/10/2014, "Hướng dẫn chẩn đoán và điều trị các bệnh về dị ứng – miễn dịch lâm sàng") | kcb.vn `/van-ban/huong-dan-chan-doan-va-dieu-tri-cac-benh-ve-di-ung-mien-dich-lam-sang.html` (trạng thái "Đã có hiệu lực"). File đính kèm là **.rar**: `https://kcb.vn/upload/2005611/20210723/d62bb141b263a41120ad6758260d3a94Mien-dich.rar` | Tải và giải nén **trong scratchpad** (fetch_pdf không nhận .rar). Không ghi vào data/raw. PDF bên trong: "The final - Dị ứng - Miễn dịch lâm sàng 3942-20141002.pdf" | rar ab82a39204574b0a; pdf 4be16be0fe6812f4 | 144 | ok |
| 3312/2015 (QĐ 3312/QĐ-BYT ngày 07/8/2015, "Hướng dẫn chẩn đoán và điều trị một số bệnh thường gặp ở trẻ em") | kcb.vn `/phac-do/huong-dan-chan-doan-va-dieu-tri-mot-so-benh-thuong-gap-o-tre.html`, file `https://kcb.vn/upload/2005611/20210723//Tre-em.rar` | Tải và giải nén trong scratchpad. Không ghi vào data/raw | rar 1b6db1425d1d6e4c; pdf a66c5e8bc460807c | 807 | ok (nhưng lớp chữ lỗi glyph: "ư" ra "ƣ", "µ" bị mất, ví dụ trang 29 ra "10g/kg") |

**TT51/2017 còn hiệu lực không, có sửa đổi không:** trang kcb.vn ghi "Đã có hiệu lực". Điều 7 (ảnh trang 3) nói TT51 có hiệu lực từ 15/02/2018 và **chỉ** làm hết hiệu lực TT08/1999/TT-BYT. Tôi không tìm thấy văn bản thay thế nào (tìm đến 9/2026). Một bản tóm tắt tìm kiếm (từ trang tư nhân) nói TT51 "được sửa đổi bởi NĐ 96/2023/NĐ-CP". Tôi **chưa kiểm được** điều này từ nguồn chính thức (trang lược đồ vbpl.vn tải động). Nếu có sửa, nhiều khả năng chỉ ở phần người được tiêm/hành nghề, không phải liều. Cần người kiểm (mục 5).

### 1b. Nguồn nước ngoài (chỉ giá trị + vị trí; không lưu đoạn văn)

| Hệ thống | Nguồn | Phiên bản | URL đã tải | fetched_at | sha256 (16) | Vị trí | Giá trị đã xác nhận bằng `sources grep` |
|---|---|---|---|---|---|---|---|
| EU_UK | RCUK Anaphylaxis algorithm 2021 | 2021 (file 2021-04; hướng dẫn phát hành 5/2021) | resus.org.uk/sites/default/files/2021-04/Anaphylaxis%20algorithm%202021.pdf | 2026-09-26 | c7b75e76a1fdba09 | tr. 1, ô liều adrenalin tiêm bắp | người lớn và trẻ > 12 tuổi: 500 µg; 6–12 tuổi: 300 µg; 6 tháng–6 tuổi: 150 µg; < 6 tháng: 100–150 µg; nhắc lại sau 5 phút |
| EU_UK | RCUK Emergency treatment of anaphylaxis: Guidelines for healthcare providers | 2021-05 | resus.org.uk/sites/default/files/2021-05/Emergency%20Treatment%20of%20Anaphylaxis%20May%202021_0.pdf | 2026-09-26 | 1c07e3dd4e238e92 | §5.1.1 (tr. 28–29 PDF) | cùng các bậc tuổi; thêm: cho 300 µg nếu trẻ > 12 tuổi nhỏ con hoặc chưa dậy thì; nhắc lại sau 5 phút (tr. 7, 13, 29) |
| EU_UK | Trang RCUK "Emergency treatment of anaphylactic reactions" (kiểm phiên bản) | — | resus.org.uk/library/additional-guidance/guidance-anaphylaxis/emergency-treatment-anaphylactic-reactions | 2026-09-26 | eb860f9833c0466e | — | Trang ghi bản mới nhất phát hành 5/2021. Bộ "Guidelines 2025" của RCUK không thay tài liệu phản vệ; trang vẫn dẫn file 2021. (Kết quả tìm kiếm nói bản 2025 chỉ đổi điểm tiêm bút tiêm thứ hai, **chưa kiểm**, không liên quan liều) |
| OTHER | WAO Anaphylaxis Guidance 2020 (World Allergy Organ J 2020;13:100472), PMC7607509 | 2020-10 | ebi.ac.uk/europepmc/webservices/rest/PMC7607509/fullTextXML (bản PMC qua Europe PMC. pmc.ncbi.nlm.nih.gov chỉ trả trang chặn bot 131 ký tự, sha b9ce887b…) | 2026-09-26 | 1d6a6919aeb0a10e | Đoạn ngay trước Bảng 6 và Bảng 6 | 0,01 mg/kg, tối đa 0,5 mg; bảng đơn giản: trẻ < 10 kg 0,01 mg/kg; 1–5 tuổi 0,15 mg; 6–12 tuổi 0,3 mg; thiếu niên và người lớn 0,5 mg; nhắc lại mỗi 5–15 phút. WAO chưa có hướng dẫn phản vệ mới hơn (WAO White Book 2026 chỉ là bài tổng quan) |
| US | AAAAI/ACAAI "Anaphylaxis: A 2023 practice parameter update" (Ann Allergy Asthma Immunol 2024;132:124) | 2024-02 | aaaai.org/.../Anaphylaxis-Practice-Paramaters-2023.pdf | 2026-09-26 | a4177e78a117c345 | tr. 4 và tr. 31 (PDF) | 0,01 mg/kg, tối đa 0,3 mg cho trẻ em và thiếu niên, 0,5 mg cho người lớn. Không có khoảng nhắc lại bằng số cho cơ sở y tế |
| EU_UK | EAACI guidelines: Anaphylaxis (2021 update), Allergy 2022;77:357 | 2021 | Wiley pdfdirect, onlinelibrary full, research.rug.nl, portal.findresearcher.sdu.dk | — | — | — | **Bị chặn 403 ở cả 4 nguồn** (cả `sources fetch` và WebFetch). Europe PMC: không có bản toàn văn. **Không ghi giá trị** (needs_human_check) |

---

## 2. Bảng mẩu

### 2a. Mẩu đã ghi vào JSONL
**Không có** (bản gốc). Lý do chung: `data/raw/TT51_2017.pdf` là bản quét và không có bản chính thức nào có lớp chữ. **[Lỗi thời từ 11:22: đã có sidecar OCR TT51; 3 mẩu đã ghi sau kiểm toán — bảng ở mục 7.2.]**

### 2b. Bản nháp: CHƯA ghi, CHƯA span_verified, giá trị Việt Nam đọc bằng mắt từ ảnh trang quét chính thức
Tôi đối chiếu việc đọc bằng mắt với bản đánh máy lại của Sở Y tế Lạng Sơn (khớp). Trạng thái dưới đây do `finalize()` tính trong scratchpad theo 3 cách hiểu tập giá trị Việt Nam:
- **A**: chỉ TT51 Phụ lục III.
- **A′**: TT51 Phụ lục III cộng sơ đồ Phụ lục X.
- **B**: hợp DR8 với QĐ 3942/2014 và QĐ 3312/2015.

Giá trị WAO và Mỹ dạng 0,01 mg/kg được quy ra µg theo cân nặng trong context.

| id nháp | slot | Quần thể | VN (TT51) | Nước ngoài | A | A′ | B | Trang PDF TT51 |
|---|---|---|---|---|---|---|---|---|
| D1 (hạt giống 15) | dose, µg; context {weight_kg:10, mg_per_ml:1, mg_per_ampoule:1} | trẻ 1 tuổi (12 tháng), 10 kg, phản vệ độ II–III, tại cơ sở y tế | PL III mục IV.1b: "Trẻ khoảng 10 kg: 0,25ml (tương đương 1/4 ống)" = 250 µg. PL X: trẻ em 1/5–1/3 ống = 200–333 µg | RCUK 2021: 150 µg (6 tháng–6 tuổi). WAO 2020: 100 µg (0,01 mg/kg × 10) và 150 µg (1–5 tuổi). Mỹ 2023: 100 µg | conflict (mồi mirror 350 µg, dung sai 50) | conflict (mồi 383 µg, dung sai 25) | **concordant** (VN thêm 100 µg và 150 µg). Nếu chỉ xét phản vệ do thuốc {250, 100}: conflict chỉ với 150 µg, nhưng WAO/Mỹ 100 µg trùng VN. Nếu coi 3942/3312 là bản bị thay: **indistinguishable** | 9 (PL III), 19–20 (PL X) |
| D2 (hạt giống 14) | dose, mg | người lớn | PL III mục IV.1e: "Người lớn: 0,5-1ml (tương đương 1/2 - 1 ống)" = 0,5–1 mg. PL X: 1/2 ống | RCUK 500 µg. WAO 0,5 mg. Mỹ tối đa 0,5 mg | concordant | concordant | concordant (VN thêm 0,3–0,5 mg của 3942 chương côn trùng đốt) | 9, 19–20 |
| D3 (mới) | duration (khoảng nhắc lại), đơn vị min | mọi tuổi, tại cơ sở y tế | PL III mục IV.3: "Tiêm nhắc lại adrenalin … 3-5 phút/lần". PL X: "Nhắc lại sau mỗi 3-5 phút" | RCUK: sau 5 phút. WAO: mỗi 5–15 phút | concordant (chạm biên 5) | concordant | concordant (VN thêm 5–15 phút của 3942 và 5–10 phút của 3312) | 9, 19–20 |
| D4 (mới) | dose, µg; weight_kg 35 | trẻ 10 tuổi, 35 kg | PL III mục IV.1d: "Trẻ > 30kg: 0,5ml (tương đương 1/2 ống)" = 500 µg. PL X: 200–333 µg | RCUK 300 µg (6–12 tuổi). WAO 300 µg (6–12 tuổi) và 350 µg (0,01 mg/kg). Mỹ 300 µg (tối đa ở trẻ) | conflict (mồi 650 µg) | conflict chỉ nhờ WAO 350 µg, cách VN 16,7 µg (dung sai 8,3). RCUK/Mỹ 300 µg nằm **trong** 200–333 | **concordant** (VN thêm 300 µg và 350 µg) | 9, 19–20 |

Nếu sau này có lớp chữ (OCR đã kiểm, hoặc bản chính thức có chữ), dựng mẩu như sau:
- Span D1/D2/D4 lấy từ PL III mục IV.1, trang 9 PDF, chép nguyên văn từ `--page`.
- Span D3 lấy từ mục IV.3, cùng trang.
- `section` = "Phụ lục III, mục IV", `printed_page` = "9".
- `conflict_family` gợi ý cho D1: `anaphylaxis_child_im_dose_rcuk_wao`.

---

## 3. Ứng viên bị loại và lý do

> Bảng dưới là **bản gốc**. Sau kiểm toán: D2, D3 và dòng "< 10 kg" (D6) đã **mở lại và ghi thành mẩu** (mục 7); D1, D4, D5 **giữ loại** với lý do đã sửa ở mục 7.4. Lý do (i) "bản quét" không còn đúng cho mọi dòng.

| Ứng viên | Lý do loại |
|---|---|
| D1 (hạt giống 15, trẻ 10 kg) | (i) TT51 là bản quét nên không kiểm span được. (ii) Về nội dung, chỉ là xung đột sạch khi bỏ qua QĐ 3942/2014 và QĐ 3312/2015. Theo DR8, mẩu là concordant. Nếu coi 2 QĐ đó là bản bị thay, mẩu là indistinguishable. **Chờ người quyết định trước khi dùng cho H1.** |
| D2 (hạt giống 14, người lớn) | Chỉ vì (i) bản quét. Về nội dung là đối chứng tốt, concordant ở mọi cách hiểu |
| D3 (khoảng nhắc lại) | Chỉ vì (i) bản quét. Là đối chứng được, nhưng khi chấm cần tập VN theo DR8 (3–5 phút; và 5–15, 5–10 phút nếu tính 3942/3312) |
| D4 (trẻ > 30 kg, ví dụ 10 tuổi 35 kg) | (i) bản quét. (ii) Sơ đồ PL X của chính TT51 cho trẻ em 1/5–1/3 ống (200–333 µg), chứa 300 µg của RCUK/Mỹ. Chỉ còn WAO 350 µg, cách tập VN 16,7 µg, quá sát để phân biệt. Theo DR8 là concordant. **Không phải xung đột sạch** |
| D5 (trẻ khoảng 20 kg: 0,3 ml = 300 µg) | Không dựng: 300 µg trùng RCUK/WAO cho 6–12 tuổi. 0,01 mg/kg × 20 = 200 µg nằm trong khoảng 200–333 của PL X và trùng 0,01 mg/kg của 3942/3312. Không có xung đột |
| "Trẻ sơ sinh hoặc < 10 kg: 0,2 ml" | Không dựng: RCUK < 6 tháng là 100–150 µg, nhưng TT51 gộp "sơ sinh hoặc < 10 kg" nên quần thể không khớp dải tuổi RCUK. WAO < 10 kg 0,01 mg/kg phụ thuộc cân nặng. Cần quy tắc cân nặng–tuổi riêng |
| EAACI 2021 | 403 ở cả 4 nguồn; không ghi giá trị từ trí nhớ |

---

## 4. SAI LỆCH SO VỚI BỘ HẠT GIỐNG (§3.3, seed_conflicts.yaml)

1. **Dòng 15, trạng thái "confirmed":** giá trị TT51 (0,25 ml = 250 µg cho trẻ khoảng 10 kg) **đúng** như bảng (đọc bằng mắt, trang 9). Nhưng trạng thái "xác nhận xung đột" **không vững**:
   - QĐ 3312/QĐ-BYT (2015), chương "Sốc phản vệ ở trẻ em", mục 4.2.1 (trang PDF 106, số in 106): "tiêm bắp Adrenalin 1/1000 (0,01 mg/kg), 0,01 ml/kg, hoặc ở trẻ em không biết cân nặng Adrenalin 1‰ 0,3 ml"; "Có thể nhắc lại 5 - 10 phút". Cùng văn bản, trang 30 và 55: "adrenalin TB liều 10mcg/kg", "Tiêm bắp adrenalin 10µg/kg".
   - QĐ 3942/QĐ-BYT (2014):
     - Chương Dị ứng thuốc, Bảng 3 (trang PDF 13, số in 8): "0,5 - 1 ml ở người lớn, 0,01 ml/kg, tối đa không quá 0,3 ml /lần ở trẻ em. Tiêm nhắc lại sau mỗi 5-15 phút".
     - Chương Dị ứng thức ăn (trang PDF 48, số in 43): "Trẻ em nặng 10-25kg: adrenaline 0,15mg tiêm bắp"; "> 25kg … 0.3mg"; người lớn "0,01mg/kg/ lần, tối đa 0.5mg/ lần"; "nhắc lại sau mỗi 5-15 phút".
     - Chương Dị ứng do côn trùng đốt (trang PDF 77, số in 72): người lớn 0,3–0,5 mg, trẻ em 0,01 mg/kg, nhắc lại mỗi 10 phút.
   - Như vậy **chính Bộ Y tế đã ghi cả 0,01 mg/kg (giá trị WAO/Mỹ) và 0,15 mg (giá trị RCUK) cho trẻ khoảng 10 kg**, trong hai văn bản kcb.vn vẫn đăng và TT51 không bãi bỏ. Theo §1.2/DR8, dòng 15 là concordant. Theo cách hiểu "đã bị thay" thì là indistinguishable. Trong cả hai trường hợp, một câu trả lời "0,01 mg/kg" hay "150 µg" **không** chứng minh mô hình theo chuẩn nước ngoài: có thể nó theo văn bản Việt Nam cũ hơn. Đây là nhiễu trực tiếp cho H1.
2. **Dòng 15, cột nước ngoài:** bảng chỉ ghi WAO "0,01 mg/kg". Bảng 6 của WAO 2020 còn có mức đơn giản **0,15 mg cho trẻ 1–5 tuổi**. Tập giá trị WAO cho trẻ 1 tuổi 10 kg là {100 µg, 150 µg}. Mỹ (AAAAI/ACAAI 2023) chưa có trong bảng: 0,01 mg/kg, tối đa 0,3 mg ở trẻ.
3. **Dòng 14:** "0,5–1 mg (TT51)" và "RCUK 0,5 mg" **đúng**. Loại khỏi xung đột và dùng làm đối chứng là đúng. Bổ sung: sơ đồ PL X của TT51 ghi người lớn "1/2 ống", vẫn trong khoảng.
4. **§3.3 viết "phản vệ cần cả RCUK và WAO/EAACI (0,01 mg/kg, tối đa 0,5 mg)":** WAO đã xác nhận đúng (tối đa 0,5 mg). EAACI **chưa kiểm được** (403).
5. **Nội bộ TT51 không thống nhất:** PL III ghi trẻ > 30 kg 0,5 ml, còn PL X ghi trẻ em 1/5–1/3 ống. PL III ghi người lớn 0,5–1 ml, còn PL X ghi 1/2 ống. PL III ghi "Theo dõi huyết áp 3-5 phút/lần", còn PL X ghi "Mạch, huyết áp 5-10 phút/lần". Theo §1.2 đây là mâu thuẫn nội bộ cần báo cáo như kết quả phụ.
6. Một kết quả tìm kiếm tóm tắt rằng TT51 đặt "khoảng 15 phút giữa các lần tiêm nhắc". Ảnh trang 9 và 19–20 cho thấy **3–5 phút**. Kết quả tìm kiếm đó sai và không được dùng.

---

## 5. Việc cần người kiểm ở HG1.2

1. **Quyết định khoa học/pháp lý (bắt buộc trước khi dùng phản vệ cho H1):** các đoạn phản vệ của QĐ 3942/2014 và QĐ 3312/2015 được xử lý thế nào?
   - (a) Là văn bản hiện hành: hợp DR8, dòng 15 thành concordant.
   - (b) Là bản đã bị TT51 thay trên thực tế (ghi `superseded`): dòng 15 thành indistinguishable.
   - (c) Ngoài kho: dòng 15 là conflict, nhưng phải ghi hạn chế trong bài.

   Đề xuất ghi quyết định vào `docs/DECISIONS.md`. Nên hỏi bác sĩ (HG3.9) xem bệnh viện Việt Nam đang dùng 0,01 mg/kg hay bảng theo cân nặng của TT51.
2. **Kiểm bằng mắt ảnh trang quét** `data/raw/TT51_2017.pdf` trang 9 (PL III mục IV.1–IV.3) và trang 19–20 (PL X): xác nhận các con số tôi chép ở mục 2b.
3. **Lớp chữ cho TT51:** duyệt OCR ở T2.4 (cần tesseract + tesseract-ocr-vie; máy chưa có), hoặc tìm bản chính thức có lớp chữ (Công báo, vbpl.vn/Bộ Tư pháp, emoh.moh.gov.vn) và quyết định nguồn nào được coi là chính thức. Danh sách `official_hosts` hiện chỉ có kcb.vn, moh.gov.vn, vncdc.gov.vn.
4. **EAACI 2021:** người dùng mở bản toàn văn (Allergy 2022;77:357, doi 10.1111/all.15032) và ghi liều tiêm bắp (mg/kg, tối đa, dải cân nặng của bút tiêm), khoảng nhắc lại và vị trí (bảng/mục).
5. **Tình trạng sửa đổi TT51:** kiểm trên vbpl.vn (lược đồ ItemID=128248) xem có văn bản sửa đổi/thay thế nào không (ví dụ lời nói "NĐ 96/2023" chưa kiểm).
6. **Tính hiện hành của QĐ 3942/2014 và QĐ 3312/2015:** tôi không tìm thấy văn bản thay thế. Cần xác nhận.
7. **Quy tắc cân nặng–tuổi cho câu hỏi:** "trẻ 1 tuổi nặng 10 kg" có hợp lý lâm sàng không (bác sĩ). RCUK 6 tháng–6 tuổi và WAO 1–5 tuổi đều bao trùm độ tuổi này.

---

## 6. Đề xuất sửa configs / mã (chưa sửa: ngoài quyền của task)

1. **Lỗi `src/vnsoc/match/decoys.py::mirror_decoy`:** hàm chọn giá trị nước ngoài gần nhất bằng `_gap` (có quy đổi đơn vị), nhưng rồi phản chiếu trên `f["lo"]/f["hi"]` và `v["lo"]/v["hi"]` **thô, chưa quy đổi**.
   - Ví dụ tái hiện: mẩu µg, `vn` = 500 µg, `foreign` có {lo:0.01, hi:0.01, unit:"mg/kg"} với weight_kg=35 → mồi "999.99 ug". `check_decoy` trả `[]`, tức không phát hiện.
   - Sửa: quy đổi cả `v` và `f` sang `atom["unit"]` bằng `nv.Num(...).to(unit, ctx)` trước khi tính `cv`, `cf`, `w`; thêm test.
   - Tạm thời: các agent nên ghi giá trị mg/kg dưới dạng µg đã quy đổi (task này đã làm vậy).
2. **`verify_span` cho văn bản quét:** hiện chỉ đọc lớp chữ PyMuPDF của `data/raw/<key>.pdf`. Đề xuất hai hướng:
   - (a) File OCR đi kèm (ví dụ `data/interim/ocr/TT51_2017.pages.jsonl`), mỗi con số đã được người so với ảnh trang (T2.4), và `verify_span` dùng khi PDF không có lớp chữ.
   - (b) Cho phép manifest chỉ định file ưu tiên cho một khóa (ví dụ `TT51_2017__<sha8>.pdf` từ nguồn chính thức có lớp chữ). Hiện bản sao khác sẽ bị `fetch_pdf` lưu dưới tên `__sha8` và `verify_span` bỏ qua.
3. **DR8 giữa nhiều văn bản:** `missing_vn_values` bắt mọi mục `vn` phải đọc lại được từ **một** `span`, nên không thể biểu diễn tập hợp giữa TT51 và QĐ 3942/3312 trong một mẩu. Đề xuất lưu nguồn cho từng giá trị (ví dụ `ValueItem.src = {guideline, page, span}`) hoặc trường `vn_extra_sources` trong Atom, mỗi nguồn kiểm span riêng.
4. **`normalize_vi`:**
   - Khoảng phân số "1/5-1/3 ống" đang được đọc thành 1 µg (giả định) và 333 µg, thay vì 200–333 µg. Cần luật cho khoảng phân số.
   - "10 kg" trong span bị đọc thành "10 ug (assumed)". Nên bỏ qua số đi kèm đơn vị cân nặng khi đơn vị mẩu là µg.
5. **Context cho mẩu phản vệ:** thêm `mg_per_ampoule: 1` (ngoài `mg_per_ml: 1`) để các câu trả lời "1/4 ống" được chấm. Đã thử: `parse_values("ĐÁP ÁN: 1/4 ống")` ra 250 µg khi có `mg_per_ampoule`.
6. `configs/grading.yaml` đã có `adrenaline: [adrenalin, epinephrine, epinephrin]`. Không cần thêm thuốc. Đơn vị `ug`, `mg`, `min` đã có trong UNIT_ALIASES.
7. **Kho văn bản (corpus-librarian):**
   - Đưa QĐ 3942/2014 và QĐ 3312/2015 vào danh sách xét DR8 cho chủ đề phản vệ. Cả hai chỉ có dạng .rar trên kcb.vn, nên cần hỗ trợ giải nén trong `fetch_pdf`, hoặc dùng bản bệnh viện đăng lại, ví dụ `benhvienhatrung.vn/wp-content/uploads/2021/09/3942-2014-qd-hddt-di-ung-mien-dich.pdf` (chưa tải, chưa kiểm).
   - Lớp chữ của QĐ 3312/2015 lỗi glyph "ƣ"/"µ". Nên sửa khi chuẩn hóa, nếu không `--find "10µg/kg"` sẽ trượt.

---

## 7. Sau kiểm toán (agent sửa lỗi, 2026-09-26 chiều)

Đầu vào: `anaphylaxis_verify.md` (integrity-auditor: pass 0 · fix 3 [D2, D3, D6] · reject 3 [D1, D4, D5]). Tôi tự kiểm lại bằng công cụ trước khi sửa; không tin số của báo cáo gốc hay của kiểm toán nếu chưa chạy lại. Mọi nhận xét lâm sàng dưới đây là của AI, **không phải bác sĩ**.

### 7.1 Kết quả

| Chỉ số | Kết quả |
|---|---|
| Mẩu trong `anaphylaxis.jsonl` | **3** — 1 conflict (P-anaphylaxis-03), 2 concordant (-01, -02) |
| `vnsoc.schemas atom` | `OK 3 dòng hợp lệ (atom)`, exit 0 |
| `vnsoc.extract.verify_span` | `OK: 0 mẩu không đạt` (3/3 OK; mọi span DR8 trong `extraction.dr8_sources` đều có đúng trang — công cụ nay hỗ trợ trường này) |
| `finalize()` chạy lại | trạng thái/dung sai lưu trong file = kết quả tính lại; `check_decoy` = [] cả 3 mẩu; `choose_decoy` cho đúng mồi đã lưu; `pilot_merge.source_warnings` = [] (mọi số nước ngoài có trong nguồn đã băm) |
| Cờ OCR | cả 3 mẩu có span chính trên trang OCR của TT51 → `extraction.ocr = true`; **phải có người so từng con số với ảnh trang** (§3.1) |
| Tính theo chỉ tiêu chủ đề (1–2 xung đột, 2 đối chứng) | 1 xung đột (chưa dùng được cho H1 xác nhận — xem 7.3) + 2 đối chứng |

### 7.2 Bảng mẩu

Văn bản Việt Nam dùng (đều đã có trong `data/raw`, không tải thêm): TT51/2017 (sha256 `cab611be9dd14312`, 20 trang, bản quét, lớp chữ OCR sidecar `data/interim/ocr/TT51_2017/`, meta sha khớp); QĐ 3942/2014 (`4be16be0fe6812f4`, 144 trang, lớp chữ); QĐ 3312/2015 (`a66c5e8bc460807c`, 807 trang, lớp chữ). `valid_from` TT51 = 2018-02-15 (Điều 7.1, OCR trang 3: "có hiệu lực từ ngày 15 tháng 02 năm 2018").

| id | slot / đơn vị | Quần thể | Tập VN (nguồn, trang PDF) | Nước ngoài (hệ thống: giá trị, phiên bản) | Trạng thái (dung sai; mồi) | Trang span chính |
|---|---|---|---|---|---|---|
| P-anaphylaxis-01 (D2, hạt giống 14) | dose, mg; ctx 60 kg, 1 mg/ml, 1 mg/ống | người lớn ≥ 18 tuổi, ~60 kg, phản vệ độ II–III do thuốc, tại cơ sở y tế, liều tiêm bắp đầu | 0,5–1 mg (TT51 PL III IV.1e, tr.9; PL X "1/2 ống", tr.20 và 3942 tr.13 "0,5 - 1 ml ở người lớn" nằm trong tập) | EU_UK RCUK 500 µg (2021-05) · OTHER WAO 0,5 mg (2020, 0,01 mg/kg áp trần) · US AAAAI/ACAAI 0,5 mg (2023, áp trần) · **WHO_global Prehospital pocket reference 0,5 mg ≥ 50 kg (2026-04-22, bối cảnh trước viện)** | **concordant** (0; không mồi) | 9 |
| P-anaphylaxis-02 (D3) | duration, phút | trẻ 5 tuổi, phản vệ độ II–III do thuốc, tại cơ sở y tế, khoảng tiêm bắp nhắc lại | 3–5 (TT51 PL X tr.20; = PL III IV.3 tr.9) ∪ 5–10 (3312 tr.106, DR8) ∪ 5–15 (3942 tr.13, DR8) | EU_UK RCUK 5 phút · OTHER WAO 5–15 · **WHO_global Pocket book 2013 5–15 (trẻ em)** · **WHO_global Prehospital 2026 5 phút** · US: không có số (AAAAI tr.29) | **concordant** (0; không mồi) | 20 |
| P-anaphylaxis-03 (D6) | dose, µg; ctx 6 kg, 1 mg/ml, 1 mg/ống | nhũ nhi 4 tháng, 6 kg, phản vệ độ II–III do thuốc, tại cơ sở y tế, liều tiêm bắp đầu | 200 µg (TT51 PL III IV.1a, tr.9) ∪ 200–333,3 µg (TT51 PL X "Trẻ em: 1/5-1/3 ống", tr.20) ∪ 0,01 mg/kg = 60 µg (3312 tr.106; 3942 tr.13 "0,01 ml/kg") | EU_UK RCUK **100–150 µg (< 6 tháng) ✗** · OTHER WAO 0,01 mg/kg = 60 ✓ · US 0,01 mg/kg = 60 ✓ · **WHO_global Pocket book 2013: 0,15 ml 1:1000 = 150 µg ✗** · **WHO_global Prehospital 2026: 0,15 mg ✗** | **conflict** (dung sai 3 µg; mồi 4–54 µg, `mirror_geom`) | 9 |

`conflict_family` của -03: `anaphylaxis_child_im_adrenaline_rcuk_age_band_150ug` — **dùng chung** với P-anaphylaxis_ocr-01/-05 (file `anaphylaxis_ocr.jsonl`) vì cùng gốc khác biệt (RCUK/WHO cho liều cố định theo tuổi ≈ 150 µg; Bộ Y tế theo cân nặng). Gộp họ để thống kê cụm không đếm thừa.

### 7.3 Đã sửa gì, giữ gì, khác kiểm toán ở đâu (và vì sao)

**D2 → P-anaphylaxis-01 (làm đúng theo kiểm toán).** Span "e) Người lớn: 0,5-1ml" (cắt trước "1⁄2 - ] ống" lỗi OCR); section PL III IV.1e; population cố định ~60 kg; context {weight_kg 60, mg_per_ml 1, mg_per_ampoule 1}; WAO/Mỹ ghi đã áp trần 0,5 mg; `extraction.ocr = true`. Tôi đã tự chạy lại: ở 45 kg WAO/Mỹ = 0,45 mg → conflict (mồi 1,05 mg) → **câu hỏi bắt buộc nêu ~60 kg** (ghi trong notes). **Thêm so với kiểm toán:** (i) `cause` = do thuốc để tập DR8 xác định (3942 ch. thức ăn và côn trùng, 3610 dị ứng dứa/ong đốt có giá trị người lớn khác — 0,3–0,5 mg — không áp); (ii) WHO_global từ *WHO Prehospital emergency care: pocket reference* (2026) — trùng 0,5 mg.

**D3 → P-anaphylaxis-02 (theo kiểm toán, có một điểm khác).** Như kiểm toán: trang 20 (PL X), slot `duration`, đơn vị `min`, `ocr = true`, không dùng trang 9 làm span (OCR "phúVlần" ngay tại đơn vị; ghi vị trí trang 9 trong `extraction.same_doc_locations`). **Khác:** kiểm toán để quần thể "mọi tuổi"; tôi đặt **trẻ 5 tuổi, do thuốc**, vì (1) câu hỏi phải hỏi một quần thể; (2) trẻ em có thêm nguồn DR8 riêng (3312 "5 - 10 phút") và có đối chiếu WHO nhi khoa (Pocket book); (3) người lớn đã có ở P-anaphylaxis_ocr-04 — tránh trùng. Span giữ dòng "- Trẻ em: 1/5-1/3 ống" để neo quần thể. Về "đối chứng yếu" mà kiểm toán nêu: theo DR8 (a), WAO/WHO 5–15 phút nằm **trọn** trong tập VN (3942 5–15); chỉ khi bỏ 3942/3312 thì mới là "chạm biên 5". Thử chấm: "10-15 phút" → correct (OTHER, WHO_global); "20 phút" → unattributed.

**D6 → P-anaphylaxis-03 (dựng theo kiểm toán, kèm cảnh báo).** Section PL III IV.1a, trang 9, span như kiểm toán, context {6 kg, 1 mg/ml, 1 mg/ống}. **Khác/bổ sung:**
- Nguyên nhân chọn **do thuốc** (không chọn "sau tiêm chủng" như gợi ý lâm sàng của kiểm toán) vì văn bản tiêm chủng hiện hành trong kho (TT13/2026) mới OCR 3/19 trang, chưa kiểm được nó có liều phản vệ riêng hay không. Tập VN không đổi nếu đổi nguyên nhân sang vắc xin (3312 áp mọi nguyên nhân ở trẻ em) — nhưng cần người xác nhận.
- **Mới: WHO_global cũng xung đột** (150 µg cố định cho trẻ em, cả Pocket book 2013 lẫn Prehospital 2026). Kiểm toán G7 ghi "chưa có đối chiếu WHO"; tôi lấy được qua API của WHO IRIS (UUID bitstream, không qua đường `bitstream/handle/...` bị trả HTML rỗng).
- `vn[1]` (PL X) ghi `hi = 1000/3` để mép trên "1/3 ống" đọc lại được từ chính span trang 20; **mép dưới "1/5" vẫn không đọc được** (lỗi `normalize_vi`, mục 7.6). Nếu không làm vậy, `vn[1]` chỉ "qua nhờ trùng số" (200 µg của span chính).
- **Mồi 4–54 µg** là kết quả bắt buộc của `choose_decoy` (auto: 2·60 − 125 < 0 → `mirror_geom` 60²/125 = 28,8 µg, giữ độ rộng 50 µg của RCUK). `check_decoy` = []. Nhưng mép dưới 4 µg vô lý lâm sàng (kiểm toán cũng nêu) — xem 7.6(4).
- **Lỗi chấm nghiêm trọng tìm thấy khi thử `grade_short`:** đáp án "0,01 ml/kg" (đúng theo 3942, cũng là cách viết của WAO) bị đọc thành 0,01 ml = 10 µg → rơi vào mồi → nhãn *unattributed* + `decoy_match`. Tức là một câu trả lời đúng theo Bộ Y tế bị tính là "trùng mồi", làm sai cả π_mồi của H1. **Không dùng -03 cho H1 cho tới khi sửa parser (7.6-1) và có quyết định DR8 (G5).**
- Thử chấm khác: "0,15 mg" → foreign [EU_UK, WHO_global]; "0,1 mg" → foreign [EU_UK]; "0,01 mg/kg", "60 mcg", "0,06 mg" → correct (trùng cả OTHER/US); "0,2 ml", "0,3 ml" → correct; "0,05 mg" → unattributed + mồi.

Độ nhạy trạng thái của -03 (tôi tự chạy `finalize` + `choose_decoy`; kiểm toán chỉ liệt kê A/A′/B):

| Cách hiểu tập VN | Trạng thái | Dung sai | Mồi |
|---|---|---|---|
| (a) DR8 hợp tập TT51 + 3312 + 3942 [bản ghi] | conflict | 3 µg | 4–54 µg (mirror_geom) |
| (b) 3942/3312 là bản đã bị TT51 thay (ghi `superseded` 60 µg) | **indistinguishable** (WAO/Mỹ 60 µg trùng bản cũ) | 25 | — |
| Chỉ TT51 (PL III + PL X) | conflict | 25 | **không có** (cả 3 quy tắc trùng tập VN) |
| Chỉ TT51 PL III | conflict | 25 | 250–300 µg (nằm trong PL X → mồi là giá trị Bộ Y tế) |
| (a) nhưng bỏ WHO | conflict | 3 | 4–54 |
| (a) nhưng bỏ RCUK (chỉ WHO 150) | conflict | 25 | không có mồi hợp lệ |

→ -03 chỉ là "xung đột có mồi" dưới cách hiểu (a) — đúng quy tắc DR8 đã đăng ký, nhưng mồi xấu và phụ thuộc quyết định G5. Kết luận của kiểm toán ("ứng viên duy nhất sống qua mọi cách hiểu DR8") **không đúng hoàn toàn**: dưới (b) nó thành indistinguishable.

**Giữ loại (reject), đã chuyển khỏi JSONL (vốn rỗng) và ghi lý do cập nhật:**

| Ứng viên | Lý do loại (sau kiểm toán) |
|---|---|
| D1 (hạt giống 15; trẻ ~10 kg) | Lý do "bản quét" lỗi thời. Lý do nội dung đứng vững: trạng thái phụ thuộc quyết định G5 và nguyên nhân (DR8 + do thuốc: conflict chỉ với RCUK/WAO 150 µg và **WHO 150 µg**; do thức ăn: concordant vì 3942 tr.48 "10-25kg: 0,15mg"; (b): indistinguishable). 10 kg nằm đúng biên "under 10 kg"/"1-5 years" của WAO. Phiên bản đã dựng có nêu nguyên nhân là P-anaphylaxis_ocr-01/-02 (file khác) — không dựng trùng ở đây. |
| D4 (trẻ > 30 kg, 10 tuổi 35 kg) | Như báo cáo gốc: PL X 200–333 µg chứa 300 µg của RCUK/Mỹ; chỉ còn WAO 350 µg cách tập VN 16,7 µg (dung sai 8,5) → thực chất không phân biệt được; theo DR8 là concordant. **Mới:** nếu WHO Pocket book (150 µg "trẻ em") được coi là áp cho trẻ 10 tuổi, mẩu sẽ thành conflict chỉ nhờ WHO — cần người quyết định phạm vi tuổi của nguồn WHO trước khi dựng lại (liên quan P-anaphylaxis_ocr-06). |
| D5 (trẻ ~20 kg, 0,3 ml) | **Lý do gốc sai** ("300 µg trùng RCUK/WAO 6–12 tuổi, không có xung đột" chỉ đúng khi trẻ ≥ 6 tuổi). Lý do đúng: cùng cấu trúc với D1 (phụ thuộc G5 và nguyên nhân: 3942 ch. thức ăn 10–25 kg 0,15 mg); "khoảng 20 kg" nằm đúng biên 6 tuổi của RCUK nên quần thể không cho một giá trị nước ngoài duy nhất; TT51 PL III không có mức 21–30 kg (G9). Bản đã dựng có cố định 5 tuổi là P-anaphylaxis_ocr-05 (file khác). |

### 7.4 Kiểm lại các khẳng định của kiểm toán (bằng công cụ)

- TT51 OCR trang 3: Điều 6.2 "phải xử trí cấp cứu phản vệ theo quy định tại Phụ lục III, Phụ lục IV"; Điều 7.2 làm hết hiệu lực TT08/1999 — **đúng**. PL III mục I.1 (OCR trang 8) "Tất cả trường hợp phản vệ" — **đúng**.
- Ảnh trang 9 và 20 (`data/cache/page_images/TT51_2017_p009.png`, `_p020.png`, tôi xem bằng mắt — là AI đọc, **không** thay kiểm tay của người): các số ở IV.1 a–e, IV.3 "3-5 phút/lần", ô TIÊM BẮP "Người lớn: 1/2 ống - Trẻ em: 1/5-1/3 ống, Nhắc lại sau mỗi 3-5 phút" — **khớp**. Xác nhận thêm lỗi OCR G2: "≥ 90mmHg" → "> 90mmHg", "1/2 - 1 ống" → "1⁄2 - ] ống", "phút/lần" → "phúVlần", và ký tự "6" thừa ở trang 20.
- 3942 tr.13, 48, 77 và 3312 tr.106 (kèm tr.103 phạm vi "mọi nguyên nhân"; tr.29, 30, 55 cùng giá trị 10 µg/kg) — **đúng nguyên văn**.
- RCUK tr.29 (< 6 tháng 100–150 µg; 6 tháng–6 tuổi 150; 6–12 tuổi 300; > 12 tuổi và người lớn 500), nhắc lại sau 5 phút (tr.7, 9, 13, 29, 31) — **đúng** (`sources grep`, sha `1c07e3dd…`). WAO (sha `1d6a6919…`) và AAAAI/ACAAI (sha `a4177e78…`) — **đúng** như kiểm toán.

### 7.5 Kiểm DR8 trong kho hiện có (mới)

Tôi quét **toàn bộ 62 PDF trong `data/raw`** (quét 2 lần, lần sau lúc ghi báo cáo) (lớp chữ hoặc OCR) tìm trang có đồng thời "adrenalin/epinephrin" + "phản vệ/SPV" + "tiêm bắp/TB": chỉ có TT51 (tr.3, 9, 11, 16, 19, 20), 3942 (tr.13, 15, 48, 77, 143), 3312 (tr.29, 30, 32, 55, 106) và **QĐ 3610/2015 – Ngộ độc** (tr.124, 133, 166). 3610 chỉ có giá trị theo nguyên nhân riêng: ong đốt tr.133 "0,3-0,5 ml dung dịch 1/1000"; dị ứng dứa tr.166 "adrenalin tiêm bắp 0,3-0,5 mg/lần, lặp lại sau 5- 15 phút" (người lớn) — không áp cho quần thể "do thuốc" của 3 mẩu, đã ghi trong `dr8_not_applied`. QĐ 1493/2015 (hồi sức tích cực) và 1494/2015 (huyết học) nhắc phản vệ nhưng không có liều tiêm bắp. **Giới hạn:** văn bản ngoài kho (ví dụ hướng dẫn phản vệ trong tiêm chủng, các trang TT13/2026 chưa OCR) chưa được kiểm.

### 7.6 Sai lệch mới so với bộ hạt giống (bổ sung mục 4)

1. **Dòng 15 thiếu WHO:** WHO_global (Pocket book of hospital care for children 2013 §4.6.4, PDF tr.133; Prehospital emergency care pocket reference 2026, PDF tr.9/11) cho trẻ em **0,15 mg cố định**, trùng RCUK 6 tháng–6 tuổi. §3.3 nói "WHO không mặc nhiên là nước ngoài" — ở chủ đề này WHO **khác** Bộ Y tế (TT51) cho trẻ em. Hệ quả cho file `anaphylaxis_ocr.jsonl` (không thuộc quyền sửa của tôi, đề xuất cho agent phụ trách/người gộp): -01 và -05 nên thêm WHO_global (xung đột); -03/-04 thêm WHO (trùng); **-06 (10 tuổi 35 kg) có thể đổi từ concordant sang conflict** nếu nguồn WHO "trẻ em" được coi là áp cho 10 tuổi.
2. **Rủi ro quy nguồn của 150 µg** rộng hơn báo cáo trước: 150 µg = RCUK = WHO = QĐ 3942 ch. dị ứng thức ăn (10–25 kg) = bút tiêm 0,15 mg của Mỹ (kê đơn ngoài cơ sở y tế, không ghi làm giá trị đối chiếu). Với -03 (6 kg), đáp án 150 µg được chấm là EU_UK + WHO_global, trong khi mô hình có thể lấy từ kiến thức bút tiêm Mỹ — ghi cho phân tích độ nhạy theo kho đối chiếu.
3. Dòng 14 (đối chứng): đúng; đã dựng (-01) và trùng P-anaphylaxis_ocr-03 — **khi gộp chỉ giữ một** (`pilot_merge` hiện chỉ loại trùng `atom_id`, không loại trùng slot + quần thể).

### 7.7 Việc cần người ở HG1.2 (tồn đọng)

1. **So số với ảnh trang (bắt buộc cả 3 mẩu):** `data/raw/TT51_2017.pdf` trang PDF 9 (IV.1a "0,2ml … 1/5 ống", IV.1e "0,5-1ml") và trang PDF 20 (ô TIÊM BẮP: "Người lớn: 1/2 ống", "Trẻ em: 1/5-1/3 ống", "Nhắc lại sau mỗi 3-5 phút"). Span là văn bản OCR ("TIEM BAP", dấu "*" thay "•") — so theo nghĩa và con số.
2. **Quyết định G5 (DR8) và ghi `docs/DECISIONS.md`:** (a) hợp tập, (b) 3942/3312 là bản bị thay, hay khác; và DR8 có áp **theo nguyên nhân** không (chương thuốc/ thức ăn/ côn trùng). Quyết định này đổi trạng thái -03 (conflict ↔ indistinguishable) và các mẩu trẻ em của `anaphylaxis_ocr`.
3. **Nguồn WHO:** mở 2 link WHO (Pocket book: PDF tr.133; Prehospital: PDF tr.9), xác nhận 0,15 ml/0,15 mg, nhắc lại 5–15/5 phút; quyết định (i) Pocket book 2013 có còn là bản hiện hành không (tìm trên IRIS bằng API không thấy bản mới; *WHO consolidated guidelines for the management of common childhood illness* 2026 đang ra theo mô-đun — chưa thấy mô-đun phản vệ, cần kiểm), (ii) nguồn trước viện 2026 có dùng được cho quần thể "tại cơ sở y tế" không, (iii) phạm vi tuổi "trẻ em" của WHO (nhũ nhi 4 tháng? trẻ 10 tuổi?).
4. **Mồi của -03** (4–54 µg): statistician/người dùng quyết định trước đóng băng có đăng ký luật mồi bổ sung (phản chiếu qua mép xa, hoặc sàn hợp lý lâm sàng) hay giữ nguyên; nếu đổi phải ghi DECISIONS + addendum.
5. **Bác sĩ thật (HG3.9):** tình huống "nhũ nhi 4 tháng, 6 kg, phản vệ độ II–III sau tiêm kháng sinh" có hợp lý; bệnh viện Việt Nam dùng bảng cân nặng TT51 hay 0,01 mg/kg; ô "Trẻ em: 1/5–1/3 ống" của PL X có áp cho nhũ nhi không.
6. **TT08/1999/TT-BYT** (bản bị TT51 thay): chưa tra được (hết lượt WebSearch của phiên; không có trong kho). Cần người tìm bản chính thức và ghi liều trẻ em/khoảng nhắc lại nếu có → điền `superseded`.
7. **EAACI 2021** (doi 10.1111/all.15032): vẫn chưa có (403, không thử lại).

### 7.8 Đề xuất sửa mã/config (không tự sửa)

1. **`normalize_vi` — đơn vị `ml/kg` (ưu tiên cao, ảnh hưởng chấm):** thêm alias `ml/kg` và cạnh `("ml/kg","mg/kg") = mg_per_ml`. Hiện "0,01 ml/kg" → 10 µg → rơi vào mồi của -03 (7.3). Thêm test: `parse_values("ĐÁP ÁN: 0,01 ml/kg")` với ctx {6 kg, 1 mg/ml} phải ra 60 µg.
2. **Khoảng phân số** "1/5-1/3 ống" (ra "1 [giả định]" và 333,3 µg) — cần luật `FRACTION_RANGE`. Đồng thời chuẩn hóa dấu gạch phân số U+2044 ("1⁄3", OCR trang 9) thành "/" trong `clean()`/`norm()`.
3. **`pilot_merge`: loại trùng theo (guideline, slot_type, intervention, population)** giữa các file chủ đề — hiện P-anaphylaxis-01 và P-anaphylaxis_ocr-03 đều sẽ vào `pilot_atoms.jsonl`.
4. **Luật mồi (đăng ký trước):** khi `mirror_arith` ≤ 0 và `mirror_geom` cho mép dưới rất nhỏ (ở đây 4 µg), cân nhắc luật dự phòng đã định trước (phản chiếu qua mép xa của tập VN, hoặc sàn = ½ giá trị VN nhỏ nhất). Chỉ đổi nếu kịp trước đóng băng và ghi DECISIONS.
5. **Chỉ mục nguồn nước ngoài:** các URL WHO IRIS dạng `bitstream/handle/...` trả HTML rỗng (sha `a859cc83…`, 6 URL); dùng API `server/api/pid/find?id=<handle>` → `items/<uuid>/bundles` → `bitstreams/<uuid>/content` (đã làm được cho 2 tài liệu WHO ở đây). Nên ghi cách này vào skill counterpart-matching.
6. `configs/grading.yaml`: không cần thêm thuốc (đã có `adrenaline`). Đơn vị `ug`, `mg`, `min`, `kg`, `ampoule` đã có trong UNIT_ALIASES; chỉ thiếu `ml/kg` (mục 1).

### 7.9 Thao tác của tôi (minh bạch)

- Ghi: `data/interim/pilot/anaphylaxis.jsonl` (3 dòng, dựng bằng script trong scratchpad rồi ghi bằng Write; nội dung trùng byte với bản dựng, chỉ khác kết thúc dòng LF) và file này (thêm mục 7; thêm ghi chú "lỗi thời/cập nhật" ở đầu file, mục 2a và mục 3; không xóa nội dung gốc).
- Tải qua `vnsoc.match.sources fetch` vào `data/cache/foreign/`: WHO Pocket book 2013 (`…/bitstreams/8f110da0-22e6-4ef1-90e4-c9f1b7daa363/content`, sha256 `e17581cf0829bea6`, 438 trang) và WHO Prehospital emergency care pocket reference 2026 (`…/bitstreams/10bda57b-b351-4d3a-9dd2-e85c8b521306/content`, sha256 `72ac8bee6a1810a8`, 22 trang). Tra metadata IRIS bằng curl vào scratchpad (JSON, không lưu vào dự án).
- Không sửa `data/raw`, `data/frozen`, `state/`, `configs/`, `src/`, `tests/`, `docs/`, `.claude/`, và không sửa `anaphylaxis_ocr.jsonl`.
