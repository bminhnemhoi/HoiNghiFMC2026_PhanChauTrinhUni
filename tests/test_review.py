from vnsoc.review import PANEL, aggregate

TPL = """```yaml
reviewer: {n}
milestone: M1
recommendation: {rec}
scores: {{importance: {s}, novelty: {s}, rigor: {s}, feasibility: {s}, q1_likelihood: {s}, fit: {s}}}
fatal_flaws: {fatal}
required_changes:
  - {{id: 1, severity: major, where: "atoms", what: "fix", acceptance: "test"}}
```
Nhận xét.
"""


def write(proj, s=8, rec="minor", fatal="[]"):
    d = proj / "review" / "M1"
    d.mkdir(parents=True, exist_ok=True)
    for n in PANEL:
        (d / f"{n}.md").write_text(TPL.format(n=n, s=s, rec=rec, fatal=fatal), encoding="utf-8")


def test_pass_and_fail(proj):
    write(proj, 8)
    ok, _ = aggregate("M1", proj)
    assert ok and "ĐẠT" in (proj / "review" / "M1" / "summary.md").read_text()
    write(proj, 6)
    assert not aggregate("M1", proj)[0]
    write(proj, 9, fatal='["circular grading"]')
    assert not aggregate("M1", proj)[0]


def test_missing_report(proj):
    write(proj, 8)
    (proj / "review" / "M1" / "rev-novelty.md").unlink()
    ok, msg = aggregate("M1", proj)
    assert not ok and "rev-novelty" in msg
