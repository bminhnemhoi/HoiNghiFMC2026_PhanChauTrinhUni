# Kiểm toán độc lập — thí điểm Tăng huyết áp (htn)

Người kiểm: integrity-auditor (Claude, AI). Góc nhìn lâm sàng là **AI đóng vai bác sĩ Việt Nam, không phải bác sĩ thật**; không có nội dung nào ở đây là "bác sĩ đã duyệt".
Ngày 2026-09-26. Chỉ đọc dữ liệu; chỉ ghi file này. Không sửa `htn.jsonl`, data/raw, src, configs.

## Kết luận nhanh

| atom_id | verdict | lý do chính |
|---|---|---|
| P-htn-01 | **fix** | Xung đột với Mỹ là thật. Cần sửa: khóa văn bản (dùng `pdf_choice.json`), `verified_by` của ESC không kiểm lại được bằng công cụ, và span chính là câu phạm vi áp dụng chứ không phải định nghĩa |
| P-htn-02 | **reject** | Không phải xung đột thật. Chính văn bản Bộ Y tế cho phép mục tiêu thấp hơn "nếu dung nạp được", và quần thể của mẩu lại ghi "dung nạp tốt". Trạng thái "conflict" chỉ do mã hóa "< 140" thành điểm 140. Mồi 141–150 trùng mục tiêu < 150 của JNC8 (đã kiểm có nguồn) |
| P-htn-03 | **fix** | Xung đột với Mỹ là thật. Quần thể 18–79 tuổi vắt qua mốc 60 tuổi của JNC8 (≥ 60 tuổi: 150/90, đã kiểm có nguồn), nên giá trị không duy nhất. Thêm khóa văn bản và `verified_by` của ESC |
| P-htn-04 | **fix** | "Đối chứng" đúng về nghĩa, nhưng chỉ đứng được nhờ hợp theo DR8 với 3192. Mã hóa "< 140" thành điểm 140 làm câu trả lời "135 mmHg" bị chấm "vô nguồn". Thêm khóa văn bản và `verified_by` của ESC |

pass 0 · fix 3 · reject 1.

---

## 0. Những gì đã tự kiểm lại bằng công cụ

- `vnsoc.schemas atom` → OK 4/4.
- `vnsoc.extract.verify_span` → OK 4/4.
- Kiểm thêm bằng script (`span_on_page`): cả 4 span phụ đều nguyên văn đúng trang:
  - `supporting_spans` 3192 tr.1 ×2;
  - `union_spans` 3192 tr.3 ×2.
- Đọc lại trang (`--page`): 5904 (bản có lớp chữ) tr. 2, 3, 11, 12, 13, 14, 28, 29; 3192 tr. 1, 2, 3, 4, 10, 12, 13.
- sha256 khớp báo cáo: 5904 `9e6bbe13d5705fc8` (bản có lớp chữ), 5904 `7cb7cd93fd30cf64` (bản scan), 3192 `b4b84c7307c69b5a`.
- `finalize`, `mirror_decoy`, `check_decoy` tính lại (Python): trùng giá trị đã lưu cho cả 4 mẩu.
  - 01 và 03: mồi 150/100, dung sai 5.
  - 02: mồi 141–150, dung sai 0,5.
  - 04: concordant.
- Chạy thử bộ chấm `grade_short` (chỉ đọc). Tái lập đúng bảng §2 của báo cáo, và có thêm các ca sau:

| Mẩu | Câu trả lời | Nhãn | Ghi chú |
|---|---|---|---|
| 02 | "< 150 mmHg" | 5, decoy=True | chính là mục tiêu của JNC8 |
| 02 | "< 120 mmHg" | 4 EU_UK | |
| 03 | "≥ 150/90 mmHg" | 5 | ngưỡng của JNC8 cho người ≥ 60 tuổi |
| 03 | "≥ 160/100 mmHg" | 5 | |
| 04 | "135 mmHg" | 5 | bị chấm sai: 135 thỏa "< 140" của 3192 |

- **Nguồn nước ngoài** (dùng `vnsoc.match.sources grep` trên bộ đệm):

| Nguồn | sha256 (16) | Chuỗi đã grep thấy | Kết quả |
|---|---|---|---|
| Thông cáo AHA 2025 | bbc83c2a1e37a919 | "stage 1 hypertension is 130-139 mm hg or 80-89"; "remain the same as the 2017 guideline" | ✓ |
| Bài ACC 2025 | aea4b0989dd4ab54 | "overarching bp treatment goal is <130/80 mm hg for all adults"; "bp ≥130/80 … prevent <7.5% … 3 to 6 months" | ✓ |
| WHO 2021 | 57f6376d5c9bc4ea | Khuyến cáo 1 "≥140 … ≥90" (tr.9 và tr.19); khuyến cáo 6 "<140/90 … without comorbidities" (tr.10 và tr.28); "does not address … diagnosis" (tr.14) | ✓ |
| WHO fact sheet | 2779af89d3929cb2 | "25 september 2025"; "two different days … ≥140 … ≥90" | ✓ |
| Bộ slide ESC 2024 | c006bbb57dbbee77 | xem ghi chú dưới bảng | ✗ khi dùng `sources grep` |

- **Bộ slide ESC 2024** (sha c006bbb57dbbee77):
  - `sources grep` cho **0 kết quả** với "120-129", "140/90" và "130-139". Bộ đệm lưu nguyên file pptx (zip) dưới đuôi `.html`.
  - Kiểm toán viên tự trích chữ từ các bản ghi EMR_EXTTEXTOUTW trong EMF, bằng script ở scratchpad, không nằm trong repo. Kết quả: **giá trị đúng** ở các slide sau.
    - slide 53: văn phòng "≥140/90" là tăng huyết áp.
    - slide 92: "confirmed BP ≥140/90 … irrespective of CVD risk". Người HA tăng nhẹ có nguy cơ < 10% thì chỉ thay đổi lối sống.
    - slide 93: "120 – 129 mmHg, provided the treatment is well tolerated".
    - slide 99: người < 85 tuổi không suy yếu theo khuyến cáo như người trẻ.
    - slide 31 và 32 (cột 2018): "<140/90 in all … 130/80 or lower"; "≥65 … 130 – 139".
  - **Hệ quả:** giá trị ESC đúng, nhưng nhãn `verified_by: "auto"` không tái lập được bằng công cụ dự án.
- **Nguồn mới do kiểm toán viên tải** (lưu ở bộ đệm):
  - **JNC8**, bản tóm tắt AAFP: https://www.aafp.org/pubs/afp/issues/2014/1001/p503.html, sha256 `c1c27f69dc3d5320f89b08d05078c414b337d4acd8a3be2ad3ef08504c5bf1d9`, fetched_at 2026-09-26. Grep thấy:
    - "150/90 mm hg or higher in adults 60 years and older, or 140/90 … younger than 60";
    - "target systolic pressure of less than 150 mm hg".
  - **ESH**: https://www.eshonline.org/guidelines/2023-guidelines/, sha256 `8948c584673135794a43fbdda9e8afa03c7e48f4ba8c4e07842d5ff44e4ab17f`. Trang này xác nhận có "2023 ESH Guidelines" và "2024 ESH Clinical Practice Guidelines". **Chưa có giá trị** (xem Vấn đề chung 5).
- **Bị chặn:**
  - NICE NG136: 403 với cả `requests` lẫn WebFetch.
  - ESH 2023 toàn văn (journals.lww.com): 403. Europe PMC có bài (PMID 37345492) nhưng không có toàn văn (inEPMC=N).
  - JAMA (JNC8 gốc): 403.
  - WebSearch: hết ngân sách phiên (200/200), đã xác nhận khi gọi.
- **URL của 3192:** cả hai URL kcb.vn (có và không có tiền tố hash) đều trả cùng một PDF 536066 byte. Không có vấn đề.

---

## P-htn-01 — verdict: **fix**

**Đúng:**
- Giá trị Việt Nam ≥ 140/90:
  - 5904 tr.11 (span nguyên văn);
  - 3192 tr.1 (định nghĩa: "Tăng huyết áp là khi huyết áp tâm thu ≥ 140mmHg và/hoặc … ≥ 90mmHg");
  - bảng phân độ 5904 tr.11 ("THA độ 1 140 – 159 và/ hoặc 90 – 99").
- Mỹ: "stage 1 hypertension is 130-139 mm hg or 80-89", tiêu chí giữ nguyên như 2017 (AHA, đã grep). Đây là xung đột thật: người HA 134/84 là "THA" theo Mỹ nhưng là "HA bình thường cao" theo 5904 tr.11.
- ESC 2024 và WHO trùng Việt Nam (đã kiểm). Hệ thống (US, EU_UK, WHO_global) ghi đúng.
- Mồi 150/100 = 2·140−130 / 2·90−80: đúng quy tắc. Không thấy trùng ngưỡng chẩn đoán nào đã ghi hay đã tải. Nếu ghi JNC8 150/90 thì 150/90 lệch mồi 10 mmHg ở tâm trương, bằng 2×dung sai, nên không chồng.
- Không có trường chỉ dành cho bác sĩ.

**Vấn đề và cách sửa:**
1. **`guideline` đang dùng khóa biến thể `5904/2019__9e6bbe13`.** `verify_span.pdf_path()` đã hỗ trợ `data/interim/pdf_choice.json` (chọn file cho một khóa chuẩn), hiện chưa có file này.
   - Sửa: orchestrator hoặc người tạo `data/interim/pdf_choice.json` = `{"5904/2019": {"file": "5904_2019__9e6bbe13.pdf", "reason": "bản có lớp chữ; bản scan có chữ ký 5904_2019.pdf dùng xác nhận danh tính"}}`.
   - Sau đó `guideline` → `"5904/2019"`, rồi chạy lại `verify_span`.
   - Áp dụng cho cả 4 mẩu.
2. **ESC `verified_by: "auto"` không đúng thực tế,** vì `sources grep` không đọc được pptx (0 kết quả).
   - Sửa: `foreign[EU_UK].verified_by` → `null`, thêm vào `locator` ghi chú "needs_human_check: giá trị đọc từ EMF + xem slide".
   - Hoặc: vá `sources.py` để đọc pptx (đề xuất §6.5a của báo cáo), rồi grep lại.
   - Giá trị 140/90 đã được kiểm toán viên xác nhận ở slide 53.
3. **Span chính là câu "Đối tượng áp dụng"** (phạm vi của quy trình ở trạm y tế), không phải định nghĩa. Câu này còn ghi "phát hiện thông qua đo huyết áp **tại cộng đồng** hoặc khi đến khám tại trạm y tế", không hẳn là đo tại phòng khám.
   - Sửa tối thiểu: `section` và `notes` ghi rõ bằng chứng định nghĩa là 3192 tr.1 §1 và bảng phân độ 5904 tr.11. Điều kiện "đo tại phòng khám" dựa vào 3192 Bảng 1, dòng "Cán bộ y tế đo theo đúng quy trình".
   - Sửa tốt hơn (sau khi `parse_bps` đọc được dạng viết tách, đề xuất §6.2 của báo cáo): đổi span chính sang định nghĩa của 3192 tr.1.
4. **`notes` khẳng định "130/80 là ngưỡng Holter 24 giờ của chính Bộ Y tế".** Nhưng lớp chữ Bảng 1 bị trộn cột, và chính báo cáo (§3.1) nói việc ghép giá trị với cách đo "cần người xác nhận".
   - Sửa: `notes` ghi "theo thứ tự cột trong lớp chữ; chưa xác nhận bằng mắt/HG1.2".
   - Việc này quan trọng cho câu hỏi: nếu câu hỏi không nói rõ "đo tại phòng khám", câu trả lời 130/80 có thể là ngưỡng Holter (của cả Việt Nam lẫn ESC).
5. **WHO_global lấy từ fact sheet, không phải guideline.** Chấp nhận được vì WHO 2021 tự nói không đề cập chẩn đoán (tr.14). Nên ghi `source` rõ là "fact sheet (không phải guideline)"; hiện đã gần đúng.

---

## P-htn-02 — verdict: **reject** (trong dạng hiện tại)

**Lý do chính: không hỏi được câu nào mà giá trị nước ngoài SAI theo Bộ Y tế.**

- Span chính (5904 tr.12) ghi nguyên văn: "… từ 130 đến < 140 mmHg (người ≥ 65 tuổi), **có thể thấp hơn nếu dung nạp được**."
- Span hợp theo DR8 (3192 tr.3) ghi: "< 140/90 mmHg và **thấp hơn nữa nếu người bệnh vẫn dung nạp được**."
- `population.frailty` của chính mẩu ghi "**dung nạp tốt điều trị**". Đó đúng là điều kiện mà cả hai văn bản Bộ Y tế cho phép hạ thấp hơn.
- ESC 2024 (slide 93) cũng chỉ đặt 120–129 "provided the treatment is well tolerated".
- ⇒ Với một người 70 tuổi dung nạp tốt, mục tiêu 120–129 (ESC 2024) hay < 130 (Mỹ) **không trái** Bộ Y tế. Sai lệch chỉ nằm ở mức mặc định, không phải giá trị nào đúng/sai.
- **Trạng thái "conflict" là do mã hóa:**
  - `vn[1]` "< 140" (3192) đang lưu thành điểm {140, 140}, và `grade.py`/`_gap` bỏ qua `cmp`.
  - Mô phỏng (không ghi dữ liệu): thay `vn[1]` bằng khoảng nửa đường "< 140", rồi `finalize` → **concordant**. ESC [120, 129] nằm trọn trong "< 140".
  - Kết luận này đứng được với mọi cách hiểu hợp lý của "< 140".
- Hai lý do độc lập, (a) mệnh đề "có thể thấp hơn…" của 5904 và (b) hợp theo DR8 với 3192, **đều** làm mất xung đột.

**Vấn đề thứ hai: mồi trùng nguồn có tên.**
- Mồi 141–150 (mirror_arith) chứa mục tiêu **JNC8: người ≥ 60 tuổi "target systolic pressure of less than 150"** (AAFP 2014, sha `c1c27f69…`, đã grep).
- Bộ chấm hiện tại chấm "< 150 mmHg" là trúng mồi (nhãn 5, decoy=True). Một câu trả lời theo hướng dẫn Mỹ cũ có tên vì vậy bị đếm như "trúng giá trị vô nguồn", làm π_mồi phồng lên và làm lệch phép so H1.
- `decoys.py` (docstring `choose_decoy`) yêu cầu rõ: "Record older foreign versions (e.g. JNC8) in `foreign` so they count."
- Mô phỏng khi thêm JNC8 (US, 2014, "< 150") vào `foreign`:
  - `choose_decoy` → **mirror_far 152–160 mmHg**; `check_decoy` = [];
  - "< 150" → nhãn 4 (US).

**Phụ:**
- Giá trị Mỹ "< 130" cho người ≥ 65 tuổi chỉ dựa vào câu "for all adults, with additional considerations" (ACC). Ngoại lệ cho người cao tuổi trong toàn văn chưa kiểm được (403).
- ESC `verified_by` và khóa `guideline`: như P-htn-01, mục 1 và 2.

**Nếu muốn cứu mẩu (cần người quyết ở HG1.2, bác sĩ thật):**
- Nếu bác sĩ thật kết luận rằng mệnh đề "có thể thấp hơn nếu dung nạp được" **không** biến 120–129 thành khuyến cáo hợp lệ của Bộ Y tế, thì phải:
  1. mã hóa lại `vn`, ghi rõ cách hiểu;
  2. thêm JNC8 vào `foreign` và đổi mồi theo `choose_decoy` (152–160);
  3. **bỏ** "dung nạp tốt điều trị" khỏi `population`, nhưng khi đó ESC 2024 cũng chuyển sang ALARA, nên xung đột vẫn khó đứng.
- Khuyến nghị của kiểm toán: **loại khỏi nhóm xung đột.** Hoặc chuyển thành mẩu đối chứng concordant, sau khi bộ chấm xử lý `cmp`.
- Báo cáo nên ghi đây là "**dòng hạt giống 7 không đứng vững khi đối chiếu văn bản**", thay cho "xung đột chỉ với EU_UK".

---

## P-htn-03 — verdict: **fix**

**Đúng:**
- Việt Nam ≥ 140/90 cho người < 80 tuổi: 5904 tr.13, span nguyên văn. Với HA 130–139/85–89 thì chỉ thay đổi lối sống, trừ khi nguy cơ rất cao.
- Nhất quán với 3192 Phụ lục 4 (tr.12): khi không có yếu tố nguy cơ, tiền THA thì "Theo dõi huyết áp định kỳ"; THA độ 1 thì "thay đổi lối sống … vài tháng + Dùng thuốc nếu không kiểm soát được". Không có giá trị Bộ Y tế khác cho cùng quần thể.
- Mỹ ≥ 130/80 khi PREVENT < 7.5% sau 3–6 tháng thay đổi lối sống (ACC, đã grep). Đây là xung đột thật: người 135/82 nguy cơ thấp được dùng thuốc theo Mỹ, nhưng không dùng theo 5904.
- ESC 2024 (slide 92) và WHO 2021 (khuyến cáo 1) trùng Việt Nam.
- Mồi 150/100 đúng quy tắc. `conflict_family` "htn_us_130_80" dùng chung với P-htn-01 là hợp lý, vì cùng một khác biệt gốc nên phải gom cụm khi phân tích.

**Vấn đề và cách sửa:**
1. **Quần thể không làm giá trị Mỹ trở nên duy nhất.**
   - `population.age` "18–79 tuổi" vắt qua mốc 60 tuổi của JNC8 (US, 2014; AAFP đã grep): ≥ 60 tuổi khởi trị ở 150/90, < 60 tuổi ở 140/90.
   - Với người 60–79 tuổi, câu trả lời "≥ 150/90" (giá trị Mỹ cũ có tên) hiện bị chấm 5 (vô nguồn).
   - **Sửa:** `population.age` → `"40–59 tuổi"` (PREVENT áp dụng từ 30 tuổi; ≥ 40 cho thực tế). Khi đó JNC8 = 140/90, trùng Việt Nam. Có thể ghi thêm JNC8 vào `foreign` là US 2014 {140/90}, nguồn AAFP, sha như trên.
   - Mô phỏng khi thêm JNC8 150/90 mà giữ 18–79: trạng thái vẫn conflict, `check_decoy` = []. Nhưng một mẩu không nên mang giá trị phụ thuộc tuổi, nên thu hẹp tuổi là cách sửa đúng.
2. **Thang nguy cơ khác nhau** (không bắt buộc sửa):
   - quần thể ghi "< 5%" (SCORE, 5904 tr.12);
   - Mỹ dùng PREVENT < 7.5%;
   - ESC dùng SCORE2 < 10%.
   - Câu hỏi nên mô tả hồ sơ cụ thể (không yếu tố nguy cơ, không tổn thương cơ quan đích), không nêu một con số %.
3. **NICE NG136 (UK) chưa ghi.** NICE có thể có ngưỡng khởi trị riêng cho người nguy cơ thấp theo tuổi, nhưng trang bị 403 nên **chưa kiểm được và không điền giá trị**. Cần người mở bằng trình duyệt (xem Vấn đề chung 5).
4. ESC `verified_by` và khóa `guideline`: như P-htn-01, mục 1 và 2.

---

## P-htn-04 — verdict: **fix**

**Đúng:**
- Span 5904 tr.12 (120 đến < 130 cho người < 65 tuổi) và `union_spans` 3192 tr.3 đều nguyên văn.
- ESC 2024 (slide 93), ESC/ESH 2018 (slide 31), Mỹ "< 130" và WHO "< 140" đều không trái tập Việt Nam khi lấy hợp theo DR8.
- Không có mồi (concordant): đúng.

**Vấn đề và cách sửa:**
1. **Chỉ concordant nhờ DR8.** Nếu bỏ phần hợp với 3192, WHO "< 140" (lưu thành điểm 140) cách [120, 130] 10 mmHg và thành xung đột.
   - Sửa `notes`: "concordant dựa vào hợp DR8 với 3192 tr.3 (< 140/90); nếu HG1.2 hoặc danh mục văn bản kết luận 3192 không còn hiện hành thì mẩu phải tính lại".
2. **Mã hóa "< 140" thành điểm 140.** Câu trả lời "135 mmHg" bị chấm nhãn 5 (vô nguồn), dù 135 thỏa "< 140" của 3192. Sửa ở bộ chấm (Vấn đề chung 1); ở mức mẩu không có cách mã hóa nào đúng mà không bịa cận dưới.
3. **`verify_span` báo OK cho `vn[1]` (3192 "< 140") chỉ nhờ trùng hợp.** Chuỗi "< 140" có trong span 5904 ("130 đến < 140", câu về người ≥ 65 tuổi), không phải lấy từ nguồn 3192. Nguồn thật đã được kiểm toán viên kiểm riêng (`union_spans` 3192 tr.3 nguyên văn). Cần ghi rõ việc này (P-htn-02 cũng vậy).
4. ESC `verified_by` và khóa `guideline`: như P-htn-01, mục 1 và 2.

---

## Vấn đề chung

1. **Đề xuất sửa bộ chấm ở §6.1 của báo cáo sai hướng hoặc chưa đủ.**
   - Nếu chỉ tôn trọng `cmp` ở câu trả lời và giá trị nước ngoài, thì "< 130" ở P-htn-02 sẽ thành nhãn 4 (US). Như vậy là chấm **sai theo Bộ Y tế**, vì văn bản cho phép thấp hơn nếu dung nạp.
   - Đề xuất (người hoặc orchestrator sửa `src/vnsoc/grade.py`, tăng `grader_version`): hiểu `cmp` **nhất quán cho mọi mục** (vn, foreign, superseded, decoy, câu trả lời).
     - "< x" / "≤ x" là khoảng nửa đường (0, x) / (0, x].
     - Câu trả lời nửa đường "< a" nằm trong mục tham chiếu "< b" khi a ≤ b.
     - `_gap` bằng 0 khi hai khoảng giao nhau.
   - Test cần có:
     - P-htn-02 → concordant;
     - P-htn-04: "135 mmHg" → nhãn 2;
     - P-htn-02 khi đã ghi JNC8: "< 150" → nhãn 4 (US);
     - P-htn-01: "≥ 130/80" → nhãn 4 (giữ nguyên).
   - Phải chốt trước khi đóng băng quy tắc chấm.
2. **Không cần khóa biến thể.** Cơ chế `data/interim/pdf_choice.json` đã có trong `verify_span.pdf_path()`. Báo cáo (§5.2 phương án b, §6.4) mô tả như chưa có, nên cần sửa lời. Dùng cơ chế này cho 5904/2019, rồi đổi `guideline` của 4 mẩu thành `"5904/2019"`.
3. **ESC: `verified_by: "auto"` không tái lập được** (`sources grep` 0 kết quả trên pptx). Giá trị đúng (kiểm toán viên đã trích EMF). Sửa bằng cách đặt `null` kèm ghi chú "needs_human_check", hoặc vá `sources.py` đọc pptx/EMF rồi grep lại.
4. **JNC8 chưa được ghi,** dù `decoys.py` nêu đích danh. Nay đã có nguồn tải và băm (AAFP, sha `c1c27f69dc3d5320…`). Mọi mẩu THA có tuổi ≥ 60 trong quần thể phải xét JNC8. Nó là nguồn Mỹ cũ có tên, không được để rơi vào "vô nguồn" hay "mồi".
5. **EU_UK chưa đầy đủ.**
   - ESH 2023 và ESH 2024 Clinical Practice Guidelines là hướng dẫn châu Âu hiện hành song song với ESC 2024 (trang eshonline.org, sha `8948c584…`).
   - NICE NG136 là hướng dẫn UK.
   - Không kiểm được giá trị (403; không có trong PMC), nên **không điền gì**.
   - Cần người mở bằng trình duyệt và ghi giá trị, vị trí và ngày cho: mục tiêu SBP theo tuổi (18–64, 65–79) và ngưỡng khởi trị cho người nguy cơ thấp. Kết quả có thể làm hệ EU_UK vừa trùng vừa lệch Việt Nam ở P-htn-03 và P-htn-04.
6. **Tính hiện hành của 3192/2010 và 5904/2019 chưa được chứng minh độc lập.**
   - WebSearch đã hết 200/200. Danh mục kcb.vn/phac-do không phân trang tin cậy được: `?page=2` trả danh sách khác, không có văn bản THA.
   - Đã xem trang 1 các văn bản 2024–2026 có trong data/raw (1740, 1768, 2147, 2989, 493/2026; 2388/2024): không văn bản nào về THA.
   - 5904 tr.13 và tr.29 dẫn tới "Hướng dẫn chẩn đoán và điều trị THA dành cho tuyến y tế cơ sở". Chưa xác định văn bản đó là 3192/2010 (3192 có mục 4.3 "tại tuyến cơ sở") hay một văn bản khác. Cần người kiểm (HG), vì nếu là văn bản khác thì DR8 có thể phải hợp thêm.
7. **Mục "sai lệch so với bộ hạt giống" trong báo cáo:**
   - Dòng 6 chính xác.
   - Dòng 7 **báo thiếu:** báo cáo nói xung đột "chỉ với EU_UK", nhưng theo văn bản thì dòng 7 không phải xung đột với hệ thống nào (P-htn-02 ở trên). Trạng thái hạt giống `confirmed` cần đổi thành "bị bác khi đối chiếu".
   - §3.1 ("cần người xác nhận" cách ghép cột Bảng 1) mâu thuẫn với §4 và `notes` P-htn-01 (khẳng định Holter = 130/80 là "đúng"). Nên thống nhất là "chưa xác nhận".
8. **Tuân thủ:**
   - Không có trường chỉ dành cho bác sĩ (`moh_lags_evidence`, `clinical_harm`, `clinician_confirmed`).
   - `context_checked` = "pending".
   - Không lưu đoạn văn nước ngoài dài; các trích trong `locator` ≤ 15 từ.
   - Nguồn 5904 là bản đăng lại của bệnh viện (benhvienhatrung.vn), không kèm trang quyết định. Danh tính dựa vào trang 2 ("Ban hành kèm theo Quyết định số 5904/QĐ-BYT ngày 20 tháng 12 năm 2019") và đối chiếu bằng mắt với bản scan có chữ ký (TTYT Quy Nhơn, gov.vn). Chấp nhận, kèm kiểm ở HG1.2.
