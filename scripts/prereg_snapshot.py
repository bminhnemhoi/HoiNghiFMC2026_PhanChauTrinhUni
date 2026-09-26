#!/usr/bin/env python3
"""Hash manifest of the registration package (prereg §1.3, §5.0, §6.8; rev-editor ids 1, 5, 9).

  PYTHONUTF8=1 .venv/bin/python scripts/prereg_snapshot.py            # write hashes into the registration + SHA256SUMS
  PYTHONUTF8=1 .venv/bin/python scripts/prereg_snapshot.py --pdf      # also render prereg/osf_preregistration.pdf
  PYTHONUTF8=1 .venv/bin/python scripts/prereg_snapshot.py --check    # exit 1 if any file changed since the snapshot

1. The SHA-256 of every analysis-package file is written into the block between the HASHES markers of
   prereg/osf_preregistration.md (Section 5.0), so the registered text quotes the exact code it registers.
2. prereg/analysis_plan/SHA256SUMS then lists those files AND the registration text itself (and the PDF with --pdf).
Run it (a) before any pilot output is opened, uploading the text + SHA256SUMS to the OSF project (pre-pilot
snapshot, human gate), and (b) again immediately before submission (HG2.9). If any listed file changes afterwards,
the change needs docs/DECISIONS.md + an addendum.
"""
from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREREG = ROOT / "prereg" / "osf_preregistration.md"
SUMS = ROOT / "prereg" / "analysis_plan" / "SHA256SUMS"
PDF = ROOT / "prereg" / "osf_preregistration.pdf"
BEGIN, END = "<!-- HASHES:BEGIN (scripts/prereg_snapshot.py; do not edit by hand) -->", "<!-- HASHES:END -->"
FILES = [
    "src/vnsoc/analysis/confirmatory.py", "src/vnsoc/ltt.py", "src/vnsoc/grade.py", "src/vnsoc/normalize_vi.py",
    "src/vnsoc/match/decoys.py", "src/vnsoc/match/atom_flags.py", "src/vnsoc/qgen/mcq.py", "src/vnsoc/qgen/qc.py",
    "src/vnsoc/extract/corpus_priority.py", "src/vnsoc/analysis/extractor_check.py", "src/vnsoc/schemas.py",
    "configs/project.yaml", "configs/conditions.yaml", "configs/grading.yaml", "configs/models.yaml",
    "tests/test_prereg_code.py", "tests/test_atom_flags.py", "tests/test_grade_review.py",
    "prereg/analysis_plan/simulate_operating_characteristics.py", "prereg/analysis_plan/operating_characteristics.json",
    "prereg/analysis_plan/README.md", "results/tables/corpus_triage.csv", "data/seed/seed_conflicts.yaml",
]


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def block(stamp: str) -> str:
    lines = [BEGIN, "", f"Snapshot {stamp}. SHA-256 of the registered analysis package (the text governs; these files "
             "implement it):", "", "| File | SHA-256 |", "| --- | --- |"]
    for f in FILES:
        p = ROOT / f
        lines.append(f"| `{f}` | `{sha(p) if p.exists() else 'missing'}` |")
    return "\n".join(lines + ["", END])


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    if a.check:
        bad = []
        for line in SUMS.read_text(encoding="utf-8").splitlines():
            if line.strip() and not line.startswith("#"):
                h, f = line.split(maxsplit=1)
                p = ROOT / f.strip()
                if not p.exists() or sha(p) != h:
                    bad.append(f.strip())
        print("\n".join(f"ĐỔI {b}" for b in bad) or "OK: gói đăng ký trùng ảnh chụp")
        return 1 if bad else 0
    stamp = datetime.now().astimezone().isoformat(timespec="seconds")
    txt = PREREG.read_text(encoding="utf-8")
    i, j = txt.find(BEGIN[:16]), txt.find(END)
    if i < 0 or j < i:
        print("thiếu dấu HASHES trong bản đăng ký")
        return 1
    PREREG.write_text(txt[:i] + block(stamp) + txt[j + len(END):], encoding="utf-8", newline="\n")
    listed = FILES + ["prereg/osf_preregistration.md"]
    if a.pdf:
        cmd = ["pandoc", str(PREREG), "-o", str(PDF), "--pdf-engine=xelatex", "-V", "mainfont=Cambria",
               "-V", "monofont=Consolas", "-V", "geometry:margin=2cm", "-V", "fontsize=10pt"]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            print("pandoc lỗi:", r.stderr[-2000:])
            return 1
        listed.append("prereg/osf_preregistration.pdf")
    rows = [f"# prereg snapshot {stamp}"] + [f"{sha(ROOT / f)}  {f}" for f in listed if (ROOT / f).exists()]
    SUMS.write_text("\n".join(rows) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote hashes into {PREREG.relative_to(ROOT)} and {SUMS.relative_to(ROOT)} ({len(rows) - 1} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
