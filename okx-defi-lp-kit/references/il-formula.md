# IL Formula Reference

## IL Definition

Impermanent Loss (IL) is the difference in value between holding two tokens in a liquidity pool vs. holding them in a wallet (HODL).

```
IL = (LP_value - HODL_value) / HODL_value * 100
```

A negative IL means you're losing relative to HODL.

---

## Two IL Formulas — Use the Right One

### Scenario A: Position is IN Range (earning fees on both tokens)

```
price_ratio = current_price / entry_price
il = (1 - 2 * sqrt(price_ratio) / (1 + price_ratio)) * 100
```

### Scenario B: Position is OUT of Range (100% one token)

```
price_ratio = current_price / entry_price
il = (1 - 2 / (1 + price_ratio)) * 100
```

⚠️ **Critical:** Out-of-range IL is 7–10x worse than the sqrt formula suggests. Never use Scenario A's formula for an out-of-range position.

---

## Examples

| Entry Price | Current Price | Price Ratio | In-Range IL | Out-of-Range IL |
|---|---|---|---|---|
| $100 | $100 | 1.0x | 0.0% | 0.0% |
| $100 | $150 | 1.5x | -2.0% | -20.0% |
| $100 | $200 | 2.0x | -5.7% | -33.3% |
| $100 | $80 | 0.8x | -0.6% | -11.1% |
| $100 | $50 | 0.5x | -5.7% | -25.0% |
| $1274 | $2184 | 1.71x | -3.5% | -26.3% |

---

## Why Out-of-Range is Catastrophic

When a position goes out of range, you become 100% exposed to a single token. The formula simplifies because you lose all diversification benefit:

```
Out-of-Range IL = (1 - 2 / (1 + P)) * 100
```

Where P is the price ratio. Notice there's no sqrt — the loss grows linearly with P, not sqrt(P).

---

## Tick Data from the API

The `onchainos defi position-detail` response contains tick data inside `positionList[].rangeInfo`:

```
rangeInfo.tickLower   — lower tick bound (API-scaled, do not convert via 1.0001^tick)
rangeInfo.tickUpper   — upper tick bound (API-scaled, do not convert via 1.0001^tick)
rangeInfo.lowerPrice  — lower price bound (USE THIS for range comparison)
rangeInfo.upperPrice  — upper price bound (USE THIS for range comparison)
```

### In-Range Check

```
lowerPrice <= currentPrice < upperPrice → IN RANGE
currentPrice < lowerPrice → BELOW RANGE (only token1 active)
currentPrice >= upperPrice → ABOVE RANGE (only token0 active)
```

---

## Drift Calculation

When out of range, compute how far the price has moved from the nearest bound:

```
# Price below range:
drift_pct = (lowerPrice - currentPrice) / currentPrice * 100

# Price above range:
drift_pct = (currentPrice - upperPrice) / currentPrice * 100
```

---

## Getting Entry Price

1. `onchainos defi depth-price-chart --investment-id <id> --chain <chain>` — historical pool price at position open
2. `onchainos defi position-detail` — some positions store `positionOpenPrice` in extraData
3. Ask the user directly

Without entry price, IL cannot be accurately computed. Display as `[ESTIMATE]` and explain what inputs are needed.

---

## Fee Recovery Time

Once IL is known, estimate how long fees take to offset it:

```
recovery_hours = abs(il_pct / 100) * position_value_usd / daily_fee_revenue_usd
```

Daily fee revenue estimate: `daily_volume_usd * fee_tier`. Note this is approximate — volume changes constantly.
