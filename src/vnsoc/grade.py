"""Rule-based grading (pre-registered, section 4.5 of the proposal). One label per answer:

  1 correct_aware  MoH value AND explicitly flags the foreign difference (or asks which country)
  2 correct        answer contained in the current MoH value set
  3 temporal       matches a superseded MoH version
  4 foreign        matches a named foreign system (US, EU_UK, WHO_global, WHO_WPRO)
  5 unattributed   a value that matches no known source (decoy matches land here, flagged)
  6 abstain        no value given

Atoms are dicts (see schemas.Atom). Value items by kind:
  num      {"lo": 15, "hi": 15, "unit": "ml/kg/h", "cmp": null}
  bp       {"sys": 140, "dia": 90}
  schedule {"seq": [0, 3, 7, 14, 28], "unit": "day"}
  drugs    {"key_drugs": ["artemether-lumefantrine"]}
  cat      {"label": "one_step"}
"""
from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field

from vnsoc import normalize_vi as nv

LABELS = {1: "correct_aware", 2: "correct", 3: "temporal", 4: "foreign", 5: "unattributed", 6: "abstain"}
ANS_LINE = re.compile(r"(?:ĐÁP\s*ÁN|Đáp\s*án|DAP\s*AN|ANSWER|Final\s+answer)\s*\**\s*[:：]\s*\**\s*(.+)", re.I)
THINK = re.compile(r"<think>.*?</think>", re.S | re.I)
ABSTAIN = re.compile(r"không\s+(?:rõ|chắc|biết|thể\s+xác\s+định|có\s+(?:đủ\s+)?(?:thông\s+tin|dữ\s+liệu))|"
                     r"tôi\s+không\s+thể|không\s+đủ\s+thông\s+tin|i\s+(?:do\s+not|don't)\s+know|"
                     r"cannot\s+(?:determine|answer|provide)|unable\s+to|not\s+sure|insufficient\s+information", re.I)
ASK_COUNTRY = re.compile(r"quốc\s+gia\s+nào|nước\s+nào|hướng\s+dẫn\s+(?:của\s+)?(?:nước|quốc\s+gia)\s+nào|"
                         r"which\s+(?:country|guideline|jurisdiction)", re.I)
CONTRAST = re.compile(r"khác\s+(?:với)?|trong\s+khi|còn\s+theo|ngược\s+lại|whereas|while|differ|in\s+contrast|"
                      r"unlike|however", re.I)
FOREIGN_NAMES = re.compile(r"\b(?:WHO|ADA|AHA|ACC|ESC|ESH|CDC|AASLD|EASL|RCUK|NICE|ACOG|GINA|GOLD|WAO|EAACI|"
                           r"IDSA|Mỹ|Hoa\s+Kỳ|châu\s+Âu|quốc\s+tế|US|USA|American|European|international)\b", re.I)
VN_MARK = re.compile(r"bộ\s+y\s+tế|việt\s+nam|\bBYT\b|\bMoH\b|Vietnam", re.I)


@dataclass
class Grade:
    label: int | None
    label_name: str | None
    vn_match: bool = False
    foreign_systems: list = field(default_factory=list)
    superseded: list = field(default_factory=list)
    decoy_match: bool = False
    parse_method: str = "none"      # answer_line | fallback | llm | none
    multi: bool = False
    partial: bool = False
    unit_assumed: bool = False
    needs_llm: bool = False
    answer_text: str = ""
    parsed: list = field(default_factory=list)

    def as_dict(self) -> dict:
        return asdict(self)


# ------------------------------------------------------------------------------ extraction
def answer_span(output: str) -> tuple[str, str]:
    text = THINK.sub(" ", output or "").strip()
    hits = ANS_LINE.findall(text)
    if hits:
        return hits[-1].strip().strip("*").strip(), "answer_line"
    return text, "fallback"


def parse_values(text: str, atom: dict, lang: str, synonyms=None, combos=None) -> list:
    kind = atom["value_kind"]
    if kind == "num":
        unit, ctx = atom.get("unit"), atom.get("context") or {}
        vals = []
        for n in nv.parse_nums(text, lang):
            if n.unit is None:
                vals.append(("assumed", nv.Num(n.lo, n.hi, unit, n.cmp)))
            elif n.to(unit, ctx) is not None:
                vals.append(("ok", n.to(unit, ctx)))
        return vals
    if kind == "bp":
        return [("ok", b) for b in nv.parse_bps(text)]
    if kind == "schedule":
        return [("ok", s) for s in nv.parse_schedules(text, min_len=int(atom.get("min_schedule_len", 2)))]
    if kind == "drugs":
        d = nv.parse_drugs(text, synonyms or {}, combos or {})
        return [("ok", d)] if d.names else []
    if kind == "cat":
        c = nv.parse_cats(text, atom.get("cat_options") or {})
        return [("ok", c)] if c.labels else []
    raise ValueError(f"value_kind lạ: {kind}")


# ------------------------------------------------------------------------------ matching
def _within(x: float, lo: float, hi: float, tol: float) -> bool:
    return (lo <= x <= hi) or (lo - tol < x < hi + tol)


def matches(val, item: dict, atom: dict) -> tuple[bool, bool]:
    """(contained, partial_overlap) of one parsed answer value in one reference value item."""
    kind, tol = atom["value_kind"], float(atom.get("tolerance") or 0.0)
    if kind == "num":
        ref = nv.Num(float(item["lo"]), float(item["hi"]), item.get("unit") or atom.get("unit"))
        ref = ref.to(atom.get("unit"), atom.get("context") or {}) or ref
        inside = _within(val.lo, ref.lo, ref.hi, tol) and _within(val.hi, ref.lo, ref.hi, tol)
        overlap = not (val.hi < ref.lo - tol or val.lo > ref.hi + tol)
        return inside, (overlap and not inside)
    if kind == "bp":
        ok = _within(val.sys, item["sys"], item["sys"], tol) and _within(val.dia, item["dia"], item["dia"], tol)
        return ok, False
    if kind == "schedule":
        return tuple(val.seq) == tuple(item["seq"]) and val.unit == item.get("unit", "day"), False
    if kind == "drugs":
        key = set(item["key_drugs"])
        return key <= set(val.names), bool(key & set(val.names)) and not key <= set(val.names)
    if kind == "cat":
        return item["label"] in val.labels, False
    raise ValueError(kind)


def classify_value(val, atom: dict) -> dict:
    r = {"vn": False, "foreign": [], "superseded": [], "decoy": False, "partial": False}
    for it in atom.get("vn") or []:
        ok, part = matches(val, it, atom)
        r["vn"] |= ok
        r["partial"] |= part
    for f in atom.get("foreign") or []:
        if any(matches(val, it, atom)[0] for it in f["values"]):
            r["foreign"].append(f["system"])
    for s in atom.get("superseded") or []:
        if any(matches(val, it, atom)[0] for it in s["values"]):
            r["superseded"].append(s["guideline"])
    r["decoy"] = any(matches(val, it, atom)[0] for it in atom.get("decoy") or [])
    return r


def _distinct(vals: list) -> list:
    out = []
    for flag, v in vals:
        if all(v != w for _, w in out):
            out.append((flag, v))
    return out


def grade_short(output: str, atom: dict, lang: str = "vi", synonyms=None, combos=None,
                extracted: str | None = None, condition: str | None = None) -> Grade:
    """Grade a short-answer output. `extracted` = answer string from the LLM extractor (method llm).
    `condition`: asking back "which country?" counts as label 1 only without a country cue (A0); always pass it."""
    if extracted is not None:
        span, method = extracted, "llm"
    else:
        span, method = answer_span(output)
    vals = _distinct(parse_values(span, atom, lang, synonyms, combos))
    full_text = THINK.sub(" ", output or "")
    g = Grade(label=None, label_name=None, parse_method=method, answer_text=span[:300])
    if method == "fallback" and len(vals) > 1:
        g.needs_llm = True
        g.parsed = [repr(v) for _, v in vals]
        return g
    if not vals:
        if atom["value_kind"] == "num" and nv.parse_nums(span, lang) and method == "answer_line":
            g.parse_method = "unit_mismatch"  # a value was given but in an unconvertible unit
            g.label, g.label_name = 5, LABELS[5]
            return g
        g.parse_method = "none" if method == "fallback" else method
        g.label = 1 if (ASK_COUNTRY.search(full_text) and condition == "A0") else 6
        g.label_name = LABELS[g.label]
        return g
    g.parsed = [repr(v) for _, v in vals]
    g.unit_assumed = any(f == "assumed" for f, _ in vals)
    cls = [classify_value(v, atom) for _, v in vals]
    g.decoy_match = any(c["decoy"] for c in cls)
    g.partial = any(c["partial"] for c in cls) and not any(c["vn"] for c in cls)
    if len(cls) > 1 and not all(c["vn"] for c in cls):
        g.multi = True
        if any(c["vn"] for c in cls) and VN_MARK.search(span):
            g.vn_match = True
            g.foreign_systems = sorted({s for c in cls for s in c["foreign"]})
            g.label, g.label_name = 1, LABELS[1]
        else:
            g.label, g.label_name = 5, LABELS[5]
        return g
    c = cls[0] if len(cls) == 1 else {"vn": True, "foreign": [], "superseded": [], "decoy": False}
    g.vn_match = c["vn"]
    g.foreign_systems = sorted(set(c["foreign"]))
    g.superseded = sorted(set(c["superseded"]))
    if c["vn"] and c["foreign"] and atom["value_kind"] == "drugs":
        # one drug list containing both the MoH and a foreign regimen
        g.multi = True
        conflicting = [f["system"] for f in atom.get("foreign") or []
                       if all(_gap(v, it, atom) > 0 for v in atom["vn"] for it in f["values"])]
        if set(c["foreign"]) & set(conflicting):
            aware = bool(VN_MARK.search(full_text) or FOREIGN_NAMES.search(full_text))
            g.label = 1 if aware else 5
            g.label_name = LABELS[g.label]
            return g
    if c["vn"]:
        aware = False
        others = _distinct(parse_values(full_text, atom, lang, synonyms, combos))
        if any(classify_value(v, atom)["foreign"] and not classify_value(v, atom)["vn"] for _, v in others):
            aware = bool(CONTRAST.search(full_text) or FOREIGN_NAMES.search(full_text))
        elif CONTRAST.search(full_text) and FOREIGN_NAMES.search(full_text):
            aware = True
        g.label = 1 if aware else 2
    elif c["superseded"]:
        g.label = 3
    elif c["foreign"]:
        g.label = 4
    else:
        g.label = 5
    g.label_name = LABELS[g.label]
    return g


MCQ_LETTER = re.compile(r"(?:ĐÁP\s*ÁN|ANSWER)?\s*[:：]?\s*\(?\b([A-F])\b\)?", re.I)


def grade_mcq(output: str, option_roles: dict[str, str]) -> Grade:
    """option_roles: letter -> 'vn' | 'foreign:US' | 'superseded:3705/2019' | 'decoy'."""
    span, method = answer_span(output)
    m = MCQ_LETTER.search(span if method == "answer_line" else span[:40])
    g = Grade(label=None, label_name=None, parse_method=method, answer_text=span[:100])
    if not m or m.group(1).upper() not in option_roles:
        g.label, g.label_name = 6, LABELS[6]
        return g
    role = option_roles[m.group(1).upper()]
    g.parsed = [m.group(1).upper()]
    if role == "vn":
        g.label, g.vn_match = 2, True
    elif role.startswith("superseded:"):
        g.label, g.superseded = 3, [role.split(":", 1)[1]]
    elif role.startswith("foreign:"):
        g.label, g.foreign_systems = 4, role.split(":", 1)[1].split("+")
    else:
        g.label, g.decoy_match = 5, role == "decoy"
    g.label_name = LABELS[g.label]
    return g


# ------------------------------------------------------------------------------ atom helpers
def _gap(a: dict, b: dict, atom: dict) -> float:
    kind = atom["value_kind"]
    if kind == "num":
        ctx, unit = atom.get("context") or {}, atom.get("unit")
        x = nv.Num(float(a["lo"]), float(a["hi"]), a.get("unit") or unit).to(unit, ctx)
        y = nv.Num(float(b["lo"]), float(b["hi"]), b.get("unit") or unit).to(unit, ctx)
        if x is None or y is None:
            return float("inf")
        return max(0.0, max(x.lo, y.lo) - min(x.hi, y.hi))
    if kind == "bp":
        return max(abs(a["sys"] - b["sys"]), abs(a["dia"] - b["dia"]))
    if kind == "schedule":
        return 0.0 if list(a["seq"]) == list(b["seq"]) else float("inf")
    if kind == "drugs":
        return 0.0 if set(a["key_drugs"]) & set(b["key_drugs"]) else float("inf")
    if kind == "cat":
        return 0.0 if a["label"] == b["label"] else float("inf")
    raise ValueError(kind)


def others(atom: dict) -> list[dict]:
    items = [it for f in atom.get("foreign") or [] for it in f["values"]]
    items += [it for s in atom.get("superseded") or [] for it in s["values"]]
    items += list(atom.get("decoy") or [])
    return items


def compute_tolerance(atom: dict) -> float:
    """Half the minimum gap between the MoH value set and every other source value (foreign,
    superseded, decoy), so tolerance windows never overlap the MoH set. Exact match (0) for
    schedule/drugs/cat kinds and when a gap is 0 (such atoms are concordant/indistinguishable)."""
    gaps = [_gap(v, o, atom) for v in atom.get("vn") or [] for o in others(atom)]
    finite = [g for g in gaps if g not in (0.0, float("inf"))]
    if not finite or atom["value_kind"] not in ("num", "bp"):
        return 0.0
    return min(finite) / 2.0


def conflict_status(atom: dict) -> str:
    """conflict | concordant | no_counterpart | indistinguishable.
    conflict: at least one foreign value lies OUTSIDE the MoH value set (gap > 0 to every MoH item).
    indistinguishable: a conflicting foreign value cannot be told apart from a superseded or decoy
    value (tolerance windows overlap), or the decoy touches the MoH set."""
    vn = atom.get("vn") or []
    foreign = [it for f in atom.get("foreign") or [] for it in f["values"]]
    if not foreign:
        return "no_counterpart"
    conflicting = [o for o in foreign if all(_gap(v, o, atom) > 0 for v in vn)]
    if not conflicting:
        return "concordant"
    tol = float(atom.get("tolerance") if atom.get("tolerance") is not None else compute_tolerance(atom))
    sup = [it for s in atom.get("superseded") or [] for it in s["values"]]
    dec = list(atom.get("decoy") or [])
    for o in conflicting:
        for x in sup + dec:
            gap = _gap(o, x, atom)
            if gap == 0.0 or gap < 2 * tol:
                return "indistinguishable"
    for x in dec + sup:
        if any(_gap(v, x, atom) == 0 for v in vn):
            return "indistinguishable" if x in dec else "conflict"
    return "conflict"
