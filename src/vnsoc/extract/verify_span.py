"""Span verification for recommendation atoms (proposal §4.1 step 3; skill atomization-protocol).

An atom is span-verified when
  (1) its `span` occurs verbatim on the stated 1-based `page` of the official PDF, after Unicode NFC and
      whitespace normalisation of both sides, and
  (2) every MoH value item in `vn` can be read back from the span with the grader's own parser
      (vnsoc.grade.parse_values + vnsoc.grade.matches at tolerance 0), so "the value is in the text" means the
      same thing at extraction time and at grading time.

The PDF of guideline 'NNNN/YYYY' is data/raw/NNNN_YYYY.pdf; circulars use the key 'TT51/2017' -> data/raw/TT51_2017.pdf.

  $PY -m vnsoc.extract.verify_span data/interim/pilot_atoms.jsonl      # one line per atom, exit 1 if any fails
  $PY -m vnsoc.extract.verify_span --find 2760/2023 "15 ml/kg"         # pages whose text contains the snippet
  $PY -m vnsoc.extract.verify_span --page 2760/2023 23                 # print the normalised text of one page
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from functools import lru_cache
from pathlib import Path

from vnsoc.paths import paths

_WS = re.compile(r"\s+")
_INVISIBLE = dict.fromkeys(map(ord, "­​‌‍﻿"), None)   # soft hyphen, zero-width chars


def norm(s: str | None) -> str:
    """NFC + NBSP->space + drop invisible characters + collapse whitespace."""
    s = unicodedata.normalize("NFC", s or "").replace(" ", " ").translate(_INVISIBLE)
    return _WS.sub(" ", s).strip()


def pdf_path(guideline: str, root=None) -> Path:
    return paths(root).root / "data" / "raw" / (guideline.replace(" ", "").replace("/", "_") + ".pdf")


@lru_cache(maxsize=32)
def _pages(pdf: str, mtime: float) -> tuple[str, ...]:
    import fitz  # PyMuPDF

    with fitz.open(pdf) as doc:
        return tuple(norm(p.get_text("text")) for p in doc)


def page_texts(pdf: Path | str) -> tuple[str, ...]:
    p = Path(pdf)
    return _pages(str(p), p.stat().st_mtime)


def page_text(pdf: Path | str, page: int) -> str:
    pages = page_texts(pdf)
    return pages[page - 1] if 1 <= page <= len(pages) else ""


def span_on_page(pdf: Path | str, page: int, span: str) -> bool:
    s = norm(span)
    return bool(s) and s in page_text(pdf, page)


def find_pages(pdf: Path | str, snippet: str) -> list[int]:
    s = norm(snippet)
    return [i for i, t in enumerate(page_texts(pdf), 1) if s and s in t]


def drug_tables(root=None) -> tuple[dict, dict]:
    import yaml

    cfg = yaml.safe_load((paths(root).configs / "grading.yaml").read_text(encoding="utf-8"))
    return cfg.get("drugs") or {}, cfg.get("combos") or {}


def missing_vn_values(atom: dict, lang: str = "vi", synonyms=None, combos=None) -> list[int]:
    """Indices of `vn` items that cannot be parsed back from the span (empty list = all present)."""
    from vnsoc.grade import matches, parse_values

    a = dict(atom, tolerance=0.0)
    vals = [v for _, v in parse_values(atom.get("span") or "", a, lang, synonyms, combos)]
    return [i for i, item in enumerate(atom.get("vn") or []) if not any(matches(v, item, a)[0] for v in vals)]


def verify_atom(atom: dict, root=None, synonyms=None, combos=None) -> dict:
    if synonyms is None or combos is None:
        synonyms, combos = drug_tables(root)
    pdf = pdf_path(atom["guideline"], root)
    out = {"atom_id": atom.get("atom_id"), "pdf": str(pdf), "pdf_exists": pdf.exists(), "span_on_page": False,
           "missing_vn": [], "ok": False, "reason": ""}
    if not pdf.exists():
        out["reason"] = f"thiếu PDF {pdf.name}"
        return out
    if len(atom.get("span") or "") > 600:
        out["reason"] = "span > 600 ký tự"
        return out
    out["span_on_page"] = span_on_page(pdf, int(atom["page"]), atom.get("span") or "")
    if not out["span_on_page"]:
        pages = find_pages(pdf, atom.get("span") or "")
        out["reason"] = f"span không có ở trang {atom['page']}" + (f" (có ở trang {pages})" if pages else "")
        return out
    out["missing_vn"] = missing_vn_values(atom, "vi", synonyms, combos)
    if out["missing_vn"]:
        out["reason"] = f"không đọc lại được giá trị vn {out['missing_vn']} từ span"
        return out
    out["ok"] = True
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="verify_span")
    ap.add_argument("atoms", nargs="?", help="JSONL of atoms")
    ap.add_argument("--find", nargs=2, metavar=("GUIDELINE", "SNIPPET"))
    ap.add_argument("--page", nargs=2, metavar=("GUIDELINE", "PAGE"))
    a = ap.parse_args(argv)
    if a.find:
        print(find_pages(pdf_path(a.find[0]), a.find[1]))
        return 0
    if a.page:
        print(page_text(pdf_path(a.page[0]), int(a.page[1])))
        return 0
    if not a.atoms:
        ap.error("cần file atoms hoặc --find/--page")
    syn, combos = drug_tables()
    bad = 0
    with open(a.atoms, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            r = verify_atom(json.loads(line), synonyms=syn, combos=combos)
            bad += not r["ok"]
            print(f"{'OK ' if r['ok'] else 'LỖI'} {r['atom_id']}: {r['reason']}")
    print(f"{'OK' if not bad else 'LỖI'}: {bad} mẩu không đạt")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
