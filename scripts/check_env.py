#!/usr/bin/env python3
"""Environment check. Prints what is present/missing WITHOUT printing any secret values.
Writes state/env_report.json. Exit 0 if everything needed for the CURRENT phase exists, else 1.
  python3 scripts/check_env.py [--need core|kaggle|api|r|ocr|all]
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NEEDS = {
    "core": ["python>=3.10", "venv", "pkg:yaml", "pkg:pydantic", "pkg:numpy", "pkg:scipy", "pkg:pandas",
             "pkg:pytest", "git"],
    "pdf": ["pkg:fitz", "pkg:pdfplumber", "bin:pdftotext"],
    "ocr": ["bin:tesseract", "tesseract:vie"],
    "kaggle": ["bin:kaggle", "kaggle_creds"],
    "api": ["env:OPENAI_API_KEY|GEMINI_API_KEY|GOOGLE_API_KEY", "pkg:openai|google.genai"],
    "r": ["bin:Rscript", "r:lme4", "r:glmmTMB", "r:sandwich", "r:boot"],
    "hf": ["env:HF_TOKEN"],
    "pubs": ["env:OSF_TOKEN", "env:ZENODO_TOKEN"],
}


def dotenv_keys() -> set[str]:
    f = ROOT / ".env"
    keys = set(k for k, v in os.environ.items() if v)
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.split("=", 1)
                if v.strip().strip('"').strip("'"):
                    keys.add(k.strip())
    return keys


def venv_bin(name: str) -> Path:
    """.venv/bin/<name>, or <name>.exe on Windows (where .venv/bin is a junction to .venv/Scripts)."""
    p = ROOT / ".venv" / "bin" / name
    return p if p.exists() or not p.with_suffix(".exe").exists() else p.with_suffix(".exe")


def check(item: str, keys: set[str]) -> bool:
    kind, _, what = item.partition(":")
    py = venv_bin("python")
    if item == "python>=3.10":
        return sys.version_info >= (3, 10)
    if item == "venv":
        return py.exists()
    if item == "git":
        return shutil.which("git") is not None
    if item == "kaggle_creds":
        return bool({"KAGGLE_API_TOKEN", "KAGGLE_KEY"} & keys) or (Path.home() / ".kaggle" / "kaggle.json").exists()
    if kind == "pkg":
        pyexe = str(py) if py.exists() else sys.executable
        for mod in what.split("|"):
            r = subprocess.run([pyexe, "-c", f"import importlib.util,sys; sys.exit(0 if importlib.util.find_spec('{mod}') else 1)"],
                               capture_output=True)
            if r.returncode == 0:
                return True
        return False
    if kind == "bin":
        return shutil.which(what) is not None or venv_bin(what).exists()
    if kind == "env":
        return any(k in keys for k in what.split("|"))
    if kind == "tesseract":
        if not shutil.which("tesseract"):
            return False
        r = subprocess.run(["tesseract", "--list-langs"], capture_output=True, text=True)
        return what in r.stdout.split()
    if kind == "r":
        if not shutil.which("Rscript"):
            return False
        r = subprocess.run(["Rscript", "-e", f"quit(status=ifelse(requireNamespace('{what}', quietly=TRUE),0,1))"],
                           capture_output=True)
        return r.returncode == 0
    return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--need", default="core", help="core|pdf|ocr|kaggle|api|r|hf|pubs|all (comma list)")
    a = ap.parse_args()
    groups = list(NEEDS) if a.need == "all" else a.need.split(",")
    keys = dotenv_keys()
    report, ok = {}, True
    for g in groups:
        for item in NEEDS[g]:
            good = check(item, keys)
            report[f"{g}/{item}"] = good
            ok &= good
            print(f"{'OK ' if good else 'THIẾU'}  {g:7s} {item}")
    (ROOT / "state").mkdir(exist_ok=True)
    (ROOT / "state" / "env_report.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
