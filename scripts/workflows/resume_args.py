"""Work left for the two agent workflows of P2–P3, computed from what is on disk (so a new session can continue where
the last one stopped; Workflow resumeFromRunId only works inside the session that started a run).

  $PY scripts/workflows/resume_args.py          # summary + logs/wf/extract_args.json, logs/wf/foreign_args.json

Main-study extraction (scripts/workflows/main_atom_extraction.js, plan = scripts/workflows/extract_plan.json):
  a chunk is DONE when data/interim/atoms_parts/<part>.jsonl and <part>_coverage.md exist and the coverage table
  reaches the chunk's last page; otherwise it goes to `todo`. Calibrated documents (repair: true in the plan) were
  re-extracted under protocol 1.1 on 27/9 and are only audited. A document is AUDITED when
  review/extraction_audit/<doc>.json exists; every non-audited document is passed to the workflow (extract its todo
  chunks, then audit, then repair if the audit asks for it).
Foreign store (scripts/workflows/foreign_store.js, groups = scripts/workflows/foreign_groups.json):
  a group is COLLECTED when data/interim/foreign_parts/<id>.jsonl exists, VERIFIED when review/foreign_audit/<id>.json
  exists; every non-verified group is passed (collect only if not collected).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PARTS = ROOT / "data" / "interim" / "atoms_parts"


def part_name(d: dict, c: list[int]) -> str:
    base = d["key"].replace("/", "_")
    return base if len(d["chunks"]) == 1 else f"{base}__p{c[0]:03d}-{c[1]:03d}"


def coverage_last_page(md: Path, first: int = 0, last: int = 10**6) -> int:
    """Highest PDF page of the chunk named in the coverage file: leading page number(s) of a table row ("| 67 (60) |",
    "| 4–10 (3–9) |", "| tr. 12 |"); a "Trang đã đọc (n/n)" line counts as the whole chunk read."""
    text = md.read_text(encoding="utf-8")
    for a_, b_ in re.findall(r"[Đđ]ã đọc\D{0,3}\((\d+)/(\d+)\)", text):
        if a_ == b_:
            return last
    top = 0
    for line in text.splitlines():
        m = re.match(r"\|\s*\**\s*(?:[Tt]r(?:ang)?\.?\s*)?(\d+)(?:\s*[–-]\s*(\d+))?", line)
        if m:
            nums = [int(x) for x in m.groups() if x]
            nums = [n for n in nums if first <= n <= last]
            if nums:
                top = max(top, max(nums))
    return top


def chunk_done(d: dict, c: list[int]) -> bool:
    name = part_name(d, c)
    js, cov = PARTS / f"{name}.jsonl", PARTS / f"{name}_coverage.md"
    return js.exists() and cov.exists() and coverage_last_page(cov, c[0], c[1]) >= c[1]


def extract_args() -> tuple[list[dict], list[str]]:
    plan = json.loads((ROOT / "scripts" / "workflows" / "extract_plan.json").read_text(encoding="utf-8"))
    out, notes = [], []
    for d in plan:
        doc = d["key"].replace("/", "_")
        audited = (ROOT / "review" / "extraction_audit" / f"{doc}.json").exists()
        if d.get("repair"):                     # calibrated documents: re-extracted on 27/9, audit only
            todo = [] if (PARTS / f"{doc}.jsonl").exists() else d["chunks"]
        else:
            todo = [c for c in d["chunks"] if not chunk_done(d, c)]
        notes.append(f"{d['key']:10s} {d['pages']:4d} tr  phần xong {len(d['chunks']) - len(todo)}/{len(d['chunks'])}"
                     f"  kiểm toán {'có' if audited else 'CHƯA'}")
        if todo or not audited:
            out.append({"key": d["key"], "pages": d["pages"], "topic": d["topic"], "chunks": d["chunks"],
                        "todo": todo, "repair": False})
    return out, notes


def foreign_args() -> tuple[list[dict], list[str]]:
    groups = json.loads((ROOT / "scripts" / "workflows" / "foreign_groups.json").read_text(encoding="utf-8"))
    out, notes = [], []
    for g in groups:
        collected = (ROOT / "data" / "interim" / "foreign_parts" / f"{g['id']}.jsonl").exists()
        verified = (ROOT / "review" / "foreign_audit" / f"{g['id']}.json").exists()
        notes.append(f"{g['id']:18s} thu thập {'có' if collected else 'CHƯA'}  kiểm {'có' if verified else 'CHƯA'}")
        if not verified:
            out.append(dict(g, collected=collected))
    return out, notes


def main() -> int:
    wf = ROOT / "logs" / "wf"
    wf.mkdir(parents=True, exist_ok=True)
    ex, n1 = extract_args()
    fo, n2 = foreign_args()
    (wf / "extract_args.json").write_text(json.dumps(ex, ensure_ascii=False), encoding="utf-8")
    (wf / "foreign_args.json").write_text(json.dumps(fo, ensure_ascii=False), encoding="utf-8")
    print("TRÍCH MẨU\n  " + "\n  ".join(n1))
    print(f"  -> {len(ex)} văn bản đưa vào workflow, {sum(len(d['todo']) for d in ex)} phần cần trích; "
          f"{wf / 'extract_args.json'}")
    print("KHO NƯỚC NGOÀI\n  " + "\n  ".join(n2))
    print(f"  -> {len(fo)} nhóm đưa vào workflow ({sum(not g['collected'] for g in fo)} cần thu thập); "
          f"{wf / 'foreign_args.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
