#!/usr/bin/env python3
"""PreToolUse(Bash): block commands that break the project's legal, integrity, budget or safety rules."""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import block, log_error, read_input, setup  # noqa: E402

PROTECTED = r"(?:data/raw|data/frozen|prereg/submitted|docs/0[123]_|state/|\.git\b|results/numbers\.json)"

RULES = [
    (r"thuvienphapluat",
     "CHẶN: không truy cập tự động thuvienphapluat.vn (điều khoản cấm công cụ tự động; robots ai-train=no). "
     "Chỉ người dùng được tra thủ công. Dùng kcb.vn / moh.gov.vn / trang Sở Y tế, bệnh viện."),
    (r"\.human_ack",
     "CHẶN: xác nhận việc của người dùng chỉ được tạo khi chính người dùng gõ 'XONG <mã>' trong chat."),
    (rf"\brm\s+(?:-\w*\s+)*.*{PROTECTED}",
     "CHẶN: không xóa dữ liệu gốc/đóng băng/đăng ký trước/tài liệu đầu vào/state. Hỏi người dùng."),
    (rf"\b(?:mv|truncate|shred)\b.*{PROTECTED}",
     "CHẶN: không di chuyển/ghi đè dữ liệu được bảo vệ. Hỏi người dùng."),
    (rf"(?:>|tee\s+(?:-a\s+)?)\s*\S*{PROTECTED}",
     "CHẶN: không ghi thẳng vào vùng được bảo vệ bằng shell. state/ chỉ qua scripts/vs; results/numbers.json "
     "chỉ qua vnsoc.numbers.put() trong mã phân tích."),
    (r"\bgit\s+push\b.*(?:--force|-f\b|--force-with-lease)", "CHẶN: không force-push."),
    (r"\bgit\s+(?:reset\s+--hard|clean\s+-\w*[fdx])", "CHẶN: lệnh git phá hủy thay đổi. Hỏi người dùng."),
    (r"\bgit\s+(?:filter-branch|filter-repo|rebase\s+-i)", "CHẶN: không viết lại lịch sử git."),
    (r"(?:^|[;&|]\s*)(?:printenv|env|set)\s*(?:$|[;&|])", "CHẶN: không in biến môi trường (có khóa bí mật)."),
    (r"\b(?:cat|less|more|head|tail|bat|nl|strings|xxd|od|grep|awk|sed|cp|scp)\b[^|;&]*(?:\.env(?![\w.])|kaggle\.json|\.netrc|"
     r"credentials|\.huggingface/token)",
     "CHẶN: không đọc file chứa khóa bí mật. Mã Python tự nạp .env qua python-dotenv."),
    (r"echo\s+.*\$\{?\w*(?:KEY|TOKEN|SECRET|PASSWORD)\w*", "CHẶN: không in khóa bí mật."),
    (r"\bsudo\b", "CHẶN: không dùng sudo. Ghi việc cần quyền quản trị vào HUMAN_TODO bằng scripts/vs block."),
    (r"--dangerously-skip-permissions|bypassPermissions", "CHẶN: không tắt lớp kiểm soát quyền."),
    (r"(?:^|[;&|(]\s*|\s)claude\s+(?:.*\s)?(?:-p|--print)\b|scripts/autopilot\.sh",
     "CHẶN: không gọi lồng Claude Code / autopilot từ bên trong phiên. Autopilot do người dùng chạy ở terminal."),
    (r"\bkaggle\s+(?:datasets|kernels)\s+\w+\b.*(?:--public|\s-u\b)|\bis_private\"?\s*:\s*false",
     "CHẶN: dataset/kernel Kaggle phải để riêng tư (có văn bản Bộ Y tế và trọng số mô hình có giấy phép)."),
    (r"\b(?:zenodo|osf)\b.*\b(?:publish|submit|actions/publish)\b",
     "CHẶN: công bố Zenodo / nộp OSF là việc của người dùng (human gate). Chỉ tạo bản nháp."),
]
API_RUN = re.compile(r"vnsoc\.run\.api_batch\s+submit|vnsoc\.run\.api_sync|openai\s+api|genai\.Client")


def main() -> int:
    data = read_input()
    root = setup(data)
    try:
        cmd = (data.get("tool_input") or {}).get("command", "")
        flat = " ".join(cmd.split())
        for pat, msg in RULES:
            if re.search(pat, flat, re.I):
                block(f"{msg}\n(lệnh: {flat[:200]})")
        if API_RUN.search(flat):
            from vnsoc import budget

            if budget.remaining() <= 0:
                block("CHẶN: đã hết ngân sách API (trần cứng). " + budget.status_line())
    except SystemExit:
        raise
    except Exception:
        log_error(root, "guard_bash")
    return 0


if __name__ == "__main__":
    sys.exit(main())
