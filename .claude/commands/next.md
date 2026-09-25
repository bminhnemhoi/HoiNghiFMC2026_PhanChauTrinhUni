---
description: Làm trọn vẹn task kế tiếp trong kế hoạch (start → làm → kiểm tra → done → commit)
allowed-tools: Bash(scripts/vs *)
---
## Trạng thái
!`scripts/vs digest`

## Task kế tiếp
!`scripts/vs next || true`

## Quy trình bắt buộc
1. Nếu kết quả là `NONE`: đọc `state/HUMAN_TODO.md`, nhắc người dùng những việc đang chờ họ (kèm hạn), rồi dừng.
2. `scripts/vs start <ID>` nếu task chưa ở trạng thái in_progress.
3. Đọc các trường của task (title, acceptance, outputs, check, skill, agent, instructions). Tìm mục liên quan trong `docs/02_KE_HOACH_TRIEN_KHAI.md` (Grep theo mã task) và trong `docs/01_DE_CUONG.md` (theo § được nhắc). Không đọc cả file.
4. Nạp skill ghi trong task bằng Skill tool; nếu task ghi `agent`, giao phần việc nặng cho subagent đó (công cụ Agent, tên cũ Task) với đầu vào/đầu ra rõ ràng.
5. Làm việc theo CLAUDE.md: mã + test trước, chạy nhỏ trước khi chạy lớn, không bịa, tiền/GPU qua các module có kiểm soát.
6. `scripts/vs done <ID> --note "<kết quả chính, lấy từ file>"`. Lệnh kiểm tra thất bại → đọc lỗi, sửa, chạy lại (tối đa 3 lần) → vẫn hỏng thì `scripts/vs block <ID> --reason "<cụ thể: cần gì từ người dùng>"`.
7. `git add -A && git commit -m "<ID>: <tóm tắt>"` (nếu chưa có repo: `git init` trước).
8. Báo người dùng 2–4 dòng: làm gì, số chính (trích từ file), task tiếp theo, việc đang chờ họ.
Nếu còn task làm được ngay, tiếp tục task sau theo đúng quy trình này.
