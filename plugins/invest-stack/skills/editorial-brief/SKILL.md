---
name: editorial-brief
description: "Build Ped's weekly brief or any long piece as a news-site style HTML page from a content.json, with inline data-drawn charts and generated cover art, then publish it as an artifact. Use whenever a playbook says to build or publish a brief."
---

# Editorial brief

The page looks like a good news site's long read: masthead, lead story with a standfirst, the portfolio's numbers, two to four stories, a two-sided debate, actions, a calendar, and footnoted sources. The look lives in `assets/brief.css`. The structure lives in `scripts/build_brief.py`. You only write `content.json`.

## content.json

`assets/example-content.json` is the full schema with sample values (all marked as examples). Keys:

- `masthead`, `edition_label`, `tagline`, `reader`, `week_start`, `week_end` (ISO dates), `read_minutes`, `prices_as_of`.
- `cover_series`: the portfolio's daily % returns for the week. It draws the cover art, so the picture is the week's actual shape.
- `lead`: `kicker`, `headline`, `dek`, `body` (list of paragraphs).
- `portfolio`: `headline`, `stats` (label, value, note, optional `tone` sign), `figure` (kind `line`, rebased to 100 vs SPY), `holdings` (ticker, name, price, week_pct, total_pct, weight, why), `alloc_figure` (kind `alloc`).
- `stories`: kicker, tickers, headline, dek, body, optional `figure` (kind `line`, `bars` or `alloc`), `impact` (list), `exposure`.
- `debate`: question, bull, bear, verdict.
- `actions`: what, why, trigger, confidence (`high`, `mid`, `low`).
- `watchlist`: when, what.
- `sources`: title, publisher, date, url. Footnote `[^n]` in any text points to `sources[n-1]`.

Inline text supports `**bold**`, `[label](https://…)` and `[^n]`.

## Writing rules

- Headlines state the fact with a number when there is one. Sentence case. No question headlines except the debate.
- The dek says why Ped should care, in one sentence.
- Story bodies are two or three short paragraphs. The `impact` box connects the story to his weights.
- Everything in Thai per **unslop-th**.

## Images

The page loads no external images. That is deliberate. Publishers own their photos and charts, and the artifact frame blocks outside images anyway.

- Charts are drawn by `build_brief.py` from your numbers: `line` for indexed performance, `bars` for contributions or any signed comparison, `alloc` for weights vs targets.
- The cover art is generated from `cover_series`.
- For a story that needs a visual beyond these, draw an inline SVG of your own from data you have (a timeline of events, a revenue bar series from the 10-Q) and add a new figure kind to `build_brief.py` rather than pasting SVG into content.json.
- The original article's photos are one click away through `sources`. Say so in the colophon (the template already does).

## Build, look, publish

```bash
python3 skills/editorial-brief/scripts/build_brief.py work/<edition>/content.json work/<edition>/brief.html
```

Look at the page once at desktop and phone width (an artifact preview, or a headless screenshot). Fix what you see in one pass. Then publish `brief.html` with the Artifact tool as a new artifact, title `Ped Weekly <edition>`, icon `news`. For a revision of the same edition, republish the same path.

## Recommended companions

- `artifact-design` and `dataviz` skills when adding a new figure kind.
- `deep-research` skill for long research fan-outs in a deep dive.
- A financial-data connector (Financial Datasets or Bigdata.com) for prices, filings and earnings transcripts. Without one, web search per ticker.
