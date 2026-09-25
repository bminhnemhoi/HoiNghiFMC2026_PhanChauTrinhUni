#!/usr/bin/env python3
"""PreCompact: leave a breadcrumb in docs/LOG.md so work resumes cleanly after context compaction."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import log_error, read_input, setup  # noqa: E402


def main() -> int:
    data = read_input()
    root = setup(data)
    try:
        from vnsoc.paths import paths
        from vnsoc.state import append_log, load

        P = paths(root)
        if P.progress.exists():
            st = load(P)
            doing = [i for i in st["order"] if st["tasks"][i]["status"] == "in_progress"]
            append_log(P, f"nén ngữ cảnh ({data.get('trigger', '?')}); đang làm: {', '.join(doing) or 'không'}")
    except Exception:
        log_error(root, "precompact")
    return 0


if __name__ == "__main__":
    sys.exit(main())
