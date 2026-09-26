"""Render a ValueItem as MCQ option text in Vietnamese or English (numbers only from the item, never retyped)."""
from __future__ import annotations

UNIT_VI = {"ml/kg/h": "ml/kg/giờ", "mg/kg/day": "mg/kg/ngày", "day": "ngày", "month": "tháng", "year": "tuổi",
           "ug": "µg", "h": "giờ", "min": "phút", "week": "tuần"}
UNIT_EN = {"ml/kg/h": "mL/kg/h", "mg/kg/day": "mg/kg/day", "day": "days", "month": "months", "year": "years",
           "ug": "µg", "h": "hours", "min": "minutes", "week": "weeks"}
CMP = {">=": "≥ ", ">": "> ", "<=": "≤ ", "<": "< ", "=": ""}


def fmt_num(x: float, lang: str) -> str:
    s = f"{x:,.4f}".rstrip("0").rstrip(".")               # 5,000.25 style
    if lang == "vi":                                       # 5.000,25
        s = s.replace(",", "\x00").replace(".", ",").replace("\x00", ".")
    return s


def _unit(u: str | None, lang: str) -> str:
    if not u:
        return ""
    return (UNIT_VI if lang == "vi" else UNIT_EN).get(u, u)


def drug_name(inn: str, synonyms: dict, combos: dict, lang: str) -> str:
    if inn in combos and "+" in inn:
        return " + ".join(drug_name(p, synonyms, combos, lang) for p in combos[inn])
    if lang == "vi" and synonyms.get(inn):
        return synonyms[inn][0]
    return inn


def render_value(item: dict, atom: dict, lang: str, synonyms: dict | None = None, combos: dict | None = None) -> str:
    kind = atom["value_kind"]
    if kind == "num":
        u = _unit(item.get("unit") or atom.get("unit"), lang)
        lo, hi = float(item["lo"]), float(item["hi"])
        body = fmt_num(lo, lang) if lo == hi else f"{fmt_num(lo, lang)}–{fmt_num(hi, lang)}"
        return f"{CMP.get(item.get('cmp') or '=', '')}{body} {u}".strip()
    if kind == "bp":
        return f"{CMP.get(item.get('cmp') or '=', '')}{item['sys']:g}/{item['dia']:g} mmHg"
    if kind == "schedule":
        unit = item.get("unit", "day")
        seq = ", ".join(str(int(s)) for s in item["seq"])
        if lang == "vi":
            return f"ngày {seq}" if unit == "day" else f"{seq} {_unit(unit, 'vi')}"
        return f"days {seq}" if unit == "day" else f"{seq} {_unit(unit, 'en')}"
    if kind == "drugs":
        return " + ".join(drug_name(d, synonyms or {}, combos or {}, lang) for d in item["key_drugs"])
    if kind == "cat":
        return item.get("text") or item["label"]
    raise ValueError(kind)
