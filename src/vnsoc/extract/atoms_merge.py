"""Merge main-study atoms (data/interim/atoms_parts/<doc>.jsonl, one file per guideline, written by the extraction
agents) into data/interim/atoms.jsonl (T3.2–T3.3; the main-study counterpart of vnsoc.extract.pilot_merge).

Same guarantees as the pilot merge — every atom is re-finalised by code (decoy by the registered rule, tolerance and
conflict_status by vnsoc.grade), re-verified against its PDF page (vnsoc.extract.verify_span) and schema-validated;
failures are left out and listed — plus two main-study rules: the atom's guideline must be an in_corpus document of
the manifest (once any document is marked in_corpus), and pilot atoms stay in the pilot file (pilot: true is rejected
here). Also writes the audit sheet used by the AI double audit and the co-authors' sample check
(review/atoms/audit_sheet.csv: one row per kept atom, verdict columns left empty).

  $PY -m vnsoc.extract.atoms_merge                              # all parts -> data/interim/atoms.jsonl + audit sheet
  $PY -m vnsoc.extract.atoms_merge --only 2760_2023 --out <tmp>  # one part, dry check: no shared file written
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

from vnsoc.extract.pilot_merge import CLINICIAN_ONLY, canonical_keys, enforce_decoy_rule, source_warnings
from vnsoc.extract.verify_span import drug_tables, pdf_path, verify_atom
from vnsoc.match.decoys import check_decoy, finalize
from vnsoc.paths import paths
from vnsoc.schemas import Atom

AUDIT_COLUMNS = ["atom_id", "guideline", "pdf", "page", "section", "span", "moh_values", "population", "foreign",
                 "superseded", "decoy", "conflict_status", "ocr", "code_warnings",
                 "a_verbatim", "b_value_unit", "c_population", "d_foreign", "note"]


def load_parts(d: Path, only: str | None = None) -> list[dict]:
    files = [d / f"{only}.jsonl"] if only else sorted(f for f in d.glob("*.jsonl") if not f.stem.endswith("_skipped"))
    atoms = []
    for f in files:
        if not f.exists():
            raise SystemExit(f"không có {f}")
        atoms += [json.loads(x) for x in f.read_text(encoding="utf-8").splitlines() if x.strip()]
    return atoms


def corpus_keys(root=None) -> set[str]:
    """doc_keys marked in_corpus in data/interim/manifest.jsonl (empty set = selection not made yet)."""
    f = paths(root).root / "data" / "interim" / "manifest.jsonl"
    if not f.exists():
        return set()
    rows = [json.loads(x) for x in f.read_text(encoding="utf-8").splitlines() if x.strip()]
    return {r["doc_key"] for r in rows if r.get("in_corpus")}


def check(atom: dict, syn, combos, in_corpus: set[str], root=None) -> list[str]:
    probs = []
    try:
        Atom.model_validate(atom)
    except Exception as e:  # noqa: BLE001
        probs.append(f"schema: {str(e)[:200]}")
    r = verify_atom(atom, root, syn, combos)
    if not r["ok"]:
        probs.append(f"verify_span: {r['reason']}")
    if atom.get("pilot"):
        probs.append("mẩu thí điểm (pilot: true) không gộp vào bộ chính")
    if in_corpus and atom.get("guideline") not in in_corpus:
        probs.append(f"văn bản {atom.get('guideline')} không thuộc kho (in_corpus)")
    if any(atom.get(k) is not None for k in CLINICIAN_ONLY):
        probs.append("có trường chỉ-bác-sĩ")
    for f in atom.get("foreign") or []:
        if not f.get("url") or not f.get("fetched_at"):
            probs.append(f"nguồn nước ngoài thiếu url/fetched_at: {f.get('source')}")
    probs += [f"mồi: {p}" for p in check_decoy(atom)]
    return probs


def _vals(items) -> str:
    return "; ".join(str(it.get("text") or {k: v for k, v in it.items() if v is not None}) for it in items or []) or ""


def audit_rows(atoms: list[dict], warns: dict[str, list[str]], root=None) -> list[dict]:
    rows = []
    for a in atoms:
        rows.append({
            "atom_id": a["atom_id"], "guideline": a["guideline"], "pdf": f"data/raw/{pdf_path(a['guideline'], root).name}",
            "page": a["page"], "section": a["section"], "span": a["span"], "moh_values": _vals(a["vn"]),
            "population": json.dumps(a.get("population") or {}, ensure_ascii=False),
            "foreign": " | ".join(f"{f['system']}: {_vals(f['values'])} ({f.get('source')}; {f.get('locator') or ''}; "
                                  f"{f.get('url') or ''})" for f in a.get("foreign") or []),
            "superseded": " | ".join(f"{s['guideline']} tr.{s.get('page')}: {_vals(s['values'])}"
                                     for s in a.get("superseded") or []),
            "decoy": _vals(a.get("decoy")), "conflict_status": a.get("conflict_status"),
            "ocr": bool((a.get("extraction") or {}).get("ocr")), "code_warnings": " | ".join(warns.get(a["atom_id"], [])),
        })
    return rows


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m vnsoc.extract.atoms_merge",
                                 description="Gộp mẩu nghiên cứu chính (data/interim/atoms_parts) thành atoms.jsonl.")
    ap.add_argument("--only", metavar="PART", help="chỉ nạp data/interim/atoms_parts/<PART>.jsonl (cần --out)")
    ap.add_argument("--out", metavar="PATH", help="ghi mẩu ra PATH thay vì data/interim/atoms.jsonl")
    ap.add_argument("--parts", metavar="DIR", help="thư mục phần mẩu (mặc định data/interim/atoms_parts)")
    args = ap.parse_args(argv)
    if args.only and not args.out:
        ap.error("--only cần --out")
    shared = not args.only and not args.out
    P = paths()
    from vnsoc.match.sources import block_hashes

    syn, combos = drug_tables()
    blocks = block_hashes()
    parts = Path(args.parts) if args.parts else P.root / "data" / "interim" / "atoms_parts"
    atoms = [finalize(enforce_decoy_rule(a)) for a in canonical_keys(load_parts(parts, args.only), write=shared)]
    in_corpus = corpus_keys()
    seen, keep, bad = set(), [], []
    for a in atoms:
        probs = check(a, syn, combos, in_corpus)
        if a["atom_id"] in seen:
            probs.append("atom_id trùng")
        seen.add(a["atom_id"])
        (bad if probs else keep).append((a, probs))
    for a, _ in keep:
        if verify_atom(a, None, syn, combos).get("ocr"):
            a["extraction"] = dict(a.get("extraction") or {}, ocr=True)
    out = Path(args.out) if args.out else P.root / "data" / "interim" / "atoms.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("".join(json.dumps(a, ensure_ascii=False) + "\n" for a, _ in keep), encoding="utf-8")
    rej = out.with_name(out.stem + "_rejects.jsonl")
    rej.write_text("".join(json.dumps({"atom_id": a.get("atom_id"), "problems": p}, ensure_ascii=False) + "\n"
                           for a, p in bad), encoding="utf-8")
    warns = {a["atom_id"]: (["trang OCR — so từng con số với ảnh trang"] if (a.get("extraction") or {}).get("ocr")
                            else []) + source_warnings(a, blocks) for a, _ in keep}
    if shared:
        sheet = P.root / "review" / "atoms" / "audit_sheet.csv"
        sheet.parent.mkdir(parents=True, exist_ok=True)
        with open(sheet, "w", encoding="utf-8-sig", newline="") as f:      # utf-8-sig: opens cleanly in Excel
            w = csv.DictWriter(f, fieldnames=AUDIT_COLUMNS, restval="")
            w.writeheader()
            w.writerows(audit_rows([a for a, _ in keep], warns))
    by = {}
    for a, _ in keep:
        by[a["conflict_status"]] = by.get(a["conflict_status"], 0) + 1
    print(f"giữ {len(keep)} mẩu {by} -> {out}; loại {len(bad)} (xem {rej.name})")
    for a, p in bad:
        print(f"  LOẠI {a.get('atom_id')}: {'; '.join(p)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
