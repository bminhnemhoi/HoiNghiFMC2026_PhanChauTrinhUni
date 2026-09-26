# Kiểm tra chuỗi thay thế và đề xuất kho chính — task C2.5 (27/9/2026)

Người làm: Claude (agent corpus-librarian), thay việc tìm tay HG2.3 theo ủy quyền của người dùng ngày 26/9/2026 (docs/DECISIONS.md 2026-09-26T20:40). **Đây là kiểm tra của AI, chưa có người kiểm.** Kế hoạch T2.5 yêu cầu agent integrity-auditor kiểm lại độc lập toàn bộ chuỗi; việc đó chưa làm.

Tệp liên quan: `data/interim/manifest_parts/c6_main_corpus.jsonl` (85 dòng, một dòng cho mọi văn bản trong danh mục, kèm lý do in_corpus), `data/interim/manifest.jsonl` (sau ghép), `results/tables/supersession.csv` (85 dòng: quan hệ, bằng chứng ≤ 150 ký tự, verified), `results/tables/corpus_triage.csv`, `state/gates/HG2.3_missing.md`.

## 1. Tóm tắt

| Chỉ số | Trước C2.5 | Sau C2.5 |
| --- | --- | --- |
| Văn bản trong danh mục | 75 | 85 |
| Văn bản hiện hành | 51 (một số sai) | 54 |
| Có PDF chính thức | 59 | 82 |
| Chưa có PDF chính thức | 16 | 3 (1003/2012, 1622/2014, 3874/2018) |
| Đề xuất in_corpus | 0 | **35** (tầng 1: 16, tầng 2: 8, tầng 3: 11); **5 văn bản OCR** trong kho |
| Văn bản OCR dùng tổng cộng (trần 10) | — | **8** = 5 trong kho + 3 bản cũ (1327/2014, 3310/2019, 3705/2019) |

- **7 văn bản "chưa xác minh" đều có thật** và đã có PDF: 1019/2025 (sởi), 1840/2025 (cúm mùa), 2855/2024 và 2065/2021 (viêm gan C), 678/2025 (dự phòng lây truyền mẹ–con), 3312/2024 (đột quỵ), 2892/2022 (béo phì).
- **Phát hiện thay đổi hiệu lực** (đọc từ điều khoản trong văn bản): 1327/2014 → bị 1019/2025 thay; 2078/2011 → bị 1840/2025 thay; 5331/2020 → bị 3312/2024 thay; **1494/2015 (huyết học, trước đây nằm trong 35 văn bản đầu) → bị 1832/2022 thay**; 250/2022 → bị 2671/2023 thay; 3879/2014 → chỉ còn hiệu lực một phần (bài béo phì bị 2892/2022 bãi bỏ; phần ĐTĐ típ 2 bị 3319/2017 bãi bỏ).
- **Không thấy văn bản mới hơn** cho các bệnh khác đến 27/9/2026 (kcb.vn, danh mục BV Bạc Liêu 2023–2026, thư viện Sở Y tế Gia Lai, WebSearch). Văn bản 2025–2026 mới thêm: 3510/2025 (thần kinh ĐTĐ), 2323/2025 (sơ sinh). Không có văn bản nào ban hành sau 15/10/2026 (DR7 chưa phát sinh).

## 2. Nguồn đã quét và cách làm

1. **kcb.vn**: agent c5 đã lấy trọn danh mục qua API công khai ngày 26/9 (1.793 mục); hôm nay tôi gọi lại API (3 loại, 15 mục mới nhất): bài mới nhất về hướng dẫn chẩn đoán–điều trị vẫn là 2989/2026 (24/9).
2. **Bệnh viện Đa khoa Bạc Liêu** (bvdkbaclieu.gov.vn, cùng CMS với kcb.vn): lấy trọn mục "Văn bản pháp quy" qua API `api/Content/Article/selectAll` (1.204 văn bản, 2/2023–9/2026, cách nhau ≥ 2 giây); lọc văn bản BYT có "chẩn đoán/điều trị/xử trí/tiêm chủng/sàng lọc" và theo tên bệnh.
3. **Thư viện "Hướng dẫn chẩn đoán điều trị…" của Sở Y tế Gia Lai** (syt.gialai.gov.vn; kế thừa thư viện Sở Y tế Bình Định sau sáp nhập tỉnh — syt.binhdinh.gov.vn nay lỗi TLS): 148 mục (8 trang danh sách). Tệp chỉ tải được trong phiên của trang mục (NukeViet `nv_download_file`); tôi dùng một script trong scratchpad theo đúng nguyên tắc của `fetch_pdf` (TLS kiểm bình thường, kiểm `%PDF`, SHA-256, không ghi đè data/raw).
4. **WebSearch** (không mở trang luật tư nhân; chỉ mở trang Sở Y tế/bệnh viện/cơ quan nhà nước) cho từng văn bản thiếu và cho "văn bản mới hơn" của từng bệnh (THA, HIV, lao, dengue, ĐTĐ típ 2, hen, dại, HCMV cấp, TCM, các sách 2014–2015).
5. **Soát nguồn gốc**: mọi tệp mới được soát metadata và nội dung tìm dấu trang luật tư nhân ("LawSoft", "LuatVietnam", tên miền). Một tệp bị loại: .doc của 1003/2012 trên thư viện Gia Lai (metadata title "THƯ VIỆN PHÁP LUẬT", author "LawSoft") — xem §7.
6. **Trang lỗi TLS không vượt qua** (không tắt kiểm chứng chỉ): vncdc.gov.vn, vaac.gov.vn, emohbackup.moh.gov.vn (Hệ thống tra cứu văn bản Bộ Y tế — chứng chỉ hết hạn), syt.binhdinh.gov.vn; bvcdn.org.vn (BV C Đà Nẵng) đóng kết nối.

## 3. Văn bản tìm được trong C2.5 (đã lưu data/raw, sha256 trong manifest)

| Khóa | Nội dung | Nguồn (host) | Lớp chữ | Trang | Ghi chú |
| --- | --- | --- | --- | --- | --- |
| 1019/2025 | Sởi | t5g.org.vn (TT Truyền thông GDSK TƯ – BYT) | có (tr.1 ảnh) | 21 | trùng sha256 bản BVĐK Quảng Ninh |
| 1840/2025 | Cúm mùa | bvdkbaclieu.gov.vn | có | 12 | tr.4 ghi nhầm "ban biên soạn … bệnh sởi" (lỗi văn bản gốc) |
| 2855/2024 | Viêm gan C | bvdkbaclieu.gov.vn | **quét** | 33 | bản Gia Lai cũng quét |
| 3312/2024 | Đột quỵ não | bvtn.org.vn (BV Thống Nhất) | có (tr.1 ảnh) | 148 | **số 3312 và ngày không in trong tệp** |
| 2892/2022 | Béo phì | syt.gialai.gov.vn | có | 28 | link daithaoduong.kcb.vn trả 404 |
| 678/2025 | Dự phòng lây truyền mẹ–con | syt.gialai.gov.vn | có | 26 (+1 tr. QĐ) | **số 678 không in trong tệp**; ký số 26/02/2025 |
| 2065/2021 | Viêm gan C (bản cũ) | syt.gialai.gov.vn | có | 23 | |
| 1911/2021 | Tiền sản giật (bản cũ) | syt.gialai.gov.vn | có | 16 (+1 tr. QĐ) | |
| 4815/2020 | Viêm phổi cộng đồng (bản cũ) | benhviencaosudautieng.vn | có | 67 | bản ký số |
| 4845/2016 | Sốt rét (bản cũ) | drive.google.com (BV Nhi TƯ liên kết) | quét | 31 | chứng thư VOffice 08/09/2016 |
| 458/2011 | Dengue (bản cũ) | quangninhcdc.vn (CDC Quảng Ninh) | quét | 23 | |
| 250/2022 | COVID-19 (bản cũ) | camau.gov.vn (Cổng TTĐT Cà Mau) | có (tr.1 ảnh) | 143 | |
| 2187/2019 | HCMV cấp | benhvienhatrung.vn | có | 36 | chỉ phần HD; metadata xóa trắng |
| 3126/2018 | Lao 2018 (bản cũ, thân HD đầy đủ) | syt.gialai.gov.vn | có | 139 | lưu `3126_2018__46f795ca.pdf` |
| 1832/2022 | Huyết học (THAY 1494/2015) | syt.gialai.gov.vn | có | 528 (+1 tr. QĐ) | |
| 3510/2025 | Thần kinh ĐTĐ (mới) | bvdkbaclieu.gov.vn | có | 40 | |
| 2323/2025 | Sơ sinh – HD quốc gia (mới) | bvdkbaclieu.gov.vn | có | 670 | **không có trang QĐ**; số/ngày theo danh mục BV Bạc Liêu |
| 3651/2024 | Nấm Aspergillus phổi mạn (mới) | bvdkbaclieu.gov.vn | có | 79 | |
| 465/2024 | Mpox (mới, thay 2099/2022) | syt.gialai.gov.vn | có | 16 | bản Bạc Liêu là bản quét |
| 2341/2024 | IMCI (mới) | syt.gialai.gov.vn | quét | 28 (+1 tr. QĐ) | |
| 2959/2023 | COVID-19 trẻ em (mới, thay 405/2022) | bvdkbaclieu.gov.vn | có (glyph ƣ) | 70 | |
| 2671/2023 | COVID-19 (mới, thay 250/2022) | syt.gialai.gov.vn | có (tr.1 OCR xấu) | 147 | |
| 2248/2023 | HCMV mạn (mới) | bvdkbaclieu.gov.vn | có, **1.145 ký tự Kirin thay chữ Việt** | 38 | |
| 1005/2023 | Bệnh phổi mô kẽ (mới) | bvdkbaclieu.gov.vn | có | 205 | |
| TT13/2026 | (bản thứ hai) | bvdkbaclieu.gov.vn | lớp OCR của bên thứ ba trên ảnh | 19 | không thay OCR của dự án; giữ bản cũ |

## 4. Văn bản chưa tìm được / không xác minh được

| Khóa | Tình trạng | Đã tìm ở đâu (27/9/2026) |
| --- | --- | --- |
| 1622/2014 (dại, hiện hành, có dòng hạt giống) | Không có PDF chính thức | WebSearch: chỉ trang luật tư nhân, scribd; BV Nhi TƯ trỏ tới syt.kontum.gov.vn (chết); chicuccntyhcm.gov.vn 404; ttytdamrong.vn không phân giải DNS. Bản .doc trên vncdc.gov.vn (TLS hết hạn) → người dùng tải. |
| 1003/2012 (TCM, bản cũ) | Không có bản chính thức | Thư viện Gia Lai chỉ có .doc lấy từ trang luật tư nhân (loại); benhvienhatrung.vn là bản LuatVietnam (agent trước đã loại). |
| 3874/2018 (COPD, bản cũ) | Không cần | Đã bị 4562/2018 thay; file kcb.vn gắn nhãn 3874 thực chất là 4562. |
| 5456/2019 (HIV, bản cũ) | Có URL chính thức, chưa tải | vaac.gov.vn lỗi TLS; WebSearch chỉ ra trang luật tư nhân. |
| 1505/2026 (Ebola) | Không có PDF | kcb.vn/tin-tuc không đính kèm; báo chí 26/5/2026 không có liên kết tệp. Chưa đưa vào danh mục. |
| Hướng dẫn chuyên môn lịch TCMR của Cục Phòng bệnh (sau TT 13/2026) | Chưa thấy văn bản | tiemchungmorong.vn trang lịch 404; WebSearch chỉ ra bài báo. |
| "Cập nhật" HIV sau 5968/2021 | **Không xác minh được** | Một kết quả tóm tắt WebSearch nói 5968/2021 "đã được cập nhật", không nêu số văn bản → coi như KHÔNG có văn bản thay thế; 5968/2021 giữ current. |

## 5. Chuỗi thay thế theo bệnh (→ = "bị thay bởi"; nguồn: điều khoản trong văn bản, trang PDF ở supersession.csv)

- **Sởi:** 476/2009 → 1327/2014 (Đ2 của 1327) → **1019/2025** (Đ3, ảnh tr.1).
- **Cúm mùa:** 2078/2011 → **1840/2025** (Đ3, lớp chữ tr.1).
- **Viêm gan C:** 5012/2016 → 2065/2021 (Đ1) → **2855/2024** (Đ1, ảnh tr.1).
- **Viêm gan B:** 5448/2014 → 3310/2019 (Đ2, ảnh tr.2) → **1740/2026** (Đ3).
- **HIV:** 5456/2019 → **5968/2021** (Đ2). (Việc 5456 thay 5418/2017 chỉ thấy ở tóm tắt WebSearch → chưa xác minh.)
- **Dự phòng lây truyền mẹ–con:** 2834/2019 → **678/2025** (Đ2 trang QĐ).
- **Lao:** 979/2009 → 4263/2015 (Đ3, ảnh) → 3126/2018 (Đ3, ảnh) → 1314/2020 (Đ3) → **162/2024** (Đ3). 2760/2021 (cập nhật lao kháng thuốc, thay tr.43–53 của 1314/2020) → 162/2024: **SUY LUẬN, chưa xác minh** (162 chỉ nêu 1314).
- **Sốt rét:** 3232/2013 → 4845/2016 (Đ2, ảnh) → 2699/2020 (Đ1 trang QĐ IMPE) → **3377/2023** (Đ1, ảnh).
- **Dengue:** 794/2009 → 458/2011 (Đ3, ảnh) → 3705/2019 (Đ2, ảnh) → **2760/2023** (Đ1).
- **Tay chân miệng:** 1003/2012 → **292/2024** (Đ1, ảnh).
- **COVID-19 người lớn:** 4689/2021 (+ 5666/2021) → 250/2022 (Đ1, ảnh) (+ 437/2022 sửa đổi) → **2671/2023** (Đ1, ảnh; văn bản ghi ngày của 250 là "28 tháng 11 năm 2022" — lỗi đánh máy, không sửa).
- **COVID-19 trẻ em:** 405/2022 → **2959/2023** (Đ1).
- **Mpox:** 2099/2022 → **465/2024** (Đ1).
- **Viêm phổi cộng đồng người lớn:** 4815/2020 → **2147/2026** (Đ3).
- **COPD:** 2866/2015 và 3874/2018 → 4562/2018 (Đ3, tr.4); 3874/2018 → 2767/2023 (Đ3) → **2131/2026** (Đ3). 4562/2018: **không văn bản nào nêu tên**; tôi để `superseded` (suy luận, verified = no) vì COPD đã có hai bản sau — cần người quyết.
- **ĐTĐ típ 2:** phần ĐTĐ típ 2 của 3879/2014 → 3319/2017 (Đ3 trang QĐ trên kcb.vn, ngoài data/raw) → **5481/2020** (Đ3) + sửa đổi 1353/2021. 3280/2011: không văn bản nào nêu tên → vẫn `current` theo quy tắc (bản xuất "LawSoft" trên kcb.vn; hạng 49, ngoài kho).
- **Béo phì:** bài "Bệnh béo phì" trong 3879/2014 → **2892/2022** (Đ3). 3879/2014 → `partial`.
- **ĐTĐ thai kỳ:** 6173/2018 → **1470/2024** (Đ3, ảnh).
- **THA thai kỳ/tiền sản giật:** 1911/2021 → **1154/2024** (Đ3 trang QĐ bản quét Drive, agent trước đọc; tệp đó chưa lưu data/raw).
- **Suy tim:** 1762/2020 → **1857/2022** (Đ3).
- **Đột quỵ:** 5331/2020 → **3312/2024** (Đ3, ảnh tr.1).
- **Thận:** 4 bài của 3931/2015 → **2388/2024** (Đ3); 3931/2015 → `partial`.
- **Huyết học:** 1494/2015 → **1832/2022** (Đ3, ảnh trang QĐ). *Mới phát hiện.*
- **Hen:** 4776/2009 và 2 bài của 3942/2014 → **1851/2020** (Đ3).
- **Tiêm chủng:** TT 38/2017 → TT 10/2024 (Đ4) → TT 52/2025 (Đ4 k2) → **TT 13/2026** (Đ27 k2 điểm d; cùng bãi bỏ TT 24/2018, 34/2018, 05/2020).
- **Phản vệ:** TT 08/1999 → **TT 51/2017** (Đ7 k2).
- **Suy dinh dưỡng cấp trẻ em:** 4487/2016 → **2989/2026** (Đ1).
- **BKLN tại trạm y tế xã:** Phần 2 của 2919/2014 → **5904/2019** (Đ3); 2919/2014 → `partial`.
- **Không có chuỗi (văn bản đơn, không thay văn bản nào theo Điều khoản đã đọc):** 1005/2023, 1530/2023, 1760/2024, 1768/2026, 2248/2023, 2341/2024, 2558/2022, 3087/2020, 3510/2025, 3651/2024, 3908/2023, 493/2026, 5642/2015, 1493/2015, 315/2015, 361/2014, 3312/2015, 6101/2019. **Chưa đọc được điều khoản** (tệp không có trang QĐ): 3192/2010 (THA), 2187/2019 (HCMV cấp), 2323/2025, 3610/2015, 4121/2009 — verified = no.

Tổng: 77/85 dòng có quan hệ lấy từ điều khoản trong văn bản (verified = yes); 8 dòng verified = no (4562/2018, 2760/2021 là suy luận; 1622/2014, 2187/2019, 2323/2025, 3192/2010, 3610/2015, 4121/2009 chưa đọc được điều khoản).

## 6. Đề xuất kho in_corpus (theo thứ tự đăng ký `vnsoc.extract.corpus_priority`, ocr_already = 3)

Tầng 1 = có dòng hạt giống/mẩu thí điểm; tầng 2 = lớp chữ, ban hành 2025–2026; tầng 3 = lớp chữ, mới trước; tầng 4 = bản quét.

| Hạng | Khóa | Tầng | OCR | Bệnh/chủ đề |
| --- | --- | --- | --- | --- |
| 1 | 1470/2024 | 1 | OCR | ĐTĐ thai kỳ |
| 2 | 162/2024 | 1 | | Lao |
| 3 | 1740/2026 | 1 | | Viêm gan B |
| 4 | 2131/2026 | 1 | | COPD |
| 5 | 2760/2023 | 1 | | Dengue |
| 6 | 2892/2022 | 1 | | Béo phì |
| 7 | 292/2024 | 1 | OCR | Tay chân miệng |
| 8 | 3192/2010 | 1 | | Tăng huyết áp |
| 9 | 3377/2023 | 1 | OCR | Sốt rét |
| 10 | 5481/2020 | 1 | | ĐTĐ típ 2 |
| 11 | 5642/2015 | 1 | | Một số bệnh truyền nhiễm |
| 12 | 5904/2019 | 1 | | BKLN tại trạm y tế xã (bản lớp chữ theo pdf_choice) |
| 13 | 5968/2021 | 1 | | HIV/AIDS |
| 14 | 678/2025 | 1 | | Dự phòng lây truyền mẹ–con |
| 15 | TT13/2026 | 1 | OCR | Tiêm chủng |
| 16 | TT51/2017 | 1 | OCR | Phản vệ |
| 17 | 2989/2026 | 2 | | Suy dinh dưỡng cấp trẻ em |
| 18 | 2147/2026 | 2 | | Viêm phổi cộng đồng người lớn |
| 19 | 1768/2026 | 2 | | Dinh dưỡng người bệnh ung thư |
| 20 | 493/2026 | 2 | | Nipah |
| 21 | 3510/2025 | 2 | | Thần kinh ĐTĐ |
| 22 | 2323/2025 | 2 | | Chăm sóc, điều trị sơ sinh |
| 23 | 1840/2025 | 2 | | Cúm mùa |
| 24 | 1019/2025 | 2 | | Sởi |
| 25 | 3651/2024 | 3 | | Nấm Aspergillus phổi mạn |
| 26 | 3312/2024 | 3 | | Đột quỵ não |
| 27 | 2388/2024 | 3 | | Bệnh thận mạn |
| 28 | 1760/2024 | 3 | | ĐTĐ típ 1 trẻ em |
| 29 | 1154/2024 | 3 | | THA thai kỳ, tiền sản giật |
| 30 | 465/2024 | 3 | | Mpox |
| 31 | 3908/2023 | 3 | | Dự phòng thuyên tắc huyết khối tĩnh mạch |
| 32 | 2959/2023 | 3 | | COVID-19 trẻ em |
| 33 | 2671/2023 | 3 | | COVID-19 |
| 34 | 2248/2023 | 3 | | Hội chứng mạch vành mạn |
| 35 | 1530/2023 | 3 | | Loét bàn chân ĐTĐ |

**Dự phòng DR2 theo đúng thứ tự:** 1005/2023 (phổi mô kẽ), 2558/2022 (võng mạc ĐTĐ), **1857/2022 (suy tim)**, 1832/2022 (huyết học), 1353/2021 (sửa đổi 1 trang của 5481/2020 — nếu tới lượt nên gộp vào 5481), 3087/2020, **1851/2020 (hen)**, 2187/2019 (HCMV cấp), 3610/2015, 3312/2015, 1493/2015, 315/2015, 361/2014, 3280/2011, rồi tầng 4: **2855/2024 (viêm gan C, quét)**, 2341/2024 (IMCI, quét), 6101/2019, 4121/2009.

**OCR:** trong kho 5 văn bản (1470/2024, 292/2024, 3377/2023, TT13/2026, TT51/2017) + 3 bản cũ dùng cho phân tích phiên bản đã OCR (1327/2014, 3310/2019, 3705/2019) = **8/10**. (CLI `corpus_priority` mặc định ocr_already = 0; tôi gọi hàm với 3 — kết quả 35 văn bản không đổi.)

**Những điểm người dùng nên biết trước khi đăng ký OSF (HG2.9 chưa nộp):**
1. **Phạm vi danh mục quyết định kết quả.** Tôi thêm vào danh mục các hướng dẫn chẩn đoán/điều trị 2022–2026 thuộc các nhóm bệnh của đề cương (truyền nhiễm, tim mạch–chuyển hóa, hô hấp, thận, bà mẹ–trẻ em) mà tôi đã tải và đọc điều khoản. Bảy văn bản mới (2248/2023, 2323/2025, 2671/2023, 2959/2023, 3510/2025, 3651/2024, 465/2024) vào kho và đẩy ra: 1353/2021, **1851/2020 (hen)**, **1857/2022 (suy tim)**, 2187/2019, 2558/2022, 3087/2020, 3610/2015. Suy tim và hen giàu giá trị số và có đối chiếu ESC/GINA — nếu người dùng muốn giữ, cần sửa quy tắc (addendum) chứ không chọn tay.
2. **Văn bản đã thấy nhưng KHÔNG thêm vào danh mục** (ngoài nhóm bệnh của đề cương, hoặc không có đối chiếu nước ngoài theo định nghĩa): 456/2026 u xơ tử cung, 422/2026 lạc nội mạc tử cung, 3898/2025 sàng lọc ung thư vú, 3991/2025 và 2730/2026 (y học cổ truyền), 2988/2025 (chế độ ăn sinh ceton), 3792/2024 (ung thư cổ tử cung), 3977/2024 (SKSS tiền mãn kinh), 472/2024 (Hemophilia), 2201/2023 (Marburg). **Mô phỏng: nếu thêm bất kỳ văn bản nào trong 9 văn bản này (giả định có lớp chữ), nó vào kho (hạng 21–35) và đẩy 1530/2023 ra**; thêm cả 9 thì 7 văn bản vào kho (456, 422, 3898, 3991, 2988, 3792, 3977) và 7 văn bản bị đẩy ra: 1154/2024 (tiền sản giật), 1530/2023, 2248/2023, 2671/2023, 2959/2023, 3908/2023, 465/2024. Các văn bản 2020–2022 khác thấy trong thư viện Gia Lai (STI 2021: 5165, 5169, 5183, 5185, 5186; 2475/2022 bệnh động mạch ngoại biên; 5332/2020, 5333/2020 tim mạch; 2122/2022, 1856/2022 hậu COVID; nhóm ký sinh trùng 2022) **chưa xử lý**; chúng xếp sau hạng 37 nên không đổi 35 văn bản đề xuất, nhưng sẽ đổi thứ tự dự phòng DR2 nếu được thêm. Đề xuất: người dùng chốt tiêu chí phạm vi danh mục và ghi vào DECISIONS/đăng ký trước.
3. **Văn bản ít giá trị số trong kho:** 493/2026 (Nipah, 10 tr., agent c5 ghi "rất ít giá trị số"), 1768/2026 (dinh dưỡng ung thư). Tầng 2 đưa chúng vào một cách cơ học.
4. **Văn bản trong kho có số/ngày chưa in trong tệp:** 3312/2024, 678/2025, 2323/2025 (xem §3); **nguồn cần người chấp nhận:** 1154/2024 (drive.google.com qua BV Sa Đéc), 2892/2022, 678/2025, 465/2024, 2671/2023 (thư viện Sở Y tế Gia Lai, tải trong phiên), 1019/2025 (t5g.org.vn).
5. **Chất lượng lớp chữ:** 2248/2023 có 1.145 ký tự Kirin thay chữ Việt (verify_span cần bảng chuẩn hóa như với ƣ→ư); 2959/2023, 5904/2019, 5968/2021 dùng glyph ƣ; 2671/2023 tr.1 là lớp OCR không dấu (trang QĐ, không cần cho mẩu).
6. **Tiêm chủng:** TT 13/2026 không còn bảng lịch tiêm → mẩu lịch TCMR (P-immunization-01/02/04) không có văn bản hiện hành trong kho cho tới khi tìm được hướng dẫn chuyên môn của Cục Phòng bệnh.
7. **Nếu người dùng tìm được** 1622/2014 (dại) → vào tầng 1 và đẩy 1530/2023 ra; bản lớp chữ của 2855/2024 → vào tầng 3 hạng ~27 và đẩy 1530/2023 ra.
8. Trước đóng băng 15/10/2026: quét lại kcb.vn, danh mục BV Bạc Liêu, thư viện Sở Y tế Gia Lai (văn bản ban hành 27/9–15/10 được thêm; sau 15/10 chỉ ghi chú theo DR7).

## 7. Việc cho người dùng (cũng ghi ở state/gates/HG2.3_missing.md, mục D)

1. Tải .doc 1622/2014 từ vncdc.gov.vn bằng trình duyệt → `data/raw/manual/1622_2014.doc`, báo Claude chạy `vnsoc.extract.doc_to_pdf`.
2. Mở https://bvcdn.org.vn/wp-content/uploads/2024/12/2855-qdbytvgc.pdf bằng trình duyệt; nếu có lớp chữ lưu `data/raw/manual/2855_2024.pdf`.
3. Tải 5456/2019 từ vaac.gov.vn bằng trình duyệt → `data/raw/manual/5456_2019.pdf`.
4. **Xóa tay** (hook chặn agent): `data/raw/manual/1003_2012.doc` (lấy từ trang luật tư nhân — tôi lỡ lưu trước khi soát metadata), `data/raw/3216_2018.pdf`, `data/raw/3874_2018.pdf`.
5. Tra thủ công số/ngày của 3312/2024, 678/2025, 2323/2025 và báo lại nếu khác.
6. Chấp nhận/không chấp nhận các nguồn ở §6 mục 4 và 2187/2019 (BVĐK Hà Trung, metadata xóa trắng), 4845/2016 (Drive do BV Nhi TƯ liên kết).
7. Quyết định: (a) tiêu chí phạm vi danh mục (§6 mục 2); (b) 4562/2018 để `superseded` (suy luận) hay `current`; (c) có dùng 3705/2019 (bản watermark LuatVietnam) cho phân tích phiên bản không; (d) chấp nhận đề xuất 35 văn bản hay sửa quy tắc trước OSF.
8. Hạn HG2.3 trong kế hoạch: 12/10/2026.

## 8. Thay đổi mã và dữ liệu trong task này

- `src/vnsoc/extract/manifest_merge.py`: khi các phần mâu thuẫn trạng thái, **lấy trạng thái của phần sau cùng** (thứ tự tên tệp c1_ … c6_) thay vì phần có nhiều bằng chứng nhất khi hòa điểm, và vẫn gắn cờ "MÂU THUẪN … cần người quyết" — đặt cờ và ghi chú của phần mới nhất lên đầu để không bị cắt ở 4.000 ký tự; `ocr` được gộp bằng OR như `in_corpus`. Test mới: `tests/test_manifest_merge.py::test_latest_part_status_wins_and_flag_survives_truncation`. Bảy dòng hiện mang cờ này (1327/2014, 1494/2015, 2078/2011, 250/2022, 3879/2014, 4562/2018, 5331/2020) — đều là thay đổi của C2.5 có bằng chứng ở supersession.csv, trừ 4562/2018 (suy luận).
- Không sửa `data/interim/pdf_choice.json`. Đề xuất thêm `"3126/2018": "3126_2018__46f795ca.pdf"` (thân HD đầy đủ; văn bản không thuộc kho và không có mẩu thí điểm). Không đổi lựa chọn của TT13/2026 (bản thứ hai là lớp OCR của bên thứ ba).
- Tệp mới trong data/raw (không commit): 1019_2025, 1840_2025, 2855_2024, 3312_2024, 2892_2022, 678_2025 (+__3241fdd5), 2065_2021, 1911_2021 (+__27810c20), 3126_2018__46f795ca, 2671_2023, 2341_2024 (+__e7639ce8), 1832_2022 (+__5a1f1b1a), 465_2024, TT13_2026__f1b47afd, 3510_2025, 2323_2025, 3651_2024, 2959_2023, 2248_2023, 1005_2023, 2187_2019, 4815_2020, 4845_2016, 458_2011, 250_2022; và `manual/1003_2012.doc` (bị loại, cần xóa).
- Kiểm tra: `vnsoc.schemas manifest` OK (85 dòng); `vnsoc.check count … --min 25 --where in_corpus=true status=current` → 35; pytest `tests/test_manifest.py tests/test_manifest_merge.py tests/test_fetch_pdf.py` (và test_prereg_support, test_freeze, test_pilot_atoms): 161 passed.
