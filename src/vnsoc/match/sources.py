"""Versioned reference sources (skill counterpart-matching): proof that a recorded value was read from a real page.

`fetch(url)` downloads a page or PDF once into data/cache/foreign/ (git-ignored, never released) and returns its
SHA-256, fetch date and plain text. The dataset keeps only VALUE + source + version date + locator + url + fetched_at
+ page_sha256 — never passages (ADA/ESC/AHA/GINA/GOLD are copyrighted). `contains()` / `grep()` let an agent prove
that the value string it records occurs in the fetched source; their output is for verification, not for storage.

  $PY -m vnsoc.match.sources fetch <url>              # -> sha256, path, chars, pages
  $PY -m vnsoc.match.sources grep <url> "<needle>"    # short contexts (+ PDF page numbers) around each hit
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import json
import re
import sys
import unicodedata
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path

from vnsoc.paths import paths

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/126.0 Safari/537.36 vn-soc-audit research (non-commercial)")
PAGE_MARK = "\n[[page {}]]\n"
DASHES = dict.fromkeys(map(ord, "‐‑‒–—―−"), "-")


def forbidden_hosts(root=None) -> tuple[str, ...]:
    """Hosts that must never be accessed automatically: configs/project.yaml corpus.forbidden_hosts."""
    import yaml

    cfg = yaml.safe_load((paths(root).configs / "project.yaml").read_text(encoding="utf-8"))
    return tuple((cfg.get("corpus") or {}).get("forbidden_hosts") or ())


@dataclass
class Fetched:
    url: str
    path: Path
    sha256: str
    fetched_at: str
    content_type: str
    text: str


def cache_dir(root=None) -> Path:
    d = paths(root).root / "data" / "cache" / "foreign"
    d.mkdir(parents=True, exist_ok=True)
    return d


class _Text(HTMLParser):
    SKIP = {"script", "style", "noscript", "svg", "head"}
    BLOCK = {"p", "div", "br", "li", "tr", "td", "th", "h1", "h2", "h3", "h4", "h5", "h6", "section", "table"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip += 1
        elif tag in self.BLOCK:
            self.out.append("\n")

    def handle_endtag(self, tag):
        if tag in self.SKIP and self.skip:
            self.skip -= 1
        elif tag in self.BLOCK:
            self.out.append("\n")

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)


def html_to_text(raw: str) -> str:
    p = _Text()
    p.feed(raw)
    text = html.unescape("".join(p.out))
    return re.sub(r"[ \t\r\f\v]+", " ", re.sub(r"\n\s*\n+", "\n", text)).strip()


def pdf_to_text(data: bytes) -> str:
    import pymupdf as fitz

    with fitz.open(stream=data, filetype="pdf") as doc:
        return "".join(PAGE_MARK.format(i) + p.get_text("text") for i, p in enumerate(doc, 1))


def _index(root=None) -> tuple[Path, dict]:
    f = cache_dir(root) / "index.json"
    return f, (json.loads(f.read_text(encoding="utf-8")) if f.exists() else {})


def _to_text(data: bytes, ctype: str) -> str:
    if data[:5] == b"%PDF-" or ("pdf" in ctype and b"%PDF-" in data[:1024]):
        return pdf_to_text(data)
    raw = data.decode("utf-8", errors="replace")
    try:
        return html_to_text(raw)
    except Exception:  # noqa: BLE001 — malformed or binary payload (e.g. zip/XML served as html): strip tags crudely
        return re.sub(r"\s+", " ", re.sub(r"<[^>]{0,2000}>", " ", raw)).strip()


def fetch(url: str, refresh: bool = False, timeout: int = 60, root=None) -> Fetched:
    if any(h in url for h in forbidden_hosts(root)):
        raise ValueError("nguồn bị cấm truy cập tự động (configs/project.yaml corpus.forbidden_hosts)")
    idx_file, idx = _index(root)
    hit = idx.get(url)
    if hit and not refresh and (cache_dir(root) / hit["file"]).exists():
        data = (cache_dir(root) / hit["file"]).read_bytes()
        return Fetched(url, cache_dir(root) / hit["file"], hit["sha256"], hit["fetched_at"], hit["content_type"],
                       _to_text(data, hit["content_type"]))
    import requests

    r = requests.get(url, headers={"User-Agent": UA, "Accept": "text/html,application/pdf,*/*"}, timeout=timeout)
    r.raise_for_status()
    data, ctype = r.content, r.headers.get("content-type", "").lower()
    sha = hashlib.sha256(data).hexdigest()
    ext = ".pdf" if ("pdf" in ctype or data[:5] == b"%PDF-") else ".html"
    name = sha[:20] + ext
    (cache_dir(root) / name).write_bytes(data)
    fetched_at = dt.date.today().isoformat()
    idx[url] = {"file": name, "sha256": sha, "fetched_at": fetched_at, "content_type": ctype, "final_url": r.url}
    idx_file.write_text(json.dumps(idx, ensure_ascii=False, indent=1), encoding="utf-8")
    return Fetched(url, cache_dir(root) / name, sha, fetched_at, ctype, _to_text(data, ctype))


def block_hashes(root=None) -> set[str]:
    """SHA-256 of HTML pages served for >= 2 different requested URLs: interstitial / anti-bot / consent pages
    (e.g. a repository returning the same HTML for several PDF links). Such a hash is not evidence of a value."""
    _, idx = _index(root)
    by: dict[str, set[str]] = {}
    for url, meta in idx.items():
        if "html" in (meta.get("content_type") or "") or meta["file"].endswith(".html"):
            by.setdefault(meta["sha256"], set()).add(url)
    return {sha for sha, urls in by.items() if len(urls) >= 2}


def cached_text(sha256: str, root=None) -> str | None:
    """Plain text of a cached source by its SHA-256 (None if not in the cache)."""
    _, idx = _index(root)
    for meta in idx.values():
        if meta["sha256"] == sha256 and (cache_dir(root) / meta["file"]).exists():
            return _to_text((cache_dir(root) / meta["file"]).read_bytes(), meta.get("content_type") or "")
    return None


def fold(s: str) -> str:
    """Case/dash/whitespace-insensitive form for matching value strings against source text."""
    s = unicodedata.normalize("NFKC", s or "").translate(DASHES).replace(" ", " ").lower()
    return re.sub(r"\s+", " ", s).strip()


def contains(text: str, needle: str) -> bool:
    return fold(needle) in fold(text)


def grep(text: str, needle: str, width: int = 90, limit: int = 8) -> list[tuple[int | None, str]]:
    """(pdf page or None, short context) for each hit. For the agent's own checking only — do not store."""
    t, n = fold(text), fold(needle)
    marks = [(m.start(), int(m.group(1))) for m in re.finditer(r"\[\[page (\d+)\]\]", t)]
    out, start = [], 0
    while n and len(out) < limit:
        i = t.find(n, start)
        if i < 0:
            break
        page = max((p for pos, p in marks if pos <= i), default=None)
        out.append((page, t[max(0, i - width): i + len(n) + width]))
        start = i + len(n)
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="sources")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("fetch"); s.add_argument("url"); s.add_argument("--refresh", action="store_true")
    s = sub.add_parser("grep"); s.add_argument("url"); s.add_argument("needle"); s.add_argument("--width", type=int, default=90)
    a = ap.parse_args(argv)
    f = fetch(a.url, refresh=getattr(a, "refresh", False))
    if a.cmd == "fetch":
        pages = f.text.count("[[page ")
        print(json.dumps({"url": f.url, "sha256": f.sha256, "fetched_at": f.fetched_at, "path": str(f.path),
                          "content_type": f.content_type, "chars": len(f.text), "pdf_pages": pages}, ensure_ascii=False))
        return 0
    hits = grep(f.text, a.needle, a.width)
    for page, ctx in hits:
        print(f"[p.{page}] …{ctx}…" if page else f"…{ctx}…")
    print(f"{len(hits)} kết quả · sha256={f.sha256[:16]} · fetched_at={f.fetched_at}")
    return 0 if hits else 1


if __name__ == "__main__":
    sys.exit(main())
