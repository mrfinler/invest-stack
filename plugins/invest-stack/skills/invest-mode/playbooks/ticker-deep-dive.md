# Ticker deep dive

One company or ETF, either held or being considered.

## Steps

1. **Frame.** Write the question in one sentence ("Is AMD a better place for the next ฿10,000 than adding to NVDA?"). A deep dive without a decision attached becomes a summary nobody acts on.
2. **Primary sources first.** `bigdata_company_tearsheet` (or `bigdata_etf_tearsheet`), then the latest 10-Q or 10-K and the last earnings call through `bigdata_search` with context "search transcripts and filings". SEC EDGAR or the IR page when Bigdata.com lacks a document. Save excerpts with section references and Bigdata.com URLs to `work/deep-<ticker>/`.
3. **Numbers that matter for this business.** Revenue growth, margins, free cash flow, share count change, valuation vs its own 5-year range and two peers. For an ETF: expense ratio, top-10 concentration, overlap with what Ped already owns (overlap matters more for him than the ETF's own merits).
4. **Overlap with the portfolio.** How much of the new idea's exposure Ped already has through VOO or other funds. Compute it, do not estimate it.
5. **Debate.** **bull-bear-arena** on the framed question.
6. **Size.** **principle-size-before-conviction**: what weight would the idea reach with one month's deposit, three months' deposits.
7. **Write.** Thai, per **unslop-th**. Store as `analyses` kind `deep`. Offer an HTML edition through **editorial-brief** if the piece is longer than a screen.
