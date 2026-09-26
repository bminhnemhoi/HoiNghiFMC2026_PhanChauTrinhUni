# Giao thức trích mẩu khuyến cáo — nghiên cứu chính (agent AI thay LLM trả phí)

Phiên bản 1.1, ngày 27/9/2026 (1.0 → 1.1 sau đợt trích thử 4 văn bản và kiểm toán độc lập: review/extraction_calibration/). Tài liệu này dành cho các agent trích mẩu. Nó bám theo đề cương §3.4 và §4.1, skill
`atomization-protocol` và prereg §3.1. Ở thí điểm, người dùng làm một mình trên laptop, không dùng API trả phí, nên việc
trích giao cho agent AI; mọi mẩu được kiểm bằng mã rồi kiểm toán AI kép (docs/DECISIONS.md 2026-09-26T20:40). Băm tệp
này được ghi ở `extraction.protocol_sha256` của mỗi mẩu (và `extraction.protocol` = "extraction_protocol 1.1").

## 1. Đơn vị: một mẩu = một khuyến cáo có GIÁ TRỊ cho MỘT quần thể/bối cảnh

Mẩu là một câu hoặc một ô bảng trong văn bản Bộ Y tế, cho một giá trị cụ thể mà câu hỏi trả lời ngắn có thể hỏi:
- **dose**: liều, tốc độ truyền, liều nạp, liều tối đa;
- **threshold**: ngưỡng chẩn đoán, chỉ định, nhập viện, chuyển tuyến, xét nghiệm;
- **duration**: thời gian điều trị hoặc theo dõi, khoảng cách giữa các lần dùng;
- **schedule**: lịch tiêm hoặc lịch dùng thuốc theo ngày/tháng;
- **first_line**: thuốc hoặc phác đồ lựa chọn đầu tay;
- **target**: đích điều trị (huyết áp, HbA1c, LDL...);
- **classification**: mốc phân độ hoặc phân loại có giá trị số;
- (các slot_type khác trong `src/vnsoc/schemas.py` nếu hợp).

**Không** lấy:
- câu mô tả, dịch tễ học, dược lý chung, ví dụ minh họa;
- khoảng giá trị bình thường của xét nghiệm (trừ khi là ngưỡng hành động);
- giá trị không gắn với quần thể xác định;
- nội dung ở trang bìa hoặc trang quyết định;
- khuyến cáo chỉ nói "theo hướng dẫn của nhà sản xuất".

Tách thành nhiều mẩu khi một câu có nhiều quần thể (người lớn và trẻ em; từng mức cân nặng) hoặc nhiều giá trị khác slot.
Nhiều giá trị cùng đúng cho CÙNG quần thể trong CÙNG văn bản thì đưa hết vào tập `vn` của một mẩu (value set, đề cương §1.2).

## 2. Trường bắt buộc (schema `Atom`, src/vnsoc/schemas.py)

| Trường | Quy tắc |
|---|---|
| `atom_id` | `A-<số_năm>-NNN`, ví dụ `A-1857_2022-001`, đánh liên tục trong một văn bản |
| `guideline` | khóa văn bản `NNNN/YYYY` hoặc `TT51/2017` |
| `page` | số trang PDF, đếm từ 1 (không phải số in trên giấy); ghi số in ở `extraction.printed_page` nếu khác |
| `section` | đường dẫn đề mục (chương, mục, điểm), đúng như văn bản |
| `span` | NGUYÊN VĂN, là chuỗi con của chữ trang (sau chuẩn hóa khoảng trắng), ≤ 600 ký tự, chứa đủ giá trị và quần thể. Trang OCR: chép đúng lớp chữ OCR (kể cả lỗi) để khớp, và ghi chữ đúng theo ảnh ở `extraction.ocr_reading` |
| `disease`, `condition`, `intervention` | ngắn, tiếng Việt |
| `population` | dict thuộc tính quần thể: tuổi, cân nặng, giới, thai kỳ/tam cá nguyệt, mức độ bệnh, bệnh kèm, nơi đo, tuyến, đường dùng... Số của khóa định lượng (`age`, `weight`, `gestational_age`, `trimester`) phải có thật trong văn bản. KHÔNG ghi chú của người trích vào đây |
| `required_terms` | cho mỗi thuộc tính phân loại quyết định đáp án (ví dụ đo tại phòng khám, HBeAg dương, sốc còn bù): `{"key": {"vi": [...], "en": [...]}}` |
| `slot_type`, `value_kind` | như mục 1; `value_kind` ∈ num / bp / schedule / drugs / cat |
| `unit` | bắt buộc với num, dùng đơn vị chuẩn của bộ đọc số (`src/vnsoc/normalize_vi.py` UNIT_ALIASES: mg, mg/kg, mg/kg/day, ml/kg/h, mmol/L, %, day, month, year, IU, kg/m2, U/L, IU/mL, mmHg...) |
| `vn` | danh sách ValueItem: num `{"lo","hi","unit","cmp","text"}`; bp `{"sys","dia","cmp","text"}`; schedule `{"seq","unit","text"}`; drugs `{"key_drugs":[INN chữ thường có trong configs/grading.yaml],"text"}`; cat `{"label","text"}` kèm `cat_options` (regex không dấu, chữ thường) |
| `valid_from`, `partially_amended_by` | theo manifest |
| `foreign`, `superseded`, `decoy` | ĐỂ TRỐNG ở bước trích; bước ghép đối chiếu điền sau |
| `pilot` | `false` |
| `extraction` | `{"agent": "atom-extractor", "protocol": "extraction_protocol 1.1", "protocol_sha256": "<sha256 của tệp này>", "date": ..., "notes": ...}` |

Không bao giờ đặt `moh_lags_evidence`, `clinical_harm`, `clinician_confirmed`, `decoy_plausible`.

## 3. Kiểm bằng mã (bắt buộc, lặp đến khi sạch)

```
PYTHONUTF8=1 .venv/bin/python -m vnsoc.extract.atoms_merge --only <số_năm> --out <scratch>/<số_năm>.jsonl
```
Lệnh phải báo 0 mẩu bị LOẠI. Mỗi mẩu phải thỏa: schema hợp lệ; `verify_span` tìm thấy span trên đúng trang; mọi giá trị
`vn` đọc lại được từ span (hoặc từ span DR8 ghi ở `extraction.dr8_sources`). Không sửa span cho khớp giá trị; không điền giá
trị hay quần thể từ trí nhớ.

## 4. Phạm vi và độ phủ

Đọc HẾT phần chuyên môn của văn bản hoặc của khoảng trang được giao, lần lượt từng trang. Lấy MỌI mẩu thỏa mục 1, không
chọn theo khả năng có xung đột với nước ngoài. Việc chọn theo xung đột sẽ làm lệch nhóm đối chứng; trạng thái xung đột do
mã tính ở bước sau. Ghi các trang đã đọc vào `data/interim/atoms_parts/<số_năm>_coverage.md`.

## 5. Quy tắc bổ sung (1.1, từ đợt trích thử)

1. **Không gộp khác quần thể.** Mỗi dòng bảng, mỗi quần thể và mỗi bối cảnh (điều trị hay dự phòng, người lớn hay trẻ em, từng mức cân nặng) là một mẩu riêng, KỂ CẢ khi giá trị giống mẩu khác. Bỏ các dòng này để "tránh trùng" sẽ làm lệch nhóm đối chứng.
2. **Khuyến cáo phân loại không có số cũng là mẩu (value_kind cat).** Gồm:
   - chỉ định và chống chỉ định;
   - "không khuyến cáo / không dùng X" cho một quần thể;
   - nơi điều trị, nhập viện, chuyển tuyến;
   - phương thức hỗ trợ.

   Quy ước chọn slot:
   - thuốc hoặc phương án lựa chọn → `first_line`;
   - câu Có/Không về chỉ định, chống chỉ định hoặc an toàn → `procedure`, với nhãn `indicated` / `not_indicated` / `contraindicated`;
   - kỹ thuật chẩn đoán → `procedure`.

   Đối xứng: đã lấy "không dùng X" ở quần thể A thì cũng lấy câu tương ứng ở quần thể B.
3. **Tần suất** ("2 lần/ngày") → `slot_type: schedule`, `value_kind: num`, đơn vị tần suất của bộ đọc số. **Khoảng cách giữa hai lần dùng** → `duration`. Ngưỡng hai chiều ("< 40 hoặc > 130") → tách hai mẩu, chiều ghi trong `required_terms`.
4. **Câu thuật lại quy định nước ngoài** (FDA, EMA, WHO "phê duyệt", "khuyến cáo của …") KHÔNG phải khuyến cáo của Bộ Y tế: không lấy; ghi vào tệp bỏ qua (mục 6) với lý do `attributed_to_foreign`.
5. **`required_terms` bắt buộc cho mọi thuộc tính phân biệt đáp án:**
   - dạng bào chế hoặc muối (metoprolol succinate);
   - đường dùng;
   - pha liều (khởi đầu, đích, tối đa, liều thấp);
   - chiều ngưỡng;
   - cấp hay mạn;
   - nhánh lưu đồ hoặc pha bệnh;
   - tuổi viết bằng chữ ("sơ sinh");
   - dân tộc hoặc khu vực, khi ngưỡng quốc tế của slot khác nhau theo dân tộc (BMI, vòng bụng).

   Khi hai mẩu trở lên cùng condition + intervention, mọi thuộc tính khác nhau giữa chúng phải nằm trong `required_terms`.
6. **Không thay đơn vị hay thuốc để qua kiểm.** Ví dụ cấm: 'l' thay L/min, 'cm' thay cmH2O, 'g' thay g/L, cat thay drugs chỉ vì thiếu bí danh. Nếu bộ đọc số hoặc bảng thuốc chưa hỗ trợ thì KHÔNG tạo mẩu. Ghi vào `data/interim/atoms_parts/<số_năm>_skipped.jsonl`, mỗi dòng `{"page", "span_excerpt" (≤ 200 ký tự), "reason", "proposed"}`. Giá trị `reason`:
   - `drug_table_gap` (kèm INN đề xuất);
   - `unit_gap`;
   - `image_only` (giá trị chỉ có trong hình hoặc lưu đồ dạng ảnh);
   - `span_across_pages`;
   - `combination_dose` ("49/51 mg");
   - `attributed_to_foreign`;
   - `ambiguous_scope`;
   - `other`.

   Người điều phối bổ sung bộ đọc rồi cho trích lại các dòng này.
7. **Phạm vi mơ hồ** (điều kiện "nếu …" áp cho phần nào, phạm vi của "hoặc"): chọn quần thể hẹp nhất mà mọi cách hiểu đều đúng; ghi `extraction.ambiguity` để bước kiểm ngữ cảnh xem.
8. **Văn bản tự mâu thuẫn** (hai giá trị không khớp cho cùng quần thể trong cùng văn bản, hoặc lỗi soạn thảo): vẫn lấy nguyên văn và ghi `extraction.internal_conflict` = {"pages", "note"}. Bước câu hỏi loại mẩu này khỏi tập xác nhận.
9. **Văn bản sửa đổi:** mẩu từ đoạn đã bị sửa (ví dụ 5481/2020 tr.39 điểm b, sửa bởi 1353/2021) phải dùng văn bản ĐÃ SỬA. Ghi nguồn sửa đổi ở `extraction.dr8_sources`.
10. **Chồng lấn giữa các văn bản Bộ Y tế** (5642/2015 ch.8 cúm với 1840/2025; ch.5 sốt rét với 3377/2023; 5904/2019 với 3192/2010, 5481/2020, 2131/2026; 678/2025 với 1740/2026, 5968/2021): trích bình thường từ mỗi văn bản. Hợp tập DR8 làm ở bước sau theo họ bệnh.
