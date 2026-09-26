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
- One value, not two (grader 1.1.0): a compound age "3 tuổi 4 tháng" (= 40 months), a fraction range of a dose
  form "1/5-1/3 ống", a split blood pressure "tâm thu ≥ 140 … tâm trương ≥ 90". Dose forms (ml, ml/kg, ống,
  viên) convert only through the atom context (mg_per_ml, mg_per_ampoule, mg_per_tablet, weight_kg); never guessed.
  Unit phrases in words are read as units ("0.01 mg per kg", "0,01 mg cho mỗi kg", "5 mL/kg per hour"); the grader
  drops product concentrations ("1:1000", "1‰", "1 mg/ml"), which are not doses (parse_nums(drop_concentrations=True)).
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
    t = t.replace("³", "3").replace("²", "2").replace("*", "").replace("⁄", "/").replace("∕", "/")
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
    "mg/kg": "mg/kg", "ml/kg": "ml/kg", "µg/kg": "ug/kg", "mcg/kg": "ug/kg", "ug/kg": "ug/kg", "microgram/kg": "ug/kg",
    "micrograms/kg": "ug/kg", "mg/kg/24 giờ": "mg/kg/day",
    "g/kg": "g/kg",
    "mg/dl": "mg/dL", "mmol/l": "mmol/L", "mmhg": "mmHg", "mm hg": "mmHg",
    "iu/ml": "IU/mL", "ui/ml": "IU/mL", "iu/kg": "IU/kg", "ui/kg": "IU/kg", "đơn vị/kg": "IU/kg", "u/l": "U/L", "iu/l": "U/L", "ui/l": "U/L", "kpa": "kPa",
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
    "ống": "ampoule", "ampoule": "ampoule", "ampoules": "ampoule", "amp": "ampoule", "amps": "ampoule",
    "vial": "ampoule", "lọ": "ampoule",
    # added 26/9/2026 from pilot-agent reports (pre-freeze): units that must NOT be taken as the atom's unit
    "kg": "kg", "cm": "cm", "mmol/mol": "mmol/mol",
    "iu": "IU", "ui": "IU", "đơn vị": "IU", "units": "IU", "international units": "IU",
    "lần/ngày": "times/day", "lần mỗi ngày": "times/day", "times/day": "times/day", "times daily": "times/day",
    "lần/tuần": "times/week", "lần": "times", "times": "times",
    "mg base/kg/ngày": "mg/kg/day", "mg base/kg": "mg/kg", "mg/kg/tuần": "mg/kg/week", "mg/kg/week": "mg/kg/week",
    "mg/ngày": "mg/day", "mg/day": "mg/day", "mg base/ngày": "mg/day", "mg/24 giờ": "mg/day", "mg/24h": "mg/day",
    "index": "index", "chỉ số": "index",
}
_UNIT_KEYS = sorted(UNIT_ALIASES, key=len, reverse=True)
UNIT_RE = "(?:" + "|".join(re.escape(u) for u in _UNIT_KEYS) + r")(?![^\W\d_])"

# (from, to): factor  value_to = value_from * factor
STATIC_EDGES = {
    ("ug", "mg"): 1e-3, ("g", "mg"): 1e3, ("l", "ml"): 1e3, ("ug/kg", "mg/kg"): 1e-3, ("g/kg", "mg/kg"): 1e3,
    ("/uL", "10^9/L"): 1e-3, ("min", "h"): 1 / 60, ("day", "h"): 24.0, ("week", "day"): 7.0, ("month", "year"): 1 / 12,
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
        e[("mg/kg/day", "mg/day")] = w
    if (ctx or {}).get("mg_per_ml"):
        e[("ml", "mg")] = float(ctx["mg_per_ml"])
        e[("ml/kg", "mg/kg")] = float(ctx["mg_per_ml"])      # "0,01 ml/kg" of a 1 mg/ml solution = 0,01 mg/kg
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


def _set_repr(s: frozenset) -> str:
    """frozenset repr in sorted order (the default order follows PYTHONHASHSEED; graded files must be reproducible)."""
    return "frozenset({" + ", ".join(repr(x) for x in sorted(s)) + "})" if s else "frozenset()"


@dataclass(frozen=True, repr=False)
class Drugs:
    names: frozenset = field(default_factory=frozenset)

    def __repr__(self) -> str:
        return f"Drugs(names={_set_repr(self.names)})"


@dataclass(frozen=True, repr=False)
class Cat:
    labels: frozenset = field(default_factory=frozenset)

    def __repr__(self) -> str:
        return f"Cat(labels={_set_repr(self.labels)})"


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
# Dose forms counted in fractions ("1/2 ống", "½ ống", "1 1/2 ống", "1/5-1/3 ống", "1⁄3 ống" after clean(), "1/5 to
# 1/3 of an ampoule"; "nửa ống" / "half an ampoule" are read as "½ ống"); the unit is required.
FORM_RE = r"(?:ống|ampoules?|amps?|lọ|vial|viên|tablets?)(?![^\W\d_])"
_OF = r"(?:of\s+(?:an?\s+|the\s+)?)?"
FRAC_RE = r"(?<![\w.,/])\d+\s*/\s*[1-9]\d*(?![\d.,])"
FRACTION_RE = re.compile(rf"(?:(?<![\w.,/])(?P<w>\d{{1,2}})\s*)?(?P<f>{FRAC_RE}|[½¼¾⅓])\s*{_OF}(?P<u>{FORM_RE})", re.I)
FRACTION_RANGE_RE = re.compile(
    rf"(?P<a>{FRAC_RE}|{NUM_RE})\s*(?:{_OF}{FORM_RE})?\s*(?:-|đến|tới|to)\s*(?P<b>{FRAC_RE}|{NUM_RE})\s*{_OF}"
    rf"(?P<u>{FORM_RE})", re.I)
HALF_WORD_RE = re.compile(rf"(?<![^\W\d_])(?:nửa|half(?:\s+(?:of\s+)?(?:an?|the))?)\s+(?={FORM_RE})", re.I)


# One age/duration written in two units: "3 tuổi 4 tháng", "3 năm 4 tháng", "3 years (and) 4 months", "3 years, 4
# months", "3 yrs 4 mos" -> 40 months; a range with such an end ("3 tuổi 4 tháng – 5 tuổi") is one range.
def _compound(y: str, m: str) -> str:
    return (rf"(?<![\w.,/])(?P<{y}>\d{{1,3}})\s*(?:tuổi|năm|years?|yrs?)(?:\s*,\s*|\s+)(?:(?:và|and)\s+)?"
            rf"(?P<{m}>\d{{1,2}})\s*(?:tháng|months?|mos?)(?![^\W\d_])")


def _age(n: str, u: str) -> str:
    return rf"(?<![\w.,/])(?P<{n}>\d{{1,3}})\s*(?P<{u}>tuổi|năm|years?|yrs?|tháng|months?|mos?)(?![^\W\d_])"


COMPOUND_RE = re.compile(rf"(?:(?P<cmp>{CMP_RE})\s*)?{_compound('y', 'm')}", re.I)
COMPOUND_RANGE_RE = re.compile(
    rf"(?:từ\s+|from\s+|between\s+)?(?:{_compound('y1', 'm1')}|{_age('n1', 'u1')})\s*(?:-|đến|tới|to|and)\s*"
    rf"(?:{_compound('y2', 'm2')}|{_age('n2', 'u2')})", re.I)
# "3 tuổi rưỡi" = 3.5 years, "1 tháng rưỡi" = 1.5 months
HALF_UNIT_RE = re.compile(
    rf"(?:(?P<cmp>{CMP_RE})\s*)?(?<![\w.,/])(?P<a>\d{{1,3}})\s*(?P<u>tuổi|năm|tháng|tuần|ngày|giờ)\s+rưỡi(?![^\W\d_])",
    re.I)

# Unit phrases in words: "0.01 mg per kg", "0,01 mg cho mỗi kg", "0,01 mg/1 kg", "0,01 ml / kg" -> "mg/kg" (before
# 1.1.0 the "/kg" was dropped: 10 µg instead of 60 µg at 6 kg, inside the decoy range); "5 mL/kg per hour" ->
# "ml/kg/h"; "0,5 mg/kg mỗi ngày", "mg/kg cân nặng/ngày" -> "mg/kg/day" (as "mg/kg/ngày" already was). An amount
# over a time ("15 ml/kg trong 1 giờ") is not rewritten.
PER_KG_RE = re.compile(
    r"(?<![^\W\d_])(?P<u>mg|µg|mcg|ug|micrograms?|ml)\s*(?:/\s*(?:1\s*)?|\s(?:per|(?:cho\s+)?mỗi)\s+(?:1\s+)?)"
    r"(?:kg|kilograms?)(?![^\W\d_])", re.I)
PER_TIME_RE = re.compile(
    r"(?P<u>(?:ml|mg)/kg)(?:\s*(?:cân\s*nặng|thể\s*trọng|body\s*weight))?(?:\s*/\s*|\s+(?:per|mỗi|một|an?|every)\s+)"
    r"(?:1\s+)?(?P<t>24\s*(?:giờ|gio|h|hours?)|giờ|gio|hours?|hr|h|ngày|days?)(?![^\W\d_])"
    r"|(?P<u2>(?:ml|mg)/kg)\s+(?P<t2>hourly|daily)(?![^\W\d_])", re.I)
# Product concentrations are not doses (dropped by the grader: parse_nums(drop_concentrations=True)): "1:1000",
# "1/10.000", "1‰", "1 mg/ml", "1 mg/1 mL", "1 mg per mL", "1 mg trong 1 ml". "0,5 mg in 0,5 mL" (a dose and its
# volume) is kept.
CONC_RE = re.compile(
    r"(?<![\w.,/:])1\s*[:/]\s*(?:1|10|100)[.,\s]?000(?![\d.,])"
    r"|(?<![\w.,])\d+(?:[.,]\d+)?\s*‰"
    r"|(?<![\w.,/])\d+(?:[.,]\d+)?\s*(?:mg|µg|mcg|ug)\s*(?:/\s*(?:1\s*)?|\s+(?:per|trong|in)\s+(?:1\s+|one\s+|a\s+)?)"
    r"ml(?![^\W\d_])", re.I)


def _frac(tok: str, lang: str) -> float:
    if "/" in tok:
        n, d = tok.split("/")
        return int(n) / int(d)
    return parse_number(tok, lang)


def _unit_phrases(t: str) -> str:
    t = PER_KG_RE.sub(lambda m: m.group("u") + "/kg", t)

    def per_time(m: re.Match) -> str:
        u, tt = (m.group("u") or m.group("u2")).lower(), (m.group("t") or m.group("t2")).lower()
        day = tt.startswith(("ng", "day", "da", "24"))
        if u == "ml/kg" and not day:
            return "ml/kg/h"
        return "mg/kg/day" if u == "mg/kg" and day else m.group(0)
    return PER_TIME_RE.sub(per_time, t)


def _months(m: re.Match, i: str) -> float:
    if m.group("y" + i):
        return 12.0 * int(m.group("y" + i)) + int(m.group("m" + i))
    n = int(m.group("n" + i))
    return float(n) if re.match(r"th|mo", m.group("u" + i), re.I) else 12.0 * n


CITATION_RE = re.compile(
    r"(?:\b(?:qđ|quyết định|quyet dinh|thông tư|tt|decision|circular|nđ|nghị định)\s*(?:số\s*)?\d+(?:/[\wđĐ\-]+)*)"
    r"|(?:\b\d{2,5}/(?:qđ|tt|nđ)[\w\-/đĐ]*)"
    r"|(?:\b\d{3,5}/(?:19|20)\d{2}\b)",
    re.I)

def strip_citations(text: str) -> str:
    """Remove decision numbers ('QĐ 2760/QĐ-BYT', '1740/2026') and bare years ('ADA 2025')."""
    t = CITATION_RE.sub(" ", clean(text))
    return re.sub(rf"(?<![\d.,])(?:19|20)\d{{2}}(?![\d.,])(?!\s*{UNIT_RE})", " ", t, flags=re.I)


def parse_nums(text: str, lang: str = "vi", drop_concentrations: bool = False) -> list[Num]:
    """All numeric values in reading order: compound ages ('3 tuổi 4 tháng', and ranges with such an end), halves
    ('3 tuổi rưỡi'), fractions of a dose form ('1/5-1/3 ống'), ranges, then singles. drop_concentrations: ignore
    product concentrations ('1:1000', '1 mg/ml'; used by the grader)."""
    t = strip_citations(text)
    if drop_concentrations:
        t = CONC_RE.sub(" ", t)
    t = _unit_phrases(HALF_WORD_RE.sub("½ ", t))
    found: list[tuple[int, Num]] = []
    taken: list[tuple[int, int]] = []

    def free(s, e):
        return all(e <= a or s >= b for a, b in taken)

    for m in COMPOUND_RANGE_RE.finditer(t):
        if not (m.group("y1") or m.group("y2")) or any(m.group(k) and int(m.group(k)) >= 12 for k in ("m1", "m2")):
            continue                                      # "4-6 tuổi" is left to RANGE_RE
        lo, hi = _months(m, "1"), _months(m, "2")
        if hi < lo:
            continue
        found.append((m.start(), Num(lo, hi, "month")))
        taken.append(m.span())
    for m in COMPOUND_RE.finditer(t):
        if not free(*m.span()) or int(m.group("m")) >= 12:   # "3 năm 18 tháng" is not one age
            continue
        v = 12.0 * int(m.group("y")) + int(m.group("m"))
        found.append((m.start(), Num(v, v, "month", _cmp_of(m.group("cmp")))))
        taken.append(m.span())
    for m in HALF_UNIT_RE.finditer(t):
        if not free(*m.span()):
            continue
        v = int(m.group("a")) + 0.5
        found.append((m.start(), Num(v, v, canon_unit(m.group("u")), _cmp_of(m.group("cmp")))))
        taken.append(m.span())
    for m in FRACTION_RANGE_RE.finditer(t):
        if not free(*m.span()) or not any("/" in m.group(k) or m.group(k) in FRACTIONS for k in ("a", "b")):
            continue                                      # plain "0,3-0,5 ống" is left to RANGE_RE
        a, b = _frac(re.sub(r"\s+", "", m.group("a")), lang), _frac(re.sub(r"\s+", "", m.group("b")), lang)
        if b < a:
            continue
        found.append((m.start(), Num(a, b, canon_unit(m.group("u")))))
        taken.append(m.span())
    for m in FRACTION_RE.finditer(t):
        if not free(*m.span()):
            continue
        v = _frac(re.sub(r"\s+", "", m.group("f")), lang) + int(m.group("w") or 0)
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
# Split form: "HA tâm thu ≥ 140 mmHg và/hoặc HA tâm trương ≥ 90 mmHg", "HATT (HATTh) ≥ 140 và HATTr ≥ 90",
# "SBP ≥140 and/or DBP ≥90 mmHg", "≥130 mmHg systolic or ≥80 mmHg diastolic", "HA ≥ 140 mmHg (tâm thu) và/hoặc
# ≥ 90 mmHg (tâm trương)", either order -> one BP(sys, dia, cmp). A range per part ("tâm thu 140–159") is not read.
_SYS = r"(?:(?:huyết\s*áp|HA)\s*)?tâm\s*thu|HA\s*TTh?(?!r)|SBP|systolic(?:\s+(?:blood\s+)?pressure|\s+BP)?"
_DIA = r"(?:(?:huyết\s*áp|HA)\s*)?tâm\s*trương|HA\s*TTr|DBP|diastolic(?:\s+(?:blood\s+)?pressure|\s+BP)?"
_MMHG = r"(?:\s*mm\s*Hg)?"
_UP = r"(?:\s*(?P<{}>trở\s*lên|trở\s*xuống|or\s+(?:higher|more|above|greater|lower|less|below)))?"  # "140 trở lên"
_JOIN = r"\s*[,;]?\s*(?:và\s*/\s*hoặc|và|hoặc|and\s*/\s*or|and|or|/)?\s*"
_BPV = r"(?<![\d.,])\d{2,3}(?![\d.,]?\d)"


def _bp_label_first(label: str, c: str, v: str, u: str) -> str:
    """'tâm thu ≥ 140 mmHg (trở lên)'"""
    return (rf"(?<![^\W\d_])(?:{label})(?![^\W\d_])\s*(?:là|:|=|of)?\s*(?:(?P<{c}>{CMP_RE})\s*)?(?P<{v}>{_BPV}){_MMHG}"
            + _UP.format(u))


def _bp_value_first(label: str, c: str, v: str) -> str:
    """'≥ 130 mmHg systolic', '≥ 140 mmHg (tâm thu)'"""
    return rf"(?:(?P<{c}>{CMP_RE})\s*)?(?P<{v}>{_BPV}){_MMHG}\s*\(?\s*(?:{label})(?![^\W\d_])\s*\)?"


BP_SPLIT_RE = re.compile("|".join([
    _bp_label_first(_SYS, "c1", "s1", "u1") + _JOIN + _bp_label_first(_DIA, "c2", "d1", "u2"),
    _bp_label_first(_DIA, "c3", "d2", "u3") + _JOIN + _bp_label_first(_SYS, "c4", "s2", "u4"),
    _bp_value_first(_SYS, "c5", "s3") + _JOIN + _bp_value_first(_DIA, "c6", "d3"),
    _bp_value_first(_DIA, "c7", "d4") + _JOIN + _bp_value_first(_SYS, "c8", "s4"),
]), re.I)


def _first(m: re.Match, prefix: str, n: int) -> str | None:
    return next((m.group(f"{prefix}{i}") for i in range(1, n + 1) if m.group(f"{prefix}{i}")), None)


def parse_bps(text: str) -> list[BP]:
    """Blood pressures written as 'S/D' or split into systolic and diastolic thresholds, in reading order."""
    t = strip_citations(text)
    found: list[tuple[int, BP]] = []
    taken: list[tuple[int, int]] = []
    for m in BP_SPLIT_RE.finditer(t):
        s, d = float(_first(m, "s", 4)), float(_first(m, "d", 4))
        cmp = _cmp_of(_first(m, "c", 8))
        up = (_first(m, "u", 4) or "").lower()
        if cmp is None and up:
            cmp = ">=" if re.search(r"lên|higher|more|above|greater", up) else "<="
        if 60 <= s <= 260 and 30 <= d <= 160 and s > d:
            found.append((m.start(), BP(s, d, cmp)))
            taken.append(m.span())
    for m in BP_RE.finditer(t):
        if any(not (m.end() <= a or m.start() >= b) for a, b in taken):
            continue
        s, d = float(m.group("s")), float(m.group("d"))
        if 60 <= s <= 260 and 30 <= d <= 160 and s > d:
            found.append((m.start(), BP(s, d, _cmp_of(m.group("cmp")))))
    return [b for _, b in sorted(found, key=lambda x: x[0])]


SCHED_SEP = r"\s*(?:-|,|;|/|và|and|&|\+)\s*"


def parse_schedules(text: str, min_len: int = 3) -> list[Schedule]:
    """Sequences like "N0-3-7-14-28", "ngày 0, 3, 7, 14", "Ngày 0 Ngày 3 Ngày 7", "2, 3, 4 tháng".
    The unit is decided locally for each sequence: a day marker (N, D, ngày, day) on its numbers -> day;
    otherwise a unit word right after it (or right before it) -> month/day; default day."""
    t = strip_citations(text).lower()
    t = re.sub(r"\b(?:n|d|ngày|day|days)\s*(?=\d)", "§", t)        # § marks a day-prefixed number
    out = []
    for m in re.finditer(rf"§?\d{{1,3}}(?:(?:{SCHED_SEP}|\s+(?=§))§?\d{{1,3}})+", t):
        seq = tuple(int(x) for x in re.findall(r"\d{1,3}", m.group(0)))
        if not (len(seq) >= min_len and list(seq) == sorted(seq) and len(set(seq)) == len(seq)):
            continue
        after, before = t[m.end():m.end() + 16], t[max(0, m.start() - 16):m.start()]
        if "§" in m.group(0):
            unit = "day"
        elif re.match(r"\s*(?:tháng|months?)\b", after):
            unit = "month"
        elif re.match(r"\s*(?:ngày|days?)\b", after):
            unit = "day"
        else:
            unit = "month" if re.search(r"(?:tháng|months?)\W*(?:thứ)?\s*$", before) else "day"
        out.append(Schedule(seq, unit))
    return out


def _norm_drug_text(s: str) -> str:
    s = strip_accents(clean(s).lower())
    s = re.sub(r"(?<![a-z0-9])([a-z]{2,5})[1-9](?![a-z0-9])", r"\1", s)   # table footnotes: "DTG1", "TAF2" -> "dtg", "taf"
    return re.sub(r"\s*(?:-|/|\+)\s*", "-", s)


def _alias_pattern(alias: str) -> str:
    """A normalised alias as a whole-word pattern; a space and a hyphen are interchangeable inside it
    ('tenofovir alafenamid' also matches 'tenofovir-alafenamid')."""
    return r"(?<![a-z0-9])" + "[ -]".join(re.escape(p) for p in re.split(r"[ -]", alias)) + r"(?![a-z0-9])"


def _chain_codes(text: str, synonyms: dict[str, list[str]]) -> set[str]:
    """INNs named by 1–2 letter TB codes (aliases '~cs', '~am', '~e'... in configs/grading.yaml), read ONLY inside a
    regimen chain holding ≥ 3 other recognised drugs ('Bdq Lzd Cfz Cs', '4-6 Am-Lfx-Pto-Cfz-Z-H'). A chain is a run
    of drug codes and numbers; any other word ends it. Accents are kept, so 'âm tính' is never 'Am'."""
    chain = {a[1:].lower(): c for c, al in synonyms.items() for a in al if a.startswith("~")}
    if not chain:
        return set()
    anchor = {}
    for c, al in synonyms.items():
        for a in [c, *al]:
            k = _norm_drug_text(a)
            if not a.startswith("~") and re.fullmatch(r"[a-z0-9]+", k):
                anchor[k] = c
    t = re.sub(r"\([^)]*\)|\[[^\]]*\]", " ", clean(text).lower())
    t = re.sub(r"(?<![^\W_])([^\W\d_]{2,5})[1-9](?![^\W_])", r"\1", t)
    out: set[str] = set()
    runs, run = [], []
    for m in re.finditer(r"[^\W_]+", t):
        tok = m.group(0)
        if tok in anchor or tok in chain or tok.isdigit():
            run.append(tok)
        else:
            runs.append(run)
            run = []
    for r in [*runs, run]:
        if len({anchor[x] for x in r if x in anchor}) >= 3:
            out.update(chain[x] for x in r if x in chain)
    return out


def parse_drugs(text: str, synonyms: dict[str, list[str]], combos: dict[str, list[str]] | None = None) -> Drugs:
    """synonyms: canonical INN -> aliases; combos: combination -> component INNs (collapsed, largest first, so
    BPaL + moxifloxacin reads as BPaLM, not BPaL). Two canonical forms carry structure (configs/grading.yaml):
    'a+b+c' is a named regimen (BPaL, TLD, Biktarvy) and expands to its member INNs; 'a|b' is a drug class
    ('tenofovir') kept as one token that stands for ONE of its members (see drugs_cover). Aliases starting with '~'
    are TB chain codes (see _chain_codes)."""
    t = " " + _norm_drug_text(text) + " "
    pairs = sorted(((_norm_drug_text(a), c) for c, al in synonyms.items() for a in [c, *al] if not a.startswith("~")),
                   key=lambda x: len(x[0]), reverse=True)
    found = _chain_codes(text, synonyms)
    for alias, canon in pairs:
        pat = _alias_pattern(alias)
        if re.search(pat, t):
            found.update(canon.split("+") if "+" in canon and "|" not in canon else [canon])
            t = re.sub(pat, " ", t)
    found -= {n for n in found if "|" in n and set(n.split("|")) & found}   # "tenofovir (TDF)" names TDF only
    return Drugs(frozenset(_collapse(found, combos)))


def _collapse(found: set, combos: dict[str, list[str]] | None) -> set:
    for combo, parts in sorted((combos or {}).items(), key=lambda kv: -len(kv[1])):
        if all(p in found for p in parts):
            found = (found - set(parts)) | {combo}
    return found


def resolve_classes(d: Drugs, choice: dict[str, str], combos: dict[str, list[str]] | None = None) -> Drugs:
    """The drug list with each class token ('tenofovir-disoproxil|tenofovir-alafenamide') replaced by the member
    chosen for it (grade_short grades every choice; see grade._class_choices)."""
    if not any(n in choice for n in d.names):
        return d
    return Drugs(frozenset(_collapse({choice.get(n, n) for n in d.names}, combos)))


def drugs_cover(names, key) -> tuple[bool, bool]:
    """(every drug of `key` is named, some drug of `key` is named). A class token 'a|b' ('tenofovir') names at most
    one required member: 'tenofovir' satisfies [tenofovir-disoproxil] but not [tenofovir-disoproxil,
    tenofovir-alafenamide]."""
    direct = {n for n in names if "|" not in n}
    classes = [set(n.split("|")) for n in names if "|" in n]
    key = set(key)

    def assign(missing: list, pool: list) -> bool:
        if not missing:
            return True
        return any(missing[0] in c and assign(missing[1:], pool[:i] + pool[i + 1:]) for i, c in enumerate(pool))

    overlap = bool(key & direct) or any(key & c for c in classes)
    return assign(sorted(key - direct), classes), overlap


def parse_cats(text: str, options: dict[str, list[str]]) -> Cat:
    t = strip_accents(clean(text).lower())
    hit = {lab for lab, pats in options.items() if any(re.search(strip_accents(p.lower()), t) for p in pats)}
    return Cat(frozenset(hit))
