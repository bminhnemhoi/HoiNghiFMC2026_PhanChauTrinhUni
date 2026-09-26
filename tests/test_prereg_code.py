"""Tests for the pre-registered confirmatory code (T2.10): src/vnsoc/analysis/confirmatory.py. Fast (< 60 s)."""
import json
import math
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
    """specs: list of dicts overriding a default graded row."""
    base = dict(model="m1", atom_id="a0", conflict_family="f0", guideline="g0", language="vi", condition="A1",
                format="short", label=2, decoy_match=False, foreign_systems="", us_unique=False,
                group_signal="agree", wrong=False)
    return pd.DataFrame([{**base, **s} for s in specs])


# ------------------------------------------------------------------ pre-registered constants
def test_constants_match_configs():
    cfg = yaml.safe_load((ROOT / "configs" / "project.yaml").read_text(encoding="utf-8"))
    h, r = cfg["hypotheses"], cfg["rq3"]
    assert h["primary"] == "H1" and h["secondary_family"] == ["H2", "H3", "H4"]
    assert cf.CI_LEVEL == h["ci_level"] and cf.H3_MARGIN == h["H3_margin"] and cf.H4_RR_BOUND == h["H4_rr_lower_bound"]
    assert math.isclose(cf.ALPHA_ONE_SIDED, (1 - h["ci_level"]) / 2)
    assert list(cf.RQ3_GROUPS) == r["groups"] and list(cf.RQ3_COVERAGES) == r["coverages"]
    assert (cf.RQ3_ALPHA, cf.RQ3_DELTA, cf.RQ3_ALPHA_FALLBACK) == (r["alpha"], r["delta"], r["alpha_fallback"])
    assert cf.RQ3_MIN_CAL_ATOMS == r["alpha_fallback_min_cal_atoms"]
    assert cf.RQ3_MIN_USEFUL_COVERAGE == r["min_useful_coverage"]
    assert cf.RQ3_REGIME_B_SPLITS == r["regime_b_splits"]
    assert cf.RQ3_REGIME_B_MAX_VIOLATION == r["regime_b_max_violation"] == 2 * r["delta"]
    assert dict(cf.RQ3_SPLIT_FRACTIONS) == r["split_fractions"] and cf.SPLIT_SEED == r["split_seed"]


# ------------------------------------------------------------------ simulate_study
def test_simulate_study_structure():
    F, apf, M = 12, 5, 3
    df = cf.simulate_study(7, n_families=F, atoms_per_family=apf, models=M)
    cpf = cf.DEFAULT_EFFECT["concordant_per_family"]
    assert set(cf.REQUIRED) <= set(df.columns)
    assert len(df) == F * (apf + cpf) * M * 2 * 4
    assert set(df["condition"]) == {"A0", "A1", "A2", "A3"} and set(df["language"]) == {"vi", "en"}
    cells = df.groupby(["atom_id", "model", "language"])["condition"].agg(lambda s: tuple(sorted(s)))
    assert (cells == ("A0", "A1", "A2", "A3")).all()
    assert df.groupby(["atom_id", "model", "language"])["group_signal"].nunique().eq(1).all()
    assert (df["wrong"] == df["label"].isin([3, 4, 5])).all()
    assert df.loc[df["decoy_match"], "label"].eq(5).all()
    assert ((df["foreign_systems"] != "") == (df["label"] == 4)).all()
    conf = df["conflict_status"] == "conflict"
    assert df.loc[conf, "conflict_family"].notna().all() and df.loc[~conf, "conflict_family"].isna().all()
    assert not df.loc[df["us_unique"], "conflict_status"].ne("conflict").any()
    assert df.loc[df["us_unique"] & (df["label"] == 4), "foreign_systems"].eq("US").all()
    assert df["score"].notna().eq(df["condition"] == "A2").all()
    assert df.loc[conf, "conflict_family"].nunique() == F
    pd.testing.assert_frame_equal(df, cf.simulate_study(7, n_families=F, atoms_per_family=apf, models=M))
    assert not df["label"].equals(cf.simulate_study(8, n_families=F, atoms_per_family=apf, models=M)["label"])


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
    assert math.isclose(r["p_one_sided"], stats.t.sf((1 / 12) / se, 2)) and not r["confirmed"]


def test_h1_detects_large_effect():
    df = cf.simulate_study(11)                                     # 30% foreign vs 5% decoy, 40 families
    r = cf.h1_delta(df, n_boot=500, seed=1)
    assert r["method"] == "bca" and r["n_clusters"] == 40 and r["n_responses"] == 400 * 4
    assert r["confirmed"] and r["ci_lo"] > 0.1 and r["p_one_sided"] < 0.001
    assert abs(r["pi_foreign"] - 0.30) < 0.08 and abs(r["pi_decoy"] - 0.05) < 0.04
    assert r["ci_lo"] < r["delta"] < r["ci_hi"] and r["excess_ci_lo"] < r["excess"] < r["excess_ci_hi"]
    assert set(r["variants"]) == {"bca", "bca_expanded", "jackknife_t"} and r["confirmed_all_variants"]
    assert r["variants"]["bca_expanded"]["lo"] <= r["variants"]["bca"]["lo"]      # expansion only widens
    one = cf.h1_delta(df, n_boot=300, seed=1, models=["sim_m1"])
    assert one["models"] == ["sim_m1"] and one["n_responses"] == 400


def test_h1_null_ci_mostly_contains_zero():
    hits, reps = 0, 40
    for i in range(reps):
        df = cf.simulate_study(1000 + i, effect=cf.NULL_EFFECT)
        r = cf.h1_delta(df, n_boot=300, seed=i)
        hits += r["ci_lo"] <= 0 <= r["ci_hi"]
    assert hits >= 0.8 * reps


def test_h1_under_20_clusters_uses_small_sample_t():
    r = cf.h1_delta(cf.simulate_study(3, n_families=10), n_boot=200)
    assert r["method"] == "t_small" and r["n_clusters"] == 10 and set(r["variants"]) == {"jackknife_t"}


def test_bca_matches_scipy_on_iid_mean():
    x = np.random.default_rng(5).exponential(size=200)          # skewed: z0 and acceleration both matter
    M = np.c_[np.ones_like(x), x]                                  # clusters of size 1 -> ratio = mean
    r = cf.cluster_interval(M, lambda S: S[..., 1] / S[..., 0], n_boot=4000, seed=2)
    ref = stats.bootstrap((x,), np.mean, method="BCa", n_resamples=4000, random_state=3).confidence_interval
    assert r["method"] == "bca"
    assert abs(r["lo"] - ref.low) < 0.02 and abs(r["hi"] - ref.high) < 0.02


# ------------------------------------------------------------------ H2 (Durkalski)
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


def test_h2_hand_example_end_to_end():
    # cluster f1: 2 pairs EN=1,VI=0; f2: 1 pair (1,0) + 3 concordant; f3: 1 pair (0,1) + 1 concordant
    pairs = [("f1", 1, 0), ("f1", 1, 0), ("f2", 1, 0), ("f2", 0, 0), ("f2", 1, 1), ("f2", 0, 0), ("f3", 0, 1),
             ("f3", 1, 1)]
    specs = []
    for i, (f, en, vi) in enumerate(pairs):
        for lang, y in (("en", en), ("vi", vi)):
            specs.append(dict(atom_id=f"a{i}", conflict_family=f, language=lang, us_unique=True,
                              label=4 if y else 2, foreign_systems="US,EU_UK" if y else ""))
    specs.append(dict(atom_id="x", conflict_family="f1", language="en", us_unique=False, label=4,
                      foreign_systems="US"))                     # not us_unique -> ignored
    r = cf.h2_mcnemar_clustered(_rows(specs))
    w = np.array([1.0, 0.25, -0.5])                               # (b_k - c_k) / n_k
    assert r["n_pairs"] == 8 and r["n_clusters"] == 3 and math.isclose(r["diff"], (4 - 1) / 8)
    assert math.isclose(r["statistic"], 3 / 7) and math.isclose(r["z"], w.sum() / math.sqrt((w ** 2).sum()))
    assert math.isclose(r["p_one_sided"], stats.norm.sf(r["z"])) and r["direction"] == "en>vi"
    assert math.isclose(r["p_first"], 5 / 8) and math.isclose(r["p_second"], 2 / 8)


def test_h2_detects_language_effect_and_not_under_null():
    alt = cf.h2_mcnemar_clustered(cf.simulate_study(21, effect={"h2_en_mult": 2.0}))
    assert alt["p_one_sided"] < 0.001 and alt["diff"] > 0
    assert cf.durkalski([0, 0], [0, 0], [3, 2])["p_one_sided"] == 1.0


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
    half = cf.h3_per_model(cf.simulate_study(32, effect={"a3_rate": [0.25, 0.25, 0.01, 0.01]}))
    assert half["confirmed_unadjusted"]
    one = cf.h3_per_model(cf.simulate_study(33, effect={"a3_rate": [0.25, 0.01, 0.01, 0.01]}))
    assert not one["confirmed_unadjusted"] and one["n_models_lb_above_margin"] <= 1
    ps = sorted(m["p_one_sided"] for m in one["per_model"].values())
    assert math.isclose(one["p_pc"], min(1.0, 3 * ps[1]))


# ------------------------------------------------------------------ H4
def test_h4_direction_and_bound():
    df = cf.simulate_study(41, effect={"h4_rr": 5.0})
    r = cf.h4_risk_ratio(df, n_boot=500, seed=2)
    assert r["method"] == "bca" and r["rr"] > 2 and r["ci_lo"] > 2 and r["p_one_sided"] < 0.025
    assert math.isclose(r["rr"], r["risk_disagree"] / r["risk_agree"]) and r["confirmed_unadjusted"]
    flipped = df.assign(group_signal=df["group_signal"].map({"agree": "disagree", "disagree": "agree"}))
    f = cf.h4_risk_ratio(flipped, n_boot=500, seed=2)
    assert f["rr"] < 1 and f["p_one_sided"] > 0.5 and math.isclose(f["rr"], 1 / r["rr"])
    null = cf.h4_risk_ratio(cf.simulate_study(42, effect={"h4_rr": 1.0}), n_boot=500, seed=2)
    assert null["ci_lo"] < 2 and null["p_one_sided"] > 0.5
    with pytest.raises(ValueError):
        cf.h4_risk_ratio(df.assign(group_signal="maybe"))


# ------------------------------------------------------------------ RQ3
def test_certified_rq3_bounds_and_alpha_fallback():
    small = cf.certified_rq3(cf.simulate_study(51))              # 600 atoms -> ~240 calibration atoms < 300
    assert len(small["bounds"]) == 8 and all(0 <= b["U"] <= 1 for b in small["bounds"])
    assert all(b["U"] >= b["empirical"] for b in small["bounds"] if b["n"])
    assert small["dr4_alpha_by_group"] == {"agree": 0.15, "disagree": 0.15}
    assert math.isclose(small["bound_confidence_each"], 1 - 0.10 / 8)
    assert isinstance(small["dr5_useful_disagree"], bool)
    big = cf.certified_rq3(cf.simulate_study(52, n_families=80, effect={"p_disagree": 0.02}))
    assert big["ltt"]["agree"]["n_cal_atoms"] >= 300 and big["ltt"]["agree"]["alpha_used"] == 0.10
    assert big["ltt"]["disagree"]["n_cal_atoms"] < 300 and big["ltt"]["disagree"]["alpha_used"] == 0.15
    assert all(0 <= b["U"] <= 1 for b in big["bounds"])
    with pytest.raises(ValueError):
        cf.certified_rq3(cf.simulate_study(53).assign(group_signal="agree"))


def test_rq3_split_keeps_atoms_together_and_uses_fractions():
    atoms = np.repeat([f"a{i}" for i in range(500)], 3)
    sp = cf.assign_rq3_split(atoms)
    s = pd.Series(sp).groupby(atoms).nunique()
    assert s.eq(1).all()
    share = pd.Series(sp[::3]).value_counts(normalize=True)
    assert abs(share["ref"] - 0.2) < 0.01 and abs(share["cal"] - 0.4) < 0.01
    assert (sp == cf.assign_rq3_split(atoms)).all()


def test_rq3_regime_b_and_run_all_serializable():
    df = cf.simulate_study(61)
    rb = cf.rq3_regime_b(df, n_splits=20)
    assert rb["n_used"] > 0 and 0 <= rb["bound_violation_rate"] <= 1 and rb["max_violation"] == 0.20
    out = cf.run_all(df, n_boot=300, regime_b_splits=10)
    assert {"h1", "h1_per_model", "h2", "h3", "h4", "holm", "dr3", "rq3", "rq3_regime_b"} <= set(out)
    assert set(out["holm"]) == {"H2", "H3", "H4"} and out["meta"]["models"] == [f"sim_m{i}" for i in range(1, 5)]
    json.dumps(out, allow_nan=False)


def test_prepare_filters_rows():
    df = _rows([dict(atom_id="a", label=4), dict(atom_id="b", label=None), dict(atom_id="c", label=4,
                                                                              conflict_status="indistinguishable"),
                dict(atom_id="d", label=4, sample_idx=1), dict(atom_id="e", label=4, temperature=0.7)])
    d = cf.prepare(df)
    assert d["atom_id"].tolist() == ["a"] and d["cluster"].tolist() == ["fam:f0"]
    assert cf.cluster_key(_rows([dict(conflict_family=None, guideline="g9")]))[0] == "gl:g9"
    with pytest.raises(ValueError):
        cf.prepare(df.drop(columns=["wrong"]))
