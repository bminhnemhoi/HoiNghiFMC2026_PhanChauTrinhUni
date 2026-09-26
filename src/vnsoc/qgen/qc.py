"""Code QC for questions (skill question-generation steps 2 and 5):
- leak: the question text must not state the MoH, foreign, superseded or decoy value (explicit-unit values only, so
  an age like "30 tuổi" is not mistaken for "30 U/L");
- population: every number in the atom's population description appears in the question, AND every categorical
  population attribute listed in the atom's `required_terms` (HBeAg status, compensated vs severe shock, clinic vs
  home measurement, trimester, G6PD, level of care...) is stated by one of its VI/EN synonyms;
- translation: VI and EN versions carry the same numbers and the same negation polarity (back-translation by code);
- A3 passage: which non-MoH values (foreign, superseded, decoy, MoH value of a neighbouring context) the oracle
  passage itself states (`passage_alt_values`; QC-table column passage_has_alt_value, flagged for a manual re-check
  before the freeze and excluded in the registered H3 sensitivity analysis).
"""
from __future__ import annotations

import re
import unicodedata

from vnsoc import normalize_vi as nv
from vnsoc.grade import _gap, classify_value, matches, parse_values

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

def required_terms_issues(text: str, atom: dict, lang: str) -> list[str]:
    """Every key of atom['required_terms'] ({key: {'vi': [...], 'en': [...]}}) must be stated in the question by at
    least one of its synonyms for `lang` (NFC, case-insensitive, whole words)."""
    t = unicodedata.normalize("NFC", text or "").casefold()
    missing = []
    for key, syn in (atom.get("required_terms") or {}).items():
        words = [unicodedata.normalize("NFC", w).casefold() for w in (syn or {}).get(lang) or []]
        if not any(re.search(r"(?<!\w)" + re.escape(w) + r"(?!\w)", t) for w in words if w):
            missing.append(key)
    return [f"thiếu thuộc tính quần thể bắt buộc: {', '.join(missing)}"] if missing else []


def passage_alt_values(passage: str, atom: dict, lang: str = "vi", synonyms=None, combos=None) -> list[str]:
    """Non-MoH values stated by an A3 oracle passage (explicit-unit values, tolerance 0): 'foreign:<SYS>',
    'superseded', 'decoy', 'neighbour' (MoH value of a neighbouring context, Atom.moh_neighbour). An item that lies
    inside the MoH set is never flagged. Empty list = the passage states only MoH values."""
    a = dict(atom, tolerance=0.0)
    vn = atom.get("vn") or []

    def outside(it) -> bool:
        return all(_gap(v, it, a) > 0 for v in vn)

    cats = [(f"foreign:{f['system']}", it) for f in atom.get("foreign") or [] for it in f["values"]]
    cats += [("superseded", it) for s in atom.get("superseded") or [] for it in s["values"]]
    cats += [("decoy", it) for it in atom.get("decoy") or []]
    cats += [("neighbour", it) for nb in atom.get("moh_neighbour") or [] for it in nb.get("values") or []]
    out = set()
    for flag, v in parse_values(passage, a, lang, synonyms, combos):
        if flag == "assumed":
            continue
        for name, it in cats:
            if outside(it) and matches(v, it, a)[0]:
                out.add(name)
    return sorted(out)
