# Báo cáo thí điểm T1.1 — chủ đề `tbhiv` (Lao, lao kháng thuốc, HIV)

Ngày: 2026-09-26 · Agent: claude (atom-extractor + counterpart-matcher) · File mẩu: `data/interim/pilot/tbhiv.jsonl` (7 mẩu)

Kiểm tra bắt buộc đã chạy trên file cuối:
- `python -m vnsoc.schemas atom data/interim/pilot/tbhiv.jsonl` → **OK 7 dòng hợp lệ**
- `python -m vnsoc.extract.verify_span data/interim/pilot/tbhiv.jsonl` → **OK: 0 mẩu không đạt** (cả 7 mẩu `span_verified: true`)
- `check_decoy(atom) == []` với mọi mẩu có mồi; `tolerance` và `conflict_status` do `finalize()` tính, không đặt tay.

Tóm tắt: **7 mẩu**. Có 3 mẩu xung đột (01, 03, 05) và 4 mẩu đối chứng (02, 04, 06, 07). Trong đó 2 mẩu lệch phiên bản (01, 02) có điền `superseded`. Mẩu 01 vừa lệch phiên bản vừa xung đột với WHO 2026.

> **LƯU Ý (sau kiểm toán, 26/9 chiều):** mục 1–6 là bản **trước kiểm toán**. Trạng thái hiện hành nằm ở **mục 7 "Sau kiểm toán"**. Tóm tắt thay đổi: 02 thành **indistinguishable** (thêm WHO 2019); 01 vẫn conflict ở phân tích chính nhưng nhãn temporal bị nhiễu nguồn (WHO 2020 ghi dưới dạng giá trị `derived`), mồi đổi BPaLM → BPaMZ; 03 có nguồn Mỹ có băm, thêm WHO 2017 và giá trị lân cận trẻ em (neighbour_overlap); cat_options 03/04 viết lại và thử 48 câu mỗi mẩu. Không còn mẩu lệch phiên bản sạch nào trong chủ đề này.

---

## 1. Văn bản đã tải

### 1a. Văn bản Bộ Y tế (tải bằng `vnsoc.extract.fetch_pdf` → `data/raw/`)

| Khóa | Nguồn (URL) | sha256 (16 ký tự) | Trang | text_kind | Ghi chú xác định danh tính / nơi đã tìm |
|---|---|---|---|---|---|
| 162/2024 | https://bvtn.org.vn/wp-content/uploads/2024/10/Tai-lieu-lao-ban-cuoi-V10-_-Final.signed.pdf (Bệnh viện Thống Nhất, đăng lại nguyên quyết định + tài liệu) | d3085cf9246c5eb9 | 213 | ok | Bản ký số, lớp chữ để trống số hiệu ("Số: /QĐ-BYT"). Tr.1 ghi quyết định ban hành "Hướng dẫn Chẩn đoán, điều trị và dự phòng bệnh Lao" năm 2024, thay thế QĐ 1314/QĐ-BYT ngày 24/03/2020, Thứ trưởng Trần Văn Thuấn ký, dấu văn thư BV Thống Nhất ngày 25/01/2024. Trang bệnh viện ghi QĐ 162/QĐ-BYT. kcb.vn không có bản này (kcb.vn/phac-do chỉ có bản 2015). Trang emohbackup.moh.gov.vn (documentId=9376) không truy cập được (lỗi TLS/"server name not supported"). |
| 2760/2021 | https://cms-chonglao.benhvienphoitrunguong.vn/uploads/QD_1314_BYT_2020_Phan_Huong_dan_dieu_tri_benh_lao_khang_thuoc_d212452cd5.pdf (Bệnh viện Phổi Trung ương, đơn vị thường trực Chương trình chống lao quốc gia) | d0845534188da21e | 53 | ok | **Chỉ có phần tài liệu đính kèm**, không có trang quyết định. Tr.1: "CẬP NHẬT HƯỚNG DẪN ĐIỀU TRỊ BỆNH LAO KHÁNG THUỐC", thay các nội dung lao kháng thuốc của 1314/QĐ-BYT (tr.43–53), tháng 04/2021, Giám đốc BV Phổi TW và Chủ tịch Hội đồng ký. Trang quyết định (1 trang, xem ở bvdksadec.vn, không lưu vào data/raw) ghi "Ban hành kèm theo Quyết định này 'Cập nhật hướng dẫn điều trị bệnh lao kháng thuốc'" và nhắc biên bản hội đồng ngày 20/4/2021, khớp với tài liệu. **Cần người xác nhận ở HG1.2.** Các nơi đã thử mà không dùng được: syt.binhdinh.gov.vn (lỗi TLS), soyt.ninhthuan.gov.vn (404), bvbnd.vn (bản quét 54 trang, không có lớp chữ), syt.khanhhoa.gov.vn (chỉ có công văn triển khai 1 trang). |
| 1314/2020 | https://www.bvbnd.vn/wp-content/uploads/2022/09/Phac-do-Lao_2020.pdf (Bệnh viện Bệnh Nhiệt đới TP.HCM) | 5072d3231393e556 | 142 | ok | Tr.1 có đủ "Số: 1314/QĐ-BYT", ngày 24/3/2020, thay QĐ 3126/QĐ-BYT ngày 23/5/2018. |
| 5968/2021 | https://soyte.laichau.gov.vn/upload/81345/20220106/5968_BYT_VE_HD_chan_doan_cham_soc_HIV_AIDS_c79a618abb.pdf (Sở Y tế Lai Châu) | babb478043425396 | 145 | ok | Bản ký số, thay QĐ 5456/QĐ-BYT ngày 20/11/2019; dấu văn thư Sở Y tế Lai Châu 01/01/2022; lớp chữ có "5968 31 12". Lớp chữ dùng ký tự "ƣ" (U+01A3) thay cho "ư" ở một số đoạn, nên span được cắt tự động từ văn bản trang, không gõ lại. Bản chính thức trên vaac.gov.vn (`/files/qd-5968-...pdf`) có nhưng chứng chỉ TLS hết hạn nên fetch_pdf từ chối. |
| 5456/2019 | — | — | — | — | **Chưa tải được.** Đã hết quota WebSearch của phiên (200/200) trước khi tìm được bản chính thức. Chỉ thấy bản trên một trang thư viện luật tư nhân và svhattc.org (chưa rõ tư cách), nên không dùng. |

Các file chỉ tải về scratchpad để kiểm tra, không đưa vào `data/raw`: bản quét 2760/2021 (bvbnd.vn), công văn Sở Y tế Khánh Hòa, trang quyết định 2760/2021 (bvdksadec.vn, 1 trang).

### 1b. Nguồn nước ngoài (tải bằng `vnsoc.match.sources`, chỉ lưu giá trị + vị trí, không lưu đoạn văn)

| Nguồn | Phiên bản | URL đã tải | page_sha256 (16) | Ghi chú |
|---|---|---|---|---|
| WHO consolidated guidelines on TB, Module 4: treatment and care, **2nd ed.** (IRIS 10665/387622) | 2026-09-21 | iris.who.int/server/api/core/bitstreams/fb7951ad-…/content | a6092c81773c72f3 | 544 trang, **bản WHO hiện hành tại 10/2026** |
| WHO Module 4: treatment and care (IRIS 10665/380799) | 2025-03-14 | …/bitstreams/f663f086-…/content | f81e9281d2669bd0 | chỉ dùng để đối chiếu (tiền siêu kháng: BPaL; BDLLfxC bỏ Lfx = BDLC) |
| WHO Module 4: drug-susceptible TB treatment (10665/353829) | 2022-05-04 | …/bitstreams/cf34aa08-…/content | d179d1244868d020 | A1.1 là 2HRZE/4HR, giống bản 2026 |
| WHO Module 4: drug-resistant TB treatment, 2022 update (10665/365308) | 2022-12-14 | …/bitstreams/b4112461-…/content | 7fdfa0ba5270e99d | BPaLM/BPaL, phác đồ 9 tháng |
| WHO Guidelines for HIV post-exposure prophylaxis (10665/378221) | 2024-07-16 | …/bitstreams/fc3c8ce2-…/content | 56493a3528ed7624 | 28 trang |
| CDC nPEP 2025, MMWR Recomm Rep 74(1) (PMC12064164) | 2025-05-08 | eutils.ncbi.nlm.nih.gov efetch db=pmc id=12064164 (XML toàn văn) | 69b99dc9b154d2a2 | trang PMC bị reCAPTCHA nên dùng E-utilities |
| CDC "Treatment for TB disease" | last reviewed 2025-04-17 | www.cdc.gov/tb/hcp/treatment/tuberculosis-disease.html | **null** | công cụ sources bị HTTP 403; đọc bằng WebFetch → **needs_human_check** |

Không dùng được: ATS/CDC/IDSA 2016 DS-TB (PMC6590850). Trang PMC bị reCAPTCHA, efetch không có phần thân bài, Europe PMC trả lỗi 500. **[Sau kiểm toán: không còn đúng — bản PDF trên cdc.gov tải được (sha256 `86123eb8…`, 49 tr.) và nay là nguồn Mỹ của mẩu 03; xem 7.1 và 7.7.]**
Lưu ý kỹ thuật: lần gọi đầu bằng URL handle IRIS cũ (`/bitstream/handle/10665/353829/...pdf`) chỉ nhận về trang SPA rỗng, và trang này đã nằm trong `data/cache/foreign/index.json` (a859cc83…). Nếu dùng lại URL đó thì phải `--refresh` hoặc dùng URL bitstream API.

---

## 2. Bảng mẩu

| ID | Slot | Việt Nam (tập giá trị) | Nước ngoài (hệ thống: giá trị, phiên bản) | Bản cũ | Trạng thái (finalize) | Trang PDF |
|---|---|---|---|---|---|---|
| P-tbhiv-01 | first_line (drugs) — lao **tiền siêu kháng** (kháng R + kháng FQ từ đầu), ≥ 14 tuổi, lao phổi không nặng, đủ tiêu chuẩn | **BPaL** (6–9 tháng) | WHO_global: BPaL **hoặc BDLC** (WHO 2026, B1.1a/B1.2a); BPaL (WHO 2022) | 2760/2021 tr.17 và 1314/2020 tr.60: E1 "Bdq Lzd Cfz Cs + 1 thuốc nhóm C" (phác đồ cá thể dài hạn) | **conflict** (do BDLC) + lệch phiên bản; mồi BPaLM | 162/2024 tr.53 |
| P-tbhiv-02 | first_line (drugs) — lao đa kháng còn nhạy FQ, người lớn, phác đồ chuẩn ngắn hạn 9–11 tháng | có **bedaquiline** (C1a/C2a, toàn uống) | WHO_global: 9-month all-oral có bedaquiline (WHO 2026, B2.1, không đổi từ 2022) | 1314/2020 tr.59: "4-6 Am Lfx Pto Cfz Z H liều cao E / 5 Lfx Cfz Z E" (**amikacin**) | **concordant** + lệch phiên bản | 162/2024 tr.49 |
| P-tbhiv-03 | first_line (cat) — lao phổi nhạy cảm, **người lớn**, phác đồ 6 tháng, giai đoạn duy trì | **4RHE** (2HRZE/4RHE) | WHO_global: 4HR (WHO 2026 A1.1); US: 4HR (trang CDC, 2025) | 1314/2020 và 2760/2021 cùng 4RHE (không lệch) | **conflict**; mồi 4RE | 162/2024 tr.44 |
| P-tbhiv-04 | first_line (cat) — lao nhạy cảm, **trẻ em**, phác đồ 6 tháng, giai đoạn duy trì | 4RH (2HRZE/4RH) | WHO_global: 4HR (WHO 2026 A1.6a/b) | 1314/2020 cùng 4RH | **concordant** (đối chứng ghép cặp với 03) | 162/2024 tr.44 |
| P-tbhiv-05 | first_line (drugs) — PEP, > 10 tuổi (câu hỏi dùng người lớn), phơi nhiễm không do nghề nghiệp | TDF + 3TC (hoặc FTC) + DTG | WHO_global: TDF + 3TC/FTC + DTG (WHO PEP 2024); US: **BIC/FTC/TAF** hoặc DTG + TDF/TAF + FTC/3TC (CDC nPEP 2025) | chưa có (thiếu 5456/2019) | **conflict** (chỉ với Mỹ, do BIC/FTC/TAF); mồi TDF + 3TC + NVP | 5968/2021 tr.29 |
| P-tbhiv-06 | duration (num, day) — thời gian PEP | 28 ngày | WHO_global: 28 ngày (2024); US: 28 ngày (CDC 2025) | — | **concordant** | 5968/2021 tr.29 |
| P-tbhiv-07 | duration (num, month) — lao kháng H nhạy R | 6 tháng | WHO_global: 6 tháng (WHO 2026 B4.1, không đổi từ 2018) | 1314/2020 cùng 6 R(H)ZELfx | **concordant** | 162/2024 tr.59 |

> **[Sau kiểm toán]** Bảng trên là bản gốc. Trạng thái hiện hành: 02 = indistinguishable; 01 mồi = BPaMZ; nguồn Mỹ 03 = ATS/CDC/IDSA 2016 + ATS/CDC/ERS/IDSA 2025. Xem bảng 7.1.

Thiết kế giá trị cần lưu ý (đã ghi trong `extraction.notes` từng mẩu):
- **key_drugs chỉ chứa thuốc phân biệt**, không liệt kê cả phác đồ. Lý do: `vnsoc.grade._gap` với kiểu drugs cho gap = 0 ngay khi hai tập có chung một thuốc, nên các phác đồ cùng có bedaquiline/linezolid/TDF sẽ bị coi là trùng nhau. **[Sau kiểm toán: lý do này đã lỗi thời — `_gap` hiện so tập bằng nhau; lý do đúng là `matches()` dùng tập con. Quy ước "thuốc phân biệt" vẫn giữ.]** Cách mã hóa: "BPaL" là tên tổ hợp mà grader gộp sẵn; E1 dùng cycloserine; BDLC dùng delamanid + clofazimine; phác đồ ngắn hạn phân biệt bằng bedaquiline và amikacin; PEP dùng lõi TDF + DTG.
- Mẩu 03/04 dùng `value_kind = cat` (nhãn HRE / HR / RE) chứ không dùng drugs, vì {R,H,E} và {H,R} giao nhau. Đã thử `cat_options` với 11 câu trả lời mẫu: "2HRZE/4HR", "4 tháng RH", "R và H" → foreign (US + WHO); "2RHZE/4RHE", "R, H và E" → đúng Bộ Y tế; "2HRZE/4RE" → mồi.

---

## 3. Ứng viên bị loại và lý do

1. **HIV bậc một người lớn TDF + 3TC + DTG** (đối chứng trong danh sách hạt giống; 5968/2021 tr.34, Bảng 5). Giá trị có trong văn bản, nhưng trong lớp chữ ô bảng ghi "+DTG1" (số chú thích dính liền). Bộ tách thuốc của grader (`(?![a-z0-9])`) nên không nhận ra DTG, và verify_span thất bại. Không có đoạn nào khác nêu phác đồ bậc một cho người lớn mà không kèm chú thích. Đã thay bằng 2 mẩu PEP (05, 06). Đề xuất sửa parser ở mục 6. **[Sau kiểm toán: `parse_drugs` đã bỏ số chú thích, nên lý do kỹ thuật không còn. Mẩu này vẫn CHƯA dựng; lý do mới ở 7.3 mục 6.]**
2. **Lao hạch người lớn: 12 tháng → 6 tháng** (ứng viên lệch phiên bản). 1314/2020 tr.54 và 2760/2021 tr.5 ghi B1 (2RHZE/10RHE) cho "lao màng não, lao xương khớp và lao hạch người lớn". 162/2024 tr.46 ghi B1 chỉ cho lao hệ thần kinh trung ương và lao xương khớp. Bản hiện hành **không có câu nào** nói lao hạch điều trị 6 tháng; đó chỉ là suy luận từ phần "không chỉ định" của A1. Loại, vì span không chứa quần thể. Nếu bác sĩ chấp nhận suy luận này thì có thể dựng mẩu.
3. **Hạt giống dòng 22 đúng nguyên văn** ("lao đa kháng: BPaL(M) vs 2760/2021"). Với lao đa kháng còn nhạy FQ, 162/2024 vẫn giữ phác đồ C, giống PĐ C của 2760/2021, bên cạnh BPaLM. Giá trị bản cũ vì vậy nằm trong tập hiện hành, nên không phải lệch phiên bản. Đã chuyển sang nhóm tiền siêu kháng (mẩu 01).
4. **Thời gian phác đồ lao đa kháng** (6 tháng BPaLM so với 9–11 tháng): tập hiện hành {6, 9–11} chứa giá trị bản cũ 9–11, nên không phân biệt được.
5. **Phác đồ 4 tháng** (A1a 2HPMZ/2HPM cho ≥ 12 tuổi; A2a 2HRZE/2RH cho trẻ thể nhẹ): đây là lựa chọn được thêm vào, bản hiện hành vẫn giữ 6 tháng, nên không phải lệch phiên bản. Có thể dùng làm đối chứng với WHO ở vòng sau. Lưu ý: A2a (tr.45) ghi "02 tháng, với 2 loại thuốc: R, H, E", tức nói 2 loại nhưng liệt kê 3 thuốc. Đây là mâu thuẫn nội bộ nên đã tránh.
6. **Tuổi tối thiểu dùng bedaquiline**: 2760/2021 ghi "trẻ em dưới 6 tuổi" là chống chỉ định tuyệt đối; 162/2024 chuyển thành "cẩn trọng" (Bảng 5). Bản hiện hành không nêu một ngưỡng tuổi cụ thể, nên không có giá trị để hỏi. Loại.
7. **HIV lệch phiên bản 5456/2019 → 5968/2021**: chưa có PDF chính thức của 5456/2019 (mục 1a).
8. **DTG 50 mg × 2 lần/ngày khi dùng rifampicin**: đoạn tìm được ở 5968/2021 tr.37 là bảng liều trẻ em; chưa tìm được câu tương ứng cho người lớn trong thời gian cho phép. Loại.

---

## 4. SAI LỆCH SO VỚI BỘ HẠT GIỐNG VÀ VỚI KỲ VỌNG CỦA BẢNG GIAO VIỆC

- **Dòng 22 (lao đa kháng) mô tả chưa đúng.** (a) 162/2024 **không thay** phác đồ của 2760/2021 cho lao đa kháng còn nhạy FQ: C1a giống PĐ C 2021, được thêm C2a và BPaLM. (b) Lệch phiên bản sạch chỉ có ở nhóm **kháng FQ từ đầu**: E1 dài hạn (2760/2021 và 1314/2020) chuyển sang BPaL (162/2024). (c) Mốc WHO trong hạt giống là "WHO 2022 BPaLM", nhưng bản WHO hiện hành là **Module 4 bản 2 (21/9/2026)**. Bản này thêm BDLC (B1.2a) cho lao phổi tiền siêu kháng không nặng, và BPaLC (B1.1b) cho thể nặng. Vì vậy mẩu 01 thành **xung đột với WHO_global**, không chỉ là "có thể trùng Việt Nam". (d) Trạng thái trong hạt giống là `version_drift`; kết quả thực tế là version_drift + conflict.
- **Kỳ vọng "lao nhạy cảm 2HRZE/4HR trùng WHO" SAI với người lớn.** 162/2024 (tr.44) quy định cho người lớn **2HRZE/4RHE**, tức có ethambutol ở giai đoạn duy trì; 1314/2020 và 2760/2021 cũng vậy. Đây là **xung đột** với WHO (2HRZE/4HR, A1.1) và CDC. Chỉ phác đồ trẻ em (A2: 2HRZE/4RH) mới trùng WHO (mẩu 04).
- **Đối chứng "HIV bậc một TDF + 3TC + DTG"** chưa dựng được vì lỗi tách thuốc (mục 3.1); không phải do giá trị sai.
- **Trùng số hiệu cần cảnh giác:** 2760/**2021** (lao kháng thuốc) khác 2760/**2023** (sốt xuất huyết). Khóa file đã khác nhau (`2760_2021.pdf` và `2760_2023.pdf`).

---

## 5. Việc cần người kiểm ở HG1.2

1. **Danh tính 2760_2021.pdf**: xác nhận tài liệu của CTCLQG/BV Phổi TW (4/2021) đúng là phần ban hành kèm QĐ 2760/QĐ-BYT ngày 03/6/2021. Tên file trên máy chủ ghi "QD_1314 … Phan_Huong_dan_dieu_tri_benh_lao_khang_thuoc".
2. **Danh tính 162_2024.pdf** (số hiệu để trống trong lớp chữ): xác nhận đây là QĐ 162/QĐ-BYT ngày 19/01/2024.
3. **Hiệu lực tại 15/10/2026**: kiểm tra xem 162/2024 và 5968/2021 có bị thay hoặc sửa một phần không. Công cụ tìm kiếm của phiên đã hết quota nên chưa rà hết. Có thấy một "Tài liệu hướng dẫn lâm sàng" của CTCLQG (2025) trên cdcvinhphuc.vn; cần xem đó có phải văn bản Bộ Y tế sửa đổi hay không.
4. **Nguồn US của mẩu 03** (trang CDC, page_sha256 = null): mở trang và xác nhận giai đoạn duy trì là isoniazid + rifampin (4HR).
5. **Mẩu 01**: 162/2024 vẫn giữ "PĐ E: Bdq Lzd Cfz Cs + 1 thuốc nhóm C" (tr.56) cho người kháng FQ **không đủ** tiêu chuẩn BPaL. Câu hỏi phải nêu đủ tiêu chuẩn BPaL. Người kiểm cần quyết định có chấp nhận nhãn "lệch phiên bản" ở mẩu này không, vì phác đồ cũ vẫn là phương án dự phòng hiện hành.
6. **Mẩu 02**: phác đồ ngắn hạn có thuốc tiêm (giá trị bản cũ) từng là khuyến cáo WHO trước 12/2019. Nếu tính cả WHO cũ thì mẩu này có thể là "không phân biệt được nguồn". Cần quyết định có tải WHO 2019 để ghi vào `foreign` không.
7. **Mẩu 03**: có thể WHO 2010 từng cho phép HRE ở giai đoạn duy trì khi tỷ lệ kháng isoniazid cao. Đây là **giả thuyết chưa kiểm**, chưa tải WHO 2010. Điều này không đổi nhãn, nhưng liên quan đến cách diễn giải `moh_lags_evidence`, việc chỉ bác sĩ được gán.
8. **Mồi**: kiểm tính hợp lý và việc "không nguồn nào khuyến cáo" của BPaLM (01, cho người kháng FQ), 4RE (03) và TDF + 3TC + NVP (05).
9. Kiểm quần thể trong `population` của từng mẩu so với span (100% mẩu xung đột: 01, 03, 05).

---

## 6. Đề xuất bổ sung configs / mã (chưa sửa — chỉ đề xuất)

**`configs/grading.yaml` → `drugs`** (thiếu nên grader không chấm được nhãn bản cũ, WHO hay mồi của các mẩu này). Mới là bí danh đề xuất; các chữ viết tắt 1–2 ký tự (H, R, Z, E, Am, Cs, Pa) rất dễ khớp nhầm, nên chỉ thêm khi có kiểm thử:
- Lao: `isoniazid: [izoniazid, inh]`, `rifampicin: [rifampin, rif, rmp]`, `pyrazinamide: [pyrazinamid, pza]`, `ethambutol: [emb]`, `rifapentine: [rpt]`, `levofloxacin: [lfx, levofloxacine]`, `clofazimine: [cfz]`, `cycloserine: [cycloserin]`, `delamanid: [dlm]`, `amikacin: [amikacine]`, `ethionamide: [eto]`, `prothionamide: [pto, prothionamid]`; thêm bí danh `bdq` cho bedaquiline, `lzd` cho linezolid, `mfx` cho moxifloxacin (mẩu mẫu "Bdq Lzd Cfz Cs" hiện bị chấm là từ chối).
- HIV: `emtricitabine: [ftc]`, `bictegravir: [bic, biktarvy]`, `nevirapine: [nvp]`, `efavirenz: [efv]`, `lopinavir-ritonavir: [lpv/r]`, `raltegravir: [ral]`, `abacavir: [abc]`, `zidovudine: [azt]`.
- `combos`: thêm `BPaLC: [bedaquiline, pretomanid, linezolid, clofazimine]` (đặt **trước** BPaL), `BDLC: [bedaquiline, delamanid, linezolid, clofazimine]`, `BDLLfxC`. Thứ tự duyệt combos hiện quyết định kết quả gộp.

**Mã (`src/vnsoc/normalize_vi.py`, `src/vnsoc/grade.py`)**:
- `parse_drugs`: bỏ qua chữ số chú thích dính sau chữ viết tắt (ví dụ "DTG1", "TAF2", "TDF3" trong bảng 5968/2021) để lấy lại mẩu HIV bậc một.
- `_gap` cho drugs đang dùng giao tập (có một thuốc chung là gap = 0), trong khi `matches` dùng tập con. Hai định nghĩa không nhất quán nên các phác đồ cùng khung (TDF + DTG và TAF + DTG; HRE và HR) bị xếp "concordant". Đề xuất cho gap = 0 khi một tập key là tập con của tập kia, hoặc ghi rõ quy ước "key_drugs = thuốc phân biệt" vào skill counterpart-matching (quy ước mẩu này đang dùng).
- `vnsoc.match.sources.fetch`: nên đánh dấu lỗi khi nội dung HTML trích được 0 ký tự (trang SPA/reCAPTCHA), để không lưu cache rỗng như với URL handle IRIS.

Đơn vị: không cần thêm (`day`, `month` đã có).

---

## 7. Sau kiểm toán (2026-09-26, agent sửa lỗi)

**Đầu vào:** `data/interim/pilot/tbhiv_verify.md`: pass 2 (06, 07), fix 5 (01–05), reject 0.

**Cách làm:**
- Tôi tự kiểm lại mọi bằng chứng bằng công cụ dự án: `verify_span --page/--find`, `vnsoc.match.sources fetch/grep`, `finalize`, `check_decoy`, `atom_flags`.
- Chỉ ghi 2 file: `tbhiv.jsonl` và file này. Không sửa `configs/`, `src/`, `tests/`.
- Nguồn nước ngoài tải thêm chỉ vào `data/cache/foreign` (qua `sources fetch`), không vào `data/raw`.
- File JSONL dựng bằng script trong scratchpad, ghi bằng công cụ Write. Nội dung trùng từng byte với bản dựng, trừ ký tự xuống dòng (LF thay CRLF).

**Bối cảnh mã thay đổi giữa chừng:** trong lúc tôi làm, `grade.py`, `schemas.py`, `decoys.py` và `atom_flags.py` mới đã đổi (12:32–12:35). Các thay đổi gồm: cờ `derived`, trường `moh_neighbour` và `decoy_rule`, và `check_decoy` nay loại mồi chạm giá trị Bộ Y tế ở bối cảnh lân cận. Mẩu được mã hóa và kiểm theo mã tại 12:35.

### 7.1 Kết quả sau khi sửa

| id | Trước kiểm toán | Sau khi sửa | Thay đổi chính |
|---|---|---|---|
| P-tbhiv-01 | conflict + lệch phiên bản; mồi BPaLM | **conflict** ở phân tích chính; **indistinguishable** ở độ nhạy `with_derived`; `temporal_confounded = true` | Thêm WHO 2020 (BPaL chỉ trong nghiên cứu vận hành + {cycloserine} `derived`); thêm Mỹ ATS/CDC/ERS/IDSA 2025 (BPaL, trùng VN); `moh_neighbour` (BPaLM tr.52; PĐ E tr.56); mồi **BPaLM → BPaMZ**; ghi chú nhiễu nguồn |
| P-tbhiv-02 | concordant + lệch phiên bản | **indistinguishable** | Thêm WHO 2019 {amikacin} |
| P-tbhiv-03 | conflict; nguồn Mỹ = trang CDC không băm | **conflict**; `neighbour_overlap = True` (độ nhạy: indistinguishable) | Mỹ → ATS/CDC/IDSA 2016 + ATS/CDC/ERS/IDSA 2025 (có băm); thêm WHO 2017 {HR, HRE}; `moh_neighbour` trẻ em 4RH; `cat_options` viết lại |
| P-tbhiv-04 | concordant | concordant | `cat_options` đồng bộ với 03; thêm Mỹ 2025 (trẻ em 2HRZE/4HR) |
| P-tbhiv-05 | conflict (chỉ với Mỹ) | conflict (chỉ với Mỹ) | Sửa ghi chú lỗi thời; `decoy_rule` ghi cảnh báo tính hợp lý của NVP |
| P-tbhiv-06 | concordant | không đổi | chỉ thêm `valid_from` |
| P-tbhiv-07 | concordant | không đổi | Ghi câu điều kiện ngay sau span (đã kiểm tr.59); `valid_from` |

**Tổng cộng 7 mẩu, không mẩu nào bị loại:**
- 3 xung đột: 01, 03, 05.
- 3 đối chứng: 04, 06, 07.
- 1 indistinguishable: 02.
- **Không còn mẩu lệch phiên bản sạch nào:** nhãn temporal của 01 bị nhiễu nguồn; 02 indistinguishable.
- Mẩu dùng được cho "H1 bền vững" (N1, không trùng giá trị lân cận): 01 và 05. Mẩu 03 chỉ vào tập chính.

**Thêm cho mọi mẩu:**
- `valid_from`: 162/2024 = `"2024-01"`; 5968/2021 = `"2021-12-31"`. Bằng chứng ghi trong `extraction.valid_from_basis`.
- 162/2024 Điều 3 ghi "có hiệu lực kể từ ngày ký". Lớp chữ để trống ngày, còn dấu văn thư nhận ngày 25/01/2024. Vì vậy chỉ ghi được tháng.
- `decoy_rule` ở cấp trên cùng = `agent_proposed` cho 01, 03, 05 (trường mới, được kiểm lúc đóng băng).

**Kiểm tra trên file cuối:**
- `vnsoc.schemas atom`: OK 7 dòng.
- `vnsoc.extract.verify_span`: OK, 0 mẩu không đạt.
- `finalize()` cho lại đúng `tolerance` và `conflict_status` đã ghi (idempotent).
- `check_decoy()` = [] cho cả 7 mẩu, kể cả luật mới về giá trị lân cận.
- `span_on_page = True` cho 3 span bản cũ (2760/2021 tr.17; 1314/2020 tr.60, tr.59) và 3 span lân cận (162/2024 tr.52: 77 ký tự; tr.56: 595; tr.44: 166).
- Không có trường chỉ-bác-sĩ.
- `atom_flags check` không báo lỗi dữ liệu. Chỉ còn các mục chờ người: `context_checked`, `decoy_plausible`, `moh_scope`, và `conflict_family` phải theo quy tắc cơ học (7.6).

### 7.2 Từng mục kiểm toán: đã sửa, giữ, và lý do

**P-tbhiv-01**

| Mục kiểm toán | Xử lý | Bằng chứng / lý do |
|---|---|---|
| 1. Bộ chấm không đọc "BPaL", "BPaLM", "BDLC", "Bdq Lzd Cfz Cs" | **Đề xuất cấu hình + mã** (7.5). Giữ key hiện có. | Tái hiện được: "ĐÁP ÁN: BPaL" → 6; "Bdq Lzd Cfz Cs + 1 thuốc nhóm C" → 5. Với cấu hình đề xuất: 2 và 3. Nếu thêm combo BDLC vào `grading.yaml`, **phải** đổi key BDLC của mẩu thành `["BDLC"]` (đã ghi trong notes). |
| 2(a) PĐ E hiện hành cho quần thể kề bên | **Đã sửa:** ghi vào notes, `temporal_confounders` và `moh_neighbour` | 162/2024 tr.56: đối tượng "Người bệnh kháng FQ không đủ tiêu chuẩn thu nhận phác đồ BpaL" … "PĐ E: Bdq Lzd Cfz Cs +1 thuốc nhóm C". Cùng trang: "…theo khuyến cáo cập nhật của WHO". |
| 2(b) WHO 2020: phác đồ dài hạn suy ra Bdq Lzd Cfz Cs | **Đã sửa bằng cơ chế `derived`** (thay vì chọn (i), (ii) hay (iii)) | WHO 2020 (IRIS 10665/332397, 2020-06-15, sha `133ba15f…`):<br>- tr.17 và tr.60: BPaL "under operational research conditions".<br>- tr.15 và tr.40: "if only one or two Group A agents are used, both Group B agents are to be included".<br>- tr.40: danh sách nhóm A và B.<br>Ghi bản ghi WHO_global 2020 gồm {BPaL} (nguyên văn) và {cycloserine, `derived: true`}. Kết quả: `finalize` = conflict; `conflict_status(with_derived(atom))` = indistinguishable. Cơ chế này được đăng ký trước (review/prereg/rev-clinician.md id 9; `atom_flags.with_derived`). |
| 2(c) Hiệu lực 2760/2021 chỉ là suy luận | **Giữ `superseded`**, ghi rõ | 162/2024 tr.1 Điều 3 chỉ thay 1314/2020; tr.201 dẫn "QĐ 2760 của BYT". Chạy thử coi 2760/2021 còn hiệu lực (DR8) vẫn cho **conflict**. Bản cũ 1314/2020 (bị thay rõ ràng) cho cùng giá trị. |
| 3. Mồi BPaLM | **Thay bằng BPaMZ** | Khi ghi `moh_neighbour`, `check_decoy` mới trả về "mồi BPaLM chạm giá trị Bộ Y tế ở bối cảnh lân cận" (đã chạy). Review id 1 nêu đúng trường hợp này.<br>BPaMZ không có trong 162/2024 (`--find` = []). WHO 2022 = 0. ATS 2025 = 0. WHO 2026 chỉ nhắc tên ở tr.357 (phần khai báo lợi ích), không khuyến cáo.<br>Key {pretomanid, moxifloxacin, pyrazinamide} tách được khỏi BPaL, BPaLM, BDLC và E1 (đã thử). |
| Đề xuất (ii): tách 01a/01b | **Không tách** | Hai mẩu sẽ cùng câu hỏi và cùng quần thể, tức đếm đôi. Cờ `derived` và `temporal_confounded` cho cùng tác dụng phân tích. |
| 4. Span tr.53 đạt nhờ tiêu chí tiền sử | Ghi vào notes | Dòng thành phần "6-9 BpaL (bedaquiline, pretomanid, linezolid)" nằm ở tr.54 (đã đọc). |
| Thêm (ngoài kiểm toán) | Nguồn Mỹ ATS/CDC/ERS/IDSA 2025 | PMC11755361, sha `43ce9bbd…`. PICO 3: "6-month BPaL" cho người ≥ 14 tuổi, lao phổi kháng R và kháng FQ (strong). **Trùng** Việt Nam. |
| Thêm | WHO 2026 B1.2 "BDLLfx/C … with or without fluoroquinolone resistance" | Đã nằm trong key BDLC, vì {delamanid, clofazimine} ⊆ BDLLfxC. Đã cập nhật locator. |

**P-tbhiv-02**

| Mục | Xử lý | Bằng chứng / lý do |
|---|---|---|
| 1. Giá trị bản cũ trùng WHO 2019 | **Đã sửa:** thêm WHO_global 2019 {amikacin} → **indistinguishable** | Đã tự kiểm (sha `df14ea4b…`, IRIS 10665/311389, 2019-03-20):<br>- tr.37: "a shorter MDR-TB regimen of 9-12 months may be used";<br>- tr.41: 4-6Km-Mfx-Cfz-Eto-Z-E-Hh/5Mfx-Cfz-Z-E;<br>- tr.42: "kanamycin be replaced by amikacin".<br>WHO 2020 (rec 2.1, tr.15/tr.31) đã chuyển sang phác đồ toàn uống có bedaquiline. Vậy WHO 2019 là **bản WHO gần nhất có giá trị khác** bản hiện hành (§3.3). |
| 2. Bộ chấm | Đề xuất (7.5) | — |
| 3. Khóa một thuốc | Ghi yêu cầu QC câu hỏi vào notes | — |
| 4. `conflict_family` gây hiểu nhầm | **Giữ**, có giải thích | Nhãn chỉ khác biệt gốc giữa các phiên bản. Mẩu không vào H1 nên không ảnh hưởng quy tắc họ cơ học. |
| **Phát hiện mới** | Lỗi `grade.py` bị kích hoạt | Có thêm WHO 2019 thì **câu trả lời đúng có bedaquiline bị chấm 5** (xem 7.3 mục 1). |

**P-tbhiv-03**

| Mục | Xử lý | Bằng chứng / lý do |
|---|---|---|
| 1. Nguồn Mỹ không băm mà `verified_by: "auto"` | **Đã sửa:** bỏ bản ghi trang CDC; thay bằng 2 nguồn có băm | - ATS/CDC/IDSA 2016 (cdc.gov, sha `86123eb8…`): tr.4 "continuation phase of 4 months of INH and RIF"; Bảng 2 "126 doses (18 wk)".<br>- ATS/CDC/ERS/IDSA 2025 (sha `43ce9bbd…`): phác đồ chuẩn 6 tháng vẫn là "2HRZE/4HR endorsed by the ATS/CDC/ERS/IDSA guidelines". |
| 2. WHO 2010 Rec 3 (HRE ở giai đoạn duy trì) | **Đã sửa:** ghi **WHO 2017** vào foreign, values {HR, HRE} | WHO 2017 (IRIS 10665/255052, 2017-04-24, sha `a7921931…`, 80 tr.): tr.17 2HRZE/4HR "remains valid"; tr.19 HRE "acceptable alternative" ở quần thể có (nghi) tỷ lệ kháng isoniazid cao, "remains valid".<br>WHO 2022 DS-TB tr.53 và WHO 2026 tr.284 ghi "Redundant". Như vậy 2017 là bản WHO trước có giá trị khác.<br>`finalize` vẫn = conflict. |
| 3. `cat_options` bỏ sót nhiều cách viết | **Viết lại, thử 48 câu mẫu** (7.4) | Không dùng chữ thoát viết hoa (`\W`, `\S`…), vì `parse_cats` hạ chữ thường cả mẫu: `\W` sẽ thành `\w`. Mẫu gợi ý của kiểm toán dùng `^\W*` nên sẽ hỏng. |
| 4. Câu rào đón "4RHE hoặc 4RH" → correct | Mức mã; đề xuất tách mỗi nhãn thành một giá trị (7.5) | Đã thử: với bản vá, câu này chấm 5 (đúng ý kiểm toán). |
| 5. Ghi chú "_gap giao tập" lỗi thời | **Đã sửa** | Lý do dùng `cat`: `matches()` so tập con. |
| Thêm | 4263/2015 tr.49: IA 2RHZE(S)/4RHE người lớn; IB 2RHZE/4RH trẻ em | Không lệch phiên bản từ 2015 (03 và 04). |
| Thêm (kiểm toán chưa nêu) | `moh_neighbour` = trẻ em 4RH (tr.44) | Giá trị lân cận này **trùng** HR của WHO và Mỹ, nên `neighbour_overlap = True`. Mẩu bị loại khỏi N1; `status_with_neighbours` = indistinguishable (độ nhạy). Câu hỏi phải nói rõ "người lớn". |
| EU_UK | Chưa ghi | NICE NG33: nice.org.uk trả HTTP 403 (trang và PDF). |

**P-tbhiv-04:**
- `cat_options` giống hệt 03, để so sánh cặp không lệch.
- Thêm Mỹ 2025 (PICO 2): trẻ không đủ tiêu chuẩn lao không nặng dùng 2HRZE/4HR.
- Ghi yêu cầu câu hỏi: nêu "phác đồ 6 tháng", hoặc trẻ không đủ tiêu chí A2a.

**P-tbhiv-05:**
- Bỏ câu "grader coi DTG + TAF là trùng" (lỗi thời). Đã chạy lại: "DTG + TAF + FTC" → foreign US.
- Không đổi key: quy trình yêu cầu dùng INN chữ thường khi thuốc chưa có trong cấu hình.
- Mồi NVP vẫn hợp lệ theo quy tắc. Tr.29: PEP trẻ ≤ 10 tuổi không có NVP, nên mồi không chạm giá trị lân cận. Tuy vậy review id 4 nghi mồi này kém hợp lý; đã ghi vào `decoy_rule`, chờ chấm ở HG3.5.

### 7.3 Phát hiện mới khi tự kiểm lại

1. **Lỗi `grade.py`: xét "xung đột" theo tên hệ thống, không theo từng giá trị** (nhánh drugs, `grade_short`). Nếu một hệ thống có một bản ghi trùng Việt Nam (WHO 2026 {bedaquiline}) và một bản ghi xung đột (WHO 2019 {amikacin}), thì mọi câu trả lời đúng có bedaquiline đều khớp "WHO_global", bị coi là trộn với giá trị xung đột và chấm **5**.
   - Tái hiện: P-tbhiv-02, "ĐÁP ÁN: bedaquiline, levofloxacin, prothionamide, …" → 5, trong khi phải là 2.
   - Cùng lỗi theo chiều ngược lại: câu rào đón "BPaL hoặc BDLC" (01) và "TDF + 3TC + DTG hoặc TAF + FTC + DTG" (05) → **2**, trong khi phải là 5. Lý do: bản ghi WHO 2026 và bản ghi CDC đều có một giá trị trùng Việt Nam, nên không bị coi là "xung đột".
   - Mọi mẩu drugs có nhiều phiên bản cùng hệ thống đều có thể dính lỗi này, không riêng tbhiv.
2. **Bản ghi chỉ gồm giá trị `derived`:**
   - Trong `grade_short`, `all(... for it in f["values"] if not it.get("derived"))` trên một danh sách rỗng trả về True, nên bản ghi bị coi là "xung đột".
   - Nếu tôi chỉ ghi WHO 2020 {cycloserine, derived}, câu trả lời đúng "BPaL" của 01 sẽ bị chấm 5 do lỗi (1).
   - Bản ghi WHO 2020 hiện có thêm giá trị nguyên văn {BPaL} (rec 4.1). Giá trị này là thật và đúng quần thể, nên bản ghi không chỉ gồm `derived` và không kích hoạt lỗi. Tôi vẫn báo lỗi này để sửa mã.
3. **Giá trị lân cận ở 03** (trẻ em 4RH trùng HR của WHO/Mỹ): xem 7.2. Kiểm toán và báo cáo gốc đều chưa nêu. Đây là đúng loại lỗi quy nguồn mà review id 1 mô tả.
4. **Nguồn Mỹ 2025 cho lao** (ATS/CDC/ERS/IDSA, AJRCCM 2025;211(1):15–33):
   - Mẩu 01: BPaL (trùng Việt Nam).
   - Mẩu 03/04: 2HRZE/4HR (không đổi).
   - Mẩu 02: không có khuyến cáo cho phác đồ 9 tháng ("several newer regimens were out of scope"), nên không có đối chiếu Mỹ.
5. **Chỉ mục cache `data/cache/foreign/index.json` bị mất mục:**
   - File `d179d1244868d020b71e.pdf` (WHO 2022 DS-TB) và `f81e9281d2669bd035cc.pdf` (WHO 2025) vẫn còn trong cache nhưng không có dòng trong `index.json`. Nhiều khả năng do nhiều agent ghi cùng lúc.
   - Tôi đọc trực tiếp file PDF (sha256 tính lại khớp `d179d124…`).
   - Đề xuất: khóa file, hoặc ghi nguyên tử theo kiểu `fetch_pdf`.
6. **Đối chứng hạt giống "HIV bậc một TDF + 3TC + DTG" vẫn chưa dựng**, vì hai lý do:
   - (a) Quy tắc "ghi mọi hệ thống" cần hướng dẫn Mỹ DHHS, nhưng clinicalinfo.hiv.gov trả HTTP 403 với công cụ sources.
   - (b) Nếu nguồn nước ngoài có phác đồ hai thuốc (ví dụ DTG/3TC), `key_drugs` không mã hóa được. Luật tập con làm {dolutegravir, lamivudine} ⊆ đáp án ba thuốc của Việt Nam, nên đáp án đúng sẽ bị coi là trộn giá trị xung đột. Muốn dựng phải dùng `cat`.
   - Việc hạt giống xếp dòng này là "đối chứng" **chưa kiểm được** (cần đọc DHHS/EACS). Đề xuất để thành task riêng.
7. **Hiệu lực tại ngày đóng băng: chưa kiểm được.**
   - WebSearch của phiên đã hết hạn mức (200/200).
   - kcb.vn/phac-do (trang đầu) không có văn bản lao/HIV nào mới.
   - Việc có văn bản thay 162/2024 hoặc 5968/2021 hay không vẫn để HG1.2.

### 7.4 Kiểm thử bộ chấm bằng câu trả lời mẫu (131 câu)

**Bộ câu:**
- 01: 14 câu; 02: 8 câu; 05: 13 câu; 03 và 04: 48 câu mỗi mẩu.
- Dạng câu: tên tổ hợp, viết tắt theo văn bản, INN đầy đủ, tiếng Việt và tiếng Anh, "4(HR)3", phủ định "không cần ethambutol", câu dài không có dòng ĐÁP ÁN, câu rào đón, câu biết bối cảnh.

**Số câu chấm sai nhãn kỳ vọng:**

| Bộ chấm | grading.yaml | Sai / 131 | Còn lại |
|---|---|---|---|
| `grade.py` hiện hành | hiện hành | 23 | 01: 7, 02: 6, 05: 7 (tên tổ hợp/viết tắt); 03/04: câu rào đón |
| `grade.py` hiện hành | đề xuất (7.5) | 9 | lỗi (1) của 7.3 ở 02; câu rào đón 01/05/03/04 |
| + vá "xung đột theo từng giá trị" | đề xuất | 3 | "Am" (02); câu rào đón cat ở 04 |
| + vá "mỗi nhãn cat là một giá trị" | đề xuất | **1** | "4-6 Am Lfx Pto…": "Am" cố ý chưa thêm vì quá mơ hồ |

**Một số câu tiêu biểu** (sau khi vá mã và thêm cấu hình):

| Mẩu | Câu | Nhãn |
|---|---|---|
| 01 | "BPaL" | 2 |
| 01 | "BDLC" | 4 WHO |
| 01 | "Bdq Lzd Cfz Cs + 1 thuốc nhóm C" | 3 |
| 01 | "BPaMZ" | 5 + mồi |
| 01 | "BPaL hoặc BDLC" | 5 |
| 02 | "4-6 Bdq-Lfx-Pto-E-Z-Hh-Cfz…" | 2 |
| 02 | "amikacin, levofloxacin, …" | 3 (mẩu indistinguishable) |
| 03 | "R, H, E" / "RHE" / "rifampicin, isoniazid và ethambutol" | 2 |
| 03 | "HR" / "RH" / "rifampicin và isoniazid, không cần ethambutol" / "2HRZE/4(HR)3" | 4 (US + WHO) |
| 03 | "RE" | 5 + mồi |
| 03 | "R, H, Z, E" | 6 |
| 03 | "72 hrs" | 6 |
| 05 | "TLD" / "tenofovir + lamivudine + dolutegravir" | 2 |
| 05 | "BIC/FTC/TAF" / "Biktarvy" | 4 US |
| 05 | "TDF + 3TC + NVP" | 5 + mồi |

Với `grade.py` hiện hành, `cat_options` mới của 03 đúng 47/48 câu và của 04 đúng 46/48 câu. Các câu sai đều là câu có hai nhãn trong một câu trả lời (sai do mã, không do mẫu):
- câu rào đón "4RHE hoặc 4RH" (cả hai mẩu);
- ở 04: "2HRZE/4RHE (Việt Nam), trong khi WHO…" được chấm 1, trong khi đúng phải là 5 (với trẻ em, HRE không phải giá trị Bộ Y tế). Script thử nằm trong scratchpad của phiên (`tbhiv_fix_probe.py`, `make_grade_patched.py`). Đề xuất chuyển bộ câu này thành test trong `tests/`.

### 7.5 Đề xuất cấu hình và mã (chưa sửa; đã thử bằng bản vá trong scratchpad)

**`configs/grading.yaml` → `drugs`** (bổ sung; tăng `grader_version`):
```yaml
bedaquiline: [bedaquilin, bdq]
linezolid: [lzd]
cycloserine: [cycloserin, cs]
moxifloxacin: [moxifloxacine, mfx]
amikacin: [amikacine]
kanamycin: [kanamycine]
prothionamide: [prothionamid, pto]
ethionamide: [ethionamid, eto]
bictegravir: [bic]
nevirapine: [nvp, nevirapin]
raltegravir: [ral]
lopinavir-ritonavir: [lpv/r, lpv-r]
zidovudine: [azt, zdv]
abacavir: [abc]
tenofovir-alafenamide: [taf, tenofovir alafenamide]
tenofovir-disoproxil: [tdf, tenofovir disoproxil fumarate, tenofovir disoproxil, tenofovir]
```

Ghi chú cho danh sách trên:
- Chữ "tenofovir" đứng riêng được quy về TDF theo một quyết định đăng ký trước. Bí danh dài hơn được khớp trước, nên "tenofovir alafenamide" không bị ảnh hưởng.
- Chưa thêm "am"/"km" (quá mơ hồ). Nếu cần, chỉ nhận trong ngữ cảnh chuỗi thuốc và phải kèm test.

**Cơ chế mới: bí danh tên tổ hợp → các thuốc thành phần** (mở rộng trước khi gộp combo):
- `bpal`, `bpalm`, `bpalc`, `bpamz`, `bdlc` → danh sách INN thành phần.
- `tld` → TDF + 3TC + DTG.
- `biktarvy` → BIC + FTC + TAF.

Không nên thêm `BDLC` thành combo. Làm vậy sẽ xóa delamanid/clofazimine khỏi tập đã tách và phá key của 01. Nếu vẫn thêm, phải đổi key cùng lúc.

**`src/vnsoc/grade.py`** (3 chỗ; đã thử toàn bộ 131 câu):
1. `classify_value`: thêm `r["conflict"]` = câu trả lời khớp **một giá trị** nước ngoài xung đột (không phải `derived`, và gap > 0 với mọi giá trị Việt Nam).
2. Nhánh "một danh sách chứa cả giá trị Bộ Y tế lẫn giá trị nước ngoài": điều kiện đổi thành `c["vn"] and c["conflict"]` thay cho so tên hệ thống. Áp dụng cho cả kiểu `cat`. Trong `_attribution_aware`, `foreign_hit(c)` dùng `c["conflict"]`.
   - Việc này sửa đồng thời lỗi 7.3(1) và lỗi 7.3(2).
3. `parse_values` với `cat`: trả về **mỗi nhãn là một giá trị**. Khi đó câu rào đón "4RHE hoặc 4RH" đi vào nhánh nhiều giá trị (nhãn 5, hoặc nhãn 1 nếu có quy nguồn rõ).
   - Đây cũng là đề xuất 2.3 của kiểm toán. Thay đổi này ảnh hưởng mọi chủ đề có mẩu `cat`.

### 7.6 Tồn đọng cho HG1.2 / HG3.x

1. **P-tbhiv-01:**
   - Xác nhận cách mã hóa: conflict ở phân tích chính, indistinguishable ở độ nhạy `with_derived`. Hai phương án khác: bỏ `superseded`, hoặc bỏ cờ `derived`.
   - Chấm `decoy_plausible` cho BPaMZ (HG3.5). Nếu không đạt thì sinh lại theo quy tắc định trước.
   - Xác nhận danh tính và hiệu lực của 2760/2021.
2. **P-tbhiv-02:** chấp nhận indistinguishable, tức không dùng cho kiểm định xác nhận. Chỉ chấm được đúng sau khi sửa 7.5 (`grade.py`).
3. **P-tbhiv-03:**
   - Câu hỏi phải nói rõ "người lớn" (vì có giá trị lân cận trẻ em).
   - Bác sĩ gán `moh_lags_evidence`, lưu ý: HRE là phương án có điều kiện của WHO 2017, nay "Redundant".
   - Chấm `decoy_plausible` cho mồi 4RE.
   - Kiểm EU_UK (NICE NG33) bằng tay, vì công cụ bị chặn HTTP 403.
4. **P-tbhiv-05:** chấm `decoy_plausible` cho NVP (review id 4). Tải 5456/2019 tay (vaac.gov.vn lỗi TLS) nếu muốn có nhãn temporal.
5. **`moh_scope`** (kiểm ngữ cảnh). Đề xuất của agent, cần người xác nhận:
   - 05 = `preferred` (văn bản ghi "Ưu tiên").
   - 03 = `exhaustive` (A1 là phác đồ 6 tháng duy nhất cho người lớn).
   - 01 = `exhaustive` hay `preferred`: cần người quyết. Review id 10 xếp BDLC là "Bộ Y tế không nhắc".
6. **`conflict_family` theo quy tắc cơ học** (`atom_flags.family_id`): 01 = `fam_08c6559c6e`, 03 = `fam_dac12b051f`, 05 = `fam_dd4487cded`. Lúc đóng băng phải thay tên đọc được; mã họ sẽ đổi nếu mẩu đổi.
7. **Văn bản:**
   - Ngày ký chính xác và số hiệu của 162/2024 (lớp chữ để trống).
   - Hiệu lực của 162/2024 và 5968/2021 tại 15/10/2026 (chưa kiểm được, xem 7.3 mục 7).
8. **Mã và cấu hình (người giữ `configs`/`src`):** áp dụng 7.5, thêm test từ bộ 131 câu, tăng `grader_version`, rồi chấm lại.

### 7.7 Nguồn đã mở thêm trong lượt sửa (chỉ lưu giá trị + vị trí + băm)

| Nguồn | Phiên bản | URL | sha256 (16) | Ghi chú |
|---|---|---|---|---|
| WHO Guidelines for treatment of drug-susceptible TB and patient care, 2017 update (IRIS 10665/255052) | 2017-04-24 | iris.who.int/server/api/core/bitstreams/b4d54e27-…/content | a7921931d9a20469 | 80 tr.; mới tải |
| ATS/CDC/ERS/IDSA Updates on the Treatment of DS- and DR-TB (PMC11755361) | 2025-01-01 | eutils efetch db=pmc id=11755361 | 43ce9bbd29d03956 | XML toàn văn; mới tải |
| WHO consolidated guidelines on DR-TB treatment (IRIS 10665/311389) | 2019-03-20 | …/bitstreams/30d89c8e-…/content | df14ea4b23abee1c | 104 tr.; tải lại từ cache của kiểm toán |
| WHO Module 4 DR-TB (IRIS 10665/332397) | 2020-06-15 | …/bitstreams/56364485-…/content | 133ba15f96e70420 | 120 tr.; cache kiểm toán |
| ATS/CDC/IDSA 2016 DS-TB (cdc.gov) | 2016-08-10 | cdc.gov/tb/publications/guidelines/pdf/clin-infect-dis.-2016-nahid-cid_ciw376.pdf | 86123eb8f815f62c | 49 tr.; cache kiểm toán |

- Ngày phát hành của WHO 2019/2020 lấy từ API DSpace của IRIS.
- Không dùng được: NICE NG33 (HTTP 403), clinicalinfo.hiv.gov DHHS (HTTP 403), WebSearch (hết hạn mức).
- Văn bản Bộ Y tế đọc thêm (đã có sẵn trong `data/raw`, không tải mới): 4263/2015 tr.49–50; 162/2024 tr.1, 44, 52–54, 56, 59, 64, 201; 5968/2021 tr.29.
