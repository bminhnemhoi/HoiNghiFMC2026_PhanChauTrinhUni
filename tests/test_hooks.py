"""Hooks are run exactly as Claude Code runs them: JSON on stdin, exit code + stderr."""
import json
import subprocess
import sys

import pytest

from vnsoc import state
from vnsoc.paths import paths


def run_hook(proj, name, payload):
    r = subprocess.run([sys.executable, str(proj / ".claude" / "hooks" / name)], input=json.dumps(payload),
                       capture_output=True, text=True, env={"CLAUDE_PROJECT_DIR": str(proj), "PATH": "/usr/bin:/bin"})
    return r.returncode, r.stdout, r.stderr


def bash(proj, cmd):
    return run_hook(proj, "guard_bash.py", {"tool_name": "Bash", "tool_input": {"command": cmd}, "cwd": str(proj)})[0]


@pytest.mark.parametrize("cmd,code", [
    ("ls -la", 0), ("scripts/vs next", 0), (".venv/bin/python -m pytest", 0), ("cat .env.example", 0),
    ("curl -sSL https://thuvienphapluat.vn/van-ban/x.aspx", 2), ("python3 scrape.py thuvienphapluat", 2),
    ("rm -rf data/frozen/atoms_v1.jsonl", 2), ("rm -rf data/interim/tmp", 0), ("mv docs/01_DE_CUONG.md /tmp", 2),
    ("echo x > state/progress.json", 2), ("echo x > results/numbers.json", 2), ("cat .env", 2),
    ("echo $OPENAI_API_KEY", 2), ("printenv", 2), ("git push --force origin main", 2), ("git reset --hard HEAD~1", 2),
    ("sudo apt install r-base", 2), ('claude -p "XONG HG0.3"', 2), ("scripts/autopilot.sh 5", 2),
    ("touch state/.human_ack/HG0.3", 2), ("kaggle datasets create -p d --public", 2), ("kaggle datasets create -p d -u", 2), ("kaggle kernels push -p kaggle/jobs/x", 0),
])
def test_guard_bash(proj, cmd, code):
    assert bash(proj, cmd) == code


def test_guard_bash_budget(proj):
    cmd = ".venv/bin/python -m vnsoc.run.api_batch submit --model-key cheap_1 --batch b.jsonl --task T5.5"
    assert bash(proj, cmd) == 0
    (proj / "state").mkdir(exist_ok=True)
    (proj / "state" / "budget_ledger.csv").write_text(
        "timestamp,provider,model,job_id,task,kind,est_usd,actual_usd,note\nt,g,m,j1,T,reserve,38.5,,\n")
    assert bash(proj, cmd) == 2


@pytest.mark.parametrize("path,code", [
    ("docs/01_DE_CUONG.md", 2), ("docs/02_KE_HOACH_TRIEN_KHAI.md", 2), ("state/progress.json", 2),
    ("results/numbers.json", 2), ("data/frozen/atoms_v1.jsonl", 2), (".env", 2), (".claude/hooks/guard_bash.py", 2),
    ("src/vnsoc/extract/atomize.py", 0), ("manuscript/main.md", 0), ("docs/DECISIONS.md", 0),
])
def test_guard_files(proj, path, code):
    payload = {"tool_name": "Write", "tool_input": {"file_path": str(proj / path), "content": "x"}}
    assert run_hook(proj, "guard_files.py", payload)[0] == code


def test_guard_web(proj):
    assert run_hook(proj, "guard_web.py", {"tool_input": {"url": "https://thuvienphapluat.vn/x"}})[0] == 2
    assert run_hook(proj, "guard_web.py", {"tool_input": {"url": "https://kcb.vn/phac-do"}})[0] == 0


def test_user_prompt_ack(proj):
    state.init(paths(proj))
    code, out, _ = run_hook(proj, "user_prompt.py", {"prompt": "XONG HG0.2 — đã điền khóa", "session_id": "s"})
    assert code == 0 and (proj / "state" / ".human_ack" / "HG0.2").exists() and "HG0.2" in out
    run_hook(proj, "user_prompt.py", {"prompt": "làm tiếp T0.3 đi", "session_id": "s"})
    assert not (proj / "state" / ".human_ack" / "T0.3").exists()


def test_stop_hook(proj):
    P = paths(proj)
    state.init(P)
    payload = {"session_id": "abc", "stop_hook_active": False}
    assert run_hook(proj, "stop_continue.py", payload)[0] == 0          # autopilot off
    P.autopilot.write_text("on")
    code, _, err = run_hook(proj, "stop_continue.py", payload)
    assert code == 2 and "T0.1" in err
    codes = [run_hook(proj, "stop_continue.py", payload)[0] for _ in range(4)]
    assert 0 in codes                                                  # stall guard releases
    P.pause.write_text("x")
    assert run_hook(proj, "stop_continue.py", {"session_id": "new"})[0] == 0


def test_session_start_and_post_edit(proj):
    state.init(paths(proj))
    code, out, _ = run_hook(proj, "session_start.py", {"source": "startup"})
    assert code == 0 and "T0.1" in out
    bad = proj / "src" / "bad.py"
    bad.write_text("def f(:\n")
    assert run_hook(proj, "post_edit.py", {"tool_input": {"file_path": str(bad)}})[0] == 2
    bad.write_text("def f():\n    return 1\n")
    assert run_hook(proj, "post_edit.py", {"tool_input": {"file_path": str(bad)}})[0] == 0
