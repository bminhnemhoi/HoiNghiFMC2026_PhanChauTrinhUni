## D. Việc bổ sung từ báo cáo của các agent (26/9/2026)

1. **QĐ 1622/QĐ-BYT (08/5/2014, bệnh dại):** link PDF chính thức cũ đã chết; bản chính thức còn lại là tệp .doc trên vncdc.gov.vn (trang tin nd13747; chứng chỉ TLS của trang đã hết hạn nên công cụ tự động không tải an toàn được). Mở bằng trình duyệt, tải tệp .doc, lưu vào `data/raw/manual/1622_2014.doc`, rồi báo Claude chạy `vnsoc.extract.doc_to_pdf` (chuyển bằng Word, có ghi nguồn gốc).
2. **QĐ 1840/2025 (cúm mùa) và QĐ 1019/2025 (sởi):** agent không xác minh được hai văn bản này có tồn tại. Tra số hiệu/ngày (được phép tra thủ công trên trang thư viện pháp luật tư nhân) và tìm bản PDF chính thức.
3. **QĐ 2855/2024 (viêm gan C), 2065/2021 (viêm gan C cũ), 678/2025 (dự phòng lây truyền mẹ–con):** không tìm thấy trên kcb.vn / vaac.gov.vn / vncdc.gov.vn. Kiểm lại số hiệu trong đề cương.
4. **QĐ 3705/2019 (dengue, bản cũ):** file đang có (từ medinet.gov.vn và benhvienhatrung.vn) là bản quét mang watermark LuatVietnam. Tìm bản sạch; nếu không có, quyết định có dùng bản này cho phân tích phiên bản không (cần OCR và so tay).
5. **Thông tư tiêm chủng:** TT 10/2024 đã bị TT 52/2025 thay, và TT 52/2025 hết hiệu lực từ 01/7/2026 (thay bằng TT 13/2026). Xác định văn bản hiện hành nào chứa lịch tiêm chủng mở rộng.
6. **QĐ 5456/QĐ-BYT (2019, dự phòng sau phơi nhiễm HIV — cần cho P-tbhiv-05):** trang vaac.gov.vn lỗi chứng chỉ TLS nên công cụ tự động không tải được. Mở bằng trình duyệt, tải PDF chính thức, lưu `data/raw/manual/5456_2019.pdf`.
7. **Văn bản tiêm chủng hiện hành (cho P-immunization-01/-02/-04):** tìm hướng dẫn chuyên môn về lịch tiêm chủng mở rộng còn hiệu lực sau 01/7/2026 (Cục Phòng bệnh / vncdc.gov.vn). Manh mối: QĐ 1637/QĐ-BYT (2015) quy định mũi sởi–rubella lúc 18 tháng (chưa có trong kho). Lưu vào `data/raw/manual/<số>_<năm>.pdf`.
8. **(Tùy chọn) TT 08/1999/TT-BYT (phản vệ, bản cũ):** chỉ cần nếu muốn có giá trị "bản cũ" cho các mẩu phản vệ. Nguồn chính thức (moh.gov.vn, vanban.chinhphu.vn).
