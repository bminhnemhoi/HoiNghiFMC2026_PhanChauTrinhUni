#!/usr/bin/env python3
"""UserPromptSubmit: the ONLY place where a human-gate acknowledgement is created.
When a line of the user's message STARTS with 'XONG HG1.9' (or 'DONE HG1.9'), write state/.human_ack/HG1.9,
so `scripts/vs human-done HG1.9` can succeed. Claude cannot create these files (guards block it)."""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import log_error, read_input, setup  # noqa: E402

ACK = re.compile(r"^\s*(?:XONG|DONE)\s+(HG[\w.]*\w)", re.I | re.M)  # only at the start of a line


def main() -> int:
    data = read_input()
    root = setup(data)
    try:
        prompt = data.get("prompt") or ""
        ids = [m.upper() for m in ACK.findall(prompt)]
        if not ids:
            return 0
        from vnsoc.paths import paths
        from vnsoc.state import now

        P = paths(root)
        P.human_ack.mkdir(parents=True, exist_ok=True)
        for i in ids:
            (P.human_ack / i).write_text(f"{now()}\n{prompt[:2000]}\n", encoding="utf-8")
        print(f"[hook] Người dùng xác nhận đã xong: {', '.join(ids)}. Ghi bằng chứng họ cung cấp (nếu task yêu cầu) "
              f"rồi chạy `scripts/vs human-done <mã> --note \"...\"`, sau đó /next.")
    except Exception:
        log_error(root, "user_prompt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
