# Phản biện độc lập — câu hỏi thí điểm chủ đề tbhiv

- Người phản biện: agent AI đóng vai rev-clinician + rev-methods (**không phải bác sĩ thật**). Mọi nhận định lâm sàng cần bác sĩ xác nhận ở HG4.2.
- Ngày: 2026-09-26.
- Đầu vào:
  - `tbhiv.jsonl` (bản nháp), `pilot_atoms.jsonl` (P-tbhiv-01..07);
  - `tbhiv_q.jsonl`, `tbhiv_p.jsonl`, `tbhiv_qc.csv`;
  - đề cương §1.2, §3.5, §4.3, §4.4, §5.7; SKILL question-generation;
  - `configs/conditions.yaml`, `configs/grading.yaml`;
  - `src/vnsoc/qgen/*.py`, `src/vnsoc/grade.py`, `src/vnsoc/run/prompts.py`;
  - bản text 162/2024 (tr.45, 55, 57, 60–63) và 5968/2021 (tr.28–29).
- Chống rò rỉ: tôi KHÔNG xem đầu ra của mô hình nào được kiểm tra. Mọi câu trả lời dùng để thử bộ chấm dưới đây đều do người phản biện tự viết.
- Kiểm bằng mã:
  - Chạy lại `vnsoc.qgen.build --only-drafted` cho kết quả giống người viết: 26 câu, 7 đoạn A3, 1 mục QC không đạt (`P-tbhiv-02|mcq`: mẩu không có mồi), exit 1.
  - Bản sửa đề xuất cho mẩu 01 và 05 đã chạy thử trong scratchpad, không ghi vào dự án. Kết quả vẫn là 26 câu, và chỉ còn đúng lỗi cũ của 02.

## Tổng hợp

| atom_id | verdict | Lý do chính |
| --- | --- | --- |
| P-tbhiv-01 | **fix** | "Người từ 14 tuổi trở lên" chạm phác đồ trẻ em kháng FQ của 162/2024. Phương án trắc nghiệm hiện ra dưới dạng mảnh thuốc. Bộ chấm không đọc được "BPaL" hay "BDLC" |
| P-tbhiv-02 | **fix** (mẩu/mã) | Mẩu không có mồi nên không dựng được trắc nghiệm. Bộ chấm không đọc được "Bdq", "amikacin" hay "prothionamide". Câu trả lời ngắn đạt |
| P-tbhiv-03 | **fix** (chữ phương án) | Câu trả lời ngắn đạt. Phương án trắc nghiệm lệch hình thức: chỉ 2 phương án "thật" có đuôi "(2HRZE/…)", và phương án Việt Nam dùng thứ tự "RHE" |
| P-tbhiv-04 | **pass** | Có ghi chú về đoạn A3 và moh_neighbour |
| P-tbhiv-05 | **fix** (mã/cấu hình) | Câu chữ đạt. Bộ chấm không nhận ra bictegravir, nevirapine, "tenofovir disoproxil" hay "tenofovir alafenamide". Phương án trắc nghiệm là mảnh thuốc. Có 2 phương án foreign:US nhưng chỉ 1 mồi |
| P-tbhiv-06 | **pass** | — |
| P-tbhiv-07 | **pass** | Ghi chú nhỏ: "24 tuần" không đọc được |

Tổng: **pass 3 / fix 4 / drop 0**.

- Không câu nào phải loại vì mơ hồ, sau khi sửa quần thể ở mẩu 01.
- Câu chữ 7 câu trả lời ngắn nhìn chung tốt:
  - không lộ đáp án;
  - không nhắc Việt Nam, Bộ Y tế, WHO hay Mỹ;
  - bản EN trung thành về nghĩa;
  - có ghi đơn vị mong đợi;
  - VI đều ≤ 59 từ, EN ≤ 51 từ.
- Phần lớn lỗi nằm **ngoài bản nháp**, ở bộ chấm, `render.py` và dữ liệu mẩu. Những lỗi này làm câu hỏi đúng về chữ nhưng **không đo được** điều cần đo.

### Vấn đề nghiêm trọng (xếp theo mức độ)

**1. [Chặn chạy thí điểm — bộ chấm] Dạng trả lời tự nhiên nhất của mẩu 01, 02, 05 không được chấm đúng.**

Tôi thử `parse_values` + `classify_value` với chuỗi tự viết:

| Mẩu | Chuỗi thử | Kết quả | Hệ quả |
| --- | --- | --- | --- |
| 01 | "BPaL" | [] (không tách được) | Câu trả lời đúng Bộ Y tế thành nhãn 6/5. Ở A3, đoạn trích chỉ gọi tên "Phác đồ BPaL", nên câu trả lời trung thành với đoạn trích cũng không chấm được |
| 01 | "BDLC" | [] | Trả lời trùng WHO 2026 bị đếm thiếu |
| 01 | "Bdq-Lzd-Cfz-Cs + 1 thuốc nhóm C" | {clofazimine} → không nguồn | Không bắt được lệch phiên bản (E1) |
| 02 | "Bdq-Lfx-Pto-E-Z-Hh-Cfz" (đúng cách viết của 162/2024) | {clofazimine, levofloxacin} → không nguồn | Câu trả lời đúng bị chấm sai |
| 02 | "amikacin, levofloxacin, prothionamide, clofazimine" | không nguồn | Không bao giờ bắt được giá trị bản cũ / WHO 2019 |
| 05 | "BIC/FTC/TAF", "bictegravir/emtricitabine/tenofovir alafenamide", "Biktarvy" | {TAF, FTC} / {FTC} / [] → không nguồn | **Giá trị xung đột chính của mẩu (CDC 2025) vô hình với bộ chấm** |
| 05 | "tenofovir disoproxil + lamivudine + dolutegravir" (INN không kèm "fumarate") | {3TC, DTG} → partial | Câu trả lời đúng Bộ Y tế bị chấm sai. "TLD" → [] |
| 05 | "TDF + 3TC + NVP" (chính là mồi) | partial, decoy_match = False | **π_mồi ≡ 0 theo cấu tạo** ở câu trả lời ngắn. Phép so H1 (π_nước ngoài − π_mồi) thiên về ủng hộ giả thuyết |

- Cần bổ sung `configs/grading.yaml` trước khi đóng băng (tệp ghi rõ đang cho phép bổ sung trước đóng băng), kèm test. Tối thiểu cần các mục sau (tên chuẩn hóa, không dấu, chữ thường):
  - bí danh `bpal` → combo BPaL, `bpalm` → combo BPaLM;
  - `bedaquiline: [bdq]`, `linezolid: [lzd]`;
  - `amikacin: [amikacine]`, `prothionamide: [prothionamid, pto]`, `ethionamide: [eto]`;
  - `bictegravir: [bic]`, `nevirapine: [nevirapin, nvp]`;
  - thêm "tenofovir disoproxil" vào tenofovir-disoproxil, "tenofovir alafenamide" vào tenofovir-alafenamide;
  - combo `biktarvy` = [bictegravir, emtricitabine, tenofovir-alafenamide], combo `tld` = [tenofovir-disoproxil, lamivudine, dolutegravir].
- Với BDLC: nếu thêm dưới dạng combo thì PHẢI đổi `key_drugs` của giá trị BDLC trong mẩu 01 thành `["BDLC"]`, vì combo gộp sẽ xóa delamanid/clofazimine khỏi tập đã tách (xem ghi chú mẩu). Cách an toàn hơn là cho "bdlc" **nở ra** thành 4 INN thay vì gộp lại.
- Viết tắt 1–2 chữ ("Pa", "Cs", "Am", "E", "Z") vẫn nên để ngoài, vì dễ nhầm.

**2. [Chặn trắc nghiệm — `qgen/render.py`] Phương án của mẩu kiểu `drugs` được in từ `key_drugs` (khóa phân biệt), không phải phác đồ.**

- Mẩu 01 hiện ra:
  - VI: "BPaL" / "cycloserin" / "pretomanid + moxifloxacine + pyrazinamid" / "dlm + clofazimin";
  - EN: "BPaL" / "cycloserine" / "pretomanid + moxifloxacin + pyrazinamide" / "delamanid + clofazimine".
- Mẩu 05 hiện ra:
  - VI: "bictegravir" / "nevirapine" / "taf + dtg" / "tdf + dtg";
  - EN: "tenofovir-alafenamide + dolutegravir" (khóa nội bộ có gạch nối).
- Hệ quả:
  - (i) Câu dẫn hỏi "phác đồ nào", nhưng 2–3 phương án là đơn trị hoặc mảnh 2 thuốc, nên bị loại ngay theo hình thức. Ở mẩu 01, phương án Bộ Y tế lại là phương án duy nhất trông như một phác đồ có tên. P(nước ngoài) và P(mồi) vì vậy bị kéo xuống giả tạo, còn P(Bộ Y tế) bị đẩy lên.
  - (ii) Bản VI trộn viết tắt chữ thường ("dlm", "tdf", "dtg") với tên INN, vì `drug_name` lấy bí danh chấm điểm đầu tiên làm tên hiển thị.
  - (iii) Nếu chuyển sang in `item.text` nguyên văn thì lại lộ thời gian ("6–9 tháng", "18–20 tháng") và chú thích ("B1.2a", "khuyến cáo chính").
- Cách sửa:
  - Thêm trường hiển thị cho ValueItem (ví dụ `display_vi` / `display_en`), hoặc thêm bảng tên hiển thị riêng, tách khỏi bí danh chấm điểm.
  - Mọi phương án phải là **phác đồ đầy đủ, cùng định dạng, cùng thứ tự nhóm thuốc, không có thời gian hay chú thích**.
  - Chữ đề xuất cho từng phương án nằm ở mục mẩu 01 và 05 bên dưới.
- Người viết đã tự nêu cảnh báo này trong `notes`. Tôi xác nhận đây là lỗi **chặn**, không chỉ là "đề nghị".

**3. [Mơ hồ quần thể — mẩu 01, sửa được ở bản nháp] "Người từ 14 tuổi trở lên" chạm phác đồ trẻ em của chính 162/2024.**

- 162/2024 tr.62–63 (mục phác đồ dài ngày cho trẻ em) gợi ý cho trẻ **kháng FQ**: "Bdq–Lzd–Cfz–Cs–(Dlm)".
- Khái niệm "trẻ em" trong văn bản có chỗ kéo tới 16 tuổi (tr.45: A2a "trẻ em từ 3 tháng đến 16 tuổi").
- Như vậy với người 14–15 tuổi, một câu trả lời theo mục trẻ em là giá trị Bộ Y tế hiện hành, nhưng bộ chấm sẽ gán:
  - **lệch phiên bản**, vì câu trả lời chứa cycloserine = E1;
  - **đồng thời nước ngoài WHO**, vì câu trả lời chứa delamanid + clofazimine = BDLC.
- Tôi đã thử chuỗi "bedaquiline + linezolid + clofazimine + cycloserine + delamanid": kết quả là foreign WHO_global + superseded 2760/2021, 1314/2020.
- Ở trắc nghiệm hiện tại, "dlm + clofazimin" và "cycloserin" đều là mảnh của phác đồ trẻ em này.
- Cách sửa: dùng đúng khuôn mà quy tắc viết đưa ra ("người lớn (≥ 16 tuổi)"), cụ thể là "người lớn (≥ 14 tuổi)". Mẩu cũng ghi sẵn "(câu hỏi dùng người lớn)". Đã thử: QC đạt, VI 58 từ.
- Bác sĩ cần xác nhận giới hạn tuổi của mục trẻ em ở 162/2024.

**4. [Hình thức phương án — mẩu 03, sửa ở chữ mẩu hoặc mã] Phương án kiểu cat in nguyên `item.text`.**

- "4RHE — rifampicin + isoniazid + ethambutol (2HRZE/4RHE)" và "4HR — isoniazid + rifampicin (2HRZE/4HR)" có đuôi ngoặc. Mồi "4RE — …" và filler "4HE — …" thì không. Khác biệt hình thức này làm P(mồi) thấp giả tạo.
- Phương án Bộ Y tế còn dùng **thứ tự ký hiệu riêng của Việt Nam** ("RHE", "rifampicin + isoniazid + …"), trong khi phương án WHO/Mỹ dùng "HR / isoniazid + rifampicin". Ở A1 (có tiền tố Bộ Y tế), đây là dấu hiệu nhận diện "ký hiệu Việt Nam" chứ không phải kiến thức.
- Cách sửa: đồng nhất chữ hiển thị (xem mục mẩu 03).

**5. [Phương pháp trắc nghiệm, cả bộ — trùng vấn đề số 2 của `immunization_review.md`] Mẩu 05 có 2 phương án foreign:US và chỉ 1 mồi.**

- Hai phương án nước ngoài là BIC/FTC/TAF và DTG + TAF.
- Ô thứ 3 được lấp bằng giá trị nước ngoài thứ hai trước khi xét filler (`mcq.options`: `sup + conf[1:]`). Cách này trái SKILL bước 3 và trái giả định 1/(số lựa chọn − 1) ở §3.5.
- Hệ quả: khi mô hình chọn bừa, tỉ lệ nước ngoài : mồi đã là 2 : 1.
- Cần chọn trước khi đăng ký OSF:
  - (a) sửa mã theo SKILL. Khi đó mẩu 05 cần filler kiểu drugs do người viết cung cấp, và filler phải qua `check_decoy`, gồm cả WHO 2014 PEP và 5456/2019 (chưa tải được);
  - (b) đăng ký trước phép so theo từng phương án.

**6. [Dữ liệu mẩu — 02] Mẩu indistinguishable, `decoy = []`, nhưng có superseded, nên `build` bắt buộc dựng trắc nghiệm, và việc dựng thất bại.**

- Tôi đề nghị **miễn trắc nghiệm cho mẩu indistinguishable** (sửa ở `build.py`, chủ mã quyết định). Mẩu này không dùng cho kiểm định xác nhận. Phương án nước ngoài (WHO 2019, amikacin) trùng phương án bản cũ (1314/2020, amikacin), nên P(nước ngoài) và P(mồi) không có nghĩa.
- Cách thay thế: người giữ mẩu thêm mồi. Ứng viên là capreomycin (thuốc tiêm cùng nhóm với amikacin, không có trong phác đồ ngắn hạn của nguồn nào đã ghi); ứng viên này phải qua `check_decoy` và được thêm vào grading.yaml.
- Bản nháp của 02 không cần sửa.

**7. [Mồi kém hợp lý — 01, 05; đã chờ HG3.5, tôi nhấn mạnh]**

- Mẩu 01: mồi BPaMZ chứa moxifloxacin, trong khi câu hỏi nói rõ người bệnh kháng FQ, nên mô hình có kiến thức sẽ loại ngay.
- Mẩu 05: mồi NVP không còn dùng trong PEP (độc gan).
- Cả hai đều làm π_mồi → 0, nên phần vượt (π_f − π_d)/(1 − π_d) gần như bằng π_f. Phần vượt này mất vai trò đối chứng.
- Nên sinh lại mồi theo quy tắc định trước nếu HG3.5 chấm không đạt.

**8. [Đoạn A3 — kiểm tay trước đóng băng]**

- **01**:
  - Đoạn trích kết thúc giữa câu ("có thể chỉ định phác đồ") và dính dấu văn thư "bvtn.vt_…14:19:00".
  - Đoạn trích không có dòng thành phần "6-9 BPaL (bedaquiline, pretomanid, linezolid)" (tr.54).
  - Đoạn trích có "6 BPaLM" (giá trị lân cận), nhưng `passage_has_alt_value` bỏ trống vì bộ chấm không đọc "BPaLM".
- **02**: đoạn trích chỉ gồm tiêu chuẩn thu nhận, **không có thành phần giai đoạn tấn công**. Câu trả lời chỉ suy ra được từ danh sách "thuốc có trong phác đồ (Bedaquiline, Fluoroquinolones, Prothionamid/Ethionamide, Linezolid, Clofazimine)".
- **04**:
  - Đoạn trích chủ yếu là A1 người lớn ("Giai đoạn duy trì: … 03 loại thuốc: R, H, E"). Phác đồ trẻ em chỉ có ký hiệu "2HRZE/4RH", còn dòng "02 loại thuốc: R, H" nằm ở tr.45, ngoài đoạn trích.
  - Mẩu 04 chưa có `moh_neighbour` (A1, HRE), nên câu trả lời "RHE" ở A3 bị chấm nhãn 5 mà không bị gắn cờ.
  - Đề nghị thêm `moh_neighbour` cho 04 (đối xứng với 03) và dịch cửa sổ đoạn trích về A2.

---

## P-tbhiv-01 — verdict: **fix**

**Mẩu**: 162/2024 tr.53, phác đồ BPaL.
- Người ≥ 14 tuổi, kháng R + FQ, lao phổi không nặng, đủ tiêu chuẩn BPaL.
- Bộ Y tế: **BPaL**.
- Xung đột: WHO 2026 B1.2a BDLC.
- Bản cũ: E1 (Bdq Lzd Cfz Cs + 1 thuốc nhóm C). Mẩu có cờ `temporal_confounded`.
- Mồi: BPaMZ.

| Tiêu chí | Đánh giá |
| --- | --- |
| (1) Đáp án Bộ Y tế duy nhất? Giá trị nước ngoài có "cũng đúng"? | **Chưa đạt.** Với người lớn thì đạt: đã nêu đủ tiêu chuẩn thu nhận và chống chỉ định tr.54, nên PĐ E (dành cho người không đủ tiêu chuẩn BPaL, tr.56) và BPaLM (chống chỉ định khi kháng FQ) không đồng thời đúng. BDLC không có trong 162/2024 cho người lớn. **Nhưng** "người từ 14 tuổi trở lên" gồm cả 14–15 tuổi, và với nhóm này mục trẻ em tr.62–63 cho "Bdq–Lzd–Cfz–Cs–(Dlm)" (vấn đề nghiêm trọng số 3) |
| (2) Lộ đáp án/nguồn? | Đạt. Không nêu tên thuốc nào: việc tránh bedaquiline/pretomanid/delamanid/linezolid là đúng, vì combo sẽ gộp thành BPaL. Không có dấu hiệu quốc gia |
| (3) EN trung thành | Đạt: pulmonary-only, non-severe; never treated with second-line TB drugs; ≥ 35 kg; BMI ≥ 17; normal QTcF… |
| (4) Tự nhiên | Đạt. Câu dài (59 từ) nhưng quen thuộc với bác sĩ lao. "Thần kinh ngoại biên bình thường" có thể thay bằng "không có bệnh thần kinh ngoại biên" (tùy chọn) |
| (5) Trắc nghiệm | **Không đạt** (vấn đề nghiêm trọng số 2 và 7): phương án là mảnh thuốc; "dlm" là viết tắt; mồi chứa moxifloxacin khi người bệnh đã kháng FQ. Theo vai trò thì không phương án nào đúng theo Bộ Y tế cho người lớn |
| (6) Đơn vị | Đạt: "(tên thuốc/phác đồ)" |

**Sửa cụ thể**

1. *(Bắt buộc, bản nháp)* Thay "người từ 14 tuổi trở lên" bằng "người lớn (≥ 14 tuổi)" / "an adult (≥ 14 years)" ở cả 4 trường. Đã chạy thử, QC đạt; VI 58/57 từ, EN 49/50 từ.
   - short_vi: "Với người lớn (≥ 14 tuổi) mắc lao phổi đơn thuần không nặng, kháng rifampicin và fluoroquinolone, chưa từng dùng thuốc lao hàng hai, không mang thai hay cho con bú, cân nặng ≥ 35 kg, BMI ≥ 17, QTcF, men gan và thần kinh ngoại biên bình thường, phác đồ nào được chỉ định (tên thuốc/phác đồ)?"
   - short_en: "For an adult (≥ 14 years) with pulmonary-only, non-severe tuberculosis resistant to rifampicin and fluoroquinolones, never treated with second-line TB drugs, not pregnant or breastfeeding, weighing ≥ 35 kg with BMI ≥ 17, and with normal QTcF, liver enzymes and peripheral nerve function, which regimen is indicated (drug names/regimen)?"
   - mcq_stem_vi / mcq_stem_en: cùng thay như trên; phần đuôi giữ nguyên ("phác đồ nào sau đây được chỉ định?" / "which of the following regimens is indicated?").
2. *(Bắt buộc, mã)* Chữ hiển thị phương án (sau khi `render.py` có trường hiển thị). Không ghi thời gian, và dùng 4 thuốc lõi cho E1 để độ dài các phương án tương đương:
   - vn: "bedaquilin + pretomanid + linezolid" / "bedaquiline + pretomanid + linezolid"
   - foreign WHO 2026: "bedaquilin + delamanid + linezolid + clofazimin" / "bedaquiline + delamanid + linezolid + clofazimine"
   - superseded: "bedaquilin + linezolid + clofazimin + cycloserin" / "bedaquiline + linezolid + clofazimine + cycloserine"
   - mồi: "bedaquilin + pretomanid + moxifloxacin + pyrazinamid" / "bedaquiline + pretomanid + moxifloxacin + pyrazinamide"
3. *(Bắt buộc, cấu hình)* Bí danh `bpal`, `bdq`, `lzd` và cách xử lý BDLC (vấn đề nghiêm trọng số 1).
4. *(HG3.5)* Thay mồi BPaMZ nếu chấm decoy_plausible không đạt, vì mồi chứa FQ trong khi người bệnh kháng FQ.
5. *(A3)* Dịch hoặc mở rộng cửa sổ để lấy dòng thành phần ở tr.54, và không kết thúc giữa câu. Gắn cờ tay "neighbour" cho "6 BPaLM".

---

## P-tbhiv-02 — verdict: **fix** (bản nháp giữ nguyên; sửa ở mẩu/mã/cấu hình)

**Mẩu**: 162/2024 tr.49, phác đồ C.
- Lao đa kháng còn nhạy FQ, phác đồ ngắn hạn 9–11 tháng.
- Bộ Y tế: {bedaquiline}.
- WHO 2019 và 1314/2020: {amikacin}.
- Mẩu **indistinguishable**, không có mồi.

| Tiêu chí | Đánh giá |
| --- | --- |
| (1) Duy nhất / "cũng đúng"? | Đạt. "Phác đồ chuẩn ngắn hạn 9–11 tháng" loại được BPaLM 6 tháng (hiện hành cùng quần thể). Amikacin không còn trong phác đồ C của 162/2024. Tôi đã kiểm cụm "phác đồ chuẩn ngắn hạn": **162/2024 cũng dùng cụm này** (tr.55 "Không sử dụng được PĐ chuẩn ngắn hạn", tr.62 "phác đồ chuẩn ngắn hạn (C1b)"), nên cụm này không nghiêng về bản cũ |
| (2) Lộ? | Đạt. Không có tên thuốc; "9–11" không phải giá trị của mẩu |
| (3) EN | Đạt. "The … standardized shorter regimen" là thuật ngữ WHO 2016–2019, nhưng không nêu tên thuốc nên chấp nhận được |
| (4) Tự nhiên | Đạt. "Lao đa kháng (kháng rifampicin)" gộp MDR với RR-TB, đúng cách 162/2024 gộp "LĐK/kháng R" |
| (5) Trắc nghiệm | **Không dựng được**: mẩu không có mồi. Filler cycloserine hợp lý: có thật, không có trong phác đồ ngắn hạn của nguồn nào đã ghi |
| (6) Đơn vị | Đạt |

**Sửa cụ thể**

1. *(Chủ mã / người dùng)* Miễn trắc nghiệm cho mẩu `indistinguishable` trong `build.py` (ưu tiên). Cách thay thế: người giữ mẩu thêm mồi, ứng viên capreomycin, qua `check_decoy`, và thêm vào grading.yaml.
2. *(Cấu hình)* `bdq`, `amikacin`, `prothionamide/pto`. Thiếu các mục này thì nhãn lệch phiên bản của mẩu luôn bằng 0 theo cấu tạo, và câu trả lời viết theo ký hiệu của chính 162/2024 bị chấm sai.
3. *(Ghi chú chấm)* Khóa một thuốc {bedaquiline} làm mọi câu có bedaquiline đều "đúng", kể cả câu trộn amikacin (mẩu đã ghi). Câu trả lời BPaLM bị gộp combo nên mất bedaquiline, và bị chấm nhãn 5 (hợp lý).
4. *(A3)* Đoạn trích thiếu thành phần phác đồ C1a; nên mở rộng cửa sổ để lấy dòng "4-6 Bdq(6)-Lfx-Pto-E-Z-Hh-Cfz / 5 Lfx-Cfz-Z-E".

---

## P-tbhiv-03 — verdict: **fix** (câu chữ đạt; sửa chữ phương án trắc nghiệm)

**Mẩu**: 162/2024 tr.44, A1.
- Người lớn, lao nhạy cảm, giai đoạn duy trì.
- Bộ Y tế: **HRE**.
- Xung đột: WHO 2026/2017, ATS 2016/2025: **HR**.
- Mồi: RE. Filler: HE.

| Tiêu chí | Đánh giá |
| --- | --- |
| (1) Duy nhất / "cũng đúng"? | Đạt. "Người lớn" loại A2 trẻ em (4RH, trùng HR). "Phác đồ chuẩn 6 tháng" loại 2HPZM/2HPM. Không nhiễm HIV và không có thai là tập con của quần thể. "Lao phổi **mới**" hẹp hơn quần thể, nhưng không hại |
| (2) Lộ? | Đạt. Không có tên thuốc hay ký hiệu phác đồ |
| (3) EN | Đạt |
| (4) Tự nhiên | Đạt |
| (5) Trắc nghiệm | Không phương án nào đúng theo Bộ Y tế. **Lỗi hình thức** (vấn đề nghiêm trọng số 4): chỉ vn và foreign có đuôi "(2HRZE/…)", và vn dùng thứ tự "RHE". Filler HE hợp lệ (không nguồn nào đã ghi khuyến cáo), nhưng cần lưu ý: Việt Nam **trước 2015** dùng 2SRHZ/**6HE** cho lao mới (không có trong superseded của mẩu, 4263/2015 đã là 4RHE). Mô hình nhớ lịch sử Việt Nam có thể chọn HE ở A1; bác sĩ nên xác nhận hoặc chọn filler khác |
| (6) Đơn vị | Đạt |

**Sửa cụ thể**

1. *(Người giữ mẩu hoặc chủ mã)* Đồng nhất chữ hiển thị theo cùng thứ tự H-R-E, bỏ đuôi ngoặc. Có thể làm bằng trường hiển thị riêng, để giữ nguyên `text` gốc của nguồn:
   - vn: "4HRE — isoniazid + rifampicin + ethambutol"
   - foreign: "4HR — isoniazid + rifampicin"
   - mồi: "4RE — rifampicin + ethambutol"
   - filler: "4HE — isoniazid + ethambutol" (giữ nguyên)
2. *(Tùy chọn, bác sĩ)* Xác nhận filler HE, hoặc thay bằng một phối hợp không có tiền sử dùng ở Việt Nam.

---

## P-tbhiv-04 — verdict: **pass**

**Mẩu**: 162/2024 tr.44, A2, trẻ em. Bộ Y tế HR; WHO và Mỹ HR (đối chứng).

| Tiêu chí | Đánh giá |
| --- | --- |
| (1) Duy nhất | Đạt. "Trẻ 5 tuổi" giữ nguyên số. "Phác đồ chuẩn 6 tháng" loại A2a 4 tháng (tr.45, trẻ 3 tháng–16 tuổi thể nhẹ) |
| (2) Lộ | Đạt |
| (3) EN | Đạt |
| (4) Tự nhiên | Đạt. Khung câu ghép cặp chặt với 03 |
| (5) Trắc nghiệm | Không áp dụng (concordant) |
| (6) Đơn vị | Đạt |

**Ghi chú**: đoạn A3 và `moh_neighbour` (vấn đề nghiêm trọng số 8). Người giữ mẩu nên thêm A1 người lớn (HRE) làm `moh_neighbour` của 04.

---

## P-tbhiv-05 — verdict: **fix** (câu chữ đạt; sửa ở cấu hình và mã)

**Mẩu**: 5968/2021 tr.29, Bảng 3.
- PEP cho người trên 10 tuổi.
- Bộ Y tế: TDF + 3TC (hoặc FTC) + DTG.
- Xung đột (CDC 2025): BIC/FTC/TAF và DTG + TAF.
- Mồi: TDF + 3TC + NVP.

| Tiêu chí | Đánh giá |
| --- | --- |
| (1) Duy nhất / "cũng đúng"? | Đạt. Hỏi phác đồ "ưu tiên" (loại LPV/r, RAL). Thận bình thường và không có thai loại phác đồ thay thế theo nguồn Mỹ. TDF + DTG cũng là phác đồ ưu tiên của CDC, nhưng điều đó không làm giá trị nước ngoài xung đột thành "đúng Bộ Y tế" |
| (2) Lộ? | Đạt. "Phơi nhiễm ngoài nghề nghiệp" là thuật ngữ của **chính** 5968/2021 tr.28 ("Phơi nhiễm ngoài môi trường nghề nghiệp"), nên không phải dấu hiệu CDC. Cụm này thừa vì đã nói quan hệ tình dục, nhưng vô hại |
| (3) EN | Đạt |
| (4) Tự nhiên | Đạt. "Người lớn (trên 10 tuổi)" hơi lạ (11–17 tuổi là vị thành niên), nhưng theo đúng quy tắc giữ số. *Tùy chọn:* "phác đồ ARV ưu tiên **để** dự phòng sau phơi nhiễm là gì" (đã thử, QC đạt, 59 từ) |
| (5) Trắc nghiệm | **Không đạt**: phương án là mảnh thuốc; VI chữ thường "taf + dtg"; 2 phương án foreign:US với 1 mồi (vấn đề nghiêm trọng số 2 và 5); mồi NVP khó được chọn (số 7). Theo vai trò thì không phương án nào đúng theo Bộ Y tế |
| (6) Đơn vị | Đạt |

**Sửa cụ thể**

1. *(Chặn, cấu hình)* bictegravir [bic], combo biktarvy, nevirapine [nevirapin, nvp], "tenofovir disoproxil", "tenofovir alafenamide", combo tld (vấn đề nghiêm trọng số 1), kèm test cho mọi chuỗi trong bảng ở mục đó.
2. *(Chặn, mã)* Chữ hiển thị phương án cùng dạng "NRTI + NRTI + thuốc thứ ba":
   - vn: "tenofovir disoproxil + lamivudin (hoặc emtricitabin) + dolutegravir" / "tenofovir disoproxil + lamivudine (or emtricitabine) + dolutegravir"
   - foreign US 1: "tenofovir alafenamide + emtricitabin + bictegravir" / "tenofovir alafenamide + emtricitabine + bictegravir"
   - foreign US 2: "tenofovir alafenamide + lamivudin (hoặc emtricitabin) + dolutegravir" / EN tương ứng
   - mồi: "tenofovir disoproxil + lamivudin + nevirapin" / "tenofovir disoproxil + lamivudine + nevirapine"
3. *(Quyết định trước OSF)* Xử lý 2 phương án nước ngoài (vấn đề nghiêm trọng số 5). Nếu chọn (a), người viết phải cung cấp filler kiểu drugs, và filler phải qua `check_decoy` (lưu ý EFV từng là phương án thay thế trong WHO 2014 PEP).

---

## P-tbhiv-06 — verdict: **pass**

**Mẩu**: 5968/2021 tr.29, PEP **28 ngày**. Đối chứng; WHO 2024 và CDC 2025 cùng giá trị.

- (1) Duy nhất: đạt.
- (2) Không lộ: câu không có số nào.
- (3) EN đạt. "Có nguy cơ" được dịch thành "high-risk", hơi mạnh hơn nhưng chấp nhận được.
- (4) Tự nhiên: đạt.
- (5) Trắc nghiệm: không áp dụng.
- (6) Đơn vị: "(ngày)".
- Thử bộ chấm: "28 ngày" và "4 tuần" → nhãn 2. "1 tháng" → không tách được (nhãn 5/6); gợi ý đơn vị "(ngày)" đã giảm rủi ro này.

---

## P-tbhiv-07 — verdict: **pass**

**Mẩu**: 162/2024 tr.59, lao kháng H nhạy R, **6 tháng**. Đối chứng với WHO 2026 B4.1.

- (1) Duy nhất: "Tổn thương không lan rộng, âm hóa đờm đúng hạn" loại được câu cho phép kéo dài ngay sau span. Không nhiễm HIV là tập con của quần thể.
- (2) Không lộ. Nêu thành phần phác đồ không phải là giá trị được hỏi.
- (3) EN đạt.
- (4) Tự nhiên đạt. "Âm hóa đờm đúng hạn" là thông tin trong quá trình điều trị, nhưng hợp lý khi hỏi "tổng thời gian".
- (5) Trắc nghiệm: không áp dụng.
- (6) Đơn vị: "(tháng)".
- Thử bộ chấm: "6 tháng" và "6 months" → nhãn 2. "24 tuần" → không tách được (normalize chưa đổi tuần sang tháng; lỗi nhỏ ở mức mã).

---

## Việc cần làm (tách theo người chịu trách nhiệm)

| # | Việc | Ai | Chặn? |
| --- | --- | --- | --- |
| 1 | Bổ sung bí danh/combo trong `grading.yaml` (BPaL, BPaLM, BDLC nở ra thành INN, bdq, lzd, amikacin, prothionamide, bictegravir, biktarvy, nevirapine, tld, "tenofovir disoproxil", "tenofovir alafenamide") và test với các chuỗi ở vấn đề nghiêm trọng số 1 | Chủ mã | **Chặn** chạy thí điểm mẩu 01, 02, 05 |
| 2 | `render.py`: tên hiển thị tách khỏi bí danh chấm điểm; phương án drugs/cat là phác đồ đầy đủ, cùng định dạng, không có thời gian hay chú thích | Chủ mã | **Chặn** trắc nghiệm 01, 03, 05 |
| 3 | Bản nháp 01: "người lớn (≥ 14 tuổi)" ở 4 trường (chữ ở trên, đã chạy thử QC) | Người viết câu hỏi | Nên sửa trước đóng băng |
| 4 | Miễn trắc nghiệm cho mẩu indistinguishable, hoặc thêm mồi cho 02 | Chủ mã / người dùng | Chặn "QC sạch" của tbhiv |
| 5 | Quyết định ô thứ 3 của trắc nghiệm (filler theo SKILL, hay chuẩn hóa theo số phương án), dùng chung với immunization | Người dùng + rev-methods | Chặn OSF |
| 6 | HG3.5: chấm decoy_plausible cho BPaMZ (01) và NVP (05); bác sĩ xác nhận filler HE (03) và giới hạn tuổi mục trẻ em 162/2024 (01) | Bác sĩ / người dùng | Chặn phép so H1 trên các mẩu này |
| 7 | A3: 01 (thiếu thành phần, cắt giữa câu, dấu văn thư, cờ neighbour BPaLM), 02 (thiếu thành phần), 04 (thêm `moh_neighbour` A1, dịch cửa sổ về A2) | Người giữ mẩu / chủ mã | Kiểm tay trước đóng băng |

---

## Xử lý sau phản biện (atom-extractor + question-writer, agent AI, 2026-09-26; mã qgen/grade 1.1.0/decoys mới; không xem đầu ra mô hình)

Sửa ở `data/interim/pilot/tbhiv.jsonl` (bản trước: scratchpad `qfix/tbhiv_atoms_before.jsonl`) và `qdrafts/tbhiv.jsonl`. Kiểm lại:

- `pilot_merge --only tbhiv`: giữ 7, loại 0. Trạng thái không đổi: conflict 3, indistinguishable 1, concordant 3. Dung sai 0.
- `qgen.build --only-drafted`: 26 câu (short 14, mcq 12), 7 đoạn A3, **0 mục QC không đạt** (exit 0). 4 mẩu bỏ trắc nghiệm có chủ đích: 02 (không mồi), 04/06/07 (đối chứng).
- Chấm thử bằng câu tự viết: 33/34 đúng kỳ vọng. Mục lệch là câu phác đồ trẻ em (vấn đề 3), xem bên dưới.

| Mục phản biện | Trạng thái | Bằng chứng |
| --- | --- | --- |
| 1. Bộ chấm (BPaL, BDLC, bdq, amikacin, pto, BIC/FTC/TAF, Biktarvy, TLD, "tenofovir disoproxil") | **Xong** (grading.yaml 1.1.0) | 'BPaL' → 2; 'BDLC' → 4; 'Bdq Lzd Cfz Cs + 1 thuốc nhóm C' → 3; '4-6 Bdq-Lfx-Pto-E-Z-Hh-Cfz' → 2; 'amikacin, levofloxacin, prothionamide…' → 3; 'BIC/FTC/TAF', 'Biktarvy' → 4; 'TLD', 'tenofovir disoproxil + lamivudine + dolutegravir' → 2. BDLC nở ra thành INN nên key_drugs [delamanid, clofazimine] giữ nguyên |
| 2. Phương án là mảnh thuốc | **Xong** | option_text đủ ô cho 01, 03, 05 (phác đồ đầy đủ, tên INN theo drug_display.yaml, không thời gian/chú thích); QC vai trò đọc lại đạt |
| 3. Tuổi mẩu 01 | **Xong** | Bản nháp đã dùng "người lớn (≥ 14 tuổi)"; population.age của mẩu nay trùng câu. Còn cần bác sĩ xác nhận giới hạn tuổi mục trẻ em (HG) |
| 4. Hình thức phương án 03 | **Xong** | 4HRE / 4HR / 4RE / 4HE, thứ tự H-R-E, không đuôi ngoặc; cat_options đọc đúng (HE không nhãn), không đổi cat_options |
| 5. Ô 3 của 05 | **Xong** (mã theo SKILL) | Ô 3 = filler TAF + FTC + NVP (không nguồn nào đã ghi; bộ chấm không xếp vào nguồn nào) |
| 6. 02 không mồi | **Giữ trống**, bỏ trắc nghiệm có chủ đích | capreomycin không có trong grading.yaml; mọi INN lao khác có trong grading.yaml đều thuộc phác đồ Bộ Y tế/nguồn đã ghi (lý do ghi ở extraction.decoy_rule) |
| 7. Mồi 01, 05 | **Thay** (agent_proposed, chờ HG3.5) | 01: BPaMZ → **BPaZ** {pretomanid, pyrazinamide} (không FQ). 05: NVP → **TLE** {efavirenz}. check_decoy = []. Câu trả lời theo nguồn đã ghi không bật decoy_match |
| 8. A3 | Một phần | Mã passages mới đã bỏ dấu văn thư và câu cụt ở 01. 04 thêm moh_neighbour A1 (HRE, tr.44), nên nay có cờ 'neighbour'. Còn lại: xem mục kiểm tay |

Chi tiết mồi mới (không nguồn nào đã ghi khuyến cáo cho quần thể; kiểm 26/9):

- **01 — BPaZ** (tránh FQ vì người bệnh kháng FQ):
  - 162/2024: tìm 'BPaZ' = []. 'Pretomanid' xuất hiện ở tr.16/20/47/48/53/160/189; tr.48 ghi "hiện chỉ áp dụng đối với phác đồ BPaL(M)".
  - 2760/2021 và 1314/2020: 'Pretomanid' = [].
  - WHO 2026/2022/2020 và ATS 2025: 'BPaZ' / 'pretomanid and pyrazinamide' = 0 kết quả. Danh mục phác đồ WHO 2026 (PDF tr.10) không có BPaZ.
  - Thử chấm: 'bedaquiline + pretomanid + pyrazinamide' và 'BPaMZ' → 5 kèm decoy_match. 'BPaL', 'BDLC', E1, 'BPaLM' → decoy_match False.
- **05 — TLE**:
  - 5968/2021: 'EFV'/'Efavirenz' không xuất hiện ở tr.28–30. Bảng 3 tr.29 không có EFV.
  - WHO 2024 PEP: 'efavirenz'/'EFV' = 0 kết quả.
  - CDC 2025: EFV chỉ có trong phần bàn luận NNRTI, không có trong Bảng 4 (ưu tiên: BIC/FTC/TAF hoặc DTG + TAF/TDF + FTC/3TC; thay thế: DRV/c hoặc DRV/r + …).
  - Thử chấm: 'TDF + 3TC + EFV', 'TLE' → 5 kèm decoy_match.
  - **Rủi ro chưa kiểm được**: 5456/2019 chưa có trong data/raw, và WHO 2014 PEP chưa tải. Nếu một trong hai từng liệt kê EFV cho PEP thì phải đổi mồi.

Còn treo (không sửa được ở mẩu/bản nháp, hoặc là việc của người):

- **Chủ mã (grading.yaml)**:
  - Bí danh 'bpaz' (quy ước đối xứng với 'bdlc'). 'bpamz' nay không còn là mồi.
  - 'BPaLC' (WHO 2026 B1.1b) chưa đọc được, cho nhãn 6. Nếu thêm như combo gộp thì sẽ khớp tập con BPaL, cho nhãn 2: cần quyết định.
  - "24 tuần" (07) và "1 tháng" (06) vẫn cho nhãn 5 (chưa quy đổi tuần/tháng ↔ tháng/ngày).
- **Bộ chấm, ghi nhận (vấn đề 3)**: câu trả lời theo phác đồ trẻ em kháng FQ của 162/2024 ('Bdq + Lzd + Cfz + Cs + Dlm') bị chấm nhãn 3 (bản cũ + WHO). Câu hỏi dùng "người lớn (≥ 14 tuổi)" để tránh trường hợp này; bác sĩ xác nhận giới hạn tuổi.
- **A3, kiểm tay trước đóng băng**:
  - 01: đoạn A3 thiếu dòng thành phần tr.54 (đoạn không qua trang), nhưng có tên "Phác đồ BPaL"; cờ 'neighbour' (6 BPaLM).
  - 02: dòng thành phần C1a nằm ở khoảng từ thứ 299 của tr.49, ngoài cửa sổ 300 từ tính từ span tiêu chuẩn thu nhận. Muốn lấy dòng này phải dời span hoặc nới cửa sổ (chủ mã / người dùng).
  - 03: cờ 'foreign:US; foreign:WHO_global; neighbour' (đoạn có A2 4RH).
  - 04: cờ 'neighbour' (A1).
- **Người dùng**:
  - moh_scope của 01/03/05 (kiểm ngữ cảnh, prereg §3.2).
  - HG3.5: decoy_plausible cho BPaZ, TLE, RE, và filler HE/NVP.
  - HG1.2/HG3.9 cho mẩu 01 (mã hóa temporal_confounded, hiệu lực 2760/2021).
  - Đưa 5456/2019 vào data/raw để kiểm lại mồi TLE.

---

## Xử lý sau kiểm độc lập — vòng 3 (atom-extractor + question-writer, agent AI, 2026-09-26; người kiểm rev-methods + rev-clinician cũng là AI, không phải bác sĩ; không xem đầu ra mô hình)

Sửa ở `data/interim/pilot/tbhiv.jsonl` (bản trước: scratchpad `qfix/tbhiv_atoms_before.jsonl` và `qfix/tbhiv_r3_before/`) và `qdrafts/tbhiv.jsonl`. Kịch bản idempotent: `qfix/tb_edit3.py`; cat_options sinh từ `qfix/tb_cat3.py` (kèm 115 câu thử); chấm thử `qfix/tb_grade3.py`.

**Đính chính vòng 2:** dòng "4. Hình thức phương án 03 … cat_options đọc đúng (HE không nhãn)" ở bảng trên là SAI. Người kiểm tìm ra 3 lỗi đọc (dấu phẩy Oxford, nhãn 6 cho câu có nội dung, HE → 6). Các lỗi này đã sửa ở vòng này.

Kiểm lại:

- `pilot_merge --only tbhiv`: giữ 7, loại 0. Trạng thái không đổi: conflict 3 (01, 03, 05), indistinguishable 1 (02), concordant 3 (04, 06, 07). Dung sai đều 0. check_decoy = [] cho 01/03/05.
- `qgen.build --only-drafted`: 26 câu (short 14, mcq 12), 7 đoạn A3, **0 mục QC không đạt**, exit 0. 4 mẩu bỏ trắc nghiệm có chủ đích: 02, 04, 06, 07.
- Chấm thử bằng câu tự viết (không phải đầu ra mô hình):
  - `tb_grade3.py`: 29/29 đúng kỳ vọng. Đáp án Bộ Y tế → 2 (01–07). Nước ngoài → 4 (01 BDLC, 03 HR, 05 BIC/FTC/TAF và DTG + TAF). Bản cũ → 3 (01 E1, 02 amikacin). Mồi → 5 kèm decoy_match.
  - `tb_cat3.py`: 115/115 đúng tập nhãn và đúng nhãn ở cả 03 lẫn 04.
  - Bộ thử của người kiểm (`rv/rv_cat.py`, `rv/rv_cat2.py`): 0 lệch.

| # | Phát hiện của người kiểm | Trạng thái | Bằng chứng / việc đã làm |
| --- | --- | --- | --- |
| 0 | 05: mồi TLE trùng phương án thay thế của WHO 2014 PEP | **(i) xong; chờ quyết định (ii)/(iii)** | `sources fetch` WHO 2014 (sha256 4319686155242daf…, 52 trang). grep: tr.11, 23 "Where available, RAL, DRV/r or EFV can be considered as alternative options"; tr.24 "EFV has also been previously recommended". Đã ghi vào extraction.decoy_rule. Không tự đổi mồi: nevirapine bị loại (WHO 2014 tr.25 "should not be used" cho PEP người lớn). Doravirine sạch (WHO 2024 = 0, WHO 2014 = 0, 5968/2021 = [], CDC 2025 chỉ ở phần bàn luận và tài liệu tham khảo) nhưng chưa có trong grading.yaml |
| 1 | 03/04: cat_options đọc sai | **Xong** | Viết lại từ khối có tên. Dấu nối nhận ", and" / ", và" / "plus". Đọc mệnh đề sau từ dẫn (continue, then, tiếp tục, duy trì…). Pyrazinamide bị phủ định không còn chặn câu. Thêm nhãn HE và HRZE (→ 5). Danh sách chữ viết tắt không đọc đoạn con. Mẫu RE/HE theo tên chỉ khớp khi hai tên đứng liền. Nay "Continuation phase: isoniazid, rifampin, and ethambutol…" ở 04 → 5 (trước: 2) |
| 2 | Cat nhiều nhãn (câu rào đón) → nhãn 2 | **Chuyển chủ mã** (grade.py) | Đã thử lại: "4HR hoặc 4HRE", "HR (WHO) or HRE", "4HR; 4HRE if high isoniazid resistance", "2RHZE/4RHE hoặc 2RHZE/4RH tùy tuổi" đều ra Cat{HR, HRE}, nhãn 2, multi=False ở cả 03 và 04. Việc này trái quy tắc `multi_value_without_vn_designation`. Tệp mẩu không sửa được. Đề xuất: Cat có nhãn Bộ Y tế cùng nhãn khác thì xử lý như nhiều giá trị (nhãn 5, hoặc 1 nếu có quy thuộc nguồn), kèm test |
| 3 | 01: không đọc "Pa"; thiếu "bpaz" | **Chuyển chủ mã** (grading.yaml) | Đã kiểm: 162/2024 tr.55 viết "(Bdq, Pa)". Luật "~" đòi ≥ 3 thuốc khác đã nhận, nên thêm "~pa" vẫn không đọc được "Bdq + Pa + Lzd". Cần chủ mã quyết cách xử lý. Đã ghi vào extraction.decoy_rule của 01 |
| 4 | 03: trắc nghiệm gợi đáp án qua độ dài và phần hợp | **Xong** | Filler HE → **HRZE** ("4HRZE — isoniazid + rifampicin + pyrazinamide + ethambutol"). Số thuốc chung với các phương án khác: HRE 7, HRZE 7, HR 5, RE 5. Nay phần hợp và phương án dài nhất là filler. Với HRZ (đề xuất của người kiểm), HRE vẫn cao nhất duy nhất (6 so với 5/5/4). check_decoy/filler_issues = []. Không văn bản Bộ Y tế nào trong kho, cũng không WHO 2017, ATS 2016, ATS 2025, dùng 4HRZE. Ghi trung thực: WHO 2026 PDF tr.52 có chuỗi "(i.e. 4HRZE/2HR)" ở mục trẻ em, thể nặng (quần thể khác) |
| 5 | 02: ghi chú capreomycin sai | **Xong** | Đã sửa decoy_rule. 1314/2020 tr.58 "Thay thế kanamycin, capreomycin bằng amikacin"; tr.113, 116 là bảng liều. Bỏ hướng "thêm capreomycin vào grading.yaml". Kết luận để trống mồi không đổi |
| 6 | 02: sót meropenem | **Xong** | 162/2024 tr.47: "Imipenem-cilastatin HOẶC Meropenem" thuộc Nhóm C, dùng cho chính quần thể lao kháng R. Đây là thuốc tiêm tĩnh mạch, kém hợp lý trong phác đồ ngắn hạn toàn uống. check_decoy = [] về mã nhưng loại, lý do đã ghi. Người dùng có thể đưa vào HG3.5 |
| 7 | 01: họ mồi {Pa, Z}; lâm sàng | **Xong (ghi chú)** | decoy_match bao cả họ (kể cả BPaMZ), không nguồn nào ghi phác đồ trong họ này. Kháng Z hay gặp ở lao đa kháng/tiền siêu kháng: ghi vào HG3.5. 162/2024 tr.55 cho hoàn thành bằng (Bdq, Pa); phối hợp này không có Z nên không khớp mồi |
| 8 | 05: "người lớn (trên 10 tuổi)" nghĩa lạ | **Xong** | population.age → "người lớn". Bỏ "(trên 10 tuổi)" / "(over 10 years of age)" ở 4 trường của bản nháp. Người lớn là tập con của nhóm "Người trên 10 tuổi" ở Bảng 3. Bỏ mốc 10 tuổi cũng bỏ luôn một mốc chia tuổi riêng của nguồn |
| 9 | 05: filler NVP kém hợp lý | **Ghi HG3.5** | WHO 2014 tr.25 ghi không dùng NVP cho PEP người lớn; tr.11–12, 25 chỉ nêu NVP là phương án theo tuổi cho trẻ < 10 tuổi. Trong grading.yaml không còn thuốc thứ ba nào khác chưa thuộc nguồn đã ghi hoặc mồi |

Phát hiện thêm của người sửa ở vòng này (tự kiểm bằng công cụ):

- **162/2024 tr.71** (mục lao/HIV, "người mắc lao phát hiện nhiễm HIV và chưa điều trị thuốc ARV") có câu: "… phác đồ 06 tháng có Rifampicin (2HRZE/4HR) thường được sử dụng". Cùng trang lại ghi "Sử dụng phác đồ điều trị chuẩn 06 tháng 2RHZE/4RHE cho người nhiễm HIV mắc lao nhạy cảm thuốc". Như vậy văn bản mâu thuẫn nội bộ ở quần thể HIV (A1 tr.44 ghi 4RHE).
  - Đã ghi thành moh_neighbour của 03 (span 513 ký tự, span_on_page = True).
  - Câu hỏi 03 nêu "không nhiễm HIV", nên đây là bối cảnh lân cận. Trạng thái mẩu không đổi.
  - Cần bác sĩ thật đọc lại (HG3.9). Agent không kết luận Bộ Y tế dùng HR cho người nhiễm HIV.

Việc còn treo:

- **Chủ mã:**
  - (a) grade.py: Cat nhiều nhãn (mục 2), kèm test.
  - (b) grading.yaml: đọc "Pa" và thêm bí danh "bpaz" (mục 3).
  - (c) Nếu người dùng chọn phương án doravirine cho 05: thêm `doravirine: [doravirin, dor]` và test.
  - (d) Nếu muốn ghi WHO 2014 thành nguồn nước ngoài cũ của 05: cần lopinavir/atazanavir.
- **Người dùng / HG3.5:**
  - Mồi 05: chọn (a) TDF + 3TC + DOR sau (c) ở trên, hoặc (b) giữ TLE, ghi hạn chế và đánh dấu mẩu ở phân tích π_d.
  - decoy_plausible cho BPaZ (01), RE (03), mồi 05.
  - Tính hợp lý của filler HRZE (03) và NVP (05).
- **Bác sĩ thật (HG3.9):**
  - Câu tr.71 của 162/2024 (2HRZE/4HR ở người nhiễm HIV chưa ARV).
  - Giới hạn tuổi mục trẻ em (01).
- **Chưa kiểm được:** 5456/2019 (chưa vào data/raw, lỗi TLS) và CDC 2005 nPEP (cdc.gov trả "Access Denied").
