# T1.1 thí điểm — Kiểm toán độc lập chủ đề Viêm gan vi rút B (ID = hbv)

Ngày: 2026-09-26 · Người kiểm: integrity-auditor (Claude), kiêm góc nhìn bác sĩ lâm sàng Việt Nam **do AI đóng vai, không phải bác sĩ thật** · Đầu vào: `data/interim/pilot/hbv.jsonl` (10 mẩu), `data/interim/pilot/hbv_report.md` · File này chỉ đọc dữ liệu; không sửa `data/raw`, `configs`, `src`.

## Kết luận ngắn

- **Phán quyết:** pass 2 (02, 10) · fix 8 (01, 03, 04, 05, 06, 07, 08, 09) · reject 0.
- **Phát hiện chính của báo cáo là đúng.** Dòng hạt giống 20 **không** phải xung đột sạch. Tôi đã tự xem ảnh bản quét 3310/2019:
  - tr.PDF 4 ghi ULN 35/25 U/L;
  - tr.PDF 7 ghi ALT > 2 lần ULN, HBV DNA ≥ 20.000 (HBeAg+) và ≥ 2.000 (HBeAg−).
  - Bằng chứng độc lập thêm: 1740/2026 tr.PDF 15 (mục viêm gan B **cấp**) định nghĩa lại "ULN đối với ALT: 30 U/L nam, 19 U/L nữ", đúng vị trí mà 3310 định nghĩa 35/25. Như vậy 35/25 là ULN dùng cho toàn văn bản 3310, không chỉ cho viêm gan cấp.
- **Báo cáo bỏ sót một câu then chốt của 3310/2019** (tr.PDF 7, tr. in 5, mục 2.4.2). Nguyên văn: *"Đối với các trường hợp chưa đáp ứng hai tiêu chuẩn trên, chỉ định điều trị khi có một trong các tiêu chuẩn sau: + Trên 30 tuổi với mức ALT cao hơn ULN kéo dài (ghi nhận ít nhất 3 lần trong khoảng 24 - 48 tuần) và HBV DNA > 20.000 IU/ml, bất kể tình trạng HBeAg."*
  - Đây chính là tiêu chí của WHO 2015 (WHO 2015 tr.22: "aged more than 30 years (in particular)… HBV DNA >20 000 IU/mL, regardless of HBeAg status").
  - Hệ quả 1: **P-hbv-08 không còn là "conflict"** với quần thể đang ghi. Tôi đã chạy `finalize()` sau khi thêm giá trị này vào `superseded`, kết quả là `indistinguishable`.
  - Hệ quả 2: P-hbv-04 cũng mất lệch phiên bản ở người > 30 tuổi.
  - Sau kiểm toán, số mẩu xung đột dùng được cho H1 của chủ đề HBV giảm từ 2 xuống **1** (P-hbv-07). Mẩu này cũng cần sửa và vẫn mong manh (xem mục 07).
- **Báo cáo đọc thiếu AASLD 2025.** Slide 24 (Recommendation 4) và slide 25 (Figure 3): với HBeAg âm tính, HBV DNA ≥ 2.000 IU/mL và ALT < 2×ULN, AASLD *gợi ý điều trị theo quyết định chung* (có điều kiện). Slide 21 (Figure 2): với HBeAg dương tính, ALT 1–<2×ULN, *gợi ý cân nhắc điều trị* nếu ≥ 40 tuổi hoặc ≥ F2. Vì vậy "AASLD = ALT ≥ 2×ULN" chỉ đúng cho định nghĩa pha "immune active". Quần thể của các mẩu 03, 04, 08 phải chốt chặt hơn.
- **Lỗi chấm điểm phát hiện bằng chạy thử:**
  - `configs/grading.yaml` không nhận "tenofovir alafenamide", "tenofovir disoproxil", "Tenofovir disoproxil fumarat" (cách viết tiếng Việt) hay tên biệt dược. Ảnh hưởng mẩu 06.
  - Regex của mẩu 04 không nhận "gấp đôi", "double", "more than 2 times", ">2ULN", "> 2 ULN".
- **Chặn pipeline:** `pilot_merge.check()` gọi `check_decoy()`. Hàm này báo "mồi làm mẩu thành indistinguishable" cho 01, 02, 03, 10, dù các mẩu này đã `indistinguishable` khi **chưa** có mồi (tôi đã chạy lại, xác nhận là báo động giả). Nếu không sửa mã, 4 mẩu này sẽ bị loại khi gộp.

---

## 0. Lệnh kiểm đã chạy (tự chạy lại, không dựa vào báo cáo)

| Lệnh / thao tác | Kết quả |
|---|---|
| `vnsoc.schemas atom data/interim/pilot/hbv.jsonl` | `OK 10 dòng hợp lệ (atom)` |
| `vnsoc.extract.verify_span data/interim/pilot/hbv.jsonl` | `OK: 0 mẩu không đạt`. Chỉ chứng minh span có trong 1740/2026, **không** kiểm `superseded_spans` |
| `verify_span --page 1740/2026` các tr. 1–3, 15, 17–25, 28, 30, 36–38, 40–42 | Đọc toàn văn quanh mọi span (xem từng mục) |
| `finalize()` / `mirror_decoy()` / `check_decoy()` chạy lại cho 10 mẩu | `tolerance` và `conflict_status` trùng file. Mồi num trùng `mirror_decoy(auto)`. Khi bỏ mồi, trạng thái của 01, 02, 03, 10 vẫn là `indistinguishable`, nên cảnh báo của check_decoy là báo động giả |
| Dựng ảnh bản quét `3310_2019__c43006cb.pdf` (sha256 `c43006cb69cb517f…`, 18 tr.) ở tr. 2, 3, 4, 5, 6, 7, 8, 9, 14, 16 bằng PyMuPDF, lưu vào scratchpad, đọc bằng mắt | Mọi `superseded_spans` 3310 **chép đúng** (có dấu "…" lược bớt ở tr.8 và tr.16). Phát hiện câu bị bỏ sót ở tr.7 (xem trên) |
| `verify_span --find 3310/2019` (file `3310_2019.pdf` của BV Hà Trung) | Có "Tenofovir (300mg/ngày) hoặc entecavir" và "3 lần xét nghiệm liên tiếp" (tr.3). **Không** có "35 U/L", "Trên 30 tuổi", "Tenofovir alafenamide", "2.4.2". Xác nhận file **sai nhãn** (nội dung là 5448/2014) |
| `vnsoc.match.sources fetch/grep` AASLD slide (sha `763a79fe…`), WHO 2024 (sha `e4423119…`), WHO 2015 (sha `e8ef75c1…`) | Mọi giá trị nước ngoài **có** trong nguồn đã băm (chi tiết từng mục) |
| `sources fetch https://journals.lww.com/10.1097/HEP.0000000000001549` | **403**. Europe PMC (WebFetch, không có sha): tiêu đề "AASLD ISDA Practice Guideline on treatment of chronic hepatitis B", đăng điện tử 2025-11-04, Hepatology 2026;83(4):974–997, PMID 41186418, không truy cập mở |
| Europe PMC, DOI 10.1016/j.jhep.2025.03.018 (EASL 2025) | PMID 40348683, "Subscription required", không có trong PMC. Khẳng định "không đọc được" của báo cáo là **đúng** |
| `nv.parse_cats` (mẩu 04), `nv.parse_drugs` (mẩu 06) trên câu trả lời mẫu | Có lỗ hổng (xem 04, 06) |
| WebSearch để kiểm 1740/2026 còn hiệu lực, và WHO có bản 2025/2026 hay chưa | **Không làm được**: phiên đã hết hạn mức 200/200 lượt tìm kiếm. Xem Vấn đề chung, mục G |

Không mẩu nào có trường chỉ-bác-sĩ (`moh_lags_evidence`, `clinical_harm`, `clinician_confirmed`). `context_checked` = `pending` ở cả 10 mẩu (đúng).

---

## 1. Phán quyết từng mẩu

### P-hbv-01 — ULN của ALT, nam · **verdict: fix** (nhỏ; trạng thái giữ nguyên)

**Đã kiểm, đúng:**
- VN 30 U/L: 1740 tr.PDF 18, khớp nguyên văn. Cùng giá trị ở tr.PDF 15 (mục cấp), nên 1740 không có mâu thuẫn nội bộ.
- AASLD 35 U/L (grep "35 U/L"):
  - slide 4: "< 35 u/l in men";
  - slide 21 và 25: "ULN for ALT: 25 U/L in women, 35 U/L in men". Cả hai slide có dòng trích "Ghany M., et al. … Hepatology 2025".
- WHO 2024 30 U/L: tr.24, 35, 41, 43, 47, 83.
- 3310 35 U/L: ảnh tr.4.
- Trạng thái `indistinguishable`: đúng, và được tăng cường bởi tr.15 của 1740 (ULN định nghĩa ở cùng vị trí, nay đổi 35/25 → 30/19).

**Vấn đề:**
1. Mồi 25 U/L (`mirror_arith`, đúng quy tắc prereg §6.4) **trùng ULN nữ** của AASLD 2025 và 3310/2019. Đó là một giá trị có nguồn thật ở mẩu anh em (02). Mẩu được dựng trắc nghiệm vì có giá trị bản cũ (prereg §6.5). Khi đó, mô hình nhầm giới mà chọn 25 sẽ bị tính là "trùng mồi", làm sai ước lượng π_mồi.
2. `check_decoy` chỉ so với nguồn ghi trong **chính** mẩu, nên không bắt được lỗi này.

**Cách sửa:**
- `decoy` → `[{"lo":26,"hi":26,"unit":"U/L","text":"26 U/L"}]` (`mirror_geom`, phương án dự phòng thứ hai đã định trước trong `choose_decoy`; tôi đã chạy `mirror_decoy(a,"mirror_geom")` → 26).
  - Việc này cần ghi `docs/DECISIONS.md`, vì prereg §6.4 chỉ mô tả `auto`.
  - Nếu không đổi mồi thì phải ghi rõ giới hạn trong QC trắc nghiệm.
- `extraction.notes`: thêm "ULN 35/25 của 3310 nằm ở mục II (cấp); 1740 tr.PDF 15 thay đúng câu đó bằng 30/19 → hiểu là ULN toàn văn bản".

### P-hbv-02 — ULN của ALT, nữ · **verdict: pass**

- VN 19 U/L: tr.PDF 18.
- AASLD 25 U/L: slide 4, 21, 25.
- WHO 2024 19 U/L: như trên.
- 3310 25 U/L: ảnh tr.4.
- Trạng thái `indistinguishable`: đúng.
- Mồi 13 U/L = `mirror_arith` (2·19 − 25). Không trùng nguồn nào tôi biết.
- Chỉ còn việc chung: cảnh báo `check_decoy` là báo động giả (Vấn đề chung B), và chuẩn hóa metadata AASLD (Vấn đề chung D).

### P-hbv-03 — Ngưỡng HBV DNA khởi trị, HBeAg dương tính · **verdict: fix** (quần thể; trạng thái giữ `indistinguishable`)

**Đã kiểm, đúng:**
- Span 1740 tr.PDF 20: "HBV DNA > 2000 IU/mL và ALT > giới hạn trên…". Áp dụng cho người ≥ 12 tuổi, không phân biệt HBeAg.
- AASLD ≥ 20.000: slide 4, 21 ("HBV DNA ≥20,000 IU/mL / ALT ≥2x ULN / Immune active / Treat").
- WHO 2024 > 2000: tr.35.
- WHO 2015 > 20 000: tr.22.
- 3310 ≥ 20.000: ảnh tr.7.
- 5448 ≥ 20.000 IU/ml: tr.4, lớp chữ.

**Vấn đề:**
1. `population.alt` = "tăng trên ULN" là chưa đủ. Với HBeAg+ và ALT 1–<2×ULN, AASLD xếp vào pha "Indeterminate": theo dõi, và chỉ "suggest consideration of treatment" nếu ≥ 40 tuổi hoặc ≥ F2 (slide 21). Giá trị 20.000 của AASLD chỉ là ngưỡng **điều trị** chắc chắn khi ALT ≥ 2×ULN.
2. `population.comorbidity` thiếu một số yếu tố của 1740 tr.PDF 20. Nếu có các yếu tố này, ngưỡng Việt Nam là "trên ngưỡng phát hiện", không phải 2000: suy giảm miễn dịch, biểu hiện ngoài gan, tái phát sau ngưng thuốc, đái tháo đường hoặc gan nhiễm mỡ chuyển hóa (MASLD).
3. `superseded` 3310 thiếu nhánh 2 (> 30 tuổi, ALT > ULN kéo dài, HBV DNA > 20.000 bất kể HBeAg). Không đổi trạng thái, nhưng cần ghi cho đủ.

**Cách sửa:**
- `population.alt` → "ALT ≥ 2×ULN".
- `population.comorbidity` → "không đồng nhiễm HIV/HCV/HDV, không ĐTĐ/MASLD, không suy giảm miễn dịch, không biểu hiện ngoài gan, không tiền sử gia đình HCC/xơ gan, không tái phát sau ngưng thuốc".
- Thêm vào `superseded[0].values`: `{"lo":20000,"hi":20000,"unit":"IU/mL","cmp":">","text":"> 20.000 IU/mL nếu > 30 tuổi, ALT > ULN kéo dài (3310/2019, nhánh 2)"}`.
- Thêm span tương ứng vào `extraction.superseded_spans`: tr.7, `visual_transcription_scan`, nguyên văn đã dẫn ở đầu file.
- Mồi 200 = `mirror_geom`: đúng.

### P-hbv-04 — Mức ALT (bội số ULN) để khởi trị, kiểu cat · **verdict: fix** (quần thể + regex; trạng thái giữ `indistinguishable`)

**Đã kiểm, đúng:**
- VN `gt_1x_uln`: tr.PDF 20.
- 3310 `gt_2x_uln`: ảnh tr.7.
- 5448 `gt_2x_uln`: tr.4.
- AASLD `gt_2x_uln` cho pha immune active: slide 4, 21, 25.
- WHO 2024 `gt_1x_uln`: tr.35.

**Vấn đề:**
1. Quần thể "HBeAg bất kỳ, HBV DNA > 2.000, người lớn ≥ 18" làm giá trị nước ngoài và giá trị bản cũ **không duy nhất**:
   - (a) AASLD Recommendation 4 (slide 24) và Figure 3 (slide 25): HBeAg−, DNA ≥ 2.000, ALT < 2×ULN → "consider treatment based on shared decision-making". Tức là với HBeAg− AASLD **không** giữ cứng 2×ULN.
   - (b) AASLD Figure 2 (slide 21): HBeAg+, ALT 1–<2×ULN → cân nhắc điều trị nếu ≥ 40 tuổi.
   - (c) 3310 nhánh 2: người > 30 tuổi chỉ cần ALT > ULN kéo dài (kèm DNA > 20.000). Khi đó giá trị bản cũ **trùng** giá trị Việt Nam, và không còn lệch phiên bản.
2. Regex thiếu các cách viết: "gấp đôi", "double", "more than 2 times", ">2ULN", "> 2 ULN". Tôi đã chạy `nv.parse_cats`: cả năm cách viết đều trả tập rỗng.
3. `decoy` rỗng thì mẩu này **không có câu trắc nghiệm** (prereg §6.5). Xử lý cũng không nhất quán với 01, 02, 03, 10: các mẩu đó giữ mồi dù `check_decoy` báo cùng lỗi.

**Cách sửa:**
- Chốt `population`: `hbeag` → "dương tính"; `age` → "18–30 tuổi"; `hbv_dna` → "≥ 20.000 và ≤ 10.000.000 IU/mL"; giữ "không ≥ F2"; `comorbidity` như mẩu 03.
  - Với quần thể này: VN `gt_1x`; 3310 và 5448 `gt_2x`; AASLD `gt_2x` (ALT 1–<2×ULN thì theo dõi, vì < 40 tuổi và < F2); WHO 2024 `gt_1x`; WHO 2015 không có khuyến cáo điều trị cho ≤ 30 tuổi.
- Thêm vào `cat_options.gt_2x_uln`: `"gap doi"`, `"double"`, `"more than\\s*(2|two)\\s*times"`, `"[>≥]\\s*2\\s*(x|×)?\\s*uln"`.
- Sau khi sửa `check_decoy` (Vấn đề chung B): đặt `decoy` = `[{"label":"gt_3x_uln","text":"ALT ≥ 3×ULN"}]`.
  - Ghi chú: 1740 tr.PDF 28 có "> 3 lần mức tăng ban đầu", nhưng đó là định nghĩa đợt bùng phát (so với mức ban đầu, không so với ULN), nên không trùng khái niệm.

### P-hbv-05 — FibroScan cho ≥ F2 · **verdict: fix** (nhỏ)

**Đã kiểm, đúng:**
- VN > 7 kPa: tr.PDF 18, 19; Phụ lục 2 tr.PDF 37 ghi "F2: >7,0 và ≤ 9,5 Kpa".
- WHO 2024 > 7 kPa: tr.35, 46, 78.
- 3310 7,0: ảnh tr.16.
- Trạng thái `concordant`: đúng.

**Vấn đề:**
- WHO 2024 ghi ngưỡng kPa kèm "(adults)" (tr.46, 84) và nêu rõ ngưỡng APRI/TE "have not yet been validated for children and adolescents" (tr.47). Mẩu lại ghi quần thể "≥ 12 tuổi".
- Locator "PDF tr.80" không chứa 7 kPa (7 kPa ở tr.78–79).

**Cách sửa:**
- `population.age` → "người lớn (≥ 18 tuổi)".
- `foreign[0].locator` → "…PDF tr.35 (in xxix); tr.46; tr.78".

### P-hbv-06 — NA đơn trị ưu tiên · **verdict: fix** (nguồn AASLD + cấu hình chấm; trạng thái giữ `concordant`)

**Đã kiểm, đúng:**
- VN {TDF, TAF, ETV}: tr.PDF 40 ("Phác đồ ưu tiên: TDF hoặc TAF hoặc ETV"). Bảng 3 tr.PDF 22–23 nhất quán.
- WHO 2024 {TDF, ETV}: tr.36 ("preferred regimens"); tr.46 ghi "ETV or TAF" cho người loãng xương hoặc bệnh thận.

**Vấn đề:**
1. Mục AASLD **sai phiên bản và sai ngữ nghĩa**. Slide 5–6 có tiêu đề "Chronic HBV: Available Treatment Options" và chú thích "Adapted from Table 1 in Terrault N, et al. … AASLD 2018 Hepatitis B Guidance". Tức là:
   - đây là bản **2018**, không phải 2025;
   - danh sách là thuốc "**có sẵn**" (gồm cả Peg-IFN), không phải "ưu tiên đầu tay".
   - Trong bộ slide, câu duy nhất về "preferred" gắn với 2025 là slide 29: "TAF hoặc ETV" cho người **có bệnh thận**, tức một quần thể khác.
2. **Lỗi chấm** (`nv.parse_drugs` với `configs/grading.yaml`): các cách viết sau đều trả tập rỗng:
   - "tenofovir alafenamide", "tenofovir disoproxil" (viết bằng dấu cách, không kèm TAF/TDF);
   - "Tenofovir disoproxil fumarat", "Tenofovir alafenamid fumarat" (cách viết Việt);
   - "Viread", "Vemlidy", "Baraclude".
   Chỉ nhận dạng viết tắt, dạng có gạch nối, hoặc "tenofovir disoproxil fumarate" (tiếng Anh).
3. Chi tiết nhỏ: `superseded` 3310 ghi TAF là đầu tay. Ảnh tr.8 cho thấy chú thích ** của 3310 chỉ ưu tiên TAF cho người > 60 tuổi, loãng xương hoặc suy thận. Với quần thể của mẩu (không bệnh thận/xương), tập đúng của 3310 là {TDF, ETV}. Không đổi trạng thái.

**Cách sửa:**
- Mục AASLD: hoặc **bỏ** (WHO 2024 đã đủ cho mẩu đối chứng); hoặc đổi thành:
  - `source` → "AASLD 2018 Hepatitis B Guidance (Terrault et al., Hepatology 2018) Table 1, as reproduced in AASLD 2025 educational slide set";
  - `version_date` → "2018";
  - `locator` → "slide 5–6 'Available Treatment Options' (không phải danh sách ưu tiên)".
- `superseded[0].values` (3310) → bỏ TAF, ghi chú điều kiện.
- Đề xuất cho `configs/grading.yaml` (tôi không sửa):
  - `tenofovir-disoproxil`: thêm `tenofovir disoproxil`, `tenofovir disoproxil fumarat`, `viread`;
  - `tenofovir-alafenamide`: thêm `tenofovir alafenamide`, `tenofovir alafenamid`, `tenofovir alafenamid fumarat`, `vemlidy`;
  - `entecavir`: thêm `baraclude`.
  - Kiểm lại bằng test trước khi đóng băng câu hỏi.

### P-hbv-07 — Thời gian HBV DNA không phát hiện trước khi ngừng NA, HBeAg âm tính · **verdict: fix** (giữ `conflict`, nhưng cần ghi đúng ngữ cảnh)

**Đã kiểm, đúng:**
- VN "ít nhất 3–4 năm và HBsAg định lượng < 100 IU/ml": tr.PDF 24, khớp nguyên văn. Đi kèm các điều kiện: không F3/F4, có điều kiện theo dõi lâu dài, và câu mở "có thể cân nhắc ngừng".
- AASLD "HBV DNA undetectable for a minimum of 2 years", kèm "HBsAg level <100 IU/mL": slide 33, đã grep.
- 3310 "dưới ngưỡng và mất HBsAg": ảnh tr.9, chép đúng.
- 5448 "3 lần xét nghiệm liên tiếp cách nhau mỗi 6 tháng": tr.4.
- `finalize()`: `conflict`, tolerance 0,5. Mồi 5 năm = `mirror_arith` (2·3,5 − 2).

**Vấn đề:**
1. Khuyến cáo **chính** của AASLD 2025 (Recommendation 5, slide 32, có trích Ghany 2025): *không* ngừng NA ở HBeAg− không xơ gan cho tới khi mất HBsAg. Điều này **trùng quy tắc của 3310/2019**. Mốc "≥ 2 năm" chỉ là một tiêu chí trong danh sách cho người "có mong muốn mạnh" ngừng thuốc, quyết định chung (slide 33).
2. Slide 33 **không có dòng trích nguồn** (slide 4, 21, 25, 32 đều có). Toàn văn Ghany 2025 bị 403, nên việc quy "2 năm" cho AASLD 2025 chưa kiểm được đầy đủ.
3. Ô số chỉ bắt được tiêu chí phụ của AASLD. Câu trả lời "không ngừng cho tới khi mất HBsAg" (trùng cả AASLD lẫn 3310) sẽ không quy được nguồn.
4. `vn[0]` thiếu `cmp` cho "ít nhất".
5. Mồi 5 năm trùng một phương án nhiễu **sai** trong câu đố AASLD (slide 30–31, "undetectable for >5 years"). Đó không phải khuyến cáo, nên chấp nhận được, nhưng cần ghi lại.
6. EASL 2025 được chính 1740 trích (tr.PDF 42, TLTK 10) và có thể là gốc của quy tắc "3–4 năm + qHBsAg < 100". Chưa đọc được. Nếu EASL ghi 3 năm, hệ EU_UK sẽ **concordant**.

**Cách sửa:**
- `foreign[0].locator` → "slide 33 'Criteria for discontinuing antiviral therapy' (áp dụng cho người muốn ngừng thuốc, quyết định chung); slide 32 Recommendation 5: không ngừng NA trước khi mất HBsAg".
- `foreign[0].verified_by` → "needs_human_check" (quy nguồn slide 33 về Ghany 2025 chưa kiểm được trên toàn văn).
- `population`: thêm `"preference": "người bệnh mong muốn ngừng thuốc; có điều kiện theo dõi định kỳ lâu dài"`.
- `vn[0]` thêm `"cmp": ">="`.
- Đề xuất thêm một mẩu cat anh em: "điều kiện ngừng NA (HBeAg−, không xơ gan)", với VN 1740 = {DNA dưới ngưỡng ≥ 3–4 năm + qHBsAg < 100}; 3310 = {mất HBsAg}; AASLD Rec 5 = {mất HBsAg}. Mẩu này sẽ `indistinguishable`, nhưng cho biết mô hình bám AASLD/3310 bao nhiêu.
- Tùy chọn: ghi 5448 (≥ 1 năm, suy từ 3 lần xét nghiệm cách 6 tháng) vào `superseded` kèm ghi chú "giá trị suy ra". Tôi đã tính: trạng thái vẫn `conflict` (khoảng cách 1 = 2·tol, không nhỏ hơn).

### P-hbv-08 — Ngưỡng HBV DNA khởi trị, HBeAg âm tính · **verdict: fix** (**trạng thái sai**: `conflict` → `indistinguishable`, hoặc đổi thành mẩu đối chứng)

**Đã kiểm, đúng:**
- VN > 2000: tr.PDF 20.
- AASLD ≥ 2.000: slide 4, 25, 29.
- WHO 2024 > 2000: tr.35.
- WHO 2015 > 20 000: tr.22, **chỉ áp dụng** cho "aged more than 30 years (in particular)" và "persistently abnormal ALT".
- 3310 ≥ 2.000: ảnh tr.7.
- 5448 ≥ 2.000: tr.4.

**Vấn đề:** với quần thể đang ghi ("người lớn ≥ 18", "ALT tăng trên ULN"), tập giá trị 3310 thực ra là **{≥ 2.000 (ALT > 2×ULN), > 20.000 (> 30 tuổi, ALT > ULN kéo dài, nhánh 2, ảnh tr.7)}**. Giá trị WHO 2015 (> 20.000) trùng nhánh 2. Tôi đã thêm giá trị này vào `superseded` rồi chạy `finalize()`: ra `indistinguishable`. Cũng vì vậy, câu "chỉ xung đột với WHO 2015, không trùng bản cũ" trong báo cáo là sai.

**Cách sửa (chọn một, ghi DECISIONS):**
- **(A, mặc định, bảo thủ):**
  - Thêm vào `superseded[0].values`: `{"lo":20000,"hi":20000,"unit":"IU/mL","cmp":">","text":"> 20.000 IU/mL nếu > 30 tuổi, ALT > ULN kéo dài, bất kể HBeAg (3310/2019, nhánh 2)"}`.
  - Thêm span tr.7 vào `superseded_spans`.
  - `conflict_status` → `indistinguishable` (qua `finalize`).
  - `conflict_family` → "hbv_dna_threshold_20000_age30".
- **(B, đổi thành mẩu đối chứng sạch):**
  - `population.age` → "18–30 tuổi"; `population.alt` → "ALT ≥ 2×ULN".
  - Bỏ mục WHO 2015, vì WHO 2015 không có khuyến cáo điều trị cho ≤ 30 tuổi (tr.22 xếp nhóm này vào "theo dõi").
  - Kết quả: VN = AASLD = WHO 2024 = 3310 = 5448 = 2.000, tức `concordant` (tôi đã chạy `finalize` khi bỏ WHO 2015: `concordant`). Bỏ mồi.
- Không khuyên dựng xung đột hẹp "> 30 tuổi, ALT ≥ 2×ULN" chỉ với WHO 2015. Quy nguồn quá mong manh, vì nhánh 2 của 3310 cũng dùng 20.000 cho người > 30 tuổi.

### P-hbv-09 — FibroScan cho F4 · **verdict: fix** (nhỏ)

**Đã kiểm, đúng:**
- VN > 12,5 kPa: tr.PDF 18, 19; Phụ lục 2 tr.PDF 37 ghi "F3: > 9,5 và ≤ 12,5; F4: > 12,5".
- WHO 2024 > 12.5 kPa: tr.34, 35, 78, 80.
- 3310 ≥ 11 KPa: ảnh tr.16.
- 5448 > 14,6 kPa: tr.9, lớp chữ.
- Trạng thái `concordant`, lệch phiên bản hai bước: đúng. tolerance 0,75 đúng.

**Vấn đề:** như mẩu 05, ngưỡng kPa của WHO chỉ dùng cho người lớn.

**Cách sửa:** `population.age` → "người lớn (≥ 18 tuổi)".

### P-hbv-10 — APRI cho F4 · **verdict: pass** (kèm ghi chú về mồi)

**Đã kiểm, đúng:**
- VN > 1: tr.PDF 18, 19; Phụ lục 2 tr.PDF 37 ghi "F4 : >1".
- WHO 2024 "APRI score of >1": tr.35.
- WHO 2015 "APRI score >2 in adults": tr.22.
- 3310 F4 ≥ 2: ảnh tr.16.
- 5448 F4 > 2: tr.9.
- Quần thể người lớn: đúng. Trạng thái `indistinguishable` (WHO 2015 = bản cũ): đúng.

**Ghi chú:**
- Mồi 0,5 (`mirror_geom`) trùng ngưỡng F2 của chính 1740, WHO 2024 và 3310. Không có mồi thay thế theo quy tắc: `mirror_far` cho giá trị ≤ 0.
- Mẩu này sẽ có câu trắc nghiệm (có giá trị bản cũ), nên cần ghi trong bảng QC trắc nghiệm rằng lựa chọn mồi là một ngưỡng thật (của F2).
- Đơn vị "index" đã tính được `_gap`/tolerance (tôi đã chạy). Đề xuất thêm alias vẫn nên làm để chấm câu trả lời.

---

## 2. Kiểm mục "Sai lệch so với bộ hạt giống" và các khẳng định khác của báo cáo

| Khẳng định trong báo cáo | Kết quả kiểm | Bằng chứng tôi tự tạo |
|---|---|---|
| (4.1) Dòng 20 không sạch vì 3310 = AASLD (35/25; > 2×ULN; ≥ 20.000 HBeAg+) | **Đúng** | Ảnh 3310 tr.4 và tr.7; AASLD slide 4/21/25. Được tăng cường bởi 1740 tr.PDF 15 (thay đúng câu định nghĩa ULN ở mục cấp) |
| (4.2) Giá trị bản cũ 3310 đã tra đủ | **Thiếu** | Bỏ sót nhánh 2 của mục 2.4.2 (> 30 tuổi, ALT > ULN kéo dài ≥ 3 lần/24–48 tuần, HBV DNA > 20.000 bất kể HBeAg). Ảnh hưởng 03, 04, **08** |
| (4.3) Mô tả AASLD của dòng 20 "đúng" | **Đúng một phần** | Đúng cho định nghĩa pha immune active. Thiếu Recommendation 4 (HBeAg−, pha không xác định: gợi ý điều trị theo quyết định chung) và mốc ≥ 40 tuổi ở Figure 2 |
| (4.4) Tiêu chí xơ hóa F2 là đối chứng | **Đúng** | WHO 2024 tr.35; 3310 ảnh tr.16 |
| (4.5) 6 lệch phiên bản thật (01, 02, 03, 04, 09, 10) | **Đúng có điều kiện** | 04 chỉ lệch phiên bản khi ≤ 30 tuổi (nhánh 2 của 3310) |
| Kết quả "2 conflict" (07, 08) | **Sai** | Sau sửa chỉ còn 1 (07). 08 thành `indistinguishable` hoặc `concordant` |
| (4.6) Dòng 21: 1740 tuần thai 14; 3310 tuần 24–28; 1740 dẫn 678/2025 | **Đúng** | 1740 tr.PDF 41 ("từ tuần thai thứ 14", "≥200.000 IU/mL hoặc HBeAg dương tính"); "678" ở tr.PDF 26, 35, 42; ảnh 3310 tr.14 ("Dùng TDF từ tuần 24 - 28"). Báo cáo bỏ sót một tiêu chí khác của 3310: "HBsAg định lượng > 10⁴ IU/mL" |
| (4.7) `data/raw/3310_2019.pdf` sai nhãn (thực là 5448) | **Đúng; nghiêm trọng** | `--find 3310/2019`: có câu của 5448, không có "35 U/L", "Trên 30 tuổi", TAF, "2.4.2". Mọi lệnh `verify_span … 3310/2019` hiện đọc sai văn bản |
| (4.8) 1740 dẫn AASLD 2018 và EASL 2025 | **Đúng** | 1740 tr.PDF 42, TLTK 8 và 10 |
| 1740: danh tính, 42 trang, Điều 3 thay 3310 | **Đúng** | tr.PDF 1 (Điều 3; dòng ký số "17/06/2026 … 1740 16 6"). Số trang in = trang PDF − 11 (kiểm ở tr.18/7, 24/13, 40/29) |
| 3310 Điều 2 bãi bỏ 5448/2014 | **Đúng** | Ảnh 3310 tr.2 |
| EASL 2025 không truy cập được | **Đúng** | Europe PMC: không truy cập mở, không có trong PMC |
| Nguồn AASLD là "Ghany et al., Hepatology 2025" | **Cần chuẩn hóa** | Europe PMC: tiêu đề "AASLD ISDA Practice Guideline on treatment of chronic hepatitis B"; đăng điện tử 2025-11-04; bản in Hepatology 2026;83(4):974–997; PMID 41186418. Toàn văn trả 403 |
| (5.6) "Mồi 01 trùng ULN nữ; mồi 10 trùng ngưỡng F2" | **Đúng** | Đã chạy lại. Với 01 có phương án dự phòng định trước (26 U/L); với 10 thì không có |
| (6.3) `check_decoy` báo động giả | **Đúng** | Khi bỏ mồi, 01, 02, 03, 10 vẫn `indistinguishable` |

---

## 3. Vấn đề chung

**A. Kho văn bản (việc của corpus-librarian / HG2.3):**
- `3310_2019.pdf` sai nhãn và đang được `pdf_path("3310/2019")` dùng. Cần:
  - đánh dấu file này không hợp lệ;
  - chọn `3310_2019__c43006cb.pdf` (bản quét chính thức, Sở Y tế TP.HCM, CV 4238/SYT-NVY) làm bản chuẩn và OCR nó. `data/interim/ocr/` đã có 3377_2023 và TT51_2017, tức là đường OCR đã tồn tại;
  - thêm 5448/2014 (superseded_by 3310/2019) vào manifest.
- Cho tới khi OCR xong, mọi `superseded_spans` 3310 (`visual_transcription_scan`) phải qua HG1.2. Tôi đã đọc bằng mắt từng span, **chép đúng**, nhưng tôi là AI, không thay được người kiểm.

**B. Mã (đề xuất, tôi không sửa):**
- `check_decoy` nên chỉ báo lỗi "mồi làm mẩu thành indistinguishable" khi trạng thái **có** mồi khác trạng thái **không** mồi. Nếu không sửa, `pilot_merge.check()` sẽ loại 01, 02, 03, 10. Đồng thời 04 đang bị để trống mồi vì cùng lý do.
- `check_decoy` nên so mồi với giá trị của các mẩu **cùng `conflict_family`/cùng span** (ví dụ ULN nam/nữ, APRI F2/F4), để bắt mồi trùng giá trị thật ở slot anh em.
- Prereg §6.4 chỉ mô tả `mirror_decoy(auto)` cho mẩu num. Code (`choose_decoy`) có thêm dự phòng `mirror_geom` → `mirror_far` qua `check_decoy`. Cần thống nhất và ghi `docs/DECISIONS.md` trước khi đăng ký.

**C. Cấu hình chấm:**
- Thiếu tên INN viết đầy đủ, cách viết tiếng Việt và biệt dược cho TDF, TAF, ETV (mẩu 06).
- Regex của 04 thiếu "gấp đôi", "double", "more than 2 times", ">2ULN".
- Đề xuất `copies/ml` và `index` như báo cáo nêu: tôi đồng ý.

**D. Metadata AASLD (áp dụng cho 01, 02, 03, 04, 07, 08):**
- Nên ghi `version_date` = "2025-11-04" và tên nguồn theo tiêu đề chính thức (Hepatology 2026;83(4):974–997, PMID 41186418). Cần kiểm bằng `scripts/verify_citations.py` (T2.8) trước khi đưa vào bài.
- Mọi giá trị AASLD chỉ đọc từ bộ slide giáo dục chính thức. Các slide có dòng trích Ghany 2025 là 4, 7, 21, 25, 32. Slide 33 không có. Slide 5–6 là AASLD 2018.
- Cần một lần đối chiếu toàn văn qua người dùng hoặc thư viện (HG).

**E. Quần thể:**
- Các mẩu tiêu chí điều trị (03, 04, 08) phải chốt tuổi (≤ 30 hoặc > 30; < 40 hoặc ≥ 40), mức ALT (≥ 2×ULN hay 1–2×ULN), khoảng HBV DNA và **toàn bộ** các yếu tố nguy cơ của 1740 tr.PDF 20.
- Lý do: ba nguồn (3310 nhánh 2, WHO 2015, AASLD 2025) đều có nhánh phụ thuộc tuổi hoặc ALT.
- Ngưỡng kPa/APRI của WHO chỉ dành cho người lớn (05, 09).

**F. Hệ EU_UK trống ở cả 10 mẩu:**
- EASL 2025 được chính 1740 trích, và có thể là gốc của các giá trị mới (ví dụ quy tắc ngừng NA "3–4 năm + qHBsAg < 100").
- Thiếu EASL nên chưa thể nói xung đột của 07 là "chỉ với Mỹ" hay "với Mỹ, còn EU đồng thuận". Cần người dùng cung cấp PDF chính thức (HG).

**G. Không kiểm được do hết hạn mức tìm kiếm (200/200):**
- (i) 1740/2026 có bị sửa hoặc thay sau 17/6/2026 không.
- (ii) WHO có cập nhật HBV 2025/2026 không.
- Mức chắc chắn hiện tại: dòng ký số ngày 17/6/2026 và Điều 3 thay 3310 là nhất quán; không có bằng chứng về văn bản thay thế.

**H. Hệ quả cho kế hoạch:**
- Với chủ đề HBV, sau kiểm toán chỉ còn **1 mẩu xung đột** (07) có thể dùng cho H1. Mẩu này dựa trên tiêu chí phụ của AASLD, và ô số không bắt được khuyến cáo chính (Rec 5).
- 6 mẩu `indistinguishable` (01, 02, 03, 04, 10, và 08 nếu chọn phương án A) vẫn có giá trị cho mô tả nhãn 3/4 và cho trắc nghiệm.
- Nên cập nhật dòng 20 trong `seed_conflicts.yaml` từ `status: confirmed` thành "indistinguishable (trùng 3310/2019)". Việc này để người dùng quyết định ở HG1.2; tôi không sửa file hạt giống.
