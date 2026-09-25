---
description: Đóng băng một tập dữ liệu (corpus | atoms | questions) sau khi đủ điều kiện
argument-hint: corpus|atoms|questions
---
Đóng băng **$ARGUMENTS** theo mục “Đóng băng” trong docs/02_KE_HOACH_TRIEN_KHAI.md:
1. Kiểm tra điều kiện của task đóng băng tương ứng (T2.7 / T3.12 / T4.3) đã đủ: schema hợp lệ, kiểm tra chất lượng đạt, cổng người dùng liên quan đã xong.
2. Chạy `$PY -m vnsoc.freeze $ARGUMENTS`: kiểm schema, chép sang `data/frozen/<tên>_v<N>.*`, ghi `data/frozen/SHA256SUMS`, KHÔNG ghi đè bản đã có.
3. Ghi `docs/DECISIONS.md` (ngày, số dòng, mã băm) và `docs/LOG.md`. Commit.
Không bao giờ sửa bản đã đóng băng; cần thay đổi thì tạo v<N+1> và ghi lý do.
