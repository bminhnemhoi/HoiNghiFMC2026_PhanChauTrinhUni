"""Foreign reference store (T2.6): schema, no passage text (> 200 chars), evidence in the cached source."""
import json
from pathlib import Path

import pytest

from vnsoc.match import foreign_store
from vnsoc.schemas import ForeignRecord

STORE = Path("data/interim/foreign_values.jsonl")


def _rec(**kw):
    r = {"record_id": "F-x-001", "disease": "Sốt xuất huyết Dengue", "topic": "dịch truyền giờ đầu, sốc, người lớn",
         "system": "WHO_global", "source": "WHO 2009 dengue", "version_date": "2009", "url": "https://example.org/x.pdf",
         "locator": "Table 4, p.42", "fetched_at": "2026-09-27", "page_sha256": "0" * 64,
         "values": [{"lo": 5, "hi": 7, "unit": "ml/kg/h"}]}
    r.update(kw)
    return r


def test_long_text_fields_flag_passages():
    assert foreign_store.long_text_fields(_rec()) == []
    assert foreign_store.long_text_fields(_rec(note="x" * 201)) == ["note"]
    assert foreign_store.long_text_fields(_rec(values=[{"lo": 5, "hi": 7, "text": "y" * 300}])) == ["values[0].text"]


def test_check_record_needs_cached_source():
    probs = foreign_store.check_record(_rec(), set())
    assert any("không có bản đệm" in p for p in probs)          # sha not in the cache -> rejected
    assert any("schema" in p for p in foreign_store.check_record(_rec(values=[]), set()))


@pytest.mark.skipif(not STORE.exists(), reason="kho nước ngoài chưa dựng")
def test_store_rows_valid_and_short():
    rows = [json.loads(x) for x in STORE.read_text(encoding="utf-8").splitlines() if x.strip()]
    assert rows
    for r in rows:
        ForeignRecord.model_validate(r)
        assert r["url"] and r["page_sha256"] and r["fetched_at"]
        assert foreign_store.long_text_fields(r) == [], r["record_id"]
    assert len({r["record_id"] for r in rows}) == len(rows)
