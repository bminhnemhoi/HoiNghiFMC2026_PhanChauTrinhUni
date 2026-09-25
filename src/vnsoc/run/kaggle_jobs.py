"""Render / push / poll / download Kaggle GPU jobs (2×T4, one vLLM process per GPU).

Requests travel as a PRIVATE Kaggle dataset (<user>/vnsoc-requests) containing JSONL files with
{"request_id", "model_key", "messages": [...], "sampling": {...}}. Each job = one kernel version
that processes <= ~10 h of work (Kaggle sessions stop at 12 h). Outputs are appended per batch,
so a stopped job can be resumed by a new job whose shard lists the same `out` file.

  $PY -m vnsoc.run.kaggle_jobs render --job-id a1-qwen-llama --spec kaggle/specs/a1.json
  $PY -m vnsoc.run.kaggle_jobs push   --job-id a1-qwen-llama
  $PY -m vnsoc.run.kaggle_jobs status --job-id a1-qwen-llama
  $PY -m vnsoc.run.kaggle_jobs fetch  --job-id a1-qwen-llama      # -> data/runs/kaggle/<job-id>/
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from vnsoc.paths import paths


def username() -> str:
    u = os.environ.get("KAGGLE_USERNAME")
    if not u:
        f = Path.home() / ".kaggle" / "kaggle.json"
        if f.exists():
            u = json.loads(f.read_text()).get("username")
    if not u:
        raise SystemExit("Thiếu KAGGLE_USERNAME (điền trong .env ở HG0.3)")
    return u


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9-]+", "-", s.lower()).strip("-")[:44]


def render(job_id: str, spec: dict, root=None) -> Path:
    """spec: {"shards": [...], "pip": ["vllm==X"], "dataset": "<user>/vnsoc-requests"}"""
    P = paths(root)
    d = P.root / "kaggle" / "jobs" / slug(job_id)
    d.mkdir(parents=True, exist_ok=True)
    job = {"job_id": slug(job_id), "shards": spec["shards"], "pip": spec.get("pip", [])}
    js = json.dumps(job, ensure_ascii=False)
    if "'''" in js:
        raise ValueError("spec không được chứa '''")
    tpl = (P.root / "kaggle" / "runner_template.py").read_text(encoding="utf-8")
    (d / "run.py").write_text(tpl.replace("__JOB__", js), encoding="utf-8")
    user = spec.get("user") or username()
    name = slug(job_id) if slug(job_id).startswith("vnsoc-") else f"vnsoc-{slug(job_id)}"
    meta = {
        "id": f"{user}/{name}", "title": name, "code_file": "run.py",
        "language": "python", "kernel_type": "script", "is_private": True, "enable_gpu": True,
        "enable_internet": True, "machine_shape": "NvidiaTeslaT4",
        "dataset_sources": [spec.get("dataset", f"{user}/vnsoc-requests")],
        "kernel_sources": spec.get("kernel_sources", []), "model_sources": spec.get("model_sources", []),
        "competition_sources": [],
    }
    (d / "kernel-metadata.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")
    return d


def _kaggle_bin() -> str:
    venv = Path(sys.executable).parent / "kaggle"
    return str(venv) if venv.exists() else "kaggle"


def _kaggle(*args: str) -> str:
    r = subprocess.run([_kaggle_bin(), *args], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f"kaggle {' '.join(args)} lỗi:\n{r.stdout}\n{r.stderr}")
    return r.stdout


def push(job_id: str) -> None:
    d = paths().root / "kaggle" / "jobs" / slug(job_id)
    print(_kaggle("kernels", "push", "-p", str(d), "--accelerator", "NvidiaTeslaT4"))


def status(job_id: str) -> str:
    meta = json.loads((paths().root / "kaggle" / "jobs" / slug(job_id) / "kernel-metadata.json").read_text())
    out = _kaggle("kernels", "status", meta["id"])
    print(out.strip())
    return out


def fetch(job_id: str) -> Path:
    meta = json.loads((paths().root / "kaggle" / "jobs" / slug(job_id) / "kernel-metadata.json").read_text())
    dest = paths().root / "data" / "runs" / "kaggle" / slug(job_id)
    dest.mkdir(parents=True, exist_ok=True)
    print(_kaggle("kernels", "output", meta["id"], "-p", str(dest)))
    return dest


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="kaggle_jobs")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("render"); s.add_argument("--job-id", required=True); s.add_argument("--spec", required=True)
    for c in ("push", "status", "fetch"):
        s = sub.add_parser(c); s.add_argument("--job-id", required=True)
    a = ap.parse_args(argv)
    if a.cmd == "render":
        print(render(a.job_id, json.loads(Path(a.spec).read_text(encoding="utf-8"))))
    elif a.cmd == "push":
        push(a.job_id)
    elif a.cmd == "status":
        status(a.job_id)
    elif a.cmd == "fetch":
        print(fetch(a.job_id))
    return 0


if __name__ == "__main__":
    sys.exit(main())
