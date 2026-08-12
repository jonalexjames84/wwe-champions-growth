# Repointing the growth case at first-purchase conversion

Date: 2026-08-06
Status: approved, in build
Amended: 2026-08-08 — see "Correction" at the foot of this document

## Why this rewrite exists

The case at `/case` argues that retention is the constrained KPI and revenue should be
protected but not touched. Five bets hang off that thesis. Two problems:

1. **It reads as scattered.** Five bets ranked against each other is a menu, not a
   recommendation. A reader finishes the page knowing the options, not the decision.
2. **The thesis fights the stated goal.** The goal is ARPDAU. Retention grows DAU — the
   *denominator*. The two lead bets add retained users who are overwhelmingly non-payers,
   so they grow revenue while being ARPDAU-neutral at best.

The fix is a re-pointing of the whole spine, not a new act bolted on. Three of the five
existing bets are already on the first-purchase causal chain; they are labelled as
retention plays and ranked against the wrong metric.

## The thesis

```
ARPDAU = (payers ÷ DAU) × ARPPU
            ↑ untouched      ↑ at ceiling, defended
```

On a 9.5-year-old title, ARPPU is at its ceiling and further extraction costs goodwill
(this argument survives from the existing case unchanged). Payer rate is the only variable
left, and payer rate is decided in a player's first week — the week the game currently
spends showing them a $99.99 offer.

The ordering principle:

> **Converting a non-payer buys you retention. Retaining a non-payer does not buy you a
> payer.**

That asymmetry is why first-purchase conversion outranks the retention bets *even on
retention grounds*, and it is the honest form of the D7/D30 downstream effect. It is
correlational until matched on session count — that becomes data pull 3.

## The cohort: the early-game spender, at three moments

| | Who | What blocks them |
|---|---|---|
| **P0→P1** | 2–5 sessions in, has a roster, has hit a wall | no offer at their price; first ask is a loss-tax; odds opaque |
| **P1→P2** | bought once — highest-propensity group in the game | ladder jumps from entry to $99.99; nothing built for them |
| **P2→P3** | bought twice, low LTV | habit forms here or they lapse back to F2P |

The whale / mid-game staller / lapsed rejections carry over unchanged. Only "the new
installer" is revised — it is *underspecified*, not wrong. Retaining installs grows the
denominator; the early-game spender is the subset where the money is.

## The evidence, re-sorted by what blocks a purchase

The corpus does not change. The sort key does — from "which KPI does this threaten" to
"where in the purchase path does this stop someone."

| Theme | Reach · rating | Reads as |
|---|---|---|
| Money & spending | 36% · 2.41★ | high intent, no rung at their price |
| Bugs & support | 20% · 2.42★ | blocks the **second** purchase — you don't buy twice from a shop that lost your order |
| Progress & grind | 14% · 2.42★ | ambivalent — the wall *is* the purchase trigger |
| Trust & odds | 9% · **2.06★** | the first purchase is a bet, not a purchase |
| Complexity | 3% · 2.37★ | blocks reaching the purchase moment at all |
| Fun & affection | 50% · 3.79★ | the asset — demand exists |

The "fun" finding gets stronger under this thesis, not weaker: the loop is loved, the
*transaction* is hated.

Structural-silence caveat sharpens: day-one churners don't write reviews, **and** non-payers
who bounced off the store don't either. The cohort is doubly silent. That is the argument
for the funnel pull, not a hole in the argument.

## The program: "The First Dollar" — three sequenced moves

**01 · Earn the ask.** No monetization surface before a win. Kill rescue-for-100-cash as
the first-ever offer; the first match cannot be lost. The first offer arrives after a win
and is aspirational. (≈ the old "Debut", re-pointed from retention to the purchase path.)
6–8 wks, 1 pod.

**02 · Build the rung.** *Load-bearing, and genuinely new.* A three-rung starter ladder at
the market entry point. Each rung **deterministic** — the player sees exactly what they
get — and tied to a superstar they have already used. Once per account, time-boxed, no
content overlap with whale SKUs. Rung 1 at the first wall, rung 2 within 72h, rung 3 gated
on rung 2. 6–8 wks, 1 pod + economy.

**03 · Make it safe to buy.** Published odds; dupe→shard conversion. Re-scoped to the
entry band only, so it touches **no existing gacha drop rate** — which flips it from "high
risk to the economy" to low. The published-odds half is largely config and can ship in
phase 1. 4–6 wks, economy.

**Why in this order — each necessary, none sufficient:**

- 02 without 01 → a great offer in front of someone who hasn't won yet.
- 02 without 03 → converts once, never twice.
- 01 + 03 without 02 → clean shop, nothing on the shelf at their price.

**Parked, and why.** Rookie Crew → D30 follow-on once a payer base exists; still blocked on
the faction pull. Catch-up track → blocked on faucet data, and it is a denominator play.
Win-back → after 02 ships, so returners land on a real ladder. Whale extraction → rejected.

## The model

Rebuilt as a payer funnel. Replaces the retention-curve model as the headline; the
retention curve is retained to compute the downstream D7/D30 line.

### Baseline reconciliation (a correction to the existing model)

`roi-model.json` sets `arpdau: 0.22` and `base_dau: 37,395`, giving $247k/mo against a
stated `rev_mo` of $800,000. These reconcile only if `base_dau` is **DAU attributable to
new installs** (90,000 × 12.5 user-days ÷ 30 = 37,500 ✓), not total DAU. Therefore:

- Total DAU = 800,000 ÷ (0.22 × 30) = **121,212**
- Legacy base = 121,212 − 37,395 = **83,817**

This was ignorable when the metric was retention. It is load-bearing now, because ARPDAU is
measured against **total** DAU.

### Funnel layer

| Input | Value | Status |
|---|---|---|
| Monthly installs | 90,000 | estimate (carried over) |
| D1 / D7 | 35% / 16% | genre benchmark (carried over) |
| ARPDAU | $0.22 | estimate (carried over) |
| Total DAU | 121,212 | derived |
| Daily payer rate | 3.0% of DAU | benchmark — **named gap** |
| Ever-pay conversion | 2.0% of installs | benchmark — **named gap** |
| 180-day value, existing converter | $62 | modelled — **named gap** |
| 180-day value, *marginal* converter | $21 | modelled — the entry-band convert is worth far less |
| Second-purchase rate (30d) | 35% | benchmark — **named gap** |

The marginal-vs-existing converter split matters and must not be glossed: adding a cheap
rung raises conversion **and lowers average first-purchase value**. Modelling added payers
at the existing payer's value would be dishonest.

### Lifts (base case)

Ever-pay conversion 2.0% → 3.0% (+1.0pp, +50% relative), attributed 01 = 0.25pp,
02 = 0.55pp, 03 = 0.20pp. Repeat rate 35% → 42% from move 03, haircut to 60% strength on
existing high-value payers.

### Outputs (base case)

| Component | $/yr |
|---|---|
| A · added payers (900/mo × $21) | 226,800 |
| B · repeat-rate lift on existing new payers | 97,200 |
| C · downstream retention from payer-mix shift | 28,500 |
| **Total** | **~352,500** |

Band: **$110k (low) / $353k (base) / $1.01M (high)**.

ΔARPDAU base: revenue +$29,375/mo, DAU +900 →
829,375 ÷ (122,112 × 30) = $0.2264 vs $0.2200 baseline = **+0.64¢, +2.9%**.

### The comparison table (the centrepiece)

| Portfolio | Δ rev/yr | Δ ARPDAU as the old model computes it | Δ ARPDAU if added users convert at half the average rate |
|---|---|---|---|
| Retention (Debut + Rookie Crew) | +$1.34M | **$0.0000 — neutral by construction** | **−$0.0133 (−6.0%)** |
| The First Dollar (01+02+03) | +$0.35M | **+$0.0064 (+2.9%)** | **+$0.0064 — unchanged** |

The retention portfolio is ARPDAU-neutral *by construction*: the model multiplies added
user-days by the **average** ARPDAU. But the users those bets add are marginal survivors in
the activation window, who convert to payer well below average. Correct for that and it
turns negative.

The First Dollar figure is robust to the same correction, because its gain comes from the
numerator rather than from added user-days.

**Stated openly on the page:** the ARPDAU-correct programme shows a *smaller absolute dollar
figure* than the retention portfolio's $2.99M. That is the point, not a weakness. A bigger
revenue number earned by adding non-payers is the wrong trade when ARPDAU is the metric.

## What ships Monday — 4 pulls (down from 6)

1. **Payer funnel by session index** — install → session 1…7 → first store impression →
   first purchase. Where, when, at what price does a first purchase happen today?
   *Confirms or kills the programme.*
2. **Price-point distribution of first purchases, and the visible early SKU ladder.** Is
   there anything under $10 a new player can see?
3. **D7/D30 for payers vs non-payers, matched on session count.** The matching is what makes
   it causal rather than selection.
4. **Second-purchase rate and time-to-second** for first-time payers.

**Kill criterion, stated up front:** if pull 2 shows a sub-$10 SKU already visible early and
pull 1 shows conversion at or above benchmark, move 02 is wrong and this collapses back to a
retention case.

**Build order.** Phase 0 pulls (wk 1–2) → Phase 1 move 01 + published odds (wk 3–8) →
Phase 2 move 02, the rung ladder (wk 5–12) → Phase 3 the parked list.

## What I'd want to be wrong about

- **That there is no sub-$10 SKU visible early.** The entire case rests on one store shelf,
  on one account, at League 2. Shelves are commonly geo- and cohort-tested. Pull 2 settles
  it. Naming this is better than having someone else find it.
- **That payer retention is causal rather than selection.** Pull 3.
- **That a cheap rung doesn't cannibalise the whale ladder.** Guardrail: once per account,
  time-boxed, no content overlap with whale SKUs; **top-decile ARPPU is a kill metric on
  move 02.**

## Scope of the change

| File | Change |
|---|---|
| `case/index.html` | Full rewrite of the CIRCLES spine around the new thesis |
| `index.html` | Realign the answer spine, the ideas act, the ROI act + its JS model, the proposal act, the specs |
| `data/roi-model.json` | Rebuild as a payer-funnel model |
| `scripts/build-model.py` | New — generates the model JSON so the numbers are reproducible |
| `README.md` | Realign the argument summary and the model description |

Prototype (`prototype/index.html`) is out of scope for this pass. Its "after" flow ends at
the day-two return; under this thesis it should eventually carry the first-purchase moment.


---

## Correction — 2026-08-08

Found while rebuilding the prototype, by re-reading the source screenshot this case rests on.

**What was wrong.** The case stated that the League 2 featured shelf held *exactly one offer, at
$99.99*, and that the entry price band was empty. `IMG_0821` also shows a **2-Star Gold Andre Starter
Pack at $14.99**, marked "One Time Offer", on a **05h 42m countdown**, beneath the $99.99 League
Essentials pack.

**What follows from it.**

- The floor is **$14.99**, not $99.99. The gap move 02 fills is $0–$14.99.
- Move 02 adds two rungs beneath an existing pack rather than building a ladder from nothing, so its
  modelled lift drops from **+0.55pp to +0.35pp**. Moves 01 and 03 are unaffected.
- Programme base case falls from $418k to **$366,673/yr**, and ARPDAU from +2.7% to **+2.2%**.
  Combined lift is now +0.80pp (+40% relative), down from +1.00pp (+50%).
- Move 02 becomes the **smallest of the three by value** while remaining the one the other two depend
  on. Both facts are stated on the page rather than reconciled away.
- The existing $14.99 pack becomes the **handoff** at the top of the entry ladder, and its six-hour
  countdown is removed — a clock on a stranger's first purchase is pressure, which is what move 03
  exists to take out.

**What survives, and is better sourced than the claim it replaces.** Nothing sits between free and
$14.99 — three to five times the conventional entry price for the genre — and the cheapest way into the
game is sold against a six-hour timer.

**Kill criterion.** Unchanged and technically survived, since $14.99 is not sub-$10. That is stated
explicitly on the page rather than left to look like a dodge; pull 2 answers it properly.

### Two further caption errors, same pass

- `IMG_0829` was captioned as an "Insufficient Currency" dead-end. It is the **Manager's League
  rewards screen** — a subscription SIGN UP and a padlocked Premium column shown to a player on 0
  reward points. (The deck's separate "padlocked Premium column at zero points" line was already
  accurate to this image.)
- `IMG_0841` was said to expose Boss Breakers, Link & Gear and crit stats. Those appear on the
  **Trainer panel** (`IMG_0818`). The match screen shows a padlocked AUTO, an X2, an unexplained 0/3
  counter and uninstructed move slots — still a "too much unexplained UI" point, but not the one
  claimed. The "rescue for 100 cash" prompt is `IMG_0844`, which is not in `prototype/shots/`.

### Prototype direction change, same pass

Rebuilt as **low-fidelity wireframes** rather than game-skinned high-fidelity screens. Before views stay
real screenshots, shown whole rather than cropped — a crop had been hiding the very $14.99 pack the
correction is about. Annotation pins now anchor to elements via `data-pin` instead of hard-coded pixel
offsets, which is what let them drift onto the text when the screens changed.
