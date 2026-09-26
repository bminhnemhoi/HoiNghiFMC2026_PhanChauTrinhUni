# Confirmatory analysis plan: code, parameters, simulation checks

*Whose Standard of Care?* (vn-soc-audit), task T2.10, revised 2026-09-26 after the preregistration review
(`review/prereg/response.md`). This folder is attached to the OSF preregistration (`prereg/osf_preregistration.md`,
HG2.9). The code was written and checked **on simulated data only, before any model output of the main study
exists**. `scripts/prereg_snapshot.py` writes the SHA-256 of every file of the package into Section 5.0 of the
registration and into `SHA256SUMS`; the confirmatory analyses (T6.3–T6.7) call exactly these functions with these
parameters. The registration text governs; any change after submission goes to `docs/DECISIONS.md` plus an addendum
in `prereg/addenda/`.

| File | Role |
|---|---|
| `src/vnsoc/analysis/confirmatory.py` | all confirmatory estimators, tests, sensitivity analyses and the simulator (numpy / scipy / pandas) |
| `src/vnsoc/match/atom_flags.py` | atom-level fields computed by code from the frozen atom (k_i, US-unique, conflict family, decoy audit, neighbour overlap, surrogates, freeze checks) |
| `tests/test_prereg_code.py`, `tests/test_atom_flags.py`, `tests/test_grade_review.py`, `tests/test_prereg_support.py` | unit tests: hand-computed examples, published Durkalski values, Holm vs statsmodels, BCa vs scipy, logistic fit vs statsmodels, exact sign-flip and wild bootstrap vs brute force, the reviewers' probes |
| `prereg/analysis_plan/simulate_operating_characteristics.py` | type I error / power by simulation at the registered B → `operating_characteristics.json`, the table below and the summary in registration §3.3 |
| `prereg/analysis_plan/operating_characteristics.json` | script output (never edited by hand) |
| `prereg/analysis_plan/SHA256SUMS` | hash manifest of the package (written by `scripts/prereg_snapshot.py`) |

## 1. Hypotheses → functions

Proposal sections: §1.4 (hypotheses), §4.4 (conditions), §4.6–4.7 (signal groups, certified abstention),
§5.3 (outcomes and analysis), §5.4 (RQ3 sample size); decision rules DR3–DR5 in the implementation plan.

| Item | Function | Analysis set | Estimand | Interval / test | Decision (pre-registered) |
|---|---|---|---|---|---|
| **H1** (primary) | `h1_delta` (+ `wild_cluster_p`) | A1, Vietnamese, short answers, conflict atoms **with a frozen decoy**, open models pooled | Δ = π_f − π_d with π_d = mean(k_i·D); also E = Δ/(1 − π_d) | family-clustered bootstrap, B = 10,000: BCa, expanded BCa, cluster jackknife-t; wild cluster restricted bootstrap-t; < 20 families → jackknife-t and wild bootstrap (exact enumeration when 2^C ≤ B) | supported iff all three lower limits > 0 and wild p ≤ 0.025 (rule `conservative`) |
| H1 robustness | `h1_robustness`, `h1_directional` | as H1 | S1 directional correction; S2 mirror_arith num/bp; S3 roundness; N1 no neighbour overlap | same rule | "H1 robust" iff S1 and S2 lower limits > 0 |
| **H2** | `h2_mcnemar_clustered` (`durkalski`, `sign_flip_exact`) | A1, (atom, model) pairs in EN and VI, US-unique conflict atoms with a decoy | P_EN − P_VI of "label 4 with system US" | Durkalski clustered McNemar over families; exact sign-flip when < 20 families have a discordant pair | Holm-adjusted p ≤ 0.025 |
| **H3** | `h3_per_model` (`cp_design_effect`, `partial_conjunction`) | A3, Vietnamese, **conflict atoms only**; each open model | P(label 3 or 4) | design-effect Clopper–Pearson with t(C−1) df; one-sided p for rate ≤ 5% | partial conjunction (M − u + 1)·p_(u), u = ⌈M/2⌉; Holm-adjusted p ≤ 0.025 |
| **H4** | `h4_risk_ratio` | A2 served answers that **state a value** (labels 1–5), both languages, open models, non-indistinguishable atoms | Mantel–Haenszel RR (strata model × language) of labels 3–5 | guideline-clustered bootstrap, rule `conservative` (BCa ∧ expanded BCa ∧ jackknife-t); zero correction | Holm-adjusted p ≤ 0.025 |
| Holm | `holm` | {H2, H3, H4} | — | Holm step-down | reject iff adjusted p ≤ 0.025 |
| DR3 | `dr3_check` | A2, conflict atoms, each model × language | P(label 3 or 4) | clustered CP upper bound | triggered iff every upper bound < 5% |
| RQ3 (a) | `certified_rq3` (`split_map`, `rq3_scores`, `fit_logistic_l2`, `group_kfold`, `rq3_rerandomise`) | **per open model, Vietnamese, one served value-stating answer per atom** | selective risk of labels 3–5 per group and coverage | simultaneous CP bounds at 1 − δ/(G·K); LTT per group; 500 re-randomisations (implementation check); cluster-split sensitivity | primary output U_gk; DR4; DR5 |
| RQ3 (b) | `rq3_regime_b` | same, split by guideline, **score refit in every split** | violation frequency | 500 guideline splits | acceptable iff ≤ 2δ |
| Missing data | `missing_bounds` | H1, H3, H4 cells with > 2% missing | extreme imputations | — | reported |
| False conflicts | `tipping_point_h1`, `tipping_point_h3` | as H1 / H3 | t* vs CP upper bound × conflict atoms | — | "robust" iff t* larger |
| all | `run_all` | — | — | — | one JSON-safe dict for the registry (`vnsoc.numbers.put` in T6.x) |

**Decision level.** Every interval is two-sided 95% (`configs/project.yaml: hypotheses.ci_level`). "Lower 95%
bound > null value" is the same decision as "one-sided p < 0.025", so every one-sided p-value is compared with 0.025
and Holm runs at that level.

## 2. Fixed parameters and seeds

| Parameter | Value | Source |
|---|---|---|
| CI level; one-sided decision level | 0.95; 0.025 | `project.yaml hypotheses.ci_level` |
| H3 margin; H4 RR bound; H1 smallest effect of interest (E, interpretation only) | 0.05; 2.0; 0.10 | `hypotheses.H3_margin`, `hypotheses.H4_rr_lower_bound`, `hypotheses.H1_sesoi_excess` |
| Holm family | H2, H3, H4 | `hypotheses.secondary_family` |
| RQ3 groups G; coverages c_k | agree, disagree (G = 2); 1.0, 0.75, 0.5, 0.25 (K = 4) | `rq3.groups`, `rq3.coverages` |
| RQ3 α; δ; α fallback; fallback trigger | 0.10; 0.10; 0.15; < 300 calibration atoms in the group | `rq3.*` |
| Minimum useful coverage (DR5) | 0.30 in the disagreement group | `rq3.min_useful_coverage` |
| Split fractions; split seed | ref 0.2 / cal 0.4 / test 0.4 by atom; 20261001 | `rq3.split_fractions`, `rq3.split_seed` |
| Regime (b) splits; acceptance | 500; ≤ 0.20 = 2δ | `rq3.regime_b_splits`, `rq3.regime_b_max_violation_rate` |
| Bootstrap resamples; bootstrap seed | 10,000; 20261001 | `N_BOOT`, `BOOT_SEED` (registration §5.1.1) |
| Interval rule | `conservative` (H1: 4-part, H4: 3-part intersection–union) | `PRIMARY_RULE` |
| BCa → small-sample switch; H2 exact switch | < 20 clusters; < 20 families with a discordant pair | `MIN_CLUSTERS_BCA`, `SIGNFLIP_MIN_FAMILIES` |
| H4 strata; clusters | model × language; guideline | `H4_STRATA` |
| RQ3 score | L2 logistic, C = 1, ≤ 1000 iterations, GroupKFold ≤ 5 folds; features s1, s2, s3, consistency, log-probability (+ missingness) | `RQ3_*` |
| Regime (a) re-randomisations | 500, seeds [20261001, 1, i] | `RQ3_RERANDOMISATIONS` |
| Missing-data trigger | > 2% missing in the cell | `MISSING_BOUND_TRIGGER` |

`tests/test_prereg_code.py::test_constants_match_configs` and `::test_registered_analysis_constants` fail if the
module constants, the configs and the registration drift apart; `::test_registration_function_table_matches_module`
fails if the registration names a function that does not exist.

## 3. Data conventions (apply to every confirmatory function)

- Input is one row per graded answer: `model, atom_id, conflict_family, guideline, language, condition, format,
  label (1–6), decoy_match, foreign_systems, conflict_status, us_unique, k_foreign, has_decoy`, plus the columns a
  function needs (`group_signal`, RQ3 features and `split`, H1-robustness and H2/H3-sensitivity columns).
- The atom-level columns come from `vnsoc.match.atom_flags.atom_covariates(frozen atom)`, never typed by hand.
- The losses are derived from the label inside the code: C = labels 1–2, W = labels 3–6, E = labels 3–5, V = label ≠ 6.
  No `wrong` column is accepted.
- Only greedy answers enter a confirmatory test (temperature 0, `sample_idx` 0). The five T = 0.7 samples feed the
  disagreement signal only.
- Atoms whose sources are indistinguishable (`conflict_status == "indistinguishable"`) never enter a confirmatory test
  (proposal §1.2). Rows without a label (runtime errors) are dropped and counted (`run_all.meta`).
- Resampling unit: the conflict family (mechanical rule, `atom_flags.family_id`) for H1–H3; the guideline for H4.
- Label 4 and a decoy match are mutually exclusive by the label priority (a decoy match is label 5 with
  `decoy_match = True`).

## 4. How to run

```bash
cd "/d/phan chau trinh _ y khoa"
PYTHONUTF8=1 .venv/bin/python -m pytest -q tests/test_prereg_code.py tests/test_atom_flags.py tests/test_grade_review.py
PYTHONUTF8=1 .venv/bin/python prereg/analysis_plan/simulate_operating_characteristics.py            # ~15 min, 11 processes
PYTHONUTF8=1 .venv/bin/python prereg/analysis_plan/simulate_operating_characteristics.py --quick    # smoke test, writes nothing
PYTHONUTF8=1 .venv/bin/python scripts/prereg_snapshot.py [--pdf]                                   # hashes (+ PDF) of the package
```

On the real graded data (T6.3–T6.7):

```python
from vnsoc.analysis import confirmatory as cf
res = cf.run_all(grades_df)          # open models from configs/models.yaml, B = 10,000, seed 20261001
```

## 5. Simulation model (`simulate_study`)

Conflict families (clusters) of conflict atoms, optionally with lognormal sizes, plus concordant atoms clustered by
guideline; 4 open models × VI/EN × A0–A3; short, greedy answers. Every null holds exactly in the superpopulation:

- H1: a "source match" event with atom mean pf_i + pd_i, where pf_i = π_f + (k_i − 1)·π_d (30% of conflict atoms have
  k_i = 2) and pd_i = π_d, or 0 for the 5% of conflict atoms without a decoy; it is split into foreign versus decoy with
  atom mean pf_i/(pf_i + pd_i) and a mean-preserving family-level perturbation. So E[F − k·D] = π_f − π_d, and the
  decoy-less atoms would bias Δ upwards if they were not excluded.
- H2: the EN source-match rate on US-unique atoms is multiplied by `h2_en_mult` (1 under the null).
- H3: per-model cluster rates with mean `a3_rate[m]`, comonotone across models.
- H4 / RQ3 at A2: model-specific disagreement shares (0.4–1.6 × 25%) and base risks (0.7–1.3 ×), both increasing
  with the model index (Simpson confounding for a crude pooled RR); self-abstention (label 6) 2% in the agreement group
  and 12% in the disagreement group; among value-stating answers the within-stratum RR of labels 3–5 equals `h4_rr`.
  Signals s1–s3 fire only in the disagreement group; consistency and log-probability depend on the error.

Scenarios: `null` = global null (π_f = π_d = 0.05; no language effect; every model's A3 rate exactly 5%; RR exactly 2
within every stratum). `alt` = the proposal's scale (30% vs 5%; EN ×1.5; A3 10%; RR 3). `modest` = a smaller effect.
`h3lfc` = the least-favourable null of the partial-conjunction test (one model at 30%, three exactly at 5%). Designs:
40 × 10 (planning), 25 × 16 (minimum of DR2), 25 families with lognormal sizes (σ = 1), and 12 × 10 (< 20 families).

## 6. Measured operating characteristics

<!-- OC:BEGIN (generated by simulate_operating_characteristics.py; do not edit by hand) -->

Generated 2026-09-26T12:46:56 by `simulate_operating_characteristics.py` from `operating_characteristics.json`. B = 10000 bootstrap resamples (the registered size) for H1 and H4; one-sided decision level 0.025; Monte Carlo standard errors in brackets. Entries are rejection rates: type I error under a null scenario, power under an alternative. Registered rules: H1 = BCa ∧ expanded BCa ∧ cluster jackknife-t ∧ wild cluster bootstrap-t; H4 = Mantel–Haenszel RR (model × language) on value-stating answers, loss = labels 3–5, guideline clusters, BCa ∧ expanded BCa ∧ jackknife-t.

| Scenario | Reps | H1 registered | H1 BCa alone | H2 | H3 (partial conj.) | H4 registered | Holm: any of H2–H4 | RQ3 (a) some U_gk exceeded (sim_m3, VI) | H1 interval path |
|---|---|---|---|---|---|---|---|---|---|
| `null_40x10`: global null, planning design (400 conflict atoms, 40 families) | 2000 | 0.023 (0.003) | 0.029 (0.004) | 0.026 (0.004) | 0.001 (0.001) | 0.018 (0.003) | 0.011 (0.002) | 0.002 (0.001) | conservative: 2000 |
| `null_25x16`: global null, minimum design (DR2: 400 atoms, 25 families) | 2000 | 0.021 (0.003) | 0.032 (0.004) | 0.026 (0.004) | 0.001 (0.000) | 0.026 (0.004) | 0.013 (0.003) | 0.002 (0.001) | conservative: 2000 |
| `null_25x16_uneq`: global null, 25 families with lognormal sizes (mean 16) | 2000 | 0.023 (0.003) | 0.053 (0.005) | 0.020 (0.003) | 0.011 (0.002) | 0.024 (0.003) | 0.015 (0.003) | 0.001 (0.000) | conservative: 2000 |
| `null_12x10`: global null, < 20 families (small-sample path) | 2000 | 0.026 (0.004) | 0.029 (0.004) | 0.016 (0.003) | 0.001 (0.000) | 0.030 (0.004) | 0.014 (0.003) | 0.000 (0.000) | t_small: 2000 |
| `h3lfc_40x10`: H3 least-favourable null: one model at 30%, three exactly at the 5% margin (other nulls as global) | 2000 | 0.017 (0.003) | 0.025 (0.003) | 0.021 (0.003) | 0.013 (0.003) | 0.025 (0.004) | 0.017 (0.003) | 0.002 (0.001) | conservative: 2000 |
| `h3lfc_25x16_uneq`: H3 least-favourable null, unequal families | 2000 | 0.025 (0.003) | 0.054 (0.005) | 0.025 (0.003) | 0.019 (0.003) | 0.028 (0.004) | 0.021 (0.003) | 0.004 (0.001) | conservative: 2000 |
| `alt_40x10`: protocol effect: pi_f 0.30 vs pi_d 0.05; H2 x1.5; H3 10%; H4 RR 3 | 400 | 1.000 (0.000) | 1.000 (0.000) | 0.998 (0.002) | 0.738 (0.022) | 0.858 (0.017) | 1.000 (0.000) | 0.010 (0.005) | conservative: 400 |
| `alt_25x16`: protocol effect, minimum design | 300 | 1.000 (0.000) | 1.000 (0.000) | 0.997 (0.003) | 0.513 (0.029) | 0.793 (0.023) | 1.000 (0.000) | 0.003 (0.003) | conservative: 300 |
| `alt_25x16_uneq`: protocol effect, unequal families | 300 | 1.000 (0.000) | 1.000 (0.000) | 0.913 (0.016) | 0.353 (0.028) | 0.597 (0.028) | 0.930 (0.015) | 0.000 (0.000) | conservative: 300 |
| `alt_12x10`: protocol effect, < 20 families | 300 | 1.000 (0.000) | 1.000 (0.000) | 0.707 (0.026) | 0.177 (0.022) | 0.403 (0.028) | 0.660 (0.027) | 0.000 (0.000) | t_small: 300 |
| `modest_40x10`: modest effect: pi_f 0.10 vs 0.05; H2 x1.2; H3 8%; H4 RR 2.5 | 300 | 0.923 (0.015) | 0.933 (0.014) | 0.207 (0.023) | 0.290 (0.026) | 0.380 (0.028) | 0.390 (0.028) | 0.000 (0.000) | conservative: 300 |

Components and the pre-review H4 estimator (same replicates). `IU3` = BCa ∧ expanded BCa ∧ jackknife-t (the rule proposed by the methods reviewer); `wild` = wild cluster restricted bootstrap-t alone; `crude W` = crude pooled RR with self-abstentions counted as errors (the estimator registered before the review), with the geometric mean of its RR estimate against the true within-stratum RR.

| Scenario | H1 IU3 | H1 wild | H4 BCa alone | H4 crude W (reject) | geo-mean RR: registered / crude W |
|---|---|---|---|---|---|
| `null_40x10` | 0.024 (0.003) | 0.025 (0.003) | 0.034 (0.004) | 0.976 (0.003) | 2.00 / 2.87 |
| `null_25x16` | 0.021 (0.003) | 0.024 (0.003) | 0.041 (0.004) | 0.920 (0.006) | 2.00 / 2.87 |
| `null_25x16_uneq` | 0.026 (0.004) | 0.025 (0.003) | 0.058 (0.005) | 0.822 (0.009) | 1.99 / 2.87 |
| `null_12x10` | 0.029 (0.004) | 0.029 (0.004) | 0.030 (0.004) | 0.570 (0.011) | 1.99 / 2.89 |
| `h3lfc_40x10` | 0.018 (0.003) | 0.021 (0.003) | 0.038 (0.004) | 0.970 (0.004) | 2.00 / 2.87 |
| `h3lfc_25x16_uneq` | 0.030 (0.004) | 0.033 (0.004) | 0.066 (0.006) | 0.845 (0.008) | 2.00 / 2.89 |
| `alt_40x10` | 1.000 (0.000) | 1.000 (0.000) | 0.887 (0.016) | 1.000 (0.000) | 2.94 / 3.62 |
| `alt_25x16` | 1.000 (0.000) | 1.000 (0.000) | 0.837 (0.021) | 1.000 (0.000) | 2.98 / 3.67 |
| `alt_25x16_uneq` | 1.000 (0.000) | 1.000 (0.000) | 0.683 (0.027) | 0.980 (0.008) | 2.92 / 3.63 |
| `alt_12x10` | 1.000 (0.000) | 1.000 (0.000) | 0.403 (0.028) | 0.930 (0.015) | 2.94 / 3.61 |
| `modest_40x10` | 0.923 (0.015) | 0.940 (0.014) | 0.450 (0.029) | 1.000 (0.000) | 2.47 / 3.25 |

Checks (size limit = 0.025 + 2·MCSE at the scenario's replicate count):

- `h1_size_registered`: PASS (null_40x10 0.0230 (limit 0.0320), null_25x16 0.0210 (limit 0.0320), null_25x16_uneq 0.0230 (limit 0.0320), null_12x10 0.0260 (limit 0.0320), h3lfc_40x10 0.0170 (limit 0.0320), h3lfc_25x16_uneq 0.0250 (limit 0.0320))
- `h1_power_registered_ge_0.95`: PASS (alt_40x10 1.000, alt_25x16 1.000, alt_25x16_uneq 1.000, alt_12x10 1.000)
- `h4_size_registered`: PASS (null_40x10 0.0185 (limit 0.0320), null_25x16 0.0260 (limit 0.0320), null_25x16_uneq 0.0235 (limit 0.0320), null_12x10 0.0305 (limit 0.0320), h3lfc_40x10 0.0255 (limit 0.0320), h3lfc_25x16_uneq 0.0280 (limit 0.0320))
- `h3_size_lfc`: PASS (h3lfc_40x10 0.0130 (limit 0.0320), h3lfc_25x16_uneq 0.0190 (limit 0.0320))
- `holm_fwer_registered`: PASS (null_40x10 0.0115 (limit 0.0320), null_25x16 0.0130 (limit 0.0320), null_25x16_uneq 0.0155 (limit 0.0320), null_12x10 0.0140 (limit 0.0320), h3lfc_40x10 0.0170 (limit 0.0320), h3lfc_25x16_uneq 0.0215 (limit 0.0320))
- `h2_size`: PASS (null_40x10 0.0260 (limit 0.0320), null_25x16 0.0260 (limit 0.0320), null_25x16_uneq 0.0200 (limit 0.0320), null_12x10 0.0160 (limit 0.0320), h3lfc_40x10 0.0215 (limit 0.0320), h3lfc_25x16_uneq 0.0250 (limit 0.0320))
- `(for comparison, not registered) h1_size_bca_only`: FAIL (null_40x10 0.0285 (limit 0.0320), null_25x16 0.0315 (limit 0.0320), null_25x16_uneq 0.0530 (limit 0.0320), null_12x10 0.0295 (limit 0.0320), h3lfc_40x10 0.0245 (limit 0.0320), h3lfc_25x16_uneq 0.0545 (limit 0.0320))
- `(for comparison, not registered) h4_size_pre_review_crude_W`: FAIL (null_40x10 0.9760 (limit 0.0320), null_25x16 0.9205 (limit 0.0320), null_25x16_uneq 0.8215 (limit 0.0320), null_12x10 0.5695 (limit 0.0320), h3lfc_40x10 0.9695 (limit 0.0320), h3lfc_25x16_uneq 0.8445 (limit 0.0320))

Run time: 764 s with 11 worker processes.

<!-- OC:END -->

## 7. Decisions settled in the registration (26 September 2026)

The points this section listed as open in the first draft are settled in `prereg/osf_preregistration.md`; the
resolution of every reviewer request is in `review/prereg/response.md`.

1. **Interval rule for H1 and H4.** Registered: `conservative`. For H1 the three bootstrap/jackknife intervals and the
   wild cluster bootstrap-t must all reject; for H4 the three intervals. BCa (the protocol's interval) stays a necessary
   condition, so the rule is never less strict than the protocol's (logged in `docs/DECISIONS.md`).
2. **H3 set and language.** Conflict atoms only, Vietnamese; no input column can widen the set.
3. **DR3 cells.** Every model × language cell must have its upper bound below 5%.
4. **H4.** Value-stating served answers, loss = labels 3–5, Mantel–Haenszel RR over model × language, guideline
   clusters; the first draft's crude pooled RR with loss W is a secondary analysis.
5. **Label 6 at A2.** A self-abstention is excluded from H4 and from the primary RQ3 population and reported as
   coverage loss.
6. **RQ3 unit.** Per open model, Vietnamese, one served answer per atom; the score is refit on the reference split of
   every regime-(b) split; the DR4 count is the number of distinct calibration atoms of the group.
7. **H2 pairs.** A pair enters only when both the EN and the VI answer are graded; the exact sign-flip test replaces
   the asymptotic Durkalski p when fewer than 20 families have a discordant pair.

## 8. References

Checked through the Crossref API on 2026-09-26 unless stated:

- Durkalski VL, Palesch YY, Lipsitz SR, Rust PF. Analysis of clustered matched-pair data. *Stat Med*
  2003;22(15):2417–28. doi:10.1002/sim.1438. The implemented statistic reproduces the published values for the
  psychiatry (χ² = 7.542) and thyroid (χ² = 2.32) examples as shipped with the CRAN package `clust.bin.pair` 0.1.2
  (test `test_durkalski_reproduces_published_examples`).
- Efron B. Better bootstrap confidence intervals. *J Am Stat Assoc* 1987;82(397):171–85.
  doi:10.1080/01621459.1987.10478410.
- Benjamini Y, Heller R. Screening for partial conjunction hypotheses. *Biometrics* 2008;64(4):1215–22.
  doi:10.1111/j.1541-0420.2007.00984.x.
- Clopper CJ, Pearson ES. The use of confidence or fiducial limits illustrated in the case of the binomial.
  *Biometrika* 1934;26(4):404–13. doi:10.1093/biomet/26.4.404.
- Cameron AC, Gelbach JB, Miller DL. Bootstrap-based improvements for inference with clustered errors. *Rev Econ
  Stat* 2008;90(3):414–27. doi:10.1162/rest.90.3.414.
- MacKinnon JG, Webb MD. Wild bootstrap inference for wildly different cluster sizes. *J Appl Econometrics*
  2017;32(2):233–54 (online 2016). doi:10.1002/jae.2508.
- Korn EL, Graubard BI. Confidence intervals for proportions with small expected number of positive counts estimated
  from survey data. *Survey Methodology* 1998, issue 2. Statistics Canada catalogue 12-001-X19980024356 (no DOI;
  catalogue page opened 2026-09-26).
- Holm S. A simple sequentially rejective multiple test procedure. *Scand J Stat* 1979;6:65 (first page). No DOI;
  details from the Crossref reference metadata of doi:10.1002/sim.3495; the first author confirms at submission.
- Learn-then-Test: Angelopoulos et al., arXiv 2110.01052 (as cited in `src/vnsoc/ltt.py`).
