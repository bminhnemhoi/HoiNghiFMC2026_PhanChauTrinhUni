---
description: Xem tiến độ, ngân sách, việc chờ người dùng
allowed-tools: Bash(scripts/vs *), Bash(.venv/bin/python -m vnsoc.budget *)
---
!`scripts/vs digest`

!`scripts/vs list`

Tóm tắt cho người dùng bằng tiếng Việt trong ≤ 10 dòng: pha hiện tại, % task xong, việc đang làm, việc bị chặn (lý do), việc chờ người dùng (kèm hạn gần nhất), ngân sách API đã dùng, giờ GPU đã dùng (cộng từ docs/LOG.md). Không bắt đầu task mới.
