# T1.1 thí điểm — Tăng huyết áp (ID = htn)

Agent: atom-extractor + counterpart-matcher (Claude), ngày 2026-09-26.

> **CẬP NHẬT SAU KIỂM TOÁN (2026-09-26), xem §7, là trạng thái hiện hành.**
> - `htn.jsonl` còn **3 mẩu**: **2 xung đột** (P-htn-01, P-htn-03, cả hai với US 2025), **1 đối chứng** (P-htn-04), 0 lệch phiên bản.
> - **P-htn-02 bị loại** (§3 mục 8).
> - Kiểm tra: `vnsoc.schemas atom` OK 3/3; `vnsoc.extract.verify_span` OK 3/3; `finalize()` tính lại khớp giá trị đã lưu; `check_decoy()` = [].
> - §1–§6 dưới đây là báo cáo gốc (trước kiểm toán). Chỗ nào đã lỗi thời thì có đánh dấu **[đã sửa, §7]**.

Báo cáo gốc: **4 mẩu**, gồm 3 xung đột (P-htn-01, 02, 03) và 1 đối chứng (P-htn-04).
Kiểm tra lúc đó: schemas OK 4/4; verify_span OK 4/4; `check_decoy()` = [] cho cả 4 mẩu.

Ba điểm cần người quyết trước khi dùng (chi tiết ở §5):
1. **Khóa văn bản 5904/2019.** Cả 4 mẩu đang dùng khóa biến thể `5904/2019__9e6bbe13`. Lý do: file chuẩn `data/raw/5904_2019.pdf` là bản scan, không có lớp chữ.
2. **Bộ chấm bỏ qua dấu so sánh `<`.** Hệ quả là giá trị Mỹ "< 130" ở P-htn-02 bị coi là không xung đột, và câu trả lời "< 130 mmHg" bị chấm là đúng theo Bộ Y tế.
3. **Toàn văn AHA/ACC 2025 bị chặn (403).** Giá trị Mỹ lấy từ hai trang tóm tắt chính thức của AHA và ACC.

---

## 1. Văn bản đã tìm / tải

### 1a. Văn bản Việt Nam (tải qua `vnsoc.extract.fetch_pdf`)

| Khóa / file | Văn bản | URL | sha256 (16) | Trang | text_kind | Dùng để |
|---|---|---|---|---|---|---|
| 3192/2010 → `3192_2010.pdf` | Hướng dẫn chẩn đoán và điều trị THA (ban hành kèm QĐ 3192/QĐ-BYT ngày 31/08/2010) | https://kcb.vn/upload/2005611/20210723/huong_dan_chan_doan_dieu_tri_tha.pdf | b4b84c7307c69b5a | 19 | ok | span phụ (P-htn-01) và span hợp theo DR8 (P-htn-02, 04) |
| 5904/2019 → `5904_2019.pdf` (file chuẩn) | QĐ 5904/QĐ-BYT ngày 20/12/2019. Bản scan có chữ ký số (KT. Bộ trưởng, Thứ trưởng Nguyễn Trường Sơn) + trang in 1–12 của tài liệu | https://benhvienquynhon.gov.vn/wp-content/uploads/2023/05/copy-of-9-qdb-2019-5904-1.pdf | 7cb7cd93fd30cf64 | 22 | **scanned_or_empty** | chỉ để đối chiếu bằng mắt (không kiểm span được) |
| 5904/2019 → `5904_2019__9e6bbe13.pdf` (status `clash_kept_both`) | Toàn văn tài liệu "Hướng dẫn chẩn đoán, điều trị và quản lý một số bệnh không lây nhiễm tại trạm y tế xã" (tr.2: "Ban hành kèm theo Quyết định số 5904/QĐ-BYT ngày 20 tháng 12 năm 2019"), không kèm trang quyết định | https://benhvienhatrung.vn/wp-content/uploads/2022/06/5904-2019-HDDT-quan-ly-Benh-K-lay-tai-xa.pdf | 9e6bbe13d5705fc8 | 68 | ok | **span chính của cả 4 mẩu** |

Nơi đã tìm:
- **3192/2010:** trang https://kcb.vn/phac-do/huong-dan-chan-doan-va-dieu-tri-tang-huyet-ap.html ghi rõ QĐ 3192/QĐ-BYT ngày 31/08/2010 và trỏ tới PDF trên. PDF chỉ có phần hướng dẫn, không có trang quyết định.
- **5904/2019:**
  - Trang kcb.vn/vanban của 5904 trả 404.
  - Trang vncdc.gov.vn (nd14992) không có link file. Trang này còn chứa **liên kết spam tới shop bán tài khoản game**, có thể đã bị chèn mã, nên không tải gì từ đó.
  - Trang daithaoduong.kcb.vn không có file.
  - Tìm được 2 bản đăng lại của cơ sở y tế: TTYT Quy Nhơn (gov.vn, bản scan có chữ ký) và BVĐK Hà Trung (bản có lớp chữ).
  - **Đối chiếu bằng mắt:** trang scan 12–14 (= trang in 2–4) khớp nguyên văn với trang 11–13 của bản có lớp chữ, gồm câu đối tượng áp dụng, mục tiêu HA và thời điểm khởi trị.
- **Có hướng dẫn THA mới hơn của Bộ Y tế không?** Đã tìm trên kcb.vn và moh.gov.vn, xem trang 1 của kcb.vn/phac-do, và tìm "Bộ Y tế … tăng huyết áp 2024/2025/2026". Không thấy văn bản Bộ Y tế nào thay 3192/2010. "Khuyến cáo 2024" là của Hội Tim mạch/VSH–VNHA (hội chuyên ngành, không phải Bộ Y tế), nên không đưa vào kho.
  - **Giới hạn:** chỉ xem trang 1 của danh mục kcb.vn/phac-do, và ngân sách WebSearch của phiên (200 lượt) đã hết, nên cần người kiểm lại (§5).
- **5481/2020 (ĐTĐ)** có mục tiêu HA riêng cho người ĐTĐ. Mọi mẩu ở đây ghi quần thể "không ĐTĐ" nên không cần hợp với 5481.
- **Bản Bộ Y tế cũ bị thay:** không tìm được văn bản THA nào bị 3192/2010 hay 5904/2019 thay thế, nên không có mẩu lệch phiên bản.
  - **[đã sửa, §7.6]** Câu này sai. Theo manifest (`c3_ncd`), Điều 3 của 5904/2019 bãi bỏ Phần 2 ("bệnh mạn tính", có THA) của **2919/2014**. Agent sửa đã đọc 2919 tr.53–58. Giá trị trùng văn bản hiện hành, nên vẫn không có mẩu lệch phiên bản.

### 1b. Nguồn nước ngoài (tải bằng `vnsoc.match.sources`; chỉ lưu giá trị, vị trí và băm)

| Hệ thống | Nguồn (phiên bản) | URL đã tải | sha256 (16) | Ghi chú |
|---|---|---|---|---|
| WHO_global | WHO 2021 Guideline for the pharmacological treatment of hypertension in adults (IRIS, phát hành 2021-08-24) | https://iris.who.int/server/api/core/bitstreams/f062769d-f075-4a00-87af-0a2106e0bd04/content | 57f6376d5c9bc4ea | PDF 61 trang. Link dạng `/bitstream/handle/10665/344424/...pdf` chỉ trả về vỏ trang Angular (DSpace 7), nên phải lấy uuid qua API `/server/api/pid/find`. PDF tr.14 nói guideline **không** đề cập chẩn đoán THA |
| WHO_global | WHO Fact sheet "Hypertension" (25/9/2025) | https://www.who.int/news-room/fact-sheets/detail/hypertension | 2779af89d3929cb2 | định nghĩa chẩn đoán ≥ 140 và/hoặc ≥ 90 đo ở 2 ngày khác nhau |
| EU_UK | 2024 ESC Guidelines, elevated BP and hypertension: **bộ slide chính thức của ESC** (pptx, lấy từ trang escardio.org của guideline) | https://yjxzhi.files.cmp.optimizely.com/download/033b7456bfae11f0940e9af5f85eac06 | c006bbb57dbbee77 | Slide là ảnh EMF. Chữ lấy từ bản ghi văn bản trong EMF, và **đã xem bằng mắt** slide 31, 32, 53, 92, 93, 99. Toàn văn OUP bị 403 với `requests`; WebFetch chỉ ra phần tóm tắt, và phần đó khớp |
| EU_UK | 2018 ESC/ESH (giá trị như được trích trong cột "2018 Guidelines" của slide ESC 2024 "Revised recommendations" 11 và 12) | như trên | c006bbb57dbbee77 | Toàn văn 2018 (OUP) không đọc được |
| US | 2025 AHA/ACC/multisociety High BP Guideline: thông cáo chính thức AHA (14/8/2025) | https://newsroom.heart.org/news/new-high-blood-pressure-guideline-emphasizes-prevention-early-treatment-to-reduce-cvd-risk | bbc83c2a1e37a919 | phân loại HA "giữ nguyên như 2017", THA ≥ 130/80 |
| US | 2025 AHA/ACC: bài "New in Clinical Guidance – Key Points" của ACC (1/10/2025) | https://www.acc.org/latest-in-cardiology/articles/2025/10/01/01/new-in-clinical-guidance-hbp | aea4b0989dd4ab54 | "overarching BP treatment goal is <130/80 mm Hg for all adults"; khởi trị ≥ 130/80 cho người nguy cơ thấp sau 3–6 tháng thay đổi lối sống |

**Bị chặn:**
- ahajournals.org (Circulation, Hypertension; HTML và PDF), jacc.org, professional.heart.org (trang hub, infographic, bản tóm tắt cho người bệnh): đều 403, cả qua `requests` lẫn WebFetch.
- Europe PMC báo cả 3 DOI của AHA/ACC 2025 và ESC 2024/2018 đều không có trong PMC.
- NCBI Bookshelf NBK573631 trả về trang reCAPTCHA.

Vì vậy giá trị Mỹ đang dựa vào 2 trang tóm tắt chính thức của AHA và ACC (có băm). Số mục và bảng trong toàn văn **cần người kiểm**.

---

## 2. Bảng mẩu

**[đã sửa, §7.4]** Bảng và kết quả chấm thử dưới đây là trạng thái TRƯỚC kiểm toán.

| id | Slot | Quần thể (rút gọn) | VN (tập giá trị) | Nước ngoài (hệ thống: giá trị, phiên bản) | Trạng thái (finalize) | Trang PDF (in) | Hạt giống |
|---|---|---|---|---|---|---|---|
| P-htn-01 | threshold: ngưỡng chẩn đoán, **HA đo tại phòng khám** | ≥ 18 tuổi, không mang thai | ≥ 140/90 (5904 tr.11; trùng 3192 tr.1) | US: ≥ 130/80 (AHA/ACC 2025) ✗ · EU_UK: ≥ 140/90 (ESC 2024, slide 53) ✓ · WHO: ≥ 140/90 (fact sheet 2025) ✓ | **conflict** (chỉ với US); mồi 150/100; dung sai 5 | 11 (in 2) | dòng 6 |
| P-htn-02 | target: HA tâm thu mục tiêu khi điều trị | 65–79 tuổi, không suy yếu, không ĐTĐ/bệnh thận mạn/bệnh tim mạch, nguy cơ không cao | {130 đến < 140} (5904) ∪ {< 140} (3192, DR8) | EU_UK: 120–129 (ESC 2024) ✗ · EU_UK: 130–139 (ESC/ESH 2018) ✓ · US: < 130 (AHA/ACC 2025), trùng cận dưới nên công cụ coi là không xung đột · WHO: < 140 (WHO 2021) ✓ | **conflict** (chỉ với ESC 2024); mồi 141–150; dung sai 0,5 | 12 (in 3) | dòng 7 |
| P-htn-03 | threshold: ngưỡng HA bắt đầu dùng thuốc | 18–79 tuổi, nguy cơ 10 năm < 5%, không bệnh đồng mắc, đã thay đổi lối sống 3–6 tháng, đo tại phòng khám | ≥ 140/90 (5904 tr.13) | US: ≥ 130/80 (AHA/ACC 2025) ✗ · EU_UK: ≥ 140/90 (ESC 2024, slide 92) ✓ · WHO: ≥ 140/90 (WHO 2021 KN 1) ✓ | **conflict** (chỉ với US); mồi 150/100; dung sai 5 | 13 (in 4) | — (mẩu thêm) |
| P-htn-04 | target: HA tâm thu mục tiêu khi điều trị | 18–64 tuổi, không ĐTĐ/bệnh thận mạn/bệnh tim mạch, nguy cơ không cao | {120 đến < 130} (5904) ∪ {< 140} (3192, DR8) | EU_UK: 120–129 (2024) ✓ · EU_UK: < 140 và ≤ 130 (2018) ✓ · US: < 130 ✓ · WHO: < 140 ✓ | **concordant**; không có mồi | 12 (in 3) | — (đối chứng) |

`conflict_family`:
- `htn_us_130_80` (P-htn-01 và 03): cùng một khác biệt gốc, là việc Mỹ hạ ngưỡng xuống 130/80 từ 2017.
- `htn_target_older_esc2024_120_129` (P-htn-02).

**Chạy thử bộ chấm hiện hành** (`vnsoc.grade.grade_short`, chỉ đọc) trên vài câu trả lời mẫu:

| Mẩu | Câu trả lời | Nhãn |
|---|---|---|
| 01 | ≥ 140/90 | 2 đúng |
| 01 | ≥ 130/80 | 4 nước ngoài (US) |
| 01 | 150/100 | 5 (trúng mồi) |
| 02 | 130–139 | 2 đúng |
| 02 | 130–140 | 2 đúng |
| 02 | < 140 | 2 đúng |
| 02 | 120–129 | 4 nước ngoài (EU_UK) |
| 02 | **< 130** | **2 đúng** ⚠ (lẽ ra phải quy về US) |
| 02 | < 150 | 5 (trúng mồi) |
| 03 | ≥ 130/80 | 4 nước ngoài (US) |
| 04 | **< 120** | **2 đúng** ⚠ (cùng lỗi ở cận dưới) |

---

## 3. Ứng viên bị loại và lý do

1. **Ngưỡng HA tự đo tại nhà ≥ 135/85 và Holter 24 giờ ≥ 130/80** (3192, Bảng 1, tr.1). Giá trị có thật trong văn bản, và ESC 2024 trùng cả hai (slide 53). Loại vì:
   - Lớp chữ của Bảng 1 bị trộn cột: "≥ 140 mmHg ≥ 130 mmHg ≥ 135 mmHg và/hoặc ≥ 90 mmHg ≥ 80 mmHg ≥ 85 mmHg". Không có dạng "135/85" nên `parse_bps` không đọc lại được, và verify_span không qua.
   - Việc ghép giá trị với cách đo dựa vào thứ tự cột, cần người xác nhận.
   - Phụ lục 1.2 của 5904 (sơ đồ khẳng định chẩn đoán, tr.16) là ảnh, không có lớp chữ.
   - Giá trị Mỹ cho HA tại nhà chưa kiểm được vì toàn văn bị chặn.
2. **Ngưỡng khởi trị ở người ≥ 80 tuổi** (5904 tr.13: "≥ 160/90 mmHg ở người ≥ 80 tuổi"). WHO 2021 là ≥ 140/90 và không giới hạn tuổi. ESC 2024 cũng ≥ 140/90: người < 85 tuổi không suy yếu theo khuyến cáo như người trẻ; người ≥ 85 tuổi "chỉ cân nhắc từ ≥ 140/90". Loại vì:
   - **Mâu thuẫn nội bộ Bộ Y tế.** 3192/2010 (Phụ lục 4, tr.12–13) chia chiến lược theo độ HA và nguy cơ, không theo tuổi, và tuổi cao lại là một yếu tố nguy cơ. Theo đó THA độ 1 có yếu tố nguy cơ được dùng thuốc nếu không kiểm soát sau vài tuần, tức ngưỡng ngầm là 140/90. Lấy hợp theo DR8 thì WHO và ESC trùng Việt Nam, mẩu không còn là xung đột sạch.
   - Giá trị ESC/ESH 2018 cho người > 80 tuổi (nếu có thì có thể trùng Việt Nam) không kiểm được.
   - Nên báo cáo như một mâu thuẫn nội bộ (kết quả phụ ở §1.2 đề cương).
3. **HA tâm trương mục tiêu 70 đến < 80** (5904 tr.12). Trùng ESC 2024 (70–79). WHO (< 90) chỉ xung đột khi không lấy hợp với 3192 (< 140/90). Nhưng số "90" không có trong span trang 12 của 5904, nên giá trị hợp theo DR8 không đọc lại được từ span. Loại.
4. **Muối.** 3192 tr.3 ghi "< 6 gam muối", còn 5904 tr.36 ghi "chỉ nên ăn <5g/ngày", tức mâu thuẫn nội bộ. WHO là < 5 g. Mỹ dùng đơn vị natri (mg), không có quy đổi đã kiểm, và mẩu lối sống ít hệ trọng. Loại; ghi như một mâu thuẫn nội bộ.
5. **Rượu.** 3192 tr.4 ghi < 3 cốc chuẩn/ngày (nam), < 2 (nữ), < 14/tuần và < 9/tuần. 5904 tr.14 ghi ≤ 2/ngày, ≤ 1/ngày, ≤ 10/tuần và ≤ 5/tuần. Đây là mâu thuẫn nội bộ. Đơn vị "cốc chuẩn" (10 g) khác đơn vị của ESC. Loại.
6. **Vòng bụng < 90/< 80 cm và BMI 18,5–22,9** (3192, 5904). ESC 2024 dùng < 94/< 80 và BMI khoảng 20–25 (theo chữ trích từ slide 27, chưa xem ảnh). Đây là họ "ngưỡng nhân trắc cho người châu Á" (giống dòng 13 hạt giống) và cần tài liệu WHO khu vực Tây Thái Bình Dương mới đối chiếu được. Loại khỏi thí điểm; là ứng viên tốt cho kho chính.
7. **Bảng phân độ HA của 3192** (tr.2): lớp chữ có lỗi đánh máy "Tăng huyết áp độ 1 … 140 – 150" và "90 – 99 110 – 109". Không dùng; 5904 tr.11 có bảng đúng, nhưng dạng "140 – 159 và/ hoặc 90 – 99" không đọc được bằng `parse_bps`.
8. **P-htn-02: HA tâm thu mục tiêu ở người 65–79 tuổi (dòng hạt giống 7). Bị loại sau kiểm toán (2026-09-26).**
   - **Lý do chính: không phải xung đột thật.** Agent sửa đã tự đọc lại hai trang bằng `verify_span --page`:
     - 5904 tr.12 ghi mục tiêu "từ 130 đến < 140 mmHg (người ≥ 65 tuổi), **có thể thấp hơn nếu dung nạp được**";
     - 3192 tr.3 ghi "< 140/90 mmHg và **thấp hơn nữa nếu người bệnh vẫn dung nạp được**".
   - Quần thể của mẩu lại ghi "dung nạp tốt điều trị". Với đúng người đó, cả hai văn bản Bộ Y tế đều cho phép hạ thấp hơn. Vì vậy 120–129 (ESC 2024, cũng chỉ áp dụng "provided the treatment is well tolerated", slide 93) và < 130 (Mỹ 2025) **không trái** Bộ Y tế. Khác nhau chỉ ở mức mặc định.
   - Trạng thái "conflict" cũ chỉ do mã hóa: "< 140" của 3192 bị lưu thành điểm 140, và bộ chấm bỏ qua `cmp`.
   - **Lý do phụ: mồi trùng nguồn có tên.** Mồi 141–150 (mirror_arith) chứa mục tiêu tâm thu < 150 mmHg của **JNC8** cho người ≥ 60 tuổi. Agent sửa đã grep lại bản tóm tắt AAFP (sha256 `c1c27f69dc3d5320`) và thấy "target systolic pressure of less than 150 mm hg".
   - Không cứu được bằng cách bỏ điều kiện "dung nạp tốt". Khi đó ESC 2024 chuyển sang nguyên tắc ALARA ("thấp nhất có thể đạt được"), nên xung đột vẫn không đứng.
   - Có thể dựng lại thành mẩu đối chứng **sau khi** bộ chấm hiểu `cmp` nhất quán (§7.8). Đây là quyết định cho HG1.2 hoặc bác sĩ thật, agent không tự làm.

---

## 4. Sai lệch so với bộ hạt giống (§3.3, `data/seed/seed_conflicts.yaml`)

**Dòng 6 (ngưỡng chẩn đoán đo tại phòng khám):**
- Giá trị Việt Nam ≥ 140/90 **khớp** (3192 tr.1 và 5904 tr.11).
- Văn bản nguồn của span khác hạt giống: hạt giống ghi 3192/2010, còn mẩu lấy span từ **5904/2019** (cùng giá trị). Lý do là 3192 viết tách "≥ 140mmHg và/hoặc … ≥ 90mmHg", bộ đọc HA không đọc được. 3192 được giữ trong `extraction.supporting_spans`.
- Nguồn WHO đã sửa. Hạt giống chỉ ghi "WHO 140/90", nhưng WHO 2021 guideline tự nói không đề cập chẩn đoán (PDF tr.14). Giá trị WHO hiện lấy từ WHO fact sheet 25/9/2025.
- Ghi chú của hạt giống "130/80 là ngưỡng đo lưu động của chính Bộ Y tế" **đúng**: 3192 Bảng 1 ghi Holter 24 giờ ≥ 130 / ≥ 80. Bổ sung thêm: ngưỡng tự đo tại nhà là ≥ 135 / ≥ 85.
  - **[đã sửa, §7.6]** Không được viết "đúng". Cách ghép này dựa vào thứ tự cột và **chưa có người xác nhận**, thống nhất với §3.1.
- Trạng thái `confirmed_us_only` **khớp**.

**Dòng 7 (mục tiêu ở người ≥ 65 tuổi):**
- Giá trị "130 đến < 140 mmHg" **khớp** (5904 tr.12), nhưng hạt giống thiếu ba điểm:
  - (a) Mệnh đề kèm theo "có thể thấp hơn nếu dung nạp được".
  - (b) Theo **DR8**, phải lấy hợp với 3192/2010 (< 140/90, áp dụng mọi tuổi, mọi cơ sở), nên tập Việt Nam là {130 đến < 140} ∪ {< 140}.
  - (c) Quần thể phải giới hạn: không ĐTĐ (5481/2020 có mục tiêu riêng), nguy cơ không cao (3192 dùng < 130/80 cho nguy cơ cao đến rất cao), và dưới 85 tuổi, không suy yếu (ESC 2024 nới mục tiêu khi ≥ 85 tuổi hoặc suy yếu). Mẩu ghi 65–79 tuổi.
- ESC 2024 120–129 và ESC/ESH 2018 130–139 **khớp**. Việt Nam bằng ESC/ESH 2018, nên khác biệt gốc là ESC đã cập nhật năm 2024 còn Bộ Y tế chưa.
- **[đã sửa, §7.6] Kết luận mới cho dòng 7: bị bác khi đối chiếu văn bản.** Không có hệ thống nào xung đột với Bộ Y tế cho quần thể dung nạp tốt (§3 mục 8). Kết luận "xung đột chỉ với EU_UK" ở dưới đã lỗi thời.
- **Mỹ "< 130/80":** giá trị đúng (áp dụng cho mọi người lớn), nhưng **về vận hành không phải xung đột**. Bộ chấm và `_gap` bỏ qua dấu so sánh, nên "< 130" bị đọc thành điểm 130, đúng bằng cận dưới của tập Việt Nam. Kết quả: finalize coi Mỹ trùng Việt Nam, và câu trả lời "< 130 mmHg" được chấm "đúng theo Bộ Y tế". Vì vậy dòng 7 hiện là **xung đột chỉ với EU_UK**, chứ không phải với cả Mỹ và châu Âu như hạt giống.
- Thêm WHO 2021 (< 140/90): **trùng** Việt Nam.

**Lỗi đánh máy trong văn bản gốc:**
- 5904 tr.28 (phần lồng ghép THA–ĐTĐ) ghi "(người <65 tuổi)" hai lần; lần hai lẽ ra là ≥ 65.
- Bảng cùng trang ghi mục tiêu HA "< 130/80" cho bệnh nhân THA kèm ĐTĐ. Đây là quần thể khác, không dùng.

---

## 5. Việc cần người kiểm ở HG1.2

1. **Đối chiếu span.** Mở `data/raw/5904_2019__9e6bbe13.pdf` trang 11, 12, 13 (trang in 2, 3, 4) và `data/raw/3192_2010.pdf` trang 1 và 3. So từng span và giá trị.
2. **Quyết định về file 5904.** File chuẩn `data/raw/5904_2019.pdf` là bản scan 22 trang (có chữ ký số, nhưng không có lớp chữ). Hai cách:
   - (a) Chấp nhận khóa biến thể `5904/2019__9e6bbe13` trong trường `guideline`.
   - (b) Người hoặc orchestrator đổi file chuẩn sang bản có lớp chữ, đổi `guideline` của 4 mẩu thành `5904/2019`, rồi chạy lại `verify_span`. Nên giữ bản scan có chữ ký làm bằng chứng danh tính.

   Agent không được sửa `data/raw`, nên chưa làm.

   **[đã sửa, §7.3]** Phương án (b) không cần đổi `data/raw`:
   - `verify_span.pdf_path()` đã đọc `data/interim/pdf_choice.json`;
   - `pilot_merge.canonical_keys()` tự ghi file đó từ khóa biến thể khi gộp.
3. **P-htn-02, quyết định lâm sàng.** Mệnh đề "có thể thấp hơn nếu dung nạp được" (5904) và "thấp hơn nữa nếu người bệnh vẫn dung nạp được" (3192) có làm mục tiêu 120–129 của ESC 2024 thành hợp lệ theo Bộ Y tế không? Nếu có, mẩu không còn là xung đột và nên loại hoặc xếp `indistinguishable`.
4. **Lỗi bộ chấm với dấu `<`** (P-htn-02, P-htn-04; xem §6.1). Cần quyết sửa bộ chấm hay chấp nhận, trước khi đóng băng quy tắc chấm. Hiện câu trả lời kiểu Mỹ "< 130" ở P-htn-02 bị chấm đúng, tức lệch **bất lợi** cho H1 (bảo thủ).
5. **AHA/ACC 2025.** Mở toàn văn bằng trình duyệt để xác nhận và điền số mục/bảng vào `locator` cho ba điểm:
   - bảng phân loại HA đo tại phòng khám, với THA ≥ 130/80;
   - mục tiêu < 130/80 cho người ≥ 65 tuổi sống tại cộng đồng (và các ngoại lệ "additional considerations");
   - khởi trị ở người nguy cơ thấp khi HA ≥ 130/80 sau 3–6 tháng thay đổi lối sống.
6. **Mồi P-htn-02 (141–150 mmHg)** có thể trùng mục tiêu "< 150" dành cho người cao tuổi của JNC8 (2014). Agent **chưa** kiểm bằng nguồn tải về. Nếu trùng, mồi không còn "vô nguồn": cân nhắc ghi JNC8 như nguồn Mỹ cũ, hoặc đổi quy tắc mồi cho mẩu này.
7. **Câu hỏi phải nêu đủ quần thể:**
   - P-htn-01: "HA đo tại phòng khám bởi nhân viên y tế", không phải HA tại nhà hay Holter.
   - P-htn-03: nguy cơ 10 năm < 5%, không bệnh đồng mắc, đã thay đổi lối sống 3–6 tháng, HA đo tại phòng khám.
   - P-htn-02: 65–79 tuổi, không suy yếu, không ĐTĐ.
   - Với P-htn-03, sơ đồ ở trang in 3 của 5904 (ảnh, agent đã xem trên bản scan) ghi rằng HA 130–139/85–89 chỉ cần thay đổi lối sống, trừ khi nguy cơ rất cao. Cần người xác nhận.
8. **Mâu thuẫn nội bộ Bộ Y tế** nên ghi vào kết quả phụ:
   - khởi trị ở người ≥ 80 tuổi (5904: 160/90; 3192: không phân tuổi);
   - muối (< 6 g hay < 5 g);
   - rượu (3192 khác 5904);
   - lỗi đánh máy 3192 tr.2 và 5904 tr.28.
9. **Kiểm lại xem Bộ Y tế có hướng dẫn THA mới sau 2019 không.** Agent chỉ xem được trang 1 của kcb.vn/phac-do, và ngân sách tìm kiếm đã hết. Nếu có văn bản mới, cả 4 mẩu phải làm lại.
10. **An toàn nguồn.** Trang vncdc.gov.vn (nd14992) chứa liên kết spam, có thể đã bị chèn mã. Không tải file từ trang đó.

---

## 6. Đề xuất bổ sung mã / configs (agent không tự sửa)

1. **`src/vnsoc/grade.py`: xử lý dấu so sánh `<` và `<=`.** **[RÚT LẠI, thay bằng §7.8 mục 1]** Như kiểm toán chỉ ra, nếu chỉ tôn trọng `cmp` ở câu trả lời và ở giá trị nước ngoài thì câu trả lời sẽ bị chấm sai theo Bộ Y tế.
   - Trong `matches()` cho num: câu trả lời chỉ có cận trên ("< x") **không** được tính là nằm trong một khoảng đóng [lo, hi] có lo = x.
   - Trong `_gap()`: "< x" so với khoảng có lo = x phải ra gap > 0 (ví dụ bằng 1 bước làm tròn), để `conflict_status` nhận ra xung đột với Mỹ ở P-htn-02.
   - Test đề xuất: P-htn-02 "< 130 mmHg" → nhãn 4 (US); P-htn-04 "< 120 mmHg" → không phải nhãn 2.
   - Phải tăng `grader_version`.
2. **`src/vnsoc/normalize_vi.py`: `parse_bps` đọc thêm dạng viết tách** "tâm thu ≥ 140 mmHg và/hoặc (huyết áp) tâm trương ≥ 90 mmHg" → BP(140, 90). Khi đó span định nghĩa gốc của 3192 tr.1 dùng được làm span chính.
3. **Trích bảng (T3.1):** Bảng 1 của 3192 cần pdfplumber hoặc trích theo tọa độ cột. Lớp chữ PyMuPDF trộn cột.
4. **Khóa trùng trong `data/raw`:** khi bản tải đầu là scan và bản sau có lớp chữ (`clash_kept_both`), cần cách "đặt bản có lớp chữ làm chuẩn" có người duyệt, hoặc một trường manifest `pdf_file` để `verify_span` biết dùng file nào mà không phải đổi khóa `guideline`.
   - **[đã sửa, §7.3]** Cơ chế này đã có: `data/interim/pdf_choice.json`, được đọc bởi `pdf_path()` và ghi bởi `pilot_merge.canonical_keys()`. Chỉ còn thiếu người duyệt.
5. **`src/vnsoc/match/sources.py`:**
   - (a) Đọc được pptx: slide ESC là EMF, chữ nằm trong bản ghi EMR_EXTTEXTOUTW.
   - (b) Tự đổi link IRIS dạng `/bitstream/handle/...` sang `/server/api/core/bitstreams/<uuid>/content`.
   - (c) Ghi rõ khi bị reCAPTCHA (NCBI) thay vì lưu trang rỗng.
6. **configs:** không cần thêm thuốc hay đơn vị (chỉ dùng mmHg, đã có trong `UNIT_ALIASES`).
7. **Ngân sách công cụ:** WebSearch đã chạm trần 200 lượt/phiên (dùng chung giữa các agent). Các agent T1.1 chạy sau có thể không tìm kiếm được.

---

## 7. Sau kiểm toán (2026-09-26)

**Đầu vào:** `data/interim/pilot/htn_verify.md`, do integrity-auditor (AI) viết. Kết luận của kiểm toán: 0 đạt, 3 sửa (P-htn-01, 03, 04), 1 loại (P-htn-02).

**Cách làm:** agent sửa (Claude, AI, không phải bác sĩ) tự kiểm lại bằng chứng bằng công cụ **trước** khi sửa. Chỉ ghi `htn.jsonl` và file này. Không sửa `data/raw`, `src`, `configs` hay `data/seed`.

### 7.1 Những gì agent sửa đã tự kiểm lại

**Đọc lại văn bản Việt Nam** (`verify_span --page`):
- 3192 tr.1, 3, 12;
- 5904 (bản có lớp chữ) tr.11, 12, 13;
- **2919/2014 tr.5, 53, 55–58** (mới, xem §7.6).

**Xem ảnh trang** (AI xem; render bằng PyMuPDF vào scratchpad, không ghi vào repo):
- 3192 tr.1, Bảng 1. Cột tâm thu thẳng hàng với từng dòng (140 / 130 / 135). Cột tâm trương xếp dồn 90 / 80 / 85 và **không** thẳng hàng với dòng. Vì vậy ghép Holter = 130/80 và tại nhà = 135/85 chỉ dựa vào thứ tự cột.
- 5904 tr.12, Bước 4. Dòng chuyển tuyến trên ghi "THA ở người trẻ (≤ 40 tuổi)". Lớp chữ bị mất "(≤".

**Nguồn nước ngoài** (`sources grep` lại trên bộ đệm; kết quả khớp kiểm toán):

| Nguồn | sha256 (16) | Đã thấy |
|---|---|---|
| AHA 2025 | bbc83c2a1e37a919 | "stage 1 hypertension is 130-139 … or 80-89"; "remain the same as the 2017 guideline" |
| ACC 2025 | aea4b0989dd4ab54 | "<130/80 mm hg for all adults"; "PREVENT <7.5%" với "3 to 6 months" |
| WHO 2021 | 57f6376d5c9bc4ea | KN 1 "≥140 … ≥90" (tr.9, 19); KN 6 "<140/90" (tr.10, 28); "does not address … diagnosis" (tr.14) |
| WHO fact sheet | 2779af89d3929cb2 | "two different days"; "25 September 2025" |
| JNC8 (bản tóm tắt AAFP, Am Fam Physician 2014;90(7):503) | c1c27f69dc3d5320 | "150/90 … 60 years and older, or 140/90 … younger than 60"; mục tiêu "< 150" (≥ 60 tuổi) và "< 140" (< 60 tuổi) |

**Bộ slide ESC 2024** (c006bbb57dbbee77):
- `sources grep` không đọc được pptx.
- Agent tự trích chữ từ các bản ghi EMR_EXTTEXTOUTW trong EMF, bằng script ở scratchpad, cho các slide 31, 32, 53, 92, 93 và 99. Giá trị **khớp** kiểm toán:
  - slide 53: văn phòng ≥ 140/90, 24 giờ ≥ 130/80, tại nhà ≥ 135/85;
  - slide 92: ≥ 140/90 dùng thuốc bất kể nguy cơ; HA tăng (elevated) + nguy cơ < 10% chỉ thay đổi lối sống;
  - slide 93: 120–129 "provided … well tolerated";
  - slide 31, cột 2018: < 140/90 cho mọi người, rồi 130/80 hoặc thấp hơn;
  - slide 32, cột 2018: ≥ 65 tuổi 130–139;
  - slide 99: người < 85 tuổi không suy yếu theo khuyến cáo như người trẻ.

**Nguồn vẫn bị chặn:** NICE NG136. Đã thử `sources fetch` bản PDF đúng 1 lần, kết quả 403.

**Kết quả cuối trên `htn.jsonl`:**
- `vnsoc.schemas atom` → OK 3/3;
- `vnsoc.extract.verify_span` → OK 3/3;
- `finalize()` tính lại trùng giá trị đã lưu (tolerance, conflict_status);
- `check_decoy()` = [];
- `pilot_merge.enforce_decoy_rule()` cho đúng mồi đã lưu;
- `pilot_merge.check()` = [] cho cả 3 mẩu.

### 7.2 Theo từng mẩu: đã sửa gì, giữ gì, vì sao

**P-htn-01, ngưỡng chẩn đoán (HA đo tại phòng khám).** Kiểm toán: fix. Trạng thái giữ **conflict (US)**.

Đã sửa:
- **Span chính đổi sang ĐỊNH NGHĨA của 3192/2010 tr.1** ("Tăng huyết áp là khi huyết áp tâm thu ≥ 140mmHg và/hoặc … ≥ 90mmHg"), thay câu "Đối tượng áp dụng" của 5904.
  - `guideline` = `3192/2010`, `valid_from` = 2010-08-31. Mẩu này không còn khóa biến thể.
  - Đây đúng là văn bản của dòng hạt giống 6, lấy từ nguồn kcb.vn.
- 5904 tr.11 chuyển vào `extraction.dr8_sources` (cùng giá trị ≥ 140/90). `verify_span` vừa kiểm nguyên văn span này vừa đọc lại 140/90 từ đó.
  - Lý do: kiểm toán đề xuất đổi span "sau khi `parse_bps` đọc được dạng viết tách". Nhưng `verify_span` đã hỗ trợ `extraction.dr8_sources` (có test), nên không cần chờ sửa mã.
  - `supporting_spans` gồm Bảng 1 của 3192 tr.1 và dòng "THA độ 1 140 – 159 và/ hoặc 90 – 99" của 5904 tr.11. Cả hai đã kiểm nguyên văn.
- `notes`: ghép Holter 130/80 và tại nhà 135/85 ghi rõ là "theo thứ tự cột, **chưa có người xác nhận** (HG1.2)", kèm mô tả ảnh trang.
- ESC 2024: `verified_by` → `null`; `locator` thêm "needs_human_check …".
- WHO_global: `source` ghi rõ "fact sheet, KHÔNG phải guideline".

Giữ nguyên:
- vn ≥ 140/90; US ≥ 130/80 (AHA 2025); ESC 2024 và WHO ≥ 140/90;
- mồi 150/100 (mirror_arith; `choose_decoy` cho cùng kết quả);
- tolerance 5; `conflict_family` = `htn_us_130_80`.

Không thêm JNC8, vì JNC8 không đưa ngưỡng chẩn đoán.

**P-htn-02, mục tiêu tâm thu ở người 65–79 tuổi.** Kiểm toán: reject. Agent **đồng ý** và đã **bỏ khỏi jsonl**; lý do ở §3 mục 8. Hai mệnh đề "dung nạp được" đã tự đọc lại. Mồi trùng JNC8 < 150 đã tự grep lại.

**P-htn-03, ngưỡng HA bắt đầu dùng thuốc (nguy cơ thấp).** Kiểm toán: fix. Trạng thái giữ **conflict (US 2025)**.

Đã sửa:
- **`population.age`: 18–79 → 41–59 tuổi.** Kiểm toán đề xuất 40–59. Agent chọn 41 vì 5904 tr.12 chuyển tuyến trên "THA ở người trẻ (≤ 40 tuổi)" (đã xem ảnh). Người ≤ 40 tuổi không được quản lý tại trạm, nên không hợp với span chính của 5904.
- **Thêm JNC8** (US, 2014, bản tóm tắt AAFP): ≥ 140/90 cho người < 60 tuổi, trùng Việt Nam, `verified_by: auto`. Trước đây người 60–79 tuổi có giá trị Mỹ cũ 150/90 mà không được ghi.
- `cv_risk`: thay "< 5%" bằng hồ sơ cụ thể: không có yếu tố nguy cơ nào khác, không thuộc nhóm nguy cơ cao hoặc rất cao của 5904 tr.12. `notes` ghi rõ ba thang khác nhau: SCORE của 5904, PREVENT < 7,5% của Mỹ, < 10% của ESC.
- ESC: `verified_by` → `null` kèm "needs_human_check".
- `notes`: ghi rằng 2919/2014 tr.57 có cùng chiến lược (không lệch phiên bản), và NICE/ESH chưa ghi.

Giữ nguyên:
- span 5904 tr.13; vn ≥ 140/90; US 2025 ≥ 130/80; ESC; WHO;
- mồi 150/100 (không trùng JNC8 140/90 hay nguồn nào đã ghi);
- `conflict_family` = `htn_us_130_80`.

**P-htn-04, mục tiêu tâm thu ở người trẻ và trung niên.** Kiểm toán: fix. Trạng thái giữ **concordant**, không có mồi.

Đã sửa:
- **`population.age`: 18–64 → 18–59 tuổi**, và **thêm JNC8** (US 2014) mục tiêu < 140 cho người < 60 tuổi.
  - Kiểm toán không nêu riêng điểm này cho P-htn-04. Agent tự áp dụng Vấn đề chung 4: mọi mẩu có tuổi ≥ 60 phải xét JNC8.
  - Nếu giữ 60–64 tuổi, câu trả lời "< 150" (JNC8 cho ≥ 60 tuổi) sẽ bị chấm vô nguồn.
- **`union_spans` → `extraction.dr8_sources`.** Từ nay `verify_span` kiểm nguyên văn span 3192 tr.3 và đọc "< 140" từ chính span đó. Đây là sửa ở mức dữ liệu cho điểm 3 của kiểm toán (trước đó vn[1] chỉ khớp nhờ trùng hợp với chuỗi "130 đến < 140" trong câu về người ≥ 65 tuổi).
- `notes` ghi rõ ba điều:
  - (a) mẩu **chỉ concordant nhờ hợp DR8 với 3192**. Nếu 3192 không còn hiện hành thì phải tính lại;
  - (b) "< 140" đang được lưu thành điểm 140;
  - (c) hệ quả chấm ở §7.5.
- ESC 2024 và ESC/ESH 2018: `verified_by` → `null` kèm "needs_human_check".

### 7.3 Khóa văn bản 5904/2019: giữ khóa biến thể, có lý do

- Kiểm toán đề xuất tạo `data/interim/pdf_choice.json` rồi đổi `guideline` thành `5904/2019`. Agent **không** làm được việc này:
  - agent chỉ được ghi 2 file;
  - nếu đổi `guideline` khi chưa có `pdf_choice.json`, `pdf_path()` sẽ trỏ vào bản scan và `verify_span` thất bại.
- Đọc mã thì thấy `vnsoc.extract.pilot_merge.canonical_keys()` đã làm việc này khi gộp. Nó đổi khóa dạng `<khóa>__<8 hex>` về khóa chuẩn và ghi `pdf_choice.json`, kèm lý do "cần người xác nhận ở HG1.2/HG2.3". Vì vậy giữ `5904/2019__9e6bbe13` ở P-htn-03 và P-htn-04 là đúng đường mà mã đã thiết kế.
- Kiểm toán mô tả việc này là "orchestrator/người tạo file". Thực tế chỉ cần chạy `pilot_merge`, rồi người duyệt ở HG1.2.
- **Lưu ý:** `canonical_keys()` chỉ đổi `atom["guideline"]`, không đổi khóa bên trong `extraction.dr8_sources` và `supporting_spans`. P-htn-01 vẫn ghi `5904/2019__9e6bbe13` ở `dr8_sources`, và vẫn trỏ đúng file vì `pdf_path()` dùng tên file mặc định. Đề xuất sửa ở §7.8.

### 7.4 Bảng mẩu hiện hành

| id | Slot | Quần thể (rút gọn) | VN | Nước ngoài (hệ thống: giá trị, phiên bản) | Trạng thái | Nguồn span (trang PDF) |
|---|---|---|---|---|---|---|
| P-htn-01 | threshold: ngưỡng chẩn đoán (đo tại phòng khám) | ≥ 18 tuổi, không mang thai | ≥ 140/90 (3192 ∪ 5904, trùng nhau) | US ≥ 130/80 (AHA/ACC 2025) ✗ · EU_UK ≥ 140/90 (ESC 2024, cần người kiểm) ✓ · WHO ≥ 140/90 (fact sheet 2025) ✓ | **conflict**; mồi 150/100; tol 5 | 3192 tr.1; DR8: 5904 tr.11 |
| P-htn-03 | threshold: khởi trị thuốc | 41–59 tuổi, không yếu tố nguy cơ khác, đã thay đổi lối sống 3–6 tháng, đo tại phòng khám | ≥ 140/90 | US ≥ 130/80 (2025) ✗ · US ≥ 140/90 (JNC8 2014) ✓ · EU_UK ≥ 140/90 (ESC 2024, cần người kiểm) ✓ · WHO ≥ 140/90 (2021) ✓ | **conflict**; mồi 150/100; tol 5 | 5904 tr.13 (trang in 4) |
| P-htn-04 | target: HA tâm thu khi điều trị | 18–59 tuổi, nguy cơ không cao, dung nạp tốt | {120 đến < 130} (5904) ∪ {< 140} (3192, DR8) | EU_UK 120–129 (2024) ✓ · EU_UK < 140 / ≤ 130 (2018) ✓ · US < 130 (2025) ✓ · US < 140 (JNC8 2014) ✓ · WHO < 140 (2021) ✓ | **concordant**; không mồi; tol 5 | 5904 tr.12 (trang in 3); DR8: 3192 tr.3 |

Tổng: 2 xung đột (cùng `conflict_family` `htn_us_130_80`, nên chỉ là **một** cụm khác biệt gốc), 1 đối chứng, 0 lệch phiên bản.

### 7.5 Chấm thử bộ chấm hiện hành (`grade_short`, chỉ đọc)

| Mẩu | Câu trả lời | Nhãn | Nhận xét |
|---|---|---|---|
| 01 | ≥ 140/90 | 2 | đúng |
| 01 | ≥ 130/80 | 4 (US) | đúng |
| 01 | 150/100 | 5, decoy_match | đúng |
| 01 | ≥ 135/85 | 5 | là ngưỡng tự đo tại nhà (3192 Bảng 1, ESC); câu hỏi phải nói "đo tại phòng khám" |
| 03 | ≥ 140/90 | 2 | đúng |
| 03 | ≥ 130/80 | 4 (US) | đúng |
| 03 | ≥ 150/90 | 5 | đúng cho quần thể 41–59 (JNC8 150/90 chỉ cho ≥ 60 tuổi) |
| 04 | 120–129 | 2 | đúng |
| 04 | < 140 | 2 | đúng |
| 04 | **135** | **5** ⚠ | sai: 135 thỏa "< 140" của 3192 |
| 04 | **130–139** | **5** ⚠ | sai, cùng nguyên nhân (cmp bị bỏ qua) |
| 04 | < 150 | 5 | đúng (không nguồn nào cho < 60 tuổi) |

### 7.6 Sai lệch so với bộ hạt giống (thay cho §4 ở các điểm sau)

**Dòng 6:**
- Nay span chính lấy từ **3192/2010**, đúng như hạt giống.
- Giá trị và trạng thái `confirmed_us_only` **khớp**.
- Ghi chú "130/80 là ngưỡng đo lưu động của Bộ Y tế" đúng theo thứ tự cột của Bảng 1, nhưng **chưa có người xác nhận**.

**Dòng 7: BỊ BÁC KHI ĐỐI CHIẾU VĂN BẢN** (§3 mục 8).
- Đề xuất người sửa `data/seed/seed_conflicts.yaml`: đổi `status: confirmed` thành trạng thái "bác khi đối chiếu", ghi lý do là mệnh đề "có thể thấp hơn nếu dung nạp được" (5904 tr.12) và "thấp hơn nữa nếu … dung nạp được" (3192 tr.3).
- Kết quả này quan trọng cho **độ nhạy trên bộ hạt giống**: không được tính dòng 7 là "pipeline bỏ sót".

**Văn bản bị thay thế: 2919/2014 Phần 2.**
- Báo cáo gốc viết "không có văn bản THA bị thay". Câu đó sai. Theo manifest (`c3_ncd`), Điều 3 của 5904/2019 bãi bỏ Phần 2 của 2919/2014.
- Agent sửa đã đọc các trang (`verify_span --page`):
  - tr.53: định nghĩa ≥ 140 / ≥ 90;
  - tr.56: mục tiêu < 140/90 (< 130/80 nếu nguy cơ cao hoặc rất cao);
  - tr.57: chiến lược theo độ HA và nguy cơ, giống 3192 Phụ lục 4.
- Cả ba slot hiện có đều **trùng** tập Việt Nam hiện hành, nên **không có mẩu lệch phiên bản** cho THA.
- Chỉ đọc 2919, không dùng tạo mẩu: `fetch_pdf` báo `text_kind = scanned_or_empty`. Manifest ghi đây là âm tính giả của heuristic, vì 380/408 trang có lớp chữ.
- Muối: 2919 ghi "< 6 g" còn 5904 ghi "< 5 g". Đây có thể là một thay đổi phiên bản ở tuyến xã, nhưng 3192 hiện hành vẫn ghi "< 6 g", nên hợp theo DR8 không tách được. Vẫn loại, như §3 mục 4.

### 7.7 Tồn đọng cho HG1.2 (người làm)

1. **Đối chiếu span bằng mắt:**
   - 3192 tr.1: định nghĩa, và **Bảng 1: xác nhận Holter 24 giờ = 130/80, tại nhà = 135/85**.
   - 3192 tr.3.
   - 5904 (bản `__9e6bbe13`) tr.11–13, so với bản scan có chữ ký.
2. **ESC 2024:** mở bộ slide (URL trong `foreign`), xác nhận slide 53, 92, 93 và 31 (cột 2018). Sau đó người đặt `verified_by` = "student" hoặc "clinician". Agent không được tự đặt.
3. **Chọn file 5904:** duyệt `pdf_choice.json` mà `pilot_merge` sẽ ghi, tức bản có lớp chữ của BVĐK Hà Trung, đối chiếu với bản scan có chữ ký của TTYT Quy Nhơn (HG1.2/HG2.3).
4. **Tính hiện hành của 3192/2010.** 5904 tr.13 dẫn tới "Hướng dẫn chẩn đoán và điều trị THA dành cho tuyến y tế cơ sở"; cần xác định đó là văn bản nào.
   - Nếu có văn bản THA mới hơn, **P-htn-04 phải tính lại**, vì concordant chỉ nhờ DR8 với 3192. P-htn-01 và 03 không đổi trạng thái, vì 5904 cho cùng giá trị.
5. **NICE NG136 và ESH 2023/2024** (bị 403 hoặc không có toàn văn): mở bằng trình duyệt và ghi giá trị, vị trí, ngày cho:
   - (a) ngưỡng chẩn đoán đo tại phòng khám;
   - (b) ngưỡng khởi trị cho người 41–59 tuổi, THA độ 1, nguy cơ thấp;
   - (c) mục tiêu tâm thu cho người < 60 tuổi.

   Không điền từ trí nhớ. Kết quả có thể thêm dòng EU_UK vào foreign; cần chạy lại `finalize` và `choose_decoy`.
6. **AHA/ACC 2025 toàn văn:** ghi số mục và bảng vào `locator` (ba điểm như §5 mục 5; điểm về người ≥ 65 tuổi nay không còn cần vì P-htn-02 đã bị loại).
7. **Sửa bộ chấm (`cmp`)** trước khi đóng băng quy tắc chấm (xem §7.8 mục 1).
8. **Viết câu hỏi:**
   - dùng tuổi cụ thể ở giữa khoảng (ví dụ 50 tuổi) cho P-htn-03 và P-htn-04;
   - P-htn-04 có 18–40 tuổi. Theo 5904, người ≤ 40 tuổi được chuyển tuyến trên, nhưng có thể được chuyển về trạm sau khi ổn định (Bước 4 B), và 3192 áp dụng ở mọi tuyến, nên tập giá trị không đổi. Tránh hỏi người ≤ 40 tuổi cho gọn;
   - P-htn-01 phải nói "HA đo tại phòng khám bởi nhân viên y tế".
9. **Dòng hạt giống 7:** người đổi trạng thái trong `seed_conflicts.yaml` (§7.6).

### 7.8 Đề xuất mã / configs (bổ sung §6; agent không tự sửa)

1. **`src/vnsoc/grade.py`** (thay §6.1, theo Vấn đề chung 1 của kiểm toán): hiểu `cmp` **nhất quán cho mọi mục** (vn, foreign, superseded, decoy và câu trả lời).
   - "< x" là khoảng nửa mở (0, x); "≤ x" là (0, x].
   - `matches()` coi câu trả lời nằm trong mục "< b" khi toàn bộ khoảng của nó < b.
   - `_gap` = 0 khi hai khoảng giao nhau.
   - Test cần có:
     - P-htn-04: "135 mmHg" → 2, "130–139 mmHg" → 2, "< 150" → 5;
     - P-htn-01: "≥ 130/80" → 4 (không đổi).
   - Phải tăng `grader_version`.
2. **`src/vnsoc/extract/pilot_merge.py`:**
   - (a) `canonical_keys()` đổi cả khóa biến thể trong `extraction.dr8_sources` và `supporting_spans`;
   - (b) `source_warnings()` phải bỏ qua hoặc gắn cờ nguồn nhị phân (pptx). Hiện nó "thấy" các số 120, 129, 130 trong byte của file zip, tức là kết quả nhiễu. ESC phải chờ người kiểm.
3. **`src/vnsoc/match/sources.py`:** đọc pptx có slide EMF (bản ghi EMR_EXTTEXTOUTW), như §6.5a. Agent đã chứng minh làm được bằng một script khoảng 30 dòng. Khi có, ESC mới được đặt `verified_by: auto`.
4. **`src/vnsoc/schemas.py`:** chính thức hóa `extraction.dr8_sources` (đã được `verify_span` dùng và có test) trong tài liệu schema và skill atomization-protocol, để các agent khác dùng thay cho `union_spans` hay `supporting_spans` tự đặt tên.
5. **configs:** không cần thêm gì.
