---
description: Kiểm tra toàn vẹn (test, số liệu, trích dẫn, kế hoạch) + audit độc lập
allowed-tools: Bash(make *), Bash(scripts/vs *)
---
!`make verify 2>&1 | tail -40`

Nếu có lỗi: liệt kê và sửa những gì thuộc phần việc của bạn. Sau đó giao agent `integrity-auditor` kiểm tra độc lập (tính lại 3 số ngẫu nhiên trong results/numbers.json từ dữ liệu, kiểm 10 trích dẫn, kiểm 10 mẩu ngẫu nhiên về trích nguyên văn) và ghi `review/audit_<ngày>.md`. Báo người dùng kết quả.
