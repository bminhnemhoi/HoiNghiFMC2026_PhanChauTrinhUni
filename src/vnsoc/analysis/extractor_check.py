"""Blinded sheet for the manual check of the answer extractor (HG6.2; prereg §2.3, §3.1 item 7; rev-editor id 10).

The checker sees the question, the atom's reference values, the output and the parsed value. Hidden: the model, the
condition label, and the retrieval citation line ('NGUỒN:'/'SOURCE:'), which would reveal condition A2. The answer
language stays visible (it is the question's language). Items are shown in a seeded random order.
"""
from __future__ import annotations

import random
import re

SOURCE_LINE = re.compile(r"^\s*\**\s*(?:NGUỒN|Nguồn|NGUON|SOURCE|Source)\s*\**\s*[:：].*$", re.M)
THINK = re.compile(r"<think>.*?</think>", re.S | re.I)


def blind_output(raw: str) -> str:
    """Model output without reasoning blocks and without the citation line."""
    t = THINK.sub(" ", raw or "")
    t = SOURCE_LINE.sub("", t)
    return re.sub(r"\n{3,}", "\n\n", t).strip()


def check_sheet(rows: list[dict], seed: int = 20261001) -> list[dict]:
    """rows: dicts with run_id, question, reference, raw_output, parsed (plus any other keys, which are dropped).
    Returns the blinded rows in a seeded random order with a running item number; the key (item -> run_id) is kept
    by the first author separately and is not shown to the checker."""
    keep = ("run_id", "question", "reference", "parsed")
    out = [{**{k: r.get(k) for k in keep}, "output": blind_output(r.get("raw_output", ""))} for r in rows]
    random.Random(seed).shuffle(out)
    for i, r in enumerate(out, 1):
        r["item"] = i
    return out
