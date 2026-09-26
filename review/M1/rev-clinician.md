```yaml
reviewer: rev-clinician (AI mô phỏng bác sĩ nội/truyền nhiễm — KHÔNG phải bác sĩ thật)
milestone: M1
recommendation: major
scores: {importance: 7, novelty: 6, rigor: 4, feasibility: 7, q1_likelihood: 3, fit: 6}
fatal_flaws: []
required_changes:
  - {id: 1, severity: major, where: "manuscript/build/fmc/abstract_fmc.md §PHƯƠNG PHÁP/METHODS; abstract_fmc_vi.docx, abstract_fmc_en.docx", what: "TRƯỚC KHI NỘP. Câu ‘65 khuyến cáo từ 13 hướng dẫn hiện hành’ sai: TT52/2025 đã bị TT13/2026 thay (data/interim/manifest.jsonl, status superseded). 3 mẩu tiêm chủng của nó và P-controls-09 chỉ được mô tả (data/interim/pilot_analysis_exclusions.yaml). Tập được phân tích là 61 mẩu từ 12 văn bản hiện hành, cộng 4 mẩu mô tả.", acceptance: "Hai DOCX không còn gọi một tập có TT52/2025 là ‘hiện hành’; số 61/12 (hoặc cách viết tương đương) lấy từ khóa mới do src/vnsoc/analysis/pilot.py put(); make verify qua."}
  - {id: 2, severity: major, where: "abstract §KẾT QUẢ + ô tóm tắt; data/interim/pilot_atoms.jsonl", what: "TRƯỚC KHI NỘP. Cách viết ‘20 khuyến cáo xung đột với chuẩn nước ngoài … đúng 7’ khiến người đọc hiểu là mô hình biết giá trị riêng của Bộ Y tế. Nhưng ở ít nhất 9/20 mẩu, giá trị Bộ Y tế trùng một giá trị nước ngoài ghi ngay trong mẩu: P-anaphylaxis-03/_ocr-01/_ocr-05 qua DR8 0,01 mg/kg = AAAAI/WAO; P-htn-01/-03 = ESC/WHO 140/90; P-malaria_ocr-01 = WHO 2015; _ocr-04 = CDC 0,5 mg/kg/ngày; _ocr-06 = WHO 3 ngày; P-tbhiv-05 = WHO 2024. Ở ô A1-VI, 5/7 câu ‘đúng’ rơi đúng vào các giá trị này (_ocr-01, _ocr-05, htn-03, malaria_ocr-06, tbhiv-05).", acceptance: "Hai DOCX viết ‘khác ít nhất một hướng dẫn nước ngoài có tên’ và có một vế nói phần lớn câu đúng cũng trùng WHO hoặc nguồn khác. Nếu thêm số (ví dụ số câu đúng trên các mẩu có giá trị Bộ Y tế khác mọi nguồn) thì số đó phải đi qua khóa registry có ghi ‘khám phá’."}
  - {id: 3, severity: major, where: "abstract §PHƯƠNG PHÁP (câu về mồi), §KẾT QUẢ (‘2 so với 0’); pilot_atoms.jsonl decoy/decoy_plausible", what: "TRƯỚC KHI NỘP. §1.2 đề cương yêu cầu mồi ‘hợp lý như nhau’, nhưng decoy_plausible đang là null ở cả 23 mẩu có mồi. Cụ thể: mồi của P-malaria_ocr-01 là pyronaridin–artesunat, thuốc đầu tay của chính 3377/2023 cho người không có thai và bị văn bản này chống chỉ định cho phụ nữ có thai (PL I tr.16). Mồi của P-tbhiv-05 (TDF+3TC+EFV) là một phác đồ có thật. Các mồi 8.500 IU HTIG, 28–32 ml/kg/giờ và AL 1 ngày không phải giá trị lâm sàng. Với n = 15, phép so 2 với 0 không cho thông tin gì; phần trắc nghiệm cho 5 lần trùng nước ngoài so với 4 lần trùng mồi (pilot.mcq_a1_vi_*) nhưng abstract không báo. Câu ‘mỗi khuyến cáo … một giá trị mồi’ cũng sai: chỉ 15/20 mẩu xung đột có mồi.", acceptance: "Abstract bỏ câu ‘2 so với 0’, hoặc báo thêm phép so trắc nghiệm 5/4 qua registry; câu phương pháp đổi thành ‘khi tạo được’. Trước khi đóng băng M2: decoy_plausible được điền cho mọi mẩu có mồi, và check_decoy (có test) bắt được mồi của P-malaria_ocr-01."}
  - {id: 4, severity: major, where: "abstract §KẾT LUẬN; review/pilot_grading/chunk*_final.jsonl", what: "TRƯỚC KHI NỘP. Câu ‘cung cấp đúng văn bản Bộ Y tế cải thiện rõ độ chính xác’ bỏ mất thông điệp an toàn. Dù có đoạn hướng dẫn, bộ chấm vẫn xếp 7/20 câu xung đột là không đúng (phân xử AI: 4/20). Trong đó có hai liều adrenalin thấp 10 lần vì mô hình tự đổi 0,25 ml thành 25 µg và 0,3 ml thành 30 µg (P-anaphylaxis_ocr-01/-05, A3-VI). Chưa làm kiểm định cặp nên chữ ‘rõ’ là nói quá.", acceptance: "Phần kết luận của cả hai bản nói rằng dù có văn bản mô hình vẫn sai, kể cả lỗi đổi đơn vị liều adrenalin; bỏ chữ ‘rõ’, hoặc kèm số cặp bất đồng lấy từ registry."}
  - {id: 5, severity: minor, where: "abstract §KẾT QUẢ", what: "TRƯỚC KHI NỘP. Ô chính chỉ cộng được 7 + 2 + 7 = 16/20. 4 câu còn lại bị bộ chấm xếp là từ chối, nhưng phân xử AI xếp cả 4 là có giá trị (pilot.adj_a1_vi_conflict_abstain = 0, correct = 8, unattributed = 10). Ở các ô xung đột, bộ chấm khớp nhãn phân xử 16/20 (A1) và 17/20 (A3), thấp hơn mức 91,5% tính trên toàn bộ.", acceptance: "Abstract nói rõ 4 câu còn lại, hoặc đưa số theo nhãn phân xử, qua khóa pilot.adj_*."}
  - {id: 6, severity: minor, where: "manuscript/build/fmc/abstract_fmc_en.docx", what: "TRƯỚC KHI NỘP. Bản EN còn một dòng tiếng Việt ‘Khoa Công nghệ thông tin, Trường Đại học Tôn Đức Thắng, Việt Nam’, trái yêu cầu mỗi file một ngôn ngữ (DECISIONS 2026-09-26T20:40). Số thập phân trong bản EN vẫn dùng dấu phẩy (91,5%; 35,0%; 15,4%–59,2%).", acceptance: "Bản EN ghi ‘Faculty of Information Technology, Ton Duc Thang University, Vietnam’ và dùng dấu chấm thập phân (dựng bản EN riêng từ registry)."}
  - {id: 7, severity: minor, where: "abstract, tiêu đề và §KẾT QUẢ", what: "TRƯỚC KHI NỘP. Tiêu đề nói tới ‘sai lệch theo phiên bản cũ’ nhưng phần kết quả không có số nào về việc này, trong khi registry đã có pilot.a1_vi_drift_stale = 3/20.", acceptance: "Thêm một vế kết quả về lệch phiên bản lấy từ registry, hoặc bỏ ý đó khỏi tiêu đề."}
  - {id: 8, severity: minor, where: "abstract §PHƯƠNG PHÁP", what: "TRƯỚC KHI NỘP. Abstract ghi ‘hai kiểm toán viên/người chấm AI độc lập’, nhưng cả hai đều là Claude (review/pilot_audit/*_final.md: ‘Người kiểm: AI (Claude)’), cùng họ mô hình đã trích mẩu và viết bộ chấm, nên không độc lập.", acceptance: "Cả hai bản đổi thành ‘hai lượt kiểm bằng AI cùng họ mô hình, có trọng tài’."}
  - {id: 9, severity: major, where: "pilot_atoms.jsonl foreign[].version_date; prereg H1", what: "Nhiều giá trị nước ngoài dùng để đối chiếu ra đời sau khi Qwen3 phát hành (4/2025): CDC AL 5 ngày, 2026-08-11 (P-malaria_ocr-06); CDC nPEP, 2025-05-08 (P-tbhiv-05); WHO metamizol, 2025-07 (P-dengue-04, là một trong 2 lần ‘trùng nước ngoài’); AHA/ACC, 2025-08-14 (P-htn-03). Mô hình không thể ‘mặc định theo’ một giá trị công bố sau ngày cắt dữ liệu của nó, nên câu ‘truy mỗi lỗi tới hướng dẫn có tên’ lúc này chỉ là trùng hợp. Bảng CDC còn dành cho một quần thể khác: người Mỹ đi về từ vùng dịch.", acceptance: "Mỗi giá trị nước ngoài có trường value_first_published (ngày giá trị xuất hiện lần đầu, không phải ngày của bản tài liệu) và cờ ‘cùng quần thể’. H1 và phần truy nguồn chỉ tính các giá trị có trước ngày cắt dữ liệu của từng mô hình; phần còn lại đưa vào độ nhạy. Ghi vào prereg trước HG2.9."}
  - {id: 10, severity: major, where: "định nghĩa conflict_status; P-malaria_ocr-01, P-anaphylaxis-*", what: "Có câu hai đáp án cùng đúng. 3377/2023 tr.10 cho dùng artemether–lumefantrin khi không có quinin. Vì vậy lần ‘trùng nước ngoài’ thứ hai ở ô A1-VI (Coartem) là phương án Bộ Y tế cho phép, lại được WHO/CDC ưu tiên, nên về lâm sàng không phải lỗi. Tập DR8 của phản vệ (60–333 µg cho trẻ 6 kg) tự nó đã chênh 5,5 lần, nên phần ‘xung đột’ chỉ còn lại với RCUK/WHO 150 µg.", acceptance: "Trước khi đóng băng: chia tầng ‘xung đột riêng’ (giá trị Bộ Y tế khác mọi giá trị nước ngoài) và ‘xung đột một phần’. Phương án thay thế có điều kiện được lưu riêng (allowed_alternative) và không nhận nhãn 4. Có phân tích độ nhạy cho P-malaria_ocr-01 khi đưa AL vào tập Bộ Y tế."}
  - {id: 11, severity: major, where: "vnsoc.qgen (đơn vị trong câu hỏi); vnsoc.grade nhãn 5", what: "Câu hỏi ép một đơn vị khác với văn bản (hỏi µg trong khi TT51 ghi ml của ống 1 mg/ml). Điều đó sinh ra lỗi quy đổi không phản ánh kiến thức hướng dẫn: 0,06/0,1/0,6/10/20/25/30 µg. Nhãn 5 lại gộp các lỗi nguy hiểm (primaquin 12 mg/kg/ngày, gấp 24 lần, ở P-malaria_ocr-04; HRZES cho lao tiền siêu kháng ở P-tbhiv-01; adrenalin 0,6 µg) chung với các khoảng chỉ chồng một phần (10–20 ml/kg/giờ khi Bộ Y tế là 15).", acceptance: "Câu hỏi dùng đơn vị gốc của văn bản hoặc chấp nhận cả hai đơn vị. Bộ chấm ghi nhãn phụ cho nhãn 5 (lỗi quy đổi/độ lớn ≥ 10 lần; chồng một phần; giá trị của bối cảnh lân cận) và tính tỉ số lệch so với Bộ Y tế làm biến thay thế cho tác hại. Việc này không cần bác sĩ và hợp với DR12."}
  - {id: 12, severity: major, where: "state/gates/HG1.2_result.md; pilot_atoms.jsonl context_checked, span", what: "Cả chuỗi trích mẩu, kiểm, chấm và phân xử đều do Claude làm. Trường context_checked vẫn là ‘pending’ ở cả 65 mẩu, dù tiêu chí (c) về quần thể có mức đồng thuận thấp nhất (61/65). Span của P-malaria_ocr-03 ghi ‘> 15 tuổi’, trong khi ảnh trang 3377/2023 tr.16 ghi ‘≥ 15 tuổi’.", acceptance: "Tác giả tự so câu nguyên văn và con số với ảnh trang PDF (việc này không cần chuyên môn lâm sàng): 100% mẩu thí điểm và ít nhất 10% mẫu ngẫu nhiên của bộ chính. Lưu file kết quả và đưa tỉ lệ sai vào registry; cập nhật context_checked."}
```

**Lưu ý:** Tôi là AI đóng vai bác sĩ nội/truyền nhiễm, KHÔNG phải bác sĩ thật. Đừng trích nhận xét này như ý kiến “bác sĩ đã duyệt”.

### 1. Đối chiếu từng con số trong abstract
Mọi số trong hai DOCX khớp `results/numbers.json` và `results/pilot/pilot_summary.md` (65; 13; 482; 441/482 = 91,5%; kappa 0,87; A1-VI xung đột 7/20, 35,0%, 15,4–59,2%, nước ngoài 2, không nguồn 7; mồi 2 so với 0 trên 15; A3 13/20 và 19/21). Độ dài: VI 486 từ, EN 364 từ; ô tóm tắt 351/402 ký tự. Không có số bịa; lỗi nằm ở diễn giải (id 1–8).

### 2. Đối chiếu PDF gốc (12 mẩu, 7 văn bản)
- 5642/2015 tr.29: HTIG 3000–6000 đơn vị. Khớp.
- 5481/2020 tr.25 “A1C ≥9%”, tr.12 “từ 45 tuổi”. Khớp.
- TT51/2017 tr.9 (ảnh trang): 0,2/0,25/0,3/0,5 ml. Khớp anaphylaxis-03, _ocr-01, _ocr-05.
- 3377/2023 tr.10, 16 (đọc ảnh), 17, 19: quinin + clindamycin (được dùng AL khi không có quinin); 4 viên × 7,5 mg; 0,5 mg/kg/ngày × 7 ngày; AL 3 ngày. Giá trị khớp, riêng span _ocr-03 có lỗi OCR (“>” thay cho “≥”).
- 162/2024 tr.44: 2HRZE/4RHE cho người lớn, 4RH cho trẻ em. Khớp.
- 2760/2023 tr.28: 15 ml/kg/giờ rồi 10 ml/kg/giờ. Khớp.
- 3192/2010 tr.1: ≥140/90; cùng bảng có 130/80 cho Holter, nên trả lời 130/80 có thể do nhầm cách đo, chưa chắc do chuẩn Mỹ.

Phía Bộ Y tế được chép đúng. Chỗ yếu nằm ở phía đối chiếu nước ngoài.

### 3. Tập “xung đột” không sạch như abstract ngụ ý
Định nghĩa trong §1.2 cho phép gọi một mẩu là xung đột chỉ cần một nguồn nước ngoài khác Bộ Y tế. Nhưng ở ≥ 9/20 mẩu, giá trị Bộ Y tế cũng chính là giá trị của WHO/ESC/CDC. Trong 7 câu “đúng”, 5 câu rơi đúng vào các giá trị này. Chỉ P-dm-03 và P-malaria_ocr-03 là đúng một giá trị riêng của Việt Nam.

Cả hai lần “trùng nước ngoài” cũng đều yếu:
- Coartem cho thai 3 tháng đầu là phương án 3377/2023 cho phép.
- Metamizol chỉ được đối chiếu với WHO 2025-07, tức sau khi Qwen3 ra đời. Nguồn thật có thể là thực hành ở Mỹ Latinh hoặc châu Âu.

Vì vậy kết luận “lỗi chủ yếu là giá trị không có nguồn” đi đúng hướng, nhưng việc *truy nguồn* thì chưa được chứng minh.

### 4. Mồi
Không mồi nào đã được kiểm độ hợp lý. Pyramax cho thai 3 tháng đầu là thuốc mà chính văn bản Bộ Y tế chống chỉ định. Trả lời Pyramax là một lỗi bối cảnh có hại, không phải trùng ngẫu nhiên. Các mồi 8.500 IU, 28–32 ml/kg/giờ, AL 1 ngày gần như không ai nói ra, nên kết quả “0 lần trùng mồi” gần như chắc chắn sẵn. Ở phần trắc nghiệm, nơi mồi hiện ra ngang hàng với các phương án khác, tỉ số là 5 trùng nước ngoài so với 4 trùng mồi.

### 5. Tác hại và giá trị cho đào tạo
Nhãn 5 đang gộp những lỗi rất khác nhau:
- Adrenalin 0,6 µg cho trẻ 6 kg (thấp hơn 300 lần).
- Primaquin 12 mg/kg/ngày (gấp 24 lần).
- HRZES cho lao tiền siêu kháng.
- Và cả các khoảng chỉ chồng một phần.

Ở A3, hai lỗi còn lại là liều adrenalin thấp 10 lần do mô hình tự đổi ml sang µg. Một phần lỗi này do câu hỏi ép đơn vị µg. Thông điệp nên dạy là: có văn bản trong tay mà mô hình vẫn sai liều. Không nên dạy rằng kèm văn bản là đủ. Ngược lại, gọi Coartem cho thai 3 tháng đầu là “lỗi” sẽ dạy sai cho sinh viên.

### 6. Đường tới bài Q1 với một người và một laptop
Tính toán khả thi (482 lượt, 2 621 s). Rủi ro lớn nhất với JMIR MI/IJMI là Claude kiểm Claude và chưa có người thật nào kiểm.

Các cách vừa rẻ vừa trong tầm tay:
- Tác giả tự so nguyên văn và con số với ảnh trang (id 12).
- Trình bày bài như một cuộc kiểm toán mức trung thành với văn bản, không phải đánh giá đúng/sai lâm sàng.
- Dùng tỉ số lệch liều làm biến thay thế cho tác hại.
- Chỉ tính “trùng nước ngoài” với các giá trị có trước ngày cắt dữ liệu của mô hình.

Thiếu id 2, 3, 9, 10 trước đóng băng M2, H1 sẽ không đứng vững trước phản biện lâm sàng.

**Trước khi nộp (hạn 30/9):** id 1–8 — sửa câu chữ và vài khóa registry, làm được trong một ngày.
