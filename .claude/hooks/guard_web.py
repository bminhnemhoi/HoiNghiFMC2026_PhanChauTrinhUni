#!/usr/bin/env python3
"""PreToolUse(WebFetch): no automated access to sites whose terms forbid it."""
import os
import sys
from urllib.parse import urlparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import block, log_error, read_input, setup  # noqa: E402

BLOCKED_HOSTS = {
    "thuvienphapluat.vn": "điều khoản cấm công cụ tự động và cấm xây hệ thống tra cứu khác; robots.txt ai-train=no. "
                          "Ghi URL vào HUMAN_TODO để người dùng tự mở và đối chiếu.",
}


def main() -> int:
    data = read_input()
    root = setup(data)
    try:
        url = (data.get("tool_input") or {}).get("url", "")
        host = (urlparse(url).hostname or "").lower()
        for h, why in BLOCKED_HOSTS.items():
            if host == h or host.endswith("." + h):
                block(f"CHẶN WebFetch {host}: {why}")
    except SystemExit:
        raise
    except Exception:
        log_error(root, "guard_web")
    return 0


if __name__ == "__main__":
    sys.exit(main())
