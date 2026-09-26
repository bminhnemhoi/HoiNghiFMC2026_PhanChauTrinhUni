"""Design numbers for the FMC abstract 'design' version (T1.6) -> results/numbers.json keys design.*.

Sources: data/seed/seed_conflicts.yaml (agent-reviewed seed table, proposal §3.3 — NOT yet checked by a person) and,
when present, data/interim/pilot_atoms.jsonl (pilot atoms span-verified against official MoH PDFs by code; context
not yet checked by a person, HG1.2). Every number in the abstract comes from here or from configs/*.yaml.

  $PY -m vnsoc.analysis.design_counts
"""
from __future__ import annotations

import json
import sys

import yaml

from vnsoc.grade import LABELS
from vnsoc.numbers import put
from vnsoc.paths import paths

CONFLICT_STATUSES = {"confirmed", "confirmed_complex", "confirmed_low_stakes", "confirmed_low_stakes_not_rechecked",
                     "confirmed_us_only", "confirmed_us_only_not_rechecked", "fixed", "fixed_relabelled"}
NOTE_SEED = "bộ hạt giống §3.3 (agent rà soát vòng 2, chưa có người kiểm)"
NOTE_PILOT = "mẩu thí điểm đã khớp nguyên văn PDF chính thức bằng mã (verify_span); chưa có người kiểm ngữ cảnh (HG1.2)"


def seed_counts(seed: dict) -> dict:
    rows = seed["rows"]
    usable = [r for r in rows if r.get("status") in CONFLICT_STATUSES]
    systems = {f["system"] for r in usable for f in r.get("foreign") or []}
    us_only = [r for r in usable if "us_only" in r.get("status", "")]
    return {
        "seed_rows": len(rows),
        "seed_conflict_rows": len(usable),
        "seed_us_only_rows": len(us_only),
        "seed_pilot_rows": sum(1 for r in rows if r.get("pilot")),
        "seed_guidelines": len({r["vn_doc"] for r in usable if r.get("vn_doc")}),
        "seed_foreign_systems": len(systems),
        "seed_version_drift_pairs": len(seed.get("version_drift_pilot") or []),
        "seed_concordant_topics": len(seed.get("concordant_controls") or []),
    }


def pilot_counts(atoms: list[dict]) -> dict:
    ok = [a for a in atoms if a.get("span_verified")]
    conflict = [a for a in ok if a.get("conflict_status") == "conflict"]
    return {
        "pdf_atoms": len(ok),
        "pdf_conflicts": len(conflict),
        "pdf_concordant": sum(1 for a in ok if a.get("conflict_status") == "concordant"),
        "pdf_version_drift": sum(1 for a in ok if a.get("superseded")),
        "pdf_guidelines": len({a["guideline"] for a in ok}),
        "pdf_conflict_families": len({a.get("conflict_family") for a in conflict if a.get("conflict_family")}),
        "pdf_seed_rows_confirmed": len({a["seed_row"] for a in conflict if a.get("seed_row")}),
        "pdf_foreign_systems": len({f["system"] for a in ok for f in a.get("foreign") or []}),
    }


def main() -> int:
    P = paths()
    seed = yaml.safe_load((P.root / "data" / "seed" / "seed_conflicts.yaml").read_text(encoding="utf-8"))
    for k, v in seed_counts(seed).items():
        put(f"design.{k}", v, str(v), NOTE_SEED)
    put("design.n_labels", len(LABELS), str(len(LABELS)), "số nhãn chấm (vnsoc.grade.LABELS, đề cương §1.2)")
    f = P.root / "data" / "interim" / "pilot_atoms.jsonl"
    if f.exists():
        atoms = [json.loads(line) for line in f.read_text(encoding="utf-8").splitlines() if line.strip()]
        for k, v in pilot_counts(atoms).items():
            put(f"design.{k}", v, str(v), NOTE_PILOT)
    print(json.dumps({**seed_counts(seed), **(pilot_counts(atoms) if f.exists() else {})}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
