#!/usr/bin/env python3
"""Portfolio metrics from a ledger export and a price file.

  python3 portfolio_math.py --ledger work/<ed>/ledger --prices work/<ed>/prices.json --out work/<ed>/metrics.json
  python3 portfolio_math.py --ledger ... --prices ... --dca 300      # split $300 toward targets

Ledger dir: what `ArtifactData list --out_dir` writes, one JSON per document under
trades/, deposits/, settings/. Price file:

  {"usdthb": {"2026-10-03": 36.4, ...},
   "tickers": {"VOO": {"closes": {"2026-10-03": 570.1, ...}, "source": "https://..."}, ...},
   "benchmark": "SPY"}

The period is the first to last date that has a close for every held ticker.
Cost method is average cost, the same as the ledger page.
"""
import argparse
import json
import sys
from pathlib import Path


def load_docs(folder):
    out = []
    p = Path(folder)
    if not p.exists():
        return out
    for f in sorted(p.glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        if isinstance(d, dict) and "data" in d and isinstance(d["data"], dict):
            row = dict(d["data"]); row.setdefault("id", d.get("id", f.stem))
        else:
            row = dict(d); row.setdefault("id", f.stem)
        out.append(row)
    return out


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def positions_as_of(trades, date):
    """Average-cost positions after all trades on or before `date`."""
    pos, realized, divs = {}, 0.0, 0.0
    for t in sorted(trades, key=lambda t: t.get("date", "")):
        if t.get("date", "") > date:
            break
        k = (t.get("ticker") or "").upper()
        h = pos.setdefault(k, {"shares": 0.0, "cost": 0.0})
        typ = t.get("type")
        if typ in ("buy", "opening"):
            h["shares"] += num(t.get("shares")); h["cost"] += num(t.get("shares")) * num(t.get("price")) + num(t.get("fee"))
        elif typ == "sell" and h["shares"] > 0:
            q = min(num(t.get("shares")), h["shares"]); avg = h["cost"] / h["shares"]
            realized += q * num(t.get("price")) - num(t.get("fee")) - q * avg
            h["cost"] -= q * avg; h["shares"] -= q
            if h["shares"] < 1e-9:
                h["shares"] = h["cost"] = 0.0
        elif typ == "dividend":
            divs += num(t.get("amount", t.get("price")))
    return {k: v for k, v in pos.items() if v["shares"] > 0}, realized, divs


def flows_on(trades, date):
    """Net external cash into positions on `date` (buys minus sell proceeds), USD."""
    f = 0.0
    for t in trades:
        if t.get("date") != date:
            continue
        if t.get("type") in ("buy", "opening"):
            f += num(t.get("shares")) * num(t.get("price")) + num(t.get("fee"))
        elif t.get("type") == "sell":
            f -= num(t.get("shares")) * num(t.get("price")) - num(t.get("fee"))
    return f


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ledger", required=True)
    ap.add_argument("--prices", required=True)
    ap.add_argument("--out")
    ap.add_argument("--dca", type=float, help="USD to split toward targets")
    a = ap.parse_args()

    trades = load_docs(Path(a.ledger) / "trades")
    deposits = load_docs(Path(a.ledger) / "deposits")
    settings = {d["id"]: d for d in load_docs(Path(a.ledger) / "settings")}
    targets = {k.upper(): num(v) for k, v in (settings.get("targets", {}).get("weights") or {}).items()}
    P = json.loads(Path(a.prices).read_text(encoding="utf-8"))
    closes = {k.upper(): v["closes"] for k, v in P["tickers"].items()}
    fx = P.get("usdthb", {})
    bench = (P.get("benchmark") or "SPY").upper()

    end_pos, _, _ = positions_as_of(trades, "9999-12-31")
    held = sorted(end_pos)
    missing = [k for k in held if k not in closes]
    if missing:
        sys.exit(f"ERROR: no prices for held tickers {missing}. Add them to the price file; never fall back to cost.")
    dates = sorted(set.intersection(*[set(closes[k]) for k in held])) if held else []
    dates = [d for d in dates if d in fx] or dates
    if len(dates) < 2:
        sys.exit("ERROR: need at least two common dates with closes for every held ticker.")
    d0, d1 = dates[0], dates[-1]

    def value(date):
        pos, _, _ = positions_as_of(trades, date)
        return sum(h["shares"] * closes[k][date] for k, h in pos.items() if date in closes.get(k, {})), pos

    # chain-linked time-weighted return; flows enter at end of day
    series, idx_usd, idx_thb = [], 1.0, 1.0
    prev_v, prev_fx = None, None
    daily = []
    for d in dates:
        v, _ = value(d)
        r = fx.get(d)
        if prev_v:
            ru = (v - flows_on(trades, d)) / prev_v - 1
            idx_usd *= 1 + ru
            if r and prev_fx:
                idx_thb *= (1 + ru) * (r / prev_fx)
            daily.append(round(ru * 100, 3))
        series.append({"date": d, "value_usd": round(v, 2), "index": round(idx_usd * 100, 3)})
        prev_v, prev_fx = v, r

    bench_series = None
    if bench in closes and d0 in closes[bench]:
        b0 = closes[bench][d0]
        bench_series = [round(closes[bench][d] / b0 * 100, 3) if d in closes[bench] else None for d in dates]

    # per-ticker dollar P&L, day by day: yesterday's shares times the price move,
    # plus same-day trades marked from their fill price to the close
    pnl = {}
    for i in range(1, len(dates)):
        dp, d = dates[i - 1], dates[i]
        prev_pos, _, _ = positions_as_of(trades, dp)
        for k, h in prev_pos.items():
            if dp in closes.get(k, {}) and d in closes.get(k, {}):
                pnl[k] = pnl.get(k, 0.0) + h["shares"] * (closes[k][d] - closes[k][dp])
        for t in trades:
            k = (t.get("ticker") or "").upper()
            if t.get("date") == d and t.get("type") in ("buy", "sell", "opening") and d in closes.get(k, {}):
                q = num(t.get("shares")) * (-1 if t["type"] == "sell" else 1)
                pnl[k] = pnl.get(k, 0.0) + q * (closes[k][d] - num(t.get("price"))) - num(t.get("fee"))
    contrib = [{"ticker": k, "usd": round(v, 2),
                "pct": round((closes[k][d1] / closes[k][d0] - 1) * 100, 2) if d0 in closes[k] and d1 in closes[k] else None}
               for k, v in pnl.items()]
    contrib.sort(key=lambda c: -abs(c["usd"]))

    v1, pos1 = value(d1)
    _, realized, divs = positions_as_of(trades, d1)
    holdings = []
    for k, h in sorted(pos1.items(), key=lambda kv: -kv[1]["shares"] * closes[kv[0]][d1]):
        px = closes[k][d1]; val = h["shares"] * px
        holdings.append({"ticker": k, "shares": round(h["shares"], 6), "avg_cost": round(h["cost"] / h["shares"], 4),
                         "price": px, "value_usd": round(val, 2), "total_pct": round((val / h["cost"] - 1) * 100, 2),
                         "weight": round(val / v1 * 100, 2), "target": targets.get(k),
                         "drift_pts": round(val / v1 * 100 - targets[k], 2) if k in targets else None})
    cost = sum(h["cost"] for h in pos1.values())

    week_usd = (idx_usd - 1) * 100
    week_thb = (idx_thb - 1) * 100 if fx.get(d0) and fx.get(d1) else None
    price_change_held = sum(c["usd"] for c in contrib)
    v0, _ = value(d0)
    flows = sum(flows_on(trades, d) for d in dates[1:])
    recon_gap = (v1 - v0 - flows) - price_change_held

    out = {
        "period": {"start": d0, "end": d1, "dates": dates},
        "value_usd": round(v1, 2), "cost_usd": round(cost, 2),
        "value_thb": round(v1 * fx[d1], 0) if fx.get(d1) else None,
        "unrealized_usd": round(v1 - cost, 2), "realized_usd": round(realized, 2), "dividends_usd": round(divs, 2),
        "return_usd_pct": round(week_usd, 3),
        "return_thb_pct": round(week_thb, 3) if week_thb is not None else None,
        "fx_effect_pct": round(((1 + week_thb / 100) / (1 + week_usd / 100) - 1) * 100, 3) if week_thb is not None else None,
        "usdthb": {"start": fx.get(d0), "end": fx.get(d1)},
        "daily_returns_pct": daily,
        "series": series, "benchmark": {"ticker": bench, "index": bench_series},
        "contributions": contrib, "holdings": holdings, "targets": targets,
        "deposits_by_month": {},
        "checks": {"reconciliation_gap_usd": round(recon_gap, 2),
                   "note": "gap = (value change - flows) - sum(contributions); must be about 0, otherwise stop and find out why"},
    }
    for dpt in deposits:
        m = dpt.get("month")
        if m:
            out["deposits_by_month"][m] = round(out["deposits_by_month"].get(m, 0) + num(dpt.get("thb")), 0)
    if out["deposits_by_month"]:
        vals = list(out["deposits_by_month"].values())
        out["avg_monthly_deposit_thb"] = round(sum(vals[-6:]) / len(vals[-6:]), 0)

    if a.dca:
        cash = a.dca
        total = v1 + cash
        gaps = {h["ticker"]: max(0.0, targets.get(h["ticker"], 0) / 100 * total - h["value_usd"]) for h in holdings}
        for k in targets:
            if k not in gaps:
                gaps[k] = targets[k] / 100 * total
        need = sum(gaps.values())
        plan = {k: round(cash * g / need, 2) for k, g in gaps.items() if g > 0} if need else {}
        out["dca_plan_usd"] = plan

    js = json.dumps(out, ensure_ascii=False, indent=2)
    if a.out:
        Path(a.out).write_text(js, encoding="utf-8")
    print(js if not a.out else f"wrote {a.out}  value ${v1:,.2f}  return {week_usd:+.2f}% USD"
          + (f" / {week_thb:+.2f}% THB" if week_thb is not None else "") + f"  recon gap ${recon_gap:.2f}")


if __name__ == "__main__":
    main()
