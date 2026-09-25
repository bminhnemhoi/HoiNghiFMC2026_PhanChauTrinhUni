"""Hard API budget (USD). Every paid API job MUST call reserve() before submitting and settle()
after results arrive. The ledger is state/budget_ledger.csv. Stdlib only (hooks read it).

  python -m vnsoc.budget status
  python -m vnsoc.budget check 1.25            # exit 1 if 1.25 USD more would break the cap
  python -m vnsoc.budget reserve --provider google --model X --job J --task T5.5 --est 1.2
  python -m vnsoc.budget settle --job J --actual 0.93
"""
from __future__ import annotations

import argparse
import csv
import re
import sys

from vnsoc.paths import paths

HEADER = ["timestamp", "provider", "model", "job_id", "task", "kind", "est_usd", "actual_usd", "note"]


class BudgetExceeded(RuntimeError):
    pass


def config(root=None) -> dict:
    P = paths(root)
    f = P.configs / "budget.yaml"
    cfg = {"cap_usd": 40.0, "safety_margin_usd": 2.0}
    if not f.exists():
        return cfg
    text = f.read_text(encoding="utf-8")
    try:
        import yaml

        cfg.update(yaml.safe_load(text) or {})
    except ImportError:  # system python in hooks
        for k in ("cap_usd", "safety_margin_usd"):
            m = re.search(rf"^{k}:\s*([0-9.]+)", text, re.M)
            if m:
                cfg[k] = float(m.group(1))
    return cfg


def _rows(root=None) -> list[dict]:
    P = paths(root)
    if not P.ledger.exists():
        return []
    with P.ledger.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def spent(root=None) -> float:
    jobs: dict[str, dict] = {}
    for r in _rows(root):
        j = jobs.setdefault(r["job_id"], {"est": 0.0, "actual": None})
        if r.get("est_usd"):
            j["est"] = max(j["est"], float(r["est_usd"]))
        if r.get("actual_usd"):
            j["actual"] = float(r["actual_usd"])
    return round(sum(j["actual"] if j["actual"] is not None else j["est"] for j in jobs.values()), 4)


def remaining(root=None) -> float:
    c = config(root)
    return round(float(c["cap_usd"]) - float(c["safety_margin_usd"]) - spent(root), 4)


def can_spend(est: float, root=None) -> tuple[bool, str]:
    rem = remaining(root)
    ok = est <= rem
    return ok, f"cần {est:.2f} USD, còn được dùng {rem:.2f} USD (trần {config(root)['cap_usd']} trừ dự phòng)"


def _append(root, row: dict) -> None:
    P = paths(root)
    P.ledger.parent.mkdir(parents=True, exist_ok=True)
    new = not P.ledger.exists()
    with P.ledger.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HEADER)
        if new:
            w.writeheader()
        w.writerow({k: row.get(k, "") for k in HEADER})


def reserve(provider: str, model: str, job_id: str, task: str, est: float, note: str = "", root=None) -> None:
    ok, msg = can_spend(est, root)
    if not ok:
        raise BudgetExceeded("VƯỢT NGÂN SÁCH — không gửi job. " + msg)
    from vnsoc.state import now

    _append(root, dict(timestamp=now(), provider=provider, model=model, job_id=job_id, task=task,
                       kind="reserve", est_usd=f"{est:.4f}", note=note))


def settle(job_id: str, actual: float, note: str = "", root=None) -> None:
    from vnsoc.state import now

    _append(root, dict(timestamp=now(), job_id=job_id, kind="settle", actual_usd=f"{actual:.4f}", note=note))


def estimate(n_requests: int, in_tokens: float, out_tokens: float, price_in_per_m: float,
             price_out_per_m: float, batch_discount: float = 0.5) -> float:
    """Upper-bound cost: out_tokens should be max_tokens (+ reasoning allowance)."""
    usd = n_requests * (in_tokens * price_in_per_m + out_tokens * price_out_per_m) / 1e6
    return round(usd * (1 - batch_discount), 4)


def status_line(root=None) -> str:
    c = config(root)
    return (f"Ngân sách API: đã dùng/đặt trước {spent(root):.2f} / trần {float(c['cap_usd']):.0f} USD"
            f" (còn dùng được {remaining(root):.2f} sau dự phòng)")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="budget")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status")
    s = sub.add_parser("check"); s.add_argument("est", type=float)
    s = sub.add_parser("reserve")
    for k in ("provider", "model", "job", "task"):
        s.add_argument(f"--{k}", required=True)
    s.add_argument("--est", type=float, required=True); s.add_argument("--note", default="")
    s = sub.add_parser("settle"); s.add_argument("--job", required=True)
    s.add_argument("--actual", type=float, required=True); s.add_argument("--note", default="")
    a = ap.parse_args(argv)
    if a.cmd == "status":
        print(status_line())
    elif a.cmd == "check":
        ok, msg = can_spend(a.est)
        print(("OK: " if ok else "KHÔNG ĐƯỢC: ") + msg)
        return 0 if ok else 1
    elif a.cmd == "reserve":
        try:
            reserve(a.provider, a.model, a.job, a.task, a.est, a.note)
        except BudgetExceeded as e:
            print(e, file=sys.stderr)
            return 1
        print(status_line())
    elif a.cmd == "settle":
        settle(a.job, a.actual, a.note)
        print(status_line())
    return 0


if __name__ == "__main__":
    sys.exit(main())
