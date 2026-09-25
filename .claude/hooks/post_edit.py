#!/usr/bin/env python3
"""PostToolUse(Edit|Write|MultiEdit): fast syntax checks. Exit 2 shows the error to Claude."""
import json
import os
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import log_error, read_input, setup  # noqa: E402


def main() -> int:
    data = read_input()
    root = setup(data)
    try:
        path = (data.get("tool_input") or {}).get("file_path") or ""
        if not path or not os.path.exists(path):
            return 0
        err = None
        if path.endswith(".py"):
            r = subprocess.run([sys.executable, "-m", "py_compile", path], capture_output=True, text=True)
            if r.returncode:
                err = r.stderr
            elif shutil.which("ruff"):
                r = subprocess.run(["ruff", "check", "--select", "E9,F63,F7,F82", "--quiet", path],
                                   capture_output=True, text=True)
                if r.returncode:
                    err = r.stdout[-2000:]
        elif path.endswith(".json"):
            try:
                json.load(open(path, encoding="utf-8"))
            except Exception as e:  # noqa: BLE001
                err = f"JSON lỗi: {e}"
        elif path.endswith((".yaml", ".yml")):
            try:
                import yaml  # may be missing in system python

                yaml.safe_load(open(path, encoding="utf-8"))
            except ImportError:
                pass
            except Exception as e:  # noqa: BLE001
                err = f"YAML lỗi: {e}"
        elif path.endswith(".jsonl"):
            with open(path, encoding="utf-8") as f:
                for i, line in enumerate(f, 1):
                    if line.strip():
                        try:
                            json.loads(line)
                        except Exception as e:  # noqa: BLE001
                            err = f"JSONL lỗi dòng {i}: {e}"
                            break
        if err:
            print(f"Lỗi cú pháp trong {path}:\n{err}\nSửa ngay trước khi làm tiếp.", file=sys.stderr)
            return 2
    except Exception:
        log_error(root, "post_edit")
    return 0


if __name__ == "__main__":
    sys.exit(main())
