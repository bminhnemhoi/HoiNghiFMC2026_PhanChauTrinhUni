#!/usr/bin/env python3
"""Stop: keep Claude working while autopilot is on and a Claude task is eligible.
Exit 2 + stderr = Claude continues with that message as its instruction.

Loop guards: state/PAUSE; state/AUTOPILOT_ON missing; at most MAX_STALL consecutive continues
without any change to state/progress.json; at most MAX_TOTAL continues per session."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import log_error, read_input, setup  # noqa: E402

MAX_STALL = 3
MAX_TOTAL = 60


def main() -> int:
    data = read_input()
    root = setup(data)
    try:
        from vnsoc.paths import paths
        from vnsoc.state import eligible_claude, fingerprint, load, waiting_human

        P = paths(root)
        if P.pause.exists() or not P.autopilot.exists() or not P.progress.exists():
            return 0
        sid = str(data.get("session_id") or "unknown")
        cdir = P.state / ".stop_counters"
        cdir.mkdir(parents=True, exist_ok=True)
        cfile = cdir / f"{sid}.json"
        c = json.loads(cfile.read_text()) if cfile.exists() else {"fp": None, "stall": 0, "total": 0}
        fp = fingerprint(P)
        c["stall"] = 0 if fp != c["fp"] else c["stall"] + 1
        c["fp"] = fp
        st = load(P)
        el = eligible_claude(st)
        if not el or c["stall"] >= MAX_STALL or c["total"] >= MAX_TOTAL:
            c["stall"] = 0
            cfile.write_text(json.dumps(c))
            return 0
        c["total"] += 1
        cfile.write_text(json.dumps(c))
        t = el[0]
        wh = waiting_human(st)
        msg = (f"[autopilot] Còn việc bạn làm được ngay: {t['id']} — {t['title']} (trạng thái {t['status']}). "
               f"Làm tiếp theo quy trình /next: đọc `scripts/vs show {t['id']}`, làm, rồi `scripts/vs done {t['id']}`. "
               "Nếu thật sự cần người dùng (khóa, quyết định, tài liệu), chạy "
               f"`scripts/vs block {t['id']} --reason \"...\"` rồi dừng.")
        if c["stall"] >= 1:
            msg += (f" LƯU Ý: lần dừng trước không có tiến triển trong state ({c['stall']}/{MAX_STALL}); "
                    "nếu đang kẹt thì block task thay vì lặp lại.")
        if wh:
            msg += " (Việc chờ người dùng: " + ", ".join(x["id"] for x in wh) + " — nhắc lại trong câu trả lời cuối.)"
        print(msg, file=sys.stderr)
        return 2
    except Exception:
        log_error(root, "stop_continue")
    return 0


if __name__ == "__main__":
    sys.exit(main())
