"""Task state machine for the project. Single source of truth: the YAML task block in
docs/02_KE_HOACH_TRIEN_KHAI.md -> state/progress.json (written ONLY through this CLI).

Stdlib only at import time (hooks use the system python3). PyYAML is imported lazily by `init`.

Usage (from the repo root):
  scripts/vs init                 # build/merge state/progress.json from the plan
  scripts/vs next [--id-only]     # next eligible Claude task (exit 3 if none)
  scripts/vs start T1.1
  scripts/vs done T1.1 [--note ...]   # verifies outputs + runs the task's check command
  scripts/vs block T1.1 --reason "..."   # needs a human; written to HUMAN_TODO.md
  scripts/vs unblock T1.1
  scripts/vs skip T5.9 --reason "DR6 ..."  # only tasks marked skippable
  scripts/vs human-done HG0.3 --note "..."  # only after the user typed: XONG HG0.3
  scripts/vs add --id R2.1 --title ... --owner claude --depends T4.7 --acceptance ... [--check ...]
  scripts/vs show [ID] | list [--status S] [--owner O] | digest | todo
"""
from __future__ import annotations

import argparse
import datetime as dt
import glob
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from vnsoc.paths import paths, python_bin

STATUSES = ("pending", "in_progress", "done", "blocked", "skipped")
OWNERS = ("claude", "human")
REQUIRED = ("id", "title", "phase", "owner")
PLAN_FIELDS = ("id", "title", "phase", "owner", "week", "depends_on", "outputs", "acceptance",
               "check", "skill", "agent", "instructions", "not_before", "deadline", "skippable",
               "timeout_s", "gate")
TASK_BLOCK = re.compile(r"<!--\s*TASKS:BEGIN\s*-->\s*```ya?ml[^\n]*\n(.*?)```\s*<!--\s*TASKS:END\s*-->", re.S)


# ----------------------------------------------------------------------------------- utilities
def now() -> str:
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


def today() -> dt.date:
    t = os.environ.get("VNSOC_TODAY")
    return dt.date.fromisoformat(t) if t else dt.date.today()


def _date(x) -> dt.date | None:
    if x in (None, ""):
        return None
    if isinstance(x, dt.date):
        return x
    return dt.date.fromisoformat(str(x))


def _atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def append_log(P, line: str) -> None:
    P.log.parent.mkdir(parents=True, exist_ok=True)
    if not P.log.exists():
        P.log.write_text("# Nhật ký dự án (tự động + ghi tay)\n\n", encoding="utf-8")
    with P.log.open("a", encoding="utf-8") as f:
        f.write(f"- {now()} · {line}\n")


def append_decision(P, line: str) -> None:
    if not P.decisions.exists():
        P.decisions.write_text("# Quyết định (DR) đã áp dụng\n\n", encoding="utf-8")
    with P.decisions.open("a", encoding="utf-8") as f:
        f.write(f"- {now()} · {line}\n")


# ------------------------------------------------------------------------------------ plan I/O
def parse_plan(text: str) -> list[dict]:
    m = TASK_BLOCK.search(text)
    if not m:
        raise SystemExit("Không thấy khối <!-- TASKS:BEGIN --> ```yaml ... ``` <!-- TASKS:END --> trong kế hoạch")
    import yaml  # lazy

    data = yaml.safe_load(m.group(1))
    tasks = data["tasks"] if isinstance(data, dict) else data
    validate_plan(tasks)
    return tasks


def validate_plan(tasks: list[dict]) -> None:
    ids, errors = set(), []
    for t in tasks:
        for k in REQUIRED:
            if k not in t:
                errors.append(f"{t.get('id', '?')}: thiếu trường {k}")
        if t.get("id") in ids:
            errors.append(f"trùng id {t.get('id')}")
        ids.add(t.get("id"))
        if t.get("owner") not in OWNERS:
            errors.append(f"{t.get('id')}: owner phải là claude|human")
        if t.get("owner") in OWNERS and (t.get("owner") == "human") != str(t.get("id", "")).startswith("HG"):
            errors.append(f"{t.get('id')}: việc của người phải có mã HG…, việc của Claude thì không")
        if t.get("owner") == "human" and not t.get("instructions"):
            errors.append(f"{t.get('id')}: việc của người cần 'instructions'")
        unknown = set(t) - set(PLAN_FIELDS)
        if unknown:
            errors.append(f"{t.get('id')}: trường lạ {sorted(unknown)}")
    for t in tasks:
        for d in t.get("depends_on") or []:
            if d not in ids:
                errors.append(f"{t['id']}: phụ thuộc không tồn tại {d}")
    # cycle check (Kahn)
    indeg = {t["id"]: len(t.get("depends_on") or []) for t in tasks}
    children: dict[str, list[str]] = {}
    for t in tasks:
        for d in t.get("depends_on") or []:
            children.setdefault(d, []).append(t["id"])
    queue = [i for i, n in indeg.items() if n == 0]
    seen = 0
    while queue:
        i = queue.pop()
        seen += 1
        for c in children.get(i, []):
            indeg[c] -= 1
            if indeg[c] == 0:
                queue.append(c)
    if seen != len(tasks):
        errors.append("đồ thị phụ thuộc có chu trình")
    if errors:
        raise SystemExit("Kế hoạch không hợp lệ:\n  " + "\n  ".join(errors))


def load(P) -> dict:
    if not P.progress.exists():
        raise SystemExit("Chưa có state/progress.json — chạy: scripts/vs init")
    return json.loads(P.progress.read_text(encoding="utf-8"))


def save(P, st: dict) -> None:
    st["updated"] = now()
    _atomic_write(P.progress, json.dumps(st, ensure_ascii=False, indent=1))
    render_human_todo(P, st)


def fingerprint(P) -> str:
    try:
        return hashlib.sha256(P.progress.read_bytes()).hexdigest()[:16]
    except FileNotFoundError:
        return "none"


# ------------------------------------------------------------------------------------ queries
def all_deps(t: dict) -> list[str]:
    return list(t.get("depends_on") or []) + list(t.get("extra_depends") or [])


def deps_met(st: dict, t: dict) -> bool:
    return all(st["tasks"][d]["status"] in ("done", "skipped") for d in all_deps(t) if d in st["tasks"])


def eligible_claude(st: dict) -> list[dict]:
    out = []
    for i in st["order"]:
        t = st["tasks"][i]
        if t["owner"] != "claude" or t["status"] not in ("pending", "in_progress"):
            continue
        if not deps_met(st, t):
            continue
        nb = _date(t.get("not_before"))
        if nb and nb > today():
            continue
        out.append(t)
    out.sort(key=lambda t: (t["status"] != "in_progress", st["order"].index(t["id"])))
    return out


def waiting_human(st: dict) -> list[dict]:
    out = []
    for i in st["order"]:
        t = st["tasks"][i]
        if t["owner"] != "human" or t["status"] not in ("pending", "in_progress") or not deps_met(st, t):
            continue
        nb = _date(t.get("not_before"))
        if nb and nb > today():
            continue
        out.append(t)
    return out


def blocked(st: dict) -> list[dict]:
    return [st["tasks"][i] for i in st["order"] if st["tasks"][i]["status"] == "blocked"]


def current_phase(st: dict) -> str:
    for i in st["order"]:
        if st["tasks"][i]["status"] not in ("done", "skipped"):
            return str(st["tasks"][i].get("phase"))
    return "HOÀN TẤT"


# ------------------------------------------------------------------------------------ commands
def init(P, force: bool = False) -> dict:
    tasks = parse_plan(P.plan.read_text(encoding="utf-8"))
    old = None
    if P.progress.exists() and not force:
        old = json.loads(P.progress.read_text(encoding="utf-8"))
    st = {"plan_sha256": hashlib.sha256(P.plan.read_bytes()).hexdigest(), "created": now(),
          "updated": now(), "order": [], "tasks": {}}
    for t in tasks:
        rec = {k: t.get(k) for k in PLAN_FIELDS}
        for k in ("not_before", "deadline"):
            if isinstance(rec.get(k), dt.date):
                rec[k] = rec[k].isoformat()
        rec["depends_on"] = list(t.get("depends_on") or [])
        rec["outputs"] = list(t.get("outputs") or [])
        rec.update(status="pending", history=[], note="", source="plan", extra_depends=[])
        if old and t["id"] in old["tasks"]:
            o = old["tasks"][t["id"]]
            rec.update(status=o["status"], history=o.get("history", []), note=o.get("note", ""),
                       extra_depends=o.get("extra_depends", []))
        st["order"].append(t["id"])
        st["tasks"][t["id"]] = rec
    if old:
        st["created"] = old.get("created", st["created"])
        for i in old["order"]:
            o = old["tasks"][i]
            if i not in st["tasks"] and o.get("source") == "dynamic":
                st["order"].append(i)
                st["tasks"][i] = o
            elif i not in st["tasks"]:
                print(f"CẢNH BÁO: task {i} không còn trong kế hoạch; bỏ khỏi state", file=sys.stderr)
    P.human_ack.mkdir(parents=True, exist_ok=True)
    save(P, st)
    return st


def _get(st: dict, tid: str) -> dict:
    if tid not in st["tasks"]:
        raise SystemExit(f"Không có task {tid}")
    return st["tasks"][tid]


def _event(t: dict, event: str, note: str = "") -> None:
    t["history"].append({"t": now(), "event": event, "note": note})


def start(P, tid: str) -> None:
    st = load(P)
    t = _get(st, tid)
    if t["owner"] != "claude":
        raise SystemExit(f"{tid} là việc của người (human gate), không start được")
    if not deps_met(st, t):
        raise SystemExit(f"{tid} chưa đủ điều kiện: phụ thuộc {all_deps(t)} chưa xong")
    if t["status"] in ("done", "skipped"):
        raise SystemExit(f"{tid} đã {t['status']}")
    t["status"] = "in_progress"
    _event(t, "start")
    save(P, st)
    append_log(P, f"{tid} bắt đầu · {t['title']}")


def check_outputs(P, t: dict) -> list[str]:
    missing = []
    for pat in t.get("outputs") or []:
        hits = [h for h in glob.glob(str(P.root / pat), recursive=True)
                if Path(h).is_dir() or Path(h).stat().st_size > 0]
        if not hits:
            missing.append(pat)
    return missing


def _bash() -> str:
    """bash for task checks. On Windows a bare "bash" resolves to System32\\bash.exe (the WSL launcher) before PATH,
    so use VNSOC_BASH if set, else the first bash.exe on PATH outside System32/WindowsApps (Git Bash)."""
    if os.environ.get("VNSOC_BASH"):
        return os.environ["VNSOC_BASH"]
    if os.name != "nt":
        return "bash"
    for d in os.environ.get("PATH", "").split(os.pathsep):
        cand = Path(d) / "bash.exe"
        low = str(cand).lower()
        if cand.is_file() and "system32" not in low and "windowsapps" not in low:
            return str(cand)
    for cand in (r"C:\Program Files\Git\bin\bash.exe", r"C:\Program Files\Git\usr\bin\bash.exe"):
        if Path(cand).is_file():
            return cand
    return "bash"


def run_check(P, t: dict) -> tuple[int, str]:
    cmd = t.get("check")
    if not cmd:
        return 0, "(không có lệnh kiểm tra)"
    env = dict(os.environ, PY=python_bin(P.root), VNSOC_ROOT=str(P.root),
               PYTHONPATH=str(P.root / "src") + os.pathsep + os.environ.get("PYTHONPATH", ""))
    try:
        r = subprocess.run([_bash(), "-c", cmd], cwd=P.root, env=env, capture_output=True, text=True,
                           timeout=int(t.get("timeout_s") or 1800))
    except subprocess.TimeoutExpired:
        return 124, f"quá thời gian: {cmd}"
    return r.returncode, (r.stdout[-3000:] + "\n" + r.stderr[-3000:]).strip()


def done(P, tid: str, note: str = "") -> int:
    st = load(P)
    t = _get(st, tid)
    if t["owner"] != "claude":
        raise SystemExit(f"{tid} là việc của người: dùng human-done sau khi người dùng gõ 'XONG {tid}'")
    if not deps_met(st, t):
        raise SystemExit(f"{tid}: phụ thuộc chưa xong")
    missing = check_outputs(P, t)
    if missing:
        print(f"CHƯA XONG {tid}: thiếu sản phẩm {missing}", file=sys.stderr)
        return 1
    code, out = run_check(P, t)
    if code != 0:
        print(f"CHƯA XONG {tid}: lệnh kiểm tra thất bại (mã {code})\n$ {t.get('check')}\n{out}", file=sys.stderr)
        return 1
    t["status"] = "done"
    _event(t, "done", note)
    save(P, st)
    append_log(P, f"{tid} XONG · {t['title']}" + (f" · {note}" if note else ""))
    print(f"OK {tid} xong. {out[-500:] if out else ''}")
    return 0


def block(P, tid: str, reason: str) -> None:
    st = load(P)
    t = _get(st, tid)
    t["status"] = "blocked"
    t["note"] = reason
    _event(t, "block", reason)
    save(P, st)
    append_log(P, f"{tid} BỊ CHẶN · {reason}")


def unblock(P, tid: str) -> None:
    st = load(P)
    t = _get(st, tid)
    if t["status"] != "blocked":
        raise SystemExit(f"{tid} không ở trạng thái blocked")
    t["status"] = "pending"
    _event(t, "unblock")
    save(P, st)
    append_log(P, f"{tid} gỡ chặn")


def skip(P, tid: str, reason: str) -> None:
    st = load(P)
    t = _get(st, tid)
    if not t.get("skippable"):
        raise SystemExit(f"{tid} không được phép bỏ qua (không có skippable: true). Hỏi người dùng.")
    if t["owner"] == "human" and not any(st["tasks"][d]["status"] == "skipped" for d in all_deps(t)):
        raise SystemExit(f"{tid} là việc của người dùng: chỉ bỏ qua được khi việc đầu vào của nó đã bị bỏ qua")
    t["status"] = "skipped"
    _event(t, "skip", reason)
    save(P, st)
    append_decision(P, f"Bỏ qua {tid} ({t['title']}): {reason}")
    append_log(P, f"{tid} bỏ qua · {reason}")


def waive(P, tid: str, by: str, reason: str) -> None:
    """Mark a task no longer needed because of a USER decision (e.g. 'solo, laptop only, no API keys'): the user's
    own acknowledgement state/.human_ack/<by> (written only by the hook when the USER types 'XONG <by> ...') is the
    authority; Claude cannot create it. The task becomes 'skipped' (dependants may proceed) and the decision is
    logged with the user's words. Unlike `skip`, it applies to any task, because the user has re-planned."""
    st = load(P)
    t = _get(st, tid)
    ack = P.human_ack / by
    if not ack.exists():
        raise SystemExit(f"TỪ CHỐI: chưa có xác nhận của người dùng '{by}'. Người dùng phải tự gõ trong chat: XONG {by} ...")
    if t["status"] in ("done", "skipped"):
        raise SystemExit(f"{tid} đã {t['status']}")
    words = ack.read_text(encoding="utf-8").strip()[:300]
    t["status"] = "skipped"
    _event(t, "waive", f"theo quyết định người dùng ({by}: «{words}») — {reason}")
    save(P, st)
    append_decision(P, f"Bỏ {tid} ({t['title']}) theo quyết định của người dùng ({by}: «{words}»): {reason}")
    append_log(P, f"{tid} bỏ theo quyết định người dùng ({by}) · {reason}")


def human_done(P, tid: str, note: str = "") -> int:
    st = load(P)
    t = _get(st, tid)
    if t["owner"] != "human":
        raise SystemExit(f"{tid} là việc của Claude: dùng done")
    ack = P.human_ack / tid
    if not ack.exists():
        print(f"TỪ CHỐI: chưa có xác nhận của người dùng cho {tid}. Người dùng phải tự gõ trong chat: XONG {tid}",
              file=sys.stderr)
        return 2
    missing = check_outputs(P, t)
    if missing:
        print(f"{tid}: thiếu bằng chứng {missing} (ghi lại thông tin người dùng cung cấp vào đó)", file=sys.stderr)
        return 1
    code, out = run_check(P, t)
    if code != 0:
        print(f"{tid}: lệnh kiểm tra thất bại\n{out}", file=sys.stderr)
        return 1
    t["status"] = "done"
    _event(t, "human_done", note or ack.read_text(encoding="utf-8")[:300])
    save(P, st)
    append_log(P, f"{tid} (người dùng) XONG · {note}")
    print(f"OK {tid} ghi nhận là xong")
    return 0


def add(P, tid: str, title: str, owner: str, phase: str, depends: list[str], acceptance: str,
        outputs: list[str], check: str | None, instructions: str | None, blocks: list[str] | None = None) -> None:
    """Add a dynamic task. `blocks`: existing tasks that must now also wait for this one."""
    st = load(P)
    for b in blocks or []:
        if _get(st, b)["status"] in ("done", "skipped"):
            raise SystemExit(f"{b} đã xong, không thể chặn thêm")
    if tid in st["tasks"]:
        raise SystemExit(f"Đã có {tid}")
    for d in depends:
        _get(st, d)
    if set(depends) & set(blocks or []):
        raise SystemExit("task mới không thể vừa phụ thuộc vừa chặn cùng một task")
    if owner == "human" and not instructions:
        raise SystemExit("Việc của người cần --instructions")
    if (owner == "human") != tid.startswith("HG"):
        raise SystemExit("Quy ước: việc của người có mã bắt đầu bằng HG; việc của Claude thì không")
    rec = {k: None for k in PLAN_FIELDS}
    rec.update(id=tid, title=title, owner=owner, phase=phase, depends_on=depends, acceptance=acceptance,
               outputs=outputs, check=check, instructions=instructions, status="pending", history=[],
               note="", source="dynamic")
    rec["extra_depends"] = []
    _event(rec, "add")
    st["order"].append(tid)
    st["tasks"][tid] = rec
    for b in blocks or []:
        st["tasks"][b].setdefault("extra_depends", []).append(tid)
        _event(st["tasks"][b], "wait_for", tid)
    save(P, st)
    append_log(P, f"thêm task {tid} · {title}")


# ------------------------------------------------------------------------------------ reports
def budget_line(P) -> str:
    try:
        from vnsoc.budget import status_line
        return status_line(P.root)
    except Exception as e:  # pragma: no cover - never break hooks
        return f"ngân sách: không đọc được ({e.__class__.__name__})"


def digest(P, n_log: int = 6) -> str:
    st = load(P)
    counts = {s: 0 for s in STATUSES}
    for t in st["tasks"].values():
        counts[t["status"]] += 1
    el = eligible_claude(st)
    wh = waiting_human(st)
    bl = blocked(st)
    lines = [f"[vn-soc-audit] Giai đoạn: {current_phase(st)} · xong {counts['done']}/{len(st['tasks'])}"
             f" · đang làm {counts['in_progress']} · chặn {counts['blocked']} · bỏ qua {counts['skipped']}",
             budget_line(P)]
    if P.pause.exists():
        lines.append("TẠM DỪNG: có state/PAUSE — không tự chạy tiếp; chờ người dùng /resume")
    if el:
        lines.append("Việc Claude làm tiếp: " + "; ".join(f"{t['id']} {t['title']}" for t in el[:3]))
    else:
        lines.append("Không còn việc Claude làm được ngay (chờ người dùng hoặc chờ ngày).")
    if wh:
        lines.append("ĐANG CHỜ NGƯỜI DÙNG: " + "; ".join(
            f"{t['id']} {t['title']}" + (f" (hạn {t['deadline']})" if t.get("deadline") else "") for t in wh))
    if bl:
        lines.append("BỊ CHẶN: " + "; ".join(f"{t['id']}: {t.get('note', '')[:80]}" for t in bl))
    if P.log.exists():
        tail = [ln for ln in P.log.read_text(encoding="utf-8").splitlines() if ln.startswith("- ")][-n_log:]
        if tail:
            lines.append("Nhật ký gần nhất:\n  " + "\n  ".join(tail))
    return "\n".join(lines)


def render_human_todo(P, st: dict) -> None:
    wh, bl = waiting_human(st), blocked(st)
    out = ["# Việc cần BẠN làm (tự sinh — đừng sửa tay)", "",
           f"Cập nhật: {now()}. Làm xong việc nào thì gửi trong Claude Code một tin nhắn có dòng BẮT ĐẦU bằng "
           "`XONG <mã>` (ví dụ `XONG HG0.3 Llama: đang chờ`) kèm thông tin được yêu cầu.", ""]
    if not wh and not bl:
        out.append("Hiện không có việc nào chờ bạn.")
    for t in wh:
        out += [f"## {t['id']} — {t['title']}" + (f" (HẠN {t['deadline']})" if t.get("deadline") else ""), "",
                str(t.get("instructions") or "").strip(), ""]
        if t.get("acceptance"):
            out += [f"Xong khi: {t['acceptance']}", ""]
    if bl:
        out += ["## Việc Claude bị chặn, cần bạn gỡ", ""]
        out += [f"- **{t['id']}** {t['title']}: {t.get('note', '')}" for t in bl]
    _atomic_write(P.human_todo, "\n".join(out) + "\n")


def show(P, tid: str | None) -> str:
    st = load(P)
    if tid:
        return json.dumps(_get(st, tid), ensure_ascii=False, indent=1)
    return "\n".join(f"{i:8s} {st['tasks'][i]['status']:11s} {st['tasks'][i]['owner']:6s} {st['tasks'][i]['title']}"
                     for i in st["order"])


# ------------------------------------------------------------------------------------ CLI
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="vs", description="Trạng thái công việc vn-soc-audit")
    ap.add_argument("--root", default=None)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("init"); s.add_argument("--force", action="store_true")
    s = sub.add_parser("next"); s.add_argument("--id-only", action="store_true")
    for name in ("start", "unblock"):
        s = sub.add_parser(name); s.add_argument("id")
    s = sub.add_parser("done"); s.add_argument("id"); s.add_argument("--note", default="")
    s = sub.add_parser("block"); s.add_argument("id"); s.add_argument("--reason", required=True)
    s = sub.add_parser("skip"); s.add_argument("id"); s.add_argument("--reason", required=True)
    s = sub.add_parser("human-done"); s.add_argument("id"); s.add_argument("--note", default="")
    s = sub.add_parser("waive"); s.add_argument("id"); s.add_argument("--by", required=True)
    s.add_argument("--reason", required=True)
    s = sub.add_parser("add")
    s.add_argument("--id", required=True); s.add_argument("--title", required=True)
    s.add_argument("--owner", default="claude", choices=OWNERS); s.add_argument("--phase", default="dynamic")
    s.add_argument("--depends", nargs="*", default=[]); s.add_argument("--acceptance", default="")
    s.add_argument("--outputs", nargs="*", default=[]); s.add_argument("--check", default=None)
    s.add_argument("--instructions", default=None)
    s.add_argument("--blocks", nargs="*", default=[], help="task hiện có phải chờ task mới này")
    s = sub.add_parser("show"); s.add_argument("id", nargs="?")
    s = sub.add_parser("list"); s.add_argument("--status"); s.add_argument("--owner")
    sub.add_parser("digest"); sub.add_parser("todo"); sub.add_parser("validate-plan")
    sub.add_parser("pause"); sub.add_parser("resume")
    s = sub.add_parser("autopilot"); s.add_argument("mode", choices=["on", "off"])
    a = ap.parse_args(argv)
    P = paths(a.root)
    if a.cmd == "init":
        st = init(P, a.force)
        print(f"OK: {len(st['tasks'])} task. " + digest(P).splitlines()[0])
    elif a.cmd == "validate-plan":
        tasks = parse_plan(P.plan.read_text(encoding="utf-8"))
        print(f"OK: kế hoạch hợp lệ, {len(tasks)} task")
    elif a.cmd == "next":
        el = eligible_claude(load(P))
        if not el:
            print("NONE")
            return 3
        print(el[0]["id"] if a.id_only else json.dumps(el[0], ensure_ascii=False, indent=1))
    elif a.cmd == "start":
        start(P, a.id)
    elif a.cmd == "done":
        return done(P, a.id, a.note)
    elif a.cmd == "block":
        block(P, a.id, a.reason)
    elif a.cmd == "unblock":
        unblock(P, a.id)
    elif a.cmd == "skip":
        skip(P, a.id, a.reason)
    elif a.cmd == "human-done":
        return human_done(P, a.id, a.note)
    elif a.cmd == "waive":
        waive(P, a.id, a.by, a.reason)
    elif a.cmd == "add":
        add(P, a.id, a.title, a.owner, a.phase, a.depends, a.acceptance, a.outputs, a.check, a.instructions,
            a.blocks)
    elif a.cmd == "show":
        print(show(P, a.id))
    elif a.cmd == "list":
        st = load(P)
        for i in st["order"]:
            t = st["tasks"][i]
            if (not a.status or t["status"] == a.status) and (not a.owner or t["owner"] == a.owner):
                print(f"{i:8s} {t['status']:11s} {t['owner']:6s} {t['title']}")
    elif a.cmd == "digest":
        print(digest(P))
    elif a.cmd == "pause":
        P.pause.parent.mkdir(parents=True, exist_ok=True)
        P.pause.write_text(now() + "\n", encoding="utf-8")
        append_log(P, "TẠM DỪNG (state/PAUSE)")
        print("Đã tạm dừng. Dùng /resume để chạy tiếp.")
    elif a.cmd == "resume":
        P.pause.unlink(missing_ok=True)
        append_log(P, "CHẠY TIẾP (bỏ state/PAUSE)")
        print("Đã bỏ tạm dừng.")
    elif a.cmd == "autopilot":
        if a.mode == "on":
            P.autopilot.write_text(now() + "\n", encoding="utf-8")
        else:
            P.autopilot.unlink(missing_ok=True)
        append_log(P, f"autopilot {a.mode}")
        print(f"autopilot {a.mode}")
    elif a.cmd == "todo":
        render_human_todo(P, load(P))
        print(P.human_todo.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
