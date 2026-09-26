"""A3 oracle passages (proposal §4.4; skill question-generation step 6): 150–300 words of the official page text
around the atom's span, cut at sentence boundaries, never mid-sentence; the span is always fully included."""
from __future__ import annotations

import re

from vnsoc.extract.verify_span import norm, page_text, pdf_path

SENT_END = re.compile(r"(?<=[.;:!?])\s+(?=[A-ZÀ-Ỹ0-9•\-–(])")


def _sentences(text: str) -> list[tuple[int, int]]:
    out, start = [], 0
    for m in SENT_END.finditer(text):
        out.append((start, m.start()))
        start = m.end()
    out.append((start, len(text)))
    return [(a, b) for a, b in out if b > a]


def oracle_passage(page_txt: str, span: str, min_words: int = 150, max_words: int = 300) -> str:
    text, s = norm(page_txt), norm(span)
    i = text.find(s)
    if i < 0:
        raise ValueError("span không có trong trang")
    sents = _sentences(text)
    first = next(k for k, (a, b) in enumerate(sents) if b > i)
    last = next(k for k, (a, b) in enumerate(sents) if b >= i + len(s))
    lo, hi = first, last

    def words(a, b):
        return len(text[sents[a][0]:sents[b][1]].split())

    while words(lo, hi) < min_words and (lo > 0 or hi < len(sents) - 1):
        grow_hi = hi < len(sents) - 1 and (lo == 0 or (hi - last) <= (first - lo))
        cand = (lo, hi + 1) if grow_hi else (lo - 1, hi)
        if words(*cand) > max_words and words(lo, hi) >= min_words // 2:
            break
        lo, hi = cand
    return text[sents[lo][0]:sents[hi][1]].strip()


def atom_passage(atom: dict, root=None, min_words: int = 150, max_words: int = 300) -> str:
    return oracle_passage(page_text(pdf_path(atom["guideline"], root), int(atom["page"])), atom["span"],
                          min_words, max_words)
