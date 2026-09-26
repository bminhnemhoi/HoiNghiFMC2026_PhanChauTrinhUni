"""PDF -> positioned text (T2.4; proposal §4.1 step 1; skill atomization-protocol step 1).

For every official PDF of the manifest: one JSONL record per text block (PyMuPDF, with bbox and font size), per
table (pdfplumber, rows kept) and per OCR page (vnsoc.extract.ocr sidecar; no bbox), each carrying the heading
path in force ("C.2 > C.2.1"). Headings are numbered lines ("C.2.1.", "2.2.1.", "IV.", "Chương 3") that are bold
or short; page furniture (digital-signature stamps "syt_…_vt_…", bare page numbers) is dropped.
Output: data/interim/text/<pdf stem>.jsonl  (+ index.json with page/record counts and the PDF sha256).

  $PY -m vnsoc.extract.pdf_to_text [--keys 2760/2023 1740/2026] [--no-tables]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys

from vnsoc.extract.verify_span import norm, ocr_pages, page_text, pdf_path
from vnsoc.paths import paths

HEAD = re.compile(r"^\s*((?:[A-Z]|\d{1,2}|[IVX]{1,5})(?:\.\d{1,2}){0,4})(\.)?\s+(?=\S)|^\s*(Chương|Phần|Mục|PHỤ LỤC|Phụ lục)\s+[\dIVX]+",
                  re.U)
STAMP = re.compile(r"^\s*(?:syt|sở y tế)?[\w.]*_vt_", re.I)


def _level(tag: str) -> int:
    return 1 + tag.count(".") if tag else 1


def is_heading(line: str, bold: bool) -> str | None:
    m = HEAD.match(line)
    if not m:
        return None
    if m.group(3):                       # "Chương/Phần/Mục/Phụ lục": only when the whole line is bold (else a cross-reference)
        return m.group(3) if bold else None
    tag = m.group(1).strip()
    if "." not in tag and not m.group(2):   # "30 phút ..." is a sentence; single-token headings need a dot: "1.", "IV."
        return None
    if bold or len(line) <= 90:
        return tag
    return None


def furniture(text: str) -> bool:
    t = text.strip()
    return not t or bool(STAMP.match(t)) or bool(re.fullmatch(r"[-–\s]*\d{1,4}[-–\s]*", t))


def page_records(doc_key: str, pno: int, page, stack: list[tuple[int, str]]) -> list[dict]:
    out = []
    for i, b in enumerate(page.get_text("dict")["blocks"]):
        if b.get("type") != 0:
            continue
        lines, sizes = [], []
        for ln in b["lines"]:
            spans = ln["spans"]
            txt = norm("".join(s["text"] for s in spans))
            if not txt or furniture(txt):
                continue
            bold = all(s["flags"] & 16 for s in spans if s["text"].strip())
            tag = is_heading(txt, bold)
            if tag:
                lv = _level(tag)
                while stack and stack[-1][0] >= lv:
                    stack.pop()
                stack.append((lv, txt[:120]))
            lines.append(txt)
            sizes += [s["size"] for s in spans]
        if lines:
            out.append({"doc_key": doc_key, "page": pno, "idx": i, "kind": "text", "bbox": [round(v, 1) for v in b["bbox"]],
                        "font_size": round(max(sizes), 1), "headings": [h for _, h in stack], "text": norm(" ".join(lines))})
    return out


def extract(doc_key: str, tables: bool = True, root=None) -> tuple[list[dict], dict]:
    import pymupdf as fitz

    pdf = pdf_path(doc_key, root)
    sha = hashlib.sha256(pdf.read_bytes()).hexdigest()
    ocr = ocr_pages(pdf)
    recs, stack = [], []
    with fitz.open(pdf) as doc:
        n = doc.page_count
        for pno in range(1, n + 1):
            if pno in ocr:
                recs.append({"doc_key": doc_key, "page": pno, "idx": 0, "kind": "ocr", "bbox": None, "font_size": None,
                             "headings": [h for _, h in stack], "text": page_text(pdf, pno)})
                continue
            recs += page_records(doc_key, pno, doc[pno - 1], stack)
    if tables:
        import pdfplumber

        with pdfplumber.open(pdf) as pl:
            for pno, pg in enumerate(pl.pages, 1):
                if pno in ocr:
                    continue
                for j, tb in enumerate(pg.extract_tables() or []):
                    rows = [[norm(c or "") for c in r] for r in tb if any(c for c in r)]
                    if len(rows) >= 2:
                        recs.append({"doc_key": doc_key, "page": pno, "idx": 1000 + j, "kind": "table", "bbox": None,
                                     "font_size": None, "headings": [], "rows": rows,
                                     "text": " || ".join(" | ".join(r) for r in rows)})
    recs.sort(key=lambda r: (r["page"], r["idx"]))
    meta = {"doc_key": doc_key, "pdf": pdf.name, "sha256": sha, "pages": n, "ocr_pages": sorted(ocr),
            "records": len(recs), "tables": sum(r["kind"] == "table" for r in recs),
            "headings": len({h for r in recs for h in r["headings"]})}
    return recs, meta


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="pdf_to_text")
    ap.add_argument("--keys", nargs="*")
    ap.add_argument("--no-tables", action="store_true")
    a = ap.parse_args(argv)
    P = paths()
    rows = [json.loads(x) for x in (P.root / "data" / "interim" / "manifest.jsonl").read_text(encoding="utf-8").splitlines()
            if x.strip()]
    keys = a.keys or [r["doc_key"] for r in rows if r.get("sha256") and pdf_path(r["doc_key"]).exists()]
    out = P.root / "data" / "interim" / "text"
    out.mkdir(parents=True, exist_ok=True)
    idx_f = out / "index.json"
    index = json.loads(idx_f.read_text(encoding="utf-8")) if idx_f.exists() else {}
    for k in keys:
        try:
            recs, meta = extract(k, not a.no_tables)
        except Exception as e:  # noqa: BLE001
            print(f"LỖI {k}: {type(e).__name__}: {str(e)[:200]}")
            continue
        (out / (pdf_path(k).stem + ".jsonl")).write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in recs),
                                                        encoding="utf-8")
        index[k] = meta
        print(f"{k}: {meta['pages']} trang, {meta['records']} khối, {meta['tables']} bảng, OCR {len(meta['ocr_pages'])} trang")
    idx_f.write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
