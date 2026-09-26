"""Download an official guideline PDF into data/raw/ (skill corpus-acquisition, T1.1/T2.2).

Atomic and never destructive: the file is downloaded to a temp name, hashed, then moved to data/raw/<key>.pdf;
if that file already exists with a different SHA-256 the new copy is kept as data/raw/<key>__<sha8>.pdf and the
clash is reported (data/raw is never overwritten). Also reports page count and text-layer quality: a PDF whose
first pages yield little Vietnamese text is flagged scanned (needs OCR), and text full of TCVN3/VNI glyphs
(e.g. "Quy¿t ®Þnh") is flagged legacy_font — neither can be span-verified without OCR.

  $PY -m vnsoc.extract.fetch_pdf --key 2760/2023 --url "https://kcb.vn/....pdf"
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
import tempfile
from urllib.parse import urlparse

from vnsoc.extract.verify_span import pdf_path
from vnsoc.paths import paths

VI_LETTERS = re.compile(r"[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]", re.I)
LEGACY = re.compile(r"[¸µ¶·¹ª«¬®¯©ÇÐ¿Þ¾½¼»º±°¡¢£¤¥¦§¨]")


def text_quality(data: bytes, first: int = 4) -> dict:
    import pymupdf as fitz

    with fitz.open(stream=data, filetype="pdf") as doc:
        pages = doc.page_count
        text = "".join(doc[i].get_text("text") for i in range(min(first, pages)))
    vi, legacy = len(VI_LETTERS.findall(text)), len(LEGACY.findall(text))
    kind = "ok" if vi >= 200 and legacy < vi / 4 else ("legacy_font" if legacy >= 50 else "scanned_or_empty")
    return {"pages": pages, "vi_chars_first_pages": vi, "legacy_glyphs": legacy, "text_layer": kind == "ok",
            "text_kind": kind}


def fetch_pdf(key: str, url: str, root=None, timeout: int = 120) -> dict:
    host = (urlparse(url).hostname or "").lower()
    import yaml

    cfg = yaml.safe_load((paths(root).configs / "project.yaml").read_text(encoding="utf-8"))
    if any(host == h or host.endswith("." + h) for h in (cfg.get("corpus") or {}).get("forbidden_hosts") or ()):
        raise SystemExit(f"CHẶN: {host} bị cấm truy cập tự động")
    import requests

    from vnsoc.match.sources import UA

    r = requests.get(url, headers={"User-Agent": UA}, timeout=timeout)
    r.raise_for_status()
    data = r.content
    if data[:5] != b"%PDF-":
        raise SystemExit(f"không phải PDF ({r.headers.get('content-type')}, {len(data)} bytes): {url}")
    sha = hashlib.sha256(data).hexdigest()
    target = pdf_path(key, root)
    target.parent.mkdir(parents=True, exist_ok=True)
    out = {"key": key, "url": url, "final_url": r.url, "host": host, "sha256": sha, "bytes": len(data),
           "downloaded": dt.date.today().isoformat(), **text_quality(data)}
    if target.exists():
        old = hashlib.sha256(target.read_bytes()).hexdigest()
        if old == sha:
            out.update(path=str(target), status="exists_same")
            return out
        target = target.with_name(f"{target.stem}__{sha[:8]}.pdf")
        out["status"] = "clash_kept_both"
    else:
        out["status"] = "downloaded"
    fd, tmp = tempfile.mkstemp(dir=target.parent, suffix=".part")
    with os.fdopen(fd, "wb") as f:
        f.write(data)
    os.replace(tmp, target)
    out["path"] = str(target)
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="fetch_pdf")
    ap.add_argument("--key", required=True, help="'2760/2023' or 'TT51/2017'")
    ap.add_argument("--url", required=True)
    a = ap.parse_args(argv)
    print(json.dumps(fetch_pdf(a.key, a.url), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
