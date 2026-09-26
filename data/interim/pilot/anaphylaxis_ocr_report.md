# T1.1 thí điểm — Phản vệ từ OCR TT51/2017, áp DR8 với QĐ 3942/2014 và QĐ 3312/2015 (ID = anaphylaxis_ocr)

Ngày: 2026-09-26 · Người làm: agent atom-extractor + counterpart-matcher (Claude) · File mẩu: `data/interim/pilot/anaphylaxis_ocr.jsonl` (6 mẩu)

> **LƯU Ý:** mục 0–7 là bản **trước kiểm toán**. Kết quả hiện hành nằm ở **mục 8 "Sau kiểm toán"**. Đã thay đổi: `verify_span` 6/6 OK, `span_verified` 6/6 true, thêm WHO_global, trạng thái của -01 và -05 phụ thuộc cách đọc DR8, và cả hai được giữ ngoài tập H1.

## 0. Tóm tắt trung thực

| Chỉ số | Kết quả |
|---|---|
| Mẩu ghi vào JSONL | 6 (2 conflict, 4 concordant, 0 indistinguishable) |
| `vnsoc.schemas atom` | **OK 6/6** |
| `verify_span <file>` | **CHỈ 1/6 OK** (P-…-03). 5 mẩu LỖI, lý do **duy nhất** là "không đọc lại được giá trị vn [i] từ span". Các mục i đó là giá trị thêm theo DR8 từ **văn bản khác hoặc trang khác** (QĐ 3312/2015, QĐ 3942/2014, TT51 PL X trang 20). Công cụ chỉ đọc giá trị từ **một** span của mẩu. |
| Kiểm từng thành phần (cùng hàm `verify_atom`, span phụ đặt vào đúng văn bản/trang) | Mọi span phụ **có trên đúng trang**. **Mọi** mục `vn` đọc lại được từ ít nhất một span nguồn thật (xem `extraction.vn_item_checks`). Ngoại lệ duy nhất: "0,01 ml/kg" của 3942 tr.13 không đọc lại được vì bộ phân tích chưa có đơn vị ml/kg (mục 6.2). Giá trị này trùng 3312 tr.106, và 3312 thì đọc lại được. |
| `span_verified` | Theo quy tắc ("true chỉ khi verify_span OK"): -03 = true, 5 mẩu còn lại = **false**. `pilot_merge` hiện sẽ **loại** 5 mẩu này cho tới khi sửa mã theo mục 6.1. |
| Kiểm ảnh trang OCR | Cả 6 mẩu: agent đã xem ảnh trang 9 và 20 của `data/raw/TT51_2017.pdf`. **Mọi con số và đơn vị trong span khớp ảnh.** Các lỗi OCR có chữ số ('Img' = 1mg; ']' = 1; ký tự '6' thừa) đều nằm **ngoài** span (span đã được cắt để tránh). |

**Kết luận chính về hạt giống 15:** khi áp DR8 trung thực, trạng thái phụ thuộc **nguyên nhân phản vệ** nêu trong quần thể:
- **Do thuốc** (P-…-01): vẫn là **conflict**, chỉ với RCUK 150 µg và mức 0,15 mg của WAO. Giá trị "0,01 mg/kg" (WAO/Mỹ) mà bảng hạt giống ghi là xung đột thì **nay nằm trong tập Bộ Y tế** (3312/2015 và 3942/2014 chương dị ứng thuốc).
- **Do thức ăn** (P-…-02): **concordant**. QĐ 3942/2014 chương dị ứng thức ăn ghi "Trẻ em nặng 10-25kg: adrenaline 0,15mg", đúng bằng RCUK.
- **Nếu coi 3942/3312 là bản đã bị TT51 thay:** indistinguishable.

Ngay cả mẩu "do thuốc" cũng có **rủi ro quy nguồn**: 150 µg là giá trị hiện hành của chính Bộ Y tế cho một quần thể bên cạnh (phản vệ do thức ăn).

---

## 1. Văn bản dùng

| Khóa | Nguồn chính thức | File | sha256 (16) | Trang | Lớp chữ | Hiệu lực |
|---|---|---|---|---|---|---|
| TT51/2017 | kcb.vn (PDF quét có ký số) | `data/raw/TT51_2017.pdf` | cab611be9dd14312 | 20 | **OCR** (Tesseract 5.4, vie+eng, 300 dpi; `data/interim/ocr/TT51_2017/`, meta sha khớp PDF) | Điều 7 (OCR tr.3): hiệu lực từ 15/02/2018; chỉ làm hết hiệu lực TT08/1999. Trang kcb.vn: "Đã có hiệu lực" |
| 3942/2014 | kcb.vn, gói RAR "Mien-dich.rar" | `data/raw/3942_2014.pdf` | 4be16be0fe6812f4 | 144 | lớp chữ PDF (tốt) | Trang kcb.vn "Đã có hiệu lực"; không thấy văn bản thay thế (cần người xác nhận) |
| 3312/2015 | kcb.vn, gói `https://kcb.vn/upload/2005611/20210723//Tre-em.rar` (rar sha 1b6db1425d1d6e4c), member "HD CĐ và ĐT một số bệnh thường gặp ở trẻ em 20150807.pdf" | `data/raw/3312_2015.pdf` (**tải trong task này** bằng `fetch_pdf --member "20150807\.pdf$"`, status downloaded) | a66c5e8bc460807c | 807 | lớp chữ PDF (glyph ƣ đã chuẩn hóa ở `norm`) | manifest: current; trang bìa tr.1 "Quyết định số 3312/QĐ-BYT ngày 07/8/2015" |

**Nguồn nước ngoài** (bản đệm `data/cache/foreign`, kiểm bằng `vnsoc.match.sources grep`; chỉ lưu giá trị và vị trí):

| Hệ thống | Nguồn | Phiên bản | sha256 (16) | Giá trị dùng |
|---|---|---|---|---|
| EU_UK | RCUK Emergency treatment of anaphylaxis (guidelines for healthcare providers) | 2021-05 | 1c07e3dd4e238e92 | tr.29: >12 tuổi và người lớn 500 µg; 6–12 tuổi 300 µg; 6 tháng–6 tuổi 150 µg; nhắc lại sau 5 phút (tr.7, 13, 29) |
| EU_UK | RCUK Anaphylaxis algorithm 2021 (tải lại qua `sources fetch`; mục chỉ mục đệm bị thiếu, file đệm còn) | 2021 | c7b75e76a1fdba09 | cùng các giá trị (ghi trong locator của mục RCUK) |
| OTHER | WAO Anaphylaxis Guidance 2020 (Europe PMC XML, PMC7607509) | 2020-10 | 1d6a6919aeb0a10e | 0,01 mg/kg, tối đa 0,5 mg; Bảng 6: <10 kg 0,01 mg/kg; 1–5 tuổi 0,15 mg; 6–12 tuổi 0,3 mg; thiếu niên và người lớn 0,5 mg; nhắc lại mỗi 5–15 phút |
| US | AAAAI/ACAAI 2023 practice parameter update | 2023 | a4177e78a117c345 | tr.4, 31: 0,01 mg/kg, tối đa 0,3 mg ở trẻ em/thiếu niên, 0,5 mg ở người lớn. Không có khoảng nhắc lại bằng số (tr.29) |
| EU_UK | EAACI 2021 | — | — | **Không ghi** (403 ở mọi nguồn, theo báo cáo trước; không thử lại vì đã hết lượt WebSearch) |

`pilot_merge.source_warnings` trả rỗng cho cả 6 mẩu: mọi con số nước ngoài đều có trong nguồn đã băm.

---

## 2. Lập luận DR8 theo quần thể (nguyên nhân phản vệ)

TT51/2017 là hướng dẫn **chung** cho mọi nguyên nhân. Các chương của hai QĐ kia có phạm vi như sau:

| Văn bản, trang PDF (số in) | Phạm vi | Liều tiêm bắp / khoảng nhắc lại | Dùng cho |
|---|---|---|---|
| 3312/2015 bài "Sốc phản vệ ở trẻ em", tr.106 (106) | **Chung mọi nguyên nhân** (mục 2 tr.103: thuốc, thức ăn, nọc côn trùng). "SPV" gồm cả thể nhẹ, trung bình, nặng (tr.105) | 0,01 mg/kg (0,01 ml/kg); trẻ không biết cân nặng 0,3 ml; nhắc lại 5–10 phút. Cùng giá trị ở tr.30, 32, 55 ("10mcg/kg") | Trẻ em, mọi nguyên nhân → -01, -02, -05, -06 |
| 3942/2014 ch.1 Dị ứng thuốc, mục 4.1, Bảng 3, tr.13 (8) | **Sốc phản vệ do thuốc**. 3942 không có chương phản vệ chung (mục lục tr.5). Ch.9 vắc xin (tr.71) chỉ ghi "Tham khảo phần bài SPV" | Người lớn 0,5–1 ml; trẻ 0,01 ml/kg, tối đa 0,3 ml; nhắc lại 5–15 phút (có thể sớm hơn 5 phút) | Nguyên nhân do thuốc → -01, -03, -04, -05, -06 |
| 3942/2014 ch.5 Dị ứng thức ăn, tr.48 (43) | **SPV do thức ăn** | Trẻ 10–25 kg: 0,15 mg; > 25 kg: 0,3 mg; người lớn 0,01 mg/kg, tối đa 0,5 mg; nhắc lại 5–15 phút | Chỉ -02 (do thức ăn) |
| 3942/2014 ch.10 Côn trùng đốt, tr.77 (72) | SPV do côn trùng đốt | Người lớn 0,3–0,5 mg; trẻ 0,01 mg/kg; nhắc lại cứ 10 phút | Không dùng (không có mẩu côn trùng đốt) |
| 3942/2014 ch.4 Mày đay – phù Quincke, tr.42 (37) | Không phải phản vệ | 0,3–0,5 mg; nhắc lại 15–20 phút | Không dùng |
| 3312/2015 bài ong đốt, tr.81 | SPV do ong đốt | "0,3ml (TDD)", tiêm dưới da | Không dùng |

Vì §3.5 loại câu hỏi thiếu thông tin quần thể khiến giá trị nước ngoài cũng đúng, **mọi mẩu đều ghi rõ nguyên nhân**. Một câu hỏi "phản vệ không rõ nguyên nhân" ở trẻ 10–25 kg sẽ làm 0,15 mg đúng theo 3942 chương thức ăn, nên không dựng mẩu cho quần thể đó.

---

## 3. Bảng mẩu

Trạng thái do `finalize()` tính. Mồi do `choose_decoy` chọn. Ảnh trang: `data/cache/page_images/TT51_2017_p009.png`, `…_p020.png`.

| id | slot / đơn vị | Quần thể | Tập VN (nguồn) | Nước ngoài | Trạng thái (dung sai, mồi) | Trang PDF span chính | verify_span | Kiểm ảnh |
|---|---|---|---|---|---|---|---|---|
| P-anaphylaxis_ocr-01 (hạt giống 15) | dose, µg; ctx 10 kg, 1 mg/ml, 1 mg/ống | 1–2 tuổi (18 tháng), 10 kg, phản vệ độ II–III **do thuốc**, tại cơ sở y tế, liều tiêm bắp đầu | 250 µg (TT51 PL III IV.1b tr.9) ∪ 200–333,3 µg (TT51 PL X tr.20) ∪ 0,01 mg/kg = 100 µg (3312 tr.106; 3942 tr.13) | RCUK 150 µg ✗ · WAO {100 µg ✓, 150 µg ✗} · Mỹ 100 µg ✓ | **conflict** (dung sai 25 µg; mồi 383,3 µg, quy tắc mirror_arith) | 9 (in 9) | LỖI vn[2] (DR8) | khớp ảnh tr.9 và tr.20 |
| P-anaphylaxis_ocr-02 (biến thể hạt giống 15) | như -01 | như -01 nhưng **do thức ăn** | như -01, thêm 0,15 mg (3942 ch.5 tr.48) | như -01, tất cả ✓ | **concordant** | 9 | LỖI vn[2], vn[3] (DR8) | khớp ảnh |
| P-anaphylaxis_ocr-03 (hạt giống 14, đối chứng) | dose, mg; ctx 60 kg | người lớn ≥ 18 tuổi, khoảng 60 kg, do thuốc | 0,5–1 mg (TT51 PL III IV.1e tr.9; = PL X "1/2 ống"; = 3942 tr.13) | RCUK 500 µg ✓ · WAO 0,5 mg ✓ · Mỹ 0,5 mg ✓ | **concordant** | 9 | **OK** | khớp ảnh (span cắt trước "1⁄2 - ] ống") |
| P-anaphylaxis_ocr-04 (mới, đối chứng) | duration, phút | người lớn, do thuốc, khoảng tiêm bắp nhắc lại | 3–5 phút (TT51 PL X tr.20; PL III IV.3 tr.9) ∪ 5–15 phút (3942 tr.13) | RCUK 5 phút ✓ · WAO 5–15 phút ✓ · Mỹ: không có số | **concordant** (concordant cả khi bỏ DR8) | 20 (in 20) | LỖI vn[1] (DR8) | khớp ảnh tr.20; OCR chèn '6' ngoài span |
| P-anaphylaxis_ocr-05 (mới, cùng họ -01) | dose, µg; ctx 20 kg | 5 tuổi, 20 kg, do thuốc | 300 µg (TT51 IV.1c tr.9) ∪ 200–333,3 µg (PL X) ∪ 0,01 mg/kg = 200 µg (3312; 3942 ≤ 0,3 ml) | RCUK 150 µg ✗ · WAO {200 µg ✓, 150 µg ✗} · Mỹ 200 µg ✓ | **conflict** (dung sai 25; mồi 383,3 µg) | 9 | LỖI vn[2] (DR8) | khớp ảnh ('1⁄3' là dấu gạch phân số U+2044, không sai số) |
| P-anaphylaxis_ocr-06 (đối chứng, bản nháp D4 trước đây) | dose, µg; ctx 35 kg | 10 tuổi, 35 kg, do thuốc | 500 µg (TT51 IV.1d) ∪ 200–333,3 µg (PL X) ∪ 350 µg (3312, không có liều tối đa) ∪ 300 µg (3942, tối đa 0,3 ml) | RCUK 300 ✓ · WAO {350 ✓, 300 ✓} · Mỹ 300 ✓ | **concordant** | 9 | LỖI vn[1] (tr.20), vn[2], vn[3] (DR8) | khớp ảnh |

`conflict_family` của -01 và -05: `anaphylaxis_child_im_adrenaline_rcuk_age_band_150ug`. Gốc khác biệt là RCUK chia bậc liều theo **tuổi** (6 tháng–6 tuổi: 150 µg), còn TT51 chia theo **cân nặng** và 3312/3942 tính theo mg/kg. Cả hai mẩu tính là **một** nhóm xung đột.

### 3a. Độ nhạy của trạng thái theo cách hiểu văn bản (tính bằng `finalize` + `choose_decoy`)

| Mẩu | DR8 (bản ghi) | (b) coi 3942/3312 là bản cũ (superseded) | (c) chỉ TT51 (PL III + PL X) | chỉ TT51 PL III |
|---|---|---|---|---|
| -01 | conflict | **indistinguishable** | conflict | conflict (mồi 350 µg) |
| -02 | concordant | indistinguishable | conflict | — |
| -03 | concordant | concordant | concordant | — |
| -04 | concordant | concordant | concordant | — |
| -05 | conflict | conflict | conflict | conflict (mồi 400 µg) |
| -06 | concordant | indistinguishable | conflict (chỉ nhờ WAO 350 µg, cách 16,7 µg) | conflict (mồi 650 µg) |

Chỉ -05 giữ được conflict ở mọi cách hiểu có ghi nguyên nhân do thuốc. -01 là conflict ở cả DR8 lẫn "chỉ TT51", nhưng thành indistinguishable nếu 3312/3942 bị coi là bản cũ.

---

## 4. Ứng viên bị loại và lý do

| Ứng viên | Lý do |
|---|---|
| Hạt giống 15 với quần thể "không nêu nguyên nhân" | §3.5: thiếu nguyên nhân thì 0,15 mg (3942 ch. thức ăn) cũng đúng theo Bộ Y tế, và RCUK 150 µg thành đúng. Thay bằng hai mẩu có nguyên nhân (-01 do thuốc, -02 do thức ăn) |
| Trẻ sơ sinh / < 10 kg (TT51: 0,2 ml) | TT51 gộp "sơ sinh hoặc < 10 kg", không khớp bậc tuổi RCUK (< 6 tháng: 100–150 µg; 6 tháng–6 tuổi: 150 µg). Cần quy tắc cân nặng–tuổi riêng |
| Thiếu niên > 12 tuổi (ví dụ 14 tuổi 45 kg) | Không dựng vì hết thời gian thí điểm. Tính nhẩm sơ bộ: TT51 500 µg = RCUK/WAO 500 µg; Mỹ tối đa 0,3 mg ở thiếu niên nằm trong PL X 200–333 → concordant. Có thể dựng làm đối chứng sau |
| Tiêm tĩnh mạch chậm người lớn 0,5–1 ml dd 1/10.000 (50–100 µg); truyền 0,1 µg/kg/phút | Khác slot (không phải tiêm bắp). Không có đối chiếu nước ngoài đã tải cho đúng slot |
| Theo dõi HA "3-5 phút/lần" (PL III IV.2) và "5-10 phút/lần" (PL X) | Là tần suất theo dõi, không phải liều. Ghi như **mâu thuẫn nội bộ TT51** (mục 5) |
| Liều bút tiêm tự động của Mỹ (0,1/0,15 mg cho < 15 kg; 0,15 mg cho 15–30 kg; AAP 0,15 mg cho 13–25 kg) | Bối cảnh kê đơn dùng ở cộng đồng, khác quần thể "tại cơ sở y tế, ống 1 mg/ml". Không ghi làm giá trị đối chiếu; đã nêu trong notes |
| Mẩu "bản cũ" TT08/1999 | Không tìm được bản chính thức (kcb.vn không có kết quả). Theo quy tắc, không điền `superseded` từ trí nhớ |
| EAACI 2021 | 403 ở mọi nguồn (báo cáo trước). Không ghi |

---

## 5. SAI LỆCH SO VỚI BỘ HẠT GIỐNG (§3.3, seed_conflicts.yaml)

1. **Dòng 15 (confirmed, pilot):**
   - Giá trị Việt Nam "0,25 ml (250 µg)" **đúng**: OCR trang 9, khớp ảnh.
   - Cột nước ngoài **sai một phần sau DR8**. "0,01 mg/kg (WAO)" **không còn là giá trị xung đột**, vì 3312/2015 (tr.106) và 3942/2014 (tr.13, chương dị ứng thuốc) đều ghi 0,01 mg/kg = 100 µg cho trẻ 10 kg. Chỉ RCUK 150 µg và mức 0,15 mg (1–5 tuổi) trong Bảng 6 của WAO còn nằm ngoài tập Việt Nam, và chỉ khi nguyên nhân **không phải thức ăn**.
   - Trạng thái "confirmed" chỉ đúng cho quần thể "phản vệ do thuốc". Với phản vệ do thức ăn: concordant. Nếu coi 3942/3312 là bản cũ: indistinguishable.
   - Ghi chú của dòng cần thêm `mg_per_ampoule: 1` và phải nêu **nguyên nhân** trong câu hỏi.
2. **Dòng 14 (removed, đối chứng):** đúng. Người lớn 0,5–1 mg; RCUK/WAO/Mỹ 0,5 mg → concordant (P-…-03).
3. **§3.3 "WAO/EAACI (0,01 mg/kg, tối đa 0,5 mg)":** WAO đúng. EAACI chưa kiểm được.
4. **Mâu thuẫn nội bộ Bộ Y tế** (báo cáo như kết quả phụ theo §1.2):
   - Trong TT51: PL III chia liều trẻ theo cân nặng (0,2/0,25/0,3/0,5 ml), còn PL X ghi "Trẻ em: 1/5-1/3 ống". Người lớn: PL III ghi 0,5–1 ml, PL X ghi 1/2 ống. Theo dõi HA: 3–5 phút/lần so với 5–10 phút/lần.
   - Giữa các văn bản: TT51 (theo cân nặng: 250 µg cho 10 kg) so với 3312/3942 (0,01 mg/kg: 100 µg), gấp **2,5 lần**. 3942 chương thức ăn (0,15 mg cho 10–25 kg) so với chương thuốc (0,01 ml/kg). Khoảng nhắc lại: TT51 3–5 phút, 3312 5–10 phút, 3942 5–15 phút, 3942 côn trùng 10 phút.
5. **Rủi ro quy nguồn chưa có trong thiết kế:** một giá trị nước ngoài (150 µg) có thể trùng giá trị Bộ Y tế **hiện hành cho quần thể bên cạnh** (khác nguyên nhân). Nhãn "indistinguishable" hiện chỉ xét bản đã bị thay và mồi. Vì vậy câu trả lời "0,15 mg" cho trẻ 10 kg phản vệ do thuốc sẽ được quy cho RCUK/WAO, dù có thể mô hình chỉ áp nhầm chương dị ứng thức ăn của 3942 (đề xuất ở mục 6.5).

---

## 6. Đề xuất sửa mã / config (chưa sửa: ngoài quyền task)

1. **DR8 nhiều văn bản trong `verify_span` / `pilot_merge` (chặn 5/6 mẩu):** cho mỗi mục `vn` chỉ ra span nguồn. Có thể chính thức hóa `extraction.dr8_sources` / `vn_item_checks`, hoặc thêm trường schema `vn_sources: [{vn_idx, guideline, page, span}]`.
   - `verify_atom` chấp nhận mục `vn[i]` khi đọc lại được từ span chính **hoặc** từ một span nguồn đã kiểm trên đúng văn bản/trang của nó.
   - `pilot_merge` và checklist HG1.2 in đủ các span phụ.
   - Khi sửa xong, chạy lại `verify_span`: theo kiểm thành phần ở đây, cả 6 mẩu sẽ qua.
   - Hiện có cả **"qua nhờ trùng số"**: mục PL X 200–333 µg "đọc lại được" từ span trang 9 vì 250 µg nằm trong khoảng. Quy tắc mới nên kiểm theo nguồn khai báo, không kiểm "bất kỳ số nào trong span".
2. **`normalize_vi`: đơn vị ml/kg.** "0,01 ml/kg" hiện bị đọc thành 0,01 ml = 10 µg. Lỗi này ảnh hưởng cả **chấm điểm**: câu trả lời "0,01 ml/kg" sẽ bị chấm sai và không quy được nguồn. Cần thêm alias `ml/kg` và cạnh quy đổi `ml/kg → mg/kg` (× mg_per_ml), rồi → mg (× weight_kg). Thêm test.
3. **`normalize_vi`: khoảng phân số "1/5-1/3 ống"** vẫn đọc thành "1 (giả định)" và 333 µg. Cần luật cho khoảng phân số (lỗi đã nêu ở báo cáo trước, chưa sửa).
4. **Số cân nặng bị đọc thành giá trị:** "< 10kg", "10 kg" → 10 µg (giả định). Nên thêm `kg` vào UNIT_ALIASES để các số này có đơn vị riêng và bị loại khi mẩu dùng đơn vị khối lượng thuốc.
5. **Nhãn quy nguồn cho "giá trị Bộ Y tế của quần thể bên cạnh":** thêm trường, ví dụ `vn_other_population: [{guideline, page, population, values}]`. Grader gắn nhãn riêng (không phải "trùng chuẩn nước ngoài"), và `conflict_status` báo cờ. Hoặc đưa vào phân tích độ nhạy của H1: loại các mẩu mà giá trị nước ngoài trùng giá trị Bộ Y tế ở quần thể khác. Cần ghi `docs/DECISIONS.md` trước đóng băng.
6. **Quy tắc mồi khi hòa khoảng cách:** `mirror_decoy` chọn cặp (nước ngoài, VN) đầu tiên có khoảng cách nhỏ nhất, nên mồi phụ thuộc thứ tự agent ghi `vn`. Với -01: RCUK 150 cách 100 µg và cách 200–333 µg **bằng nhau** (50 µg); thứ tự hiện tại cho mồi 383,3 µg, đảo thứ tự sẽ cho 50 µg. Đề xuất đăng ký trước một luật phá hòa tất định (ví dụ chọn mục VN có tâm gần giá trị nước ngoài nhất, rồi mục nhỏ nhất).
7. **OCR:** Tesseract đọc "1mg" thành "Img" và "1" thành "]". Đề xuất công cụ OCR in cảnh báo các token nghi ngờ (I, l, ], | cạnh đơn vị) ở trang có mẩu, để người kiểm tập trung vào đó ở HG1.2.
8. **Kho văn bản:** `data/raw/3312_2015.pdf` vừa tải (manifest `c4_resp_circulars` có dòng 3312/2015 với `downloaded: null`, cần cập nhật qua corpus-librarian). 3942/2014 chưa có dòng manifest trong `data/interim/manifest_parts/`. Cả hai cần được đưa vào danh sách xét DR8 cho chủ đề phản vệ.
9. **Chỉ mục bản đệm nước ngoài** `data/cache/foreign/index.json` thiếu khóa URL của RCUK algorithm (file đệm c7b75e76… vẫn còn). Có thể do nhiều agent ghi đè đồng thời. Nên ghi chỉ mục theo kiểu khóa file hoặc ghi nguyên tử.

---

## 7. Việc cho người ở HG1.2

1. **Kiểm số trên ảnh trang OCR (bắt buộc cho cả 6 mẩu):** mở `data/raw/TT51_2017.pdf`.
   - **Trang PDF 9** (số in 9), PL III mục IV.1: a) 0,2ml – 1/5 ống; b) 0,25ml – 1/4 ống; c) 0,3ml – 1/3 ống; d) > 30kg 0,5ml – 1/2 ống; e) 0,5-1ml. Mục IV.3: 3-5 phút/lần.
   - **Trang PDF 20** (số in 20), ô "TIÊM BẮP": Người lớn 1/2 ống; Trẻ em 1/5-1/3 ống; Nhắc lại sau mỗi 3-5 phút.
   - Agent đã so bằng ảnh và thấy khớp. Người cần xác nhận lại.
2. **Quyết định khoa học (trước khi dùng phản vệ cho H1):**
   - (i) 3942/2014 và 3312/2015 có được coi là văn bản hiện hành cho DR8 không, hay là bản bị TT51 thay trên thực tế (xem bảng 3a)?
   - (ii) DR8 có áp theo **nguyên nhân** như ở đây không (chương thuốc chỉ áp cho do thuốc, chương thức ăn chỉ áp cho do thức ăn)?
   - (iii) Xử lý rủi ro quy nguồn 150 µg (mục 5.5, đề xuất 6.5).
   - Ghi vào `docs/DECISIONS.md`.
3. **Phạm vi Bảng 3 của 3942 (tr.13):** chỉ cho SPV do thuốc, hay là "bài SPV" chung (ch.9 tr.71 trỏ tới "phần bài SPV")? Quyết định này không đổi tập giá trị trẻ em (trùng 3312) nhưng đổi tập cho người lớn và khoảng nhắc lại ở các nguyên nhân khác.
4. **Bác sĩ (HG3.9):**
   - "18 tháng, 10 kg" và "5 tuổi, 20 kg" có hợp lý không?
   - Ô "Trẻ em: 1/5–1/3 ống" của PL X có áp cho **mọi** trẻ (kể cả > 30 kg) không?
   - Bệnh viện Việt Nam đang dùng bảng cân nặng của TT51 hay 0,01 mg/kg?
5. **EAACI 2021** (Allergy 2022;77:357, doi 10.1111/all.15032): mở bản toàn văn, ghi liều tiêm bắp, khoảng nhắc lại và vị trí.
6. **TT08/1999** (bản bị TT51 thay): tìm bản chính thức (Công báo/vbpl). Nếu có, ghi giá trị trẻ em và khoảng nhắc lại vào `superseded`.
7. Xác nhận **không có văn bản thay thế/sửa đổi** 3942/2014, 3312/2015 và TT51/2017 (kiểm lược đồ trên vbpl.vn).

---

## 8. Sau kiểm toán (2026-09-26)

- Kiểm toán: `data/interim/pilot/anaphylaxis_ocr_verify.md` (integrity-auditor). Kết quả: pass 1 (-03), fix 5 (-01, -02, -04, -05, -06), reject 0.
- Người sửa: agent sửa lỗi (Claude). Góc nhìn lâm sàng trong mục này là AI, **không phải bác sĩ**.
- Chỉ ghi 2 file: `anaphylaxis_ocr.jsonl` và file này. Bản trước khi sửa lưu ở scratchpad của phiên, không nằm trong dự án.

### 8.1 Tôi tự kiểm lại bằng chứng trước khi sửa

| Bằng chứng | Cách kiểm | Kết quả |
|---|---|---|
| TT51 tr.9 và tr.20 (OCR) | `--page`, rồi `--image` và mở PNG bằng Read | **Khớp ảnh.** Các số trong span đúng: b) 0,25ml – 1/4 ống; c) 0,3ml – 1/3 ống; d) > 30kg 0,5ml – 1/2 ống; e) 0,5-1ml; IV.3 "3-5 phút/lần"; PL X "Người lớn: 1/2 ống - Trẻ em: 1/5-1/3 ống", "Nhắc lại sau mỗi 3-5 phút". Có thêm một lỗi OCR ngoài span: ảnh ghi "≥ 90mmHg", "≥ 70mmHg", OCR đọc thành ">" |
| TT51 tr.3 (Điều 6.2), tr.7 (PL II), tr.8 (PL III mục I, III) | `--page` | Điều 6.2: "phải xử trí cấp cứu phản vệ theo quy định tại Phụ lục III, Phụ lục IV". PL II: độ II "Huyết áp chưa tụt hoặc tăng"; độ III "Tuần hoàn: sốc, mạch nhanh nhỏ, tụt huyết áp". PL III mục III áp cho "mức nặng và nguy kịch (độ II, III)". Sơ đồ PL X: độ III tiêm bắp trước, sang tĩnh mạch khi "tiêm bắp adrenalin > 2 lần" chưa đáp ứng |
| 3942 tr.13, 48, 71; 3312 tr.103, 105, 106 | `--page` (lớp chữ) | Đúng như span DR8. 3312 tr.103 định nghĩa SPV có "hạ huyết áp, trụy tim mạch"; tr.105: cả 3 thể (nhẹ, trung bình, nặng) đều có HA giảm hoặc hạ |
| 3610/2015 tr.133, tr.166 (sha `2dcadc4999e397f0`) | `--page` | tr.166 (dị ứng dứa): "adrenalin tiêm bắp 0,3-0,5 mg/lần, lặp lại sau 5- 15 phút", không nêu tuổi. tr.133 (ong đốt): "0,3-0,5 ml dung dịch 1/1000"; **thêm:** "EpiPen Jr. chứa 0.15 mg" (dự phòng ong đốt, tiêm dưới da) |
| RCUK tr.29, WAO Bảng 6 và "5-15 min", AAAAI tr.3/4/7/20/31 | `sources grep` (bản đệm) | Đúng như bản ghi. AAAAI: FDA 0,15 mg bút tiêm cho 15–30 kg; AAP 0,15 mg cho 13–25 kg; khuyến cáo 12: 0,1 hoặc 0,15 mg cho trẻ < 15 kg |
| `verify_span` bản mã 11:51 | chạy lại | 6/6 OK (xác nhận phát hiện 2 của kiểm toán) |

### 8.2 Phát hiện kiểm toán: tôi đồng ý hay không, và đã làm gì

| # | Phát hiện | Đánh giá | Việc đã làm |
|---|---|---|---|
| 1 | -01, -05 chỉ là conflict khi DR8 tách theo nguyên nhân | **Đồng ý** (tôi tự tính lại, kết quả trùng) | **Giữ** trạng thái tính theo cách đọc (a) đã ghi, **không** tự chuyển sang (b). Thêm `extraction.dr8_reading_sensitivity` (tính bằng `choose_decoy` + `finalize`) cho 5 mẩu sửa, cờ trong notes, và ghi "CHƯA tính vào tập xác nhận H1 và chỉ tiêu mẩu xung đột cho tới khi có quyết định HG" (lý do ở 8.3) |
| 2 | `span_verified` lỗi thời | Đồng ý | `span_verified` đặt theo `verify_atom()`: 6/6 true. Bỏ câu "verify_span LỖI" khỏi notes |
| 2b | `vn_item_checks` ghi sai chỉ số ("vn [0]" ở 3942 tr.13) | Đồng ý | Tính lại **theo từng nguồn khai báo** (chỉ span của nguồn đó). Ghi đúng lý do: '0,01 ml/kg' bị đọc thành 10 µg. Ghi rằng mục 200–333 µg chỉ đọc lại được cận trên 333 từ '1/3 ống' |
| 3 | 3942/2014 chưa có dòng manifest | Đồng ý | Ngoài quyền (chỉ ghi 2 file). Chuyển thành đề xuất 8.6.4 |
| 4 | Checklist HG1.2 không in `dr8_sources`, không nhắc so ảnh OCR | Đồng ý | Đề xuất 8.6.1. Mục 8.7 liệt kê tay các span cần so |
| 5 | Bộ chấm đọc sai "0,01 ml/kg" và "1⁄3" | Đồng ý (tôi tự chạy `parse_values`: "0,01 ml/kg" → 10 µg; "1/5-1/3 ống" → 1 µg (giả định) và 333 µg) | Đề xuất 8.6.3 |
| -01.3, -02.3, -04.2, -05.5, -06.2 | `severity` "độ II–III" rộng hơn phạm vi "sốc phản vệ" của 3312/3942 | **Đồng ý.** Tôi kiểm lại TT51 PL II tr.7 và 3312 tr.103/105 | Thu hẹp còn "phản vệ độ III (nguy kịch) theo TT51 PL II: có sốc/tụt huyết áp, chưa ngừng tuần hoàn". Giá trị và trạng thái không đổi |
| -01.4 | Span có dòng a) của quần thể khác | Đồng ý | -01 và -02 cắt span còn "b) Trẻ khoảng 10 kg: 0,25ml (tương đương 1/4 ống)." (nguyên văn OCR tr.9, khớp ảnh). `ocr_visual_check` ghi lại |
| -01.5, -05.4 | Quy nguồn 150 µg: trùng bút tiêm tự động của Mỹ | Đồng ý (đã kiểm AAAAI) | Ghi vào notes. Vẫn **không** ghi làm giá trị đối chiếu (bút tiêm kê đơn dùng tại cộng đồng, khác quần thể "tại cơ sở y tế, ống 1 mg/ml") |
| -01.6 | WHO_global chưa được xét | **Đã giải quyết một phần** | Tìm được WHO Pocket Book 2013 bản PDF **đã có trong bản đệm** (xem 8.4) và ghi vào -01, -02, -05 |
| -02.2 | Nguyên nhân "do thức ăn" chưa đủ để tập VN duy nhất (3610 tr.166 dứa) | Đồng ý | `cause` = "lạc (đậu phộng) hoặc sữa bò — không phải dứa (bromelain)". Notes ghi 3610 tr.133, tr.166 đã kiểm |
| -02.4 | Nếu chọn (b), -02 trùng hẳn -01 | Đồng ý | Ghi vào notes: khi đó chỉ giữ một mẩu |
| -04.3 | RCUK 5 phút chỉ chạm biên | Đồng ý | Ghi "đối chứng yếu" trong notes |
| -03 | pass | Đồng ý | Không sửa. Mức độ vẫn là độ II–III: mọi nguồn cho người lớn đều ghi 0,5–1 mg, nên tập VN vẫn duy nhất. Chỉ chạy lại `finalize` (không đổi gì) |

### 8.3 Vì sao giữ trạng thái theo cách đọc (a) mà không chuyển sang (b)

- Quy tắc DR8 (đề cương §1.2) hợp giá trị của các văn bản hiện hành **cho CÙNG quần thể**.
  - 3942 tr.48 tự nêu phạm vi: "là thuốc quan trọng nhất trong điều trị **SPV do thức ăn**".
  - Mẩu -01 và -05 ghi rõ nguyên nhân do thuốc. Theo câu chữ, 0,15 mg không thuộc quần thể của hai mẩu này.
  - Theo cách đọc (c), căn cứ Điều 6.2 của TT51 (văn bản quy phạm pháp luật), hai mẩu cũng là conflict.
- Cách đọc (b) là cách đọc lâm sàng hợp lý: liều adrenalin tiêm bắp không đổi theo tác nhân. Có thêm hai dấu hiệu ủng hộ (b):
  - 3610 tr.166 gọi liều 0,3–0,5 mg là "phác đồ sốc phản vệ của Bộ Y tế", tức coi phác đồ là chung.
  - 3942 ch.9 (tr.71) trỏ về "phần bài SPV".
- Chọn giữa (a), (b) và (c) là **quyết định khoa học/pháp lý của người dùng**, và phải ghi `docs/DECISIONS.md` trước khi đóng băng mẩu. Agent tự chọn (b) cũng là chọn thay người dùng, giống như âm thầm giữ (a).
  - Vì vậy tôi giữ bản ghi (a) và gắn cờ cho cả hai mẩu, ghi rõ là **chưa dùng cho H1**.
  - Làm vậy không nhằm giữ chỉ tiêu: nếu người dùng chọn (b), chủ đề này **không còn mẩu xung đột nào**.

| Mẩu | (a) theo nguyên nhân (bản ghi) | (b) không phụ thuộc nguyên nhân | (c) chỉ TT51 (PL III + PL X), Điều 6.2 |
|---|---|---|---|
| -01 (10 kg, do thuốc) | conflict | **concordant** | conflict |
| -02 (10 kg, lạc/sữa bò) | concordant | concordant (trùng -01) | conflict |
| -03 (người lớn) | concordant | concordant (tập VN thêm 0,3–0,5 mg) | concordant |
| -04 (khoảng nhắc lại, người lớn) | concordant | concordant | concordant |
| -05 (20 kg, do thuốc) | conflict | **concordant** | conflict |
| -06 (35 kg, do thuốc) | concordant | concordant | conflict (WAO 350 µg nằm ngoài) |

Cách tính:
- Cột (b) thêm các giá trị cùng tuổi, cùng cân nặng từ 3942 ch.5 tr.48 (thức ăn) và ch.10 tr.77 (côn trùng).
- Cột (b) **không** đưa 3610 tr.166 và tr.133 (0,3–0,5 mg, không nêu tuổi) vào mẩu trẻ em, vì về lâm sàng đây là liều người lớn. Nếu chọn (b), người dùng cũng phải quyết định cách xử lý các giá trị không nêu tuổi này.

### 8.4 Phát hiện mới của agent sửa lỗi

1. **WHO_global: WHO Pocket book of hospital care for children, 2nd ed. (2013).**
   - Nguồn: PDF trong bản đệm, URL `https://iris.who.int/server/api/core/bitstreams/8f110da0-22e6-4ef1-90e4-c9f1b7daa363/content`, sha256 `e17581cf0829bea6…`. Trang mục IRIS handle 10665/81170 tải lại hôm nay, sha `98702ec07bd45084…`.
   - Nội dung: PDF tr.133 (số in 109), mục 4.6.4 ghi liều **cố định 0,15 ml dd 1:1000 tiêm bắp** cho "severe anaphylactic shock", nhắc lại mỗi 5–15 phút.
   - Ghi cho -01, -02, -05 (trẻ 10 kg và 20 kg). Trạng thái cả ba không đổi: -01 và -05 conflict (WHO 150 µg nằm ngoài tập VN), -02 concordant.
   - **Không ghi cho -06** (10 tuổi, 35 kg). Phạm vi sách là "young children" (tr.17), và bảng liều thuốc dừng ở cột "20-29 kg" (tr.379).
     - **Cờ:** nếu người kiểm cho rằng liều WHO áp cho mọi trẻ, -06 thành conflict (150 µg cách 200 µg là 50 µg, lớn hơn dung sai 8,33).
   - Chưa xác minh bản 2013 có phải bản hiện hành không (hết lượt WebSearch). Việc này để HG.
2. **Họ xung đột 150 µg là đồng thuận quốc tế, không riêng EU_UK.** RCUK (6 tháng–6 tuổi), WAO (1–5 tuổi), WHO Pocket Book (liều cố định trẻ em) và bút tiêm tự động của Mỹ đều cho 150 µg.
   - Khi phân tích H1/RQ2 cho họ `anaphylaxis_child_im_adrenaline_rcuk_age_band_150ug`, không nên quy câu trả lời 150 µg riêng cho RCUK. Tên họ vẫn giữ để không lệch với các file khác.
3. **Thêm một giá trị Bộ Y tế 0,15 mg ở quần thể bên cạnh:** 3610/2015 tr.133 "EpiPen Jr. chứa 0.15 mg" (dự phòng ong đốt, tiêm dưới da). Như vậy 0,15 mg xuất hiện trong **hai** văn bản Bộ Y tế hiện hành (3942 tr.48, 3610 tr.133), đều cho quần thể khác. Điều này củng cố đề xuất nhãn chấm "giá trị Bộ Y tế của quần thể bên cạnh" (6.5).
4. **3610 tr.166 gọi liều 0,3–0,5 mg/lần là "phác đồ sốc phản vệ của Bộ Y tế".** QĐ 3610 có từ 2015, trước TT51. Rất có thể câu này phản ánh phác đồ trước TT51, nhưng **chưa kiểm được** vì chưa có bản chính thức TT08/1999. Không dùng làm `superseded`.

### 8.5 Bảng mẩu sau sửa

Trạng thái do `finalize()` tính. Mồi do `choose_decoy` chọn: -01 và -05 cho 383,333 µg (`mirror_arith`), trùng bản trước, `check_decoy` = []. `verify_span` OK và `span_verified` = true cho cả 6 mẩu.

| id | slot | Quần thể (sau sửa) | Tập VN | Nước ngoài | Trạng thái | (a)/(b)/(c) | Trang span chính | Kiểm ảnh |
|---|---|---|---|---|---|---|---|---|
| -01 (hạt giống 15) | dose, µg | 18 tháng, 10 kg, **độ III**, do thuốc, tại cơ sở y tế | 250 (TT51 tr.9) ∪ 200–333 (TT51 tr.20) ∪ 0,01 mg/kg = 100 (3312 tr.106; 3942 tr.13) | RCUK 150 ✗ · WAO {100 ✓, 150 ✗} · Mỹ 100 ✓ · **WHO 150 ✗** | conflict (dung sai 25; mồi 383,3) · **giữ ngoài H1** | conflict / concordant / conflict | 9 (span chỉ dòng b) | khớp tr.9, tr.20 |
| -02 | dose, µg | như -01, **lạc hoặc sữa bò** (không phải dứa) | như -01 ∪ 0,15 mg (3942 tr.48) | tất cả ✓ (kể cả WHO 150) | concordant | concordant / concordant / conflict | 9 (span chỉ dòng b) | khớp |
| -03 (hạt giống 14) | dose, mg | người lớn, độ II–III, do thuốc (không sửa) | 0,5–1 mg | RCUK/WAO/Mỹ 0,5 mg ✓ | concordant | concordant ×3 | 9 | khớp |
| -04 | duration, phút | người lớn, **độ III**, do thuốc | 3–5 (TT51) ∪ 5–15 (3942 tr.13) | RCUK 5 ✓ · WAO 5–15 ✓ | concordant | concordant ×3 | 20 | khớp |
| -05 | dose, µg | 5 tuổi, 20 kg, **độ III**, do thuốc | 300 ∪ 200–333 ∪ 0,01 mg/kg = 200 | RCUK 150 ✗ · WAO {200 ✓, 150 ✗} · Mỹ 200 ✓ · **WHO 150 ✗** | conflict (dung sai 25; mồi 383,3) · **giữ ngoài H1** | conflict / concordant / conflict | 9 | khớp ("1⁄3" là U+2044) |
| -06 | dose, µg | 10 tuổi, 35 kg, **độ III**, do thuốc | 500 ∪ 200–333 ∪ 350 (3312) ∪ 300 (3942) | RCUK 300 ✓ · WAO {350 ✓, 300 ✓} · Mỹ 300 ✓ · WHO: không áp (cờ) | concordant | concordant / concordant / conflict | 9 | khớp |

**Tóm tắt trung thực:**
- **Không có mẩu xung đột nào đứng vững dưới mọi cách đọc.** -01 và -05 là conflict dưới (a) và (c), concordant dưới (b).
- Nếu người dùng chọn (b), phản vệ đóng góp **0** mẩu xung đột.
- Nếu chọn (a) hoặc (c), phản vệ đóng góp **1 họ** xung đột (2 mẩu), kèm cảnh báo quy nguồn (8.4.2, 8.4.3).

### 8.6 Đề xuất sửa mã/config (cập nhật; chưa sửa, ngoài quyền)

1. **`pilot_merge.checklist()`:**
   - In mọi `extraction.dr8_sources` (văn bản, trang, span).
   - Với trang OCR, in dòng "SO SỐ VỚI ẢNH TRANG N" kèm đường dẫn PNG.
2. **`verify_span`:**
   - Kiểm theo **nguồn khai báo** của từng mục `vn` (ví dụ `dr8_sources[k].vn_idx`), không gộp số của mọi span. Hiện mục 200–333 µg vẫn có thể "khớp" nhờ "0,3 ml" của 3312 (trẻ không biết cân nặng).
   - `pilot_merge` đặt `span_verified` theo kết quả `verify_atom`.
3. **`normalize_vi`:**
   - Thêm đơn vị `ml/kg`, quy đổi qua `mg_per_ml` rồi `weight_kg`.
   - Map U+2044 "⁄" thành "/".
   - Đọc khoảng phân số "1/5-1/3 ống".
   - Thêm `kg` vào UNIT_ALIASES. Kèm test cho từng mục.
4. **Manifest (corpus-librarian):**
   - Lập dòng 3942/2014: kcb.vn `Mien-dich.rar`, PDF sha `4be16be0fe6812f4…`, `partially_amended_by: ['1851/2020']` (chỉ 2 bài hen). Sha của gói rar lấy theo kiểm toán (`ab82a392…`); tôi chưa tự tính.
   - Cập nhật trường `downloaded` của 3312/2015.
   - Nếu thiếu các dòng này, 5 mẩu dựa vào 3942 sẽ nằm ngoài kho đóng băng ngày 15/10.
5. **Nhãn chấm "giá trị Bộ Y tế của quần thể bên cạnh"** (như 6.5): nay có hai văn bản chứa 0,15 mg (3942 tr.48, 3610 tr.133).
6. **Luật phá hòa tất định cho `mirror_decoy`** (như 6.6). Kiểm toán xác nhận: đảo thứ tự `vn` của -01 cho mồi 50 µg, trùng liều tiêm tĩnh mạch chậm người lớn của TT51.
7. **`pilot_merge` / chọn tập H1:**
   - Đọc `extraction.dr8_reading_sensitivity`. Mẩu có trạng thái khác nhau giữa các cách đọc thì **không** vào tập xác nhận H1, cho tới khi `docs/DECISIONS.md` chốt cách đọc.
   - Khi đã chốt, mã tính lại trạng thái theo cách đọc đó, không sửa tay.
8. **Quy nguồn theo họ xung đột:** cho phép một họ gắn nhiều hệ thống cùng giá trị (EU_UK + OTHER + WHO_global + US bút tiêm), để phân tích RQ2 không quy 150 µg riêng cho một hệ thống.

### 8.7 Việc cho người (HG), cập nhật

1. **Quyết định DR8 cho liều adrenalin tiêm bắp** (ghi `docs/DECISIONS.md` trước khi đóng băng mẩu):
   - Chọn (a) tách theo nguyên nhân, (b) không phụ thuộc nguyên nhân, hoặc (c) chỉ TT51 theo Điều 6.2 ("Bác sĩ, y sỹ, điều dưỡng viên, hộ sinh viên, kỹ thuật viên phải xử trí cấp cứu phản vệ theo quy định tại Phụ lục III, Phụ lục IV", OCR tr.3).
   - Kèm: 3942/3312 có còn "hiện hành" cho phản vệ không? Nếu chọn (b), xử lý thế nào với giá trị không nêu tuổi (3610 tr.166, tr.133)?
2. **HG1.2** (checklist tự động chưa in các mục này):
   - **Ảnh TT51 tr.9:** b) 0,25ml – 1/4 ống; c) 0,3ml – 1/3 ống; d) > 30kg 0,5ml – 1/2 ống; e) 0,5-1ml; mục 3 "3-5 phút/lần".
   - **Ảnh TT51 tr.20:** "Người lớn: 1/2 ống - Trẻ em: 1/5-1/3 ống", "Nhắc lại sau mỗi 3-5 phút".
   - **Span DR8 (lớp chữ):** 3312 tr.106 "0,01 mg/kg … 0,01 ml/kg … 0,3 ml … 5 - 10 phút"; 3942 tr.13 "0,5 - 1 ml … 0,01 ml/kg, tối đa không quá 0,3 ml … 5-15 phút"; 3942 tr.48 "Trẻ em nặng 10-25kg: adrenaline 0,15mg".
3. **WHO:**
   - Xác nhận Pocket Book 2013 (2nd ed.) có còn là bản hiện hành không, hay đã có bản mới hơn.
   - Liều cố định 0,15 ml có áp cho trẻ 10 tuổi, 35 kg không? Câu trả lời quyết định -06.
   - Nếu có thể, xem thêm WHO Model Formulary for Children.
4. **EAACI 2021:** mở bản toàn văn, ghi liều và vị trí (bản đệm hiện 403).
5. **Bác sĩ thật (HG3.9):**
   - Liều adrenalin tiêm bắp có phụ thuộc tác nhân không, theo thực hành tại Việt Nam?
   - Bệnh viện dùng bảng cân nặng của TT51 hay 0,01 mg/kg?
   - Quần thể "18 tháng, 10 kg" và "5 tuổi, 20 kg" có hợp lý không?
6. **TT08/1999:** tìm bản chính thức. Nếu có, ghi `superseded`, và đối chiếu câu "phác đồ sốc phản vệ của Bộ Y tế: 0,3-0,5 mg/lần" ở 3610 tr.166.

### 8.8 Kiểm cuối (chạy sau khi ghi file)

| Lệnh | Kết quả |
|---|---|
| `vnsoc.schemas atom data/interim/pilot/anaphylaxis_ocr.jsonl` | OK 6 dòng hợp lệ |
| `vnsoc.extract.verify_span data/interim/pilot/anaphylaxis_ocr.jsonl` | OK cả 6, 0 mẩu không đạt |
| `pilot_merge.check()` và `source_warnings()` (gọi trực tiếp, chỉ đọc) | `[]` cho cả 6 mẩu (kể cả 3 bản ghi WHO_global mới) |
| `finalize(atom) == atom` | True cho cả 6 |
| `check_decoy` | `[]` cho cả 6 |
| sha256 PDF | TT51 `cab611be9dd14312`, 3942 `4be16be0fe6812f4`, 3312 `a66c5e8bc460807c`, 3610 `2dcadc4999e397f0`. Meta OCR TT51 khớp sha PDF (Tesseract 5.4.0, vie+eng, 300 dpi) |
