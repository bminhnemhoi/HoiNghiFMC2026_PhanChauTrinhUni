"""Manifest merge: one row per document, richest row wins, lists unioned, status conflicts flagged."""
from vnsoc.extract.manifest_merge import merge_rows, missing_md, triage

BASE = {"number": "2760", "year": 2023, "kind": "QĐ", "title": "Hướng dẫn chẩn đoán, điều trị SXH Dengue",
        "disease": "dengue", "status": "current"}


def test_merge_prefers_evidence_and_flags_conflicts():
    a = dict(BASE, doc_key="2760/2023", supersedes=["3705/2019"], notes="c1")
    b = dict(BASE, doc_key="2760/2023", source_url="https://kcb.vn/x.pdf", source_host="kcb.vn", sha256="ab" * 32,
             pages=100, text_layer=True, supersedes=["458/2011"], notes="c5")
    c = dict(BASE, doc_key="3705/2019", number="3705", year=2019, status="current", notes="c1")
    d = dict(BASE, doc_key="3705/2019", number="3705", year=2019, status="superseded", notes="c5")
    rows = merge_rows([a, b, c, d])
    assert [r["doc_key"] for r in rows] == ["2760/2023", "3705/2019"]
    assert rows[0]["source_url"] and rows[0]["supersedes"] == ["3705/2019", "458/2011"]
    assert "MÂU THUẪN" in rows[1]["notes"]
    t = triage(rows)
    assert t[0]["official_pdf"] and not t[1]["official_pdf"]
    assert "3705/2019" in missing_md(rows)
