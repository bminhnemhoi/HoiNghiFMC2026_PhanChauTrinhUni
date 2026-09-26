"""Rule-based grading (pre-registered, section 4.5 of the proposal). One label per answer:

  1 correct_aware  MoH value AND explicitly flags the foreign difference (or asks which country)
  2 correct        answer contained in the current MoH value set
  3 temporal       matches a superseded MoH version
  4 foreign        matches a named foreign system (US, EU_UK, WHO_global, WHO_WPRO)
  5 unattributed   a value that matches no known source (decoy matches land here, flagged)
  6 abstain        no value given

Atoms are dicts (see schemas.Atom). Value items by kind:
  num      {"lo": 15, "hi": 15, "unit": "ml/kg/h", "cmp": null}
  bp       {"sys": 140, "dia": 90}
  schedule {"seq": [0, 3, 7, 14, 28], "unit": "day"}
  drugs    {"key_drugs": ["artemether-lumefantrine"]}   (an answer's class token 'a|b', e.g. 'tenofovir', covers one)
  cat      {"label": "one_step"}

A drug class named without its form ('tenofovir') is graded once per member (grader 1.1.0, neutral rule): the label
all members agree on, 2 when they only disagree between 1 and 2, otherwise 5 with underspecified=True.

A cat answer naming several categories is several values (grader 1.2.0; parse_values): all in the MoH set -> 2,
otherwise the multi-value rule (5, or 1 with source attribution). A conditional next step ('Ringer lactate; nếu không
đáp ứng chuyển cao phân tử', 'colloid; crystalloid only if unavailable') is not read as "first line = the first
category": it is two values, whichever category comes first and whichever form the condition takes (neither the MoH
nor the foreign reading is credited; multi=True lets the analysis report such answers separately). A category that is
named but negated or only a vehicle is not a value (normalize_vi.parse_cats). An atom's own pattern must not read a
conditional mention differently for one category (P-dengue-03 colloid: DECISIONS 1.2.0, owner fix pending).

Grader 1.3.0 (from the AI check of the pilot grading; the pilot itself stays reported with 1.2.0):
  - rule 5 for every value kind: an answer line (or LLM-extracted answer) holding a number that is no value of the
    atom's kind is label 5 (unit_mismatch), and a cat answer naming a drug (or, on a TB-phase atom, a TB code)
    outside every category is label 5 ('unlisted'); without an answer line such a text is flagged needs_llm instead
    of label 6. A cat answer that mentions a category without stating it (negated) keeps the 1.2.0 handling.
    After review: an answer line that abstains is 6 and one that asks back which country (A0) is 1 BEFORE the number
    test; ordinal labels and stem numbers inside a phrase are no values (_value_numbers).
  - drugs: every drug of the answer must belong to a recorded regimen it names (key drugs + drugs of the item's
    recorded text, pooled over items at gap 0, + the atom's background); otherwise the answer is a regimen of its own
    (label 5). A '+' combination is one regimen. Excluded drugs ('không dùng EFV') are not read. An MoH regimen listed
    with a superseded or decoy regimen is rule 7 like a conflicting foreign one (see regimen_fit, classify_value); an
    answer line whose whole list is not in the MoH set is read piece by piece for rule 6 (_drug_segments_multi).
  - normalize_vi: template slots ('<unit>' dropped, '<TDF>' kept as text), 'N /ULN', 'S mmHg / D mmHg', 'S D mmHg',
    'S by D', '≥S mmHg or ≥D mmHg', mixed split forms, 'R H E', TB code letter order, more negation words.

Grader 1.3.1 (reader inventory of the 25 corpus documents, review/extraction_calibration/reader_inventory.md): the drug
table and the unit reader cover the corpus (configs/grading.yaml, normalize_vi). A larger table must not change what
an answer means: supportive drugs listed in configs/grading.yaml `adjunct_drugs` (paracetamol, vitamins, iron, zinc,
ORS, fluids, acid suppression, antiemetics, antihistamines) that are the key drug of no recorded item of the atom belong
to every regimen (regimen_drugs), so 'TDF + 3TC + DTG + vitamin B6' keeps the label of 'TDF + 3TC + DTG'.
"""
from __future__ import annotations

import itertools
import math
import re
from dataclasses import asdict, dataclass, field, replace
from decimal import Decimal
from functools import lru_cache

from vnsoc import normalize_vi as nv

LABELS = {1: "correct_aware", 2: "correct", 3: "temporal", 4: "foreign", 5: "unattributed", 6: "abstain"}
# Quantities read on a log scale (viral load): distances, tolerance windows and decoy mirrors are taken on log10 of
# the value, so a 10-fold difference is one unit whatever the magnitude (grader 1.1.0; '> 10.000 IU/mL' is not
# within the window of a 2.000 IU/mL threshold whose nearest foreign value is 20.000). Values already in log10 are
# linear. The atom's `tolerance` of such an atom is in log10 units.
LOG_SCALE_UNITS = frozenset({"iu/ml", "ui/ml", "copies/ml", "copy/ml", "cp/ml", "bảnsao/ml"})
REL_TOL = 1e-9           # binary rounding noise allowed in distance comparisons (below)


def log_scale(atom: dict) -> bool:
    """True for quantities read on a log scale (viral load in IU/mL or copies/mL, any spelling)."""
    return re.sub(r"\s+", "", atom.get("unit") or "").lower() in LOG_SCALE_UNITS


def below(g: float, t: float) -> bool:
    """g < t as in exact arithmetic on the recorded decimals: False when g equals t up to binary rounding noise
    (relative REL_TOL), e.g. gap 0.19999999999999996 against 2·tol 0.20000000000000007 (vn 0.7, foreign 0.9)."""
    return g < t and not math.isclose(g, t, rel_tol=REL_TOL, abs_tol=0.0)


def _on_scale(n, atom: dict):
    """A Num on the atom's comparison scale: log10 for log-scale atoms (positive values only), else unchanged."""
    if n is None or not log_scale(atom) or n.lo <= 0:
        return n
    return replace(n, lo=math.log10(n.lo), hi=math.log10(n.hi))
ANS_LINE = re.compile(r"(?:ĐÁP\s*ÁN|Đáp\s*án|DAP\s*AN|ANSWER|Final\s+answer)\s*\**\s*[:：]\s*\**\s*(.+)", re.I)
THINK = re.compile(r"<think>.*?</think>", re.S | re.I)
# An explicit abstention (grader 1.3.0 uses it: rule 5, and cat answers, see _grade_short / parse_values).
ABSTAIN = re.compile(
    r"không\s+(?:rõ|chắc(?:\s+chắn)?|biết|thể\s+(?:xác\s+định|trả\s+lời|khẳng\s+định|đưa\s+ra)|"
    r"có\s+(?:đủ\s+)?(?:thông\s+tin|dữ\s+liệu))|chưa\s+(?:rõ|có\s+(?:đủ\s+)?(?:thông\s+tin|dữ\s+liệu))|"
    r"tôi\s+không\s+thể|không\s+đủ\s+(?:thông\s+tin|dữ\s+liệu)|"
    r"\bi\s+(?:do\s+not|don't|don’t)\s+know\b|\bunknown\b|\bnot\s+sure\b|\bunsure\b|\buncertain\b|"
    r"\bcannot\s+(?:determine|answer|provide|say|be\s+determined)\b|\bcan(?:'|’)t\s+(?:determine|answer|say)\b|"
    r"\bunable\s+to\b|\binsufficient\s+(?:information|data)\b|\bnot\s+enough\s+(?:information|data)\b|"
    r"\bno\s+(?:sufficient\s+|enough\s+|reliable\s+)?(?:information|data)(?:\s+(?:is\s+)?available)?\b", re.I)
ASK_COUNTRY = re.compile(r"quốc\s+gia\s+nào|nước\s+nào|hướng\s+dẫn\s+(?:của\s+)?(?:nước|quốc\s+gia)\s+nào|"
                         r"theo\s+hướng\s+dẫn\s+nào|which\s+(?:country|guidelines?|jurisdiction|national)", re.I)
# Numbers that label an ordinal, a line or a class, not a value ("ARV bậc 1", "first-line: nhóm 2", "type 2", "2nd"):
# not counted by rule 5 (grader 1.3.0, after review).
ORDINAL_LABEL_RE = re.compile(
    r"(?<![^\W\d_])(?:bậc|tuyến|hàng|lines?|nhóm|groups?|loại|type|typ|độ|grade|giai\s+đoạn|stage|phase|cấp|level|"
    r"mức|class)\s*\d+[a-z]?(?![\d.,]?\d)|(?<![\w.,])\d+\s*(?:st|nd|rd|th)(?![^\W\d_])", re.I)
# Label 1 (context-aware) needs a NAMED foreign body/country in the same sentence as a non-MoH value, or together
# with an explicit contrast phrase (prereg §6.3 rule 8; revised 2026-09-26 after the clinician review: generic
# connectives such as "while", "however", "khác" and case-insensitive acronyms such as "who", "us" gave label 1 to
# ordinary answers). Acronyms are case-sensitive with letter boundaries; "quốc tế"/"international" never count
# inside "đơn vị quốc tế"/"international units".
CONTRAST = re.compile(r"khác\s+(?:với|so\s+với)|không\s+giống|trong\s+khi|còn\s+theo|ngược\s+lại|"
                      r"whereas|unlike|in\s+contrast|differs?\s+from|different\s+from|as\s+opposed\s+to", re.I)
FOREIGN_NAMES = re.compile(
    r"(?<![A-Za-z])(?:WHO|ADA|AHA|ACC|ESC|ESH|CDC|AASLD|EASL|APASL|RCUK|NICE|ACOG|GINA|GOLD|WAO|EAACI|IDSA|USPSTF|"
    r"KDIGO|US|USA|UK)(?![A-Za-z])"
    r"|\b(?:Mỹ|Hoa\s+Kỳ|[cC]hâu\s+Âu|Anh\s+quốc|Vương\s+quốc\s+Anh|nước\s+Anh|Tổ\s+chức\s+Y\s+tế\s+Thế\s+giới)\b"
    r"|(?i:\b(?:american|european|british|united\s+states|world\s+health\s+organi[sz]ation)\b)"
    r"|(?<!vị\s)(?i:\bquốc\s+tế\b)|(?i:\binternational\b(?!\s+units?))")
SENT_SPLIT = re.compile(r"(?<=[.!?;])\s+|\n+")
VN_MARK = re.compile(r"bộ\s+y\s+tế|việt\s+nam|\bBYT\b|\bMoH\b|Vietnam", re.I)


@dataclass
class Grade:
    label: int | None
    label_name: str | None
    vn_match: bool = False
    foreign_systems: list = field(default_factory=list)
    foreign_sources: list = field(default_factory=list)   # 'source|version_date' of every matched foreign record
    superseded: list = field(default_factory=list)
    decoy_match: bool = False
    parse_method: str = "none"      # answer_line | fallback | llm | none | unit_mismatch | unlisted (cat, 1.3.0)
    multi: bool = False
    partial: bool = False
    unit_assumed: bool = False
    needs_llm: bool = False
    underspecified: bool = False    # a drug class ('tenofovir') whose members lead to different labels (label 5)
    answer_text: str = ""
    parsed: list = field(default_factory=list)

    def as_dict(self) -> dict:
        return asdict(self)


# ------------------------------------------------------------------------------ extraction
def answer_span(output: str) -> tuple[str, str]:
    text = THINK.sub(" ", output or "").strip()
    hits = ANS_LINE.findall(text)
    if hits:
        return hits[-1].strip().strip("*").strip(), "answer_line"
    return text, "fallback"


def parse_values(text: str, atom: dict, lang: str, synonyms=None, combos=None, resolve: dict | None = None) -> list:
    """(flag, value) pairs; flag 'assumed' = a number without unit, read in the atom's unit. Product concentrations
    ('1:1000', '1 mg/ml') are not values. resolve: class token -> member (drugs; see grade_short)."""
    kind = atom["value_kind"]
    if kind == "num":
        unit, ctx = atom.get("unit"), atom.get("context") or {}
        vals = []
        for n in nv.parse_nums(text, lang, drop_concentrations=True):
            if n.unit is None:
                vals.append(("assumed", nv.Num(n.lo, n.hi, unit, n.cmp)))
            elif n.to(unit, ctx) is not None:
                vals.append(("ok", n.to(unit, ctx)))
        return vals
    if kind == "bp":
        return [("ok", b) for b in nv.parse_bps(text)]
    if kind == "schedule":
        return [("ok", s) for s in nv.parse_schedules(text, min_len=int(atom.get("min_schedule_len", 2)))]
    if kind == "drugs":
        # grader 1.3.0: a drug named only to be excluded is not read ("… (không dùng EFV)", "TLD instead of TLE"); a
        # list joined as one combination ("TDF + ETV") is flagged `joined` (see regimen_fit)
        stated, joined = nv.stated_drugs_text(text, synonyms or {})
        d = nv.parse_drugs(stated, synonyms or {}, combos or {})
        if resolve:
            d = nv.resolve_classes(d, resolve, combos)
        return [("ok", nv.Drugs(d.names, joined=joined))] if d.names else []
    if kind == "cat":
        # one value per category named (grader 1.2.0): "Ringer lactate hoặc cao phân tử", "4HR hoặc 4HRE" and the
        # conditional "Ringer lactate; nếu không đáp ứng chuyển cao phân tử" are several values, graded by the
        # multi-value rule like num/drugs (label 5, or 1 when each value is attributed to its source); before 1.2.0
        # one Cat holding every label was label 2 whenever the MoH label was among them.
        c = parse_cat(text, atom)
        return [("ok", nv.Cat(frozenset([lab]))) for lab in sorted(c.labels)]
    raise ValueError(f"value_kind lạ: {kind}")


def _tb_atom(options: dict) -> bool:
    """A cat atom whose categories are TB phase codes (labels 'HRE', 'HR', 'RE'...)."""
    return any(re.fullmatch(r"[HRZES]{2,5}", lab) for lab in options)


def parse_cat(text: str, atom: dict) -> nv.Cat:
    """Categories of a cat answer (grader 1.3.0 around normalize_vi.parse_cats): an explicit abstention is not a
    category ('Không rõ' is not the answer 'Không' of a yes/no atom; 'No information available' is not 'No'), and on
    a TB-phase atom a code the atom's patterns do not read in its written order is read in the one order they read
    ('E H R' -> 'EHR' -> 'HRE'; letter order carries no meaning in TB notation), when exactly one reading exists."""
    opts = atom.get("cat_options") or {}
    text = ABSTAIN.sub(" ", text or "")
    c = nv.parse_cats(text, opts)
    if not _tb_atom(opts):
        return c
    t, codes = nv.tb_codes(text)
    new = t
    for m in reversed(codes):
        if nv.parse_cats(m.group(0), opts).labels:
            continue
        reads: dict[frozenset, str] = {}
        for p in itertools.permutations(m.group("c")):
            q = m.group("d") + "".join(p)
            labs = nv.parse_cats(q, opts).labels
            if labs:
                reads.setdefault(labs, q)
        if len(reads) == 1:
            new = new[:m.start()] + next(iter(reads.values())) + new[m.end():]
    return c if new == t else nv.parse_cats(new, opts)


# ------------------------------------------------------------------------------ matching
def _within(x: float, lo: float, hi: float, tol: float) -> bool:
    return (lo <= x <= hi) or (lo - tol < x < hi + tol)


def matches(val, item: dict, atom: dict) -> tuple[bool, bool]:
    """(contained, partial_overlap) of one parsed answer value in one reference value item."""
    kind, tol = atom["value_kind"], float(atom.get("tolerance") or 0.0)
    if kind == "num":
        ref = nv.Num(float(item["lo"]), float(item["hi"]), item.get("unit") or atom.get("unit"))
        ref = ref.to(atom.get("unit"), atom.get("context") or {}) or ref
        if log_scale(atom) and val.lo > 0 and ref.lo > 0:
            val, ref = _on_scale(val, atom), _on_scale(ref, atom)
        inside = _within(val.lo, ref.lo, ref.hi, tol) and _within(val.hi, ref.lo, ref.hi, tol)
        overlap = not (val.hi < ref.lo - tol or val.lo > ref.hi + tol)
        if _open_touch(val, getattr(val, "cmp", None), ref, item.get("cmp")):
            inside = overlap = False             # '<130' is not inside '130 to <140' (and vice versa)
        return inside, (overlap and not inside)
    if kind == "bp":
        ok = _within(val.sys, item["sys"], item["sys"], tol) and _within(val.dia, item["dia"], item["dia"], tol)
        return ok, False
    if kind == "schedule":
        return tuple(val.seq) == tuple(item["seq"]) and val.unit == item.get("unit", "day"), False
    if kind == "drugs":
        full, some = nv.drugs_cover(val.names, item["key_drugs"])   # a class token ('tenofovir') covers one member
        return full, some and not full
    if kind == "cat":
        return item["label"] in val.labels, False
    raise ValueError(kind)


def _named(val):
    """A drug list without its class tokens ('tenofovir'): what the answer names explicitly."""
    if isinstance(val, nv.Drugs):
        return nv.Drugs(frozenset(n for n in val.names if "|" not in n))
    return val


# ------------------------------------------------------------------------------ drug regimens (grader 1.3.0)
# A drug value item records only the DISCRIMINATING drugs of a regimen (key_drugs: 'cycloserine' for 'Bdq Lzd Cfz Cs
# + 1 thuốc nhóm C'), so `matches` asks only that the answer names them (containment). Before 1.3.0 an answer naming
# the key drugs PLUS other drugs was a full match ('TDF + 3TC' matched the MoH monotherapy 'TDF'; 'Bdq, Lzd, Cfz, Z,
# E, R' matched C1a through bedaquiline), against prereg §6.2 ("a regimen differing by any drug lies outside the
# other"). Since 1.3.0 every drug of the answer must belong to a recorded regimen it names.
#   - The drugs of a regimen (regimen_drugs) are the key drugs and the drugs named in the recorded `text` of its item,
#     pooled over the items at gap 0 (WHO 2026 C1a with ethionamide = MoH C1a with prothionamide), PLUS the atom's
#     background: every drug named in some recorded text of the atom (MoH, foreign, superseded, decoy) that is the key
#     drug of no item (3TC/FTC of HIV PEP, primaquine after an ACT, the companion drugs of the MDR-TB regimens). The
#     background is one set per atom and is allowed in every regimen, so whether one source's text happens to write the
#     backbone out ('+ primaquin liều duy nhất', '(hoặc FTC)') does not change which source an answer matches (after
#     review of the first 1.3.0 draft: a WHO ACT + primaquine was 5, the MoH ACT + primaquine 2).
#   - A class token in a recorded text ('Tenofovir 300 mg') names the member that is the item's own key drug, or every
#     member when none is.
#   - A drug that belongs to none of the regimens the answer names ('extra') makes the answer a regimen of its own: it
#     matches no source (label 5; `partial` when it names an MoH key drug). Drugs the answer excludes ('không dùng EFV',
#     'instead of TLE') are not read (normalize_vi.stated_drugs_text).
#   - A list JOINED as one combination ('TDF + ETV', 'TLD + NVP'; Drugs.joined) is one regimen: one recorded regimen
#     (with its gap-0 items) must hold every drug. Other lists ('TDF hoặc ETV', 'Bdq, Lfx, Cfz…') may spread over the
#     regimens they name, which stay several values: an MoH regimen listed with a superseded or decoy regimen outside
#     the MoH set is rule 7 (label 5, or 1 when attributed), as a conflicting foreign regimen already was.
# One rule for MoH, foreign, superseded and decoy items. Recorded texts are read with the caller's drug tables
# (configs/grading.yaml when none is given).
_TEXT_DRUGS: dict = {}


@lru_cache(maxsize=1)
def _config_drug_tables() -> tuple[dict, dict]:
    import yaml

    from vnsoc.paths import paths

    cfg = yaml.safe_load((paths().configs / "grading.yaml").read_text(encoding="utf-8")) or {}
    return cfg.get("drugs") or {}, cfg.get("combos") or {}


def _tables(synonyms, combos) -> tuple[dict, dict]:
    """The caller's drug tables, or configs/grading.yaml when none is given."""
    if synonyms is None:
        return _config_drug_tables()
    return synonyms, combos or {}


@lru_cache(maxsize=1)
def adjunct_drugs() -> frozenset:
    """configs/grading.yaml `adjunct_drugs` (grader 1.3.1): supportive drugs (antipyretic, vitamins, iron, zinc, ORS,
    fluids, acid suppression, antiemetics, antihistamines) that do not make a drug answer another regimen when they are
    the key drug of no recorded item of the atom (see regimen_drugs)."""
    import yaml

    from vnsoc.paths import paths

    cfg = yaml.safe_load((paths().configs / "grading.yaml").read_text(encoding="utf-8")) or {}
    return frozenset(cfg.get("adjunct_drugs") or [])


def _item_drugs(item: dict, synonyms: dict, combos: dict) -> frozenset:
    """Single drugs of one recorded item: its key drugs and the drugs named in its text (cached per text, key and table
    objects; the tables are kept alive). A class token in the text names the item's own key member, else every member."""
    key = (item.get("text") or "", tuple(item["key_drugs"]), id(synonyms), id(combos))
    hit = _TEXT_DRUGS.get(key)
    if hit is None or hit[0] is not synonyms or hit[1] is not combos:
        own = nv.drug_leaves(item["key_drugs"], combos, classes="members")
        names = nv.parse_drugs(key[0], synonyms, combos).names if key[0] else frozenset()
        out = set(own)
        for n in names:
            if "|" in n:
                out |= (set(n.split("|")) & own) or set(n.split("|"))
            else:
                out |= nv.drug_leaves([n], combos, classes="members")
        hit = (synonyms, combos, frozenset(out))
        _TEXT_DRUGS[key] = hit
    return hit[2]


def _recorded(atom: dict) -> list[dict]:
    """Every recorded value item that grading reads (MoH, foreign, superseded, decoy; derived items are ignored)."""
    items = list(atom.get("vn") or [])
    items += [it for f in atom.get("foreign") or [] for it in f["values"] if not it.get("derived")]
    items += [it for s in atom.get("superseded") or [] for it in s["values"] if not it.get("derived")]
    return items + list(atom.get("decoy") or [])


def background_drugs(atom: dict, synonyms=None, combos=None) -> frozenset:
    """Drugs named in the recorded texts of a drug atom that are the key drug of no recorded item (see above)."""
    syn, cmb = _tables(synonyms, combos)
    items = _recorded(atom)
    named = set().union(*(_item_drugs(it, syn, cmb) for it in items)) if items else set()
    keys = set().union(*(nv.drug_leaves(it["key_drugs"], cmb, classes="members") for it in items)) if items else set()
    return frozenset(named - keys)


def regimen_drugs(item: dict, atom: dict, synonyms=None, combos=None) -> set:
    """Single drugs of the regimen a drug item stands for: key drugs and text drugs of the item and of every recorded
    item at gap 0, plus the atom's background (see the section comment above), plus (grader 1.3.1) the adjunct drugs
    of configs/grading.yaml that are the key drug of no recorded item of the atom: before 1.3.1 these supportive drugs
    were not in the drug table, so 'TDF + 3TC + DTG + vitamin B6' or 'AL + paracetamol' kept the label of the regimen;
    the larger table must not turn such an answer into another regimen (label 5). Same rule for every source."""
    syn, cmb = _tables(synonyms, combos)
    out: set = set(background_drugs(atom, syn, cmb))
    adj = adjunct_drugs()
    if adj:
        items = _recorded(atom)
        keys = set().union(*(nv.drug_leaves(it["key_drugs"], cmb, classes="members") for it in items)) if items else set()
        out |= adj - keys
    for it in [x for x in _recorded(atom) if _gap(x, item, atom) == 0] or [item]:
        out |= _item_drugs(it, syn, cmb)
    return out


def regimen_fit(val, atom: dict, synonyms=None, combos=None) -> tuple[list[dict], list[str]]:
    """(recorded items the drug answer matches, extra drugs). An item matches when the answer names its key drugs
    (`matches`) and every drug of the answer belongs to the regimens it names: the union of their regimens for a list,
    ONE regimen for a joined combination (val.joined). extra: the drugs outside (for a joined list, outside the nearest
    regimen); [] when the answer names no recorded key drug (then nothing matches anyway). A class token ('tenofovir')
    is extra only when no member belongs."""
    items = [it for it in _recorded(atom) if matches(val, it, atom)[0]]
    if not items:
        return [], []
    syn, cmb = _tables(synonyms, combos)
    leaves = nv.drug_leaves(val.names, cmb)

    def outside(known: set) -> list[str]:
        return sorted(n for n in leaves if n not in known and not ("|" in n and set(n.split("|")) & known))

    if not getattr(val, "joined", False):
        ex = outside(set().union(*(regimen_drugs(it, atom, syn, cmb) for it in items)))
        return ([], ex) if ex else (items, [])
    families: dict[frozenset, list[dict]] = {}
    for it in items:
        families.setdefault(frozenset(it["key_drugs"]), []).append(it)
    fit: list[dict] = []
    nearest: list[str] | None = None
    for fam in families.values():
        ex = outside(regimen_drugs(fam[0], atom, syn, cmb))
        if not ex:
            fit += fam
        elif nearest is None or len(ex) < len(nearest):
            nearest = ex
    return (fit, []) if fit else ([], nearest or [])


def extra_drugs(val, atom: dict, synonyms=None, combos=None) -> list[str]:
    """Drugs of a drug answer outside the recorded regimens it names (regimen_fit)."""
    return regimen_fit(val, atom, synonyms, combos)[1]


def classify_value(val, atom: dict, synonyms=None, combos=None) -> dict:
    """Sources one parsed value matches. foreign_conflict: it matches a foreign value lying OUTSIDE the MoH set (a
    value-level test; a system can have one concordant and one conflicting record, e.g. WHO 2026 vs WHO 2019). A
    foreign drug value reached only through a class token ('tenofovir' for TAF) is under-specification, not a second
    regimen, so it does not set foreign_conflict. Drugs (grader 1.3.0): only the items of regimen_fit match; a list
    with a drug outside every regimen it names ('extra') matches no source; other_conflict: the list also names a
    superseded or decoy regimen outside the MoH set (rule 7, like foreign_conflict)."""
    r = {"vn": False, "foreign": [], "superseded": [], "decoy": False, "partial": False, "foreign_conflict": False,
         "other_conflict": False, "extra": [], "sources": []}
    vn = atom.get("vn") or []
    drugs = atom["value_kind"] == "drugs"
    fit = None
    if drugs:
        items, r["extra"] = regimen_fit(val, atom, synonyms, combos)
        fit = {id(it) for it in items}

    def hit_(it) -> bool:
        return matches(val, it, atom)[0] and (fit is None or id(it) in fit)

    for it in vn:
        ok, part = matches(val, it, atom)
        if ok and fit is not None and id(it) not in fit:
            ok, part = False, True                   # the MoH key drugs are named, inside another regimen
        r["vn"] |= ok
        r["partial"] |= part
    if drugs and not fit:
        return r

    def outside(it) -> bool:
        return all(_gap(v, it, atom) > 0 for v in vn)

    for f in atom.get("foreign") or []:
        hit = [it for it in f["values"] if not it.get("derived") and hit_(it)]
        if hit:
            r["foreign"].append(f["system"])
            r["sources"].append(f"{f.get('source', '')}|{f.get('version_date', '')}")
            r["foreign_conflict"] |= any(outside(it) and matches(_named(val), it, atom)[0] for it in hit)
    for s in atom.get("superseded") or []:
        hit = [it for it in s["values"] if not it.get("derived") and hit_(it)]
        if hit:
            r["superseded"].append(s["guideline"])
            r["other_conflict"] |= drugs and any(outside(it) and matches(_named(val), it, atom)[0] for it in hit)
    hit = [it for it in atom.get("decoy") or [] if hit_(it)]
    r["decoy"] = bool(hit)
    r["other_conflict"] |= drugs and any(outside(it) and matches(_named(val), it, atom)[0] for it in hit)
    return r


def _same(v, w) -> bool:
    """One value restated: equal up to the float noise of a unit conversion ('0,15 mg (150 µg)'), with a comparator
    written once or not at all ('130/80 … tâm thu ≥ 130 hoặc tâm trương ≥ 80', '35 tuổi (từ 35 tuổi trở lên)')."""
    if type(v) is not type(w):
        return False
    if isinstance(v, nv.Num):
        close = all(math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-12) for a, b in ((v.lo, w.lo), (v.hi, w.hi)))
        return close and v.unit == w.unit and (v.cmp == w.cmp or None in (v.cmp, w.cmp))
    if isinstance(v, nv.BP):
        return v.sys == w.sys and v.dia == w.dia and (v.cmp == w.cmp or None in (v.cmp, w.cmp))
    return v == w


def _distinct(vals: list) -> list:
    """Distinct parsed values in reading order (see _same); a restated value keeps its comparator, and flag 'ok'
    when any statement had an explicit unit."""
    out = []
    for flag, v in vals:
        i = next((k for k, (_, w) in enumerate(out) if _same(v, w)), None)
        if i is None:
            out.append((flag, v))
            continue
        f0, w = out[i]
        keep = v if getattr(w, "cmp", None) is None and getattr(v, "cmp", None) is not None else w
        out[i] = ("ok" if "ok" in (f0, flag) else f0, keep)
    return out


def _names_drug(text: str, atom: dict, synonyms=None, combos=None) -> bool:
    """A cat answer states a drug of the drug tables, or (TB-phase atom) a TB phase code, that it does not negate (a
    value, grader 1.3.0: see _grade_short)."""
    syn, cmb = _tables(synonyms, combos)
    if nv.parse_drugs(nv.stated_drugs_text(text, syn)[0], syn, cmb).names:
        return True
    return _tb_atom(atom.get("cat_options") or {}) and bool(nv.tb_codes(text)[1])


def _stem_numbers(atom: dict) -> list:
    """Numbers of the question stem as recorded in the atom (population, condition, intervention; the question is
    rendered from them)."""
    pop = atom.get("population")
    texts = list(pop.values()) if isinstance(pop, dict) else [pop]
    texts += [atom.get("condition"), atom.get("intervention")]
    return [n for x in texts if isinstance(x, str) for n in nv.parse_nums(x, "vi")]


def _restated(n, stem: list) -> bool:
    """A number that repeats a number of the question stem (same bounds; a unit on one side only is allowed)."""
    return any(math.isclose(n.lo, s.lo) and math.isclose(n.hi, s.hi) and (n.unit == s.unit or None in (n.unit, s.unit))
               for s in stem)


# A bare quantity: the whole answer is one number (or range) with at most one unit word ('4 tháng', '6 months', '2').
BARE_QUANTITY_RE = re.compile(r"^\W*(?:[≥≤<>]\s*)?\d[\d.,\s-]*(?:[^\W\d_][^\s\d]{0,11})?[\W_]*$")


def _value_numbers(span: str, atom: dict, lang: str) -> list:
    """Numbers of a span that could be a value in another unit or kind (rule 5; grader 1.3.0, after review): ordinal
    and class labels ('ARV bậc 1', 'type 2') are not counted, nor are numbers restated from the question stem inside a
    phrase that restates the question ('PEP within 72 hours', 'OGTT at 24–28 weeks', 'standard 6-month regimen'). A
    bare quantity is the answer the model gives, stem number or not ('4 tháng' to the drugs of the 4-month phase: 5)."""
    nums = nv.parse_nums(ORDINAL_LABEL_RE.sub(" ", span), lang)
    if BARE_QUANTITY_RE.match(nv.clean(span)):
        return nums
    stem = _stem_numbers(atom)
    return [n for n in nums if not _restated(n, stem)]


def _sentences(text: str) -> list[str]:
    return [x for x in SENT_SPLIT.split(text or "") if x.strip()]


def _name_segments(sentence: str) -> list[tuple[str | None, str]]:
    """Split a sentence at every named source; each segment is attributed to the name it starts with ('vn' for a
    Vietnam/MoH marker, 'foreign' for a named foreign body/country, None before the first name)."""
    marks = sorted([(m.start(), "vn") for m in VN_MARK.finditer(sentence)] +
                   [(m.start(), "foreign") for m in FOREIGN_NAMES.finditer(sentence)])
    segs, prev, kind = [], 0, None
    for pos, k in marks:
        if pos > prev:
            segs.append((kind, sentence[prev:pos]))
        prev, kind = pos, k
    segs.append((kind, sentence[prev:]))
    return segs


def _attributed(text: str, atom: dict, lang: str, synonyms=None, combos=None,
                resolve=None) -> list[tuple[str | None, dict]]:
    """(attribution, classification) of every value parsed in `text`, segment by segment; unit-less numbers are
    ignored when a value with an explicit unit exists (years such as 'WHO 2009' are not answers)."""
    out = []
    for sent in _sentences(text):
        for kind, seg in _name_segments(sent):
            for flag, v in parse_values(seg, atom, lang, synonyms, combos, resolve):
                out.append((kind, flag, classify_value(v, atom, synonyms, combos)))
    if any(f == "ok" for _, f, _ in out):
        out = [x for x in out if x[1] == "ok"]
    return [(k, c) for k, _, c in out]


def _attribution_aware(span: str, atom: dict, lang: str, synonyms=None, combos=None, conflicting: bool = False,
                       resolve=None) -> bool:
    """Label 1 for an answer giving several values (prereg §6.3 rules 6-7): every non-MoH value must sit in a segment
    introduced by a named foreign source, and at least one MoH value in a segment introduced by a Vietnam/MoH marker
    or by no name. 'Theo Bộ Y tế: 5-10 hoặc 15' attaches the foreign value to the MoH marker, so it is label 5.
    conflicting=True (drug lists): a list that also contains a conflicting foreign regimen (since 1.3.0 also a
    superseded or decoy regimen outside the MoH set) counts as non-MoH."""
    av = _attributed(span, atom, lang, synonyms, combos, resolve)

    def foreign_hit(c) -> bool:
        return conflicting and (c["foreign_conflict"] or c["other_conflict"])

    moh = [k for k, c in av if c["vn"] and not foreign_hit(c)]
    non = [k for k, c in av if not c["vn"] or foreign_hit(c)]
    return bool(moh) and bool(non) and all(k == "foreign" for k in non) and any(k in (None, "vn") for k in moh)


def _drug_segments_multi(span: str, atom: dict, lang: str, synonyms=None, combos=None, resolve=None) -> bool:
    """A drug answer that, read piece by piece (sentences cut at every named source, as rule 6), holds at least two
    drug lists, one of them in the MoH set (grader 1.3.0; see _grade_short)."""
    av = _attributed(span, atom, lang, synonyms, combos, resolve)
    return len(av) >= 2 and any(c["vn"] for _, c in av)


def _sentence_aware(text: str, atom: dict, lang: str, synonyms=None, combos=None, resolve=None) -> bool:
    """Label 1 for a single MoH value (prereg §6.3 rule 8): some sentence names a foreign body/country AND either
    states a non-MoH value (explicit unit) or uses an explicit contrast phrase."""
    for sent in _sentences(text):
        if not FOREIGN_NAMES.search(sent):
            continue
        if CONTRAST.search(sent):
            return True
        if any(f == "ok" and not classify_value(v, atom, synonyms, combos)["vn"]
               for f, v in parse_values(sent, atom, lang, synonyms, combos, resolve)):
            return True
    return False


def _class_choices(output: str, span: str, atom: dict, lang: str, synonyms, combos) -> list[dict]:
    """Every way to read the drug classes ('tenofovir') named in the answer or its sentences as one member each
    ([] when no class token survives parsing, e.g. 'tenofovir (TDF)')."""
    if atom["value_kind"] != "drugs" or not any("|" in k and "+" not in k for k in synonyms or {}):
        return []
    full = THINK.sub(" ", output or "")
    texts = [span, *_sentences(full)] + [seg for sent in _sentences(span) for _, seg in _name_segments(sent)]
    present = sorted({n for x in texts for _, d in parse_values(x, atom, lang, synonyms, combos) for n in d.names
                      if "|" in n})
    return [dict(zip(present, pick)) for pick in itertools.product(*(c.split("|") for c in present))]


def _merge_choices(gs: list[Grade]) -> Grade:
    """Neutral rule for a class name: one label if every member gives it; 2 if they differ only between 1 and 2;
    otherwise 5 and underspecified (no source is credited: vn/foreign/superseded empty, decoy only if all agree)."""
    common = {k: sorted(set.intersection(*(set(getattr(g, k)) for g in gs)))
              for k in ("foreign_systems", "foreign_sources", "superseded")}
    labels = {g.label for g in gs}
    base = dict(common, vn_match=all(g.vn_match for g in gs), decoy_match=all(g.decoy_match for g in gs),
                multi=any(g.multi for g in gs), partial=any(g.partial for g in gs))
    if len(labels) == 1:
        return replace(gs[0], **base)
    if labels <= {1, 2}:
        return replace(gs[0], label=2, label_name=LABELS[2], **base)
    return replace(gs[0], label=5, label_name=LABELS[5], underspecified=True,
                   **dict(base, vn_match=False, foreign_systems=[], foreign_sources=[], superseded=[]))


def grade_short(output: str, atom: dict, lang: str = "vi", synonyms=None, combos=None,
                extracted: str | None = None, condition: str | None = None) -> Grade:
    """Grade a short-answer output. `extracted` = answer string from the LLM extractor (method llm).
    `condition`: asking back "which country?" counts as label 1 only without a country cue (A0); always pass it.
    A drug class named without its form is graded once per member (_class_choices, _merge_choices)."""
    span = extracted if extracted is not None else answer_span(output)[0]
    choices = _class_choices(output, span, atom, lang, synonyms, combos)
    if not choices:
        return _grade_short(output, atom, lang, synonyms, combos, extracted, condition)
    g = _merge_choices([_grade_short(output, atom, lang, synonyms, combos, extracted, condition, resolve=c)
                        for c in choices])
    g.parsed = [repr(v) for _, v in _distinct(parse_values(span, atom, lang, synonyms, combos))]
    return g


def _grade_short(output: str, atom: dict, lang: str, synonyms, combos, extracted: str | None, condition: str | None,
                 resolve: dict | None = None) -> Grade:
    if extracted is not None:
        span, method = extracted, "llm"
    else:
        span, method = answer_span(output)
    vals = _distinct(parse_values(span, atom, lang, synonyms, combos, resolve))
    full_text = THINK.sub(" ", output or "")
    g = Grade(label=None, label_name=None, parse_method=method, answer_text=span[:300])
    if method == "fallback" and len(vals) > 1:
        g.needs_llm = True
        g.parsed = [repr(v) for _, v in vals]
        return g
    if not vals:
        # prereg §6.3 rule 5, for every value kind since 1.3.0: an answer line (or LLM-extracted answer) holding a
        # number that is not a value of the atom's kind ('0 mg' to a yes/no atom, '4 tháng' to a drug list, '140
        # mmHg' alone to a BP atom) is a value, label 5 (unit_mismatch), not an abstention; so is a cat answer naming
        # a drug outside every category ('rifampicin, isoniazid, pyrazinamide' to a closed set of TB phases:
        # 'unlisted'). Without an answer line the same text goes to the LLM extractor (needs_llm) instead of label 6.
        # A cat answer that mentions a category but does not state it ('Dextran 40 không được khuyến cáo', negated) is
        # handled as before 1.3.0 (label 6): a number inside a product name must not tell it from 'Ringer lactate
        # không được khuyến cáo'.
        # After review of the first 1.3.0 draft, BEFORE the number rule: an answer line that asks back which country or
        # guideline applies (A0) is label 1, and an answer line that abstains ('Không rõ, cần hỏi bác sĩ trong 24 giờ',
        # 'Insufficient information (depends on age ≥ 14 years)') is label 6, whatever number it mentions; numbers
        # restated from the question stem and ordinal labels are not counted (_value_numbers).
        cat = atom["value_kind"] == "cat"
        line = method in ("answer_line", "llm")
        if line and condition == "A0" and ASK_COUNTRY.search(span):
            g.label, g.label_name = 1, LABELS[1]
            return g
        if line and ABSTAIN.search(span):
            g.label, g.label_name = 6, LABELS[6]
            return g
        if cat and nv.cat_mentioned(ABSTAIN.sub(" ", span), atom.get("cat_options") or {}):
            number = drug = False
        else:
            number = bool(_value_numbers(span, atom, lang))
            drug = not number and cat and _names_drug(span, atom, synonyms, combos)
        if line and (number or drug):
            g.parse_method = "unit_mismatch" if number else "unlisted"
            g.label, g.label_name = 5, LABELS[5]
            return g
        if ASK_COUNTRY.search(full_text) and condition == "A0":
            g.parse_method = "none" if method == "fallback" else method
            g.label, g.label_name = 1, LABELS[1]
        elif method == "fallback" and (number or drug):
            g.needs_llm = True                        # label None until the LLM extraction (DR9)
        else:
            g.parse_method = "none" if method == "fallback" else method
            g.label, g.label_name = 6, LABELS[6]
        return g
    g.parsed = [repr(v) for _, v in vals]
    g.unit_assumed = any(f == "assumed" for f, _ in vals)
    cls = [classify_value(v, atom, synonyms, combos) for _, v in vals]
    g.decoy_match = any(c["decoy"] for c in cls)
    g.partial = any(c["partial"] for c in cls) and not any(c["vn"] for c in cls)
    if len(cls) > 1 and not all(c["vn"] for c in cls):
        g.multi = True
        if any(c["vn"] for c in cls) and _attribution_aware(span, atom, lang, synonyms, combos, resolve=resolve):
            g.vn_match = True
            g.foreign_systems = sorted({s for c in cls for s in c["foreign"]})
            g.foreign_sources = sorted({s for c in cls for s in c["sources"]})
            g.label, g.label_name = 1, LABELS[1]
        else:
            g.label, g.label_name = 5, LABELS[5]
        return g
    c = cls[0] if len(cls) == 1 else {"vn": True, "foreign": [], "superseded": [], "decoy": False, "sources": []}
    g.vn_match = c["vn"]
    g.foreign_systems = sorted(set(c["foreign"]))
    g.foreign_sources = sorted(set(c["sources"]))
    g.superseded = sorted(set(c["superseded"]))
    if c["vn"] and (c.get("foreign_conflict") or c.get("other_conflict")) and atom["value_kind"] == "drugs":
        # one drug list containing both the MoH regimen and a conflicting foreign regimen (value-level test: a
        # concordant WHO 2026 record is not vetoed by a conflicting WHO 2019 record of the same system); since 1.3.0
        # also a superseded or decoy regimen outside the MoH set ('TLD + EFV': MoH and decoy, two regimens)
        g.multi = True
        aware = _attribution_aware(span, atom, lang, synonyms, combos, conflicting=True, resolve=resolve)
        g.label = 1 if aware else 5
        g.label_name = LABELS[g.label]
        return g
    if not c["vn"] and atom["value_kind"] == "drugs" and _drug_segments_multi(span, atom, lang, synonyms, combos,
                                                                              resolve):
        # grader 1.3.0 (after review): the whole answer line is one drug list, which an unrecorded regimen given for a
        # named foreign body makes 'extra' ('Theo Bộ Y tế: TDF + 3TC + DTG. Theo CDC (US): TDF/FTC + DRV/r'). Read
        # piece by piece it holds an MoH regimen and other regimens: rule 6, as for num atoms (1 when attributed).
        g.multi = True
        aware = _attribution_aware(span, atom, lang, synonyms, combos, conflicting=True, resolve=resolve)
        if aware:
            cls = [c for _, c in _attributed(span, atom, lang, synonyms, combos, resolve)]
            g.vn_match = True
            g.foreign_systems = sorted({s for x in cls for s in x["foreign"]})
            g.foreign_sources = sorted({s for x in cls for s in x["sources"]})
            g.superseded = []
            g.partial = False
        g.label = 1 if aware else 5
        g.label_name = LABELS[g.label]
        return g
    if c["vn"]:
        g.label = 1 if _sentence_aware(full_text, atom, lang, synonyms, combos, resolve) else 2
    elif c["superseded"]:
        g.label = 3
    elif c["foreign"]:
        g.label = 4
    else:
        g.label = 5
    g.label_name = LABELS[g.label]
    return g


MCQ_LETTER = re.compile(r"(?:ĐÁP\s*ÁN|ANSWER)?\s*[:：]?\s*\(?\b([A-F])\b\)?", re.I)


ROLE_TOKEN = re.compile(r"vn|decoy|filler|foreign:\w+(?:\+\w+)*|superseded:[^|:\s][^|]*")


def mcq_role_tokens(role: str) -> dict:
    """Parse one option role: tokens joined by '|' ('vn' | 'foreign:<SYS>[+<SYS>...]' | 'superseded:<guideline>' |
    'decoy' | 'filler'); an option matching several sources carries every token ('superseded:3310/2019|foreign:US').
    An unknown or malformed token ('VN', 'foreign:', 'foregin:US', 'superseded', '') raises ValueError: a typo in a
    question file must not turn an MoH or foreign option into 'unattributed'."""
    r = {"vn": False, "foreign": [], "superseded": [], "decoy": False}
    for tok in (x.strip() for x in (role or "").split("|")):
        if not ROLE_TOKEN.fullmatch(tok):
            raise ValueError(f"vai trò phương án không hợp lệ: {tok!r} trong {role!r}")
        if tok == "vn":
            r["vn"] = True
        elif tok.startswith("foreign:"):
            r["foreign"] += tok.split(":", 1)[1].split("+")
        elif tok.startswith("superseded:"):
            r["superseded"].append(tok.split(":", 1)[1].strip())
        elif tok == "decoy":
            r["decoy"] = True
    return r


def grade_mcq(output: str, option_roles: dict[str, str]) -> Grade:
    """option_roles: letter -> role tokens joined by '|' (see mcq_role_tokens). Same precedence as grade_short:
    vn -> 2; else superseded -> 3 (foreign systems recorded too); else foreign -> 4; else 5 (decoy_match for 'decoy';
    'filler' -> plain 5). Every role is checked, so a malformed question fails on its first output."""
    roles = {k: mcq_role_tokens(v) for k, v in option_roles.items()}
    span, method = answer_span(output)
    m = MCQ_LETTER.search(span if method == "answer_line" else span[:40])
    g = Grade(label=None, label_name=None, parse_method=method, answer_text=span[:100])
    if not m or m.group(1).upper() not in option_roles:
        g.label, g.label_name = 6, LABELS[6]
        return g
    r = roles[m.group(1).upper()]
    g.parsed = [m.group(1).upper()]
    g.vn_match, g.decoy_match = r["vn"], r["decoy"]
    g.foreign_systems = sorted(set(r["foreign"]))
    g.superseded = sorted(set(r["superseded"]))
    g.label = 2 if r["vn"] else 3 if r["superseded"] else 4 if r["foreign"] else 5
    g.label_name = LABELS[g.label]
    return g


# ------------------------------------------------------------------------------ atom helpers
def _gap(a: dict, b: dict, atom: dict) -> float:
    kind = atom["value_kind"]
    if kind == "num":
        ctx, unit = atom.get("context") or {}, atom.get("unit")
        x = nv.Num(float(a["lo"]), float(a["hi"]), a.get("unit") or unit).to(unit, ctx)
        y = nv.Num(float(b["lo"]), float(b["hi"]), b.get("unit") or unit).to(unit, ctx)
        if x is None or y is None:
            return float("inf")
        if log_scale(atom) and x.lo > 0 and y.lo > 0:
            lx, ly = _on_scale(x, atom), _on_scale(y, atom)
            g = max(0.0, max(lx.lo, ly.lo) - min(lx.hi, ly.hi))
            if g == 0 and _open_touch(x, a.get("cmp"), y, b.get("cmp")):
                p = x.lo if x.lo == x.hi else y.lo      # the touching point; one recorded unit above it, in log10
                return math.log10((p + _resolution(a, b)) / p)
            return g
        g = max(0.0, max(x.lo, y.lo) - min(x.hi, y.hi))
        if g == 0 and _open_touch(x, a.get("cmp"), y, b.get("cmp")):
            return _resolution(a, b)                 # disjoint but adjacent: one unit of the last recorded decimal
        return g
    if kind == "bp":
        return max(abs(a["sys"] - b["sys"]), abs(a["dia"] - b["dia"]))
    if kind == "schedule":
        return 0.0 if list(a["seq"]) == list(b["seq"]) else float("inf")
    if kind == "drugs":   # a regimen that differs by any drug lies outside the other (value-set definition, §1.2)
        return 0.0 if set(a["key_drugs"]) == set(b["key_drugs"]) else float("inf")
    if kind == "cat":
        return 0.0 if a["label"] == b["label"] else float("inf")
    raise ValueError(kind)


def _open_touch(x, xc, y, yc) -> bool:
    """Two numeric items that touch at one point p are disjoint when a strict comparator puts one of them on the
    other side of p: a point '<p' against a proper interval starting at p, or '>p' against one ending at p
    (prereg §6.2). Point-against-point thresholds ('> 2000' vs '>= 2000') stay equal (gap 0)."""
    def one(a, ac, b) -> bool:
        if a.lo != a.hi:
            return False
        p = a.lo
        return (ac == "<" and b.lo == p and b.hi > p) or (ac == ">" and b.hi == p and b.lo < p)
    return one(x, xc, y) or one(y, yc, x)


def _resolution(a: dict, b: dict) -> float:
    nd = 0
    for it in (a, b):
        for k in ("lo", "hi"):
            e = Decimal(str(float(it[k]))).normalize().as_tuple().exponent
            nd = max(nd, -e if isinstance(e, int) and e < 0 else 0)
    return 10.0 ** (-nd)


def others(atom: dict) -> list[dict]:
    """Every non-MoH source value (foreign, superseded, decoy); values flagged derived=True are ignored."""
    items = [it for f in atom.get("foreign") or [] for it in f["values"] if not it.get("derived")]
    items += [it for s in atom.get("superseded") or [] for it in s["values"] if not it.get("derived")]
    items += list(atom.get("decoy") or [])
    return items


def compute_tolerance(atom: dict) -> float:
    """Half the minimum gap between the MoH value set and every other source value (foreign,
    superseded, decoy), so tolerance windows never overlap the MoH set. Exact match (0) for
    schedule/drugs/cat kinds and when a gap is 0 (such atoms are concordant/indistinguishable)."""
    gaps = [_gap(v, o, atom) for v in atom.get("vn") or [] for o in others(atom)]
    finite = [g for g in gaps if g not in (0.0, float("inf"))]
    if not finite or atom["value_kind"] not in ("num", "bp"):
        return 0.0
    return min(finite) / 2.0


def conflict_status(atom: dict) -> str:
    """conflict | concordant | no_counterpart | indistinguishable.
    conflict: at least one foreign value lies OUTSIDE the MoH value set (gap > 0 to every MoH item).
    indistinguishable: a conflicting foreign value cannot be told apart from a superseded or decoy
    value (tolerance windows overlap), or the decoy touches the MoH set."""
    vn = atom.get("vn") or []
    foreign = [it for f in atom.get("foreign") or [] for it in f["values"] if not it.get("derived")]
    if not foreign:
        return "no_counterpart"
    conflicting = [o for o in foreign if all(_gap(v, o, atom) > 0 for v in vn)]
    if not conflicting:
        return "concordant"
    tol = float(atom.get("tolerance") if atom.get("tolerance") is not None else compute_tolerance(atom))
    sup = [it for s in atom.get("superseded") or [] for it in s["values"] if not it.get("derived")]
    dec = list(atom.get("decoy") or [])
    for o in conflicting:
        for x in sup + dec:
            gap = _gap(o, x, atom)
            if gap == 0.0 or below(gap, 2 * tol):
                return "indistinguishable"
    for x in dec + sup:
        if any(_gap(v, x, atom) == 0 for v in vn):
            return "indistinguishable" if x in dec else "conflict"
    return "conflict"
