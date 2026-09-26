"""Pre-registered confirmatory analyses (T2.10; proposal §1.4, §4.6–4.7, §5.3–5.4; skills statistics-plan and
certified-abstention). Pure numpy / scipy / pandas; runs on SIMULATED data before any real model output exists.

Hypotheses (proposal §1.4). Only H1 is primary; H2–H4 form one Holm family.

  H1  h1_delta             A1, Vietnamese, short answers, conflict atoms, open models pooled.
                           Delta = P(label 4) - P(decoy_match); 95% CI by cluster bootstrap over conflict families
                           (BCa, acceleration by delete-one-cluster jackknife); < 20 clusters -> small-sample t interval
                           (jackknife SE over clusters, t with C-1 df). Confirmed iff ci_lo > 0 (proposal §5.3).
  H2  h2_mcnemar_clustered A1, (atom, model) pairs EN vs VI on us_unique atoms; outcome = label 4 with system US;
                           clustered McNemar test of Durkalski et al. (2003), clusters = conflict families; one-sided
                           (EN > VI).
  H3  h3_per_model         A3, atoms with a distinct foreign or superseded value; per open model the rate of labels
                           3|4, 95% CI = Clopper-Pearson on a design-effect (Kish) effective sample size with a t(C-1)
                           degrees-of-freedom adjustment; one-sided p for H0 rate <= 5%; "at least half of the open
                           models" = Bonferroni partial-conjunction p (M - u + 1) * p_(u), u = ceil(M/2).
  H4  h4_risk_ratio        A2 served answers; RR = P(wrong | disagree) / P(wrong | agree); cluster-bootstrap BCa CI on
                           log RR; one-sided p for H0 RR <= 2.
  --  holm                 Holm step-down over {H2, H3, H4}.
  RQ3 certified_rq3        wraps vnsoc.ltt (simultaneous Clopper-Pearson bounds at c_k = 100/75/50/25%, delta = 0.10,
                           G = 2; Learn-then-Test at alpha = 0.10, alpha = 0.15 for a group with < 300 calibration
                           atoms (DR4); certified coverage < 30% in the disagreement group -> not useful (DR5)).
      rq3_regime_b         split by guideline (unseen guidelines), 500 splits, violation rate vs 2*delta.
  DR3 dr3_check            A2, conflict atoms: upper 95% bound of P(label 3|4) < 5% for every model and language.

Decision level. Every CI is two-sided 95% (configs/project.yaml ci_level). "Lower 95% bound > null value" is the
same decision as "one-sided p < 0.025", so every one-sided p-value here is compared with ALPHA_ONE_SIDED = 0.025, and
Holm is run at that level. A Holm-adjusted p <= 0.025 confirms H2/H3/H4.

Input: one row per graded answer, long format. Required columns
  model, atom_id, conflict_family, guideline, language ('vi'|'en'), condition ('A0'..'A6'), format ('short'|...),
  label (1-6), decoy_match (bool), foreign_systems (str, e.g. "US,EU_UK"), us_unique (bool),
  group_signal ('agree'|'disagree'; RQ3/H4), wrong (bool; defined upstream by the grading rules).
Optional columns
  conflict_status  'conflict'|'concordant'|'no_counterpart'|'indistinguishable'. Missing -> 'conflict' iff
                   conflict_family is set. 'indistinguishable' atoms are never used in confirmatory tests (§1.2).
  distinct         atom has a foreign OR superseded value distinguishable from the MoH set (H3 denominator).
                   Missing -> conflict_status == 'conflict'.
  temperature, sample_idx  when present only greedy answers (temperature 0, sample_idx 0) are analysed; the
                   T = 0.7 samples used for the disagreement signal never enter a confirmatory test.
  score, split     RQ3 only: label-free confidence score c(x) and pre-assigned split ('ref'|'cal'|'test').
Clusters: conflict_family for conflict atoms; atoms without a family fall back to their guideline ('gl:<id>').
Rows with a missing label (runtime errors) are dropped and counted.

References checked on 2026-09-26 (Crossref): Durkalski, Palesch, Lipsitz & Rust, Stat Med 2003;22(15):2417-28,
doi:10.1002/sim.1438 (statistic reproduced against the published examples in tests); Efron, JASA 1987;82(397):171-85,
doi:10.1080/01621459.1987.10478410 (BCa); Benjamini & Heller, Biometrics 2008;64(4):1215-22,
doi:10.1111/j.1541-0420.2007.00984.x (partial conjunction); Clopper & Pearson, Biometrika 1934;26(4):404-13,
doi:10.1093/biomet/26.4.404. Learn-then-Test: Angelopoulos et al., arXiv 2110.01052 (see vnsoc.ltt).
"""
from __future__ import annotations

import math
from collections.abc import Callable, Iterable, Mapping, Sequence

import numpy as np
import pandas as pd
from scipy import stats
from scipy.special import expit

from vnsoc import ltt

# ------------------------------------------------------------------ pre-registered constants
# Mirror configs/project.yaml (hypotheses, rq3); tests/test_prereg_code.py fails if they drift apart.
CI_LEVEL = 0.95
ALPHA_ONE_SIDED = (1 - CI_LEVEL) / 2          # 0.025
H3_MARGIN = 0.05
H4_RR_BOUND = 2.0
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
# Analysis constants of this module (not design constants): bootstrap size, bootstrap seed (= the study seed),
# minimum number of clusters for BCa (proposal §5.3: "< 20 clusters -> small-sample t").
N_BOOT = 2000
BOOT_SEED = 20261001
MIN_CLUSTERS_BCA = 20

REQUIRED = ("model", "atom_id", "conflict_family", "guideline", "language", "condition", "format", "label",
            "decoy_match", "foreign_systems", "us_unique", "group_signal", "wrong")
WRONG_LABELS = (3, 4, 5)                      # label -> wrong, used by simulate_study (upstream owns `wrong`)


# ------------------------------------------------------------------ data preparation
def cluster_key(d: pd.DataFrame) -> np.ndarray:
    """Resampling unit: 'fam:<conflict_family>' or, when an atom has no family, 'gl:<guideline>'."""
    fam = d["conflict_family"].astype(object).fillna("").astype(str).to_numpy(dtype=object)
    glk = d["guideline"].astype(object).fillna("").astype(str).to_numpy(dtype=object)
    return np.where(fam != "", "fam:" + fam, "gl:" + glk)


def _as_bool(s: pd.Series) -> pd.Series:
    return s.astype("boolean").fillna(False).astype(bool)


def prepare(df: pd.DataFrame) -> pd.DataFrame:
    """Validate columns, keep greedy graded answers, drop 'indistinguishable' atoms, add `cluster`."""
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
    for c in ("decoy_match", "us_unique", "wrong"):
        d[c] = _as_bool(d[c])
    d["foreign_systems"] = d["foreign_systems"].fillna("").astype(str)
    if "conflict_status" not in d.columns:
        d["conflict_status"] = np.where(d["conflict_family"].notna(), "conflict", "other")
    d = d[d["conflict_status"] != "indistinguishable"].copy()
    d["distinct"] = _as_bool(d["distinct"]) if "distinct" in d.columns else d["conflict_status"].eq("conflict")
    d["cluster"] = cluster_key(d)
    return d


def _subset(d: pd.DataFrame, *, condition: str, language: str | None = None, fmt: str = "short",
            models: Iterable[str] | None = None) -> pd.DataFrame:
    m = (d["condition"] == condition) & (d["format"] == fmt)
    if language is not None:
        m &= d["language"] == language
    if models is not None:
        m &= d["model"].isin(list(models))
    return d[m]


def _cluster_sums(d: pd.DataFrame, cols: Sequence[str]) -> tuple[np.ndarray, np.ndarray]:
    g = d.groupby("cluster", sort=True)[list(cols)].sum()
    return g.index.to_numpy(), g.to_numpy(dtype=float)


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
                     min_clusters: int = MIN_CLUSTERS_BCA, primary: str = "bca") -> dict:
    """CI and one-sided p (H0: theta <= null) for a statistic of per-cluster sums (proposal §5.3).

    M: (C, k) per-cluster sums; stat maps (..., k) totals to (...) values (vectorised).
    C >= min_clusters: cluster bootstrap (whole clusters resampled with replacement) with
      'bca'           textbook BCa (Efron 1987); acceleration from the delete-one-cluster jackknife — the
                      proposal's rule and the default `primary`;
      'bca_expanded'  same resamples, normal quantiles replaced by sqrt(C/(C-1)) * t_{C-1} (small-sample expansion);
      'jackknife_t'   estimate +/- t_{C-1} * cluster-jackknife SE.
    All three are always returned under `variants`; `primary` picks lo / hi / p_one_sided / method.
    C < min_clusters: 'jackknife_t' only, reported as method 't_small' (proposal: "< 20 clusters -> small-sample t").
    """
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
    z0, acc = _z0(boot, est), _acceleration(jack)
    var = {
        "bca": {"lo": _bca_limit(boot, z0, acc, a2), "hi": _bca_limit(boot, z0, acc, 1 - a2),
                "p_one_sided": _bca_pvalue(boot, z0, acc, null)},
        "bca_expanded": {"lo": _bca_limit(boot, z0, acc, a2, C), "hi": _bca_limit(boot, z0, acc, 1 - a2, C),
                         "p_one_sided": _bca_pvalue(boot, z0, acc, null, C)},
        "jackknife_t": jt,
    }
    if primary not in var:
        raise ValueError(f"primary phải thuộc {sorted(var)}")
    return {**out, **var[primary], "method": primary, "n_boot": int(n_boot), "seed": int(seed), "z0": z0,
            "acceleration": acc, "variants": var}


# ------------------------------------------------------------------ H1
def h1_delta(df: pd.DataFrame, n_boot: int = N_BOOT, seed: int = BOOT_SEED, *, models: Iterable[str] | None = None,
             language: str = "vi", condition: str = "A1", level: float = CI_LEVEL,
             min_clusters: int = MIN_CLUSTERS_BCA) -> dict:
    """H1 (primary; proposal §1.4, §5.3). Delta = P(foreign match, label 4) - P(decoy match) on conflict atoms,
    A1 Vietnamese short answers, open models pooled (pass `models`). Also the excess over chance
    (pi_f - pi_d) / (1 - pi_d) = (F - D) / (N - D) with its own interval (same resamples). Confirmed iff ci_lo > 0.
    """
    d = _subset(prepare(df), condition=condition, language=language, models=models)
    d = d[d["conflict_status"] == "conflict"]
    if d.empty:
        raise ValueError("H1: không có câu trả lời nào (A1, vi, short, mẩu xung đột)")
    d = d.assign(n=1.0, f=(d["label"] == 4).astype(float), dm=d["decoy_match"].astype(float))
    _, M = _cluster_sums(d, ["n", "f", "dm"])
    kw = dict(n_boot=n_boot, seed=seed, level=level, min_clusters=min_clusters)
    r = cluster_interval(M, lambda S: (S[..., 1] - S[..., 2]) / S[..., 0], null=0.0, **kw)
    ex = cluster_interval(M, lambda S: (S[..., 1] - S[..., 2]) / (S[..., 0] - S[..., 2]), null=0.0, **kw)
    N, F, D = M.sum(axis=0)
    return {
        "delta": r["estimate"], "ci_lo": r["lo"], "ci_hi": r["hi"], "method": r["method"],
        "p_one_sided": r["p_one_sided"], "confirmed": bool(r["lo"] > 0),
        "n_clusters": r["n_clusters"], "n_responses": int(N), "n_atoms": int(d["atom_id"].nunique()),
        "pi_foreign": F / N, "pi_decoy": D / N, "excess": ex["estimate"], "excess_ci_lo": ex["lo"],
        "excess_ci_hi": ex["hi"], "models": sorted(d["model"].unique().tolist()), "n_boot": r["n_boot"],
        "seed": r["seed"], "level": level, "language": language, "condition": condition,
    }


# ------------------------------------------------------------------ H2
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
                         system: str = "US", first: str = "en", second: str = "vi") -> dict:
    """H2 (proposal §1.4, §5.3). Pairs (atom, model) answered in EN and VI at A1, restricted to us_unique conflict
    atoms (US value differs from every other source); outcome = label 4 with `system` among foreign_systems.
    Durkalski clustered McNemar over conflict families; one-sided p for EN > VI.
    """
    d = _subset(prepare(df), condition=condition, models=models)
    d = d[d["us_unique"] & (d["conflict_status"] == "conflict") & d["language"].isin([first, second])]
    if d.duplicated(["model", "atom_id", "language"]).any():
        raise ValueError("H2: có nhiều hơn một câu trả lời cho cùng (mô hình, mẩu, ngôn ngữ)")
    sys_hit = d["foreign_systems"].str.split(",").apply(lambda xs: system in [x.strip() for x in xs])
    d = d.assign(y=(d["label"] == 4) & sys_hit)
    wide = d.pivot(index=["model", "atom_id"], columns="language", values="y")
    wide = wide.dropna(subset=[first, second]) if {first, second} <= set(wide.columns) else wide.iloc[0:0]
    if wide.empty:
        raise ValueError("H2: không có cặp EN/VI nào")
    clus = d.drop_duplicates(["model", "atom_id"]).set_index(["model", "atom_id"])["cluster"]
    p = pd.DataFrame({"y1": wide[first].astype(bool), "y2": wide[second].astype(bool)})
    p["cluster"] = clus.reindex(p.index).to_numpy()
    p["b"] = p["y1"] & ~p["y2"]
    p["c"] = ~p["y1"] & p["y2"]
    g = p.groupby("cluster")[["b", "c"]].sum().join(p.groupby("cluster").size().rename("n"))
    t = durkalski(g["b"], g["c"], g["n"])
    N, B, Cc = len(p), int(p["b"].sum()), int(p["c"].sum())
    return {
        "p_first": float(p["y1"].mean()), "p_second": float(p["y2"].mean()), "diff": (B - Cc) / N,
        "statistic": t["statistic"], "z": t["z"], "p_one_sided": t["p_one_sided"], "p_two_sided": t["p_two_sided"],
        "no_discordant_pairs": t["no_discordant_pairs"],
        "mcnemar_naive_statistic": ((B - Cc) ** 2 / (B + Cc)) if B + Cc else 0.0,
        "n_pairs": N, "n_discordant_first_only": B, "n_discordant_second_only": Cc, "n_clusters": len(g),
        "direction": f"{first}>{second}", "system": system, "models": sorted(d["model"].unique().tolist()),
    }


# ------------------------------------------------------------------ H3
def cp_design_effect(k_c: Sequence[float], n_c: Sequence[float], *, level: float = CI_LEVEL,
                     null: float | None = None) -> dict:
    """Clopper-Pearson interval for a clustered proportion using a design-effect effective sample size.

    deff = V_cluster / V_srs (V_cluster: cluster-robust linearised variance with C/(C-1) factor), truncated at >= 1
    so the interval is never narrower than exact CP; n_eff = n / deff, then multiplied by
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
        deff = max(1.0, v_clu / (p * (1 - p) / n))
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
                 alpha: float = ALPHA_ONE_SIDED) -> dict:
    """H3 (proposal §1.4, §4.4). Per open model: rate of labels 3|4 at A3 on atoms with a distinct foreign or
    superseded value, clustered CP interval (cp_design_effect) and one-sided p for H0: rate <= margin.
    'At least half of the open models' is tested by the partial-conjunction p with u = ceil(M/2).
    Choice of interval: rates near the 5% margin are where percentile bootstraps under-cover with 25-40 clusters;
    CP on the effective sample size stays exact without clustering and only widens with it (deff >= 1).
    """
    d = _subset(prepare(df), condition=condition, language=language, models=models)
    d = d[d["distinct"]]
    if d.empty:
        raise ValueError("H3: không có câu trả lời nào (A3, mẩu có giá trị khác biệt)")
    d = d.assign(n=1.0, y=d["label"].isin([3, 4]).astype(float))
    per = {}
    for m, dm in d.groupby("model", sort=True):
        _, M = _cluster_sums(dm, ["y", "n"])
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
            "condition": condition, "method": "clopper_pearson_design_effect_t_df"}


# ------------------------------------------------------------------ H4
def h4_risk_ratio(df: pd.DataFrame, bound: float = H4_RR_BOUND, n_boot: int = N_BOOT, seed: int = BOOT_SEED, *,
                  models: Iterable[str] | None = None, condition: str = "A2", language: str | None = None,
                  level: float = CI_LEVEL, min_clusters: int = MIN_CLUSTERS_BCA) -> dict:
    """H4 (proposal §1.4, §4.6). Served A2 answers (greedy, same language as the question; both languages by
    default), open models pooled: RR = P(wrong | disagree) / P(wrong | agree) at full coverage. Cluster-bootstrap
    BCa CI on log RR (small-sample t below 20 clusters); one-sided p for H0: RR <= bound. Confirmed (before Holm)
    iff ci_lo > bound.
    """
    d = _subset(prepare(df), condition=condition, language=language, models=models)
    bad = set(d["group_signal"].dropna().unique()) - set(RQ3_GROUPS)
    if bad or d["group_signal"].isna().any():
        raise ValueError(f"H4: group_signal phải là {RQ3_GROUPS}; gặp {sorted(map(str, bad))} hoặc trống")
    dis = d["group_signal"].eq("disagree").astype(float)
    wr = d["wrong"].astype(float)
    d = d.assign(nd=dis, wd=dis * wr, na=1 - dis, wa=(1 - dis) * wr)
    _, M = _cluster_sums(d, ["nd", "wd", "na", "wa"])
    r = cluster_interval(M, lambda S: np.log(S[..., 1] / S[..., 0]) - np.log(S[..., 3] / S[..., 2]),
                         null=math.log(bound), n_boot=n_boot, seed=seed, level=level, min_clusters=min_clusters)
    nd, wd, na, wa = M.sum(axis=0)
    ex = lambda x: float(np.exp(x)) if np.isfinite(x) else (float("inf") if x > 0 else 0.0)  # noqa: E731
    return {
        "rr": ex(r["estimate"]), "ci_lo": ex(r["lo"]), "ci_hi": ex(r["hi"]), "log_rr": r["estimate"],
        "method": r["method"], "p_one_sided": r["p_one_sided"], "bound": bound,
        "confirmed_unadjusted": bool(ex(r["lo"]) > bound), "risk_disagree": wd / nd if nd else float("nan"),
        "risk_agree": wa / na if na else float("nan"), "n_disagree": int(nd), "n_agree": int(na),
        "n_clusters": r["n_clusters"], "n_responses": int(nd + na), "models": sorted(d["model"].unique().tolist()),
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


# ------------------------------------------------------------------ RQ3
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


def served(df: pd.DataFrame, *, models: Iterable[str] | None = None, condition: str = "A2",
           score_col: str = "score") -> pd.DataFrame:
    """Served answers for RQ3: greedy A2 short answers with a score and a signal group."""
    d = _subset(prepare(df), condition=condition, models=models)
    if score_col not in d.columns:
        raise ValueError(f"RQ3: thiếu cột điểm tin cậy '{score_col}'")
    d = d[d[score_col].notna()]
    bad = set(d["group_signal"].unique()) - set(RQ3_GROUPS)
    if bad:
        raise ValueError(f"RQ3: nhóm lạ {bad}")
    return d


def _alpha_by_group(n_cal_atoms: Mapping[str, int], alpha: float, alpha_fallback: float,
                    min_cal_atoms: int) -> dict:
    """DR4 (label-free): alpha_fallback for a group with fewer than min_cal_atoms calibration atoms."""
    return {g: (alpha_fallback if n < min_cal_atoms else alpha) for g, n in n_cal_atoms.items()}


def certified_rq3(df: pd.DataFrame, *, score_col: str = "score", split_col: str = "split",
                  models: Iterable[str] | None = None, condition: str = "A2",
                  coverages: Sequence[float] = RQ3_COVERAGES, delta: float = RQ3_DELTA, alpha: float = RQ3_ALPHA,
                  alpha_fallback: float = RQ3_ALPHA_FALLBACK, min_cal_atoms: int = RQ3_MIN_CAL_ATOMS,
                  min_useful_coverage: float = RQ3_MIN_USEFUL_COVERAGE,
                  fractions: Sequence[tuple[str, float]] = RQ3_SPLIT_FRACTIONS, seed: int = SPLIT_SEED,
                  groups: Sequence[str] = RQ3_GROUPS) -> dict:
    """RQ3 regime (a) (proposal §4.7, §5.4; skill certified-abstention).

    Primary: simultaneous CP upper bounds U_gk (confidence 1 - delta/(G*K), G = 2 groups, K = 4 coverages) with
    thresholds from the reference split. Secondary: Learn-then-Test per group at alpha (alpha_fallback when the
    group has < min_cal_atoms calibration atoms, DR4), Bonferroni over the G pre-registered groups (delta / G).
    DR5: certified test coverage < min_useful_coverage in the disagreement group -> 'not useful' (still reported).
    Violations are judged against the POOL risk (calibration U test), never the test half alone.
    Uses the `split` column when every row carries ref/cal/test; otherwise assign_rq3_split(seed).
    """
    d = served(df, models=models, condition=condition, score_col=score_col)
    if split_col in d.columns and d[split_col].isin(["ref", "cal", "test"]).all():
        sp = d[split_col].to_numpy(dtype=object)
        split_source = "column"
    else:
        sp = assign_rq3_split(d["atom_id"].to_numpy(), fractions, seed)
        split_source = f"assign_rq3_split(seed={seed})"
    s = d[score_col].to_numpy(dtype=float)
    e = d["wrong"].to_numpy(dtype=int)
    g = d["group_signal"].to_numpy(dtype=object)
    atoms = d["atom_id"].to_numpy(dtype=object)
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
        at = mt & (s >= lam)
        ap = mp & (s >= lam)
        lt[grp] = {"alpha_used": alpha_g[grp], "n_cal_atoms": n_cal_atoms[grp], "threshold": float(lam),
                   "certified": bool(np.isfinite(lam)),
                   "coverage_cal": float((s[mc] >= lam).mean()) if mc.any() else float("nan"),
                   "coverage_test": float((s[mt] >= lam).mean()) if mt.any() else float("nan"),
                   "risk_test": float(e[at].mean()) if at.any() else float("nan"),
                   "risk_pool": float(e[ap].mean()) if ap.any() else float("nan"),
                   "violation_pool": bool(ap.any() and e[ap].mean() > alpha_g[grp])}
    cov_dis = lt["disagree"]["coverage_test"] if "disagree" in lt else float("nan")
    baseline = {str(grp): float(e[test & (g == grp)].mean()) if np.any(test & (g == grp)) else float("nan")
                for grp in groups}
    return {
        "bounds": rows, "ltt": lt, "G": G, "K": len(coverages), "delta": delta,
        "bound_confidence_each": 1 - delta / (G * len(coverages)),
        "dr4_alpha_by_group": alpha_g, "dr5_useful_disagree": bool(np.isfinite(cov_dis) and
                                                                   cov_dis >= min_useful_coverage),
        "min_useful_coverage": min_useful_coverage, "baseline_full_coverage_risk_test": baseline,
        "abstain_all_disagree": {"coverage_test": float(np.mean(g[test] == "agree")) if test.any() else float("nan"),
                                 "risk_test": baseline.get("agree", float("nan"))},
        "any_bound_violation_pool": any(r["violation_pool"] for r in rows),
        "n_rows": {"ref": int(ref.sum()), "cal": int(cal.sum()), "test": int(test.sum())},
        "split_source": split_source,
    }


def rq3_regime_b(df: pd.DataFrame, *, n_splits: int = RQ3_REGIME_B_SPLITS, seed: int = SPLIT_SEED,
                 score_col: str = "score", models: Iterable[str] | None = None, condition: str = "A2",
                 coverages: Sequence[float] = RQ3_COVERAGES, delta: float = RQ3_DELTA, alpha: float = RQ3_ALPHA,
                 alpha_fallback: float = RQ3_ALPHA_FALLBACK, min_cal_atoms: int = RQ3_MIN_CAL_ATOMS,
                 fractions: Sequence[tuple[str, float]] = RQ3_SPLIT_FRACTIONS,
                 max_violation: float = RQ3_REGIME_B_MAX_VIOLATION, groups: Sequence[str] = RQ3_GROUPS) -> dict:
    """RQ3 regime (b): split by GUIDELINE (unseen guidelines), n_splits random splits with the same fractions.
    No theoretical guarantee; reports the empirical violation frequency (test-guideline risk above U_gk, or above
    alpha at the LTT threshold) against the pre-registered acceptance level 2*delta (proposal §4.7)."""
    d = served(df, models=models, condition=condition, score_col=score_col)
    s = d[score_col].to_numpy(dtype=float)
    e = d["wrong"].to_numpy(dtype=int)
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
    return {"n_splits": n_splits, "n_used": done, "bound_violation_rate": rb, "ltt_violation_rate": rl,
            "max_violation": max_violation, "bound_acceptable": bool(rb <= max_violation),
            "ltt_acceptable": bool(rl <= max_violation), "n_guidelines": len(ug), "seed": seed}


# ------------------------------------------------------------------ simulation
DEFAULT_EFFECT = {
    "pi_foreign": 0.30,        # H1: P(label 4) at A1-VI on conflict atoms (proposal pilot scale: 30% vs 5%)
    "pi_decoy": 0.05,          # H1: P(decoy match)
    "kappa_family": 8.0,       # Beta concentration of cluster-level rates (ICC ~ 1/(1 + kappa))
    "kappa_atom": 10.0,        # Beta concentration of atom-level rates around the cluster rate
    "kappa_direction": 6.0,    # cluster heterogeneity of P(foreign | a source value is matched)
    "model_spread": 0.3,       # model multipliers evenly spaced in [1 - spread, 1 + spread] (mean 1)
    "a0_mult": 1.3,            # A0 source-match multiplier (descriptive only)
    "h2_en_mult": 1.5,         # H2: EN multiplier of the source-match rate on us_unique atoms (1 = null)
    "a3_rate": 0.10,           # H3: P(label 3|4 | A3, distinct atom); scalar or one value per model
    "h4_base": 0.08,           # H4: P(wrong | agree) at A2
    "h4_rr": 3.0,              # H4: P(wrong | disagree) / P(wrong | agree)
    "kappa_h4": 20.0,          # concentration for the A2 wrong-risk (kept high so rr * risk rarely clips at 1)
    "p_disagree": 0.25,        # share of the disagreement group
    "frac_us_unique": 0.4,     # share of conflict atoms whose US value differs from every other source
    "frac_superseded": 0.3,    # share of atoms with a distinct superseded MoH value
    "concordant_per_family": 5,
    "n_guidelines": 30,
}
# Global null: H1 pi_f = pi_d, H2 no language effect, H3 every model exactly at the margin, H4 RR at the bound.
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

    Cluster- and atom-level rates are Beta draws with EXACT marginal means, so the nulls in NULL_EFFECT hold exactly
    in the superpopulation: H1 foreign and decoy matches share one source-match event split by a cluster-level
    direction with mean pi_f / (pi_f + pi_d); H2 multiplies the EN source-match rate on us_unique atoms; H3 uses
    comonotone per-model cluster rates with mean a3_rate[m]; H4 draws the signal group independently of the
    cluster/atom wrong-risk, so P(wrong | disagree) / P(wrong | agree) = h4_rr. Scores for RQ3 depend on `wrong`
    (simulation only; real scores are label-free). `effect` overrides DEFAULT_EFFECT.
    """
    e = {**DEFAULT_EFFECT, **(effect or {})}
    rng = np.random.default_rng(seed)
    F, apf, cpf, M = int(n_families), int(atoms_per_family), int(e["concordant_per_family"]), int(models)
    nG = max(1, min(int(e["n_guidelines"]), F))
    fam_gl = np.arange(F) % nG
    n_conf, n_conc = F * apf, F * cpf
    A = n_conf + n_conc
    is_conf = np.r_[np.ones(n_conf, bool), np.zeros(n_conc, bool)]
    fam = np.r_[np.repeat(np.arange(F), apf), np.full(n_conc, -1)]
    gl = np.r_[fam_gl[np.repeat(np.arange(F), apf)], fam_gl[np.repeat(np.arange(F), cpf)]]
    cl = np.where(is_conf, fam, F + gl)                     # simulation cluster: family, or guideline
    CL = F + nG
    has_sup = rng.random(A) < e["frac_superseded"]
    us_unique = is_conf & (rng.random(A) < e["frac_us_unique"])
    distinct = is_conf | has_sup
    fsys = np.where(us_unique, "US", np.asarray(_FOREIGN_SETS, dtype=object)[rng.integers(len(_FOREIGN_SETS), size=A)])
    fsys = np.where(is_conf, fsys, "")
    rho = np.linspace(1 - e["model_spread"], 1 + e["model_spread"], M) if M > 1 else np.ones(1)

    # latent rates ----------------------------------------------------------------------------------------------
    pi_s = e["pi_foreign"] + e["pi_decoy"]
    q = e["pi_foreign"] / pi_s if pi_s > 0 else 0.5
    ps_cl = np.where(np.arange(CL) < F, _beta_mean(rng, pi_s, e["kappa_family"], CL),
                     _beta_mean(rng, e["pi_decoy"], e["kappa_family"], CL))
    ps_atom = _beta_mean(rng, ps_cl[cl], e["kappa_atom"])
    q_cl = _beta_mean(rng, q, e["kappa_direction"], CL)
    r3 = np.broadcast_to(np.asarray(e["a3_rate"], dtype=float), (M,))
    u3 = rng.random(CL)
    p3_cl = np.stack([stats.beta.ppf(u3, max(r, 1e-6) * e["kappa_family"], max(1 - r, 1e-6) * e["kappa_family"])
                      for r in r3], axis=1)                  # (CL, M), comonotone across models
    pd_cl = _beta_mean(rng, e["p_disagree"], e["kappa_family"], CL)
    b_cl = _beta_mean(rng, e["h4_base"], e["kappa_h4"], CL)
    b_atom = _beta_mean(rng, b_cl[cl], e["kappa_h4"])

    # units = (atom, model, language) --------------------------------------------------------------------------
    ua = np.repeat(np.arange(A), M * 2)
    um = np.tile(np.repeat(np.arange(M), 2), A)
    en = np.tile(np.array([False, True]), A * M)
    U = len(ua)
    conf_u, sup_u = is_conf[ua], has_sup[ua]
    disagree = rng.random(U) < pd_cl[cl[ua]]

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
        score = np.full(U, np.nan)
        if cond in ("A0", "A1"):
            mult = e["a0_mult"] if cond == "A0" else 1.0
            p = ps_atom[ua] * rho[um] * mult * np.where(en & us_unique[ua], e["h2_en_mult"], 1.0)
            S = rng.random(U) < np.clip(p, 0, 1)
            Fm = S & conf_u & (rng.random(U) < q_cl[cl[ua]])
            label[Fm] = 4
            dm = S & ~Fm
            label[dm], decoy[dm] = 5, True
            rest = ~S
            label[rest] = background(rest, bg_short)
        elif cond == "A3":
            p3 = _beta_mean(rng, p3_cl[cl[ua], um], e["kappa_atom"])
            y = distinct[ua] & (rng.random(U) < p3)
            stale = sup_u & (~conf_u | (rng.random(U) < 0.3))
            label[y] = np.where(stale[y], 3, 4)
            rest = ~y
            label[rest] = background(rest, {"c": (0.05, 0.85, 0.0, 0.05, 0.05), "n": (0.05, 0.85, 0.0, 0.05, 0.05)})
        else:  # A2 served
            risk = b_atom[ua] * rho[um] * np.where(disagree, e["h4_rr"], 1.0)
            w = rng.random(U) < np.clip(risk, 0, 1)
            kind = rng.random(U)
            label[w] = np.where(conf_u[w] & (kind[w] < 0.6), 4, np.where(sup_u[w] & (kind[w] < 0.8), 3, 5))
            label[~w] = np.where(rng.random(int((~w).sum())) < 0.9, 2, 1)
            score = expit(0.8 - 1.6 * w - 0.4 * disagree + rng.normal(size=U))
        blocks.append(pd.DataFrame({
            "model": np.array([f"sim_m{i + 1}" for i in range(M)], dtype=object)[um],
            "atom_id": np.char.add("a", np.char.zfill(ua.astype(str), 5)),
            "conflict_family": np.where(is_conf[ua], np.char.add("fam", np.char.zfill(np.maximum(fam[ua], 0)
                                                                                     .astype(str), 3)), None),
            "guideline": np.char.add(np.char.add("gl", np.char.zfill(gl[ua].astype(str), 2)), "/2026"),
            "language": np.where(en, "en", "vi"), "condition": cond, "format": "short", "label": label,
            "decoy_match": decoy, "foreign_systems": np.where(label == 4, fsys[ua], ""),
            "us_unique": us_unique[ua], "group_signal": np.where(disagree, "disagree", "agree"),
            "wrong": np.isin(label, WRONG_LABELS), "conflict_status": np.where(conf_u, "conflict", "concordant"),
            "distinct": distinct[ua], "score": score, "sample_idx": 0, "temperature": 0.0,
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


def run_all(df: pd.DataFrame, *, models: Iterable[str] | None = None, n_boot: int = N_BOOT, seed: int = BOOT_SEED,
            rq3: bool = True, regime_b_splits: int = RQ3_REGIME_B_SPLITS) -> dict:
    """Every pre-registered confirmatory result (H1, per-model H1, H2, H3, H4, Holm over H2-H4, DR3, RQ3 (a) and
    (b)) as one JSON-safe dict, for later registry writes (vnsoc.numbers.put in T6.x)."""
    ms = resolve_models(df, models)
    n_missing = int(df["label"].isna().sum())
    out = {"meta": {"models": ms, "n_rows": len(df), "n_rows_missing_label": n_missing, "n_boot": n_boot,
                    "seed": seed, "alpha_one_sided": ALPHA_ONE_SIDED, "ci_level": CI_LEVEL}}
    out["h1"] = h1_delta(df, n_boot, seed, models=ms)
    out["h1_per_model"] = {m: h1_delta(df, n_boot, seed, models=[m]) for m in ms}
    out["h2"] = h2_mcnemar_clustered(df, models=ms)
    out["h3"] = h3_per_model(df, models=ms)
    out["h4"] = h4_risk_ratio(df, n_boot=n_boot, seed=seed, models=ms)
    out["holm"] = holm({"H2": out["h2"]["p_one_sided"], "H3": out["h3"]["p_pc"], "H4": out["h4"]["p_one_sided"]})
    out["dr3"] = dr3_check(df, models=ms)
    if rq3 and "score" in df.columns:
        out["rq3"] = certified_rq3(df, models=ms)
        out["rq3_regime_b"] = rq3_regime_b(df, models=ms, n_splits=regime_b_splits) if regime_b_splits else None
    return _py(out)
