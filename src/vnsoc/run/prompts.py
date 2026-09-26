"""Prompts for every condition, built ONLY from configs/conditions.yaml (pre-registered wording, proposal §4.4, §5.7).

The country cue of A1 is the text of the A1 template before "{question}", so MCQs at A1 carry exactly the same cue.
Questions are stored sentence-case; after a cue the first letter is lower-cased (acronyms such as "HbA1c" kept).
request_id = "<question_id>|<condition>|<model_key>|<sample>" (question_id itself contains '|': split from the right).
A3 names the section by `section_label(atom)` (the path only, without the extractor's pointers to the answer line).
"""
from __future__ import annotations

import re
import unicodedata
from functools import lru_cache

import yaml

from vnsoc.paths import paths


@lru_cache(maxsize=4)
def conditions(root=None) -> dict:
    return yaml.safe_load((paths(root).configs / "conditions.yaml").read_text(encoding="utf-8"))


def doc_label(guideline: str, lang: str) -> str:
    """'2760/2023' -> 'Quyết định 2760/QĐ-BYT (2023)'; 'TT51/2017' -> 'Thông tư 51/2017/TT-BYT'."""
    g = guideline.replace(" ", "")
    if g.upper().startswith("TT"):
        num, year = g[2:].split("/")
        return f"{'Thông tư' if lang == 'vi' else 'Circular'} {num}/{year}/TT-BYT"
    num, year = g.split("/")
    return f"{'Quyết định' if lang == 'vi' else 'Decision'} {num}/QĐ-BYT ({year})"


# A pointer word names a line of the page only when a marker follows: a quote, one letter ('điểm a'), a number or an
# upper-case word ('cột SXHD nặng'); 'Thời điểm khởi trị', 'thuốc hàng đầu' are titles, not pointers.
_PTR = r"(?i:điểm|tiêu chí|ô|dòng|cột|hàng)\s+(?=['\"“‘]|[a-zđ](?![^\W\d_])|\d|[A-ZĐ])"
_NOTE_WORDS = re.compile(r"(?<!\w)(?:(?i:cùng trang|xem|tiếp)(?!\w)|" + _PTR + ")")
_NOTE_START = re.compile(r"\s*(?i:điểm|tiêu chí|ô|dòng|cột|hàng)(?!\w)")
_QUOTED = re.compile(r"\s*(?:'[^']*'|\"[^\"]*\"|“[^”]*”|‘[^’]*’)")
_POINTER = re.compile(r"(?:\s*[,;]\s*|\s+)(?<!\w)" + _PTR + r"(?:'[^']*'|\"[^\"]*\"|“[^”]*”|‘[^’]*’|[^,;'\"“‘])*")
_PATH = re.compile(r"(?<!\w)(?i:mục|chương|phần|phụ lục|điều|khoản)\s+[\dIVXLC]")
SECTION_MAX = 120


def _drop_note_parens(s: str) -> str:
    """Remove '( … )' groups (balanced) that follow a space and hold an extractor's note: a digit or a pointer word
    ('cùng trang', 'dòng', 'cột', 'ô', 'điểm', 'tiêu chí', 'xem', 'tiếp'). Numbering such as 'III.2.2.1(a)' stays."""
    out, i = [], 0
    while i < len(s):
        if s[i] == "(" and (i == 0 or s[i - 1].isspace()):
            depth, j = 0, i
            while j < len(s):
                depth += {"(": 1, ")": -1}.get(s[j], 0)
                if depth == 0:
                    break
                j += 1
            inner = s[i + 1:j]
            if j < len(s) and (any(c.isdigit() for c in inner) or _NOTE_WORDS.search(inner)
                               or _NOTE_START.match(inner)):
                while out and out[-1].isspace():
                    out.pop()
                i = j + 1
                continue
        out.append(s[i])
        i += 1
    return "".join(out)


def section_label(atom: dict, max_len: int = SECTION_MAX) -> str:
    """Clean section label for {section} of the A3 prompt: the chapter/section/appendix path of atom['section']
    without the extractor's notes — note parentheses ('(cùng trang: … Bảng 1 …)'), quoted titles, pointers to the
    answer line ('điểm a', 'tiêu chí c', 'ô …', 'dòng …', 'cột …'; not 'Thời điểm …' or 'hàng đầu') and em-dash
    annotations ('— Phác đồ BPaL'; an em-dash part that continues the path, '— Điều trị, mục 3.2 …', is kept);
    at most `max_len` characters (cut at a word, marked '…')."""
    s = unicodedata.normalize("NFC", atom.get("section") or "")
    s = _drop_note_parens(s)
    s = _POINTER.sub("", s)                              # before the quotes: "ô 'TIÊM BẮP'" goes as a whole
    s = _QUOTED.sub("", s)
    head, *rest = s.split("—")
    s = " — ".join([head.strip()] + [r.strip() for r in rest if _PATH.search(r)])
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"\s+([,;])", r"\1", s)
    s = re.sub(r"([,;])(?:\s*[,;])+", r"\1", s).strip(" ,;:–-")
    if len(s) > max_len:
        s = s[:max_len - 1].rsplit(" ", 1)[0].rstrip(" ,;:–-") + "…"
    return s


def _after_cue(q: str) -> str:
    if len(q) > 1 and q[0].isupper() and not q[1].isupper():
        return q[0].lower() + q[1:]
    return q


def cue(lang: str, root=None) -> str:
    return conditions(root)["prompts"][lang]["A1"].split("{question}")[0]


def short_prompt(question: dict, condition: str, atom: dict | None = None, passage: str | None = None,
                 root=None) -> str:
    P = conditions(root)["prompts"][question["language"]]
    q = question["text"].strip()
    fill = {"answer_line": P["answer_line"], "question": q}
    if condition in ("A1", "A2", "A3", "A4", "A5"):
        fill["question"] = _after_cue(q)
    if condition == "A3":
        if not (atom and passage):
            raise ValueError("A3 cần atom + đoạn oracle")
        fill.update(doc=doc_label(atom["guideline"], question["language"]), section=section_label(atom),
                    passage=passage)
    elif condition in ("A2", "A4", "A5"):
        raise NotImplementedError(f"{condition}: cần đoạn truy xuất/chương (T5.1, T5.3)")
    elif condition == "A6":
        fill["vignette"] = q
    return P[condition].format(**fill)


def mcq_prompt(question: dict, condition: str = "A1", root=None) -> str:
    P = conditions(root)["prompts"][question["language"]]
    stem = question["text"].strip()
    if condition == "A1":
        stem = cue(question["language"], root) + _after_cue(stem)
    elif condition != "A0":
        raise ValueError(f"trắc nghiệm chỉ chạy ở A0/A1, không {condition}")
    opts = "\n".join(f"{k}. {v}" for k, v in sorted(question["options"].items()))
    return P["mcq"].format(stem=stem, options=opts)


def messages(question: dict, condition: str, atom: dict | None = None, passage: str | None = None,
             root=None) -> list[dict]:
    text = (mcq_prompt(question, condition, root) if question["format"] == "mcq"
            else short_prompt(question, condition, atom, passage, root))
    return [{"role": "user", "content": text}]


def request_id(question_id: str, condition: str, model_key: str, sample: int = 0) -> str:
    return f"{question_id}|{condition}|{model_key}|{sample}"


def parse_request_id(rid: str) -> tuple[str, str, str, int]:
    qid, cond, mk, s = rid.rsplit("|", 3)
    return qid, cond, mk, int(s)
