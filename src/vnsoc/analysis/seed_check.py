"""Outcome of checking each seed-conflict row (proposal §3.3) against the official texts (T1.1 pilot).

Inputs: data/interim/pilot_atoms.jsonl (atoms carry `seed_row` and a code-computed conflict_status) and
data/interim/seed_row_notes.yaml — for rows that produced NO conflict atom, a person/agent-written outcome with the
evidence pointer (report path + section), e.g. {row: 4, outcome: not_a_recommendation, evidence: "...report.md §4"}.
Outcome per row: confirmed_conflict (≥ 1 conflict atom) | not_clean (checked; concordant under DR8, indistinguishable,
or not the value/population the table says) | blocked (no official text usable yet) | not_checked.
Writes results/tables/seed_row_check.csv and registry keys design.seed_rows_checked / _confirmed / _not_clean /
_blocked (numbers only by code).

  $PY -m vnsoc.analysis.seed_check
"""
from __future__ import annotations

import csv
import json
import sys

import yaml

from vnsoc.numbers import put
from vnsoc.paths import paths

NOT_CLEAN = {"not_clean", "concordant_dr8", "indistinguishable", "not_a_recommendation", "wrong_value", "wrong_population"}
BLOCKED = {"blocked", "no_official_text", "superseded_no_current"}


def outcomes(seed: dict, atoms: list[dict], notes: list[dict]) -> list[dict]:
    by_row: dict[int, list[dict]] = {}
    for a in atoms:
        if a.get("seed_row"):
            by_row.setdefault(int(a["seed_row"]), []).append(a)
    note = {int(n["row"]): n for n in notes}
    out = []
    for r in seed["rows"]:
        n, atoms_r = r["row"], by_row.get(r["row"], [])
        conf = [a["atom_id"] for a in atoms_r if a.get("conflict_status") == "conflict"]
        if conf:
            oc, ev = "confirmed_conflict", "; ".join(conf)
        elif n in note:
            raw = note[n]["outcome"]
            oc = "not_clean" if raw in NOT_CLEAN else "blocked" if raw in BLOCKED else raw
            ev = note[n].get("evidence", "")
        elif atoms_r:
            oc, ev = "not_clean", "; ".join(f"{a['atom_id']}={a.get('conflict_status')}" for a in atoms_r)
        else:
            oc, ev = "not_checked", ""
        out.append({"row": n, "topic": r["topic"], "seed_status": r.get("status"), "outcome": oc,
                    "detail": (note.get(n) or {}).get("outcome", ""), "evidence": ev})
    return out


def main() -> int:
    P = paths()
    seed = yaml.safe_load((P.root / "data" / "seed" / "seed_conflicts.yaml").read_text(encoding="utf-8"))
    f = P.root / "data" / "interim" / "pilot_atoms.jsonl"
    atoms = [json.loads(x) for x in f.read_text(encoding="utf-8").splitlines() if x.strip()] if f.exists() else []
    nf = P.root / "data" / "interim" / "seed_row_notes.yaml"
    notes = (yaml.safe_load(nf.read_text(encoding="utf-8")) or {}).get("rows", []) if nf.exists() else []
    rows = outcomes(seed, atoms, notes)
    out = P.results / "tables" / "seed_row_check.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    usable = [r for r in rows if r["seed_status"] not in ("removed",)]
    counts = {k: sum(r["outcome"] == k for r in usable) for k in ("confirmed_conflict", "not_clean", "blocked", "not_checked")}
    checked = len(usable) - counts["not_checked"]
    note = "đối chiếu thí điểm T1.1 (agent + mã; chưa có người/bác sĩ kiểm), results/tables/seed_row_check.csv"
    put("design.seed_rows_checked", checked, str(checked), note)
    put("design.seed_rows_confirmed", counts["confirmed_conflict"], str(counts["confirmed_conflict"]), note)
    put("design.seed_rows_not_clean", counts["not_clean"], str(counts["not_clean"]), note)
    put("design.seed_rows_blocked", counts["blocked"], str(counts["blocked"]), note)
    print(json.dumps({"checked": checked, **counts}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
