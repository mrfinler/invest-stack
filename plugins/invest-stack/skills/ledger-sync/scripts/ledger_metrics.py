#!/usr/bin/env python3
"""Metrics for the Folio ledger (portfolios, holdings, transactions, checkins).

  python3 ledger_metrics.py --ledger work/<id>/ledger --start 2026-10-03 --end 2026-10-10 --out work/<id>/metrics.json

Values are in THB at the ledger's USD/THB rate. A holding's value is net + profit.
The period return uses checkins: change in value minus change in net invested,
divided by the value at the start (money put in during the week is not counted as gain).
"""
import argparse
import json
import sys
from datetime import date
from pathlib import Path


def load(folder):
    out = []
    p = Path(folder)
    for f in sorted(p.glob("*.json")) if p.exists() else []:
        d = json.loads(f.read_text(encoding="utf-8"))
        row = dict(d["data"]) if isinstance(d, dict) and isinstance(d.get("data"), dict) else dict(d)
        row.setdefault("id", d.get("id", f.stem) if isinstance(d, dict) else f.stem)
        out.append(row)
    return out


def num(x):
    try:
        return float(str(x).replace(",", ""))
    except (TypeError, ValueError):
        return 0.0


def at_or_before(series, day):
    last = None
    for c in series:
        if c["date"] <= day:
            last = c
        else:
            break
    return last


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ledger", required=True)
    ap.add_argument("--start", required=True)
    ap.add_argument("--end", default=date.today().isoformat())
    ap.add_argument("--out")
    a = ap.parse_args()
    L = Path(a.ledger)
    portfolios = load(L / "portfolios")
    holdings = load(L / "holdings")
    transactions = load(L / "transactions")
    checkins = load(L / "checkins")
    settings = {d["id"]: d for d in load(L / "settings")}
    fx = num(settings.get("app", {}).get("usdthb"))
    if not portfolios:
        sys.exit("ERROR: the ledger has no portfolios yet.")
    if not fx and any(h.get("currency") == "USD" for h in holdings):
        sys.exit("ERROR: settings/app.usdthb is missing; USD holdings cannot be valued in THB.")

    thb = lambda v, cur: v * fx if cur == "USD" else v
    out = {"period": {"start": a.start, "end": a.end}, "usdthb": fx, "portfolios": [], "by_type_thb": {}}
    tot_v = tot_n = 0.0
    tot_start_v = tot_start_n = tot_end_v = tot_end_n = 0.0
    for p in sorted(portfolios, key=lambda p: p.get("order", 0)):
        hs = [h for h in holdings if h.get("portfolioId") == p["id"]]
        rows = []
        for h in hs:
            v = thb(num(h.get("net")) + num(h.get("profit")), h.get("currency"))
            n = num(h.get("netTHB")) or thb(num(h.get("net")), h.get("currency")) if h.get("currency") == "USD" else num(h.get("net"))
            out["by_type_thb"][h.get("type", "other")] = out["by_type_thb"].get(h.get("type", "other"), 0) + v
            rows.append({"symbol": h.get("symbol") or h.get("name"), "type": h.get("type"), "currency": h.get("currency"),
                         "qty": num(h.get("qty")), "net": num(h.get("net")), "profit": num(h.get("profit")),
                         "value_thb": round(v), "profit_pct": round(num(h.get("profit")) / num(h.get("net")) * 100, 2) if num(h.get("net")) else None,
                         "valued_at": h.get("valuedAt"), "rpId": h.get("rpId")})
        v = sum(r["value_thb"] for r in rows)
        n = sum((num(h.get("netTHB")) or thb(num(h.get("net")), "USD")) if h.get("currency") == "USD" else num(h.get("net")) for h in hs)
        tot_v += v
        tot_n += n
        series = sorted([c for c in checkins if c.get("portfolioId") == p["id"]], key=lambda c: c["date"])
        s0, s1 = at_or_before(series, a.start), at_or_before(series, a.end)
        period = None
        if s0 and s1 and s0["date"] != s1["date"] and num(s0["value"]):
            gain = (num(s1["value"]) - num(s0["value"])) - (num(s1["net"]) - num(s0["net"]))
            period = {"from": s0["date"], "to": s1["date"], "gain_thb": round(gain), "return_pct": round(gain / num(s0["value"]) * 100, 2),
                      "added_thb": round(num(s1["net"]) - num(s0["net"]))}
            tot_start_v += num(s0["value"]); tot_start_n += num(s0["net"]); tot_end_v += num(s1["value"]); tot_end_n += num(s1["net"])
        txs = [t for t in transactions if t.get("portfolioId") == p["id"] and a.start < (t.get("date") or "") <= a.end]
        stale = [r["symbol"] for r in rows if (r["valued_at"] or "") < a.start]
        out["portfolios"].append({"id": p["id"], "name": p.get("name"), "goal_thb": p.get("goal"), "value_thb": round(v), "net_thb": round(n),
                                  "profit_thb": round(v - n), "profit_pct": round((v - n) / n * 100, 2) if n else None,
                                  "period": period, "transactions_in_period": [{k: t.get(k) for k in ("date", "kind", "holdingId", "qty", "price", "fee", "fxRate", "total", "currency", "thb", "realized")} for t in txs],
                                  "fees_thb_in_period": round(sum(num(t.get("fee")) * (num(t.get("fxRate")) or fx if t.get("currency") == "USD" else 1) for t in txs)),
                                  "stale_values": stale, "holdings": sorted(rows, key=lambda r: -r["value_thb"])})
    out["total"] = {"value_thb": round(tot_v), "net_thb": round(tot_n), "profit_thb": round(tot_v - tot_n),
                    "profit_pct": round((tot_v - tot_n) / tot_n * 100, 2) if tot_n else None}
    if tot_start_v:
        gain = (tot_end_v - tot_start_v) - (tot_end_n - tot_start_n)
        out["total"]["period_gain_thb"] = round(gain)
        out["total"]["period_return_pct"] = round(gain / tot_start_v * 100, 2)
    out["by_type_thb"] = {k: round(v) for k, v in sorted(out["by_type_thb"].items(), key=lambda kv: -kv[1])}
    js = json.dumps(out, ensure_ascii=False, indent=2)
    if a.out:
        Path(a.out).write_text(js, encoding="utf-8")
        print(f"wrote {a.out}  total ฿{tot_v:,.0f}  profit ฿{tot_v - tot_n:,.0f}")
    else:
        print(js)
    stale_all = [s for p in out["portfolios"] for s in p["stale_values"]]
    if stale_all:
        print(f"NOTE: values older than the period start for {stale_all}; refresh them before writing the brief.", file=sys.stderr)


if __name__ == "__main__":
    main()
