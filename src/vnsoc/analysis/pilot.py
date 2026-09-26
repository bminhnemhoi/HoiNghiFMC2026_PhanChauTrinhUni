"""Pilot grading and summary (T1.5; proposal §5.7, skill statistics-plan "Thí điểm").

Grades every pilot RunRecord with the pre-registered rules (vnsoc.grade, configs/grading.yaml), then reports COUNTS
a/b with exact Clopper–Pearson 95% intervals — separately for conflict, version-drift and concordant atoms — and the
foreign-vs-decoy comparison (no bootstrap: ~10 guidelines). The pilot atoms are hand-picked (stated in every output).
Registry keys pilot.* feed the FMC abstract placeholders [n] [k] [a] [b] [c] [d] [e] [f] (proposal §7.3).

Exclusions (data/interim/pilot_analysis_exclusions.yaml, decided before grading — HG1.2 errors, pending reference
standards, invalid decoys) never delete data: `atoms` drops every row of an atom, `mcq` drops its MCQ rows,
`descriptive` keeps the atom but reports it in group "descriptive", outside every pooled cell.
The foreign-vs-decoy comparison (the H1 analogue) uses only conflict atoms WITH a decoy (a conflict atom without a
valid decoy cannot produce a decoy match; prereg: excluded from H1/H2 and counted); `*_decoy_scaled` weights each
decoy match by k_i, the number of distinct conflicting foreign values of the atom (prereg §4.3). MCQ foreign counts
use the role TOKEN (an option carrying 'foreign:' counts even when it also carries 'superseded:'; D13 default).

  $PY -m vnsoc.analysis.pilot --runs data/runs/pilot --questions data/interim/pilot_questions.jsonl \
      --atoms data/interim/pilot_atoms.jsonl
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml
from scipy.stats import beta

from vnsoc.grade import grade_mcq, grade_short
from vnsoc.match.atom_flags import k_foreign
from vnsoc.numbers import put
from vnsoc.paths import paths

HAND = "mẫu chọn tay, chưa có bác sĩ duyệt"


def cp(k: int, n: int, level: float = 0.95) -> tuple[float, float]:
    """Exact Clopper–Pearson interval for k successes out of n."""
    if n == 0:
        return (0.0, 1.0)
    a = (1 - level) / 2
    lo = 0.0 if k == 0 else float(beta.ppf(a, k, n - k + 1))
    hi = 1.0 if k == n else float(beta.ppf(1 - a, k + 1, n - k))
    return lo, hi


def pct(x: float) -> str:
    return f"{100 * x:.1f}".replace(".", ",") + "%"


def group_of(atom: dict) -> str:
    if atom.get("conflict_status") == "conflict":
        return "conflict"
    if atom.get("superseded"):
        return "drift"
    return atom.get("conflict_status") or "other"


def grade_all(runs: list[dict], questions: dict[str, dict], atoms: dict[str, dict], synonyms, combos,
              grader_version: str) -> list[dict]:
    out = []
    for r in runs:
        a, q = atoms[r["atom_id"]], questions[r["question_id"]]
        if r.get("error"):
            g = None
        elif r["format"] == "mcq":
            g = grade_mcq(r["raw_output"], q["option_roles"])
        else:
            g = grade_short(r["raw_output"], a, r["language"], synonyms, combos, condition=r["condition"])
        row = {"run_id": r["run_id"], "question_id": r["question_id"], "atom_id": r["atom_id"], "model": r["model"],
               "condition": r["condition"], "language": r["language"], "format": r["format"], "group": group_of(a),
               "guideline": a["guideline"], "grader_version": grader_version, "error": r.get("error")}
        if g is not None:
            d = g.as_dict()
            row.update({k: d.get(k) for k in ("label", "label_name", "vn_match", "decoy_match", "parse_method", "multi",
                                              "partial", "unit_assumed", "needs_llm", "underspecified")})
            row["foreign_any"] = bool(d["foreign_systems"])
            row["foreign_systems"] = ",".join(d["foreign_systems"])
            row["superseded"] = ",".join(d["superseded"])
            row["answer_text"] = d["answer_text"]
        out.append(row)
    return out


def load_exclusions(path) -> dict:
    """{'atoms': {id: reason}, 'mcq': {id: reason}, 'descriptive': {id: reason}} (missing file = none)."""
    p = Path(path)
    d = (yaml.safe_load(p.read_text(encoding="utf-8")) or {}) if p.exists() else {}
    return {k: dict(d.get(k) or {}) for k in ("atoms", "mcq", "descriptive")}


def apply_exclusions(grades: list[dict], excl: dict) -> list[dict]:
    out = []
    for g in grades:
        if g["atom_id"] in excl["atoms"] or (g["format"] == "mcq" and g["atom_id"] in excl["mcq"]):
            continue
        if g["atom_id"] in excl["descriptive"]:
            g = dict(g, group="descriptive")
        out.append(g)
    return out


def cell(rows: list[dict], atoms: dict[str, dict] | None = None) -> dict:
    ok = [r for r in rows if r.get("label") is not None]
    n = len(ok)
    c = {f"L{i}": sum(1 for r in ok if r["label"] == i) for i in range(1, 7)}
    c.update(n=n, errors=len(rows) - n, needs_llm=sum(1 for r in rows if r.get("needs_llm")),
             correct=c["L1"] + c["L2"], foreign=c["L4"], stale=c["L3"],
             foreign_any=sum(1 for r in ok if r.get("foreign_any")),
             decoy=sum(1 for r in ok if r.get("decoy_match")),
             foreign_or_stale=c["L3"] + c["L4"])
    if atoms is not None:
        c["decoy_scaled"] = sum(k_foreign(atoms[r["atom_id"]]) for r in ok if r.get("decoy_match"))
    return c


def summarize(grades: list[dict]) -> dict:
    keys = sorted({(g["model"], g["condition"], g["language"], g["format"], g["group"]) for g in grades})
    return {"|".join(k): cell([g for g in grades if (g["model"], g["condition"], g["language"], g["format"],
                                                        g["group"]) == k]) for k in keys}


def register(grades: list[dict], atoms: dict[str, dict]) -> dict:
    """pilot.* keys. Pooled over models; A1 Vietnamese short answers are the confirmatory-analogue cell."""
    def pool(cond, lang, fmt, group, h1=False):
        return cell([g for g in grades if g["condition"] == cond and g["language"] == lang and g["format"] == fmt
                     and g["group"] == group and (not h1 or atoms[g["atom_id"]].get("decoy"))], atoms)

    reg = {}
    used = {g["atom_id"] for g in grades}
    ua = [atoms[i] for i in used]
    reg["n_atoms"] = len(ua)
    reg["n_guidelines"] = len({a["guideline"] for a in ua})
    groups = {g["atom_id"]: g["group"] for g in grades}
    reg["n_conflict_atoms"] = sum(1 for i in used if groups[i] == "conflict")
    reg["n_conflict_h1_atoms"] = sum(1 for i in used if groups[i] == "conflict" and atoms[i].get("decoy"))
    reg["n_descriptive_atoms"] = sum(1 for i in used if groups[i] == "descriptive")
    reg["n_concordant_atoms"] = sum(1 for i in used if groups[i] == "concordant")
    reg["n_drift_atoms"] = sum(1 for i in used if groups[i] == "drift")
    reg["n_models"] = len({g["model"] for g in grades})
    for lang in ("vi", "en"):
        c = pool("A1", lang, "short", "conflict")
        reg[f"a1_{lang}_conflict_n"] = c["n"]
        reg[f"a1_{lang}_foreign"] = c["foreign"]
        reg[f"a1_{lang}_correct"] = c["correct"]
        h = pool("A1", lang, "short", "conflict", h1=True)       # foreign vs decoy: conflict atoms with a decoy
        reg[f"a1_{lang}_h1_n"] = h["n"]
        reg[f"a1_{lang}_h1_foreign"] = h["foreign"]
        reg[f"a1_{lang}_decoy"] = h["decoy"]
        reg[f"a1_{lang}_decoy_scaled"] = h["decoy_scaled"]
        d = pool("A1", lang, "short", "concordant")
        reg[f"a1_{lang}_concordant_n"] = d["n"]
        reg[f"a1_{lang}_concordant_correct"] = d["correct"]
        s = pool("A1", lang, "short", "drift")
        reg[f"a1_{lang}_drift_n"] = s["n"]
        reg[f"a1_{lang}_stale"] = s["stale"]
        o = pool("A3", lang, "short", "conflict")
        reg[f"a3_{lang}_conflict_n"] = o["n"]
        reg[f"a3_{lang}_foreign_or_stale"] = o["foreign_or_stale"]
        z = pool("A0", lang, "short", "conflict")
        reg[f"a0_{lang}_conflict_n"] = z["n"]
        reg[f"a0_{lang}_foreign"] = z["foreign"]
        m = pool("A1", lang, "mcq", "conflict", h1=True)
        reg[f"mcq_a1_{lang}_n"] = m["n"]
        reg[f"mcq_a1_{lang}_foreign"] = m["foreign_any"]
        reg[f"mcq_a1_{lang}_decoy"] = m["decoy"]
    for cond in ("A0", "A1", "A3"):                    # every short-answer cell: <cond>_<lang>_<group>_<metric>
        for lang in ("vi", "en"):
            for group in ("conflict", "concordant", "drift"):
                c = pool(cond, lang, "short", group)
                for m in ("n", "correct", "foreign", "stale", "decoy"):
                    reg[f"{cond.lower()}_{lang}_{group}_{m}"] = c[m]
                reg[f"{cond.lower()}_{lang}_{group}_unattributed"] = c["L5"]
                reg[f"{cond.lower()}_{lang}_{group}_abstain"] = c["L6"]
    return reg


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="analysis.pilot")
    ap.add_argument("--runs", required=True, help="thư mục RunRecord JSONL")
    ap.add_argument("--questions", required=True)
    ap.add_argument("--atoms", required=True)
    ap.add_argument("--out-grades", default="data/processed/pilot_grades.parquet")
    ap.add_argument("--out-summary", default="results/pilot/pilot_summary.md")
    ap.add_argument("--exclusions", default="data/interim/pilot_analysis_exclusions.yaml")
    a = ap.parse_args(argv)
    P = paths()
    gcfg = yaml.safe_load((P.configs / "grading.yaml").read_text(encoding="utf-8"))
    load = lambda p: [json.loads(x) for x in Path(p).read_text(encoding="utf-8").splitlines() if x.strip()]  # noqa: E731
    from vnsoc.check import record_files

    runs = [r for f in record_files(a.runs) for r in load(f)]
    questions = {q["question_id"]: q for q in load(a.questions)}
    atoms = {x["atom_id"]: x for x in load(a.atoms)}
    grades = grade_all(runs, questions, atoms, gcfg.get("drugs") or {}, gcfg.get("combos") or {}, gcfg["grader_version"])
    excl = load_exclusions(a.exclusions)
    graded_all = grades
    grades = apply_exclusions(grades, excl)
    import pandas as pd

    Path(a.out_grades).parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(graded_all).to_parquet(a.out_grades, index=False)          # every row; exclusions applied below
    reg = register(grades, atoms)
    for k, v in reg.items():
        put(f"pilot.{k}", v, str(v), HAND)
    for lang in ("vi", "en"):
        k, n = reg[f"a1_{lang}_h1_foreign"], reg[f"a1_{lang}_h1_n"]
        if n:
            lo, hi = cp(k, n)
            put(f"pilot.a1_{lang}_h1_foreign_pct", k / n, pct(k / n), HAND)
            put(f"pilot.a1_{lang}_h1_foreign_ci", [lo, hi], f"{pct(lo)}–{pct(hi)}", "Clopper–Pearson 95%, " + HAND)
    for lang in ("vi", "en"):
        for num, den in (("foreign", "conflict_n"), ("decoy", "conflict_n"), ("concordant_correct", "concordant_n")):
            k, n = reg[f"a1_{lang}_{num}"], reg[f"a1_{lang}_{den}"]
            if n:
                lo, hi = cp(k, n)
                put(f"pilot.a1_{lang}_{num}_pct", k / n, pct(k / n), HAND)
                put(f"pilot.a1_{lang}_{num}_ci", [lo, hi], f"{pct(lo)}–{pct(hi)}", "Clopper–Pearson 95%, " + HAND)
        for cond in ("a0", "a1", "a3"):
            for group in ("conflict", "concordant"):
                n = reg[f"{cond}_{lang}_{group}_n"]
                for m in ("correct", "unattributed"):
                    k = reg[f"{cond}_{lang}_{group}_{m}"]
                    if n:
                        lo, hi = cp(k, n)
                        put(f"pilot.{cond}_{lang}_{group}_{m}_pct", k / n, pct(k / n), HAND)
                        put(f"pilot.{cond}_{lang}_{group}_{m}_ci", [lo, hi], f"{pct(lo)}–{pct(hi)}",
                            "Clopper–Pearson 95%, " + HAND)
        k, n = reg[f"a3_{lang}_foreign_or_stale"], reg[f"a3_{lang}_conflict_n"]
        if n:
            lo, hi = cp(k, n)
            put(f"pilot.a3_{lang}_foreign_or_stale_pct", k / n, pct(k / n), HAND)
            put(f"pilot.a3_{lang}_foreign_or_stale_ci", [lo, hi], f"{pct(lo)}–{pct(hi)}", "Clopper–Pearson 95%, " + HAND)
    summ = summarize(grades)
    lines = ["# Thí điểm — kết quả chấm (tự sinh bởi src/vnsoc/analysis/pilot.py)", "",
             f"Mẫu chọn tay, chưa có bác sĩ duyệt. grader_version {gcfg['grader_version']}. Nhãn: 1 đúng+biết bối cảnh, "
             "2 đúng, 3 lệch phiên bản, 4 trùng nước ngoài, 5 không quy được nguồn, 6 từ chối.", "",
             "Loại khỏi phân tích (quyết trước khi chấm, " + a.exclusions + "): "
             + ("; ".join(f"{kind} {i}: {why}" for kind in ("atoms", "mcq", "descriptive") for i, why in excl[kind].items())
                or "không có") + ".", "",
             "| mô hình | điều kiện | ngôn ngữ | dạng | nhóm mẩu | n | L1 | L2 | L3 | L4 | L5 | L6 | trùng mồi | lỗi | cần LLM |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for k, c in summ.items():
        m, cond, lang, fmt, grp = k.split("|")
        lines.append(f"| {m} | {cond} | {lang} | {fmt} | {grp} | {c['n']} | {c['L1']} | {c['L2']} | {c['L3']} | "
                     f"{c['L4']} | {c['L5']} | {c['L6']} | {c['decoy']} | {c['errors']} | {c['needs_llm']} |")
    Path(a.out_summary).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out_summary).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(reg, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
