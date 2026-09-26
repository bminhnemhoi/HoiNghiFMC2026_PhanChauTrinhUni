"""Foreign-source cache: hashing, text extraction and value lookup — offline (requests is faked)."""
import hashlib

import pytest

from vnsoc.match import sources


class FakeResp:
    def __init__(self, content, ctype):
        self.content, self.headers, self.url = content, {"content-type": ctype}, "https://example.org/final"

    def raise_for_status(self):
        pass


def test_html_to_text_drops_scripts():
    raw = "<html><head><title>x</title><script>var a=1</script></head><body><p>Adults: 0.01&nbsp;mg/kg</p>" \
          "<table><tr><td>max</td><td>0.5 mg</td></tr></table></body></html>"
    t = sources.html_to_text(raw)
    assert "var a" not in t and "0.01" in t and "0.5 mg" in t


def test_fold_and_contains():
    assert sources.contains("Give 5–10 mL/kg/hour over 1 hour", "5-10 ml/kg/hour")
    assert not sources.contains("Give 5–10 mL/kg/hour", "15 ml/kg")


def test_fetch_caches_and_hashes(proj, monkeypatch):
    requests = pytest.importorskip("requests")
    body = b"<html><body><p>Post-exposure: days 0, 3, 7 and 14</p></body></html>"
    calls = []
    monkeypatch.setattr(requests, "get", lambda url, **kw: calls.append(url) or FakeResp(body, "text/html; charset=utf-8"))
    f = sources.fetch("https://example.org/pep", root=proj)
    assert f.sha256 == hashlib.sha256(body).hexdigest() and f.path.exists() and "days 0, 3, 7 and 14" in f.text
    g = sources.fetch("https://example.org/pep", root=proj)          # served from cache
    assert len(calls) == 1 and g.sha256 == f.sha256
    assert sources.grep(f.text, "days 0, 3, 7")[0][0] is None
    with pytest.raises(ValueError):
        sources.fetch("https://thuvienphapluat.vn/van-ban/x.aspx", root=proj)


def test_pdf_pages_marked(proj, monkeypatch):
    fitz = pytest.importorskip("fitz")
    requests = pytest.importorskip("requests")
    doc = fitz.open()
    for s in ("intro", "Pregnant women, first trimester: artemether-lumefantrine"):
        doc.new_page().insert_text((72, 72), s)
    data = doc.tobytes()
    monkeypatch.setattr(requests, "get", lambda url, **kw: FakeResp(data, "application/pdf"))
    f = sources.fetch("https://example.org/malaria.pdf", root=proj)
    hits = sources.grep(f.text, "first trimester")
    assert hits and hits[0][0] == 2


def test_block_page_detection_and_cached_text(proj, monkeypatch):
    requests = pytest.importorskip("requests")
    interstitial = b"<html><body>Checking your browser...</body></html>"
    monkeypatch.setattr(requests, "get", lambda url, **kw: FakeResp(interstitial, "text/html"))
    a = sources.fetch("https://repo.example.org/a.pdf", root=proj)
    sources.fetch("https://repo.example.org/b.pdf", root=proj)
    assert sources.block_hashes(proj) == {a.sha256}
    assert "Checking your browser" in sources.cached_text(a.sha256, proj)
    assert sources.cached_text("0" * 64, proj) is None
