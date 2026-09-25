---
name: atomization-protocol
description: Quy trình trích mẩu khuyến cáo từ PDF Bộ Y tế bằng LLM giá rẻ + kiểm khớp nguyên văn + kiểm ngữ cảnh + kiểm tra chất lượng phân tầng (T1.1, T3.1–T3.4, T3.10). Dùng khi tạo hoặc kiểm atoms.
---
# Trích mẩu khuyến cáo (đề cương §3.4, §4.1)

## Đầu vào → đầu ra
PDF trong kho (manifest `in_corpus`) + bản cũ → `data/interim/atoms.jsonl` (schema `Atom`), `data/interim/extraction_rejects.jsonl`.

## Các bước
1. **Tách văn bản có vị trí** (`src/vnsoc/extract/pdf_to_text.py`): PyMuPDF theo trang và khối; bảng liều bằng pdfplumber; giữ số trang; tách theo đề mục (heading số La Mã/1.2.3). Bản quét → OCR + đối chiếu ảnh.
2. **Trích bằng LLM** (`atomize.py`): mỗi đề mục một yêu cầu, nhiệt độ 0, JSON theo schema rút gọn (condition, population, slot_type, intervention, value text, span, page). Qua `vnsoc.run.api_batch` (Batch, rẻ). Prompt ghi trong `configs/prompts_extract.yaml`, băm prompt vào `extraction.prompt_hash`.
3. **Kiểm khớp nguyên văn** (`verify_span.py`): `span` phải là chuỗi con của văn bản trang (sau chuẩn hóa khoảng trắng); giá trị phải parse được từ `span` bằng `normalize_vi` và khớp giá trị LLM đưa ra. Không khớp → reject (lý do).
4. **Dựng value set**: đổi sang `ValueItem` theo `value_kind`; đơn vị chuẩn; quần thể đầy đủ (tuổi/cân nặng, thai kỳ, G6PD, HBeAg, nơi đo…). Nhiều giá trị cùng hợp lệ trong văn bản hiện hành → một tập (mục 1.2).
5. **Kiểm ngữ cảnh** (T3.4 + HG3.5): công cụ `review_ui` (HTML tĩnh hoặc CSV) hiển thị span, trang, quần thể, giá trị, giá trị nước ngoài; sinh viên kiểm **100% mẩu xung đột** theo `review/adjudication_rubric.md` (đúng bệnh? đúng quần thể? đúng can thiệp? giá trị có điều kiện kèm theo?). Lần hai sau ≥ 7 ngày trên mẫu ngẫu nhiên 20% → báo cáo đồng thuận (kappa).
6. **Kiểm tra chất lượng phân tầng** (mẫu ở T3.4, người dùng kiểm ở HG3.6, tính ở T3.10): 200 mẩu (100 ngẫu nhiên + 100 xung đột); độ chính xác với KTC Clopper–Pearson; cận dưới < 90% → sửa prompt, chạy lại (DR1).

## Không được
- Điền giá trị/quần thể từ trí nhớ; sửa `span` cho khớp; gộp hai quần thể vào một mẩu.
- Dùng mẩu có `span_verified: false` hoặc `context_checked != pass` trong phân tích chính.

## Thí điểm (T1.1)
Từ `data/seed/seed_conflicts.yaml` (dòng `pilot: true`) + khoảng 10 mẩu lệch phiên bản + 30 mẩu đối chứng: tải PDF tương ứng (nguồn chính thức), tìm đoạn chứa giá trị, tạo atom có `span` + `page` thật. Dòng nào không tìm được PDF/đoạn → bỏ khỏi thí điểm và ghi lý do (không bịa). Người dùng kiểm trích dẫn ở HG1.2.
