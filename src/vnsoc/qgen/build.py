"""Assemble the question set from atoms + per-atom wording drafts, with code QC (T1.3 pilot; reused by T4.1).

Drafts JSONL (one line per atom, written by the question-writer): {"atom_id", "short_vi", "short_en",
"mcq_stem_vi", "mcq_stem_en", "filler": ValueItem|null, "option_text": {slot: {"vi", "en"}}|null, "notes"}
(slot = vn | foreign | superseded | decoy | filler; option_text is required for cat atoms, optional for
drugs/schedule). Short-answer questions are made for every atom; MCQs (2 orders x VI/EN) only for atoms that qualify
(vnsoc.qgen.mcq.skip_reasons: a planted value outside the MoH set, a decoy, one distinct MoH item) — the others are
skipped on purpose (QC row ok=True with a note; a null MCQ stem is then valid). One A3 oracle passage per atom.
Questions failing leak/population/translation/option QC are left out and listed in the QC table
(columns: question_id, ok, issues, note, passage_has_alt_value, passage_ocr, option_rank). option_rank (num/bp MCQs)
= the option slots in increasing value ('filler<foreign<vn<decoy'); the summary counts how often the foreign option
and the decoy sit at the numeric edge (H1 symmetry of the MCQ analogue, vnsoc.qgen.mcq.filler_side). The A3 row
also fails when the section label given to the model (vnsoc.run.prompts.section_label) states a non-MoH value.

  $PY -m vnsoc.qgen.build --atoms data/interim/pilot_atoms.jsonl --drafts data/interim/pilot_question_drafts.jsonl \
      --out data/interim/pilot_questions.jsonl --passages data/interim/pilot_passages.jsonl \
      --qc results/tables/pilot_question_qc.csv
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

import yaml

from vnsoc.extract.verify_span import drug_tables
from vnsoc.paths import paths
from vnsoc.qgen import mcq
from vnsoc.qgen.passages import atom_passage, passage_ocr, residual_furniture
from vnsoc.qgen.qc import (leak_issues, option_issues, option_text_issues, passage_alt_values, population_issues,
                           required_terms_issues, translation_issues)
from vnsoc.run.prompts import section_label
from vnsoc.schemas import Question

QC_FIELDS = ["question_id", "ok", "issues", "note", "passage_has_alt_value", "passage_ocr", "option_rank"]
SKIP_NOTE = "bỏ trắc nghiệm có chủ đích: "


def _jsonl(p: str) -> list[dict]:
    return [json.loads(x) for x in Path(p).read_text(encoding="utf-8").splitlines() if x.strip()]


def build_all(atoms: list[dict], drafts: dict[str, dict], seed: int, words: tuple[int, int], root=None):
    syn, combos = drug_tables(root)
    questions, passages, qc_rows = [], [], []

    def add(q: dict, issues: list[str], note: str = "", rank: str = ""):
        qc_rows.append({"question_id": q["question_id"], "ok": not issues, "issues": "; ".join(issues), "note": note,
                        "option_rank": rank})
        if not issues:
            questions.append(Question.model_validate(q).model_dump())

    for a in atoms:
        d = drafts.get(a["atom_id"])
        if not d:
            qc_rows.append({"question_id": f"{a['atom_id']}|*", "ok": False, "issues": "thiếu bản nháp câu hỏi"})
            continue
        pid = f"{a['atom_id']}#A3"
        try:
            text = atom_passage(a, root, *words)
            ocr = passage_ocr(a, root)
            passages.append({"passage_id": pid, "atom_id": a["atom_id"], "guideline": a["guideline"],
                             "section": a["section"], "page": a["page"], "words": len(text.split()), "ocr": ocr,
                             "text": text})
            alt = passage_alt_values(text, a, "vi", syn, combos)   # flagged, re-checked by hand before the freeze
            lab = passage_alt_values(section_label(a), a, "vi", syn, combos)
            bad = [f"nhãn mục A3 nêu giá trị ngoài Bộ Y tế ({', '.join(lab)})"] if lab else []
            if residual_furniture(text):
                bad.append("đoạn A3 có thể còn dấu chữ ký/ký số/e-mail: kiểm tay (riêng tư)")
            qc_rows.append({"question_id": pid, "ok": not bad, "issues": "; ".join(bad),
                            "passage_has_alt_value": ";".join(alt), "passage_ocr": ocr,
                            "note": "trang OCR: kiểm tay với ảnh trang" if ocr else ""})
        except Exception as e:  # noqa: BLE001
            qc_rows.append({"question_id": pid, "ok": False, "issues": f"không tạo được đoạn A3: {e}"})
            pid = None
        tr = translation_issues(d["short_vi"], d["short_en"])
        for lang in ("vi", "en"):
            t = d[f"short_{lang}"]
            issues = (leak_issues(t, a, lang, syn, combos) + population_issues(t, a, lang)
                      + required_terms_issues(t, a, lang))
            if lang == "en":
                issues += tr
            add({"question_id": f"{a['atom_id']}|short|{lang}", "atom_id": a["atom_id"], "format": "short",
                 "language": lang, "text": t, "oracle_passage_id": pid, "population_complete": True,
                 "translation_qc": ("pass" if not tr else "fail") if lang == "en" else "n/a"}, issues)
        why = mcq.skip_reasons(a)
        if why:
            qc_rows.append({"question_id": f"{a['atom_id']}|mcq", "ok": True, "issues": "",
                            "note": SKIP_NOTE + "; ".join(why)})
            continue
        stems = {"vi": d.get("mcq_stem_vi"), "en": d.get("mcq_stem_en")}
        if not all(stems.values()):
            qc_rows.append({"question_id": f"{a['atom_id']}|mcq", "ok": False, "issues": "thiếu stem trắc nghiệm"})
            continue
        try:
            qs, meta = mcq.build(a, stems, seed, syn, combos, d.get("filler"), d.get("option_text"))
        except ValueError as e:
            qc_rows.append({"question_id": f"{a['atom_id']}|mcq", "ok": False, "issues": str(e)})
            continue
        mtr = translation_issues(stems["vi"], stems["en"])
        ot_issues = option_text_issues(d.get("option_text"))          # VI/EN option texts not parallel: both out
        opt_issues = {lang: ot_issues + option_issues(meta["opts"], meta["texts"][lang], meta["by_writer"][lang], a,
                                                      lang, syn, combos) for lang in stems}
        note = "; ".join(meta["notes"] + ([f"filler thử phía {meta['side']} trước"] if meta["rank"] else []))
        for q in qs:
            issues = (leak_issues(q["text"], a, q["language"], syn, combos)
                      + required_terms_issues(q["text"], a, q["language"]) + opt_issues[q["language"]])
            if q["language"] == "en":
                issues += mtr
                q["translation_qc"] = "pass" if not mtr else "fail"
            add(q, issues, note, meta["rank"])
    return questions, passages, qc_rows


def edge_summary(qc_rows: list[dict]) -> str:
    """How often the foreign option and the decoy sit at the numeric edge of a num/bp MCQ (one count per atom)."""
    ranks = {r["question_id"].split("|")[0]: r["option_rank"] for r in qc_rows
             if r.get("option_rank") and "foreign" in r["option_rank"] and r.get("ok")}
    f = sum("foreign" in mcq.edge_slots(x) for x in ranks.values())
    d = sum("decoy" in mcq.edge_slots(x) for x in ranks.values())
    return f"trắc nghiệm num/bp có nước ngoài: {len(ranks)} mẩu, nước ngoài ở biên {f}, mồi ở biên {d}"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="qgen.build")
    ap.add_argument("--atoms", required=True)
    ap.add_argument("--drafts", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--passages", required=True)
    ap.add_argument("--qc", required=True)
    ap.add_argument("--only-drafted", action="store_true", help="chỉ xử lý mẩu có bản nháp (agent tự kiểm phần mình)")
    a = ap.parse_args(argv)
    P = paths()
    cfg = yaml.safe_load((P.configs / "project.yaml").read_text(encoding="utf-8"))
    cond = yaml.safe_load((P.configs / "conditions.yaml").read_text(encoding="utf-8"))
    atoms = _jsonl(a.atoms)
    drafts = {d["atom_id"]: d for d in _jsonl(a.drafts)}
    if a.only_drafted:
        atoms = [x for x in atoms if x["atom_id"] in drafts]
    qs, ps, qc = build_all(atoms, drafts, int(cfg["qgen"]["mcq_order_seed"]), tuple(cond["a3_passage_words"]))
    for path, rows in ((a.out, qs), (a.passages, ps)):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    Path(a.qc).parent.mkdir(parents=True, exist_ok=True)
    with open(a.qc, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=QC_FIELDS, restval="")
        w.writeheader()
        w.writerows(qc)
    bad = [r for r in qc if not r["ok"]]
    skipped = [r for r in qc if str(r.get("note", "")).startswith(SKIP_NOTE)]
    by = {}
    for q in qs:
        by[(q["format"], q["language"])] = by.get((q["format"], q["language"]), 0) + 1
    print(f"{len(qs)} câu ({', '.join(f'{k[0]}/{k[1]}={v}' for k, v in sorted(by.items()))}); "
          f"{len(ps)} đoạn A3 ({sum(bool(p.get('ocr')) for p in ps)} từ trang OCR); "
          f"{len(skipped)} mẩu bỏ trắc nghiệm có chủ đích; {len(bad)} mục QC không đạt")
    print(edge_summary(qc))
    for r in bad[:40]:
        print(f"  QC LỖI {r['question_id']}: {r['issues']}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
