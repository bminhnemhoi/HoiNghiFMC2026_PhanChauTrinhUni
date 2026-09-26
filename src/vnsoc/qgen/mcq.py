"""MCQ with planted options (proposal §3.5; skill question-generation step 3). Roles are recorded per letter for
vnsoc.grade.grade_mcq.

Eligibility (`skip_reasons`, empty = an MCQ is required): a planted non-MoH value lies outside the WHOLE MoH set
(conflict_status "conflict", or a verbatim superseded value with gap > 0 to every MoH item), the atom has a decoy, and
the MoH set has ONE distinct item (items at gap 0 merged, and one threshold written in two units; a DR8 multi-item
set would make a one-answer MCQ ambiguous). The MoH option shows the item written in the atom's unit (`vn_item`).
Ineligible atoms are skipped on purpose, not errors.

Options (`options`) = {MoH, nearest conflicting foreign (systems with the same value merged), superseded (outside the
MoH set and distinct from the other options), decoy}; with no such superseded value the third option is a FILLER
that belongs to no recorded source (never a second foreign value). With no conflicting foreign value, slots 2-3 hold
superseded values. Every option carries every recorded source it coincides with (gap 0), in grading priority, joined
by "|": "vn" | "superseded:<guideline>" | "foreign:<SYS>[+<SYS>]" | "decoy" | "filler", e.g.
"superseded:3310/2019|foreign:US" (grade_mcq: vn > superseded > foreign > decoy > filler, as grade_short).
Every non-MoH option has gap > 0 to every MoH item and to every other option.

Filler: num/bp by rule (`rule_filler`, fixed candidate order, nicely rounded); the draft's num/bp filler is used only
when no rule candidate qualifies (note "filler tay"; otherwise it is ignored, with a note). drugs/cat/schedule: from
the draft. Filler SIDE (review 26/9, H1 symmetry): the decoy is built on the far side of the MoH value from the foreign
value, so a filler always tried beyond the foreign value first put the foreign option "inside" and the decoy at the
numeric edge in 15/20 pilot MCQs (an extreme-avoidance bias then favours the foreign option over the decoy). The side
tried first (beyond the foreign/anchor value or beyond the decoy) is a coin seeded by atom_id (`filler_side`); the
realised numeric order of the options is recorded (`option_rank`, QC column option_rank) for a stratified check.
A filler must lie >= 2·tolerance (and > 0) from every recorded value (MoH, foreign incl. derived, superseded, decoy,
MoH neighbour); for drugs/cat/schedule it must differ from every recorded value.

Display: planted options (decoy, filler) carry the comparator of the displayed foreign option (else of the MoH
option), so no option is told apart by its form (display only; atom values unchanged; a range never gets one).
Option texts come from the writer's `option_text` when given (required for cat atoms, optional for drugs/schedule,
refused for num/bp whose options are always rendered from the values), else from render_value.

Two orders: order 0 = seeded shuffle; order 1 = order 0 rotated by two positions (position i -> (i+2) mod 4), so every
option changes letter and middle/edge positions swap."""
from __future__ import annotations

import hashlib
import random

from vnsoc.grade import _gap, below, compute_tolerance
from vnsoc.match.decoys import _decimals, in_atom_unit, log_scale
from vnsoc.qgen.render import nice_round, render_value, round_exp, sig_exp

LETTERS = "ABCD"
SLOTS = ("vn", "foreign", "superseded", "decoy", "filler")
NO_DECOY = "mẩu không có mồi hợp lệ (DECISIONS 2026-09-26: giữ mẩu, ngoài H1/H2)"
MULTI_VN = "tập giá trị Bộ Y tế nhiều mục (DR8) — trắc nghiệm một đáp án sẽ mơ hồ"
NO_OUTSIDE = "không có giá trị nước ngoài/bản cũ nằm ngoài tập Bộ Y tế"
NOT_SEPARABLE = ("giá trị nước ngoài không tách được khỏi mồi/bản cũ (indistinguishable) và không có giá trị bản cũ "
                 "nằm ngoài tập Bộ Y tế")
CMP_MISMATCH = "dấu so sánh khác nhau giữa các phương án theo dữ liệu mẩu"
HAND_FILLER = "filler tay"
DRAFT_FILLER_UNUSED = "filler bản nháp không dùng (quy tắc có ứng viên)"


def _outside_vn(item: dict, atom: dict) -> bool:
    return all(_gap(v, item, atom) > 0 for v in atom.get("vn") or [])


def _same_value(a: dict, b: dict, atom: dict) -> bool:
    """gap 0, or one num threshold written in two units whose conversion differs only by rounding (<= 0.5 %, e.g.
    7.0 mmol/L and 126 mg/dL glucose): not two DR8 items."""
    g = _gap(a, b, atom)
    if g == 0:
        return True
    unit = atom.get("unit")
    if atom["value_kind"] != "num" or (a.get("unit") or unit) == (b.get("unit") or unit):
        return False
    x, y = in_atom_unit(a, atom), in_atom_unit(b, atom)
    return bool(x and y) and g <= 0.005 * max(abs(x.hi), abs(y.hi))


def distinct_vn(atom: dict) -> list[dict]:
    """MoH items with the same value merged (gap 0, or the same threshold in two units)."""
    out: list[dict] = []
    for v in atom.get("vn") or []:
        if not any(_same_value(v, o, atom) for o in out):
            out.append(v)
    return out


def vn_item(atom: dict) -> dict:
    """The MoH item shown as the MoH option: of the items equal to the first one, the one written in the atom's unit
    (126 mg/dL and 7.0 mmol/L in a mmol/L atom -> 7.0 mmol/L, never a converted '6,994 mmol/L')."""
    vn = atom.get("vn") or []
    same = [v for v in vn if _same_value(v, vn[0], atom)]
    unit = atom.get("unit")
    return next((v for v in same if (v.get("unit") or unit) == unit), vn[0])


def _conflicting(atom: dict) -> list[tuple[str, dict]]:
    vn = atom.get("vn") or []
    out: list[tuple[list[str], dict]] = []
    for f in atom.get("foreign") or []:
        for it in f["values"]:
            if it.get("derived") or not _outside_vn(it, atom):   # derived values: never options
                continue
            same = next((o for o in out if _gap(o[1], it, atom) == 0), None)
            if same:
                if f["system"] not in same[0]:
                    same[0].append(f["system"])
            else:
                out.append(([f["system"]], it))
    near = sorted(out, key=lambda o: min(_gap(v, o[1], atom) for v in vn))
    return [("foreign:" + "+".join(sorted(s)), it) for s, it in near]


def superseded_outside(atom: dict) -> list[dict]:
    """Verbatim superseded items outside the whole MoH set, nearest to it first."""
    items = [it for s in atom.get("superseded") or [] for it in s["values"]
             if not it.get("derived") and _outside_vn(it, atom)]
    return sorted(items, key=lambda it: min(_gap(v, it, atom) for v in atom["vn"]))


def skip_reasons(atom: dict) -> list[str]:
    """Why no MCQ is built for this atom (empty list = an MCQ is required)."""
    out = []
    if not (atom.get("conflict_status") == "conflict" or superseded_outside(atom)):
        out.append(NOT_SEPARABLE if atom.get("conflict_status") == "indistinguishable" else NO_OUTSIDE)
    if len(distinct_vn(atom)) > 1:
        out.append(MULTI_VN)
    if not atom.get("decoy"):
        out.append(NO_DECOY)
    return out


def role_of(item: dict, atom: dict) -> str:
    """Every recorded source the item coincides with (gap 0; derived values ignored, as in grading), in grading
    priority, joined by '|'; 'filler' when none."""
    if any(_gap(v, item, atom) == 0 for v in atom.get("vn") or []):
        return "vn"
    toks: list[str] = []
    for s in atom.get("superseded") or []:
        tok = "superseded:" + s["guideline"]
        if tok not in toks and any(not it.get("derived") and _gap(it, item, atom) == 0 for it in s["values"]):
            toks.append(tok)
    systems = sorted({f["system"] for f in atom.get("foreign") or [] for it in f["values"]
                      if not it.get("derived") and _gap(it, item, atom) == 0})
    if systems:
        toks.append("foreign:" + "+".join(systems))
    if any(_gap(d, item, atom) == 0 for d in atom.get("decoy") or []):
        toks.append("decoy")
    return "|".join(toks) or "filler"


def recorded_values(atom: dict) -> list[dict]:
    """Every value recorded for the atom: MoH, foreign (incl. derived), superseded, decoy, MoH neighbour."""
    items = list(atom.get("vn") or []) + list(atom.get("decoy") or [])
    items += [it for f in atom.get("foreign") or [] for it in f["values"]]
    items += [it for s in atom.get("superseded") or [] for it in s["values"]]
    items += [it for nb in atom.get("moh_neighbour") or [] for it in nb.get("values") or []]
    return items


def _tolerance(atom: dict) -> float:
    t = atom.get("tolerance")
    return float(t if t is not None else compute_tolerance(atom))


def filler_issues(item: dict, atom: dict) -> list[str]:
    """Problems of a filler (empty = acceptable): it must match no recorded source (num/bp: >= 2·tolerance and > 0
    away from every recorded value; other kinds: different from every recorded value)."""
    kind = atom["value_kind"]
    need = 2 * _tolerance(atom) if kind in ("num", "bp") else 0.0
    if kind == "num":
        n = in_atom_unit(item, atom)
        if n is None:
            return ["filler không quy đổi được về đơn vị của mẩu"]
        if n.lo <= 0:
            return ["filler ≤ 0"]
    close = [it for it in recorded_values(atom)
             if not (_gap(it, item, atom) > 0 and not below(_gap(it, item, atom), need))]
    if close:
        what = "trùng" if any(_gap(it, item, atom) == 0 for it in close) else f"cách < 2·dung sai ({need:g})"
        return [f"filler {item.get('text') or _short(item)} {what} một giá trị đã ghi của mẩu"]
    return []


def _short(item: dict) -> str:
    keys = ("lo", "hi", "unit", "sys", "dia", "seq", "key_drugs", "label")
    return str({k: item[k] for k in keys if item.get(k) is not None})


def _centre_width(item: dict, atom: dict):
    n = in_atom_unit(item, atom)
    return (None, None) if n is None else ((n.lo + n.hi) / 2, n.hi - n.lo)


def filler_side(atom_id: str, seed: int) -> str:
    """Side the rule filler is tried on first: 'anchor' (beyond the foreign/superseded option) or 'decoy' (beyond the
    decoy), a coin seeded by atom_id so that over the question set the foreign option and the decoy are equally often
    at the numeric edge of the options."""
    h = int(hashlib.sha256(f"{seed}|{atom_id}|filler-side".encode()).hexdigest()[:12], 16)
    return "decoy" if h % 2 else "anchor"


def rule_filler(atom: dict, anchor: dict, decoy: dict | None = None, side: str = "anchor") -> dict | None:
    """num/bp filler by a fixed rule. anchor = the displayed foreign option (else the first displayed superseded one).
    Candidates in order (side 'anchor'): the MoH value reflected through the anchor (beyond it, same distance),
    reflected through the decoy, then 'far' (twice the distance) beyond the anchor and beyond the decoy; side 'decoy'
    tries the decoy first at each distance. Log-scale quantities (viral load, decoys.log_scale) are reflected by
    ratio, as their decoys are. num candidates keep the anchor's width and are rounded nicely
    (2 significant digits, never finer than the decimals of the source values in the atom unit; integers from 10 up);
    bp per component. The first candidate that passes filler_issues is returned."""
    v = vn_item(atom)
    a, d = (anchor, decoy) if side == "anchor" else (decoy, anchor)
    pivots = [(a, 1), (d, 1), (a, 2), (d, 2)]
    kind = atom["value_kind"]
    if kind == "bp":
        for p, k in pivots:
            if p is None:
                continue
            c = {"sys": nice_round(p["sys"] + k * (p["sys"] - v["sys"]), 2, 0),
                 "dia": nice_round(p["dia"] + k * (p["dia"] - v["dia"]), 2, 0)}
            c = {key: int(x) if float(x).is_integer() else x for key, x in c.items()}
            if c["sys"] > 0 and c["dia"] > 0 and not filler_issues(c, atom):
                return c
        return None
    if kind != "num":
        return None
    cv, _ = _centre_width(v, atom)
    _, w = _centre_width(anchor, atom)
    if cv is None or w is None:
        return None
    src = [in_atom_unit(it, atom) for it in (v, anchor, decoy) if it is not None]
    nd = _decimals(*[round(x, 6) for n in src if n is not None for x in (n.lo, n.hi)])
    for p, k in pivots:
        if p is None:
            continue
        cp, _ = _centre_width(p, atom)
        if cp is None:
            continue
        geo = log_scale(atom) and cp > 0 and cv > 0            # viral load: same ratio, as the decoy mirror
        c = cp * (cp / cv) ** k if geo else cp + k * (cp - cv)
        lo, hi = c - w / 2, c + w / 2
        if lo <= 0:
            continue
        exp = sig_exp(max(abs(lo), abs(hi)), 2, nd)              # one rounding step for both ends
        lo_r, hi_r = (_clean(round_exp(x, exp)) for x in (lo, hi))
        if lo_r <= 0:
            continue
        cand = {"lo": lo_r, "hi": hi_r, "unit": atom.get("unit")}
        if not filler_issues(cand, atom):
            return cand
    return None


def _clean(x: float):
    return int(x) if float(x).is_integer() else x


def options(atom: dict, filler: dict | None = None,
            side: str = "anchor") -> tuple[list[tuple[str, str, dict]], list[str]]:
    """([(slot, role, item)] x 4 in slot order vn, foreign/superseded, superseded/filler, decoy; notes), or raise
    ValueError. slot is one of SLOTS (the key of the writer's option_text); side: see rule_filler / filler_side."""
    why = skip_reasons(atom)
    if why:
        raise ValueError("mẩu không đủ điều kiện trắc nghiệm: " + "; ".join(why))
    decoy = atom["decoy"][0]
    picked: list[tuple[str, dict]] = [("vn", vn_item(atom))]
    conf = _conflicting(atom)
    if conf:
        picked.append(("foreign", conf[0][1]))
    for it in superseded_outside(atom):
        if len(picked) >= 3:
            break
        if all(_gap(it, o, atom) > 0 for _, o in picked) and _gap(it, decoy, atom) > 0:
            picked.append(("superseded", it))
    if len(picked) < 2:
        raise ValueError("không có giá trị cài sẵn nào khác mồi (nước ngoài/bản cũ trùng mồi)")
    notes: list[str] = []
    if len(picked) < 3:
        fill = None
        if atom["value_kind"] in ("num", "bp"):
            fill = rule_filler(atom, picked[1][1], decoy, side)
            if fill is None and filler:
                fill = filler
                notes.append(HAND_FILLER)
            elif filler:
                notes.append(DRAFT_FILLER_UNUSED)
        else:
            fill = filler
        if fill is None:
            raise ValueError("cần lựa chọn nhiễu (filler) cho mẩu này")
        bad = filler_issues(fill, atom)
        if bad:
            raise ValueError("; ".join(bad))
        picked.append(("filler", fill))
    picked.append(("decoy", decoy))
    for slot, it in picked[1:]:
        if not _outside_vn(it, atom):
            raise ValueError(f"lựa chọn {slot} nằm trong tập giá trị Bộ Y tế")
        if any(_same_value(it, v, atom) for v in atom["vn"]):   # 126 mg/dL beside 7.0 mmol/L: one threshold
            raise ValueError(f"lựa chọn {slot} là ngưỡng Bộ Y tế ghi bằng đơn vị khác (kiểm lại dữ liệu mẩu)")
    for i, (_, a) in enumerate(picked):
        for _, b in picked[i + 1:]:
            if _gap(a, b, atom) == 0:
                raise ValueError("hai lựa chọn trùng nhau")
    out = [(slot, "vn" if slot == "vn" else ("filler" if slot == "filler" else role_of(it, atom)), it)
           for slot, it in picked]
    if any(slot != "filler" and role == "filler" for slot, role, _ in out):
        raise ValueError("một lựa chọn không khớp nguồn đã ghi nào")
    return out, notes


def _point(item: dict) -> bool:
    return "sys" in item or item.get("lo") == item.get("hi")


def display_items(atom: dict, opts: list[tuple[str, str, dict]]) -> list[dict]:
    """Items as displayed: decoy and filler take the comparator of the foreign option (else of the MoH option); a
    range ('5–7') never takes one."""
    if atom["value_kind"] not in ("num", "bp"):
        return [it for _, _, it in opts]
    ref = next((it for slot, _, it in opts if slot == "foreign"), opts[0][2])
    return [dict(it, cmp=ref.get("cmp") if _point(it) else None) if slot in ("decoy", "filler") else it
            for slot, _, it in opts]


def cmp_notes(atom: dict, opts: list[tuple[str, str, dict]]) -> list[str]:
    """Comparators that still differ between displayed point options (recorded values, e.g. MoH '>= 9' vs foreign
    '10'): a form cue that display cannot remove honestly; noted for the reviewer, not an error."""
    if atom["value_kind"] not in ("num", "bp"):
        return []
    cmps = {it.get("cmp") or "=" for it in display_items(atom, opts) if _point(it)}
    return [f"{CMP_MISMATCH}: {', '.join(sorted(cmps))}"] if len(cmps) > 1 else []


def _position(item: dict, atom: dict) -> tuple:
    if atom["value_kind"] == "bp":
        return (float(item["sys"]), float(item["dia"]))
    n = in_atom_unit(item, atom)
    return ((n.lo + n.hi) / 2,) if n is not None else (float("inf"),)


def option_rank(atom: dict, opts: list[tuple[str, str, dict]]) -> str:
    """num/bp: the option slots in increasing value ('filler<foreign<vn<decoy'); '' for other kinds."""
    if atom["value_kind"] not in ("num", "bp"):
        return ""
    return "<".join(slot for slot, _, it in sorted(opts, key=lambda o: _position(o[2], atom)))


def edge_slots(rank: str) -> set[str]:
    """Slots at the numeric edges of an option_rank string."""
    parts = rank.split("<") if rank else []
    return {parts[0], parts[-1]} if parts else set()


def option_texts(atom: dict, opts: list[tuple[str, str, dict]], lang: str, synonyms=None, combos=None,
                 option_text: dict | None = None) -> tuple[list[str], set[str]]:
    """Displayed text of each option (slot order) and the slots whose text the writer supplied."""
    written = {k: v for k, v in (option_text or {}).items() if v}
    if written and atom["value_kind"] in ("num", "bp"):
        raise ValueError("option_text không dùng cho mẩu num/bp: phương án luôn render từ giá trị mẩu")
    texts, by_writer = [], set()
    for (slot, _, _), it in zip(opts, display_items(atom, opts)):
        t = (written.get(slot) or {}).get(lang)
        if t:
            texts.append(t.strip())
            by_writer.add(slot)
        else:
            texts.append(render_value(it, atom, lang, synonyms, combos))
    if atom["value_kind"] == "cat":
        missing = [slot for slot, _, _ in opts if slot not in by_writer]
        if missing:
            raise ValueError(f"mẩu cat cần option_text ({lang}) cho: {', '.join(missing)}")
    return texts, by_writer


def orders(atom_id: str, n: int, seed: int) -> list[list[int]]:
    h = int(hashlib.sha256(f"{seed}|{atom_id}".encode()).hexdigest()[:12], 16)
    first = list(range(n))
    random.Random(h).shuffle(first)
    second = [0] * n
    for i, x in enumerate(first):                     # rotate by two: A->C, B->D, C->A, D->B
        second[(i + 2) % n] = x
    return [first, second]


def build(atom: dict, stems: dict[str, str], seed: int, synonyms=None, combos=None, filler=None,
          option_text: dict | None = None) -> tuple[list[dict], dict]:
    """(question dicts (schema Question) for both languages x both orders, meta). meta: notes (e.g. 'filler tay'),
    opts [(slot, role, item)], texts {lang: [text per slot]}, by_writer {lang: set of slots}, side (filler side tried
    first), rank (option_rank)."""
    side = filler_side(atom["atom_id"], seed)
    opts, notes = options(atom, filler, side)
    notes = notes + cmp_notes(atom, opts)
    meta = {"notes": notes, "opts": opts, "texts": {}, "by_writer": {}, "side": side,
            "rank": option_rank(atom, opts)}
    for lang in stems:
        meta["texts"][lang], meta["by_writer"][lang] = option_texts(atom, opts, lang, synonyms, combos, option_text)
    out = []
    for variant, perm in enumerate(orders(atom["atom_id"], len(opts), seed)):
        for lang, stem in stems.items():
            out.append({
                "question_id": f"{atom['atom_id']}|mcq|{lang}|o{variant}", "atom_id": atom["atom_id"], "format": "mcq",
                "language": lang, "text": stem, "order_variant": variant,
                "options": {LETTERS[k]: meta["texts"][lang][i] for k, i in enumerate(perm)},
                "option_roles": {LETTERS[k]: opts[i][1] for k, i in enumerate(perm)},
                "translation_qc": "pending" if lang == "en" else "n/a",
            })
    return out, meta
