import numpy as np

from vnsoc.ltt import certified_bounds, ltt_thresholds, make_grids, simulate, split_by_atom, thresholds_from_reference


def test_bounds_cover_pool_risk():
    rng = np.random.default_rng(1)
    s_ref, _, g_ref = simulate(3000, rng)
    thr = thresholds_from_reference(s_ref, g_ref)
    fails = 0
    for _ in range(60):
        s, e, g = simulate(4000, rng)
        idx = rng.permutation(len(s))[:2000]
        b = certified_bounds(s[idx], e[idx], g[idx], thr, 0.10)
        for (gg, c), r in b.items():
            m = (g == gg) & (s >= thr[gg][c])
            if m.any() and e[m].mean() > r["U"]:
                fails += 1
                break
    assert fails / 60 <= 0.2


def test_ltt_returns_inf_when_nothing_certifiable():
    s = np.linspace(0, 1, 200); e = np.ones(200, dtype=int); g = np.zeros(200, dtype=int)
    grids = make_grids(s, g)
    assert ltt_thresholds(s, e, g, grids)[0] == np.inf


def test_split_by_atom_keeps_atoms_together():
    atoms = np.array(["a", "a", "b", "b", "c", "c", "d"])
    cal = split_by_atom(atoms, 0.5, seed=3)
    for a in np.unique(atoms):
        assert len(set(cal[atoms == a])) == 1
