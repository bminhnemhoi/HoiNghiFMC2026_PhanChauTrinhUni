"""OCR for scanned official PDFs (proposal §3.1: at most 10 OCR documents; every value read from OCR is checked by a
person against the page image — atoms from OCR pages carry extraction.ocr = true and are listed for that check).

Pages are rendered with PyMuPDF and read by Tesseract (lang vie+eng). Text goes to a sidecar directory
data/interim/ocr/<pdf stem>/pNNN.txt with meta.json (PDF sha256, engine version, dpi, lang, date). verify_span uses a
page's OCR text when the PDF page has no text layer, or for every page when meta.json has "override_text_layer": true
(a PDF whose embedded text layer is itself a bad OCR, e.g. no diacritics).

  $PY -m vnsoc.extract.ocr --key 3377/2023 [--pages 1-40] [--override-text-layer] [--force]
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from vnsoc.extract.verify_span import pdf_path
from vnsoc.paths import paths

CANDIDATES = (r"C:\Program Files\Tesseract-OCR\tesseract.exe", r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe")


def tesseract_bin() -> str | None:
    exe = os.environ.get("VNSOC_TESSERACT") or shutil.which("tesseract")
    if exe:
        return exe
    return next((c for c in CANDIDATES if Path(c).is_file()), None)


def tessdata_dir(root=None) -> Path | None:
    """Project model dir data/cache/tessdata (tessdata_best vie/eng/osd, downloaded 2026-09-26), else Tesseract's own."""
    d = Path(os.environ.get("VNSOC_TESSDATA") or paths(root).root / "data" / "cache" / "tessdata")
    return d if (d / "vie.traineddata").exists() else None


def sidecar_dir(pdf: Path | str, root=None) -> Path:
    return paths(root).root / "data" / "interim" / "ocr" / Path(pdf).stem


def sidecar_meta(pdf: Path | str, root=None) -> dict | None:
    f = sidecar_dir(pdf, root) / "meta.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else None


def sidecar_page(pdf: Path | str, page: int, root=None) -> str | None:
    f = sidecar_dir(pdf, root) / f"p{page:03d}.txt"
    return f.read_text(encoding="utf-8") if f.exists() else None


def _pages_arg(s: str | None, n: int) -> list[int]:
    if not s:
        return list(range(1, n + 1))
    out = []
    for part in s.split(","):
        a, _, b = part.partition("-")
        out += list(range(int(a), int(b or a) + 1))
    return [p for p in out if 1 <= p <= n]


def ocr_pdf(key: str, pages: str | None = None, dpi: int = 300, lang: str = "vie+eng", override: bool = False,
            force: bool = False, root=None) -> dict:
    exe = tesseract_bin()
    if not exe:
        raise SystemExit("Chưa cài Tesseract (HG0.3): winget install --id UB-Mannheim.TesseractOCR -e -i (chọn Vietnamese)")
    td = tessdata_dir(root)
    base = [exe] + (["--tessdata-dir", str(td)] if td else [])
    langs = subprocess.run(base + ["--list-langs"], capture_output=True, text=True).stdout
    if "vie" not in langs.split():
        raise SystemExit("Tesseract thiếu dữ liệu tiếng Việt (vie.traineddata)")
    import pymupdf as fitz

    pdf = pdf_path(key, root)
    data = pdf.read_bytes()
    out_dir = sidecar_dir(pdf, root)
    out_dir.mkdir(parents=True, exist_ok=True)
    version = subprocess.run([exe, "--version"], capture_output=True, text=True).stdout.splitlines()[0]
    done = []
    with fitz.open(stream=data, filetype="pdf") as doc, tempfile.TemporaryDirectory() as tmp:
        for p in _pages_arg(pages, doc.page_count):
            target = out_dir / f"p{p:03d}.txt"
            if target.exists() and not force:
                continue
            img = Path(tmp) / f"p{p}.png"
            doc[p - 1].get_pixmap(dpi=dpi).save(img)
            r = subprocess.run(base + [str(img), "stdout", "-l", lang, "--psm", "3"], capture_output=True)
            target.write_text(r.stdout.decode("utf-8", errors="replace"), encoding="utf-8")
            done.append(p)
    models = {f.name: hashlib.sha256(f.read_bytes()).hexdigest()[:16] for f in sorted(td.glob("*.traineddata"))} if td else {}
    meta = {"key": key, "pdf": pdf.name, "pdf_sha256": hashlib.sha256(data).hexdigest(), "engine": version,
            "tessdata": "tessdata_best (project copy)" if td else "tesseract default", "models": models,
            "lang": lang, "dpi": dpi, "psm": 3, "override_text_layer": override, "date": dt.date.today().isoformat(),
            "pages_done": sorted({int(f.stem[1:]) for f in out_dir.glob("p*.txt")})}
    (out_dir / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    return {**meta, "new_pages": done}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="ocr")
    ap.add_argument("--key", required=True)
    ap.add_argument("--pages")
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--override-text-layer", action="store_true")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args(argv)
    r = ocr_pdf(a.key, a.pages, a.dpi, override=a.override_text_layer, force=a.force)
    print(json.dumps({k: v for k, v in r.items() if k != "pages_done"} | {"pages": len(r["pages_done"])},
                     ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
