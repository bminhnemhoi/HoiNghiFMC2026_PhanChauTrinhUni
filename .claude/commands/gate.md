---
description: Liệt kê việc chờ người dùng và cách xác nhận đã xong
allowed-tools: Bash(scripts/vs *)
---
!`scripts/vs todo`

Trình bày cho người dùng từng việc đang chờ (mã HG, việc cần làm, thông tin cần gửi lại, hạn). Nhắc cách xác nhận: gõ **XONG <mã> <thông tin>** thành một tin nhắn bình thường (không phải lệnh /). Khi họ đã gõ, hook tạo xác nhận; bạn ghi thông tin vào file `outputs` của task rồi chạy `scripts/vs human-done <mã> --note "..."` và tiếp tục /next.
