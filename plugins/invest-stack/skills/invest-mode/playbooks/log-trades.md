# Log trades

Ped tells Claude about trades, deposits or dividends, pastes a Dime statement, or attaches a screenshot or CSV.

## Steps

1. **Parse.** Turn the input into ledger rows per the schema in **ledger-sync**. A snapshot of what Ped already holds (a Dime Portfolio screenshot, "ถือ VOO 1.25 หุ้น ต้นทุน 512") becomes `opening-<TICKER>` docs, not buys. Dime shows fractional shares, prices in USD, and a THB amount with the rate it used. Keep the rate as `fx`. Dividends go in net of the US withholding tax shown by Dime.
2. **Show before writing.** Reply with a compact table of the rows you will write and anything you could not read. Wait for Ped's yes. This step is the Always-pause rule for `trades` and `deposits`.
3. **Write.** Use one `batch` through **ledger-sync**.
4. **Read back.** List the collection once and confirm the counts match. Recompute holdings with `portfolio_math.py` and tell Ped the new position sizes for the tickers touched.
5. **Lesson check.** If Ped wrote no reason for a buy, ask once for a one-line reason and add it to `note` when he answers. The note is what **thesis-check** tests later.
