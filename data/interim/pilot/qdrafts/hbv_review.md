# Phản biện độc lập — bộ câu hỏi thí điểm chủ đề hbv (P-hbv-01..10)

- Vai: rev-clinician + rev-methods. **Người phản biện là AI, không phải bác sĩ thật.** Không thay cho HG3.9.
- Ngày: 2026-09-26. Đã đọc: `hbv.jsonl` (bản nháp), `pilot_atoms.jsonl` (P-hbv-*), `hbv_q.jsonl`, `hbv_qc.csv`, `hbv_p.jsonl`, `src/vnsoc/qgen/*.py`, `grade.py` (grade_short/grade_mcq/_gap), đề cương §3.5, §4.3, §4.4, §5.7, SKILL question-generation.
- **Không xem đầu ra của mô hình nào** (quy tắc chống rò rỉ). Các phép thử chấm điểm bên dưới dùng câu trả lời do người phản biện tự gõ.
- Mọi đề xuất viết lại ở mục 3 **đã chạy thử** bằng `vnsoc.qgen.build --only-drafted` trên bản sao trong scratchpad (không ghi vào dữ liệu dự án). Kết quả: 0 lỗi lộ đáp án, số quần thể, số VI≠EN, phủ định; mọi câu VI ≤ 60 từ (đếm theo khoảng trắng). Chỉ còn 2 lỗi dự kiến: P-hbv-05 MCQ (mẩu không có mồi) và P-hbv-06 MCQ (tôi cố ý bỏ stem).

## 1. Tóm tắt

| atom | dạng | trạng thái | phán quyết chung | lời câu (người viết) | việc cần làm ngoài bản nháp |
|---|---|---|---|---|---|
| P-hbv-01 | num U/L | indistinguishable | **fix** | fix (phụ thuộc sửa mẩu) | mẩu: population.age → ≥ 18; mồi 25 → 26 |
| P-hbv-02 | num U/L | indistinguishable | **fix** | fix (phụ thuộc sửa mẩu) | mẩu: population.age → ≥ 18 |
| P-hbv-03 | num IU/mL | indistinguishable | **fix** | fix (VI) | mã: dấu so sánh của mồi/nhiễu, nhãn vai trò, nhiễu 38.000 |
| P-hbv-04 | cat | indistinguishable | **fix** | fix (VI) | mẩu: mồi gt_3x, regex gt_1x, text phương án; A3 |
| P-hbv-05 | num kPa | concordant | **pass** (câu ngắn) · MCQ **drop** | pass | mã: bỏ MCQ khi bản cũ trùng giá trị Bộ Y tế |
| P-hbv-06 | drugs | concordant | **fix** · MCQ **drop** | fix (thêm HIV) | mã: bỏ MCQ; lỗi options() với tập nhiều giá trị |
| P-hbv-07 | num năm | **conflict** (duy nhất) | **fix** | pass (có góp ý nhỏ) | mã: "tuổi"→"năm", dấu so sánh mồi; mẩu: giá trị suy ra; kiểm AASLD |
| P-hbv-08 | num IU/mL | indistinguishable | **fix** | fix (VI) | mã: như P-hbv-03; nhãn WHO 2015 |
| P-hbv-09 | num kPa | concordant | **fix** (chỉ MCQ) | pass | mẩu: cần mồi (MCQ sẽ đủ 4 phương án) |
| P-hbv-10 | num index | indistinguishable | **fix** (chỉ MCQ/A3) | pass | mã: hiển thị "index", dấu so sánh; mẩu: mồi = ngưỡng F2 thật; A3 |

**Đếm theo mẩu (phán quyết chung): pass 1 · fix 9 · drop 0.** Thêm 2 thành phần MCQ nên bỏ (P-hbv-05, P-hbv-06).
**Chỉ tính lời câu hỏi (phần người viết kiểm soát):** pass 4 (05, 07, 09, 10) · fix 6 (01, 02, 03, 04, 06, 08) · drop 0.

Không câu nào **mơ hồ** theo tiêu chí (1): với quần thể đã nêu, mỗi câu có đúng một đáp án Bộ Y tế (P-hbv-06 là một tập được chấp nhận), và giá trị nước ngoài xung đột không đồng thời đúng theo 1740/2026. Không câu nào lộ giá trị hay nhắc Việt Nam, Bộ Y tế, WHO, Mỹ hoặc số quyết định. Phần lớn lỗi nằm ở **mã dựng/hiển thị trắc nghiệm, chấm điểm và mẩu**, không ở lời câu.

## 2. Vấn đề nghiêm trọng (phải xử lý trước khi đóng băng)

**S1. Phương án trắc nghiệm để lộ phương án nào là "thật" qua dấu so sánh** (mã `match/decoys.py` + `qgen/mcq.rule_filler`; P-hbv-03, 07, 08, 10).
Giá trị Bộ Y tế, nước ngoài và bản cũ hiện có dấu `>`/`≥`. Mồi và nhiễu thì không, vì cả hai được sinh ra không kèm `cmp`. Ví dụ đang có trong `hbv_q.jsonl`:
- P-hbv-03: `38.000 IU/mL` · `> 2.000 IU/mL` · `≥ 20.000 IU/mL` · `200 IU/mL`
- P-hbv-07: `≥ 3–4 …` · `≥ 1 …` · `5 …` · `≥ 2 …`
- P-hbv-10: `> 2 index` · `0,5 index` · `> 1 index` · `3 index`

Mô hình loại được mồi và nhiễu chỉ nhờ hình thức. P(mồi) vì thế bị kéo xuống giả tạo, làm phồng tương phản P(nước ngoài) so với P(mồi) của §3.5/H1. P-hbv-07 là mẩu xung đột duy nhất của chủ đề nên bị ảnh hưởng trực tiếp.
**Sửa:** mồi và nhiễu kế thừa `cmp` của giá trị Bộ Y tế (hoặc bỏ `cmp` ở mọi phương án khi hiển thị). Thêm vào QC một kiểm tra "các phương án cùng khuôn: cùng có hoặc cùng không có dấu so sánh, cùng dạng điểm hoặc khoảng". Rất có thể lỗi này có ở mọi chủ đề, không riêng hbv.

**S2. MCQ tiếng Việt của P-hbv-07 hiển thị "tuổi" thay cho "năm"** (`render.py` UNIT_VI `"year": "tuổi"`).
Phương án đang là `≥ 3–4 tuổi`, `≥ 1 tuổi`, `5 tuổi`, `≥ 2 tuổi`, vô nghĩa với câu hỏi về thời gian. QC không bắt được lỗi này. Bản tiếng Anh cũng sai ngữ pháp: `≥ 1 years`.
**Sửa (mã):** tách đơn vị tuổi khỏi đơn vị thời gian, ví dụ theo `slot_type == "duration"` → "năm"/"year(s)", hoặc dùng mã đơn vị riêng cho tuổi. Trước khi sửa, không dùng 2 câu `P-hbv-07|mcq|vi|o0/o1`.

**S3. Nhãn trắc nghiệm không nhất quán với nhãn câu trả lời ngắn, và gán WHO không ghi phiên bản** (`mcq._conflicting`/`options`; P-hbv-01, 03, 08, 10).
Khi giá trị nước ngoài trùng giá trị bản cũ, `options()` bỏ vai trò bản cũ, nên chọn phương án đó ra **nhãn 4 (nước ngoài)**. Cùng giá trị ấy ở câu ngắn lại ra **nhãn 3 (temporal)**. Tôi đã kiểm bằng `grade_short`: "35 U/L" (01), "≥ 20.000" (03), "> 20.000" (08), "> 2" (10) đều ra nhãn 3 kèm cả foreign lẫn superseded.
Ngoài ra, giá trị WHO 2015 (bản đã bị WHO 2024 thay) mang vai trò `foreign:WHO_global` (08, 10; và `US+WHO_global` ở 03), trong khi WHO 2024 hiện hành **trùng** Bộ Y tế. Quy một câu trả lời về "WHO" như vậy là sai cho RQ2 (lệch theo chuẩn nước ngoài có tên).
**Sửa:** vai trò mang đủ nguồn (ví dụ `foreign:US|superseded:3310/2019`) và `grade_mcq` áp cùng thứ tự ưu tiên như `grade_short`. Khóa hệ thống có phiên bản (`WHO_global@2015`), hoặc xếp WHO 2015 là "nước ngoài đã bị thay".

**S4. P-hbv-04: bộ regex cat chấm lệch về phía đáp án cũ/nước ngoài** (mẩu, `cat_options`). Tôi đã thử `grade_short`:
- Đáp án Bộ Y tế viết gọn → **nhãn 6 (abstain)**: `> ULN`, `1 lần ULN`, `> 1 ULN`, `1x ULN`, `> 1 times ULN`.
- Đáp án bản cũ/nước ngoài viết gọn → **nhận dạng được** (nhãn 3): `2 lần ULN`, `≥ 2 ULN`, `2x ULN`. Riêng `2 times ULN` thì không.

Gợi ý đơn vị "(so với ULN)" trong câu và khuôn `ĐÁP ÁN: <giá trị> <đơn vị>` làm câu trả lời `> ULN` rất dễ xảy ra.
**Sửa regex gt_1x_uln**, ví dụ: `(^|[^\d.,])[>≥]\s*(1\s*(x|×|lan|times)?\s*)?(uln|gioi han tren)` và `(?<![\d.,])1\s*(x|×|lan|times)?\s*(uln|gioi han tren)`. Với gt_2x_uln thêm `(2|two)\s*times\s*(the\s*)?(uln|upper limit)`. Sau đó chạy lại test chấm.

**S5. Chẩn đoán "chỉ thiếu mồi" của người viết đúng cho 04 và 09 nhưng sai cho 05 và 06.** Tôi đã mô phỏng `mcq.options` với mồi thêm tạm trong bộ nhớ:
- **P-hbv-05:** bản cũ 3310 (≥ 7 kPa) trùng giá trị Bộ Y tế (gap = 0). Có thêm mồi và nhiễu vẫn chỉ được 3 phương án (`số lựa chọn = 3`), nên MCQ không bao giờ dựng được và cũng không có ý nghĩa.
- **P-hbv-06:** thêm mồi (adefovir) và nhiễu (lamivudine) thì MCQ **dựng được nhưng sai im lặng**: ETV mang vai trò `superseded:3310/2019` trong khi ETV là phác đồ **ưu tiên hiện hành** của 1740. Kết quả là hai đáp án đúng, và mô hình chọn ETV bị chấm nhãn 3. Nguyên nhân: `options()` chỉ so ứng viên với `vn[0]`, không so với cả tập `vn`.
- **Sửa (mã, `build.py` + `mcq.py`):** (a) chỉ làm MCQ khi có ít nhất một giá trị nước ngoài hoặc bản cũ nằm **ngoài toàn bộ tập vn** (gap > 0 với mọi phần tử vn); (b) trong `options()`, loại mọi ứng viên có gap = 0 với **bất kỳ** phần tử vn nào.

**S6. Đoạn A3 có giá trị gây nhiễu mà QC không gắn cờ, và có thông tin cá nhân** (`passages.py`, `qc.passage_alt_values`):
- **P-hbv-10#A3** có "APRI > 0,5" (ngưỡng F2), trùng giá trị mồi 0,5. QC để trống vì giá trị đơn vị `index` không có đơn vị viết rõ nên bị xếp "assumed". Cần gắn cờ tay `decoy` và đưa vào loại trừ của phân tích độ nhạy H3.
- **P-hbv-04#A3** có câu dành cho vị thành niên: "ALT > giới hạn trên … **ít nhất 2 lần** trong 6-12 tháng". Đây là mồi đọc nhầm thành "2 lần ULN" (gt_2x = bản cũ/Mỹ) trong khi quần thể là 18–30 tuổi. Cần gắn cờ tay `neighbour`.
- **P-hbv-07#A3** đã được gắn cờ `superseded`: "12 tháng" là thời gian củng cố của nhóm HBeAg dương tính, trùng giá trị bản cũ suy ra "≥ 1 năm". Câu trả lời "12 tháng" ở A3 là nhầm ngữ cảnh lân cận, không phải bám bản cũ. Nên thêm `moh_neighbour` cho mẩu.
- **3 đoạn hbv (05, 09, 10, cùng trang 19) và 1 đoạn controls** chứa dòng hình mờ khi tải từ kcb.vn: `tienph.kcb_<họ tên một cán bộ>_17/06/2026 11:12:23`. Đó là tên người thật, và số "11" trong đó trùng giá trị bản cũ 3310 của P-hbv-09. Cần lọc dòng hình mờ trong `passages.py` trước khi dùng A3 hay phát hành.

**S7. P-hbv-01: mồi 25 U/L là giá trị thật** (ULN nữ của AASLD/3310, tức mẩu anh em). Ghi chú mẩu nói đã đổi sang 26, nhưng trường `decoy` vẫn là 25. Chọn "25" là nhầm giới tính, không phải lỗi ngẫu nhiên. **Sửa mẩu:** decoy = 26 U/L, rồi dựng lại.

**S8. P-hbv-07 (mẩu xung đột duy nhất, vào H1): giá trị Mỹ ≥ 2 năm còn mong manh.** Giá trị lấy từ slide 33, không có dòng trích Ghany 2025. Khuyến cáo chính (Rec 5) là không ngừng NA đến khi mất HBsAg, trùng quy tắc của 3310. Phải đối chiếu toàn văn AASLD 2025 (cần người) trước khi đóng băng. Nếu không xác nhận được, chuyển mẩu sang no_counterpart/indistinguishable.

## 3. Nhận xét và sửa cụ thể theo từng mẩu

### P-hbv-01 — fix
1. Đáp án duy nhất: có, Bộ Y tế 30 U/L. Mỹ 35 (= 3310) không đúng theo 1740.
2. Gợi ý nguồn: cụm "(tiêu chí điều trị áp dụng cho người ≥ 12 tuổi)" **không liên quan** đến giá trị được hỏi (ULN của nam người lớn) và là **dấu vân tay của WHO 2024** (hướng dẫn lớn đầu tiên gộp trẻ ≥ 12 tuổi). Ở A0 cụm này có thể kéo mô hình về 30/19 (= Bộ Y tế) và làm giảm khả năng phát hiện lệch theo AASLD. Cụm này chỉ có vì `population.age` của mẩu buộc phải có số 12.
3. Bản tiếng Anh: trung thành. 4. Lâm sàng: rõ, và đã tránh được đáp án 40 U/L của phòng xét nghiệm. 6. Đơn vị: (U/L).
5. MCQ: 30 / 25 (mồi = giá trị thật, xem S7) / 35 (Mỹ, cũng là 3310; nhãn, xem S3) / 40 (nhiễu). 40 U/L là ULN phổ biến của phòng xét nghiệm (theo trí nhớ, gần mức EASL 2017 dùng; **chưa kiểm**), nên là phương án nhiễu mạnh nhưng không thuộc nguồn nào đã ghi. Chấp nhận được, nhưng ghi chú khi đọc tỉ lệ chọn.
- **Sửa mẩu:** `population.age` = "người lớn (≥ 18 tuổi)" (ULN của 1740 không phụ thuộc tuổi; AASLD dành cho người lớn); decoy = 26.
- **Sửa câu (đã thử QC):**
  - short_vi: "Khi đánh giá giai đoạn bệnh và xét chỉ định điều trị kháng vi rút ở người mắc viêm gan vi rút B mạn, giới hạn trên của mức bình thường (ULN) của ALT huyết thanh ở nam giới người lớn (≥ 18 tuổi) là bao nhiêu (U/L)?"
  - short_en: "When staging disease and assessing eligibility for antiviral treatment in people with chronic hepatitis B, what is the upper limit of normal (ULN) of serum ALT in adult men (≥ 18 years) (U/L)?"
  - mcq_stem_vi: như short_vi, đổi đuôi thành "… (≥ 18 tuổi) là giá trị nào sau đây?"
  - mcq_stem_en: "When staging disease and assessing eligibility for antiviral treatment in people with chronic hepatitis B, which of the following is the upper limit of normal (ULN) of serum ALT in adult men (≥ 18 years)?"
- Nếu không sửa mẩu: giữ nguyên câu hiện tại (qua QC), ghi hạn chế "gợi ý khung WHO 2024".

### P-hbv-02 — fix
Giống P-hbv-01 (Bộ Y tế 19; Mỹ và 3310 là 25; mồi 13; nhiễu 31). MCQ hiển thị ổn: cùng khuôn, không có dấu so sánh. Nhiễu 31 U/L hợp lý.
- **Sửa mẩu:** `population.age` = "người lớn (≥ 18 tuổi)".
- **Sửa câu (đã thử QC):** như P-hbv-01, thay "nam giới" bằng "nữ giới" và "men" bằng "women".

### P-hbv-03 — fix
1. Duy nhất: Bộ Y tế > 2.000 IU/mL. Mỹ, WHO 2015, 3310 và 5448 đều là 20.000 và không đúng theo 1740. Quần thể ALT ≥ 2×ULN và "không yếu tố nguy cơ" được chọn đúng để giá trị Mỹ áp dụng và giá trị Bộ Y tế không đổi thành "trên ngưỡng phát hiện".
2. Không lộ đáp án. Lưu ý hạn chế: danh sách yếu tố nguy cơ là danh sách tiêu chí 3 của WHO 2024 (= 1740), nên cũng là dấu vân tay WHO 2024. Danh sách này bắt buộc để đáp án là duy nhất, nhưng thiên về phía Bộ Y tế (bảo thủ cho H1). Nên ghi trong phần hạn chế.
3. **VI/EN lệch nghĩa:** bản EN khép danh sách phủ định bằng "or relapse after stopping treatment". Bản VI kết thúc bằng dấu phẩy "…, tái phát sau ngừng thuốc, ngưỡng HBV DNA…", nên mô hình có thể hiểu "tái phát sau ngừng thuốc" (và các mục cuối) là đặc điểm **có**. Khi đó đáp án Bộ Y tế sẽ đổi thành "trên ngưỡng phát hiện".
5. MCQ: dấu so sánh lộ phương án thật (S1). Nhiễu 38.000 IU/mL là phản chiếu số học trên một đại lượng thang log: con số lẻ, không hướng dẫn nào dùng, bị loại ngay. Nên phản chiếu hình học và làm tròn, **tránh 200.000 IU/mL** vì đó là ngưỡng dự phòng mẹ–con có thật. Nhãn `foreign:US+WHO_global` gộp WHO 2015 (S3).
- **Sửa câu (đã thử QC, 60 từ):**
  - short_vi: "Ở người ≥ 18 tuổi mắc viêm gan B mạn HBeAg dương tính, ALT ≥ 2×ULN, chưa xơ hóa ≥ F2, không đồng nhiễm HIV/HCV/HDV, đái tháo đường/MASLD, suy giảm miễn dịch, biểu hiện ngoài gan, tiền sử gia đình ung thư gan/xơ gan **hay** tái phát sau ngừng thuốc, ngưỡng HBV DNA để khởi trị là bao nhiêu (IU/mL)?"
  - mcq_stem_vi: "… tiền sử gia đình ung thư gan/xơ gan hay tái phát sau ngừng thuốc, ngưỡng HBV DNA khởi trị là mức nào sau đây?"
  - EN: giữ nguyên.

### P-hbv-04 — fix
1. Duy nhất: Bộ Y tế ALT > ULN. Mỹ ≥ 2×ULN (= 3310, 5448) không đúng theo 1740. Quần thể 18–30 tuổi, HBeAg dương tính, HBV DNA 20.000–10⁷ được chọn chặt, nên tốt.
2. Không lộ đáp án: người viết đã tránh mọi cụm khớp regex, và điều đó đúng.
3. VI/EN: cùng lỗi khép danh sách như P-hbv-03.
4. "(so với ULN)" dễ hiểu, nhưng xem S4 về chấm điểm.
5. MCQ (mô phỏng với mồi gt_3x_uln và nhiễu gt_5x_uln): dựng đủ 4 phương án. Tuy vậy phương án Bộ Y tế hiển thị `ALT > ULN (vượt giới hạn trên bình thường)`, **có chú thích tiếng Việt ngay trong MCQ tiếng Anh** (`render_value` cat dùng `text` cho cả hai ngôn ngữ) và dài hơn các phương án khác, nên đó là dấu hiệu nhận biết. Nhiễu gt_5x_uln chấp nhận được (mốc 5×ULN là của viêm gan cấp/bùng phát, khác quần thể).
- **Sửa mẩu:** decoy = `{"label":"gt_3x_uln","text":"ALT ≥ 3×ULN"}`; `vn[0].text` = "ALT > ULN" (hoặc render cat theo bảng nhãn riêng VI/EN, cùng khuôn "ALT > k×ULN"); regex theo S4; gắn cờ tay đoạn A3 (S6).
- **Sửa câu (đã thử QC, 60/59 từ):**
  - short_vi: "Ở người 18–30 tuổi mắc viêm gan B mạn HBeAg dương tính, HBV DNA 20.000–10.000.000 IU/mL, chưa xơ hóa ≥ F2, không đồng nhiễm HIV/HCV/HDV, đái tháo đường/MASLD, suy giảm miễn dịch, biểu hiện ngoài gan, tiền sử gia đình ung thư gan/xơ gan **hay** tái phát sau ngừng thuốc, ngưỡng ALT khởi trị là bao nhiêu (so với ULN)?"
  - mcq_stem_vi: "… hay tái phát sau ngừng thuốc, ngưỡng ALT khởi trị là mức nào sau đây?"
  - EN: giữ nguyên.

### P-hbv-05 — pass (câu ngắn) · MCQ drop
Câu ngắn: duy nhất (> 7 kPa), trung tính, EN trung thành, đơn vị (kPa) rõ, người lớn đúng theo chú thích của WHO 2024. MCQ: xem S5, không bao giờ dựng được và không có ý nghĩa. Bỏ MCQ bằng quy tắc mã S5(a), không cần mồi.

### P-hbv-06 — fix · MCQ drop
1. Đáp án là tập {TDF, TAF, ETV}. WHO {TDF, ETV} nằm trong tập nên concordant. **Thiếu loại trừ HIV:** khi đồng nhiễm HIV thì không dùng NA đơn trị (ETV đơn trị bị chống chỉ định vì gây kháng HIV; phác đồ là ARV chứa TDF). Câu hiện tại ngầm hiểu là đơn nhiễm; nên nói rõ.
3–4, 6: EN trung thành; (tên thuốc/phác đồ) rõ.
- Ghi chú chấm (tôi đã thử): trả lời "Tenofovir" không ghi rõ dạng → nhãn 6 (abstain). Với mẩu này cả TDF lẫn TAF đều ưu tiên, nên có thể chấm đúng. Đề xuất cho grading-protocol, không chặn.
- **Sửa câu (đã thử QC, 60 từ):**
  - short_vi: "Ở người 18–60 tuổi, nặng ≥ 50 kg, không mang thai, không nhiễm HIV, mắc viêm gan B mạn có chỉ định điều trị, chưa điều trị, không bệnh thận (eGFR ≥ 50 ml/phút), loãng xương, tăng huyết áp, đái tháo đường hay dùng thuốc độc thận, NA uống đơn trị nào được ưu tiên khởi đầu (tên thuốc/phác đồ)?"
  - short_en: "In people aged 18–60 years, weighing ≥ 50 kg, not pregnant, without HIV infection, with chronic hepatitis B eligible for treatment, treatment-naive, without kidney disease (eGFR ≥ 50 mL/min), osteoporosis, hypertension, diabetes or nephrotoxic drug use, which oral nucleos(t)ide analogue (NA) monotherapy is preferred for initial treatment (drug name/regimen)?"
  - mcq_stem_vi/en: null (MCQ bỏ theo S5).

### P-hbv-07 — fix (lời câu: pass, góp ý nhỏ)
1. Duy nhất: Bộ Y tế ≥ 3–4 năm. Mỹ ≥ 2 năm không đúng theo 1740. Cụm "muốn ngừng thuốc, theo dõi được" là cần để giá trị Mỹ áp dụng. Tôi đã thử chấm: "3 năm", "3-4 năm", "36 tháng" → đúng; "2 năm" → nhãn 4; "12 tháng" → nhãn 3.
2. Nêu "HBsAg định lượng < 100 IU/mL" là một nửa tiêu chí của 1740, gợi khung EASL/1740, nhưng cần để quần thể đúng. Chấp nhận, ghi hạn chế.
3–4. EN trung thành. VI dùng "NA" không giải nghĩa, trong khi EN có giải nghĩa; bác sĩ gan mật Việt Nam quen "NAs" nên chấp nhận.
5. MCQ: S2 (hiển thị "tuổi"), S1 (mồi "5 năm" không có ≥; riêng phương án Bộ Y tế là một khoảng). Phương án bản cũ "≥ 1 năm" là **giá trị suy ra** ("3 lần XN cách nhau 6 tháng"). Mã đã loại giá trị suy ra khỏi phương án nước ngoài (`derived`) nhưng chưa loại ở bản cũ. **Sửa mẩu:** thêm `"derived": true` cho giá trị 5448, và để mã bỏ giá trị suy ra khỏi mọi phương án. Khi đó nhiễu tự sinh là 0,5 năm (6 tháng), vẫn hợp lý. Nếu nhóm quyết giữ, phải ghi rõ trong supplement. Việc kiểm AASLD: xem S8.
- **Góp ý nhỏ cho câu (đã thử QC, 59/58 từ):** nói rõ đồng nhiễm gì.
  - short_vi: "Ở người mắc viêm gan B mạn HBeAg âm tính, chưa xơ hóa nặng/xơ gan (F3/F4), không đồng nhiễm HIV/HCV/HDV, đang dùng NA, HBsAg định lượng < 100 IU/mL, muốn ngừng thuốc và có điều kiện theo dõi định kỳ lâu dài, HBV DNA cần dưới ngưỡng phát hiện tối thiểu bao lâu mới có thể ngừng NA (năm)?"
  - short_en: "… without HIV/HCV/HDV coinfection, …" (phần còn lại giữ nguyên). MCQ stem sửa tương tự.

### P-hbv-08 — fix
1. Duy nhất: Bộ Y tế > 2.000. Mỹ ≥ 2.000 trùng Bộ Y tế. WHO 2015 > 20.000 (= nhánh 2 của 3310) không đúng theo 1740.
3. VI/EN: cùng lỗi khép danh sách như P-hbv-03. (Ghi chú của người viết nói "bất kể mức tăng", nhưng câu ghi "ALT > ULN": không sai, chỉ lệch ghi chú.)
5. MCQ: `200` / `38.000` / `> 2.000` / `> 20.000`. Hai phương án có dấu `>` là hai phương án thật (S1). Nhiễu 38.000 lẻ. Vai trò `foreign:WHO_global` gán cho WHO 2015 trong khi WHO 2024 = Bộ Y tế (S3), nên đây là quy nguồn sai nặng nhất trong chủ đề.
- **Sửa câu (đã thử QC, 60 từ):**
  - short_vi: "Ở người ≥ 18 tuổi mắc viêm gan B mạn HBeAg âm tính, ALT > ULN, chưa xơ hóa ≥ F2, không đồng nhiễm HIV/HCV/HDV, đái tháo đường/MASLD, suy giảm miễn dịch, biểu hiện ngoài gan, tiền sử gia đình ung thư gan/xơ gan **hay** tái phát sau ngừng thuốc, ngưỡng HBV DNA để khởi trị là bao nhiêu (IU/mL)?"
  - mcq_stem_vi: "… hay tái phát sau ngừng thuốc, ngưỡng HBV DNA khởi trị là mức nào sau đây?"
  - EN: giữ nguyên.

### P-hbv-09 — fix (chỉ MCQ; câu ngắn pass)
Câu ngắn: duy nhất (> 12,5 kPa), trung tính, EN trung thành, (kPa) rõ. MCQ: tôi đã mô phỏng với một mồi thử (chỉ để kiểm mã, **không phải đề xuất giá trị**) và dựng được đủ 4 phương án: > 12,5 (vn), ≥ 11 (3310), > 14,6 (5448), mồi. Đây là MCQ lệch phiên bản hai bước có giá trị, nên giữ.
- **Sửa mẩu:** gán mồi theo quy tắc. Ràng buộc: cách 11, 12,5 và 14,6 kPa ít nhất 0,75 kPa (tolerance), và không trùng ngưỡng có thật của giai đoạn lân cận (7; 9,5 là F3 của 3310; các ngưỡng Baveno 10/15/20/25). Mồi cũng phải mang `cmp` giống vn (S1).

### P-hbv-10 — fix (chỉ MCQ/A3; câu ngắn pass)
Câu ngắn: duy nhất (> 1), trung tính, EN trung thành, "(giá trị APRI)" hợp lý cho đại lượng không thứ nguyên.
MCQ: (a) hiển thị `> 2 index`, `0,5 index` (lẫn tiếng Anh, không tự nhiên): cần `render.py` bỏ đơn vị `index` (hiển thị "APRI > 2" hoặc "> 2"). (b) S1: dấu so sánh. (c) Mồi 0,5 = ngưỡng APRI F2 thật của chính 1740/WHO 2024, nên chọn mồi là nhầm F2/F4, không phải ngẫu nhiên. Mẩu đã ghi nhận điều này; cần loại mẩu này khỏi mọi so sánh P(nước ngoài) với P(mồi), hoặc báo cáo riêng. (d) Nhãn WHO 2015 (S3). (e) Đoạn A3 chứa đúng giá trị mồi mà không được gắn cờ (S6).

## 4. Việc tiếp theo (theo người chịu trách nhiệm)

- **question-writer (bản nháp):** áp dụng lời câu mới cho 03, 04, 06, 08 ngay (đã qua QC). Áp dụng 01, 02 sau khi mẩu đổi `population.age`. 07 tùy chọn. Đặt `mcq_stem_*` = null cho 06 (và 05 nếu mã chưa đổi quy tắc thì QC vẫn báo lỗi).
- **counterpart-matcher/atom (mẩu):** decoy 01 = 26; decoy 04 = gt_3x_uln; decoy 09 theo ràng buộc trên; `population.age` 01/02; regex gt_1x/gt_2x của 04; `derived` cho giá trị 5448 của 07; `moh_neighbour` cho 07 (12 tháng, HBeAg dương tính); khóa hệ thống WHO có phiên bản; kiểm toàn văn AASLD cho 07 (cần người).
- **mã (không thuộc quyền người viết hay người phản biện):** S1 dấu so sánh mồi/nhiễu và kiểm tra "cùng khuôn" trong QC; S2 đơn vị năm/tuổi; S3 vai trò đa nguồn + thứ tự ưu tiên thống nhất giữa MCQ và câu ngắn; S5 điều kiện làm MCQ và `options()` so với cả tập vn; nhiễu thang log (hình học, làm tròn); hiển thị `index`; render cat theo ngôn ngữ; lọc hình mờ kcb trong `passages.py`; `passage_alt_values` xét cả giá trị "assumed" khi đơn vị của mẩu là `index`.
- Sau khi sửa: dựng lại, chạy lại QC, và phản biện lại riêng các câu MCQ (vòng 2).

## 5. Xử lý sau phản biện (V3, 2026-09-26; atom-extractor + question-writer, AI; mã qgen/grade 1.1.0/decoys mới)

Kiểm bằng mã: `pilot_merge --only hbv` giữ 10/10 mẩu (6 indistinguishable, 3 concordant, 1 conflict), 0 cảnh báo nguồn; `qgen.build --only-drafted`: 44 câu (20 ngắn, 24 trắc nghiệm = 6 mẩu × 2 thứ tự × VI/EN), 4 mẩu bỏ trắc nghiệm có chủ đích (05, 06, 09, 10), **0 mục QC không đạt**; chấm thử `grade_short` bằng câu tự viết (không phải đầu ra mô hình): 50/51 đúng nhãn cần có — ca lệch duy nhất là 'adefovir' ở P-hbv-06 (nhãn 6 thay vì 5, vì configs/grading.yaml chưa có adefovir/telbivudine; ngoài quyền sửa).

| mục | trạng thái |
|---|---|
| S1 dấu so sánh | mã đã sửa; 01, 02, 04, 07, 08 cùng khuôn. **Còn 03**: phương án Bộ Y tế là phương án duy nhất có '>' (nước ngoài hiển thị là bản Mỹ '≥ 20.000', mồi/filler lấy dấu đó). QC có ghi chú; lệch này đối xứng giữa nước ngoài và mồi. |
| S2 'tuổi'→'năm' | mã đã sửa (07: '≥ 3–4 năm', '≥ 2 years'). |
| S3 vai trò | mã đã sửa (token đa nguồn, ưu tiên như grade_short). **Còn**: khóa WHO_global chưa ghi phiên bản (08, 10: WHO 2015), việc của schema/mã. |
| S4 regex 04 | đã viết lại cat_options (gt_1x/gt_2x/gt_3x + nhãn other_multiple_uln không nguồn nào); 48/48 câu tự viết đúng nhãn. |
| S5 điều kiện MCQ | mã đã sửa; 05, 06 bỏ có chủ đích. |
| S6 A3 | hình mờ kcb đã lọc (0 dòng). 07: moh_neighbour 12 tháng → cột A3 = neighbour;superseded. **Còn gắn cờ tay**: 10 (APRI > 0,5: số không đơn vị bị QC bỏ qua), 04 (câu vị thành niên 'ít nhất 2 lần'). |
| S7 mồi 01 | quy tắc sinh lại **25 U/L** (mồi tay 26 bị bỏ theo DECISIONS 26/9). 25 U/L là ULN **nữ** của AASLD/3310, không phải giá trị của slot nam → không ghi vào foreign/superseded. **Chờ người dùng quyết.** |
| S8 07 AASLD | toàn văn Ghany 2025 không tải được (lww 403; Europe PMC chỉ bản trả phí; IDSA trỏ về lww). Slide 33 xác nhận '≥ 2 năm', 'HBsAg < 100', 'không HIV/HDV'. verified_by giữ 'auto'. **Cần người đối chiếu (HG1.2 d).** |
| 01/02 quần thể | population.age = 'người lớn (≥ 18 tuổi)'; lời câu thay thế đã áp; thêm moh_neighbour (giới kia; ULN AST 40 U/L). Filler 01 = 45 U/L (không còn 20/40), 02 = 7 U/L. |
| 03/08 | dung sai 0,5 log10; mồi 200 IU/mL; moh_neighbour ≥ 200.000 (dự phòng mẹ–con) → filler 20 IU/mL, không còn 200.000. |
| 04 | mồi agent_proposed gt_3x_uln; option_text 'ALT > k×ULN' (k = 1, 2, 3, 5) cho VI/EN. |
| 07 | 5448 '≥ 1 năm' derived → ô 3 là filler '≥ 7 năm'. |
| 09 | không có giá trị nước ngoài xung đột nên không có mồi. MCQ bỏ có chủ đích; mất MCQ lệch phiên bản hai bước. |
| 10 | quy tắc loại mồi 0,5; moh_neighbour APRI > 0,5 (≥ F2). MCQ bỏ có chủ đích. |

Cân bằng biên (H1): 5 MCQ num có phương án nước ngoài; nước ngoài ở biên trị số 4/5 và mồi ở biên 1/5 trong chủ đề này. Phía thử filler trước do đồng xu có seed quyết định. Không chỉnh tay.

## 6. Xử lý sau phản biện V4 (2026-09-26; atom-extractor + question-writer, AI)

Kiểm bằng mã sau khi sửa. `pilot_merge --only hbv` giữ 10/10 mẩu (6 indistinguishable, 3 concordant, 1 conflict), loại 0, check_decoy rỗng. `qgen.build --only-drafted` cho 44 câu, 4 mẩu bỏ trắc nghiệm có chủ đích, **0 mục QC không đạt**. Cân bằng biên trong 5 trắc nghiệm num có nước ngoài: nước ngoài ở biên 2, mồi ở biên 3 (vòng trước 4 và 1). Chấm thử `grade_short` bằng câu tự viết (không phải đầu ra mô hình): 71/72 đúng nhãn. Ca lệch duy nhất vẫn là 'adefovir' ở P-hbv-06 (configs/grading.yaml, ngoài quyền sửa). Trắc nghiệm của 03/04/08: 48/48 chữ cái chấm đúng vai trò.

| mục phản biện V4 | xử lý |
|---|---|
| CHẶN — 04: gt_1x bắt nhầm bội số viết quanh ULN | **Đã sửa** (cat_options lần 3; thiết kế ghi trong extraction.notes của mẩu). Bội số k ≠ 1 được nhận ở ba dạng. (A) Bội số đứng trước ULN, kể cả có từ so sánh hoặc 'so với/compared with/or more' xen giữa. (B) Bội số đứng sau ULN qua 'gấp/từ/tới/đến/lên/by/x/×/ít nhất'. (C) Bội số đi sau từ so sánh mà không có ULN. Có chốt 'số lần đo' ('trong 6-12 tháng', 'occasions', 'liên tiếp', 'cách nhau'). gt_1x chỉ được bắt khi câu trả lời không có bội số nào, trừ bội số bị phủ định hoặc được nêu là bản cũ. Script phản biện chạy trên mẩu đã gộp: rv_hbv04b 18/18 và rv_hbv04 41/41 đúng nhãn. Thêm 184 câu liệt kê, 67 câu bổ sung và 11.136 câu sinh theo ngữ pháp (qfix/hbv04_r3*.py): 0 sai. |
| NÊN SỬA — 04: bỏ sót 'lớn hơn', 'over', 'trên mức bình thường' | **Đã sửa.** 7 câu sai của rv_hbv04 nay đúng. Thêm 'ALT tăng/elevated/abnormal', 'any ALT elevation', 'vượt ngưỡng bình thường' vào gt_1x và 'twice or more the ULN' vào gt_2x. |
| NÊN SỬA — 03/08: filler 20 IU/mL = ngưỡng phát hiện | **Đã sửa.** Thêm moh_neighbour 'trên ngưỡng phát hiện (thường < 20 IU/mL)'. Nguyên văn ở tr.PDF 11 (span_on_page True); tiêu chí 3 ở tr.PDF 20 cũng nguyên văn True. Filler quy tắc nay là 2.000.000 IU/mL (03: '≥', 08: '>'), không nguồn nào đã ghi. Mồi 200 IU/mL cách 20 IU/mL đúng 1 log = 2·dung sai, nên check_decoy không báo. |
| Bộ chấm: copies/mL, lũy thừa 10, log10 | **Không sửa được** (mã src/, ngoài quyền). rv_hbv_num sai 3/44: '2 x 10^3 IU/mL' ra 5 (cần 2); '10^4 copies/mL' bị đọc thành 10 IU/mL nên ra 5 (cần 2); '10^5 copies/mL' ra 5 (cần 3). Phải sửa normalize_vi trước khi đóng băng quy tắc chấm. |
| 07: giá trị Mỹ '≥ 2 năm' | Chưa đổi. Toàn văn Ghany 2025 chỉ có bản trả phí, **cần người dùng đối chiếu (HG1.2 d)**. |
| Mơ hồ còn lại của 04 (ghi rõ, không sửa) | 'ALT > ULN ít nhất 2 lần' và 'ALT > ULN at least twice' không kèm khoảng thời gian được đọc là bội số (gt_2x, nhãn 3); có khoảng thời gian ('trong 6-12 tháng', 'over 6 months') thì là gt_1x. Câu trả lời chỉ ghi U/L ('ALT > 35 U/L') không mang bội số ULN nên ra nhãn 6. |
