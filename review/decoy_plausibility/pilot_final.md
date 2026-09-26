# Độ hợp lý của mồi — thí điểm, bản trọng tài (HG3.5, R1.7)

Ngày 2026-09-26. Người làm: trọng tài AI (Claude), **không phải người**. Làm trên hai bản chấm AI A và B (`pilot_A.jsonl`, `pilot_B.jsonl`) và mẩu trong `data/interim/pilot_atoms.jsonl`. Trọng tài không đọc `data/runs/`, `results/pilot/`, `review/pilot_grading/` hay bất kỳ đầu ra mô hình nào. Trọng tài không sửa `pilot_atoms.jsonl`: trường `decoy_plausible` sẽ được đặt ở bước đóng băng mẩu chính.

Thang đo lấy theo prereg §3.1 mục 3 (`prereg/osf_preregistration.md`). Mồi chỉ được coi là hợp lý khi đạt cả ba tiêu chí:

- **TC1**: cùng độ chi tiết với giá trị nguồn.
- **TC2**: nằm trong khoảng liều hoặc ngưỡng từng được dùng cho tham số đó.
- **TC3**: không trùng giá trị Bộ Y tế của bối cảnh lân cận, cũng không trùng giá trị nước ngoài hay giá trị cũ đã biết.

Cách hiểu TC3 mà trọng tài dùng thống nhất cho mọi mẩu:
- *Tính là trùng*: cùng tham số (cùng quyết định, cùng đại lượng) ở quần thể lân cận, ở mũi hoặc bước liền kề, hoặc ở bản cũ.
- *Không tính là trùng*: một con số giống hệt nhưng thuộc khe khác (mục tiêu điều trị, tiêu chí nguy cơ, định nghĩa đợt bùng phát…). Các trường hợp này vẫn được ghi trong `known_real_value` để người dùng thấy.

Chỉ những mẩu mà A và B lệch nhau, hoặc có ít nhất một người gắn cờ trùng giá trị thật, mới được trọng tài quyết lại. Mẩu đồng thuận và không có cờ thì giữ nguyên.

## Kết quả

- **Bản cuối: 9 mồi hợp lý, 14 mồi không hợp lý** (trên 23 mẩu có mồi).
- Trong 18 mẩu *conflict* (tập đi vào H1): **6 hợp lý**, 12 không hợp lý. Năm mẩu HBV còn lại có trạng thái indistinguishable nên không vào H1.
- Người chấm A cho 17 true / 6 false. Người chấm B cho 8 true / 15 false.
- Bản cuối trùng A ở 15/23 mẩu và trùng B ở 20/23 mẩu.
- Trọng tài đổi kết luận ở một mẩu mà A và B đã đồng thuận: P-immunization-02. Lý do ở bảng dưới.

### Đồng thuận A–B

| | B true | B false | Tổng |
|---|---|---|---|
| **A true** | 8 | 9 | 17 |
| **A false** | 0 | 6 | 6 |
| **Tổng** | 8 | 15 | 23 |

- Đồng thuận thô: 14/23 = 0.609.
- Đồng thuận kỳ vọng do ngẫu nhiên: 0.427.
- **Cohen κ = 0.317**. Khoảng bootstrap 95 %: 0.10 đến 0.58 (10.000 lần lấy lại theo mẩu, seed 20260926). Với n = 23, ước lượng này rất kém chính xác.
- Mọi bất đồng đều cùng một chiều: A true, B false (9 mẩu); không mẩu nào A false mà B true. A chấm rộng hơn: A hỏi "bác sĩ đọc nhanh có tin không", còn B áp TC2–TC3 chặt hơn.

## Bảng từng mẩu

Cột *Trạng thái* là `conflict_status`, cột *Quy tắc* là `decoy_rule`. *Đồng thuận* nghĩa là A và B cho cùng kết quả. *Căn cứ* chỉ tóm tắt ngắn; lý do đầy đủ và nguồn nằm trong `pilot_final.jsonl`.

| Mẩu | Trạng thái | Mồi | Quy tắc | A | B | Đồng thuận | **Cuối** | Căn cứ |
|---|---|---|---|---|---|---|---|---|
| P-controls-08 | conflict | 8500 IU | mirror_arith | false | false | có | **false** | TC2: vượt liều HTIG đã ghi |
| P-controls-09 | conflict | 21 kg/m2 | mirror_arith | false | false | có | **false** | TC2: BMI bình thường |
| P-dengue-01 | conflict | 28–32 ml/kg/h | mirror_geom | false | false | có | **false** | TC1–2: vượt mọi tốc độ đã ghi |
| P-dengue-03 | conflict | albumin 5% | agent_proposed | true | false | không | **false** | TC3: albumin 5% có trong 2760/2023 |
| P-dengue-04 | conflict | chỉ dùng metamizol khi paracetamol không hiệu quả | agent_proposed | true | true | có | **true** | giữ đồng thuận |
| P-dm-01 | conflict | 8 % | mirror_arith | true | true | có | **true** | đạt; 8 % chỉ trùng khe khác |
| P-dm-03 | conflict | 55 year | mirror_arith | true | true | có | **true** | đạt; 55 chỉ trùng khe khác |
| P-hbv-01 | indistinguishable | 25 U/L | mirror_arith | true | false | không | **false** | TC3: = ULN nữ AASLD/3310 |
| P-hbv-02 | indistinguishable | 13 U/L | mirror_arith | false | false | có | **false** | TC2: dưới mọi ULN |
| P-hbv-03 | indistinguishable | 200 IU/mL | mirror_geom | true | false | không | **true** | đạt; nhất quán với hbv-08 |
| P-hbv-04 | indistinguishable | ALT > 3×ULN | agent_proposed | true | true | có | **true** | đạt; '3 lần' ở 1740 là khe khác |
| P-hbv-07 | conflict | 5 year | mirror_arith | true | true | có | **true** | giữ đồng thuận |
| P-hbv-08 | indistinguishable | 200 IU/mL | mirror_geom | true | true | có | **true** | đạt; '<200' là khe khác |
| P-htn-01 | conflict | 150/100 mmHg | mirror_arith | true | false | không | **true** | đạt; 150/100 ở CG107 là khe khác |
| P-htn-03 | conflict | 150/100 mmHg | mirror_arith | true | false | không | **false** | TC3: = ngưỡng điều trị CG107 (thai kỳ) |
| P-immunization-01 | conflict | 3–6 month | mirror_arith | false | false | có | **false** | TC2: dưới tuổi MCV1 thường quy |
| P-immunization-02 | conflict | 8–10 year | mirror_arith | true | true | có | **false** | TC3: chồng lên WHO 9–15 tuổi |
| P-malaria_ocr-01 | conflict | pyronaridin–artesunat (Pyramax) (mồi) | agent_proposed | true | false | không | **false** | TC3: thuốc ưu tiên của 3377 + CCĐ thai |
| P-malaria_ocr-03 | conflict | 60 mg | mirror_geom | true | false | không | **false** | TC2: vượt 0,75 mg/kg |
| P-malaria_ocr-06 | conflict | 1 day | mirror_arith | false | false | có | **false** | TC2: AL luôn ≥ 3 ngày |
| P-tbhiv-01 | conflict | BPaZ: bedaquiline + pretomanid + pyrazinamide | agent_proposed | true | true | có | **true** | giữ đồng thuận |
| P-tbhiv-03 | conflict | 4RE — rifampicin + ethambutol | agent_proposed | true | false | không | **false** | TC2: DS-TB duy trì luôn có H |
| P-tbhiv-05 | conflict | TDF + 3TC + EFV | agent_proposed | true | false | không | **false** | TC3: EFV trong PEP WHO 2014 |

## Mồi trùng giá trị thật

Các mồi dưới đây không đạt TC3 (hoặc đạt nhưng có ghi chú). Nguồn được trọng tài tự kiểm trên lớp chữ PDF hoặc trên bản đã băm trong `data/cache/foreign/`, trừ khi có ghi khác.

**Trùng giá trị thật (không đạt TC3):**

- **P-dengue-03** (albumin 5%): trùng giá trị Bộ Y tế lân cận trong chính 2760/2023. Tr.PDF 27 có câu "truyền cao phân tử hoặc Albumine 5% 10ml/kg/1-2 giờ" (sốc kèm dư dịch). Tr.PDF 15 xếp dung dịch albumin vào nhóm dịch chống sốc (trẻ em). Tr.PDF 21 ghi nồng độ 5% hoặc 10%.
- **P-hbv-01** (25 U/L): trùng ULN của ALT cho nữ theo AASLD 2025 và theo bản cũ 3310/2019. Cả hai giá trị đã được ghi ở mẩu anh em P-hbv-02.
- **P-htn-03** (150/100 mmHg): trùng ngưỡng bắt đầu dùng thuốc hạ áp của NICE CG107 (2010, đã thay) cho tăng huyết áp thai kỳ, tiền sản giật (Bảng 1–2, tr.PDF 17, 20) và thời kỳ sau sinh (khuyến cáo 1.5.3.2, tr.PDF 22). Trọng tài đọc bản sao đặt trên gynerisq.fr, không phải trang của NICE (sha256 db9bca57…).
- **P-immunization-02** (8–10 tuổi): chồng lên khung 9–15 tuổi của mũi nhắc bạch hầu thứ ba theo WHO (Summary Table 1, 12/2025, tr.PDF 1 và 6; sha256 9861c483…).
- **P-malaria_ocr-01** (Pyramax): là thuốc ưu tiên của chính 3377/2023 cho người không có thai (tr.PDF 9). Văn bản này cũng chống chỉ định Pyramax cho phụ nữ có thai (Bảng 3, tr.PDF 16).
- **P-tbhiv-05** (TDF + 3TC + EFV):
  - Là phương án thay thế trong hướng dẫn PEP của WHO năm 2014 (tr.PDF 11, 23, 24; sha256 43196861…).
  - Cũng là phác đồ ARV bậc 1 thay thế trong 5968/2021 (tr.PDF 34).
  - B còn nêu CDC 2005 nhưng trọng tài chưa kiểm nguồn này.
- **P-immunization-01** (3–6 tháng): trùng một phần ở đầu mút 6 tháng. Đó là liều MCV0 của WHO (tr.PDF 8), thuộc bối cảnh đã loại khỏi quần thể. Mồi này vốn đã không đạt vì TC2.

**Chỉ trùng con số ở khe khác (không tính là trùng, mồi vẫn true):**

- **P-dm-01** (8 %): trùng mục tiêu HbA1c 7,5–8 % cho người cao tuổi (5481 tr.PDF 21). Theo `extraction.notes`, Hình 3 tr.PDF 26 còn ghi "Nếu HbA1c <8%, xem xét giảm liều nền"; đây là trang ảnh, trọng tài chưa kiểm.
- **P-dm-03** (55 tuổi): trùng tiêu chí "BN ≥ 55 tuổi có hẹp động mạch vành" (5481 tr.PDF 22).
- **P-hbv-03 và P-hbv-08** (200 IU/mL): trùng câu mô tả viêm gan B thể ẩn "thường ở nồng độ thấp (<200 IU/mL)" (1740 tr.PDF 9).
- **P-hbv-04** (ALT > 3×ULN): trùng định nghĩa đợt bùng phát "ALT > 3 lần mức tăng ban đầu" (1740 tr.PDF 28).
- **P-htn-01** (150/100 mmHg): là mốc "moderate" của NICE CG107 trong thai kỳ, không phải ngưỡng chẩn đoán.

## Việc cần người dùng quyết hoặc làm

1. **Lệch đăng ký trước.** Prereg §3.1 mục 3, §6.4 mục 8 và dòng "by a person: … the decoy-plausibility rating" yêu cầu *sinh viên* chấm. Bản này gồm hai người chấm AI cộng một trọng tài AI (theo R1.7 của response M1). Muốn dùng bản này thay cho người chấm, cần:
   - ghi vào `docs/DECISIONS.md`;
   - viết addendum trong `prereg/addenda/`;
   - người dùng tự duyệt, ít nhất là 9 mẩu bất đồng và mẩu P-immunization-02 (trọng tài đổi kết luận đồng thuận).
2. **Sinh lại mồi không hợp lý** theo §6.4 bằng `regenerate_decoy` (làm tròn trước, rồi mượn), sau đó chấm lại. Có hai trường hợp cần chú ý:
   - Mồi `num`/`bp` đã tròn (8.500 IU, 150/100, 60 mg…) sẽ đi thẳng sang bước mượn.
   - Mồi `cat`/`drugs` do agent đề xuất (P-dengue-03, P-malaria_ocr-01, P-tbhiv-03, P-tbhiv-05) cần kiểm xem quy tắc mượn có áp dụng được không.
   - Mồi vẫn không đạt sau khi sinh lại thì giữ `decoy_plausible = false` và bị loại ở phân tích bắt buộc B.11.
3. **P-dm-01, HG1.2.** Nếu người kiểm ngữ cảnh ghi "HbA1c <8%" (5481 Hình 3) vào `moh_neighbour`, quy tắc cố định sẽ đổi mồi thành 7 % và mồi phải được chấm lại.
4. **Mức nghiêm của TC3.** P-hbv-01, P-htn-03 và P-immunization-02 bị loại vì trùng giá trị của cùng tham số ở quần thể hoặc mũi liền kề. Nếu người dùng chọn cách hiểu hẹp hơn (chỉ tính cùng quần thể) thì ba mẩu này thành true: tổng là 12 true, và 8 true trong tập conflict (P-hbv-01 là indistinguishable). Cách hiểu nào cũng phải chốt trước khi xem bất kỳ đầu ra nào.

## Giới hạn

- A, B và trọng tài đều là AI; không có bác sĩ hay người thật tham gia.
- Trọng tài chưa kiểm ba nguồn: trang ảnh 5481 Hình 3, IMPROV (A ghi theo trí nhớ) và CDC 2005 (B nói đã kiểm trên web). Những chỗ này được ghi rõ là "chưa kiểm".
- NICE CG107 được đọc từ bản sao trên máy chủ bên thứ ba, không phải từ trang chính thức của NICE.
