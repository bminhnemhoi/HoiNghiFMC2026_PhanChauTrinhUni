# c3_ncd — Bệnh không lây nhiễm, tim mạch, thận, sản (T2.1 + T2.2)

Người làm: agent corpus-librarian, 2026-09-26. File dữ liệu: `data/interim/manifest_parts/c3_ncd.jsonl` (18 dòng: 15 dòng được giao và 3 văn bản thêm). Kiểm schema: `vnsoc.schemas manifest` trả OK, 18 dòng hợp lệ. Sha256 của cả 15 dòng có file đã được so lại với `data/raw/<khóa>.pdf` và đều khớp.

**Giới hạn của lượt này:** WebSearch đã dùng hết hạn mức phiên (200/200) ngay từ lệnh đầu tiên, nên không tìm được trên web rộng. Tôi chỉ tìm trong các trang chính thức và trang bệnh viện bằng công cụ tìm kiếm riêng của từng trang: tìm kiếm kcb.vn, dotquy.kcb.vn, daithaoduong.kcb.vn, danh mục bvdksadec.vn, thư viện media WordPress của benhvienhatrung.vn và benhvienquynhon.gov.vn, danh mục bvphcnbg.com. Ngoài ra tôi dùng bản sao toàn bộ danh mục API kcb.vn mà một agent khác tải hôm nay vào scratchpad `kcb/`. Không truy cập trang thư viện pháp luật tư nhân.

## 1. Bảng văn bản

| Khóa | Tiêu đề ngắn | Host nguồn | text_kind | Số trang | Hiệu lực (căn cứ) |
|---|---|---|---|---|---|
| 3192/2010 | HD CĐ&ĐT tăng huyết áp | kcb.vn | ok | 19 | current. PDF không có trang QĐ; trang kcb.vn/van-ban ghi "Đã có hiệu lực"; không thấy bản mới hơn |
| 5904/2019 | HD CĐ, ĐT, quản lý BKLN tại trạm y tế xã | benhvienquynhon.gov.vn | **scanned_or_empty** | 22 | current. Tr.1 Điều 3 (ảnh + OCR) chỉ bãi bỏ Phần 2 của 2919/2014 |
| 5481/2020 | HD CĐ&ĐT ĐTĐ típ 2 | benhviendakhoabaria.vn | ok | 77 | current. Tr.1 Điều 3 thay 3319/2017 (máy đọc được); bị 1353/2021 sửa một phần |
| 3319/2017 | HD CĐ&ĐT ĐTĐ típ 2 (bản cũ) | kcb.vn | ok | 37 | superseded (5481 tr.1). Trang QĐ riêng: Điều 3 bãi bỏ phần ĐTĐ típ 2 của 3879/2014 |
| 1353/2021 | QĐ sửa đổi, bổ sung 5481/2020 | benhviendakhoabaria.vn | ok | 1 | current (văn bản sửa đổi) |
| 1470/2024 | HD quốc gia sàng lọc, quản lý ĐTĐ thai kỳ | bvdkbaclieu.gov.vn | **scanned_or_empty** | 31 | current. Tr.1 Điều 3 thay 6173/2018 (**chỉ đọc bằng mắt**) |
| 6173/2018 ➕ | HD quốc gia dự phòng, kiểm soát ĐTĐ thai kỳ | benhvienhatrung.vn | ok | 31 | superseded (theo 1470/2024) |
| 1857/2022 | HD CĐ&ĐT suy tim cấp và mạn | kcb.vn | ok | 27 | current. Tr.1 Điều 3 thay 1762/2020 (lớp OCR không dấu + ảnh) |
| 1762/2020 | HD CĐ&ĐT suy tim mạn tính | kcb.vn | ok | 22 | superseded (1857 tr.1) |
| 5331/2020 | HD CĐ và xử trí đột quỵ não | bvdksadec.vn | ok | 71 | current, **hiệu lực chưa xác nhận** (không tìm thấy 3312/2024) |
| 3312/2024 | [chưa xác minh] HD đột quỵ | — | — | — | **không tìm thấy; chưa xác minh văn bản có tồn tại** |
| 2388/2024 | HD CĐ&ĐT bệnh thận mạn và một số bệnh lý thận | kcb.vn | ok | 192 | current. Tr.1 Điều 3 bãi bỏ 4 bài của 3931/2015 |
| 3931/2015 | HD CĐ&ĐT bệnh thận – tiết niệu | kcb.vn | ok | 202 | **partial** (2388/2024) |
| 1154/2024 | HD sàng lọc, CĐ, xử trí THA thai kỳ, TSG, SG | drive.google.com (liên kết từ bvdksadec.vn) | ok | 33 | current. Điều 3 thay 1911/2021 (**chỉ đọc bằng mắt** trên bản quét ký số) |
| 1911/2021 | HD sàng lọc và điều trị dự phòng TSG | — | — | — | superseded (theo 1154/2024); không tìm thấy file |
| 2892/2022 | [chưa xác minh] HD béo phì | — | — | — | **không tìm thấy** |
| 2919/2014 ➕ | TL HD khám, chữa bệnh tại trạm y tế xã, phường | benhvienhatrung.vn | scanned_or_empty (**âm tính giả**) | 408 | partial (5904/2019 bãi bỏ Phần 2) |
| 3280/2011 ➕ | HD CĐ&ĐT ĐTĐ týp 2 (2011) | kcb.vn | ok | 18 | current tạm thời, **hiệu lực chưa xác nhận**; nguồn gốc tệp đáng ngờ |

➕ = văn bản thêm, không có trong danh sách giao.

Tệp mới tải hôm nay qua `fetch_pdf` (status downloaded): 1857/2022, 1762/2020, 2388/2024, 3931/2015, 5331/2020, 1154/2024, 6173/2018, 2919/2014, 3280/2011.

Tệp đã có sẵn, tôi tải lại và `fetch_pdf` báo exists_same (URL nguồn được xác nhận qua sha256): 3192/2010, 3319/2017 (URL kcb.vn), 5481/2020, 1353/2021, 1470/2024, 5904/2019 (bản quét).

Bản 5904 có lớp chữ (`5904_2019__9e6bbe13.pdf`) được xác nhận nguồn bằng cách tải lại vào scratchpad và so sha256. Tôi không tải qua `fetch_pdf` để tránh ghi lại tệp clash.

## 2. Chuỗi thay thế

Chuỗi đã xác nhận bằng máy, tức điều khoản đọc được trong lớp chữ PDF:
- 3319/2017 → 5481/2020: 5481 tr.1, Điều 3.
- 5481/2020, bị sửa một phần bởi 1353/2021: 1353 tr.1, Điều 1. Chỉ sửa điểm b, mục 3, trang in 37 (insulin cho bệnh nặng không nguy kịch) và thêm một người biên soạn.
- 3931/2015, bị bãi bỏ một phần bởi 2388/2024: 2388 tr.1, Điều 3. Bốn bài bị bãi bỏ là 5 "Bệnh thận IgA", 6 "Viêm thận Lupus", 7 "Bệnh thận đái tháo đường" và 21 "Bệnh thận mạn". **Các bài 18 "THA trong bệnh thận mạn", 22 "Bệnh thận mạn giai đoạn cuối" và 23 "Thiếu máu ở bệnh thận mạn" vẫn còn hiệu lực**, nên hiệu lực phải gắn tới từng mẩu.

Chuỗi xác nhận bằng lớp OCR chất lượng thấp, có đối chiếu ảnh trang:
- 1762/2020 → 1857/2022: 1857 tr.1.
- 2919/2014, bị bãi bỏ Phần 2 bởi 5904/2019: 5904 tr.1, Điều 3.
- 3879/2014, bị bãi bỏ phần ĐTĐ típ 2 bởi 3319/2017: căn cứ là trang QĐ riêng của 3319 trên kcb.vn, bản quét 1 trang, sha256 `ca840b6d…`, chỉ lưu ở scratchpad.

Chuỗi **chỉ đọc bằng mắt** (bản quét, chưa kiểm được bằng máy):
- 6173/2018 → 1470/2024: 1470 tr.1, Điều 3.
- 1911/2021 → 1154/2024: tr.1 Điều 3 của bản quét ký số trên Drive. Tệp này sha256 `ea8043c0…`, chỉ lưu ở scratchpad.

Chuỗi trong đề cương **chưa xác nhận được**:
- 5331/2020 → 3312/2024: không tìm thấy văn bản 3312/2024.

Không có văn bản nào thay 3192/2010. **3192/2010 và 5904/2019 cùng hiệu lực** (DR8).

Việc cho bước hợp nhất: cụm c5_listing đang ghi `3879/2014` là current mà chưa có `partially_amended_by`. Cần thêm `"3319/2017"` vì Điều 3 trong QĐ 3319 bãi bỏ nội dung ĐTĐ típ 2 của 3879/2014. Ghi chú của c5 nói "rối loạn lipid máu (tr.247–264)", nhưng tr. PDF 247 thực ra là **Chương 5 "Bệnh béo phì"** (`verify_span --find 3879/2014 "Chương 5"` cho kết quả [8, 247]).

## 3. Không tìm được và nơi đã tìm

- **3312/2024 (đột quỵ).** Đã tìm ở các nơi sau:
  - kcb.vn: tìm kiếm trang với "3312", "đột quỵ", "đột quỵ não", "xử trí đột quỵ"; danh mục API toàn bộ. "3312" chỉ ra **3312/QĐ-BYT năm 2015, "HD CĐ&ĐT một số bệnh thường gặp ở trẻ em"**.
  - dotquy.kcb.vn: tìm "3312", "5331", "quyết định", "hướng dẫn chẩn đoán".
  - bvdksadec.vn: danh mục "Hướng dẫn chẩn đoán và điều trị", 5 trang. HD đột quỵ duy nhất là 5331/2020.
  - benhvienhatrung.vn: media "3312" và "dot-quy" chỉ ra 3312/2015 và 5331/2020.
  - benhvienquynhon.gov.vn (media) và bvphcnbg.com: không có.

  **Nghi đề cương nhầm số với 3312/2015 (trẻ em).** Nếu không có HD đột quỵ năm 2024 thì bản hiện hành là 5331/2020.
- **2892/2022 (béo phì).** Đã tìm ở kcb.vn ("2892", "béo phì", "thừa cân"; API), daithaoduong.kcb.vn (các trang béo phì, trang HD, trang dự thảo), bvdksadec.vn, benhvienhatrung.vn, benhvienquynhon.gov.vn và bvphcnbg.com. Không thấy.
- **1911/2021 (tiền sản giật, bản cũ).** Đã tìm ở kcb.vn, bvdksadec.vn, benhvienhatrung.vn ("1911", "san giat", "sang loc"), benhvienquynhon.gov.vn và sannhiphuyen.vn (tìm kiếm WordPress). Tên và ngày trong manifest lấy từ Điều 3 của 1154/2024.

## 4. Văn bản mới phát hiện

- **Không thấy văn bản 2025–2026 nào thay các văn bản của cụm** trên kcb.vn. Tôi đã quét toàn bộ danh mục API kcb.vn (tải hôm nay) tìm các mục từ 2024 trở đi có chủ đề THA, ĐTĐ, suy tim, đột quỵ, thận, TSG, béo phì. Chỉ thấy 2388/2024 và 1760/2024 (ĐTĐ típ 1 trẻ em, đã có trong c5). **Chưa kiểm được moh.gov.vn** vì trang dùng JavaScript và không có ô tìm kiếm dùng được.
- **6173/2018** (ĐTĐ thai kỳ, bản trước 1470/2024): đã tải và có lớp chữ. Đây là bản cũ dùng cho phân tích phiên bản, và có lớp chữ trong khi 1470 là bản quét.
- **2919/2014** (khám chữa bệnh tại trạm y tế xã, Phần 2 bị 5904 bãi bỏ): đã tải.
- **3280/2011** (HD ĐTĐ týp 2 năm 2011, vẫn nằm trong danh mục kcb.vn/phac-do): **không văn bản nào tôi đọc được bãi bỏ nó.** Các văn bản đã đọc là 5481 tr.1, trang QĐ của 3319 và trang QĐ của 3879 (tr.3). Nếu 3280 còn hiệu lực thì sẽ ảnh hưởng DR8 cho các mẩu ĐTĐ. **Cảnh báo:** siêu dữ liệu của tệp trên kcb.vn ghi title/author "LawSoft", tức tệp được xuất từ trang thư viện pháp luật tư nhân rồi đăng lại. Đây không phải bản ký gốc, nên không dùng để tạo mẩu khi chưa có người xác nhận.
- Trùng số: **1470/QĐ-BYT năm 2021** là HD bệnh thận mạn giai đoạn cuối trong dịch COVID-19, có trên kcb.vn. Đây là ví dụ thứ hai cho thấy khóa phải là (số, năm).

## 5. Kết quả trái kỳ vọng và cảnh báo cho các bước sau

1. **Dòng hạt giống 13 (béo phì).** Không tìm thấy 2892/2022. Nhưng 3879/2014 Chương 5 (tr. PDF 247) có cả Bảng 1 tiêu chuẩn châu Á (béo phì độ 1: 25–29,9) và Bảng 2 theo WHO (béo phì độ 1: 30–34,9), và tr.249 ghi áp dụng cả hai bảng. Theo DR8, giá trị WHO chung có thể cũng "đúng theo Bộ Y tế", nên cần xét trước khi coi là xung đột.
2. **5904/2019.** File khóa là bản quét 22 trang và thiếu phần lớn tài liệu. Bản toàn văn có lớp chữ nằm ở biến thể `__9e6bbe13` (68 trang). `verify_span` theo khóa sẽ đọc bản quét, nên cần quyết định đổi file chuẩn. Các agent pilot THA/ĐTĐ đã nêu việc này.
3. **1470/2024** chỉ có bản quét (Bạc Liêu và Sa Đéc đều vậy). Chưa có OCR thì không tạo mẩu được.
4. **1154/2024** chỉ lấy được qua Google Drive do bệnh viện liên kết. Cần người chấp nhận host này hoặc tìm bản khác.
5. **3192/2010** tr.2, Bảng 2: lớp chữ có lỗi đánh máy ("140 – 150", "110 – 109"), không dùng bảng này.
6. Lớp chữ của **5331/2020** và của bản 5904 `__9e6bbe13` dùng ký tự "ƣ/Ƣ" (U+01A3/U+01A2) thay cho "ư/Ư". Span có chữ ư phải chép đúng như lớp chữ, còn tìm kiếm có dấu chuẩn sẽ trượt.
7. **2919/2014** bị `fetch_pdf` gắn nhãn scanned_or_empty do 4 trang đầu là ảnh bìa. Thực tế 380/408 trang có lớp chữ tiếng Việt.
8. Trên kcb.vn, tên tệp có dấu tiếng Việt có lúc phải mã hóa **NFD** mới tải được. Ví dụ: trang QĐ 3319 báo 404 khi mã hóa NFC nhưng trả 200 khi mã hóa NFD. Các link daithaoduong.kcb.vn cho 5481 và 1353 hỏng cả hai dạng.

## 6. Việc cho người dùng (HG2.3)

1. Tìm bản chính thức (kcb.vn, moh.gov.vn, Sở Y tế, bệnh viện) cho: **3312/2024**, và trước hết xác nhận văn bản này có tồn tại không (nghi nhầm với 3312/2015 trẻ em); **2892/2022** (béo phì); **1911/2021** (TSG, chỉ cần cho phân tích phiên bản). Có thể dùng trang thư viện pháp luật để tra số hiệu và ngày, nhưng không lấy tệp từ đó. Lưu vào `data/raw/manual/`.
2. Quyết định có chấp nhận nguồn **drive.google.com** (liên kết từ bvdksadec.vn) cho 1154/2024 không. Kèm theo đó: có chấp nhận các trang bệnh viện (benhviendakhoabaria.vn, bvdkbaclieu.gov.vn, benhvienquynhon.gov.vn, benhvienhatrung.vn, bvdksadec.vn) là "bệnh viện đăng lại nguyên quyết định" không. Hiện `configs/project.yaml` → `official_hosts` chỉ có kcb.vn, moh.gov.vn, vncdc.gov.vn.
3. Xác nhận hiệu lực của **3280/2011**: còn hiệu lực hay đã bị thay trên thực tế. Nếu tìm được bản ký gốc có lớp chữ thì thay tệp hiện tại, vốn có nguồn gốc từ thư viện tư nhân.
4. Xác nhận bằng mắt Điều 3 của **1470/2024** (thay 6173/2018) và của **1154/2024** (thay 1911/2021) nếu muốn có người thật ký nhận. Ảnh trang nằm ở scratchpad `c3/s1470_p1.png` và `c3/s1154_p1.png`.
5. Chọn file chuẩn cho **5904/2019**: bản quét có chữ ký hay bản toàn văn có lớp chữ.

## 7. Đề xuất sửa mã và config (không tự sửa)

- `src/vnsoc/extract/fetch_pdf.py`, hàm `text_quality`: lấy mẫu nhiều trang rải khắp tệp (ví dụ 10 trang đều nhau) thay vì chỉ 4 trang đầu, để khỏi gắn nhãn sai tệp có bìa ảnh như 2919/2014. Có thể thêm trường `pages_with_text`.
- `fetch_pdf`: khi gặp 404, thử lại với tên tệp mã hóa NFD (máy chủ kcb.vn). Thêm tùy chọn `--variant` hoặc khóa phụ cho trường hợp một văn bản có hai bản chính thức (bản quét có chữ ký và bản Word có lớp chữ), thay cho cơ chế clash tự động. Hiện nay `verify_span` không đọc được biến thể clash theo khóa.
- `src/vnsoc/extract/verify_span.py`, hàm `norm`: ánh xạ U+01A3→U+01B0 và U+01A2→U+01AF ("ƣ/Ƣ"→"ư/Ư") trước khi so khớp. Việc này cần test và cần ghi vào DECISIONS vì làm thay đổi định nghĩa "nguyên văn".
- `configs/project.yaml`: thêm danh sách host "bệnh viện/Sở Y tế đăng lại" đã được người duyệt, hoặc thêm trường `source_class` trong ManifestRow (official | repost_hospital | repost_drive).
- `ManifestRow`: cân nhắc thêm trường `partially_amends` (chiều mới → cũ) để chuỗi bãi bỏ một phần có trong cả hai dòng (2388→3931, 5904→2919, 3319→3879). Hiện chiều này chỉ ghi trong notes.

## 8. Bằng chứng trong scratchpad (không phải dữ liệu dự án)

`…/scratchpad/c3/`: `s1154_p1.png`, `s1470_p1.png`, `s1857_p1.png`, `s5904_p1.png`, `qd3319_p1.png` (ảnh trang QĐ); `qd3319_kcb.pdf` (trang QĐ 3319, sha256 ca840b6d…); `drv_1mH8…bin` (QĐ 1154 bản quét); `drv_1BWw…bin` (công văn Vụ BMTE liệt kê HD 2024); `5904_hatrung.pdf` (so sha256 bản 9e6bbe13); `than_kcb.pdf`, `tha_*.pdf` (so sha256).
