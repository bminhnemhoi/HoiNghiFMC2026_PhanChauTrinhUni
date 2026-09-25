#!/usr/bin/env python3
"""Verify every reference in manuscript/references.yaml against a registry (never trust memory).

Entry fields: key, title, authors (list), year, venue, and at least one of doi | arxiv | url.
- doi   -> https://api.crossref.org/works/<doi>  (DataCite fallback: https://api.datacite.org/dois/<doi>)
- arxiv -> https://export.arxiv.org/api/query?id_list=<id>
- url only (laws, MoH decisions, web pages) -> NOT auto-verifiable: needs `checked_by_human: true`
  (set only after the user confirms, human gate HG7.3).
Title match: normalised token similarity >= 0.85 and year within +-1.
Writes manuscript/citations_verified.json; exit 1 if any entry fails or is unverified.
"""
import json
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UA = {"User-Agent": "vn-soc-audit-citation-check/0.1"}


def norm(s: str) -> list[str]:
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return re.findall(r"[a-z0-9]+", s)


def similarity(a: str, b: str) -> float:
    ta, tb = norm(a), norm(b)
    if not ta or not tb:
        return 0.0
    sa, sb = set(ta), set(tb)
    return 2 * len(sa & sb) / (len(sa) + len(sb))


def get(url: str) -> bytes | None:
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read()
        except Exception:
            time.sleep(2 * (attempt + 1))
    return None


def lookup_doi(doi: str) -> tuple[str | None, int | None]:
    raw = get("https://api.crossref.org/works/" + urllib.parse.quote(doi))
    if raw:
        m = json.loads(raw)["message"]
        year = (m.get("issued", {}).get("date-parts") or [[None]])[0][0]
        return (m.get("title") or [None])[0], year
    raw = get("https://api.datacite.org/dois/" + urllib.parse.quote(doi))
    if raw:
        a = json.loads(raw)["data"]["attributes"]
        return (a.get("titles") or [{}])[0].get("title"), a.get("publicationYear")
    return None, None


def lookup_arxiv(aid: str) -> tuple[str | None, int | None]:
    raw = get("https://export.arxiv.org/api/query?id_list=" + urllib.parse.quote(aid))
    if not raw:
        return None, None
    ns = {"a": "http://www.w3.org/2005/Atom"}
    e = ET.fromstring(raw).find("a:entry", ns)
    if e is None or e.find("a:title", ns) is None:
        return None, None
    title = " ".join(e.find("a:title", ns).text.split())
    year = int(e.find("a:published", ns).text[:4])
    return title, year


def main() -> int:
    import yaml

    refs = yaml.safe_load((ROOT / "manuscript" / "references.yaml").read_text(encoding="utf-8")) or []
    out, bad = [], 0
    for r in refs:
        res = {"key": r.get("key"), "status": "unverified", "found_title": None, "similarity": None}
        found_title, found_year = None, None
        if r.get("doi"):
            found_title, found_year = lookup_doi(r["doi"])
        if not found_title and r.get("arxiv"):
            found_title, found_year = lookup_arxiv(r["arxiv"])
        if found_title:
            sim = similarity(r.get("title", ""), found_title)
            year_ok = not r.get("year") or not found_year or abs(int(r["year"]) - int(found_year)) <= 1
            res.update(found_title=found_title, similarity=round(sim, 3),
                       status="ok" if sim >= 0.85 and year_ok else "MISMATCH")
        elif r.get("url") and r.get("checked_by_human"):
            res["status"] = "ok_manual"
        elif r.get("url"):
            res["status"] = "needs_human_check"
        else:
            res["status"] = "NO_IDENTIFIER"
        bad += res["status"] not in ("ok", "ok_manual")
        out.append(res)
        print(f"{res['status']:18s} {r.get('key')}  {res.get('similarity') or ''}")
        time.sleep(0.5)
    (ROOT / "manuscript" / "citations_verified.json").write_text(json.dumps(out, indent=1, ensure_ascii=False),
                                                                 encoding="utf-8")
    print(f"{len(out) - bad}/{len(out)} trích dẫn đã kiểm chứng")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
