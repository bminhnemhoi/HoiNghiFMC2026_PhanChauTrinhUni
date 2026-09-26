# Kiểm toán độc lập — Phản vệ, adrenalin tiêm bắp (ID = anaphylaxis)

Ngày: 2026-09-26 · Người kiểm: integrity-auditor (Claude, AI). Góc nhìn lâm sàng trong file này là **AI đóng vai bác sĩ Việt Nam, không phải bác sĩ thật**. Chưa có người nào kiểm các nội dung ở đây.

Phạm vi kiểm:
- `data/interim/pilot/anaphylaxis.jsonl`: 0 byte, tạo lúc 10:59.
- `data/interim/pilot/anaphylaxis_report.md`: tạo lúc 11:01.

Tôi chỉ đọc dữ liệu. File duy nhất tôi ghi trong dự án là file này. Các thao tác phụ (tải vào scratchpad và cache) được kê ở mục 8.

## 0. Kết luận ngắn

- JSONL rỗng, không có mẩu nào để cho qua. Tôi kiểm **6 ứng viên** mà báo cáo đã loại: D1, D2, D3, D4, D5 và dòng "trẻ < 10 kg".
- Kết quả: **pass 0 · fix 3 · reject 3**.
  - **Giữ loại (reject): D1, D4, D5.** Riêng D5, lý do loại trong báo cáo sai, xem mục 3.
  - **Mở lại (fix): D2, D3 và dòng trẻ < 10 kg.**
- Lý do (i) "TT51 là bản quét nên không kiểm span được" **đã lỗi thời**:
  - Sidecar OCR `data/interim/ocr/TT51_2017/` được tạo lúc 11:15–11:17 (Tesseract 5.4, vie+eng, 300 dpi, meta.json khớp sha256 `cab611be…` của PDF).
  - Từ 11:22, `verify_span` dùng sidecar này. Kết quả: `--page TT51/2017 9` nay trả về văn bản, và `--find TT51/2017 "0,25ml"` trả về `[9, 10]`.
  - Giá trị lấy từ OCR vẫn phải có **người** so với ảnh trang (§3.1 đề cương; docstring của `ocr.py`).
- Phát hiện chính của báo cáo (dòng hạt giống 15 **không** phải xung đột sạch) **đứng vững**:
  - Tôi đã tự kiểm lại nguyên văn QĐ 3942/2014 (trang PDF 13, 48, 77) và QĐ 3312/2015 (trang PDF 29, 30, 55, 106).
  - Báo cáo **bỏ sót** Điều 6.2 của TT51. Điều này bắt buộc nhân viên y tế xử trí phản vệ theo Phụ lục III và IV, và rất quan trọng cho quyết định DR8.

## 1. Hai lệnh kiểm bắt buộc

```
vnsoc.schemas atom data/interim/pilot/anaphylaxis.jsonl   → "OK 0 dòng hợp lệ (atom)", exit 0
vnsoc.extract.verify_span data/interim/pilot/anaphylaxis.jsonl → "OK: 0 mẩu không đạt", exit 0
```
Cả hai qua **chỉ vì file rỗng**. Báo cáo đã nói đúng điều này.

## 2. Công cụ đã thay đổi SAU khi báo cáo được viết (11:01)

| Giờ | Thay đổi | Hệ quả cho báo cáo |
|---|---|---|
| 11:13 | Thêm `src/vnsoc/extract/ocr.py` | Máy đã có OCR (báo cáo viết "máy chưa có OCR") |
| 11:15–11:17 | Sidecar OCR TT51, 20/20 trang | Kiểm span được trên văn bản OCR (cờ `ocr=True`) |
| 11:17 | Sửa `decoys.py::mirror_decoy`: quy đổi đơn vị trước khi phản chiếu; thêm `test_mirror_converts_units_first` (ghi công cho agent thí điểm phản vệ) | Lỗi mục 6.1 của báo cáo **đã sửa**. Tôi chạy lại: không còn tái hiện "999.99 ug" |
| 11:20 | `fetch_pdf` nhận bó .rar (`--member`), và `data/raw/3942_2014.pdf` xuất hiện | sha256 `4be16be0fe6812f4…` = đúng bản PDF trong .rar mà báo cáo đã giải nén. Các span của 3942 nay kiểm được bằng `verify_span` |
| 11:22 | `verify_span` dùng OCR cho trang không có lớp chữ, và `norm()` sửa "ƣ"→"ư" | Lý do (i) của báo cáo lỗi thời |

## 3. Từng ứng viên

### anaphylaxis-D1 (nháp; seed_row 15; trẻ khoảng 10 kg) — verdict: **reject** (không dùng làm xung đột H1 cho tới khi có quyết định HG)

**Giá trị Việt Nam đúng.**
- Ảnh trang 9 (tôi render ở 170 dpi và đọc bằng mắt): "b) Trẻ khoảng 10 kg: 0,25ml (tương đương 1/4 ống)."
- OCR trang 9 khớp nguyên văn.
- Span đọc lại được: `missing_vn = []`.

**Giá trị nước ngoài đúng** (kiểm bằng `sources grep`, dùng cache):

| Nguồn | Hệ thống | sha256 | Vị trí | Giá trị |
|---|---|---|---|---|
| RCUK 2021 | EU_UK | `1c07e3dd…` | tr. 29 | 6 tháng–6 tuổi: 150 µg |
| WAO 2020 | OTHER | `1d6a6919…` | Bảng 6 | 0,01 mg/kg, tối đa 0,5 mg; "children aged 1-5 years 0.15 mg"; "infants under 10 kg 0.01 mg/kg" |
| AAAAI/ACAAI 2023 | US | `a4177e78…` | tr. 4, 31 | 0,01 mg/kg, tối đa 0,3 mg ở trẻ em |

Chạy `finalize`/`choose_decoy` tái hiện đúng các số của báo cáo:

| Cách hiểu tập VN | Trạng thái | Mồi | Dung sai |
|---|---|---|---|
| A (chỉ PL III) | conflict | 350 µg | 50 |
| A′ (PL III + PL X) | conflict | 383 µg | 25 |
| B (hợp DR8 với QĐ 3942 và 3312) | concordant | — | — |
| Coi 3942/3312 là bản bị thay | indistinguishable | — | — |

**Lý do loại, đã sửa lại:**
1. Lý do "bản quét" không còn đúng (mục 2).
2. Lý do nội dung đúng. Tôi đã tự kiểm nguyên văn:
   - **QĐ 3942/2014:**
     - Trang PDF 13: "0,01 ml/kg, tối đa không quá 0,3 ml /lần ở trẻ em", "5-15 phút/lần".
     - Trang PDF 48: "Trẻ em nặng 10-25kg: adrenaline 0,15mg tiêm bắp".
     - Trang PDF 77: "Trẻ em: 0,01mg/kg TB", "cứ 10 phút/lần".
   - **QĐ 3312/2015** (bản trong .rar kcb.vn, sha256 PDF `a66c5e8bc460807c…`):
     - Trang 106: "tiêm bắp Adrenalin 1/1000 (0,01 mg/kg), 0,01 ml/kg", "nhắc lại 5 - 10 phút".
     - Trang 30: "adrenalin TB liều 10mcg/kg".
     - Trang 55: "Tiêm bắp adrenalin 10µg/kg".
     - Thêm trang 29, mà báo cáo không nêu: "adrenalin 1‰ 10µg/kg, tiêm bắp".
   - kcb.vn (WebFetch hôm nay) ghi 3942/2014 và TT51 là "Đã có hiệu lực", còn 3312/2015 là "Active". Không trang nào nêu văn bản thay thế.

**Vấn đề báo cáo bỏ sót:**
- **TT51 Điều 6.2** (ảnh trang 3) ghi: bác sĩ, y sỹ, điều dưỡng… "phải xử trí cấp cứu phản vệ theo quy định tại Phụ lục III, Phụ lục IV". PL III mục I.1 (OCR trang 8) áp cho "Tất cả trường hợp phản vệ".
  - TT51 là văn bản quy phạm pháp luật và ban hành sau 3942/3312. Đây là lý lẽ pháp lý mạnh cho cách hiểu (b) "đã bị thay trên thực tế".
  - Ở cả (a) lẫn (b), dòng 15 **không** dùng được cho H1 xác nhận.
  - Cách (c) (bỏ hai QĐ khỏi kho) trái §1.2: mâu thuẫn nội bộ phải được báo cáo, không loại âm thầm. Cách (c) cũng trái trạng thái "Đã có hiệu lực" trên kcb.vn.
- **Văn bản tiền nhiệm TT08/1999/TT-BYT chưa được tra.** TT51 Điều 7.2 làm văn bản này hết hiệu lực. Cần tra giá trị liều trẻ em của TT08/1999 từ nguồn chính thức.
  - Nếu TT08/1999 ghi 0,01 mg/kg (**chưa kiểm, không dùng làm dữ liệu**), dòng 15 thành indistinguishable ngay cả theo cách (c).
- **Quần thể nằm đúng biên.** "Trẻ 1 tuổi, 10 kg" ở đúng biên tuổi WAO ("1-5 years") và đúng biên cân nặng ("under 10 kg").

**Fix, nếu sau này dựng lại:**
- `population`: "trẻ 18 tháng, 10 kg, phản vệ độ II–III, tại cơ sở y tế", để tránh biên.
- `section`: "Phụ lục III, mục IV.1.b"; `page`: 9; `span`: "b) Trẻ khoảng 10 kg: 0,25ml (tương đương 1/4 ống)."
- `valid_from`: "2018-02-15". Điều 7.1, ảnh trang 3. Trang kcb.vn ghi 29/12/2017 là sai với văn bản.
- `extraction.ocr`: true, kèm người kiểm ảnh trang.
- `vn` theo quyết định HG. Bắt buộc gồm cả PL X (trang 19–20). Hiện chưa mã hóa được, xem Vấn đề chung G3.
- `superseded`: ghi giá trị TT08/1999 sau khi tra.
- `conflict_family` chỉ đặt sau quyết định HG.

### anaphylaxis-D2 (nháp; seed_row 14; người lớn) — verdict: **fix** (dựng được ngay, làm đối chứng concordant)

**Giá trị đã kiểm:**
- VN: ảnh trang 9 ghi "e) Người lớn: 0,5-1ml (tương đương 1/2 - 1 ống)". OCR đọc sai "1 ống" thành "] ống".
- PL X (ảnh trang 19 và 20): "Người lớn: 1/2 ống".
- Nước ngoài:
  - RCUK tr. 29: người lớn và trẻ > 12 tuổi 500 µg.
  - WAO: 0,01 mg/kg, tối đa 0,5 mg; Bảng 6: thiếu niên và người lớn 0,5 mg.
  - Mỹ tr. 4 và 31: tối đa 0,5 mg ở người lớn.

**Vấn đề báo cáo không nêu: trạng thái phụ thuộc cân nặng.**
- Chạy lại với `weight_kg` = 45: WAO/Mỹ 0,01 mg/kg thành 450 µg, nằm **ngoài** 0,5–1 mg, nên thành **conflict** (mồi 1050 µg).
- Với 60 kg: concordant.
- Người lớn Việt Nam 45 kg rất thường gặp, nên câu hỏi phải nêu cân nặng.

**Fix:**
- `population`: {nhóm tuổi: người lớn, cân nặng: 60 kg, bối cảnh: cơ sở y tế}.
- `context`: {weight_kg: 60, mg_per_ml: 1, mg_per_ampoule: 1}; `unit`: "mg".
- `span`: "e) Người lớn: 0,5-1ml", có trên trang 9. Bỏ phần có ký tự OCR lỗi "]". Đã thử: `missing_vn = []`.
- `section`: "Phụ lục III, mục IV.1.e".
- Ghi giá trị Mỹ và WAO dưới dạng **đã áp trần**, ví dụ 0,5 mg ở 60 kg, vì `ValueItem` không có trường "tối đa".
- `foreign`:
  - RCUK 2021-05, `1c07e3dd…`, tr. 29.
  - WAO 2020, url Europe PMC XML, `1d6a6919…`, "Bảng 6".
  - AAAAI/ACAAI 2023 (xuất bản 2024), `a4177e78…`, tr. 4/31.
- `extraction.ocr`: true.
- Cần người so ảnh trang 9 trước khi `span_verified`.

### anaphylaxis-D3 (nháp; khoảng nhắc lại liều tiêm bắp) — verdict: **fix** (dựng được ngay; nên đổi span sang PL X trang 20)

**Giá trị đã kiểm:**
- Ảnh trang 9: "3-5 phút/lần". OCR trang 9 đọc sai thành "3-5 phúVlần"; parser vẫn đọc ra 3–5 phút nhờ đơn vị "assumed", nhưng rất mong manh.
- OCR trang 20 sạch: "Nhắc lại sau mỗi 3-5 phút". `--find` trả `[20]`; `missing_vn = []`.
- RCUK: "after 5 minutes" (tr. 7, 13, 29).
- WAO: "every 5-15 min".

**Vấn đề:**
- WAO 5–15 chỉ được tính concordant vì `_gap` của hai khoảng chạm nhau ở đúng 5 phút bằng 0. Một câu trả lời "10–15 phút" theo WAO là sai theo Bộ Y tế, nhưng mẩu vẫn mang nhãn concordant.
- Đối chứng này yếu. Nên dựa chủ yếu vào RCUK (5 phút nằm trong 3–5).
- Nên ghi chú cho người làm quy tắc chấm (khớp theo chồng lấn).

**Fix:**
- `section`: "Phụ lục X, mục II (sơ đồ tóm tắt), ô Tiêm bắp"; `page`: 20; `span`: "Nhắc lại sau mỗi 3-5 phút".
- `slot_type`: "duration"; `unit`: "min".
- `extraction.ocr`: true, kèm người kiểm ảnh trang 20.

### anaphylaxis-D4 (nháp; trẻ > 30 kg, ví dụ 10 tuổi 35 kg) — verdict: **reject** (giữ loại)

**Đã kiểm:**
- Ảnh trang 9: "d) Trẻ > 30kg: 0,5ml".
- Ảnh trang 19 và 20: "Trẻ em: 1/5-1/3 ống".
- RCUK 6–12 tuổi: 300 µg. Mỹ: tối đa 0,3 mg ở trẻ em và thiếu niên. WAO: 0,01 mg/kg, tối đa **0,5 mg**, nên 350 µg là đúng theo WAO; Bảng 6: 6–12 tuổi 0,3 mg.

Chạy lại:
- A: conflict, mồi 650 µg.
- A′: conflict chỉ nhờ WAO 350, **dung sai 8,5 µg**. Báo cáo ghi 8,3 do dùng 333,3 thay vì 333. Thực tế là không phân biệt được.
- B: concordant. 3942 trang 13 cho tối đa 0,3 ml ở trẻ em; trang 48 cho > 25 kg 0,3 mg.

Kết luận của báo cáo đúng.

### anaphylaxis-D5 (nháp; trẻ khoảng 20 kg, 0,3 ml) — verdict: **reject** (giữ loại, nhưng **lý do trong báo cáo sai**)

Báo cáo viết: "300 µg trùng RCUK/WAO cho 6–12 tuổi, không có xung đột". Điều này chỉ đúng khi giả định trẻ ≥ 6 tuổi.

Trẻ 20 kg thường khoảng 5–6 tuổi. Với trẻ **5 tuổi, 20 kg**:
- RCUK: 150 µg (6 tháng–6 tuổi). WAO: 1–5 tuổi 0,15 mg, và 0,01 mg/kg = 200 µg.
- Chạy lại:
  - A: conflict, mồi 400 µg.
  - A′: conflict (RCUK 150 nằm ngoài {300, 200–333}), mồi 383 µg.
  - B: concordant (3942 trang 48: 10–25 kg 0,15 mg; 0,01 mg/kg = 200 µg).

Như vậy D5 có **cùng cấu trúc với D1**, không phải "không có xung đột". Thêm nữa, "khoảng 20 kg" nằm đúng biên 6 tuổi của RCUK, nên quần thể không xác định được một giá trị duy nhất.

**Sửa báo cáo, mục 3:** lý do loại là "phụ thuộc quyết định DR8 như D1; cân nặng 20 kg ở biên 6 tuổi của RCUK".

### anaphylaxis-D6 (nháp; "trẻ sơ sinh hoặc < 10 kg: 0,2 ml") — verdict: **fix** (mở lại để xét; lý do loại trong báo cáo không đứng)

**Đã kiểm:**
- Ảnh trang 9: "a) Trẻ sơ sinh hoặc trẻ < 10kg: 0,2ml (tương đương 1/5 ống)". Span đọc lại được: `missing_vn = []`.
- RCUK tr. 29: < 6 tháng 100–150 µg. WAO: < 10 kg 0,01 mg/kg. Mỹ: 0,01 mg/kg.

**Lý do của báo cáo** ("TT51 gộp sơ sinh hoặc < 10 kg nên quần thể không khớp dải tuổi RCUK") **không đứng.** Câu hỏi "trẻ 4 tháng, 6 kg" thuộc cả TT51 mục a lẫn RCUK < 6 tháng.

Chạy lại với 6 kg:

| Cách hiểu tập VN | Trạng thái | Mồi | Dung sai |
|---|---|---|---|
| A | conflict | 250–300 µg | 25 |
| A′ | conflict | **cả 3 quy tắc mồi đều trùng tập VN, nên không có mồi** | — |
| B (thêm 0,01 mg/kg = 60 µg) | conflict với RCUK | "4–54 µg" (mirror_geom) | 3 |

Đây là **ứng viên duy nhất mà xung đột với RCUK sống qua mọi cách hiểu DR8**. Nhưng:
- Mồi hỏng hoặc vô lý lâm sàng. Mồi 4–54 µg trái yêu cầu "hợp lý như nhau" ở §1.2.
- Theo cách A, mồi 250–300 µg lại nằm trong khoảng PL X "Trẻ em 1/5–1/3 ống", tức là một giá trị Bộ Y tế cho trẻ em.

Góc nhìn lâm sàng (AI đóng vai):
- 200 µg cho trẻ 6 kg bằng khoảng 3,3 lần mức 0,01 mg/kg; cho trẻ sơ sinh 3 kg là khoảng 6,7 lần.
- Tình huống thực tế hay gặp nhất là phản vệ sau tiêm chủng lúc 2–4 tháng tuổi, tại điểm tiêm chủng. Đó chính là nơi TT51 được áp dụng. Nên liên kết với chủ đề immunization.

**Fix:**
- Đưa vào danh sách xét lại, ghi rõ vấn đề mồi.
- Giao người làm thống kê hoặc HG quyết định: quy tắc mồi có cần phản chiếu qua **mép xa** của tập VN không, nếu đăng ký trước còn cho sửa.
- Tra TT08/1999.
- Cần bác sĩ thật (HG3.9) xác nhận câu hỏi "trẻ 4 tháng 6 kg" hợp lý.
- Nếu dựng: `section` "Phụ lục III, mục IV.1.a", `page` 9, `span` như trên, `context` {weight_kg: 6, mg_per_ml: 1, mg_per_ampoule: 1}.

## 4. Kiểm các khẳng định trong báo cáo

| Khẳng định | Kết quả kiểm | Bằng chứng |
|---|---|---|
| TT51 kcb.vn là bản quét, 20 trang, sha256 `cab611be9dd14312…`, chỉ có lớp chữ chữ ký số | **Đúng** | PyMuPDF: trang 1 có 104 ký tự ("Chứng thư: Bộ Y tế · Ngày ký: 19/01/2018"), trang 2–20 có 0 ký tự |
| Giá trị PL III mục IV.1a–e và IV.3 (3–5 phút) | **Đúng** | Ảnh trang 9 |
| PL X: người lớn 1/2 ống, trẻ em 1/5–1/3 ống, nhắc lại 3–5 phút, theo dõi mạch/huyết áp 5–10 phút/lần | **Đúng** | Ảnh trang 19 và 20 |
| TT51 chỉ làm hết hiệu lực TT08/1999 | **Đúng** | Ảnh trang 3, Điều 7.2 |
| Trích 3942 (trang 13, 48, 77) | **Đúng nguyên văn** | `verify_span --page 3942/2014` |
| Trích 3312 (trang 106, 30, 55) | **Đúng nguyên văn** | Bản giải nén trong scratchpad, sha256 PDF `a66c5e8b…`; rar `1b6db142…` |
| 3312: "µ bị mất, ví dụ trang 29 ra 10g/kg" | **Gần đúng** | "µ" thực ra là ký tự riêng U+F06D của font Symbol, `norm()` không đổi được |
| RCUK 2021, WAO 2020, Mỹ 2023: các giá trị như bảng 1b | **Đúng** | `sources grep` (sha256 như bảng mục 3). Bản sơ đồ thuật toán RCUK `c7b75e76…` có trên đĩa và có đủ các giá trị, nhưng **mất mục trong `index.json`** (xem G6) |
| Không có bản RCUK mới hơn | **Đúng** tại ngày tải | Trang RCUK `eb860f98…` ghi bản gần nhất phát hành 5/2021 |
| EAACI 2021: 403 | **Đúng** | Tôi thử lại Wiley pdfdirect: 403. Europe PMC: isOpenAccess N, không có PMCID |
| Lỗi `mirror_decoy` quy đổi đơn vị | **Đúng lúc viết, nay đã sửa** | Mục 2 |
| `normalize_vi`: "1/5-1/3 ống" đọc thành 1 µg (assumed) + 333 µg; "10 kg" đọc thành 10 µg (assumed) | **Đúng** | Tôi chạy `parse_values` |
| Các số mồi và dung sai của D1 và D4 | **Đúng** | D4 ở A′ ra 8,5 chứ không phải 8,3 (chênh do làm tròn) |
| Lý do loại D5 | **Sai** | Mục 3, D5 |
| Lý do loại dòng < 10 kg | **Không đứng** | Mục 3, D6 |
| Điều 6.2 TT51 | **Báo cáo bỏ sót** | Ảnh trang 3 |
| Văn bản cũ TT08/1999 | **Báo cáo bỏ sót** (không tra) | — |
| Đối chiếu WHO_global | **Báo cáo bỏ sót** | Tôi thử WHO Pocket Book 2013 trên WHO IRIS: trả HTML rỗng; NCBI: reCAPTCHA. Cần người kiểm |

## 5. "Sai lệch so với bộ hạt giống": đánh giá

- **Dòng 15** (status "confirmed", pilot true): tôi **đồng ý** hạ trạng thái xuống "không phải xung đột sạch". Mục 4.1–4.2 của báo cáo chính xác, và tôi đã kiểm lại từng trích dẫn. Bổ sung:
  - Điều 6.2 TT51.
  - TT08/1999 chưa tra.
  - Chính TT51 PL X (1/5–1/3 ống) cũng thuộc tập VN.
  - Mỹ còn cho 0,1 hoặc 0,15 mg bút tiêm với trẻ < 15 kg (tr. 3, 7, 20; Rec 12). Giá trị này dành cho kê đơn bút tiêm, không phải liều tại cơ sở y tế.
- **Dòng 14:** đúng. Nhưng làm đối chứng thì phải cố định cân nặng ≥ 50 kg (mục 3, D2).
- **§3.3** "WAO/EAACI 0,01 mg/kg, tối đa 0,5 mg": phần WAO đúng. Phần EAACI chưa kiểm được. Mỹ có trần **0,3 mg ở trẻ em** (khác WAO).
- Ghi chú thêm: `state/gates/project_onepager.md` đã cập nhật dòng 15 là "Nhiều khả năng không phải xung đột", nhất quán với kiểm toán này.

## 6. Vấn đề chung

- **G1. Báo cáo lỗi thời so với công cụ.** Cần chạy lại bước tạo mẩu cho D2 và D3 trên sidecar OCR, với `extraction.ocr = true`.
  - Tôi (AI) đã đọc ảnh trang 3, 9, 19, 20. Các số khớp với OCR ở những chỗ nêu trên.
  - Đây **không** phải lần kiểm của người theo §3.1.
- **G2. OCR có lỗi ở chỗ ảnh hưởng tới giá trị.** Ba ví dụ ở trang 9:
  - Ảnh ghi "≥ 90mmHg", OCR ra "> 90mmHg" (sai dấu so sánh).
  - "1/2 - 1 ống" ra "1⁄2 - ] ống".
  - "phút/lần" ra "phúVlần".

  Mọi mẩu ngưỡng hoặc mục tiêu lấy từ OCR TT51 phải được người so dấu so sánh với ảnh.
- **G3. Chặn kỹ thuật: tập VN nhiều nguồn.**
  - Mỗi mẩu chỉ có một `span`, nên không gộp được PL III (trang 9) với PL X (trang 19–20), và càng không gộp được với 3942/3312.
  - `normalize_vi` đọc sai "1/5-1/3 ống".
  - Hệ quả: **mọi mẩu liều trẻ em từ TT51 dựng hôm nay đều theo cách A (chỉ PL III)**. Cách này làm phồng số xung đột (D4) và có thể sinh mồi nằm trong khoảng PL X (D6).
  - Tôi ủng hộ đề xuất 6.3 và 6.4 của báo cáo (nguồn riêng cho từng `ValueItem`; luật khoảng phân số). Đây là điều kiện trước khi dựng bất kỳ mẩu phản vệ trẻ em nào.
- **G4. Trần liều.** `ValueItem` không có trường "tối đa". Giá trị kiểu "0,01 mg/kg, tối đa X" phải được quy đổi và áp trần theo `weight_kg` trước khi ghi, và phải ghi rõ trong `text`. Ví dụ Mỹ ở trẻ 35 kg là 300 µg, không phải 350.
- **G5. Quyết định DR8 cho phản vệ (HG):**
  - (a) Hợp tập, đúng như DR8 đã đăng ký: dòng 15 thành concordant. Nên báo cáo "TT51 250 µg so với 3942/3312 100 µg cho trẻ 10 kg (gấp 2,5 lần)" như một mâu thuẫn nội bộ của Bộ Y tế.
  - (b) Coi phần phản vệ của 3942/3312 đã bị TT51 thay, dựa trên Điều 6.2, PL III I.1 và nguyên tắc văn bản sau: dòng 15 thành indistinguishable. Nếu chọn (b) phải ghi `docs/DECISIONS.md`.
  - (c) Bỏ ngoài kho: trái §1.2.
  - Ở cả (a) và (b), dòng 15 **không vào H1 xác nhận**.
- **G6. Tranh chấp ghi `data/cache/foreign/index.json`.**
  - `sources.fetch` đọc index, tải, rồi ghi đè cả file mà không khóa. Khi nhiều agent chạy song song, mục của nhau bị mất. Mục cho sơ đồ thuật toán RCUK đã mất, dù file `c7b75e76a1fdba0926bd.pdf` vẫn còn trên đĩa.
  - Đề xuất: khóa file, hoặc đọc lại và gộp ngay trước khi ghi, hoặc mỗi URL một file JSON riêng.
  - Ngoài ra, trang chặn bot dùng cho một URL duy nhất vẫn được đưa vào index. `block_hashes` chỉ bắt được khi cùng một HTML xuất hiện cho ≥ 2 URL. Đề xuất: coi trang HTML 0 ký tự là tải hỏng và không ghi vào index.
- **G7. Hệ thống WHO_global chưa có đối chiếu cho phản vệ.** WHO IRIS và NCBI chặn. Cần người mở WHO Pocket Book of Hospital Care for Children (2013) và tài liệu AEFI của WHO để xem có liều adrenalin tiêm bắp hay không.
- **G8. Chất lượng văn bản QĐ 3312/2015.**
  - Trang 106 ghi "Adrenalin 1/10.000 tiêm TM liều 0,1 mg/Kg (0,1 ml/Kg)". 0,1 ml/kg dung dịch 1/10.000 thực ra là 0,01 mg/kg, nên hai con số tự mâu thuẫn gấp 10 lần.
  - Không tạo mẩu liều tĩnh mạch từ đoạn này nếu chưa có bác sĩ thật xem.
  - Link đính kèm trên trang kcb.vn là `…/20210723/5dcac44ad73df3863c3c42f8e4de23ffTre-em.rar`, khác link báo cáo dùng (`…/20210723//Tre-em.rar`). Nên ghi link có trên trang vào manifest.
  - Nên thêm U+F06D→"µ" vào `_GLYPH` trong `verify_span.norm`. Đây là đề xuất; tôi không sửa mã.
- **G9. Khoảng trống trong bảng cân nặng của TT51.**
  - PL III không có mức cho 21–30 kg.
  - "0,3ml (tương đương 1/3 ống)" tự lệch nhẹ (0,3 so với 0,333 ml).
  - Tránh dựng câu hỏi ở 21–30 kg và ở biên 10 hoặc 20 kg.

## 7. Việc cần người (bổ sung cho mục 5 của báo cáo)

1. Quyết định G5 (DR8) và ghi vào `docs/DECISIONS.md`.
2. Người so ảnh trang 9, 19, 20 của `data/raw/TT51_2017.pdf` với OCR, cho D2, D3, D6 (có thể thêm D1).
3. Tra TT08/1999/TT-BYT từ nguồn chính thức: liều trẻ em và khoảng nhắc lại.
4. EAACI 2021 (doi 10.1111/all.15032) và đối chiếu WHO (G7): người mở và ghi giá trị cùng vị trí.
5. Bác sĩ thật (HG3.9): tình huống "trẻ 4 tháng 6 kg sau tiêm chủng" có hợp lý không, và bệnh viện đang dùng bảng TT51 hay 0,01 mg/kg.

## 8. Thao tác của kiểm toán viên (minh bạch)

- **Chỉ đọc:** các file pilot, `src/`, `configs/`, `data/seed/seed_conflicts.yaml`, OCR sidecar, `data/raw/TT51_2017.pdf` và `data/raw/3942_2014.pdf`.
- **Scratchpad** (ngoài dự án):
  - Ảnh render các trang 3, 9, 19, 20 của TT51.
  - `Tre-em.rar` tải từ kcb.vn, khớp sha256 của báo cáo, giải nén bằng tar.exe của Windows.
- **Ghi vào `data/cache/foreign/`** qua `vnsoc.match.sources fetch`:
  - Wiley EAACI: 403, không ghi gì.
  - WHO IRIS Pocket Book: được ghi vào index nhưng là **HTML rỗng**, sha256 `a859cc83…`, 0 ký tự. **Không phải bằng chứng**; cần tải lại với `refresh`.
- Các lệnh `sources grep` cho RCUK, WAO, Mỹ dùng cache, không tải lại.
- Không sửa `data/raw`, `data/frozen`, `state/`, `configs/`, `src/`, `tests/`, `docs/`.
