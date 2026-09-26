# c5_listing — Quét danh mục kcb.vn để bổ sung văn bản (T2.1 + T2.2)

Ngày làm: 2026-09-26 · Người làm: agent corpus-librarian (cụm c5_listing) · Manifest: `data/interim/manifest_parts/c5_listing.jsonl` (18 dòng, `vnsoc.schemas manifest` → OK).

**Tránh trùng với c4:** tôi đã xử lý 1851/2020 (hen) và 4562/2018 (COPD 2018). Cụm c4 (`c4_resp_circulars.jsonl`) cũng đã ghi hai khóa này, kèm dòng 3874/2018 với cùng phát hiện nhãn sai. Để bước ghép manifest không có khóa trùng, tôi **bỏ hai dòng này khỏi c5** và chỉ giữ thông tin ở mục 2–3 dưới đây. **Có một điểm vênh cần quyết định:** c4 để 4562/2018 `status = current`; c5 đánh giá `superseded` (bị 2767/2023 thay, nhưng đây chỉ là suy luận). Hai cụm đều ghi "hiệu lực chưa xác nhận". Xem mục 3.1.

Mọi số hiệu, ngày ký, điều khoản thay thế dưới đây đều đọc từ PDF chính thức đã tải (lớp chữ qua `vnsoc.extract.verify_span`, hoặc **đọc bằng mắt ảnh trang** khi trang quyết định là ảnh — đã ghi rõ trong `notes`). Không dùng trí nhớ. Chỗ nào chưa chắc thì ghi "chưa xác nhận".

## 1. Cách quét và giới hạn

**kcb.vn — quét hết.** Trang danh mục (`/phac-do`, `/tai-lieu/huong-dan-chan-doan-dieu-tri`, `/tin-tuc`, `/van-ban`) phân trang bằng JavaScript (CMS VHV). Thêm `?page=2` hay `?pageNo=2` vẫn trả trang 1. Vì vậy dùng API công khai mà chính trang gọi để lấy danh sách:
`https://kcb.vn/api/Content/Article/selectAll?site=2005611&options[type]=<LOẠI>&itemsPerPage=100&pageNo=<N>&orderBy=publishTime DESC`
(các lần gọi cách nhau ≥ 2 giây). Đã lấy trọn:

| Loại (options[type]) | Số mục | Bao phủ |
| --- | --- | --- |
| `Article.Download` | 171 | Gồm 52 mục chuyên mục `/phac-do` (categoryId 101796520, khớp `totalItems: 52` của trang) và 1 mục ở `/tai-lieu/huong-dan-chan-doan-dieu-tri` (101819468, là 2388/2024). Phần còn lại thuộc thư viện tài liệu / quy trình kỹ thuật. |
| `Article.News` | 1.182 | `/tin-tuc` và các bài ở `/tai-lieu/...`. PDF đính kèm nằm trong `otherFiles`. |
| `Article.LegalDocument` | 440 | `/van-ban` (có trường mã số `code`), gồm cả mục "Thư viện Hướng dẫn chẩn đoán, điều trị" (đã đọc, không có văn bản ngoài bảng mục 5). |

Bước lọc: giữ tiêu đề và tóm tắt có "hướng dẫn chẩn đoán", "chẩn đoán và điều trị", "chẩn đoán, điều trị", "chẩn đoán và xử trí", "hướng dẫn điều trị" hoặc "phác đồ"; bỏ bài hội nghị, tập huấn và quy trình kỹ thuật; gộp theo số quyết định. Kết quả là **69 văn bản**, liệt kê ở mục 5.

**Không quét được:**
- **moh.gov.vn.** Cổng hiện tại là ứng dụng một trang chạy JS. HTML trả về chỉ có khung "Cổng thông tin", không có liên kết nào; các đường dẫn `/web/guest/...` trả 404. `vbpl.moh.gov.vn` trả 503. WebFetch cũng không đọc được nội dung.
- **vncdc.gov.vn.** Chứng chỉ TLS đã hết hạn (`SEC_E_CERT_EXPIRED`), không kết nối được.
- **WebSearch.** Hạn mức của phiên đã hết (200/200) ngay từ lần gọi đầu. Vì vậy chưa tìm được văn bản nằm ngoài kcb.vn. Hệ quả nêu ở mục 6.
- Không truy cập trang thư viện pháp luật tư nhân.

**Phạm vi thực tế của kcb.vn:** phần lớn văn bản của các cụm c1–c4 **không có** trên danh mục kcb.vn. Các số sau không xuất hiện trong 1.793 mục đã tải: 2760, 3377, 292, 2855, 5968, 1154, 2892, 5481, 1353, 1622, 1840/2025, 1019/2025, 678/2025, 2131/2026. kcb.vn chỉ bao phủ một phần kho.

## 2. Văn bản đã xử lý (20 văn bản; 18 dòng trong c5_listing.jsonl, 2 dòng 1851/2020 và 4562/2018 thuộc c4)

| Khóa | Tiêu đề ngắn | Host | text_kind | Trang | Hiệu lực (status) | Ghi chú |
| --- | --- | --- | --- | --- | --- | --- |
| 2989/2026 | Suy dinh dưỡng cấp tính trẻ 0–59 tháng | kcb.vn | ok | 44 | current; thay thế 4487/2016 (tr.1 Điều 1) | **MỚI**. Ngày ký lệch giữa hai nguồn (mục 3.3). |
| 1768/2026 | Dinh dưỡng cho người bệnh ung thư | kcb.vn | ok | 86 | current | **MỚI** |
| 493/2026 | Bệnh do vi rút Nipah | kcb.vn | ok | 10 | current | **MỚI**; rất ít giá trị số |
| 1760/2024 | Đái tháo đường típ 1 trẻ em và thanh thiếu niên | kcb.vn | ok | 64 | current (ảnh QĐ: không thay thế văn bản nào) | Đối chiếu ISPAD |
| 3908/2023 | Dự phòng thuyên tắc huyết khối tĩnh mạch | kcb.vn | ok | 81 | current (ảnh QĐ: không thay thế văn bản nào) | Liều chống đông |
| 1530/2023 | Loét bàn chân do đái tháo đường | kcb.vn | ok | 43 | current | Đối chiếu IWGDF |
| 2558/2022 | Bệnh võng mạc đái tháo đường | kcb.vn | ok | 25 | current | |
| 3087/2020 | Tiền đái tháo đường | kcb.vn | ok | 19 | current | Đối chiếu ADA/WHO |
| 1851/2020 *(dòng ở c4)* | Hen phế quản người lớn và trẻ ≥ 12 tuổi | kcb.vn | ok | 48 | current; bãi bỏ 4776/2009 và 2 bài hen của 3942/2014 (tr.1 Điều 3) | Tệp đã có sẵn (exists_same); c5 kiểm độc lập, khớp với c4 |
| 1493/2015 | Hồi sức tích cực (sốc nhiễm khuẩn tr.79–93) | kcb.vn | ok | 217 | current; hiện còn hiệu lực hay không chưa xác nhận | Nguồn cho chủ đề nhiễm khuẩn huyết |
| 1494/2015 | Một số bệnh lý huyết học (thiếu máu thiếu sắt) | kcb.vn | ok | 236 | current; chưa xác nhận | |
| 315/2015 | Các bệnh sản phụ khoa (tiền sản giật, thiếu máu) | kcb.vn | ok | 285 | current; chưa xác nhận (chồng lấn 1911/2021, 1154/2024) | |
| 361/2014 | Các bệnh cơ xương khớp (loãng xương, gút) | kcb.vn | ok | 218 | current; chưa xác nhận | |
| 3879/2014 | Nội tiết – chuyển hóa (rối loạn lipid máu tr.247–264) | kcb.vn | ok | 275 | current; chưa xác nhận (chồng lấn các văn bản ĐTĐ) | |
| 4562/2018 *(dòng ở c4)* | COPD (bản 2018) | kcb.vn | ok | 86 | c5 đánh giá superseded; c4 ghi current. Thay thế 3874/2018 và 2866/2015 (tr.4). Việc 2767/2023 thay 4562/2018 là **suy luận** | kcb.vn ghi sai tiêu đề (mục 3.1); c4 phát hiện độc lập cùng lỗi |
| 4263/2015 | Lao (bản 2015) | kcb.vn | ok | 108 | superseded; thay thế 979/2009, bị 3126/2018 thay (cả hai đọc từ ảnh QĐ) | Bản cũ của chuỗi lao |
| 3126/2018 | Lao (bản 2018): chỉ có 1 trang quyết định | kcb.vn | scanned_or_empty | 1 | superseded; thay thế 4263/2015, bị 1314/2020 thay | kcb.vn ghi sai số thành 3216 (mục 3.2). Không dùng để tạo mẩu. |
| 4121/2009 | Xử trí tiêu chảy ở trẻ em | kcb.vn | legacy_font | 53 | current; chưa xác nhận | Phông TCVN3, không kiểm span được; ngoài khung 2014–2026 |
| 2187/2019 | Hội chứng mạch vành cấp | — | — | — | chưa xác nhận | **Không có PDF**: link wp-content đã chết |
| 250/2022 | COVID-19 (phiên bản 8) | — | — | — | chưa xác nhận | **Không có PDF**: tệp đính kèm trả 404 |

Tổng kết: đã xử lý **16 văn bản có lớp chữ tốt (text_kind = ok)**, dùng được cho T2.5 và T3.x: 14 văn bản chuyên đề hoặc sách hướng dẫn, cộng 2 bản cũ (4562/2018, 4263/2015) để phân tích phiên bản. Trong manifest c5 có **14 dòng text_kind = ok** (1851/2020 và 4562/2018 đã nằm ở c4). Ngoài ra có 1 bản quét 1 trang (3126/2018), 1 bản phông cũ (4121/2009) và 2 dòng không có PDF.

Liên hệ với các chủ đề ưu tiên trong đề bài:
- Nhiễm khuẩn huyết → 1493/2015.
- Hen → 1851/2020.
- Bệnh mạch vành → 2187/2019, chưa có PDF.
- Rối loạn lipid máu → 3879/2014.
- Loãng xương → 361/2014.
- Thiếu máu thai kỳ → 315/2015 và 1494/2015.
- Tiêu chảy trẻ em → 4121/2009, phông cũ.
- COVID-19 → 250/2022, chưa có PDF.
- Viêm phổi trẻ em → 3312/2015 (kcb.vn chỉ có tệp .rar; data/raw đã có `3312_2015.pdf` do agent khác tải).

## 3. Phát hiện bất thường (cần biết khi ghép manifest)

1. **kcb.vn ghi nhầm tiêu đề cho QĐ 4562/QĐ-BYT (19/7/2018).**
   - Tệp COPD "bản cập nhật 2018" được đăng dưới tên "Quyết định số 3874/QĐ-BYT ngày 26/06/2018". Tuy nhiên trang 4 của chính tệp là QĐ 4562/QĐ-BYT. Điều 3 ghi quyết định này thay thế 3874/2018 và 2866/2015.
   - Hệ quả: `data/raw/3874_2018.pdf` (do agent khác tải) **không phải QĐ 3874**. Tệp này trùng SHA-256 `68a2f132…` với `data/raw/4562_2018.pdf`. Dòng manifest của cụm nào đang dùng khóa 3874/2018 cho tệp này phải sửa.
   - Thêm một điểm lạ: 2767/2023 (tr.1, Điều 3) ghi thay thế **3874/2018**, không nhắc 4562/2018. Chuỗi COPD 2866/2015 → 3874/2018 → 4562/2018 → 2767/2023 vì vậy có một mắt xích chỉ là suy luận.
2. **kcb.vn ghi nhầm số 3126 thành 3216** (lao, 23/5/2018). Hai nguồn độc lập xác nhận số đúng là 3126: ảnh trang quyết định ("Số: 3126/QĐ-BYT"), và lớp chữ trang 1 của 1314/2020 ("thay thế Quyết định số 3126/QĐ-BYT ngày 23 tháng 5 năm 2018"). Tệp trên kcb.vn chỉ có 1 trang quyết định, không có thân hướng dẫn. Lần tải đầu, tôi dùng nhầm khóa 3216/2018, nên `data/raw/3216_2018.pdf` là **bản trùng mang khóa sai** (cùng SHA-256 `a734645a…` với `3126_2018.pdf`). Tôi không xóa được tệp này vì quy tắc cấm; người dùng cần xóa tay.
3. **2989/2026: hai nguồn lệch ngày ký.** Bài tin kcb.vn ghi "ngày 22/8/2026". Dấu ký số trên PDF ghi "2989 22 9" và "22/09/2026". Manifest dùng ngày 2026-09-22 theo dấu ký số; cần người kiểm. Cả hai ngày đều trước mốc đóng băng 15/10/2026.
4. **Nhiều tệp đính kèm trên kcb.vn đã hỏng:**
   - 250/2022 và 405/2022 trả 404.
   - 4689/2021 trả về tệp 90 byte, không phải PDF.
   - Mọi link `kcb.vn/wp-content/uploads/...` trả 302 hoặc HTML: 2187/2019, 439/2016, 2536/2020. Link 5904/2019 trong mục văn bản cũng thuộc dạng này.
5. **Tên tệp tiếng Việt phải mã hóa đúng từng byte.** Với 1851/2020, chữ "tuổi" trong tên tệp ở dạng NFD. Với 4263/2015, URL gõ lại tay trả 404. URL phải lấy nguyên byte từ HTML trang rồi percent-encode; `source_url` trong manifest là bản đã mã hóa và tải được.
6. **Trùng số giữa các năm:** mục văn bản kcb.vn ghi mã "1470/QĐ-BYT" cho "Hướng dẫn điều trị, quản lý bệnh thận mạn giai đoạn cuối trong dịch COVID-19" (đăng 03/2021). Văn bản này khác 1470/2024 (ĐTĐ thai kỳ, thuộc c1–c4). Chưa kiểm văn bản gốc. Khóa (số, năm) vẫn phân biệt được hai văn bản.
7. **Trang quyết định là ảnh** (lớp chữ chỉ có dấu ký số) ở các văn bản 3908/2023, 1760/2024, 1493/2015, 1494/2015, 4263/2015, 3126/2018 và bìa của 4562/2018. Điều khoản hiệu lực của các văn bản này đọc bằng mắt, không kiểm được bằng `verify_span`.
8. **Số hiệu trong lớp chữ bị để trống** ("Số: /QĐ-BYT") ở 2989/2026, 1768/2026, 493/2026, 1530/2023, 2558/2022, 1760/2024. Số và ngày lấy từ dấu ký số, có đối chiếu với tiêu đề bài trên kcb.vn.

## 4. Văn bản mới phát hiện (2025–2026)

- **2989/QĐ-BYT (2026)**, suy dinh dưỡng cấp tính trẻ 0–59 tháng. **Thay thế 4487/QĐ-BYT ngày 18/8/2016** (tr.1). Đã đưa vào manifest.
- **1768/QĐ-BYT (18/6/2026)**, dinh dưỡng cho người bệnh ung thư. Đã đưa vào manifest.
- **493/QĐ-BYT (13/2/2026)**, bệnh do vi rút Nipah. Đã đưa vào manifest.
- **1505/QĐ-BYT (25/5/2026)**, Ebola, cập nhật bản 2968/2014. Bài tin kcb.vn không đính kèm PDF, nên chưa ghi vào manifest. Việc nó thay 2968/2014 chưa được xác nhận.
- **2147/2026** (viêm phổi cộng đồng người lớn, thuộc c1–c4). Đề cương ghi "chưa thấy trên kcb.vn", nhưng PDF có trên kcb.vn/tin-tuc (bài 23/07/2026): https://kcb.vn/upload/2005611/20260723/Huong_dan_CD_v__DT_VPMPCD_singed_5fa4c.pdf. Tóm tắt bài tin ghi văn bản thay thế 4815/2020. data/raw đã có `2147_2026.pdf`.
- **1986/QĐ-BYT (01/7/2026)** sửa hiệu lực thi hành của một số QĐ quy trình kỹ thuật. Đây không phải hướng dẫn chẩn đoán–điều trị, chỉ ghi lại để biết.
- Trên kcb.vn **không thấy** hướng dẫn chẩn đoán–điều trị nào ban hành năm 2025.

## 5. Danh sách đầy đủ đã quét trên kcb.vn (69 văn bản, 2009–2026, xếp theo ngày đăng)

Cột "Danh mục": download = `/phac-do` và thư viện tài liệu, news = `/tin-tuc` và `/tai-lieu`, legal = `/van-ban`. Cột "Ngày" ghi rõ nguồn của ngày; ngày theo tiêu đề kcb.vn chưa được đối chiếu với văn bản.

| Số/năm | Chủ đề | Ngày (nguồn) | Danh mục | URL trang | URL tệp | Phân loại |
| --- | --- | --- | --- | --- | --- | --- |
| 2989/2026 | Suy dinh dưỡng cấp tính trẻ 0–59 tháng | 22/09/2026 (dấu ký số; tin kcb.vn ghi 22/8/2026) | news | https://kcb.vn/tin-tuc/huong-dan-chan-doan-va-dieu-tri-suy-dinh-duong-cap-tinh-o-tre-em-tu-0-den-59-thang-tuoi.html | https://kcb.vn/upload/2005611/20260924/Q__ban_hanh_TL.signed_6bdd3.pdf | **c5 – chọn, đã tải** (MỚI; thay 4487/2016) |
| 2147/2026 | Viêm phổi mắc phải cộng đồng người lớn | 15/07/2026 (tin kcb.vn) | news | https://kcb.vn/tin-tuc/huong-dan-chan-doan-va-dieu-tri-viem-phoi-mac-phai-cong-dong-o-nguoi-lon.html | https://kcb.vn/upload/2005611/20260723/Huong_dan_CD_v__DT_VPMPCD_singed_5fa4c.pdf | c1–c4 (PDF có trên kcb.vn/tin-tuc — đề cương ghi 'chưa thấy') |
| 1768/2026 | Dinh dưỡng cho người bệnh ung thư | 18/06/2026 (dấu ký số) | news | https://kcb.vn/tin-tuc/huong-dan-chan-doan-va-dieu-tri-dinh-duong-cho-nguoi-benh-ung-thu.html | https://kcb.vn/upload/2005611/20260620/uploadiframe_openFile_do_9cb35.pdf | **c5 – chọn, đã tải** (MỚI) |
| 1740/2026 | Viêm gan vi rút B | 16/06/2026 (theo đề cương; tin kcb.vn 17/06/2026) | news | https://kcb.vn/tin-tuc/quyet-dinh-1740-qd-byt-ban-hanh-tai-lieu-chuyen-mon-huong-dan-chan-doan-va-dieu-tri-viem-gan-vi-rut-b.html | https://kcb.vn/upload/2005611/20260617/BYT__QD_ban_hanh_HDCDT_viem_gan_vi_rut_B_-_final_2_signed_8c1b5.pdf | c1–c4 |
| 1505/2026 | Bệnh do vi rút Ebola (cập nhật) | 25/05/2026 (tin kcb.vn) | news | https://kcb.vn/tin-tuc/ban-hanh-huong-dan-chan-doan-va-dieu-tri-benh-do-vi-rut-ebola.html | — | không chọn: tin không đính kèm PDF; MỚI (có thể thay 2968/2014 — chưa xác nhận) |
| 493/2026 | Bệnh do vi rút Nipah | 13/02/2026 (dấu ký số) | news | https://kcb.vn/tin-tuc/ban-hanh-tai-lieu-chuyen-mon-huong-dan-chan-doan-va-dieu-tri-benh-do-vi-rut-nipah.html | https://kcb.vn/upload/2005611/20260213/QD_BH_HD_CD__signed_e07eb.pdf | **c5 – chọn, đã tải** (MỚI; ít giá trị số) |
| 2388/2024 | Bệnh thận mạn và một số bệnh lý thận | 12/08/2024 (tiêu đề kcb.vn) | download | https://kcb.vn/phac-do/quyet-dinh-so-2388-qd-byt-ngay-12-8-2024-ve-viec-ban-hanh-tai-lieu-chuyen-mon-huong-dan-chan-doan-va-dieu-tri-benh-than-.html | https://kcb.vn/upload/2005611/20240826/QD_ban_hanh_HD_chan_doan__dieu_tri_benh_than_man_va_mot_so_benh_ly_than__2024_08_12_f0584.pdf | c1–c4 |
| 1760/2024 | Đái tháo đường típ 1 trẻ em và thanh thiếu niên | 21/06/2024 (ảnh QĐ) | news | https://kcb.vn/tin-tuc/le-ky-ket-hop-tac-nang-cao-nang-luc-y-te-va-trien-khai-huong-dan-chan-doan-va-dieu-tri-benh-dai-thao-duong-tip-1-o-tre-e.html | https://kcb.vn/upload/2005611/20240625/QD__1760_signed_cf911.pdf | **c5 – chọn, đã tải** |
| 2767/2023 | COPD | 04/07/2023 (tiêu đề kcb.vn) | download | https://kcb.vn/phac-do/quyet-dinh-2767-qd-byt-cua-bo-y-te-ngay-04-07-2023-ve-viec-ban-hanh-tai-lieu-chuyen-mon-huong-dan-chan-doan-va-dieu-tri-.html | https://kcb.vn/upload/2005611/20231028/2767__QD__HD_chan_doan_va_dieu_tri_COPD_2023final_signed_e5721.pdf | c1–c4 |
| 3908/2023 | Dự phòng thuyên tắc huyết khối tĩnh mạch | 20/10/2023 (ảnh QĐ + tr.2) | download | https://kcb.vn/phac-do/quyet-dinh-3908-qd-byt-cua-bo-y-te-ngay-20-10-2023-ve-viec-ban-hanh-tai-lieu-chuyen-mon-huong-dan-dieu-tri-du-phong-thuy.html | https://kcb.vn/upload/2005611/20231028/3908__QD__ban_hanh_HD_thuyen_tac_huyet_khoi_tinh_mach_signed_12ec6.pdf | **c5 – chọn, đã tải** |
| 2558/2022 | Bệnh võng mạc đái tháo đường | 20/09/2022 (dấu ký số) | news | https://kcb.vn/tai-lieu/huong-dan-chan-doan-dieu-tri-va-quan-ly-benh-vong-mac-dai-thao-duong-quyet-dinh-2558-qd-byt-va-quyet-dinh-2557-qd-byt-ng.html | https://kcb.vn/upload/2005611/20230625/Quyet_dinh_huong_dan_benh_VMDTD15-9-2022_signed_e40c8.pdf | **c5 – chọn, đã tải** |
| 1530/2023 | Loét bàn chân do đái tháo đường | 24/03/2023 (dấu ký số) | news | https://kcb.vn/tai-lieu/huong-dan-chan-doan-dieu-tri/quyet-dinh-so-1530-qd-byt-ngay-24-3-2023-ve-viec-ban-hanh-tai-lieu-chuyen-mon-huong-dan-chan-doan-dieu-tri-loet-ban-chan.html | https://kcb.vn/upload/2005611/20230421/QD_2023_1530_Quyet_dinh_ban_hanh_tai_lieu_chuyen_mon__Huong_dan_chan_doan_va_dieu_tri_Loet_ban_chan_do_dai_thao_duong__25013.pdf | **c5 – chọn, đã tải** |
| 1531/2023 | Triệu chứng đường tiểu dưới do tăng sinh lành tính tuyến tiền liệt | 24/03/2023 (tiêu đề kcb.vn) | news | https://kcb.vn/tai-lieu/huong-dan-chan-doan-dieu-tri/quyet-dinh-ve-viec-ban-hanh-tai-lieu-chuyen-mon-huong-dan-chan-doan-va-dieu-tri-trieu-chung-duong-tieu-duoi-do-tang-sinh.html | https://kcb.vn/upload/2005611/20230421/QD_2023_1531__Quyet_dinh_ban_hanh_tai_lieu_chuyen_mon__Huong_dan_chan_doan_va_dieu_tri_trieu_chung_duong_tieu_duoi_do_tang_sinh_lanh_tinh_tuyen_tien_liet__28254.pdf | không chọn: ưu tiên thấp (ít xung đột quốc tế nổi bật) |
| 1857/2022 | Suy tim cấp và mạn | 05/07/2022 (tiêu đề kcb.vn) | download | https://kcb.vn/phac-do/quyet-dinh-1857-qd-byt-ngay-05-07-2022-ve-viec-ban-hanh-tai-lieu-chuyen-mon-huong-dan-chan-doan-va-dieu-tri-suy-tim-cap-.html | https://kcb.vn/upload/2005611/20220722/1857_Huong_dan_suy_tim_signed_8e519ed3f9.pdf | c1–c4 |
| 405/2022 | COVID-19 ở trẻ em (phiên bản 2) | 22/02/2022 (tin kcb.vn) | news | https://kcb.vn/tin-tuc/cap-nhat-huong-dan-chan-doan-va-dieu-tri-covid-19-o-tre-em-phien-ban-2-.html | https://kcb.vn/upload/2005611/20220330/qd-405_-huong-dan-dieu-tri-covid-19-tre-em-phien-ban-26b17.pdf | không tải được: PDF 404 |
| 250/2022 | COVID-19 (phiên bản 8) | 28/01/2022 (tin kcb.vn) | news | https://kcb.vn/tin-tuc/cap-nhat-huong-dan-chan-doan-va-dieu-tri-covid-19-va-quan-ly-fo-tai-nha.html | https://kcb.vn/upload/2005611/20220330/3.-huong-dan-chan-doan-va-dieu-tri-covid-phien-ban-83b0a.pdf | **c5 – ghi dòng, source_url null**: PDF 404 |
| 5155/2021 | COVID-19 ở trẻ em (bản 1) | 08/11/2021 (tin kcb.vn nêu trong bài 405) | news | https://kcb.vn/tin-tuc/ban-hanh-huong-dan-chan-doan-va-dieu-tri-covid-19-o-tre-em.html | https://kcb.vn/upload/2005611/20220207/5155-qd-byt-hu-o-ng-da-n-cha-n-doa-n-va-die-u-tri-covid-19-o-tre-emda98.pdf | không chọn: đã bị 405/2022 thay (theo tin kcb.vn) |
| 4689/2021 | COVID-19 (phiên bản 7) | 06/10/2021 (tiêu đề tin) | news | https://kcb.vn/tin-tuc/quyet-dinh-so-4689-qd-byt-ngay-06-10-2021-huong-dan-chan-doan-va-dieu-tri-covid-19-cap-nhat-lan-thu-7-.html | https://kcb.vn/upload/2005611/20220207/qd-4689_qd_byt_-huong-dan-chan-doan-va-dieu-tri-covid-19-phien-ban-so-7-1ccf3.pdf | không tải được: link trả tệp 90 byte |
| 3429/2021 | Nhiễm nấm xâm lấn | 14/07/2021 (tiêu đề kcb.vn) | download/legal | https://kcb.vn/phac-do/quyet-dinh-so-3429-qd-byt-ngay-14-7-2021-ve-viec-ban-hanh-tai-lieu-chuyen-mon-huong-dan-chan-doan-va-dieu-tri-nhiem-nam-.html | — | không chọn: kcb.vn không đính kèm tệp |
| 1966/2021 | Giảm tiểu cầu, huyết khối sau tiêm vắc xin COVID-19 | (không rõ trên tiêu đề) | news | https://kcb.vn/tin-tuc/huong-dan-chan-doan-dieu-tri-hoi-chung-giam-tieu-cau-huyet-k.html | https://kcb.vn/upload/2005611/20220207/huong-dan-chan-doan-dieu-tri-theo-tuyen-tong-hop-ban-hanh_1.signedf9f3.pdf | không chọn: chủ đề hẹp |
| 1470/2021? | Thận mạn giai đoạn cuối trong dịch COVID-19 (mục văn bản kcb.vn ghi mã 1470/QĐ-BYT; chưa kiểm văn bản) | (bài đăng 08/03/2021; ngày ký chưa rõ) | download/legal | https://kcb.vn/phac-do/quyet-dinh-ve-viec-ban-hanh-tai-lieu-chuyen-mon-huong-dan-di.html | https://kcb.vn/upload/2005611/20210723//QD-ban-hanh-HD-benh-than-giai-doan-cuoi-final.signed.pdf | không chọn: chủ đề COVID tạm thời; LƯU Ý khóa 1470/2021 ≠ 1470/2024 |
| 3875? | Ngộ độc botulinum (hướng dẫn tạm thời) | (tên tệp gợi ý QĐ 3875/2020 — chưa xác nhận) | news | https://kcb.vn/tin-tuc/huong-dan-tam-thoi-chan-doan-va-dieu-tri-ngo-doc-botulinum.html | https://kcb.vn/upload/2005611/20210722/55d104e7bf8069120b40e217bd52a639q-b-3875-1.pdf | không chọn: chủ đề hẹp |
| 3129/2020 | Ung thư biểu mô tế bào gan | 17/07/2020 | download/legal | https://kcb.vn/phac-do/quyet-dinh-so-3129-qd-byt-ngay-17-thang-07-nam-2020-ve-viec-.html | https://kcb.vn/upload/2005611/20210723//3129_QD-BYT_Huong-dan-chan-doan-va-dieu-tri-ung-thu-bieu-mo-te-bao-gan.pdf | không chọn: ung thư (ưu tiên thấp cho kho đối chiếu) |
| 3130/2020 | Ung thư tuyến tiền liệt | 17/07/2020 | download/legal | https://kcb.vn/phac-do/quyet-dinh-so-3130-qd-byt-ngay-17-thang-07-nam-2020-ve-viec-.html | https://kcb.vn/upload/2005611/20210723//3130_QD-BYT_Huong-dan-chan-doan-va-dieu-tri-UT-tuyen-tien-liẹt.pdf | không chọn: ung thư |
| 3128/2020 | Ung thư vú | 17/07/2020 | download/legal | https://kcb.vn/phac-do/quyet-dinh-so-3128-qd_byt-ngay-17-thang-07-nam-2020-ve-viec-.html | https://kcb.vn/upload/2005611/20210723//3128_QD-BYT_Huong-dan-chan-doan-va-dieu-tri-ung-thu-vu.pdf | không chọn: ung thư |
| 3127/2020 | Ung thư dạ dày | 17/07/2020 | download/legal | https://kcb.vn/phac-do/quyet-dinh-so-3127-qd-byt-ngay-17-thang-07-nam-2020-ve-viec-.html | https://kcb.vn/upload/2005611/20210723//3127_QD-BYT_Huong-dan-chan-doan-va-dieu-tri-ung-thu-DD-1.pdf | không chọn: ung thư |
| 3087/2020 | Tiền đái tháo đường | 16/07/2020 (lớp chữ tr.1) | download/legal | https://kcb.vn/phac-do/quyet-dinh-so-3087-qd-byt-ngay-16-thang-7-nam-2020-ve-viec-b.html | https://kcb.vn/upload/2005611/20210723//3087_QD-BYT_Huong-dan-chan-doan-va-dieu-tri-tien-dai-thao-duong-1.pdf | **c5 – chọn, đã tải** |
| 2536/2020 | Ngôn ngữ trị liệu (đột quỵ, chấn thương sọ não…) | 16/06/2020 | news | https://kcb.vn/kham-chua-benh/phuc-hoi-chuc-nang/ban-hanh-huong-dan-chan-doan-dieu-tri-phu-c-ho-i-chu-c-nang-.html | https://kcb.vn/wp-content/uploads/2020/06/2536_QD-BYT_16062020_8-ban-hành-bộ-tài-liệu-ST.pdf | không chọn: phục hồi chức năng |
| 1514/2020 | Một số bệnh ung bướu | 01/04/2020 | download/legal | https://kcb.vn/phac-do/quyet-dinh-so-1514-qd-byt-ngay-01-thang-04-nam-2020-cua-bo-t.html | — | không chọn: kcb.vn không đính kèm tệp |
| 2058/2020 | Một số rối loạn tâm thần | 14/05/2020 | download/legal | https://kcb.vn/phac-do/quyet-dinh-so-2058-qd-byt-ngay-14-thang-5-nam-2020-ve-viec-v.html | — | không chọn: kcb.vn không đính kèm tệp |
| 1886/2020 | Bệnh không lây nhiễm trong dịch COVID-19 | 27/04/2020 | download/legal | https://kcb.vn/phac-do/quyet-dinh-so-1886-qd-byt-ngay-27-4-2020-ve-viec-ban-hanh-ta.html | https://kcb.vn/upload/2005611/20210723//1886_QD-BYT_Huong-dan-dieu-tri-quan-ly-BKLN-trong-dich-COVID19.pdf | không chọn: hướng dẫn tạm thời thời COVID |
| 1762/2020 | Suy tim mạn tính | 17/04/2020 | download/legal | https://kcb.vn/phac-do/quyet-dinh-so-1762-qd-byt-ngay-17-thang-4-nam-2020-cua-bo-y-.html | https://kcb.vn/upload/2005611/20210723//QD-1762-Ban-hành-Hướng-dẫn-chẩn-đoán-và-điều-trị-suy-tim-mạn-tính.pdf | c1–c4 |
| 1851/2020 | Hen phế quản người lớn và trẻ ≥ 12 tuổi | 24/04/2020 (ảnh + tr.2) | download/legal | https://kcb.vn/phac-do/quyet-dinh-so-1851-qd-byt-ngay-24-thang-4-nam-2020-cua-bo-y-.html | https://kcb.vn/upload/2005611/20210723//Hướng-dẫn-chẩn-đoán-và-điều-trị-Hen-phế-quản-người-lớn-và-trẻ-_12-tuổi.pdf (mã hóa byte NFD: xem manifest) | c4 đã ghi dòng (c5 kiểm lại, khớp; bỏ khỏi c5 để tránh trùng) |
| 1344/2020 | COVID-19 (phiên bản 3) | (tin kcb.vn 26/03/2020) | news | https://kcb.vn/tin-tuc/huong-dan-chan-doan-va-dieu-tri-viem-duong-ho-hap-cap-do-sar.html | https://kcb.vn/upload/2005611/20210722/8ca3a165ba66d52a55e4681703ee179dqdb-2020-1344-1.pdf | không chọn: phiên bản cũ |
| 5904/2019 | Bệnh không lây nhiễm tại trạm y tế xã | 20/12/2019 | legal | https://kcb.vn/van-ban/quyet-dinh-so-5904-qd-byt-ngay-20-12-2019-ve-viec-ban-hanh-tai-lieu-chuyen-mon-huong-dan-chan-doan-dieu-tri-va-quan-ly-m.html | https://kcb.vn/wp-content/uploads/2020/01/HD-chẩn-đoán-điều-trị-quản-lý-BKLN-tai-xa.-Final.-2019.12.30.Approved.pdf | c1–c4 |
| 2187/2019 | Hội chứng mạch vành cấp | 03/06/2019 (tiêu đề kcb.vn) | download/legal | https://kcb.vn/phac-do/quyet-dinh-2187-qd-byt-ngay-03-6-2019-cua-bo-truong-bo-y-te-.html | http://kcb.vn/wp-content/uploads/2019/06/Quyết-định-2187-QĐ-BYT-Hướng-dẫn-chẩn-đoán-và-xử-trí-hội-chứng-mạch-vành-cấp.pdf | **c5 – ghi dòng, source_url null**: link wp-content chết |
| 3874/2018 | COPD — TIÊU ĐỀ SAI: tệp thực chất là QĐ 4562/QĐ-BYT 19/7/2018 | 26/06/2018 (tiêu đề kcb.vn) | download/legal | https://kcb.vn/phac-do/quyet-dinh-so-3874-qd-byt-ngay-26-06-2018-ban-hanh-tai-lieu-.html | https://kcb.vn/upload/2005611/20210723//Bộ-Y-tế-Hướng-dẫn-chẩn-đoán-và-điều-trị-BPTNMT-bản-cập-nhật-2018.pdf | c4 đã ghi dòng 4562/2018 và 3874/2018 (c5 phát hiện độc lập cùng lỗi; vênh status, xem mục 3.1) |
| 3216/2018 | Lao — TIÊU ĐỀ SAI: số đúng 3126/QĐ-BYT (ảnh QĐ + 1314/2020) | 23/05/2018 | download/legal | https://kcb.vn/phac-do/quyet-dinh-so-3216-qd-byt-ngay-23-5-2018-ve-viec-ban-hanh-hu.html | https://kcb.vn/upload/2005611/20210723//111.pdf | **c5 – ghi dòng 3126/2018** (chỉ 1 trang quét) |
| TT51/2017 | Phản vệ (Thông tư 51/2017/TT-BYT) | 29/12/2017 | legal | https://kcb.vn/van-ban/thong-tu-so-51-2017-tt-byt-ngay-29-12-2017-huong-dan-phong-chan-doan-va-xu-tri-phan-ve.html | https://kcb.vn/upload/2005611/20210723/fda42ab303f0f256316b69ff98643f48tt-2017-51-1.pdf | c1–c4 (TT51/2017) |
| 3319/2017 | Đái tháo đường típ 2 | 19/07/2017 | download/legal | https://kcb.vn/phac-do/quyet-dinh-so-3319-qd-byt-ngay-19-7-2017-ve-viec-ban-hanh-ta.html | https://kcb.vn/upload/2005611/20210723//QĐ-ban-hành-HD-Điều-trị-ĐTĐ-típ-2.pdf | c1–c4 |
| 439/2016 | Bệnh do vi rút Zika | 05/02/2016 | legal | https://kcb.vn/van-ban/quyet-dinh-so-439-qd-byt-ngay-5-02-2016-cua-bo-y-te-ban-hanh-huong-dan-chan-doan-va-dieu-tri-benh-do-vi-rut-zika.html | https://kcb.vn/wp-content/uploads/2016/04/Phác-đồ-chẩn-đoán-và-điều-trị-bệnh-do-vi-rút-Zika.pdf | không chọn: link wp-content chết (302) |
| 5642/2015 | Một số bệnh truyền nhiễm | 31/12/2015 | download/legal | https://kcb.vn/phac-do/quyet-dinh-so-5642-qd-byt-ngay-31-12-2015-ve-viec-ban-hanh-t.html | https://kcb.vn/upload/2005611/20210723//Truyen-nhiem-1.pdf | c1–c4 |
| 5643/2015 | Một số bệnh tai mũi họng | 31/12/2015 (mục văn bản) | download/legal | https://kcb.vn/phac-do/huong-dan-chan-doan-va-dieu-tri-mot-so-benh-ve-tai-mui-hong.html | https://kcb.vn/upload/2005611/20210723//HDĐT-TMH.pdf | không chọn: ưu tiên thấp |
| 4263/2015 | Chẩn đoán, điều trị và dự phòng bệnh lao (bản 2015) | 13/10/2015 (tr.1 + ảnh QĐ tr.2) | download/legal | https://kcb.vn/phac-do/huong-dan-chan-doan-va-dieu-tri-du-phong-benh-lao.html | https://kcb.vn/upload/2005611/20210723//Huong-dan-chan-doan-dieu-tri-du-phong-benh-lao-ban-h%C3%A0nh-k%C3%A8m-Q-.pdf | **c5 – chọn, đã tải** (bản cũ chuỗi lao; URL phải lấy đúng byte từ HTML) |
| 3931/2015 | Các bệnh thận – tiết niệu | 21/09/2015 (mục văn bản) | download/legal | https://kcb.vn/phac-do/huong-dan-chan-doan-va-dieu-tri-cac-benh-than-tiet-nieu.html | https://kcb.vn/upload/2005611/20210723//Hướng-dẫn-chẩn-đoán-và-điều-trị-các-bệnh-Thận-Tiết-niệu.pdf | c1–c4 |
| 3610/2015 | Chẩn đoán và xử trí ngộ độc | 31/08/2015 | download/legal | https://kcb.vn/phac-do/huong-dan-chan-doan-va-xu-tri-ngo-doc.html | https://kcb.vn/upload/2005611/20210723//Huong-dan-chan-doan-va-xu-tri-Ngo-doc.pdf | c1–c4 |
| 3312/2015 | Một số bệnh thường gặp ở trẻ em (viêm phổi trẻ em…) | 07/08/2015 (mục văn bản) | download/legal | https://kcb.vn/phac-do/huong-dan-chan-doan-va-dieu-tri-mot-so-benh-thuong-gap-o-tre.html | https://kcb.vn/upload/2005611/20210723//Tre-em.rar | không chọn: kcb.vn chỉ có .rar (tệp 3312_2015.pdf đã có trong data/raw do agent khác) — nguồn cho viêm phổi/tiêu chảy trẻ em |
| 3108/2015 | Một số bệnh răng hàm mặt | 28/07/2015 | download/legal | https://kcb.vn/phac-do/huong-dan-chan-doan-va-dieu-tri-mot-so-benh-ve-rang-ham-mat.html | https://kcb.vn/upload/2005611/20210723//Bản-cuối-20150728-HD-CĐĐT-RHM.pdf | không chọn: ưu tiên thấp |
| 1494/2015 | Một số bệnh lý huyết học | 22/04/2015 (ảnh QĐ + tr.1) | download/legal | https://kcb.vn/thu-vien-tai-lieu/huong-dan-chan-doan-va-dieu-tri-mot-so-benh-ly-huyet-hoc.html | https://kcb.vn/upload/2005611/20210723//Hướng-dẫn-chẩn-đoán-và-điều-trị-một-số-bệnh-lý-Huyết-học.pdf | **c5 – chọn, đã tải** |
| 1493/2015 | Hồi sức tích cực (sốc nhiễm khuẩn…) | 22/04/2015 (ảnh QĐ + tr.1) | download/legal | https://kcb.vn/thu-vien-tai-lieu/huong-dan-chan-doan-va-xu-tri-hoi-suc-tich-cuc.html | https://kcb.vn/upload/2005611/20210723//Hướng-dẫn-chẩn-đoán-điều-trị-hồi-sức-tích-cực.pdf | **c5 – chọn, đã tải** |
| 315/2015 | Các bệnh sản phụ khoa | 29/01/2015 (lớp chữ tr.2) | download/legal | https://kcb.vn/thu-vien-tai-lieu/huong-dan-chan-doan-va-dieu-tri-cac-benh-san-phu-khoa.html | https://kcb.vn/upload/2005611/20210723//Hướng-dẫn-chẩn-đoán-và-điều-trị-Sản-phụ-khoa.pdf | **c5 – chọn, đã tải** |
| 75/2015 | Các bệnh da liễu | 13/01/2015 (mục văn bản) | download/legal | https://kcb.vn/phac-do/huong-dan-chan-doan-va-dieu-tri-cac-benh-da-lieu.html | https://kcb.vn/upload/2005611/20210723//Huong-dan-chan-doan-dieu-tri-Da-lieu.pdf | không chọn: ưu tiên thấp |
| 40/2015 | Các bệnh về mắt | 12/01/2015 (mục văn bản) | download/legal | https://kcb.vn/phac-do/huong-dan-chan-doan-va-dieu-tri-cac-benh-ve-mat.html | https://kcb.vn/upload/2005611/20210723//mat.rar | không chọn: tệp .rar |
| 5447/2014 | Viêm gan vi rút A | (mục văn bản ghi 19/06/2015 — ngày đăng?) | download/legal | https://kcb.vn/thu-vien-tai-lieu/huong-dan-chan-doan-dieu-tri-benh-viem-gan-vi-rut-a.html | https://kcb.vn/upload/2005611/20210723//Hướng-dẫn-chẩn-đoán-và-điều-trị-bệnh-viêm-gan-vi-rút-A.pdf | không chọn: ít giá trị số |
| 5448/2014 | Viêm gan vi rút B (bản 2014) | 30/12/2014 (mục văn bản) | download/legal | https://kcb.vn/thu-vien-tai-lieu/huong-dan-chan-doan-dieu-tri-benh-viem-gan-vi-rut-b.html | https://kcb.vn/upload/2005611/20210723//Hướng-dẫn-chẩn-đoán-và-điều-trị-bệnh-viêm-gan-vi-rút-B.pdf | không chọn (tệp 5448_2014.pdf đã có trong data/raw do agent khác; bản cũ chuỗi VGB) |
| 5449/2014 | Viêm gan vi rút D | 30/12/2014 | download/legal | https://kcb.vn/thu-vien-tai-lieu/huong-dan-chan-doan-dieu-tri-benh-viem-gan-vi-rut-d.html | https://kcb.vn/upload/2005611/20210723//Hướng-dẫn-chẩn-đoán-và-điều-trị-bệnh-viêm-gan-vi-rút-D.pdf | không chọn: ít giá trị số |
| 5450/2014 | Viêm gan vi rút E | 30/12/2014 | download/legal | https://kcb.vn/thu-vien-tai-lieu/huong-dan-chan-doan-dieu-tri-benh-viem-gan-vi-rut-e.html | https://kcb.vn/upload/2005611/20210723//Hướng-dẫn-chẩn-đoán-và-điều-trị-bệnh-viêm-gan-vi-rút-E.pdf | không chọn: ít giá trị số |
| 5204/2014 | Chẩn đoán và điều trị bằng y học hạt nhân | 18/12/2014 | download/legal | https://kcb.vn/thu-vien-tai-lieu/huong-dan-chan-doan-va-dieu-tri-benh-bang-y-hoc-hat-nhan.html | https://kcb.vn/upload/2005611/20210723//Hướng-dẫn-chẩn-đoán-và-điều-trị-YHHN.pdf | không chọn: ưu tiên thấp |
| 5152/2014 | Rắn lục xanh đuôi đỏ cắn | 12/12/2014 | download/legal | https://kcb.vn/thu-vien-tai-lieu/chan-doan-va-dieu-tri-ran-luc-xanh-duoi-do-can.html | https://kcb.vn/upload/2005611/20210723//Hướng-dẫn-chẩn-đoán-và-điều-trị-Rắn-lục-xanh-đuôi-đỏ.pdf | không chọn: chủ đề hẹp (rắn cắn đã có trong 3610/2015) |
| 3942/2014 | Dị ứng – miễn dịch lâm sàng | 02/10/2014 | download/legal | https://kcb.vn/phac-do/huong-dan-chan-doan-va-dieu-tri-cac-benh-ve-di-ung-mien-dich.html | https://kcb.vn/upload/2005611/20210723//Mien-dich.rar | không chọn: tệp .rar (tệp 3942_2014.pdf đã có trong data/raw do agent khác); 2 bài hen bị 1851/2020 bãi bỏ |
| 3879/2014 | Nội tiết – chuyển hóa (lipid máu…) | 30/09/2014 (lớp chữ tr.3) | download/legal | https://kcb.vn/thu-vien-tai-lieu/huong-dan-chan-doan-va-dieu-tri-benh-noi-tiet-chuyen-hoa.html | https://kcb.vn/upload/2005611/20210723//Chẩn-đoán-và-điều-trị-bệnh-Nội-tiết-chuyển-hóa.pdf | **c5 – chọn, đã tải** |
| 3014/2014 | MERS-CoV | 13/08/2014 (mục văn bản) | download/legal | https://kcb.vn/thu-vien-tai-lieu/huong-dan-chan-doan-va-dieu-tri-hoi-chung-viem-duong-ho-hap-.html | https://kcb.vn/upload/2005611/20210723//Huong-dan-Mers-CoV-trinh-ban-hanh.pdf | không chọn: ưu tiên thấp |
| 2968/2014 | Bệnh do vi rút Ebola (bản 2014) | 08/08/2014 | download/legal | https://kcb.vn/thu-vien-tai-lieu/huong-dan-chan-doan-va-dieu-tri-benh-do-vi-rut-ebola.html | https://kcb.vn/upload/2005611/20210723//Hướng-dẫn-chẩn-đoán-và-điều-trị-Ebola.pdf | không chọn: ưu tiên thấp |
| 361/2014 | Các bệnh cơ xương khớp (loãng xương, gút…) | 25/01/2014 (lớp chữ tr.3) | download/legal | https://kcb.vn/phac-do/huong-dan-chan-doan-va-dieu-tri-cac-benh-co-xuong-khop.html | https://kcb.vn/upload/2005611/20210723//HDĐT-Cơ-Xương-Khớp.pdf | **c5 – chọn, đã tải** |
| 4235/2012 | Bệnh hô hấp | 31/10/2012 (mục văn bản) | download/legal | https://kcb.vn/phac-do/huong-dan-chan-doan-va-dieu-tri-benh-ho-hap.html | https://kcb.vn/upload/2005611/20210723//PDF-HO-HAP.rar | không chọn: ngoài khung 2014–2026; tệp .rar |
| 1454/2012 | Viêm da dày sừng bàn tay, bàn chân | 04/05/2012 | download/legal | https://kcb.vn/phac-do/huong-dan-chan-doan-va-dieu-tri-hoi-chung-viem-da-day-sung-b.html | https://kcb.vn/upload/2005611/20210723//huongdanchandoan-dieu-tri-viem-da-day-sung.pdf | không chọn: ngoài khung |
| 3280/2011 | Đái tháo đường típ 2 (bản 2011) | 09/09/2011 | download/legal | https://kcb.vn/phac-do/h-uong-dan-chan-doan-va-dieu-tri-dai-thao-duong-type-2.html | https://kcb.vn/upload/2005611/20210723//3280_Q-BYT.pdf | không chọn: ngoài khung (bản cũ của chuỗi ĐTĐ) |
| 3192/2010 | Tăng huyết áp | 31/08/2010 | download/legal | https://kcb.vn/phac-do/huong-dan-chan-doan-va-dieu-tri-tang-huyet-ap.html | https://kcb.vn/upload/2005611/20210723//huong_dan_chan_doan_dieu_tri_tha.pdf | c1–c4 |
| 4121/2009 | Xử trí tiêu chảy ở trẻ em | 28/10/2009 (tr.1, phông TCVN3) | download/legal | https://kcb.vn/thu-vien-tai-lieu/tai-lieu-huong-dan-xu-tri-tieu-chay-o-tre-em.html | https://kcb.vn/upload/2005611/20210723//Hướng-dẫn-xử-trí-tiêu-chảy-ở-trẻ-em.pdf | **c5 – chọn, đã tải** (legacy_font, ngoài khung) |

URL tệp có dấu tiếng Việt ở bảng trên là dạng hiển thị. Khi tải, phải lấy đúng byte từ HTML trang rồi percent-encode (mục 3.5). URL đã tải thành công nằm trong `source_url` của manifest.

## 6. Không tìm được và nơi đã tìm

| Văn bản / chủ đề | Nơi đã tìm | Kết quả |
| --- | --- | --- |
| 2187/2019 hội chứng mạch vành cấp | kcb.vn/phac-do, /van-ban, thư viện | Chỉ có link wp-content, trả HTML (5.849 byte). moh.gov.vn không quét được. |
| 250/2022 COVID-19 phiên bản 8, 405/2022 COVID trẻ em | kcb.vn/tin-tuc | Tệp đính kèm trả 404. 4689/2021 trả tệp 90 byte. **Chưa rõ phiên bản COVID-19 cuối cùng**; có thể có bản sau 2022 nhưng chưa tìm được do WebSearch hết hạn mức và moh.gov.vn không đọc được. |
| 1505/2026 Ebola | kcb.vn/tin-tuc | Bài tin không đính kèm PDF. |
| Thân hướng dẫn lao 3126/2018 | kcb.vn (tệp 111.pdf, link wp-content) | Chỉ có 1 trang quyết định; link wp-content trả 302. |
| QĐ 3874/2018 (bản thật) | kcb.vn | Không có; tệp mang tên 3874 thực chất là 4562/2018. |
| 439/2016 Zika, 3429/2021 nấm xâm lấn, 1514/2020 ung bướu, 2058/2020 tâm thần | kcb.vn | Link chết hoặc không đính kèm tệp. |
| **Chủ đề ưu tiên chưa có văn bản riêng trên kcb.vn:** sốt mò, nhiễm khuẩn huyết, viêm màng não (có thể nằm trong 5642/2015, thuộc c1–c4), bạch hầu (chỉ có công văn 07/2024 gửi Nghệ An, Bắc Giang), ho gà, đậu mùa khỉ (chỉ có tài liệu tập huấn .pptx 08/2022), cúm (1840/2025 thuộc c1–c4, không có trên kcb.vn), rung nhĩ, bệnh mạch vành mạn, thiếu máu thai kỳ (chỉ có dưới dạng bài trong 315/2015) | kcb.vn: toàn bộ 1.793 mục | Không thấy quyết định riêng. Chưa tìm được trên moh.gov.vn hay vncdc.gov.vn (xem mục 1). |

## 7. Việc cho người dùng (HG2.3)

1. **Tìm PDF chính thức** cho các văn bản sau (từ moh.gov.vn qua trình duyệt, Sở Y tế hoặc bệnh viện đăng lại nguyên quyết định):
   - 2187/QĐ-BYT (03/6/2019), hội chứng mạch vành cấp;
   - 250/QĐ-BYT (28/01/2022), COVID-19 phiên bản 8, và xác định có bản COVID-19 nào **mới hơn** hay không;
   - 405/QĐ-BYT (22/02/2022), COVID-19 trẻ em;
   - 1505/QĐ-BYT (2026), Ebola;
   - thân hướng dẫn lao 3126/QĐ-BYT (23/5/2018);
   - các hướng dẫn riêng về bạch hầu, ho gà, đậu mùa khỉ, sốt mò, nhiễm khuẩn huyết, viêm màng não, rung nhĩ (nếu có).
2. **Kiểm ngày ký của 2989/2026:** 22/8/2026 theo tin kcb.vn hay 22/9/2026 theo dấu ký số trên PDF. Ngày nào cũng trước mốc đóng băng.
3. **Xóa tay `data/raw/3216_2018.pdf`.** Đây là bản trùng mang khóa sai của 3126/2018, cùng SHA-256 `a734645a…`. Agent không được xóa trong data/raw.
4. **Quyết định cách xử lý `data/raw/3874_2018.pdf`.** Nội dung tệp là QĐ 4562/2018. Dòng 3874/2018 trong c4 đã đặt `source_url = null` và cảnh báo đúng; chỉ còn tệp mang khóa sai trong data/raw cần xóa hoặc đổi tên tay.
5. **Xác nhận chuỗi COPD và thống nhất status của 4562/2018** (c4 ghi `current`, c5 đánh giá `superseded`): 2767/2023 có thay 4562/2018 hay không? Văn bản 2767/2023 chỉ nêu 3874/2018.
6. **Kiểm bằng mắt các điều khoản đọc từ ảnh trang:** 4263/2015 thay 979/2009; 3126/2018 thay 4263/2015; 3908/2023, 1760/2024, 1493/2015, 1494/2015 không thay thế văn bản nào.

## 8. Đề xuất sửa mã / cấu hình (không tự sửa)

- Thêm vào `vnsoc.extract` bộ chuyển mã **TCVN3/ABC → Unicode** cho PDF có `text_kind = legacy_font` (ví dụ 4121/2009). Cách này rẻ hơn OCR và giữ được số liệu.
- `fetch_pdf`: thêm tùy chọn `--page-url`. Tùy chọn này tự lấy link PDF với đúng byte từ HTML trang kcb.vn, tránh 404 do NFC/NFD. Nên cảnh báo khi status = `downloaded` mà cùng SHA-256 đã có dưới một khóa khác (trường hợp 3216/3126 và 3874/4562).
- Thêm script chụp danh mục kcb.vn qua API (`/api/Content/Article/selectAll`, ba loại Download, News, LegalDocument) và lưu `data/interim/kcb_listing_<ngày>.json` để tái lập. Lần quét này chỉ lưu trong scratchpad của agent.
- `verify_span`: đánh dấu các trang không có lớp chữ nhưng có ảnh, như trang quyết định dạng ảnh, để T2.4 biết điều khoản hiệu lực ở đó cần kiểm tay hoặc OCR.
