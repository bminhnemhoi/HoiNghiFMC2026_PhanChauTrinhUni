"""Co-author review pack: builds a self-contained HTML with page images; imports answers and compares with AI audit."""
import json
from pathlib import Path

import pytest

from vnsoc import review_pack


def test_build_and_import(tmp_path):
    f = Path("data/interim/pilot_atoms.jsonl")
    if not f.exists() or not Path("data/raw").exists():
        pytest.skip("không có mẩu thí điểm/PDF")
    a = next(json.loads(x) for x in f.read_text(encoding="utf-8").splitlines() if '"P-dengue-01"' in x)
    out = review_pack.build([a], tmp_path / "pack.html", "Thử")
    t = out.read_text(encoding="utf-8")
    assert "data:image/jpeg;base64," in t and "P-dengue-01|a" in t and "Tải kết quả" in t
    assert 10_000 < out.stat().st_size < 3_000_000
    ans = tmp_path / "pack_X.json"
    ans.write_text(json.dumps({"reviewer": "X", "answers": {"P-dengue-01|a": "dung", "P-dengue-01|b": "sai",
                                                            "P-dengue-01|note": "sai đơn vị"}}), encoding="utf-8")
    audit = tmp_path / "audit"
    audit.mkdir()
    (audit / "t_final.json").write_text(json.dumps({"atoms": [{"atom_id": "P-dengue-01", "a": "pass", "b": "pass",
                                                               "c": "pass"}]}), encoding="utf-8")
    r = review_pack.import_answers(ans, audit)
    assert r["compared"] == 2 and r["agree"] == 1 and r["rows"][0]["note"] == "sai đơn vị"
