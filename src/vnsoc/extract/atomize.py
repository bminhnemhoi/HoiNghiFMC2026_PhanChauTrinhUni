"""Main-study atomisation (T3.1), agent-based: extraction agents follow configs/extraction_protocol.md (the prompt of
record, hashed into every atom's extraction.protocol_sha256) and write data/interim/atoms_parts/<doc>*.jsonl; code
verifies every atom (vnsoc.extract.verify_span via vnsoc.extract.atoms_merge). The paid-API batch extractor of the
original plan is replaced (docs/DECISIONS.md 2026-09-26T20:40, laptop-only, no paid API).

This module measures the plan's acceptance criterion for the pipeline: the share of pilot atoms re-found by the main
extraction (target >= 90%). A pilot atom counts as re-found when a main atom of the same guideline, on the same page
(+-1), states a value of the pilot atom's MoH set (value gap 0 under vnsoc.grade._gap, same value kind), or quotes an
overlapping span (>= 60% of the shorter span's words).

  $PY -m vnsoc.extract.atomize refind      # pilot atoms re-found in data/interim/atoms_parts (on in-corpus documents)
"""
from __future__ import annotations

import json
import sys

from vnsoc.paths import paths


def _words(s: str) -> list[str]:
    from vnsoc.extract.verify_span import norm

    return norm(s or "").lower().split()


def span_overlap(a: str, b: str) -> float:
    wa, wb = _words(a), _words(b)
    if not wa or not wb:
        return 0.0
    sa, sb = set(wa), set(wb)
    return len(sa & sb) / min(len(sa), len(sb))


def same_value(p: dict, m: dict) -> bool:
    from vnsoc.grade import _gap

    if p.get("value_kind") != m.get("value_kind"):
        return False
    atom = dict(p, context=p.get("context") or m.get("context") or {})
    for x in p.get("vn") or []:
        for y in m.get("vn") or []:
            try:
                if _gap(x, y, atom) == 0:
                    return True
            except Exception:  # noqa: BLE001 - unconvertible units: not the same value
                continue
    return False


def refound(pilot: dict, mains: list[dict]) -> str | None:
    """atom_id of the main atom that re-finds the pilot atom, or None."""
    for m in mains:
        if m.get("guideline") != pilot.get("guideline") or abs(int(m["page"]) - int(pilot["page"])) > 1:
            continue
        if same_value(pilot, m) or span_overlap(pilot.get("span", ""), m.get("span", "")) >= 0.6:
            return m["atom_id"]
    return None


def refind_rate(pilot_atoms: list[dict], main_atoms: list[dict], in_corpus: set[str] | None = None) -> dict:
    rows = [a for a in pilot_atoms if not in_corpus or a["guideline"] in in_corpus]
    by_doc: dict[str, list[dict]] = {}
    for m in main_atoms:
        by_doc.setdefault(m["guideline"], []).append(m)
    hits = {a["atom_id"]: refound(a, by_doc.get(a["guideline"], [])) for a in rows}
    n, k = len(hits), sum(1 for v in hits.values() if v)
    return {"n": n, "refound": k, "rate": (k / n) if n else None, "missing": sorted(i for i, v in hits.items() if not v),
            "matches": {i: v for i, v in hits.items() if v}}


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if not argv or argv[0] != "refind":
        print(__doc__)
        return 2
    from vnsoc.extract.atoms_merge import corpus_keys, load_parts

    P = paths()
    pilot = [json.loads(x) for x in (P.root / "data" / "interim" / "pilot_atoms.jsonl").read_text(encoding="utf-8")
             .splitlines() if x.strip()]
    parts = P.root / "data" / "interim" / "atoms_parts"
    mains = load_parts(parts)
    r = refind_rate(pilot, mains, corpus_keys())
    out = P.root / "review" / "extraction_audit" / "pilot_refind.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
    rate = "—" if r["rate"] is None else f"{r['rate']:.1%}"
    print(f"mẩu thí điểm trên văn bản trong kho: {r['n']}; tìm lại {r['refound']} ({rate}); thiếu: {r['missing']}")
    return 0 if r["rate"] is not None and r["rate"] >= 0.9 else 1


if __name__ == "__main__":
    sys.exit(main())
