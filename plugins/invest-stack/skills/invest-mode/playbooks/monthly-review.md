# Monthly review

End-of-month look at the whole plan rather than the week's news. Output is an `analyses` row (kind `monthly`) in the ledger and a short Thai reply. Publish an HTML edition only when Ped asks.

## Steps

1. **Read the ledger.** **ledger-sync** "Read everything".
2. **Check the month is complete.** Compare deposits and buy trades for the month. If money went in but no buy is logged, or a buy has no matching deposit, list the gap and ask Ped before computing anything that depends on it.
3. **Compute.** `portfolio_math.py --month YYYY-MM`. Report month return in USD and THB, split into price and FX effect, contributions vs the trailing 6-month average, realized gains and dividends, and drift against targets.
4. **Benchmark honestly.** Compare against SPY over the same dates with the same cash flows (money-weighted), not a simple start-to-end percentage. Say which method you used.
5. **Next month's DCA split.** Run **rebalance-plan** step 3 with the average deposit as the amount.
6. **Thesis pulse.** For each holding, one line: is the reason Ped wrote in his trade notes still true this month? Anything that looks broken goes to **thesis-check** next.
7. **Write and store.** Thai, per **unslop-th**. Store through **ledger-sync** as an `analyses` row.
8. **Reply.** The month in one sentence per currency, the DCA split, and any thesis flag.
