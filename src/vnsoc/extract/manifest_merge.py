"""Merge the corpus-triage parts (data/interim/manifest_parts/*.jsonl) into data/interim/manifest.jsonl (T2.1/T2.2).

One row per doc_key: the row with the most evidence (official URL, sha256, pages) is the base; list fields are
unioned; notes are concatenated; disagreeing statuses between agents are flagged in notes (a person decides) and the
status of the LATEST part (part files are read in name order c1_, c2_, … so a later review — e.g. the supersession
check that read the repeal clause of a newer document — wins) is kept until that person decides.
Also writes results/tables/corpus_triage.csv (official PDF? text layer? scanned? only on a private legal site?) and
state/gates/HG2.3_missing.md (documents without an official PDF, scanned-only documents, where agents searched).

  $PY -m vnsoc.extract.manifest_merge
"""
from __future__ import annotations

import csv
import json
import sys

from vnsoc.paths import paths
from vnsoc.schemas import ManifestRow

LISTS = ("supersedes", "superseded_by", "partially_amended_by")
PRIVATE_SITE = "thư viện pháp luật tư nhân"


def _score(r: dict) -> int:
    return sum(bool(r.get(k)) for k in ("source_url", "sha256", "pages", "issued", "title")) + (r.get("text_layer") is True)


def merge_rows(rows: list[dict]) -> list[dict]:
    by: dict[str, list[dict]] = {}
    for r in rows:
        by.setdefault(r["doc_key"].replace(" ", ""), []).append(r)
    out = []
    for key, rs in sorted(by.items()):
        rs = sorted(rs, key=_score, reverse=True)
        base = dict(rs[0], doc_key=key)
        for k in LISTS:
            base[k] = sorted({x for r in rs for x in r.get(k) or []})
        # latest part's note first, so the 4000-character cut never drops the most recent review or the flag
        notes = [n for r in reversed(by[key]) for n in [r.get("notes") or ""] if n]
        statuses = sorted({r["status"] for r in rs})
        if len(statuses) > 1:
            latest = by[key][-1]["status"]                  # input order = part order; later review wins
            base["status"] = latest
            notes.insert(0, f"MÂU THUẪN trạng thái giữa các agent: {statuses} — tạm lấy '{latest}' của phần sau "
                            "cùng; cần người quyết")
        base["notes"] = " | ".join(dict.fromkeys(notes))[:4000]
        base["in_corpus"] = any(r.get("in_corpus") for r in rs)
        base["ocr"] = any(r.get("ocr") for r in rs)         # values read from OCR in any review → counts to the cap
        out.append(ManifestRow.model_validate(base).model_dump())
    return out


def triage(rows: list[dict]) -> list[dict]:
    t = []
    for r in rows:
        t.append({"doc_key": r["doc_key"], "kind": r["kind"], "disease": r["disease"], "status": r["status"],
                  "issued": r.get("issued") or "", "official_pdf": bool(r.get("source_url")),
                  "host": r.get("source_host") or "", "text_layer": r.get("text_layer"),
                  "scanned": r.get("text_layer") is False, "pages": r.get("pages") or "",
                  "only_private_site": PRIVATE_SITE in (r.get("notes") or "") and not r.get("source_url"),
                  "supersedes": ";".join(r["supersedes"]), "superseded_by": ";".join(r["superseded_by"]),
                  "title": r["title"][:160]})
    return t


def missing_md(rows: list[dict]) -> str:
    miss = [r for r in rows if not r.get("source_url")]
    scan = [r for r in rows if r.get("source_url") and r.get("text_layer") is False]
    out = ["# HG2.3 — Văn bản cần bạn tìm tay (bản PDF chính thức)", "",
           "Với từng văn bản: tìm bản PDF CHÍNH THỨC (kcb.vn, moh.gov.vn, trang Sở Y tế/bệnh viện đăng lại nguyên "
           "quyết định, thư viện trường). Được TRA số hiệu/ngày trên trang thư viện pháp luật tư nhân, nhưng KHÔNG dùng "
           "file từ đó. Lưu PDF vào data/raw/manual/<số>_<năm>.pdf và ghi URL nguồn cạnh tên văn bản dưới đây.",
           "Khi xong gõ: `XONG HG2.3 tìm được <n>/<tổng>`.", "", f"## A. Chưa có PDF chính thức ({len(miss)})", ""]
    for r in miss:
        out.append(f"- **{r['doc_key']}** — {r['title'][:120]} ({r['disease']}; {r['status']}). Đã tìm: "
                   f"{(r.get('notes') or '—')[:400]}")
    out += ["", f"## B. Chỉ có bản quét không lớp chữ ({len(scan)}) — cần bản có lớp chữ hoặc OCR (tối đa 10 văn bản)", ""]
    for r in scan:
        out.append(f"- **{r['doc_key']}** — {r['title'][:120]} · {r.get('source_url')}")
    out += ["", "## C. Nguồn nước ngoài cần đăng ký/bị chặn (tải thủ công vào data/raw/manual_foreign/, chỉ dùng nội bộ)",
            "", "- GINA, GOLD (cần đăng ký); EAACI 2021 (403); CDC (403 với công cụ — mở bằng trình duyệt để kiểm).", ""]
    return "\n".join(out) + "\n"


def main(argv=None) -> int:
    P = paths()
    parts = sorted((P.root / "data" / "interim" / "manifest_parts").glob("*.jsonl"))
    rows = [json.loads(x) for f in parts for x in f.read_text(encoding="utf-8").splitlines() if x.strip()]
    merged = merge_rows(rows)
    (P.root / "data" / "interim" / "manifest.jsonl").write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in merged), encoding="utf-8")
    tri = triage(merged)
    out = P.results / "tables" / "corpus_triage.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(tri[0]) if tri else ["doc_key"])
        w.writeheader()
        w.writerows(tri)
    (P.state / "gates").mkdir(parents=True, exist_ok=True)
    extra = P.state / "gates" / "HG2.3_extra.md"          # hand-written items (agent findings), kept across re-merges
    (P.state / "gates" / "HG2.3_missing.md").write_text(
        missing_md(merged) + ("\n" + extra.read_text(encoding="utf-8") if extra.exists() else ""), encoding="utf-8")
    n_off = sum(t["official_pdf"] for t in tri)
    n_txt = sum(bool(t["text_layer"]) for t in tri)
    cur = sum(r["status"] == "current" for r in merged)
    print(f"{len(rows)} dòng từ {len(parts)} phần → {len(merged)} văn bản ({cur} hiện hành); PDF chính thức {n_off}; "
          f"có lớp chữ {n_txt}; thiếu {len(merged) - n_off}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
