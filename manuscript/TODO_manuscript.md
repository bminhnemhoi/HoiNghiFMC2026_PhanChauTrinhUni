# TODO cho bản thảo tạp chí (manuscript/main.md)

Tạo trong task C4.8. File này nằm trong manuscript/ nên cũng bị `vnsoc.numbers verify` quét: mọi con số và mọi tên khóa đều đặt trong khối mã (```), không viết dấu ngoặc nhọn kép ngoài khối mã.

Trạng thái: bản khung. Methods, Introduction, Limitations viết xong bằng văn xuôi theo bản đăng ký hiện tại (prereg/osf_preregistration.md, bản sửa gần nhất, còn các mục D18–D26 chờ tác giả xác nhận). Results, Abstract (phần kết quả) và phần lớn Discussion là mẫu câu có khóa registry, chờ dữ liệu. Chưa có bác sĩ nào duyệt; bài không được viết là có bác sĩ duyệt.

## 1. Khóa registry mới cần mã phân tích tạo (cho statistician)

Quy ước (giữ như registry hiện có):
- Giá trị ghi bằng `vnsoc.numbers.put()` từ `src/vnsoc/analysis/`, `analysis_R/` hoặc `scripts/analysis/`.
- `display` theo định dạng tiếng Việt (dấu phẩy thập phân, dấu chấm hàng nghìn); main.md gọi mọi khóa số với hậu tố `|en` để in kiểu tiếng Anh.
- Khóa `*_ci`: đề nghị display chỉ là khoảng "a–b" (không kèm chữ KTC và mức tin cậy), câu văn tự thêm; hiện main.md đặt khóa `*_ci` trong ngoặc sau ước lượng, không có chữ "CI" đứng trước — statistician chọn một cách và báo lại để sửa câu.
- Khóa `*_text` là chuỗi tiếng Anh (không dùng `|en`), ví dụ "supported" / "not supported"; "robust" / "not robust"; tên các lát cắt DR6 đã áp dụng.
- Khóa `*_min` / `*_max` là min/max qua các mô hình (hoặc tầng) kèm tên mô hình trong `note`.

```text
# design.* — hằng số ĐÃ ĐĂNG KÝ nhưng KHÔNG có trong configs/*.yaml (không sửa configs: đã băm trong prereg §5.0).
# Đề xuất: src/vnsoc/analysis/design_counts.py put() kèm note trích mục prereg.
design.alpha_one_sided        mức một phía của mọi kiểm định xác nhận (prereg §5.1.6)          0,025
design.bootstrap_b            số lần lặp bootstrap B (prereg §5.1.1)                           10.000
design.ci_pct                 mức KTC hai phía, lấy từ configs hypotheses.ci_level              95%
design.small_cluster_min      ngưỡng "ít cụm" (C < 20: jackknife-t / sign-flip) (prereg §5.1.1, §5.1.3)   20
design.gv_atoms_per_stratum   số mẩu mỗi tầng ở kiểm bộ chấm giữ riêng (prereg §3.1 mục 7)      20
design.gv_responses_approx    số câu trả lời xấp xỉ của kiểm bộ chấm giữ riêng                  240
design.gv_acc_min             ngưỡng độ chính xác chấp nhận bộ chấm                             0,90
design.gv_lcl_min             ngưỡng cận dưới KTC design-effect CP                              0,85
design.label1_check_n         số câu nhãn 1 được kiểm (prereg §3.1 mục 7)                       200
design.mcq_max_tokens         max token trắc nghiệm (Addendum 1 C5; chờ D26)                    384
design.num_ctx                cửa sổ ngữ cảnh A0–A3 trên Ollama (chờ D26)                       4.096
design.run_valid_min_pct      ngưỡng hoàn tất ô chạy (prereg §3.1 mục 6)                        98%
design.dr6_hours              ngưỡng giờ laptop kích hoạt DR6                                   80
compute.sec_per_request       thông lượng đo 27/9 (review/M1/R1.3_compute.md), qwen3 num_ctx 4096   ~4,9

# pilot.* — MỚI, tính được NGAY từ file có sẵn (thí điểm, grader 1.2.0). Đề xuất: src/vnsoc/analysis/pilot.py
pilot.audit_confirmed         số mẩu kiểm toán trích dẫn AI xác nhận (review/pilot_audit/pilot_final.jsonl; Addendum 1 ghi 33)
pilot.audit_corrected         số mẩu sửa nhưng không đổi giá trị (Addendum 1 ghi 24)
pilot.audit_errors            số mẩu có lỗi thật (Addendum 1 ghi 8)
pilot.rule_label6_n           số câu bộ chấm quy tắc gán nhãn 6 (review/M1: 53)
pilot.adj_label6_n            số câu nhãn 6 sau trọng tài AI (review/M1: 17)
pilot.grader_err_conflict_pct tỉ lệ lỗi bộ chấm ở ô mẩu xung đột (rev-methods: 22/120)
pilot.grader_err_concordant_pct tỉ lệ lỗi bộ chấm ở ô mẩu đối chứng (rev-methods: 5/126)
pilot.decoy_plausible         số mồi thí điểm được AI chấm hợp lý (review/decoy_plausibility/pilot_final.md: 9)
pilot.decoy_rated             số mẩu thí điểm có mồi được chấm (23)
pilot.mcq_truncated           số đầu ra trắc nghiệm chạm trần 128 token (R1.3: 53)
pilot.mcq_total               tổng đầu ra trắc nghiệm thí điểm (92)
# Các số trong ngoặc chỉ để đối chiếu; mã phải tự đếm lại từ file, không chép tay.

# corpus.*  (sau đóng băng kho 15/10; nguồn: manifest + corpus_triage.csv + supersession table)
corpus.n_catalogued  corpus.n_catalogued_current  corpus.n_current  corpus.n_ocr
corpus.n_superseded  corpus.n_chains  corpus.n_partial_amendments

# atoms.*  (sau đóng băng mẩu; vnsoc.match.atom_flags)
atoms.n_total  atoms.n_conflict  atoms.n_families  atoms.n_families_multi_guideline
atoms.n_concordant  atoms.n_no_counterpart  atoms.n_indistinguishable  atoms.n_drift
atoms.n_conflict_decoy  atoms.n_conflict_no_decoy  atoms.n_us_unique  atoms.n_dr8
atoms.n_pilot  atoms.h1_share_pilot (tỉ lệ đơn vị H1 đến từ mẩu thí điểm)  atoms.n_gv (mẩu kiểm bộ chấm)

# questions.*  (sau đóng băng câu hỏi; bảng QC)
questions.n_short (mỗi ngôn ngữ)  questions.n_mcq  questions.n_removed  questions.n_removed_ambiguity
questions.n_translation_edited

# qc.*  (chất lượng dữ liệu; kiểm toán AI + kiểm bằng mã)
qc.extraction_precision  qc.extraction_precision_ci  qc.dr1_text
qc.false_conflicts  qc.false_conflict_ucl (cận trên một phía CP)
qc.matching_precision  qc.matching_precision_ci  qc.matching_sensitivity  qc.matching_sensitivity_ci
qc.audit_agree_pct  qc.audit_kappa (hai lượt AI trước trọng tài, kiểm bối cảnh mẩu xung đột)
qc.code_span_ok_pct  qc.code_values_ok_pct  qc.code_ai_agree_pct (vnsoc.analysis.independent_check)
qc.decoy_plausible_pct  qc.decoy_regenerated

# coauthor.*  (CHỈ khi hai đồng tác giả sinh viên thực sự kiểm; bảng tính có seed)
coauthor.atoms_n  coauthor.atoms_agree_pct  coauthor.atoms_agree_ci
coauthor.labels_n  coauthor.labels_agree_pct  coauthor.labels_kappa  coauthor.vignettes_n

# grader.*
grader.version_frozen (chuỗi, vd "1.3.0")  grader.gv_n_responses  grader.gv_n_atoms
grader.gv_accuracy  grader.gv_accuracy_ci  grader.gv_decision_text
grader.extractor_err_pct  grader.extractor_err_ci  grader.needs_llm_max_pct  grader.dr9_text
grader.label1_precision_min  grader.label1_precision_max  grader.label6_precision  grader.label6_recall

# runs.*
runs.n_models  runs.n_requests  runs.laptop_hours  runs.valid_min_pct  runs.ollama_version (chuỗi)
runs.answer_line_min_pct  runs.answer_line_max_pct  runs.truncated_min_pct  runs.truncated_max_pct
runs.dr6_text  runs.dr10_dr11_text

# rq1.*  (A1 mô tả; trắc nghiệm; A0 khám phá)
rq1.a1_vi_concordant_pct  rq1.a1_vi_l3_pct  rq1.a1_vi_l4_pct  rq1.a1_vi_l5_pct  rq1.a1_vi_l6_pct
rq1.a1_l1_pct  rq1.a1_vi_control_correct_pct (mẩu concordant ở A1)
rq1.mcq_delta  rq1.mcq_delta_ci  rq1.mcq_order_agree_pct
rq1.a0_us_en_pct  rq1.a0_us_vi_pct  rq1.a0_ask_country_pct

# h1.*  (confirmatory.h1_delta, h1_robustness, tipping_point_h1; tỉ lệ quy nguồn C7)
h1.n_responses  h1.n_atoms  h1.n_families  h1.pi_f  h1.pi_f_ci  h1.pi_d  h1.pi_d_ci  h1.pi_d_unweighted
h1.delta  h1.delta_ci  h1.p  h1.decision_text  h1.excess  h1.excess_ci  h1.sesoi_text
h1.systems_text  h1.delta_model_min  h1.delta_model_max
h1.as  h1.as_ci  h1.as_c  h1.as_c_ci  h1.unattributed_share  h1.decoy_share_l5  h1.n_nonconcordant
h1.s1_delta_ci  h1.s2_delta_ci  h1.s3_delta_ci  h1.n1_delta_ci  h1.robust_text
h1.b1_n  h1.b1_delta  h1.b1_delta_ci  h1.b26_n  h1.b26_delta  h1.b26_delta_ci
h1.b10_delta_ci  h1.b11_delta_ci  h1.l4_not_knowable  h1.tipping_point  h1.false_conflicts_plausible

# h2.*
h2.n_atoms  h2.n_pairs  h2.n_discordant_families  h2.rate_en  h2.rate_vi  h2.diff  h2.diff_ci
h2.test_text (Durkalski hay sign-flip)  h2.p  h2.p_holm  h2.decision_text

# h3.*  (mỗi mô hình local_main: qwen3_8b, sailor2_8b, vistral_7b, llama31_8b)
h3.r_qwen3_8b  h3.r_qwen3_8b_ci  h3.r_sailor2_8b  h3.r_sailor2_8b_ci  h3.r_vistral_7b  h3.r_vistral_7b_ci
h3.r_llama31_8b  h3.r_llama31_8b_ci  h3.r_min  h3.r_max  h3.n_responses
h3.p_pc  h3.p_holm  h3.decision_text  h3.n_models_lcl_above
h3.b22_min  h3.b22_max  h3.b1_range  h3.b26_range

# rq2.*
rq2.l34_a0_pct  rq2.l34_a1_pct  rq2.l34_a2_pct  rq2.l34_a3_pct  rq2.l34_a4_pct
rq2.stubborn_pct  rq2.stubborn_ci  rq2.recall_pct  rq2.retrieval_err_share  rq2.incontext_err_share  rq2.dr3_text
rq2.recall_<model>  rq2.retrieval_err_<model>  rq2.incontext_err_<model>   (4 mô hình, như h3)

# drift.*  (khám phá)
drift.n_atoms  drift.l3_a1_pct  drift.model_text  drift.latest_bias  drift.latest_bias_ci

# h4.*
h4.n_answers  h4.disagree_share  h4.rr_mh  h4.rr_ci  h4.p  h4.p_holm  h4.rr_crude  h4.decision_text

# rq3.*  (c050 = mức phủ 0,5)
rq3.u_disagree_c050_min  rq3.u_disagree_c050_max  rq3.u_agree_c050_min  rq3.u_agree_c050_max
rq3.ltt_cov_disagree_min  rq3.ltt_cov_disagree_max  rq3.dr4_text  rq3.dr5_text
rq3.self_abstain_min  rq3.self_abstain_max  rq3.regime_a_violation
rq3.regime_b_bound_violation_min  rq3.regime_b_bound_violation_max
rq3.regime_b_ltt_violation_min  rq3.regime_b_ltt_violation_max  rq3.regime_b_text

# rq4.*  (chỉ khi ánh xạ khung vấn đề cốt lõi xong)
rq4.n_problems_covered  rq4.summary_text  rq4.a6_a1_agree_pct  rq4.a6_a1_kappa
```

Khóa registry hiện có được dùng lại (không cần làm gì): `design.seed_rows` và các khóa `pilot.*` của thí điểm (n_atoms, n_atoms_analysed, n_guidelines, n_guidelines_analysed, grader_n, grader_short_*, indep_*, a1_vi_conflict_*, a1_vi_concordant_*, a1_vi_h1_foreign, a1_vi_decoy, a1_vi_drift_*, a3_vi_conflict_*, a3_vi_foreign_or_stale, a1a3_vi_conflict_*, adj_a1_vi_conflict_correct, mcq_a1_vi_*, n_conflict_h1_atoms, ci_level).

## 2. Trích dẫn còn thiếu (TODO-CITE trong main.md)

Không tự thêm vào references.yaml khi chưa tra được bản ghi. Các mục có DOI dưới đây được bản đăng ký (prereg §6.11) ghi là đã tra Crossref, nhưng CHƯA có trong manuscript/references.yaml → lit-scout thêm, chạy `scripts/verify_citations.py`, rồi thay TODO-CITE bằng khóa.

```text
Thống kê (có trong prereg §6.11):
  Clopper & Pearson 1934, Biometrika                        doi:10.1093/biomet/26.4.404
  Efron 1987, J Am Stat Assoc (BCa)                          doi:10.1080/01621459.1987.10478410
  Field & Welsh 2007, J R Stat Soc B (cluster bootstrap)     doi:10.1111/j.1467-9868.2007.00593.x
  Cameron, Gelbach & Miller 2008, Rev Econ Stat              doi:10.1162/rest.90.3.414
  MacKinnon & Webb 2017, J Appl Econ                         doi:10.1002/jae.2508
  Durkalski et al 2003, Stat Med (clustered McNemar)         doi:10.1002/sim.1438
  Benjamini & Heller 2008, Biometrics (partial conjunction)  doi:10.1111/j.1541-0420.2007.00984.x
  Bates et al 2015, J Stat Softw (lme4)                      doi:10.18637/jss.v067.i01
  Brooks et al 2017, R J (glmmTMB)                           doi:10.32614/RJ-2017-066
  Pustejovsky & Tipton 2018, J Bus Econ Stat                 doi:10.1080/07350015.2016.1247004
  Korn & Graubard 1998, Survey Methodology — KHÔNG có DOI (Statistics Canada 12-001-X19980024356) → người kiểm (HG7.3)
  Holm 1979, Scand J Stat — KHÔNG có DOI → người đối chiếu bản gốc (prereg D11)
Chưa có bản ghi nào trong dự án (phải tra mới, không đoán):
  Ước lượng tỉ số nguy cơ Mantel–Haenszel (chọn một tài liệu chuẩn và tra)
  Zeileis, Köll & Graham 2020 (gói sandwich) — prereg §5.1.8 nêu tên nhưng không có trong §6.11
  BAAI/bge-m3 (bài hoặc model card)
  Model card / báo cáo kỹ thuật: Qwen3-8B (HF model card; configs ghi arXiv 2505.09388), Llama-3.1-8B-Instruct (HF model card),
    Sailor2-8B-Chat (blog sea-sailor.github.io/blog/sailor2), Vistral-7B-Chat (HF model card), Gemma nếu chạy
  Ollama, llama.cpp (phần mềm; trích URL + phiên bản)
Văn bản Bộ Y tế (lấy từ manifest kho, người kiểm HG7.3; KHÔNG thuộc references.yaml theo quy ước hiện tại):
  QĐ 1740/QĐ-BYT (2026), 3310/QĐ-BYT (2019), 2760/QĐ-BYT (2023), 3705/QĐ-BYT (2019), 162/QĐ-BYT (2024), 2760/QĐ-BYT (2021),
  2131/QĐ-BYT (2026), 2147/QĐ-BYT (2026); các QĐ về đái tháo đường/tăng huyết áp dùng cho ví dụ huyết áp ở Introduction
  → quyết định cách trích (danh mục riêng hay references.yaml với checked_by_human)
```

Trích dẫn đã dùng: mọi khóa trong main.md đều có trong references.yaml, tất cả trạng thái `ok` trong manuscript/citations_verified.json. Lưu ý trước khi nộp:

```text
- Bản thảo chưa bình duyệt (arXiv / Preprints.org), nên ghi rõ trong danh mục tài liệu:
  abonizio2026brazilian angelopoulos2022crc duwal2025mka guan2026temporal gurram2026selective harris2025pubhealthbench
  liu2026certified mutisya2025alama nguyen2025vm14k nguyen2026vihermes noonan2026exceedance prior2026oldfriend
  salem2026hgcrc tan2026cpgbench wang2026jurisdictional wong2026implicit wu2024clasheval xie2023chameleon
  yu2026outdated zhou2026falsesense
- xie2023chameleon: ghi chú arXiv là ICLR 2024 → tra bản xuất bản nếu có; wu2024clasheval, angelopoulos2022crc: nơi đăng chính thức chưa kiểm.
- Mọi mô tả kết quả của bài khác trong Introduction/Discussion là định tính (không có số). Trước khi nộp, đối chiếu lại với bản gốc:
  bazerbachi2026cultural (dùng toàn văn, không dùng tóm tắt), siepmann2025hepatitisb, zhou2026localization,
  wang2026jurisdictional (tỉ lệ Mỹ chỉ cao ở điều kiện buộc một đáp án), bui2026kap (không nêu tên công cụ),
  ada2025cvd (mục tiêu huyết áp so với QĐ Bộ Y tế — kiểm đúng quần thể), guan2026temporal (cách diễn đạt "poorly aware").
- 7 mục chỉ có URL (who2022drtb ... cdc2025childschedule) đang needs_human_check; main.md hiện không trích mục nào trong số này.
```

## 3. Phần chờ dữ liệu

```text
Abstract          Results, Conclusions (chọn phương án A/B sau phân tích xác nhận; câu A3)
Methods           [TODO] ai kiểm lại chuỗi thay thế; ai kiểm câu tình huống; đoạn kiểm mẫu của đồng tác giả (chỉ giữ nếu làm xong,
                  ghi tình trạng đăng ký: addendum trước đóng băng mẩu hay "không đăng ký, khám phá"); ngày nộp OSF + DOI;
                  grader_version đóng băng; DR6/DR10/DR11 đã áp dụng; giá trị design.* chờ D26 (num_ctx, max token trắc nghiệm)
Results           toàn bộ (sau đóng băng 15/10, chạy chính 12/11–2/12, chấm, phân tích xác nhận bằng mã)
Tables            T1 kho hướng dẫn, T2 mô hình: mã sinh bảng (results/tables) — chưa có script; T3, T4: khóa như trên
Figures           F1 quy trình, F2 quy nguồn A1 (nhãn 1–6 + vạch mồi), F3 bậc thang A0→A4, F4 lệch phiên bản theo tháng,
                  F5 cận chứng nhận RQ3 — chưa có script (results/figures, PDF + PNG)
Discussion        Principal Findings (chọn A/B, và các nhánh E thực tế/không kết luận, "H1 robust"), Comparison (các câu [result-dependent]),
                  Implications (chèn số A1/A3), Limitations (nhánh đồng tác giả có/không; DR2/DR6), Conclusions (A/B)
Supplements       S1 danh mục + chuỗi thay thế; S2 quy tắc trích, rubric, mồi, QC; S3 prompt; S4 quy tắc chấm + kiểm bộ chấm/bộ tách;
                  S5 đặc tả thống kê đầy đủ + mô phỏng + độ nhạy + khám phá; S6 checklist TRIPOD-LLM; S7 thí điểm đầy đủ (VI+EN);
                  S8 dòng thời gian đăng ký trước, Addendum 1 (C1–C12), các lệch sau đó
Pilot khóa mới    tính được ngay (mục 1) — nên làm trước để giảm số placeholder thiếu
```

## 4. Việc của tác giả trước khi nộp (không ai làm thay được)

```text
- Chọn tiêu đề: giữ tiêu đề đã đăng ký hay dùng tiêu đề nêu rõ phạm vi (mô hình mở chạy cục bộ) — quyết TRƯỚC khi chạy chính.
- prereg/osf_preregistration.md §0 vẫn ghi "sole author ... no co-author or clinician" — trái với DECISIONS 2026-09-27T10:30
  (có hai đồng tác giả sinh viên). Sửa trước khi nộp OSF (HG2.9), và quyết việc kiểm mẫu của đồng tác giả có đưa vào đăng ký không.
- Thống nhất thứ tự họ–tên cả ba tác giả; ORCID; địa chỉ bưu chính; email tác giả 2 (pctu.edu.com hay .vn).
- CRediT: ba tác giả xác nhận vai trò thật (hiện là đề xuất trong state/gates/coauthor_roles.md).
- Xung đột lợi ích, tài trợ: mỗi tác giả xác nhận.
- Đạo đức: xác nhận trường có yêu cầu văn bản miễn xét duyệt hay không (HG1.10 đã không làm).
- Công bố dùng AI: điền định danh mô hình Claude và thời gian dùng từ nhật ký.
- Kho dữ liệu công khai + DOI lưu trữ; DOI OSF.
```

## 5. Ghi chú kỹ thuật

```text
- Nhãn trả lời viết là L1–L6 trong bài (tránh số trần); phương trình đặt trong khối ```math (bị verify bỏ qua) — khi dàn trang đổi sang
  công thức thật.
- Hằng số thiết kế dùng dạng {{=…}} chỉ khi đúng tham số đó có trong configs (vd 400, 25, 0,10, 0,05, 2,0, 0,95, seed 20261001).
  Các hằng số không có trong configs dùng khóa design.* ở mục 1 (không dùng trùng số ngẫu nhiên trong configs).
- make verify sẽ báo LỖI cho tới khi mọi khóa ở mục 1 có trong registry — đây là dự kiến ở giai đoạn khung.
- Bảng nhãn L1–L6 ở Methods chưa đánh số (JMIR: đặt thành Textbox khi dàn trang); Bảng 1–4 và Hình 1–5 đã được trích theo thứ tự.
- Tài liệu tham khảo: pandoc + CSL AMA (JMIR) từ references.yaml khi dựng bản nộp (T8.1).
```
