#!/usr/bin/env python3
"""Convert ledger closes/<date> docs into the price file portfolio_math.py reads.

  python3 closes_to_prices.py <closes_dir> <start YYYY-MM-DD> <end YYYY-MM-DD> > prices.json

Include the last trading day before the week as <start> so the first day's return exists.
"""
import json
import sys
from pathlib import Path

folder, start, end = sys.argv[1], sys.argv[2], sys.argv[3]
out = {"usdthb": {}, "tickers": {}, "benchmark": "SPY", "source": "Bigdata.com daily closes in the ledger"}
for f in sorted(Path(folder).glob("*.json")):
    d = json.loads(f.read_text(encoding="utf-8"))
    d = d.get("data", d)
    date = d.get("date", f.stem)
    if not (start <= date <= end):
        continue
    if d.get("usdthb"):
        out["usdthb"][date] = float(d["usdthb"])
    if d.get("alt"):
        out["alt"] = d["alt"]  # files are sorted by date, so the last day in the window wins
    for t, px in (d.get("prices") or {}).items():
        out["tickers"].setdefault(t.upper(), {"closes": {}, "source": d.get("source", "")})["closes"][date] = float(px)
if not out["tickers"]:
    sys.exit(f"ERROR: no closes between {start} and {end} in {folder}")
print(json.dumps(out, indent=2))
