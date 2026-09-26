"""Atom-level fields derived BY CODE from a frozen atom (prereg §1.1, §4.2–4.3, §5.4, §5.6 B, §6.2–6.4; review of
the preregistration, review/prereg/response.md). Nothing here reads a model output; every function is a pure function
of the atom (and, where stated, of the MoH issue date or a frozen atom pool), so all of it is fixed before any run.

  atom_covariates(atom)      the per-atom columns the confirmatory code needs (k_foreign, has_decoy, us_unique, ...)
  family_key / family_id     mechanical conflict-family rule (the H1–H3 cluster unit)
  roundness / roundness_ok   decoy 'roundness' check (sensitivity S3)
  decoy_distance_ratio       distance of the decoy from the MoH set / that of the nearest conflicting foreign value
  answer_side                side of the MoH value an unattributed numeric answer falls on (sensitivity S1)
  neighbour_overlap          conflicting foreign value within 2·tolerance of an MoH value of a neighbouring context
  strict_tolerance           'exact match' tolerance (sensitivity B.18)
  moh_older_than_counterpart code surrogate for 'MoH lags evidence' when no clinician is available (DR12)
  foreign_direction          more / less aggressive than MoH, by the registered slot convention
  conflict_kind              'moh_differs' vs 'moh_silent' (drug / category atoms, by moh_scope)
  acuity_suggestion          registered high-acuity topic list (student confirms)
  regenerate_decoy           pre-specified regeneration of a decoy rated implausible (round -> borrow)
  freeze_problems            checks run before the atom freeze (python -m vnsoc.match.atom_flags check <atoms.jsonl>)

Values are value SETS as in vnsoc.grade. Items flagged derived=True (a value computed by the extractor rather than
read verbatim) are ignored by vnsoc.grade for status, tolerance and attribution; with_derived() restores them for the
registered sensitivity analysis.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import sys
from decimal import Decimal
from pathlib import Path

from vnsoc.grade import _gap, compute_tolerance, conflict_status
# roundness(x) and round_to(x, step): one definition in vnsoc.match.decoys, shared with the decoy rule
from vnsoc.match.decoys import below, check_decoy, in_atom_unit, num_item, roundness
from vnsoc.match.decoys import round_to as _round_to

FREEZE_DATE = "2026-10-15"                    # configs/project.yaml dates.corpus_freeze
# Slot convention for foreign_direction (registered, prereg §4.2): True = a higher value is more aggressive.
# threshold: depends on the MoH comparator (act above t: lower t is more aggressive; act below t: higher t is).
AGGRESSIVE_HIGHER = {"dose": True, "duration": True, "target": False}
HIGH_ACUITY = re.compile(r"sốc|shock|phản\s+vệ|anaphyla|sốt\s+rét\s+(?:nặng|ác\s+tính|biến\s+chứng)|severe\s+malaria|"
                         r"nhiễm\s+khuẩn\s+huyết|nhiễm\s+trùng\s+huyết|sepsis|septic", re.I)


# ------------------------------------------------------------------ helpers
def _items(recs) -> list[dict]:
    return [it for r in recs or [] for it in r["values"] if not it.get("derived")]


def with_derived(atom: dict) -> dict:
    """Copy of the atom in which derived values count like verbatim ones (sensitivity: keep derived values)."""
    a = dict(atom)
    for key in ("foreign", "superseded"):
        a[key] = [dict(r, values=[{k: v for k, v in it.items() if k != "derived"} for it in r["values"]])
                  for r in atom.get(key) or []]
    return a


def conflicting_items(atom: dict) -> list[tuple[list[str], dict]]:
    """Distinct conflicting foreign items (gap > 0 to every MoH item), identical items (gap 0) merged across systems,
    nearest to the MoH set first — the rule of vnsoc.qgen.mcq._conflicting, derived items excluded."""
    vn = atom.get("vn") or []
    out: list[tuple[list[str], dict]] = []
    for f in atom.get("foreign") or []:
        for it in f["values"]:
            if it.get("derived") or not all(_gap(v, it, atom) > 0 for v in vn):
                continue
            same = next((o for o in out if _gap(o[1], it, atom) == 0), None)
            if same:
                if f["system"] not in same[0]:
                    same[0].append(f["system"])
            else:
                out.append(([f["system"]], it))
    return sorted(out, key=lambda o: min(_gap(v, o[1], atom) for v in vn))


def k_foreign(atom: dict) -> int:
    """k_i: number of distinct conflicting foreign value items (prereg §4.3)."""
    return len(conflicting_items(atom))


def _distinguishable(a: dict, b: dict, atom: dict, tol: float) -> bool:
    """gap >= 2·tol (num/bp, tol > 0; binary noise at the boundary does not count, as in decoys.check_decoy),
    else gap > 0."""
    g = _gap(a, b, atom)
    return not below(g, 2 * tol) if atom["value_kind"] in ("num", "bp") and tol > 0 else g > 0


def us_unique(atom: dict) -> bool:
    """H2 set (prereg §4.3): a conflict atom with >= 1 conflicting US item, every one of which is distinguishable
    (gap >= 2·tolerance for num/bp, gap > 0 otherwise) from every non-US foreign item, every superseded item and the
    decoy."""
    if conflict_status(atom) != "conflict":
        return False
    tol = compute_tolerance(atom)
    vn = atom.get("vn") or []
    us = [it for f in atom.get("foreign") or [] if f["system"] == "US" for it in f["values"]
          if not it.get("derived") and all(_gap(v, it, atom) > 0 for v in vn)]
    others = [it for f in atom.get("foreign") or [] if f["system"] != "US" for it in f["values"]
              if not it.get("derived")]
    others += _items(atom.get("superseded")) + list(atom.get("decoy") or [])
    return bool(us) and all(_distinguishable(u, o, atom, tol) for u in us for o in others)


# ------------------------------------------------------------------ conflict family (cluster unit)
def _canon(it: dict, atom: dict) -> str:
    kind = atom["value_kind"]
    if kind == "num":
        n = in_atom_unit(it, atom)
        lo, hi = (n.lo, n.hi) if n is not None else (float(it["lo"]), float(it["hi"]))
        return f"{lo:.6g}-{hi:.6g}{it.get('cmp') or ''}"
    if kind == "bp":
        return f"{float(it['sys']):g}/{float(it['dia']):g}"
    if kind == "schedule":
        return ",".join(str(int(x)) for x in it["seq"]) + (it.get("unit") or "day")
    if kind == "drugs":
        return "+".join(sorted(it["key_drugs"]))
    return str(it["label"])


def family_key(atom: dict) -> str | None:
    """Mechanical conflict-family key (prereg §1.1): slot type x value kind x unit x the canonical MoH value set x the
    canonical nearest conflicting foreign item. Atoms sharing the key share one root discrepancy (the same MoH value
    against the same foreign value for the same kind of parameter), whatever their guideline or disease."""
    if conflict_status(atom) != "conflict":
        return None
    near = conflicting_items(atom)[0][1]
    vn = "|".join(sorted(_canon(v, atom) for v in atom["vn"]))
    return "::".join([atom["slot_type"], atom["value_kind"], atom.get("unit") or "", vn, _canon(near, atom)])


def family_id(atom: dict) -> str | None:
    k = family_key(atom)
    return None if k is None else "fam_" + hashlib.sha256(k.encode("utf-8")).hexdigest()[:10]


# ------------------------------------------------------------------ decoy audit
def item_roundness(it: dict, atom: dict) -> float | None:
    kind = atom["value_kind"]
    if kind == "num":
        n = in_atom_unit(it, atom)
        if n is None:
            return None
        return min(roundness(n.lo), roundness(n.hi))
    if kind == "bp":
        return min(roundness(it["sys"]), roundness(it["dia"]))
    return None


def roundness_ok(atom: dict) -> bool | None:
    """S3 stratum (prereg §5.6 B.7): roundness(decoy) >= roundness(nearest conflicting foreign item), num/bp only."""
    dec = list(atom.get("decoy") or [])
    conf = conflicting_items(atom)
    if atom["value_kind"] not in ("num", "bp") or not dec or not conf:
        return None
    rd, rf = item_roundness(dec[0], atom), item_roundness(conf[0][1], atom)
    return None if rd is None or rf is None else bool(rd >= rf)


def decoy_distance_ratio(atom: dict) -> float | None:
    """Distance of the decoy from the MoH set divided by that of the nearest conflicting foreign item (num/bp; 1.0 for
    an unrounded mirror_arith decoy, within decoys.BAND of it when rounded, 2.0 for mirror_far). Reported per atom so
    that a decoy farther from (or closer to) the MoH value than the foreign value is visible (review of the decoy
    rounding, 2026-09-26). None without a decoy or a conflicting item."""
    dec = list(atom.get("decoy") or [])
    conf = conflicting_items(atom)
    if atom["value_kind"] not in ("num", "bp") or not dec or not conf:
        return None
    gf = min(_gap(v, conf[0][1], atom) for v in atom["vn"])
    gd = min(_gap(v, dec[0], atom) for v in atom["vn"])
    return None if not (0 < gf < math.inf) or not math.isfinite(gd) else round(gd / gf, 6)


def _anchor(atom: dict):
    """(MoH item v, nearest conflicting foreign item f): the pair the decoy rule mirrors."""
    conf = [it for _, it in conflicting_items(atom)]
    if not conf:
        return None
    return min(((v, f) for f in conf for v in atom["vn"]), key=lambda p: _gap(p[0], p[1], atom))


def answer_side(val, atom: dict) -> str | None:
    """'foreign' | 'decoy' | None: side of the anchor MoH value v on which a parsed answer value falls, relative to the
    nearest conflicting foreign value f (projection on f - v; bp uses both components). None when undefined."""
    kind = atom["value_kind"]
    anc = _anchor(atom)
    if anc is None or kind not in ("num", "bp"):
        return None
    v, f = anc
    if kind == "num":
        vv, ff = in_atom_unit(v, atom), in_atom_unit(f, atom)
        if vv is None or ff is None:
            return None
        cv, cf = (vv.lo + vv.hi) / 2, (ff.lo + ff.hi) / 2
        x = (val.lo + val.hi) / 2
        dot = (x - cv) * (cf - cv)
    else:
        dot = (val.sys - v["sys"]) * (f["sys"] - v["sys"]) + (val.dia - v["dia"]) * (f["dia"] - v["dia"])
    return "foreign" if dot > 0 else ("decoy" if dot < 0 else None)


def response_side(output: str, atom: dict, lang: str = "vi", extracted: str | None = None) -> str | None:
    """answer_side of a response's single parsed value (None if the answer has 0 or several distinct values)."""
    from vnsoc.grade import _distinct, answer_span, parse_values

    span = extracted if extracted is not None else answer_span(output)[0]
    vals = _distinct(parse_values(span, atom, lang))
    return answer_side(vals[0][1], atom) if len(vals) == 1 else None


# ------------------------------------------------------------------ neighbouring MoH values, strict tolerance
def neighbour_items(atom: dict) -> list[dict]:
    return [it for nb in atom.get("moh_neighbour") or [] for it in nb.get("values") or []]


def neighbour_overlap(atom: dict) -> bool:
    """True if a conflicting foreign item lies within 2·tolerance (num/bp; gap 0 for other kinds) of an MoH value
    recorded for a neighbouring context (another step, population or level of care in the current corpus)."""
    nb = neighbour_items(atom)
    if not nb or conflict_status(atom) != "conflict":
        return False
    tol = compute_tolerance(atom)
    return any(not _distinguishable(o, x, atom, tol) for _, o in conflicting_items(atom) for x in nb)


def status_with_neighbours(atom: dict) -> str:
    """Conflict status if neighbour overlap made an atom 'indistinguishable' (option (b) of the clinician review;
    registered as a sensitivity analysis unless the authors adopt it as primary before submission)."""
    s = conflict_status(atom)
    return "indistinguishable" if s == "conflict" and neighbour_overlap(atom) else s


def strict_tolerance(atom: dict) -> float:
    """'Exact match' tolerance (prereg §5.6 B.18): half a unit of the last recorded decimal place of the MoH values
    (num: 0.5 for integers; bp: 0.5), never wider than the registered tolerance; 0 for other kinds."""
    kind = atom["value_kind"]
    reg = float(atom.get("tolerance") if atom.get("tolerance") is not None else compute_tolerance(atom))
    if kind == "bp":
        return min(0.5, reg) if reg > 0 else 0.0
    if kind != "num":
        return 0.0
    nd = 0
    for v in atom["vn"]:
        for x in (v["lo"], v["hi"]):
            e = Decimal(str(float(x))).normalize().as_tuple().exponent
            nd = max(nd, -e if isinstance(e, int) and e < 0 else 0)
    t = 0.5 * 10 ** (-nd)
    return min(t, reg) if reg > 0 else t


# ------------------------------------------------------------------ clinician-free surrogates (DR12)
def _date_key(s: str | None) -> tuple[int, int, int] | None:
    if not s:
        return None
    m = re.match(r"(\d{4})(?:-(\d{2}))?(?:-(\d{2}))?", str(s))
    if not m:
        return None
    return int(m.group(1)), int(m.group(2) or 1), int(m.group(3) or 1)


def moh_older_than_counterpart(atom: dict, moh_issued: str | None, sources: list[str] | None = None) -> bool | None:
    """Surrogate, not a clinical judgement (prereg §4.2): True if the foreign source version is dated after the MoH
    document's issue date. sources = matched 'source|version_date' strings of a response (GradeRecord.foreign_sources);
    without them, the atom's conflicting foreign records are used. Partial dates count from their first day."""
    mk = _date_key(moh_issued)
    if mk is None:
        return None
    if sources is not None:
        dates = [s.rsplit("|", 1)[-1] for s in sources]
    else:
        vn = atom.get("vn") or []
        dates = [f.get("version_date") for f in atom.get("foreign") or []
                 if any(not it.get("derived") and all(_gap(v, it, atom) > 0 for v in vn) for it in f["values"])]
    keys = [k for k in (_date_key(d) for d in dates) if k is not None]
    return None if not keys else any(k > mk for k in keys)


def foreign_direction(atom: dict) -> str | None:
    """'more_aggressive' | 'less_aggressive' | None: the nearest conflicting foreign value relative to the MoH value,
    by the registered slot convention (AGGRESSIVE_HIGHER; threshold by the MoH comparator; atom field
    aggressive_higher overrides, set at the context check). num uses interval centres, bp the systolic value."""
    kind, slot = atom["value_kind"], atom.get("slot_type")
    anc = _anchor(atom)
    if anc is None or kind not in ("num", "bp"):
        return None
    v, f = anc
    higher = atom.get("aggressive_higher")
    if higher is None:
        if slot == "threshold":
            cmp = v.get("cmp")
            higher = None if cmp is None else cmp in ("<", "<=")
        else:
            higher = AGGRESSIVE_HIGHER.get(slot)
    if higher is None:
        return None
    if kind == "num":
        vv, ff = in_atom_unit(v, atom), in_atom_unit(f, atom)
        if vv is None or ff is None:
            return None
        up = (ff.lo + ff.hi) / 2 > (vv.lo + vv.hi) / 2
    else:
        up = f["sys"] > v["sys"]
    return "more_aggressive" if up == bool(higher) else "less_aggressive"


def conflict_kind(atom: dict) -> str | None:
    """'moh_differs' | 'moh_silent' | 'unknown' for conflict atoms (prereg §5.6 A.1): num/bp/schedule values either
    are or are not the MoH value ('moh_differs'); for drug/category atoms a conflicting foreign option is 'moh_silent'
    unless the MoH text is exhaustive (moh_scope == 'exhaustive'); 'unknown' if moh_scope was not recorded."""
    if conflict_status(atom) != "conflict":
        return None
    if atom["value_kind"] in ("num", "bp", "schedule"):
        return "moh_differs"
    scope = atom.get("moh_scope")
    if scope is None:
        return "unknown"
    return "moh_differs" if scope == "exhaustive" else "moh_silent"


def acuity_suggestion(atom: dict) -> str:
    """'high' if the registered high-acuity topic list matches (shock, anaphylaxis, severe malaria, sepsis), else
    'not_high'. The student confirms and records Atom.acuity; harm weights are used only with a real clinician."""
    text = " ".join(str(atom.get(k) or "") for k in ("disease", "condition", "intervention"))
    text += " " + " ".join(str(v) for v in (atom.get("population") or {}).values())
    return "high" if HIGH_ACUITY.search(text) else "not_high"


# ------------------------------------------------------------------ decoy regeneration (implausible decoys)
def _dist_from_moh(it: dict, atom: dict) -> float:
    return min(_gap(v, it, atom) for v in atom["vn"])


def regenerate_decoy(atom: dict, pool: list[dict] | None = None) -> tuple[dict | None, str]:
    """Pre-specified regeneration for a decoy rated implausible at HG3.5 (prereg §6.4), before any output exists:
    (1) num/bp: round the current decoy to the granularity of the source values, g = min roundness of the MoH items
        and the nearest conflicting foreign item; accepted if check_decoy passes;
    (2) otherwise borrow a foreign value of another atom in `pool` with the same value kind, slot type and unit
        (protocol §4.2), choosing the candidate whose distance from the MoH set is closest to that of the nearest
        conflicting foreign value (ties: atom_id, record order); accepted if check_decoy passes.
    Returns (decoy item, rule) or (None, reason). The new decoy is rated again, blind to outputs."""
    kind = atom["value_kind"]
    dec = list(atom.get("decoy") or [])
    conf = conflicting_items(atom)
    if not conf:
        return None, "không có giá trị nước ngoài xung đột"
    if kind in ("num", "bp") and dec:
        steps = [item_roundness(v, atom) for v in atom["vn"]] + [item_roundness(conf[0][1], atom)]
        steps = [s for s in steps if s and math.isfinite(s)]
        if steps:
            g = min(steps)
            d0 = dec[0]
            n = in_atom_unit(d0, atom) if kind == "num" else None
            if kind == "num" and n is None:
                ok, cand = False, {}
            elif kind == "num":
                lo, hi = _round_to(n.lo, g), _round_to(n.hi, g)
                cand, ok = num_item(lo, hi, atom.get("unit")), lo > 0
            else:
                s, di = _round_to(d0["sys"], g), _round_to(d0["dia"], g)
                cand, ok = {"sys": s, "dia": di, "text": f"{s:g}/{di:g} mmHg"}, s > 0 and di > 0
            if ok and cand != {k: d0.get(k) for k in cand} and not check_decoy(dict(atom, decoy=[cand])):
                return cand, "rounded"
    target = _dist_from_moh(conf[0][1], atom)
    best = None
    for b in sorted(pool or [], key=lambda x: str(x.get("atom_id"))):
        if b.get("atom_id") == atom.get("atom_id") or b.get("value_kind") != kind or \
                b.get("slot_type") != atom.get("slot_type") or (b.get("unit") or None) != (atom.get("unit") or None):
            continue
        for j, it in enumerate(_items(b.get("foreign"))):
            cand = {k: v for k, v in it.items() if k != "derived"}
            if check_decoy(dict(atom, decoy=[cand])):
                continue
            score = (abs(_dist_from_moh(cand, atom) - target), str(b.get("atom_id")), j)
            if best is None or score < best[0]:
                best = (score, cand, b.get("atom_id"))
    if best is not None:
        return best[1], f"borrowed:{best[2]}"
    return None, "không tạo lại được mồi (làm tròn và mượn đều không đạt)"


# ------------------------------------------------------------------ analysis covariates and freeze checks
def distinct_version(atom: dict) -> bool:
    """Atom has a superseded value outside the MoH set (descriptive stubbornness index, together with conflict)."""
    vn = atom.get("vn") or []
    return any(all(_gap(v, it, atom) > 0 for v in vn) for it in _items(atom.get("superseded")))


def atom_covariates(atom: dict, moh_issued: str | None = None) -> dict:
    """Per-atom columns joined to every graded response of the atom by the analysis frame (prereg §4.2)."""
    st = conflict_status(atom)
    return {
        "atom_id": atom["atom_id"], "guideline": atom["guideline"], "conflict_status": st,
        "conflict_family": atom.get("conflict_family"), "k_foreign": k_foreign(atom),
        "has_decoy": bool(atom.get("decoy")), "us_unique": us_unique(atom), "value_kind": atom["value_kind"],
        "slot_type": atom.get("slot_type"), "decoy_rule": atom.get("decoy_rule"), "roundness_ok": roundness_ok(atom),
        "decoy_distance_ratio": decoy_distance_ratio(atom),
        "moh_neighbour_overlap": neighbour_overlap(atom), "distinct": st == "conflict" or distinct_version(atom),
        "has_superseded": bool(_items(atom.get("superseded"))), "pilot": bool(atom.get("pilot")),
        "seed_row": atom.get("seed_row"), "moh_older_than_counterpart": moh_older_than_counterpart(atom, moh_issued),
        "foreign_direction": foreign_direction(atom), "conflict_kind": conflict_kind(atom),
        "acuity": atom.get("acuity"), "moh_scope": atom.get("moh_scope"), "decoy_plausible": atom.get("decoy_plausible"),
    }


def freeze_problems(atoms: list[dict], freeze_date: str = FREEZE_DATE) -> tuple[list[str], dict]:
    """Checks run before the atom freeze (prereg §3.1 item 2, §5.4). Returns (problems, report). The freeze is refused
    while problems remain. The report (counts per decoy rule, decoy-less conflict atoms, derived values, neighbour
    overlaps, family x guideline cross-tabulation, decoy plausibility) goes into the freeze addendum."""
    probs: list[str] = []
    fk = _date_key(freeze_date)
    rules: dict[str, int] = {}
    roundings: dict[str, int] = {}
    fam_gl: dict[str, set] = {}
    n_no_decoy = n_derived = n_neigh = n_plaus = n_conf = 0
    for a in atoms:
        aid = a.get("atom_id")
        vf = _date_key(a.get("valid_from"))
        if vf is None:
            probs.append(f"{aid}: thiếu valid_from")
        elif vf > fk:
            probs.append(f"{aid}: valid_from {a.get('valid_from')} sau ngày đóng băng {freeze_date}")
        tol, st = compute_tolerance(a), conflict_status(a)
        if a.get("tolerance") is None or abs(float(a["tolerance"]) - tol) > 1e-9 or a.get("conflict_status") != st:
            probs.append(f"{aid}: tolerance/conflict_status khác kết quả tính lại bằng mã (gọi decoys.finalize)")
        n_derived += sum(1 for r in (a.get("foreign") or []) + (a.get("superseded") or [])
                         for it in r["values"] if it.get("derived"))
        if st != "conflict":
            continue
        n_conf += 1
        fid = family_id(a)
        if a.get("conflict_family") != fid:
            probs.append(f"{aid}: conflict_family {a.get('conflict_family')!r} ≠ quy tắc cơ học {fid}")
        fam_gl.setdefault(fid, set()).add(a.get("guideline"))
        if a.get("context_checked") != "pass":
            probs.append(f"{aid}: chưa qua kiểm ngữ cảnh (context_checked = {a.get('context_checked')})")
        if a.get("decoy"):
            rules[str(a.get("decoy_rule"))] = rules.get(str(a.get("decoy_rule")), 0) + 1
            rd = str((a.get("extraction") or {}).get("decoy_rounding"))
            roundings[rd] = roundings.get(rd, 0) + 1
            if not a.get("decoy_rule"):
                probs.append(f"{aid}: có mồi nhưng thiếu decoy_rule")
            if a["value_kind"] in ("num", "bp") and a.get("roundness_ok") != roundness_ok(a):
                probs.append(f"{aid}: roundness_ok khác kết quả tính bằng mã")
            if a.get("decoy_plausible") is None:
                probs.append(f"{aid}: chưa chấm decoy_plausible (HG3.5)")
            elif a.get("decoy_plausible"):
                n_plaus += 1
        else:
            n_no_decoy += 1
        if a["value_kind"] in ("drugs", "cat") and a.get("moh_scope") is None:
            probs.append(f"{aid}: thiếu moh_scope (mẩu thuốc/phân loại)")
        n_neigh += neighbour_overlap(a)
    report = {"n_atoms": len(atoms), "n_conflict": n_conf, "decoy_rules": rules, "decoy_roundings": roundings,
              "n_conflict_without_decoy": n_no_decoy,
              "n_derived_values": n_derived, "n_neighbour_overlap": n_neigh, "n_decoy_plausible": n_plaus,
              "n_families": len(fam_gl), "n_families_multi_guideline": sum(len(v) > 1 for v in fam_gl.values()),
              "family_x_guideline": {k: sorted(map(str, v)) for k, v in sorted(fam_gl.items(), key=lambda x: str(x[0]))}}
    return probs, report


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if len(argv) != 2 or argv[0] != "check":
        print("dùng: python -m vnsoc.match.atom_flags check <atoms.jsonl>")
        return 2
    atoms = [json.loads(x) for x in Path(argv[1]).read_text(encoding="utf-8").splitlines() if x.strip()]
    probs, rep = freeze_problems(atoms)
    print(json.dumps({k: v for k, v in rep.items() if k != "family_x_guideline"}, ensure_ascii=False))
    for p in probs[:60]:
        print("LỖI", p)
    print(f"{len(probs)} vấn đề" if probs else "OK: đủ điều kiện đóng băng mẩu")
    return 1 if probs else 0


if __name__ == "__main__":
    sys.exit(main())
