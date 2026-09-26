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
- Grader 1.2.0: powers of ten ("2 x 10^3", "2.10^4") are one number; copies/mL is never converted to IU/mL; numbers
  in words before a unit are read ("bảy ngày", "two weeks"); frequencies are one value in times/day ("once a day",
  "ngày 1 lần"), counts in times ("twice" = "hai lần"); dose/visit ordinals ("mũi 1", "dose 1") and reference doses
  ("sau mũi 18 tháng", "after the 18-month visit") yield to real values; a BP range "130–139/80–89" is read at its
  lower bounds, "120–129/<80" and opposite comparators ("≥140/<90") are no BP; a negated or vehicle mention of a
  category ("không dùng X", "X rather than", "HES in 0.9% saline") is not that category (parse_cats, same rule for
  every label and a Vietnamese phrase for every English one; negation words read with their accents).
"""
from __future__ import annotations

import re
import unicodedata
from collections import deque
from dataclasses import dataclass, field

# ------------------------------------------------------------------------------------ cleaning
DASHES = "‐‑‒–—―−"
FRACTIONS = {"½": 0.5, "¼": 0.25, "¾": 0.75, "⅓": 1 / 3}
SUPERSCRIPTS = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻", "0123456789-")


def clean(text: str) -> str:
    t = unicodedata.normalize("NFC", text or "")
    for d in DASHES:
        t = t.replace(d, "-")
    t = t.replace(" ", " ").replace(" ", " ").replace("μ", "µ")
    t = t.replace("≧", "≥").replace("≦", "≤").replace("=>", "≥").replace(">=", "≥").replace("<=", "≤")
    # a power of ten keeps its caret ("2×10³" -> "2×10^3", grader 1.2.0); other superscripts are unit exponents
    t = re.sub(r"(?<![\d.,])10([⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+)", lambda m: "10^" + m.group(1).translate(SUPERSCRIPTS), t)
    t = re.sub(r"(?<=\d)\s*\*\s*(?=10\s*\^)", "×", t)    # "2*10^3" is 2×10³ (before: "210^3", read as 210)
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
    "phút": "min", "min": "min", "minute": "min", "minutes": "min", "ngày": "day", "day": "day", "days": "day",
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
    "times/week": "times/week", "times/month": "times/month", "lần/tháng": "times/month",   # frequencies (1.2.0)
    "mg base/kg/ngày": "mg/kg/day", "mg base/kg": "mg/kg", "mg/kg/tuần": "mg/kg/week", "mg/kg/week": "mg/kg/week",
    "mg/ngày": "mg/day", "mg/day": "mg/day", "mg base/ngày": "mg/day", "mg/24 giờ": "mg/day", "mg/24h": "mg/day",
    "index": "index", "chỉ số": "index",
    # grader 1.2.0: viral load in copies is its own unit. It is NOT converted to IU/mL (the factor depends on the
    # assay), so a copies/mL answer to an IU/mL atom is a value in an unconvertible unit (label 5, unit_mismatch).
    "copies/ml": "copies/mL", "copy/ml": "copies/mL", "cp/ml": "copies/mL", "bản sao/ml": "copies/mL",
    "cps/ml": "copies/mL", "copies per ml": "copies/mL", "iu per ml": "IU/mL", "ui per ml": "IU/mL",
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
# "once" (grader 1.2.0): "10 mg/kg once daily", "once a day", "1 lần mỗi ngày", "1 lần/ngày" = mg/kg/day. "twice daily"
# is never rewritten (10 mg/kg twice daily is 20 mg/kg/day; the per-dose value stays in mg/kg).
_ONCE = r"(?:once|(?:1|một)\s*lần)"
PER_TIME_RE = re.compile(
    r"(?P<u>(?:ml|mg)/kg)(?:\s*(?:cân\s*nặng|thể\s*trọng|body\s*weight))?"
    rf"(?:\s*/\s*|\s+(?:{_ONCE}\s+)?(?:per|mỗi|một|an?|every)\s+|\s+{_ONCE}\s*/\s*)"
    r"(?:1\s+)?(?P<t>24\s*(?:giờ|gio|h|hours?)|giờ|gio|hours?|hr|h|ngày|days?)(?![^\W\d_])"
    r"|(?P<u2>(?:ml|mg)/kg)\s+(?:once\s+)?(?P<t2>hourly|daily)(?![^\W\d_])", re.I)
# Unit spellings (grader 1.2.0): "kg/m^2", "kg/m²", "kg/m 2", "kg per m2", "kg per square metre", "kg·m-2" -> "kg/m2";
# "mg base" (EN and VI) -> "mg" (the MoH and WHO primaquine doses are both in mg base); "18-month", "7-day",
# "4-year-old" -> "18 month" (the unit attaches; before 1.2.0 "18-month" was a unit-less 18, read in the atom's unit).
KG_M2_RE = re.compile(
    r"(?<![^\W\d_])kg\s*(?:(?:/|per(?![^\W\d_]))\s*(?:m\s*\^?\s*2(?!\d)|sq(?:uare)?\.?\s*met(?:re|er)s?(?![^\W\d_])"
    r"|sq\.?\s*m(?![^\W\d_]))|[·.\s]\s*m\s*\^?\s*-\s*2(?!\d))", re.I)
MG_BASE_RE = re.compile(r"(?<![^\W\d_])mg\s+(?:base|bazơ|bazo)(?![^\W\d_])", re.I)
HYPHEN_UNIT_RE = re.compile(
    r"(?<![\w.,])(?P<n>\d{1,3})-(?P<u>months?|years?|weeks?|days?|hours?|minutes?)(?:-old)?(?![^\W\d_])", re.I)
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
    t = KG_M2_RE.sub("kg/m2", t)
    t = MG_BASE_RE.sub("mg", t)
    t = HYPHEN_UNIT_RE.sub(lambda m: f"{m.group('n')} {m.group('u')}", t)
    t = ADJ_UNIT_RE.sub(" ", t)                         # "3 consecutive days" -> "3 days" (see NUM_WORD_RE)
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


# ------------------------------------------------------------------ numbers written in words (grader 1.2.0)
# Read only right before a unit ("ba ngày", "bảy ngày", "hai tuần", "mười lăm phút", "hai mươi bốn giờ", "three days",
# "seven days", "two weeks", "twenty-four hours"), in both languages up to 999. "twice"/"once" are frequencies, not
# numbers ("100 mg twice daily" stays 100 mg). Vietnamese: "lăm"/"tư"/"mốt" only after "mười"/"mươi", so "mười năm" is
# ten years (not 15) and "hai năm" is two years.
_VI_DIG = {"một": 1, "hai": 2, "ba": 3, "bốn": 4, "năm": 5, "sáu": 6, "bảy": 7, "bẩy": 7, "tám": 8, "chín": 9}
_VI_AFTER_TENS = dict(_VI_DIG, mốt=1, tư=4, lăm=5, nhăm=5)
del _VI_AFTER_TENS["năm"]
_EN_ONES = {w: i for i, w in enumerate("one two three four five six seven eight nine".split(), 1)}
_EN_TEENS = {w: i for i, w in enumerate("ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen "
                                         "nineteen".split(), 10)}
_EN_TENS = {w: 10 * i for i, w in enumerate("twenty thirty forty fifty sixty seventy eighty ninety".split(), 2)}


def _alt(words) -> str:
    return "(?:" + "|".join(sorted(words, key=len, reverse=True)) + ")"


_VD, _VA = _alt(_VI_DIG), _alt(_VI_AFTER_TENS)
_VT = rf"(?:mười|{_VD}\s+mươi)(?:\s+{_VA})?"
_VI_NUM = rf"{_VD}\s+trăm(?:\s+(?:(?:linh|lẻ)\s+{_VD}|{_VT}))?|{_VT}|{_VD}"
_EO, _ET = _alt(_EN_ONES), _alt(_EN_TEENS)
_EN_T = rf"{_alt(_EN_TENS)}(?:[\s-]{_EO})?|{_ET}|{_EO}"
_EN_NUM = rf"(?:{_EO}|a)\s+hundred(?:\s+(?:and\s+)?(?:{_EN_T}))?|{_EN_T}"
# English puts an adjective between the number and the unit ("three consecutive days", "3 full weeks"); Vietnamese puts
# it after the unit ("ba ngày liên tiếp"). Both read as the number with its unit (after review, still 1.2.0).
_EN_ADJ = r"(?:consecutive|successive|straight|full|whole|entire|additional|further|more|extra|separate)"
NUM_WORD_RE = re.compile(
    rf"(?<![^\W_])(?<!\d\s)(?P<w>{_VI_NUM}|{_EN_NUM})(?=\s+(?:{_EN_ADJ}\s+)?(?P<u>{UNIT_RE}))", re.I)
ADJ_UNIT_RE = re.compile(rf"(?<=\d)\s+{_EN_ADJ}\s+(?={UNIT_RE})", re.I)
# "một"/"one"/"a"/"an" before a unit are mostly articles ("vào một ngày khác", "after an hour", "consult a doctor
# within a day"): read as 1 only when the text has no other value than a frequency (like the labels below) AND the
# phrase opens its clause (≤ 3 words before it since the last , ; : . - and frequencies not counted: "một tuần",
# "ANSWER: one week", "within a day", "once a day for a week", "Theo Bộ Y tế: một tuần" = "Per MoH: one week"), so a
# hedge ("consult a doctor within a day") is not a value; never before a count ("một lần", "one time": adverbs).
# "năm" is the word "year", not 5, in a unit hint "(năm tuổi)" and in "năm tuổi thứ 7" (the 7th year of age); elsewhere
# "năm tuổi", "năm năm", "năm tháng" are 5 (after review: "năm tuổi" = "five years").
_COUNT_UNIT = r"(?:lần|times?)(?![^\W\d_])"
WEAK_ONE_RE = re.compile(rf"(?<![^\W_])(?<!\d\s)(?:một|one|an?)(?=\s+{UNIT_RE})(?!\s+{_COUNT_UNIT})", re.I)

# Frequencies (grader 1.2.0, after review): "once a day", "twice daily", "3 times a day", "3x/day", "one time a day",
# "ngày một lần", "mỗi ngày uống 2 lần", "1 lần/ngày", "một lần mỗi ngày" are ONE value in a frequency unit
# (times/day, times/week, times/month), never a duration: before, the "a day" of "once a day" was read as 1 day (the
# decoy of P-malaria_ocr-06). Digits, words and adverbs read alike ("ngày 1 lần" = "ngày một lần" = "once a day"),
# as "2 lần/ngày" already was a times/day value in 1.1.0. No pilot atom is a frequency, so such a value is dropped
# by the grader when another value exists and is a unit mismatch (label 5) when alone. A dose per kg with "once
# daily" is still a daily dose (PER_TIME_RE runs first). A bare count stays a count in `times`: "hai lần" = "2 lần",
# "twice"/"thrice" = "2 times"/"3 times" (so "Repeat twice" = "Nhắc lại hai lần"); "once"/"một lần" alone are not
# read (mostly adverbs: "once stable", "một lần nữa").
_FREQ_WORD = {"once": 1, "twice": 2, "thrice": 3, "one": 1, "một": 1}
FREQ_RE = re.compile(
    r"(?<![^\W\d_])(?:(?P<a1>once|twice|thrice)|(?P<n1>\d+|one)\s*(?:x|×|times?))\s*(?:(?:a|an|per|each|every)\s+|/\s*)?"
    r"(?P<p1>days?|daily|weeks?|weekly|months?|monthly)(?![^\W\d_])"
    r"|(?<![\w.,])(?<!\d\s)(?:(?:mỗi|một|hàng)\s+)?(?P<p2>ngày|tuần|tháng)\s+(?:(?:uống|dùng|tiêm|bôi|nhỏ|chia)\s+(?:làm\s+)?)?"
    r"(?P<n2>\d+|một)\s*lần(?![^\W\d_])(?!\s*/)"
    r"|(?<![^\W\d_])(?P<n3>\d+|một)\s*lần\s*(?:/\s*|(?:mỗi|một|trong\s+(?:một|1)|trên|trong)\s+)(?P<p3>ngày|tuần|tháng)"
    r"(?![^\W\d_])", re.I)
TWICE_RE = re.compile(r"(?<![^\W\d_])(?P<w>twice|thrice)(?![^\W\d_])", re.I)
FREQ_UNITS = frozenset({"times/day", "times/week", "times/month"})
_FREQ_TOKEN = re.compile(r"\d+ times/(?:day|week|month)")


def _period(p: str) -> str:
    p = p.lower()
    return "week" if p.startswith(("w", "tu")) else "month" if p.startswith(("mo", "th")) else "day"


def frequencies(t: str) -> str:
    """Frequency phrases as 'N times/day|week|month', then 'twice'/'thrice' as counts (see FREQ_RE)."""
    def sub(m: re.Match) -> str:
        w = next(g for g in (m.group("a1"), m.group("n1"), m.group("n2"), m.group("n3")) if g)
        n = _FREQ_WORD.get(w.lower()) or int(w)
        return f"{n} times/{_period(m.group('p1') or m.group('p2') or m.group('p3'))}"
    t = FREQ_RE.sub(sub, t)
    return TWICE_RE.sub(lambda m: "2 times" if m.group("w").lower() == "twice" else "3 times", t)


def _word_value(w: str) -> int:
    toks = re.split(r"[\s-]+", w.lower())
    total = 0
    if "trăm" in toks or "hundred" in toks:
        i = toks.index("trăm" if "trăm" in toks else "hundred")
        total, toks = 100 * (_VI_DIG.get(toks[0]) or _EN_ONES.get(toks[0], 1)), [x for x in toks[i + 1:] if x != "and"]
        if toks and toks[0] in ("linh", "lẻ"):
            return total + _VI_DIG[toks[1]]
    if not toks:
        return total
    if toks[0] == "mười":
        return total + 10 + (_VI_AFTER_TENS[toks[1]] if len(toks) > 1 else 0)
    if len(toks) > 1 and toks[1] == "mươi":
        return total + 10 * _VI_DIG[toks[0]] + (_VI_AFTER_TENS[toks[2]] if len(toks) > 2 else 0)
    if toks[0] in _EN_TENS:
        return total + _EN_TENS[toks[0]] + (_EN_ONES[toks[1]] if len(toks) > 1 else 0)
    return total + (_VI_DIG.get(toks[0]) or _EN_ONES.get(toks[0]) or _EN_TEENS[toks[0]])


_WEAK_CUT = re.compile(r"[;:,!?\n]|\.(?!\d)|\s-+\s")


def _weak_one(t: str) -> str:
    """The opening "một/one/a/an <unit>" of its clause as "1 <unit>" (see WEAK_ONE_RE); frequencies already rewritten
    ('1 times/day') do not count as words before it."""
    m = WEAK_ONE_RE.search(t)
    clause = _WEAK_CUT.split(t[:m.start()])[-1] if m else ""
    if m and len(re.findall(r"[^\W_]+", _FREQ_TOKEN.sub(" ", clause))) <= 3:
        return t[:m.start()] + "1" + t[m.end():]
    return t


def number_words(t: str) -> str:
    """Numbers written in words before a unit -> digits ('bảy ngày' -> '7 ngày', 'two weeks' -> '2 weeks'). A word
    used as the unit of a number is not read again as a number ('mười năm ngày' is '10 năm ngày', not '10 5 ngày')."""
    out, pos, unit_end = [], 0, -1
    for m in NUM_WORD_RE.finditer(t):
        w = m.group("w").lower()
        if m.start() < unit_end or w in ("một", "one") or (w == "năm" and (
                re.search(r"\(\s*$", t[:m.start()]) or re.match(r"\s+tuổi\s+thứ", t[m.end():], re.I))):
            continue                                 # "(năm tuổi)", "năm tuổi thứ 7": the word "year", not 5
        out += [t[pos:m.start()], str(_word_value(w))]
        pos, unit_end = m.end(), m.end("u")
    return "".join(out) + t[pos:]


# ------------------------------------------------------------------ labels that are not values (grader 1.2.0)
# Ordinals of a dose/visit ("mũi 1", "mũi thứ 2", "liều 2", "lần 1", "dose 1", "(MMR dose 1)") are not answer values,
# nor is a PREVIOUS dose or visit named by its age and introduced as a reference point ("sau mũi 18 tháng", "after the
# 18-month dose", "following the 18 month booster", "kể từ mũi 9 tháng"). They yield to real values: parse_nums reads
# the text with them masked, and only when nothing else is left reads it again unmasked. A number with a unit is
# never an ordinal ("liều 2 mg", "2 liều", "liều 1-2 viên" are values). After review (still 1.2.0): a dose named by
# its age WITHOUT such a reference word ("mũi 9 tháng", "the 9-month dose", "18-month booster") is a value like any
# other, so "mũi 9 tháng; một số nước tiêm lúc 12 tháng" is two values (before: the 9 was masked and the answer
# became the foreign 12 months); a restated value ("12 months (at the 12-month visit)") is one value (grade._distinct).
_ORD_NOUN = (r"(?:mũi(?:\s+tiêm)?|liều|lần|lượt|đợt|chu\s+kỳ|doses?|shots?|injections?|boosters?|visits?|rounds?|"
             r"cycles?)")                    # "đợt 1" = "round 1", "chu kỳ 1" = "cycle 1" (after review)
ORDINAL_RE = re.compile(
    rf"(?<![^\W\d_]){_ORD_NOUN}\s*(?:thứ\s+|số\s+|#\s*|no\.?\s*|number\s+)?"
    rf"(?P<n>\d{{1,2}}(?:\s*(?:,|và|and|&)\s*\d{{1,2}})*)(?![\d.,]*\d)(?!\s*(?:-|đến|tới|to)\s*\d)(?!\s*{UNIT_RE})",
    re.I)
_LABEL_NOUN_EN = (r"(?:doses?|shots?|injections?|visits?|boosters?|vaccinations?|vaccines?|check-?ups?|appointments?|"
                  r"well[- ]child\s+visits?)")
TIME_LABEL_RE = re.compile(
    r"(?<![^\W\d_])(?:after|following|since)\s+(?:(?:the|a|an|his|her|their)\s+)?"
    rf"\d{{1,2}}[- ](?:months?|years?|weeks?|days?)(?:[- ]old)?\s+{_LABEL_NOUN_EN}(?![^\W\d_])"
    r"|(?<![^\W\d_])(?:sau(?:\s+khi)?|kể\s+từ|tính\s+từ)\s+(?:tiêm\s+)?"
    r"mũi(?:\s+(?:tiêm|nhắc(?:\s+lại)?|vắc[- ]?xin))?\s+\d{1,2}\s*(?:tháng|tuổi|tuần|năm)(?:\s+tuổi)?(?![^\W\d_])",
    re.I)


def mask_labels(t: str) -> str:
    """The text with dose/visit ordinals and dose/visit names blanked (see ORDINAL_RE, TIME_LABEL_RE)."""
    t = TIME_LABEL_RE.sub(" ", t)
    return ORDINAL_RE.sub(lambda m: m.group(0)[: m.start("n") - m.start()] + " ", t)


# ------------------------------------------------------------------ powers of ten (grader 1.2.0)
# "2 x 10^3", "2×10³" ("10^3" after clean()), "2 · 10^3", "2.10^4" / "2,5.10^4" (Vietnamese: a dot before "10^" is a
# multiplication sign), "10^4 IU/mL", "2e3", "2E+03" -> one number. "× 10^9/L" stays a unit (UNIT_ALIASES), so a
# platelet count "100 × 10^9/L" is 100 in 10^9/L.
POW_RE = re.compile(
    rf"(?:(?P<cmp>{CMP_RE})\s*)?"
    rf"(?:(?P<m>{NUM_RE})\s*[x×·]\s*|(?<![\w.,/^])(?P<md>\d+(?:,\d+)?)\.|(?<![\w.,/^]))"
    rf"10\s*\^\s*\(?(?P<e>-?\d{{1,2}})\)?(?!\d)(?!\s*/\s*l(?![^\W\d_]))\s*(?P<u>{UNIT_RE})?"
    rf"|(?:(?P<cmp2>{CMP_RE})\s*)?(?<![\w.,/^])(?P<m2>\d+(?:[.,]\d+)?)e(?P<e2>[+-]?\d{{1,2}})(?![\w.,])\s*"
    rf"(?P<u2>{UNIT_RE})?", re.I)


def _pow_value(m: re.Match, lang: str) -> float:
    if m.group("m2"):
        return parse_number(m.group("m2"), lang) * 10.0 ** int(m.group("e2"))
    mant = m.group("m") or m.group("md")
    return (parse_number(mant, lang) if mant else 1.0) * 10.0 ** int(m.group("e"))


def parse_nums(text: str, lang: str = "vi", drop_concentrations: bool = False) -> list[Num]:
    """All numeric values in reading order: powers of ten ('2 x 10^3'), compound ages ('3 tuổi 4 tháng', and ranges
    with such an end), halves ('3 tuổi rưỡi'), fractions of a dose form ('1/5-1/3 ống'), ranges, then singles.
    Numbers in words before a unit are read ('bảy ngày'); frequencies are one value in times/day ('once a day');
    dose/visit ordinals and reference doses ('mũi 1', 'after the 18-month visit') yield to real values (mask_labels).
    drop_concentrations: ignore product concentrations ('1:1000', '1 mg/ml'; used by the grader)."""
    t = strip_citations(text)
    if drop_concentrations:
        t = CONC_RE.sub(" ", t)
    t = number_words(HALF_WORD_RE.sub("½ ", t))
    masked = frequencies(_unit_phrases(mask_labels(t)))
    found = _parse_nums(masked, lang)
    if all(n.unit in FREQ_UNITS for n in found):   # nothing else: read the labels and the weak "một/one/a" too
        full = _weak_one(frequencies(_unit_phrases(t)))
        if full != masked:
            found = _parse_nums(full, lang)
    return found


def _parse_nums(t: str, lang: str) -> list[Num]:
    found: list[tuple[int, Num]] = []
    taken: list[tuple[int, int]] = []

    def free(s, e):
        return all(e <= a or s >= b for a, b in taken)

    pows = list(POW_RE.finditer(t))
    i = 0
    while i < len(pows):                              # "10^4–10^5 copies/mL", "từ 10^4 đến 10^5": one range, one unit
        m, n = pows[i], pows[i + 1] if i + 1 < len(pows) else None
        lo = hi = _pow_value(m, lang)
        unit, cmp = m.group("u") or m.group("u2"), _cmp_of(m.group("cmp") or m.group("cmp2"))
        end = m.end()
        n_unit = n and (n.group("u") or n.group("u2"))
        if n and re.fullmatch(r"\s*(?:-|đến|tới|to)\s*", t[m.end():n.start()], re.I) and _pow_value(n, lang) >= lo \
                and (not unit or not n_unit or canon_unit(unit) == canon_unit(n_unit)):
            hi, unit, cmp, end = _pow_value(n, lang), unit or n_unit, None, n.end()    # "từ … đến": no comparator
            i += 1
        found.append((m.start(), Num(lo, hi, canon_unit(unit), cmp)))
        taken.append((m.start(), end))
        i += 1
    for m in COMPOUND_RANGE_RE.finditer(t):
        if not free(*m.span()):
            continue
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


# 'S/D' (grader 1.2.0: also "140 over 90", "140 trên 90", a comparator on each part "≥140/≥90 mmHg"). A systolic that
# ends a range whose diastolic is no range ("120–129/<80", the ACC/AHA "elevated" category) is no BP value (after
# review: 1.2.0 read it as 129/80 '<', i.e. near the US 130/80); nor is a pair with opposite comparators ("≥140/<90",
# isolated systolic hypertension), in every BP form.
BP_RE = re.compile(
    rf"(?:(?P<cmp>{CMP_RE})\s*)?(?<![\d.,])(?<!\d-)(?<!\d\s-)(?<!\d-\s)(?<!\d\s-\s)(?P<s>\d{{2,3}})"
    rf"(?:\s*/\s*|\s+(?:over|trên)\s+)(?:(?P<cmp2>{CMP_RE})\s*)?(?P<d>\d{{2,3}})(?!\s*(?:u/l|iu|ui))", re.I)


def _opposite(*cmps: str | None) -> bool:
    """Explicit comparators pointing both up ('≥', '>', 'trở lên') and down ('<', '≤', 'trở xuống')."""
    dirs = {1 if c in (">=", ">") else -1 for c in cmps if c}
    return len(dirs) > 1
# A range 'S1–S2/D1–D2' ("130–139/80–89", "140–159/90–99 mmHg"): the BP value type has no interval, and every pilot bp
# atom is a threshold (P-htn-01, P-htn-03), so a range is read as the threshold at its LOWER bounds, BP(S1, D1, '>=')
# (grader 1.2.0; before, the inner '139/80' was read as a BP). The same rule for every source: the ACC/AHA stage-1
# range reads 130/80 (US), the MoH/ESC grade-1 range reads 140/90. A bp target atom would need an interval type.
BP_RANGE_RE = re.compile(
    rf"(?:(?P<cmp>{CMP_RE})\s*)?(?<![\d.,])(?P<s>\d{{2,3}})\s*-\s*(?P<s2>\d{{2,3}})\s*/\s*(?P<d>\d{{2,3}})\s*-\s*"
    rf"(?P<d2>\d{{2,3}})(?![\d.,]?\d)", re.I)
# Split form: "HA tâm thu ≥ 140 mmHg và/hoặc HA tâm trương ≥ 90 mmHg", "HATT (HATTh) ≥ 140 và HATTr ≥ 90",
# "SBP ≥140 and/or DBP ≥90 mmHg", "≥130 mmHg systolic or ≥80 mmHg diastolic", "HA ≥ 140 mmHg (tâm thu) và/hoặc
# ≥ 90 mmHg (tâm trương)", either order -> one BP(sys, dia, cmp). A range per part ("tâm thu 140–159 và/hoặc tâm
# trương 90–99", "130-139 systolic or 80-89 diastolic") is read at its lower bounds, as BP_RANGE_RE (grader 1.2.0).
_SYS = r"(?:(?:huyết\s*áp|HA)\s*)?tâm\s*thu|HA\s*TTh?(?!r)|SBP|systolic(?:\s+(?:blood\s+)?pressure|\s+BP)?"
_DIA = r"(?:(?:huyết\s*áp|HA)\s*)?tâm\s*trương|HA\s*TTr|DBP|diastolic(?:\s+(?:blood\s+)?pressure|\s+BP)?"
_MMHG = r"(?:\s*mm\s*Hg)?"
_UP = r"(?:\s*(?P<{}>trở\s*lên|trở\s*xuống|or\s+(?:higher|more|above|greater|lower|less|below)))?"  # "140 trở lên"
# joiners between the two parts; grader 1.2.0 adds "hay", "và/hay", "hoặc là" (Vietnamese 'or')
_JOIN = r"\s*[,;]?\s*(?:và\s*/\s*(?:hoặc|hay)|và|hoặc(?:\s+là)?|hay|and\s*/\s*or|and|or|/)?\s*"
_BPV = r"(?<![\d.,])\d{2,3}(?![\d.,]?\d)"


def _bp_label_first(label: str, c: str, v: str, u: str, r: str) -> str:
    """'tâm thu ≥ 140 mmHg (trở lên)', 'tâm thu 140–159'"""
    return (rf"(?<![^\W\d_])(?:{label})(?![^\W\d_])\s*(?:là|:|=|of)?\s*(?:(?P<{c}>{CMP_RE})\s*)?(?P<{v}>{_BPV})"
            rf"(?:\s*-\s*(?P<{r}>{_BPV}))?{_MMHG}" + _UP.format(u))


def _bp_value_first(label: str, c: str, v: str, r: str) -> str:
    """'≥ 130 mmHg systolic', '≥ 140 mmHg (tâm thu)', '130-139 systolic'"""
    return (rf"(?:(?P<{c}>{CMP_RE})\s*)?(?P<{v}>{_BPV})(?:\s*-\s*(?P<{r}>{_BPV}))?{_MMHG}\s*\(?\s*(?:{label})"
            rf"(?![^\W\d_])\s*\)?")


BP_SPLIT_RE = re.compile("|".join([
    _bp_label_first(_SYS, "c1", "s1", "u1", "r1") + _JOIN + _bp_label_first(_DIA, "c2", "d1", "u2", "r2"),
    _bp_label_first(_DIA, "c3", "d2", "u3", "r3") + _JOIN + _bp_label_first(_SYS, "c4", "s2", "u4", "r4"),
    _bp_value_first(_SYS, "c5", "s3", "r5") + _JOIN + _bp_value_first(_DIA, "c6", "d3", "r6"),
    _bp_value_first(_DIA, "c7", "d4", "r7") + _JOIN + _bp_value_first(_SYS, "c8", "s4", "r8"),
]), re.I)
# Two bare numbers joined by a conjunction ("≥ 140 và/hoặc ≥ 90 mmHg", "140 và 90 mmHg", "HA 140 and 90"; grader
# 1.2.0): read only with a BP context (mmHg after the second number, or HA/huyết áp/BP/blood pressure right before)
# and a plausible pair (diastolic ≤ 130, systolic − diastolic ≥ 20), so "140 và 130 mmHg" (two systolic values) is
# not a BP. Bare "hoặc"/"hay"/"or" are not joiners here (between two numbers they list alternatives).
BP_WORDS_RE = re.compile(
    r"(?P<ctx>(?:huyết\s*áp|(?-i:HA|BP)|blood\s+pressure)\s*(?:là|:|=|of)?\s*)?"
    rf"(?:(?P<cmp>{CMP_RE})\s*)?(?P<s>{_BPV}){_MMHG}\s*[,;]?\s*(?:và\s*/\s*(?:hoặc|hay)|and\s*/\s*or|và|and)\s*"
    rf"(?:(?P<cmp2>{CMP_RE})\s*)?(?P<d>{_BPV})(?P<mm>\s*mm\s*Hg)?", re.I)


def _first(m: re.Match, prefix: str, n: int) -> str | None:
    return next((m.group(f"{prefix}{i}") for i in range(1, n + 1) if m.group(f"{prefix}{i}")), None)


def _bp_ok(s: float, d: float) -> bool:
    return 60 <= s <= 260 and 30 <= d <= 160 and s > d


def parse_bps(text: str) -> list[BP]:
    """Blood pressures written as 'S/D' ('S over D', 'S trên D'), a range 'S1–S2/D1–D2' (read at its lower bounds),
    split into systolic and diastolic parts, or as two numbers joined by 'và'/'and' in a BP context; reading order."""
    t = strip_citations(text)
    found: list[tuple[int, BP]] = []
    taken: list[tuple[int, int]] = []

    def free(m: re.Match) -> bool:
        return all(m.end() <= a or m.start() >= b for a, b in taken)

    def up_cmp(u: str | None) -> str | None:
        return None if not u else ">=" if re.search(r"lên|higher|more|above|greater", u, re.I) else "<="

    for m in BP_SPLIT_RE.finditer(t):
        s, d = float(_first(m, "s", 4)), float(_first(m, "d", 4))
        ranges = [(m.group(v), m.group(f"r{i}")) for i, v in enumerate(
            ["s1", "d1", "d2", "s2", "s3", "d3", "d4", "s4"], 1) if m.group(f"r{i}")]
        if any(float(hi) <= float(lo) for lo, hi in ranges):
            continue                                     # '140-90' is not a range
        part = [_cmp_of(m.group(c)) or up_cmp(m.group(u) if u else None)
                for c, u in (("c1", "u1"), ("c2", "u2"), ("c3", "u3"), ("c4", "u4"), ("c5", None), ("c6", None),
                             ("c7", None), ("c8", None))]
        if _opposite(*part):
            continue                                     # 'tâm thu ≥ 140 và tâm trương < 90' is no threshold pair
        cmp = _cmp_of(_first(m, "c", 8)) or up_cmp(_first(m, "u", 4))
        if cmp is None and ranges:
            cmp = ">="                                   # a range read at its lower bound
        if _bp_ok(s, d):
            found.append((m.start(), BP(s, d, cmp)))
            taken.append(m.span())
    for m in BP_RANGE_RE.finditer(t):
        s, s2, d, d2 = (float(m.group(k)) for k in ("s", "s2", "d", "d2"))
        if free(m) and s < s2 and d < d2 and _bp_ok(s, d) and _bp_ok(s2, d2):
            found.append((m.start(), BP(s, d, ">=")))
            taken.append(m.span())
    for m in BP_WORDS_RE.finditer(t):
        s, d = float(m.group("s")), float(m.group("d"))
        if _opposite(_cmp_of(m.group("cmp")), _cmp_of(m.group("cmp2"))):
            continue
        if free(m) and (m.group("ctx") or m.group("mm")) and _bp_ok(s, d) and d <= 130 and s - d >= 20:
            found.append((m.start(), BP(s, d, _cmp_of(m.group("cmp") or m.group("cmp2")))))
            taken.append(m.span())
    for m in BP_RE.finditer(t):
        if not free(m) or _opposite(_cmp_of(m.group("cmp")), _cmp_of(m.group("cmp2"))):
            continue
        s, d = float(m.group("s")), float(m.group("d"))
        if _bp_ok(s, d):
            found.append((m.start(), BP(s, d, _cmp_of(m.group("cmp") or m.group("cmp2")))))
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
    of drug codes and numbers; any other word ends it. Accents are kept, so 'âm tính' is never 'Am'. '~code@n' sets
    the minimum to n, and a code written with a capital letter is matched case-sensitively (grader 1.2.0: '~Pa@2', so
    'Bdq, Pa, Lzd' reads pretomanid while 'X-quang PA, Bdq, Lzd' does not)."""
    chain, exact = {}, {}
    for c, al in synonyms.items():
        for a in al:
            if a.startswith("~"):
                code, _, n = a[1:].partition("@")
                (chain if code == code.lower() else exact)[code] = (c, int(n) if n else 3)
    if not chain and not exact:
        return set()
    anchor = {}
    for c, al in synonyms.items():
        for a in [c, *al]:
            k = _norm_drug_text(a)
            if not a.startswith("~") and re.fullmatch(r"[a-z0-9]+", k):
                anchor[k] = c
    t = re.sub(r"\([^)]*\)|\[[^\]]*\]", " ", clean(text))                 # case kept for the exact codes
    t = re.sub(r"(?<![^\W_])([^\W\d_]{2,5})[1-9](?![^\W_])", r"\1", t)

    def code(tok: str):
        return exact.get(tok) or chain.get(tok.lower())

    out: set[str] = set()
    runs, run = [], []
    for m in re.finditer(r"[^\W_]+", t):
        tok = m.group(0)
        if tok.lower() in anchor or code(tok) or tok.isdigit():
            run.append(tok)
        else:
            runs.append(run)
            run = []
    for r in [*runs, run]:
        n_anchor = len({anchor[x.lower()] for x in r if x.lower() in anchor})
        out.update(code(x)[0] for x in r if code(x) and n_anchor >= code(x)[1])
    return out


# A named regimen spelled letter by letter ("B-Pa-L", "B Pa L M", "B + Pa + Z"; grader 1.2.0): capitalised 1–2 letter
# tokens joined by spaces, '-', '+' or '/', read only when the joined letters are exactly a regimen alias of
# configs/grading.yaml (bpal, bpalm, bpamz, bpaz, bdlc, tld...). The ≥ 3-drug rule of the '~' codes is not relaxed.
SPELLED_RE = re.compile(r"(?<![^\W_])[A-Z][a-z]?(?:\s*[-+/\s]\s*[A-Z][a-z]?)+(?![^\W_])")


def _spelled_regimens(text: str, synonyms: dict[str, list[str]]) -> set[str]:
    names = {_norm_drug_text(a): c for c, al in synonyms.items() if "+" in c and "|" not in c
             for a in al if not a.startswith("~")}
    out: set[str] = set()
    for m in SPELLED_RE.finditer(clean(text)):
        toks = re.findall(r"[A-Z][a-z]?", m.group(0))
        for i in range(len(toks)):
            for j in range(i + 2, len(toks) + 1):
                key = "".join(toks[i:j]).lower()
                if key in names:
                    out.update(names[key].split("+"))
    return out


def parse_drugs(text: str, synonyms: dict[str, list[str]], combos: dict[str, list[str]] | None = None) -> Drugs:
    """synonyms: canonical INN -> aliases; combos: combination -> component INNs (collapsed, largest first, so
    BPaL + moxifloxacin reads as BPaLM, not BPaL). Two canonical forms carry structure (configs/grading.yaml):
    'a+b+c' is a named regimen (BPaL, TLD, Biktarvy) and expands to its member INNs; 'a|b' is a drug class
    ('tenofovir') kept as one token that stands for ONE of its members (see drugs_cover). Aliases starting with '~'
    are TB chain codes (see _chain_codes); a regimen spelled letter by letter ('B-Pa-L') is read (_spelled_regimens)."""
    t = " " + _norm_drug_text(text) + " "
    pairs = sorted(((_norm_drug_text(a), c) for c, al in synonyms.items() for a in [c, *al] if not a.startswith("~")),
                   key=lambda x: len(x[0]), reverse=True)
    found = _chain_codes(text, synonyms) | _spelled_regimens(text, synonyms)
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


# ------------------------------------------------------------------ category mentions (grader 1.2.0, revised)
# Since 1.2.0 a cat answer that names several categories is several values (grade.parse_values), so a category that
# is named but NOT stated must not count: "cao phân tử, không dùng Ringer lactate", "4HRE thay vì 4HR", "colloid
# rather than crystalloid", "HES 6% pha trong NaCl 0,9%" (a vehicle). One rule for every label (MoH, foreign,
# superseded, decoy), and a Vietnamese phrase for every English one (tests/test_grade_fixes.py, NEG_PAIRS):
#   - negation right before the mention, in its clause: "không (bao giờ/còn/nên/được/cần/phải) dùng/truyền/chọn/là/
#     khuyến cáo/chỉ định", "không phải (là)", "chứ không (phải)", "cũng không", "mà không có", "không kèm", "tránh
#     (dùng)", "thay vì", "thay cho", "ngoại trừ", "bỏ" ~ "not (use/give/recommended)", "no (longer)", "never", "nor",
#     "neither", "avoid(ing)", "without", "instead of", "rather than", "in place of", "except (for)", "do/should not
#     use", "don't use", "drop(ping)", "omit(ting)", "exclud(e|ing)"; up to 2 filler words ("dung dịch", "thuốc", "the").
#   - a negative predicate right after it (≤ 2 words between, no conjunction): "không (còn/nên/được/cần) dùng/khuyến
#     cáo/khuyến khích/chỉ định/ưu tiên/cần thiết/yêu cầu/bắt buộc/cho phép/phù hợp", bare "không nên/được/còn/cần",
#     "không phải (là) (lựa chọn) đầu tay/đầu tiên/hàng đầu/ưu tiên", "nên/cần tránh", "bị cấm", "chống chỉ định" ~
#     "not/no longer (be) recommended/used/needed/required/first-line/first choice/preferred/allowed...", "should/must
#     not", "avoided", "discouraged", "contraindicated", "prohibited", "banned".
#   - a vehicle ("trong", "pha/hòa trong/với", "in", "dissolved/diluted in", "mixed in/with") right before it, only when
#     ANOTHER category was named earlier in the same clause ("HES 6% trong NaCl 0,9%"; "a bolus in Ringer's lactate"
#     names Ringer's lactate).
#   A conditional or fallback mention ("chỉ dùng khi…", "only if refractory", "nếu không đáp ứng thì chuyển …") is NOT
#   a negation: it is a second value (grade.py), whichever category it names.
# Clauses end at ; : ! ? newline, a sentence or list comma/dot (not a decimal), a spaced dash (" - "), and "vì"/"bởi
# vì"/"because"/"since" (before: "Không - metamizol không nên dùng" read the second clause as negating the answer
# "không").
# Not checked (the atom's pattern carries its own logic): a match without letters or digits (look-ahead only); a match
# that itself holds a polarity word ("không", "no", "not", "avoid", "tránh", "cấm", "chống chỉ định"...) or is a bare
# yes/no answer ("có", "không", "yes", "no", "được"); a match of a pattern anchored at the start of the answer ("^",
# "(?s)^") that spans a clause boundary (a whole-answer classifier, e.g. P-dengue-03 colloid: "Colloid (dextran 40);
# HES is not recommended" is a colloid answer). An anchored match inside one clause is checked like any mention.
# Accents: the rules read the lower-case text WITH its accents, aligned 1:1 with the accent-free text the atom patterns
# read. An answer written with diacritics must write the Vietnamese negation with them ("chứa" is not "chưa", "nó" is
# not "no", "bộ" is not "bỏ"); an answer without any diacritic is read in its accent-free form ("khong dung").


def _fold(text: str) -> tuple[str, str]:
    """(accent-free, accent-kept) lower-case forms of the cleaned text, aligned character by character."""
    free, kept = [], []
    for c in clean(text).lower():
        f = strip_accents(c)
        free.append(f)
        kept.append(c * len(f))
    return "".join(free), "".join(kept)


_FILLER = (r"(?:dung\s+dịch|dịch|các|loại|phác\s+đồ|thuốc|dùng|sử\s+dụng|truyền|regimens?|drugs?|a|an|any|the|use|"
           r"using|give|giving|of|>|≥|trên|above|over)")
_NEG_PRE_ALTS = [
    r"\b(?:không|chẳng)(?:\s+(?:bao\s+giờ|còn|nên|được|cần|phải))*"
    r"(?:\s+(?:dùng|sử\s+dụng|truyền|chọn|cho|là|phải\s+là|khuyến\s+cáo|khuyến\s+nghị|chỉ\s+định|ưu\s+tiên|kê))?",
    r"\bchứ\s+không(?:\s+phải)?(?:\s+là)?", r"\bcũng\s+không", r"\bmà\s+không\s+(?:có|dùng|cần)",
    r"\bkhông\s+kèm(?:\s+theo)?", r"\b(?:(?:nên|cần|phải)\s+)?tránh(?:\s+(?:dùng|sử\s+dụng|truyền))?",
    r"\bthay\s+vì", r"\bthay\s+cho", r"\bngoại\s+trừ",
    r"\bnot(?:\s+(?:use|using|give|giving|with|recommended|recommend))?",
    r"\bno(?:\s+longer\s+(?:use|using|give|giving|recommended|recommend))?", r"\bnever(?:\s+(?:use|give))?",
    r"\bnor", r"\bneither", r"\bavoid(?:s|ed|ing)?", r"\bwithout", r"\binstead\s+of", r"\brather\s+than",
    r"\bin\s+place\s+of", r"\bexcept(?:\s+for)?",
    r"\b(?:do|does|did|should|must)\s+not\s+(?:use|give|recommend)",
    r"\b(?:don'?t|doesn'?t|shouldn'?t)\s+(?:use|give|recommend)",
    r"\b(?:drop|dropping|omit|omitting|exclude|excluding)"]
# only with diacritics: unaccented "chua" is also "chứa" (contains), "bo" also "bộ" (Bộ Y tế)
_NEG_PRE_ACCENTED = [r"\bchưa(?:\s+(?:nên|được|cần))*(?:\s+(?:dùng|sử\s+dụng|truyền))?", r"\b(?:loại\s+)?bỏ(?:\s+qua)?"]
_NEG_POST_SRC = (
    r"^[\w'’%-]*(?:\s+(?!(?:hoặc|hay|và|or|and|nor|rồi|sau|then|nhưng|but|nếu|if|khi|when)\b)[\w'’%-]+){0,2}?\s*"
    r"(?:\([^()]*\)\s*)?"
    r"(?:(?:is|are|should|must|be|been|was|were|now|currently|generally|usually|also|là|thì|cũng|sẽ|đều|bị|hiện|nay|"
    r"hiện\s+nay|hiện\s+tại|thường)\s+)*"
    r"(?:(?:not|no\s+longer)\s+(?:be\s+|been\s+)?(?:the\s+|a\s+)?(?:recommended|advised|indicated|used|given|preferred|"
    r"appropriate|needed|required|necessary|first[- ]line|first[- ]choice|encouraged|suggested|allowed|permitted)"
    r"|(?:should|must)\s+not|(?:be\s+)?avoided|discouraged|contraindicated|prohibited|banned"
    r"|không\s+(?:(?:nên|được|còn|cần|phải)\s+)*(?:dùng|sử\s+dụng|truyền|khuyến\s+cáo|khuyến\s+nghị|khuyến\s+khích|"
    r"chỉ\s+định|ưu\s+tiên|khuyên\s+dùng|cần\s+thiết|phù\s+hợp|yêu\s+cầu|đòi\s+hỏi|bắt\s+buộc|cho\s+phép)"
    r"|không\s+(?:nên|được|còn|cần)"
    r"|không\s+phải\s+(?:là\s+)?(?:(?:lựa\s+chọn|thuốc|phác\s+đồ)\s+)?(?:đầu\s+tay|đầu\s+tiên|hàng\s+đầu|ưu\s+tiên|"
    r"được\s+ưu\s+tiên)"
    r"|(?:nên|cần|phải)\s+tránh|bị\s+cấm|chống\s+chỉ\s+định)\b")
_CARRIER_SRC = (r"(?:\b(?:pha|hòa|hoà)\s+(?:trong|với|vào)|\btrong|\bdissolved\s+in|\bdiluted\s+in|\bmixed\s+(?:in|with)"
                r"|\bin)\s+(?:(?:dung\s+dịch|a|the)\s+)?(?:\d+(?:[.,]\d+)?\s*%\s*)?$")
_CUT_SRC = r"[;:!?\n]|[.,](?!\d)|\s-+\s|(?<!thay\s)\bvì\b|\bbởi\s+vì\b|\bbecause\b|\bsince\b"
_POLAR_ALTS = [r"không", r"chẳng", r"cấm", r"tránh", r"chống\s+chỉ\s+định", r"no", r"not", r"never", r"nor",
               r"avoid\w*", r"contraindicat\w*", r"without", r"instead", r"rather\s+than"]
_YES_NO_SRC = r"^\W*(?:có|được|yes|không|no)\W*$"


@dataclass(frozen=True)
class _Lex:
    cut: re.Pattern          # clause ends, parentheses included (text before a mention)
    cut_post: re.Pattern     # clause ends (text after a mention: "X (6%) không được dùng" keeps its parenthesis)
    neg_pre: re.Pattern
    neg_post: re.Pattern
    carrier: re.Pattern
    polar: re.Pattern
    yes_no: re.Pattern


def _lex(accented: bool) -> _Lex:
    def form(src: str) -> re.Pattern:
        return re.compile(src if accented else strip_accents(src))
    pre = _NEG_PRE_ALTS + (_NEG_PRE_ACCENTED if accented else [])
    polar = _POLAR_ALTS + (["chưa"] if accented else [])
    return _Lex(cut=form(_CUT_SRC + r"|[()]"), cut_post=form(_CUT_SRC),
                neg_pre=form("(?:" + "|".join(pre) + rf")\s+(?:{_FILLER}\s+){{0,2}}(?:\d+\s*)?$"),
                neg_post=form(_NEG_POST_SRC), carrier=form(_CARRIER_SRC),
                polar=form(r"\b(?:" + "|".join(polar) + r")\b"), yes_no=form(_YES_NO_SRC))


_LEX = {True: _lex(True), False: _lex(False)}
_ANCHORED = re.compile(r"(?:\(\?[a-zA-Z]+\))*\^")
_ALNUM = re.compile(r"[^\W_]")
# A mention pattern (not anchored at the start of the answer) matches inside one sentence or ';'-clause: "Có, gelatin
# có thể dùng thay thế; không dùng albumin" does not state "gelatin ... không dùng" (P-dengue-06 not_used reads
# 'gelatin[^.]{0,40}khong dung', which crossed the ';'). Commas do not cut here (a pattern may read "X, Y").
_HARD_CUT = re.compile(r"[;!?\n]|\.(?!\d)")
_WINDOW = 400          # characters read before/after a mention (a clause is shorter; keeps long outputs linear)
_MAX_CLAUSES = 50      # clauses re-read for an anchored whole-answer pattern (see _anchored_dismissed)


def _dismissed(s: str, span: tuple[int, int], lex: _Lex, others: list[tuple[int, int]]) -> bool:
    """A category mention (one clause) that does not state the category: negated or a vehicle (see above).
    s: the text the rules read (accent-kept when the answer has diacritics), aligned with the text the match is in."""
    a, b = span
    k = _ALNUM.search(s, a, b)
    if not k:
        return False                                  # look-ahead only: the pattern carries its own logic
    core = s[k.start():b]
    if lex.polar.search(core) or lex.yes_no.match(core):
        return False                                  # the pattern states the polarity itself
    w = max(0, a - _WINDOW)                           # the rules read a clause's width around the mention
    pre = lex.cut.split(s[w:a])[-1]
    post = lex.cut_post.split(s[b:b + _WINDOW])[0]
    if lex.neg_pre.search(pre) or lex.neg_post.match(post):
        return True
    pre = lex.cut_post.split(s[w:a])[-1]              # the vehicle's clause keeps parentheses: "Dextran (40) pha trong"
    c = lex.carrier.search(pre)
    if not c:
        return False
    start = a - len(pre)                              # clause start; the vehicle needs another category before it
    return any(start < e <= start + c.start() for _, e in others)


def _anchored_dismissed(pat: re.Pattern, t: str, s: str, span: tuple[int, int], lex: _Lex,
                        others: list[tuple[int, int]]) -> bool:
    """A match of a pattern anchored at the start ('(?s)^… .*KEYWORD' ends at the LAST mention it accepts). Inside one
    clause it is checked like any mention. Across clauses the pattern read the whole answer: the label stands unless
    the last clause's mention is dismissed AND the pattern accepts no mention before that clause (checked again the
    same way): "Colloid (dextran 40); HES is not recommended" is colloid, "Truyền dịch; HES không được dùng" is not.
    After _MAX_CLAUSES dismissed clauses (a degenerate, repeated output) the label stands, as the pattern read it."""
    for _ in range(_MAX_CLAUSES):
        a, b = span
        k = _ALNUM.search(s, a, b)
        cuts = list(lex.cut.finditer(s, k.start(), b)) if k else []
        if not cuts:
            return _dismissed(s, span, lex, others)
        last = cuts[-1]
        if not _dismissed(s, (last.end(), b), lex, others):
            return False
        m = pat.match(t[:last.start()])
        if not m:
            return True
        span = m.span()                               # the last mention the pattern accepts in the earlier clauses
    return False


def _segments(t: str) -> list[tuple[int, int]]:
    bounds = [0] + [m.end() for m in _HARD_CUT.finditer(t)] + [len(t)]
    return [(x, y) for x, y in zip(bounds, bounds[1:]) if y > x]


def parse_cats(text: str, options: dict[str, list[str]]) -> Cat:
    """Categories stated in the text (options: label -> regex patterns over the lower-case, accent-free text); a
    mention that is negated or a vehicle does not count (_dismissed; grader 1.2.0). A pattern anchored at the start
    ('^') reads the whole answer (_anchored_dismissed); any other pattern reads one sentence or ';'-clause at a time
    (_HARD_CUT)."""
    t, kept = _fold(text)
    accented = kept != t
    lex, s = _LEX[accented], (kept if accented else t)
    segs = _segments(t)
    hits = []                                         # (label, (start, end), compiled pattern if anchored)
    for lab, pats in options.items():
        for pat in (re.compile(strip_accents(x.lower())) for x in pats):
            if _ANCHORED.match(pat.pattern):
                hits += [(lab, m.span(), pat) for m in pat.finditer(t)]
            else:
                hits += [(lab, (x + m.start(), x + m.end()), None) for x, y in segs for m in pat.finditer(t[x:y])]
    keep: set[str] = set()
    named = [(other, o) for other, o, _ in hits if _ALNUM.search(t, *o)]
    others = {lab: [o for other, o in named if other != lab] for lab in options}
    for lab, span, anchored in hits:
        if lab in keep:
            continue
        if not (_anchored_dismissed(anchored, t, s, span, lex, others[lab]) if anchored
                else _dismissed(s, span, lex, others[lab])):
            keep.add(lab)
    return Cat(frozenset(keep))
