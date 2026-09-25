"""Aggregate the agent review panel for a milestone.

  $PY -m vnsoc.review M2            # reads review/M2/rev-*.md -> review/M2/summary.md (+ exit 0 PASS / 1 REVISE)

Each reviewer file starts with a ```yaml block (see .claude/agents/rev-*.md). Decision rule
(fixed in advance): PASS iff no fatal flaws, no 'reject', and mean weighted score >= 7.0.
Round 2 of a milestone that still fails -> escalate to the user (a human decides).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from vnsoc.paths import paths

WEIGHTS = {"importance": .20, "novelty": .20, "rigor": .15, "feasibility": .15, "q1_likelihood": .15, "fit": .15}
PANEL = ["rev-editor", "rev-clinician", "rev-methods", "rev-feasibility", "rev-novelty"]
PASS_SCORE = 7.0
YAML_BLOCK = re.compile(r"```ya?ml\s*\n(.*?)```", re.S)


def parse(path: Path) -> dict:
    import yaml

    m = YAML_BLOCK.search(path.read_text(encoding="utf-8"))
    if not m:
        raise ValueError(f"{path.name}: thiếu khối ```yaml ở đầu")
    d = yaml.safe_load(m.group(1))
    missing = [k for k in WEIGHTS if k not in (d.get("scores") or {})]
    if missing:
        raise ValueError(f"{path.name}: thiếu điểm {missing}")
    d["weighted"] = round(sum(float(d["scores"][k]) * w for k, w in WEIGHTS.items()), 2)
    return d


def aggregate(milestone: str, root=None) -> tuple[bool, str]:
    P = paths(root)
    d = P.root / "review" / milestone
    reviews, problems = {}, []
    for name in PANEL:
        f = d / f"{name}.md"
        if not f.exists():
            problems.append(f"thiếu báo cáo {name}")
            continue
        try:
            reviews[name] = parse(f)
        except Exception as e:  # noqa: BLE001
            problems.append(str(e))
    if problems:
        return False, "CHƯA ĐỦ BÁO CÁO: " + "; ".join(problems)
    mean = round(sum(r["weighted"] for r in reviews.values()) / len(reviews), 2)
    fatal = [(n, f) for n, r in reviews.items() for f in (r.get("fatal_flaws") or [])]
    rejects = [n for n, r in reviews.items() if r.get("recommendation") == "reject"]
    ok = not fatal and not rejects and mean >= PASS_SCORE
    lines = [f"# Hội đồng phản biện {milestone}", "", f"Kết luận: **{'ĐẠT' if ok else 'CẦN SỬA'}** "
             f"(điểm trung bình có trọng số {mean}; ngưỡng {PASS_SCORE}; lỗi chết người {len(fatal)}; bác bỏ {len(rejects)})",
             "", "| Thành viên | Khuyến nghị | Điểm | " + " | ".join(WEIGHTS) + " |",
             "|" + "---|" * (3 + len(WEIGHTS))]
    for n, r in reviews.items():
        lines.append(f"| {n} | {r.get('recommendation')} | {r['weighted']} | "
                     + " | ".join(str(r['scores'][k]) for k in WEIGHTS) + " |")
    lines += ["", "## Lỗi chết người"] + ([f"- {n}: {f}" for n, f in fatal] or ["- (không có)"])
    lines += ["", "## Yêu cầu sửa (major trước)"]
    for sev in ("major", "minor"):
        for n, r in reviews.items():
            for c in r.get("required_changes") or []:
                if c.get("severity") == sev:
                    lines.append(f"- [{sev}] {n}#{c.get('id')} · {c.get('where')}: {c.get('what')} "
                                 f"→ kiểm: {c.get('acceptance')}")
    (d / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return ok, "\n".join(lines[:3])


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print(__doc__)
        return 2
    ok, msg = aggregate(argv[0])
    print(msg)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
