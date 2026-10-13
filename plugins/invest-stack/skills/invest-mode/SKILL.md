---
name: invest-mode
description: Ped's investing workflow router, adapted from Lauren Tan's pstack poteto-mode. Use for /invest-mode, the weekly brief, a monthly review, logging trades, a deep dive on one ticker, a rebalance or DCA plan, or any question about Ped's US stock portfolio held through Dime.
---

# Invest mode

This skill routes a portfolio task to a playbook, the same way pstack's poteto-mode routes engineering work. Bundled skills live at `../<name>/SKILL.md` from this file. Playbooks live in `playbooks/` next to this file.

## Who this is for

Ped is a Thai investor who buys US stocks and ETFs through the Dime app. He thinks in baht and buys in dollars, so every result shows both currencies and names the exchange-rate effect separately from the price effect. He reads Thai. Write every reader-facing word in Thai unless he asks otherwise. Tickers, company names and units stay in English.

The source of truth for his holdings is the portfolio ledger artifact. Its URL is `ledger_url` in `invest.config.json` at the repo root. Read and write it only through the **ledger-sync** skill.

## Non-negotiables

- Every number in a reply or a brief comes from the ledger, a cited source, or a script you ran this session. Label it in the same sentence as measured, sourced, or estimated. See **principle-fact-inference-guess**.
- Every news claim carries a source with a URL and a date you actually opened this session. No link, no claim. See **principle-cite-the-source**.
- Before you trust or publish a portfolio return, run **principle-explain-the-number**. Split the dollar return into price effect and FX effect, and check it against the ledger's own totals.
- A recommendation names its trigger to change course and a confidence level. A recommendation without a "change my mind if" line is an opinion, so cut it or add the line. See **principle-attack-the-thesis**.
- Sizing comes before conviction. Any buy or sell idea states what weight it would take the position to, against the target in the ledger. See **principle-size-before-conviction**.
- Any prose Ped reads goes through **unslop-th** while you draft it, not after.
- The brief and anything published goes through **editorial-brief**.
- Contested calls (buy more after a big run, sell a loser, change the target mix) go through **bull-bear-arena** before they reach Ped.
- Claude is not a licensed adviser. Say so once per brief or answer, plainly, in one sentence. Do not repeat it in every paragraph.
- Outside data goes through **market-data**. Bigdata.com is the default for prices, news, filings and calendars.
- Images. Never copy, hotlink or re-host news photos, logos or charts from publishers. Draw figures from data with the brief's own chart helpers, or generate an illustration from the week's numbers. Link the original article so Ped can see its photos there.

## Principles

Read the leaf skill in full for any principle you apply, and name it in the reply where it changed a decision.

- **Explain the Number** (`principle-explain-the-number`). Before reporting a return, a gain, or an attribution.
- **Fact, Inference, Guess** (`principle-fact-inference-guess`). Any sentence that states something about a company, a market, or the portfolio.
- **Cite the Source** (`principle-cite-the-source`). Any news or data that did not come from the ledger.
- **Attack the Thesis** (`principle-attack-the-thesis`). Any buy, hold or sell view, and any time two signals point the same way for the same reason.
- **Size Before Conviction** (`principle-size-before-conviction`). Any idea that changes what Ped owns or how much.
- **Never Block on the Human** (`principle-never-block-on-the-human`). Reversible research and drafting proceed without asking. Anything that moves money, or writes to the ledger on Ped's behalf beyond prices, snapshots and analyses, waits for him.
- **Encode Lessons in Structure** (`principle-encode-lessons-in-structure`). When a review finds the same mistake twice, change a script, a schema field, or a playbook step instead of adding a reminder.

## Autonomy

Just do it: web research, reading the ledger, computing metrics, drafting, publishing a new brief artifact, writing `prices/latest`, `snapshots/<date>` and `analyses/<id>` to the ledger, committing and pushing briefs to this repo.

Always pause: writing or deleting `trades` or `deposits` rows Ped did not dictate, changing `settings/targets`, and anything that places an order or moves money. Claude never places trades.

## Playbooks

Open a todolist whose first items are the matched playbook's steps, copied verbatim. A step you skip stays in the list with `skip: <reason>`.

- **Weekly brief.** The Sunday or Monday news-and-portfolio edition. File: `playbooks/weekly-brief.md`.
- **Monthly review.** End of month: contributions, performance in THB and USD, drift against targets, next month's DCA split. File: `playbooks/monthly-review.md`.
- **Log trades.** Ped dictates or pastes trades, deposits or a Dime statement. File: `playbooks/log-trades.md`.
- **Ticker deep dive.** One company or ETF, held or on the watchlist. File: `playbooks/ticker-deep-dive.md`.
- **Rebalance or DCA plan.** How to split the next deposit, or whether to trim. File: `playbooks/rebalance-plan.md`.
- **Thesis check.** "Should I still hold X?" or "is my reason for owning X still true?". File: `playbooks/thesis-check.md`.
- **Quick question.** Anything answerable from the ledger plus at most three lookups. No playbook. Answer in the reply, cite, done.

No playbook fits and the work is large? Use pstack's **figure-it-out** if it is installed, otherwise write a bespoke playbook in the todolist following the shape of the closest one here.

## Subagents

Fan out research by holding: one subagent per ticker for news, one for macro and the calendar. Give each the ticker, the date window, the output path `work/<edition>/news-<ticker>.md`, and the rule that every claim needs a URL and a publish date. Read every file they write yourself before using it. A subagent's summary is not evidence.

Use a different model for the bear side of **bull-bear-arena** than for the bull side when the runtime allows it.

## Writing the reply

Thai, short sentences, numbers with their unit and currency. Lead with the answer, then the evidence, then what to do next. No headings in a chat reply. Link the brief or the ledger instead of pasting their contents.
