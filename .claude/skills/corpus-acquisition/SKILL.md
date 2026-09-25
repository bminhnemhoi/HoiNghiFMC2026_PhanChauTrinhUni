---
name: corpus-acquisition
description: Quy trình tìm, tải, kiểm và lập danh mục văn bản hướng dẫn Bộ Y tế từ nguồn chính thức, dựng chuỗi thay thế và đóng băng kho (T2.1–T2.7). Dùng khi làm việc với data/raw, manifest, supersession.
---
# Lấy kho hướng dẫn Bộ Y tế

## Nguồn được phép (theo thứ tự)
1. `kcb.vn/phac-do`, `kcb.vn/tai-lieu`, `kcb.vn/tin-tuc` (PDF ký số của Cục Quản lý Khám, chữa bệnh).
2. `moh.gov.vn` (cổng Bộ Y tế), `vncdc.gov.vn`.
3. Trang Sở Y tế / bệnh viện đăng lại nguyên quyết định (ghi rõ host; ưu tiên bản có chữ ký số).
**Cấm**: thuvienphapluat.vn (điều khoản cấm công cụ tự động, robots `ai-train=no`) — hook chặn. Văn bản chỉ có ở đó → thêm vào danh sách người dùng tự tìm bản chính thức (HG2.3).

## Quy trình
1. **Danh mục ứng viên** (T2.1): bắt đầu từ bảng mục 3.1 đề cương (52 quyết định đã kiểm kê + các văn bản bổ sung: 1622/2014, TT 10/2024, 1470/2024, 678/2025, 5904/2019, 5642/2015, 6101/2019, 3610/2015). Mỗi văn bản một dòng `ManifestRow` (`src/vnsoc/schemas.py`), khóa `doc_key = "số/năm"`.
2. **Tìm PDF**: WebSearch với `site:kcb.vn "<số>/QĐ-BYT"` và tên bệnh; mở trang bằng WebFetch; lấy link PDF.
3. **Tải**: `curl -sSL -o data/raw/<số>_<năm>.pdf "<url>"`; rồi `sha256sum`; `pdfinfo` (số trang); `pdftotext -l 3` để kiểm có lớp chữ (≥ 200 ký tự tiếng Việt có dấu/ trang → có).
4. **Hiệu lực**: tìm trong văn bản các câu “thay thế”, “bãi bỏ”, “hết hiệu lực” (PyMuPDF search) → `supersedes`, `superseded_by`, `partially_amended_by` (ví dụ 2388/2024 chỉ thay vài chương của 3931/2015). Không suy từ trí nhớ; chưa rõ → `notes`.
5. **Chọn kho** (T2.5): 25–35 văn bản **hiện hành** có PDF chính thức có lớp chữ (`in_corpus: true`), ưu tiên bệnh giàu xung đột (dengue, sốt rét, dại, viêm gan B, tăng huyết áp, đái tháo đường, phản vệ, lao, tiêm chủng, truyền nhiễm tổng hợp); bản cũ để phân tích phiên bản không tính vào con số này; tối đa 10 văn bản OCR (Tesseract `vie`, mọi con số so với ảnh trang, ghi `ocr: true`).
6. **Đóng băng** (T2.7, không trước 15/10/2026): `$PY -m vnsoc.freeze corpus`. Văn bản ban hành sau ngày đóng băng: không thêm (DR7), chỉ ghi chú.

## Kiểm tra xong
- `$PY -m vnsoc.schemas manifest data/interim/manifest.jsonl` OK; mọi dòng `in_corpus` có `sha256`, `source_url` không phải TVPL, file PDF tồn tại.
- Báo cáo `results/tables/corpus_triage.csv`: 52+ văn bản × (có PDF chính thức?, lớp chữ?, bản quét?, chỉ thấy ở TVPL?).
- Ghi giờ công vào docs/LOG.md (ngân sách 45–100 giờ cho cả phần này).
