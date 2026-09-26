# T1.1 thí điểm — Kiểm toán độc lập chủ đề Lao (kể cả lao kháng thuốc) và HIV (ID = tbhiv)

Ngày: 2026-09-26 · Người kiểm: integrity-auditor (Claude), kiêm góc nhìn bác sĩ lâm sàng Việt Nam **do AI đóng vai, không phải bác sĩ thật**
Đầu vào: `data/interim/pilot/tbhiv.jsonl` (7 mẩu, ghi lúc 11:15), `data/interim/pilot/tbhiv_report.md` (11:18)
Nguyên tắc: không tin báo cáo, tự kiểm bằng công cụ. File này chỉ ghi kết quả kiểm; **không sửa** mẩu, config hay mã.

## Kết luận ngắn

- **Phán quyết:** pass = 2 (06, 07); fix = 5 (01, 02, 03, 04, 05); reject = 0.
- **Giá trị Bộ Y tế: cả 7 mẩu đều đúng.** Tôi đã đọc lại từng trang PDF, và từng span nằm đúng trang ghi.
- **Giá trị nước ngoài: đều có trong nguồn đã băm, đúng phiên bản và ngày.** Riêng nguồn Mỹ của mẩu 03 chưa có mã băm.
- **Trạng thái do `finalize()` tính: tính lại bằng mã hiện hành vẫn cho kết quả y hệt.**
- Tuy vậy có **4 vấn đề lớn** mà báo cáo chưa nêu, hoặc nêu nhưng chưa kiểm:
  1. **Bộ chấm không đọc được đáp án điển hình.** Các dạng "BPaL", "BPaLM", "Bdq Lzd Cfz Cs", "Am Lfx Pto…", "BIC/FTC/TAF", "TLD", "tenofovir + lamivudine + dolutegravir", "R, H, E", "RHE", "HR", "rifampicin và isoniazid"… đều bị chấm là **abstain** hoặc **unattributed**. Hệ quả: mồi của 01 và 05, giá trị Mỹ BIC của 05, và giá trị bản cũ của 01 và 02 **không đo được** nếu mô hình trả lời theo cách viết thông thường.
  2. **Mẩu 02: giá trị bản cũ trùng một bản WHO cũ.** Phác đồ ngắn hạn có amikacin trùng khuyến cáo WHO 2019 (WHO 2019 tr.37 và tr.42: "kanamycin be replaced by amikacin"). Theo §1.2 đề cương và skill counterpart-matching ("Ghi cả bản WHO hiện hành và bản trước"), mẩu 02 phải thành **indistinguishable**. Tôi đã chạy thử: thêm WHO 2019 {amikacin} thì `finalize()` cho `indistinguishable`.
  3. **Mẩu 01: nhãn "lệch phiên bản" bị nhiễu nguồn.** Phác đồ E1 cũ (Bdq Lzd Cfz Cs + 1 thuốc nhóm C) vẫn có trong 162/2024 (tr.56, "PĐ E") cho người kháng FQ **không đủ** tiêu chuẩn BPaL. Nó cũng đúng là phác đồ dài hạn dựng theo quy tắc WHO (nhóm A bỏ FQ + nhóm B). Ngoài ra, việc 2760/2021 bị thay chỉ là **suy luận**: Điều 3 của 162/2024 chỉ nêu thay 1314/2020.
  4. **Mẩu 03: giá trị Việt Nam trùng một khuyến cáo WHO 2010 đã bị loại.** Giá trị 4RHE trùng "Recommendation 3" của WHO 2010 (HRE ở giai đoạn duy trì nơi kháng isoniazid cao). Phụ lục 1 của chính WHO 2026 ghi khuyến cáo này là "Redundant" (PDF tr.284). Báo cáo coi đây là "giả thuyết chưa kiểm"; nay **đã kiểm và xác nhận**. Trạng thái `conflict` không đổi (đã tính thử), nhưng điểm này phải ghi vào mẩu để bác sĩ diễn giải.

---

## 0. Lệnh kiểm đã chạy (tóm tắt)

| Lệnh / thao tác | Kết quả |
|---|---|
| `vnsoc.schemas atom data/interim/pilot/tbhiv.jsonl` | `OK 7 dòng hợp lệ (atom)` |
| `vnsoc.extract.verify_span data/interim/pilot/tbhiv.jsonl` | `OK: 0 mẩu không đạt` (01–07 đều OK) |
| `verify_span.span_on_page` cho **mọi** `extraction.superseded_spans` (script scratchpad `supspan.py`) | 01: 2760/2021 tr.17 **True**, 1314/2020 tr.60 **True**; 02: 1314/2020 tr.59 **True** |
| `finalize()` + `check_decoy()` bằng mã hiện hành (grade.py và grading.yaml sửa lúc 11:44, **sau** khi mẩu được tạo lúc 11:15; commit 9243d61) | tolerance và conflict_status **giống hệt** giá trị lưu; `check_decoy` = [] cho cả 7 |
| `grade_short` với 60+ câu trả lời mẫu (script `tbhiv_grade_probe.py`, `probe2.py`) | Xem §1 và §2 (lỗi bộ chấm) |
| Chạy thử có thêm bản WHO cũ vào `foreign` (script `whatif.py`) | 02 + WHO 2019 {amikacin} → **indistinguishable**; 01 + WHO 2020 (dài hạn) {cycloserine} → **indistinguishable**; 03 + WHO 2010 HRE → vẫn **conflict** |
| `vnsoc.match.sources fetch/grep` với các nguồn trong mẩu | Mọi chuỗi giá trị đều tìm thấy (§1). Tôi tải thêm 3 nguồn vào `data/cache/foreign` (không vào data/raw): WHO 2019 DR-TB (sha `df14ea4b…`, 104 tr.), WHO 2020 Module 4 DR-TB (sha `133ba15f…`, 120 tr.), ATS/CDC/IDSA 2016 DS-TB trên cdc.gov (sha `86123eb8…`, 49 tr.) |
| Siêu dữ liệu IRIS (DSpace API) | WHO Module 4 bản 2: 2026-09-21 (10665/387622). WHO PEP: 2024-07-16 (10665/378221). WHO DR-TB 2022: 2022-12-14 (10665/365308). Tìm theo tiêu đề "post-exposure prophylaxis" trên IRIS: **không có** hướng dẫn HIV PEP nào mới hơn 7/2024 |
| WebSearch | **Hết hạn mức phiên (200/200)**. Không rà thêm được văn bản Bộ Y tế mới thay 162/2024 hoặc 5968/2021; chỉ dựa vào ghi chú manifest |

---

## 1. Phán quyết từng mẩu

### P-tbhiv-01 — lao tiền siêu kháng, đủ tiêu chuẩn BPaL, lao phổi không nặng, từ 14 tuổi — **verdict: fix**

**Đã xác nhận đúng**
- **162/2024 tr.53 (in 52):**
  - Span có thật.
  - Đối tượng BPaL: "Kháng ít nhất với R và FQ…", "Tuổi từ đủ 14 tuổi trở lên".
  - Thành phần "6-9 BpaL (bedaquiline, pretomanid, linezolid)" nằm ở tr.54.
  - Chống chỉ định ở tr.54 khớp trường `population.contraindications` (QTcF > 500, cân nặng < 35 kg, có thai hoặc cho con bú…).
  - BPaLM chống chỉ định khi "Kháng FQ" (tr.53). Điều này ủng hộ việc BPaLM không phải giá trị Việt Nam cho quần thể này.
- **WHO 2026 (sha `a6092c81…`) PDF tr.22:**
  - B1.1a: BPaL cho "non-severe pulmonary pre-XDR-TB" (NEW 2026).
  - B1.2a: "6-month BDLC regimen in patients with non-severe pulmonary pre-XDR-TB" (NEW 2026).
  - B1.1b (BPaLC, thể nặng) và B1.2b (không dùng BDLC ở thể nặng) đúng là quần thể khác.
  - **Xung đột có thật:** BDLC không có trong 162/2024 cho người đủ tiêu chuẩn BPaL.
- **WHO 2022 (sha `7fdfa0ba…`) PDF tr.26, remark 1:** "…in cases of documented resistance to fluoroquinolones, BPaL without moxifloxacin…". Đúng.
- **Bản cũ:**
  - 2760/2021 tr.17: "Phác đồ E1-FQ mới … Bdq Lzd Cfz Cs +1 thuốc nhóm C".
  - 1314/2020 tr.60: "E1-TSFQ mới …" cùng thành phần.
  - Cả hai bản **không có** BPaL hay pretomanid (`--find` "BPaL", "Pretomanid", "pretomanid" đều = []). Lệch phiên bản có thật trong văn bản.
- Hệ thống WHO_global đúng. Không có trường chỉ-bác-sĩ.

**Vấn đề**
1. **Bộ chấm (nghiêm trọng).** Kết quả `grade_short` với grading.yaml hiện hành:

   | Câu trả lời | Nhãn | Nên là |
   |---|---|---|
   | "ĐÁP ÁN: BPaL" | **abstain** | correct |
   | "ĐÁP ÁN: BPaLM" (mồi) | **abstain** | unattributed + decoy |
   | "ĐÁP ÁN: Bdq Lzd Cfz Cs + 1 thuốc nhóm C" (giá trị bản cũ, đúng cách viết trong văn bản) | **unattributed** (chỉ tách được clofazimine) | temporal |

   - Chỉ khi viết tên đầy đủ thì mới ra đúng: "bedaquiline + pretomanid + linezolid" → correct; "bedaquiline, linezolid, clofazimine, cycloserine" → temporal.
   - Nguyên nhân: `parse_drugs` chỉ gộp combo từ các thuốc thành phần. Tên tổ hợp (bpal, bpalm, bdlc) và chữ viết tắt bdq, lzd, cs **không có** trong `drugs`.
2. **Nhiễu nguồn cho nhãn temporal (§1.2, nguy cơ "không phân biệt được nguồn").**
   - (a) 162/2024 tr.56 (in 55): mục "Phác đồ cá thể", đối tượng "Người bệnh kháng FQ không đủ tiêu chuẩn thu nhận phác đồ BpaL", ghi "…kháng FQ mới…: xem xét chỉ định phác đồ E. PĐ E: Bdq Lzd Cfz Cs +1 thuốc nhóm C". Tức là **giá trị bản cũ vẫn là giá trị hiện hành cho quần thể kề bên**. Câu "Đối với người bệnh kháng FQ mới…" nếu đọc tách khỏi tiêu đề mục có thể hiểu là áp dụng cho mọi người kháng FQ mới. Việc tập Việt Nam có gồm PĐ E hay không cho người **đủ** tiêu chuẩn BPaL là quyết định của bác sĩ. Nếu có, lệch phiên bản biến mất.
   - (b) WHO 2020 Module 4 DR-TB (sha `133ba15f…`):
     - tr.17 ghi BPaL cho kháng FQ chỉ "under operational research conditions".
     - Phác đồ dài hạn dựng theo nhóm: tr.40 "group A = levofloxacin or moxifloxacin, bedaquiline and linezolid; group B = clofazimine, and cycloserine…". Bỏ FQ thì ra đúng Bdq Lzd Cfz Cs.
     - WHO 2026 B3.1 (tr.23) vẫn giữ quy tắc này, và B1.2a so sánh với "currently recommended longer … regimens".
     - WHO **không** nêu nguyên văn tổ hợp "Bdq Lzd Cfz Cs", nên đây là trùng **suy ra**, không phải trùng nguyên văn.
     - Chạy thử nếu ghi WHO 2020 {cycloserine} vào foreign: `indistinguishable`.
   - (c) **Hiệu lực của 2760/2021 là suy luận.** 162/2024 tr.1 Điều 3 chỉ ghi "thay thế Quyết định số 1314/QĐ-BYT"; tr.201 còn dẫn "sơ đồ 3.1. 2 (QĐ 2760 của BYT)". Manifest cũng để `superseded_by: []`. 1314/2020 thì bị thay rõ ràng, nên bản cũ 1314/2020 vẫn đứng vững.
3. **Mồi BPaLM hợp lệ theo quy tắc** (không nguồn nào khuyến cáo cho **quần thể này**; check_decoy = []). Nhưng đây là phác đồ nổi bật nhất và là giá trị hiện hành (VN, WHO B1.1) cho quần thể **kề bên** (lao đa kháng còn nhạy FQ). Vì vậy π_mồi sẽ cao do nhầm quần thể chứ không do trùng ngẫu nhiên, làm H1 thiên về bảo thủ. Cần ghi vào `decoy_rule`; bác sĩ quyết có giữ hay không.
4. Span (tr.53) chứa tên "Phác đồ BPaL" và tiêu chí đối tượng. `verify_span` đạt là nhờ danh sách thuốc ở tiêu chí "không có tiền sử dùng" (Bedaquiline, Pretomanid…, Linezolid), chứ **không** nhờ dòng thành phần phác đồ (tr.54). Chấp nhận được, nhưng nên ghi chú.

**Sửa cụ thể**
- `configs/grading.yaml` (đề xuất; mẩu không đổi):
  - Thêm cơ chế **bí danh tên tổ hợp → thuốc thành phần**, ví dụ `combo_aliases: {bpal: BPaL, bpalm: BPaLM, bdlc: [bedaquiline, delamanid, linezolid, clofazimine], bpalc: [...]}`. `parse_drugs` mở rộng ra thành phần trước khi gộp combo, để "BDLC" khớp khóa {delamanid, clofazimine}.
  - Thêm `bedaquiline: [bdq]`, `linezolid: [lzd]`, `moxifloxacin: [mfx]`, `cycloserine: [cs]` (2 ký tự, **chỉ thêm khi có test**).
  - Thêm combos `BPaLC` (đặt trước BPaL) và `BDLC`.
  - Test bắt buộc: "BPaL" → correct; "BPaLM" → decoy; "Bdq Lzd Cfz Cs + 1 thuốc nhóm C" → temporal; "BDLC" → foreign WHO_global.
- `extraction.notes`: thêm nhiễu nguồn 2(a), 2(b), 2(c), kèm trang: 162/2024 tr.56; WHO 2020 tr.17 và tr.40; WHO 2026 tr.23.
- Chuyển cho người kiểm (HG1.2/HG3.9) quyết định:
  - (i) giữ nhãn lệch phiên bản;
  - (ii) **tách** thành 01a (xung đột BDLC, bỏ `superseded`, dùng cho H1) và 01b (lệch phiên bản, mô tả); hoặc
  - (iii) ghi WHO 2020 phác đồ dài hạn vào `foreign`, để mẩu thành indistinguishable.
  - Đề xuất của kiểm toán: **(ii)**. Xung đột BDLC sạch và đã kiểm; nhãn temporal thì chưa sạch.
- `decoy_rule`: bổ sung "BPaLM là giá trị hiện hành cho quần thể kề bên (lao đa kháng còn nhạy FQ); nguy cơ π_mồi cao".

### P-tbhiv-02 — lao đa kháng còn nhạy FQ, phác đồ chuẩn ngắn hạn 9–11 tháng — **verdict: fix**

**Đã xác nhận đúng**
- **162/2024 tr.49 (in 48):**
  - Span có thật.
  - Thành phần cùng trang: "Phác đồ C1a: 4-6Bdq[6]-Lfx-Pto-E-Z-Hh-Cfz / 5 Lfx-Cfz-Z-E" và C2a (Lzd thay Pto). C3 và BPaL (cho người không dùng được H/E/Z) cũng có Bdq.
  - Tìm "Am Lfx" trong 162/2024 = []: **không còn** phác đồ ngắn hạn có thuốc tiêm. Tập Việt Nam {bedaquiline} đúng.
- 2760/2021 tr.12: PĐ C đã là "4-6Bdq[6]-Lfx-Pto-E-Z-Hh-Cfz…". Báo cáo đúng khi không ghi bản này vào `superseded`.
- 1314/2020 tr.59: "4-6 Am Lfx Pto Cfz Z H liều cao E / 5 Lfx Cfz Z E". Span bản cũ đúng trang.
- WHO 2026 tr.22 (B2.1, Unchanged 2022) và tr.140: "bedaquiline (used for 6 months), in combination with levofloxacin/moxifloxacin, ethionamide…". Trùng Việt Nam (concordant). B2.2 (BLMZ, BLLfxCZ, BDLLfxZ) cũng đều có Bdq.

**Vấn đề**
1. **Giá trị bản cũ trùng WHO cũ (báo cáo nêu ở HG mục 6 là "cần quyết định"; nay đã kiểm).** WHO 2019 (sha `df14ea4b…`, IRIS 10665/311389, 2019-03-20):
   - tr.37, Recommendation 4.1: "a shorter MDR-TB regimen of 9–12 months may be used"; thành phần 4–6Km–Mfx–Cfz–Eto–Z–E–Hh/5Mfx–Cfz–Z–E (tr.41).
   - tr.42: "kanamycin be replaced by amikacin".
   - WHO 2026 tr.73 cũng ghi phác đồ Bdq toàn uống "recommended by WHO since 2019".
   - Theo skill counterpart-matching, bản WHO trước phải được ghi. Thêm WHO_global 2019 {amikacin} → `finalize()` = **indistinguishable** (đã chạy).
   - Kết luận: mẩu 02 **không dùng được** cho kiểm định xác nhận như một mẩu lệch phiên bản. Trạng thái "concordant" hiện tại có được là vì **thiếu** bản WHO trước.
2. **Bộ chấm:** giá trị bản cũ và giá trị hiện hành đều **không đo được** theo cách viết của văn bản.
   - "4-6 Am Lfx Pto Cfz Z H liều cao E / 5 Lfx Cfz Z E" → unattributed.
   - "amikacin, levofloxacin, prothionamide…" → unattributed (amikacin không có trong `drugs`).
   - "4-6 Bdq-Lfx-Pto-E-Z-Hh-Cfz / 5 Lfx-Cfz-Z-E" (đúng Bộ Y tế) → **unattributed** (thiếu bí danh bdq).
3. Khóa một thuốc {bedaquiline}: mọi câu trả lời có bedaquiline đều là correct, kể cả câu trộn cả amikacin. Chấp nhận theo quy ước "thuốc phân biệt", nhưng câu hỏi phải hỏi rõ "phác đồ ngắn hạn toàn uống gồm những thuốc nào" và câu hỏi cần được QC.
4. `conflict_family` = "dr_tb_short_regimen_injectable_to_bdq" cho một mẩu concordant/drift: không sai schema, nhưng tên "conflict" gây hiểu nhầm (nhỏ).

**Sửa cụ thể**
- Thêm vào `foreign`:

  ```
  {system: WHO_global, source: "WHO consolidated guidelines on drug-resistant tuberculosis treatment (2019)",
   version_date: "2019-03-20",
   url: "https://iris.who.int/server/api/core/bitstreams/30d89c8e-8e59-4f52-82b4-9a30882a09bf/content",
   page_sha256: "df14ea4b23abee1c59ce79c6612159e4371e8a7e9bf8fc9a75dddfe0e1e34778",
   locator: "Recommendation 4.1 PDF p.37; composition p.41; 'kanamycin be replaced by amikacin' p.42",
   values: [{key_drugs: [amikacin], text: "phác đồ ngắn hạn chuẩn 9–12 tháng có thuốc tiêm (Km→Am)"}]}
  ```

  Sau đó gọi lại `finalize()`; trạng thái kỳ vọng là `indistinguishable`.
- `configs/grading.yaml` (đề xuất): thêm `amikacin: [amikacine]`, `kanamycin: [kanamycine]`, `capreomycin: []`, `prothionamide: [prothionamid, pto]`, `ethionamide: [eto]`, `bedaquiline: [bdq]`. "am", "km" quá mơ hồ; chỉ nhận trong ngữ cảnh chuỗi thuốc, có test. Test: câu bản cũ → temporal (hoặc indistinguishable sau khi thêm WHO 2019); câu C1a → correct.
- Báo cáo §2: sửa trạng thái 02 và ghi rõ chủ đề tbhiv **không có mẩu lệch phiên bản sạch nào** trước khi bác sĩ quyết định mẩu 01.

### P-tbhiv-03 — lao phổi nhạy cảm, người lớn, phác đồ 6 tháng, giai đoạn duy trì — **verdict: fix**

**Đã xác nhận đúng**
- **162/2024 tr.44 (in 43):**
  - A1 "2HRZE/4RHE (phác đồ 06 tháng – điều trị lao cho người lớn)", "Giai đoạn duy trì: kéo dài 04 tháng, với 03 loại thuốc: R, H, E".
  - Áp dụng cả người nhiễm HIV và phụ nữ mang thai; không áp dụng cho lao thần kinh trung ương và lao xương khớp (B1 2HRZE/10RHE ở tr.46). Không trang nào khác cho giá trị khác với quần thể này.
  - Bản cũ 1314/2020 (tr.53, 54, 62) và 2760/2021 (tr.4–5) cùng RHE, nên không lệch phiên bản.
- WHO 2026 PDF tr.19: A1.1 "2HRZE/4HR" (Strong/high, Unchanged 2010); tr.32 lặp lại.
- CDC (WebFetch, cập nhật 17/4/2025): duy trì "4 or 7 months of isoniazid and rifampin". Đúng giá trị nhưng không có mã băm.
- **Xung đột có thật** (người lớn: Việt Nam có E ở giai đoạn duy trì, WHO và Mỹ không có). Báo cáo đúng khi sửa kỳ vọng của bảng giao việc.

**Vấn đề**
1. **Nguồn Mỹ chưa có mã băm nhưng `verified_by: "auto"`.** Kiểm toán đã tải được **bản chính thức có băm** trên cdc.gov: ATS/CDC/IDSA 2016 (sha `86123eb8…`, 49 tr., "Advance Access published August 10, 2016"). PDF tr.4 ghi "continuation phase of 4 months of INH and RIF" và Bảng 2 ghi "INH RIF 7 d/wk for 126 doses (18 wk)". Báo cáo §1b ghi nguồn này "Không dùng được" là **không còn đúng**: bản PMC bị chặn, nhưng bản PDF trên cdc.gov tải được.
2. **WHO 2010 "Recommendation 3" (báo cáo: "giả thuyết chưa kiểm") nay đã xác nhận.** WHO 2026 Phụ lục 1, PDF tr.284 (in 256) ghi:
   - Nội dung: "In populations with known or suspected high levels of isoniazid resistance, new TB patients may receive HRE as therapy in the continuation phase as an acceptable alternative to HR".
   - Trạng thái: "Remained valid → Redundant", thay bằng chính sách lao kháng H năm 2020.
   - Nghĩa là giá trị Việt Nam = **một phương án WHO cũ đã bị loại**. Nhãn `conflict` không đổi: thêm WHO 2010 HRE vào foreign vẫn ra `conflict` (đã chạy). Nhưng điều này quyết định cách diễn giải (`moh_lags_evidence` là trường chỉ bác sĩ gán; kiểm toán **không** gán).
3. **`cat_options` bỏ sót nhiều dạng trả lời thường gặp** (kết quả `grade_short`):

   | Câu trả lời | Nhãn | Nên là |
   |---|---|---|
   | "R, H, E" | abstain | correct |
   | "RHE" | abstain | correct |
   | "ANSWER: RHE for 4 months" | abstain | correct |
   | "Rifampicin (R), Isoniazid (H), Ethambutol (E) trong 4 tháng" | abstain | correct |
   | "giai đoạn duy trì gồm rifampicin, isoniazid và ethambutol" | abstain | correct |
   | "HR" | abstain | foreign |
   | "RH" | abstain | foreign |
   | "rifampicin và isoniazid" | abstain | foreign |
   | "ANSWER: isoniazid and rifampin for 4 months" | abstain | foreign |
   | "2HRZE/4(HR)3" | abstain | foreign |

   Dạng có số tháng ("4RHE", "4 tháng HRE", "2HRZE/4HR") thì đúng. Sai lệch này **không đối xứng**: câu trả lời theo WHO viết bằng tên thuốc bị đếm là từ chối, làm giảm π_nước ngoài.
4. **Câu trả lời rào đón** "2RHZE/4RHE hoặc 2RHZE/4RH" → **correct**. `parse_cats` trả về một giá trị có hai nhãn, nên không vào nhánh multi-value. Đây là lỗi mức bộ chấm (xem Vấn đề chung).
5. `extraction.notes` giải thích chọn `cat` vì "_gap giao tập". Mã hiện hành đã đổi: `_gap` so tập bằng nhau. Lý do đúng bây giờ là `matches()` dùng **tập con**, nên {H,R} ⊆ {H,R,E} sẽ khớp cả WHO lẫn Việt Nam. Vẫn nên dùng `cat`, nhưng ghi chú phải sửa.

**Sửa cụ thể**
- `foreign[US]`: thay (hoặc bổ sung) bằng:

  ```
  {system: US, source: "ATS/CDC/IDSA Clinical Practice Guidelines: Treatment of Drug-Susceptible Tuberculosis (Nahid et al., Clin Infect Dis 2016)",
   version_date: "2016-08-10",
   url: "https://www.cdc.gov/tb/publications/guidelines/pdf/clin-infect-dis.-2016-nahid-cid_ciw376.pdf",
   page_sha256: "86123eb8f815f62ca3606c1a905e06e3a8d30eaff42d84f1260549af0d2261a0",
   locator: "Table 2 và phần khuyến cáo, PDF p.4",
   values: [{label: HR}]}
  ```

  Nếu giữ trang CDC thì đặt `verified_by: null` (không phải "auto"), vì page_sha256 = null.
- Ghi WHO 2010 Rec.3 vào `extraction.notes`, hoặc vào `foreign` như một bản WHO cũ, trích từ WHO 2026 Phụ lục 1 PDF tr.284, sha `a6092c81…`, value {label: HRE}, version_date "2010". Trạng thái vẫn là conflict.
- `cat_options` (đề xuất, phải có test cho cả 03 và 04 trước khi đóng băng; văn bản đã bỏ dấu và viết thường):
  - HRE:
    - `^\W*(?:r\s*,?\s*h|h\s*,?\s*r)\s*(?:,|va|and|\+)?\s*e\W*(?:\(|for|trong|x|$)`
    - `^(?=.*\b(?:isoniazid|izoniazid|inh)\b)(?=.*\brifamp)(?=.*\bethambutol)(?!.*pyrazinamid)`
  - HR:
    - `^\W*(?:hr|rh|h\s*(?:,|va|and|\+)\s*r|r\s*(?:,|va|and|\+)\s*h)\W*(?:\(|for|trong|x|$)`
    - `^(?=.*\b(?:isoniazid|izoniazid|inh)\b)(?=.*\brifamp)(?!.*ethambutol)(?!.*pyrazinamid)`
    - `4\s*\(\s*(?:hr|rh)\s*\)\s*3`
  - RE (mồi): tương tự, không có isoniazid.
  - Mẫu dùng lookahead chỉ an toàn khi câu trả lời **chỉ** nêu giai đoạn duy trì. Câu hỏi phải hỏi riêng giai đoạn duy trì. Cần test với các câu nêu cả hai giai đoạn bằng chữ.
- Sửa `extraction.notes` như vấn đề 5.

### P-tbhiv-04 — lao nhạy cảm trẻ em, phác đồ 6 tháng, giai đoạn duy trì (đối chứng ghép cặp với 03) — **verdict: fix**

**Đã xác nhận đúng**
- 162/2024 tr.44: "Phác đồ A2: 2HRZE/4RH (… điều trị lao cho trẻ em)". Tr.45: "Giai đoạn duy trì kéo dài 04 tháng với 02 loại thuốc: R, H".
- WHO 2026 PDF tr.20: A1.6a (HRZ/HR) và A1.6b ("HRZE for 2 months followed by … HR for 4 months") đều là duy trì HR. **Concordant có thật.**
- Quần thể loại đúng phác đồ 4 tháng A2a (tr.45–46). Mâu thuẫn nội bộ của A2a ("2 loại thuốc: R, H, E") không ảnh hưởng mẩu này.

**Vấn đề**
- Cùng lỗi `cat_options` với 03: "rifampicin và isoniazid", "HR", "RH", "R, H" → abstain.
- Là đối chứng ghép cặp nên phải sửa đồng bộ với 03, nếu không so sánh cặp sẽ lệch.

**Sửa cụ thể**
- Dùng cùng bộ `cat_options` đã sửa và test cho 03.
- Câu hỏi phải nêu trẻ **không** đủ 3 tiêu chí của A2a, hoặc nêu rõ "phác đồ 6 tháng".

### P-tbhiv-05 — dự phòng sau phơi nhiễm HIV (PEP), trên 10 tuổi, phác đồ ưu tiên — **verdict: fix**

**Đã xác nhận đúng**
- **5968/2021 tr.29, Bảng 3:** "Người trên 10 tuổi | Ưu tiên: TDF + 3TC (hoặc FTC) + DTG | Thay thế: … LPV/r … RAL". Không trang nào khác nêu phác đồ PEP người lớn khác (đã đọc tr.19, 22, 27, 28, 30, 31).
- **WHO PEP 2024 (sha `56493a35…`) PDF tr.8:** "TDF + 3TC (or FTC) is recommended as the preferred backbone", "DTG is recommended as the preferred third drug". Bản 2024 là mới nhất trên IRIS.
- **CDC nPEP 2025** (PMC12064164, epub 08/05/2025, MMWR RR 74(1), doi 10.15585/mmwr.rr7401a1): "preferred regimens … bictegravir/emtricitabine/tenofovir alafenamide or dolutegravir plus (tenofovir alafenamide or tenofovir disoproxil fumarate) plus (emtricitabine or lamivudine)".
- **Xung đột có thật, chỉ với Mỹ:**
  - BIC/FTC/TAF và DTG + TAF đều ngoài tập Việt Nam.
  - Mã hiện hành xếp "DTG + TAF + FTC" là **foreign US** (đã chạy thử).
  - Ghi chú trong mẩu nói "grader coi là trùng (gap giao tập)" là **đã lỗi thời**.
- Mồi TDF + 3TC + NVP:
  - Tìm "nevirapine" = 0 trong WHO 2024 và CDC 2025.
  - Trong 5968/2021, NVP chỉ xuất hiện trong phác đồ trẻ em và sơ sinh, và trong phác đồ người lớn cũ cần chuyển sang DTG (tr.35, Bảng 6).
  - Hợp lệ.

**Vấn đề**
1. **Bộ chấm không nhận diện được giá trị Mỹ xung đột chính và mồi.**

   | Câu trả lời | Nhãn | Nên là |
   |---|---|---|
   | "BIC/FTC/TAF" | unattributed | foreign US |
   | "bictegravir/emtricitabine/tenofovir alafenamide" | unattributed | foreign US |
   | "Biktarvy" | abstain | foreign US |
   | "TDF + 3TC + NVP" (mồi) | unattributed, **decoy = False** | decoy |
   | "TLD" (tên phổ biến của đúng phác đồ Bộ Y tế) | **abstain** | correct |
   | "tenofovir + lamivudine + dolutegravir" | **unattributed** | correct (theo quy ước ngữ cảnh) |

   Nguyên nhân: thiếu `bictegravir`, `nevirapine`; thiếu bí danh "tld" và "biktarvy"; chữ "tenofovir" đứng riêng không ánh xạ được.
2. Không có `superseded` vì chưa có PDF 5456/2019 trong data/raw (manifest: có URL chính thức vaac.gov.vn nhưng chứng chỉ TLS hết hạn). Nhãn temporal không đo được ở mẩu này. Chấp nhận, nhưng phải ghi là hạn chế.
3. `extraction.notes` về "gap giao tập" đã lỗi thời (xem trên).

**Sửa cụ thể**
- `configs/grading.yaml` (đề xuất, có test):
  - `bictegravir: [bic, bictegravir sodium]`
  - `nevirapine: [nvp, nevirapin]`
  - `raltegravir: [ral]`
  - `lopinavir-ritonavir: [lpv/r]`
  - `zidovudine: [azt, zdv]`
  - `abacavir: [abc]`
  - combo_aliases: `tld → [tenofovir-disoproxil, lamivudine, dolutegravir]`, `biktarvy → [bictegravir, emtricitabine, tenofovir-alafenamide]`
  - Quyết định có ghi (đăng ký trước) cho "tenofovir" đứng riêng: ví dụ ánh xạ về tenofovir-disoproxil. Bí danh dài "tenofovir alafenamide" được khớp trước, nên TAF không bị ảnh hưởng.
  - Test: "BIC/FTC/TAF" → foreign US; "TDF + 3TC + NVP" → decoy; "TLD" → correct.
- Sửa `extraction.notes`: bỏ câu "grader coi là trùng (gap giao tập)"; ghi "DTG + TAF là giá trị Mỹ xung đột thứ hai (mã hiện hành xếp foreign US)".

### P-tbhiv-06 — thời gian PEP — **verdict: pass**

- 5968/2021 tr.29: "…đủ 28 ngày liên tục". Tr.22 ("Sử dụng PEP trong 28 ngày") cũng thống nhất.
- WHO 2024 tr.8: "28-day prescription". CDC 2025: "recommended nPEP course is 28 days".
- Concordant có thật. Không có xung đột nên không cần mồi; `mirror_decoy` → "không có giá trị nước ngoài xung đột".
- Bộ chấm: "28 ngày", "4 tuần", "28 days" → correct; "30 ngày" → unattributed.
- Ghi chú nhỏ: "1 tháng" → unattributed (không quy đổi tháng sang ngày). Chấp nhận, vì 1 tháng ≠ 28 ngày.

### P-tbhiv-07 — lao kháng H nhạy R, thời gian điều trị — **verdict: pass**

- 162/2024 tr.58 (tiêu đề "d) Phác đồ kháng H nhạy R … 6 R(H)ZELfx") và tr.59 (in 58): "Thời gian điều trị 06 tháng." Phương án thay thế "6 RHZE" (tr.58) cũng 6 tháng. Không trang nào khác cho thời gian khác (tr.77 chỉ nói theo dõi).
- WHO 2026 PDF tr.25: B4.1 "…rifampicin, ethambutol, pyrazinamide and levofloxacin … for a duration of 6 months" (Unchanged 2018). Concordant có thật.
- Bộ chấm: "6 tháng", "6 R(H)ZELfx", "6 months" → correct.
- Góp ý không bắt buộc: câu ngay sau span ("Tuy nhiên, cần lưu ý: - Người bệnh có tổn thương rộng hoặc âm hóa chậm có thể kéo dài thời gian điều trị…") là điều kiện đi kèm. `population.site` đã phản ánh đúng ("không tổn thương rộng, âm hóa đúng hạn"), nên không cần sửa. Có thể ghi thêm vào `extraction.notes` cho người kiểm.

---

## 2. Vấn đề chung

1. **Mẩu được tạo trước khi bộ chấm đổi (11:15 so với 11:44, commit 9243d61).**
   - Tôi đã tính lại: `tolerance` và `conflict_status` **không đổi**.
   - Nhưng 3 phần trong báo cáo và ghi chú mẩu đã lỗi thời:
     - (a) Báo cáo §6 và ghi chú 03/05: "_gap … giao tập". Nay `_gap` so **tập bằng nhau**.
     - (b) Báo cáo §3.1: loại đối chứng "HIV bậc một TDF + 3TC + DTG" vì chú thích "DTG1". `parse_drugs` hiện hành đã bỏ số chú thích: "TDF + 3TC (hoặc FTC) + DTG1" tách được đủ 4 thuốc. **Nên dựng lại đối chứng này** (5968/2021 Bảng 5, tr.34); đây là đối chứng có trong bộ hạt giống.
     - (c) Một phần đề xuất config ở §6 đã được thêm (isoniazid, rifampicin, ethambutol, levofloxacin, clofazimine, cycloserine, delamanid, emtricitabine…). Các thứ **còn thiếu** như liệt kê ở mục 01, 02, 05.
2. **Bộ chấm với phác đồ thuốc: cần một đợt "test bằng câu trả lời mẫu thật" trước khi đóng băng.** Với 5 mẩu drugs/cat của chủ đề này, dạng trả lời phổ biến nhất (tên tổ hợp, chữ viết tắt trong văn bản Bộ Y tế, tên biệt dược, liệt kê chữ cái) cho abstain hoặc unattributed. Đề xuất cho người giữ grading.yaml:
   - (i) thêm cơ chế bí danh tên tổ hợp → thuốc thành phần;
   - (ii) thêm các INN và viết tắt đã liệt kê;
   - (iii) mỗi mẩu drugs/cat có ≥ 10 câu trả lời mẫu kèm nhãn kỳ vọng trong `tests/` (đầu vào của scratchpad `tbhiv_grade_probe.py` có thể làm mầm);
   - (iv) tăng `grader_version`.
3. **Nhãn `cat` với câu trả lời rào đón.** `parse_cats` trả về **một** giá trị có nhiều nhãn, nên "4RHE hoặc 4RH" được chấm **correct**. Với `drugs` và `num`, câu nhiều giá trị lại đi nhánh multi (unattributed hoặc correct_aware). Cần quy tắc thống nhất: coi mỗi nhãn là một giá trị để dùng logic multi. Đây là thay đổi mã trong `grade.py`/`normalize_vi.py`, ảnh hưởng mọi chủ đề có mẩu `cat`.
4. **Bản WHO cũ chưa được ghi một cách hệ thống.** Skill counterpart-matching yêu cầu "Ghi cả bản WHO hiện hành và bản trước". Chủ đề này có 3 trường hợp đã kiểm bằng nguồn có băm:
   - WHO 2019: phác đồ ngắn hạn có thuốc tiêm → mẩu 02 thành indistinguishable;
   - WHO 2020: phác đồ dài hạn cho người kháng FQ, BPaL chỉ trong nghiên cứu vận hành → nhiễu mẩu 01;
   - WHO 2010 Rec.3: HRE ở giai đoạn duy trì → diễn giải mẩu 03.
   - Đề xuất: quy trình ghép phải tra **phụ lục lịch sử khuyến cáo** (Annex 1 của WHO Module 4 bản 2 liệt kê đầy đủ) cho mọi mẩu lao.
5. **Chuỗi thay thế.**
   - 1314/2020 → 162/2024: rõ ràng (Điều 3, tr.1).
   - 2760/2021 → 162/2024: **suy luận**. Danh tính 2760/2021 cũng chưa xác nhận: file chỉ có phần tài liệu, không có trang quyết định. Bằng chứng gián tiếp là 162/2024 tr.201 dẫn "QĐ 2760 của BYT" cho sơ đồ 3.1.2, và sơ đồ này có ở 2760_2021.pdf tr.37.
   - Số hiệu 162 và ngày ký của 162/2024 chưa xác nhận từ PDF (lớp chữ để trống).
   - Cả hai vẫn ở HG1.2 như báo cáo ghi. Kiểm toán **đồng ý** với báo cáo ở điểm này.
6. **Hiệu lực tại ngày đóng băng (15/10/2026):**
   - Không kiểm thêm được vì hết hạn mức WebSearch.
   - Theo manifest: danh mục quyết định trên vaac.gov.vn chỉ cập nhật tới 12/2024; moh.gov.vn chưa kiểm; tài liệu "hướng dẫn lâm sàng CTCLQG 2025" chưa rõ tư cách.
   - WHO Module 4 bản 2 phát hành **21/9/2026, 5 ngày trước hôm nay**. Mọi mẩu lao phải dùng bản này làm mốc WHO_global. Các mẩu 01–04 và 07 đã làm đúng.
7. **Đánh giá "sai lệch so với bộ hạt giống" trong báo cáo (§4): đúng.** Tôi đã kiểm lại từng điểm:
   - (a) 2760/2021 tr.12 PĐ C đã có Bdq; 162/2024 tr.49 C1a giống, thêm C2a, C3 và BPaLM.
   - (b) Lệch phiên bản chỉ còn ở nhóm kháng FQ từ đầu (nhưng xem nhiễu nguồn ở mẩu 01).
   - (c) Mốc WHO trong hạt giống ("WHO 2022 BPaLM") đã cũ; bản 2026 có B1.1a và B1.2a mới.
   - (d) Người lớn lao nhạy cảm: Việt Nam dùng 2HRZE/4RHE, xung đột với WHO.
   - Cần **bổ sung** vào báo cáo:
     - (e) dòng 22 sau khi thêm bản WHO cũ không còn mẩu lệch phiên bản sạch nào (02 indistinguishable; 01 chờ bác sĩ);
     - (f) đối chứng HIV bậc một nay dựng được (Vấn đề chung 1b).
8. **Không có trường chỉ-bác-sĩ** (`moh_lags_evidence`, `clinical_harm`, `clinician_confirmed`) trong cả 7 mẩu: đúng quy tắc. `context_checked` đều là "pending": đúng, chờ HG.
9. **Tệp kiểm toán đã tạo** (không vào data/raw, data/frozen hay state):
   - Cache nguồn nước ngoài qua `vnsoc.match.sources fetch`: `data/cache/foreign/df14ea4b23abee1c59ce.pdf` (WHO 2019), `data/cache/foreign/133ba15f96e70420da57.pdf` (WHO 2020), `data/cache/foreign/86123eb8f815f62ca360.pdf` (ATS/CDC/IDSA 2016).
   - Script trong scratchpad của phiên: `tbhiv_grade_probe.py`, `probe2.py`, `supspan.py`, `whatif.py`, `pg.py`.
