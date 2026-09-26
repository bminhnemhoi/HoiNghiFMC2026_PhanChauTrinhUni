"""Data contracts (pydantic v2). Every JSONL file in data/interim, data/processed and data/frozen
must validate:  $PY -m vnsoc.schemas <kind> <file.jsonl>   (kind: manifest|atom|question|run|grade)

Atom = one span-verified recommendation "mẩu" (proposal §3.4). Values are value SETS.
"""
from __future__ import annotations

import json
import sys
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

System = Literal["US", "EU_UK", "WHO_global", "WHO_WPRO", "OTHER"]
SlotType = Literal["dose", "threshold", "duration", "schedule", "first_line", "classification", "target",
                   "procedure"]
ValueKind = Literal["num", "bp", "schedule", "drugs", "cat"]
ConflictStatus = Literal["conflict", "concordant", "no_counterpart", "indistinguishable"]


class Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ManifestRow(Strict):
    doc_key: str = Field(description="(số, năm) as 'NNNN/YYYY', e.g. '2760/2023'")
    number: str
    year: int
    kind: Literal["QĐ", "TT", "OTHER"] = "QĐ"
    title: str
    disease: str
    issued: str | None = None                 # YYYY-MM-DD
    status: Literal["current", "superseded", "partial"]
    supersedes: list[str] = []
    superseded_by: list[str] = []
    partially_amended_by: list[str] = []
    source_url: str | None = None             # official source only (kcb.vn, moh.gov.vn, ...)
    source_host: str | None = None
    downloaded: str | None = None
    sha256: str | None = None
    text_layer: bool | None = None
    ocr: bool = False
    pages: int | None = None
    in_corpus: bool = False
    notes: str = ""

    @model_validator(mode="after")
    def _no_tvpl(self):
        if self.source_url and "thuvienphapluat" in self.source_url:
            raise ValueError("source_url không được là thuvienphapluat (chỉ dùng tra cứu thủ công)")
        return self


class ValueItem(Strict):
    # num
    lo: float | None = None
    hi: float | None = None
    unit: str | None = None
    cmp: Literal[">=", ">", "<=", "<", "="] | None = None
    # bp
    sys: float | None = None
    dia: float | None = None
    # schedule
    seq: list[int] | None = None
    # drugs
    key_drugs: list[str] | None = None
    # cat
    label: str | None = None
    text: str | None = None                   # human-readable rendering, e.g. "5–10 ml/kg/giờ"
    derived: bool = False                     # computed by the extractor, not read verbatim (e.g. a bolus converted
    #                                           to a rate): ignored by vnsoc.grade for status/tolerance/attribution


class ForeignValue(Strict):
    system: System
    source: str                               # e.g. "WHO 2009 dengue", "ADA Standards of Care 2025 §10"
    version_date: str                         # YYYY or YYYY-MM-DD
    url: str | None = None
    locator: str | None = None                # section/table/page — NO verbatim passage text
    fetched_at: str | None = None             # ISO date the page/PDF was opened to verify the value
    page_sha256: str | None = None            # hash of the fetched page/PDF (proves it was actually read)
    values: list[ValueItem]
    verified_by: Literal["auto", "student", "clinician"] | None = None


class ForeignRecord(Strict):
    """One row of data/interim/foreign_values.jsonl (the versioned foreign reference store)."""
    record_id: str
    disease: str
    topic: str                                # slot/population the value applies to
    system: System
    source: str
    version_date: str
    url: str
    locator: str
    fetched_at: str                           # required here: proves the page/PDF was opened
    page_sha256: str
    values: list[ValueItem] = Field(min_length=1)
    note: str = ""


class NeighbourValue(Strict):
    """An MoH value of the CURRENT corpus for a neighbouring context of the atom (another step of the same protocol,
    another population, another level of care), recorded at the context check (prereg §5.6 B.21)."""
    context: str                              # e.g. "bước 2 (giờ thứ 2–3)", "trẻ em", "tuyến trạm y tế"
    guideline: str | None = None              # 'NNNN/YYYY'; None = same document as the atom
    section: str | None = None
    page: int | None = None
    span: str | None = None                   # verbatim MoH text (<= 600 chars)
    values: list[ValueItem] = Field(min_length=1)


class SupersededValue(Strict):
    guideline: str                            # 'NNNN/YYYY'
    section: str | None = None
    page: int | None = None
    values: list[ValueItem]


class Atom(Strict):
    atom_id: str
    guideline: str                            # 'NNNN/YYYY'
    section: str
    page: int
    span: str                                 # verbatim MoH text containing the value (<= 600 chars)
    valid_from: str | None = None
    valid_to: str | None = None
    partially_amended_by: list[str] = []
    disease: str
    condition: str
    population: dict[str, str]                # age/weight/pregnancy/G6PD/HBeAg/setting... (required keys vary)
    slot_type: SlotType
    intervention: str
    value_kind: ValueKind
    unit: str | None = None
    context: dict[str, float | str] = {}      # weight_kg, mg_per_ml, mg_per_tablet, analyte...
    cat_options: dict[str, list[str]] | None = None
    min_schedule_len: int | None = None
    vn: list[ValueItem] = Field(min_length=1)
    foreign: list[ForeignValue] = []
    superseded: list[SupersededValue] = []
    decoy: list[ValueItem] = []
    decoy_rule: str | None = None             # mirror_arith | mirror_geom | mirror_far | agent_proposed | rounded |
    #                                           borrowed:<atom_id> (frozen with the atom; prereg §6.4)
    roundness_ok: bool | None = None          # vnsoc.match.atom_flags.roundness_ok (num/bp), frozen
    decoy_plausible: bool | None = None       # rated blind to outputs at HG3.5 by the registered rubric
    decoy_plausible_reason: str | None = None
    moh_neighbour: list[NeighbourValue] = []  # MoH values of neighbouring contexts (clinician review id 1)
    required_terms: dict[str, dict[str, list[str]]] = {}   # population key -> {"vi": [...], "en": [...]} synonyms
    moh_scope: Literal["preferred", "acceptable", "exhaustive"] | None = None   # drugs/cat: what the MoH text lists
    acuity: Literal["high", "not_high"] | None = None      # student, from the registered topic list
    aggressive_higher: bool | None = None     # override of the slot convention for foreign_direction
    tolerance: float | None = None
    conflict_status: ConflictStatus | None = None
    conflict_family: str | None = None
    span_verified: bool = False
    context_checked: Literal["pass", "fail", "pending"] = "pending"
    moh_lags_evidence: bool | None = None     # clinician only
    clinical_harm: str | None = None          # clinician only: acuity x direction
    clinician_confirmed: bool | None = None
    core_problem_id: str | None = None
    pilot: bool = False
    seed_row: int | None = None
    extraction: dict = {}                     # model, prompt_hash, date

    @model_validator(mode="after")
    def _kind_fields(self):
        for it in self.vn + self.decoy:
            _check_item(self.value_kind, it)
        for f in self.foreign:
            for it in f.values:
                _check_item(self.value_kind, it)
        for nb in self.moh_neighbour:
            for it in nb.values:
                _check_item(self.value_kind, it)
        if self.value_kind == "num" and not self.unit:
            raise ValueError("value_kind=num cần unit chuẩn hóa")
        if self.value_kind == "cat" and not self.cat_options:
            raise ValueError("value_kind=cat cần cat_options")
        return self


def _check_item(kind: str, it: ValueItem) -> None:
    need = {"num": ("lo", "hi"), "bp": ("sys", "dia"), "schedule": ("seq",), "drugs": ("key_drugs",),
            "cat": ("label",)}[kind]
    missing = [k for k in need if getattr(it, k) is None]
    if missing:
        raise ValueError(f"giá trị kiểu {kind} thiếu {missing}")
    if kind == "num" and it.lo > it.hi:
        raise ValueError("lo > hi")


class Question(Strict):
    question_id: str
    atom_id: str
    format: Literal["short", "mcq", "vignette"]
    language: Literal["vi", "en"]
    text: str
    options: dict[str, str] | None = None      # mcq: letter -> text
    option_roles: dict[str, str] | None = None  # mcq: letter -> vn | foreign:US | superseded:NNNN/YYYY | decoy
    order_variant: int = 0
    population_complete: bool = True
    translation_qc: Literal["pass", "fail", "n/a", "pending"] = "n/a"
    translation_hand_edited: bool = False      # EN text edited by hand after machine translation (RQ3 B.12)
    ambiguity_check: Literal["pass", "fail", "pending", "n/a"] = "n/a"   # manual check, 100% of conflict atoms
    oracle_passage_id: str | None = None
    gold_chunk_ids: list[str] = []
    split: Literal["ref", "cal", "test", "unassigned"] = "unassigned"   # ref = thresholds, cal = certification


class RunRecord(Strict):
    run_id: str
    model: str
    model_version: str
    date: str
    atom_id: str
    question_id: str
    format: str
    language: Literal["vi", "en"]
    condition: Literal["A0", "A1", "A2", "A3", "A4", "A5", "A6"]
    sample_idx: int = 0
    temperature: float
    max_tokens: int
    prompt_hash: str
    retrieved_ids: list[str] = []
    raw_output: str
    tokens_in: int | None = None
    tokens_out: int | None = None
    logprob_answer: float | None = None
    finish_reason: str | None = None          # 'stop' | 'length' (truncated at max_tokens) | ...
    options: dict = {}                        # backend decoding options actually sent (seed, num_ctx, ...)
    backend: Literal["vllm", "hf", "openai_batch", "gemini_batch", "api_sync", "ollama"]
    error: str | None = None


class GradeRecord(Strict):
    run_id: str
    question_id: str
    atom_id: str
    label: int | None
    label_name: str | None
    vn_match: bool
    foreign_systems: list[str]
    foreign_sources: list[str] = []           # 'source|version_date' of the matched foreign records
    superseded: list[str]
    decoy_match: bool
    parse_method: str
    multi: bool
    partial: bool
    unit_assumed: bool
    needs_llm: bool
    underspecified: bool = False               # drug class without its form, members disagree (grader 1.1.0)
    grader_version: str


KINDS = {"manifest": ManifestRow, "atom": Atom, "question": Question, "run": RunRecord, "grade": GradeRecord,
         "foreign": ForeignRecord}


def validate_jsonl(kind: str, path: str) -> tuple[int, list[str]]:
    model = KINDS[kind]
    n, errs = 0, []
    opener = open
    if path.endswith(".gz"):
        import gzip

        opener = gzip.open
    with opener(path, "rt", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            if not line.strip():
                continue
            n += 1
            try:
                model.model_validate(json.loads(line))
            except Exception as e:  # noqa: BLE001
                errs.append(f"dòng {i}: {str(e)[:300]}")
    return n, errs


def main(argv=None) -> int:
    argv = argv or sys.argv[1:]
    if len(argv) != 2 or argv[0] not in KINDS:
        print(f"dùng: python -m vnsoc.schemas <{'|'.join(KINDS)}> <file.jsonl>")
        return 2
    n, errs = validate_jsonl(argv[0], argv[1])
    if errs:
        print(f"LỖI {len(errs)}/{n} dòng:\n" + "\n".join(errs[:30]))
        return 1
    print(f"OK {n} dòng hợp lệ ({argv[0]})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
