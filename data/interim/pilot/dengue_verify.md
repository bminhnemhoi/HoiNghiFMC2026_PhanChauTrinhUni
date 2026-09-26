# Kiểm toán độc lập — thí điểm Sốt xuất huyết Dengue (ID = dengue)

Ngày: 2026-09-26 · Người kiểm: integrity-auditor (AI; có góc nhìn bác sĩ lâm sàng do AI đóng vai, **không phải bác sĩ thật**)
Đối tượng: `data/interim/pilot/dengue.jsonl` (10 mẩu) và `data/interim/pilot/dengue_report.md`.
Nguyên tắc: không tin báo cáo, tự chạy lại mọi kiểm tra. Chỉ đọc dữ liệu; chỉ ghi file này. Mọi tệp phụ (ảnh trang, OCR thử,
script dò bộ chấm) nằm trong scratchpad của phiên (`…/scratchpad/audit_dengue/`), **không** ghi vào `data/`.

## 0. Kết luận nhanh

| Mẩu | Verdict | Lý do chính (một dòng) |
|---|---|---|
| P-dengue-01 | **fix** | Giá trị CDC "40–80 ml/kg/h" do agent tự quy đổi, không có trong nguồn; thiếu điều kiện "chưa truyền dịch trước"; mồi 20–25 trùng giá trị thật của quần thể lân cận |
| P-dengue-02 | **fix** | Giá trị CDC là diễn giải một dòng in lỗi ("10mg/kg for 1-2 hrs") nhưng ghi `verified_by: auto`; mồi 13–15 trùng giá trị thật; cùng họ với P-01 |
| P-dengue-03 | **fix** | Xung đột thật, nhưng quần thể phải ghi "chưa nhận bolus dịch tinh thể" (WHO 2012 ưu tiên dịch keo nếu đã bolus); bộ chấm xếp "dịch keo" thành **abstain** |
| P-dengue-04 | **fix** (nhẹ) | Xung đột thật; sai locator tóm tắt WHO 2025 (PDF p.15, không phải p.7); bộ chấm xếp "Chống chỉ định analgin" thành abstain; câu mồi bị chấm thành foreign |
| P-dengue-05 | **fix** | Giá trị bản cũ đúng, nhưng span bản cũ có dấu "…" (không nguyên văn); nên dùng Phụ lục 14 (3705 p.39), nơi ghi thẳng "SỐC SXHD hoặc SỐC SXHD NẶNG → 15 ml/kg/giờ x 1 giờ" |
| P-dengue-06 | **pass** | 2760 p.16 và 3705 p.9 (đọc ảnh + OCR thử) khớp; WHO 2009/2012/2025 không có đối chiếu cho đúng câu hỏi (no_counterpart đúng) |
| P-dengue-07 | **reject** | Không phân biệt được (indistinguishable); giá trị cuối của WHO không phải sàn ("or less"); WHO 2009 cho 1,5–2 ml/kg/h duy trì ở người IBW > 50 kg; "3 ml/kg/giờ x 4-6 giờ" **vẫn là một bước hiện hành** cho 13–16 tuổi (2760 Phụ lục 11, p.50) |
| P-dengue-08 | **pass** | 2760 p.12, 3705 p.6, WHO 2025 p.44, WHO 2012 p.35 đều khớp |
| P-dengue-09 | **fix** (nhẹ) | CDC xếp nhóm C ở p.1 với "ALT or AST>1000 IU" (dấu ">"), còn "≥1000" ở p.6 là tiêu chí nhập viện; cần sửa cmp + locator (trạng thái không đổi) |
| P-dengue-10 | **fix** (nhẹ) | Giá trị đúng; phải chặn nhầm với quy tắc "mạch nhanh, HA kẹt 25 mmHg: xử trí như sốc" (2760 p.14, p.46, p.50) khi sinh câu hỏi |

Tổng: **pass 2 · fix 7 · reject 1**. Nếu áp dụng các fix: xung đột 4 (P-01…04; P-01 và P-02 cùng họ), lệch phiên bản 2
(P-05, P-06), đối chứng 3 (P-08, P-09, P-10). Chỉ tiêu lệch phiên bản 2–4 vẫn đạt khi bỏ P-07.

Báo cáo của agent **trung thực và phần lớn chính xác**. Mọi số trang, giá trị Bộ Y tế, giá trị WHO và giá trị CDC mà tôi
kiểm đều khớp nguồn. Có **một nhận định sai** (mục 3.2: tiêu chí "nôn ≥ 3 lần/1 giờ" không phải no_counterpart) và một số
chỗ ghi `verified_by: auto` cho giá trị đã diễn giải.

---

## 1. Kiểm lại công cụ, văn bản và nguồn

| Mục | Lệnh / cách kiểm | Kết quả |
|---|---|---|
| Schema | `vnsoc.schemas atom data/interim/pilot/dengue.jsonl` | "OK 10 dòng hợp lệ (atom)" ✓ |
| Span | `vnsoc.extract.verify_span data/interim/pilot/dengue.jsonl` | "OK: 0 mẩu không đạt" ✓ |
| tolerance / conflict_status | `finalize()` chạy lại trong Python | Khớp 10/10 giá trị lưu (2,5 · 1,5 · 0 · 0 · 22,5 · 0 · 0,25 · 0 · 0 · 0) ✓ |
| Mồi num | `mirror_decoy` / `choose_decoy` chạy lại | P-01 → 20–25 (mirror_arith) ✓; P-02 → 13–15 ✓; P-07 → 0,4–1,4 (geom) nhưng `choose_decoy` trả None vì làm mẩu indistinguishable ✓. `check_decoy == []` với cả 10 mẩu ✓ |
| Trường chỉ-bác-sĩ | `grep moh_lags_evidence\|clinical_harm\|clinician_confirmed` | 0 dòng ✓ |
| `data/raw/2760_2023.pdf` | `sha256sum`; `--page 1` | sha `5936c4e425a17db8…` ✓. Lớp chữ để trống số ("Số: /QĐ-BYT"). Chữ ký số "Ký bởi: Bộ Y tế … Ngày ký: 04-07-2023", tem văn thư "2760 04 7". Điều 1 thay thế HD kèm QĐ 3705/QĐ-BYT ngày 22/8/2019 ✓. Ảnh Phụ lục 11, 16.1, 16.2 có ghi tay "2760 /QĐ-BYT ngày 04 tháng 7 năm 2023" ✓ |
| `data/raw/3705_2019.pdf` | `sha256sum`; ảnh trang (PyMuPDF 130–150 dpi) | sha `fcd393c4ef07ad8c…` ✓. Bản quét; ảnh p.39 có ghi tay "3705 /QĐ-BYT ngày 22 tháng 8 năm 2019"; mọi trang tôi xem (6, 8, 9, 19, 20, 39) có logo LuatVietnam ở chân trang ✓ (đúng như báo cáo) |
| Có bản Bộ Y tế mới hơn 2760/2023 không? | WebFetch tìm kiếm nội bộ kcb.vn ("sốt xuất huyết") | Không có kết quả 2024–2026. **Không loại trừ hoàn toàn được**: WebSearch của phiên đã hết (200/200), và kcb.vn cũng không liệt kê 2760/2023. → corpus-librarian cần xác nhận trước khi đóng băng kho (15/10/2026) |
| WHO 2009 | `sources fetch` (cache) | sha `f6f48811df824c02`, 160 trang ✓ |
| WHO 2012 Handbook | `sources fetch` (cache) | sha `b0ca16915451b163`, 124 trang ✓ |
| WHO 2025 arbovirus | `sources fetch` (cache) | sha `cbbe4513ef91cc6b`, 125 trang ✓. **Không có tốc độ dịch ml/kg/h nào cho dengue** (grep "ml/kg" chỉ ra mô tả nghiên cứu p.69/76/81 và liều NAC p.97) ✓, đúng như báo cáo |
| CDC Pocket Guide 5/2024 | `sources fetch` (cache) | sha `20dad79a31da86cc`, 8 trang ✓ |

**Kiểm bằng máy các span bản cũ 3705 (mới, do tôi làm).** Tesseract 5.4 + tessdata_best `vie+eng` đã có trên máy
(`vnsoc.extract.ocr.tesseract_bin()` trả đường dẫn). Tôi OCR các trang 6, 8, 9, 19, 20, 39 ở 300 dpi **vào scratchpad**,
không vào `data/interim/ocr`. Sau đó so với `extraction.superseded_spans`:
- Khớp nguyên văn: P-03 (p.8), P-06 (p.9), phần đầu span P-05 (p.19).
- Các span còn lại chỉ lệch do lỗi OCR:
  - dấu thanh bị mất: "phai thay thé", "Khong dung";
  - "giờ" đọc thành "gid" hoặc "gio";
  - "10" đọc thành "I0";
  - "→" đọc thành "—".
- **Không có span nào sai chữ hoặc sai số so với ảnh trang.** Tôi đọc lại ảnh từng trang bằng mắt (p.6, 8, 9, 19, 20, 39):
  mọi giá trị bản cũ ghi trong mẩu đều đúng.

→ Đề xuất: chạy `vnsoc.extract.ocr --key 3705/2019 --override-text-layer` để `verify_span` tự kiểm được. Cần cờ override
vì lớp chữ hiện có là OCR cũ không dấu. Việc này cần người có quyền ghi `data/interim/ocr`. Nó tính vào trần 10 văn bản OCR;
manifest ghi đang dùng 5/10.

---

## 2. Từng mẩu

### P-dengue-01 — người lớn sốc còn bù, tốc độ dịch tinh thể giờ đầu · **fix**

Đã kiểm:
- **2760 p.28**, C.2.1.2: "…Ringer lactate hoặc NaCl 0,9% 15ml/kg/giờ sau đó đánh giá lại…" ✓.
- **Phụ lục 16.1, p.55** (ảnh): hộp "SỐC SXHD" → "RL hoặc NaCl 0,9% 15 ml/kg/giờ x 1 giờ" ✓.
- **Sốc nặng tách riêng:** C.2.2 (p.30) và Phụ lục 16.2 (p.56) dùng "Bolus RL hoặc NaCl 0,9% 15 ml/kg/15 phút". Vậy
  15 ml/kg/giờ đúng cho sốc chưa phải sốc nặng ✓.
- **Bản cũ 3705:**
  - p.19 (ảnh + OCR): "15ml/kg/giờ" ✓.
  - p.39, Phụ lục 14 (ảnh): hộp "SỐC SXHD hoặc SỐC SXHD NẶNG" → "RL hoặc NaCl 0,9% 15 ml/kg/giờ x 1 giờ".
  - Vậy dòng hạt giống 1 đúng là **không đổi** giữa hai bản ✓.
- **WHO 2009:** PDF p.48 "at 5-10 ml/kg/hour over one hour" (sốc còn bù, không phân tuổi); p.49 (Fig 2.2) và p.65 ✓.
- **WHO 2012:** PDF p.38 "5-10 ml/kg/hour over one hour in adults" ✓.
- **Xung đột có thật:** với câu hỏi "người lớn vào viện vì sốc SXHD còn bù, giờ đầu truyền bao nhiêu?", 5–10 **không**
  đúng theo Bộ Y tế (15) ✓.

Vấn đề:
1. **Giá trị CDC "40–80 ml/kg/h" không có trong nguồn.**
   - CDC p.5 chỉ ghi "1st dose of IV crystalloid solution at 20mL/kg in 15-30 min". Đây là **một bolus rồi đánh giá lại**,
     không phải tốc độ trong 1 giờ. Con số 40–80 do agent tự quy đổi, nhưng vẫn ghi `verified_by: "auto"`.
   - Tôi dò bộ chấm bằng câu giả (không phải đầu ra mô hình): "ĐÁP ÁN: 20 ml/kg trong 15-30 phút" → nhãn 5
     (unattributed), không phải 4. Nghĩa là giá trị này **không bao giờ khớp** được một câu trả lời theo kiểu CDC.
   - Hệ thống US bị ghi nhận mà không có cơ sở đo được.
2. **Thiếu điều kiện "chưa truyền dịch trước".** Cũng trong 2760:
   - p.15 và Phụ lục 6 (p.42) nói người lớn có dấu hiệu cảnh báo **đang truyền dịch** mà chuyển sang sốc thì liều chống
     sốc đầu là **cao phân tử 10–15 ml/kg/giờ**.
   - Nếu câu hỏi không nói rõ bệnh nhân vào viện trong tình trạng sốc, tập giá trị Bộ Y tế cho câu đó không duy nhất.
3. **Mồi 20–25 ml/kg/h (đúng quy tắc mirror_arith) trùng giá trị thật của quần thể hoặc bước lân cận:**
   - 20 ml/kg/giờ là tốc độ giờ đầu cho **trẻ em** (2760 p.15) và **thiếu niên 13–16** (p.18, p.50);
   - WHO 2012 p.38: trẻ em "10-20 ml/kg/hour over one hour";
   - WHO 2012 p.38: người lớn bolus thứ hai "10-20 ml/kg/hour for one hour".
   - Dò bộ chấm: "20 ml/kg/giờ" → `decoy_match: True`. Tỉ lệ khớp mồi sẽ bị thổi phồng vì nhầm quần thể hoặc bước, không
     phải trùng ngẫu nhiên. Mồi vẫn đúng theo quy tắc đăng ký trước nên không tự sửa được (xem 3.3).

Fix cụ thể:
- `foreign[2]` (CDC): **bỏ khỏi mẩu này**.
  - Khi `normalize_vi` đọc được "ml/kg" và "X ml/kg/Y phút", nên dựng mẩu riêng cho *thể tích/thời gian bolus*.
  - Nếu vẫn muốn giữ: đổi `verified_by` → `"needs_human_check"` và ghi rõ trong `values[0].text` là "quy đổi, không có
    trong nguồn".
  - Đã kiểm lại: bỏ CDC thì tolerance vẫn 2,5, status vẫn conflict, mồi không đổi.
- `population`: thêm `"history": "vào viện trong tình trạng sốc; chưa được truyền dịch tĩnh mạch trước đó"`, kèm ghi chú
  loại trừ nhánh B2 (2760 p.15 và p.42: liều đầu là CPT 10–15 ml/kg/giờ).
- `extraction.superseded_spans`: thêm span p.39 (3705 Phụ lục 14) `"RL hoặc NaCl 0,9% 15 ml/kg/giờ x 1 giờ"`, dưới hộp
  `"SỐC SXHD hoặc SỐC SXHD NẶNG"`, method `visual_transcription_from_scanned_page`.
- `decoy`: giữ theo quy tắc, nhưng ghi vào DECISIONS: mồi trùng giá trị thật lân cận; đề xuất quy tắc ở 3.3.

### P-dengue-02 — người lớn sốc còn bù đã cải thiện, bước 2 · **fix**

Đã kiểm:
- **2760 p.28:** "a) Nếu cải thiện lâm sàng (…hiệu áp > 20 mmHg) Tiếp tục truyền … 10ml/kg/giờ x 2 giờ" ✓.
- **Phụ lục 16.1** (ảnh): "RL hoặc NaCl 0,9% 10 ml/kg/giờ x 2 giờ" ✓.
- **3705 p.19** (ảnh): "a) Nếu cải thiện lâm sàng (mạch giảm, HA bình thường, hết kẹt) - Tiếp tục … 10ml/kg/giờ x 2 giờ" ✓.
  OCR đọc "I0ml/kg/giờ".
- **WHO 2009** p.48: "gradually reduced to 5-7 ml/kg/hr for 1-2 hours" ✓.
- **WHO 2012** p.38: "adult patient's condition improves … 5-7 ml/kg/hour for 1-2 hours" ✓.
- Xung đột với WHO có thật ✓.

Vấn đề:
1. **Giá trị CDC là diễn giải, không phải đọc thẳng.**
   - CDC p.5 in "Reduce IV crystalloid solution to 10mg/kg for 1-2 hrs". Sai đơn vị (mg thay mL) **và** không có "/hr".
   - Cùng tài liệu p.4 dùng "10mL/kg in 1 hr" cho một liều tổng, nên dòng này có thể là 10 mL/kg/h **hoặc** 10 mL/kg
     trong 1–2 giờ.
   - Hiện ghi `verified_by: "auto"` là không đúng.
   - Giá trị US này trùng Bộ Y tế, nên không ảnh hưởng trạng thái.
2. **Mồi 13–15 chứa 15 ml/kg/giờ:**
   - đó là tốc độ giờ đầu người lớn (P-01);
   - cũng là **bước 2 thật của Bộ Y tế** cho người lớn sốc nặng đã cải thiện: 2760 p.30 "chuyển sang truyền Ringer lactate
     hoặc NaCl 0,9% 15ml/kg/giờ x 1 giờ"; Phụ lục 16.2 p.56.
   - Dò bộ chấm: "15 ml/kg/giờ" → `decoy_match: True`.
3. **Cùng `conflict_family` với P-01**, nên không độc lập. Đồng ý với báo cáo: nếu phải cắt về 3 xung đột thì bỏ P-02.

Fix cụ thể:
- `foreign[2]` (CDC): đổi `verified_by` → `"needs_human_check"`, `locator` giữ, `values[0].text` →
  `"10 (nguồn in '10mg/kg for 1-2 hrs'; đơn vị và 'mỗi giờ' là diễn giải)"`. Hoặc bỏ hẳn. Bỏ CDC thì tolerance vẫn 1,5,
  status vẫn conflict.
- `population.severity`: thêm "không phải sốc nặng (M = 0, HA = 0), vì nhánh sốc nặng bước 2 là 15 ml/kg/giờ".
- Mồi: như P-01, ghi DECISIONS.

### P-dengue-03 — loại dịch cho liều chống sốc đầu (người lớn có dấu hiệu cảnh báo đang truyền dịch → sốc) · **fix**

Đã kiểm:
- **2760 p.15:** "…liều chống sốc đầu tiên là cao phân tử 10 - 15ml/kg/giờ" ✓. Phụ lục 6 p.42: "Chống sốc theo Phụ lục
  16, với liều đầu là CPT 10-15ml/kg/giờ" ✓.
- **3705 p.8:** span khớp nguyên văn cả ảnh lẫn OCR thử ✓.
- **WHO 2025:**
  - p.16 (tóm tắt) và p.60 §5.1: "suggests using crystalloid fluid rather than colloid fluid" cho bệnh arbovirus nặng
    cần dịch truyền (khuyến cáo có điều kiện) ✓;
  - p.61 ghi bằng chứng giới hạn ở dengue ✓.
- **WHO 2009:**
  - p.48: sốc còn bù dùng dịch tinh thể đẳng trương ✓;
  - p.46: dấu hiệu cảnh báo nặng lên thì tăng tốc độ dịch tinh thể lên 5–10 ml/kg/giờ ✓.
- **WHO 2012:** p.36 như WHO 2009; p.38 và p.39 (Fig 5) bắt đầu bằng dịch tinh thể 5–10 ml/kg/giờ ✓.
- **CDC:**
  - p.4: nhóm B2 xấu đi → "Treat as group C";
  - p.5: nhóm C, liều đầu dịch tinh thể 20 mL/kg;
  - p.6: dịch keo "only in refractory shock after crystalloid solutions have been administered" ✓.
- Kết luận: xung đột có thật, và CDC áp dụng **đúng quần thể** (bệnh nhân B2 chuyển sốc).

Vấn đề:
1. **Ngoại lệ WHO 2012 chưa ghi:** p.39, p.40, p.42 có chú thích "colloid is preferable if the patient has already received
   previous boluses of crystalloid". Nếu câu hỏi để mơ hồ "đang truyền dịch", đáp án "dịch keo" cũng hợp WHO 2012.
   - Quần thể phải nói rõ: đang truyền **tốc độ duy trì** theo phác đồ B2 (6 ml/kg/giờ → 3 → 1,5, 2760 p.14–15) và
     **chưa nhận bolus nào**.
   - WHO 2025 p.60 cũng có ghi chú: cần cá thể hóa "particularly to choices of fluid subsequent to the initial
     resuscitation".
2. **Lỗi bộ chấm (cat_options):** nhóm `colloid` không có "dịch keo", từ tiếng Việt thông dụng nhất cho colloid. Dò bộ chấm:
   - "ĐÁP ÁN: dịch keo" → nhãn **6 (abstain)**, lẽ ra là 2;
   - "dịch keo như albumin" → nhãn 5 + mồi;
   - "a colloid such as albumin" → nhãn 2 **và** `decoy_match: True`.
3. **Mồi "albumin 5%" chồng nghĩa với "colloid".** Albumin là dịch keo, và CDC p.2 nêu "colloids (such as albumin) for
   refractory shock". Không nguồn nào khuyên albumin làm **liều đầu**, nên `check_decoy == []` là đúng. Nhưng nhãn chấm sẽ
   nhập nhằng.
4. **Chênh lệch nội tại của Bộ Y tế:**
   - C.2.1: người lớn vào viện vì sốc dùng dịch tinh thể trước;
   - B2: bệnh nhân đang truyền dịch rồi chuyển sốc dùng CPT trước.
   - Cần ghi trong notes để người sinh câu hỏi và bác sĩ (HG) thấy.

Fix cụ thể:
- `population.severity` → thêm "đang truyền Ringer lactate/NaCl 0,9% theo phác đồ dấu hiệu cảnh báo (6 → 3 → 1,5
  ml/kg/giờ), CHƯA nhận bolus dịch tinh thể nào".
- `foreign[2].locator` (WHO 2012): thêm "ngoại lệ: colloid preferable nếu đã nhận bolus crystalloid trước đó (PDF p.39, 40,
  42)".
- `foreign[0].locator` (WHO 2025): thêm "p.60 ghi chú cá thể hóa sau hồi sức ban đầu".
- `cat_options.colloid`: thêm các mẫu `"dich keo"`, `"dung dich keo"`, `"\\bkeo\\b"`, `"starch"`.
- Mồi: đổi sang một phương án không phải dịch keo và không nguồn nào nêu cho liều đầu. Nếu giữ albumin, bộ chấm phải xếp
  "colloid … albumin" vào **một** nhãn: đề xuất gán albumin chỉ khi không có từ dịch keo tổng hợp. Cần bác sĩ HG chọn.

### P-dengue-04 — có được dùng analgin (metamizol) để hạ sốt? · **fix** (nhẹ)

Đã kiểm:
- **2760 p.12:** "Không dùng aspirin (acetylsalicylic acid), analgin, ibuprofen…" ✓.
- **3705 p.6:** ảnh ✓; OCR chỉ lệch dấu ("Khong dung").
- **WHO 2025:**
  - p.47 §4.2.2: "suggests the use of metamizole (dipyrone) for the treatment of pain and/or fever" cho bệnh arbovirus
    không nặng (có điều kiện, bằng chứng thấp) ✓;
  - bằng chứng "limited to dengue" (p.47) ✓;
  - bảng liều 4-5 (p.49) cho cả người lớn/thiếu niên ≥ 15 tuổi và trẻ ≤ 14 tuổi (10 mg/kg) ✓.
- Xung đột thật ✓. analgin = metamizol natri (dipyrone) ✓.

Vấn đề:
1. `foreign[0].locator` ghi "summary PDF p.7". **p.7 là danh mục bảng**; khuyến cáo tóm tắt nằm ở **PDF p.15**.
2. **Lỗi bộ chấm:**
   - "ĐÁP ÁN: Chống chỉ định analgin" → **abstain**. Mẫu `not_allowed` chỉ bắt "analgin … chống chỉ định", không bắt chiều
     ngược lại.
   - Câu đúng kiểu mồi "Có thể dùng metamizol khi paracetamol không hiệu quả" → nhãn **4 (foreign)**, không phải mồi. Mẫu
     `allowed` ("^co", "co the dung … metamizol") thắng, vì mẫu `second_line_only` đòi có chữ "chỉ".
   - Hệ quả: tỉ lệ khớp nước ngoài bị thổi phồng, tỉ lệ khớp mồi bị hạ.

Fix cụ thể:
- `foreign[0].locator` → "§4.2.2 PDF p.47 (in 33); tóm tắt khuyến cáo PDF p.15; bảng liều 4-5 PDF p.49".
- `cat_options.not_allowed`: thêm `"chong chi dinh[^.]{0,40}(analgin|metamizol\\w*|dipyron\\w*)"`,
  `"(contraindicat\\w*)[^.]{0,40}(metamizole|dipyrone|analgin)"`.
- `cat_options.second_line_only`: thêm `"khi[^.]{0,40}paracetamol[^.]{0,30}(khong (hieu qua|dap ung)|that bai)"`,
  `"(if|when)[^.]{0,40}(paracetamol|acetaminophen)[^.]{0,30}(fails|ineffective|not effective)"`. Bộ chấm cần ưu tiên
  second_line trước allowed khi cả hai khớp. Đây là thay đổi quy tắc chấm, phải làm **trước** khi đóng băng.

### P-dengue-05 — người lớn sốc nặng (M = 0, HA = 0): thời gian truyền 15 ml/kg đầu · **fix**

Đã kiểm:
- **2760 p.30** C.2.2: "15ml/kg trong vòng 15 phút" ✓. Phụ lục 16.2 p.56 (ảnh): "Bolus RL hoặc NaCl 0,9% 15 ml/kg/15
  phút" ✓.
- **3705 p.19** (ảnh): mục "C.2.1. Điều trị sốc SXHD, sốc SXHD nặng" chỉ có một phác đồ 15 ml/kg/giờ trong giờ đầu.
  **p.20:** C.2.2 là "Điều trị tái sốc" (không có mục sốc nặng người lớn riêng).
- **3705 p.39** (Phụ lục 14, ảnh + OCR): hộp "SỐC SXHD hoặc SỐC SXHD NẶNG" → "RL hoặc NaCl 0,9% 15 ml/kg/giờ x 1 giờ".
  → Giá trị bản cũ 60 phút là **đúng**, dù là phép tính (15 ml/kg ở 15 ml/kg/giờ). Bằng chứng mạnh hơn báo cáo nêu.
- **Nước ngoài:**
  - WHO 2009 p.49: "20 ml/kg as a bolus given over 15 minutes" (sốc tụt HA) ✓;
  - WHO 2012 p.41 "Treatment of profound shock (hypotensive; undetectable pulse and BP)": "over 15-30 minutes" ✓;
    nhưng p.34 (tóm tắt) cùng tài liệu ghi "bolus for 15 min";
  - CDC p.5: "20mL/kg in 15-30 min" ✓.

Vấn đề:
1. `extraction.superseded_spans[0].text` nối hai đoạn bằng "…", **không phải span nguyên văn**.
2. Giá trị bản cũ là **suy ra**, nhưng không có cờ nào ghi điều đó.
3. **Ghi chú (không lỗi):**
   - Tolerance 22,5 phút làm "30 phút" và "15-30 phút" được chấm **đúng Bộ Y tế** (đã dò). Chấp nhận được vì nước ngoài
     trùng, nhưng cần ghi cho H2.
   - Nước ngoài chỉ trùng về **thời gian**; thể tích khác (20 so với 15 ml/kg).

Fix cụ thể:
- `extraction.superseded_spans`: thay bằng hai span nguyên văn:
  - (a) p.19: `"C.2.1. Điều trị sốc sốt xuất huyết Dengue, sốc sốt xuất huyết Dengue nặng"`;
  - (b) p.39 (Phụ lục 14): `"SỐC SXHD hoặc SỐC SXHD NẶNG"` + `"RL hoặc NaCl 0,9% 15 ml/kg/giờ x 1 giờ"`.
  - Giữ span "Trong 1 giờ đầu… 15ml/kg/giờ…" (p.19) làm span thứ ba.
- `superseded[0].values[0].text` → "15 ml/kg/giờ x 1 giờ (sốc và sốc nặng chung phác đồ) ⇒ 15 ml/kg trong 60 phút (phép
  tính)". `superseded[0].page` có thể thêm p.39.
- `foreign[1].locator` (WHO 2012): thêm "tóm tắt p.34 ghi 'bolus for 15 min'".

### P-dengue-06 — trẻ em sốc, Hct cao, không có Dextran/HES 200: dùng Gelatin thay thế? · **pass**

Đã kiểm:
- **2760 p.16:** "…có thể thay thế bằng dung dịch 6% HES 130 hoặc Gelatin, nhưng cần theo dõi sát…" ✓. `--find
  "Gelatin"` chỉ ra p.16, tức không có giá trị khác cho quần thể khác.
- **3705 p.9:** "…6% HES 200, không dùng Gelatin do hiệu quả kém." ✓ Khớp nguyên văn cả ảnh lẫn OCR thử.
- **no_counterpart đúng:** WHO 2009 p.62 và WHO 2012 p.121 chỉ so sánh tác dụng phụ ("gelatine has the least effect on
  coagulation but the highest risk of allergic reactions"). WHO 2025 p.62 chỉ liệt kê gelafusine trong bảng bằng chứng.
  Không nguồn nào trả lời câu "có dùng gelatin thay thế không".
- Mẫu cat: dò "Có" → 2; "Không, không dùng gelatin do hiệu quả kém" → 3 (temporal) ✓.

Điều kiện kèm theo: phụ thuộc quyết định chung về nguồn 3705 (mục 3.1), không phải lỗi của mẩu.

### P-dengue-07 — thiếu niên 13–16 tuổi, tốc độ duy trì cuối · **reject**

Đã kiểm:
- **2760 p.18:** "sau đó duy trì 1,5 ml/kg/giờ trong 12 - 18 giờ" ✓. Phụ lục 11 p.50 (ảnh): "RL hoặc NaCl 0,9% 1,5 ml/kg/giờ
  x 12-18 giờ" là bước cuối ✓.
- **3705 p.9** (ảnh): "… 3ml/kg/giờ x 4-6 giờ" ✓. 3705 p.6 và p.8: trẻ em < 16, người lớn ≥ 16 ✓.
- **WHO 2012:** p.38 trẻ em "then to 3 ml/kg/hour" ✓.
- **WHO 2009:** p.48 "then to 2-3 ml/kg/hr" ✓.
- **CDC:** p.5 "2-4mL/kg/hr for 24-48 hrs" ✓.

Lý do bác bỏ:
1. `conflict_status = indistinguishable` (bản cũ 3 trùng WHO 2012), nên không dùng được cho kiểm định xác nhận.
2. **"Xung đột" với nước ngoài không sạch:**
   - WHO 2009 p.48: "then further depending on haemodynamic status";
   - WHO 2012 p.41: "finally to 2-3 ml/kg/hour (or less)";
   - bước cuối của WHO không phải sàn;
   - **WHO 2009 p.61 (Textbox J):** "for adults with IBW >50 kg, 1.5-2 ml/kg" cho dịch duy trì mỗi giờ. Phần lớn trẻ
     13–16 tuổi nặng trên 50 kg, nên 1,5 **nằm trong** WHO.
3. **"3 ml/kg/giờ x 4-6 giờ" vẫn là một bước hiện hành** của phác đồ thiếu niên 2760 (Phụ lục 11, p.50, ảnh: sau 5 ml/kg/giờ
   và trước 1,5 ml/kg/giờ). Một câu trả lời "3" có thể đang nói về bước áp chót hiện hành, không phải bản cũ.
4. **Văn bản hiện hành tự mâu thuẫn:** lời văn p.18 nói thời gian mỗi mức "bằng 1/2 trẻ nhỏ", còn sơ đồ p.50 vẫn ghi "3
   ml/kg/giờ x 4-6 giờ" (bằng thời gian trẻ nhỏ). WHO/CDC cũng không có nhóm thiếu niên riêng.

→ Loại khỏi bộ thí điểm. Ghi vào báo cáo làm ví dụ "lệch phiên bản không đo được".

### P-dengue-08 — liều paracetamol mỗi lần, trẻ < 16 tuổi · **pass**

- **2760 p.12:** "10 - 15mg/kg cân nặng/lần, cách nhau mỗi 4 - 6 giờ" ✓. **3705 p.6** (ảnh): "10-15mg/kg" ✓; OCR đọc
  "10- 15mg/kg".
- **WHO 2025 p.44**, Bảng 4-2: "paediatrics 10-15mg/kg every 4-6 hours (maximum daily dose: 60 mg/kg)" ✓.
- **WHO 2012 p.35:** "10 mg/kg/dose, not more than 3-4 times in 24 hours in children" ✓.
- **CDC p.3** chỉ ghi khoảng cách 6 giờ và tối đa 4 liều/ngày, không có mg/kg, nên không ghi là đúng ✓.
- Concordant thật ✓. Giới hạn trẻ em hợp lý: WHO 2025 dùng liều cố định cho người lớn > 50 kg.

### P-dengue-09 — AST/ALT ≥ 1000 xếp SXHD nặng · **fix** (nhẹ)

Đã kiểm:
- **2760 p.38** (Phụ lục 2): "Gan: AST hoặc ALT ≥ 1000U/L" ✓.
- **WHO 2009 p.23:** "liver: AST or ALT >=1000" ✓.
- **WHO 2012 p.17** ✓.
- **CDC:**
  - p.1 xếp **nhóm C** khi "hepatitis [ALT or AST>1000 IU]" (dấu **>**);
  - p.6 "Hepatitis (AST or ALT ≥1000 IU)" nằm trong **tiêu chí nhập viện**, không phải phân độ.

Vấn đề:
- Mục CDC ghi `cmp ">="` và gộp locator p.1 + p.6.
- Cho slot "phân độ nặng", đúng phải là p.1 với `">"`. Trạng thái không đổi, vì bộ chấm bỏ qua cmp (đã chạy `finalize`
  với cmp ">": concordant).

Fix:
- `foreign[2].values[0].cmp` → `">"`.
- `foreign[2].values[0].text` → "ALT hoặc AST > 1000 IU (nhóm C)".
- `foreign[2].locator` → "p.1 Group C – severe organ impairment (hepatitis ALT or AST>1000 IU); p.6 dùng ≥1000 cho tiêu chí
  nhập viện".
- Có thể thêm: WHO 2025 p.28 dùng "WHO 2009 definition" cho bệnh nặng.

### P-dengue-10 — trẻ em, ngưỡng hiệu áp của "huyết áp kẹt" · **fix** (nhẹ)

Đã kiểm:
- **2760 p.9:** "huyết áp kẹt (hiệu số huyết áp tối đa và tối thiểu ≤ 20mmHg" ✓. Định nghĩa chung, không phân tuổi.
  Phụ lục 8/11 (p.46, p.50): "HA tụt hoặc kẹt ≤ 20 mmHg" ✓.
- **WHO 2009 p.40:** "≤ 20 mm Hg in children"; người lớn "may indicate a more severe shock" ✓.
- **WHO 2012 p.14** ✓.
- **CDC p.2:** "systolic minus diastolic BP < 20 mmHg" (dấu "<", không phân tuổi) ✓.

Vấn đề:
- Cũng trong 2760 có quy tắc liền kề: p.14 "huyết áp bình thường hoặc hiệu áp = 25 mmHg: điều trị như sốc SXHD", và chú
  thích sơ đồ p.46, p.50 "Mạch nhanh, HA kẹt 25 mmHg: xử trí như sốc SXH Dengue".
- Câu hỏi dạng "hiệu áp bao nhiêu thì xử trí như sốc?" sẽ có tập Bộ Y tế {≤ 20, 25}, không duy nhất.

Fix:
- `population.context` → "ĐỊNH NGHĨA huyết áp kẹt (không phải ngưỡng 'xử trí như sốc' 25 mmHg kèm mạch nhanh/chi lạnh ở
  2760 p.14, p.46, p.50)".
- `extraction.notes`: thêm ghi chú này cho question-writer.

---

## 3. Vấn đề chung

### 3.1 Nguồn bản cũ 3705/2019 (ảnh hưởng P-01…P-08; quyết định sống còn cho P-05, P-06)

- File duy nhất là bản quét mang logo **LuatVietnam** trên mọi trang, do BV quận Phú Nhuận (medinet.gov.vn) và BVĐK Hà Trung
  đăng lại, cùng sha256.
- Theo chữ quy tắc ("trang Sở Y tế/bệnh viện đăng lại NGUYÊN quyết định"), file có thể chấp nhận. Nhưng gốc là thư viện
  pháp luật tư nhân, nên **người dùng quyết định ở HG1.2/HG2.3**.
- Nội dung thì tôi xác nhận: đọc ảnh 6 trang và OCR thử 300 dpi, mọi giá trị bản cũ trong 8 mẩu đều đúng.
- Đề xuất:
  1. chạy `vnsoc.extract.ocr --key 3705/2019 --override-text-layer` để span bản cũ được `verify_span` kiểm bằng máy;
  2. sau đó đổi `machine_verified` thành kết quả thật.

### 3.2 Độ chính xác của báo cáo agent

Đúng (tôi tự kiểm):
- dòng hạt giống 1 không đổi giữa 3705 và 2760 (3705 p.19 và p.39);
- vị trí C.2.1.2 (PDF p.28, in 27);
- 2760 tách sốc nặng người lớn (C.2.2, p.30);
- WHO 2009 không phân tuổi (p.48), WHO 2012 phân người lớn/trẻ em (p.38);
- WHO 2025 không có tốc độ ml/kg/h;
- hai xung đột định tính từ WHO 2025 (metamizol p.47; crystalloid > colloid p.16/60);
- ngưỡng albumin đổi từ < 2 g/dL (3705 p.12, OCR) sang < 2,5 g/dL (2760 p.20);
- cân nặng hiệu chỉnh đổi từ > 120% CN lý tưởng (3705 p.20, ảnh) sang BMI ≥ 25 (2760 p.29);
- Hct nền 43%/38% không đổi (3705 p.20, 2760 p.29);
- 3705 không có nhánh "20 ml/kg/30 phút" cho trẻ tụt HA nặng (p.9, ảnh).

**Sai:**
- Bảng loại ở mục (3) xếp "nôn ≥ 3 lần/1 giờ" là "Riêng của Việt Nam … (no_counterpart)"; mục (4).7 cũng xem việc định lượng
  số lần nôn là điểm khác với WHO.
- Thực tế tiêu chí này **trùng nguyên văn** với:
  - CDC 2024 p.1: "Persistent vomiting (≥3 episodes in 1 hr or ≥4 in 6 hrs)";
  - WHO 2025 p.28: "three or more episodes in one hour or four episodes in six hours";
  - so với 2760 p.38: "≥ 3 lần/1 giờ hoặc ≥ 4 lần/6 giờ".
- Nó chỉ khác WHO 2009. → Đây là **ứng viên đối chứng (concordant)** tốt, không phải no_counterpart.

**Không chính xác nhỏ:**
- CDC p.1 ghi "ALT or AST>1000 IU" (cả hai men), không chỉ "AST > 1000".
- `verified_by: "auto"` được dùng cho giá trị đã quy đổi hoặc diễn giải (P-01 CDC, P-02 CDC). Báo cáo có nói "cần diễn giải"
  ở mục (5), nhưng dữ liệu không phản ánh điều đó.

**Chưa kiểm được:** ngày IRIS "dc.date.issued 2025-07-03" của WHO 2025. Tôi không tải metadata IRIS; mẩu ghi
`version_date: "2025-07"`, không mâu thuẫn.

### 3.3 Mồi `mirror_decoy` trúng giá trị thật của quần thể/bước lân cận (P-01, P-02)

- Quy tắc đăng ký trước chỉ kiểm mồi với các giá trị *đã ghi trong mẩu*.
- Với dengue, phác đồ có nhiều bậc (15 → 10 → 6 → 3 → 1,5; trẻ em 20 → 10 → 7,5 → 5 → 3) nên phản chiếu dễ rơi vào giá
  trị thật:
  - P-01: 20 = trẻ em/thiếu niên (Bộ Y tế) và WHO 2012 trẻ em/bolus 2;
  - P-02: 15 = giờ đầu người lớn và bước 2 sốc nặng (Bộ Y tế).
- Hệ quả: `decoy_match` đo cả nhầm quần thể, làm hỏng vai trò "đối chứng trùng ngẫu nhiên" của H1.
- Đề xuất (không tự sửa; cần DECISIONS + báo người dùng vì là quy tắc đăng ký trước):
  1. thêm trường `extraction.neighbor_values` (giá trị cùng văn bản/nguồn cho quần thể hoặc bước lân cận, có trang);
  2. `check_decoy` loại mồi trùng các giá trị đó;
  3. `choose_decoy` chuyển sang `mirror_geom` / `mirror_far` theo thứ tự đã định.
- Thử nhanh: với P-01, `mirror_geom` cho c = 15²/7,5 = 30, tức 27,5–32,5 ml/kg/h. Tôi **chưa** kiểm giá trị này với mọi
  nguồn.

### 3.4 Bộ chấm với mẩu cat (P-03, P-04)

Hai lỗi mẫu làm câu trả lời đúng Bộ Y tế thành abstain:
- "dịch keo" (P-03);
- "chống chỉ định analgin" (P-04).

Một lỗi làm câu kiểu mồi thành foreign (P-04). Cả ba phát hiện bằng câu giả; tôi **không** xem đầu ra mô hình nào.

Đề xuất:
- Viết test trong `tests/` cho mỗi mẩu cat với ≥ 5 cách diễn đạt VI/EN mỗi nhãn, kể cả phủ định đảo trật tự.
- Sửa `cat_options` **trước** khi đóng băng quy tắc chấm.

### 3.5 Giá trị nước ngoài quy đổi/diễn giải

Quy tắc "mọi giá trị nước ngoài phải từ nguồn đã tải" nghĩa là chuỗi giá trị phải grep được. Hai trường hợp không grep được:
- "40–80 ml/kg/h" (P-01): không có trong CDC;
- "10 mL/kg/h" (P-02): CDC in "10mg/kg for 1-2 hrs".

Đề xuất:
- Trong schema, thêm cờ `derived: true` hoặc dùng `verified_by: "needs_human_check"` cho mọi giá trị không grep nguyên văn
  được.
- `vnsoc.check` nên từ chối `verified_by: auto` khi `sources.grep(url, value_text)` rỗng.

### 3.6 Tính hiện hành của 2760/2023

- Tìm kiếm nội bộ kcb.vn không thấy văn bản dengue 2024–2026. Nhưng kcb.vn cũng không liệt kê 2760/2023, và WebSearch đã
  hết.
- → Rủi ro còn lại: có thể đã có bản cập nhật chưa phát hiện. Giao corpus-librarian kiểm lại (moh.gov.vn, vncdc.gov.vn,
  trang Sở Y tế) trước 15/10/2026.

### 3.7 Việc cho người/bác sĩ thật (HG1.2 / HG3.9)

- Xác nhận nguồn 3705 (3.1).
- Chọn mồi cho P-03 (albumin hay phương án khác).
- Xác nhận cách diễn đạt quần thể P-01/P-03 (vào viện vì sốc; đang truyền duy trì, chưa bolus).
- Quyết định giữ P-02 khi cắt còn 3 xung đột.
- Nhận định lâm sàng về chênh lệch nội tại C.2.1 và B2 của 2760 (dịch tinh thể trước hay cao phân tử trước khi người lớn
  đang truyền dịch chuyển sốc).

Không có trường chỉ-bác-sĩ nào được điền; tôi không kết luận thay bác sĩ.
