# Portfolio dashboard UX/UI research (single-file HTML/CSS/JS, inline SVG, desktop + phone)

Researched 2026-10-13. "Unverified" marks claims I could not confirm from a fetched source. Product details marked "secondary" come from third-party teardowns or reviews, not the vendors themselves.

---

## 1. Onboarding an empty finance app

**What the research says**
- **Empty states should teach and act** (NN/g, Kate Kaplan, 2021-09-19, https://www.nngroup.com/articles/empty-state-interface-design/). They should do three things: show system status (say whether the app is loading or simply has no data, and never show "no records" while still loading), teach what the area does in context, and give a direct button to the task that fills it.
- **Progressive disclosure** (NN/g, Jakob Nielsen, 2006-12-03, https://www.nngroup.com/articles/progressive-disclosure/). Show only the frequent essentials first and keep at most 2 levels. The "more options" control should be visible and clearly labeled. Use staged, wizard-style disclosure only when the steps don't depend on each other.
- **Sensible defaults** (NN/g, Nielsen, 2005-09-25, https://www.nngroup.com/articles/the-power-of-defaults/). Pre-fill the most likely value and choose it on purpose, not alphabetically. Users treat a default as the expected answer. For this app that means base currency THB, today's date, and a "Main portfolio" name.
- **Live validation and preview** (Baymard, Edward Scott, 2024-01-09, https://baymard.com/research-articles/inline-form-validation). Validate on blur, not mid-typing. Once a field shows an error, re-check it on every keystroke so the error clears right away. Show positive confirmation (a check mark). An inline live preview of the computed result (e.g. "10 sh x $182.40 = $1,824 = about 59,800 THB") applies the same immediate-feedback idea. That preview is my extrapolation, not a Baymard finding.

**What products do**
- **Delta** (support doc, "updated over 5 months ago", https://support.delta.app/en/articles/4538243-setting-up-your-portfolio). Starts from one blank "main" portfolio. A "+" opens "Add manual transaction": asset type, ticker search, Buy/Sell, then details, with optional fields hidden under "Additional options". Delta recommends entering manual history before connecting a broker.
- **Kubera** (founder's story, undated, https://www.kubera.com/blog/story-behind-kubera). Deliberately spreadsheet-like: "list your assets ... in simple spreadsheet form" and "simple and lightweight". It started from the founder's Google Sheet. That suggests an editable table-like ledger is a valid primary UI for power users.
- **Monarch** (secondary, screensdesign teardown with 2026 screens, https://screensdesign.com/apps/monarch-budget-track-money/). An onboarding checklist with a count ("1/5") on the dashboard. Empty states each have one CTA. Bottom sheets prompt the next action. Net-worth chart with time-range tabs. Multi-step modals with a progress bar.
- **Copilot Money** (secondary, https://screensdesign.com/showcase/copilot-track-budget-money and https://freenance.io/products/copilot-money-review-2026-budgeting-app-iphone-best-design/, 2026). Lets users add accounts manually before asking for bank credentials, which builds trust. A guided tour uses dismissible tooltips. Empty states have a CTA. Its custom type and animation give it a premium, Apple-like feel.
- **Robinhood, Revolut, Apple Stocks, Sharesight onboarding:** I found no primary onboarding source. Unverified.

**Recommendations for an empty app**
1. The first screen is a single card titled "Create your first portfolio". It asks for a name (pre-filled), a base currency (THB), and "Add first holding". Nothing else.
2. While typing, a live preview line shows quantity x price, the converted value, and the resulting weight in the portfolio.
3. After the first save, the dashboard shows real (if tiny) numbers right away. Empty modules (dividends, history) teach in one line and offer one button.
4. Keep a dismissible "Getting started 1/4" checklist, Monarch-style. Pair it with a "Load sample data" option so users can explore without commitment. Sample data is a common pattern, but I found no source for it. Unverified.

---

## 2. Data display

**Hero number.** I found no single authoritative source for this pattern. My synthesis: lead with one large total, followed by the period change as an absolute value and a percentage with sign and arrow, followed by a period selector (1D/1M/YTD/1Y/All), as in Monarch's tabs. Apple's HIG chart talk (WWDC22 "Design app experiences with charts", Nicholas Felton, June 2022, https://developer.apple.com/videos/play/wwdc2022/110342/) supports two parts of this:
- Every chart gets a standalone sentence summary ("Up 4.2% this month, 1.23M THB"), and that sentence doubles as the SVG `<title>`/aria-label.
- Small charts drop gridlines and axes. When you expand a chart, keep the same shape and state.

**Sparklines** (Tufte, 2004-05-27, https://www.edwardtufte.com/notebook/sparkline-theory-and-practice-edward-tufte/). Word-sized, with no frame. Mark the last point with a dot that ties to the printed number. Optionally mark min and max, and add a grey "normal" band. Scale the aspect ratio so slopes average about 45 degrees. On holding cards: put the sparkline beside the number, never alone.

**Allocation: donut vs treemap vs bar**
- **NN/g dashboards** (Page Laubheimer, 2017-06-18, https://www.nngroup.com/articles/dashboards-preattentive/). Position and length are read most accurately; angle and area are poor. Avoid pie charts unless one slice dominates. Donuts are worse still because the hollow centre removes the angle cue.
- **Stephen Few, "Save the Pies for Dessert"** (Aug 2007, https://www.betterevaluation.org/sites/default/files/08-21-07.pdf). Use a sorted bar chart on a percentage scale, titled as a breakdown of the whole. Use a table when exact values matter.
- **Datawrapper** (Lisa Charlotte Muth, 2018-01-03, updated 2025-02-21, https://www.datawrapper.de/blog/pie-charts). A pie is acceptable only with 5 or fewer slices and shares near 25/50/75%. Switch to a stacked bar or bars beyond that, or when shares must be compared.
- **NN/g treemaps** (Laubheimer, 2019-09-29, https://www.nngroup.com/articles/treemaps/). Use only for hierarchical data with positive values. Treemaps are bad for precise comparison, negatives, items of similar size, or tracking items over time, and small tiles can't hold labels.
- **Verdict for a single-file SVG app:**
  - Default view: one 100% stacked horizontal bar (asset class or currency) above a sorted bar list of holdings with % labels.
  - A donut is acceptable as a decorative "hero" only with 5 or fewer segments and direct labels.
  - Use a treemap only for asset class > holding views with 15+ holdings.

**Gain/loss colour**
- **WCAG 1.4.1 Use of Color** (W3C, updated 2025-09-16, https://www.w3.org/WAI/WCAG21/Understanding/use-of-color.html). Colour must not be the only cue. Add text, symbols, or patterns.
- **NN/g** (2017, above). Colour has no inherent order and should reinforce shape or position, not replace it.
- **Futubull** (Android Developers story, page updated 2023-01-11, https://developer.android.com/stories/apps/futu). Built an opt-in colour-blind-safe pink/green scheme tested with CVD users. Uses hollow vs filled candles so direction doesn't need colour. Prefers blue/orange elsewhere. User-switchable in settings.
- **Regional convention** (Benzinga, 2021-10-08, https://www.benzinga.com/general/education/21/10/23258001/did-you-know-you-dont-want-to-be-in-the-green-if-youre-trading-in-china-japan-or-taiwan). Red means "up" in China, Taiwan and Japan. That Thai apps use green for up, Western-style, is unverified, so offer an "up colour" setting.
- **Rules:**
  - Always print the sign (+/−, with a real minus U+2212) and an arrow (▲/▼).
  - Use a blue/orange option or tested red/green tones that differ in lightness.
  - Never colour a treemap tile red/green alone.

**Tabular numbers.** Use `font-variant-numeric: tabular-nums` on every column, the hero, and changing numbers, so digits don't jitter and decimals align. Right-align numbers in tables. Check that the chosen Thai font's Latin digits actually support `tnum`; I did not confirm this for Thai Google Fonts. Unverified. If they don't, set numbers in IBM Plex Mono or IBM Plex Sans (both have tnum) as the numeric face.

**Currency effect.** Sharesight splits return into capital gain, dividends and currency gain (David Olsen, 2020-02-17, https://sharesight.com/blog/how-sharesight-calculates-your-investment-performance). For a THB-based investor holding USD stocks:
- Show "Price return +8.1%, FX effect −2.3%, Total +5.6%" on each holding and in the hero tooltip.
- Show both native-currency and THB values, with the FX rate and its as-of time.

---

## 3. Interaction patterns

**Native `<dialog>`** (MDN, last modified 2026-10-02, https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/dialog).
- `showModal()` gives you inert background, Esc to close, `aria-modal`, and focus moved into the dialog.
- Use `<form method="dialog">`, read `returnValue`, and add `formnovalidate` on Cancel.
- `autofocus` the most likely field.
- `closedby="any"` enables light-dismiss (check browser support; newer feature).
- Style the overlay with `::backdrop`.
- Animate with `@starting-style` plus `transition-behavior: allow-discrete`.
- Always include a visible close button.
- Baseline since March 2022.
- On phones, style the dialog as a bottom sheet: full width, anchored to the bottom, with `max-height: 90dvh`. Monarch uses bottom sheets (secondary).

**Editable table vs card forms**
- NN/g big tables on small screens (video, 2021-08-20, https://www.nngroup.com/videos/big-tables-small-screens/). Use sticky headers, let users pick a column subset, and hide or reorder columns.
- Desktop: an editable ledger table, Kubera-style, with inline edit on click or Enter.
- Phone: each row becomes a card showing name, value, and change. Tapping a card opens the same `<dialog>` form. Don't do inline cell editing on touch. This split is my synthesis.

**Numeric inputs** (GOV.UK Design System, guidance updated June 2026, https://design-system.service.gov.uk/components/text-input/).
- Avoid `type=number`, because scrolling increments the value by accident and it gives poor feedback. Use `type=text` with `inputmode="decimal"`.
- `inputmode="decimal"` can block negative input on some devices.
- Put currency prefixes outside the input and state the currency in the label, because screen readers skip prefixes. Accept typed "฿" or "$".

**Undo vs confirm**
- NN/g (Nielsen, 2018-02-18, reviewed 2026-08-07, https://www.nngroup.com/articles/confirmation-dialog/). Confirm only rare, irreversible actions. Name the object and the effect, use verb button labels ("Delete holding" / "Keep"), and never "Yes/No". Make undo the primary safety net, or soft-delete with a grace period.
- GitHub Primer (undated, https://primer.style/product/components/confirmation-dialog/guidelines). Don't confirm actions that can be undone. Frequent confirms cause fatigue.
- For this app:
  - Deleting a transaction or holding uses an undo toast for about 6–10 s (my estimate; Material's snackbar page didn't load).
  - Deleting a whole portfolio or importing over existing data uses a confirm dialog that names the item.

**Optimistic save and saved state**
- NN/g Visibility of System Status (Aurora Harley, 2018-06-03, https://www.nngroup.com/articles/visibility-system-status/). Confirm every action right away, and never change data silently.
- Show a persistent status chip: "Saving…" → "Saved 14:02" → "Not saved — Retry". Update the UI immediately and roll back with a visible error on failure.

**Keyboard and screen reader basics**
- Saved/undo messages go in a `role="status"` region (polite, `aria-atomic="true"`) that exists before the message is inserted (W3C ARIA22, updated 2026-01-12, https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA22).
- Each SVG chart gets `role="img"` and an aria-label carrying the summary sentence, plus a visually hidden data table or a "Show as table" toggle.
- Use real `<button>` and `<table>` elements, a visible `:focus-visible` ring, and give the period selector tab-style `aria-pressed`.

---

## 4. Visual direction (avoiding the generic AI-dashboard look)

**Why the generic look happens.** Models fall back on the most common training patterns, such as Tailwind indigo defaults and purple gradients on white. The fix is to give explicit constraints (palette tokens, banned fonts, a named reference aesthetic) and to ask for several directions (prg.sh, 2025-10-26, https://prg.sh/ramblings/Why-Your-AI-Keeps-Building-the-Same-Purple-Gradient-Website; author not stated on page).

**Thai type facts used below**
- **Looped vs loopless** (Typotheque, Héctor Mangas, 2025-02-15, https://www.typotheque.com/research/effects-of-loops-in-thai). Looped Thai reads slightly faster in continuous text and is rated more readable. Loopless reads as "modern" and is preferred by younger readers for short text and headlines. So: loopless for UI labels and headings, looped for longer paragraphs such as notes or a weekly brief.
- **IBM Plex Sans Thai and Plex Sans Thai Looped** (Ben Mitchell and Mark Frömberg, 2019, 7 weights each, https://www.fontpad.co.uk/?p=1772). Fontpad lists both looped and loopless styles; the Google Fonts names map loopless = "IBM Plex Sans Thai" and looped = "... Looped".
- **Anuphan** (Mint Tantisuwanna, Cadson Demak, https://fonts.google.com/specimen/Anuphan/about). A loopless version of IBM Plex Thai. Variable weight is likely but not confirmed on the page fetched. Unverified.
- **Noto Sans Thai**: loopless, variable weight 100–900 plus a width axis 62.5–100 (https://fontsource.org/fonts/noto-sans-thai/about). **Noto Serif Thai**: variable weight 100–900 plus width (https://fontsource.org/fonts/noto-serif-thai/about).
- **Chakra Petch** (Cadson Demak): square sans with tapered corners, keeps looped Thai forms, weights 300–700 plus italics, tagged "techno" (https://fontsource.org/fonts/chakra-petch/about). **Bai Jamjuree** (Cadson Demak): square, superelliptic, Eurostyle-like, weights 200–700 plus italics, "headings and small passages" (https://fontsource.org/fonts/bai-jamjuree/about).
- **Mitr** (Cadson Demak): loopless, rounded terminals, wide and friendly, weights 200–700 (https://fontsource.org/fonts/mitr/about). **Prompt** (Cadson Demak, per Wikipedia National Fonts entry): loopless geometric. Prompt's details are unverified beyond the designer.
- **Sarabun** (Suppakit Chalermlarp): based on TH Sarabun New, the Thai Government Gazette font since 2011, weights 100–800 plus italics (https://fontsource.org/fonts/sarabun/about; https://en.wikipedia.org/wiki/National_Fonts). It reads as "official document", which suits statements but feels bureaucratic as a UI face.

**Three directions**

**A. "Passbook / bank ledger"**: calm, trustworthy, print-like.
- **Concept:** A Thai savings passbook (สมุดบัญชี) meets a modern ledger.
- **Palette:** Off-white paper (not cream, a cool grey-white #F6F7F5) with deep ink navy text #14213D. One accent, teal-green #0F766E. Losses in brick #B4442F. Hairline 1px rules instead of cards with shadows.
- **Layout:** Dense ruled table and monospaced-feeling numbers. The hero number sits at the top left like a balance line.
- **Type:** IBM Plex Sans Thai (UI) + IBM Plex Sans Thai Looped (notes and long text) + IBM Plex Mono (numbers, tnum). One coherent superfamily.
- **Dark mode:** Navy-black #0E1420, ink becomes #E6E8EB.

**B. "Trading terminal, warm"**: data-dense, confident, for a power user.
- **Concept:** A Bloomberg-style terminal without the neon.
- **Palette:** Graphite #121417 background, #1B1F24 panels, amber accent #F2A900 for focus and selection. Up/down in blue #4DA3FF and orange #FF8A3D by default, with red/green as an option (CVD-safe per Futubull).
- **Layout:** Square corners (radius 2px), 1px borders, a compact 13–14px base. Sparklines in every row.
- **Type:** Chakra Petch for headings and the hero number (squared, techno, looped Thai keeps it legible), Anuphan for body and UI, IBM Plex Mono for figures.
- **Light mode:** Pale grey #F3F4F6 with the same amber.

**C. "Tropical modern / editorial"**: friendly, colourful but disciplined, best on phone.
- **Concept:** A Thai design-magazine feel with big numbers and flat colour blocks. Avoid gradients and glass.
- **Palette:** White background. Primary deep jade #00594F. Allocation categories in a flat, limited set: jade, saffron #E0A100, lotus pink #D9467A, indigo #3949AB, clay #A0522D (check contrast and run a CVD simulation). Use solid colour chips, not gradients.
- **Layout:** Large rounded cards (radius 16px) on phone and a 12-column grid on desktop. The hero number is oversized, about 44–56px.
- **Type:** Mitr (or Prompt) for headings and the hero, with Noto Sans Thai (variable; the width axis lets you condense tight table columns) for UI and body. Noto Serif Thai for the occasional editorial pull figure or the weekly-brief title. This replaces the "serif" cliché with an earned one.

**Common rules across all three**
- Colour tokens live on `:root` with light and dark variants.
- One accent colour only.
- Gain/loss always shown with sign and arrow.
- `tabular-nums` everywhere.
- No `backdrop-filter` glass, no purple, no gradient text.

---

## Not verified / gaps
- Robinhood, Revolut, Apple Stocks and Sharesight onboarding flows: no primary sources fetched. The Apple Stocks support page body didn't load.
- Material 3 snackbar/undo duration guidance: page needs JS, not read.
- Whether Thai Google Fonts (Anuphan, Mitr, Chakra Petch) ship `tnum` tabular figures.
- Thai market up/down colour convention.
- Prompt's style details. Anuphan's variable axes.
- Visualising Data "Five ways to design for red-green colour-blindness" (2019, https://visualisingdata.com/2019/08/five-ways-to-design-for-red-green-colour-blindness/) was found but could not be read (page returned garbled content).
- Kubera onboarding specifics. A third-party review (thecfoclub, updated 2026-09-25) only called it "clean, fast onboarding".
