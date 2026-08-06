# WWE Champions — a growth diagnosis

An independent product analysis of [WWE Champions](https://apps.apple.com/us/app/wwe-champions-wrestling-rpg/id1017432937) (Scopely), built from a firsthand new-player playthrough and a quantitative read of 2,945 public player reviews.

**[Read the presentation →](https://wwe-champions-growth.vercel.app)**  ·  **[Play the prototype →](https://wwe-champions-growth.vercel.app/prototype)**

---

## The argument

The growth opportunity on this title is an **activation and social-on-ramp** opportunity, not a monetization one.

The evidence for that sits in a single number: across 2,945 reviews, the word *"fun"* appears at essentially the same rate in 1–2★ reviews (19.2%) as in 4–5★ reviews (20.3%) — a skew of **−1.1 percentage points**. For comparison, *"love"* skews −15.0 and *"money"* skews **+26.7**.

Players who rate this game one star still call it fun. The core loop and the IP are working; what's breaking is the economy wrapped around them — which is a fixable problem, not a dying game.

## What's here

| Path | What it is |
|---|---|
| `index.html` | The presentation, in seven acts: lifecycle context → method → findings → player pain → ideas → ROI model → proposal. |
| `prototype/index.html` | Interactive prototype — the first 10 minutes of a new account, with a before/after toggle. "Before" screens are real screenshots; "after" screens are proposed. |
| `data/review-analysis.json` | Derived dataset behind the charts — word frequencies, rating divergence, theme reach, population histogram. |
| `data/roi-model.json` | The ROI model: inputs, per-idea lift assumptions, and three-scenario outputs. |

## Method

**Firsthand play.** A new account played to League 2, capturing 42 screenshots of the activation window. Every claim in the analysis cites a specific screen, and captions were re-verified against the images before publishing.

**Review corpus.** 2,945 unique reviews — 474 from the iTunes customer-review feed, 2,471 from Google Play — sampled across newest, highest/lowest-rated, and most-helpful orderings, then de-duplicated. Analysis covers word frequency, keyword-family reach, and per-rating divergence.

**Population baseline.** Google Play exposes the full rating histogram: 402,333 ratings at 4.36★ (70% five-star, 8% one-star), against 50M+ installs. Only 8.1% of raters write text, which is why the written corpus skews negative — the histogram is the honest denominator, and the corpus is quoted only for *what people say*, never *how many feel it*.

**Evidence tiers.** Every claim is tagged as verified fact, player-reported signal, or a named data gap requiring internal telemetry. The tiering is deliberate: player sentiment is treated as a hypothesis to validate against funnel and cohort data, not as measurement.

## The ROI model

Value estimates are a **transparent model, not a forecast**. A power-law retention curve is fitted through D1 and D7, integrated over 180 days to give lifetime user-days per install, multiplied by daily installs and ARPDAU. A retention lift re-fits the curve; the difference in area is the gain.

Two inputs (D1, D7) are genre benchmarks rather than measured values, and the result is highly sensitive to the fitted decay exponent — a ~3-point D7 lift moves lifetime user-days by roughly a third. That sensitivity is stated in the document rather than hidden, because it is the argument for measuring rather than modelling. Every input is in `data/roi-model.json`.

## Limitations

- The review corpus is not a representative sample, by construction. It over-weights both tails.
- Onboarding complaints are only 3% of the corpus — which is expected, since players who churn on day one don't come back to write reviews. This is exactly why the analysis calls for funnel data rather than resting on reviews.
- Retention curves, ARPDAU, drop rates and funnel conversion are all internal and unavailable. Where a number is needed and absent, the analysis names the query rather than guessing.

## Notes

Screenshots and review text are the property of their respective owners and are reproduced here for commentary and analysis. Not affiliated with or endorsed by Scopely or WWE.

Built by [Jon Martin](https://github.com/jonalexjames84).
