"""Merge per-topic pilot atoms (data/interim/pilot/<topic>.jsonl) into data/interim/pilot_atoms.jsonl (T1.1).

Every atom is re-finalised (tolerance + conflict_status recomputed by vnsoc.grade — never trusted from the topic
file), re-verified against its PDF (vnsoc.extract.verify_span) and schema-validated; failures are left out and
listed. Also writes the human checklist for HG1.2 (state/gates/HG1.2_checklist.md): one block per atom with the
PDF page to open, the verbatim span, the value set, population, and every foreign source (url + locator).

  $PY -m vnsoc.extract.pilot_merge
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from vnsoc.extract.verify_span import drug_tables, pdf_path, verify_atom
from vnsoc.match.decoys import check_decoy, finalize
from vnsoc.paths import paths
from vnsoc.schemas import Atom

CLINICIAN_ONLY = ("moh_lags_evidence", "clinical_harm", "clinician_confirmed")


def load_topics(d: Path) -> list[dict]:
    atoms = []
    for f in sorted(d.glob("*.jsonl")):
        atoms += [json.loads(x) for x in f.read_text(encoding="utf-8").splitlines() if x.strip()]
    return atoms


def check(atom: dict, syn, combos, root=None) -> list[str]:
    probs = []
    try:
        Atom.model_validate(atom)
    except Exception as e:  # noqa: BLE001
        probs.append(f"schema: {str(e)[:200]}")
    r = verify_atom(atom, root, syn, combos)
    if not r["ok"]:
        probs.append(f"verify_span: {r['reason']}")
    if not atom.get("pilot"):
        probs.append("pilot != true")
    if any(atom.get(k) is not None for k in CLINICIAN_ONLY):
        probs.append("có trường chỉ-bác-sĩ")
    for f in atom.get("foreign") or []:
        if not f.get("url") or not f.get("fetched_at"):
            probs.append(f"nguồn nước ngoài thiếu url/fetched_at: {f.get('source')}")
    probs += [f"mồi: {p}" for p in check_decoy(atom)]
    return probs


def _vals(items: list[dict]) -> str:
    return "; ".join(str(it.get("text") or {k: v for k, v in it.items() if v is not None}) for it in items) or "—"


def checklist(atoms: list[dict]) -> str:
    out = ["# HG1.2 — Kiểm tay trích dẫn các mẩu thí điểm", "",
           "Với từng mẩu: mở PDF ở đúng **trang PDF** (số trang trong trình xem PDF, đếm từ 1) và xác nhận:",
           "(a) đoạn trích đúng nguyên văn; (b) giá trị và đơn vị đúng; (c) quần thể/bối cảnh đúng (người lớn/trẻ em, "
           "đo tại phòng khám, 3 tháng đầu thai kỳ...); (d) giá trị nước ngoài khớp trang nguồn (mở link, tìm theo vị trí).",
           "", "Khi xong, gõ trong chat: `XONG HG1.2 không có lỗi` hoặc `XONG HG1.2 sai: <mã mẩu và lỗi>`.", ""]
    for a in atoms:
        pdf = pdf_path(a["guideline"]).name
        out += [f"## {a['atom_id']} — {a['disease']}: {a['intervention']} ({a['conflict_status']})", "",
                f"- Văn bản: `{a['guideline']}` → `data/raw/{pdf}`, **trang PDF {a['page']}**"
                + (f" (trang in {a['extraction'].get('printed_page')})" if (a.get("extraction") or {}).get("printed_page") else "")
                + f", mục {a['section']}",
                f"- Quần thể: {json.dumps(a['population'], ensure_ascii=False)}",
                f"- Giá trị Bộ Y tế: **{_vals(a['vn'])}**",
                f"- Đoạn trích: «{a['span']}»"]
        for f in a.get("foreign") or []:
            out.append(f"- {f['system']} — {f['source']} ({f['version_date']}): **{_vals(f['values'])}** · "
                       f"vị trí: {f.get('locator') or '—'} · {f.get('url')}"
                       + ("" if f.get("page_sha256") else " · ⚠ chưa băm được trang (cần mở kiểm)"))
        for s in a.get("superseded") or []:
            out.append(f"- Bản cũ {s['guideline']} (trang PDF {s.get('page')}, mục {s.get('section')}): **{_vals(s['values'])}**")
        if a.get("decoy"):
            out.append(f"- Giá trị mồi (quy tắc {(a.get('extraction') or {}).get('decoy_rule', '—')}): {_vals(a['decoy'])}")
        out += ["- [ ] (a) nguyên văn  - [ ] (b) giá trị/đơn vị  - [ ] (c) quần thể  - [ ] (d) nguồn nước ngoài", ""]
    return "\n".join(out) + "\n"


def main(argv=None) -> int:
    P = paths()
    syn, combos = drug_tables()
    atoms = [finalize(a) for a in load_topics(P.root / "data" / "interim" / "pilot")]
    seen, keep, bad = set(), [], []
    for a in atoms:
        probs = check(a, syn, combos)
        if a["atom_id"] in seen:
            probs.append("atom_id trùng")
        seen.add(a["atom_id"])
        (bad if probs else keep).append((a, probs))
    out = P.root / "data" / "interim" / "pilot_atoms.jsonl"
    out.write_text("".join(json.dumps(a, ensure_ascii=False) + "\n" for a, _ in keep), encoding="utf-8")
    (P.state / "gates").mkdir(parents=True, exist_ok=True)
    (P.state / "gates" / "HG1.2_checklist.md").write_text(checklist([a for a, _ in keep]), encoding="utf-8")
    rej = P.root / "data" / "interim" / "pilot_merge_rejects.jsonl"
    rej.write_text("".join(json.dumps({"atom_id": a.get("atom_id"), "problems": p}, ensure_ascii=False) + "\n"
                           for a, p in bad), encoding="utf-8")
    by = {}
    for a, _ in keep:
        by[a["conflict_status"]] = by.get(a["conflict_status"], 0) + 1
    print(f"giữ {len(keep)} mẩu {by}; loại {len(bad)} (xem {rej.name})")
    for a, p in bad:
        print(f"  LOẠI {a.get('atom_id')}: {'; '.join(p)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
