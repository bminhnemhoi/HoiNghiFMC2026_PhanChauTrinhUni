"""Code QC for questions (skill question-generation steps 2 and 5):
- leak: the question text must not state the MoH, foreign, superseded or decoy value (explicit-unit values only, so
  an age like "30 tuổi" is not mistaken for "30 U/L");
- population: every number in the atom's population description appears in the question, AND every categorical
  population attribute listed in the atom's `required_terms` (HBeAg status, compensated vs severe shock, clinic vs
  home measurement, trimester, G6PD, level of care...) is stated by one of its VI/EN synonyms;
- translation: VI and EN versions carry the same numbers and the same negation polarity (back-translation by code);
- A3 passage: which non-MoH values (foreign, superseded, decoy, MoH value of a neighbouring context) the oracle
  passage itself states (`passage_alt_values`; QC-table column passage_has_alt_value, flagged for a manual re-check
  before the freeze and excluded in the registered H3 sensitivity analysis);
- MCQ options (`option_issues`): no word that names a source or a role (i), the writer's drugs/cat/schedule option
  texts read back by the grader's own parser as exactly the option's role (ii; a filler text must match no recorded
  source, and may be unreadable), similar lengths (iii), English options without Vietnamese letters (iv), four
  different texts per language (v), no drug option rendered from a regimen's discriminating key_drugs alone
  (a fragment such as "cycloserine" for "Bdq-Lzd-Cfz-Cs"; the writer's option_text is then required) (vi);
  the writer's option_text given in both languages with the same numbers (`option_text_issues`).
"""
from __future__ import annotations

import re
import unicodedata

from vnsoc import normalize_vi as nv
from vnsoc.grade import FOREIGN_NAMES, _gap, classify_value, matches, parse_values

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


POP_NUMERIC_KEYS = re.compile(r"^(?:age|tuoi|tuổi|weight|weight_kg|can_nang|cân_nặng|gestational_age|gestation|trimester|"
                              r"pregnancy_week|age_months|age_years)$", re.I)


def _value_numbers(atom: dict) -> set[float]:
    """Numbers of every recorded value (MoH, foreign, superseded, decoy): never demanded in a question (would leak)."""
    items = list(atom.get("vn") or []) + list(atom.get("decoy") or [])
    items += [it for f in atom.get("foreign") or [] for it in f["values"]]
    items += [it for s in atom.get("superseded") or [] for it in s["values"]]
    out = set()
    for it in items:
        for k in ("lo", "hi", "sys", "dia"):
            if it.get(k) is not None:
                out.add(round(float(it[k]), 6))
        out |= {round(float(x), 6) for x in it.get("seq") or []}
    return out


def population_issues(text: str, atom: dict, lang: str, pop_lang: str = "vi") -> list[str]:
    """Numbers of the QUANTITATIVE population keys (age, weight, gestational age...) must appear in the question.
    Descriptive keys (severity, setting, history...) often quote incidental numbers or even the answer, so they are
    checked by `required_terms` and by the reviewer, not here; numbers equal to a recorded value are never demanded."""
    want = set()
    for k, v in (atom.get("population") or {}).items():
        if POP_NUMERIC_KEYS.match(str(k)):
            want |= set(numbers(str(v), pop_lang))
    want -= _value_numbers(atom)
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


# ------------------------------------------------------------------------------ MCQ options
OPTION_HINT = re.compile(
    r"(?<![A-Za-z])(?:WHO|CDC|ADA|ESC|NICE|AASLD|EASL|UK|US|EU|NHS|BYT|MoH|QĐ|TT-BYT)(?![A-Za-z])"
    r"|(?<![^\W\d_])Anh(?![^\W\d_])"
    r"|(?i:(?<![^\W\d_])(?:mồi|nhiễu|decoy|filler|mỹ|hoa\s+k[ỳì]|ch[âa]u\s+[âa]u|bộ\s+y\s+tế|việt\s+nam|viet\s*nam(?:ese)?|"
    r"moh|ministry(?:\s+of\s+health)?|europe(?:an)?|england|english\s+guidance|brit(?:ish|ain)|america(?:n)?|"
    r"nước\s+ngoài|foreign|khuyến\s+(?:cáo|nghị)|recommend(?:ed|s|ations?)?|hướng\s+dẫn|guidelines?|"
    r"cũ|trước\s+đây|bản\s+trước|previous(?:ly)?|former(?:ly)?|outdated|superseded|"
    r"quyết\s+định\s+(?:số\s+)?\d+|thông\s+tư\s+(?:số\s+)?\d+)(?![^\W\d_]))"
    r"|(?<![\d.,])\d{2,5}/(?:19|20)\d{2}(?!\d)")        # document numbers such as 2760/2023 (not 140/90, 1/2000)


def _nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s or "")


def option_hint_issues(text: str) -> list[str]:
    """(i) words that name a source or a role: mồi/decoy/filler, WHO/CDC/..., Mỹ/Anh/châu Âu/EU/NHS (VI and EN),
    Bộ Y tế/Việt Nam/Ministry of Health, khuyến cáo/khuyến nghị/hướng dẫn/guideline, cũ/previous (a version cue),
    document numbers and labels (2760/2023, QĐ, Quyết định 2760)."""
    t = _nfc(text)
    hits = sorted({m.group(0) for m in OPTION_HINT.finditer(t)} | {m.group(0) for m in FOREIGN_NAMES.finditer(t)})
    return [f"phương án có từ gợi nguồn/vai trò: {', '.join(hits)}"] if hits else []


def _as_parsed(item: dict, kind: str):
    if kind == "drugs":
        return nv.Drugs(frozenset(item["key_drugs"]))
    if kind == "schedule":
        return nv.Schedule(tuple(item["seq"]), item.get("unit", "day"))
    return nv.Cat(frozenset([item["label"]]))


def _cls_key(c: dict) -> tuple:
    return bool(c["vn"]), tuple(sorted(set(c["foreign"]))), tuple(sorted(set(c["superseded"]))), bool(c["decoy"])


NO_SOURCE = (False, (), (), False)


def option_role_issues(text: str, slot: str, item: dict, atom: dict, lang: str, synonyms=None,
                       combos=None) -> list[str]:
    """(ii) drugs/cat/schedule: the option text, parsed by vnsoc.grade.parse_values, is classified exactly like the
    option's own value (vn -> MoH and no conflicting foreign; foreign -> that system; superseded; decoy). A filler
    text must match no recorded source; it may be unreadable to the grader (a cat atom's cat_options hold only the
    labels of its sources, so a filler such as 'fresh frozen plasma' cannot be parsed, and need not be)."""
    kind = atom["value_kind"]
    if kind not in ("drugs", "cat", "schedule"):
        return []
    vals = [v for f, v in parse_values(text, atom, lang, synonyms, combos) if f == "ok"]
    if slot == "filler":
        if any(_cls_key(classify_value(v, atom)) != NO_SOURCE for v in vals):
            return [f"phương án filler ({lang}) được bộ chấm xếp vào một nguồn đã ghi"]
        return []
    if not vals:
        return [f"bộ chấm không đọc lại được phương án {slot} ({lang})"]
    want = _cls_key(classify_value(_as_parsed(item, kind), atom))
    got = [_cls_key(classify_value(v, atom)) for v in vals]
    if any(g != want for g in got):
        names = ("vn", "foreign", "superseded", "decoy")
        return [f"phương án {slot} ({lang}) được bộ chấm xếp {dict(zip(names, got[0]))}, "
                f"cần {dict(zip(names, want))}"]
    return []


def option_length_issues(texts: list[str]) -> list[str]:
    """(iii) longest option (words) <= 2 x shortest + 3, so the MoH option is not the long, specific one."""
    n = [len(t.split()) for t in texts]
    return [f"độ dài phương án lệch ({min(n)}–{max(n)} từ)"] if n and max(n) > 2 * min(n) + 3 else []


VI_LETTER = re.compile(r"[đĐ]|[^\W\d_][\u0302\u0306\u031b]|[^\W\d_]\u031b?[\u0309\u0323]")   # NFD: â ă ơ, hook above, dot below
TONE = re.compile(r"[\u0300\u0301\u0303]")


def option_script_issues(text: str, lang: str) -> list[str]:
    """(iv) an English option written in Vietnamese (e.g. a cat item's Vietnamese text): a letter only Vietnamese
    uses (đ, circumflex/breve/horn, hook above, dot below), or two words with tone marks (one accented loanword such
    as 'Guillain-Barré' passes)."""
    if lang != "en":
        return []
    t = unicodedata.normalize("NFD", text)
    vi = VI_LETTER.search(t) or sum(bool(TONE.search(w)) for w in t.split()) >= 2
    return ["phương án EN có chữ tiếng Việt"] if vi else []


def _norm_option(t: str) -> str:
    return re.sub(r"\s+", " ", _nfc(t).casefold()).strip(" .;,")


def option_distinct_issues(texts: list[str]) -> list[str]:
    """(v) the displayed texts differ pairwise (e.g. two writer texts copied alike, or two values that print the same
    after rounding)."""
    counts: dict[str, int] = {}
    for t in texts:
        counts[_norm_option(t)] = counts.get(_norm_option(t), 0) + 1
    dup = sorted(k for k, n in counts.items() if n > 1)
    return [f"hai phương án hiển thị giống nhau: {', '.join(dup)}"] if dup else []


def drug_fragment_issues(slot: str, item: dict, atom: dict, synonyms=None, combos=None) -> list[str]:
    """(vi) a drugs option rendered from key_drugs whose recorded text names more drugs (the key is only the
    discriminating part of a regimen: 'cycloserine' for 'Bdq-Lzd-Cfz-Cs'): the writer's option_text is required. A
    class token covering a key drug ('tenofovir' for TDF) is not an extra drug."""
    if atom["value_kind"] != "drugs" or not item.get("text"):
        return []
    key = set(item["key_drugs"])
    names = nv.parse_drugs(item["text"], synonyms or {}, combos or {}).names
    extra = sorted(n for n in names if n not in key and not ("|" in n and set(n.split("|")) & key))
    if not extra:
        return []
    return [f"phương án {slot} tự render từ key_drugs chỉ là mảnh phác đồ (văn bản gốc còn {', '.join(extra)}): "
            f"cần option_text"]


def option_text_issues(option_text: dict | None) -> list[str]:
    """The writer's option_text: every slot in both languages, with the same numbers in VI and EN."""
    out = []
    for slot, tx in (option_text or {}).items():
        tx = tx or {}
        miss = [lang for lang in ("vi", "en") if not (tx.get(lang) or "").strip()]
        if miss:
            out.append(f"option_text {slot} thiếu bản {'/'.join(miss)}")
            continue
        a, b = numbers(tx["vi"], "vi"), numbers(tx["en"], "en")
        if a != b:
            out.append(f"option_text {slot}: số khác nhau VI {a} ≠ EN {b}")
    return out


def option_issues(opts: list[tuple[str, str, dict]], texts: list[str], by_writer: set[str], atom: dict, lang: str,
                  synonyms=None, combos=None) -> list[str]:
    """QC of the 4 displayed options of one language (slot order): (i), (iii), (iv), (v) for every option; (ii) for
    the writer's drugs/cat/schedule texts; (vi) for drug options rendered from key_drugs."""
    out = option_length_issues(texts) + option_distinct_issues(texts)
    for (slot, _, item), t in zip(opts, texts):
        out += option_hint_issues(t) + option_script_issues(t, lang)
        if slot in by_writer:
            out += option_role_issues(t, slot, item, atom, lang, synonyms, combos)
        else:
            out += drug_fragment_issues(slot, item, atom, synonyms, combos)
    return list(dict.fromkeys(out))
