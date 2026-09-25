"""Vietnamese/English clinical value normalisation (numbers, ranges, comparators, units,
blood pressure, schedules, drugs, categories). Pure stdlib. Pre-registered: changes after the
question freeze must be logged in docs/DECISIONS.md and re-run on the whole run set.

Conventions
- Vietnamese: comma = decimal ("0,5"), dot + 3 digits = thousands ("5.000"). A dot with other
  than 3 digits, or a leading 0 ("0.500"), is read as a decimal (models often use English style).
  "2,000" (comma + "000") is read as thousands in both languages (a decimal would not be written so).
- English: dot = decimal, comma + 3 digits = thousands; "2.000" (dot + "000", non-zero integer part)
  is read as thousands.
- Values are intervals [lo, hi] in a unit; a point has lo == hi; comparators are kept in `cmp`
  but thresholds are compared by value only.
"""
from __future__ import annotations

import re
import unicodedata
from collections import deque
from dataclasses import dataclass, field

# ------------------------------------------------------------------------------------ cleaning
DASHES = "‐‑‒–—―−"
FRACTIONS = {"½": 0.5, "¼": 0.25, "¾": 0.75, "⅓": 1 / 3}


def clean(text: str) -> str:
    t = unicodedata.normalize("NFC", text or "")
    for d in DASHES:
        t = t.replace(d, "-")
    t = t.replace(" ", " ").replace(" ", " ").replace("μ", "µ")
    t = t.replace("≧", "≥").replace("≦", "≤").replace("=>", "≥").replace(">=", "≥").replace("<=", "≤")
    t = t.replace("³", "3").replace("²", "2").replace("*", "")
    return re.sub(r"[ \t]+", " ", t).strip()


def strip_accents(s: str) -> str:
    s = s.replace("đ", "d").replace("Đ", "D")
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


# ------------------------------------------------------------------------------------ numbers
NUM_RE = r"(?<![\w.,/^])(?:\d{1,3}(?:[.,]\d{3})+(?:[.,]\d+)?|\d+(?:[.,]\d+)?|[½¼¾⅓])"


def parse_number(tok: str, lang: str = "vi") -> float:
    tok = tok.strip()
    if tok in FRACTIONS:
        return FRACTIONS[tok]
    if "." in tok and "," in tok:
        dec = "." if tok.rfind(".") > tok.rfind(",") else ","
        th = "," if dec == "." else "."
        return float(tok.replace(th, "").replace(dec, "."))
    for sep in (".", ","):
        if sep in tok:
            parts = tok.split(sep)
            groups3 = all(len(p) == 3 for p in parts[1:]) and parts[0] not in ("0", "")
            if len(parts) > 2 and groups3:
                return float("".join(parts))  # 1.000.000
            head, tail = parts[0], parts[1]
            if lang == "vi":
                thousands = (sep == "." and groups3) or (sep == "," and tail == "000" and head != "0")
            else:
                thousands = (sep == "," and groups3) or (sep == "." and tail == "000" and head != "0")
            return float(head + tail) if thousands else float(head + "." + tail)
    return float(tok)


# ------------------------------------------------------------------------------------ units
UNIT_ALIASES = {
    "ml/kg/giờ": "ml/kg/h", "ml/kg/gio": "ml/kg/h", "ml/kg/h": "ml/kg/h", "ml/kg/hr": "ml/kg/h",
    "ml/kg/hour": "ml/kg/h", "ml/kg/tiếng": "ml/kg/h",
    "mg/kg/ngày": "mg/kg/day", "mg/kg/day": "mg/kg/day", "mg/kg/d": "mg/kg/day", "mg/kg/24h": "mg/kg/day",
    "mg/kg": "mg/kg", "µg/kg": "ug/kg", "mcg/kg": "ug/kg", "ug/kg": "ug/kg", "microgram/kg": "ug/kg",
    "g/kg": "g/kg",
    "mg/dl": "mg/dL", "mmol/l": "mmol/L", "mmhg": "mmHg", "mm hg": "mmHg",
    "iu/ml": "IU/mL", "ui/ml": "IU/mL", "u/l": "U/L", "iu/l": "U/L", "ui/l": "U/L", "kpa": "kPa",
    "kg/m2": "kg/m2", "/mm3": "/uL", "/µl": "/uL", "/ul": "/uL", "/microlit": "/uL",
    "x10^9/l": "10^9/L", "×10^9/l": "10^9/L", "x 10^9/l": "10^9/L", "× 10^9/l": "10^9/L",
    "x109/l": "10^9/L", "g/l tiểu cầu": "10^9/L",
    "mg": "mg", "µg": "ug", "mcg": "ug", "ug": "ug", "microgram": "ug", "micrograms": "ug", "g": "g", "gram": "g",
    "ml": "ml", "l": "l", "lít": "l", "lit": "l",
    "%": "%", "giờ": "h", "gio": "h", "h": "h", "hr": "h", "hrs": "h", "hour": "h", "hours": "h", "tiếng": "h",
    "phút": "min", "min": "min", "minutes": "min", "ngày": "day", "day": "day", "days": "day",
    "tuần": "week", "week": "week", "weeks": "week", "tháng": "month", "month": "month", "months": "month",
    "tháng tuổi": "month", "months old": "month", "năm": "year", "year": "year", "years": "year",
    "tuổi": "year", "years old": "year", "viên": "tablet", "tablet": "tablet", "tablets": "tablet",
    "ống": "ampoule", "ampoule": "ampoule", "ampoules": "ampoule", "vial": "ampoule", "lọ": "ampoule",
}
_UNIT_KEYS = sorted(UNIT_ALIASES, key=len, reverse=True)
UNIT_RE = "(?:" + "|".join(re.escape(u) for u in _UNIT_KEYS) + r")(?![^\W\d_])"

# (from, to): factor  value_to = value_from * factor
STATIC_EDGES = {
    ("ug", "mg"): 1e-3, ("g", "mg"): 1e3, ("l", "ml"): 1e3, ("ug/kg", "mg/kg"): 1e-3, ("g/kg", "mg/kg"): 1e3,
    ("/uL", "10^9/L"): 1e-3, ("min", "h"): 1 / 60, ("week", "day"): 7.0, ("month", "year"): 1 / 12,
}
ANALYTE_MGDL_PER_MMOL = {"glucose": 18.016, "ldl": 38.67, "cholesterol": 38.67, "hdl": 38.67, "triglyceride": 88.57}


def canon_unit(u: str | None) -> str | None:
    if not u:
        return None
    return UNIT_ALIASES.get(clean(u).lower(), clean(u))


def _edges(ctx: dict) -> dict:
    e = dict(STATIC_EDGES)
    a = (ctx or {}).get("analyte")
    if a in ANALYTE_MGDL_PER_MMOL:
        e[("mmol/L", "mg/dL")] = ANALYTE_MGDL_PER_MMOL[a]
    if (ctx or {}).get("weight_kg"):
        w = float(ctx["weight_kg"])
        e[("mg/kg", "mg")] = w
        e[("ug/kg", "ug")] = w
    if (ctx or {}).get("mg_per_ml"):
        e[("ml", "mg")] = float(ctx["mg_per_ml"])
    if (ctx or {}).get("mg_per_tablet"):
        e[("tablet", "mg")] = float(ctx["mg_per_tablet"])
    if (ctx or {}).get("mg_per_ampoule"):
        e[("ampoule", "mg")] = float(ctx["mg_per_ampoule"])
    both = {}
    for (a_, b_), f in e.items():
        both[(a_, b_)] = f
        both.setdefault((b_, a_), 1 / f)
    return both


def convert(value: float, frm: str | None, to: str | None, ctx: dict | None = None) -> float | None:
    """Convert value between canonical units; None if impossible. Missing unit -> assume `to`."""
    if frm is None or to is None or frm == to:
        return value
    edges = _edges(ctx or {})
    graph: dict[str, list[tuple[str, float]]] = {}
    for (a, b), f in edges.items():
        graph.setdefault(a, []).append((b, f))
    q, seen = deque([(frm, 1.0)]), {frm}
    while q:
        u, f = q.popleft()
        if u == to:
            return value * f
        for v, g in graph.get(u, []):
            if v not in seen:
                seen.add(v)
                q.append((v, f * g))
    return None


# ------------------------------------------------------------------------------------ values
@dataclass(frozen=True)
class Num:
    lo: float
    hi: float
    unit: str | None = None
    cmp: str | None = None  # >=, >, <=, <, None

    def to(self, unit: str | None, ctx: dict | None = None) -> "Num | None":
        lo, hi = convert(self.lo, self.unit, unit, ctx), convert(self.hi, self.unit, unit, ctx)
        if lo is None or hi is None:
            return None
        return Num(min(lo, hi), max(lo, hi), unit or self.unit, self.cmp)


@dataclass(frozen=True)
class BP:
    sys: float
    dia: float
    cmp: str | None = None


@dataclass(frozen=True)
class Schedule:
    seq: tuple
    unit: str | None = "day"


@dataclass(frozen=True)
class Drugs:
    names: frozenset = field(default_factory=frozenset)


@dataclass(frozen=True)
class Cat:
    labels: frozenset = field(default_factory=frozenset)


CMP_WORDS = [
    (r"≥|không dưới|ít nhất|tối thiểu|từ|at least|no less than|≥", ">="),
    (r"≤|không quá|tối đa|at most|up to|no more than|maximum|max", "<="),
    (r">|trên|lớn hơn|cao hơn|vượt quá|above|over|greater than|more than|exceeding|higher than", ">"),
    (r"<|dưới|nhỏ hơn|thấp hơn|below|under|less than|lower than", "<"),
]
CMP_RE = "(?:" + "|".join(p for p, _ in CMP_WORDS) + ")"


def _cmp_of(word: str | None) -> str | None:
    if not word:
        return None
    w = word.strip().lower()
    for pat, c in CMP_WORDS:
        if re.fullmatch(pat, w):
            return c
    return None


RANGE_RE = re.compile(
    rf"(?:từ\s+|from\s+|between\s+)?(?P<a>{NUM_RE})\s*(?P<ua>{UNIT_RE})?\s*(?:-|đến|tới|to)\s*"
    rf"(?P<b>{NUM_RE})\s*(?P<ub>{UNIT_RE})?", re.I)
SINGLE_RE = re.compile(rf"(?:(?P<cmp>{CMP_RE})\s*)?(?P<a>{NUM_RE})\s*(?P<u>{UNIT_RE})?", re.I)
FRACTION_RE = re.compile(r"(?P<n>\d+)\s*/\s*(?P<d>\d+)\s*(?P<u>ống|ampoules?|viên|tablets?)", re.I)


CITATION_RE = re.compile(
    r"(?:\b(?:qđ|quyết định|quyet dinh|thông tư|tt|decision|circular|nđ|nghị định)\s*(?:số\s*)?\d+(?:/[\wđĐ\-]+)*)"
    r"|(?:\b\d{2,5}/(?:qđ|tt|nđ)[\w\-/đĐ]*)"
    r"|(?:\b\d{3,5}/(?:19|20)\d{2}\b)",
    re.I)

def strip_citations(text: str) -> str:
    """Remove decision numbers ('QĐ 2760/QĐ-BYT', '1740/2026') and bare years ('ADA 2025')."""
    t = CITATION_RE.sub(" ", clean(text))
    return re.sub(rf"(?<![\d.,])(?:19|20)\d{{2}}(?![\d.,])(?!\s*{UNIT_RE})", " ", t, flags=re.I)


def parse_nums(text: str, lang: str = "vi") -> list[Num]:
    """All numeric values (ranges first, then singles) in reading order."""
    t = strip_citations(text)
    found: list[tuple[int, Num]] = []
    taken: list[tuple[int, int]] = []

    def free(s, e):
        return all(e <= a or s >= b for a, b in taken)

    for m in FRACTION_RE.finditer(t):
        v = int(m.group("n")) / int(m.group("d"))
        found.append((m.start(), Num(v, v, canon_unit(m.group("u")))))
        taken.append(m.span())
    for m in RANGE_RE.finditer(t):
        if not free(*m.span()):
            continue
        a, b = parse_number(m.group("a"), lang), parse_number(m.group("b"), lang)
        if b < a:  # "10-5" is not a range
            continue
        u = canon_unit(m.group("ub") or m.group("ua"))
        found.append((m.start(), Num(a, b, u)))
        taken.append(m.span())
    for m in SINGLE_RE.finditer(t):
        if not free(*m.span("a")):
            continue
        v = parse_number(m.group("a"), lang)
        found.append((m.start(), Num(v, v, canon_unit(m.group("u")), _cmp_of(m.group("cmp")))))
        taken.append(m.span())
    return [n for _, n in sorted(found, key=lambda x: x[0])]


BP_RE = re.compile(rf"(?:(?P<cmp>{CMP_RE})\s*)?(?P<s>\d{{2,3}})\s*/\s*(?P<d>\d{{2,3}})(?!\s*(?:u/l|iu|ui))", re.I)


def parse_bps(text: str) -> list[BP]:
    out = []
    for m in BP_RE.finditer(strip_citations(text)):
        s, d = float(m.group("s")), float(m.group("d"))
        if 60 <= s <= 260 and 30 <= d <= 160 and s > d:
            out.append(BP(s, d, _cmp_of(m.group("cmp"))))
    return out


SCHED_SEP = r"\s*(?:-|,|;|/|và|and|&|\+)\s*"


def parse_schedules(text: str, min_len: int = 3) -> list[Schedule]:
    t = strip_citations(text).lower()
    t = re.sub(r"\b(?:n|d|ngày|day|days)\s*(?=\d)", "", t)
    unit = "month" if re.search(r"tháng|month", t) else "day"
    out = []
    for m in re.finditer(rf"\d{{1,3}}(?:{SCHED_SEP}\d{{1,3}})+", t):
        seq = tuple(int(x) for x in re.findall(r"\d{1,3}", m.group(0)))
        if len(seq) >= min_len and list(seq) == sorted(seq) and len(set(seq)) == len(seq):
            out.append(Schedule(seq, unit))
    return out


def _norm_drug_text(s: str) -> str:
    s = strip_accents(clean(s).lower())
    return re.sub(r"\s*(?:-|/|\+)\s*", "-", s)


def parse_drugs(text: str, synonyms: dict[str, list[str]], combos: dict[str, list[str]] | None = None) -> Drugs:
    """synonyms: canonical INN -> aliases; combos: combination -> component INNs."""
    t = " " + _norm_drug_text(text) + " "
    pairs = sorted(((_norm_drug_text(a), c) for c, al in synonyms.items() for a in [c, *al]),
                   key=lambda x: len(x[0]), reverse=True)
    found = set()
    for alias, canon in pairs:
        pat = rf"(?<![a-z0-9]){re.escape(alias)}(?![a-z0-9])"
        if re.search(pat, t):
            found.add(canon)
            t = re.sub(pat, " ", t)
    for combo, parts in (combos or {}).items():
        if all(p in found for p in parts):
            found -= set(parts)
            found.add(combo)
    return Drugs(frozenset(found))


def parse_cats(text: str, options: dict[str, list[str]]) -> Cat:
    t = strip_accents(clean(text).lower())
    hit = {lab for lab, pats in options.items() if any(re.search(strip_accents(p.lower()), t) for p in pats)}
    return Cat(frozenset(hit))
