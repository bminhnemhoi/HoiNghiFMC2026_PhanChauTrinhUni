"""Render a ValueItem as MCQ option text in Vietnamese or English (numbers only from the item, never retyped).

Display rules (pilot review 2026-09-26): at most 4 significant digits and no trailing zeros (the integer part is never
rounded); unit "year" reads "tuổi" (age) or "năm" (slot_type duration) in Vietnamese; a whole number of months that is
not a whole number of years reads "3 tuổi 4 tháng" / "3 years 4 months"; English singular for 1 ("1 day");
dimensionless indices (unit "index", e.g. APRI) carry no unit; drug names come from configs/drug_display.yaml
(display only, never used for grading; fallback: the INN key).
"""
from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal
from functools import lru_cache

import yaml

UNIT_VI = {"ml/kg/h": "ml/kg/giờ", "mg/kg/day": "mg/kg/ngày", "day": "ngày", "month": "tháng", "year": "tuổi",
           "ug": "µg", "h": "giờ", "min": "phút", "week": "tuần"}
UNIT_EN = {"ml/kg/h": "mL/kg/h", "mg/kg/day": "mg/kg/day", "day": "days", "month": "months", "year": "years",
           "ug": "µg", "h": "hours", "min": "minutes", "week": "weeks"}
SINGULAR_EN = {"days": "day", "months": "month", "years": "year", "weeks": "week", "hours": "hour",
               "minutes": "minute"}
NO_UNIT = {"index"}                                        # dimensionless scores (APRI...)
CMP = {">=": "≥ ", ">": "> ", "<=": "≤ ", "<": "< ", "=": ""}


def sig_exp(x: float, sig: int, nd: int | None = None, keep_int: bool = False) -> int:
    """Decimal exponent of the rounding step for x: `sig` significant digits, never finer than 10**-nd (nd = decimals
    of the source values); keep_int: never coarser than 1 (the integer part is kept)."""
    exp = Decimal(repr(float(x))).adjusted() - sig + 1 if x else 0
    if nd is not None:
        exp = max(exp, -nd)
    if keep_int:
        exp = min(exp, 0)
    return exp


def round_exp(x: float, exp: int) -> float:
    """x rounded half-up to a multiple of 10**exp."""
    return float(Decimal(repr(float(x))).quantize(Decimal(1).scaleb(exp), rounding=ROUND_HALF_UP))


def nice_round(x: float, sig: int, nd: int | None = None, keep_int: bool = False) -> float:
    """x rounded half-up to `sig` significant digits (see sig_exp). Shared by fmt_num (4 digits, integer part kept)
    and mcq.rule_filler (2 digits, not finer than the source values)."""
    x = float(x)
    if x == 0 or x != x or x in (float("inf"), float("-inf")):
        return x
    return round_exp(x, sig_exp(x, sig, nd, keep_int))


def fmt_num(x: float, lang: str) -> str:
    x = float(x)
    nd = max(0, -sig_exp(x, 4, keep_int=True)) if x else 0
    s = f"{nice_round(x, 4, keep_int=True):,.{nd}f}"                         # 5,000.25 style
    s = s.rstrip("0").rstrip(".") if "." in s else s
    if lang == "vi":                                                         # 5.000,25
        s = s.replace(",", "\x00").replace(".", ",").replace("\x00", ".")
    return s


def _unit(u: str | None, lang: str, slot_type: str | None = None, one: bool = False) -> str:
    if not u or u in NO_UNIT:
        return ""
    if u == "year" and lang == "vi":
        return "năm" if slot_type == "duration" else "tuổi"
    s = (UNIT_VI if lang == "vi" else UNIT_EN).get(u, u)
    return SINGULAR_EN.get(s, s) if (lang == "en" and one) else s


def _whole(x: float, eps: float = 1e-6) -> bool:
    return abs(x - round(x)) < eps


def _years_months(x: float, lang: str, slot_type: str | None) -> str:
    """40 months as years -> '3 tuổi 4 tháng' / '3 năm 4 tháng' / '3 years 4 months'."""
    y, m = divmod(int(round(x * 12)), 12)
    parts = []
    if lang == "vi":
        if y:
            parts.append(f"{y} {'năm' if slot_type == 'duration' else 'tuổi'}")
        if m:
            parts.append(f"{m} tháng")
    else:
        if y:
            parts.append(f"{y} year{'' if y == 1 else 's'}")
        if m:
            parts.append(f"{m} month{'' if m == 1 else 's'}")
    return " ".join(parts) or "0"


def _amount(lo: float, hi: float, unit: str | None, lang: str, slot_type: str | None) -> str:
    if unit == "year" and not (_whole(lo) and _whole(hi)) and _whole(lo * 12) and _whole(hi * 12):
        a, b = _years_months(lo, lang, slot_type), _years_months(hi, lang, slot_type)
        return a if lo == hi else f"{a} – {b}"
    a, b = fmt_num(lo, lang), fmt_num(hi, lang)
    body = a if a == b else f"{a}–{b}"                  # 1.0 and 1.0000000001 print as one value
    return f"{body} {_unit(unit, lang, slot_type, one=(body == '1'))}".strip()


@lru_cache(maxsize=4)
def drug_display(root=None) -> dict:
    """configs/drug_display.yaml: INN key -> {"vi": ..., "en": ...} (display names; {} when the file is absent)."""
    from vnsoc.paths import paths

    f = paths(root).configs / "drug_display.yaml"
    return (yaml.safe_load(f.read_text(encoding="utf-8")) or {}) if f.exists() else {}


def drug_name(inn: str, synonyms: dict, combos: dict, lang: str, display: dict | None = None) -> str:
    """Display name of one key_drugs entry; 'a+b' combos are shown part by part. `synonyms` (grading aliases) are no
    longer used for display: the first alias is often a French form or an abbreviation ('clindamycine', 'tdf')."""
    if inn in combos and "+" in inn:
        return " + ".join(drug_name(p, synonyms, combos, lang, display) for p in combos[inn])
    d = (drug_display() if display is None else display).get(inn) or {}
    return d.get(lang) or inn


def render_value(item: dict, atom: dict, lang: str, synonyms: dict | None = None, combos: dict | None = None,
                 display: dict | None = None) -> str:
    kind = atom["value_kind"]
    if kind == "num":
        unit = item.get("unit") or atom.get("unit")
        lo, hi = float(item["lo"]), float(item["hi"])
        if item.get("unit") and atom.get("unit") and item["unit"] != atom["unit"]:
            from vnsoc.match.decoys import in_atom_unit

            n = in_atom_unit(item, atom)                 # e.g. 0.01 mg/kg x 10 kg -> 100 ug, same unit as the stem
            if n is not None:
                lo, hi, unit = n.lo, n.hi, atom["unit"]
        body = _amount(lo, hi, unit, lang, atom.get("slot_type"))
        return f"{CMP.get(item.get('cmp') or '=', '')}{body}".strip()
    if kind == "bp":
        return f"{CMP.get(item.get('cmp') or '=', '')}{fmt_num(item['sys'], lang)}/{fmt_num(item['dia'], lang)} mmHg"
    if kind == "schedule":
        unit = item.get("unit", "day")
        seq = ", ".join(str(int(s)) for s in item["seq"])
        one = [float(x) for x in item["seq"]] == [1.0]
        if lang == "vi":
            return f"ngày {seq}" if unit == "day" else f"{seq} {_unit(unit, 'vi')}"
        if unit == "day":
            return f"day{'' if one else 's'} {seq}"
        return f"{seq} {_unit(unit, 'en', one=one)}"
    if kind == "drugs":
        return " + ".join(drug_name(d, synonyms or {}, combos or {}, lang, display) for d in item["key_drugs"])
    if kind == "cat":
        return item.get("text") or item["label"]         # MCQ: the writer's option_text is required (qgen.build)
    raise ValueError(kind)
