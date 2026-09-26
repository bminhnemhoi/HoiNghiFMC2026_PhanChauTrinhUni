# Kiểm toán độc lập — thí điểm Đối chứng liên chuyên khoa (ID = controls)

Ngày: 2026-09-26 · Người kiểm: integrity-auditor (AI; có góc nhìn bác sĩ lâm sàng do AI đóng vai, **không phải bác sĩ thật**)
Đối tượng: `data/interim/pilot/controls.jsonl` (9 mẩu, ghi 11:26) và `data/interim/pilot/controls_report.md` (ghi 11:28).
Nguyên tắc: không tin báo cáo, tự chạy lại mọi kiểm tra. Chỉ đọc dữ liệu; chỉ ghi file này. Không gán trường chỉ-bác-sĩ.

## 0. Kết luận nhanh

| atom_id | verdict | Lý do chính (ngắn) |
| --- | --- | --- |
| P-controls-01 | **fix** | Giá trị đúng (VN tr.12 = GOLD 2026). Ghi chú gọi nhầm bản cũ là 3874/2018 (thực chất 4562/2018). Câu trả lời "FEV1/FVC < 0,7" hiện bị chấm nhãn 5, nên mẩu đối chứng sẽ bị chấm sai nếu không sửa |
| P-controls-02 | **fix** (nhỏ) | Giá trị đúng. Chỉ sửa ghi chú bản cũ (4562/2018 tr.28) |
| P-controls-03 | **fix** (nhỏ) | Giá trị đúng. Sửa ghi chú bản cũ. Thêm vị trí GOLD tr.103 ("up to 5 days") |
| P-controls-04 | **fix** | Ngưỡng 300 trùng GOLD. Nhưng quần thể/slot chưa đủ chặt: cùng đoạn có ngưỡng ≥ 100. Cần ghi thêm khác biệt về can thiệp (GOLD 2026 không khuyến khích LABA+ICS; VN vẫn nâng bậc lên ICS/LABA) |
| P-controls-05 | **fix** (nhỏ) | Giá trị đúng; tôi đã đọc lại trang CDC. `verified_by: "auto"` sai thực tế (đọc bằng WebFetch, không có sha256) → `null` |
| P-controls-06 | **fix** | Liều 2 g đúng và đối chứng đứng vững. Nhưng báo cáo/ghi chú bỏ sót **6101/2019** (Whitmore) và **2147/2026** tr.53 (melioidosis). Hai văn bản này làm mất hai "xung đột" báo cáo nêu (khoảng cách liều, meropenem). Cần thêm DR8 |
| P-controls-07 | **pass** | VN tr.29 = WHO 2010 tr.5 (500 mg). Grep lại được. Không có văn bản Bộ Y tế nào khác cho giá trị khác |
| P-controls-08 | **fix** | Xung đột là thật (500 ∉ 3000–6000). Sửa `verified_by` của CDC. Ghi chú thiếu một điểm quan trọng: trang CDC nói 500 IU "appears as effective as higher doses (3,000 to 6,000 IU)" |
| P-controls-09 | **fix** (nặng) | VN 23 và WHO chung 25 đều có nguồn thật. Nhưng: (a) WPRO `verified_by: "auto"` sai (PDF quét); (b) các văn bản Bộ Y tế hiện hành khác dùng 25 cho "thừa cân" ở nhóm người nhiễm HIV/ung thư/thai phụ, nên quần thể phải loại trừ rõ, nếu không DR8 làm mất xung đột; (c) mẩu **không cùng slot** với dòng hạt giống 13 (hạt giống so ngưỡng *béo phì* 25 vs 30); (d) thiếu đối chiếu ADA (tầm soát ĐTĐ) và tham vấn WHO về người châu Á |

**Tổng: pass 1 · fix 8 · reject 0.**
Không mẩu nào sai giá trị. Các lỗi nằm ở ghi chú/nhãn nguồn, độ chặt quần thể, `verified_by`, và thiếu văn bản Bộ Y tế đã có sẵn trong `data/raw`.

**Phát hiện chính mà báo cáo không có hoặc đã lỗi thời:**
1. **6101/2019 (Whitmore) CÓ tồn tại.**
   - File `data/raw/6101_2019.pdf`, sha `a3baf8fa8f119d73…`, do corpus-librarian tải lúc 11:30, tức **sau** báo cáo (11:28). Báo cáo trung thực tại thời điểm viết, nhưng nay đã lỗi thời.
   - Là bản quét, chưa có OCR, nên `verify_span` chưa kiểm được.
   - Tôi xem ảnh PDF tr.4 (tr. in 3) và thấy:
     - "Ceftazidim (lựa chọn ưu tiên): 2g tiêm tĩnh mạch chậm, mỗi 6 - 8 giờ … tối đa 8g/ngày";
     - "Meropenem: 1g truyền tĩnh mạch, mỗi 8 giờ";
     - tấn công "ít nhất hai tuần", duy trì "tối thiểu ba tháng".
   - Ảnh PDF tr.5 (tr. in 4): bảng thời gian 2–8 tuần / 3–6 tháng; TMP-SMX 6-8 mg/kg mỗi 12 giờ; doxycyclin 100 mg/lần × 2 lần/ngày.
2. **2147/2026 (viêm phổi cộng đồng người lớn, hiện hành, có lớp chữ).**
   - PDF tr.53 (tr. in 43), mục 5.4.1.6 Melioidosis: "Ceftazidim 2g TTM mỗi 6h Hoặc meropenem 1-2g TTM trong 3h, lặp lại mỗi 8h"; tấn công 2 tuần; duy trì 3 tháng.
   - File đã có trong `data/raw` từ 11:06, **trước** báo cáo, nhưng không được dùng.
3. **`data/raw/3874_2018.pdf` do chính nhóm controls tải lúc 11:19 thực chất là QĐ 4562/QĐ-BYT ngày 19/7/2018.**
   - Cùng sha `68a2f132…` với `4562_2018.pdf`.
   - PDF tr.4: "Số: 4562/QĐ-BYT … ngày 19 tháng 7 năm 2018". Điều 3 thay thế 3874/2018 và 2866/2015.
   - Mọi chỗ "bản cũ 3874/2018" trong báo cáo và notes P-01…P-04 phải đổi thành 4562/2018. Chưa có bản gốc 3874/2018.
4. **5331/2020 (đột quỵ não, có lớp chữ) đã có trong `data/raw` từ 11:17**, trước báo cáo.
   - PDF tr.26 ghi "Khởi phát triệu chứng < 4.5 giờ" cho rt-PA tĩnh mạch.
   - Báo cáo kết luận "không làm được đột quỵ" mà không nhắc bản này. Manifest (c3_ncd) nghi đề cương nhầm số 3312/2024.

---

## 1. Kiểm lại công cụ, văn bản, nguồn

| Mục | Kiểm bằng | Kết quả |
| --- | --- | --- |
| Schema | `vnsoc.schemas atom` | OK 9/9 ✓ |
| Span | `vnsoc.extract.verify_span` | OK 9/9 ✓ |
| Dung sai / trạng thái / mồi | `finalize`, `mirror_decoy`, `choose_decoy`, `check_decoy` (chạy lại trong Python) | Khớp 9/9 với giá trị đã lưu. P-08: mồi 8500 IU (mirror_arith, tâm VN 4500 → 2·4500−500), tol 1250. P-09: mồi 21 kg/m2, tol 1,0. `check_decoy` = [] ✓ |
| Trường chỉ-bác-sĩ | đọc JSON | Không có `moh_lags_evidence` / `clinical_harm` / `clinician_confirmed` ✓. `context_checked` = pending ở cả 9 mẩu |
| 2767/2023 | sha256sum; `--page 1` | sha `16816ec28c986975…` ✓. 87 trang (đề cương ghi 81) ✓. Điều 3 thay 3874/2018 ✓ |
| 5642/2015 | sha256sum; `--page 3` | sha `541e140fccfa3269…` ✓. "Số: 5642/QĐ-BYT … ngày 31 tháng 12 năm 2015" ✓ |
| 5481/2020 | sha256sum; `--page 11` | sha `305fc9c51d54418f…` ✓. Tr. in 9 ✓. 1353/2021 không nhắc BMI (`--find` → []) ✓ |
| "3874/2018" | sha256sum; `--page 4562/2018 4` | **Sai danh tính** (xem phát hiện 3 ở mục 0) |
| 6101/2019 | ảnh trang 1, 4, 5 (pymupdf → PNG ở scratchpad) | Có thật, bản quét, `text_kind` ≠ ok. Giá trị như phát hiện 1 ở mục 0 |
| GOLD 2026 v1.3 | `sources grep` | sha `fa12e8e2…`. FEV1/FVC < 0.7: tr.15, 18, 32, 40. PaO2 ≤ 55 mmHg (7.3 kPa): tr.87. 40 mg × 5 ngày: tr.114; "up to 5 days": tr.103. ≥ 300 cells/µL: tr.75, 76, 132, 161; ≥ 100: tr.77, 80 ✓ |
| Darwin 2024 | `sources grep` | sha `54cfa18f…`. Ceftazidime (ward) 2 g "6-hourly for at least 14 days"; meropenem (ICU) 1 g 8-hourly (tr.4); eradication "at least a further 3 months" (tr.5). Version 11.0, approved 10/2/24, **review date 10/2/26 đã qua** |
| WHO tetanus 2010 | `sources grep` | sha `637bb6b9…`. "human TIG 500 units" IM/IV; metronidazole "500 mg every six hours" (tr.5) ✓. Không có "3000" |
| WHO tetanus fact sheet | `sources fetch` + grep (tôi tải mới) | sha `d4bf943e…`. Có nhắc TIG nhưng không có liều → WHO 2010 vẫn là nguồn số WHO mới nhất tìm được |
| WHO obesity fact sheet | `sources grep` | sha `dc1d9d01…`, ngày 8/12/2025. Overweight "greater than or equal to 25", obesity ≥ 30 ✓. Không nhắc người châu Á |
| WPRO 2000 | `sources grep` → 0 kết quả (PDF quét); xem ảnh PDF tr.19 | Table 2.2: "Overweight: ≥ 23; At risk 23-24.9; Obese I 25-29.9; Obese II ≥ 30" ✓ (tr. in 18). Văn bản gọi đây là khuyến nghị "provisional" |
| CDC scrub typhus | WebFetch (script bị 403) | "100 mg twice per day" cho người lớn > 45 kg; trẻ < 45 kg 2.2 mg/kg; last reviewed 15/5/2024 ✓ |
| CDC tetanus clinical care | WebFetch | "A single, 500 international unit (IU) dose"; "appears as effective as higher doses (3,000 to 6,000 IU)"; chỉ tiêm bắp; last reviewed 8/9/2026 ✓ |
| ADA 2026 (slide pptx đã cache) | tôi trích XML slide | Không có bảng tiêu chí tầm soát theo BMI. Chỉ có ngưỡng béo phì cho phẫu thuật (≥ 27.5 ở người Mỹ gốc Á, slide 157, 159) → phía US của P-09 **chưa kiểm được** |
| Tìm web rộng | WebSearch | **Hết hạn mức (200/200)**, nên không quét được phiên bản mới (WHO uốn ván, Darwin > 2024, COPD 2131/2026). Trang tin kcb.vn về 2147/2026: không có tin liên quan COPD/đột quỵ |

---

## 2. Từng mẩu

### P-controls-01 — ngưỡng FEV1/FVC sau giãn phế quản chẩn đoán COPD
- **verdict: fix**
- Bằng chứng VN:
  - 2767/2023 PDF tr.12 (tr. in 11): "chỉ số FEV1/FVC < 70% sau test HPPQ".
  - Tr.13 lưu đồ nhắc lại < 70%.
  - Không thấy giá trị khác (ví dụ LLN) cho cùng quần thể trong trang lân cận.
- Bằng chứng nước ngoài: GOLD 2026 tr.15/18/32/40 "post-bronchodilator … < 0.7" ✓. Đúng slot, đúng quần thể. `concordant` đúng.
- Issues:
  1. `extraction.notes` ghi "Bản cũ 3874/2018 (kcb.vn) … (PDF tr.16)". Tệp đó là **4562/2018**. Giá trị "FEV1/FVC < 70%" có ở 4562/2018 tr.16–18 ✓, nhưng sai tên văn bản.
  2. Chấm điểm: tôi chạy `grade_short("Đáp án: FEV1/FVC < 0.7")` → **nhãn 5 (unattributed)**; "< 70%" → nhãn 2.
     GOLD và phần lớn LLM viết dạng tỉ số 0,7, nên mẩu đối chứng sẽ bị chấm sai có hệ thống.
  3. Hiệu lực: 2131/2026 (COPD mới theo đề cương §3.1) vẫn chưa tìm thấy (manifest c4 đã ghi). Đây là rủi ro chung cho P-01…P-04.
- fix:
  - `extraction.notes`: thay "Bản cũ 3874/2018 (kcb.vn) có cùng giá trị 'FEV1/FVC < 70% sau test HPPQ' (PDF tr.16)" → "Bản cũ 4562/2018 (tệp data/raw/3874_2018.pdf = 4562_2018.pdf, sha 68a2f132…; PDF tr.4 'Số: 4562/QĐ-BYT … 19/7/2018', thay 3874/2018 và 2866/2015) có cùng giá trị (PDF tr.16–18)".
  - Chấm điểm (chọn một):
    - (a) sau khi có mã và test: `context` → `{"ratio_percent": 1}`, quy tắc là giá trị không đơn vị ≤ 1 thì ×100 khi đơn vị mẩu là %;
    - (b) quy tắc sinh câu hỏi bắt buộc "trả lời theo %". Ghi vào `extraction.notes` "grading_caveat: tỉ số 0,7".
  - Giữ `conflict_status` = concordant.

### P-controls-02 — PaO2 chỉ định thở oxy dài hạn
- **verdict: fix** (chỉ ghi chú)
- Bằng chứng VN:
  - 2767/2023 PDF tr.23 (tr. in 22) mục 2.4.2: "PaO2 ≤ 55 mmHg hoặc SaO2 ≤ 88% …".
  - Nhánh "PaO2 từ 56 - 59 mmHg … kèm" đã được loại đúng qua `population.comorbidity`.
- Nước ngoài: GOLD 2026 tr.87 "at or below 55 mmHg (7.3 kPa)" ✓. `concordant` đúng.
- Issues:
  - notes ghi "Bản cũ 3874/2018 … (PDF tr.28)" → đúng là 4562/2018 (`--find "55 mmHg"` → [28]).
  - Câu trả lời "7,3 kPa" → nhãn 5 (đã tái hiện). Mức độ thấp vì câu hỏi tiếng Việt thường trả lời mmHg.
- fix: `extraction.notes`: "3874/2018" → "4562/2018 (tệp 3874_2018.pdf, sha 68a2f132…)". Giữ nguyên các trường khác.

### P-controls-03 — thời gian glucocorticoid toàn thân trong đợt cấp COPD
- **verdict: fix** (nhỏ)
- Bằng chứng VN:
  - 2767/2023 PDF tr.31: "30-40 mg/ngày … trong 5-7 ngày" (ngoại trú).
  - Tr.34 (nội trú): "Thời gian dùng: 5-7 ngày, thường không quá 14 ngày". Cùng tập 5–7; "14" là giới hạn trên, không phải giá trị khuyến cáo. Chấm "14 ngày" → nhãn 5, hợp lý.
- Nước ngoài: GOLD 2026 tr.114 "40 mg prednisone-equivalent per day for 5 days" ✓; tr.103 "up to 5 days" (đợt cấp trung bình/nặng).
  5 ∈ [5,7] nên `concordant` đúng. "5 ngày" và "7 ngày" đều chấm nhãn 2.
- Issues:
  - notes ghi bản cũ "3874/2018 … (PDF tr.36, 38)". Đúng là 4562/2018:
    - tr.36: "1mg/kg/ngày. Thời gian dùng corticoid: thường không quá 5-7 ngày";
    - tr.38: "Methylprednisolon 1-2 mg/kg/ngày … không quá 5-7 ngày".
    - Ứng viên lệch phiên bản về **liều** vẫn đúng, nhưng phải ghi 4562/2018.
  - GOLD thực ra là "≤ 5 ngày". Mẩu vẫn là đối chứng, nhưng chỉ trùng ở điểm 5.
- fix:
  - `extraction.notes`: "3874/2018" → "4562/2018".
  - `foreign[0].locator` thêm "; PDF p.103 (up to 5 days, moderate/severe exacerbations)".
  - Tùy chọn: `foreign[0].values[0]` thêm `"cmp": "<="`. Tôi đã kiểm ngữ nghĩa: vẫn chồng tại 5, nên vẫn concordant.

### P-controls-04 — ngưỡng bạch cầu ái toan dự báo đáp ứng ICS
- **verdict: fix**
- Bằng chứng VN, 2767/2023 PDF tr.22–23:
  - Bối cảnh: "Trường hợp bệnh nhân còn đợt cấp sau khi đã điều trị theo phác đồ ban đầu" (tr.22).
  - Rồi tr.23: nâng bậc từ LABA/LAMA đơn trị lên LABA/LAMA hoặc ICS/LABA. ICS/LABA dùng khi "+ tiền sử mắc hen. Bệnh nhân có thể có đáp ứng tốt với ICS khi có bạch cầu ái toan máu ≥300" **hoặc** "+ ≥ 2 đợt cấp trung bình/năm hoặc ≥1 đợt cấp nhập viện, và bạch cầu ái toan ≥ 100".
  - Đây đúng là khung GOLD 2022.
- Nước ngoài, GOLD 2026:
  - ≥ 300 ở tr.75 (khởi trị nhóm E bằng LABA+LAMA+ICS), tr.132 ("could be used to support ICS use"), tr.161 (đỉnh quan hệ liên tục eos–ICS) ✓.
  - ≥ 100 ở tr.77 và tr.80.
  - **Tr.75: "use of LABA+ICS in COPD is not encouraged".**
- Issues:
  1. Slot dễ nhập nhằng: cả VN lẫn GOLD đều dùng ngưỡng 100 ở ngữ cảnh khác. `grade_short("100 tế bào/µL")` → nhãn 5. Nếu câu hỏi không nói rõ "ngưỡng cao/đáp ứng tốt", một câu trả lời hợp lệ theo cả hai nguồn sẽ bị chấm "vô nguồn".
  2. `population` chỉ ghi "giai đoạn ổn định", thiếu bối cảnh nâng bậc do còn đợt cấp.
  3. Khác biệt can thiệp chưa được ghi. VN nâng bậc lên **ICS/LABA**; GOLD 2026 không khuyến khích LABA+ICS mà ưu tiên LABA+LAMA+ICS. Đây là **ứng viên xung đột mới** (kiểu `drugs`; VN theo GOLD 2022), chuyển cho nhóm xung đột. Không ảnh hưởng giá trị 300.
  4. notes ghi "Bản 3874/2018 … ACO (PDF tr.22)" → đúng là 4562/2018 (`--find "300"` → [22, 24, 43]).
- fix:
  - `intervention` → "ngưỡng bạch cầu ái toan máu 'cao' dự báo đáp ứng tốt với ICS (không phải ngưỡng tối thiểu ≥ 100 dùng cho người có đợt cấp thường xuyên)".
  - `population.stage` → "giai đoạn ổn định, cân nhắc thêm ICS do còn đợt cấp khi đang dùng thuốc giãn phế quản tác dụng kéo dài (2767/2023 tr.22–23)".
  - `foreign[0].locator` → "PDF p.132 và p.161 (ngưỡng 300 hỗ trợ dùng ICS); p.75 (khởi trị nhóm E); ngưỡng 100: p.77, p.80".
  - `extraction.notes`: thêm "GOLD 2026 p.75: LABA+ICS not encouraged ↔ VN tr.23 nâng bậc ICS/LABA → ứng viên xung đột drugs, không thuộc mẩu này", và sửa "3874/2018" → "4562/2018".

### P-controls-05 — doxycyclin cho sốt mò, liều mỗi lần
- **verdict: fix** (nhỏ)
- Bằng chứng VN:
  - 5642/2015 PDF tr.63: "Doxycyclin: liều 0,1 g x 2 viên uống chia 2 lần/ngày trong 5 ngày" → 100 mg/lần. Cách hiểu hợp lý: 2 viên 0,1 g/ngày chia 2 lần.
  - Azithromycin dành cho thai phụ, trẻ < 10 tuổi và người chống chỉ định tetracyclin **và** cloramphenicol ✓.
- Nước ngoài: CDC (tôi đã đọc lại bằng WebFetch) "100 mg twice per day" cho người lớn > 45 kg; last reviewed 15/5/2024 ✓. `concordant` đúng.
- Issues:
  1. `foreign[0].verified_by: "auto"` nhưng `page_sha256: null`. Giá trị đọc bằng WebFetch, không kiểm bằng mã → nhãn "auto" sai thực tế.
  2. `population.age` "người lớn (≥ 10 tuổi)" gộp tiêu chí VN (tuổi) với CDC (cân nặng) và dễ gây hiểu nhầm. Trẻ 10–17 tuổi < 45 kg theo CDC là 2,2 mg/kg.
  3. Báo cáo §2/§6 ghi "100 mg x 2 lần/ngày" bị nhãn 5. **Nay không còn tái hiện** (nhãn 2), vì `normalize_vi.py` và `grade.py` đã sửa lúc 11:44.
  4. Span chứa ký tự vùng riêng U+F02D. Qua được vì lưu nguyên văn. `verify_span.norm` chỉ ánh xạ U+F0B3/F0A3/F0B1/F0B4, chưa có F02D.
- fix:
  - `foreign[0].verified_by` → `null`.
  - `foreign[0].locator` → "mục Treatment (người lớn > 45 kg); needs_human_check: đọc bằng WebFetch 26/9/2026 (hai lần, người trích + kiểm toán)".
  - `population.age` → "người lớn"; giữ `weight` "> 45 kg".

### P-controls-06 — ceftazidim cho bệnh Whitmore, liều mỗi lần
- **verdict: fix**
- Bằng chứng VN:
  - 5642/2015 PDF tr.84 (bảng kháng sinh nhiễm khuẩn huyết, dòng B. pseudomallei): "Ceftazidim 2 g/lần, tiêm tĩnh mạch chậm 8 giờ/lần … Meropenem 500 mg/lần" ✓. Lỗi gốc "Imipenem+cisplatin" ✓.
  - **Văn bản chuyên đề bị bỏ sót:**
    - 6101/2019 PDF tr.4 (ảnh): ceftazidim 2 g mỗi 6–8 giờ, tối đa 8 g/ngày; meropenem 1 g mỗi 8 giờ (gấp đôi nếu viêm màng não); ICU ưu tiên carbapenem.
    - 2147/2026 PDF tr.53: "Ceftazidim 2g TTM mỗi 6h Hoặc meropenem 1-2g TTM trong 3h, lặp lại mỗi 8h".
- Nước ngoài: Darwin 2024 tr.4, ceftazidime (ward) 2 g 6-hourly ≥ 14 ngày ✓. Hệ thống OTHER hợp lý.
- Issues:
  1. Liều/lần 2 g **trùng ở cả ba văn bản VN**, nên `concordant` vẫn đúng.
  2. Ghi chú mẩu và báo cáo §3.3–3.4, §4.2 sai theo DR8:
     - "khoảng cách liều khác (8 h vs 6 h)": sai, vì hợp tập VN {8 h; 6–8 h; 6 h} chứa 6 h;
     - "meropenem 500 mg vs 1 g là xung đột thật": sai, vì hợp tập VN {500 mg; 1 g; 1–2 g} chứa 1 g.
     - Như vậy "điều trị Whitmore" gần như là **đối chứng đúng như đề cương** §3.3.
  3. `population` thiếu "không phải ICU". Phác đồ ceftazidime của Darwin là cho khoa thường; ICU dùng meropenem (Darwin và 6101/2019 đều vậy).
  4. Darwin: review date 10/2/26 đã qua → cần kiểm có bản mới (không làm được: hết WebSearch).
- fix (đã thử trong bộ nhớ: `verify_atom` ok, `finalize` → concordant, tol 0, schema ok):
  - `extraction.dr8_sources` = `[{"guideline": "2147/2026", "page": 53, "span": "Ceftazidim 2g TTM mỗi 6h Hoặc meropenem 1-2g TTM trong 3h, lặp lại mỗi 8h."}]`.
  - `extraction.notes`: bỏ câu "KHOẢNG CÁCH liều khác … ứng viên mẩu xung đột riêng", thay bằng:
    - "Khoảng cách liều: 5642/2015 8 giờ; 6101/2019 (PDF tr.4, bản quét, đọc ảnh, chưa OCR) 6–8 giờ, tối đa 8 g/ngày; 2147/2026 (PDF tr.53) 6 giờ → hợp tập VN chứa 6 giờ (DR8), không xung đột.
    - 6101/2019 có trong data/raw (sha a3baf8fa…); khi có OCR thì thêm vào dr8_sources."
  - `population.setting` → "điều trị tại khoa thường (không ICU), không tổn thương thần kinh trung ương".
  - `foreign[0].locator` thêm "; version 11.0, review date 10/2/26 (đã quá hạn — needs_human_check phiên bản mới)".

### P-controls-07 — metronidazol cho uốn ván, liều mỗi lần
- **verdict: pass**
- Bằng chứng VN: 5642/2015 PDF tr.29: "metronidazol 500 mg, truyền TM cách 6 - 8 giờ/lần … thời gian điều trị 7 - 10 ngày" ✓. Tr.28 ghi điều trị tại hồi sức, khớp `population`.
- Nước ngoài: WHO 2010 tr.5 "500 mg every six hours" IV hoặc uống; grep lại được, sha `637bb6b9…` ✓. Đúng slot (liều/lần), đúng hệ thống. `concordant` đúng.
- Đã quét toàn bộ `data/raw`: không có văn bản Bộ Y tế nào khác cho liều metronidazol điều trị uốn ván.
- Ghi chú (không cần sửa):
  - WHO 2010 là "technical note" cho tình huống nhân đạo khẩn cấp.
  - Fact sheet WHO uốn ván hiện hành (tôi đã tải, sha `d4bf943e…`) không có liều, nên đây vẫn là nguồn số WHO mới nhất tìm được.

### P-controls-08 — HTIG điều trị uốn ván, tổng liều
- **verdict: fix**
- Bằng chứng VN:
  - 5642/2015 PDF tr.29: "Globulin miễn dịch uốn ván từ người (HTIG) liều 3000 - 6000 đơn vị tiêm bắp" ✓. SAT ngựa được loại đúng qua `population.product`.
  - Quét `data/raw`: 3312/2015 tr.79 "HTIG … 250 UI" và 3610/2015 tr.133 "SAT 2000 đv" là **dự phòng vết thương**, khác slot. Không có giá trị điều trị khác.
- Nước ngoài:
  - WHO 2010 tr.5 "human TIG 500 units" IM/IV ✓ (grep).
  - CDC (tôi đọc lại bằng WebFetch): "A single, 500 international unit (IU) dose", last reviewed 8/9/2026 ✓.
  - `conflict` đúng: 500 ∉ [3000, 6000], nên hỏi được một câu mà giá trị nước ngoài không đúng theo Bộ Y tế.
- Mồi 8500 IU tái hiện đúng (`mirror_arith`). Không trùng liều HTIG hay SAT nào đã biết.
- Issues:
  1. CDC `verified_by: "auto"` với sha null → sai thực tế.
  2. **Thiếu thông tin lâm sàng quan trọng:** trang CDC nói 500 IU "appears as effective as higher doses (3,000 to 6,000 IU)". Giá trị VN chính là mức liều cao cũ mà CDC nhắc tới.
     Đây là dữ kiện cho HG3.9 (bác sĩ thật). Agent **không** gán `moh_lags_evidence` hay `clinical_harm`.
  3. Dung sai 1250 (quy tắc đăng ký: nửa khoảng cách nhỏ nhất):
     - "2000 IU" → nhãn 2 (đúng VN);
     - "250 IU" → nhãn 4 (foreign).
     - Không phải lỗi mẩu, nhưng nên nêu ở phần chấm (xem Vấn đề chung).
- fix:
  - `foreign[1]` (US): `verified_by` → `null`.
  - `foreign[1].locator` → "mục TIG for tetanus treatment; needs_human_check: WebFetch 26/9/2026".
  - `extraction.notes` thêm "CDC ghi 500 IU 'appears as effective as higher doses (3,000 to 6,000 IU)' → giá trị VN trùng mức liều cao cũ; chuyển HG3.9".

### P-controls-09 — ngưỡng BMI thừa cân/béo phì (người trưởng thành châu Á)
- **verdict: fix** (nặng; nếu không cố định được quần thể thì chuyển thành **reject**)
- Bằng chứng VN:
  - 5481/2020 PDF tr.11 (tr. in 9): "thừa cân hoặc béo phì (BMI ≥ 23 kg/m2)" trong tiêu chí tầm soát ĐTĐ ✓. 1353/2021 không sửa phần này ✓.
  - Cùng giá trị ở:
    - 3087/2020 tr.7 (tiền ĐTĐ, cùng câu);
    - 3087/2020 tr.12: "Thừa cân: BMI 23-25 … Béo phì : BMI ≥ 25-30";
    - 2919/2014 tr.60: "Thừa cân 23 – 24,9; Béo độ 1 25 – 29,9".
- Nước ngoài:
  - WHO fact sheet 8/12/2025: overweight ≥ 25 ✓ (grep).
  - WPRO 2000 Table 2.2: overweight ≥ 23 ✓ (tôi xem ảnh PDF tr.19; grep không đọc được).
  - `conflict` với WHO_global, trùng WHO_WPRO: đúng như đề cương đã sửa nhãn.
- Issues:
  1. WPRO `verified_by: "auto"` là sai. PDF quét, `sources grep` trả 0 kết quả; giá trị đọc bằng mắt.
  2. **DR8, các văn bản Bộ Y tế hiện hành khác dùng 25 cho "thừa cân":**
     - 5968/2021 (HIV/AIDS) tr.100: "Thừa cân: nếu BMI từ 25 - 30";
     - 1768/2026 (dinh dưỡng người bệnh ung thư) tr.28: bảng phân loại theo WHO "Thừa cân 25 ≤ BMI < 30";
     - 5481/2020 tr.55 và 6173/2018 tr.19: bảng tăng cân thai kỳ, "thừa cân (BMI 25–29,9)" trước mang thai.
     - Đây là các quần thể riêng. Nếu câu hỏi chỉ nói "người trưởng thành", DR8 có thể đưa 25 vào tập VN → mẩu thành concordant hoặc indistinguishable.
  3. **Không cùng slot với dòng hạt giống 13.** Dòng 13 so **béo phì** (VN độ I 25–29,9 vs WHO chung ≥ 30). Mẩu này so **thừa cân** (23 vs 25).
     Báo cáo §4.1 chỉ nói "23 khớp cận dưới của dòng 13", nên chưa chính xác (xem mục 3).
  4. Chưa đối chiếu US: bối cảnh span là tầm soát ĐTĐ, mà đối chiếu tự nhiên là tiêu chí tầm soát của ADA 2026 (ngưỡng riêng cho người Mỹ gốc Á).
     Slide ADA đã cache không có bảng này (tôi đã kiểm XML), nên chưa kiểm được. Không ghi giá trị từ trí nhớ.
  5. Chưa tải/kiểm **tham vấn chuyên gia WHO 2004 về BMI ở quần thể châu Á** (văn bản WHO toàn cầu nói riêng về người châu Á). Có thể ảnh hưởng cách gán WHO_global cho quần thể "người châu Á". Cần tải bản chính thức rồi mới ghi.
- fix:
  - `foreign[WHO_WPRO].verified_by` → `null`.
  - `foreign[WHO_WPRO].locator` thêm "; needs_human_check: PDF quét, grep 0 kết quả; kiểm toán viên AI xem ảnh PDF p.19 thấy 'Overweight ≥ 23'".
  - `population` → `{"age": "người trưởng thành", "ethnicity": "người Việt Nam (châu Á)", "setting": "định nghĩa thừa cân/béo phì chung (thang châu Á)", "exclusions": "không mang thai; không thuộc nhóm có hướng dẫn riêng dùng thang WHO chung (người nhiễm HIV — 5968/2021 tr.100; người bệnh ung thư — 1768/2026 tr.28)"}`.
  - `extraction.dr8_sources` (cùng giá trị 23, làm vững tập VN) = `[{"guideline": "3087/2020", "page": 7, "span": "Người trưởng thành ở bất kỳ tuổi nào có thừa cân hoặc béo phì (BMI ≥ 23 kg/m2)"}]`.
    Đã thử trong bộ nhớ cùng `population` mới và WPRO `verified_by: null`: `verify_atom` ok, `finalize` → conflict, tol 1,0, `check_decoy` = [], schema ok.
  - `extraction.notes` thêm:
    - danh mục DR8 ở issue 2;
    - "seed_row 13 được đặt lại slot: hạt giống so béo phì 25 vs 30; mẩu này so thừa cân 23 vs 25";
    - "US (ADA 2026 tầm soát) và tham vấn WHO 2004 về người châu Á chưa kiểm".
  - Nếu người kiểm HG không chấp nhận loại trừ quần thể → **reject**.

---

## 3. Kiểm báo cáo — "Sai lệch so với bộ hạt giống / đề cương"

| Mục báo cáo | Đánh giá | Ghi chú |
| --- | --- | --- |
| §1a "3874/2018 (COPD, bản cũ) … Tải mới" | **Sai danh tính** | Tệp là QĐ 4562/2018 (PDF tr.4). Manifest c4/c5 đã phát hiện. Mọi so sánh "bản cũ" phải ghi 4562/2018 |
| §1a "6101/2019 không tải được / chưa xác nhận tồn tại" | **Lỗi thời** | Có từ 11:30 (sau báo cáo). Văn bản có thật: QĐ 6101/QĐ-BYT 30/12/2019, ký số 07/01/2020 |
| §3.2 "Whitmore: không có giá trị VN về thời gian" | **Sai (nay)** | 2147/2026 tr.53 (có lớp chữ): tấn công 2 tuần, duy trì 3 tháng. 6101/2019 tr.4–5: ≥ 2 tuần, ≥ 3 tháng (3–6 tháng). Darwin: ≥ 14 ngày, ≥ 3 tháng. → **ứng viên đối chứng thời gian**, nên làm |
| §3.3 "meropenem 500 mg vs 1 g là xung đột thật" | **Sai theo DR8** | 6101/2019: 1 g mỗi 8 giờ; 2147/2026: 1–2 g mỗi 8 giờ |
| §3.4 "khoảng cách ceftazidim 8 giờ vs 6 giờ" | **Sai theo DR8** | 6101/2019: 6–8 giờ; 2147/2026: 6 giờ |
| §4.1 dòng 13 | **Chưa chính xác** | Ngưỡng 23 có thật và trùng WPRO. Nhưng hạt giống so ngưỡng béo phì (VN 25 vs WHO 30), còn P-09 so ngưỡng thừa cân. Ngoài ra thiếu các văn bản Bộ Y tế dùng thang WHO chung (5968/2021, 1768/2026). 1768/2026 tr.85 ghi cả "Người lớn (Châu Á): BMI ≥ 25" lẫn "Người lớn (WHO): BMI ≥ 30" trên cùng dòng, nên mẩu béo phì theo đúng hạt giống sẽ gặp rủi ro DR8 |
| §4.2 Whitmore "chỉ đúng một phần" | **Sai (nay)** | Với 6101/2019 và 2147/2026, liều, khoảng cách và thời gian đều trùng Darwin. Đề cương gọi Whitmore là đối chứng là đúng |
| §4.3 đột quỵ | **Thiếu** | 3312/2024 chưa xác minh là đúng, nhưng 5331/2020 có sẵn: PDF tr.26 "< 4.5 giờ" rt-PA. Lớp chữ không có liều mg/kg alteplase (`--find` "0,9"/"0.9 mg"/"0,6" → []), nên phải xem ảnh/bảng |
| §4.4 COPD 2131/2026, 87 trang | Đúng | Vẫn chưa tìm thấy 2131/2026 |
| §4.6 "Imipenem+cisplatin" | Đúng | PDF tr.84, xuất hiện 2 lần |
| §4.7 HTIG xung đột mới | Đúng | Thiếu nhận xét của CDC về liều 3000–6000 (xem P-08) |
| §2/§6 lỗi chấm | Một phần lỗi thời | Đề xuất 1 (bí danh IU) và 4 (tần suất "lần/ngày") **đã có**: "500 đơn vị", "500 units" → IU; "100 mg x 2 lần/ngày" → nhãn 2. Đề xuất 2 (tỉ số ↔ %) và 3 (kPa) **vẫn cần**. Đề xuất 5 (U+F02D) chưa làm |

---

## 4. Vấn đề chung

1. **Nhóm trích không quét `data/raw`/manifest trước khi kết luận "không tìm thấy".** Ba văn bản liên quan đã có trên đĩa trước khi viết báo cáo:
   - 2147/2026 (11:06);
   - 5331/2020 (11:17);
   - 4562/2018 (chính nhóm tải và đặt nhầm khóa, 11:19).

   Đề xuất cho quy trình (skill atomization-protocol / counterpart-matching; tôi không sửa): trước khi trích một chủ đề, chạy quét toàn văn `data/raw/*.pdf` theo tên bệnh và tác nhân, rồi đọc `data/interim/manifest_parts/*.jsonl`.
2. **Nhầm khóa trong `data/raw`.** `data/raw/3874_2018.pdf` là 4562/2018.
   - Không sửa được (thư mục chỉ đọc). Cần người dùng hoặc task T2.x đổi khóa/xóa, hoặc ghi `pdf_choice.json`.
   - Ngoài ra cần HG2.3 quyết định hiệu lực của 4562/2018 so với 2767/2023. Với P-01…P-04 thì giá trị giống nhau, không ảnh hưởng.
3. **`verified_by: "auto"` bị dùng cho giá trị không kiểm bằng mã** (P-05 CDC, P-08 CDC, P-09 WPRO). Thống nhất với các kiểm toán dm/htn/hbv: đặt `null` và ghi needs_human_check trong `locator` cho tới HG.
4. **Hiệu lực chưa đóng:**
   - COPD 2131/2026 (4 mẩu);
   - đột quỵ 3312/2024 (nghi nhầm số);
   - các chương sốt mò/uốn ván/nhiễm khuẩn huyết của 5642/2015;
   - 5968/2021 so với hướng dẫn HIV mới hơn (nếu có).

   WebSearch đã hết hạn mức (200/200) nên kiểm toán không quét rộng được. Chuyển HG1.2/HG2.3.
5. **Chấm điểm** (đề xuất mã, kèm test, không tự sửa):
   - P-01: câu trả lời dạng tỉ số → nhãn 5. Cần `ratio_percent` hoặc ràng buộc câu hỏi.
   - P-02: "kPa" → nhãn 5. Chỉ nên thêm quy đổi khi context đánh dấu khí máu.
   - `verify_span.norm`: thêm U+F02D (và dải U+F0xx dùng làm gạch đầu dòng) → khoảng trắng.
   - Dung sai P-08 (1250) cho "2000 IU" = đúng VN và "250 IU" = nước ngoài. Đây là hệ quả của quy tắc "nửa khoảng cách nhỏ nhất" với tập VN rộng. Nên nêu ở phân tích độ nhạy (skill statistics-plan) thay vì đổi quy tắc sau khi thấy dữ liệu.
6. **Ứng viên mới nên làm** (chưa làm vì kiểm toán chỉ ghi file này):
   - Whitmore thời gian tấn công 2 tuần / duy trì 3 tháng (2147/2026 tr.53 ↔ Darwin tr.4–5): đối chứng.
   - Whitmore liều meropenem (hợp tập VN 0,5 / 1 / 1–2 g ↔ Darwin 1 g): đối chứng.
   - Tiêu sợi huyết < 4,5 giờ (5331/2020 tr.26), nếu HG2.3 xác nhận 5331/2020 là bản hiện hành.
   - COPD: VN nâng bậc lên ICS/LABA (2767/2023 tr.23) ↔ GOLD 2026 tr.75 không khuyến khích LABA+ICS: ứng viên xung đột kiểu `drugs` (VN theo GOLD 2022).
7. **Phiên bản nguồn nước ngoài:**
   - GOLD 2026 v1.3 (8/12/2025) là bản hiện hành tại 26/9/2026 ✓.
   - Darwin: review date 10/2/26 đã qua → kiểm bản mới.
   - WHO uốn ván: fact sheet không có liều, nên WHO 2010 vẫn dùng được, nhưng phải ghi rõ phạm vi "humanitarian emergencies".
8. **Tệp do kiểm toán tạo** (không thuộc data/raw):
   - `data/cache/foreign/d4bf943ec4a4339bee02.html` (fact sheet WHO uốn ván, qua `sources fetch`);
   - ảnh PNG trang 6101/2019 và WPRO chỉ nằm ở scratchpad phiên, không nằm trong dự án.

## 5. Việc cho người kiểm (HG1.2 / HG2.3 / HG3.9)

1. **6101/2019:** chạy OCR (`vnsoc.extract.ocr`) để tạo sidecar. Sau đó thêm span tr.4 vào `dr8_sources` của P-06 và tạo mẩu thời gian/meropenem.
2. **P-09:** chấp nhận hay không việc loại trừ quần thể (HIV/ung thư/thai kỳ). Nếu không, **reject** P-09. Quyết định có làm mẩu "béo phì 25 vs 30" đúng như hạt giống 13 hay không.
3. **Xác nhận bằng trình duyệt:**
   - CDC scrub typhus (15/5/2024) và CDC tetanus (8/9/2026), vì không có sha256;
   - ảnh WPRO 2000 PDF tr.19.
4. **Hiệu lực:** COPD 2131/2026; đột quỵ 3312/2024 so với 5331/2020; 4562/2018 so với 2767/2023; các chương 5642/2015.
5. **P-08** là xung đột cần bác sĩ thật (HG3.9). Dữ kiện: CDC coi 500 IU hiệu quả tương đương liều 3000–6000 IU.
