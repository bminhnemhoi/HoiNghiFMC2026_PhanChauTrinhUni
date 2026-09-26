"""Registered, mechanical corpus inclusion order (prereg §3.1 item 1; rev-editor id 6). Replaces the discretionary
"prioritise text-layer PDFs, 2025-2026 guidance and conflict-rich topics" of protocol §3.1 with an ordered rule that
an outsider can reproduce from the catalogue alone; the same order serves DR2 additions before the corpus freeze.

Eligible: status 'current', an official PDF (official_pdf true), not only on a private site, issued on or before the
freeze date. Order (ties by doc_key):
  tier 1  documents cited by a row of the seed-conflict table (data/seed/seed_conflicts.yaml, rows not 'removed') or
          by a pilot atom — the operational meaning of "conflict-rich topic", fixed before any main-study output;
  tier 2  text-layer PDFs issued 2025-2026 (the clean set for version drift, protocol §3.1 item 3);
  tier 3  other text-layer PDFs, most recent first;
  tier 4  scanned PDFs (OCR), most recent first.
Documents are taken in this order until 35 are included; at most 10 OCR documents (current or superseded) in total, so
an OCR document beyond the cap is skipped. Scope (configs/corpus_scope.yaml, decision 2026-09-27): only documents of
the disease families of protocol §3.1 are included; a document outside the scope, or listed there as excluded, is a
DR2 reserve (ordered after every in-scope document by the same tiers, never included in the initial selection). DR2 (fewer than 400 conflict atoms or 25 families at T3.3) adds the next
eligible documents in the same order, never documents issued after the freeze date.

  $PY -m vnsoc.extract.corpus_priority results/tables/corpus_triage.csv   # prints the order with tier and reason
"""
from __future__ import annotations

import csv
import json
import os
import sys
from pathlib import Path

import yaml

MAX_DOCS = 35
MIN_DOCS = 25
MAX_OCR = 10
FREEZE = "2026-10-15"


def _truthy(x) -> bool:
    return str(x).strip().lower() in ("true", "1", "yes")


def seed_docs(seed_yaml: str | Path, pilot_atoms: list[dict] | None = None) -> set[str]:
    rows = (yaml.safe_load(Path(seed_yaml).read_text(encoding="utf-8")) or {}).get("rows") or []
    docs = {str(r["vn_doc"]) for r in rows if r.get("vn_doc") and r.get("status") != "removed"}
    docs |= {str(a["guideline"]).split("__")[0] for a in pilot_atoms or [] if a.get("guideline")}
    return docs


def load_scope(root=None) -> tuple[set[str] | None, dict[str, str]]:
    """(in-scope doc_keys, excluded {doc_key: reason}) from configs/corpus_scope.yaml; (None, {}) if absent."""
    from vnsoc.paths import paths

    f = paths(root).configs / "corpus_scope.yaml"
    if not f.exists():
        return None, {}
    d = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
    keys = {str(k) for docs in (d.get("families") or {}).values() for k in docs}
    return keys, {str(k): str(v) for k, v in (d.get("excluded") or {}).items()}


def priority_order(rows: list[dict], seeded: set[str], *, freeze: str = FREEZE, max_docs: int = MAX_DOCS,
                   max_ocr: int = MAX_OCR, ocr_already: int = 0, scope: set[str] | None = None,
                   excluded: dict[str, str] | None = None) -> list[dict]:
    """Ordered eligible documents with tier, inclusion flag and reason. `ocr_already` counts OCR documents already
    used outside this list (e.g. superseded versions), which share the cap of 10. With `scope`, documents outside it
    (or in `excluded`) come after all in-scope ones and are never included (DR2 reserve)."""
    excluded = excluded or {}

    def in_scope(r) -> bool:
        return (scope is None or r["doc_key"] in scope) and r["doc_key"] not in excluded
    elig = [r for r in rows if r.get("status") == "current" and _truthy(r.get("official_pdf"))
            and not _truthy(r.get("only_private_site")) and (not r.get("issued") or str(r["issued"]) <= freeze)]

    def tier(r) -> int:
        if r["doc_key"] in seeded:
            return 1
        if _truthy(r.get("text_layer")):
            return 2 if str(r.get("issued") or "")[:4] in ("2025", "2026") else 3
        return 4

    def key(r):
        return (not in_scope(r), tier(r),
                "" if tier(r) == 1 else "".join(chr(0x10FFFF - ord(c)) for c in str(r.get("issued") or "")), r["doc_key"])

    out, n_in, n_ocr = [], 0, ocr_already
    for r in sorted(elig, key=key):
        ocr = not _truthy(r.get("text_layer"))
        if not in_scope(r):
            inc, why = False, excluded.get(r["doc_key"]) or "ngoài phạm vi §3.1 (configs/corpus_scope.yaml) — dự phòng DR2"
        elif n_in >= max_docs:
            inc, why = False, "vượt 35 văn bản (dự phòng cho DR2 theo đúng thứ tự)"
        elif ocr and n_ocr >= max_ocr:
            inc, why = False, "vượt trần 10 văn bản OCR"
        else:
            inc, why = True, "trong 35 văn bản đầu"
            n_in += 1
            n_ocr += ocr
        out.append({"doc_key": r["doc_key"], "tier": tier(r), "issued": r.get("issued"), "ocr": ocr,
                    "in_scope": in_scope(r), "included": inc, "reason": why})
    return out


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if len(argv) != 1:
        print("dùng: python -m vnsoc.extract.corpus_priority <corpus_triage.csv>")
        return 2
    rows = list(csv.DictReader(open(argv[0], encoding="utf-8")))
    root = Path(argv[0]).resolve().parents[2]
    pilot = root / "data" / "interim" / "pilot_atoms.jsonl"
    atoms = [json.loads(x) for x in pilot.read_text(encoding="utf-8").splitlines() if x.strip()] if pilot.exists() else []
    scope, excluded = load_scope()
    order = priority_order(rows, seed_docs(root / "data" / "seed" / "seed_conflicts.yaml", atoms), scope=scope,
                           excluded=excluded, ocr_already=int(os.environ.get("VNSOC_OCR_ALREADY", "0")))
    for i, r in enumerate(order, 1):
        print(f"{i:3d} tier {r['tier']} {'IN ' if r['included'] else 'out'} {r['doc_key']:<14} {r['issued'] or '?':<10}"
              f"{' OCR' if r['ocr'] else ''}  {r['reason']}")
    n = sum(r["included"] for r in order)
    print(f"{n} văn bản được chọn" + ("" if n >= MIN_DOCS else f" (< {MIN_DOCS}: DR2 / báo người dùng)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
