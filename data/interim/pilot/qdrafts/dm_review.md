# Phản biện độc lập bộ câu hỏi thí điểm: chủ đề `dm`

- Người phản biện: agent AI đóng vai rev-clinician và rev-methods. **Đây không phải bác sĩ thật.** Không được ghi "bác sĩ đã duyệt".
- Ngày: 2026-09-26. Không xem bất kỳ đầu ra nào của mô hình được kiểm tra (quy tắc chống rò rỉ).
- Đầu vào đã đọc:
  - `dm.jsonl` (8 bản nháp);
  - `pilot_atoms.jsonl` (P-dm-01..08, đọc đủ mọi trường);
  - `dm_q.jsonl` (24 câu), `dm_p.jsonl` (8 đoạn A3), `dm_qc.csv`;
  - `src/vnsoc/qgen/*.py`, `grade.py` (`_gap`, `classify_value`, `grade_mcq`), `configs/conditions.yaml`;
  - đề cương §3.5, §4.3, §4.4, §5.7; skill question-generation.
- Tái lập: chạy lại `vnsoc.qgen.build --only-drafted`, ghi ra scratchpad. Kết quả: 24 câu, 8 đoạn A3, 1 mục QC không đạt (`P-dm-05|mcq: mẩu không có mồi`). `dm_q.jsonl` và `dm_p.jsonl` trùng từng byte với bản trong dự án.

## Tổng kết

| atom | trạng thái | vai trò thực tế | bản nháp | câu đã dựng | kết luận |
|---|---|---|---|---|---|
| P-dm-01 | conflict (US) | xung đột sạch | pass | short pass; **MCQ cần sửa bằng mã** (S1) | **fix** (mã) |
| P-dm-02 | concordant | đối chứng sạch | pass | pass | **pass** |
| P-dm-03 | conflict (US) | xung đột sạch | pass | short pass; **MCQ cần sửa bằng mã** (S1) | **fix** (mã) |
| P-dm-04 | concordant (hợp DR8) | **đối chứng suy biến** (S3) | pass | pass + gắn cờ | **pass** (gắn cờ) |
| P-dm-05 | concordant (hợp DR8) + superseded | **đối chứng suy biến** (S3) | pass | short pass + gắn cờ; **MCQ loại** | **drop** (chỉ MCQ) |
| P-dm-06 | concordant | đối chứng sạch | pass | pass | **pass** |
| P-dm-07 | concordant | đối chứng sạch | pass | pass | **pass** |
| P-dm-08 | concordant | đối chứng sạch | pass | pass (ghi chú DR8) | **pass** |

- **Theo mẩu:** pass 5 (02, 04, 06, 07, 08), fix 2 (01, 03), drop 1 (05, chỉ phần MCQ).
- **Bản nháp:** không mẩu nào phải sửa chữ. Mọi việc cần sửa nằm ở mã hoặc ở gắn nhãn phân tích.
- **Theo câu đã dựng (24):**
  - 16 câu trả lời ngắn: pass;
  - 8 câu MCQ của P-dm-01 và P-dm-03: fix, phải chờ sửa mã S1 rồi dựng lại;
  - MCQ của P-dm-05 (chưa dựng): drop.

## Vấn đề nghiêm trọng (phải xử lý trước khi đóng băng bộ câu hỏi)

**S1. Dấu so sánh làm lộ phương án (lỗi hệ thống, nằm ở mã dựng MCQ).**
- Ở P-dm-01, bốn phương án là `8 %`, `> 10 %`, `11 %`, `≥ 9 %`. Ở P-dm-03 là `55 tuổi`, `25 tuổi`, `≥ 45 tuổi`, `≥ 35 tuổi`.
- Chỉ phương án VN và phương án nước ngoài có dấu `≥/>`. Mồi (không có `cmp`) và nhiễu do `rule_filler` sinh (không đặt `cmp`) thì không có dấu.
- Với câu hỏi "ngưỡng", hai phương án có dấu trông như ngưỡng thật. Mô hình có thể loại mồi và nhiễu chỉ nhờ hình thức. Hệ quả là P(nước ngoài) bị đẩy lên so với P(mồi) vì lý do không liên quan đến kiến thức. Phép so sánh chính của MCQ (§3.5) bị lệch **đúng theo chiều giả thuyết**.
- Tôi quét toàn bộ MCQ thí điểm (vi, o0): **7/29 câu** mắc lỗi này. Ngoài dm-01 và dm-03 còn có controls-09, hbv-03, hbv-07, hbv-08, hbv-10.
- Sửa (mã, người giữ `src/`): hiển thị cả 4 phương án cùng một dạng. Có hai cách:
  - (a) mồi và nhiễu nhận `cmp` của `vn[0]` khi dựng (`rule_filler`, `mirror_arith`);
  - (b) bỏ `cmp` khỏi mọi phương án khi slot là threshold.
- Sau khi sửa phải dựng lại. Nên có test: mọi câu MCQ có số phương án mang dấu là 0 hoặc 4.

**S2. `mcq.options()` gán sai vai "superseded" cho giá trị vẫn thuộc tập Bộ Y tế hiện hành (lỗi tiềm ẩn).**
- Ứng viên bản cũ chỉ được so với các phương án đã chọn, tức `vn[0]` và `conf[0]`, không so với cả tập `vn`. Riêng `_conflicting()` thì lọc nước ngoài theo cả tập `vn`.
- Mô phỏng (thêm mồi giả vào bản sao P-dm-05): `superseded:3319/2017 = two_step_allowed` được chọn làm phương án. Nhưng `two_step_allowed` nằm trong tập VN (3879/2014, DR8), nên câu sẽ có **hai phương án đúng theo Bộ Y tế**.
- `grade_mcq` tin vai trò theo chữ cái, nên mô hình chọn phương án này sẽ bị chấm là lệch phiên bản (nhãn 3) dù đúng theo Bộ Y tế.
- Hiện lỗi đang bị che vì P-dm-05 không có mồi. Mẩu khác có cùng tình trạng (bản cũ nằm trong tập VN): **P-hbv-06** (3310/2019 và 5448/2014), cũng đang bị che vì không có mồi.
- Sửa (mã):
  - `options()` lọc `sup` bằng `all(_gap(it, v) > 0 for v in atom["vn"])`;
  - `build_all` chỉ dựng MCQ khi có ít nhất một giá trị cài sẵn không thuộc Bộ Y tế (nước ngoài xung đột, hoặc bản cũ ngoài tập VN). Nếu không có, ghi `ok=True` kèm ghi chú "MCQ không áp dụng" thay vì lỗi.
- Bản nháp không sửa được lỗi này. Đặt stem = null sẽ sinh lỗi QC "thiếu stem trắc nghiệm".

**S3. Hai mẩu "concordant" chỉ vì DR8 lấy hợp hai giá trị loại trừ nhau (P-dm-04, P-dm-05).**
- Tập VN của P-dm-04 là {≥ 130, ≥ 140}. Tập VN của P-dm-05 là {one_step_only, two_step_allowed}. Vì vậy mọi đáp án theo chuẩn Mỹ hoặc chuẩn Việt Nam đều được chấm "đúng Bộ Y tế".
- Hai mẩu này không phải mẩu xung đột, cũng không phải đối chứng sạch. Đưa vào mẫu số độ chính xác đối chứng sẽ thổi phồng độ chính xác đối chứng.
- Không sửa được bằng quần thể: 5481/2020 và bài của 3879/2014 cùng áp dụng cho người lớn ĐTĐ típ 2 và thai phụ tuần 24–28.
- Đề nghị:
  - gắn nhãn phân tích (ví dụ `concordant_by_union`);
  - loại khỏi mẫu số đối chứng, hoặc báo cáo riêng;
  - quyết định cuối để HG1.2 (hiệu lực của các bài trong 3879/2014) trả lời.
- Việc này là của statistician/người giữ atoms, không phải của người viết câu.

## Vấn đề mức vừa và nhẹ

- **M1. Nhiễu `11 %` của P-dm-01 có thể không "trung lập" (chưa kiểm nguồn).**
  - Theo hiểu biết chung, **chưa kiểm nguồn**: đồng thuận ADA/EASD 2018 và Hình 9.2 của ADA Standards 2019–2020 ghi "insulin là thuốc tiêm đầu tiên nếu A1C > 11%". Nếu đúng, `11 %` là giá trị Mỹ/châu Âu bản cũ, không phải giá trị "không nguồn nào".
  - Tác động nhỏ vì phép so sánh chính là nước ngoài với mồi, và chọn nhiễu bị chấm "khác".
  - Việc cần làm: counterpart-matcher kiểm nguồn. Nếu đúng, đặt `filler` rõ ràng trong bản nháp (build nhận `filler` cả cho num), ví dụ `{"lo": 12, "hi": 12, "unit": "%"}`. Tôi chưa thấy nguồn nào dùng 12%, nhưng con số này cũng phải kiểm.
- **M2. `passages.py`: regex tách câu `SENT_END` coi chữ thường tiếng Việt là đầu câu.**
  - Lớp `À-Ỹ` (U+00C0–U+1EF8) chứa cả `à á ư ơ đ …`, nên đoạn bị cắt sau dấu ":" hoặc ";" ngay giữa câu.
  - Hệ quả: đoạn A3 của P-dm-01 và P-dm-02 bắt đầu bằng "ưu tiên chọn SGLT-2i, GLP-1 f) …", trái quy tắc "không cắt giữa câu".
  - Sửa (mã): chỉ chấp nhận chữ in hoa, ví dụ kiểm `ch.isupper()`, hoặc lớp ký tự in hoa tiếng Việt tường minh.
- **M3. Đoạn A3 của P-dm-03 thiếu ngữ cảnh.**
  - Đoạn bắt đầu bằng số trang in "10 b) Phụ nữ …". Tiêu đề mục 1.2 ("Khuyến cáo làm xét nghiệm để tầm soát … ở người lớn không có triệu chứng") và điểm a) nằm ở trang PDF 11, nên không có trong đoạn.
  - Đáp án "c) Tất cả mọi người từ 45 tuổi trở lên" vẫn có mặt, nhưng người đọc chỉ suy ra đây là tầm soát nhờ điểm d).
  - Đề nghị (mã): cho phép đoạn A3 nối phần cuối của trang trước khi span nằm gần đầu trang, và bỏ số trang in ở đầu. Trước đóng băng nên kiểm tay đoạn này, và gắn cờ trong phân tích độ nhạy H3.
- **M4. P-dm-08, ghi chú DR8 (không đổi câu hỏi).**
  - 3879/2014 tr. 235, Bảng 2, liệt kê ngưỡng lúc đói của nghiệm pháp 75 g: "WHO ≥ 7 mmol/L; EASD ≥ 6 mmol/L". Bảng này mang tính thông tin ("người ta cũng đang cố gắng toàn cầu hoá …"), không phải khuyến cáo.
  - Khuyến cáo một bước của chính bài đó (mục 2.1) là ≥ 92 mg/dL (5,1 mmol/L).
  - Câu hỏi nêu "phương pháp một bước" và "chẩn đoán ĐTĐ thai kỳ", nên đáp án 5,1 vẫn duy nhất.
  - Đề nghị ghi vào `extraction.notes` của mẩu để HG1.2 và người kiểm bộ chấm biết: đáp án "7,0 mmol/L" sẽ bị chấm "khác" (nhãn 5).

## Nhận xét từng mẩu

Ký hiệu 6 tiêu chí: (1) đáp án duy nhất, nước ngoài không "cũng đúng"; (2) lộ đáp án hoặc nguồn; (3) EN trung thành; (4) tự nhiên; (5) MCQ; (6) đơn vị.

### P-dm-01: fix (ở mã; bản nháp giữ nguyên)
- **(1) Đạt.**
  - 5481/2020 mục 4.2.f: "A1C ≥ 9%". Tôi quét lớp chữ toàn bộ 77 trang và đọc bằng mắt Hình 2 (tr. 23, sơ đồ thuốc) và Hình 3 (tr. 26, sơ đồ insulin). Không có ngưỡng HbA1c khởi trị insulin nào khác. Hình 3 chỉ có "HbA1c < 8%, xem xét giảm liều nền", là ngữ cảnh chỉnh liều.
  - 1353/2021 chỉ sửa tr. 37 điểm b. 5904/2019 chuyển phần insulin sang hướng dẫn khác. Bài ĐTĐ típ 2 của 3879/2014 đã bị bãi bỏ.
  - Câu hỏi hỏi ngưỡng dưới ("từ mức nào trở lên"), nên "> 10 %" không đồng thời đúng: ở HbA1c 9,5% Bộ Y tế cân nhắc insulin, ADA thì không.
  - Loại trừ rõ dị hóa và triệu chứng là đúng. Việc này còn tránh trùng với kiểu ngưỡng "≥ 9% kèm triệu chứng" của các thuật toán Mỹ khác (hiểu biết chung, chưa kiểm).
- **(2) Đạt.**
- **(3) Đạt:** "based on HbA1c alone", "at what … level or higher".
- **(4) Đạt.** "HbA1c" lặp hai lần nhưng chấp nhận được.
- **(5) Không đạt vì S1.** Cùng đơn vị %. Không phương án nào đúng theo Bộ Y tế. Nhiễu 11% xem M1.
- **(6) Đạt:** "(%)".
- **Sửa cụ thể:** sửa mã theo S1 rồi dựng lại MCQ. Kiểm M1; nếu xác nhận thì thêm `filler` rõ ràng vào bản nháp.

### P-dm-02: pass
- **(1) Đạt:** concordant, Bộ Y tế và ADA cùng ≥ 300 mg/dL (16,7 mmol/L).
- **(2), (3), (4), (6) Đạt:** "(mg/dL)".
- Tùy chọn, không bắt buộc: thêm "không có dấu hiệu dị hóa và không có triệu chứng tăng đường huyết" để song song với P-dm-01.
- Đoạn A3 bắt đầu giữa câu (M2), dùng chung đoạn với P-dm-01.

### P-dm-03: fix (ở mã; bản nháp giữ nguyên)
- **(1) Đạt.**
  - 5481 mục 1.2 có ba nhánh:
    - a) người lớn có BMI ≥ 23 kèm ≥ 1 yếu tố nguy cơ (tr. 11);
    - b) phụ nữ có tiền sử ĐTĐ thai kỳ;
    - c) mọi người từ 45 tuổi.
  - Quần thể được viết là "không thừa cân/béo phì **và** không yếu tố nguy cơ **và** không tiền sử ĐTĐ thai kỳ", nên chỉ còn nhánh c) → 45. 3087/2020 và 3319/2017 cũng là 45. 5904/2019 không nêu tuổi tầm soát.
  - ADA "mọi người khác" → 35. USPSTF (35–70, có thừa cân) không áp dụng vì quần thể không thừa cân.
  - Cách viết tập con chặt hơn của người viết là đúng.
- **(2) Đạt.**
- **(3) Đạt.**
- **(4) Đạt.** Tùy chọn: "típ 2/tiền đái tháo đường" → "típ 2 hoặc tiền đái tháo đường". Câu có 55 từ, gần trần 60.
- **(5) Không đạt vì S1.** Cùng đơn vị tuổi.
  - Nhiễu 25: theo hiểu biết chung, chưa kiểm, NICE PH38 đánh giá nguy cơ từ 25 tuổi cho người gốc Nam Á/Trung Quốc. Đó là nhóm có yếu tố nguy cơ sắc tộc, không thuộc quần thể đã nêu, nên chấp nhận được. Không nên đổi sang 40 vì NICE/NHS Health Check dùng ≥ 40 (chưa kiểm).
  - Mồi 55 xuất hiện ở Hình 2 của 5481 dưới dạng "tuổi ≥ 55", nhưng đó là tiêu chí nguy cơ tim mạch, là đại lượng khác, nên chấp nhận được.
- **(6) Đạt:** "(tuổi)".
- **Sửa cụ thể:** sửa mã S1 rồi dựng lại MCQ. Kiểm tay đoạn A3 (M3).

### P-dm-04: pass (bản nháp), gắn cờ S3
- **(1) Không duy nhất, và không sửa được bằng quần thể.** Tập VN là {≥ 140 (5481 mục 6.1.1), ≥ 130 (3879/2014, bài THA ở người ĐTĐ, DR8)}. Giá trị Mỹ 130 cũng đúng theo Bộ Y tế.
- Câu hỏi đã nêu đủ các yếu tố tách ngữ cảnh: đo tại phòng khám, kiểm tra lại vào ngày khác, huyết áp tâm thu, ngưỡng **chẩn đoán xác định**. Nhờ vậy câu tách được khỏi ngưỡng đo lại 130/80 (cùng đoạn) và ngưỡng điều trị ở 6.1.3.
- **(2)–(4), (6) Đạt:** "(mmHg)".
- **Sửa cụ thể:** không sửa chữ. Gắn nhãn `concordant_by_union`, loại khỏi mẫu số đối chứng, chờ HG1.2.

### P-dm-05: drop phần MCQ; câu trả lời ngắn pass, gắn cờ S3
- **MCQ.**
  - Theo DR8: hai phương án đúng theo Bộ Y tế, trong đó một phương án bị gán sai vai "superseded" (S2).
  - Nếu HG1.2 bỏ 3879/2014: `two_step_allowed` trùng cùng lúc Mỹ (ADA 2026), 3319/2017 và 3879/2014, nên không quy được vai trò.
  - Loại chỉ có hai nhãn nên sẽ cần hai phương án bịa thêm.
  - Kết luận: MCQ không cho thông tin theo cả hai cách hiểu. **Loại.** Tôi đồng ý với người viết.
- **Câu trả lời ngắn.**
  - (2) Không lộ đáp án: tránh mọi từ khóa của `cat_options` (1/2 bước, 75/50/100 g).
  - (3) và (4) đạt. (6) Đạt: "(tên phương pháp/nghiệm pháp)".
  - (1) Theo DR8, mọi chiến lược đều được chấm "đúng Bộ Y tế" (S3).
  - Ghi chú cho HG1.2: 5481 viết "Hiện tại ở Việt Nam **có thể** thực hiện phương pháp 1 bước". Đây là lời cho phép, nên nhãn `one_step_only` là một cách diễn giải. 1470/2024 (bản quét) viết theo kiểu chỉ định rõ hơn.
- **Sửa cụ thể:**
  - giữ các stem trong bản nháp (vô hại, dùng được nếu HG1.2 đổi kết luận);
  - sửa mã S2 để build ghi "MCQ không áp dụng" thay vì lỗi QC;
  - trước khi sửa mã, coi dòng `P-dm-05|mcq` trong `dm_qc.csv` là ngoại lệ đã giải trình.

### P-dm-06: pass
- **(1) Đạt:** concordant, ≥ 7,0 mmol/L (126 mg/dL) ở 5481, 5904/2019 tr. 18, WHO 2006 và ADA 2026.
- Câu nêu "huyết tương tĩnh mạch" và "lúc đói ≥ 8 giờ", đủ để tách khỏi glucose 2 giờ sau NPDNG, HbA1c, glucose bất kỳ, rối loạn glucose lúc đói (5,6–6,9) và ngưỡng ĐTĐ thai kỳ.
- **(2)–(6) Đạt.** Đoạn A3 có lỗi chữ "ngư ng" từ lớp chữ PDF; chỉ là lỗi hình thức.

### P-dm-07: pass
- **(1) Đạt:** ≥ 6,5% ở 5481, 5904/2019, WHO 2011 và ADA 2026.
- **(2) Đạt:** "tiêu chuẩn quốc tế" là yêu cầu về phương pháp đo (có trong chính văn bản 5481), không gợi ý quốc gia.
- **(3)–(6) Đạt:** "(%)" loại được đáp án IFCC mmol/mol.

### P-dm-08: pass
- **(1) Đạt:** 5,1 mmol/L ở 5481, 3319/2017, 1470/2024, 3879/2014 mục 2.1, WHO 2013 và ADA 2026 (một bước). Xem ghi chú DR8 ở M4.
- "75 g" trong câu thuộc quần thể (loại nghiệm pháp), không phải giá trị trả lời, nên không lộ.
- **(2)–(6) Đạt:** "(mmol/L)".

## Nhật ký kiểm chứng (để tái lập)

- Build dựng lại vào scratchpad: exit 1, đúng 1 mục QC không đạt (P-dm-05|mcq). File đầu ra trùng byte với bản trong dự án.
- 5481/2020: quét regex lớp chữ cả 77 trang tìm ngưỡng HbA1c/insulin. Trang 23 và 26 là ảnh, đã render 130 dpi và đọc bằng mắt.
- 1353/2021: toàn văn 1 trang. Chỉ bổ sung người biên soạn và sửa tr. 37 điểm b.
- 5904/2019 (`__9e6bbe13`), tr. 15–31: không có tuổi tầm soát, không có ngưỡng HbA1c khởi trị insulin. Có HbA1c ≥ 6,5%, glucose lúc đói ≥ 7,0 mmol/L, mục tiêu HbA1c 6,5–8,5%.
- 3879/2014, tr. 234–236 (bài ĐTĐ thai kỳ): một bước 5,1 mmol/L; hai bước 50 g → 100 g; Bảng 2 WHO/EASD (M4).
- Mô phỏng `mcq.options()` cho P-dm-05 có mồi giả; quét mọi mẩu thí điểm có bản cũ nằm trong tập VN → P-dm-05, P-hbv-06 (S2).
- Quét 29 MCQ thí điểm (vi, o0) tìm lệch dấu so sánh → 7 câu (S1).
- Kiểm `SENT_END` với các ký tự `ư à á đ ơ` → đều khớp lớp "đầu câu" (M2).

## Xử lý sau phản biện (atom-extractor + question-writer, agent AI, 2026-09-26)

Không xem đầu ra mô hình. Tái lập: `pilot_merge --only dm` (8 giữ, 0 loại) → `qgen.build --only-drafted` (24 câu, 0 QC lỗi) → chấm thử 24 câu trả lời tự viết (24/24 đúng nhãn).

- **S1 (dấu so sánh):** sửa ở mã. Mồi và filler nay hiển thị cùng dấu với phương án nước ngoài. P-dm-03: cả bốn phương án là `≥`. P-dm-01: mồi, filler và nước ngoài là `>`, Bộ Y tế là `≥` (dấu thật của hai nguồn). **Còn lại:** phương án Bộ Y tế là phương án duy nhất khác dạng, nên lộ đáp án đúng. So sánh nước ngoài–mồi không lệch. Cần sửa ở mã.
- **S2:** sửa ở mã (`superseded_outside` so với cả tập Bộ Y tế; `skip_reasons`). P-dm-05 được bỏ trắc nghiệm có chủ đích, không còn lỗi QC.
- **S3:** đã ghi `[concordant_by_union]` vào `extraction.notes` của P-dm-04 và P-dm-05. Chờ statistician và HG1.2.
- **M1:** đã kiểm nguồn. ADA/EASD 2018 (Europe PMC PMC6245208, sha256 `4ad79df8…`) nêu HbA1c > 11% trong mục "Choice of Glucose-Lowering Medication After Metformin". Giá trị này được ghi thành giá trị nước ngoài (US, 2018) của P-dm-01, nên k_i = 2. Bỏ filler tay 12%. Filler quy tắc mới là 7%, trùng số với mục tiêu HbA1c < 7% ở 5481 Bảng 4. Mồi 8% trùng số với chú thích "HbA1c <8%, xem xét giảm liều nền" ở 5481 Hình 3 (tr. 26, trang ảnh). Cả hai thuộc khe khác. Người kiểm ngữ cảnh quyết định (ghi ở `extraction.notes`).
- **M2:** sửa ở mã. Đoạn A3 của P-dm-01/02 nay bắt đầu ở "e) Với các BN…".
- **M3:** mới sửa một phần. Số trang in đã bỏ, nhưng đoạn vẫn thiếu tiêu đề 1.2 và điểm a) (ở trang 11). Vẫn phải kiểm tay trước đóng băng.
- **M4:** đã kiểm `verify_span --page 3879/2014 235` và ghi vào `extraction.notes` của P-dm-08. Chấm thử cho "7,0 mmol/L" → nhãn 5; "6 mmol/L" → nhãn 5.
- **P-dm-05:** khôi phục bản nháp. Có 2 câu trả lời ngắn; trắc nghiệm được bỏ có chủ đích.
- **population:** tách ghi chú của người trích ra khỏi population. P-dm-01 thêm khóa `clinical`. P-dm-04 bỏ khóa `setting`. P-dm-03 viết lại rõ theo đúng tập con mà câu hỏi nêu. P-dm-05 và P-dm-08 thêm khóa định lượng `gestational_age`. Câu chữ các câu hỏi không đổi.

## Xử lý sau phản biện vòng 2 (atom-extractor + question-writer, agent AI, 2026-09-26)

Không xem đầu ra mô hình, không sửa `src/`, không commit. Script: `scratchpad/qfix/edit_dm_round2.py`, chạy từ bản sao lưu `dm_atoms_before.jsonl` và `dm_drafts_before.jsonl`; bản gốc vòng 1 giữ ở `*_before_round1.jsonl`.

- **Lộ đáp án qua dấu so sánh ở trắc nghiệm P-dm-01:** xác nhận, nhưng không sửa được ở dữ liệu. Dấu là của chính nguồn: 5481 ghi "≥9%", ADA 2026 slide 176 ghi "A1C >10%" (kiểm lại bằng XML). `option_text` bị mã từ chối cho mẩu num. **Không đóng băng 4 câu `P-dm-01|mcq|*`** trước khi `src/` được sửa. Trên toàn bộ trắc nghiệm thí điểm (23 câu vi/o0), có 2 câu mà phương án Bộ Y tế là phương án duy nhất khác dấu: P-dm-01 và P-hbv-03.
- **P-dm-04, câu trả lời nêu cả tâm thu lẫn tâm trương bị chấm nhãn 5:** xác nhận. Đã thử chuyển sang bp (mô phỏng, không ghi). verify_span đạt, nhưng chỉ nhờ span DR8 của 5904/2019. Bộ chấm bp lại cho nhãn 6 với dạng "và/hay", dạng "hay" và câu chỉ nêu tâm thu, tức tệ hơn num. Vì vậy giữ num. Giảm thiểu ở bản nháp: câu hỏi ngắn thêm "(mmHg; chỉ nêu giá trị tâm thu)". Sửa gốc thuộc `src/`: thêm "và/hay", "hay" vào `normalize_vi._JOIN`.
- **P-dm-08, tiêu chí WHO 1999 (lúc đói ≥ 7,0 mmol/L):** đã tải được nguồn gốc (IRIS, sha256 `2887575f…`). Nguồn là bản quét, grep ra 0. Giá trị đọc bằng ảnh ở §6.1 (tr. 26) và Bảng 1 (tr. 58), và được xác nhận gián tiếp bằng máy qua bảng của WHO 2013 tr. 21. **Không ghi**, vì hai lý do: chỉ có thể ghi với `verified_by` null, và mô phỏng cho thấy quy tắc sẽ sinh mồi 3,0 mmol/L và filler 0,9 mmol/L (phi lý lâm sàng, sẽ thổi phồng F−D theo chiều H1). Chờ người quyết.
- **P-dm-02, cảnh báo "không thấy 16.7":** giới hạn của mã. `cached_text` đọc pptx như byte zip thô. Đã kiểm lại bằng XML slide 176 (16,7 mmol/L đúng), cùng các slide 29, 44, 200. Chỉ thêm ghi chú.
