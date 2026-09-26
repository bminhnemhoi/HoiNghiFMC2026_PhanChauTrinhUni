```yaml
reviewer: rev-novelty (AI, không phải người)
milestone: M1
recommendation: major
scores: {importance: 6, novelty: 6, rigor: 5, feasibility: 6, q1_likelihood: 4, fit: 7}   # trung bình không trọng số 5,7
fatal_flaws: []
required_changes:
  - id: 1
    severity: major
    where: "manuscript/fmc/abstract_fmc.md dòng 25 (VI) và 55 (EN); bản dựng manuscript/build/fmc/abstract_fmc_{vi,en}.docx"
    what: "[TRƯỚC KHI NỘP] Hai câu Phương pháp sai sự thật. (a) ‘65 khuyến cáo … từ 13 hướng dẫn hiện hành’: TT52/2025 đã hết hiệu lực 01/7/2026 (state/gates/HG1.2_result.md dòng 14–16), 3 mẩu của văn bản này chỉ còn mô tả; tập phân tích là 61 mẩu từ 12 văn bản hiện hành. (b) ‘Mỗi khuyến cáo gắn giá trị WHO, Mỹ, châu Âu, giá trị bản cũ và một giá trị mồi’: trong data/interim/pilot_atoms.jsonl chỉ 11/65 mẩu có đủ WHO + Mỹ + châu Âu, 13/65 có giá trị châu Âu, 27/65 có bản cũ, 23/65 có mồi, 1 mẩu không có đối chiếu nước ngoài."
    acceptance: "Câu mới viết đại ý: 65 mẩu từ 13 văn bản, phân tích 61 mẩu từ 12 văn bản hiện hành; giá trị nước ngoài có phiên bản khi có, bản cũ khi có, mồi cho 15 mẩu xung đột. Số 61 và 12 đi qua khóa registry mới do src/vnsoc/analysis/pilot.py put() sinh ra; make verify qua; grep ‘Mỗi khuyến cáo gắn’ trong cả hai DOCX không còn kết quả."
  - id: 2
    severity: major
    where: "abstract_fmc.md dòng 21/51 (Mục tiêu), 29/59 (Kết quả), 33/63 (Kết luận), 7 và 79 (ô tóm tắt)"
    what: "[TRƯỚC KHI NỘP] Kết luận nói quá, và cách chọn số để báo có thiên lệch. (a) ‘Lỗi chủ yếu là giá trị không có nguồn’: nhãn 5 là nhóm còn lại, gồm cả câu trả lời sai dạng, sai đơn vị, giá trị nằm ở biên dung sai và khoảng giá trị trộn nhiều nguồn; không được hiểu là ‘bịa’. (b) Không báo phép so sánh cần thiết: ở A1 tiếng Việt, mẩu xung đột đúng 7/20 còn mẩu không xung đột (trùng chuẩn quốc tế) đúng 9/21 (pilot_summary.md dòng 29–30). (c) Chữ ‘cải thiện rõ’ gắn với 13/20, nhưng trên 20 mẩu xung đột có 9 câu từ sai thành đúng và 3 câu từ đúng thành sai. (d) Chỉ báo so sánh với mồi ở trả lời ngắn (2 so với 0) mà bỏ phần trắc nghiệm có hiện mồi: tiếng Việt 5 so với 4, tiếng Anh 3 so với 4, trên 26 câu (pilot.mcq_a1_*). (e) Mục tiêu ‘truy mỗi lỗi tới một hướng dẫn có tên’ và tiêu đề ‘Sai lệch theo chuẩn nước ngoài và theo phiên bản cũ’ mâu thuẫn với kết luận."
    acceptance: "Kết luận và ô tóm tắt diễn đạt nhãn 5 là ‘không khớp giá trị nào trong tập đối chiếu’, không dùng ‘không có nguồn’. Kết quả có 9/21 ({{pilot.a1_vi_concordant_correct}}/{{pilot.a1_vi_concordant_n}}). Chữ ‘rõ’ bị bỏ, hoặc chỉ gắn với số gộp đã qua registry. Hoặc bỏ hẳn so sánh với mồi, hoặc báo thêm số trắc nghiệm. Mục tiêu đổi thành ‘phân loại mỗi lỗi theo nguồn’. Tiêu đề trung tính, ví dụ ‘Đo và truy nguồn sai lệch… : kết quả thí điểm’."
  - id: 3
    severity: major
    where: "abstract_fmc.md dòng 29/59; registry pilot.adj_*; review/pilot_grading/chunk*_final.jsonl"
    what: "[TRƯỚC KHI NỘP] Các ô kết quả chính cộng không đủ và che lỗi hệ thống của bộ chấm. Ta có 7 + 2 + 7 = 16/20; 4 câu còn lại bộ chấm quy tắc xếp ‘từ chối’, trong khi nhãn trọng tài AI của ô này có 0 câu từ chối (pilot.adj_a1_vi_conflict_abstain = 0). Trên cả 482 câu, 36/41 bất đồng là do bộ chấm gán nhãn 6 cho câu có đưa giá trị: nhãn 6 theo quy tắc là 53 câu, theo trọng tài là 17, tức độ chính xác của nhãn 6 khoảng 32%. Theo nhãn trọng tài: 8/20 đúng, 10 không khớp; khi kèm đoạn thì 16/20 chứ không phải 13/20."
    acceptance: "Abstract nêu 4 câu bộ chấm xếp là từ chối, hoặc thêm một mệnh đề độ nhạy dùng pilot.adj_a1_vi_conflict_correct và pilot.adj_a3_vi_conflict_correct; nói rõ nhãn tham chiếu là của AI. Tổng các thành phần được nêu bằng n."
  - id: 4
    severity: major
    where: "manuscript/build/fmc/abstract_fmc_en.docx; cách hiển thị registry cho tiếng Anh"
    what: "[TRƯỚC KHI NỘP] Bản tiếng Anh vi phạm yêu cầu mỗi file một ngôn ngữ: dòng cơ quan viết tiếng Việt (‘Khoa Công nghệ thông tin, Trường Đại học Tôn Đức Thắng, Việt Nam’). Số thập phân dùng dấu phẩy: ‘91,5%’, ‘kappa 0,87’, ‘35,0%; 95% CI 15,4%–59,2%’."
    acceptance: "unzip -p abstract_fmc_en.docx word/document.xml | grep -cE 'Khoa|Trường|[0-9],[0-9]' trả về 0. Số tiếng Anh vẫn render từ registry (thêm dạng hiển thị EN), không gõ tay."
  - id: 5
    severity: minor
    where: "abstract_fmc.md dòng 25/55 (‘hai kiểm toán viên AI độc lập’, ‘hai người chấm AI độc lập’), dòng 17/47 (‘lịch tiêm’); tên tác giả trong DOCX"
    what: "[TRƯỚC KHI NỘP] Kiểm toán viên A, B và trọng tài đều là Claude (review/pilot_audit/dm_final.md dòng 3), cũng chính là mô hình đã trích mẩu (extraction.agent = claude). Vì vậy ‘độc lập’ là nói quá, và cụm ‘người chấm AI’ dễ gây hiểu nhầm là có người chấm. ‘Lịch tiêm’ không có bằng chứng phân tích, vì các mẩu lịch tiêm bị loại. Tên tác giả chỉ ghi ‘Bình Minh’."
    acceptance: "Câu viết lại: ‘hai lượt kiểm riêng bằng Claude (cùng mô hình đã trích) và một trọng tài AI’. Bỏ ‘lịch tiêm’ khỏi phần đặt vấn đề hoặc ghi là chưa phân tích. Ghi đủ họ tên đúng như hồ sơ nộp. Chạy lại vnsoc.fmc: bản tiếng Việt, tính cả tiêu đề, ≤ 500 từ (hiện là 486)."
  - id: 6
    severity: major
    where: "state/gates/HG1.2_result.md; review/pilot_grading/; kế hoạch M2 (HG3.5–3.7, HG6.2 thay bằng AI)"
    what: "[SAU ABSTRACT, TRƯỚC ĐÓNG BĂNG] Chuẩn tham chiếu hoàn toàn do AI kiểm, lại là cùng mô hình với bên trích mẩu. HG1.2 tìm ra 8/65 lỗi thật và 24/65 chỗ sửa không đổi giá trị: tỉ lệ lỗi trích là 12% mà chưa có người nào kiểm. Tạp chí Q1 sẽ hỏi. Việc chép lại con số, đơn vị, trang và quần thể từ PDF không cần bác sĩ; tác giả tự làm được."
    acceptance: "Có file kiểm tay do tác giả ký tên: toàn bộ mẩu xung đột, hoặc ít nhất 100 mẩu ngẫu nhiên phân tầng, cộng ít nhất 200 nhãn chấm ngẫu nhiên. Báo độ đồng thuận giữa người và AI kèm KTC. Bài báo phân biệt rõ phần người kiểm với phần AI kiểm."
  - id: 7
    severity: major
    where: "bộ chấm grader 1.2.0 → bản dùng cho nghiên cứu chính; docs/DECISIONS.md 2026-09-26T23:45"
    what: "41 lỗi bộ chấm được lấy ra từ chính đầu ra thí điểm. Sửa theo các lỗi đó rồi báo độ chính xác trên thí điểm là tinh chỉnh theo dữ liệu. Nhãn 6 (độ chính xác khoảng 32%) phải được kiểm lại trên đầu ra chưa dùng để sửa."
    acceptance: "Có báo cáo kiểm bộ chấm mới trên đầu ra của một mô hình khác hoặc một tập câu mới, kèm độ chính xác và độ nhạy theo từng nhãn (nhất là nhãn 5 và 6), làm trước khi đóng băng quy tắc chấm."
  - id: 8
    severity: major
    where: "prereg / docs/01_DE_CUONG.md §1.4, §3.6, §5.1"
    what: "Theo tín hiệu thí điểm, H1 và H3 dễ ra kết quả âm tính: H1 là 2/15 nước ngoài so với 0 mồi, còn trắc nghiệm ngang mức mồi; H3 có tỉ lệ nước ngoài hoặc bản cũ ở A3 là 0/20 (VI) và 1/20 (EN). Bỏ mô hình thương mại làm yếu lập luận ‘sinh viên dùng LLM’, trong khi §5.1 tự ghi mô hình API mạnh là ‘loại mô hình sinh viên dùng thật’."
    acceptance: "Bản đăng ký trước có: (a) phân rã nhãn 5 định trước (sai dạng, sai đơn vị hoặc tính toán, giá trị giữa các nguồn, khác); (b) lực kiểm định tính lại từ tỉ lệ thí điểm và cách diễn giải khi kết quả âm tính. Thêm ít nhất một mô hình lớn qua kênh miễn phí trên các mẩu xung đột ở A0/A1; nếu không, ghi rõ phạm vi là ‘mô hình mở chạy cục bộ’ trong câu hỏi nghiên cứu và tiêu đề."
  - id: 9
    severity: minor
    where: "data/interim/pilot_analysis_exclusions.yaml; results/numbers.json design.*"
    what: "(a) P-tbhiv-05 bị loại khỏi trắc nghiệm vì mồi trùng phương án WHO 2014, nhưng vẫn nằm trong tập H1 trả lời ngắn (n = 15). Mồi đã không hợp lệ thì cũng không hợp lệ cho trả lời ngắn. (b) Registry design.pdf_conflicts = 24 và pdf_concordant = 31 đã cũ so với pilot_atoms.jsonl sau HG1.2 (23 và 32). Các số này dùng trong abstract_fmc_design.md."
    acceptance: "Tập H1 thành 14 mẩu, hoặc có ghi chú giải thích vì sao giữ; design_counts chạy lại hoặc khóa được đánh dấu ‘trước HG1.2’."
  - id: 10
    severity: minor
    where: "review/lit/2026-10.md; manuscript/references.yaml"
    what: "Thêm các bài 2025–2026 gần với phát hiện ‘đưa văn bản thì đúng hơn’ mà chưa được trích (xem mục 3). Không trình bày A3 như một đóng góp mới."
    acceptance: "Ba DOI/arXiv ở mục 3 qua scripts/verify_citations.py và được đưa vào phần Related work."
```

## Nhận xét

**1. Đối chiếu số.** Mọi số trong `manuscript/fmc/abstract_fmc.md` khớp `results/numbers.json` và `results/pilot/pilot_summary.md` (65, 13, 7/20, 35,0%, CP 15,4–59,2% — tôi tính lại đúng, 2, 7, 15, 0, 13/20, 19/21, 441/482, κ 0,87). Sai nằm ở câu chữ: "13 hướng dẫn hiện hành" (TT52/2025 hết hiệu lực); "mỗi khuyến cáo có WHO/Mỹ/châu Âu/bản cũ/mồi" (chỉ 11/65 đủ ba hệ, 23/65 có mồi); ô chính cộng 16/20; EN DOCX có dòng tiếng Việt và dấu phẩy thập phân.

**2. Lỗi logic, nói quá.**
- Nhãn 5 là thùng dư. Ghi chú trọng tài: câu sai dạng (P-tbhiv-01..04, dòng đáp án chỉ có số), sai đơn vị (P-controls-07), giá trị ở biên dung sai giữa hai nguồn (P-dm-01: 8,5% giữa BYT 9 và mồi 8), khoảng trộn (P-dengue-02 "5–10" chồng WHO 5–7 và BYT 10), tính liều theo cân sai (P-anaphylaxis-03). "Lỗi chủ yếu là giá trị không có nguồn" không đứng được.
- A1-VI: xung đột 7/20, không xung đột 9/21 (Fisher p ≈ 0,75, tôi tính). Không có dấu hiệu xung đột làm mô hình sai hơn; abstract nêu 19/21 ở A3 nhưng giấu 9/21 ở A1.
- A1→A3 trên 20 mẩu xung đột VI: 9 sai→đúng, 3 đúng→sai (P-anaphylaxis_ocr-01, -05, P-malaria_ocr-03); McNemar chính xác p ≈ 0,15 (tôi tính từ `data/processed/pilot_grades.parquet`, chưa có trong registry). Gộp 61 mẩu thì rõ (25→50).
- Mồi: trả lời ngắn 2 vs 0; trắc nghiệm (mồi hiển thị) VI 5 vs 4, EN 3 vs 4 — chỉ báo phần có lợi là báo cáo chọn lọc.
- "Kiểm toán viên độc lập" đều là Claude, cùng mô hình đã trích mẩu; κ A–B 0,96 không chứng minh độc lập. Bộ chấm gán nhãn 6 thừa (53 vs 17), bị che bởi con số 91,5%.

**3. Bài 2025–2026 gần giống** (DataCite `arxiv.content`, Crossref, PubMed E-utilities):
- Bazerbachi et al. 2026, *Cultural bias in LLMs' ability to follow neuroradiology guidelines*, Eur Radiol, 10.1007/s00330-026-12634-0 — mặc định chuẩn Mỹ dù được yêu cầu chuẩn khác; đưa hướng dẫn khôi phục độ chính xác.
- Siepmann et al. 2025, *The Impact of Access to Clinical Guidelines on LLM-Based Treatment Recommendations for Chronic Hepatitis B*, Liver Int, 10.1111/liv.70324 — trục phiên bản WHO 2015/2024, cùng bệnh; có hướng dẫn thì khớp hơn.
- Zhou Y. et al. 2026, *Knowledge localization…*, Front Oncol, 10.3389/fonc.2026.1808714 — lỗi GPT-5 do theo NCCN thay CSCO.
- Wang & Suresh 2026, arXiv 2606.00333 (chuẩn mặc định theo ngôn ngữ, H2); CPGBench arXiv 2603.25196; Abonizio 2026 arXiv 2605.01077 (benchmark hướng dẫn quốc gia).
- Chưa có trong `review/lit/2026-10.md`: Zhou et al. 2026, *From Guideline Benchmarks to Real-World Discrepancy Adjudication*, SSRN 10.2139/ssrn.6965075 (hướng dẫn quốc gia Trung Quốc, Qwen3/GPT-5 có/không RAG); Gupta et al. 2025, *Locally deployed context-aware chatbot outperforms generic LLMs…*, Pediatr Radiol, 10.1007/s00247-025-06453-6 (mô hình cục bộ + ngữ cảnh); BioPulse-QA, arXiv 2601.12632 (hướng dẫn mới ban hành).

Không bài nào truy nguồn mức giá trị có mồi cho chuẩn quốc gia Đông Nam Á, nên đóng góp chính còn đứng. Nhưng phát hiện duy nhất có tín hiệu (đưa đúng đoạn thì đúng hơn) đã biết; hai điểm mới thật cho tín hiệu gần 0 (H1 2/15 vs 0, trắc nghiệm ngang mồi; H3 0/20). Abstract không tuyên bố "đầu tiên" — giữ vậy.

**4. Đường tới Q1 (một người, laptop).** Tính toán khả thi (482 lượt trong 2 621 s, `docs/DECISIONS.md` 18:25). Ba rủi ro: chuẩn tham chiếu 100% do AI kiểm với tỉ lệ lỗi trích 12% — tác giả tự kiểm chép số–trang được, không cần bác sĩ; không có mô hình thương mại dù §5.1 gọi đó là "loại sinh viên dùng thật"; H1/H3 có thể âm tính — cần đăng ký trước phân rã nhãn 5 và cách diễn giải âm tính.

**Phải sửa trước khi nộp abstract: mục 1–5.** Mục 6–10 sau khi nộp, trước M2.
