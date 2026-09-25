import pytest

from vnsoc import budget, numbers
from vnsoc.paths import paths


def test_budget(proj):
    assert budget.remaining(proj) == pytest.approx(38)
    budget.reserve("google", "m", "j1", "T5.5", 10, root=proj)
    budget.settle("j1", 3.2, root=proj)
    assert budget.spent(proj) == pytest.approx(3.2)
    with pytest.raises(budget.BudgetExceeded):
        budget.reserve("google", "m", "j2", "T5.5", 35, root=proj)
    assert budget.estimate(1000, 300, 128, 0.25, 1.5) == pytest.approx(0.1335)


def test_numbers(proj):
    P = paths(proj)
    (proj / "src" / "analysis_demo.py").write_text("x")
    import json
    P.results.mkdir(exist_ok=True)
    P.numbers.write_text(json.dumps({"h1.delta": {"value": 0.21, "display": "21,0%", "source": "src/analysis_demo.py"}}))
    P.manuscript.mkdir(exist_ok=True)
    (P.manuscript / "main.md").write_text(
        "# 1 Results\n\nIn 2026, H1 held: Δ = {{h1.delta}} at α = {{=0.05}} (Table 2) [3].\nModel Qwen3-8B on T4.\n")
    assert numbers.verify(proj) == 0
    (P.manuscript / "main.md").write_text("Δ was 21% and {{h9.missing}}\n")
    assert numbers.verify(proj) == 1
    assert numbers.bare_numbers("accuracy 87.5% in 400 atoms") == ["87.5%", "400"]
    (P.manuscript / "main.md").write_text("Design: 25–35 guidelines ({{=25–35}}), α = {{=0,10}}; bogus {{=0,37}}\n")
    assert numbers.verify(proj) == 1                               # 0,37 is not a configured constant
    (P.manuscript / "main.md").write_text("Design: {{=25–35}} guidelines, α = {{=0,10}}\n")
    assert numbers.verify(proj) == 0
    (P.manuscript / "fmc").mkdir()
    (P.manuscript / "fmc" / "abs.md").write_text("Δ = {{h1.delta}}\n")
    assert numbers.render(proj) == 0
    assert (P.manuscript / "build" / "fmc" / "abs.md").read_text() == "Δ = 21,0%\n"


def test_put_only_from_analysis_code(proj):
    with pytest.raises(ValueError):
        numbers.put("x", 1, "1", root=proj)
