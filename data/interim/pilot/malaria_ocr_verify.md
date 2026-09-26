# Kiểm toán độc lập — thí điểm Sốt rét từ OCR của QĐ 3377/2023 (ID = malaria_ocr)

Ngày: 2026-09-26 · Người kiểm: integrity-auditor (AI, kiêm góc nhìn bác sĩ lâm sàng Việt Nam do AI đóng vai — **không phải bác sĩ thật**)
Đối tượng: `data/interim/pilot/malaria_ocr.jsonl` (8 mẩu) và `data/interim/pilot/malaria_ocr_report.md`.
Nguyên tắc: không tin báo cáo, tự chạy lại mọi kiểm tra; chỉ đọc dữ liệu; chỉ ghi file này. Không sửa JSONL.

## 0. Kết luận nhanh

| Mẩu | Slot | Trạng thái (tính lại) | Verdict | Lý do chính |
|---|---|---|---|---|
| 01 | first_line · thai 3 tháng đầu | conflict | **fix** | Bỏ sót nguồn DR8: 315/2015 tr. 75 và 3312/2015 tr. 520 (báo cáo nói "không có nguồn DR8"). Câu trả lời chép đúng 3377 (Q+C, không có quinin thì AL) bị chấm nhãn 5 |
| 02 | first_line · P. falciparum, người lớn | indistinguishable | **pass** | Đúng như báo cáo; chỉ dùng làm bản ghi, không dùng cho kiểm định xác nhận |
| 03 | dose · primaquin liều đơn | conflict | **fix** | Quần thể "≥ 15 tuổi" chồng lên phạm vi 3312/2015 (0,6 mg base/kg). `version_date = "trước 2015"` sai định dạng schema |
| 04 | dose · primaquin mg/kg/ngày | conflict | **fix** | Mồi 0,2 nằm trong dung sai của giá trị bản cũ 0,25: chính câu trả lời "0,2" bị chấm **nhãn 3**. "30 mg/ngày" (kiểu CDC, đúng liều/ngày của VN) bị chấm nhãn 5 |
| 05 | duration · primaquin | indistinguishable | **pass** | Đúng như báo cáo |
| 06 | duration · AL | conflict (US) | **pass** | VN 3 ngày = WHO; CDC 2026 là 5 ngày. Chỉ có ghi chú nhỏ |
| 07 | dose · artesunat tiêm, trẻ < 20 kg | conflict (US) | **fix** | Bỏ sót nguồn DR8: 3312/2015 tr. 521 ("Trẻ em < 7 tuổi: 1,5 mg/kg/ngày, 7 ngày"). Chưa ghi WHO bản cũ |
| 08 | dose · artesunat tiêm, người lớn | concordant | **pass** | Đối chứng trùng thật |

**Tổng: 4 pass · 4 fix · 0 reject.** Không mẩu nào đổi trạng thái khi áp các sửa đổi dưới đây (đã chạy `finalize` trong bộ nhớ), nhưng
tập giá trị VN, cách chấm và mồi của 4 mẩu phải sửa trước khi đóng băng.

**Ba phát hiện quan trọng nhất:**

1. **Báo cáo sai về DR8.** Báo cáo (§3.6) viết rằng hướng dẫn nhi khoa của Bộ Y tế "không có trong `data/raw`". Thực tế:
   - `data/raw/3312_2015.pdf` (QĐ 3312/QĐ-BYT, "một số bệnh thường gặp ở trẻ em", manifest: `current`) đã được tải lúc
     11:32, trước khi báo cáo được viết (11:50). Văn bản có chương "SỐT RÉT Ở TRẺ EM" (tr. 517–523).
   - `data/raw/315_2015.pdf` (QĐ 315/QĐ-BYT, sản phụ khoa, `current`, tải lúc 11:25) có mục 2.1.4 "Sốt rét" trong phần
     "Sốt trong khi có thai" (tr. 75).
   - Cả hai có giá trị cho quần thể của mẩu 01 và 07, và chạm tới quần thể của mẩu 03. Chi tiết ở mục 3.
2. **Mồi mẩu 04 không dùng được** (mục 4, mẩu 04).
3. **Bộ chấm có ba lỗi ảnh hưởng trực tiếp tới các mẩu này**: lỗi 7.1 (đã tái hiện), câu trả lời đầy đủ theo VN ở mẩu 01 bị
   nhãn 5, và "30 mg/ngày" ở mẩu 04 bị nhãn 5 (mục 6).

---

## 1. Kiểm lại bằng máy (tự chạy)

| Kiểm tra | Kết quả |
|---|---|
| `vnsoc.schemas atom` | OK 8/8 |
| `vnsoc.extract.verify_span <file>` | OK 8/8 (0 mẩu không đạt) |
| `finalize` (tính lại) | trạng thái và dung sai khớp đúng giá trị lưu ở cả 8 mẩu |
| `check_decoy` | [] ở cả 8 mẩu (nhưng xem mẩu 04: quy tắc hiện hành không bắt được lỗi) |
| `choose_decoy` (num) | 03 → 60 mg (mirror_geom); 04 → 0,2 (mirror_geom); 05 → None; 06 → 1 ngày; 07 → 3,6 mg/kg; 08 → None. Khớp giá trị lưu |
| `pilot_merge.check(atom, drugs, combos)` | [] ở cả 8 mẩu |
| `pilot_merge.source_warnings(atom, block_hashes())` | [] ở cả 8 mẩu |
| `pilot_merge.enforce_decoy_rule` | không đổi mồi mẩu nào |
| Trường chỉ-bác-sĩ | không có (moh_lags_evidence, clinical_harm, clinician_confirmed đều vắng) |
| Độ dài span | 93–287 ký tự (≤ 600) |

sha256 (16 ký tự đầu, tự tính):

| Văn bản | sha256 | Lớp chữ |
|---|---|---|
| 3377/2023 | `aa1792688e9dda03` ✓ khớp báo cáo | OCR (sidecar `data/interim/ocr/3377_2023/`, 23 trang) |
| 2699/2020 | `8bc1a6b403476197` ✓ | lớp chữ |
| 5642/2015 | `541e140fccfa3269` ✓ | lớp chữ |
| 3312/2015 (mới, DR8) | `a66c5e8bc460807c` | lớp chữ |
| 315/2015 (mới, DR8) | `8038358264cdbc64` | lớp chữ |
| CDC Treatment Tables PDF | `7893052505772ec3` ✓ | 7 trang |
| WHO guidelines for malaria 10/9/2026 | `4e2c67b2ec74124e` ✓ | 494 trang |
| WHO 3rd ed. 2015 (bản văn bản IRIS) | `f1bab2b81e7429c3` ✓ | text/plain, không số trang |

## 2. Kiểm ảnh trang OCR (3377/2023)

Tôi xuất lại ảnh (`verify_span --image 3377/2023 N`) và đọc từng trang bằng mắt.

| Trang PDF (in) | Mẩu | Kết quả so ảnh |
|---|---|---|
| 9 (8) | 02 | Khớp: "Pyronaridin tetraphosphat - artesunat (Pyramax) uống 3 ngày (xem Bảng 2 hoặc 3) và primaquin liều duy nhất (xem Bảng 4)". Lỗi OCR chỉ ở chữ ("Sot", "Jalciparum", "uông 3 ngay", "Bang", "hoic", "va", "liêu"), không ở số |
| 10 (9) | 01 | Khớp từng chữ số và tên thuốc: "quinin sulfat 7 ngày (xem Bảng 6) + clindamycin 7 ngày (xem Bảng 7)" và "Trường hợp không có quinin sulfat, có thể dùng artemether - lumefantrin (xem Bảng 10)" |
| 11 (10) | 07, 08 | Khớp: "Trẻ em > 20 kg và người lớn: Liều giờ đầu 2,4 mg/kg, tiêm nhắc lại 2,4 mg/kg vào giờ thứ 12 (ngày đầu)" và "Trẻ em < 20kg liều sử dụng artesunat tiêm là 3mg/kg/lần". OCR "gio" = "giờ" |
| 16 (PL 2) | 03 | Khớp: Bảng 4 "Primaquin (viên chứa 7,5 mg primaquin base)", hàng **"≥ 15 tuổi"** (OCR ghi ">"), cột "P. falciparum, P. knowlesi, P. malariae điều trị 1 lần" = **4 viên**. Bảng 3 Pyramax trên cùng trang ghi "Phụ nữ có thai" trong chống chỉ định (dùng cho mồi mẩu 01) ✓ |
| 17 (PL 3) | 04, 05 | Khớp: "Bán thiếu G6PD (hoạt độ G6PD từ 30 - 70% ...), liều primaquin: 0,25 mg/kg/ngày x 14 ngày. - Không thiếu G6PD: liều primaquin: 0,5 mg/kg/ngày x 7 ngày." |
| 19 (PL 5) | 06 | Khớp: "Bảng 10. Artemether 40mg – lumefantrin 240mg - Uống 2 lần/ ngày, liên tục trong 3 ngày. Hai liều đầu tiên cách nhau 8 giờ." Hàng cân nặng trong ảnh là "≥ 35kg" |

**Kết luận:** không có sai chữ số, đơn vị hay tên thuốc trong 8 span. `ocr_visual_check` của agent đúng.
Với người ở HG1.2: vẫn phải tự so, vì kết luận trên là của AI.

## 3. Kiểm nguồn nước ngoài (grep lại bản đệm, sha khớp)

| Giá trị trong mẩu | Kiểm | Kết quả |
|---|---|---|
| CDC Table 1: AL "Five-day course", A=AL, B=AP "listed in order of preference", chú thích 5 và 7 (p.1–2, "Last Updated: August 11, 2026") | đọc toàn văn PDF đã băm | ✓ (02, 06) |
| CDC Table 2: primaquin 30 mg base qd × 14; trẻ em 0,5 mg/kg × 14; ≥ 70 kg chỉnh tổng liều 6 mg/kg (p.4, June 26, 2026) | như trên | ✓ (04, 05) |
| CDC Table 4: AL "(preferred)"; Q+C; mefloquin (chỉ khi không còn lựa chọn) (p.6, June 26, 2026) | như trên | ✓ (01) |
| CDC Table 5: 2,4 mg/kg IV lúc 0, 12, 24 h; chú thích 2: trẻ < 20 kg dùng 2,4 mg/kg, ghi rõ WHO dùng 3 mg/kg (p.7, August 11, 2026) | như trên | ✓ (07, 08) |
| WHO 2026 p.17: 6 ACT (có ASPY 2022); ACT 3 ngày (2015) | `sources grep` | ✓ (02, 06). WHO p.183 nêu AL 5 ngày ở thai kỳ nhưng "data are insufficient to recommend" → WHO vẫn là 3 ngày ✓ |
| WHO 2026 p.18/183: AL trong 3 tháng đầu (2022, strong) | grep | ✓ (01) |
| WHO 2026 p.18/180: 0,25 mg/kg liều đơn, vùng lan truyền thấp (2026) | grep | ✓ (03) |
| WHO 2026 p.21/207: 7 mg/kg = 0,5 × 14 hoặc 1 × 7 (1 mg/kg chỉ khi G6PD ≥ 70%); 3,5 mg/kg chỉ cho tiểu lục địa Ấn Độ và châu Mỹ | grep | ✓ (04, 05) |
| WHO 2026 p.22/218: trẻ < 20 kg 3 mg/kg; trẻ lớn và người lớn 2,4 mg/kg | grep | ✓ (07, 08) |
| WHO 2015: "therapeutic dose: 0.25-0.5 mg/kg bw per day ... for 14 days" | grep | ✓ (04, 05) |
| WHO 2015 và WHO 2026 p.180: "previously recommended dose of 0.75 mg/kg bw" | grep | ✓ giá trị có trong nguồn (03), nhưng **ngày phiên bản không có trong nguồn** |
| WHO 2015: thai 3 tháng đầu "7 days of quinine + clindamycin" | grep | ✓ (ghi chú ở 01, không ghi vào foreign) |

Không thấy giá trị nước ngoài nào sai hoặc bị gắn nhầm quần thể/slot/phiên bản. `page_sha256` có ở mọi mục.

**Khoảng trống chung (không đổi trạng thái, nhưng ảnh hưởng quy nguồn):** không mẩu nào ghi hệ thống **EU_UK**. Đề cương §3.3
yêu cầu kho đối chiếu gồm cả châu Âu/Anh, và Anh có hướng dẫn điều trị sốt rét riêng. Chưa kiểm được vì hạn mức WebSearch đã cạn.
→ Việc cho counterpart-matcher trước khi đóng băng: tìm bản chính thức (UKHSA/BIA) và ghi giá trị cho 01, 04, 06, 07, 08.
Nếu không tìm được thì ghi rõ "chưa kiểm EU_UK" trong báo cáo.

## 4. DR8 — phát hiện mới (kiểm bằng `--find`, `--page` và ảnh trang)

Tôi quét mọi văn bản hiện hành có thể có nội dung sốt rét: 1493/2015 (hồi sức), 3312/2015 (nhi), 5642/2015 (truyền nhiễm),
315/2015 (sản phụ khoa), 2919/2014 (trạm y tế xã) và 5904/2019.

| Văn bản | Kết quả |
|---|---|
| 1493/2015, 5904/2019 | không có "sốt rét"/"artesunat"/"primaquin" |
| 5642/2015 tr. 33–37 | chỉ nói sốt rét kháng thuốc và thất bại điều trị (second line) → **khác quần thể**. Báo cáo đúng |
| 2919/2014 tr. 253 | "theo phác đồ sốt rét của địa phương" → không có giá trị |
| **315/2015 tr. 75** (in 74), mục "SỐT TRONG KHI CÓ THAI" → 2.1.4 Sốt rét | **có giá trị điều trị cho phụ nữ có thai bị sốt rét** (không phân tam cá nguyệt, loài hay mức độ) |
| **3312/2015 tr. 520–522**, "SỐT RÉT Ở TRẺ EM" (Bảng 1 ghi rõ lấy theo QĐ 3232/QĐ-BYT 2013) | **có giá trị cho trẻ em, và có hàng "Phụ nữ có thai trong 3 tháng"** |

Span nguyên văn (chép từ `--page`, đã kiểm `--find` → đúng trang; ảnh tr. 520, 521 của 3312 và tr. 75 của 315 đã xem, khớp):

| Mã | Văn bản · trang | span_nguyen_van | Giá trị |
|---|---|---|---|
| D-315 | 315/2015 · 75 | `- Xử trí: + Chloroquin liều khởi đầu 10mg/kg cân nặng1 lần/ngày trong 2 ngày, sau đó 5mg/kg ngày thứ 3. + Sulfadoxin /pyrimethamin 3v uống liều duy nhất. + Muối quinine 10mg/kg cân nặng uống 3l/ngày trong 7 ngày` (248 ký tự) | chloroquin; sulfadoxin–pyrimethamin; quinin đơn trị 7 ngày |
| D-3312a | 3312/2015 · 520 | `Phụ nữ có thai trong 3 tháng Quinin + Clindamycin Quinin + Clindamycin Chloroquin Chloroquin Quinin + Clindamycin` (119) | P. falciparum ở thai 3 tháng đầu: quinin + clindamycin (= 3377) |
| D-3312b | 3312/2015 · 520 | `Từ 3 tuổi trở lên DHA-PPQ(1) DHA-PPQ(1) +Primaquin` (57) | trẻ ≥ 3 tuổi, P. falciparum: DHA-PPQ + primaquin |
| D-3312c | 3312/2015 · 521 | `Artesunat tiêm tĩnh mạch hoặc tiêm bắp, lọ 60mg: dùng trong điều trị cấp cứu.` (98) rồi `Trẻ em < 7 tuổi: 1,5 mg/kg/ngày, 7 ngày` (45) | artesunat tiêm, trẻ < 7 tuổi: 1,5 mg/kg/ngày × 7 ngày (**đọc theo vị trí**; văn bản không ghi liều cho trẻ ≥ 7 tuổi) |
| D-3312d | 3312/2015 · 522 | `Primaquine phosphate viên 13.2mg = 7.5mg base: Liều 0,6 mg base / kg / ngày. Để diệt giao bào P. Falciparum: uống 1 ngày cuối của đợt điều trị. Để điều trị P. vivax và P. ovale: dùng 14 ngày` (226) | primaquin 0,6 mg base/kg: liều đơn diệt giao bào; hoặc × 14 ngày cho P. vivax/ovale |

Mô phỏng DR8 (trong bộ nhớ, `finalize` + `check_decoy`):

| Mẩu | Tập VN sau khi hợp | Trạng thái | Mồi |
|---|---|---|---|
| 01 + D-315 | {Q+C, chloroquin, SP, quinin} | vẫn **conflict** (AL nằm ngoài) | Pyramax, check_decoy = [] |
| 07 + D-3312c | {3; 1,5} mg/kg | vẫn **conflict** (US 2,4 nằm ngoài), tol 0,3 | choose_decoy vẫn 3,6 mg/kg |
| 03 + D-3312d (nếu hỏi người 15 tuổi) | {30; 36} mg | vẫn **conflict**, tol đổi thành 4,5 | choose_decoy đổi thành **27 mg** |

Vậy DR8 **không làm mất xung đột**. Nhưng nó đổi tập giá trị đúng khi chấm, đổi mồi ở mẩu 03, và phải được ghi và báo cáo như
kết quả phụ (đề cương, DR8).

Nhận định lâm sàng (AI đóng vai, không phải bác sĩ):

- Chương sốt rét của 3312/2015 lấy theo QĐ 3232/2013, và mục sốt rét của 315/2015 đều **lạc hậu so với 3377/2023**:
  - 315/2015 dùng chloroquin cho P. falciparum ở vùng kháng thuốc;
  - 315/2015 dùng SP trong 3 tháng đầu (antifolat bị chống chỉ định ở tam cá nguyệt 1 theo WHO 2026 p.18);
  - 3312/2015 có một liều artesunat trẻ em không rõ nguồn.
- Tuy vậy, DR8 đã đăng ký trước và không có quy tắc "văn bản chuyên ngành mới hơn thắng". Theo manifest, cả hai văn bản vẫn `current`.
- Vì vậy phải **áp DR8 trung thực** hoặc **ghi quyết định lệch** vào `docs/DECISIONS.md` và addendum (quy tắc cứng 4).
- Đây cũng là một phát hiện có giá trị cho bài báo: **các văn bản Bộ Y tế hiện hành mâu thuẫn nhau về điều trị sốt rét**.

---

## 5. Từng mẩu

### P-malaria_ocr-01 — first_line · P. falciparum chưa biến chứng, thai 3 tháng đầu
- **verdict: fix**
- Đã xác nhận: span khớp ảnh tr. 10. VN = {Q+C}; WHO 2026 = AL (2022, strong, p.18); CDC Table 4 = AL (preferred).
  Trạng thái conflict là thật ở slot "lựa chọn đầu tiên". Mồi Pyramax: 3377 Bảng 3 chống chỉ định "Phụ nữ có thai" (ảnh tr. 16),
  WHO p.17 "not recommended ... first trimester", CDC không có, 2699 và WHO 2015 dùng Q+C; check_decoy = [] ✓.
- **Vấn đề:**
  1. **DR8 bỏ sót** (mục 4): 315/2015 tr. 75 (D-315) và 3312/2015 tr. 520 (D-3312a). `extraction.dr8_sources = []` và câu
     "không có nguồn DR8" là sai.
  2. **Rủi ro chấm.** Chạy `grade_short` với từ điển `grading.yaml`:
     - `"ĐÁP ÁN: quinin + clindamycin; nếu không có quinin thì artemether-lumefantrin"` → **nhãn 5**. Đây là câu trả lời chép
       đúng 3377.
     - Chỉ khi toàn văn có "Bộ Y tế" hoặc "WHO" thì câu này mới được nhãn 1, mà nhãn 1 cũng sai nghĩa.
     - Mẩu này đặc biệt dễ dính lỗi vì chính 3377 có câu dự phòng AL.
  3. Lỗi 7.1 **đã tái hiện**: thêm WHO 2015 (Q+C) vào `foreign` thì câu trả lời Q+C bị nhãn 5. Do đó WHO 2015 phải để ngoài
     `foreign`, trái quy tắc "ghi phiên bản cũ của nguồn nước ngoài khi giá trị khác" (WHO 2015 Q+C ≠ WHO 2026 AL).
- **Fix cụ thể:**
  - Ghi `extraction.dr8_sources` hai dòng D-3312a (values_text "quinin + clindamycin", trùng VN) và D-315 (values_text
    "chloroquin; sulfadoxin–pyrimethamin; quinin đơn trị 7 ngày"). Span lấy đúng như bảng mục 4.
  - Người/bác sĩ quyết định ở HG1.2 xem D-315 (không phân tam cá nguyệt, loài, mức độ; không xếp thứ tự) có tính là "cùng quần
    thể, cùng slot lựa chọn đầu tiên" không:
    - **có** → thêm vào `vn` các mục `{key_drugs:["chloroquine"]}`, `{key_drugs:["sulfadoxine-pyrimethamine"]}`,
      `{key_drugs:["quinine"]}`; trạng thái vẫn conflict (đã mô phỏng);
    - **không** → ghi lý do vào `docs/DECISIONS.md`.
  - Thêm `sulfadoxine-pyrimethamine: [sulfadoxin-pyrimethamin, sp, fansidar]` vào `grading.yaml`.
  - Câu hỏi phải yêu cầu **một** phác đồ lựa chọn đầu tiên. Sửa lỗi 7.1 rồi thêm WHO 2015 vào `foreign`.

### P-malaria_ocr-02 — first_line · P. falciparum chưa biến chứng, người lớn không có thai
- **verdict: pass** (giữ làm bản ghi; indistinguishable nên không vào kiểm định xác nhận)
- Đã xác nhận:
  - span khớp ảnh tr. 9;
  - bản cũ 2699 tr. 6 (DHA-PPQ) `--find` → [6];
  - WHO p.17 có đủ 6 ACT, trong đó có ASPY;
  - CDC Table 1 A = AL, B = AP (chú thích 7 gọi cả hai là "preferred").
- Trạng thái: DHA-PPQ (WHO) trùng bản cũ, nên `conflict_status` = indistinguishable ✓.
- Ghi chú:
  - D-3312b ("Từ 3 tuổi trở lên: DHA-PPQ + Primaquin") nằm trong hướng dẫn **nhi khoa**, nên tôi coi là ngoài quần thể người lớn.
    Nếu người quyết định áp nó cho người lớn thì VN ∪ DHA-PPQ và trạng thái đổi thành conflict. Cần xác nhận cách hiểu phạm vi ở HG.
  - `grading.yaml` vẫn thiếu `amodiaquine`, combo `artesunate-mefloquine`, `artesunate-amodiaquine`,
    `artesunate+sulfadoxine-pyrimethamine`. Hệ quả: "artesunat-mefloquin" và "artesunat + amodiaquin" → nhãn 5 thay vì nhãn 4 WHO.

### P-malaria_ocr-03 — dose · primaquin liều đơn diệt giao bào, P. falciparum, 60 kg
- **verdict: fix**
- Đã xác nhận:
  - Ảnh tr. 16: hàng "≥ 15 tuổi", cột "điều trị 1 lần" = 4 viên × 7,5 mg base = 30 mg ✓.
  - WHO 2026 p.18 ghi 0,25 mg/kg (vùng lan truyền thấp) ✓.
  - "previously recommended dose of 0.75 mg/kg bw" có ở WHO 2015 và WHO 2026 p.180 ✓.
  - Bản cũ 2699 tr. 15 ghi 0,5 mg base/kg, "Từ 15 tuổi trở lên 4 viên uống 1 lần" = VN ở 60 kg, nên không có lệch phiên bản ✓.
  - Chấm thử: "30 mg"/"4 viên"/"0,5 mg/kg" → 2; "0,25 mg/kg"/"15 mg" → 4; "45 mg" → 4; "60 mg" → 5 kèm decoy ✓.
- **Vấn đề:**
  1. `population.age = "≥ 15 tuổi"`. Người 15–< 16 tuổi thuộc phạm vi hướng dẫn nhi 3312/2015, trong đó primaquin là
     **0,6 mg base/kg** liều đơn (D-3312d; = 36 mg ở 60 kg). Nếu câu hỏi dùng tuổi 15 thì DR8 áp dụng: tập VN {30; 36}, và
     choose_decoy đổi từ 60 thành 27 mg.
  2. Mục WHO bản cũ có `version_date = "trước 2015"`. Schema quy định định dạng "YYYY or YYYY-MM-DD" (`schemas.py`, dòng 75);
     chuỗi này qua được máy chỉ vì trường là `str`. Nguồn đã tải chỉ nói "previously recommended", không nêu năm.
     Mục này **không được bỏ**: nếu bỏ, choose_decoy chọn 45 mg, trùng khuyến cáo cũ của WHO (đã chạy).
- **Fix cụ thể:**
  - Đặt `population.age = "người lớn ≥ 18 tuổi (câu hỏi dùng 30 tuổi, 60 kg)"`, để 3312/2015 nằm ngoài quần thể.
  - Ghi vào `notes`: "3312/2015 tr. 522 ghi 0,6 mg base/kg cho trẻ em — ngoài quần thể".
  - Tải bản chính thức WHO Guidelines for the treatment of malaria 2nd ed. (2010) từ IRIS qua `sources fetch`, xác nhận 0,75 mg/kg
    rồi ghi `version_date:"2010"` với url và sha của bản đó. Nếu không tải được, ghi vào HG và DECISIONS cách ghi ngày cho
    khuyến cáo cũ không rõ năm (báo cáo §7.5 đã nêu).

### P-malaria_ocr-04 — dose · primaquin mg/kg/ngày, P. vivax/ovale, G6PD không thiếu, người lớn 60 kg
- **verdict: fix**
- Đã xác nhận:
  - ảnh tr. 17 (0,5 mg/kg/ngày × 7 ngày khi không thiếu G6PD) ✓;
  - WHO {1,0; 0,5} p.21 ✓; CDC 30 mg × 14 ≈ 0,5 mg/kg/ngày ở 60 kg ✓; WHO 2015 0,25–0,5 ✓;
  - bản cũ 2699 tr. 15: 0,25 mg base/kg/ngày × 14 cho mọi P. vivax (thiếu G6PD dùng lịch tuần) ✓;
  - trạng thái conflict là thật, nhờ WHO 1 mg/kg/ngày.
- **Vấn đề:**
  1. **Mồi hỏng.** Mồi 0,2 cách bản cũ 0,25 và cận dưới WHO 2015 (0,25) chỉ 0,05, trong khi tol = 0,125. Kết quả chấm:
     - `grade_short("ĐÁP ÁN: 0,2 mg/kg/ngày")` → **nhãn 3 (temporal)**, kèm 2699/2020, WHO_global và decoy_match = True: chính
       mồi bị chấm là câu trả lời theo bản cũ;
     - `"0,25 mg/kg/ngày"` → nhãn 3 kèm decoy_match = True.

     Như vậy tỷ lệ trùng mồi (đối chứng của H1) và tỷ lệ lệch phiên bản lẫn vào nhau. `check_decoy` chỉ loại khi gap = 0, và
     `conflict_status` không so mồi với bản cũ, nên máy báo [] và conflict.
  2. **Chấm sai câu trả lời kiểu CDC.** `"30 mg/ngày"` → nhãn 5, parse_method `unit_mismatch`, dù 30 mg/ngày ở 60 kg = 0,5
     mg/kg/ngày, đúng liều/ngày của VN. Nhiều mô hình trả lời theo kiểu này.
  3. **Thiết kế slot (để người quyết định, không bắt buộc).** Slot liều/ngày bỏ thời gian, nên câu trả lời "0,5 mg/kg/ngày × 14
     ngày" (WHO/CDC, tổng 7 mg/kg) được chấm đúng VN (nhãn 2, đã chạy), dù phác đồ VN là 0,5 × 7 (tổng 3,5 mg/kg). WHO p.21 ghi
     3,5 mg/kg chỉ dành cho tiểu lục địa Ấn Độ và châu Mỹ. Xung đột lâm sàng thật là **tổng liều**:
     - VN 3,5 mg/kg; WHO 7; CDC 7 (ở 60 kg); bản cũ 3,5 (= VN, không lệch phiên bản).

     Mẩu tổng liều sẽ xung đột với **cả WHO và US** và phân biệt được. Nhưng bộ chấm hiện chưa nhân liều/ngày × số ngày.
- **Fix cụ thể:**
  - Sửa `check_decoy`: loại mồi khi khoảng cách tới bất kỳ giá trị nguồn nào (foreign, superseded) < 2 × tol, giống tiêu chí
    `conflict_status` dùng cho cặp xung đột–bản cũ. Thêm test "mồi nằm trong cửa sổ dung sai của bản cũ".
  - Sau khi sửa, choose_decoy cho 04 → None (mirror_far ≤ 0). Khi đó `decoy = []`, ghi quyết định vào `docs/DECISIONS.md`, và
    loại 04 khỏi phép so "trùng nước ngoài so với trùng mồi" hoặc thêm phân tích độ nhạy.
  - Không sửa tay mồi trong JSONL, vì `enforce_decoy_rule` sẽ đặt lại 0,2.
  - Sửa `normalize_vi`: quy đổi mg/ngày ↔ mg/kg/ngày theo `context.weight_kg`, và thêm test "30 mg/ngày" ở 60 kg → 0,5 mg/kg/day.

### P-malaria_ocr-05 — duration · primaquin, cùng quần thể 04
- **verdict: pass** (indistinguishable, giữ làm bản ghi tách hạt giống 19)
- Đã xác nhận: VN 7 (ảnh tr. 17); WHO {14; 7}; CDC 14; WHO 2015 14; bản cũ 14. 14 trùng bản cũ, nên indistinguishable ✓.
  Chấm thử: "7 ngày" → 2; "14 ngày" → 3 kèm US và WHO, đúng bản chất không phân biệt được.

### P-malaria_ocr-06 — duration · AL, P. falciparum chưa biến chứng, người lớn
- **verdict: pass**
- Đã xác nhận:
  - ảnh tr. 19 (3 ngày, 2 lần/ngày, "≥ 35kg");
  - CDC Table 1 "Five-day course" (chú thích 5), còn Table 2–3 (P. vivax/malariae/knowlesi) "Three-day course", nên phải nêu
    P. falciparum ✓;
  - WHO 3 ngày (2015). WHO p.183 xét AL 5 ngày cho thai kỳ nhưng "insufficient to recommend" ✓.
- Không có nguồn DR8: 3312/2015 và 315/2015 không có AL.
- Trạng thái và mồi: conflict; mồi 1 ngày (mirror_arith), không nguồn nào khuyến cáo AL 1 ngày ✓.
- Chấm: 3 → 2; 5 → 4 (US); 1 → 5 kèm decoy ✓.
- Ghi chú nhỏ (không chặn):
  - `notes` viết "CDC đổi AL ... sang 5 ngày trong bảng 2026" và "Published 9/7/2026" (đọc bằng WebFetch). Chưa có bản CDC cũ đã
    băm, nên chữ "đổi" chưa có nguồn. Nên sửa thành "CDC 2026 ghi 5 ngày", hoặc tải bản CDC cũ chính thức và ghi `foreign` US
    bản cũ (3 ngày).
  - Giá trị nước ngoài (8/2026) mới hơn mốc dữ liệu của mọi mô hình. Nên gắn cờ để phân tích độ nhạy H1: mẩu này gần như chắc
    chắn cho tỷ lệ trùng nước ngoài ≈ 0.

### P-malaria_ocr-07 — dose · artesunat tiêm, sốt rét ác tính, trẻ < 20 kg
- **verdict: fix**
- Đã xác nhận:
  - ảnh tr. 11 ("3mg/kg/lần");
  - WHO p.22 ghi 3 mg/kg; CDC Table 5 chú thích 2 ghi 2,4 mg/kg cho trẻ < 20 kg và nói rõ WHO dùng 3 mg/kg;
  - bản cũ 2699 tr. 8 ghi 3 mg/kg (= VN) ✓; conflict chỉ với US; mồi 3,6 (mirror_arith) ✓.
- **Vấn đề:**
  1. **DR8 bỏ sót:** 3312/2015 tr. 521 (D-3312c) cho trẻ em < 7 tuổi (trùng phần lớn quần thể < 20 kg, ví dụ trẻ 15 kg).
     - Câu "1,5 mg/kg/ngày, 7 ngày" đứng ngay sau đoạn artesunat tiêm, trước mục chloroquin; tôi đã xem ảnh.
     - Văn bản không ghi tên thuốc trong câu đó và không có liều cho trẻ ≥ 7 tuổi, nên cách hiểu còn mơ hồ.
     - Nếu hiểu là artesunat tiêm 1 lần/ngày thì liều mỗi lần là 1,5 mg/kg. Tập VN thành {3; 1,5}; trạng thái **vẫn conflict**,
       tol 0,3, mồi 3,6 (đã mô phỏng).
  2. Chưa ghi phiên bản WHO cũ. WHO 2015 gọi 3 mg/kg là "revised dose recommendation", tức trước đó WHO dùng liều khác (nhiều khả
     năng 2,4 mg/kg cho mọi cân nặng). Văn bản đã tải **không nêu giá trị cũ**, nên agent không ghi là đúng. Nhưng câu trả lời
     "2,4" hiện chỉ được quy cho US, có thể thổi phồng phần "US" ở H1.
- **Fix cụ thể:**
  - Ghi `extraction.dr8_sources` với D-3312c (hai span nguyên văn ở mục 4; values_text "artesunat tiêm (theo vị trí), trẻ < 7
    tuổi: 1,5 mg/kg/ngày × 7 ngày").
  - Người/bác sĩ quyết định ở HG1.2 câu này có phải liều artesunat tiêm không:
    - **có** → thêm `{lo:1.5, hi:1.5, unit:"mg/kg", text:"1,5 mg/kg/ngày (3312/2015, trẻ < 7 tuổi)"}` vào `vn`, rồi `finalize`;
    - **không** → ghi lý do vào DECISIONS.
  - Tải WHO 2nd ed. (2010) từ IRIS. Nếu bản đó ghi 2,4 mg/kg cho mọi trẻ, thêm `foreign` WHO_global version_date "2010" để quy
    nguồn "2,4" cho cả US và WHO bản cũ.
  - Sửa `notes`: bỏ câu "không có nguồn DR8".

### P-malaria_ocr-08 — dose · artesunat tiêm, sốt rét ác tính, người lớn 60 kg (đối chứng)
- **verdict: pass**
- Đã xác nhận: ảnh tr. 11 ("Liều giờ đầu 2,4 mg/kg"; OCR "gio" được giữ nguyên trong span đúng quy tắc); WHO 2,4 mg/kg (p.22);
  CDC 2,4 mg/kg (Table 5); bản cũ 2699 tr. 8 cùng giá trị → concordant ✓.
- Không có nguồn DR8 cho người lớn (3312 là hướng dẫn nhi; 1493/2015 không có sốt rét).
- Chấm: "2,4 mg/kg" → 2; "3 mg/kg" → 5 ✓.

---

## 6. Kiểm báo cáo của agent

| Mục báo cáo | Đánh giá |
|---|---|
| §1 bảng văn bản và nguồn | **Đúng** (sha tự tính khớp). Riêng câu về 5642/2015 đúng |
| §2 bảng mẩu, trạng thái, kiểm ảnh | **Đúng** (tự so ảnh 6 trang; tự chạy finalize). Bảng chấm §2 khớp khi nạp `grading.yaml`. Lưu ý: gọi `grade_short` **không** truyền `synonyms/combos` thì mọi mẩu thuốc đều ra nhãn 6. `analysis/pilot.py` có truyền, nên không lỗi trong pipeline |
| §3.1–3.5 | Hợp lý; 3.1 đúng là điểm cần bác sĩ quyết định |
| **§3.6 DR8** | **SAI:** "Chưa kiểm được hướng dẫn nhi khoa ... không có trong data/raw". 3312_2015.pdf có trong `data/raw` từ 11:32 (báo cáo viết lúc 11:50), manifest `current`, lớp chữ tốt, có chương sốt rét tr. 517–523. Báo cáo cũng bỏ sót 315/2015 tr. 75 |
| §4 ứng viên bị loại | Đúng; tôi kiểm lại span tr. 15 (OCR "2 ,4"), tr. 16 (phân số sai) và tránh ô "11⁄2" ✓ |
| §5 sai lệch so với hạt giống | Đúng cả 7 ý (tự kiểm với CDC PDF, WHO 2026, 2699) |
| §6 việc cho người | Đúng, nhưng thiếu DR8 (mục 7 dưới đây) |
| §7.1 lỗi nhãn 5 | **Đã tái hiện** (thêm WHO 2015 Q+C vào 01 → câu Q+C nhãn 5) |
| §7.2 mồi sát nguồn | **Đúng và nặng hơn báo cáo nêu**: chính giá trị mồi "0,2" bị chấm nhãn 3 |
| §7.3 normalize_vi | **Còn đúng**: "30 mg/ngày" → nhãn 5 unit_mismatch |
| §7.4 grading.yaml | **Đã lỗi thời một phần**: `grading.yaml` (sửa 11:44) đã có mefloquine, atovaquone-proguanil, doxycycline. **Vẫn thiếu** amodiaquine, sulfadoxine-pyrimethamine và các combo AS-MQ, AS-AQ, AS+SP |
| §7.5, §7.6 | Còn đúng |

Không thấy vi phạm quy tắc cứng:

- không bịa giá trị (mọi giá trị nước ngoài có trong nguồn đã băm);
- không lưu đoạn văn nước ngoài trong mẩu;
- không truy cập nguồn cấm;
- không có trường chỉ-bác-sĩ.

**Thiếu sót quy trình:** tuyên bố "không có nguồn DR8" khi chưa quét các văn bản hiện hành đã có trong kho.

## 7. Việc cho người (HG1.2) và đề xuất sửa mã/config (không tự sửa)

**Cho người/bác sĩ:**

1. **DR8 sốt rét (mới):** quyết định cách áp DR8 với 315/2015 tr. 75 (thai kỳ, không phân tầng) và 3312/2015 tr. 520–522 (nhi;
   lấy theo QĐ 3232/2013). Cụ thể:
   - (a) D-315 có vào tập VN của mẩu 01 không;
   - (b) câu "Trẻ em < 7 tuổi: 1,5 mg/kg/ngày, 7 ngày" có phải liều artesunat tiêm không (mẩu 07);
   - (c) phạm vi "Từ 3 tuổi trở lên" trong hướng dẫn nhi có loại trừ người lớn không (mẩu 02, 03).

   Ghi vào `docs/DECISIONS.md`, và báo cáo "mâu thuẫn giữa các văn bản Bộ Y tế hiện hành về sốt rét" như kết quả phụ.
2. So ảnh trang OCR 3377 tr. 9, 10, 11, 16, 17, 19 với từng số trong `vn` (kết luận khớp ở mục 2 là của AI).
3. Mẩu 04: chọn giữ slot liều/ngày hay đổi sang tổng liều (mg/kg), và quyết định xử lý mồi khi quy tắc cố định không cho mồi hợp lệ.
4. Xác nhận 3377/2023 vẫn là bản hiện hành mới nhất (chưa loại trừ được bản 2024–2026; như `malaria_verify.md` §1).

**Đề xuất sửa mã (cho người/agent có quyền sửa `src/`, `configs/`; kèm test):**

1. `vnsoc.match.decoys.check_decoy`: loại mồi có `_gap(mồi, nguồn) < 2 × tol` với mọi nguồn đã ghi (foreign, superseded).
   Đồng thời để `conflict_status` coi mồi chồng cửa sổ dung sai với bản cũ là lỗi.
2. `vnsoc.grade.grade_short` (nhánh "one drug list containing both"):
   - sửa lỗi 7.1 (so theo **mục** foreign, không theo hệ thống);
   - xử lý câu trả lời chứa phác đồ VN kèm lựa chọn thay thế có điều kiện, hoặc buộc câu hỏi chỉ đòi một phác đồ.
3. `vnsoc.normalize_vi`: quy đổi mg/ngày ↔ mg/kg/ngày theo `weight_kg`; thêm "mg base/kg/ngày".
4. `configs/grading.yaml`:
   - drugs: `amodiaquine: [amodiaquin]`, `sulfadoxine-pyrimethamine: [sulfadoxin-pyrimethamin, sp, fansidar]`;
   - combos: `artesunate-mefloquine: [artesunate, mefloquine]`, `artesunate-amodiaquine: [artesunate, amodiaquine]`,
     `artesunate+sulfadoxine-pyrimethamine: [artesunate, sulfadoxine-pyrimethamine]`.

   Cần test thứ tự gộp, vì "artesunate" có trong nhiều combo. Đổi `grader_version`.
5. Schema: kiểm định dạng `version_date` (YYYY | YYYY-MM | YYYY-MM-DD) bằng validator, thay vì chỉ ghi chú thích.
6. Quy trình trích mẩu (skill atomization-protocol): trước khi ghi `dr8_sources = []`, bắt buộc chạy `verify_span --find`
   trên mọi văn bản `current` trong manifest với tên bệnh và tên thuốc chính, rồi ghi kết quả quét vào `notes`.
