"""Project paths. Stdlib only: hooks import this with the system python3."""
from __future__ import annotations

import os
from pathlib import Path
from types import SimpleNamespace


def project_root() -> Path:
    env = os.environ.get("VNSOC_ROOT") or os.environ.get("CLAUDE_PROJECT_DIR")
    if env:
        return Path(env).resolve()
    here = Path(__file__).resolve()
    for p in [here, *here.parents]:
        if (p / "pyproject.toml").exists() and (p / "src" / "vnsoc").exists():
            return p
    return Path.cwd().resolve()


def paths(root: Path | str | None = None) -> SimpleNamespace:
    r = Path(root).resolve() if root else project_root()
    s = r / "state"
    return SimpleNamespace(
        root=r,
        docs=r / "docs",
        plan=r / "docs" / "02_KE_HOACH_TRIEN_KHAI.md",
        state=s,
        progress=s / "progress.json",
        human_todo=s / "HUMAN_TODO.md",
        human_ack=s / ".human_ack",
        ledger=s / "budget_ledger.csv",
        pause=s / "PAUSE",
        autopilot=s / "AUTOPILOT_ON",
        log=r / "docs" / "LOG.md",
        decisions=r / "docs" / "DECISIONS.md",
        configs=r / "configs",
        results=r / "results",
        numbers=r / "results" / "numbers.json",
        manuscript=r / "manuscript",
    )


def python_bin(root: Path | str | None = None) -> str:
    r = paths(root).root
    venv = r / ".venv" / "bin" / "python"
    for cand in (venv, venv.with_suffix(".exe")):   # Windows venv: python.exe (.venv/bin is a junction to Scripts)
        if cand.exists():
            # Task checks expand $PY unquoted with cwd = project root; a root containing spaces would word-split.
            return ".venv/bin/python" if any(ch.isspace() for ch in str(r)) else str(cand)
    return "python3"
