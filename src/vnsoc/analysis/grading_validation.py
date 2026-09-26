"""Validation of the rule-based grader on the pilot (replaces the manual parser check HG6.2, delegated by the user):
two blind AI adjudicators (A, B) label every graded answer, an AI referee resolves every disagreement with the rule
label and records the cause (review/pilot_grading/chunk*_final.jsonl). Reports raw agreement and Cohen's kappa,
the rule grader's accuracy against the resolved reference label (Clopper–Pearson 95%), and the causes of grader
errors; registers pilot.grader_* keys. The adjudicators are AI, not people (stated in every output).

  $PY -m vnsoc.analysis.grading_validation
"""
from __future__ import annotations

import collections
import json
import sys

from vnsoc.analysis.pilot import cp, pct
from vnsoc.numbers import put
from vnsoc.paths import paths

NOTE = "người chấm là AI (hai người chấm mù + trọng tài), không phải người; thí điểm chọn tay"


def kappa(a: list, b: list) -> float | None:
    """Cohen's kappa for two raters over the same items (None if undefined)."""
    n = len(a)
    if n == 0 or n != len(b):
        return None
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = collections.Counter(a), collections.Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)
    return None if pe == 1 else (po - pe) / (1 - pe)


def load(root=None) -> list[dict]:
    d = paths(root).root / "review" / "pilot_grading"
    return [json.loads(x) for f in sorted(d.glob("chunk*_final.jsonl"))
            for x in f.read_text(encoding="utf-8").splitlines() if x.strip()]


def summary(rows: list[dict]) -> dict:
    rows = [r for r in rows if r.get("final") is not None and r.get("rule") is not None]
    rule = [int(r["rule"]) for r in rows]
    fin = [int(r["final"]) for r in rows]
    a = [int(r["A"]) for r in rows if r.get("A") is not None and r.get("B") is not None]
    b = [int(r["B"]) for r in rows if r.get("A") is not None and r.get("B") is not None]
    agree = sum(x == y for x, y in zip(rule, fin))
    causes = collections.Counter(r.get("cause") for r in rows if int(r["rule"]) != int(r["final"]))
    return {"n": len(rows), "agree": agree, "kappa_rule_final": kappa(rule, fin), "kappa_ab": kappa(a, b),
            "ab_agree": sum(x == y for x, y in zip(a, b)), "ab_n": len(a), "causes": dict(causes)}


def main(argv=None) -> int:
    s = summary(load())
    if not s["n"]:
        print("chưa có review/pilot_grading/chunk*_final.jsonl")
        return 1
    lo, hi = cp(s["agree"], s["n"])
    put("pilot.grader_n", s["n"], str(s["n"]), NOTE)
    put("pilot.grader_agree", s["agree"], str(s["agree"]), NOTE)
    put("pilot.grader_agree_pct", s["agree"] / s["n"], pct(s["agree"] / s["n"]), NOTE)
    put("pilot.grader_agree_ci", [lo, hi], f"{pct(lo)}–{pct(hi)}", "Clopper–Pearson 95%, " + NOTE)
    for k in ("kappa_rule_final", "kappa_ab"):
        if s[k] is not None:
            put(f"pilot.grader_{k}", s[k], f"{s[k]:.2f}".replace(".", ","), NOTE)
    print(json.dumps(s, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
