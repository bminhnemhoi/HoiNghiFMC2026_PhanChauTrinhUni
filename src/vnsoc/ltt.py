"""Certified selective answering for the "Whose Standard of Care?" study.

Two tools, both from the Learn-then-Test family (Angelopoulos et al., arXiv 2110.01052):

1. certified_bounds(): PRIMARY RQ3 output. For each group g and pre-specified coverage level c_k
   (thresholds fixed from a SEPARATE split), a simultaneous Clopper-Pearson upper bound U_gk on the
   selective risk P(error | answered, group g). Never empty: "at coverage c_k, risk <= U_gk".
2. ltt_thresholds(): SECONDARY output. Largest-coverage threshold per group certified to have
   selective risk <= alpha (exact binomial p-values, fixed-sequence testing, Bonferroni over groups).

Validity: calibration and deployment items exchangeable within each group; groups, scores and
thresholds fixed without looking at calibration labels. Split by ATOM (all languages/formats of an
atom on one side). Violations must be judged against the POOL risk (calibration U test) or a
superpopulation, not against the test half alone (test-half noise inflates apparent violations).
"""
import numpy as np
from scipy.stats import beta, binom


def split_by_atom(atom_ids, frac_cal=0.5, seed=0):
    """Boolean mask 'calibration' with every row of one atom on the same side."""
    atom_ids = np.asarray(atom_ids)
    uniq = np.unique(atom_ids)
    rng = np.random.default_rng(seed)
    cal_atoms = set(rng.choice(uniq, size=int(round(frac_cal * len(uniq))), replace=False).tolist())
    return np.array([a in cal_atoms for a in atom_ids])


def thresholds_from_reference(score_ref, group_ref, coverages=(1.0, 0.75, 0.5, 0.25)):
    """Per-group score thresholds giving the requested coverage on a separate reference split."""
    return {g: {c: (-np.inf if c >= 1.0 else np.quantile(score_ref[group_ref == g], 1 - c))
                for c in coverages} for g in np.unique(group_ref)}


def certified_bounds(score, error, group, thr, delta=0.10):
    """Simultaneous (over groups x coverage levels) Clopper-Pearson upper bounds."""
    K = sum(len(v) for v in thr.values())
    conf = 1 - delta / K
    out = {}
    for g, levels in thr.items():
        for c, lam in levels.items():
            ans = (group == g) & (score >= lam)
            n, k = int(ans.sum()), int(error[ans].sum())
            out[(g, c)] = dict(n=n, k=k, emp=(k / n if n else np.nan),
                               U=(beta.ppf(conf, k + 1, n - k) if 0 < n and k < n else 1.0))
    return out


def make_grids(score_ref, group_ref, start_q=0.85, n_steps=60):
    """Per-group LTT grids from a separate split, strict -> lenient (start: answer top 15%)."""
    return {g: np.quantile(score_ref[group_ref == g], np.linspace(start_q, 0.0, n_steps))
            for g in np.unique(group_ref)}


def ltt_thresholds(score, error, group, grids, alpha=0.10, delta=0.10):
    level = delta / len(grids)
    out = {}
    for g, grid in grids.items():
        s, e = score[group == g], error[group == g]
        lam_hat = np.inf
        for lam in grid:
            ans = s >= lam
            n, k = int(ans.sum()), int(e[ans].sum())
            if n == 0 or binom.cdf(k, n, alpha) > level:
                break
            lam_hat = lam
        out[g] = lam_hat
    return out


def simulate(n, rng):
    """0 = agreement group; 1 = disagreement group (conflict signal fired). Illustrative only."""
    grp = rng.choice([0, 1], n, p=[0.75, 0.25])
    s = rng.random(n)
    base = np.array([0.06, 0.30])[grp]
    err = (rng.random(n) < np.clip(base * (1.7 - 1.5 * s), 0, 1)).astype(int)
    return s, err, grp


if __name__ == "__main__":
    rng = np.random.default_rng(0)
    alpha, delta, trials = 0.10, 0.10, 300
    s_ref, _, g_ref = simulate(3000, rng)
    thr = thresholds_from_reference(s_ref, g_ref)
    grids = make_grids(s_ref, g_ref)
    cover_fail, viol_pool, viol_marg, covs, bounds = 0, 0, 0, [], None
    for _ in range(trials):
        s, e, g = simulate(4000, rng)                    # finite pool of generated questions
        idx = rng.permutation(len(s)); cal, test = idx[:2000], idx[2000:]
        b = certified_bounds(s[cal], e[cal], g[cal], thr, delta)
        # simultaneous coverage of the bounds, judged against the POOL risk
        for (gg, c), r in b.items():
            lam = thr[gg][c]; m = (g == gg) & (s >= lam)
            if m.any() and e[m].mean() > r["U"]:
                cover_fail += 1; break
        t = ltt_thresholds(s[cal], e[cal], g[cal], grids, alpha, delta)
        bad = False
        for gg, lam in t.items():
            m = (g == gg) & (s >= lam)
            if m.any() and e[m].mean() > alpha: bad = True
        viol_pool += bad
        covs.append([((g[test] == gg) & (s[test] >= t[gg])).sum() / (g[test] == gg).sum() for gg in (0, 1)])
        tm = ltt_thresholds(s[cal], e[cal], np.zeros_like(g[cal]), make_grids(s_ref, np.zeros_like(g_ref)), alpha, delta)[0]
        m1 = (g == 1) & (s >= tm)
        viol_marg += bool(m1.any() and e[m1].mean() > alpha)
        bounds = b
    print(f"CP bounds: P(some bound fails vs pool risk) = {cover_fail/trials:.3f} (target <= {delta})")
    print(f"group LTT: P(some group exceeds alpha, pool risk) = {viol_pool/trials:.3f}")
    print(f"marginal LTT: P(disagreement group exceeds alpha) = {viol_marg/trials:.3f}")
    print("mean LTT coverage (agree, disagree):", np.round(np.mean(covs, 0), 3))
    print("example certified bounds (last run):")
    for (gg, c), r in sorted(bounds.items()):
        print(f"  group {gg}, coverage {c:.2f}: n={r['n']}, empirical={r['emp']:.3f}, U={r['U']:.3f}")
