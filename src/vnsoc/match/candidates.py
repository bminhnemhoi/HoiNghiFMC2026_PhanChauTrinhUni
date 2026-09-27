"""Candidate foreign counterparts for main-study atoms (T3.3, step 1 — code only; an agent confirms each pair).

For every atom, the ForeignRecords of the same disease group (configs/foreign_groups.yaml) are scored:
  * hard filters: same value kind; for num the record's unit converts to the atom's unit (atom context, e.g. weight);
    for drugs at least one shared INN; for cat at least one label of the atom's cat_options;
  * score: word overlap between the atom's condition/intervention/population text and the record's topic (Vietnamese
    folded, stop words removed), plus a bonus for shared drugs.
The top candidates (score >= MIN_SCORE, at most K per atom) are written for the matching agents to accept or reject;
nothing is attached to an atom here. Matching sensitivity is measured afterwards on the pilot's recorded pairs.

  $PY -m vnsoc.match.candidates                     # -> data/interim/match_candidates.jsonl
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata

import yaml

from vnsoc.paths import paths

K = 5
MIN_SCORE = 0.15
STOP = set("và hoặc của cho có không là với trong theo các những một người bệnh nhân mỗi lần ngày liều khi từ đến "
           "the of and or for in with to a an per dose patients patient adults adult".split())


def fold(s: str) -> str:
    s = unicodedata.normalize("NFD", (s or "").lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn").replace("đ", "d")
    return re.sub(r"[^a-z0-9 ]+", " ", s)


def tokens(s: str) -> set[str]:
    return {w for w in fold(s).split() if len(w) > 1 and w not in STOP}


def atom_text(a: dict) -> str:
    pop = " ".join(str(v) for v in (a.get("population") or {}).values())
    return " ".join([a.get("condition") or "", a.get("intervention") or "", a.get("disease") or "", pop])


def compatible(atom: dict, rec: dict) -> bool:
    kind = atom.get("value_kind")
    items = rec.get("values") or []
    if not items:
        return False
    if kind == "num":
        from vnsoc import normalize_vi as nv

        for it in items:
            if it.get("lo") is None:
                return False
            if nv.Num(float(it["lo"]), float(it["hi"]), it.get("unit") or atom.get("unit")).to(
                    atom.get("unit"), atom.get("context") or {}) is None:
                return False
        return True
    if kind == "bp":
        return all(it.get("sys") is not None for it in items)
    if kind == "schedule":
        return all(it.get("seq") for it in items)
    if kind == "drugs":
        return all(it.get("key_drugs") for it in items)   # a different first-line regimen is exactly a conflict
    if kind == "cat":
        labels = set((atom.get("cat_options") or {}).keys())
        return any(it.get("label") in labels for it in items)
    return False


def score(atom: dict, rec: dict) -> float:
    a, r = tokens(atom_text(atom)), tokens(rec.get("topic") or "")
    if not a or not r:
        return 0.0
    s = len(a & r) / min(len(a), len(r))
    if atom.get("value_kind") == "drugs":
        mine = {d for it in atom.get("vn") or [] for d in it.get("key_drugs") or []}
        theirs = {d for it in rec.get("values") or [] for d in it.get("key_drugs") or []}
        s += 0.3 * bool(mine & theirs)
    return round(s, 4)


def group_of(root=None) -> dict[str, str]:
    cfg = yaml.safe_load((paths(root).configs / "foreign_groups.yaml").read_text(encoding="utf-8"))
    return {doc: g for g, docs in cfg["groups"].items() for doc in docs}


def candidates(atoms: list[dict], records: dict[str, list[dict]], groups: dict[str, str],
               k: int = K, min_score: float = MIN_SCORE) -> list[dict]:
    out = []
    for a in atoms:
        g = groups.get(a["guideline"])
        pool = records.get(g, []) if g else []
        scored = sorted(((score(a, r), r["record_id"]) for r in pool if compatible(a, r)), reverse=True)
        top = [{"record_id": rid, "score": s} for s, rid in scored if s >= min_score][:k]
        if top:
            out.append({"atom_id": a["atom_id"], "group": g, "candidates": top})
    return out


def main(argv=None) -> int:
    from vnsoc.extract.atoms_merge import load_parts

    P = paths()
    atoms = load_parts(P.root / "data" / "interim" / "atoms_parts")
    recs: dict[str, list[dict]] = {}
    for f in sorted((P.root / "data" / "interim" / "foreign_parts").glob("*.jsonl")):
        recs[f.stem] = [json.loads(x) for x in f.read_text(encoding="utf-8").splitlines() if x.strip()]
    rows = candidates(atoms, recs, group_of())
    out = P.root / "data" / "interim" / "match_candidates.jsonl"
    out.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    print(f"{len(atoms)} mẩu; {len(rows)} mẩu có ứng viên; {sum(len(r['candidates']) for r in rows)} cặp -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
