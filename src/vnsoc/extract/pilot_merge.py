"""Merge per-topic pilot atoms (data/interim/pilot/<topic>.jsonl) into data/interim/pilot_atoms.jsonl (T1.1).

Every atom is re-finalised (tolerance + conflict_status recomputed by vnsoc.grade — never trusted from the topic
file), re-verified against its PDF (vnsoc.extract.verify_span) and schema-validated; failures are left out and
listed. Also writes the human checklist for HG1.2 (state/gates/HG1.2_checklist.md): one block per atom with the
PDF page to open, the verbatim span, the value set, population, and every foreign source (url + locator).

  $PY -m vnsoc.extract.pilot_merge                                   # all topics -> pilot_atoms.jsonl + checklist
  $PY -m vnsoc.extract.pilot_merge --only dm --out <tmp>/dm.jsonl    # one topic, dry check: no shared file written

Options (none = the shared merge above): --only <topic> loads only data/interim/pilot/<topic>.jsonl and requires
--out; --out <path> writes the atoms there and the rejects next to them (<stem>_rejects.jsonl); --no-checklist
writes neither the HG1.2 checklist, the default rejects file nor data/interim/pdf_choice.json. --only implies
--no-checklist (a one-topic checklist would overwrite the shared one).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from vnsoc.extract.verify_span import drug_tables, pdf_path, verify_atom
from vnsoc.match.decoys import _conflicting, check_decoy, choose_decoy_detail, finalize
from vnsoc.paths import paths
from vnsoc.schemas import Atom

CLINICIAN_ONLY = ("moh_lags_evidence", "clinical_harm", "clinician_confirmed")


def load_topics(d: Path, only: str | None = None) -> list[dict]:
    """Atoms of every data/interim/pilot/<topic>.jsonl, or of the one topic `only`."""
    files = sorted(d.glob("*.jsonl")) if only is None else [d / f"{only}.jsonl"]
    atoms = []
    for f in files:
        if not f.exists():
            raise SystemExit(f"không có tệp chủ đề {f}")
        atoms += [json.loads(x) for x in f.read_text(encoding="utf-8").splitlines() if x.strip()]
    return atoms


def source_warnings(atom: dict, blocks: set[str], root=None) -> list[str]:
    """Code-level evidence check of foreign values: hash must not be an anti-bot page; the recorded numbers / drug
    names should occur in the cached source text (a warning, not a rejection: a value may be derived, e.g. mg/kg
    times the weight in context)."""
    from vnsoc.match.sources import cached_text, fold

    warns = []
    for f in atom.get("foreign") or []:
        sha = f.get("page_sha256")
        if not sha:
            warns.append(f"{f['source']}: không có page_sha256 (cần người mở kiểm)")
            continue
        if sha in blocks:
            warns.append(f"{f['source']}: page_sha256 là trang chặn/trung gian, không phải tài liệu")
            continue
        text = cached_text(sha, root)
        if text is None:
            warns.append(f"{f['source']}: không có bản đệm với sha {sha[:12]}")
            continue
        t = fold(text)
        for it in f["values"]:
            toks = []
            if it.get("lo") is not None:
                toks += [f"{it['lo']:g}", f"{it['hi']:g}"]
            if it.get("sys") is not None:
                toks += [f"{it['sys']:g}/{it['dia']:g}"]
            if it.get("seq"):
                toks += [str(s) for s in it["seq"]]
            if it.get("key_drugs"):
                toks += [p for d in it["key_drugs"] for p in d.replace("+", "-").split("-") if len(p) > 3]
            def variants(x: str) -> set[str]:
                v = {fold(x), fold(x).replace(".", ",")}
                if x.isdigit() and len(x) >= 4:               # 20000 -> 20,000 / 20.000 / 20 000
                    g = f"{int(x):,}"
                    v |= {g, g.replace(",", "."), g.replace(",", " ")}
                if "/" in x:                                    # 140/90 -> 140 / 90
                    v.add(fold(x.replace("/", " / ")))
                return v
            missing = [x for x in dict.fromkeys(toks) if not any(s in t for s in variants(x))]
            if missing:
                warns.append(f"{f['source']}: không thấy {missing} trong nguồn đã băm")
    return warns


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


def canonical_keys(atoms: list[dict], root=None, write: bool = True) -> list[dict]:
    """'5904/2019__9e6bbe13' (a second official copy saved by fetch_pdf) -> guideline '5904/2019', and the copy is
    recorded as the chosen PDF in data/interim/pdf_choice.json (one choice per document, else the atoms conflict).
    write=False (dry checks) leaves pdf_choice.json untouched."""
    import re

    f = paths(root).root / "data" / "interim" / "pdf_choice.json"
    choice = json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}
    out = []
    for a in atoms:
        m = re.fullmatch(r"(.+)__([0-9a-f]{8})", a["guideline"])
        if m:
            key, file = m.group(1), a["guideline"].replace("/", "_") + ".pdf"
            prev = choice.get(key, {}).get("file")
            if prev and prev != file:
                raise SystemExit(f"{key}: hai lựa chọn PDF khác nhau ({prev} / {file})")
            choice[key] = {"file": file, "reason": "bản chính thức thứ hai có lớp chữ, do agent thí điểm chọn "
                                                   f"({a['atom_id']}); cần người xác nhận nguồn ở HG1.2/HG2.3"}
            a = dict(a, guideline=key)
        out.append(a)
    if choice and write:
        f.write_text(json.dumps(choice, ensure_ascii=False, indent=1), encoding="utf-8")
    return out


def enforce_decoy_rule(atom: dict) -> dict:
    """num/bp atoms: the decoy is whatever the fixed rule gives (vnsoc.match.decoys.choose_decoy_detail); a stored
    decoy that differs is replaced and the change noted in extraction.decoy_rule. Atom.decoy_rule is the rule name
    only (mirror_arith | mirror_geom | mirror_far: the registered S2 set is decoy_rule == "mirror_arith"); the rounding
    goes to extraction.decoy_rounding (none | step <s> | raw). Where the rule applies (a conflicting foreign value
    exists) but gives no valid decoy, the atom is kept with decoy [] and a hand-set decoy is never kept
    (DECISIONS 2026-09-26; prereg: excluded from H1/H2, counted, descriptive only); so is a hand-set decoy that fails
    check_decoy. Atom.decoy_rule and Atom.roundness_ok are (re)computed by code."""
    from vnsoc.match.atom_flags import roundness_ok

    if atom.get("value_kind") not in ("num", "bp"):
        return atom
    d, rule, rounding = choose_decoy_detail(atom)
    a = dict(atom)
    ex = dict(atom.get("extraction") or {})
    ex.pop("decoy_rounding", None)
    if d is None:
        if _conflicting(atom) or (atom.get("decoy") and check_decoy(atom)):
            a["extraction"] = dict(ex, decoy_rule=f"none — {rule}")
            a["decoy"], a["decoy_rule"] = [], None
    else:
        old = list(atom.get("decoy") or [])
        a["decoy"], a["decoy_rule"] = [d], rule
        a["extraction"] = dict(ex, decoy_rule=rule + ("" if old == [d] else " (đặt lại khi gộp)"),
                               decoy_rounding=rounding)
    a["roundness_ok"] = roundness_ok(a)
    return a


def _vals(items: list[dict]) -> str:
    return "; ".join(str(it.get("text") or {k: v for k, v in it.items() if v is not None}) for it in items) or "—"


def checklist(atoms: list[dict], warns: dict[str, list[str]] | None = None) -> str:
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
            ex = a.get("extraction") or {}
            out.append(f"- Giá trị mồi (quy tắc {ex.get('decoy_rule', '—')}, làm tròn {ex.get('decoy_rounding', '—')}): "
                       f"{_vals(a['decoy'])}")
        for w in (warns or {}).get(a["atom_id"], []):
            out.append(f"- ⚠ Kiểm bằng mã: {w}")
        out += ["- [ ] (a) nguyên văn  - [ ] (b) giá trị/đơn vị  - [ ] (c) quần thể  - [ ] (d) nguồn nước ngoài", ""]
    return "\n".join(out) + "\n"


def parse_args(argv=None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(prog="python -m vnsoc.extract.pilot_merge",
                                 description="Gộp mẩu thí điểm theo chủ đề thành data/interim/pilot_atoms.jsonl (T1.1).")
    ap.add_argument("--only", metavar="TOPIC", help="chỉ nạp data/interim/pilot/<TOPIC>.jsonl (cần --out)")
    ap.add_argument("--out", metavar="PATH",
                    help="ghi mẩu ra PATH (loại ghi ra <stem>_rejects.jsonl cạnh PATH) thay vì pilot_atoms.jsonl")
    ap.add_argument("--no-checklist", action="store_true",
                    help="không ghi state/gates/HG1.2_checklist.md, rejects mặc định, data/interim/pdf_choice.json")
    args = ap.parse_args(argv)
    if args.only and not args.out:
        ap.error("--only cần --out (không ghi đè pilot_atoms.jsonl bằng một chủ đề)")
    return args


def main(argv=None) -> int:
    args = parse_args(argv)
    shared = not (args.no_checklist or args.only)        # write the shared checklist / rejects / pdf_choice.json
    P = paths()
    from vnsoc.match.sources import block_hashes

    syn, combos = drug_tables()
    blocks = block_hashes()
    topics = load_topics(P.root / "data" / "interim" / "pilot", args.only)
    atoms = [finalize(enforce_decoy_rule(a)) for a in canonical_keys(topics, write=shared)]
    import yaml

    ex_f = P.root / "data" / "interim" / "pilot_exclusions.yaml"      # deliberate, reasoned exclusions (duplicates...)
    excl = (yaml.safe_load(ex_f.read_text(encoding="utf-8")) or {}).get("exclude", {}) if ex_f.exists() else {}
    seen, keep, bad = set(), [], []
    for a in atoms:
        if a["atom_id"] in excl:
            bad.append((a, [f"loại có chủ đích: {excl[a['atom_id']]}"]))
            continue
        probs = check(a, syn, combos)
        if a["atom_id"] in seen:
            probs.append("atom_id trùng")
        seen.add(a["atom_id"])
        (bad if probs else keep).append((a, probs))
    for a, _ in keep:                                   # OCR pages: every number must be checked against the image
        if verify_atom(a, None, syn, combos).get("ocr"):
            a["extraction"] = dict(a.get("extraction") or {}, ocr=True)
    out = Path(args.out) if args.out else P.root / "data" / "interim" / "pilot_atoms.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("".join(json.dumps(a, ensure_ascii=False) + "\n" for a, _ in keep), encoding="utf-8")
    warns = {a["atom_id"]: (["trang OCR — so TỪNG con số với ảnh trang PDF (§3.1)"]
                            if (a.get("extraction") or {}).get("ocr") else []) + source_warnings(a, blocks)
             for a, _ in keep}
    if shared:
        (P.state / "gates").mkdir(parents=True, exist_ok=True)
        (P.state / "gates" / "HG1.2_checklist.md").write_text(checklist([a for a, _ in keep], warns), encoding="utf-8")
    if args.out:
        rej = out.with_name(out.stem + "_rejects.jsonl")
    else:
        rej = P.root / "data" / "interim" / "pilot_merge_rejects.jsonl" if shared else None
    if rej is not None:
        rej.write_text("".join(json.dumps({"atom_id": a.get("atom_id"), "problems": p}, ensure_ascii=False) + "\n"
                               for a, p in bad), encoding="utf-8")
    by = {}
    for a, _ in keep:
        by[a["conflict_status"]] = by.get(a["conflict_status"], 0) + 1
    print(f"giữ {len(keep)} mẩu {by} -> {out}; loại {len(bad)}" + (f" (xem {rej.name})" if rej is not None else ""))
    for a, p in bad:
        print(f"  LOẠI {a.get('atom_id')}: {'; '.join(p)}")
    for aid, w in warns.items():
        for x in w:
            print(f"  CẢNH BÁO {aid}: {x}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
