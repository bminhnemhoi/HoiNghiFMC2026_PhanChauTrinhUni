# Phản biện độc lập: bộ câu hỏi thí điểm chủ đề htn

- **Người phản biện:** agent AI, kiêm hai vai rev-clinician và rev-methods. Đây KHÔNG phải bác sĩ thật; mọi nhận định lâm sàng vẫn chờ bác sĩ duyệt (HG1.2 / HG4.2).
- **Ngày:** 2026-09-26.
- **Đầu vào đã đọc:**
  - `qdrafts/htn.jsonl` (sha256 7562b0fecedd5ecf, 3 dòng);
  - mẩu P-htn-01, 03, 04 trong `data/interim/pilot_atoms.jsonl`;
  - `htn_q.jsonl` (sha256 6e25bdaa25f119f2, 14 câu), `htn_p.jsonl`, `htn_qc.csv`;
  - đề cương §1.2, §3.5, §4.3, §4.4, §5.7; SKILL question-generation; `configs/conditions.yaml`; `src/vnsoc/qgen/*.py`; `src/vnsoc/run/prompts.py`; `schemas.Question`;
  - `data/interim/pilot/htn_report.md` §7;
  - lớp chữ PDF: 3192/2010 tr.1, 3, 7, 12 và 5904/2019 tr.11–13.
- **Chống rò rỉ:** KHÔNG xem đầu ra của mô hình nào được kiểm tra. Những ví dụ chấm điểm ở dưới là câu trả lời do người phản biện TỰ VIẾT để thử bộ chấm.
- **Kiểm lại bằng mã:**
  - Chạy lại `vnsoc.qgen.build --only-drafted` trên bản nháp gốc, ghi ra scratchpad: 14 câu, 3 đoạn A3, **0 mục QC không đạt**. Kết quả giống hệt `htn_q.jsonl`.
  - Các bản sửa đề xuất bên dưới cũng đã chạy qua build trên bản sao ở scratchpad: đều **0 mục QC không đạt**.
  - Không sửa file nào ngoài file review này.

## Tổng hợp

| atom_id | Loại | Verdict | Vấn đề chính |
|---|---|---|---|
| P-htn-01 | conflict (US 130/80), bp | **pass** | Chỉ còn đánh bóng bản tiếng Anh (tùy chọn). Có vấn đề chéo về bộ chấm dạng HA viết tách (xem X1). |
| P-htn-03 | conflict (US 130/80), bp | **fix** | (a) "sau 3–6 tháng thay đổi lối sống" lặp gần nguyên văn khuyến cáo Mỹ 2025, tức là gợi ý nguồn nước ngoài. (b) Câu tiếng Việt 79 từ (tách theo khoảng trắng), vượt giới hạn 60. |
| P-htn-04 | concordant (đối chứng), num | **pass** | Tiếng Anh hơi vụng (tùy chọn sửa). "Dung nạp tốt" mở mệnh đề "có thể thấp hơn": ghi chú cho người chấm. |

**Kết quả: 2 pass / 1 fix / 0 drop.**

---

## P-htn-01: ngưỡng chẩn đoán THA, HA đo tại phòng khám

**Verdict: pass.** Không cần sửa. Chỉ có đề xuất đánh bóng (tùy chọn).

1. **Đáp án Bộ Y tế duy nhất? Giá trị nước ngoài có "cũng đúng" không?**
   - Đáp án Bộ Y tế là ≥ 140/90, duy nhất: định nghĩa ở 3192 tr.1, trùng 5904 tr.11.
   - 3192 Bảng 1 có ghép 130/80 cho Holter 24 giờ và 135/85 cho tự đo tại nhà. Câu hỏi đã loại trừ rõ cả hai cách đo, nên 130/80 không thể "đúng theo Bộ Y tế".
   - Đã kiểm thêm: nhóm 130–139/85–89 trong 3192 là "Tiền tăng huyết áp", không phải THA. Vì vậy 130/80 không trùng một nhãn chẩn đoán nào của Bộ Y tế.
   - ESC 2024 và WHO cùng ≥ 140/90. Chỉ Mỹ 2025 (≥ 130/80, giai đoạn 1) xung đột.
   - Câu hỏi không có giới hạn tuổi trên hay bệnh kèm. Điều này không làm đổi tập giá trị, vì mọi nguồn đã ghi đều dùng một ngưỡng chẩn đoán cho mọi người lớn.
   - Kết luận: câu **không mơ hồ**.
2. **Lộ đáp án hay gợi ý nguồn:**
   - Không có số nào của vn/foreign/decoy trong câu (QC đạt). Không nhắc quốc gia hay tổ chức.
   - "Nhân viên y tế" là cách nói trung tính. Người viết đã tránh "cán bộ y tế" và "trạm y tế", là cách dùng từ của văn bản Bộ Y tế. Đồng ý với lựa chọn này.
3. **Bản tiếng Anh:** trung thành về số (18, 24), phủ định và quần thể. Có hai chỗ diễn đạt chưa chuẩn tiếng Anh y khoa:
   - "24-hour ambulatory Holter monitoring": trong tiếng Anh, "Holter" thường chỉ Holter điện tim. Cụm chuẩn là "24-hour ambulatory blood pressure monitoring".
   - "health worker … following the correct procedure" mang giọng tài liệu WHO/y tế cơ sở. Nên dùng "healthcare professional using the standard procedure".
4. **Tự nhiên, bác sĩ Việt Nam hiểu ngay?**
   - Có. "Holter huyết áp 24 giờ" đúng là cách 3192 gọi (Phụ lục 2).
   - "chẩn đoán xác định … lần đầu" hơi cứng nhưng đúng ý "chẩn đoán mới" (khóa `setting` của mẩu). Không bắt buộc sửa.
5. **Trắc nghiệm** (htn_q.jsonl):
   - Bốn phương án 120/70, 130/80, 140/90, 150/100 cùng dạng "x/y mmHg".
   - Chỉ 140/90 đúng theo Bộ Y tế. Mồi 150/100 cách giá trị Việt Nam 10 mmHg, đối xứng với giá trị Mỹ.
   - Nhiễu 120/70 (do mã sinh) không phải ngưỡng chẩn đoán THA của nguồn nào. Lưu ý: 120/70 là cận dưới của nhóm "elevated BP" của ESC 2024 (không phải THA). Mô hình chọn 120/70 được chấm nhãn 5, không phải mồi, nên không ảnh hưởng phép so nước ngoài với mồi. Chấp nhận.
   - Hai thứ tự đảo đúng: mỗi phương án đổi chữ cái.
6. **Đơn vị:** câu ngắn ghi "(mmHg)"; phương án trắc nghiệm có "mmHg". Hỏi "tâm thu/tâm trương" để câu trả lời có dạng cặp, là hợp lý (xem X1).

**Đánh bóng tùy chọn** (đã chạy qua build, 0 lỗi QC):
- `short_en`: thay "by a health worker following the correct procedure" bằng "by a healthcare professional using the standard procedure"; thay "24-hour ambulatory Holter monitoring" bằng "24-hour ambulatory blood pressure monitoring". Sửa y như vậy ở `mcq_stem_en`.

---

## P-htn-03: ngưỡng HA khởi trị thuốc, nguy cơ thấp, 41–59 tuổi

**Verdict: fix.**

1. **Đáp án Bộ Y tế duy nhất? Giá trị nước ngoài có "cũng đúng" không?**
   - Đáp án Bộ Y tế là ≥ 140/90, duy nhất:
     - 5904 tr.13: khởi trị khi ≥ 140/90 ở người < 80 tuổi; ở mức 130–139/85–89 chỉ thay đổi lối sống, dùng thuốc chỉ khi nguy cơ rất cao.
     - 3192 Phụ lục 4 (tr.12, đã đọc lại): nếu không có yếu tố nguy cơ, "Tiền THA" chỉ cần theo dõi định kỳ; "THA độ 1" thì thay đổi lối sống **vài tháng**, rồi dùng thuốc nếu không kiểm soát được.
   - Mỹ 2025 là ≥ 130/80, và ngưỡng này không phụ thuộc tầng PREVENT (nguy cơ thấp: sau 3–6 tháng lối sống; nguy cơ cao: ngay). Vì vậy cách mô tả hồ sơ thay cho con số % là đúng. 130/80 không thể "đúng theo Bộ Y tế" với hồ sơ nguy cơ thấp. Câu **không mơ hồ**.
   - Có một điểm không nhất quán nội tại, nhưng **không đổi đáp án**:
     - 3192 tr.7 liệt kê "Tuổi (nam > 55, nữ > 65)" là một yếu tố nguy cơ. Nam 56–59 tuổi vì vậy có một yếu tố nguy cơ, mâu thuẫn với "không có yếu tố nguy cơ tim mạch nào khác".
     - Với 1–2 yếu tố nguy cơ, 3192 Phụ lục 4 vẫn cho: Tiền THA thì chỉ thay đổi lối sống; THA độ 1 thì dùng thuốc nếu không kiểm soát. Ngưỡng vẫn là 140/90. Không bắt buộc sửa.
2. **Lộ đáp án hay gợi ý nguồn: CÓ VẤN ĐỀ (lý do chính của verdict fix).**
   - Cụm "sau 3–6 tháng thay đổi lối sống" / "after 3–6 months of lifestyle change" lặp gần nguyên văn khuyến cáo Mỹ 2025, đúng câu mà mẩu dùng làm locator: "start medication if 3–6 months of lifestyle fail to lower BP <130/80".
   - Văn bản Bộ Y tế KHÔNG dùng mốc này. Đã grep lớp chữ: 3192 PL4 ghi "vài tháng"; sơ đồ 5904 ghi 1–3 tháng; ESC 2024 ghi 3 tháng.
   - Như vậy câu hỏi mang một dấu hiệu đặc trưng của nguồn nước ngoài xung đột. Dấu hiệu này có thể kéo mô hình về đáp án Mỹ 130/80 và làm tăng P(nước ngoài) mà **không** làm tăng P(mồi). Kết quả là phần vượt trội của H1 bị thổi phồng, một đe dọa về độ giá trị cấu trúc mà phản biện tạp chí dễ bắt.
   - Vi phạm quy tắc "không chứa từ gợi ý nguồn" (SKILL question-generation, mục 1).
   - Độ dài lối sống không cần cho tính duy nhất: ngưỡng Bộ Y tế (140/90) và ngưỡng Mỹ (130/80) đều không đổi theo thời gian thay đổi lối sống. Vì vậy có thể dùng một mốc trung tính mà không mất gì.
   - Tiếng Anh "stays high" là đúng. **Không** được đổi thành "remains elevated": "elevated BP" là tên nhóm của ESC 2024 (120–139/70–89) và của ACC/AHA.
3. **Bản tiếng Anh:** trung thành về số, phủ định và quần thể.
4. **Tự nhiên và độ dài:**
   - Câu tiếng Việt `short_vi` và `mcq_stem_vi` đều **79 từ** khi tách theo khoảng trắng, vượt ≤ 60. Mã dự án đếm "từ" theo cách này (`passages.py`: `len(text.split())`).
   - Người viết đã tự ghi nhận điểm này. Có thể rút xuống 60 mà không mất khóa quần thể nào:
     - "không hút thuốc, lipid máu bình thường" là ví dụ đã nằm trong "không có yếu tố nguy cơ tim mạch khác";
     - "(dày thất trái, protein niệu)" là ví dụ đã nằm trong "tổn thương cơ quan đích".
5. **Trắc nghiệm:**
   - Bốn phương án 120/70, 130/80, 140/90, 150/100, cùng đơn vị. Chỉ 140/90 đúng theo Bộ Y tế.
   - 150/100 không trùng JNC8 (140/90 cho < 60 tuổi; 150/90 cho ≥ 60 tuổi nằm ngoài quần thể).
   - Nhiễu 120/70 không phải ngưỡng khởi trị của nguồn nào. Chấp nhận.
6. **Đơn vị:** "(mmHg)" có trong câu ngắn và trong phương án.

**Sửa cụ thể:** thay 4 trường của dòng P-htn-03 trong `htn.jsonl`, rồi chạy lại build. Bản dưới đây đã chạy qua build: 0 lỗi QC. Tiếng Việt 60 và 59 từ, tiếng Anh 48 và 52 từ.

```json
{"short_vi": "Ở người 41–59 tuổi, không mang thai, không có yếu tố nguy cơ tim mạch khác, không đái tháo đường, bệnh thận mạn, bệnh tim mạch hay tổn thương cơ quan đích, huyết áp tại phòng khám vẫn cao qua nhiều lần khám sau vài tháng thay đổi lối sống, ngưỡng khởi trị thuốc hạ áp là bao nhiêu (mmHg)?",
 "short_en": "In a non-pregnant person aged 41–59 years with no other cardiovascular risk factors and no diabetes, chronic kidney disease, cardiovascular disease or target-organ damage, whose office blood pressure stays high at repeated visits after several months of lifestyle change, what blood pressure threshold warrants starting antihypertensive drugs (mmHg)?",
 "mcq_stem_vi": "Ở người 41–59 tuổi, không mang thai, không có yếu tố nguy cơ tim mạch khác, không đái tháo đường, bệnh thận mạn, bệnh tim mạch hay tổn thương cơ quan đích, huyết áp tại phòng khám vẫn cao qua nhiều lần khám sau vài tháng thay đổi lối sống, nên khởi trị thuốc hạ áp từ ngưỡng nào?",
 "mcq_stem_en": "In a non-pregnant person aged 41–59 years with no other cardiovascular risk factors and no diabetes, chronic kidney disease, cardiovascular disease or target-organ damage, whose office blood pressure stays high at repeated visits after several months of lifestyle change, from which of the following blood pressure thresholds should antihypertensive drugs be started?"}
```

- **Phương án dự phòng**, nếu điều phối viên chấp nhận đếm theo từ vựng (khoảng 55 từ) thay vì theo âm tiết:
  - chỉ thay "sau 3–6 tháng thay đổi lối sống" bằng "sau vài tháng thay đổi lối sống";
  - thay "after 3–6 months of lifestyle change" bằng "after several months of lifestyle change";
  - giữ nguyên phần còn lại. Bản này cũng đã chạy qua build: 0 lỗi QC.
- Việc thay "3–6 tháng" là **bắt buộc** ở cả hai phương án.
- **Việc cho người giữ mẩu** (người phản biện không được sửa atoms): đổi `population.prior_management` từ "đã thay đổi lối sống 3–6 tháng, HA vẫn tăng" thành "đã thay đổi lối sống vài tháng, HA vẫn tăng", để câu hỏi và mẩu khớp nhau. Khóa này không phải khóa định lượng, nên QC quần thể không bị ảnh hưởng.
- Tùy chọn: nếu muốn hết mâu thuẫn về yếu tố nguy cơ tuổi, có thể viết "phụ nữ 41–59 tuổi". Nhưng như vậy là thu hẹp quần thể so với mẩu, nên phải được người giữ mẩu đồng ý. Không khuyến nghị làm ngay, vì đáp án không đổi.

---

## P-htn-04: HA tâm thu mục tiêu, 18–59 tuổi, nguy cơ không cao (đối chứng)

**Verdict: pass.**

1. **Đáp án Bộ Y tế:**
   - Tập hợp gồm {120 đến < 130} (5904, < 65 tuổi) ∪ {< 140} (3192 tr.3, đã đọc lại: "< 140/90 … Nếu nguy cơ tim mạch từ cao đến rất cao thì … < 130/80").
   - "Nguy cơ tim mạch không cao" cùng với không có ĐTĐ, bệnh thận mạn, bệnh tim mạch đã loại đúng nhánh < 130/80 của 3192 và mục tiêu riêng của 5481.
   - Mọi giá trị nước ngoài đều nằm trong tập: ESC 2024 120–129; ESC/ESH 2018 < 140 và ≤ 130; Mỹ 2025 < 130; JNC8 < 140 (< 60 tuổi); WHO < 140. Trạng thái concordant là hợp lệ, nhưng phụ thuộc DR8 (mẩu đã ghi rõ).
   - Cận trên 59 tuổi tránh được JNC8 < 150.
2. **Lộ đáp án hay gợi ý nguồn:** không lộ. Người viết đã bỏ "trạm y tế" dù trường population có ghi. Đồng ý.
3. **Bản tiếng Anh:** trung thành. Riêng "cardiovascular risk that is not high" vụng; nên viết "without high cardiovascular risk". Đã chạy qua build: 0 lỗi QC.
4. **Tự nhiên:** tốt. Bác sĩ Việt Nam hiểu ngay.
5. **Trắc nghiệm:** không áp dụng (concordant, không có bản cũ). Stem và filler để null là đúng.
6. **Đơn vị:** có "(mmHg)".

**Ghi chú cho người chấm / người giữ mẩu (không phải lỗi câu hỏi):**
- "Dung nạp tốt" là khóa `status` của mẩu nên phải nêu. Tuy vậy, nó kích hoạt mệnh đề "có thể thấp hơn nếu dung nạp được" (5904) và "thấp hơn nữa nếu … dung nạp được" (3192).
  - Thử bộ chấm bằng câu trả lời tự viết: "ĐÁP ÁN: < 120 mmHg" bị chấm nhãn 5, dù có thể coi là hợp văn bản Bộ Y tế.
  - Hiếm gặp, nhưng nên ghi vào tiêu chí kiểm tay.
- Lỗi `cmp` đã biết ("135 mmHg" và "130–139" bị chấm nhãn 5; htn_report §7.5, §7.8) vẫn còn. Phải sửa bộ chấm trước khi đóng băng, nếu không tỉ lệ đúng của mẩu đối chứng sẽ bị hạ giả tạo.
- Về phương pháp: tập giá trị Bộ Y tế ở đây là hợp của hai văn bản nên rất rộng. Mẩu đối chứng này vì vậy **dễ hơn** các mẩu xung đột, vốn chỉ có một giá trị. Khi báo cáo số đếm a/b "xung đột so với đối chứng" (§5.7) cần nói rõ, hoặc đưa độ rộng tập giá trị vào làm hiệp biến. Không nên đọc chênh lệch như một phép so khớp chuẩn.

---

## Vấn đề chéo (ngoài phạm vi bản nháp; chuyển điều phối viên)

- **X1. Bộ chấm với HA viết tách (nghiêm trọng cho H3 ở P-htn-01).** Dùng câu trả lời tự viết để thử `grade_short`:
  - "ĐÁP ÁN: HA tâm thu ≥ 140 mmHg và/hoặc HA tâm trương ≥ 90 mmHg" cho nhãn **6 (từ chối)**;
  - "ANSWER: SBP ≥140 mmHg and/or DBP ≥90 mmHg" cho nhãn 6;
  - "≥130 mmHg systolic or ≥80 mmHg diastolic" cho nhãn 6.

  Đoạn oracle A3 của P-htn-01 nêu ngưỡng đúng ở dạng tách này ("huyết áp tâm thu ≥ 140mmHg và/hoặc huyết áp tâm trương ≥ 90mmHg"). Mô hình chép lại nguyên dạng sẽ bị tính là từ chối. Điều đó hạ cả tỉ lệ đúng lẫn tỉ lệ cố chấp ở A3.
  - Cần sửa `normalize_vi.parse_bps` (dạng "tâm thu ≥ X … tâm trương ≥ Y", "SBP ≥ X and/or DBP ≥ Y") và thêm test, trước khi đóng băng quy tắc chấm.
  - Nếu chưa sửa được, phải bảo đảm bộ tách LLM dự phòng (DR9) nhận các câu nhãn 6 còn chứa số.
  - Mẩu đã ghi rằng "parse_bps chưa đọc dạng viết tách". Chỗ mới ở đây là hệ quả trực tiếp cho A3.
- **X2. Nhãn mục trong prompt A3.** `short_prompt` đưa nguyên `atom["section"]` vào prompt. Với P-htn-01 prompt thành:

  > "section 1. ĐỊNH NGHĨA (cùng trang: 3.1 Chẩn đoán xác định THA, Bảng 1 — ngưỡng theo cách đo, dòng 'Cán bộ y tế đo theo đúng quy trình')"

  Đây là ghi chú của người trích mẩu, nhắc tới Bảng 1 không có trong đoạn trích, và xuất hiện cả trong prompt tiếng Anh. Không lộ giá trị nhưng là nhiễu. Đề xuất dùng một nhãn hiển thị sạch (ví dụ "1. ĐỊNH NGHĨA"), qua trường riêng hoặc cắt phần trong ngoặc. Việc này cần người giữ mẩu hoặc mã.
- **X3. Thứ tự trắc nghiệm.** Thứ tự 1 là thứ tự 0 đảo ngược, nên phương án ở giữa (B/C) luôn ở giữa và phương án ở biên (A/D) luôn ở biên.
  - Ở cả hai mẩu htn, đáp án Bộ Y tế luôn nằm ở B/C.
  - Giá trị Mỹ ở biên (P-htn-01) và ở giữa (P-htn-03). Mồi thì ngược lại.

  Thiên lệch vị trí kiểu "giữa so với biên" vì vậy không triệt tiêu trong từng mẩu. Trên toàn bộ tập nó được cân bằng nhờ xáo trộn có seed. Đề xuất ghi vị trí làm hiệp biến trong phân tích trắc nghiệm, hoặc cân nhắc xoay vòng 4 thứ tự ở nghiên cứu chính. Mức độ thấp.
- **X4. Đoạn A3 của P-htn-03** bắt đầu bằng số trang in sót "4 3. Cần khởi trị sớm…". Chỉ là hình thức, không có giá trị lạ (cột `passage_has_alt_value` trống).
- **X5. Mẩu P-htn-01 và P-htn-03 cùng nhóm xung đột `htn_us_130_80`,** nên chỉ là một cụm khác biệt gốc. Không phải lỗi câu hỏi; ghi lại để tính cụm.

## Kiểm lại sau sửa

Sau khi người viết áp bản sửa P-htn-03, chạy:

```
cd "/d/phan chau trinh _ y khoa" && PYTHONUTF8=1 .venv/bin/python -m vnsoc.qgen.build \
  --atoms data/interim/pilot_atoms.jsonl --drafts data/interim/pilot/qdrafts/htn.jsonl \
  --out data/interim/pilot/qdrafts/htn_q.jsonl --passages data/interim/pilot/qdrafts/htn_p.jsonl \
  --qc data/interim/pilot/qdrafts/htn_qc.csv --only-drafted
```

Kết quả phải là 14 câu và 0 mục QC không đạt. Sau đó kiểm bằng mắt rằng các câu P-htn-03 trong `htn_q.jsonl` không còn chứa "3–6".

---

## Xử lý phản biện (người viết câu hỏi/người giữ mẩu, agent AI, 2026-09-26, lượt 2)

Phần này do agent atom-extractor + question-writer ghi, không phải người phản biện. Không xem đầu ra mô hình nào.

- **P-htn-03 (fix):** bản nháp đã dùng bản sửa của phản biện ("vài tháng"/"several months", VI 60/59 từ). Mẩu: `population.prior_management` → "đã thay đổi lối sống vài tháng, HA vẫn tăng"; bỏ ghi chú nguồn "của 5904 tr.12" khỏi `population.cv_risk`. "Vài tháng" là chữ của 3192 PL4 tr.12 (không YTNC + THA độ 1). Câu hỏi trong `htn_q.jsonl` không còn "3–6".
- **P-htn-01, P-htn-04:** đánh bóng EN đã có trong bản nháp. Ghi chú người chấm của P-htn-04 (dung nạp tốt → "< 120" kiểm tay; tập Bộ Y tế là hợp hai văn bản) đã chép vào `extraction.notes` của mẩu.
- **X1:** hết. Grader 1.1.0 chấm dạng HA viết tách (VI/EN, cả dạng chép từ đoạn A3) → nhãn 2 cho 140/90, nhãn 4 cho 130/80 (câu trả lời tự viết).
- **X2:** hết. Nhãn mục trong prompt A3 nay là "1. ĐỊNH NGHĨA".
- **X3:** hết. Thứ tự 1 = thứ tự 0 xoay 2 vị trí; đáp án Bộ Y tế ở C (thứ tự 0) và A (thứ tự 1) ở cả hai mẩu.
- **X4:** hết. Đoạn A3 của P-htn-03 bắt đầu "3. Cần khởi trị sớm…".
- **X5:** P-htn-01 và P-htn-03 cùng `conflict_family` "htn_us_130_80" và cùng họ cơ học `fam_6265f986bb` (threshold::bp::mmHg::140/90::130/80).
- **Nhiễu trắc nghiệm mới (mã sinh):** 160/110 mmHg thay 120/70 cho cả hai mẩu bp. Phương án: 130/80 · 140/90 · 150/100 · 160/110, cùng dạng, không từ gợi nguồn. Chỉ 140/90 đúng theo Bộ Y tế. option_rank foreign<vn<decoy<filler: giá trị Mỹ ở biên. Đây là do đồng xu của mã, nghiêng về phía bảo thủ với H1.
- **Thêm (không có trong phản biện):**
  - `moh_neighbour` có nguyên văn:
    - P-htn-01: 3192 tr.1 Bảng 1, 24 giờ ≥ 130/80, tại nhà ≥ 135/85. Ghép theo thứ tự cột, chờ HG1.2.
    - P-htn-03: 5904 tr.13, ≥ 80 tuổi ≥ 160/90; nguy cơ rất cao 130–139/85–89.
  - Mã tính ra `moh_neighbour_overlap` = True cho cả hai. Hai mẩu bị loại ở phân tích độ nhạy N1/B.21; phân tích chính không đổi. Đoạn A3 của P-htn-03 được gắn cờ `neighbour`.
  - Thêm `required_terms` (cách đo; nguy cơ tim mạch; dung nạp) cho cả 3 mẩu. Mọi câu đều qua QC.
- **Kiểm lại:**
  - `pilot_merge --only htn`: giữ 3, loại 0.
  - `qgen.build --only-drafted`: 14 câu, 3 đoạn A3, 1 mẩu bỏ trắc nghiệm có chủ đích (P-htn-04), **0 mục QC không đạt**.

---

## Xử lý người kiểm độc lập (người viết câu hỏi/người giữ mẩu, agent AI, 2026-09-26, lượt 3)

Phần này do agent atom-extractor + question-writer ghi. Không xem đầu ra mô hình nào; mọi câu trả lời dùng để thử bộ chấm là câu tự viết. Chữ câu hỏi, phương án, thứ tự và đoạn A3 không đổi: `htn_q.jsonl`, `htn_p.jsonl`, `htn_qc.csv` build lại giống hệt từng byte bản lượt 2.

- **Bộ chấm, dạng HA (nên sửa, ngoài dữ liệu htn):** đã thử lại bằng câu tự viết, đúng như người kiểm nêu. `grade_short` cho nhãn 6 với 'ANSWER: 140 over 90 mmHg', 'at least 130 over 80 mmHg', '≥140/≥90 mmHg', '≥130/≥80 mmHg', '140 và 90 mmHg' và '130-139 systolic or 80-89 diastolic'. HA dạng khoảng bị ghép thành cặp (b, c): '130–139/80–89' cho nhãn 5 (đúng ra 4), '140–159/90–99' cho nhãn 5 (đúng ra 2). Người sửa dữ liệu không được sửa `src/`, nên đã ghi danh sách kiểm tay vào `extraction.notes` của P-htn-01 và P-htn-03: mọi câu nhãn 5/6 còn chứa số HA phải kiểm tay; khoảng a–b/c–d đọc theo cận dưới a/c. **Việc của điều phối viên:** sửa `parse_bps` (thêm các dạng trên, kèm test) trước khi đóng băng quy tắc chấm; nếu chưa sửa kịp, bộ tách DR9 phải nhận mọi câu nhãn 6 còn chứa số.
- **P-htn-04, lỗi cmp (nên sửa):** tiêu chí kiểm tay trong `extraction.notes` đổi thành: *mọi giá trị hoặc khoảng nằm trọn dưới 140 mmHg, và mọi đích < 120 mmHg*. Thử bằng câu tự viết: '135', '130–139', '130 to 135', '< 120', '110-119' đều cho nhãn 5. **Việc của điều phối viên:** sửa cách bộ chấm hiểu `cmp` trước khi đóng băng.
- **P-htn-01, giá trị lân cận theo cách đo (nên sửa):** hai giá trị của 3192 Bảng 1 (Holter 24 giờ ≥ 130/80, tự đo tại nhà ≥ 135/85) được chuyển từ `moh_neighbour` sang `extraction.moh_neighbour_pending`. Span và giá trị giữ nguyên. Lý do: định nghĩa đã viết (prereg §4, §5.6 B.21; docstring `NeighbourValue`) chỉ gồm bước khác, quần thể khác, tuyến khác. Hệ quả do mã tính:
  - `moh_neighbour_overlap`: P-htn-01 = False (vào lại N1); P-htn-03 vẫn = True (Mỹ 130/80 cách giá trị 130/85 của nhóm nguy cơ rất cao 5 < 10).
  - `n_neighbour_overlap` của htn: 2 → 1.

  **Việc cần người quyết (điều phối viên/người dùng):** có coi "cách đo khác" là bối cảnh lân cận không. Lý do nên nhận: 130/80 là ngưỡng Holter của chính Bộ Y tế (và của ESC 2024), nên câu trả lời 130/80 có thể do nhầm cách đo chứ không do hướng dẫn Mỹ; đó đúng là mục đích của N1. Các chủ đề khác cũng đang ghi giá trị lân cận nằm ngoài ba loại đã viết (P-hbv-01/02: AST, một chất phân tích khác; P-controls-09: ngưỡng béo phì, một nhóm phân loại khác), nên phải quyết đồng loạt, ghi `docs/DECISIONS.md` và sửa câu chữ prereg trước HG2.9. Nếu nhận thì chép `records` trong `moh_neighbour_pending` về `moh_neighbour`. Câu hỏi vẫn giữ phần loại trừ Holter/tự đo tại nhà: bỏ phần này thì đáp án Bộ Y tế không còn duy nhất.
- **P-htn-03, khóa văn bản (nhỏ):** `moh_neighbour[*].guideline` đổi thành null (= cùng văn bản với mẩu). Nếu HG1.2/HG2.3 đổi sang bản scan có chữ ký thì đoạn này ở trang 14, phải sửa cùng lúc với trang của mẩu.
- **P-htn-03, mồi (nhỏ):** đã xem ảnh 5904 tr.13 (`verify_span --image`). Ô sơ đồ ghi "Đơn trị cho người THA độ I nguy cơ thấp (HATTh < 150mmHg) hoặc người rất già (≥ 80 tuổi) hoặc dễ tổn thương". Chữ này chỉ có trong ảnh: `--find '150'` không ra tr.13. Đã ghi vào `extraction.notes` cho người chấm HG3.5. Không đổi mồi vì mồi do quy tắc sinh; không đặt `decoy_plausible`.
- **Vị trí phương án (nhỏ):** giữ nguyên. Đề xuất đưa biên/giữa làm hiệp biến trong phân tích trắc nghiệm (đã ghi trong notes bản nháp).
- **`atom_flags check` (nhỏ):** vẫn 6 vấn đề đóng băng, đều không thuộc việc sửa dữ liệu:
  - `conflict_family` đặt tay ≠ `fam_6265f986bb`: mọi chủ đề đều đặt tay; điều phối viên đổi lúc đóng băng.
  - `context_checked` = pending.
  - `decoy_plausible` chưa chấm (HG3.5).
- **Ghép cột 3192 Bảng 1 (nhỏ):** vẫn chờ người thật xác nhận ở HG1.2. AI đã xem ảnh trang, nhưng như thế không được coi là đã duyệt.
- **Kiểm lại bằng mã:**
  - `pilot_merge --only htn`: giữ 3, loại 0. Cảnh báo ESC là cảnh báo cũ: slide EMF, `verified_by` null.
  - `qgen.build --only-drafted`: 14 câu, 3 đoạn A3, 1 mẩu bỏ trắc nghiệm có chủ đích, **0 mục QC không đạt**.
  - Schema atom/question hợp lệ.
  - Chấm thử bằng câu tự viết:
    - các dạng thông dụng: Bộ Y tế → 2, Mỹ → 4, mồi → 5 (`decoy_match`), nhiễu → 5, từ chối → 6;
    - dạng chép đoạn A3 → 2;
    - không có giá trị bản cũ nên không có phép thử nhãn 3;
    - 16 ca lệch đều là lỗi bộ chấm đã biết ở trên.
