# Rebalance or DCA plan

How to split the next deposit, or whether to sell anything to get back to target.

## Steps

1. **Read targets and holdings.** **ledger-sync**, then `ledger_metrics.py`. Targets live in `settings/app.typeTargets` {type: percent of total wealth} and optional per-portfolio `targets` {symbol: percent}. If none are set, propose them from the current mix rounded to 5%, show them, and stop until Ped confirms; then write them.
2. **Measure drift at two levels.** First by asset type against `typeTargets`, using `by_type_thb` from `ledger_metrics.py`. Then per holding inside a portfolio against that portfolio's `targets`. Drift = weight minus target, in percentage points. Decide how much of the deposit goes to each class before splitting the stock share across tickers. Keep an emergency cash floor Ped names before counting cash as investable.
3. **Fill with new money first.** Give the deposit to the most underweight holdings until each reaches target or the money runs out (compute it in a short script from `metrics.json` and keep the script in the work dir). Dime allows fractional shares, so allocate in dollars, not whole shares.
4. **Sell only past a band.** Suggest a trim only when a holding is more than 5 points over target after the deposit, and say what the sale would realize as a gain or loss. Mention that Thai tax treatment of foreign gains depends on when money is brought back to Thailand, and that Ped should confirm his own case.
5. **Debate if it sells.** Any trim goes through **bull-bear-arena**.
6. **Reply.** A table of ticker, amount in USD and THB, resulting weight. One sentence on why.
