"""Tests for the pre-registered confirmatory code (T2.10): src/vnsoc/analysis/confirmatory.py. Fast (< 90 s).
Revised 2026-09-26 after the preregistration review (review/prereg/response.md): every point of rev-methods id 2
(a)-(h) and rev-editor id 1 has a test here."""
import itertools
import json
import math
import re
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import yaml
from scipy import stats
from statsmodels.stats.multitest import multipletests

from vnsoc.analysis import confirmatory as cf
from vnsoc.analysis.pilot import cp

ROOT = Path(__file__).resolve().parents[1]


def _rows(specs):
    """specs: list of dicts overriding a default graded row (a conflict atom with one foreign target and a decoy)."""
    base = dict(model="m1", atom_id="a0", conflict_family="f0", guideline="g0", language="vi", condition="A1",
                format="short", label=2, decoy_match=False, foreign_systems="", conflict_status="conflict",
                us_unique=False, k_foreign=1, has_decoy=True, group_signal="agree")
    return pd.DataFrame([{**base, **s} for s in specs])


# ------------------------------------------------------------------ pre-registered constants
def test_constants_match_configs():
    cfg = yaml.safe_load((ROOT / "configs" / "project.yaml").read_text(encoding="utf-8"))
    h, r = cfg["hypotheses"], cfg["rq3"]
    assert h["primary"] == "H1" and h["secondary_family"] == ["H2", "H3", "H4"]
    assert cf.CI_LEVEL == h["ci_level"] and cf.H3_MARGIN == h["H3_margin"] and cf.H4_RR_BOUND == h["H4_rr_lower_bound"]
    assert cf.H1_SESOI_EXCESS == h["H1_sesoi_excess"]
    assert math.isclose(cf.ALPHA_ONE_SIDED, (1 - h["ci_level"]) / 2)
    assert list(cf.RQ3_GROUPS) == r["groups"] and list(cf.RQ3_COVERAGES) == r["coverages"]
    assert (cf.RQ3_ALPHA, cf.RQ3_DELTA, cf.RQ3_ALPHA_FALLBACK) == (r["alpha"], r["delta"], r["alpha_fallback"])
    assert cf.RQ3_MIN_CAL_ATOMS == r["alpha_fallback_min_cal_atoms"]
    assert cf.RQ3_MIN_USEFUL_COVERAGE == r["min_useful_coverage"]
    assert cf.RQ3_REGIME_B_SPLITS == r["regime_b_splits"]
    assert cf.RQ3_REGIME_B_MAX_VIOLATION == r["regime_b_max_violation_rate"] == 2 * r["delta"]
    assert dict(cf.RQ3_SPLIT_FRACTIONS) == r["split_fractions"] and cf.SPLIT_SEED == r["split_seed"]


def test_registered_analysis_constants():
    # rev-methods id 2(b): B = 10,000 as registered (prereg §5.1.1); decision rule and switches as registered
    assert cf.N_BOOT == 10_000 and cf.BOOT_SEED == 20261001 and cf.MIN_CLUSTERS_BCA == 20
    assert cf.PRIMARY_RULE == "conservative" and cf.SIGNFLIP_MIN_FAMILIES == 20
    assert cf.H4_STRATA == ("model", "language") and cf.RQ3_RERANDOMISATIONS == 500
    assert cf.RQ3_FEATURES == ("s1", "s2", "s3", "consistency", "logprob") and cf.RQ3_LOGIT_C == 1.0
    assert cf.MISSING_BOUND_TRIGGER == 0.02


def test_registration_function_table_matches_module():
    # rev-editor id 1: the §5.0 table maps every decision to a function that exists in the analysed module
    txt = (ROOT / "prereg" / "osf_preregistration.md").read_text(encoding="utf-8")
    names = set(re.findall(r"`confirmatory\.([a-z_0-9]+)", txt))
    assert {"h1_delta", "h1_robustness", "h2_mcnemar_clustered", "h3_per_model", "h4_risk_ratio", "holm",
            "certified_rq3", "rq3_regime_b", "rq3_rerandomise", "missing_bounds", "tipping_point_h1",
            "wild_cluster_p", "run_all"} <= names
    missing = sorted(n for n in names if not hasattr(cf, n))
    assert not missing, f"prereg names functions that do not exist: {missing}"
    assert "N_BOOT = 2000" not in txt and "10,000" in txt


# ------------------------------------------------------------------ simulate_study
def test_simulate_study_structure():
    F, apf, M = 12, 5, 3
    df = cf.simulate_study(7, n_families=F, atoms_per_family=apf, models=M, effect={"frac_no_decoy": 0.0})
    cpf = cf.DEFAULT_EFFECT["concordant_per_family"]
    assert set(cf.REQUIRED) <= set(df.columns) and "wrong" not in df.columns
    assert len(df) == F * (apf + cpf) * M * 2 * 4
    assert set(df["condition"]) == {"A0", "A1", "A2", "A3"} and set(df["language"]) == {"vi", "en"}
    cells = df.groupby(["atom_id", "model", "language"])["condition"].agg(lambda s: tuple(sorted(s)))
    assert (cells == ("A0", "A1", "A2", "A3")).all()
    assert df.groupby(["atom_id", "model", "language"])["group_signal"].nunique().eq(1).all()
    assert df.loc[df["decoy_match"], "label"].eq(5).all()
    assert ((df["foreign_systems"] != "") == (df["label"] == 4)).all()
    conf = df["conflict_status"] == "conflict"
    assert df.loc[conf, "conflict_family"].notna().all() and df.loc[~conf, "conflict_family"].isna().all()
    assert df.loc[conf, "k_foreign"].isin([1, 2]).all() and df.loc[~conf, "k_foreign"].eq(0).all()
    assert not df.loc[df["us_unique"], "conflict_status"].ne("conflict").any()
    assert df.loc[df["us_unique"] & (df["label"] == 4), "foreign_systems"].eq("US").all()
    a2 = df[df["condition"] == "A2"]
    fired = a2[["s1", "s2", "s3"]].sum(axis=1) > 0
    assert (fired == a2["group_signal"].eq("disagree")).all()                 # disagreement = any signal fired
    assert a2["label"].eq(6).any() and df.loc[df["condition"] != "A2", "s1"].isna().all()
    assert df.loc[conf, "conflict_family"].nunique() == F
    pd.testing.assert_frame_equal(df, cf.simulate_study(7, n_families=F, atoms_per_family=apf, models=M,
                                                        effect={"frac_no_decoy": 0.0}))
    assert not df["label"].equals(cf.simulate_study(8, n_families=F, atoms_per_family=apf, models=M)["label"])
    uneq = cf.simulate_study(9, n_families=25, atoms_per_family=16, effect={"family_size_sigma": 1.0})
    sizes = uneq[uneq["conflict_status"] == "conflict"].groupby("conflict_family")["atom_id"].nunique()
    assert sizes.max() > 3 * sizes.min()                                      # unequal clusters


# ------------------------------------------------------------------ H1
def test_h1_hand_example_small_cluster_t():
    fam = {"A": [4, 4, 5, 2], "B": [4, 2, 2, 2], "C": [5, 2, 2, 6]}
    decoy = {"A": [False, False, True, False], "B": [False] * 4, "C": [True, False, False, False]}
    df = _rows([dict(atom_id=f"{f}{i}", conflict_family=f, label=lab, decoy_match=decoy[f][i])
                for f, labs in fam.items() for i, lab in enumerate(labs)])
    r = cf.h1_delta(df, n_boot=200)
    assert r["method"] == "t_small" and r["n_clusters"] == 3 and r["n_responses"] == 12
    assert math.isclose(r["delta"], 1 / 12) and math.isclose(r["pi_foreign"], 3 / 12)
    assert math.isclose(r["pi_decoy"], 2 / 12) and math.isclose(r["excess"], 1 / 10)
    se = 1 / 6          # jackknife: leave-out estimates 0, 0, 1/4 -> var = (2/3) * (1/24)
    assert math.isclose(r["ci_lo"], 1 / 12 - stats.t.ppf(0.975, 2) * se)
    assert math.isclose(r["ci_hi"], 1 / 12 + stats.t.ppf(0.975, 2) * se)
    assert math.isclose(r["variants"]["jackknife_t"]["p_one_sided"], stats.t.sf((1 / 12) / se, 2))
    assert r["wild_cluster"]["exact"] and r["wild_cluster"]["n_draws"] == 8 and not r["confirmed"]
    assert math.isclose(r["p_one_sided"], max(stats.t.sf((1 / 12) / se, 2), r["wild_cluster"]["p_one_sided"]))


def test_h1_decoy_weighted_by_k():
    # rev-methods id 2(a): pi_d = mean(k_i * D). Atom b has k = 2 targets and a decoy hit -> counts twice.
    df = _rows([dict(atom_id="a", label=4), dict(atom_id="b", label=5, decoy_match=True, k_foreign=2),
                dict(atom_id="c", label=2), dict(atom_id="d", label=2)])
    r = cf.h1_delta(df, n_boot=100)
    assert math.isclose(r["pi_decoy"], 2 / 4) and math.isclose(r["pi_decoy_unscaled"], 1 / 4)
    assert math.isclose(r["delta"], 1 / 4 - 2 / 4) and r["decoy_weight"] == "k"
    u = cf.h1_delta(df, n_boot=100, decoy_weight="unscaled")                  # sensitivity B.7a
    assert math.isclose(u["delta"], 0.0) and u["decoy_weight"] == "unscaled"
    with pytest.raises(ValueError):                                         # a conflict atom needs k_i >= 1
        cf.prepare(df.assign(k_foreign=0))


def test_h1_excludes_conflict_atoms_without_decoy():
    # rev-methods id 5 / rev-editor id 4(b): decoy-less conflict atoms (D = 0 by construction) never enter H1
    df = _rows([dict(atom_id="a", label=4), dict(atom_id="b", label=2),
                dict(atom_id="x", label=4, has_decoy=False), dict(atom_id="y", label=4, has_decoy=False)])
    r = cf.h1_delta(df, n_boot=100)
    assert r["n_atoms"] == 2 and r["n_conflict_atoms_without_decoy_excluded"] == 2
    assert math.isclose(r["pi_foreign"], 0.5)
    sim = cf.simulate_study(3, effect={**cf.NULL_EFFECT, "frac_no_decoy": 0.3})
    assert cf.h1_delta(sim, n_boot=200)["n_conflict_atoms_without_decoy_excluded"] > 0


def test_h1_detects_large_effect():
    df = cf.simulate_study(11, effect={"frac_no_decoy": 0.0})                  # 30% foreign vs 5% decoy, 40 families
    r = cf.h1_delta(df, n_boot=500, seed=1)
    assert r["method"] == "conservative" and r["n_clusters"] == 40 and r["n_responses"] == 400 * 4
    assert r["confirmed"] and r["ci_lo"] > 0.1 and r["p_one_sided"] < 0.005
    assert r["ci_lo"] < r["delta"] < r["ci_hi"] and r["excess_ci_lo"] < r["excess"] < r["excess_ci_hi"]
    assert set(r["variants"]) == {"bca", "bca_expanded", "jackknife_t"} and r["confirmed_all_variants"]
    assert r["variants"]["bca_expanded"]["lo"] <= r["variants"]["bca"]["lo"]      # expansion only widens
    assert r["ci_lo"] == min(v["lo"] for v in r["variants"].values())
    assert r["excess_lo_at_least_sesoi"] == (r["excess_ci_lo"] >= 0.10)
    one = cf.h1_delta(df, n_boot=300, seed=1, models=["sim_m1"])
    assert one["models"] == ["sim_m1"] and one["n_responses"] == 400
    g = cf.h1_delta(df, n_boot=300, seed=1, cluster_by="guideline")          # sensitivity B.10
    assert g["n_clusters"] == 30 and g["cluster_by"] == "guideline"


def test_h1_null_ci_mostly_contains_zero():
    hits, reps = 0, 30
    for i in range(reps):
        df = cf.simulate_study(1000 + i, effect=cf.NULL_EFFECT)
        r = cf.h1_delta(df, n_boot=300, seed=i)
        hits += r["ci_lo"] <= 0 <= r["ci_hi"]
    assert hits >= 0.8 * reps


def test_conservative_rule_is_intersection_union_of_variants():
    df = cf.simulate_study(12, effect={"pi_foreign": 0.08})
    b = cf.h1_delta(df, n_boot=400, seed=4, primary="bca")
    c = cf.h1_delta(df, n_boot=400, seed=4)
    v = c["variants"]
    assert c["method"] == "conservative" and b["variants"] == v
    assert c["ci_lo"] == min(x["lo"] for x in v.values()) and c["ci_hi"] == max(x["hi"] for x in v.values())
    assert c["p_one_sided"] == max([x["p_one_sided"] for x in v.values()] + [c["wild_cluster"]["p_one_sided"]])
    assert c["confirmed"] == c["confirmed_all_variants"] and c["ci_lo"] <= b["ci_lo"]
    h = cf.h4_risk_ratio(df, n_boot=400, seed=4)
    assert h["method"] == "conservative" and h["p_one_sided"] == max(x["p_one_sided"] for x in h["variants"].values())
    with pytest.raises(ValueError):
        cf.h1_delta(df, primary="percentile")


def test_wild_cluster_p_exact_and_monte_carlo():
    z, n = np.array([3.0, -1.0, 2.0]), np.array([10.0, 10.0, 10.0])
    r = cf.wild_cluster_p(z, n, n_boot=100)
    assert r["exact"] and r["n_draws"] == 8
    th = z.sum() / n.sum()
    t = []
    for e in itertools.product([1.0, -1.0], repeat=3):
        zs = np.array(e) * z
        ths = zs.sum() / n.sum()
        t.append(ths / (math.sqrt(1.5 * np.sum((zs - ths * n) ** 2)) / n.sum()))
    t_obs = th / (math.sqrt(1.5 * np.sum((z - th * n) ** 2)) / n.sum())
    assert math.isclose(r["t"], t_obs) and math.isclose(r["p_one_sided"], np.mean(np.array(t) >= t_obs - 1e-12))
    big = cf.wild_cluster_p(np.r_[np.ones(30), -np.ones(30)], np.full(60, 5.0), n_boot=2000, seed=1)
    assert not big["exact"] and 0.3 < big["p_one_sided"] < 0.7                  # symmetric: p near 1/2
    strong = cf.wild_cluster_p(np.full(25, 2.0) + np.linspace(0, 1, 25), np.full(25, 10.0), n_boot=2000)
    assert strong["p_one_sided"] < 0.001


def test_h1_under_20_clusters_uses_small_sample_t():
    r = cf.h1_delta(cf.simulate_study(3, n_families=10), n_boot=200)
    assert r["method"] == "t_small" and r["n_clusters"] == 10 and set(r["variants"]) == {"jackknife_t"}
    assert not r["wild_cluster"]["exact"] or r["wild_cluster"]["n_draws"] <= 200


def test_bca_matches_scipy_on_iid_mean():
    x = np.random.default_rng(5).exponential(size=200)          # skewed: z0 and acceleration both matter
    M = np.c_[np.ones_like(x), x]                                  # clusters of size 1 -> ratio = mean
    r = cf.cluster_interval(M, lambda S: S[..., 1] / S[..., 0], n_boot=4000, seed=2, primary="bca")
    ref = stats.bootstrap((x,), np.mean, method="BCa", n_resamples=4000, random_state=3).confidence_interval
    assert r["method"] == "bca"
    assert abs(r["lo"] - ref.low) < 0.02 and abs(r["hi"] - ref.high) < 0.02


def test_h1_robustness_set():
    df = cf.simulate_study(13)
    r = cf.h1_robustness(df, n_boot=300)
    assert {"S1", "S2", "S3", "N1", "h1_robust"} <= set(r)
    assert all(r[k]["computed"] for k in ("S1", "S2", "S3", "N1")) and r["h1_robust"]
    assert 0.5 < r["S1"]["rho"] < 2.0                                          # symmetric noise in the simulation
    part = cf.h1_robustness(df.drop(columns=["side"]), n_boot=200)
    assert not part["S1"]["computed"] and not part["h1_robust"]               # S1 required for 'robust'


def test_h1_directional_correction_by_hand():
    # 4 unattributed numeric answers on the foreign side, 1 on the decoy side -> rho = 4.5 / 1.5 = 3
    specs = [dict(atom_id="a", label=4), dict(atom_id="b", label=5, decoy_match=True)]
    specs += [dict(atom_id=f"u{i}", label=5, side="foreign") for i in range(4)] + [dict(atom_id="v", label=5,
                                                                                         side="decoy")]
    df = _rows(specs).assign(value_kind="num")
    df["side"] = df["side"].fillna("")
    r = cf.h1_directional(df, n_boot=100)
    assert math.isclose(r["rho"], 3.0) and math.isclose(r["delta_dir"], (1 - 3.0 * 1) / 7)


# ------------------------------------------------------------------ H2 (Durkalski + exact sign-flip)
PSYCH_B = [0, 1, 1, 1, 0, 3, 3, 3, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 3, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0]
PSYCH_C = [4, 2, 3, 2, 1, 3, 0, 2, 2, 4, 2, 4, 3, 2, 1, 3, 1, 2, 0, 0, 0, 2, 1, 2, 2, 0, 0, 1, 1]
PSYCH_N = [7, 6, 7, 6, 4, 6, 5, 8, 4, 7, 3, 6, 7, 6, 5, 4, 6, 5, 4, 3, 5, 4, 4, 2, 3, 2, 2, 3, 1]


def test_durkalski_reproduces_published_examples():
    # Psychiatry data (29 psychiatrists, 135 pairs) and Obuchowski's thyroid data, as shipped in the CRAN package
    # clust.bin.pair 0.1.2, whose test-suite attributes X2 = 7.542 and 2.32 (McNemar 4.5) to Durkalski et al. 2003.
    assert round(cf.durkalski(PSYCH_B, PSYCH_C, PSYCH_N)["statistic"], 3) == 7.542
    pet = [[0, 0, 0], [1, 1, 0], [1, 1, 1], [1], [1, 1, 0], [1, 1, 1, 1], [1, 1, 1], [1, 1], [1, 1], [1], [1, 1, 0],
           [1, 1], [1, 1, 1], [1, 1], [0, 0], [1, 1, 0], [1, 1, 0], [1, 1, 0], [1, 1], [1], [1, 1]]
    spect = [[0, 1, 1], [1, 1, 1], [1, 1, 1], [1], [1, 1, 1], [1, 1, 1, 1], [1, 1, 1], [1, 1], [1, 0], [1], [1, 1, 0],
             [1, 1], [1, 1, 1], [1, 1], [1, 1], [1, 1, 0], [1, 1, 0], [1, 1, 1], [1, 1], [1], [1, 1]]
    b = [sum(x == 1 and y == 0 for x, y in zip(p, s)) for p, s in zip(pet, spect)]
    c = [sum(x == 0 and y == 1 for x, y in zip(p, s)) for p, s in zip(pet, spect)]
    t = cf.durkalski(b, c, [len(p) for p in pet])
    assert round(t["statistic"], 2) == 2.32 and (sum(b) - sum(c)) ** 2 / (sum(b) + sum(c)) == 4.5
    assert math.isclose(t["p_two_sided"], stats.chi2.sf(t["statistic"], 1))


def test_sign_flip_exact_matches_brute_force():
    rng = np.random.default_rng(3)
    for _ in range(5):
        w = rng.normal(size=int(rng.integers(1, 9)))
        brute = np.mean([np.dot(e, w) >= w.sum() - 1e-12 for e in itertools.product([1, -1], repeat=len(w))])
        assert math.isclose(cf.sign_flip_exact(w), brute)
    assert cf.sign_flip_exact([0.0, 0.0]) == 1.0 and cf.sign_flip_exact([0.3, 0.0]) == 0.5


def _h2_rows(pairs):
    specs = []
    for i, (f, en, vi) in enumerate(pairs):
        for lang, y in (("en", en), ("vi", vi)):
            specs.append(dict(atom_id=f"a{i}", conflict_family=f, language=lang, us_unique=True,
                              label=4 if y else 2, foreign_systems="US,EU_UK" if y else ""))
    return specs


def test_h2_hand_example_end_to_end():
    # cluster f1: 2 pairs EN=1,VI=0; f2: 1 pair (1,0) + 3 concordant; f3: 1 pair (0,1) + 1 concordant
    pairs = [("f1", 1, 0), ("f1", 1, 0), ("f2", 1, 0), ("f2", 0, 0), ("f2", 1, 1), ("f2", 0, 0), ("f3", 0, 1),
             ("f3", 1, 1)]
    specs = _h2_rows(pairs)
    specs.append(dict(atom_id="x", conflict_family="f1", language="en", us_unique=False, label=4,
                      foreign_systems="US"))                     # not us_unique -> ignored
    specs.append(dict(atom_id="nd", conflict_family="f1", language="en", us_unique=True, has_decoy=False, label=4,
                      foreign_systems="US"))                     # no decoy -> ignored (rev-editor id 4)
    r = cf.h2_mcnemar_clustered(_rows(specs), n_boot=200)
    w = np.array([1.0, 0.25, -0.5])                               # (b_k - c_k) / n_k
    assert r["n_pairs"] == 8 and r["n_clusters"] == 3 and math.isclose(r["diff"], (3 - 1) / 8)
    assert math.isclose(r["statistic"], 3 / 7) and math.isclose(r["z"], w.sum() / math.sqrt((w ** 2).sum()))
    assert math.isclose(r["p_durkalski_one_sided"], stats.norm.sf(r["z"])) and r["direction"] == "en>vi"
    # rev-methods id 2(c): 3 < 20 families with discordant pairs -> exact sign-flip on w: 3 of 8 sums >= 0.75
    assert r["test"] == "sign_flip_exact" and r["n_families_discordant"] == 3
    assert math.isclose(r["p_one_sided"], 3 / 8)
    assert math.isclose(r["p_first"], 5 / 8) and math.isclose(r["p_second"], 3 / 8)


def test_h2_detects_language_effect_and_clean_pairs():
    df = cf.simulate_study(21, effect={"h2_en_mult": 2.0})
    alt = cf.h2_mcnemar_clustered(df, n_boot=300)
    assert alt["test"] == "durkalski" and alt["p_one_sided"] < 0.001 and alt["diff"] > 0 and alt["diff_ci_lo"] > 0
    clean = cf.h2_mcnemar_clustered(df, clean_only=True, n_boot=300)          # sensitivity B.19
    assert clean["clean_only"] and clean["n_pairs"] < alt["n_pairs"]
    assert cf.durkalski([0, 0], [0, 0], [3, 2])["p_one_sided"] == 1.0
    none = cf.h2_mcnemar_clustered(_rows(_h2_rows([("f1", 0, 0), ("f2", 1, 1)])), n_boot=100)
    assert none["test"] == "no_discordant_pairs" and none["p_one_sided"] == 1.0


# ------------------------------------------------------------------ Holm + partial conjunction
def test_holm_standard_example():
    p = {"H2": 0.01, "H3": 0.04, "H4": 0.03}
    r = cf.holm(p, alpha=0.05)
    assert [round(r[k]["p_holm"], 10) for k in ("H2", "H3", "H4")] == [0.03, 0.06, 0.06]
    assert [r[k]["reject"] for k in ("H2", "H3", "H4")] == [True, False, False]
    assert not cf.holm(p)["H2"]["reject"]                          # pre-registered one-sided level 0.025
    rng = np.random.default_rng(0)
    for _ in range(20):
        v = rng.random(3) ** 2
        ours = cf.holm(dict(zip("abc", v)))
        ref = multipletests(v, method="holm")[1]
        assert np.allclose([ours[k]["p_holm"] for k in "abc"], ref)
    assert cf.holm({"H2": float("nan"), "H3": 0.001})["H2"] == {"p": 1.0, "p_holm": 1.0, "reject": False,
                                                              "missing": True}


def test_partial_conjunction():
    assert math.isclose(cf.partial_conjunction([0.001, 0.02, 0.3, 0.5]), 3 * 0.02)      # M = 4, u = 2
    assert math.isclose(cf.partial_conjunction([0.2, 0.01, 0.04]), 2 * 0.04)            # M = 3, u = 2
    assert cf.partial_conjunction([0.9, 0.8], u=1) == 1.0
    assert cf.partial_conjunction([0.01, 0.2, 0.03], u=3) == 0.2                        # u = M: max p
    with pytest.raises(ValueError):
        cf.partial_conjunction([0.1, 0.2], u=3)


# ------------------------------------------------------------------ H3
def test_cp_design_effect_reduces_to_exact_cp_without_clustering():
    for k, n in ((0, 40), (3, 40), (12, 100), (40, 40)):
        r = cf.cp_design_effect([1] * k + [0] * (n - k), [1] * n, null=0.05)
        lo, hi = cp(k, n)
        assert r["deff"] == 1.0 and math.isclose(r["lo"], lo, abs_tol=1e-9) and math.isclose(r["hi"], hi, abs_tol=1e-9)
        assert math.isclose(r["p_one_sided"], 1.0 if k == 0 else stats.binom.sf(k - 1, n, 0.05))


def test_cp_design_effect_widens_with_clustering_and_matches_its_test():
    k_c, n_c = [9, 0, 1, 0, 8, 0, 2, 0, 0, 7], [10] * 10          # strongly clustered, 27/100
    r = cf.cp_design_effect(k_c, n_c, null=0.05)
    lo, _ = cp(27, 100)
    assert r["deff"] > 2 and r["lo"] < lo and r["n_eff"] < 100
    for kc in ([2, 1, 3, 0, 2, 1, 2, 0, 1, 2], [0, 1, 0, 0, 1, 0, 2, 0, 0, 1], k_c):
        q = cf.cp_design_effect(kc, n_c, null=0.05)
        assert (q["lo"] > 0.05) == (q["p_one_sided"] < 0.025)


def test_h3_per_model_partial_conjunction_decision():
    big = cf.h3_per_model(cf.simulate_study(31, effect={"a3_rate": 0.25}))
    assert big["n_models"] == 4 and big["u"] == 2 and big["confirmed_unadjusted"]
    assert big["n_models_lb_above_margin"] == 4 and all(m["deff"] >= 1 for m in big["per_model"].values())
    half = cf.h3_per_model(cf.simulate_study(32, effect={"a3_rate": [0.3, 0.3, 0.01, 0.01]}))
    assert half["confirmed_unadjusted"]
    one = cf.h3_per_model(cf.simulate_study(33, effect={"a3_rate": [0.25, 0.01, 0.01, 0.01]}))
    assert not one["confirmed_unadjusted"] and one["n_models_lb_above_margin"] <= 1
    ps = sorted(m["p_one_sided"] for m in one["per_model"].values())
    assert math.isclose(one["p_pc"], min(1.0, 3 * ps[1]))


def test_h3_set_is_conflict_atoms_only():
    # rev-methods id 2(f): no input column can widen the registered H3 set (conflict atoms)
    df = cf.simulate_study(34)
    base = cf.h3_per_model(df)
    widened = cf.h3_per_model(df.assign(distinct=True))
    assert base["per_model"] == widened["per_model"]
    n_conf = df[(df["condition"] == "A3") & (df["language"] == "vi") & (df["model"] == "sim_m1") &
                (df["conflict_status"] == "conflict")].shape[0]
    assert base["per_model"]["sim_m1"]["n"] == n_conf


# ------------------------------------------------------------------ H4
def _h4_rows(cells):
    """cells: list of (model, language, guideline, group, n_rows, n_errors, n_abstain)."""
    specs, i = [], 0
    for m, lang, gl, grp, n, k, a in cells:
        for j in range(n):
            lab = 6 if j < a else (4 if j < a + k else 2)
            specs.append(dict(model=m, language=lang, guideline=gl, atom_id=f"x{i}", condition="A2",
                              conflict_status="concordant", conflict_family=None, k_foreign=0, has_decoy=False,
                              group_signal=grp, label=lab))
            i += 1
    return _rows(specs)


def test_h4_mantel_haenszel_by_hand_and_guideline_clusters():
    # two strata (m1|vi, m2|vi); each spread over 3 guidelines so the cluster count is checkable
    cells = []
    for gl in ("g1", "g2", "g3"):
        cells += [("m1", "vi", gl, "disagree", 10, 4, 0), ("m1", "vi", gl, "agree", 30, 3, 0),
                  ("m2", "vi", gl, "disagree", 20, 2, 0), ("m2", "vi", gl, "agree", 10, 1, 0)]
    r = cf.h4_risk_ratio(_h4_rows(cells), n_boot=200)
    a1, n11, c1, n01 = 12, 30, 9, 90
    a2, n12, c2, n02 = 6, 60, 3, 30
    mh = (a1 * n01 / (n11 + n01) + a2 * n02 / (n12 + n02)) / (c1 * n11 / (n11 + n01) + c2 * n12 / (n12 + n02))
    assert math.isclose(r["rr"], mh) and r["estimator"] == "mh" and r["loss"] == "value_error"
    assert r["n_clusters"] == 3 and r["cluster_by"] == "guideline" and r["method"] == "t_small"
    assert set(r["per_stratum"]) == {"m1|vi", "m2|vi"}


def test_h4_zero_correction():
    # rev-methods id 2(d): no error in the agreement group -> +0.5 errors, +1 total in both groups of every stratum
    cells = [(m, "vi", gl, "disagree", 10, 2, 0) for m in ("m1",) for gl in ("g1", "g2")]
    cells += [(m, "vi", gl, "agree", 10, 0, 0) for m in ("m1",) for gl in ("g1", "g2")]
    r = cf.h4_risk_ratio(_h4_rows(cells), n_boot=100)
    assert r["zero_corrected"] and np.isfinite(r["rr"])
    assert math.isclose(r["rr"], ((4.5) * 21 / 42) / ((0.5) * 21 / 42))


def test_h4_self_abstention_is_not_an_error_in_the_primary_loss():
    # rev-methods id 3, rev-editor id 3, rev-clinician id 7: label 6 is excluded (coverage loss), not counted wrong
    cells = [("m1", "vi", gl, "disagree", 20, 2, 8) for gl in ("g1", "g2")]
    cells += [("m1", "vi", gl, "agree", 40, 4, 0) for gl in ("g1", "g2")]
    df = _h4_rows(cells)
    prim = cf.h4_risk_ratio(df, n_boot=100)
    wl = cf.h4_risk_ratio(df, n_boot=100, loss="W")
    assert math.isclose(prim["rr"], (4 / 24) / (8 / 80)) and prim["n_self_abstain_excluded"]["disagree"] == 16
    assert math.isclose(wl["rr"], (20 / 40) / (8 / 80)) and wl["rr"] > 2 * prim["rr"]


def test_h4_mantel_haenszel_removes_simpson_confounding():
    # rev-methods id 3(ii): within each model RR = 1 (A: 0.30 vs 0.30; B: 0.03 vs 0.03); crude pooling gives RR > 2
    cells = []
    for gl in ("g1", "g2", "g3", "g4"):
        cells += [("A", "vi", gl, "disagree", 60, 18, 0), ("A", "vi", gl, "agree", 40, 12, 0),
                  ("B", "vi", gl, "disagree", 100, 3, 0), ("B", "vi", gl, "agree", 900, 27, 0)]
    df = _h4_rows(cells)
    mh = cf.h4_risk_ratio(df, n_boot=100)
    crude = cf.h4_risk_ratio(df, n_boot=100, estimator="crude")
    assert crude["rr"] > 2.0 and math.isclose(mh["rr"], 1.0)


def test_h4_direction_and_bound():
    df = cf.simulate_study(41, effect={"h4_rr": 5.0})
    r = cf.h4_risk_ratio(df, n_boot=500, seed=2)
    assert r["method"] == "conservative" and r["rr"] > 2 and r["ci_lo"] > 2 and r["p_one_sided"] < 0.025
    assert r["confirmed_unadjusted"] and r["n_clusters"] == 30
    flipped = df.assign(group_signal=df["group_signal"].map({"agree": "disagree", "disagree": "agree"}))
    f = cf.h4_risk_ratio(flipped, n_boot=500, seed=2)
    assert f["rr"] < 1 and f["p_one_sided"] > 0.5 and math.isclose(f["rr"], 1 / r["rr"])
    null = cf.h4_risk_ratio(cf.simulate_study(42, effect={"h4_rr": 1.0}), n_boot=500, seed=2)
    assert null["ci_lo"] < 2 and null["p_one_sided"] > 0.5
    with pytest.raises(ValueError):
        cf.h4_risk_ratio(df.assign(group_signal="maybe"))


# ------------------------------------------------------------------ RQ3
def test_fit_logistic_l2_matches_unpenalised_mle_and_kkt():
    import statsmodels.api as sm

    rng = np.random.default_rng(1)
    X = rng.normal(size=(400, 3))
    y = (rng.random(400) < 1 / (1 + np.exp(-(0.5 + X @ np.array([1.0, -0.5, 0.0]))))).astype(float)
    w, b = cf.fit_logistic_l2(X, y, C=1e6)
    ref = sm.Logit(y, sm.add_constant(X)).fit(disp=0).params
    assert np.allclose(np.r_[b, w], ref, atol=1e-3)
    w1, b1 = cf.fit_logistic_l2(X, y, C=1.0)
    p = 1 / (1 + np.exp(-(X @ w1 + b1)))
    assert np.allclose(w1 + X.T @ (p - y), 0, atol=1e-3) and abs(np.sum(p - y)) < 1e-3   # KKT of the registered fit


def test_group_kfold_keeps_groups_together():
    g = np.repeat([f"g{i}" for i in range(7)], [9, 1, 5, 5, 3, 8, 2])
    f = cf.group_kfold(g, 3)
    assert pd.Series(f).groupby(g).nunique().eq(1).all() and set(f) == {0, 1, 2}
    assert (f == cf.group_kfold(g, 3)).all()
    loads = np.bincount(f)
    assert loads.max() - loads.min() <= 9


def test_rq3_scores_use_reference_labels_only():
    df = cf.simulate_study(55)
    d, _ = cf.rq3_frame(df, model="sim_m1")
    sp = d["atom_id"].map(cf.split_map(df)).to_numpy(dtype=object)
    s1 = cf.rq3_scores(d, sp)
    d2 = d.copy()
    nonref = sp != "ref"
    d2.loc[nonref, "C"] = ~d2.loc[nonref, "C"]                                 # flip every non-reference label
    assert np.allclose(s1, cf.rq3_scores(d2, sp))
    assert np.all((s1 > 0) & (s1 < 1))


def test_certified_rq3_is_per_model_vietnamese_one_row_per_atom():
    # rev-methods id 2(e): RQ3 per model, Vietnamese, one served answer per atom (value-stating)
    df = cf.simulate_study(51)
    r = cf.certified_rq3(df, model="sim_m1")
    n_atoms = df.loc[(df["model"] == "sim_m1") & (df["condition"] == "A2") & (df["language"] == "vi") &
                     (df["label"] != 6), "atom_id"].nunique()
    assert r["model"] == "sim_m1" and r["language"] == "vi" and sum(r["n_rows"].values()) == n_atoms
    assert r["n_self_abstain"] > 0 and 0 < r["self_abstention_rate"] < 0.2
    assert len(r["bounds"]) == 8 and all(0 <= b["U"] <= 1 for b in r["bounds"])
    assert all(b["U"] >= b["empirical"] for b in r["bounds"] if b["n"])
    assert r["dr4_alpha_by_group"] == {"agree": 0.15, "disagree": 0.15}
    assert math.isclose(r["bound_confidence_each"], 1 - 0.10 / 8)
    with pytest.raises(ValueError):
        cf.rq3_frame(pd.concat([df, df]), model="sim_m1")                     # duplicates -> refused
    with pytest.raises(ValueError):
        cf.certified_rq3(df.assign(group_signal="agree"), model="sim_m1")


def test_rq3_split_is_over_all_atoms_and_cluster_sensitivity():
    atoms = np.repeat([f"a{i}" for i in range(500)], 3)
    sp = cf.assign_rq3_split(atoms)
    assert pd.Series(sp).groupby(atoms).nunique().eq(1).all()
    share = pd.Series(sp[::3]).value_counts(normalize=True)
    assert abs(share["ref"] - 0.2) < 0.01 and abs(share["cal"] - 0.4) < 0.01
    df = cf.simulate_study(52)
    m = cf.split_map(df)
    assert len(m) == df["atom_id"].nunique()
    mc = cf.split_map(df, unit="cluster")
    fam = df.drop_duplicates("atom_id").set_index("atom_id")["conflict_family"].dropna()
    assert pd.Series({a: mc[a] for a in fam.index}).groupby(fam).nunique().eq(1).all()   # families stay together
    r = cf.certified_rq3(df, model="sim_m2", split_unit="cluster")
    assert r["split_unit"] == "cluster" and len(r["bounds"]) == 8


def test_rq3_rerandomisation_and_regime_b_refit():
    df = cf.simulate_study(61)
    r = cf.certified_rq3(df, model="sim_m3", n_rerandomise=20)
    rr = r["rerandomisation"]
    assert rr["n"] == 20 and 0 <= rr["bound_violation_rate"] <= 1 and rr["target"] == 0.10
    calls = []

    def counting_fit(X, y, **kw):
        calls.append(len(y))
        return cf.fit_logistic_l2(X, y, **kw)

    rb = cf.rq3_regime_b(df, model="sim_m3", n_splits=6, fit=counting_fit)
    assert rb["n_used"] > 0 and rb["score_refit_per_split"] and rb["max_violation"] == 0.20
    n_ref_gl = round(0.2 * rb["n_guidelines"])
    assert len(calls) == rb["n_used"] * (1 + min(5, n_ref_gl))                 # rev-methods id 2(g): refit per split


# ------------------------------------------------------------------ missing data, tipping points, run_all
def test_missing_bounds_triggered_above_two_percent():
    df = cf.simulate_study(71)
    m = (df["condition"] == "A1") & (df["language"] == "vi") & (df["conflict_status"] == "conflict")
    idx = df.index[m][:: 20]                                                   # ~5% missing in the H1 cell
    d = df.copy()
    d.loc[idx, "label"] = np.nan
    r = cf.missing_bounds(d, n_boot=200)
    assert r["h1"]["triggered"] and r["h1"]["high"]["delta"] > r["h1"]["low"]["delta"]
    assert not r["h3"]["triggered"] and not r["h4"]["triggered"]
    assert not cf.missing_bounds(df, n_boot=100)["h1"]["triggered"]


def test_tipping_points():
    df = cf.simulate_study(72, effect={"pi_foreign": 0.12})
    t = cf.tipping_point_h1(df, false_conflicts_found=2, n_checked=100, n_boot=300)
    assert 0 < t["t_star"] <= t["n_conflict_atoms"]
    assert math.isclose(t["false_conflict_cp_upper"], stats.beta.ppf(0.95, 3, 98))
    assert t["robust"] == (t["t_star"] > t["false_conflict_cp_upper"] * t["n_conflict_atoms"])
    t3 = cf.tipping_point_h3(cf.simulate_study(73, effect={"a3_rate": 0.25}), p_h2=0.5, p_h4=0.5,
                             false_conflicts_found=0, n_checked=100)
    assert t3["t_star"] > 0


def test_run_all_serializable_and_complete():
    df = cf.simulate_study(81)
    out = cf.run_all(df, n_boot=200, regime_b_splits=4, rerandomisations=5)
    keys = {"h1", "h1_per_model", "h1_unscaled_decoy", "h1_guideline_clusters", "h1_robustness", "h2",
            "h2_clean_pairs", "h3", "h3_guideline_clusters", "h3_without_flagged_passages", "h4", "h4_crude_W",
            "h4_mh_W", "h4_vi_only", "holm", "dr3", "missing_bounds", "rq3"}
    assert keys <= set(out) and out["meta"]["decision_rule"] == "conservative"
    assert set(out["holm"]) == {"H2", "H3", "H4"} and out["meta"]["models"] == [f"sim_m{i}" for i in range(1, 5)]
    assert set(out["rq3"]) == set(out["meta"]["models"])
    for m, r in out["rq3"].items():
        assert r["vi"]["language"] == "vi" and r["vi"]["model"] == m and r["en"]["language"] == "en"
        assert r["vi"]["rerandomisation"]["n"] == 5 and r["vi_regime_b"]["n_splits"] == 4
    assert out["h4"]["estimator"] == "mh" and out["h4"]["cluster_by"] == "guideline"
    json.dumps(out, allow_nan=False)


def test_prepare_filters_rows():
    df = _rows([dict(atom_id="a", label=4), dict(atom_id="b", label=None), dict(atom_id="c", label=4,
                                                                              conflict_status="indistinguishable"),
                dict(atom_id="d", label=4, sample_idx=1), dict(atom_id="e", label=4, temperature=0.7)])
    d = cf.prepare(df)
    assert d["atom_id"].tolist() == ["a"] and d["cluster"].tolist() == ["fam:f0"] and d["cluster_gl"].tolist() == ["gl:g0"]
    assert d[["C", "W", "E", "V"]].iloc[0].tolist() == [False, True, True, True]
    assert cf.cluster_key(_rows([dict(conflict_family=None, guideline="g9")]))[0] == "gl:g9"
    with pytest.raises(ValueError):
        cf.prepare(df.drop(columns=["k_foreign"]))
    with pytest.raises(ValueError):
        cf.prepare(df.assign(conflict_status="maybe"))
