"""Prompts for every condition, built ONLY from configs/conditions.yaml (pre-registered wording, proposal §4.4, §5.7).

The country cue of A1 is the text of the A1 template before "{question}", so MCQs at A1 carry exactly the same cue.
Questions are stored sentence-case; after a cue the first letter is lower-cased (acronyms such as "HbA1c" kept).
request_id = "<question_id>|<condition>|<model_key>|<sample>" (question_id itself contains '|': split from the right).
"""
from __future__ import annotations

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
        fill.update(doc=doc_label(atom["guideline"], question["language"]), section=atom["section"], passage=passage)
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
