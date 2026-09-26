"""Official-PDF download: atomic, never overwrites data/raw, reports text-layer quality (requests is faked)."""
import hashlib

import pytest

from vnsoc.extract import fetch_pdf as fp


class Resp:
    def __init__(self, data):
        self.content, self.headers, self.url = data, {"content-type": "application/pdf"}, "https://kcb.vn/x.pdf"

    def raise_for_status(self):
        pass


def _pdf(text: str) -> bytes:
    fitz = pytest.importorskip("fitz")
    doc = fitz.open()
    doc.new_page().insert_text((72, 72), text)
    return doc.tobytes()


def test_download_then_reuse_then_clash(proj, monkeypatch):
    requests = pytest.importorskip("requests")
    a, b = _pdf("version one"), _pdf("version two")
    monkeypatch.setattr(requests, "get", lambda url, **kw: Resp(a))
    r = fp.fetch_pdf("9999/2099", "https://kcb.vn/x.pdf", root=proj)
    assert r["status"] == "downloaded" and r["sha256"] == hashlib.sha256(a).hexdigest() and r["pages"] == 1
    assert fp.fetch_pdf("9999/2099", "https://kcb.vn/x.pdf", root=proj)["status"] == "exists_same"
    monkeypatch.setattr(requests, "get", lambda url, **kw: Resp(b))
    r = fp.fetch_pdf("9999/2099", "https://kcb.vn/x.pdf", root=proj)
    assert r["status"] == "clash_kept_both" and r["path"].endswith(f"9999_2099__{hashlib.sha256(b).hexdigest()[:8]}.pdf")
    assert (proj / "data" / "raw" / "9999_2099.pdf").read_bytes() == a


def test_forbidden_host_and_non_pdf(proj, monkeypatch):
    requests = pytest.importorskip("requests")
    with pytest.raises(SystemExit):
        fp.fetch_pdf("1/2020", "https://" + "thuvienphap" + "luat.vn/van-ban/x.pdf", root=proj)

    class Html(Resp):
        def __init__(self):
            super().__init__(b"<html></html>")
    monkeypatch.setattr(requests, "get", lambda url, **kw: Html())
    with pytest.raises(SystemExit):
        fp.fetch_pdf("1/2020", "https://kcb.vn/page.html", root=proj)


def test_text_quality_flags_scans():
    q = fp.text_quality(_pdf("short ascii text"))
    assert not q["text_layer"] and q["text_kind"] == "scanned_or_empty"
