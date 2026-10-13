---
name: principle-explain-the-number
description: "Apply before you trust, report, or act on a portfolio number: a return, a gain, an attribution, a drift. Adapted from pstack's Explain the Number."
user-invocable: false
---

# Explain the Number

- **Split it.** A Thai investor's baht return is price effect plus FX effect. Report both. A week where the portfolio rose 1% in dollars and the baht strengthened 0.6% is a different week from a flat dollar rate.
- **Reconcile it.** The sum of per-ticker contributions must equal the portfolio's change within rounding. The value from `portfolio_math.py` must equal the ledger page's headline for the same prices. If they disagree, find out why before writing a word about the number.
- **List what else it could be.** A missing price that fell back to cost, a deposit counted as a gain, a dividend counted twice, a sale without its realized gain, a stale `prices/latest`, a ticker change or split. Rule each out with evidence.
- **Name the benchmark method.** Simple start-to-end percent is wrong whenever money went in during the period. Use money-weighted return for anything over a month, and say so.
- **Keep the evidence with the number.** `metrics.json` and `prices.json` stay in the work dir and are committed with the brief.

You skipped this when a return in the brief has no matching line in `metrics.json`, or the brief reports a dollar return with no baht figure next to it.
