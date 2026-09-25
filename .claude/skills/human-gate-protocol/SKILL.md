---
name: human-gate-protocol
description: Cách chuẩn bị, trình bày và xác nhận các việc chỉ người dùng làm được (HG…) — tài khoản, khóa, nộp bài, email, pháp lý, bác sĩ — và cách block task đúng cách.
---
# Cổng người dùng

1. **Chuẩn bị trước**: khi một HG sắp tới (phụ thuộc gần xong), soạn sẵn mọi thứ người dùng cần: bản nháp email (tiếng Việt, lịch sự, ngắn), file cần nộp, danh sách bước bấm, thông tin cần gửi lại. Lưu ở `state/gates/<HG>.md` và nhắc trong câu trả lời.
2. **Trình bày**: mỗi HG gồm: việc gì, vì sao chỉ người làm được, các bước (đánh số), hạn, và câu cần gõ khi xong: `XONG <HG> <thông tin>`.
3. **Xác nhận**: chỉ hook UserPromptSubmit tạo `state/.human_ack/<HG>` khi một dòng tin nhắn của người dùng BẮT ĐẦU bằng `XONG <HG>`. Cổng quyết định sau hội đồng có mã HGM2/HGM3/HGM4. Bạn ghi thông tin họ đưa (URL, mã, ngày) vào file `outputs` của task (ví dụ `state/gates/HG2.9_osf.txt`), rồi `scripts/vs human-done <HG> --note "..."`.
4. **Không bao giờ**: tự tạo xác nhận; đoán rằng người dùng đã làm; gửi email/đăng ký/nộp thay; lưu mật khẩu hay khóa vào repo; mô tả AI phản biện như người thật.
5. **Block đúng cách**: task của bạn cần người dùng → `scripts/vs block <ID> --reason "<cụ thể: cần gì, ở đâu, vì sao>"`; HUMAN_TODO tự cập nhật. Khi họ cung cấp xong → `scripts/vs unblock <ID>`.
6. **Hạn gấp** (FMC 30/9/2026, đóng băng 15/10/2026, đăng ký FMC 30/11/2026): nhắc ở đầu mỗi câu trả lời khi còn ≤ 3 ngày.
