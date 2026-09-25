#!/usr/bin/env python3
"""PreToolUse(Edit|Write|MultiEdit|NotebookEdit): protect inputs, frozen data, state and results."""
import fnmatch
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import block, log_error, read_input, rel, setup  # noqa: E402

PROTECTED = [
    ("docs/01_DE_CUONG.md", "Đề cương là đầu vào chỉ đọc. Thay đổi phạm vi → ghi docs/DECISIONS.md và hỏi người dùng."),
    ("docs/02_KE_HOACH_TRIEN_KHAI.md", "Kế hoạch là đầu vào chỉ đọc. Thêm việc bằng: scripts/vs add ..."),
    ("docs/03_PROMPT_CLAUDE_CODE.md", "Prompt khởi tạo là đầu vào chỉ đọc."),
    ("data/raw/*", "data/raw chỉ nhận file tải về (qua script tải), không sửa tay."),
    ("data/raw/**", "data/raw chỉ nhận file tải về (qua script tải), không sửa tay."),
    ("data/frozen/**", "Dữ liệu đã đóng băng: không sửa. Cần sửa → tạo phiên bản mới + ghi DECISIONS + hỏi người dùng."),
    ("data/frozen/*", "Dữ liệu đã đóng băng: không sửa."),
    ("prereg/submitted/*", "Bản đăng ký trước đã nộp là bất biến; thay đổi → viết addendum trong prereg/addenda/."),
    ("prereg/submitted/**", "Bản đăng ký trước đã nộp là bất biến."),
    ("state/progress.json", "Chỉ cập nhật trạng thái qua scripts/vs (start/done/block/...)."),
    ("state/HUMAN_TODO.md", "File tự sinh từ state; dùng scripts/vs."),
    ("state/budget_ledger.csv", "Sổ ngân sách chỉ ghi qua vnsoc.budget."),
    ("state/.human_ack/*", "Chỉ người dùng tạo xác nhận (gõ 'XONG <mã>' trong chat)."),
    ("results/numbers.json", "Số kết quả chỉ được ghi bởi mã phân tích qua vnsoc.numbers.put(); không gõ tay."),
    (".env", "Không đọc/sửa .env (khóa bí mật). Người dùng tự điền."),
    (".claude/settings.json", "Không tự sửa lớp kiểm soát (hook/quyền). Đề xuất thay đổi cho người dùng."),
    (".claude/hooks/*", "Không tự sửa hook. Đề xuất thay đổi cho người dùng."),
]


def main() -> int:
    data = read_input()
    root = setup(data)
    try:
        ti = data.get("tool_input") or {}
        path = ti.get("file_path") or ti.get("notebook_path") or ""
        if not path:
            return 0
        r = rel(root, path)
        for pat, why in PROTECTED:
            if fnmatch.fnmatch(r, pat):
                block(f"CHẶN sửa {r}: {why}")
    except SystemExit:
        raise
    except Exception:
        log_error(root, "guard_files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
