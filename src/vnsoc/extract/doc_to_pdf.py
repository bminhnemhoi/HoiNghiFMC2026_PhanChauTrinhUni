"""Official guideline published only as Word (.doc/.docx) on an official host (e.g. QĐ 1622/QĐ-BYT 2014 on
vncdc.gov.vn). A PERSON downloads the original in a browser (HG2.3) and saves it under data/raw/manual/; this
converts that local file to data/raw/<key>.pdf with Microsoft Word (COM, "Save as PDF"), so span verification reads
the document's own text. Provenance (source url given by the person, original sha256, converter, date) goes to
data/interim/pdf_provenance/<key>.json. No network access here. Windows + Word only.

  $PY -m vnsoc.extract.doc_to_pdf --key 1622/2014 --file data/raw/manual/1622_2014.doc --source-url "<url>"
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import subprocess
import sys
from pathlib import Path

from vnsoc.extract.fetch_pdf import text_quality
from vnsoc.extract.verify_span import pdf_path
from vnsoc.paths import paths

PS = r"""
$ErrorActionPreference = 'Stop'
$w = New-Object -ComObject Word.Application
$w.Visible = $false
try {
  $d = $w.Documents.Open('{src}', $false, $true)
  $d.SaveAs2('{dst}', 17)
  $d.Close($false)
  Write-Output $w.Version
} finally { $w.Quit() }
"""


def convert(key: str, file: str, source_url: str, root=None) -> dict:
    src = Path(file).resolve()
    data = src.read_bytes()
    if not (data[:4] == b"PK\x03\x04" or data[:8] == bytes.fromhex("d0cf11e0a1b11ae1")):
        raise SystemExit("không phải tệp Word (.doc/.docx)")
    dst = pdf_path(key, root)
    if dst.exists():
        raise SystemExit(f"{dst.name} đã có trong data/raw — không ghi đè")
    dst.parent.mkdir(parents=True, exist_ok=True)
    script = PS.replace("{src}", str(src)).replace("{dst}", str(dst.resolve()))
    r = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", script],
                       check=True, capture_output=True, text=True)
    pdf = dst.read_bytes()
    prov = {"key": key, "source_url": source_url, "original_file": str(src), "original_sha256": hashlib.sha256(data).hexdigest(),
            "converter": f"Microsoft Word {r.stdout.strip()} (COM SaveAs2 wdFormatPDF=17)",
            "pdf_sha256": hashlib.sha256(pdf).hexdigest(), "date": dt.date.today().isoformat(),
            "note": "PDF dựng từ tệp Word chính thức do người dùng tải; lớp chữ là văn bản của chính tệp gốc",
            **text_quality(pdf)}
    d = paths(root).root / "data" / "interim" / "pdf_provenance"
    d.mkdir(parents=True, exist_ok=True)
    (d / (key.replace("/", "_") + ".json")).write_text(json.dumps(prov, ensure_ascii=False, indent=1), encoding="utf-8")
    return prov


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="doc_to_pdf")
    ap.add_argument("--key", required=True)
    ap.add_argument("--file", required=True, help="tệp .doc/.docx chính thức người dùng đã tải")
    ap.add_argument("--source-url", required=True)
    a = ap.parse_args(argv)
    print(json.dumps(convert(a.key, a.file, a.source_url), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
