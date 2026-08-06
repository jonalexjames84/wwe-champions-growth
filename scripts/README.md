# Scripts

How the datasets in `../data/` were produced. Both review feeds are public and
unauthenticated, so every number in the site can be re-derived independently.

## 1. Store metadata and rating histogram

```js
// npm i google-play-scraper
const g = require('google-play-scraper');
const app = await g.app({ appId: 'com.scopely.whiplash' });
// -> score, ratings, reviews, minInstalls, histogram, released, version, updated
```

```bash
curl "https://itunes.apple.com/lookup?id=1017432937&country=us"
# -> averageUserRating, userRatingCount, releaseDate, screenshotUrls
```

## 2. Review corpus (n = 2,945)

**iOS — 474 reviews.** The iTunes customer-reviews RSS feed, pages 1–5 across two
sort orders, de-duplicated on review id:

```bash
curl "https://itunes.apple.com/us/rss/customerreviews/page=${P}/id=1017432937/sortBy=${SORT}/json"
# SORT in {mostRecent, mostHelpful}; P in 1..5
```

**Android — 2,471 reviews.** `google-play-scraper`, 6 pages of 150 across three
sort orders (newest, rating, helpfulness), de-duplicated on review id.

Note this sampling deliberately over-weights both tails — it was chosen to read
*what people say*, not to estimate *how many feel it*. The population baseline is
the Play rating histogram, which is complete.

## 3. Text analysis

Tokenise on `[a-z]+`, drop tokens under 3 characters, a stop-word list, and
game-name words (`wwe`, `champions`, `game`, `player`, …). Then:

- **Frequency** — raw token counts across the corpus.
- **Divergence** — for each token, the share of 1–2★ reviews containing it minus
  the share of 4–5★ reviews containing it, in percentage points. Computed on
  review presence, not raw count, so long reviews don't dominate. This measure is
  robust to the sampling bias because it compares rates *within* each group.
- **Theme reach** — keyword families (money, fun, trust/odds, grind, social,
  complexity); a review may match several. Reported as share of reviews and the
  mean rating of matching reviews.

Output: `../data/review-analysis.json`.

## 4. ROI model

Fit `k = ln(D1/D7) / ln(7)`, integrate `D1 · d^-k` over days 1–180 for lifetime
user-days per install, multiply by daily installs for steady-state DAU, and by
ARPDAU for revenue. A retention lift re-fits the curve; the delta in area is the
gain.

D1, D7, monthly installs and ARPDAU are **assumptions**, not measurements — see
the Sources act on the site. The model is reproduced in JavaScript on the page
itself so the inputs can be edited live. Output: `../data/roi-model.json`.
