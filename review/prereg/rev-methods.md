```yaml
reviewer: rev-methods
milestone: prereg
recommendation: major
fatal_flaws: []
required_changes:
  - {id: 1, severity: major, where: "prereg/osf_preregistration.md §1.1 bảng H1 (dòng 138), §5.1.1 (dòng 719–737), §5.3; confirmatory.cluster_interval primary='bca'",
     what: "BCa (tiêu chí quyết định H1, nguồn p của H4) vượt cỡ danh nghĩa 0,025. Chạy lại dưới H0 (2.000 lần lặp, B = 2.000): H1 bca 0,060 (25×16), 0,048 (40×10), 0,067 (25 nhóm, cỡ cụm lognormal); B = 10.000 vẫn 0,055; H0 dày hơn (π = 0,15) 0,041. Jackknife-t và quy tắc 'conservative': 0,020–0,030. README §7.1 đã khuyến nghị 'conservative' nhưng bản OSF ghi các biến thể là 'not decisive'. Đăng ký quy tắc giao–hợp (BCa ∧ BCa mở rộng ∧ jackknife-t; p = max) cho H1 và H4, vẫn giữ BCa của đề cương làm điều kiện cần; ghi DECISIONS.md.",
     acceptance: "OSF §5.1.1–5.1.5 nêu quy tắc này là tiêu chí; mã mặc định primary='conservative'; operating_characteristics.json chạy lại có thêm kịch bản cụm không đều, cho cỡ ≤ 0,025 + 2·MCSE với H1 và H4 ở 25×16, 40×10 và cụm không đều; tiêu chí T2.10 đổi từ '≤ 0,05' thành mức này."}
  - {id: 2, severity: major, where: "confirmatory.py dòng 85, 129, 280, 437–447, 857; match/decoys.py dòng 85–98; OSF §6.2 dòng 1103, §6.4, §7 mục 31",
     what: "Mã sắp băm chưa làm đúng văn bản đăng ký: (a) π_d chưa nhân k_i; (b) N_BOOT = 2000, văn bản ghi 10.000; (c) H2 chưa có kiểm định đổi dấu chính xác; (d) H4 lấy cụm = nhóm xung đột, mẩu không có nhóm thì lấy hướng dẫn (hai loại cụm không lồng nhau), trong khi văn bản ghi cụm = hướng dẫn; chưa có hiệu chỉnh 0,5; (e) run_all gọi certified_rq3 gộp 4 mô hình × 2 ngôn ngữ, tức 8 dòng phụ thuộc cho mỗi mẩu, nên cận Clopper–Pearson không hợp lệ; (f) cột `distinct` từ đầu vào ghi đè tập H3 (simulate_study đặt distinct = xung đột ∪ có bản cũ, nên OC đã kiểm H3 trên tập rộng hơn tập đăng ký); (g) rq3_regime_b không fit lại điểm trong từng lần chia; chưa có 500 lần chia lại ở chế độ (a); (h) §6.4 không mô tả choose_decoy với dự phòng mirror_far (mồi xa gấp 2 lần); §6.2 ghi thuốc 'chung một thuốc' là trùng, trong khi grade.py dòng 253 nay đòi hai tập bằng nhau.",
     acceptance: "Mỗi điểm (a)–(h) có test trong tests/test_prereg_code.py; run_all trên simulate_study cho RQ3 theo từng mô hình, tiếng Việt, 1 dòng/mẩu; §7 mục 31 hết việc tồn; §6.2/§6.4 khớp mã ở commit được băm."}
  - {id: 3, severity: major, where: "OSF §4.3 (dòng 680–683, 689), §5.1.5 (dòng 796–806); confirmatory.h4_risk_ratio",
     what: "Cách ước lượng H4 tự đẩy RR lên: (i) câu từ chối ở A2 được tính W = 1, và quy tắc 'có giá trị ≠ không có giá trị' xếp chúng vào nhóm bất đồng. Mô phỏng: 4% câu từ chối (80% rơi vào nhóm bất đồng), RR thật của lỗi có nêu giá trị = 2, cho RR ước lượng 2,78 và tỉ lệ bác bỏ 0,84. (ii) RR thô gộp mô hình × ngôn ngữ bị nhiễu kiểu Simpson: mô hình A (60% bất đồng, rủi ro 0,30) gộp với B (10%, 0,03) cho RR 2,31, dù trong từng mô hình RR = 1. Sửa: H4 chính là RR Mantel–Haenszel phân tầng theo mô hình × ngôn ngữ, loss = nhãn 3–5 trên các câu trả lời có giá trị, bootstrap cụm theo hướng dẫn; bản W hiện tại chuyển thành phân tích phụ.",
     acceptance: "Văn bản, mã và test cập nhật; mô phỏng có câu từ chối và mô hình dị biệt cho cỡ ≤ 0,025 + 2·MCSE tại RR = 2."}
  - {id: 4, severity: major, where: "OSF §3.1 mục 2, §5.4, §5.6 B; qgen/passages.py; DR1",
     what: "Lỗi trích xuất tạo 'xung đột giả' và đẩy H1, H3 theo chiều dương (không bảo thủ). Mô phỏng: H0 cộng thêm mẩu xung đột giả, ở đó mô hình trả giá trị Bộ Y tế thật (trùng giá trị 'nước ngoài') với xác suất 0,6. Với 2% mẩu, H1 bác bỏ 0,21 (bca) / 0,13 (conservative); với 5%, 0,58 / 0,50. DR1 vẫn cho phép cận dưới độ chính xác là 0,90. H3 còn dễ bị ảnh hưởng hơn, vì đoạn oracle ở A3 chứa giá trị thật. Cần: (a) trước khi có đầu ra, kiểm bằng mã xem đoạn oracle A3 có chứa giá trị nước ngoài/bản cũ/mồi (sau chuẩn hóa) không, gắn cờ và kiểm tay lại trước đóng băng, báo cáo H3 có và không có các mẩu này; (b) phân tích điểm tới hạn cho H1 và H3: số mẩu xung đột giả (trường hợp xấu nhất) đủ để xóa kết luận, so với cận trên Clopper–Pearson của tỉ lệ xung đột giả (từ 100 mẩu xung đột được kiểm) × số mẩu xung đột; (c) quy tắc cho lỗi mẩu phát hiện sau đóng băng: bộ đóng băng là phân tích chính, bộ đã sửa là độ nhạy, liệt kê đủ mọi mẩu sửa.",
     acceptance: "Có cột passage_has_alt_value trong bảng QC kèm test; §5.6 B thêm (b) và (c), với tiêu chí 'bền vững' viết trước."}
  - {id: 5, severity: major, where: "OSF §4.3 (dòng 648), §5.4, §6.4 (dòng 1169–1190); match/decoys.py; grade.conflict_status dòng 277–300",
     what: "Mồi có thể kém 'hấp dẫn' hơn giá trị nước ngoài: nằm phía bên kia, có thể không tròn số, mirror_geom/mirror_far nằm xa hơn, mồi thuốc/phân loại do người đề xuất. Khi đó π_d thấp và Δ phồng. Mẩu xung đột không có mồi (choose_decoy trả None nhưng conflict_status vẫn là 'conflict') có D ≡ 0, và chưa có quy tắc loại. Cần: loại mẩu không có mồi khỏi H1 (báo số lượng trong addendum đóng băng); thêm ba phân tích độ nhạy cố định trước. (S1) Hiệu chỉnh hướng: ρ̂ = số câu trả lời số không khớp nguồn nào nằm phía giá trị nước ngoài / số nằm phía mồi, so với v; Δ_dir = π_f − ρ̂·π_d, bootstrap theo cùng cụm. (S2) H1 riêng trên tầng num/bp dùng mirror_arith. (S3) Tầng mẩu có độ tròn(mồi) ≥ độ tròn(nước ngoài), với độ tròn = bước lớn nhất dạng {1, 2, 5}×10^j chia hết giá trị, tính khi đóng băng. Viết trước: chỉ gọi 'H1 bền vững' khi S1 và S2 đều có cận dưới > 0.",
     acceptance: "Trường decoy_rule và roundness_ok đóng băng cùng mẩu; có hàm và test; §5.6 B.7/B.11 mở rộng; §5.4 có quy tắc cho mẩu không có mồi."}
  - {id: 6, severity: minor, where: "OSF §1.1 định nghĩa conflict family (dòng 96), §5.6 B.10",
     what: "Nhóm xung đột chưa có định nghĩa vận hành. Cách gán nhóm là quyết định chủ quan, quyết định số cụm C và việc chuyển giữa BCa và t tại ngưỡng 20 cụm. Nhóm xung đột và hướng dẫn lại đan chéo nhau. Cần: quy tắc gán (ví dụ cùng bản ghi nguồn nước ngoài × tham số × giá trị Bộ Y tế); bắt buộc mọi mẩu xung đột có nhóm khi đóng băng; báo số nhóm trải qua hơn một hướng dẫn; viết trước câu chữ sẽ dùng nếu B.10 (cụm theo hướng dẫn) không xác nhận H1.",
     acceptance: "Định nghĩa có trong §1.1; kiểm bằng schema; bảng chéo nhóm × hướng dẫn trong addendum đóng băng."}
  - {id: 7, severity: minor, where: "OSF §5.1.3, §5.4 (dòng 1012), §3.1 mục 7",
     what: "H2 dễ lệch đo lường theo ngôn ngữ: tiếng Việt tốn nhiều token hơn nên dễ bị cắt ở 128 token, mất dòng ĐÁP ÁN và khó tách đáp án, làm FUS(VI) thấp giả. Cần: độ nhạy H2 chỉ trên các cặp mà cả hai câu có parse_method = answer_line và không bị cắt (finish_reason = length); báo tỉ lệ bị cắt theo mô hình × ngôn ngữ; kiểm tay 500 câu phân tầng theo ngôn ngữ; xét DR9 riêng theo ngôn ngữ.",
     acceptance: "Các mục trên có trong §5.6 B và §3.1."}
  - {id: 8, severity: minor, where: "OSF §5.1.7 (dòng 860–872), §5.3",
     what: "Chế độ (a): so với rủi ro toàn kho là đúng ước lượng cho quần thể hữu hạn. Nhưng 500 lần chia lại cal/test (giữ ref cố định) đã được bảo đảm theo thiết kế (lấy mẫu không hoàn lại, phân phối siêu bội), nên chỉ là kiểm tra cài đặt, không phải bằng chứng trao đổi được với câu hỏi lúc triển khai. Cần: nêu phạm vi bảo đảm (câu hỏi rút đều từ kho không-ref của từng mô hình, tại ngày đóng băng); nói rõ δ = 0,10 áp dụng cho từng mô hình (với 4 mô hình, xác suất ít nhất một bộ cận sai tới 1 − 0,9⁴ ≈ 0,34); thêm độ nhạy chia theo cụm (nhóm xung đột, dự phòng hướng dẫn) mà đề cương §4.7 ưu tiên.",
     acceptance: "Câu chữ có trong §5.1.7 và §5.3; thêm một dòng phân tích độ nhạy."}
  - {id: 9, severity: minor, where: "OSF §5.4–5.5",
     what: "Quy tắc loại trừ và dữ liệu thiếu chưa đủ. Chưa có cách xử lý một ô không đạt 98% sau khi đã chạy lại. Câu needs_llm không tách được (thành nhãn 6) cần phân tích độ nhạy loại chúng ra. Cận thiếu dữ liệu theo kịch bản cực trị mới áp cho H1; cần mở rộng cho H3 (theo từng mô hình) và H4. Lời nhắc của LLM tách đáp án phải không chứa giá trị tham chiếu.",
     acceptance: "§5.4–5.5 có đủ các quy tắc trên."}
  - {id: 10, severity: minor, where: "OSF §5.1.4, §5.1.6; prereg/analysis_plan/simulate_operating_characteristics.py",
     what: "Partial conjunction dạng Bonferroni hợp lệ dưới mọi kiểu phụ thuộc, và Holm chỉ cần p biên hợp lệ, nên đưa H3 vào Holm là hợp lệ. Tuy vậy p_m từ cp_design_effect chỉ xấp xỉ và mới được kiểm với cụm cỡ đều. Cần: thêm kịch bản LFC của H3 với cụm không đều; viết lập luận về tính hợp lệ vào văn bản.",
     acceptance: "Dòng OC mới cho cỡ ≤ 0,025 + 2·MCSE."}
```

# Phản biện phương pháp — bản đăng ký trước OSF

Người phản biện: agent rev-methods (Claude), không phải người thật. Ngày 2026-09-26.

**Kết luận: sửa lớn.** Chưa có lỗi chết người nếu sửa xong trước khi băm mã và nộp OSF (HG2.9, hạn 7/10). Hiện mã và văn bản chưa khớp, tiêu chí chính H1 chưa giữ đúng mức sai loại I, và cách ước lượng H4 tự thiên lệch.

## Kiểm lại

- `pytest -q tests/test_prereg_code.py`: 21/21 đạt.
- Tự mô phỏng dưới H0 trên `simulate_study`: 2.000 lần lặp, B = 2.000. Cỡ cụm không đều: giữ số mẩu lognormal trong mỗi nhóm. H4 lấy cụm theo hướng dẫn, đúng như văn bản.

| Bác bỏ (danh nghĩa 0,025) | 25×16 | 40×10 | 25 nhóm, không đều |
|---|---|---|---|
| H1 BCa (tiêu chí đăng ký) | **0,060** | **0,048** | **0,067** |
| H1 conservative | 0,029 | 0,024 | 0,024 |
| H4 BCa, cụm hướng dẫn | 0,028 | 0,031 | **0,043** |
| H4 conservative | 0,015 | 0,020 | 0,024 |

Với B = 10.000, H1 BCa vẫn là 0,055, nên lỗi nằm ở chính BCa khi có ít cụm, không phải ở sai số Monte Carlo. README §6 cũng ghi "FAIL" cho `bca`. Ngưỡng T2.10 "≤ 0,05" cho phép cỡ gấp đôi danh nghĩa (yêu cầu 1).

## Các điểm chính

**Mã ≠ văn bản** (yêu cầu 2). Ngoài 5 điểm §7 mục 31 đã tự liệt kê, tôi tìm thêm:
- `run_all` (dòng 857) gộp RQ3 qua mô hình và ngôn ngữ, nên cận Clopper–Pearson mất hiệu lực;
- cột `distinct` ghi đè tập H3 (dòng 129);
- §6.4 không mô tả `mirror_far`, và §6.2 lệch với `grade._gap` cho thuốc (dòng 253).

**H4** (yêu cầu 3). Quy tắc "có giá trị ≠ không giá trị" (§4.3) đưa câu từ chối ở A2 vào nhóm bất đồng, trong khi W vẫn tính câu từ chối là lỗi. Gọi lựa chọn này là "conservative" (§7 mục 11) đúng với cận RQ3 nhưng sai với H4. RR thô gộp nhiều mô hình còn bị nhiễu bởi khác biệt giữa các mô hình.

**Xung đột giả** (yêu cầu 4). Chỉ 2% mẩu xung đột giả đã đẩy tỉ lệ bác bỏ H1 dưới H0 lên 0,13–0,21. H3 còn dễ bị ảnh hưởng hơn: ở A3 mô hình đọc đúng giá trị thật trong đoạn rồi bị chấm là "cố chấp". Kiểm đoạn oracle bằng mã không cần nhãn và làm được trước khi có đầu ra.

**Mồi** (yêu cầu 5). B.11 chỉ chạy nếu có chú thích thêm, mà hiện chưa ai thu. Rủi ro lớn nhất là thiên lệch hướng: nếu lỗi của mô hình nghiêng về phía giá trị quốc tế, mồi đối xứng ở phía bên kia sẽ đánh giá thấp mức trùng ngẫu nhiên. S1 đo đúng điều này và chỉ dùng dữ liệu đã có. Mẩu xung đột không có mồi hiện có D ≡ 0.

**Chia tập và cụm** (yêu cầu 6, 8).
- Mỗi mô hình một dòng tiếng Việt cho mỗi mẩu: đúng cho cận Clopper–Pearson.
- Nhóm xung đột chưa có định nghĩa vận hành, mà nó quyết định số cụm C.

**H3, H4 một phía, McNemar** (yêu cầu 10).
- Partial conjunction dạng Bonferroni cộng Holm là hợp lệ. Chỗ còn yếu là p theo từng mô hình dựa trên hệ số thiết kế.
- H4 kiểm định một phía đúng dạng; vấn đề nằm ở ước lượng.
- Durkalski khớp các ví dụ đã công bố; kiểm định đổi dấu dự phòng chưa được viết thành mã.

## Khả thi

Mọi yêu cầu chỉ là mã Python, trường dữ liệu đóng băng hoặc câu chữ; không cần thêm GPU hay API. Khoảng 1–2 ngày làm việc, kịp hạn 7/10.
