# c2_viral_tb: viêm gan, HIV, lao (T2.1 + T2.2)

Người làm: agent corpus-librarian. Ngày: 2026-09-26.
Manifest: `data/interim/manifest_parts/c2_viral_tb.jsonl`, 11 dòng. `python -m vnsoc.schemas manifest` trả về OK.

Tôi xác nhận lại nguồn của mọi PDF có trong manifest bằng cách chạy lại `vnsoc.extract.fetch_pdf` với URL chính thức. Kết quả là `exists_same`, hoặc `clash_kept_both` và băm trùng với file `__c43006cb` đã có. Tôi cũng đọc trang 1–3 của từng file bằng `verify_span --page`. Mọi đoạn trích điều khoản trong notes đều được kiểm lại bằng `verify_span --find`, trừ bản quét 3310/2019: bản đó tôi đọc bằng mắt trên ảnh trang.

## 1. Bảng văn bản

| Khóa | Tiêu đề ngắn | Host | text_kind | Trang | Hiệu lực (theo điều khoản đã đọc) |
|---|---|---|---|---|---|
| 1740/2026 | HD chẩn đoán, điều trị viêm gan vi rút B | kcb.vn | ok | 42 | **current**. Điều 3 tr.1 thay 3310/2019 |
| 3310/2019 | HD chẩn đoán, điều trị bệnh viêm gan vi rút B | admin.medinet.gov.vn (Sở Y tế TP.HCM) | **scanned_or_empty** | 18 | superseded bởi 1740/2026. Điều 2 (ảnh tr.2) bãi bỏ 5448/2014 |
| 5448/2014 *(thêm)* | HD chẩn đoán, điều trị bệnh viêm gan vi rút B | kcb.vn | ok | 10 | superseded, bị 3310/2019 bãi bỏ |
| 2855/2024 | HD viêm gan vi rút C | — | — | — | **không tìm thấy**. "current" chỉ theo đề cương, chưa xác nhận |
| 2065/2021 | HD viêm gan vi rút C (cũ) | — | — | — | **không tìm thấy**. "superseded" chỉ theo đề cương, chưa xác nhận |
| 5968/2021 | HD điều trị và chăm sóc HIV/AIDS | soyte.laichau.gov.vn | ok (lỗi glyph "ƣ") | 145 | **current**. Điều 2 tr.1 thay 5456/2019. Chưa thấy văn bản nào thay nó |
| 5456/2019 | HD điều trị và chăm sóc HIV/AIDS (cũ) | vaac.gov.vn (**chưa tải được**) | — | — | superseded bởi 5968/2021 (theo Điều 2 của 5968) |
| 678/2025 | Dự phòng lây truyền mẹ–con HIV, giang mai, viêm gan B | — | — | — | **không tìm thấy** |
| 162/2024 | HD chẩn đoán, điều trị và dự phòng bệnh Lao | bvtn.org.vn (BV Thống Nhất) | ok (lỗi glyph Cyrillic) | 213 | **current**. Điều 3 tr.1 thay 1314/2020 |
| 1314/2020 | HD chẩn đoán, điều trị và dự phòng bệnh lao | www.bvbnd.vn (BV Bệnh Nhiệt đới TP.HCM) | ok | 142 | superseded bởi 162/2024; bị thay một phần bởi tài liệu 2760/2021. Điều 3 tr.1 thay 3126/2018 |
| 2760/2021 | Cập nhật HD điều trị bệnh lao kháng thuốc | cms-chonglao.benhvienphoitrunguong.vn | ok | 53 | "superseded" là **suy luận**. **Chưa xác nhận danh tính số hiệu** |

Kết quả: tải hoặc xác nhận được 7/11 văn bản trong data/raw (6 có lớp chữ, 1 bản quét). 1 văn bản tìm thấy URL chính thức nhưng không tải được (5456/2019). 3 văn bản không tìm thấy (2855/2024, 2065/2021, 678/2025).

Chuỗi thay thế đã xác nhận từ chính văn bản:
- Viêm gan B: 5448/2014 → 3310/2019 (Điều 2, bãi bỏ; đọc trên ảnh) → 1740/2026 (Điều 3, tr.1).
- HIV: 5456/2019 → 5968/2021 (Điều 2, tr.1).
- Lao: 4263/2015 → 3126/2018 → 1314/2020 → 162/2024. Mắt xích 4263 → 3126 đọc trên ảnh QĐ 2018 của kcb.vn. Hai mắt xích sau là Điều 3, tr.1 của 1314 và của 162. 1314/2020 bị thay tr.43–53 bởi tài liệu "Cập nhật HD điều trị lao kháng thuốc", tức file 2760_2021.pdf, tr.1.

## 2. Cảnh báo phải xử lý trước khi trích mẩu

1. **`data/raw/3310_2019.pdf` SAI NHÃN. Tôi đã kiểm độc lập.**
   - File này có sha256 `e2b720f8…`, 8 trang, từ benhvienhatrung.vn. Dòng đầu ghi "Ban hành kèm theo Quyết định số: 3310/QĐ-BYT ngày 29 tháng 07 năm 2019", nhưng nội dung là hướng dẫn 5448/2014:
     - độ giống văn bản với 5448_2014.pdf là 0,835;
     - câu "HBV-DNA ≥ 105 copies/ml (20.000 IU/ml)" (tr.3) có nguyên văn trong 5448;
     - file không có TAF và ULN 35/25 U/L. Bản quét chính thức tr.4 thì có cả hai.
   - Bản 3310 chính thức duy nhất trong data/raw là `3310_2019__c43006cb.pdf`. Đây là bản quét, chưa OCR được.
   - `verify_span` mặc định đọc `3310_2019.pdf`, nên mọi lệnh `--page/--find 3310/2019` hiện trả về **văn bản sai**. Mọi giá trị "bản cũ 3310" lấy theo đường mặc định đều không hợp lệ.
2. **Lỗi glyph lớp chữ** (text_kind vẫn là `ok`). Span phải cắt nguyên từ văn bản trang, không gõ lại.
   - 5968/2021: 2.032 ký tự "ƣ/Ƣ" (U+01A3/01A2) thay cho "ư/Ư", trên 137/145 trang.
   - 162/2024: 1.102 "ӟ" (U+04DF) thay cho "ớ" và 231 "ү" (U+04AF) thay cho "ẫ". Ví dụ: "Hưӟng dүn".
   - 1740/2026 tr.37: "≥" được mã hóa bằng ký tự PUA U+F0B3 (font Symbol) trong "F ≥ 2", "F ≥ 3". Dấu so sánh ở đây không đọc được.
3. **2760_2021.pdf không có trang quyết định.** Chuỗi "2760" không xuất hiện ở trang nào. Bằng chứng bổ trợ duy nhất: 162/2024 tr.201 dẫn "sơ đồ 3.1. 2 (QĐ 2760 của BYT)", khớp với "Sơ đồ 3.1.2" ở tr.37 của file này. Số hiệu và ngày ký cần người xác nhận.
4. **162/2024 không có số và ngày trong PDF.** Lớp chữ để trống số và ngày, không có dấu số hiệu. Số 162 chỉ biết qua trang bvtn.org.vn. File đã qua Ghostscript (2026-02-01). `issued` để null.
5. **Số hiệu bản lao 2018: 3126 hay 3216?** Tiêu đề trang kcb.vn ghi "3216/QĐ-BYT ngày 23/5/2018". Còn văn bản 1314/2020 và ảnh QĐ 2018 do chính kcb.vn đăng (1 trang quét, ký VOffice) đều ghi **3126**. Vậy tiêu đề trang kcb.vn gõ nhầm. Manifest dùng "3126/2018".

## 3. Không tìm được và nơi đã tìm

WebSearch đã hết hạn mức phiên (200/200) ngay từ đầu task, nên tôi chỉ duyệt được từng trang chính thức và dùng ô tìm kiếm nội bộ của chúng.

| Khóa | Nơi đã tìm (từ khóa) |
|---|---|
| 2855/2024 | kcb.vn (tìm nội bộ: "2855/QĐ-BYT", "viêm gan vi rút C", "vi rút C", "HCV"; mục phac-do, tai-lieu, thu-vien-tai-lieu chỉ có viêm gan A/B/D/E); vaac.gov.vn ("2855", "viêm gan C"; danh mục QĐ trang 1–4); vncdc.gov.vn; benhnhietdoi.vn (chỉ có bài viết *trích dẫn* 2855/QĐ-BYT, không có PDF); bvbnd.vn; tudu.com.vn; medinet.gov.vn; bvtn.org.vn |
| 2065/2021 | kcb.vn ("2065/QĐ-BYT", "viêm gan vi rút C", "HCV"); vaac.gov.vn; vncdc.gov.vn; benhnhietdoi.vn; bvbnd.vn; medinet.gov.vn |
| 678/2025 | kcb.vn ("678/QĐ-BYT", "lây truyền HIV", "mẹ sang con", "giang mai"); vaac.gov.vn ("678", "mẹ sang con", "giang mai", "loại trừ lây truyền"; trang này ngừng cập nhật sau 12/2024); vncdc.gov.vn; benhnhietdoi.vn; tudu.com.vn; bvbnd.vn; medinet.gov.vn |
| 5456/2019 | **Tìm thấy** trên vaac.gov.vn (`/files/huong-dan-dieu-tri-va-cham-soc-hiv-dang-web.pdf`, bản sách NXB Y học 144 trang, không có trang quyết định), nhưng fetch_pdf từ chối vì chứng chỉ TLS của vaac.gov.vn hết hạn |

Các cổng không dùng được với công cụ hiện có:
- moh.gov.vn: cổng SPA, và requests báo `DH_KEY_TOO_SMALL`.
- vaac.gov.vn, vncdc.gov.vn: chứng chỉ hết hạn.
- Trang Chương trình Chống lao Quốc gia (chonglao.benhvienphoitrunguong.vn): danh mục văn bản tải bằng JS, và API danh mục không công khai.

Tôi không tìm tới trang thư viện pháp luật tư nhân.

## 4. Văn bản mới phát hiện

- **Không phát hiện văn bản 2025–2026 nào thay thế** 5968/2021, 162/2024 hay 1740/2026 trong các nguồn đã duyệt được. Đây *không* phải bằng chứng là chúng không tồn tại, vì chưa kiểm được moh.gov.vn.
- Tôi thêm dòng **5448/2014**. Đây là bản *cũ* trong chuỗi viêm gan B, file đã có sẵn trong data/raw, và tôi đã xác nhận nguồn kcb.vn. Dòng này hữu ích cho phân tích phiên bản.
- Tôi có ghi nhận nhưng không thêm dòng:
  - **3126/QĐ-BYT ngày 23/5/2018** (lao; chưa tải vào data/raw; bản trên kcb.vn chỉ là 1 trang quyết định quét).
  - **3286/QĐ-BYT ngày 05/11/2024** (vaac.gov.vn: *kế hoạch* điều trị viêm gan C cho người nhiễm HIV, không phải hướng dẫn chuyên môn).

## 5. Đề xuất sửa mã/config (không tự sửa)

1. `vnsoc.extract.verify_span.pdf_path`: cho phép chọn file theo `sha256` trong manifest, hoặc thêm bảng ánh xạ khóa → tên file. Khi đó 3310/2019 sẽ trỏ tới `3310_2019__c43006cb.pdf`. Nên thêm test để khóa có file sai nhãn không bao giờ được dùng.
2. `verify_span.norm` và `fetch_pdf.text_quality`:
   - chuẩn hóa `ƣ→ư`, `Ƣ→Ư`, `ӟ→ớ`, `ү→ẫ`;
   - ánh xạ PUA của font Symbol (U+F0B3 → "≥", U+F0A3 → "≤", U+F02B → "+", U+F02D → "−", U+F0B7 → "•");
   - `text_quality` nên báo `glyph_substitution` khi đếm được các ký tự này.

   Cần test hai chiều, vì span đã lưu dạng thô sẽ phải khớp sau khi chuẩn hóa.
3. `fetch_pdf`: thêm tùy chọn TLS cho các host chính thức trong `configs/project.yaml: corpus.official_hosts`. Cụ thể: cho phép chứng chỉ hết hạn, hoặc dùng `SECLEVEL=1` cho khóa DH yếu. Mặc định vẫn tắt, và khi dùng thì ghi `tls_verified: false` vào JSON và notes. Cần thêm `vaac.gov.vn` vào `official_hosts` nếu người dùng đồng ý đây là nguồn chính thức (Cục Phòng, chống HIV/AIDS thuộc Bộ Y tế).
4. `fetch_pdf`: ghi mỗi lần tải vào nhật ký, ví dụ `logs/fetch_pdf.jsonl` (key, url, sha256, status). Lần này tôi phải dựa vào báo cáo thí điểm để tìm lại URL của các file đã có.

## 6. Việc cho người dùng (HG2.3)

1. **Tải tay từ nguồn chính thức** (moh.gov.vn, Cục KCB, hoặc Sở Y tế): QĐ **2855/QĐ-BYT (2024)** viêm gan C, **2065/QĐ-BYT (2021)** viêm gan C, **678/QĐ-BYT (2025)** dự phòng lây truyền mẹ–con. Ghi lại URL để agent chạy fetch_pdf, hoặc đặt file vào chỗ agent chỉ định.
2. **5456/2019**: mở `https://vaac.gov.vn/files/huong-dan-dieu-tri-va-cham-soc-hiv-dang-web.pdf` bằng trình duyệt (chứng chỉ trang đã hết hạn) và tải về. Hoặc duyệt đề xuất 3 ở mục 5.
3. **3310_2019.pdf sai nhãn**: agent bị cấm sửa data/raw, nên người dùng cần quyết định cách xử lý:
   - (a) đổi tên file sai nhãn, ví dụ thành `3310_2019__MISLABELED_5448content.pdf`, và đưa `3310_2019__c43006cb.pdf` về tên chuẩn; hoặc
   - (b) duyệt đề xuất 1 ở mục 5.
4. **Xác nhận danh tính 2760/2021**: tìm trang quyết định (số, ngày ký) của "Cập nhật hướng dẫn điều trị bệnh lao kháng thuốc" (4/2021). Đồng thời xác nhận văn bản này còn hay hết hiệu lực sau 162/2024.
5. **Xác nhận ngày ký 162/2024.** Đề cương ghi 19/01/2024, nhưng PDF không có ngày.
6. Kiểm trên moh.gov.vn xem có hướng dẫn HIV, lao hoặc viêm gan C nào ban hành 2025–2026 thay các văn bản trên hay không. Hạn trước ngày đóng băng kho 15/10/2026.
