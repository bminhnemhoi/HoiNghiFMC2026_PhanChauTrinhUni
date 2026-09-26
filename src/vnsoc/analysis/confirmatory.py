"""Pre-registered confirmatory analyses (T2.10; proposal §1.4, §4.6–4.7, §5.3–5.4; prereg/osf_preregistration.md §5;
skills statistics-plan and certified-abstention). Pure numpy / scipy / pandas; runs on SIMULATED data before any real
model output exists. The registration text governs; this module implements it one-to-one (prereg §5.0 maps every
decision to a function and its arguments). Revised 2026-09-26 after the preregistration review panel
(review/prereg/response.md).

Hypotheses (proposal §1.4). Only H1 is primary; H2–H4 form one Holm family.

  H1  h1_delta             A1, Vietnamese, short answers, conflict atoms WITH a frozen decoy, open models pooled.
                           Delta = pi_f - pi_d, pi_f = mean(label 4), pi_d = mean(k_i * decoy_match) (k_i = number of
                           distinct conflicting foreign targets). Decision rule 'conservative' (intersection-union):
                           BCa (Efron 1987), expanded BCa and cluster jackknife-t lower 95% limits must all be > 0
                           AND the wild cluster restricted bootstrap-t p (wild_cluster_p) must be <= 0.025;
                           p = max of the four one-sided p-values. < 20 clusters -> jackknife-t and wild bootstrap.
      h1_robustness        S1 directional-asymmetry correction, S2 mirror_arith num/bp atoms, S3 roundness stratum,
                           N1 atoms without an MoH-neighbour overlap. "H1 robust" iff S1 and S2 lower limits > 0.
  H2  h2_mcnemar_clustered A1 (atom, model) pairs EN vs VI on US-unique conflict atoms with a decoy; outcome = label 4
                           with system US; Durkalski et al. (2003) clustered McNemar over conflict families, one-sided
                           (EN > VI); exact sign-flip test when < 20 families have a discordant pair.
  H3  h3_per_model         A3, Vietnamese, conflict atoms; per open model the rate of labels 3|4, design-effect
                           Clopper-Pearson (Korn & Graubard 1998 construction) with a t(C-1) df adjustment; one-sided
                           p for rate <= 5%; "at least half of the models" = Bonferroni partial-conjunction p.
  H4  h4_risk_ratio        A2 served answers that state a value (labels 1-5); loss = labels 3-5; Mantel-Haenszel RR
                           stratified by model x language; guideline-clustered bootstrap; one-sided p for RR <= 2.
  --  holm                 Holm step-down over {H2, H3, H4}.
  RQ3 certified_rq3        per open model, Vietnamese served answers, one per atom, value-stating; score = L2
                           logistic fit on the reference split (GroupKFold by guideline for reference scores);
                           simultaneous Clopper-Pearson bounds (primary) + Learn-then-Test (secondary).
      rq3_rerandomise      regime (a) implementation check: 500 cal/test re-draws with the reference split fixed.
      rq3_regime_b         leave-guideline-out, 500 splits, score REFIT on the reference guidelines of each split.
  DR3 dr3_check            A2, conflict atoms: upper 95% bound of P(label 3|4) < 5% for every model and language.
  --  missing_bounds, tipping_point_h1, tipping_point_h3: registered sensitivity analyses (prereg §5.5, §5.6 B).

Decision level. Every CI is two-sided 95% (configs/project.yaml ci_level). "Lower 95% limit > null value" is the same
decision as "one-sided p < 0.025"; Holm runs at 0.025.

Input: one row per graded answer, long format. Required columns
  model, atom_id, conflict_family, guideline, language ('vi'|'en'), condition ('A0'..'A6'), format ('short'|...),
  label (1-6, NaN = runtime error), decoy_match (bool), foreign_systems (str, e.g. "US,EU_UK"),
  conflict_status ('conflict'|'concordant'|'no_counterpart'|'indistinguishable'), and the atom-level covariates
  us_unique (bool), k_foreign (int), has_decoy (bool) — computed by code from the frozen atom
  (vnsoc.match.atom_flags.atom_covariates), never typed by hand.
Function-specific columns: group_signal ('agree'|'disagree'; H4, RQ3), s1, s2, s3, consistency, logprob (RQ3 score
  features), split ('ref'|'cal'|'test'; RQ3, from Question.split), value_kind, decoy_rule, roundness_ok, side,
  moh_neighbour_overlap (H1 robustness), parse_method, truncated (H2 sensitivity), passage_has_alt_value (H3
  sensitivity).
Losses are derived from `label` here, never supplied upstream: correct C = label in {1, 2}; W = 1 - C (labels 3-6);
value error E = label in {3, 4, 5}; value stated V = label != 6.
Only greedy answers enter a confirmatory test (temperature 0, sample_idx 0). 'indistinguishable' atoms are dropped.
Clusters: conflict_family (atoms without a family fall back to 'gl:<guideline>') or the guideline, as registered.

References checked on 2026-09-26: Durkalski, Palesch, Lipsitz & Rust, Stat Med 2003;22(15):2417-28,
doi:10.1002/sim.1438 (statistic reproduced against the published examples in tests); Efron, JASA 1987;82(397):171-85,
doi:10.1080/01621459.1987.10478410 (BCa); Benjamini & Heller, Biometrics 2008;64(4):1215-22,
doi:10.1111/j.1541-0420.2007.00984.x (partial conjunction); Clopper & Pearson, Biometrika 1934;26(4):404-13,
doi:10.1093/biomet/26.4.404; Korn & Graubard, Survey Methodology 1998 issue 2 (Statistics Canada catalogue
12-001-X19980024356, page opened 2026-09-26). Learn-then-Test: Angelopoulos et al., arXiv 2110.01052 (vnsoc.ltt).
"""
from __future__ import annotations

import math
from collections.abc import Callable, Iterable, Mapping, Sequence

import numpy as np
import pandas as pd
from scipy import optimize, stats
from scipy.special import expit

from vnsoc import ltt

# ------------------------------------------------------------------ pre-registered constants
# Mirror configs/project.yaml (hypotheses, rq3); tests/test_prereg_code.py fails if they drift apart.
CI_LEVEL = 0.95
ALPHA_ONE_SIDED = (1 - CI_LEVEL) / 2          # 0.025
H3_MARGIN = 0.05
H4_RR_BOUND = 2.0
H1_SESOI_EXCESS = 0.10                        # smallest excess over chance of practical interest (descriptive)
RQ3_GROUPS = ("agree", "disagree")
RQ3_COVERAGES = (1.0, 0.75, 0.5, 0.25)
RQ3_ALPHA = 0.10
RQ3_DELTA = 0.10
RQ3_ALPHA_FALLBACK = 0.15
RQ3_MIN_CAL_ATOMS = 300
RQ3_MIN_USEFUL_COVERAGE = 0.30
RQ3_SPLIT_FRACTIONS = (("ref", 0.2), ("cal", 0.4), ("test", 0.4))
RQ3_REGIME_B_SPLITS = 500
RQ3_REGIME_B_MAX_VIOLATION = 0.20
SPLIT_SEED = 20261001
# Analysis constants registered in prereg §5.1 (not in configs): bootstrap size and seed, BCa -> t switch, decision
# rule, H2 exact-test switch, H4 strata, RQ3 score model, regime (a) re-randomisations, missing-data trigger.
N_BOOT = 10_000
BOOT_SEED = 20261001
MIN_CLUSTERS_BCA = 20
PRIMARY_RULE = "conservative"
PRIMARY_RULES = ("bca", "bca_expanded", "jackknife_t", "conservative")
SIGNFLIP_MIN_FAMILIES = 20
H4_STRATA = ("model", "language")
RQ3_FEATURES = ("s1", "s2", "s3", "consistency", "logprob")
RQ3_LOGIT_C = 1.0
RQ3_LOGIT_MAX_ITER = 1000
RQ3_MAX_FOLDS = 5
RQ3_RERANDOMISATIONS = 500
MISSING_BOUND_TRIGGER = 0.02

REQUIRED = ("model", "atom_id", "conflict_family", "guideline", "language", "condition", "format", "label",
            "decoy_match", "foreign_systems", "conflict_status", "us_unique", "k_foreign", "has_decoy")
STATUSES = ("conflict", "concordant", "no_counterpart", "indistinguishable")


# ------------------------------------------------------------------ data preparation
def cluster_key(d: pd.DataFrame, by: str = "family") -> np.ndarray:
    """Resampling unit. by='family': 'fam:<conflict_family>' or, without a family, 'gl:<guideline>';
    by='guideline': 'gl:<guideline>' for every atom."""
    glk = d["guideline"].astype(object).fillna("").astype(str).to_numpy(dtype=object)
    if by == "guideline":
        return np.asarray(["gl:" + g for g in glk], dtype=object)
    if by != "family":
        raise ValueError("cluster_by phải là 'family' hoặc 'guideline'")
    fam = d["conflict_family"].astype(object).fillna("").astype(str).to_numpy(dtype=object)
    return np.where(fam != "", "fam:" + fam, "gl:" + glk)


def _as_bool(s: pd.Series) -> pd.Series:
    return s.astype("boolean").fillna(False).astype(bool)


def prepare(df: pd.DataFrame) -> pd.DataFrame:
    """Validate columns, keep greedy graded answers, drop 'indistinguishable' atoms, derive losses and clusters."""
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError(f"thiếu cột: {missing}")
    d = df
    if "temperature" in d.columns:
        d = d[d["temperature"].fillna(0).astype(float) == 0]
    if "sample_idx" in d.columns:
        d = d[d["sample_idx"].fillna(0).astype(int) == 0]
    d = d[d["label"].notna()].copy()
    d["label"] = d["label"].astype(int)
    if not d["label"].between(1, 6).all():
        raise ValueError("label phải thuộc 1..6")
    bad = set(d["conflict_status"].astype(str).unique()) - set(STATUSES)
    if bad:
        raise ValueError(f"conflict_status lạ: {sorted(bad)}")
    for c in ("decoy_match", "us_unique", "has_decoy"):
        d[c] = _as_bool(d[c])
    d["k_foreign"] = pd.to_numeric(d["k_foreign"], errors="coerce").fillna(0).astype(int)
    if (d.loc[d["conflict_status"] == "conflict", "k_foreign"] < 1).any():
        raise ValueError("mẩu xung đột phải có k_foreign >= 1")
    d["foreign_systems"] = d["foreign_systems"].fillna("").astype(str)
    d = d[d["conflict_status"] != "indistinguishable"].copy()
    lab = d["label"]
    d["C"] = lab.isin([1, 2])
    d["W"] = ~d["C"]
    d["E"] = lab.isin([3, 4, 5])
    d["V"] = lab != 6
    d["cluster"] = cluster_key(d, "family")
    d["cluster_gl"] = cluster_key(d, "guideline")
    return d


def _subset(d: pd.DataFrame, *, condition: str, language: str | None = None, fmt: str = "short",
            models: Iterable[str] | None = None) -> pd.DataFrame:
    m = (d["condition"] == condition) & (d["format"] == fmt)
    if language is not None:
        m &= d["language"] == language
    if models is not None:
        m &= d["model"].isin(list(models))
    return d[m]


def _cluster_sums(d: pd.DataFrame, cols: Sequence[str], cluster_col: str = "cluster") -> tuple[np.ndarray, np.ndarray]:
    g = d.groupby(cluster_col, sort=True)[list(cols)].sum()
    return g.index.to_numpy(), g.to_numpy(dtype=float)


def _ccol(cluster_by: str) -> str:
    if cluster_by not in ("family", "guideline"):
        raise ValueError("cluster_by phải là 'family' hoặc 'guideline'")
    return "cluster" if cluster_by == "family" else "cluster_gl"


# ------------------------------------------------------------------ cluster bootstrap machinery
def _finite(x: np.ndarray) -> np.ndarray:
    return x[np.isfinite(x)]


def _z0(boot: np.ndarray, est: float) -> float:
    B = len(boot)
    prop = (np.sum(boot < est) + 0.5 * np.sum(boot == est)) / B
    return float(stats.norm.ppf(np.clip(prop, 0.5 / B, 1 - 0.5 / B)))


def _acceleration(jack: np.ndarray) -> float:
    j = _finite(jack)
    if len(j) < 3:
        return 0.0
    dev = j.mean() - j
    den = 6.0 * np.sum(dev ** 2) ** 1.5
    return float(np.sum(dev ** 3) / den) if den > 0 else 0.0


def _zq(q: float, C: int | None) -> float:
    """Normal quantile, or the small-sample 'expanded' quantile sqrt(C/(C-1)) * t_{C-1}(q) when C is given."""
    return float(stats.norm.ppf(q)) if C is None else math.sqrt(C / (C - 1)) * float(stats.t.ppf(q, C - 1))


def _bca_limit(boot: np.ndarray, z0: float, a: float, q: float, C: int | None = None) -> float:
    zq = _zq(q, C)
    denom = 1 - a * (z0 + zq)
    level = stats.norm.cdf(z0 + (z0 + zq) / denom) if denom > 0 else (1.0 if q > 0.5 else 0.0)
    return float(np.quantile(boot, np.clip(level, 0.0, 1.0), method="inverted_cdf"))


def _bca_pvalue(boot: np.ndarray, z0: float, a: float, null: float, C: int | None = None) -> float:
    """One-sided p for H0: theta <= null, by inverting the BCa lower limit (a = z0 = 0 -> share of boot <= null).
    With C (expanded variant) the returned p inverts the expanded quantile: p = T_{C-1}(z_alpha * sqrt((C-1)/C))."""
    B = len(boot)
    G = (np.sum(boot < null) + 0.5 * np.sum(boot == null)) / B
    G = float(np.clip(G, 0.5 / B, 1 - 0.5 / B))
    w = stats.norm.ppf(G) - z0
    if 1 + a * w <= 0:
        return G
    z_alpha = w / (1 + a * w) - z0
    if C is None:
        return float(stats.norm.cdf(z_alpha))
    return float(stats.t.cdf(z_alpha * math.sqrt((C - 1) / C), C - 1))


def _jackknife_t(est: float, jack: np.ndarray, C: int, null: float, a2: float) -> dict:
    """estimate +/- t_{C-1} * delete-one-cluster jackknife SE; one-sided p from t_{C-1}."""
    j = _finite(jack)
    se = math.sqrt((len(j) - 1) / len(j) * float(np.sum((j - j.mean()) ** 2))) if len(j) >= 2 else float("nan")
    tq = float(stats.t.ppf(1 - a2, C - 1))
    if not np.isfinite(se):
        p = float("nan")
    elif se > 0:
        p = float(stats.t.sf((est - null) / se, C - 1))
    else:                                              # every leave-one-cluster-out estimate identical
        p = 0.0 if est > null else 1.0
    return {"lo": est - tq * se, "hi": est + tq * se, "p_one_sided": p, "se_jackknife": se}


def cluster_interval(M: np.ndarray, stat: Callable[[np.ndarray], np.ndarray], *, null: float = 0.0,
                     n_boot: int = N_BOOT, seed: int = BOOT_SEED, level: float = CI_LEVEL,
                     min_clusters: int = MIN_CLUSTERS_BCA, primary: str = PRIMARY_RULE) -> dict:
    """CI and one-sided p (H0: theta <= null) for a statistic of per-cluster sums (prereg §5.1.1).

    M: (C, k) per-cluster sums; stat maps (..., k) totals to (...) values (vectorised).
    C >= min_clusters: cluster bootstrap (whole clusters resampled with replacement, multinomial weights) with
      'bca'           textbook BCa (Efron 1987); acceleration from the delete-one-cluster jackknife;
      'bca_expanded'  same resamples, normal quantiles replaced by sqrt(C/(C-1)) * t_{C-1};
      'jackknife_t'   estimate +/- t_{C-1} * cluster-jackknife SE;
      'conservative'  REGISTERED RULE: intersection-union of the three (lo = min, hi = max, p = max; reject only if
                      all three reject). BCa (the protocol's interval) stays a necessary condition.
    All three are always returned under `variants`.
    C < min_clusters, or a degenerate bootstrap distribution: 'jackknife_t' only (method 't_small' / 't_degenerate').
    """
    if primary not in PRIMARY_RULES:
        raise ValueError(f"primary phải thuộc {PRIMARY_RULES}")
    M = np.asarray(M, dtype=float)
    C = M.shape[0]
    tot = M.sum(axis=0)
    with np.errstate(divide="ignore", invalid="ignore"):
        est = float(stat(tot))
        jack = np.asarray(stat(tot[None, :] - M), dtype=float) if C >= 2 else np.array([])
    a2 = (1 - level) / 2
    out = {"estimate": est, "n_clusters": C, "n_boot": 0, "seed": None}
    if C < 2 or not np.isfinite(est):
        return {**out, "lo": float("nan"), "hi": float("nan"), "p_one_sided": float("nan"), "method": "none",
                "variants": {}}
    jt = _jackknife_t(est, jack, C, null, a2)
    if C < min_clusters:
        return {**out, **jt, "method": "t_small", "variants": {"jackknife_t": jt}}
    rng = np.random.default_rng(seed)
    W = rng.multinomial(C, np.full(C, 1.0 / C), size=n_boot).astype(float)
    with np.errstate(divide="ignore", invalid="ignore"):
        boot = np.asarray(stat(W @ M), dtype=float)
    boot = boot[~np.isnan(boot)]
    if len(boot) == 0 or np.all(boot == boot[0]):
        return {**out, **jt, "method": "t_degenerate", "variants": {"jackknife_t": jt}}
    z0, acc = _z0(boot, est), _acceleration(jack)
    var = {
        "bca": {"lo": _bca_limit(boot, z0, acc, a2), "hi": _bca_limit(boot, z0, acc, 1 - a2),
                "p_one_sided": _bca_pvalue(boot, z0, acc, null)},
        "bca_expanded": {"lo": _bca_limit(boot, z0, acc, a2, C), "hi": _bca_limit(boot, z0, acc, 1 - a2, C),
                         "p_one_sided": _bca_pvalue(boot, z0, acc, null, C)},
        "jackknife_t": jt,
    }
    if primary == "conservative":
        los, his, ps = ([v[k] for v in var.values()] for k in ("lo", "hi", "p_one_sided"))
        chosen = {"lo": float(np.nanmin(los)) if not np.all(np.isnan(los)) else float("nan"),
                  "hi": float(np.nanmax(his)) if not np.all(np.isnan(his)) else float("nan"),
                  "p_one_sided": float(np.nanmax(ps)) if not np.all(np.isnan(ps)) else float("nan")}
    else:
        chosen = var[primary]
    return {**out, **chosen, "method": primary, "n_boot": int(n_boot), "seed": int(seed), "z0": z0,
            "acceleration": acc, "variants": var}


def wild_cluster_p(z: Sequence[float], n: Sequence[float], *, null: float = 0.0, n_boot: int = N_BOOT,
                   seed: int = BOOT_SEED) -> dict:
    """Wild cluster restricted bootstrap-t (Cameron, Gelbach & Miller 2008; MacKinnon & Webb 2017) for a ratio of
    cluster sums theta = sum z_c / sum n_c, H0: theta <= null, Rademacher weights, null imposed.
    Restricted residuals r_c = z_c - null * n_c; resample r*_c = eps_c r_c; t = (theta_hat - null) / SE with
    SE = sqrt(C/(C-1) sum_c (z_c - theta_hat n_c)^2) / sum n_c, and the same studentisation in every resample.
    If 2^C <= n_boot (C <= 13 at B = 10,000) all 2^C sign vectors are enumerated (exact randomisation p); otherwise
    n_boot sign vectors are drawn from default_rng(seed) and p = (1 + #{t* >= t}) / (n_boot + 1)."""
    z, n = np.asarray(z, dtype=float), np.asarray(n, dtype=float)
    C, Ntot = len(z), float(n.sum())
    if C < 2 or Ntot == 0:
        return {"p_one_sided": float("nan"), "t": float("nan"), "exact": False, "n_draws": 0}
    th = z.sum() / Ntot
    se = math.sqrt(C / (C - 1) * float(np.sum((z - th * n) ** 2))) / Ntot
    r = z - null * n
    if 2 ** C <= n_boot:
        idx = np.arange(2 ** C, dtype=np.int64)
        eps = 1.0 - 2.0 * ((idx[:, None] >> np.arange(C)) & 1)
        exact = True
    else:
        eps = np.random.default_rng(seed).choice([-1.0, 1.0], size=(n_boot, C))
        exact = False
    zs = eps * r + null * n
    ths = zs.sum(axis=1) / Ntot
    ses = np.sqrt(C / (C - 1) * np.sum((zs - ths[:, None] * n) ** 2, axis=1)) / Ntot
    with np.errstate(divide="ignore", invalid="ignore"):
        ts = (ths - null) / ses
        t = (th - null) / se if se > 0 else (math.inf if th > null else -math.inf)
    ts = np.where(np.isnan(ts), -np.inf, ts)
    hits = float(np.sum(ts >= t - 1e-12))
    p = hits / len(ts) if exact else (1.0 + hits) / (len(ts) + 1.0)
    return {"p_one_sided": float(min(1.0, p)), "t": float(t), "exact": exact, "n_draws": int(len(ts))}


# ------------------------------------------------------------------ H1
def _h1_set(df: pd.DataFrame, *, models, language: str, condition: str) -> tuple[pd.DataFrame, int]:
    d = _subset(prepare(df), condition=condition, language=language, models=models)
    d = d[d["conflict_status"] == "conflict"]
    n_no_decoy = int(d.loc[~d["has_decoy"], "atom_id"].nunique())
    return d[d["has_decoy"]], n_no_decoy


def h1_delta(df: pd.DataFrame, n_boot: int = N_BOOT, seed: int = BOOT_SEED, *, models: Iterable[str] | None = None,
             language: str = "vi", condition: str = "A1", level: float = CI_LEVEL,
             min_clusters: int = MIN_CLUSTERS_BCA, primary: str = PRIMARY_RULE, decoy_weight: str = "k",
             cluster_by: str = "family") -> dict:
    """H1 (primary; prereg §4.3, §5.1.2). Delta = pi_f - pi_d on conflict atoms that have a frozen decoy (decoy-less
    conflict atoms are excluded and counted), A1 Vietnamese short answers, open models pooled (pass `models`).
    pi_d = mean(k_i * D) (decoy_weight='k', registered) or mean(D) (decoy_weight='unscaled', sensitivity B.7a).
    Also the excess over chance E = (pi_f - pi_d) / (1 - pi_d) with its own interval (same resamples).
    Supported iff the lower limit of the `primary` rule (registered: 'conservative') is > 0."""
    if decoy_weight not in ("k", "unscaled"):
        raise ValueError("decoy_weight phải là 'k' hoặc 'unscaled'")
    d, n_no_decoy = _h1_set(df, models=models, language=language, condition=condition)
    if d.empty:
        raise ValueError("H1: không có câu trả lời nào (A1, vi, short, mẩu xung đột có mồi)")
    k = d["k_foreign"].astype(float) if decoy_weight == "k" else 1.0
    d = d.assign(n=1.0, f=(d["label"] == 4).astype(float), kd=k * d["decoy_match"].astype(float),
                 dm=d["decoy_match"].astype(float))
    _, M = _cluster_sums(d, ["n", "f", "kd"], _ccol(cluster_by))
    kw = dict(n_boot=n_boot, seed=seed, level=level, min_clusters=min_clusters, primary=primary)
    r = cluster_interval(M, lambda S: (S[..., 1] - S[..., 2]) / S[..., 0], null=0.0, **kw)
    ex = cluster_interval(M, lambda S: (S[..., 1] - S[..., 2]) / (S[..., 0] - S[..., 2]), null=0.0, **kw)
    wc = wild_cluster_p(M[:, 1] - M[:, 2], M[:, 0], null=0.0, n_boot=n_boot, seed=seed)
    N, F, KD = M.sum(axis=0)
    alpha = (1 - level) / 2
    if primary == "conservative":      # registered: interval rule AND wild cluster bootstrap-t (4-part IU test)
        confirmed = bool(r["lo"] > 0) and bool(wc["p_one_sided"] <= alpha)
        ps = [x for x in (r["p_one_sided"], wc["p_one_sided"]) if np.isfinite(x)]
        p_one = float(max(ps)) if ps else float("nan")
    else:
        confirmed, p_one = bool(r["lo"] > 0), r["p_one_sided"]
    return {
        "delta": r["estimate"], "ci_lo": r["lo"], "ci_hi": r["hi"], "method": r["method"],
        "p_one_sided": p_one, "confirmed": confirmed, "wild_cluster": wc,
        "confirmed_all_variants": bool(r["variants"]) and all(v["lo"] > 0 for v in r["variants"].values())
        and bool(wc["p_one_sided"] <= alpha),
        "variants": r["variants"], "n_clusters": r["n_clusters"], "n_responses": int(N),
        "n_atoms": int(d["atom_id"].nunique()), "n_conflict_atoms_without_decoy_excluded": n_no_decoy,
        "pi_foreign": F / N, "pi_decoy": KD / N, "pi_decoy_unscaled": float(d["dm"].sum()) / N,
        "excess": ex["estimate"], "excess_ci_lo": ex["lo"], "excess_ci_hi": ex["hi"],
        "excess_sesoi": H1_SESOI_EXCESS, "excess_lo_at_least_sesoi": bool(ex["lo"] >= H1_SESOI_EXCESS),
        "models": sorted(d["model"].unique().tolist()), "decoy_weight": decoy_weight, "cluster_by": cluster_by,
        "n_boot": r["n_boot"], "seed": r["seed"], "level": level, "language": language, "condition": condition,
    }


def h1_directional(df: pd.DataFrame, n_boot: int = N_BOOT, seed: int = BOOT_SEED, *,
                   models: Iterable[str] | None = None, language: str = "vi", condition: str = "A1",
                   level: float = CI_LEVEL, min_clusters: int = MIN_CLUSTERS_BCA,
                   primary: str = PRIMARY_RULE) -> dict:
    """Sensitivity S1 (prereg §5.6 B.7): directional-asymmetry correction on num/bp conflict atoms.
    rho = (n_foreign_side + 0.5) / (n_decoy_side + 0.5), counting single-valued answers that match no source
    (label 5, not decoy_match) by the side of the MoH value they fall on (column `side`: 'foreign' | 'decoy' | '').
    Delta_dir = pi_f - rho * pi_d, bootstrapped over the same clusters (rho recomputed in every resample)."""
    d, _ = _h1_set(df, models=models, language=language, condition=condition)
    d = d[d["value_kind"].isin(["num", "bp"])]
    if d.empty:
        raise ValueError("S1: không có mẩu num/bp")
    side = d["side"].fillna("").astype(str)
    u = (d["label"] == 5) & ~d["decoy_match"]
    d = d.assign(n=1.0, f=(d["label"] == 4).astype(float),
                 kd=d["k_foreign"].astype(float) * d["decoy_match"].astype(float),
                 sf=(u & side.eq("foreign")).astype(float), sd=(u & side.eq("decoy")).astype(float))
    _, M = _cluster_sums(d, ["n", "f", "kd", "sf", "sd"])

    def stat(S):
        rho = (S[..., 3] + 0.5) / (S[..., 4] + 0.5)
        return (S[..., 1] - rho * S[..., 2]) / S[..., 0]

    r = cluster_interval(M, stat, null=0.0, n_boot=n_boot, seed=seed, level=level, min_clusters=min_clusters,
                         primary=primary)
    tot = M.sum(axis=0)
    return {"delta_dir": r["estimate"], "ci_lo": r["lo"], "ci_hi": r["hi"], "p_one_sided": r["p_one_sided"],
            "method": r["method"], "rho": float((tot[3] + 0.5) / (tot[4] + 0.5)), "n_foreign_side": int(tot[3]),
            "n_decoy_side": int(tot[4]), "n_responses": int(tot[0]), "n_clusters": r["n_clusters"],
            "positive": bool(r["lo"] > 0)}


def h1_robustness(df: pd.DataFrame, n_boot: int = N_BOOT, seed: int = BOOT_SEED, *,
                  models: Iterable[str] | None = None, primary: str = PRIMARY_RULE) -> dict:
    """Pre-registered H1 robustness set (prereg §5.6 B.7): S1 directional correction; S2 H1 on num/bp atoms whose
    decoy came from mirror_arith; S3 H1 on atoms with roundness_ok; N1 H1 without atoms whose conflicting foreign
    value overlaps an MoH value of a neighbouring context. 'H1 robust' iff S1 and S2 were computed and both lower
    limits are > 0. A sensitivity whose columns are absent is reported as not computed."""
    out: dict = {}
    kw = dict(n_boot=n_boot, seed=seed, models=models, primary=primary)

    def sub(mask_fn, name, cols):
        if not set(cols) <= set(df.columns):
            out[name] = {"computed": False, "reason": f"thiếu cột {sorted(set(cols) - set(df.columns))}"}
            return
        try:
            r = h1_delta(df[mask_fn(df)], **kw)
            out[name] = {"computed": True, "delta": r["delta"], "ci_lo": r["ci_lo"], "ci_hi": r["ci_hi"],
                         "p_one_sided": r["p_one_sided"], "n_atoms": r["n_atoms"], "positive": r["confirmed"]}
        except ValueError as e:
            out[name] = {"computed": False, "reason": str(e)}

    if {"value_kind", "side"} <= set(df.columns):
        try:
            s1 = h1_directional(df, **kw)
            out["S1"] = {"computed": True, **s1}
        except ValueError as e:
            out["S1"] = {"computed": False, "reason": str(e)}
    else:
        out["S1"] = {"computed": False, "reason": "thiếu cột value_kind/side"}
    sub(lambda x: x["value_kind"].isin(["num", "bp"]) & x["decoy_rule"].astype(str).eq("mirror_arith"), "S2",
        ["value_kind", "decoy_rule"])
    sub(lambda x: _as_bool(x["roundness_ok"]), "S3", ["roundness_ok"])
    sub(lambda x: ~_as_bool(x["moh_neighbour_overlap"]), "N1", ["moh_neighbour_overlap"])
    s1_ok = out["S1"].get("computed") and out["S1"].get("positive")
    s2_ok = out["S2"].get("computed") and out["S2"].get("positive")
    out["h1_robust"] = bool(s1_ok and s2_ok)
    return out


# ------------------------------------------------------------------ H2
def sign_flip_exact(w: Sequence[float]) -> float:
    """Exact one-sided sign-flip p-value P(sum eps_k w_k >= sum w_k) over all 2^K sign vectors (w_k != 0 only).
    Under H0 each cluster statistic w_k is symmetric about 0. Enumerated fully (K < 20 -> at most 2^19 vectors)."""
    w = np.asarray([x for x in w if x != 0], dtype=float)
    K = len(w)
    if K == 0:
        return 1.0
    if K > 24:
        raise ValueError("sign_flip_exact: K quá lớn để liệt kê đầy đủ")
    obs = float(w.sum())
    idx = np.arange(2 ** K, dtype=np.int64)
    tot = np.zeros(2 ** K)
    for k in range(K):
        tot += w[k] * (1 - 2 * ((idx >> k) & 1))
    return float(np.mean(tot >= obs - 1e-12))


def durkalski(b: Sequence[float], c: Sequence[float], n: Sequence[float]) -> dict:
    """Clustered McNemar statistic of Durkalski et al. (2003), df = 1.

    Per cluster k: b_k = pairs (first = 1, second = 0), c_k = pairs (0, 1), n_k = all pairs.
    X2 = (sum_k (b_k - c_k)/n_k)^2 / sum_k ((b_k - c_k)/n_k)^2; the signed root Z gives the one-sided p (first >
    second). No discordant pair at all -> statistic 0 and p = 1 (no evidence).
    """
    b, c, n = (np.asarray(x, dtype=float) for x in (b, c, n))
    keep = n > 0
    w = (b[keep] - c[keep]) / n[keep]
    den = float(np.sum(w ** 2))
    if den == 0:
        return {"statistic": 0.0, "z": 0.0, "p_two_sided": 1.0, "p_one_sided": 1.0, "no_discordant_pairs": True}
    z = float(np.sum(w) / math.sqrt(den))
    return {"statistic": z * z, "z": z, "p_two_sided": float(stats.chi2.sf(z * z, 1)),
            "p_one_sided": float(stats.norm.sf(z)), "no_discordant_pairs": False}


def h2_mcnemar_clustered(df: pd.DataFrame, *, models: Iterable[str] | None = None, condition: str = "A1",
                         system: str = "US", first: str = "en", second: str = "vi", clean_only: bool = False,
                         n_boot: int = N_BOOT, seed: int = BOOT_SEED, primary: str = PRIMARY_RULE,
                         min_families_asymptotic: int = SIGNFLIP_MIN_FAMILIES) -> dict:
    """H2 (prereg §5.1.3). Pairs (atom, model) answered in EN and VI at A1 on US-unique conflict atoms with a
    decoy; outcome FUS = label 4 with `system` among foreign_systems. Durkalski clustered McNemar over conflict
    families (one-sided EN > VI); if fewer than `min_families_asymptotic` families have a discordant pair, the
    p-value is the exact sign-flip test on the same w_k. Effect size P(FUS|EN) - P(FUS|VI) with a family-clustered
    interval (registered rule). clean_only=True (sensitivity B.19): pairs whose two answers both have
    parse_method == 'answer_line' and truncated == False."""
    d = _subset(prepare(df), condition=condition, models=models)
    d = d[d["us_unique"] & d["has_decoy"] & (d["conflict_status"] == "conflict") & d["language"].isin([first, second])]
    if d.duplicated(["model", "atom_id", "language"]).any():
        raise ValueError("H2: có nhiều hơn một câu trả lời cho cùng (mô hình, mẩu, ngôn ngữ)")
    if clean_only:
        if not {"parse_method", "truncated"} <= set(d.columns):
            raise ValueError("H2 clean_only cần cột parse_method, truncated")
        d = d.assign(clean=(d["parse_method"] == "answer_line") & ~_as_bool(d["truncated"]))
    sys_hit = d["foreign_systems"].str.split(",").apply(lambda xs: system in [x.strip() for x in xs])
    d = d.assign(y=(d["label"] == 4) & sys_hit)
    wide = d.pivot(index=["model", "atom_id"], columns="language", values="y")
    wide = wide.dropna(subset=[first, second]) if {first, second} <= set(wide.columns) else wide.iloc[0:0]
    if clean_only and not wide.empty:
        cl = d.pivot(index=["model", "atom_id"], columns="language", values="clean").reindex(wide.index)
        wide = wide[cl[first].fillna(False).astype(bool) & cl[second].fillna(False).astype(bool)]
    if wide.empty:
        raise ValueError("H2: không có cặp EN/VI nào")
    clus = d.drop_duplicates(["model", "atom_id"]).set_index(["model", "atom_id"])["cluster"]
    p = pd.DataFrame({"y1": wide[first].astype(bool), "y2": wide[second].astype(bool)})
    p["cluster"] = clus.reindex(p.index).to_numpy()
    p["b"] = p["y1"] & ~p["y2"]
    p["c"] = ~p["y1"] & p["y2"]
    g = p.groupby("cluster")[["b", "c"]].sum().join(p.groupby("cluster").size().rename("n"))
    t = durkalski(g["b"], g["c"], g["n"])
    k_disc = int(((g["b"] + g["c"]) > 0).sum())
    w = ((g["b"] - g["c"]) / g["n"]).to_numpy(dtype=float)
    if t["no_discordant_pairs"]:
        p_one, test = 1.0, "no_discordant_pairs"
    elif k_disc < min_families_asymptotic:
        p_one, test = sign_flip_exact(w), "sign_flip_exact"
    else:
        p_one, test = t["p_one_sided"], "durkalski"
    M = np.c_[g["n"].to_numpy(float), g["b"].to_numpy(float), g["c"].to_numpy(float)]
    eff = cluster_interval(M, lambda S: (S[..., 1] - S[..., 2]) / S[..., 0], null=0.0, n_boot=n_boot, seed=seed,
                           primary=primary)
    N, B, Cc = len(p), int(p["b"].sum()), int(p["c"].sum())
    return {
        "p_first": float(p["y1"].mean()), "p_second": float(p["y2"].mean()), "diff": (B - Cc) / N,
        "diff_ci_lo": eff["lo"], "diff_ci_hi": eff["hi"], "diff_method": eff["method"],
        "statistic": t["statistic"], "z": t["z"], "p_one_sided": p_one, "test": test,
        "p_durkalski_one_sided": t["p_one_sided"], "p_two_sided": t["p_two_sided"],
        "no_discordant_pairs": t["no_discordant_pairs"], "n_families_discordant": k_disc,
        "mcnemar_naive_statistic": ((B - Cc) ** 2 / (B + Cc)) if B + Cc else 0.0,
        "n_pairs": N, "n_discordant_first_only": B, "n_discordant_second_only": Cc, "n_clusters": len(g),
        "direction": f"{first}>{second}", "system": system, "clean_only": clean_only,
        "models": sorted(d["model"].unique().tolist()),
    }


# ------------------------------------------------------------------ H3
def cp_design_effect(k_c: Sequence[float], n_c: Sequence[float], *, level: float = CI_LEVEL,
                     null: float | None = None) -> dict:
    """Clopper-Pearson interval for a clustered proportion using a design-effect effective sample size
    (the Korn & Graubard 1998 construction).

    deff = V_cluster / V_srs (V_cluster: cluster-robust linearised variance with the C/(C-1) factor; V_srs: the
    matching unbiased binomial variance p(1-p)/(n-1)), truncated at >= 1 so the interval is never narrower than
    exact CP; n_eff = n / deff, then multiplied by
    (t_{n-1} / t_{C-1})^2 for the few-cluster degrees of freedom; k_eff = p_hat * n_eff; exact beta quantiles with
    real-valued parameters. With one answer per cluster this is the exact Clopper-Pearson interval. The one-sided
    p for H0: rate <= null is the matching binomial tail P(X >= k_eff | n_eff, null), so lo > null <=> p < (1-level)/2.
    """
    k_c, n_c = np.asarray(k_c, dtype=float), np.asarray(n_c, dtype=float)
    n, k, C = float(n_c.sum()), float(k_c.sum()), len(n_c)
    if n == 0:
        return {"n": 0, "k": 0, "rate": float("nan"), "lo": 0.0, "hi": 1.0, "deff": float("nan"),
                "n_eff": 0.0, "n_clusters": C, "p_one_sided": 1.0}
    p = k / n
    deff = 1.0
    if C >= 2 and 0 < p < 1:
        v_clu = C / (C - 1) * float(np.sum((k_c - p * n_c) ** 2)) / n ** 2
        deff = max(1.0, v_clu / (p * (1 - p) / (n - 1)))
    a2 = (1 - level) / 2
    n_eff = n / deff
    if C >= 2 and n > 1:
        n_eff *= (stats.t.ppf(1 - a2, n - 1) / stats.t.ppf(1 - a2, C - 1)) ** 2
    k_eff = p * n_eff
    lo = 0.0 if k_eff <= 0 else float(stats.beta.ppf(a2, k_eff, n_eff - k_eff + 1))
    hi = 1.0 if k_eff >= n_eff else float(stats.beta.ppf(1 - a2, k_eff + 1, n_eff - k_eff))
    out = {"n": int(n), "k": int(k), "rate": p, "lo": lo, "hi": hi, "deff": deff, "n_eff": n_eff, "n_clusters": C}
    if null is not None:
        out["p_one_sided"] = 1.0 if k_eff <= 0 else float(stats.beta.cdf(null, k_eff, n_eff - k_eff + 1))
    return out


def partial_conjunction(pvals: Sequence[float], u: int | None = None) -> float:
    """Bonferroni partial-conjunction p-value (Benjamini & Heller 2008) for 'at least u of M nulls false':
    min(1, (M - u + 1) * p_(u)); default u = ceil(M/2). Valid under arbitrary dependence."""
    p = np.sort(np.asarray(pvals, dtype=float))
    M = len(p)
    if M == 0:
        return float("nan")
    u = math.ceil(M / 2) if u is None else u
    if not 1 <= u <= M:
        raise ValueError("u phải trong 1..M")
    return float(min(1.0, (M - u + 1) * p[u - 1]))


def h3_per_model(df: pd.DataFrame, margin: float = H3_MARGIN, *, models: Iterable[str] | None = None,
                 language: str | None = "vi", condition: str = "A3", level: float = CI_LEVEL,
                 alpha: float = ALPHA_ONE_SIDED, cluster_by: str = "family") -> dict:
    """H3 (prereg §5.1.4). Per open model: rate of labels 3|4 at A3 on CONFLICT atoms (the registered set; no other
    column can widen it), clustered CP interval (cp_design_effect) and one-sided p for H0: rate <= margin.
    'At least half of the open models' is tested by the partial-conjunction p with u = ceil(M/2)."""
    d = _subset(prepare(df), condition=condition, language=language, models=models)
    d = d[d["conflict_status"] == "conflict"]
    if d.empty:
        raise ValueError("H3: không có câu trả lời nào (A3, mẩu xung đột)")
    d = d.assign(n=1.0, y=d["label"].isin([3, 4]).astype(float))
    per = {}
    for m, dm in d.groupby("model", sort=True):
        _, M = _cluster_sums(dm, ["y", "n"], _ccol(cluster_by))
        r = cp_design_effect(M[:, 0], M[:, 1], level=level, null=margin)
        r["lb_above_margin"] = bool(r["lo"] > margin)
        per[str(m)] = r
    pv = [r["p_one_sided"] for r in per.values()]
    M_ = len(per)
    u = math.ceil(M_ / 2)
    p_pc = partial_conjunction(pv, u)
    return {"per_model": per, "n_models": M_, "u": u, "p_pc": p_pc,
            "n_models_lb_above_margin": sum(r["lb_above_margin"] for r in per.values()),
            "confirmed_unadjusted": bool(p_pc <= alpha), "margin": margin, "language": language,
            "condition": condition, "cluster_by": cluster_by, "method": "clopper_pearson_design_effect_t_df"}


# ------------------------------------------------------------------ H4
def h4_risk_ratio(df: pd.DataFrame, bound: float = H4_RR_BOUND, n_boot: int = N_BOOT, seed: int = BOOT_SEED, *,
                  models: Iterable[str] | None = None, condition: str = "A2", language: str | None = None,
                  level: float = CI_LEVEL, min_clusters: int = MIN_CLUSTERS_BCA, primary: str = PRIMARY_RULE,
                  loss: str = "value_error", estimator: str = "mh", cluster_by: str = "guideline") -> dict:
    """H4 (prereg §4.3, §5.1.5). Served A2 answers (greedy, question language), open models pooled.
    Registered primary: loss='value_error' (population = answers that state a value, labels 1-5; error = labels
    3-5), estimator='mh' (Mantel-Haenszel RR stratified by model x language), cluster_by='guideline'.
    Secondary: loss='W' (all served answers, error = labels 3-6) and/or estimator='crude'.
    Zero correction: if the agreement-side MH denominator (crude: agreement errors) is 0 in the full sample, 0.5 is
    added to both groups' error counts and 1 to both groups' totals in every stratum, in every estimate.
    One-sided p for H0: RR <= bound (log scale); confirmed (before Holm) iff the lower limit > bound."""
    if loss not in ("value_error", "W") or estimator not in ("mh", "crude"):
        raise ValueError("loss phải là 'value_error'|'W', estimator phải là 'mh'|'crude'")
    d = _subset(prepare(df), condition=condition, language=language, models=models)
    if "group_signal" not in d.columns:
        raise ValueError("H4: thiếu cột group_signal")
    bad = set(d["group_signal"].dropna().unique()) - set(RQ3_GROUPS)
    if bad or d["group_signal"].isna().any():
        raise ValueError(f"H4: group_signal phải là {RQ3_GROUPS}; gặp {sorted(map(str, bad))} hoặc trống")
    n_self_abstain = {g: int(((d["group_signal"] == g) & ~d["V"]).sum()) for g in RQ3_GROUPS}
    if loss == "value_error":
        d = d[d["V"]]
        y = d["E"].astype(float)
    else:
        y = d["W"].astype(float)
    if d.empty:
        raise ValueError("H4: không có câu trả lời nào")
    strata = (d["model"].astype(str) + "|" + d["language"].astype(str)) if estimator == "mh" else pd.Series(
        "all", index=d.index)
    levels = sorted(strata.unique())
    S = len(levels)
    dis = d["group_signal"].eq("disagree").astype(float)
    cols = []
    for s in levels:
        m = (strata == s).astype(float)
        cols += [f"nd{s}", f"ed{s}", f"na{s}", f"ea{s}"]
        d = d.assign(**{f"nd{s}": m * dis, f"ed{s}": m * dis * y, f"na{s}": m * (1 - dis), f"ea{s}": m * (1 - dis) * y})
    _, M = _cluster_sums(d, cols, _ccol(cluster_by))
    T = M.sum(axis=0).reshape(S, 4)
    present = (T[:, 0] + T[:, 2]) > 0
    den_full = np.sum(np.where(present, T[:, 3] * T[:, 0] / np.where(present, T[:, 0] + T[:, 2], 1), 0.0))
    corrected = bool(den_full == 0)
    add = np.where(present, 1.0, 0.0)

    def stat(X):
        Z = X.reshape(X.shape[:-1] + (S, 4))
        nd, ed, na, ea = Z[..., 0], Z[..., 1], Z[..., 2], Z[..., 3]
        if corrected:
            nd, na, ed, ea = nd + add, na + add, ed + 0.5 * add, ea + 0.5 * add
        N = nd + na
        with np.errstate(divide="ignore", invalid="ignore"):
            num = np.sum(np.where(N > 0, ed * na / np.where(N > 0, N, 1), 0.0), axis=-1)
            den = np.sum(np.where(N > 0, ea * nd / np.where(N > 0, N, 1), 0.0), axis=-1)
            return np.log(num) - np.log(den)

    r = cluster_interval(M, stat, null=math.log(bound), n_boot=n_boot, seed=seed, level=level,
                         min_clusters=min_clusters, primary=primary)
    nd, ed, na, ea = T.sum(axis=0)
    ex = lambda x: float(np.exp(x)) if np.isfinite(x) else (float("inf") if x > 0 else 0.0)  # noqa: E731
    variants = {k: {"lo": ex(v["lo"]), "hi": ex(v["hi"]), "p_one_sided": v["p_one_sided"]}
                for k, v in r["variants"].items()}
    per_stratum = {}
    for i, s in enumerate(levels):
        a, b, c, e = T[i]
        per_stratum[s] = {"n_disagree": int(a), "n_agree": int(c), "risk_disagree": b / a if a else float("nan"),
                          "risk_agree": e / c if c else float("nan")}
    return {
        "rr": ex(r["estimate"]), "ci_lo": ex(r["lo"]), "ci_hi": ex(r["hi"]), "log_rr": r["estimate"],
        "method": r["method"], "p_one_sided": r["p_one_sided"], "bound": bound,
        "confirmed_unadjusted": bool(ex(r["lo"]) > bound), "variants": variants,
        "risk_disagree": ed / nd if nd else float("nan"), "risk_agree": ea / na if na else float("nan"),
        "rr_crude": (ed / nd) / (ea / na) if nd and na and ea else float("nan"),
        "n_disagree": int(nd), "n_agree": int(na), "n_self_abstain_excluded": n_self_abstain if loss == "value_error"
        else {g: 0 for g in RQ3_GROUPS}, "zero_corrected": corrected, "per_stratum": per_stratum,
        "n_clusters": r["n_clusters"], "n_responses": int(nd + na), "models": sorted(d["model"].unique().tolist()),
        "loss": loss, "estimator": estimator, "cluster_by": cluster_by,
        "n_boot": r["n_boot"], "seed": r["seed"], "condition": condition, "language": language,
    }


# ------------------------------------------------------------------ Holm
def holm(pvals: Mapping[str, float], alpha: float = ALPHA_ONE_SIDED) -> dict:
    """Holm step-down adjustment within the secondary family {H2, H3, H4} (proposal §1.4).
    Adjusted p_(i) = max_{j<=i} min(1, (m - j + 1) p_(j)); reject iff adjusted p <= alpha.
    A missing/NaN p-value is treated as 1 (not rejected) and flagged."""
    items = [(k, (1.0 if v is None or not np.isfinite(v) else float(v)), v is None or not np.isfinite(v))
             for k, v in pvals.items()]
    order = sorted(range(len(items)), key=lambda i: (items[i][1], items[i][0]))
    m, run, out = len(items), 0.0, {}
    for rank, i in enumerate(order):
        name, p, was_missing = items[i]
        run = max(run, min(1.0, (m - rank) * p))
        out[name] = {"p": p, "p_holm": run, "reject": bool(run <= alpha), "missing": was_missing}
    return {k: out[k] for k in pvals}


# ------------------------------------------------------------------ DR3
def dr3_check(df: pd.DataFrame, margin: float = H3_MARGIN, *, models: Iterable[str] | None = None,
              condition: str = "A2", level: float = CI_LEVEL) -> dict:
    """DR3 (plan §DR, pre-registered): if the upper 95% bound of P(label 3|4) at A2 on conflict atoms is < 5% for
    every model (and every language), the main result is the A1 bias and 'RAG on the MoH corpus suffices';
    RQ3 becomes exploratory."""
    d = _subset(prepare(df), condition=condition, models=models)
    d = d[d["conflict_status"] == "conflict"]
    d = d.assign(n=1.0, y=d["label"].isin([3, 4]).astype(float))
    cells = {}
    for (m, lang), dm in d.groupby(["model", "language"], sort=True):
        _, M = _cluster_sums(dm, ["y", "n"])
        cells[f"{m}|{lang}"] = cp_design_effect(M[:, 0], M[:, 1], level=level)
    return {"cells": cells, "margin": margin,
            "triggered": bool(cells) and all(c["hi"] < margin for c in cells.values())}


# ------------------------------------------------------------------ RQ3: splits
def assign_rq3_split(atom_ids: Sequence[str], fractions: Sequence[tuple[str, float]] = RQ3_SPLIT_FRACTIONS,
                     seed: int = SPLIT_SEED) -> np.ndarray:
    """Atom-level ref/cal/test split (every row of an atom on one side; §4.7). Two calls of ltt.split_by_atom:
    ref = fraction f_ref of atoms (seed); cal = f_cal / (f_cal + f_test) of the remaining atoms (seed + 1)."""
    fr = dict(fractions)
    a = np.asarray(atom_ids).astype(str)
    ref = ltt.split_by_atom(a, frac_cal=fr["ref"], seed=seed)
    rest = np.flatnonzero(~ref)
    cal_rest = ltt.split_by_atom(a[rest], frac_cal=fr["cal"] / (fr["cal"] + fr["test"]), seed=seed + 1)
    out = np.full(len(a), "test", dtype=object)
    out[ref] = "ref"
    out[rest[cal_rest]] = "cal"
    return out


def split_map(df: pd.DataFrame, *, unit: str = "atom", seed: int = SPLIT_SEED) -> dict:
    """Registered split over U = every atom of the input frame (all statuses, before any filtering), as written into
    Question.split at the question freeze. unit='cluster' (sensitivity, prereg §5.1.7): whole clusters (conflict
    family, else guideline) are split with the same fractions and seeds, and every atom takes its cluster's side."""
    atoms = df.drop_duplicates("atom_id")
    if unit == "atom":
        ids = np.sort(atoms["atom_id"].astype(str).unique())
        return dict(zip(ids, assign_rq3_split(ids, seed=seed)))
    if unit != "cluster":
        raise ValueError("unit phải là 'atom' hoặc 'cluster'")
    ck = pd.Series(cluster_key(atoms, "family"), index=atoms["atom_id"].astype(str).to_numpy())
    units = np.sort(ck.unique())
    side = dict(zip(units, assign_rq3_split(units, seed=seed)))
    return {a: side[c] for a, c in ck.items()}


# ------------------------------------------------------------------ RQ3: score model
def fit_logistic_l2(X: np.ndarray, y: np.ndarray, C: float = RQ3_LOGIT_C, max_iter: int = RQ3_LOGIT_MAX_ITER):
    """L2-penalised logistic regression, objective 0.5*||w||^2 + C * sum log-loss (intercept not penalised), the
    objective of scikit-learn's LogisticRegression(penalty='l2', C=C); minimised by L-BFGS (scipy)."""
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    p = X.shape[1]

    def f(theta):
        w, b = theta[:p], theta[p]
        z = X @ w + b
        ll = np.logaddexp(0.0, z) - y * z
        g = expit(z) - y
        return 0.5 * w @ w + C * ll.sum(), np.r_[w + C * (X.T @ g), C * g.sum()]

    res = optimize.minimize(f, np.zeros(p + 1), jac=True, method="L-BFGS-B", options={"maxiter": max_iter})
    return res.x[:p], float(res.x[p])


def group_kfold(groups: Sequence[str], n_splits: int) -> np.ndarray:
    """Deterministic GroupKFold: groups sorted by size (descending, ties by label) are assigned one by one to the
    fold with the fewest rows so far (ties: lowest fold index). Returns the fold index of every row."""
    g = np.asarray(groups).astype(str)
    uniq, counts = np.unique(g, return_counts=True)
    order = sorted(range(len(uniq)), key=lambda i: (-counts[i], uniq[i]))
    load = np.zeros(n_splits)
    fold_of = {}
    for i in order:
        f = int(np.argmin(load))
        fold_of[uniq[i]] = f
        load[f] += counts[i]
    return np.asarray([fold_of[x] for x in g])


def _design(d: pd.DataFrame, ref: np.ndarray, features: Sequence[str]) -> np.ndarray:
    """Feature matrix: logprob missing -> reference-split median plus a missingness indicator; every column
    standardised with reference-split mean and SD (SD 0 -> 1)."""
    cols = []
    for f in features:
        x = pd.to_numeric(d[f], errors="coerce").to_numpy(dtype=float)
        if f == "logprob":
            miss = np.isnan(x)
            med = float(np.nanmedian(x[ref])) if np.any(ref & ~miss) else 0.0
            cols += [np.where(miss, med, x), miss.astype(float)]
        else:
            if np.isnan(x).any():
                raise ValueError(f"RQ3: đặc trưng {f} bị thiếu")
            cols.append(x)
    X = np.column_stack(cols)
    mu, sd = X[ref].mean(axis=0), X[ref].std(axis=0)
    return (X - mu) / np.where(sd > 0, sd, 1.0)


def rq3_scores(d: pd.DataFrame, split: np.ndarray, *, features: Sequence[str] = RQ3_FEATURES,
               max_folds: int = RQ3_MAX_FOLDS, fit: Callable = fit_logistic_l2) -> np.ndarray:
    """Confidence score c(x) = P(correct) from the registered L2 logistic model fit on the reference split only.
    Reference rows get out-of-fold scores from GroupKFold by guideline with min(max_folds, #reference guidelines)
    folds; calibration and test rows are scored by the model refit on the whole reference split."""
    ref = np.asarray(split) == "ref"
    if not ref.any():
        raise ValueError("RQ3: phần tham chiếu rỗng")
    X = _design(d, ref, features)
    y = d["C"].to_numpy(dtype=float)                   # target: correct (labels 1-2)
    s = np.full(len(d), np.nan)
    w, b = fit(X[ref], y[ref])
    s[~ref] = expit(X[~ref] @ w + b)
    gl = d["guideline"].astype(str).to_numpy()[ref]
    k = min(max_folds, len(np.unique(gl)))
    idx = np.flatnonzero(ref)
    if k >= 2:
        folds = group_kfold(gl, k)
        for f in range(k):
            tr, te = idx[folds != f], idx[folds == f]
            wf, bf = fit(X[tr], y[tr])
            s[te] = expit(X[te] @ wf + bf)
    else:
        s[idx] = expit(X[idx] @ w + b)
    return s


def rq3_frame(df: pd.DataFrame, *, model: str, language: str = "vi", condition: str = "A2",
              loss: str = "value_error") -> tuple[pd.DataFrame, int]:
    """Served answers of ONE model in ONE language, one row per atom (prereg §5.1.7). loss='value_error' (primary)
    keeps value-stating answers (labels 1-5) and returns the number of self-abstentions (label 6) separately."""
    d = _subset(prepare(df), condition=condition, language=language, models=[model])
    if d.empty:
        raise ValueError(f"RQ3: không có câu trả lời phục vụ cho {model}/{language}")
    if d["atom_id"].duplicated().any():
        raise ValueError("RQ3: mỗi mẩu chỉ được một câu trả lời (một mô hình, một ngôn ngữ)")
    bad = set(d["group_signal"].unique()) - set(RQ3_GROUPS)
    if bad:
        raise ValueError(f"RQ3: nhóm lạ {bad}")
    n_abst = int((~d["V"]).sum())
    if loss == "value_error":
        d = d[d["V"]]
    elif loss != "W":
        raise ValueError("loss phải là 'value_error' hoặc 'W'")
    return d.reset_index(drop=True), n_abst


def _alpha_by_group(n_cal_atoms: Mapping[str, int], alpha: float, alpha_fallback: float,
                    min_cal_atoms: int) -> dict:
    """DR4 (label-free): alpha_fallback for a group with fewer than min_cal_atoms calibration atoms."""
    return {g: (alpha_fallback if n < min_cal_atoms else alpha) for g, n in n_cal_atoms.items()}


def _bounds_and_ltt(s, e, g, atoms, sp, *, coverages, delta, alpha, alpha_fallback, min_cal_atoms, groups):
    ref, cal, test = sp == "ref", sp == "cal", sp == "test"
    pool = cal | test
    for grp in groups:
        if not np.any(ref & (g == grp)):
            raise ValueError(f"RQ3: nhóm '{grp}' không có mẫu trong phần tham chiếu")
    thr = ltt.thresholds_from_reference(s[ref], g[ref], tuple(coverages))
    bounds = ltt.certified_bounds(s[cal], e[cal], g[cal], thr, delta)
    rows = []
    for (grp, c), b in sorted(bounds.items(), key=lambda kv: (str(kv[0][0]), -kv[0][1])):
        lam = thr[grp][c]
        mp, mt = pool & (g == grp) & (s >= lam), test & (g == grp)
        pool_risk = float(e[mp].mean()) if mp.any() else float("nan")
        rows.append({"group": str(grp), "coverage_target": float(c), "threshold": float(lam), "n": b["n"],
                     "k": b["k"], "empirical": b["emp"], "U": float(b["U"]), "pool_risk": pool_risk,
                     "violation_pool": bool(np.isfinite(pool_risk) and pool_risk > b["U"]),
                     "test_coverage": float((s[mt] >= lam).mean()) if mt.any() else float("nan")})
    n_cal_atoms = {str(grp): int(len(set(atoms[cal & (g == grp)]))) for grp in groups}
    alpha_g = _alpha_by_group(n_cal_atoms, alpha, alpha_fallback, min_cal_atoms)
    grids = ltt.make_grids(s[ref], g[ref])
    G = len(groups)
    lt = {}
    for grp in groups:
        lam = ltt.ltt_thresholds(s[cal], e[cal], g[cal], {grp: grids[grp]}, alpha=alpha_g[grp], delta=delta / G)[grp]
        mc, mt, mp = cal & (g == grp), test & (g == grp), pool & (g == grp)
        at, ap = mt & (s >= lam), mp & (s >= lam)
        lt[grp] = {"alpha_used": alpha_g[grp], "n_cal_atoms": n_cal_atoms[grp], "threshold": float(lam),
                   "certified": bool(np.isfinite(lam)),
                   "coverage_cal": float((s[mc] >= lam).mean()) if mc.any() else float("nan"),
                   "coverage_test": float((s[mt] >= lam).mean()) if mt.any() else float("nan"),
                   "risk_test": float(e[at].mean()) if at.any() else float("nan"),
                   "risk_pool": float(e[ap].mean()) if ap.any() else float("nan"),
                   "violation_pool": bool(ap.any() and e[ap].mean() > alpha_g[grp])}
    return thr, rows, lt, alpha_g


def certified_rq3(df: pd.DataFrame, *, model: str, language: str = "vi", split_col: str = "split",
                  split_unit: str = "atom", loss: str = "value_error", condition: str = "A2",
                  coverages: Sequence[float] = RQ3_COVERAGES, delta: float = RQ3_DELTA, alpha: float = RQ3_ALPHA,
                  alpha_fallback: float = RQ3_ALPHA_FALLBACK, min_cal_atoms: int = RQ3_MIN_CAL_ATOMS,
                  min_useful_coverage: float = RQ3_MIN_USEFUL_COVERAGE, seed: int = SPLIT_SEED,
                  groups: Sequence[str] = RQ3_GROUPS, features: Sequence[str] = RQ3_FEATURES,
                  n_rerandomise: int = 0) -> dict:
    """RQ3 regime (a) for ONE open model (prereg §5.1.7; skill certified-abstention).

    Unit: one served answer per atom in `language` (primary 'vi'); primary loss 'value_error' on value-stating
    answers (label 6 = model self-abstention, reported as coverage loss). Split: the `split` column when every row
    carries ref/cal/test (Question.split), else split_map over every atom of the input frame (unit 'atom';
    'cluster' = sensitivity). Score: rq3_scores (reference split only). Primary: simultaneous CP upper bounds U_gk
    (confidence 1 - delta/(G*K)); secondary: Learn-then-Test per group (DR4 alpha fallback, Bonferroni over G);
    DR5 usefulness. Violations are judged against the POOL risk (calibration U test).
    n_rerandomise > 0 adds the implementation check of prereg §5.1.7 (rq3_rerandomise)."""
    if split_col in df.columns and df[split_col].isin(["ref", "cal", "test"]).all() and split_unit == "atom":
        smap = dict(zip(df["atom_id"].astype(str), df[split_col]))
        split_source = "column"
    else:
        smap = split_map(df, unit=split_unit, seed=seed)
        split_source = f"split_map(unit={split_unit}, seed={seed})"
    d, n_abst = rq3_frame(df, model=model, language=language, condition=condition, loss=loss)
    sp = d["atom_id"].astype(str).map(smap).to_numpy(dtype=object)
    s = rq3_scores(d, sp, features=features)
    e = (d["E"] if loss == "value_error" else d["W"]).to_numpy(dtype=int)
    g = d["group_signal"].to_numpy(dtype=object)
    atoms = d["atom_id"].to_numpy(dtype=object)
    kw = dict(coverages=coverages, delta=delta, alpha=alpha, alpha_fallback=alpha_fallback,
              min_cal_atoms=min_cal_atoms, groups=groups)
    thr, rows, lt, alpha_g = _bounds_and_ltt(s, e, g, atoms, sp, **kw)
    test = sp == "test"
    cov_dis = lt["disagree"]["coverage_test"] if "disagree" in lt else float("nan")
    baseline = {str(grp): float(e[test & (g == grp)].mean()) if np.any(test & (g == grp)) else float("nan")
                for grp in groups}
    out = {
        "model": model, "language": language, "loss": loss, "split_unit": split_unit,
        "bounds": rows, "ltt": lt, "G": len(groups), "K": len(coverages), "delta": delta,
        "bound_confidence_each": 1 - delta / (len(groups) * len(coverages)),
        "dr4_alpha_by_group": alpha_g, "dr5_useful_disagree": bool(np.isfinite(cov_dis) and
                                                                   cov_dis >= min_useful_coverage),
        "min_useful_coverage": min_useful_coverage, "baseline_full_coverage_risk_test": baseline,
        "abstain_all_disagree": {"coverage_test": float(np.mean(g[test] == "agree")) if test.any() else float("nan"),
                                 "risk_test": baseline.get("agree", float("nan"))},
        "any_bound_violation_pool": any(r["violation_pool"] for r in rows),
        "n_rows": {"ref": int((sp == "ref").sum()), "cal": int((sp == "cal").sum()), "test": int(test.sum())},
        "n_self_abstain": n_abst, "self_abstention_rate": n_abst / (n_abst + len(d)) if (n_abst + len(d)) else
        float("nan"), "split_source": split_source,
    }
    if n_rerandomise:
        out["rerandomisation"] = rq3_rerandomise(s, e, g, atoms, sp, n=n_rerandomise, seed=seed, **kw)
    return out


def rq3_rerandomise(s, e, g, atoms, sp, *, n: int = RQ3_RERANDOMISATIONS, seed: int = SPLIT_SEED,
                    coverages=RQ3_COVERAGES, delta=RQ3_DELTA, alpha=RQ3_ALPHA, alpha_fallback=RQ3_ALPHA_FALLBACK,
                    min_cal_atoms=RQ3_MIN_CAL_ATOMS, groups=RQ3_GROUPS) -> dict:
    """Regime (a) implementation check: the reference split, score and thresholds are held fixed; the calibration
    and test halves of the non-reference atoms are redrawn n times (re-draw i: ltt.split_by_atom(non-reference
    atoms, 0.5, seed=[seed, 1, i])). Reports how often any of the G*K bounds (or any group's LTT risk) is exceeded
    by the pool risk. By construction this checks the implementation, not transfer to new questions."""
    sp = np.asarray(sp, dtype=object)
    nonref = sp != "ref"
    vb = vl = 0
    kw = dict(coverages=coverages, delta=delta, alpha=alpha, alpha_fallback=alpha_fallback,
              min_cal_atoms=min_cal_atoms, groups=groups)
    for i in range(n):
        spi = sp.copy()
        cal = ltt.split_by_atom(np.asarray(atoms)[nonref].astype(str), frac_cal=0.5, seed=[seed, 1, i])
        spi[np.flatnonzero(nonref)] = np.where(cal, "cal", "test")
        _, rows, lt, _ = _bounds_and_ltt(s, e, g, atoms, spi, **kw)
        vb += any(r["violation_pool"] for r in rows)
        vl += any(v["violation_pool"] for v in lt.values())
    return {"n": n, "bound_violation_rate": vb / n if n else float("nan"),
            "ltt_violation_rate": vl / n if n else float("nan"), "target": delta}


def rq3_regime_b(df: pd.DataFrame, *, model: str, language: str = "vi", n_splits: int = RQ3_REGIME_B_SPLITS,
                 seed: int = SPLIT_SEED, loss: str = "value_error", condition: str = "A2",
                 coverages: Sequence[float] = RQ3_COVERAGES, delta: float = RQ3_DELTA, alpha: float = RQ3_ALPHA,
                 alpha_fallback: float = RQ3_ALPHA_FALLBACK, min_cal_atoms: int = RQ3_MIN_CAL_ATOMS,
                 fractions: Sequence[tuple[str, float]] = RQ3_SPLIT_FRACTIONS,
                 max_violation: float = RQ3_REGIME_B_MAX_VIOLATION, groups: Sequence[str] = RQ3_GROUPS,
                 features: Sequence[str] = RQ3_FEATURES, fit: Callable = fit_logistic_l2) -> dict:
    """RQ3 regime (b) for ONE model: split by GUIDELINE (unseen guidelines). Split i permutes the sorted guideline
    ids with default_rng([seed, i]); the first round(0.2 N_g) are reference, the next round(0.4 N_g) calibration.
    In every split the score model is REFIT on the reference guidelines only (rq3_scores), so test guidelines never
    touch the score. Two violation frequencies vs 2*delta: any of the G*K bounds exceeded by the empirical risk on
    test guidelines; any group's test-guideline risk at the LTT threshold above alpha_g."""
    d, _ = rq3_frame(df, model=model, language=language, condition=condition, loss=loss)
    e = (d["E"] if loss == "value_error" else d["W"]).to_numpy(dtype=int)
    g = d["group_signal"].to_numpy(dtype=object)
    gl = d["guideline"].astype(str).to_numpy()
    atoms = d["atom_id"].to_numpy(dtype=object)
    ug = np.unique(gl)
    fr = dict(fractions)
    n_ref, n_cal = max(1, round(fr["ref"] * len(ug))), max(1, round(fr["cal"] * len(ug)))
    if n_ref + n_cal >= len(ug):
        raise ValueError("RQ3 chế độ (b): quá ít hướng dẫn để chia ref/cal/test")
    G = len(groups)
    vb = vl = done = 0
    for i in range(n_splits):
        perm = np.random.default_rng([seed, i]).permutation(ug)
        ref, cal = np.isin(gl, perm[:n_ref]), np.isin(gl, perm[n_ref:n_ref + n_cal])
        test = ~(ref | cal)
        if not all(np.any(ref & (g == grp)) and np.any(cal & (g == grp)) for grp in groups):
            continue
        done += 1
        sp = np.where(ref, "ref", np.where(cal, "cal", "test")).astype(object)
        s = rq3_scores(d, sp, features=features, fit=fit)
        thr = ltt.thresholds_from_reference(s[ref], g[ref], tuple(coverages))
        bnd = ltt.certified_bounds(s[cal], e[cal], g[cal], thr, delta)
        viol = False
        for (grp, c), b in bnd.items():
            m = test & (g == grp) & (s >= thr[grp][c])
            viol |= bool(m.any() and e[m].mean() > b["U"])
        vb += viol
        grids = ltt.make_grids(s[ref], g[ref])
        n_at = {grp: len(set(atoms[cal & (g == grp)])) for grp in groups}
        a_g = _alpha_by_group(n_at, alpha, alpha_fallback, min_cal_atoms)
        bad = False
        for grp in groups:
            lam = ltt.ltt_thresholds(s[cal], e[cal], g[cal], {grp: grids[grp]}, alpha=a_g[grp], delta=delta / G)[grp]
            m = test & (g == grp) & (s >= lam)
            bad |= bool(m.any() and e[m].mean() > a_g[grp])
        vl += bad
    rb, rl = (vb / done if done else float("nan")), (vl / done if done else float("nan"))
    return {"model": model, "language": language, "n_splits": n_splits, "n_used": done,
            "bound_violation_rate": rb, "ltt_violation_rate": rl, "max_violation": max_violation,
            "bound_acceptable": bool(rb <= max_violation), "ltt_acceptable": bool(rl <= max_violation),
            "n_guidelines": len(ug), "seed": seed, "score_refit_per_split": True}


# ------------------------------------------------------------------ registered sensitivity analyses
def missing_bounds(df: pd.DataFrame, *, models: Iterable[str] | None = None, n_boot: int = N_BOOT,
                   seed: int = BOOT_SEED, trigger: float = MISSING_BOUND_TRIGGER) -> dict:
    """Extreme-case imputation (prereg §5.5) for H1, H3 (per model) and H4 when the analysis cell has more than
    `trigger` missing responses (label NaN). H1: missing -> label 4 (raises Delta) / label 5 + decoy match (lowers).
    H3: missing -> label 4 (raises r_m) / label 2 (lowers). H4: missing in the disagreement group -> label 4 and in
    the agreement group -> label 2 (raises RR), and the reverse (lowers). Cells below the trigger are not re-run."""
    g = df
    if "temperature" in g.columns:
        g = g[g["temperature"].fillna(0).astype(float) == 0]
    if "sample_idx" in g.columns:
        g = g[g["sample_idx"].fillna(0).astype(int) == 0]
    ms = list(models) if models is not None else None
    sel = (g["format"] == "short") & (g["conflict_status"] != "indistinguishable")
    if ms is not None:
        sel &= g["model"].isin(ms)
    out = {}

    def fill(mask, **vals):
        x = df.copy()
        idx = x.index.isin(g.index[mask]) & x["label"].isna()
        for k, v in vals.items():
            x.loc[idx, k] = v(x.loc[idx]) if callable(v) else v
        return x

    h1m = sel & (g["condition"] == "A1") & (g["language"] == "vi") & (g["conflict_status"] == "conflict") & \
        _as_bool(g["has_decoy"])
    sh = float(g.loc[h1m, "label"].isna().mean()) if h1m.any() else 0.0
    out["h1"] = {"missing_share": sh, "triggered": sh > trigger}
    if sh > trigger:
        hi = h1_delta(fill(h1m, label=4, decoy_match=False), n_boot, seed, models=ms)
        lo = h1_delta(fill(h1m, label=5, decoy_match=True), n_boot, seed, models=ms)
        out["h1"].update({"high": {k: hi[k] for k in ("delta", "ci_lo", "ci_hi")},
                          "low": {k: lo[k] for k in ("delta", "ci_lo", "ci_hi")}})
    h3m = sel & (g["condition"] == "A3") & (g["language"] == "vi") & (g["conflict_status"] == "conflict")
    sh = float(g.loc[h3m, "label"].isna().mean()) if h3m.any() else 0.0
    out["h3"] = {"missing_share": sh, "triggered": sh > trigger}
    if sh > trigger:
        out["h3"]["high_p_pc"] = h3_per_model(fill(h3m, label=4), models=ms)["p_pc"]
        out["h3"]["low_p_pc"] = h3_per_model(fill(h3m, label=2), models=ms)["p_pc"]
    if "group_signal" in g.columns:
        h4m = sel & (g["condition"] == "A2") & g["group_signal"].isin(RQ3_GROUPS)
        sh = float(g.loc[h4m, "label"].isna().mean()) if h4m.any() else 0.0
        out["h4"] = {"missing_share": sh, "triggered": sh > trigger}
        if sh > trigger:
            up = lambda x: np.where(x["group_signal"].eq("disagree"), 4, 2)  # noqa: E731
            down = lambda x: np.where(x["group_signal"].eq("disagree"), 2, 4)  # noqa: E731
            hi = h4_risk_ratio(fill(h4m, label=up), n_boot=n_boot, seed=seed, models=ms)
            lo = h4_risk_ratio(fill(h4m, label=down), n_boot=n_boot, seed=seed, models=ms)
            out["h4"].update({"high": {k: hi[k] for k in ("rr", "ci_lo", "p_one_sided")},
                              "low": {k: lo[k] for k in ("rr", "ci_lo", "p_one_sided")}})
    return out


def cp_upper_one_sided(k: int, n: int, level: float = 0.95) -> float:
    """One-sided exact (Clopper-Pearson) upper bound for a proportion k/n."""
    return 1.0 if k >= n else float(stats.beta.ppf(level, k + 1, n - k))


def tipping_point_h1(df: pd.DataFrame, *, false_conflicts_found: int, n_checked: int,
                     models: Iterable[str] | None = None, n_boot: int = N_BOOT, seed: int = BOOT_SEED,
                     primary: str = PRIMARY_RULE) -> dict:
    """Tipping point for H1 under false conflicts (prereg §5.6 B.20). Worst case: the false conflict atoms are those
    contributing most to Delta (atoms ranked by sum over models of F - k*D, ties by atom_id). t* = the smallest
    number of top-ranked atoms whose removal makes the registered lower limit <= 0 (bisection, then t*-1 and t*
    are re-evaluated). Compared with the one-sided 95% CP upper bound of the false-conflict proportion (from the
    manual check of `n_checked` conflict atoms) times the number of conflict atoms. Robust iff t* > that number."""
    d, _ = _h1_set(df, models=models, language="vi", condition="A1")
    contrib = (d["label"].eq(4).astype(float) - d["k_foreign"] * d["decoy_match"].astype(float)).groupby(
        d["atom_id"]).sum()
    order = sorted(contrib.index, key=lambda a: (-contrib[a], str(a)))
    N = len(order)

    def supported(t: int) -> bool:
        drop = set(order[:t])
        keep = df[~df["atom_id"].isin(drop)]
        try:
            return h1_delta(keep, n_boot, seed, models=models, primary=primary)["confirmed"]
        except ValueError:
            return False

    if not supported(0):
        t_star = 0
    else:
        lo, hi = 0, N
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if supported(mid):
                lo = mid
            else:
                hi = mid
        t_star = hi
    U = cp_upper_one_sided(false_conflicts_found, n_checked)
    return {"t_star": t_star, "n_conflict_atoms": N, "false_conflict_cp_upper": U,
            "worst_case_false_conflicts": U * N, "robust": bool(t_star > U * N)}


def tipping_point_h3(df: pd.DataFrame, *, p_h2: float, p_h4: float, false_conflicts_found: int, n_checked: int,
                     models: Iterable[str] | None = None) -> dict:
    """Tipping point for H3 (prereg §5.6 B.20): atoms ranked by the number of models answering label 3|4 at A3 (ties
    by atom_id); t* = smallest number of top-ranked atoms whose removal makes H3 no longer confirmed by Holm (H2
    and H4 p-values held fixed). Robust iff t* > CP upper bound of the false-conflict share x conflict atoms."""
    d = _subset(prepare(df), condition="A3", language="vi", models=models)
    d = d[d["conflict_status"] == "conflict"]
    contrib = d["label"].isin([3, 4]).astype(float).groupby(d["atom_id"]).sum()
    order = sorted(contrib.index, key=lambda a: (-contrib[a], str(a)))
    N = len(order)

    def confirmed(t: int) -> bool:
        try:
            p = h3_per_model(df[~df["atom_id"].isin(set(order[:t]))], models=models)["p_pc"]
        except ValueError:
            return False
        return holm({"H2": p_h2, "H3": p, "H4": p_h4})["H3"]["reject"]

    if not confirmed(0):
        t_star = 0
    else:
        lo, hi = 0, N
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if confirmed(mid):
                lo = mid
            else:
                hi = mid
        t_star = hi
    U = cp_upper_one_sided(false_conflicts_found, n_checked)
    return {"t_star": t_star, "n_conflict_atoms": N, "false_conflict_cp_upper": U,
            "worst_case_false_conflicts": U * N, "robust": bool(t_star > U * N)}


# ------------------------------------------------------------------ simulation
DEFAULT_EFFECT = {
    "pi_foreign": 0.30,        # H1: P(label 4) at A1-VI on conflict atoms with k_i = 1 (pilot scale: 30% vs 5%)
    "pi_decoy": 0.05,          # H1: P(decoy match) per target; atoms with k_i = 2 get pi_foreign + pi_decoy
    "frac_k2": 0.3,            # share of conflict atoms with k_i = 2 conflicting foreign targets
    "frac_no_decoy": 0.05,     # conflict atoms without a decoy (D = 0; excluded from H1/H2 by the registered rule)
    "kappa_family": 8.0,       # Beta concentration of cluster-level rates (ICC ~ 1/(1 + kappa))
    "kappa_atom": 10.0,        # Beta concentration of atom-level rates around the cluster rate
    "kappa_direction": 6.0,    # cluster heterogeneity of P(foreign | a source value is matched)
    "model_spread": 0.3,       # model multipliers evenly spaced in [1 - spread, 1 + spread] (mean 1)
    "a0_mult": 1.3,            # A0 source-match multiplier (descriptive only)
    "h2_en_mult": 1.5,         # H2: EN multiplier of the source-match rate on us_unique atoms (1 = null)
    "a3_rate": 0.10,           # H3: P(label 3|4 | A3, conflict atom); scalar or one value per model
    "h4_base": 0.08,           # H4: P(value error | agree, value stated) at A2 (x model multiplier)
    "h4_rr": 3.0,              # H4: within-stratum P(value error | disagree) / P(value error | agree)
    "kappa_h4": 20.0,          # concentration for the A2 error risk (kept high so rr * risk rarely clips at 1)
    "p_disagree": 0.25,        # mean share of the disagreement group
    "disagree_spread": 0.6,    # model-specific disagreement shares p_disagree * [1 - s, 1 + s] (Simpson confounding)
    "abstain_agree": 0.02,     # A2 self-abstention (label 6) in the agreement group
    "abstain_disagree": 0.12,  # ... and in the disagreement group (abstentions pile up where signals fire)
    "frac_us_unique": 0.4,     # share of conflict atoms whose US value differs from every other source
    "frac_superseded": 0.3,    # share of atoms with a distinct superseded MoH value
    "concordant_per_family": 5,
    "n_guidelines": 30,
    "family_size_sigma": 0.0,  # > 0: lognormal family sizes with mean atoms_per_family (unequal clusters)
    "logprob_missing": 0.05,   # share of A2 answers without a log-probability (RQ3 feature)
}
# Global null: H1 pi_f = pi_d (k-weighted), H2 no language effect, H3 every model exactly at the margin, H4 RR at
# the bound within every model x language stratum (with abstentions and model heterogeneity kept).
NULL_EFFECT = {"pi_foreign": 0.05, "pi_decoy": 0.05, "h2_en_mult": 1.0, "a3_rate": H3_MARGIN, "h4_rr": H4_RR_BOUND}
_FOREIGN_SETS = ("US,EU_UK", "WHO_global", "EU_UK", "WHO_WPRO", "US,WHO_global")


def _beta_mean(rng: np.random.Generator, mean, kappa: float, size=None) -> np.ndarray:
    m = np.clip(np.asarray(mean, dtype=float), 1e-6, 1 - 1e-6)
    return rng.beta(m * kappa, (1 - m) * kappa, size=size)


def _draw_cat(rng: np.random.Generator, probs: np.ndarray, cats: Sequence[int]) -> np.ndarray:
    cum = np.cumsum(probs / probs.sum(axis=1, keepdims=True), axis=1)
    idx = (rng.random(len(probs))[:, None] > cum).sum(axis=1)
    return np.asarray(cats)[np.minimum(idx, len(cats) - 1)]


def simulate_study(seed: int, n_families: int = 40, atoms_per_family: int = 10, models: int = 4,
                   effect: Mapping[str, float] | None = None) -> pd.DataFrame:
    """Simulated graded answers with the study's structure (proposal §5.2): conflict families (clusters) of conflict
    atoms, concordant atoms clustered by guideline, `models` open models x VI/EN x A0-A3, short answers, greedy.

    Every null in NULL_EFFECT holds EXACTLY in the superpopulation:
    H1  a 'source match' event S with atom mean pf_i + pd_i (pf_i = pi_foreign + (k_i - 1) pi_decoy, pd_i = pi_decoy
        or 0 without a decoy; cluster multiplier 2u, u ~ Beta(mean 1/2)) is split into foreign vs decoy with atom
        mean q_i = pf_i / (pf_i + pd_i) and a mean-preserving cluster perturbation; so E[F - k D] = pi_f - pi_d.
    H2  the EN source-match rate on us_unique atoms is multiplied by h2_en_mult.
    H3  per-model cluster rates with mean a3_rate[m], comonotone across models.
    H4  A2: model-specific disagreement shares and base risks (confounded across models), self-abstention (label 6)
        more frequent under disagreement, value error with within-stratum RR = h4_rr among value-stating answers.
    RQ3 features s1/s2/s3 (disagreement = any fired), consistency and log-probability depend on the error (the
        score is fitted by the registered model; real scores are label-free).
    `effect` overrides DEFAULT_EFFECT."""
    e = {**DEFAULT_EFFECT, **(effect or {})}
    rng = np.random.default_rng(seed)
    F, apf, cpf, M = int(n_families), int(atoms_per_family), int(e["concordant_per_family"]), int(models)
    if e["family_size_sigma"] > 0:
        sig = float(e["family_size_sigma"])
        sizes = np.maximum(1, np.round(rng.lognormal(math.log(apf) - sig ** 2 / 2, sig, F))).astype(int)
    else:
        sizes = np.full(F, apf)
    nG = max(1, min(int(e["n_guidelines"]), F))
    fam_gl = np.arange(F) % nG
    n_conf, n_conc = int(sizes.sum()), F * cpf
    A = n_conf + n_conc
    is_conf = np.r_[np.ones(n_conf, bool), np.zeros(n_conc, bool)]
    fam = np.r_[np.repeat(np.arange(F), sizes), np.full(n_conc, -1)]
    gl = np.r_[fam_gl[np.repeat(np.arange(F), sizes)], fam_gl[np.repeat(np.arange(F), cpf)]]
    cl = np.where(is_conf, fam, F + gl)                     # simulation cluster: family, or guideline
    CL = F + nG
    has_sup = rng.random(A) < e["frac_superseded"]
    us_unique = is_conf & (rng.random(A) < e["frac_us_unique"])
    k_i = np.where(is_conf, np.where(rng.random(A) < e["frac_k2"], 2, 1), 0)
    has_decoy = is_conf & (rng.random(A) >= e["frac_no_decoy"])
    fsys = np.where(us_unique, "US", np.asarray(_FOREIGN_SETS, dtype=object)[rng.integers(len(_FOREIGN_SETS), size=A)])
    fsys = np.where(is_conf, fsys, "")
    rho = np.linspace(1 - e["model_spread"], 1 + e["model_spread"], M) if M > 1 else np.ones(1)
    dmult = np.linspace(1 - e["disagree_spread"], 1 + e["disagree_spread"], M) if M > 1 else np.ones(1)
    decoy_rule = np.where(rng.random(A) < 0.85, "mirror_arith", np.where(rng.random(A) < 0.7, "mirror_geom",
                                                                          "mirror_far"))
    roundness_ok = rng.random(A) < 0.8
    neighbour = is_conf & (rng.random(A) < 0.05)
    passage_alt = is_conf & (rng.random(A) < 0.10)

    # latent rates ----------------------------------------------------------------------------------------------
    pd_i = np.where(has_decoy, e["pi_decoy"], 0.0)
    pf_i = np.where(is_conf, e["pi_foreign"] + (k_i - 1) * e["pi_decoy"], 0.0)
    base = pf_i + pd_i
    u_cl = _beta_mean(rng, 0.5, e["kappa_family"], CL)
    ps_atom = np.where(base > 0, _beta_mean(rng, np.clip(base * 2 * u_cl[cl], 1e-6, 1 - 1e-6), e["kappa_atom"]), 0.0)
    q_i = np.where(base > 0, pf_i / np.where(base > 0, base, 1), 0.0)
    d_cl = _beta_mean(rng, 0.5, e["kappa_direction"], CL)
    q_atom = q_i + (d_cl[cl] - 0.5) * 2 * np.minimum(q_i, 1 - q_i)
    r3 = np.broadcast_to(np.asarray(e["a3_rate"], dtype=float), (M,))
    u3 = rng.random(CL)
    p3_cl = np.stack([stats.beta.ppf(u3, max(r, 1e-6) * e["kappa_family"], max(1 - r, 1e-6) * e["kappa_family"])
                      for r in r3], axis=1)                  # (CL, M), comonotone across models
    pdis_cl = _beta_mean(rng, e["p_disagree"], e["kappa_family"], CL)
    b_cl = _beta_mean(rng, e["h4_base"], e["kappa_h4"], CL)
    b_atom = _beta_mean(rng, b_cl[cl], e["kappa_h4"])

    # units = (atom, model, language) --------------------------------------------------------------------------
    ua = np.repeat(np.arange(A), M * 2)
    um = np.tile(np.repeat(np.arange(M), 2), A)
    en = np.tile(np.array([False, True]), A * M)
    U = len(ua)
    conf_u, sup_u = is_conf[ua], has_sup[ua]
    disagree = rng.random(U) < np.clip(pdis_cl[cl[ua]] * dmult[um], 0, 1)

    def background(n_rows_mask: np.ndarray, table: dict) -> np.ndarray:
        cats = (1, 2, 3, 5, 6)
        pr = np.array([[table["c"][k] if c else table["n"][k] for k in range(5)] for c in (True, False)])
        probs = np.where(conf_u[n_rows_mask][:, None], pr[0], pr[1]).copy()
        probs[:, 2] *= sup_u[n_rows_mask]
        return _draw_cat(rng, probs, cats)

    bg_short = {"c": (0.05, 0.70, 0.08, 0.10, 0.07), "n": (0.02, 0.83, 0.05, 0.06, 0.04)}
    blocks = []
    for cond in ("A0", "A1", "A2", "A3"):
        label = np.zeros(U, dtype=int)
        decoy = np.zeros(U, dtype=bool)
        side = np.full(U, "", dtype=object)
        feats = {k: np.full(U, np.nan) for k in RQ3_FEATURES}
        if cond in ("A0", "A1"):
            mult = e["a0_mult"] if cond == "A0" else 1.0
            p = ps_atom[ua] * rho[um] * mult * np.where(en & us_unique[ua], e["h2_en_mult"], 1.0)
            S = conf_u & (rng.random(U) < np.clip(p, 0, 1))
            Fm = S & (rng.random(U) < q_atom[ua])
            label[Fm] = 4
            dm = S & ~Fm
            label[dm], decoy[dm] = 5, True
            rest = ~S
            label[rest] = background(rest, bg_short)
            u5 = (label == 5) & ~decoy
            side[u5] = np.where(rng.random(int(u5.sum())) < 0.5, "foreign", "decoy")
        elif cond == "A3":
            p3 = _beta_mean(rng, p3_cl[cl[ua], um], e["kappa_atom"])
            y = (conf_u | sup_u) & (rng.random(U) < p3)
            stale = sup_u & (~conf_u | (rng.random(U) < 0.3))
            label[y] = np.where(stale[y], 3, 4)
            rest = ~y
            label[rest] = background(rest, {"c": (0.05, 0.85, 0.0, 0.05, 0.05), "n": (0.05, 0.85, 0.0, 0.05, 0.05)})
        else:  # A2 served
            abst = rng.random(U) < np.where(disagree, e["abstain_disagree"], e["abstain_agree"])
            risk = b_atom[ua] * rho[um] * np.where(disagree, e["h4_rr"], 1.0)
            w = ~abst & (rng.random(U) < np.clip(risk, 0, 1))
            kind = rng.random(U)
            label[w] = np.where(conf_u[w] & (kind[w] < 0.6), 4, np.where(sup_u[w] & (kind[w] < 0.8), 3, 5))
            ok = ~abst & ~w
            label[ok] = np.where(rng.random(int(ok.sum())) < 0.9, 2, 1)
            label[abst] = 6
            fired = rng.random((U, 3)) < 0.6
            none = disagree & ~fired.any(axis=1)
            fired[none, rng.integers(3, size=int(none.sum()))] = True
            fired &= disagree[:, None]
            feats["s1"], feats["s2"], feats["s3"] = (fired[:, j].astype(float) for j in range(3))
            feats["consistency"] = np.where(w, rng.beta(2.5, 2.5, U), np.where(abst, rng.beta(1, 3, U),
                                                                               rng.beta(6, 2, U)))
            lp = np.where(w, rng.normal(-1.0, 0.4, U), rng.normal(-0.3, 0.4, U))
            feats["logprob"] = np.where(rng.random(U) < e["logprob_missing"], np.nan, lp)
        blocks.append(pd.DataFrame({
            "model": np.array([f"sim_m{i + 1}" for i in range(M)], dtype=object)[um],
            "atom_id": np.char.add("a", np.char.zfill(ua.astype(str), 5)),
            "conflict_family": np.where(is_conf[ua], np.char.add("fam", np.char.zfill(np.maximum(fam[ua], 0)
                                                                                     .astype(str), 3)), None),
            "guideline": np.char.add(np.char.add("gl", np.char.zfill(gl[ua].astype(str), 2)), "/2026"),
            "language": np.where(en, "en", "vi"), "condition": cond, "format": "short", "label": label,
            "decoy_match": decoy, "foreign_systems": np.where(label == 4, fsys[ua], ""),
            "conflict_status": np.where(conf_u, "conflict", "concordant"), "us_unique": us_unique[ua],
            "k_foreign": k_i[ua], "has_decoy": has_decoy[ua],
            "group_signal": np.where(disagree, "disagree", "agree"), **feats,
            "value_kind": "num", "decoy_rule": np.where(has_decoy[ua], decoy_rule[ua], ""),
            "roundness_ok": roundness_ok[ua] & has_decoy[ua], "moh_neighbour_overlap": neighbour[ua],
            "passage_has_alt_value": passage_alt[ua], "side": side,
            "parse_method": np.where(rng.random(U) < 0.95, "answer_line", "fallback"),
            "truncated": rng.random(U) < np.where(en, 0.01, 0.03),
            "sample_idx": 0, "temperature": 0.0,
        }))
    return pd.concat(blocks, ignore_index=True)


# ------------------------------------------------------------------ everything
def open_model_keys() -> list[str]:
    """Open-model keys from configs/models.yaml (the H1/H3 'open models')."""
    import yaml

    from vnsoc.paths import paths

    cfg = yaml.safe_load((paths().configs / "models.yaml").read_text(encoding="utf-8"))
    return [m["key"] for m in cfg.get("open") or []]


def resolve_models(df: pd.DataFrame, models: Iterable[str] | None = None) -> list[str]:
    """Explicit list, else configured open models present in df, else every model in df (simulation)."""
    present = sorted(df["model"].dropna().unique().tolist())
    if models is not None:
        return sorted(models)
    try:
        keys = [m for m in open_model_keys() if m in present]
    except (OSError, KeyError, TypeError):
        keys = []
    return keys or present


def _py(x):
    """JSON-safe copy: numpy -> python, NaN/inf -> None."""
    if isinstance(x, Mapping):
        return {str(k): _py(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_py(v) for v in x]
    if isinstance(x, np.ndarray):
        return [_py(v) for v in x.tolist()]
    if isinstance(x, (bool, np.bool_)):
        return bool(x)
    if isinstance(x, (int, np.integer)):
        return int(x)
    if isinstance(x, (float, np.floating)):
        return float(x) if np.isfinite(x) else None
    return x


def _safe(fn, *a, **kw):
    try:
        return fn(*a, **kw)
    except ValueError as e:
        return {"computed": False, "reason": str(e)}


def run_all(df: pd.DataFrame, *, models: Iterable[str] | None = None, n_boot: int = N_BOOT, seed: int = BOOT_SEED,
            rq3: bool = True, regime_b_splits: int = RQ3_REGIME_B_SPLITS,
            rerandomisations: int = RQ3_RERANDOMISATIONS) -> dict:
    """Every registered confirmatory result and its registered sensitivity analyses as one JSON-safe dict (prereg
    §5.0 table): H1 (+ per model, unscaled decoy B.7a, guideline clusters B.10, robustness S1/S2/S3/N1), H2 (+ clean
    pairs B.19), H3 (+ guideline clusters, without A3 passages that state a non-MoH value), H4 (primary MH value-
    error loss; secondary crude W loss, MH W loss, Vietnamese only), Holm over H2-H4, DR3, missing-data bounds, and
    RQ3 per open model (Vietnamese primary: regime (a) + re-randomisations + regime (b) + cluster split; English
    secondary: regime (a))."""
    ms = resolve_models(df, models)
    n_missing = int(df["label"].isna().sum())
    kw = dict(n_boot=n_boot, seed=seed)
    out = {"meta": {"models": ms, "n_rows": len(df), "n_rows_missing_label": n_missing, "n_boot": n_boot,
                    "seed": seed, "alpha_one_sided": ALPHA_ONE_SIDED, "ci_level": CI_LEVEL,
                    "decision_rule": PRIMARY_RULE}}
    out["h1"] = h1_delta(df, models=ms, **kw)
    out["h1_per_model"] = {m: h1_delta(df, models=[m], **kw) for m in ms}
    out["h1_unscaled_decoy"] = _safe(h1_delta, df, models=ms, decoy_weight="unscaled", **kw)
    out["h1_guideline_clusters"] = _safe(h1_delta, df, models=ms, cluster_by="guideline", **kw)
    out["h1_robustness"] = h1_robustness(df, models=ms, **kw)
    out["h2"] = h2_mcnemar_clustered(df, models=ms, **kw)
    if {"parse_method", "truncated"} <= set(df.columns):
        out["h2_clean_pairs"] = _safe(h2_mcnemar_clustered, df, models=ms, clean_only=True, **kw)
    out["h3"] = h3_per_model(df, models=ms)
    out["h3_guideline_clusters"] = _safe(h3_per_model, df, models=ms, cluster_by="guideline")
    if "passage_has_alt_value" in df.columns:
        out["h3_without_flagged_passages"] = _safe(h3_per_model, df[~_as_bool(df["passage_has_alt_value"])],
                                                   models=ms)
    out["h4"] = h4_risk_ratio(df, models=ms, **kw)
    out["h4_crude_W"] = _safe(h4_risk_ratio, df, models=ms, loss="W", estimator="crude", **kw)
    out["h4_mh_W"] = _safe(h4_risk_ratio, df, models=ms, loss="W", **kw)
    out["h4_vi_only"] = _safe(h4_risk_ratio, df, models=ms, language="vi", **kw)
    out["holm"] = holm({"H2": out["h2"]["p_one_sided"], "H3": out["h3"]["p_pc"], "H4": out["h4"]["p_one_sided"]})
    out["dr3"] = dr3_check(df, models=ms)
    out["missing_bounds"] = missing_bounds(df, models=ms, **kw)
    if rq3 and set(RQ3_FEATURES) <= set(df.columns):
        out["rq3"] = {}
        for m in ms:
            r = {"vi": _safe(certified_rq3, df, model=m, language="vi", n_rerandomise=rerandomisations),
                 "vi_cluster_split": _safe(certified_rq3, df, model=m, language="vi", split_unit="cluster"),
                 "en": _safe(certified_rq3, df, model=m, language="en")}
            r["vi_regime_b"] = (_safe(rq3_regime_b, df, model=m, language="vi", n_splits=regime_b_splits)
                                if regime_b_splits else None)
            out["rq3"][m] = r
    return _py(out)
