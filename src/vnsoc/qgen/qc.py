"""Code QC for questions (skill question-generation steps 2 and 5):
- leak: the question text must not state the MoH, foreign, superseded or decoy value (explicit-unit values only, so
  an age like "30 tuổi" is not mistaken for "30 U/L");
- population: every number in the atom's population description appears in the question;
- translation: VI and EN versions carry the same numbers and the same negation polarity (back-translation by code).
"""
from __future__ import annotations

import re

from vnsoc import normalize_vi as nv
from vnsoc.grade import classify_value, parse_values

NEG_VI = re.compile(r"\b(?:không|chưa|ngoại\s+trừ|trừ\s+khi)\b", re.I)
NEG_EN = re.compile(r"\b(?:no|not|without|except|never|unless|non-)\b", re.I)


def numbers(text: str, lang: str) -> list[float]:
    t = nv.strip_citations(nv.clean(text))
    return sorted(round(nv.parse_number(m.group(0), lang), 6) for m in re.finditer(nv.NUM_RE, t))


def leak_issues(text: str, atom: dict, lang: str, synonyms=None, combos=None) -> list[str]:
    a = dict(atom, tolerance=0.0)
    out = []
    for flag, v in parse_values(text, a, lang, synonyms, combos):
        if flag == "assumed":
            continue
        c = classify_value(v, a)
        if c["vn"]:
            out.append("lộ giá trị Bộ Y tế")
        if c["foreign"]:
            out.append("lộ giá trị nước ngoài " + ",".join(c["foreign"]))
        if c["superseded"]:
            out.append("lộ giá trị bản cũ")
        if c["decoy"]:
            out.append("lộ giá trị mồi")
    return sorted(set(out))


def population_issues(text: str, atom: dict, lang: str, pop_lang: str = "vi") -> list[str]:
    want = set()
    for v in (atom.get("population") or {}).values():
        want |= set(numbers(str(v), pop_lang))
    have = set(numbers(text, lang))
    missing = sorted(want - have)
    return [f"thiếu số của quần thể {missing}"] if missing else []


def translation_issues(vi: str, en: str) -> list[str]:
    out = []
    a, b = numbers(vi, "vi"), numbers(en, "en")
    if a != b:
        out.append(f"số khác nhau VI {a} ≠ EN {b}")
    if bool(NEG_VI.search(vi)) != bool(NEG_EN.search(en)):
        out.append("phủ định không khớp giữa VI và EN")
    return out
