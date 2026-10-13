# Ledger v2 design

The portfolio ledger rebuilt as a multi-portfolio tracker for any asset. Research notes behind each decision are in `docs/research/`.

## Who it is for and what they do

Ped tracks several portfolios (US stocks through Dime, Thai funds, gold, crypto, cash) and wants one THB view across all of them. No Thai tool combines these in one view today (research-investors.md, Thai market section). The jobs, in order of frequency:

1. Glance at total wealth and how each portfolio is doing.
2. Log the monthly investment.
3. Refresh values: live prices where a feed exists, a manual check-in where it does not.
4. Read what changed in the news and what Claude makes of it.
5. Create or restructure a portfolio (rare, but the first thing a new user does).

## Data model

Manual entry is kept to what every app already shows: quantity, net invested and current profit. Value is derived as net plus profit, so any asset works without a price feed (the Kubera pattern of manual values with check-ins).

| Collection | Fields |
|---|---|
| `portfolios/<id>` | `name`, `color`, `note`, `goal` (THB, optional), `order`, `createdAt` |
| `holdings/<id>` | `portfolioId`, `type` (`us_stock`, `th_stock`, `fund`, `gold`, `crypto`, `cash`, `bond`, `other`), `name`, `symbol`, `currency` (`THB`/`USD`), `qty`, `net`, `profit`, `valuedAt`, `rpId` (Bigdata.com id for live US prices) |
| `transactions/<id>` | The cost log: buy, sell or dividend with price, quantity, commission and the USD/THB rate at the time. Saving one updates the holding; deleting reverses it. See `ledger-sync` for every field. |
| `checkins/<portfolioId>_<date>` | `portfolioId`, `date`, `value`, `net` (both THB). Written whenever a portfolio's holdings change, one per portfolio per day. Charts draw from these. |
| `news/<id>` | `date`, `title`, `url`, `source`, `summary`, `symbols`, `fetchedBy` (`bigdata` or `claude-weekly`) |
| `analyses/<id>` | `date`, `kind`, `portfolioId` (optional), `title`, `summary`, `body`, `link` |
| `settings/app` | `usdthb`, `fxAsOf` |

## Screens

- **Home.** Hero with total wealth in THB, profit with sign and arrow, net invested, and a value-vs-net area chart. Allocation by asset type and by portfolio as 100% stacked bars with sorted lists (bars read better than donuts; research-design.md section 2). Portfolio cards with a colour stripe, value, profit, sparkline and top holdings. A dashed "create portfolio" card.
- **Portfolio.** Header with value, profit and net; chart; allocation; holdings table on desktop and cards on phone; live price comparison for US holdings; external links per holding; monthly buys chart and the cost log (price, quantity, commission, USD/THB at the time, baht paid).
- **News and analysis.** Feed of saved news (fetched live from Bigdata.com or written by the weekly brief), Claude's summary on demand, and the archive of analyses.
- **Empty state.** One card that says what the app does in three steps and opens the create dialog, plus a sample view.

## Interaction

- Native `<dialog>` with `showModal()`, styled as a bottom sheet under 640px.
- Number fields use `inputmode="decimal"` text inputs; profit has an explicit gain or loss toggle so phones never need a minus key.
- Validation after interaction with `:user-invalid`.
- Live preview of value and return while typing.
- Undo toast after deleting a holding or contribution. A confirm dialog naming the portfolio before deleting a portfolio.
- Saving status announced in a `role="status"` region.
- View transitions between home and a portfolio, with focus moved to the new heading.

## Visual direction

"Passbook": cool mist paper, navy ink, teal accent and a marigold highlight used only for the active state and the hero mark. Bai Jamjuree for headings, IBM Plex Sans Thai for UI, IBM Plex Sans Thai Looped for long analysis text, IBM Plex Mono for every number. Gains and losses always carry a sign and an arrow, never colour alone.

## Live data

- US stocks and ETFs: Bigdata.com through the page's connector (`bigdata_portfolio_tearsheet`), resolved once per symbol with `find_securities` and cached as `rpId`.
- News: Bigdata.com `bigdata_search`, one call per symbol, saved to `news` so it stays readable.
- Everything else: manual check-ins, or Claude's weekly run.
- External links per type: Yahoo Finance and TradingView for US stocks, SET for Thai stocks, Finnomena for funds, Bitkub and TradingView for crypto, the Gold Traders Association for gold.

## Folio (2026-10-13 revision)

- Renamed to Folio, English UI, its own mark: two stacked sheets with a rising line, in ink, teal and marigold.
- Portfolio icons: twelve built-in glyphs or an uploaded image, cropped to 128px and stored on the portfolio doc as a data URL.
- Live USD/THB, spot gold and crypto from the Bigdata.com market snapshot, refreshed every 10 minutes; the manual rate is a fallback.
- Charts view: price history from Financial Datasets when that account has credits, otherwise Folio's own daily record (`pricehist`), plus a watchlist for symbols not held.
- Invest / adjust: one dialog for a month's buys, sells and dividends across assets, each line with price, quantity, commission and the USD/THB rate the broker gave. It updates holdings and writes the cost log; deleting a line reverses it exactly.
- Display font changed to Bricolage Grotesque with IBM Plex Sans and Plex Mono; IBM Plex Sans Thai stays in the stack for Thai names.
