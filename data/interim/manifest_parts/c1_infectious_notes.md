# c1_infectious: ghi chú phân loại và tải văn bản (T2.1 + T2.2)

Ngày: 2026-09-26 · agent: corpus-librarian · file dữ liệu: `data/interim/manifest_parts/c1_infectious.jsonl` (16 dòng; `python -m vnsoc.schemas manifest` báo OK 16 dòng hợp lệ). Mọi dòng có `sha256` đều khớp đúng file `data/raw/<số>_<năm>.pdf` (đã kiểm lại bằng máy).

**Giới hạn công cụ:** hạn mức WebSearch của phiên đã hết (200/200) ngay từ lệnh tìm đầu tiên, nên tôi không dùng được máy tìm kiếm. Tôi cũng không lách giới hạn này bằng máy tìm kiếm khác. Thay vào đó, tôi dùng công cụ tìm kiếm có sẵn trên chính các trang chính thức: `kcb.vn/page/search`, `vncdc.gov.vn/tim-kiem.html`, và API thư viện media WordPress (`/wp-json/wp/v2/media?search=`) của các bệnh viện công. Tôi cũng tận dụng URL mà các agent thí điểm đã tìm (dengue_report.md, malaria_report.md, rabies_report.md) và kiểm lại từng URL bằng `fetch_pdf` (kết quả `exists_same`).

## 1. Bảng văn bản

| Khóa | Tiêu đề ngắn | Host | text_kind | Trang | Hiệu lực (theo điều khoản đã đọc) |
|---|---|---|---|---|---|
| 2760/2023 | HD chẩn đoán, điều trị SXH Dengue | file.medinet.gov.vn (SYT TP.HCM) | ok | 104 | **Hiện hành.** Thay 3705/2019 (Điều 1, tr. PDF 1) |
| 3705/2019 | HD chẩn đoán, điều trị SXH Dengue | file.medinet.gov.vn (cùng file ở benhvienhatrung.vn) | scanned_or_empty | 75 | Bị 2760/2023 thay. Bãi bỏ 458/2011 (Điều 2, tr. 1, đọc ảnh). **Có watermark LuatVietnam** |
| 458/2011 | HD chẩn đoán, điều trị SXH Dengue | — (không tìm thấy) | — | — | Bị 3705/2019 bãi bỏ |
| 292/2024 | HD chẩn đoán và điều trị bệnh tay chân miệng | benhvienhatrung.vn (sao y SYT Thanh Hóa) | scanned_or_empty | 24 | **Hiện hành.** Thay 1003/2012 (Điều 1, tr. 1, đọc ảnh). Công văn kcb.vn ngày 30/3/2026 vẫn dẫn 292/2024 |
| 1003/2012 | HD chẩn đoán, điều trị bệnh TCM | — (chỉ có bản LuatVietnam, không dùng) | — | — | Bị 292/2024 thay |
| 3377/2023 | HD chẩn đoán và điều trị bệnh Sốt rét | benhvienhatrung.vn (sao y SYT Thanh Hóa) | scanned_or_empty | 23 | **Hiện hành.** Thay 2699/2020 (Điều 1, tr. 1, đọc ảnh) |
| 2699/2020 | HD chẩn đoán, điều trị bệnh Sốt rét | quantri.impe-qn.org.vn (Viện SR-KST-CT Quy Nhơn) | ok | 30 | Bị 3377/2023 thay. Thay 4845/2016 (Điều 1 của file QĐ riêng, tr. 1) |
| 4845/2016 *(mới thêm)* | HD chẩn đoán, điều trị bệnh Sốt rét | — (không tìm thấy) | — | — | Bị 2699/2020 thay. Bản trước nó: chưa rõ |
| 1622/2014 | HD giám sát, phòng chống bệnh dại trên người | — (chỉ có .doc trên vncdc.gov.vn) | — | — | Không có điều khoản thay thế. Chưa thấy văn bản thay nó (chưa quét hết) |
| 1840/2025 | [CHƯA XÁC MINH] cúm mùa | — (không tìm thấy) | — | — | Chưa xác minh được cả việc văn bản tồn tại |
| 2078/2011 | HD chẩn đoán và điều trị cúm mùa | benhvienhatrung.vn (**bản gõ lại**, Word 2019) | ok | 5 | Không có điều khoản thay thế. Đề cương ghi bị 1840/2025 thay, **chưa xác nhận** |
| 1019/2025 | [CHƯA XÁC MINH] sởi | — (không tìm thấy) | — | — | Chưa xác minh được cả việc văn bản tồn tại |
| 1327/2014 | HD chẩn đoán, điều trị bệnh Sởi | benhvienhatrung.vn (bản quét 2014) | scanned_or_empty | 14 | Bãi bỏ 476/2009 (Điều 2, tr. 1, đọc ảnh). Đề cương ghi bị 1019/2025 thay, **chưa xác nhận** |
| 5642/2015 | HD chẩn đoán và điều trị một số bệnh truyền nhiễm | kcb.vn | ok | 86 | Không có điều khoản thay thế (tr. 3). kcb.vn ghi "Đã có hiệu lực" |
| 6101/2019 | HD chẩn đoán, điều trị bệnh Whitmore | benhvienhatrung.vn (bản ký số VOffice) | scanned_or_empty | 6 | Không có điều khoản thay thế (tr. 1, đọc ảnh) |
| 3610/2015 | HD chẩn đoán và xử trí ngộ độc (gồm rắn cắn) | kcb.vn | ok (**lỗi glyph ư**) | 228 | PDF không có trang QĐ. kcb.vn ghi "Đã có hiệu lực". Chưa đọc được điều khoản thay thế |

Tổng: 16 dòng (15 văn bản được giao + 4845/2016 mới thêm).
- **10 dòng có PDF trong data/raw.** 5 file có lớp chữ: 2760/2023, 2699/2020, 5642/2015, 3610/2015 (cần chuẩn hóa glyph) và 2078/2011 (bản gõ lại). 5 file là bản quét: 3705/2019 (thêm watermark tư nhân), 292/2024, 3377/2023, 1327/2014, 6101/2019.
- **6 dòng không có PDF chính thức:** 458/2011, 1003/2012, 4845/2016, 1622/2014 (chỉ có .doc), 1840/2025, 1019/2025.

PDF mới tải vào data/raw trong task này (qua `fetch_pdf`, status `downloaded`): `3610_2015.pdf`, `292_2024.pdf`, `6101_2019.pdf`, `1327_2014.pdf`, `2078_2011.pdf`. Các file đã có từ trước, tôi chỉ xác nhận lại bằng URL (`exists_same`): `2760_2023`, `3705_2019`, `3377_2023`, `2699_2020`, `5642_2015`.

Chuỗi thay thế đã xác nhận bằng điều khoản trong chính văn bản:
- Dengue: 458/2011 → 3705/2019 → 2760/2023
- Tay chân miệng: 1003/2012 → 292/2024
- Sốt rét: 4845/2016 → 2699/2020 → 3377/2023
- Sởi: 476/2009 → 1327/2014 → (1019/2025: chưa xác nhận)
- Cúm: 2078/2011 → (1840/2025: chưa xác nhận)

## 2. Kết quả trái kỳ vọng và cảnh báo

1. **3705/2019: bản duy nhất tìm được có watermark LuatVietnam** (logo ở chân ảnh trang 1; agent dengue cũng thấy watermark trên mọi trang). Cùng một file (cùng sha256) được hai nơi đăng lại: BV quận Phú Nhuận trên medinet.gov.vn và BVĐK Hà Trung. Hai bệnh viện đã đăng lại bản lấy từ thư viện pháp luật tư nhân. Đây không phải bản gốc sạch.
2. **Bảng đề cương ghi "chuỗi 6 phiên bản" cho sốt rét.** Tôi chỉ xác nhận được 3 mắt xích từ điều khoản văn bản: 3377/2023 → 2699/2020 → 4845/2016.
3. **1840/2025 (cúm mùa) và 1019/2025 (sởi): không tìm thấy trên mọi nguồn chính thức duyệt được.** Tôi chưa xác minh được hai văn bản này có tồn tại không, cũng như tiêu đề, ngày ban hành và việc chúng thay 2078/2011 và 1327/2014. Hai công văn của Cục KCB về sởi trên kcb.vn (8/2024 và 12/2024) chỉ viết "Hướng dẫn chẩn đoán, điều trị bệnh sởi đã được Bộ Y tế ban hành", không nêu số. Theo quy tắc "status theo chuỗi thay thế đã xác nhận", 2078/2011 và 1327/2014 đang để `current`, kèm cảnh báo trong notes. **Không được hiểu `current` ở hai dòng này là đã khẳng định còn hiệu lực.**
4. **2078/2011 là bản gõ lại** (Microsoft Word 2019, tạo ngày 23/8/2022, trùng ngày bệnh viện đăng), không phải bản gốc có dấu. Mọi span lấy từ bản này phải đối chiếu với bản gốc.
5. **3610/2015 có lớp chữ lỗi glyph:** dùng "ƣ/Ƣ" (U+01A3/U+01A2) thay cho "ư/Ư" (2.843 lần). `verify_span --find 3610/2015 "HƯỚNG DẪN CHẨN ĐOÁN VÀ XỬ TRÍ NGỘ ĐỘC"` trả `[]`, còn `"HƢỚNG DẪN CHẨN ĐOÁN"` trả `[1]`. Nếu chưa chuẩn hóa, mọi span có chữ "ư" sẽ thất bại. Các file 2760/2023, 2699/2020, 5642/2015 và 2078/2011 không bị lỗi này.
6. **5642/2015 trùng chủ đề với các hướng dẫn chuyên bệnh mới hơn:** có chương "Sốt rét kháng thuốc" (trang sách 33) và "Cúm mùa" (trang sách 49). Không văn bản nào tôi đã đọc ghi rằng nó thay các chương này. Báo cáo controls đề xuất ghi `partial`, nhưng đó là suy luận ("nhiều khả năng"), chưa có điều khoản xác nhận, nên tôi để `current` và ghi rõ trong notes. PDF trên kcb.vn chỉ gồm 14 bệnh (86 trang). Phần phụ lục in các QĐ cũ (dengue, TCM, não mô cầu…; trang sách 87–144) không có trên mạng.
7. **1622/2014 là hướng dẫn giám sát – phòng chống** (do Cục Y tế dự phòng đề xuất), không phải hướng dẫn chẩn đoán – điều trị của Cục KCB. Bản chính thức duy nhất là file .doc.
8. **2760/2023 có hai bản chính thức khác sha256** (tem văn thư SYT TP.HCM và bản đăng tại Hà Trung). Lớp chữ của hai bản trùng khớp 104/104 trang, chỉ khác dòng tem. Manifest ghi bản TP.HCM (đang nằm trong data/raw). Bản Hà Trung không được đưa vào data/raw, để tránh tạo file trùng.

## 3. Văn bản không tìm được bản chính thức (và nơi đã tìm)

| Khóa | Đã tìm ở đâu, từ khóa gì | Ghi chú |
|---|---|---|
| 458/2011 | Tìm kiếm nội bộ kcb.vn ("Dengue", "sốt xuất huyết", "điều trị sốt xuất huyết Dengue", "458"). Media benhvienhatrung.vn ("458", "dengue", "sot-xuat-huyet", "hddt"). bvbnd.vn, benhviennhitrunguong.gov.vn, bvtb.org.vn | Tên và ngày lấy từ Điều 2 của 3705/2019 |
| 1003/2012 | Tìm kiếm nội bộ kcb.vn ("tay chân miệng", "điều trị bệnh tay chân miệng", "1003"). Media benhvienhatrung.vn, bvbnd.vn, benhviennhitrunguong.gov.vn, bvtb.org.vn | Chỉ thấy bản dàn trang LuatVietnam (Hà Trung đăng lại, sha256 90d69e2a…). Không dùng |
| 4845/2016 | Media benhvienhatrung.vn ("sot-ret", "hddt"). impe-qn.org.vn mục "Văn bản của Bộ Y tế" (chỉ liệt kê từ 2017). kcb.vn ("sốt rét" = 0 kết quả) | Mới thêm (lần ngược chuỗi) |
| 1622/2014 | kcb.vn ("dại", "bệnh dại", "phòng bệnh dại", "vắc xin phòng dại", "1622" = 0 kết quả). Media benhvienhatrung.vn ("1622", "dai", "benh-dai"). benhviennhitrunguong.gov.vn. Tìm kiếm vncdc.gov.vn ("dại") | Có bản .doc chính thức trên vncdc.gov.vn (sha256 feee9c61…). fetch_pdf không nhận .doc. Link PDF cũ (syt.kontum.gov.vn) đã chết |
| 1840/2025 | kcb.vn ("cúm", "cúm mùa", "điều trị cúm", "1840", "Quyết định 1840"). vncdc.gov.vn ("cúm mùa"; trang dừng cập nhật khoảng 2/2025). Media benhvienhatrung.vn (liệt kê mọi PDF đăng từ 2025). bvbnd.vn, benhviennhitrunguong.gov.vn, bvtb.org.vn. moh.gov.vn là ứng dụng JS nên không duyệt được | Chưa xác minh được việc văn bản tồn tại |
| 1019/2025 | Như trên, với từ khóa "sởi", "bệnh sởi", "điều trị bệnh Sởi", "1019". Đã đọc thêm 2 công văn về sởi trên kcb.vn | Chưa xác minh được việc văn bản tồn tại |

Không truy cập trang thư viện pháp luật tư nhân bị chặn. Kết quả tìm kiếm của các agent trước cho 3705/2019 và 1622/2014 chỉ trỏ tới trang đó hoặc các trang tư nhân khác.

## 4. Văn bản mới phát hiện

- **Không tìm thấy văn bản 2025–2026 nào thay thế văn bản trong danh sách.** Công văn hỏa tốc của Bộ Y tế ngày 30/3/2026 (đăng trên kcb.vn) vẫn dẫn 292/2024 cho tay chân miệng. Tin Whitmore ngày 23/4/2026 trên kcb.vn không nêu văn bản mới. Mục lục IMPE Quy Nhơn vẫn để 3377/2023 là bản sốt rét mới nhất.
- **4845/2016** (sốt rét): thêm dòng, là mắt xích trước 2699/2020.
- **Có nêu, không thêm dòng:** QĐ 476/2009 (sởi; bị 1327/2014 bãi bỏ). QĐ 5152/QĐ-BYT ngày 12/12/2014, "Hướng dẫn chẩn đoán và điều trị rắn lục xanh đuôi đỏ cắn" (có trang trên kcb.vn và bản đăng lại tại benhvienhatrung.vn/wp-content/uploads/2022/06/5152-2014-hddt-ran-luc-xanh-duoi-do-can.pdf; chưa tải). Văn bản này liên quan đến chương "Rắn lục cắn" trong 3610/2015, nhưng chưa rõ bản nào thay bản nào.
- **Nguồn đăng lại hữu ích cho các cụm khác:** thư viện media của BVĐK Hà Trung (`benhvienhatrung.vn/wp-json/wp/v2/media?search=hddt`) có khoảng 80 hướng dẫn chẩn đoán – điều trị của Bộ Y tế, ví dụ 3312/2015, 3942/2014, 1493/2015, 4815/2020, 3931/2015, 2065/2021, 3310/2019, 5481/2020, 5904/2019, 1314/2020 và 2957/2020. Cần kiểm từng file: có watermark tư nhân không, có phải bản gõ lại không.

## 5. Việc cho người dùng (HG2.3)

1. **1840/2025 (cúm mùa) và 1019/2025 (sởi):** xác nhận hai văn bản này có tồn tại không, rồi tìm PDF chính thức, tốt nhất là bản ký số trên kcb.vn, moh.gov.vn hoặc cổng Sở Y tế. Nếu có, chạy `fetch_pdf --key 1840/2025 --url <url>` (tương tự cho 1019/2025) và cho agent đọc điều khoản thay thế. Hai dòng 2078/2011 và 1327/2014 phụ thuộc vào kết quả này.
2. **3705/2019:** tìm bản sạch, không có watermark LuatVietnam, tốt nhất có lớp chữ. Nếu không có, quyết định có chấp nhận bản quét đang có hay không (chỉ dùng cho phân tích phiên bản; cần OCR và so tay).
3. **1003/2012, 458/2011, 4845/2016:** tìm bản chính thức nếu muốn dùng trong phân tích phiên bản TCM, dengue và sốt rét.
4. **1622/2014:** quyết định có chấp nhận bản .doc chính thức của vncdc.gov.vn làm nguồn hay không (xem đề xuất mã 2). Đồng thời xác nhận văn bản này chưa bị thay sau khi thành lập Cục Phòng bệnh năm 2025.
5. **Bản quét cần OCR** mới trích mẩu được. Hiện hành: 292/2024, 3377/2023, 6101/2019. Bản cũ: 3705/2019, 1327/2014. Tổng là 5 trên trần 10 văn bản OCR của đề cương.
6. **2078/2011:** nếu dùng cho phân tích phiên bản, cần đối chiếu bản gõ lại với bản gốc.
7. **Nếu muốn tìm tiếp bằng máy:** tăng `CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION` (hạn mức hiện đã hết), hoặc tự tìm và đưa URL.

## 6. Đề xuất sửa mã/config (không tự sửa)

1. **`src/vnsoc/extract/verify_span.py` / `normalize_vi.py`:** thêm bước ánh xạ U+01A3→U+01B0 (ƣ→ư) và U+01A2→U+01AF (Ƣ→Ư) khi chuẩn hóa văn bản trang. Lỗi này có trong 3610/2015 và theo báo cáo phản vệ còn có trong 3312/2015. Cân nhắc cho `fetch_pdf.text_quality` gắn cờ `glyph_substitution` khi tỷ lệ ƣ/ư cao.
2. **`src/vnsoc/extract/fetch_pdf.py`:** (a) nhận .doc/.docx từ host chính thức, lưu file gốc kèm sha256 và chuyển sang văn bản bằng công cụ tất định (antiword hoặc LibreOffice), gắn cờ `derived_from_doc` (cùng đề xuất với rabies_report.md); (b) thêm tùy chọn `verify=False` có ghi log cho host chính thức có chứng chỉ hết hạn (vncdc.gov.vn); (c) ghi URL, sha256 và ngày tải vào một nhật ký nối thêm, ví dụ `data/raw/FETCH_LOG.jsonl`. Trong task này, file 2760_2023.pdf đã nằm trong data/raw mà không có URL nguồn, và tôi chỉ truy lại được nhờ báo cáo thí điểm dengue.
3. **`configs/project.yaml` → `corpus.official_hosts`:** hiện chỉ có kcb.vn, moh.gov.vn và vncdc.gov.vn. Cần quyết định có thêm các host đăng lại được chấp nhận hay không (file.medinet.gov.vn của SYT TP.HCM, benhvienhatrung.vn, quantri.impe-qn.org.vn). Nên kèm quy tắc loại file có watermark hoặc dàn trang của thư viện pháp luật tư nhân (LuatVietnam), ví dụ kiểm chuỗi "LuatVietnam" trong lớp chữ và gắn cờ khi nghi có logo trong ảnh.
