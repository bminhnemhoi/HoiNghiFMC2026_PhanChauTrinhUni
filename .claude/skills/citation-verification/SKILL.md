---
name: citation-verification
description: Quản lý manuscript/references.yaml và kiểm chứng mọi trích dẫn qua Crossref/DataCite/arXiv; không bao giờ trích từ trí nhớ (T2.8, P7, P8).
---
# Trích dẫn đã kiểm chứng

- Mỗi tài liệu một mục trong `manuscript/references.yaml`: `key, title, authors, year, venue, doi | arxiv | url, checked_by_human (chỉ cho luật/quyết định/trang web, sau HG7.3)`.
- Chỉ thêm tài liệu đã mở được trang (WebFetch) hoặc tra được qua API: Crossref `https://api.crossref.org/works?query.bibliographic=<tiêu đề>&rows=5`, DataCite cho arXiv `https://api.datacite.org/dois?query=<từ khóa>&client-id=arxiv.content&page[size]=25&sort=-created`, arXiv `https://export.arxiv.org/api/query?id_list=<id>`, PubMed E-utilities `esearch.fcgi`/`esummary.fcgi` (kèm `NCBI_API_KEY` nếu có, ≤ 3 yêu cầu/giây).
- Chạy `$PY scripts/verify_citations.py` → `manuscript/citations_verified.json`; mọi mục phải `ok` hoặc `ok_manual` trước khi nộp. `MISMATCH` → sửa theo bản ghi gốc, không sửa bản ghi cho khớp bài.
- Số liệu lấy từ bài khác (ví dụ 74,5% của Wang & Suresh; 86,7–95% của Bazerbachi) phải được đối chiếu với bản gốc trước khi nộp (đề cương ghi các số này lấy qua công cụ đọc web).
- Tài liệu Việt Nam: tìm thêm trên tapchiyhocvietnam.vn (từ khóa “ChatGPT”, “phác đồ”, “Bộ Y tế”, “mô hình ngôn ngữ lớn”) — việc đề cương ghi là chưa làm được.
- Định dạng đầu ra: JMIR dùng AMA/Vancouver đánh số; IJMI dùng kiểu Elsevier số — xuất bằng pandoc + CSL khi dàn trang (T8.1).
