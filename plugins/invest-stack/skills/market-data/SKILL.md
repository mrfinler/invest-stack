---
name: market-data
description: "Which connector or tool to use for each kind of market data in invest-stack: prices, news, filings, calendars, ETF holdings, macro. Bigdata.com is the default; Financial Datasets and web search are fallbacks. Use before any playbook step that needs outside data."
---

# Market data

Bigdata.com is the default source for finance in this workflow. Brand it exactly "Bigdata.com" with a link to https://bigdata.com in anything Ped reads. Load its tools with ToolSearch (`+Bigdata_com`) when they are deferred.

## Routing

| Need | First choice | Notes |
|---|---|---|
| Ticker to entity id | `find_securities` (one ticker per call, all in parallel) | Pick the row whose `listing_values` has the ticker on a US venue (`XNAS`, `XNYS`, `ARCX`, `BATS`, `XASE`). NVDA also lists in Bangkok as a DR (`XBKK:NVDA80`); never use that row. Cache ids in the ledger at `settings/entities.ids`. |
| Latest price, 1-day move, analyst target, news sentiment, EPS surprise | `bigdata_portfolio_tearsheet` with all held ids in one call | Works for ETFs (price only). The ledger page has a button that does this with Ped's own connector. |
| ETF facts, top 10 holdings, 5D/1M/YTD returns, dividends | `bigdata_etf_tearsheet` | Top 10 holdings feed the overlap check in **principle-size-before-conviction**. |
| Company financials, segments, estimates, ratings, earnings date | `bigdata_company_tearsheet` (`company_type` from `find_securities`'s `listing_type`) | Ask for `sections` only when a playbook needs one part. |
| News for one holding | `bigdata_search` smart mode, one ticker and one aspect per call, e.g. "NVIDIA Corp. news this week" | Keep each result's URL and timestamp for `sources`. Cite as "Source name - MMM DD, YYYY". |
| Filings and earnings calls | `bigdata_search` with context "search transcripts and filings" | Fetch the whole document with `bigdata_fetch_document` only when the excerpt is not enough. |
| Next week's calendar | `bigdata_events_calendar`: `economic_calendar` with `countries:["US"]`, `impacts:["HIGH","MEDIUM"]`, plus `corporate_calendar` with the held ids | Always pass explicit start and end dates for the week. |
| Daily closes for the weekly chart | `snapshots` written by the daily price task (see below) | Bigdata.com gives the latest price, not a history. |
| USD/THB | Bank of Thailand reference rate or a quote page via web search | Write it to `prices/latest.usdthb` and each snapshot. |
| Macro series (CPI, yields, payrolls) | Financial Datasets `get_macro_data` | Financial Datasets is connected but its account balance was $0.00 on 2026-10-13, so calls fail until Ped adds credits. Fall back to `bigdata_search` or the BLS/Treasury pages. |
| Price history for a deep dive | Financial Datasets `get_stock_prices` when it has credits, else the ETF tearsheet returns or web search | |

## Daily price task

Bigdata.com returns only the latest price. To get the daily series the weekly chart needs, a scheduled task runs Tuesday to Saturday at 06:15 Bangkok time (after the US close). Each run:

1. Reads `settings/entities.ids` and the held tickers from the ledger.
2. Calls `bigdata_portfolio_tearsheet` once for all ids plus SPY (`672082`).
3. Gets USD/THB.
4. Writes `closes/<YYYY-MM-DD>` = `{date, usdthb, prices: {TICKER: price}, source: "Bigdata.com"}` and refreshes `prices/latest`.

The weekly brief builds `prices.json` for `portfolio_math.py` from the five `closes` docs of the week.

## Saving work back to Bigdata.com

After publishing a weekly brief or a deep dive, upload the content.json text (or a markdown version) with `bigdata_upload_document` and tag it `ped-weekly` or `ped-deep`. Later `bigdata_search` calls with context "search in my private files" can then find past views, which **thesis-check** uses to see what Claude said before.
