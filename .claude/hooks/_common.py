"""Shared helpers for hooks. Stdlib only (runs with the system python3).
Exit codes (Claude Code): 0 = allow/continue; 2 = block (PreToolUse) or keep working (Stop);
stderr of an exit-2 hook is shown to Claude. Hooks FAIL OPEN on their own bugs (log + exit 0)."""
from __future__ import annotations

import json
import os
import sys
import traceback
from pathlib import Path


def read_input() -> dict:
    try:
        return json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        return {}


def project_dir(data: dict | None = None) -> Path:
    d = os.environ.get("CLAUDE_PROJECT_DIR") or (data or {}).get("cwd") or os.getcwd()
    return Path(d).resolve()


def setup(data: dict | None = None) -> Path:
    root = project_dir(data)
    os.environ.setdefault("VNSOC_ROOT", str(root))
    src = str(root / "src")
    if src not in sys.path:
        sys.path.insert(0, src)
    return root


def block(msg: str) -> None:
    print(msg, file=sys.stderr)
    sys.exit(2)


def log_error(root: Path, name: str) -> None:
    try:
        d = root / "logs" / "hooks"
        d.mkdir(parents=True, exist_ok=True)
        with (d / f"{name}.err").open("a", encoding="utf-8") as f:
            f.write(traceback.format_exc() + "\n")
    except Exception:
        pass


def rel(root: Path, p: str) -> str:
    try:
        return str(Path(p).resolve().relative_to(root))
    except Exception:
        return p
