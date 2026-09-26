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
  $PY -m vnsoc.extract.verify_span --image 3377/2023 23                # PNG of the page (check OCR numbers by eye)
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


_GLYPH = str.maketrans({"\u01a3": "\u01b0", "\u01a2": "\u01af",   # ƣ/Ƣ -> ư/Ư
                        "\uf0b3": "\u2265", "\uf0a3": "\u2264",   # Symbol-font PUA: ≥ ≤
                        "\uf0b1": "\u00b1", "\uf0b4": "\u00d7",   # ± ×
                        "\uf02b": "+", "\uf02d": "-", "\uf020": " ",   # Symbol-font + - space (bullets: 162/2024, 3879/2014)
                        "\uf06d": "\u00b5", "\uf0b0": "\u00b0",        # Symbol mu (ug/kg in 3312/2015), degree
                        "\uf0ad": "\u2191", "\uf0af": "\u2193", "\uf0b7": "\u2022",   # up/down arrows, bullet
                        "\u04df": "\u1edb", "\u04af": "\u1eab"})  # Cyrillic look-alikes in 162/2024 -> Vietnamese o-horn-acute, a-circumflex-tilde


def norm(s: str | None) -> str:
    """NFC + NBSP->space + drop invisible characters + common glyph fixes + collapse whitespace."""
    s = unicodedata.normalize("NFC", s or "").replace("\u00a0", " ").translate(_INVISIBLE).translate(_GLYPH)
    return _WS.sub(" ", s).strip()


def pdf_choice(root=None) -> dict[str, str]:
    """doc_key -> file name in data/raw/, when a document exists in several official copies (e.g. a scanned signed
    decision and a text-layer copy of the attached guideline): data/interim/pdf_choice.json, written by code/people
    with the reason; the corpus freeze hashes the chosen file."""
    import json

    f = paths(root).root / "data" / "interim" / "pdf_choice.json"
    return {k: v["file"] for k, v in json.loads(f.read_text(encoding="utf-8")).items()} if f.exists() else {}


def pdf_path(guideline: str, root=None) -> Path:
    key = guideline.replace(" ", "")
    raw = paths(root).root / "data" / "raw"
    chosen = pdf_choice(root).get(key)
    return raw / chosen if chosen else raw / (key.replace("/", "_") + ".pdf")


@lru_cache(maxsize=32)
def _pages(pdf: str, mtime: float) -> tuple[str, ...]:
    import pymupdf as fitz

    with fitz.open(pdf) as doc:
        return tuple(norm(p.get_text("text")) for p in doc)


def _side_mtime(pdf: Path) -> float:
    from vnsoc.extract.ocr import sidecar_dir  # lazy: ocr imports this module

    d = sidecar_dir(pdf)
    return max((f.stat().st_mtime for f in d.glob("*")), default=0.0) if d.exists() else 0.0


@lru_cache(maxsize=32)
def _resolved(pdf: str, mtime: float, smtime: float) -> tuple[tuple[str, ...], frozenset[int]]:
    """Page texts, using the OCR sidecar (vnsoc.extract.ocr) for pages without a text layer, or for every page
    when the sidecar says override_text_layer. A sidecar made from a different PDF (sha256) is ignored."""
    base, ocr = list(_pages(pdf, mtime)), set()
    if smtime:
        import hashlib

        from vnsoc.extract.ocr import sidecar_meta, sidecar_page

        meta = sidecar_meta(pdf) or {}
        if meta.get("pdf_sha256") == hashlib.sha256(Path(pdf).read_bytes()).hexdigest():
            for i in range(len(base)):
                t = sidecar_page(pdf, i + 1)
                if t is None:
                    continue
                t = norm(t)
                # scanned pages often carry only a digital-signature / watermark line in their text layer
                if meta.get("override_text_layer") or (len(base[i]) < 200 and len(t) > 2 * len(base[i])):
                    base[i], _ = t, ocr.add(i + 1)
    return tuple(base), frozenset(ocr)


def page_texts(pdf: Path | str) -> tuple[str, ...]:
    p = Path(pdf)
    return _resolved(str(p), p.stat().st_mtime, _side_mtime(p))[0]


def ocr_pages(pdf: Path | str) -> frozenset[int]:
    """1-based pages whose text comes from OCR (values must be checked against the page image)."""
    p = Path(pdf)
    return _resolved(str(p), p.stat().st_mtime, _side_mtime(p))[1]


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


def dr8_spans(atom: dict) -> list[dict]:
    """Secondary current-MoH sources merged into the value set under DR8 (proposal §1.2): extraction.dr8_sources =
    [{guideline, page, span (or span_nguyen_van), ...}]."""
    out = []
    for s in (atom.get("extraction") or {}).get("dr8_sources") or []:
        span = s.get("span") or s.get("span_nguyen_van") or ""
        if s.get("guideline") and s.get("page") and span:
            out.append({"guideline": s["guideline"], "page": int(s["page"]), "span": span})
    return out


def missing_vn_values(atom: dict, lang: str = "vi", synonyms=None, combos=None) -> list[int]:
    """Indices of `vn` items that cannot be parsed back from the span or from a DR8 source span (empty = all present).
    Drug classes named without their form ('tenofovir') do not count: the span must name the drug itself."""
    from vnsoc.grade import _named, matches, parse_values

    a = dict(atom, tolerance=0.0)
    vals = []
    for s in [atom.get("span") or ""] + [d["span"] for d in dr8_spans(atom)]:
        vals += [v for _, v in parse_values(s, a, lang, synonyms, combos)]
    return [i for i, item in enumerate(atom.get("vn") or []) if not any(matches(_named(v), item, a)[0] for v in vals)]


def verify_atom(atom: dict, root=None, synonyms=None, combos=None) -> dict:
    if synonyms is None or combos is None:
        synonyms, combos = drug_tables(root)
    pdf = pdf_path(atom["guideline"], root)
    out = {"atom_id": atom.get("atom_id"), "pdf": str(pdf), "pdf_exists": pdf.exists(), "span_on_page": False,
           "missing_vn": [], "ok": False, "reason": "", "ocr": False}
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
    out["ocr"] = int(atom["page"]) in ocr_pages(pdf)
    for d in dr8_spans(atom):                       # every DR8 span must itself be verbatim on its page
        p2 = pdf_path(d["guideline"], root)
        if not p2.exists() or not span_on_page(p2, d["page"], d["span"]):
            out["reason"] = f"span DR8 của {d['guideline']} không có ở trang {d['page']}"
            return out
        out["ocr"] = out["ocr"] or d["page"] in ocr_pages(p2)
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
    ap.add_argument("--image", nargs=2, metavar=("GUIDELINE", "PAGE"), help="render the page to PNG (check OCR by eye)")
    a = ap.parse_args(argv)
    if a.image:
        import pymupdf as fitz

        pdf, pg = pdf_path(a.image[0]), int(a.image[1])
        out = paths().root / "data" / "cache" / "page_images" / f"{pdf.stem}_p{pg:03d}.png"
        out.parent.mkdir(parents=True, exist_ok=True)
        with fitz.open(pdf) as doc:
            doc[pg - 1].get_pixmap(dpi=150).save(out)
        print(out)
        return 0
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
