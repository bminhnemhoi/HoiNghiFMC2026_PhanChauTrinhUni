# Giao thức trích mẩu khuyến cáo — nghiên cứu chính (agent AI thay LLM trả phí)

Phiên bản 1.0, ngày 27/9/2026. Tài liệu này dành cho các agent trích mẩu. Nó bám theo đề cương §3.4 và §4.1, skill
`atomization-protocol` và prereg §3.1. Ở thí điểm, người dùng làm một mình trên laptop, không dùng API trả phí, nên việc
trích giao cho agent AI; mọi mẩu được kiểm bằng mã rồi kiểm toán AI kép (docs/DECISIONS.md 2026-09-26T20:40). Băm tệp
này được ghi ở `extraction.protocol` của mỗi mẩu.

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
| `extraction` | `{"agent": "atom-extractor", "protocol": "extraction_protocol 1.0", "date": "2026-09-27", "notes": ...}` |

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
