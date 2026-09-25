---
description: Bật/tắt chế độ tự làm liên tục (hook Stop)
argument-hint: on|off
allowed-tools: Bash(scripts/vs *)
---
!`scripts/vs autopilot $ARGUMENTS`

Giải thích ngắn: khi bật, hook Stop giữ Claude làm task kế tiếp cho đến khi chỉ còn việc của người dùng, gặp PAUSE, hoặc 3 lần liên tiếp không có tiến triển. Muốn chạy không cần ngồi canh: chạy `scripts/autopilot.sh` ở terminal.
