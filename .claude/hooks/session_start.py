#!/usr/bin/env python3
"""SessionStart: inject a short project digest (plain stdout is added to Claude's context)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import log_error, read_input, setup  # noqa: E402


def main() -> int:
    data = read_input()
    root = setup(data)
    try:
        from vnsoc.paths import paths
        from vnsoc.state import digest

        P = paths(root)
        if not P.progress.exists():
            print("[vn-soc-audit] Chưa khởi tạo state. Làm theo docs/03_PROMPT_CLAUDE_CODE.md mục Khởi tạo.")
            return 0
        print(digest(P))
        print("Quy trình: /next để làm việc kế tiếp · /status · /gate khi người dùng báo xong việc · "
              "mọi thay đổi trạng thái qua scripts/vs. Đọc CLAUDE.md nếu chưa đọc trong phiên này.")
        if data.get("source") == "compact":
            print("Phiên vừa được nén ngữ cảnh: đọc lại task đang làm bằng `scripts/vs show <ID>` trước khi tiếp tục.")
    except Exception:
        log_error(root, "session_start")
    return 0


if __name__ == "__main__":
    sys.exit(main())
