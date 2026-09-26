# Phản biện độc lập — câu hỏi thí điểm chủ đề immunization

- Người phản biện: agent AI đóng vai rev-clinician + rev-methods (**không phải bác sĩ thật**; mọi nhận định lâm sàng cần bác sĩ xác nhận ở HG4.2).
- Ngày: 2026-09-26. Đầu vào: `immunization.jsonl` (bản nháp), `pilot_atoms.jsonl` (P-immunization-01..04), `immunization_q.jsonl`, `immunization_p.jsonl`, `immunization_qc.csv`, đề cương §3.5/§4.3/§4.4/§5.7, SKILL question-generation, `configs/conditions.yaml`, `src/vnsoc/qgen/*.py`, `src/vnsoc/grade.py`.
- Chống rò rỉ: KHÔNG xem đầu ra của mô hình nào được kiểm tra. Mọi câu trả lời dùng để thử bộ chấm dưới đây do người phản biện tự viết.
- Kiểm bằng mã: đã chạy lại `vnsoc.qgen.build --only-drafted` trên bản nháp hiện tại (16 câu, 0 mục QC lỗi). Bản sửa đề xuất cho mẩu 01 cũng đã chạy thử trong scratchpad (không ghi vào dự án): 16 câu, 0 mục QC lỗi, exit 0.

## Tổng hợp

| atom_id | verdict | Lý do chính |
| --- | --- | --- |
| P-immunization-01 | **fix** | Filler trắc nghiệm do mã sinh là "16,5–19,5 tháng": số lẻ lộ vai trò và phủ 18 tháng, là tuổi mũi 2 (MR) của chính Bộ Y tế; cụm "trước khi đi du lịch nước ngoài" là gợi ý kiểu CDC |
| P-immunization-02 | **fix** (sửa ở mã, bản nháp giữ nguyên) | Phương án EU_UK hiển thị "3,3333 tuổi"; 2 phương án nước ngoài so với 1 mồi làm lệch phép so P(nước ngoài) và P(mồi); câu trả lời "3 tuổi 4 tháng" bị chấm nhãn 5 thay vì nước ngoài EU_UK |
| P-immunization-03 | **pass** | Có ghi chú theo dõi: tình trạng lịch CDC 2026, lỗi OCR trong đoạn A3 |
| P-immunization-04 | **pass** | Có ghi chú: dấu chữ ký số ở cuối đoạn A3 |

Tổng: **pass 2 / fix 2 / drop 0**. Không mẩu nào bị loại vì mơ hồ quần thể. Với quần thể đã nêu, cả 4 câu đều chỉ có một đáp án Bộ Y tế, và không giá trị nước ngoài xung đột nào cũng đúng theo Bộ Y tế.

### Vấn đề nghiêm trọng (xếp theo mức độ)

1. **[Chặn dữ liệu, HG1.2] Mẩu 01, 02, 04 neo vào TT52/2025, văn bản đã hết hiệu lực từ 01/7/2026.** TT13/2026 không có lịch tiêm, còn văn bản hướng dẫn chuyên môn của Cục Phòng bệnh chưa tìm thấy. Prompt A1 lại hỏi theo "hướng dẫn … **hiện hành** của Bộ Y tế", nên "đáp án Bộ Y tế" của 3 mẩu này hiện không có văn bản còn hiệu lực làm căn cứ. Câu chữ đã sẵn sàng, nhưng **không được đưa vào atoms/questions v1** trước khi người dùng chọn (a), (b) hoặc (c) theo `extraction.hg_block` và ghi vào DECISIONS.md. Hiện chỉ mẩu 03 (TT13/2026) đủ điều kiện.
2. **[Phương pháp trắc nghiệm, cả bộ] Ô thứ 3 của trắc nghiệm ưu tiên giá trị nước ngoài thứ hai trước filler** (`mcq.options`: `sup + conf[1:]` được xét trước filler). Cách này lệch với SKILL question-generation bước 3 ("nếu thiếu bản cũ thì 3 lựa chọn + 1 nhiễu hợp lý **không thuộc nguồn nào**") và với §3.5, vốn giả định chỉ có một phương án nước ngoài: lỗi ngẫu nhiên rơi vào phương án nước ngoài với xác suất 1/(số lựa chọn − 1). Ở mẩu 02 có hai phương án nước ngoài (US 4–6 tuổi, EU_UK 40 tháng) nhưng chỉ một mồi. Khi mô hình chọn bừa, tỉ lệ nước ngoài : mồi đã là 2 : 1, trong khi `analysis/pilot.py` gộp `mcq_a1_*_foreign` với `mcq_a1_*_decoy` mà không chuẩn hóa theo số phương án. Kết quả là phép so lệch về phía ủng hộ H1. Cần quyết định trước OSF, chọn một trong hai:
   - (a) sửa mã theo SKILL: ô 3 = bản cũ, nếu không có thì filler;
   - (b) giữ 2 phương án nước ngoài nhưng đăng ký trước phép so theo từng phương án, tức P(nước ngoài)/k_nước ngoài so với P(mồi)/k_mồi, hoặc chỉ tính phương án nước ngoài gần nhất.

   Vấn đề này ảnh hưởng mọi mẩu có từ 2 giá trị nước ngoài xung đột phân biệt, không riêng immunization.
3. **[Hiển thị và chấm, mẩu 02]**
   - `render_value` đổi 40 tháng sang đơn vị năm của mẩu, rồi `fmt_num` in 4 chữ số thập phân, thành "3,3333 tuổi" / "3.3333 years". Không hướng dẫn nào viết như vậy, nên phương án này tự lộ là phương án "nhân tạo", mô hình dễ loại, và P(nước ngoài) của EU_UK bị kéo xuống.
   - Khi chấm câu trả lời ngắn, "ĐÁP ÁN: 3 tuổi 4 tháng" / "ANSWER: 3 years 4 months" (đúng cách UKHSA viết) bị tách thành 2 giá trị (3 và 0,333 năm) và chấm **nhãn 5 (unattributed)**, không phải nhãn 4 foreign:EU_UK. "40 tháng" thì được chấm đúng là EU_UK. Như vậy câu trả lời trùng Anh bị đếm thiếu một cách có hệ thống.
   - Cả hai lỗi phải sửa ở mã: `qgen/render.py` hiển thị tuổi hỗn hợp; `normalize_vi` gộp "X tuổi Y tháng" / "X years Y months" thành một giá trị.
4. **[Vừa, mẩu 01] Filler 16,5–19,5 tháng.** Xem mục mẩu 01.

---

## P-immunization-01 — verdict: **fix**

**Mẩu**: TT52/2025 tr.7. Bộ Y tế: sởi đơn giá **9 tháng**. Xung đột: US 12–15 tháng (MMR), EU_UK 12 tháng (MMRV). WHO trùng Bộ Y tế (9 tháng). Mồi 3–6 tháng, tol 1,5.

| Tiêu chí | Đánh giá |
| --- | --- |
| (1) Đáp án Bộ Y tế duy nhất? Giá trị nước ngoài có "cũng đúng" theo Bộ Y tế? | Có một đáp án duy nhất (9 tháng). Câu đã loại trừ liều bổ sung khi có dịch, và loại trừ này cần thiết vì Bộ Y tế từng cho tiêm sởi 6–< 9 tháng ở vùng dịch; "18 tháng" là mũi 2 (MR). 12–15 và 12 tháng không đúng theo Bộ Y tế cho mũi 1 thường xuyên. Đạt. |
| (2) Lộ đáp án/nguồn? | Không có số của giá trị nào. Tôi đồng ý với việc bỏ "quốc gia còn lưu hành sởi / TCMR": đó là thuộc tính quốc gia và sẽ gợi thẳng quy tắc WHO 9 tháng. **Tuy vậy, cụm "không phải liều tiêm sớm trước khi đi du lịch nước ngoài" là khái niệm riêng của CDC** (liều 6–11 tháng trước chuyến đi). Nó ngầm đặt bối cảnh là nước có mũi 1 muộn và đã loại trừ sởi, nên có thể đẩy câu trả lời ở A0 (và phần nào ở A1) về 12–15 tháng. Cụm này không cần cho tính duy nhất vì Bộ Y tế không có liều du lịch, và "đúng lịch" đã loại liều sớm. |
| (3) EN trung thành | Đạt: routine, on-schedule, not…/not…, dose 1, months of age. |
| (4) Tự nhiên | Đạt: "mũi 1 vắc xin có chứa thành phần sởi" là cách nói quen thuộc. |
| (5) Trắc nghiệm | Cùng đơn vị (tháng); không phương án nào đúng theo Bộ Y tế cho mũi 1. **Filler "16,5–19,5 tháng" có hai vấn đề.** (i) Là phương án duy nhất có số lẻ ",5", nên lộ ngay là giá trị sinh theo phép toán. (ii) Khoảng này chứa 18 tháng, tức tuổi mũi 2 (MR) của chính TT52/2025 (và cũng là mũi 2 theo WHO 15–18 tháng), nên không còn là "nhiễu không thuộc nguồn nào" (SKILL bước 3). Mồi 3–6 tháng chạm mốc 6 tháng của liều sớm/liều dịch; điều này đã ghi trong mẩu và có tác dụng bảo thủ cho H1. |
| (6) Đơn vị | Đạt: "(tháng tuổi)" / "(months of age)". |

Thử bộ chấm với câu trả lời tự viết: "9 tháng" → nhãn 2 (vn, trùng WHO); "12 tháng" / "1 tuổi" / "1 year" → nhãn 4 [EU_UK, US]; "12–15 tháng" → nhãn 4 [US]; "18 tháng" → nhãn 5; "6 tháng" → nhãn 5, decoy_match. Hợp lý.

**Sửa cụ thể**
1. *(Bắt buộc)* Thêm filler ghi đè vào bản nháp (mã có nhận: `fill = filler or rule_filler(...)`): `"filler": {"lo": 24, "hi": 24, "unit": "month", "text": "24 tháng"}`. Đây là số nguyên, không nguồn nào đã ghi (vn/foreign/decoy/mũi 2) khuyến cáo cho mũi 1. Đã chạy thử: phương án hiển thị {24 tháng, 12–15 tháng, 9 tháng, 3–6 tháng}, EN {24 months, 12–15 months, 9 months, 3–6 months}, QC 0 lỗi. Có một điểm lệch nhỏ với quy tắc "filler null cho num": ghi lý do vào `notes`. *Cách thay thế ở mức mã* (chủ mã quyết định): `rule_filler` làm tròn về số nguyên khi các phương án khác đều nguyên, và né giá trị Bộ Y tế của ngữ cảnh lân cận (`moh_neighbour`).
2. *(Khuyến nghị mạnh)* Bỏ gợi ý du lịch nhưng vẫn giữ loại trừ liều dịch. Đã chạy thử, 0 lỗi QC, 44/34 từ:
   - short_vi: "Trong tiêm chủng thường xuyên đúng lịch cho trẻ em (không tính liều tiêm sớm hoặc liều bổ sung ngoài lịch thường xuyên, ví dụ khi có dịch), mũi 1 vắc xin có chứa thành phần sởi được tiêm ở tuổi nào (tháng tuổi)?"
   - short_en: "In routine, on-schedule childhood immunization (not counting early or supplementary doses given outside the routine schedule, e.g. during an outbreak), at what age is dose 1 of a measles-containing vaccine given (months of age)?"
   - mcq_stem_vi/en: như trên, bỏ "(tháng tuổi)" / "(months of age)".
3. *(Cho người giữ mẩu, không sửa câu hỏi)* Đoạn A3 (tr.7) có dòng MCV2 "Tiêm nhắc lại khi trẻ đủ 18 tháng tuổi". Nên thêm `moh_neighbour` (MR 18 tháng) vào mẩu để `passage_has_alt_value` gắn cờ "neighbour" cho phân tích độ nhạy H3.

---

## P-immunization-02 — verdict: **fix** (bản nháp giữ nguyên; sửa ở mã và kế hoạch phân tích)

**Mẩu**: TT52/2025 tr.3. Bộ Y tế: nhắc lại lần 2 (bạch hầu giảm liều) lúc **7 tuổi**. Xung đột: US 4–6 tuổi (DTaP liều 5), EU_UK 3 tuổi 4 tháng (40 tháng, dTaP/IPV). WHO 4–7 tuổi chứa cả 7. Mồi 8–10 tuổi, tol 0,5.

| Tiêu chí | Đánh giá |
| --- | --- |
| (1) Duy nhất / nước ngoài "cũng đúng"? | Đạt. Neo mũi nhắc 1 lúc 18 tháng làm "mũi nhắc lần hai" khớp với DTaP liều 5 của Mỹ và dTaP/IPV 3 tuổi 4 tháng của Anh (nhóm sinh từ 01/7/2024). Không nêu dạng bào chế (giảm liều/Td) là lựa chọn đúng: nếu nêu thì slot Mỹ thành Tdap 11–12 tuổi. "Theo đúng lịch" loại trừ quy tắc bắt kịp của Bộ Y tế ("từ 7 tuổi trở lên, cách ≥ 4 năm"), vốn có thể làm mồi 8–10 tuổi "đúng" với trẻ tiêm muộn. |
| (2) Lộ đáp án/nguồn? | Không. "18 tháng" là số quần thể, không phải giá trị của mẩu này, và không riêng Việt Nam (Anh 18 tháng, Mỹ 15–18 tháng). |
| (3) EN trung thành | Đạt: first/second booster, 18 months, routine schedule, years of age. |
| (4) Tự nhiên | Đạt. "(năm tuổi)" hơi lạ tai. *Tùy chọn* đổi thành "(tuổi)" hoặc "(tuổi, tính theo năm)", không bắt buộc. |
| (5) Trắc nghiệm | Không phương án nào đúng theo Bộ Y tế. **Lỗi:** phương án foreign:EU_UK hiển thị "3,3333 tuổi" / "3.3333 years". Không tự nhiên, lộ vai trò, kéo P(nước ngoài) xuống. **Lỗi phương pháp:** 2 phương án nước ngoài và 1 mồi (xem vấn đề nghiêm trọng số 2). |
| (6) Đơn vị | Đạt. |

Thử bộ chấm: "7 tuổi" → 2; "4–6 tuổi" / "5 tuổi" / "4–6 years" → 4 [US, WHO_global]; "4–7 tuổi" → 4 [WHO], partial; "40 tháng" → 4 [EU_UK]; **"3 tuổi 4 tháng" / "3 years 4 months" → 5 (sai, phải là 4 EU_UK)**.

**Sửa cụ thể** (không sửa được ở mức bản nháp: phương án EU_UK lấy từ `foreign` của mẩu, filler chỉ dùng khi thiếu phương án)
1. `src/vnsoc/qgen/render.py`: khi đổi đơn vị tháng→năm cho ra số không nguyên, hiển thị dạng tuổi hỗn hợp "3 tuổi 4 tháng" / "3 years 4 months". Ít nhất phải làm tròn theo độ chính xác của nguồn, không in 4 chữ số thập phân.
2. `normalize_vi` / `grade.parse_values`: gộp "X tuổi Y tháng", "X years Y months" (và "X năm Y tháng") thành **một** giá trị X + Y/12 năm, kèm test. Đã được ghi là đề xuất trong ghi chú mẩu nhưng chưa làm; cần xong trước khi chạy thí điểm.
3. Quyết định trước OSF về cách xử lý mẩu có 2 phương án nước ngoài (vấn đề nghiêm trọng số 2). Nếu chọn (a) theo SKILL, filler theo luật phản chiếu sẽ rơi vào khoảng 2–4 tuổi, chồng 3 tuổi 4 tháng của Anh. Khi đó cần filler do người viết cung cấp, và người viết sẽ phải đề xuất lại.
4. *(Ghi chú A3)* Đoạn A3 mở đầu bằng mảnh câu nối từ dòng trên của bảng, và **kết thúc giữa danh sách ở "Tiêm lần 2:"** vì `SENT_END` cắt sau dấu ":", trái SKILL bước 6 "không cắt giữa câu". Cột `passage_has_alt_value = foreign:US` là do "trước khi trẻ đủ 4 tuổi", tức mốc bắt kịp của nhắc lại lần 1 theo Bộ Y tế, trùng số với cận dưới của US. Về ý nghĩa đây là dương tính giả, nhưng nên giữ cờ để phân tích độ nhạy H3 loại ra. Đề nghị sửa `passages.py`: không kết thúc đoạn tại ":".

---

## P-immunization-03 — verdict: **pass**

**Mẩu**: TT13/2026 tr.18 (OCR, văn bản hiện hành). Liều viêm gan B sơ sinh **≤ 24 giờ**; mẩu đối chứng (US ≤ 24 giờ, WHO ≤ 24 giờ).

| Tiêu chí | Đánh giá |
| --- | --- |
| (1) Duy nhất | Đạt. Hỏi "thời hạn tối đa" loại được "12 giờ" (mẹ HBsAg dương tính). Các giới hạn "mẹ HBsAg âm tính, ≥ 2000 g, lâm sàng ổn định" không tạo mơ hồ, vì Bộ Y tế không phân nhóm và ngưỡng < 2000 g thường là lý do tạm hoãn theo khám sàng lọc (mẩu ghi là chưa kiểm; bác sĩ cần xác nhận). |
| (2) Lộ | Không. Các giới hạn quần thể mang dấu ấn CDC, nhưng mẩu đối chứng nên không làm lệch về giá trị khác. |
| (3) EN | Đạt: HBsAg-negative, ≥ 2,000 g, medically stable, delivery room, not catch-up, hours. |
| (4) Tự nhiên | Đạt. *Tùy chọn:* "phải được tiêm chậm nhất trong bao nhiêu giờ sau sinh?" tự nhiên hơn "thời hạn tối đa bao lâu … (giờ)". Câu VI 57/60 từ, sát trần, nên nếu sửa thì nên rút gọn. |
| (5) Trắc nghiệm | Không áp dụng (concordant, stem null đúng quy tắc). |
| (6) Đơn vị | Đạt: "(giờ)". Bộ chấm: "24 giờ" / "within 24 hours" → 2; "1 ngày" → unit_mismatch (nhãn 5), vì vậy gợi ý đơn vị là cần thiết. |

**Ghi chú theo dõi (không chặn câu hỏi)**
- **Bắt buộc kiểm lại trước ngày đóng băng 15/10/2026**: nếu lịch CDC 2026 có hiệu lực (liều sơ sinh cho trẻ có mẹ HBsAg âm tính thành quyết định cá nhân), thì đúng quần thể mà câu hỏi nêu ("mẹ HBsAg âm tính") là nhóm đang tranh chấp. Khi đó mẩu có thể chuyển sang xung đột, và value_kind num/h có thể không biểu diễn được giá trị Mỹ.
- Mã QC: `POP_NUMERIC_KEYS` không khớp khóa `birth_weight`, nên số "2000" **không được mã bắt buộc**. Người viết đã tự đưa vào. Đề nghị thêm `birth_weight` (và các khóa `*_weight`) vào regex. Mẩu cũng chưa có `required_terms` cho `maternal_hbsag`. Nên thêm để QC bắt buộc có "HBsAg âm tính" / "HBsAg-negative".
- Đoạn A3 (OCR) còn lỗi chính tả ("Điêu", "co sở", "sinh pham", "thầm quyền", "sự có"). Số "24" đúng. Nên sửa theo ảnh trang trước khi đóng băng, vì mô hình ở A3 nhận đúng văn bản này.

---

## P-immunization-04 — verdict: **pass**

**Mẩu**: TT52/2025 tr.3. Mũi nhắc lại đầu tiên (mũi thứ 4) vắc xin chứa ho gà lúc **18 tháng**; mẩu đối chứng (US 15–18, UK 18 với nhóm sinh từ 01/7/2024, WHO 12–23).

| Tiêu chí | Đánh giá |
| --- | --- |
| (1) Duy nhất | Đạt (18 tháng). |
| (2) Lộ | Không. Số 3 và 4 là số quần thể. |
| (3) EN | Đạt: 3-dose primary series, first booster (dose 4), months of age. |
| (4) Tự nhiên | Đạt. |
| (5) Trắc nghiệm | Không áp dụng (concordant). |
| (6) Đơn vị | Đạt: "(tháng tuổi)". |

**Ghi chú**
- Đoạn A3 kết thúc bằng dấu chữ ký số "dunglt.pb_Le Tuan Dung_31/12/2025 16:49:21", gồm tên người ký và dấu thời gian, là nhiễu có số. Đề nghị lọc dấu chữ ký số ở `page_text` hoặc `atom_passage` cho mọi văn bản TT-BYT ký số.
- Theo thiết kế chấm: "15–18 tháng" → nhãn 4 [US, WHO], partial, dù đây là mẩu đối chứng. Nhóm phân tích cần biết khi đọc tỉ lệ đúng ở mẩu đối chứng.
- Rò rỉ chéo mẩu: câu của mẩu 02 chứa "18 tháng", là đáp án của mẩu 04. Không sao nếu mỗi câu là một lượt gọi độc lập (như `run/plan.py`). Không được ghép hai câu vào cùng một ngữ cảnh (A6, few-shot, hoặc người kiểm HG4.2 đọc liền nhau nên biết điều này).
- Trẻ ở Anh sinh trước 01/7/2024 không có mũi 18 tháng. Câu trả lời "40 tháng" sẽ bị chấm nhãn 5, đây là hạn chế đã biết.

---

## Việc cần làm (tách theo người chịu trách nhiệm)

| # | Việc | Ai | Chặn? |
| --- | --- | --- | --- |
| 1 | Quyết định HG1.2 cho mẩu 01/02/04 (văn bản Cục Phòng bệnh / lịch công bố gần nhất / bỏ mẩu) | Người dùng | Chặn v1 |
| 2 | Quyết định cách dựng ô 3 trắc nghiệm (filler theo SKILL, hay chuẩn hóa theo số phương án) và đăng ký trước | Người dùng + rev-methods | Chặn OSF |
| 3 | `render.py`: hiển thị tuổi hỗn hợp; `normalize_vi`: gộp "X tuổi Y tháng" | Chủ mã | Chặn chạy thí điểm mẩu 02 |
| 4 | Bản nháp mẩu 01: thêm filler 24 tháng và bỏ gợi ý du lịch (văn bản ở trên, đã chạy thử QC 0 lỗi) | Người viết câu hỏi | Nên sửa trước đóng băng |
| 5 | `qc.py`: thêm `birth_weight` vào `POP_NUMERIC_KEYS`; mẩu 03 thêm `required_terms` maternal_hbsag; mẩu 01 thêm `moh_neighbour` MR 18 tháng | Chủ mã / người giữ mẩu | Không |
| 6 | `passages.py`: không kết thúc đoạn tại ":"; lọc dấu chữ ký số; sửa lỗi OCR đoạn 03 theo ảnh trang | Chủ mã / người kiểm OCR | Không (kiểm tay trước đóng băng) |
| 7 | Kiểm lại tình trạng lịch CDC 2026 (viêm gan B sơ sinh) trước 15/10/2026 | Người ghép giá trị nước ngoài | Có thể đổi trạng thái mẩu 03 |

---

## Kiểm lại sau khi sửa mã (26/9/2026, agent atom-extractor + question-writer; không xem đầu ra mô hình)

Lệnh: `pilot_merge --only immunization --out <scratchpad>/immunization_atoms.jsonl --no-checklist` → giữ 4, loại 0 (conflict 2, concordant 2; mồi không đổi: 01 = 3–6 tháng, 02 = 8–10 tuổi, mirror_arith, làm tròn none; dung sai 1,5 / 0,5 / 0 / 0). `qgen.build --only-drafted` → 16 câu, 2 mẩu bỏ trắc nghiệm có chủ đích (03, 04: đối chứng, không có mồi), **0 mục QC không đạt**, exit 0.

| # (mục Việc cần làm) | Trạng thái |
| --- | --- |
| 1 HG1.2 mẩu 01/02/04 | **Vẫn chờ người dùng** — mỗi mẩu ghi `pending_user_decision` trong extraction.notes. tiemchungmorong.vn/documents (WebFetch 26/9): văn bản mới nhất vẫn TT52/2025. Manh mối: QĐ 1637/QĐ-BYT (ký 6/5/2015, ảnh quét, sha256 24424e71…) chỉ phê duyệt MR lúc 18 tháng; không thay được văn bản neo của 01/02/04; hiệu lực hiện nay chưa rõ. |
| 2 Ô 3 trắc nghiệm | Mã đã theo SKILL bước 3 (ô 3 = bản cũ, không có thì filler theo quy tắc). Mẩu 02 nay 1 nước ngoài : 1 mồi. |
| 3 render / normalize | Xong ở mã. `render_value` EU_UK 40 tháng → "3 tuổi 4 tháng" / "3 years 4 months". Chấm "3 tuổi 4 tháng", "3 years 4 months", "3 years and 4 months", "40 tháng" → nhãn 4 [EU_UK]. |
| 4 Filler mẩu 01 | Filler tay 24 tháng đã bỏ (mã không dùng filler tay khi quy tắc có ứng viên). Filler quy tắc = 21–24 tháng. Câu chữ bỏ gợi ý du lịch giữ nguyên. |
| 5 required_terms / neighbour | Mẩu 03: thêm required_terms maternal_hbsag + clinical_status; khóa birth_weight → weight (QC mã bắt buộc số 2000; thử âm tính: bắt được). Mẩu 01: thêm moh_neighbour 18 tháng (TT52/2025 tr.7, `verify_span --find` → [7]); đoạn A3 nay gắn cờ `neighbour`. |
| 6 passages | Đoạn 02 không còn cắt ở "Tiêm lần 2:". Đoạn 04 không còn chữ ký số. Đoạn 03 vẫn còn lỗi OCR: cần kiểm tay theo ảnh trang trước đóng băng. |
| 7 CDC 2026 viêm gan B | Chưa kiểm (WebSearch hết hạn mức phiên). **Bắt buộc trước 15/10/2026.** |

Phương án trắc nghiệm hiển thị (đã đọc từng phương án VI/EN):
- **01**: {21–24 tháng, 12–15 tháng, 9 tháng, 3–6 tháng} / {21–24 months, 12–15 months, 9 months, 3–6 months}.
- **02**: {12–14 tuổi, 8–10 tuổi, 4–6 tuổi, 7 tuổi} / {12–14 years, 8–10 years, 4–6 years, 7 years}.
- Cả hai câu: cùng đơn vị, không có từ gợi nguồn hay vai trò. Không phương án nào ngoài đáp án đúng theo Bộ Y tế cho quần thể "đúng lịch".

**Điểm mới cho rev-methods** (không sửa được ở bản nháp):
- (a) Ở cả hai câu, phương án Bộ Y tế là phương án **duy nhất dạng điểm**. Mồi và filler lấy độ rộng của khoảng nước ngoài, nên thành khoảng. Gợi ý "phương án lạ" này nghiêng về đáp án đúng. Nó đối xứng giữa nước ngoài và mồi, nên không làm lệch phép so H1, nhưng làm tăng tỉ lệ đúng trắc nghiệm.
- (b) Filler 12–14 tuổi của mẩu 02 trùng tuổi mũi nhắc thứ ba ở nước khác: Tdap Mỹ 11–12 tuổi, Td/IPV Anh 14 tuổi, Td WHO 9–15 tuổi. Đây là liều khác, không ghi làm giá trị của mẩu.

Chấm thử `grade_short` bằng câu trả lời tự viết:
- **01**: "9 tháng" → 2; "12–15 tháng" → 4 [US]; "12 tháng" / "1 tuổi" / "1 year" → 4 [EU_UK, US]; "18 tháng" → 5; "3–6 tháng" → 5 (decoy); "21–24 tháng" → 5.
- **02**: "7 tuổi" → 2; "4–6 tuổi" → 4 [US, WHO]; "3 tuổi 4 tháng" → 4 [EU_UK]; "8–10 tuổi" → 5 (decoy).
- **03**: "trong vòng 24 giờ" / "within 24 hours" → 2; "1 ngày" → 2 (trước đây nhãn 5); "12 giờ" → 5.
- **04**: "18 tháng" → 2; "15–18 tháng" → 4 partial; "40 tháng" → 5.
- Không mẩu nào có giá trị bản cũ khác giá trị hiện hành, nên không có phép thử nhãn 3.
- `grade_mcq` theo từng chữ cái khớp vai trò ở cả 8 câu trắc nghiệm.

---

## Sửa lần 3 theo kiểm độc lập (26/9/2026, agent atom-extractor + question-writer; không xem đầu ra mô hình)

Người kiểm độc lập (rev-methods + rev-clinician, **AI, không phải bác sĩ**) kiểm lần sửa 2: không có lỗi chặn ở dữ liệu. Có 1 lỗi mã ưu tiên cao, 2 mục nên sửa và 8 mục nhỏ. Xử lý như sau:

| # | Phát hiện | Xử lý |
| --- | --- | --- |
| 1 | **[Mã, ưu tiên cao — chặn bước chấm thí điểm]** `normalize_vi.parse_nums` đọc số thứ tự mũi/liều không đơn vị ('mũi 1', 'Dose 1', 'lần 2', 'mũi thứ 4', 'dose 4', 'liều 1', 'sau 3 mũi cơ bản') thành một giá trị (đơn vị giả định) → multi → nhãn 5. Kiểm lại 26/9: vẫn còn. | **Ngoài quyền người sửa dữ liệu (không sửa src/) — chuyển chủ mã.** Giảm thiểu ở dữ liệu: câu hỏi 01 và 04 nay viết số thứ tự/số mũi bằng chữ ('mũi đầu tiên', 'ba mũi cơ bản', 'mũi thứ tư' / 'the first dose', 'three-dose', 'the fourth dose'); 02 vốn đã dùng 'lần thứ nhất/thứ hai'; 03 dùng 'liều … sơ sinh'. Dạng chữ không bị đọc thành số ('mũi thứ tư … 18 tháng' → 2). Lỗi vẫn phải sửa ở mã vì mô hình có thể tự viết 'Mũi 1'. Thêm lỗi cùng loại tôi thấy: số quần thể lặp lại trong câu trả lời ('7 tuổi (sau mũi nhắc lúc 18 tháng)' → 5), và '18-month' bị đọc thành 18 **năm**. Đề xuất chủ mã: bỏ số không đơn vị ngay sau từ chỉ thứ tự (mũi/lần/liều/thứ/dose/booster/shot #); bỏ số trùng số quần thể đã nêu trong câu hỏi; đọc 'N-month/N-year' đúng đơn vị; thêm test; tăng phiên bản grader. |
| 2 | Bỏ sót manh mối QĐ 1327/2014 cho mẩu 01. | **Đã sửa (ghi chú).** Tự kiểm: `verify_span --find 1327/2014 "mũi đầu tiên bat buộc tiêm lúc 9 tháng"` → [6]; xem ảnh trang (`--image`), mục V.1, trang PDF 6 (trang in 5): "Thực hiện tiêm chủng 2 mũi vắc xin cho trẻ em trong độ tuổi tiêm chủng theo quy định của Dự án tiêm chủng mở rộng quốc gia (mũi đầu tiên bắt buộc tiêm lúc 9 tháng tuổi)". Ghi vào extraction.notes mẩu 01 kèm giới hạn: status 'current' là giá trị giữ chỗ; đề cương nói bị 1019/2025 thay (chưa xác minh); in_corpus false; bản quét đăng lại (benhvienhatrung.vn); dẫn chiếu sang quy định TCMR; chỉ dùng được cho 01. **Không đổi văn bản neo, không thêm giá trị.** |
| 3 | Phương án Bộ Y tế là phương án duy nhất dạng điểm (01: {21–24, 12–15, 9, 3–6 tháng}; 02: {12–14, 8–10, 4–6, 7 tuổi}). | Mã/thiết kế — không sửa được ở bản nháp (filler do quy tắc sinh khi có ứng viên). Ghi trong notes 01/02 cho rev-methods: đề xuất `rule_filler` lấy dạng của giá trị Bộ Y tế, hoặc đăng ký hạn chế trước OSF. |
| 4 | '9 tháng, sau đó MR lúc 18 tháng' (giá trị Bộ Y tế + moh_neighbour) → 5 (multi). | Hạn chế bộ chấm, ghi trong notes 01. Đề xuất chủ mã coi giá trị moh_neighbour đi kèm giá trị Bộ Y tế là không xung đột, hoặc ghi vào grading-protocol/prereg. |
| 5 | Câu cũ trong notes 02 ("'3 tuổi 4 tháng' hiện bị tách…") mâu thuẫn kết quả mới. | **Đã sửa**: thay bằng câu đúng (nay gộp thành 40 tháng → nhãn 4 [EU_UK]). |
| 6 | Filler 12–14 tuổi (02) chứa tuổi mũi nhắc thứ ba ở nước khác. | Giữ (quy tắc). Đưa vào danh sách hạn chế cho HG4.2 (dưới). |
| 7 | 01: khoảng cách US 12–15 tới moh_neighbour 18 = 3,0 = 2 × dung sai 1,5 (đúng biên). | Ghi notes 01 cho rev-methods (N1 lật nếu dung sai tăng rất nhỏ). Không sửa. |
| 8 | 01: 'mũi 1 vắc xin có chứa thành phần sởi' có thể bị hiểu là mũi đầu của vắc xin phối hợp (MR 18 tháng). | **Đã sửa**: 'mũi đầu tiên của bất kỳ vắc xin nào có chứa thành phần sởi' / 'the first dose of any measles-containing vaccine' (không nêu 'đơn giá' vì gợi nước còn lưu hành sởi → 9 tháng). population.dose sửa theo. QC 0 lỗi. |
| 9 | 02: '4–6 tuổi' mang vai trò foreign:US+WHO_global (WHO 4–7 chứa cả 7 của Bộ Y tế). | Mã/quy ước phân tích RQ2 — ghi notes 02, chuyển chủ mã. |
| 10 | 03: đổi birth_weight → weight để lách regex. | Giữ (nghĩa chấp nhận được); ghi notes 03: trả lại tên khóa khi chủ mã thêm birth_weight/*_weight vào POP_NUMERIC_KEYS. |
| 11 | QĐ 1637 chỉ ở scratchpad, notes chỉ ghi sha rút gọn. | **Đã sửa**: notes 01/02/04 ghi sha256 đầy đủ 24424e7195b76542db109c8d2baf3ac95287d2c04e0098ec456da66cb5c4fb65, vị trí tệp, và điều kiện nhập kho qua corpus-librarian (manifest, HG2.3) nếu người dùng chọn dùng. |

Mẩu 04 cũng được sửa theo mục 1: 'đủ 3 mũi cơ bản' → 'đủ ba mũi cơ bản' (tách từ khóa age sang khóa prior_doses), 'mũi thứ 4' → 'mũi thứ tư', EN '3-dose' → 'three-dose', '(dose 4)' → '(the fourth dose)'.

**Tự kiểm bằng mã**
- `pilot_merge --only immunization --no-checklist`: giữ 4, loại 0 (conflict 2, concordant 2). Mồi, dung sai (1,5 / 0,5 / 0 / 0) và conflict_status không đổi. So với lần trước chỉ đổi: population (01, 02, 04), intervention (04), notes.
- `qgen.build --only-drafted`: 16 câu, 2 mẩu bỏ trắc nghiệm có chủ đích, **0 mục QC không đạt**, exit 0. Phương án và thứ tự trắc nghiệm giống hệt lần trước; đoạn A3 giống từng byte.
- `vnsoc.schemas`: atom 4/4, question 16/16 hợp lệ; `verify_span` trên tệp mẩu: 0 không đạt.
- `grade_short` (câu tự viết): 71 câu của người kiểm → 0 lệch; 40 câu mới cho cách viết mới → 0 lệch (Bộ Y tế → 2; nước ngoài → 4; mồi → 5 kèm cờ decoy). Nhãn 3 vẫn không thử được (không mẩu nào có giá trị bản cũ khác giá trị hiện hành). 10 câu minh họa lỗi mục 1/4 vẫn cho 5 như dự kiến. `grade_mcq`: 8 câu × 4 chữ cái → khớp vai trò.

**Danh sách hạn chế cho người kiểm HG4.2** (bác sĩ thật)
1. 01/02: phương án Bộ Y tế là phương án duy nhất dạng điểm.
2. 02: filler 12–14 tuổi nằm trong tuổi mũi nhắc thứ ba ở nước khác (Tdap Mỹ 11–12, Td/IPV Anh 14, Td WHO 9–15).
3. 01: mồi 3–6 tháng chạm mốc 6 tháng của liều sớm/liều khi có dịch.
4. 02 chứa '18 tháng', là đáp án của 04: không đọc liền hai câu hoặc ghép vào cùng ngữ cảnh.
5. 04: '15–18 tháng' chấm nhãn 4 dù là mẩu đối chứng; '40 tháng' (trẻ Anh sinh trước 01/7/2024) chấm nhãn 5.
6. 03: đoạn A3 còn lỗi OCR, phải so với ảnh trang trước khi đóng băng.
