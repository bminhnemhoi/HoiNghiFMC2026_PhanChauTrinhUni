"""T2.2 acceptance: every manifest row that has an official source_url has its PDF in data/raw/ with the recorded
SHA-256 (the default file or a second official copy <key>__<sha8>.pdf / the file chosen in pdf_choice.json), no row
points to a forbidden host, doc_key is unique, and rows are schema-valid."""
import hashlib
import json

import pytest
import yaml

from vnsoc.extract.verify_span import pdf_path
from vnsoc.paths import paths
from vnsoc.schemas import ManifestRow

ROOT = paths().root
F = ROOT / "data" / "interim" / "manifest.jsonl"
ROWS = [json.loads(x) for x in F.read_text(encoding="utf-8").splitlines() if x.strip()] if F.exists() else []
pytestmark = pytest.mark.skipif(not F.exists(), reason="chưa có data/interim/manifest.jsonl (T2.1)")
FORBIDDEN = yaml.safe_load((ROOT / "configs" / "project.yaml").read_text(encoding="utf-8"))["corpus"]["forbidden_hosts"]


def _sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def test_unique_keys_and_schema():
    keys = [r["doc_key"] for r in ROWS]
    assert len(keys) == len(set(keys)), [k for k in keys if keys.count(k) > 1]
    for r in ROWS:
        ManifestRow.model_validate(r)
        assert not any(h in (r.get("source_url") or "") for h in FORBIDDEN)


@pytest.mark.raw_data   # needs the official PDFs in data/raw (not redistributed)
@pytest.mark.parametrize("row", [r for r in ROWS if r.get("source_url") and r.get("sha256")], ids=lambda r: r["doc_key"])
def test_downloaded_file_matches_sha(row):
    default = pdf_path(row["doc_key"])
    base = default.stem.split("__")[0]                  # pdf_choice.json may point to a second official copy
    cands = [default, default.parent / f"{base}.pdf", *default.parent.glob(base + "__*.pdf")]
    shas = {_sha(p) for p in cands if p.exists()}
    assert shas, f"thiếu file PDF cho {row['doc_key']} trong data/raw/"
    assert row["sha256"] in shas, f"{row['doc_key']}: sha256 trong manifest không khớp file nào trong data/raw/"
