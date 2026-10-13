# Lessons

Each entry: date, what went wrong, what structure changed, commit.

- 2026-10-13. Contribution by ticker ignored positions bought mid-week, so the parts did not add up to the whole. `portfolio_math.py` now marks P&L day by day and from fill price to close, and reports `checks.reconciliation_gap_usd`.
- 2026-10-13. Bigdata.com resolved TSM to TSMC's Taipei listing and returned a TWD price, which would have been read as USD. The ledger page and `ledger-sync` now accept a live price only when its currency is USD (or absent, for ETFs).
- 2026-10-13. The contribution form copied the holding's currency, so ฿5,000 into a USD stock was saved as $5,000 in a mock run. The form now defaults to THB and converts at the ledger's rate; found by the mock-runtime test before publishing.
- 2026-10-13. A buy changes cost and value by different amounts (commission), and a sell must remove average cost, not sale proceeds, from money invested. Transactions now store the exact `applied` change so a delete reverses it, and the e2e test checks buy, sell, delete and undo against hand-computed numbers.
