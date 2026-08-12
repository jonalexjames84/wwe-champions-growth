#!/usr/bin/env python3
"""Builds data/roi-model.json — the payer-funnel model behind the case.

The headline metric is ARPDAU, so the model is written as ARPDAU = (payers/DAU) x ARPPU
and the moves act on the payer-rate factor. A retention curve is still fitted, but only
to compute (a) the DAU denominator and (b) the downstream retention line — not the
headline number.

Run: python3 scripts/build-model.py
"""
import json
import math
import pathlib

HORIZON = 180

# ---------------------------------------------------------------- inputs
I = {
    # carried over from the original model, all still estimates
    "installs_mo": 90000,
    "d1": 0.35,
    "d7": 0.16,
    "arpdau": 0.22,
    "rev_mo": 800000,
    "horizon": HORIZON,

    # the payer-funnel layer — every one of these is a named gap
    "payer_rate_dau": 0.030,      # paying DAU / total DAU
    "ever_pay": 0.020,            # share of installs that ever make a purchase
    "ltv180_existing": 62.00,     # 180-day value of a converter under today's ladder
    "ltv180_marginal": 21.00,     # 180-day value of an *added*, entry-band converter
    "repeat30": 0.35,             # second purchase within 30 days, first-time payers
    "repeat_haircut": 0.60,       # how much of a repeat lift lands on existing payers
    "payer_extra_userdays": 12.0, # extra 180-day user-days for a converted payer

    # marginal retained users in the activation window do not monetise at the average.
    # applied symmetrically to both portfolios in the comparison.
    "marginal_arpdau_factor": 0.50,
}

# scenario-varying funnel assumptions
SC = {
    "low":  {"ltv180_marginal": 14.0},
    "base": {"ltv180_marginal": 21.0},
    "high": {"ltv180_marginal": 34.0},
}

# ---------------------------------------------------------------- the programme
# conv = added ever-pay conversion, in percentage points of installs
# repeat = added second-purchase rate, in percentage points
# d1/d7 = non-payer retention side-effect, in percentage points (move 01 only)
MOVES = [
    {
        "id": 1, "name": "Earn the ask",
        "sub": "no monetisation surface before a win",
        "effort": "6-8 wks · 1 pod",
        "low":  {"conv": 0.0010, "repeat": 0.0, "d1": 0.01, "d7": 0.004},
        "base": {"conv": 0.0025, "repeat": 0.0, "d1": 0.02, "d7": 0.008},
        "high": {"conv": 0.0055, "repeat": 0.0, "d1": 0.03, "d7": 0.012},
    },
    {
        # Lift cut from 0.55pp base after re-reading IMG_0821: a $14.99 starter pack
        # already exists on the League 2 shelf, so this adds two rungs BELOW an
        # existing floor rather than creating the ladder from nothing.
        "id": 2, "name": "Build the rung",
        "sub": "two deterministic rungs below the existing $14.99 floor",
        "effort": "5-7 wks · 1 pod + economy",
        "low":  {"conv": 0.0014, "repeat": 0.0, "d1": 0, "d7": 0},
        "base": {"conv": 0.0035, "repeat": 0.0, "d1": 0, "d7": 0},
        "high": {"conv": 0.0070, "repeat": 0.0, "d1": 0, "d7": 0},
    },
    {
        "id": 3, "name": "Make it safe to buy",
        "sub": "published odds + dupe-to-shard, entry band only",
        "effort": "4-6 wks · economy",
        "low":  {"conv": 0.0008, "repeat": 0.03, "d1": 0, "d7": 0},
        "base": {"conv": 0.0020, "repeat": 0.07, "d1": 0, "d7": 0},
        "high": {"conv": 0.0035, "repeat": 0.14, "d1": 0, "d7": 0},
    },
]

# the two lead bets of the previous, retention-first portfolio — kept so the case can
# show what they do to ARPDAU. dau deltas are the originals.
OLD_RETENTION_LEADS = {"name": "Debut + Rookie Crew", "d_dau": 2804 + 13939}


# ---------------------------------------------------------------- helpers
def area(d1, k):
    """Lifetime user-days per install: the integral of d1 * t^-k from 1 to HORIZON."""
    return d1 * (HORIZON ** (1 - k) - 1) / (1 - k)


def fit(d1, d7):
    return math.log(d1 / d7) / math.log(7)


# ---------------------------------------------------------------- baseline
k = fit(I["d1"], I["d7"])
user_days = area(I["d1"], k)
dau_new = I["installs_mo"] / 30 * user_days
dau_total = I["rev_mo"] / (I["arpdau"] * 30)
dau_legacy = dau_total - dau_new

payers_mo = I["installs_mo"] * I["ever_pay"]
arppu_day = I["arpdau"] / I["payer_rate_dau"]
purchases_base = 1 / (1 - I["repeat30"])

BASE = {
    "k": round(k, 4),
    "user_days": round(user_days, 2),
    "dau_new_installs": round(dau_new),
    "dau_total": round(dau_total),
    "dau_legacy": round(dau_legacy),
    "arppu_per_paying_dau_day": round(arppu_day, 2),
    "new_payers_mo": round(payers_mo),
    "purchases_per_new_payer_180d": round(purchases_base, 3),
    "new_payer_value_mo": round(payers_mo * I["ltv180_existing"]),
}


def evaluate(move, sc):
    """Annualised incremental revenue and DAU for one move under one scenario."""
    m = move[sc]
    ltv_marginal = SC[sc]["ltv180_marginal"]

    added_payers_mo = I["installs_mo"] * m["conv"]

    # A — the added payers themselves, at the entry-band value not the incumbent value
    a = added_payers_mo * ltv_marginal * 12

    # B — repeat-rate lift, applied to the existing new-payer cohort with a haircut
    b = 0.0
    if m["repeat"]:
        p_new = 1 / (1 - (I["repeat30"] + m["repeat"]))
        uplift = p_new / purchases_base - 1
        b = payers_mo * I["ltv180_existing"] * uplift * I["repeat_haircut"] * 12

    # C — downstream retention from the payer-mix shift. counted at full ARPDAU because
    # a converted payer monetises at or above the average, unlike a marginal survivor.
    dau_from_payers = added_payers_mo * I["payer_extra_userdays"] / 30
    c = dau_from_payers * I["arpdau"] * 365

    # D — the non-payer retention side-effect of move 01, counted at the marginal rate
    d = 0.0
    dau_from_retention = 0.0
    if m["d1"]:
        nk = fit(I["d1"] + m["d1"], I["d7"] + m["d7"])
        dau_from_retention = I["installs_mo"] / 30 * (area(I["d1"] + m["d1"], nk) - user_days)
        d = dau_from_retention * I["arpdau"] * I["marginal_arpdau_factor"] * 365

    return {
        "added_payers_mo": round(added_payers_mo),
        "conv_pp": round(m["conv"] * 100, 2),
        "added_payer_rev": round(a),
        "repeat_rev": round(b),
        "payer_retention_rev": round(c),
        "nonpayer_retention_rev": round(d),
        "rev": round(a + b + c + d),
        "d_dau": round(dau_from_payers + dau_from_retention),
    }


def arpdau_after(d_rev_yr, d_dau):
    return (I["rev_mo"] + d_rev_yr / 12) / ((dau_total + d_dau) * 30)


# ---------------------------------------------------------------- run
moves_out, totals = [], {}
for sc in ("low", "base", "high"):
    totals[sc] = {"rev": 0, "d_dau": 0, "conv_pp": 0.0}

for mv in MOVES:
    row = {"id": mv["id"], "name": mv["name"], "sub": mv["sub"], "effort": mv["effort"], "sc": {}}
    for sc in ("low", "base", "high"):
        r = evaluate(mv, sc)
        row["sc"][sc] = r
        totals[sc]["rev"] += r["rev"]
        totals[sc]["d_dau"] += r["d_dau"]
        totals[sc]["conv_pp"] += r["conv_pp"]
    moves_out.append(row)

arpdau_base = I["arpdau"]
for sc in ("low", "base", "high"):
    t = totals[sc]
    new_arpdau = arpdau_after(t["rev"], t["d_dau"])
    t["ever_pay_after"] = round(I["ever_pay"] * 100 + t["conv_pp"], 2)
    t["arpdau_after"] = round(new_arpdau, 5)
    t["d_arpdau"] = round(new_arpdau - arpdau_base, 5)
    t["d_arpdau_pct"] = round((new_arpdau / arpdau_base - 1) * 100, 2)
    t["conv_pp"] = round(t["conv_pp"], 2)

# the comparison: what the retention-first portfolio does to ARPDAU, under the model's
# own convention and under the corrected marginal-monetisation convention.
def retention_portfolio(factor):
    d_dau = OLD_RETENTION_LEADS["d_dau"]
    rev = d_dau * I["arpdau"] * factor * 365
    new_arpdau = arpdau_after(rev, d_dau)
    return {
        "d_dau": d_dau,
        "rev": round(rev),
        "arpdau_after": round(new_arpdau, 5),
        "d_arpdau": round(new_arpdau - arpdau_base, 5),
        "d_arpdau_pct": round((new_arpdau / arpdau_base - 1) * 100, 2),
    }


def programme_at(factor):
    """The programme re-scored with marginal retained users at `factor` x ARPDAU."""
    rev = d_dau = 0
    for mv in MOVES:
        m = mv["base"]
        added = I["installs_mo"] * m["conv"]
        a = added * SC["base"]["ltv180_marginal"] * 12
        b = 0.0
        if m["repeat"]:
            p_new = 1 / (1 - (I["repeat30"] + m["repeat"]))
            b = payers_mo * I["ltv180_existing"] * (p_new / purchases_base - 1) * I["repeat_haircut"] * 12
        dp = added * I["payer_extra_userdays"] / 30
        c = dp * I["arpdau"] * 365
        dr = 0.0
        if m["d1"]:
            nk = fit(I["d1"] + m["d1"], I["d7"] + m["d7"])
            dr = I["installs_mo"] / 30 * (area(I["d1"] + m["d1"], nk) - user_days)
        rev += a + b + c + dr * I["arpdau"] * factor * 365
        d_dau += dp + dr
    new_arpdau = arpdau_after(rev, d_dau)
    return {
        "d_dau": round(d_dau),
        "rev": round(rev),
        "arpdau_after": round(new_arpdau, 5),
        "d_arpdau": round(new_arpdau - arpdau_base, 5),
        "d_arpdau_pct": round((new_arpdau / arpdau_base - 1) * 100, 2),
    }


COMPARE = {
    "note": "Same DAU denominator, same baseline. The only difference between the two "
            "columns is whether a marginal retained user is assumed to monetise at the "
            "average ARPDAU or at half of it.",
    "as_modelled": {
        "retention_leads": retention_portfolio(1.0),
        "first_dollar": programme_at(1.0),
    },
    "marginal_corrected": {
        "retention_leads": retention_portfolio(I["marginal_arpdau_factor"]),
        "first_dollar": programme_at(I["marginal_arpdau_factor"]),
    },
}

OUT = {
    "generated_by": "scripts/build-model.py",
    "metric": "ARPDAU = (payers / DAU) x ARPPU",
    "inputs": I,
    "scenario_inputs": SC,
    "baseline": BASE,
    "moves": moves_out,
    "programme": totals,
    "compare": COMPARE,
    "parked": [
        {"name": "Rookie Crew", "why": "D30 follow-on; build once a payer base exists. Still blocked on the faction correlate."},
        {"name": "Mid-game catch-up track", "why": "Blocked on faucet-vs-sink data, and it is a denominator play."},
        {"name": "Tentpole win-back", "why": "Ships after move 02, so returners land on a real ladder."},
        {"name": "Deeper whale extraction", "why": "Rejected. No headroom, and the corpus prices the goodwill cost."},
    ],
}

path = pathlib.Path(__file__).resolve().parent.parent / "data" / "roi-model.json"
path.write_text(json.dumps(OUT, indent=1) + "\n")

# ---------------------------------------------------------------- report
print(f"baseline  k={BASE['k']}  user-days={BASE['user_days']}")
print(f"          DAU total={BASE['dau_total']:,}  new-install={BASE['dau_new_installs']:,}  legacy={BASE['dau_legacy']:,}")
print(f"          ARPPU/paying-DAU/day=${BASE['arppu_per_paying_dau_day']}  new payers/mo={BASE['new_payers_mo']:,}")
print()
for m in moves_out:
    b = m["sc"]["base"]
    print(f"  {m['id']}. {m['name']:<22} +{b['conv_pp']}pp conv  +{b['added_payers_mo']:>4}/mo  ${b['rev']:>9,}/yr")
print()
for sc in ("low", "base", "high"):
    t = totals[sc]
    print(f"  {sc:<5} ever-pay 2.00% -> {t['ever_pay_after']}%   ${t['rev']:>9,}/yr   "
          f"ARPDAU {arpdau_base} -> {t['arpdau_after']}  ({t['d_arpdau']:+.5f}, {t['d_arpdau_pct']:+.1f}%)")
print()
for label in ("as_modelled", "marginal_corrected"):
    print(f"  {label}")
    for who in ("retention_leads", "first_dollar"):
        c = COMPARE[label][who]
        print(f"    {who:<18} rev ${c['rev']:>9,}/yr   dDAU {c['d_dau']:>6,}   "
              f"dARPDAU {c['d_arpdau']:+.5f} ({c['d_arpdau_pct']:+.1f}%)")
print(f"\nwrote {path}")
