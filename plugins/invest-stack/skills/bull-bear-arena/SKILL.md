---
name: bull-bear-arena
description: "Run a contested investment call as a bakeoff: a bull analyst and a bear analyst argue in parallel from the same evidence, a judge on a different model scores them, and Claude writes the verdict with a kill condition. Adapted from pstack's arena. Use for /bull-bear-arena or any buy-more, trim, sell or target-change decision."
---

# Bull-bear arena

Open a todolist with one entry per phase (Frame, Fan out, Judge, Verdict) before launching anything.

## Frame

1. Write the question as a decision with an amount: "เติม NVDA อีก $150 จากเงิน DCA เดือนพฤศจิกายน หรือไม่".
2. Collect the shared evidence into `work/arena-<slug>/evidence.md`: ledger position and weight, target, the cited news items, the primary-source numbers. Both sides get the same file. Neither side may add a fact without a source URL.
3. Rubric for the judge, fixed before anyone writes:
   - Uses only evidence with sources, or labels the rest as guess.
   - Addresses the portfolio (weight, overlap, cost basis), not the stock in the abstract.
   - States what would prove it wrong.
   - Engages the other side's strongest point.

## Fan out

Spawn two subagents in one message, in the background. One argues for, one against. Use different models when the runtime allows (for example `opus` for the bull, `fable` for the bear). Each writes up to 250 words in Thai to its own file in `work/arena-<slug>/`, three reasons at most, each with a footnote into `evidence.md`.

## Judge

After both finish, spawn one read-only judge on a third model, or the model neither side used. It scores both against the rubric and names the stronger case and the single point the weaker side got right.

## Verdict

Read both cases yourself. Write the verdict in two to four Thai sentences: the call, the reason, and "เปลี่ยนใจถ้า…". If the judge disagrees with you, say so in the verdict and why. The brief's `debate` block takes the best paragraph from each side, rewritten per **unslop-th**, plus your verdict.
