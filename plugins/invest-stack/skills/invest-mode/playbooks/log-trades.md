# Log trades

Ped tells Claude what he holds or what he invested this month, pastes a Dime statement, or attaches a screenshot or CSV. Most of the time he will do this in the ledger page himself; this playbook is for when he hands it to Claude.

## Steps

1. **Parse.** Turn the input into ledger rows per the schema in **ledger-sync**. A snapshot of what Ped holds (a Dime Portfolio screen) becomes `holdings` rows with `qty`, `net` and `profit` in the right portfolio. Money put in this month becomes `transactions` rows (price, quantity, commission, the USD/THB rate the broker gave), each also changing its holding's `qty`, `net` and `netTHB` the way the page's Invest/adjust does. Dime shows fractional shares, prices in USD, and a THB amount with the rate it used. Keep the rate as `fxRate`. Dividends go in net of the US withholding tax shown by Dime.
2. **Show before writing.** Reply with a compact table of the rows you will write and anything you could not read. Wait for Ped's yes. This step is the Always-pause rule for `holdings` and `transactions`.
3. **Write.** Use one `batch` through **ledger-sync**.
4. **Read back.** List the collection once and confirm the counts match. Write today's `checkins` for each portfolio touched, run `ledger_metrics.py`, and tell Ped the new value of each portfolio touched.
5. **Lesson check.** If Ped wrote no reason for a buy, ask once for a one-line reason and add it to `note` when he answers. The note is what **thesis-check** tests later.
