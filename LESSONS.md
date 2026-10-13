# Lessons

Each entry: date, what went wrong, what structure changed, commit.

- 2026-10-13. Contribution by ticker ignored positions bought mid-week, so the parts did not add up to the whole. `portfolio_math.py` now marks P&L day by day and from fill price to close, and reports `checks.reconciliation_gap_usd`.
