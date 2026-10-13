# Monthly review

End-of-month look at the whole plan rather than the week's news. Output is an `analyses` row (kind `monthly`) in the ledger and a short Thai reply. Publish an HTML edition only when Ped asks.

## Steps

1. **Read the ledger.** **ledger-sync** "Read everything".
2. **Check the month is complete.** List the month's `transactions` per portfolio (buys, fees, average USD/THB) next to the trailing 6-month average. Flag holdings whose `valuedAt` is older than the month start; their values are stale. Ask Ped to refresh them or refresh priced ones per **market-data** before computing.
3. **Compute.** `ledger_metrics.py --start <last day of previous month> --end <last day of this month>`. Report each portfolio's gain with new money taken out, total wealth, money added, progress against each portfolio's goal, and the mix by asset type.
4. **Benchmark honestly.** Compare against SPY over the same dates with the same cash flows (money-weighted), not a simple start-to-end percentage. Say which method you used.
5. **Next month's DCA split.** Run **rebalance-plan** step 3 with the average deposit as the amount.
6. **Thesis pulse.** For each holding, one line: is the reason Ped wrote in his trade notes still true this month? Anything that looks broken goes to **thesis-check** next.
7. **Write and store.** Thai, per **unslop-th**. Store through **ledger-sync** as an `analyses` row.
8. **Reply.** The month in one sentence per currency, the DCA split, and any thesis flag.
