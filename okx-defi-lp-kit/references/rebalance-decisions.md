# Rebalance Decisions Workflow

Given an out-of-range Uniswap V3 position, compare staying vs. rebalancing vs. exiting — and recommend the best option.

## When to Use

This workflow fires when:
1. `position-health` reports a position is out of range
2. User asks "should I rebalance", "out of range what to do", "remove and redeposit"

If the position is **in range**, redirect to `position-health` — rebalancing an in-range position is rarely beneficial.

---

## Workflow

### Step 1: Confirm Out-of-Range Status

```
onchainos defi position-detail --address <addr> --chain ethereum --platform-id 68
```

Extract:
- `rangeInfo.lowerPrice`, `rangeInfo.upperPrice`
- `positionList[].positionStatus` (INACTIVE = out of range)
- `assetsTokenList[].coinAmount` and `assetsTokenList[].currencyAmount`

### Step 2: Estimate Exit Value

When removing liquidity out of range, you receive mostly the one-sided token.
Calculate USD value from `currencyAmount` fields.

```
onchainos token price-info --address <tokenAddr>
```

### Step 3: Estimate Rebalancing Cost

```
onchainos gateway gas --chain ethereum
```

Rebalancing costs:
1. **Gas** — 2 transactions (remove + redeposit). Ethereum ~$10–30, Base ~$0.50
2. **Swap cost** — if redepositing with different token composition
3. **Temporary IL** — price could move between remove and redeposit
4. **Fee earning loss** — removed liquidity stops earning immediately

### Step 4: Estimate Recovery Time

```
recovery_days = rebalance_cost_usd / daily_fee_earnings_usd
daily_fee_earnings = daily_volume_usd * fee_tier
```

Note: this is an estimate — volume changes constantly.

### Step 5: Suggest Tick Ranges

| Range Type | Width | Fee APY | IL Risk | Recovery |
|---|---|---|---|---|
| Tight | ±5–10% | Highest | Highest | Fastest |
| Medium | ±20–30% | Medium | Medium | Medium |
| Wide | ±50%+ | Lowest | Lowest | Slowest |

---

## Decision Matrix

| Option | When to Choose |
|---|---|
| Stay in position | Recovery time < 7 days, IL is small, gas is high |
| Rebalance to same range | Price has fundamentally changed — original thesis still valid |
| Rebalance to tighter range | Confident price will stay in a narrower band — earns more fees but higher IL risk |
| Remove entirely | Thesis is broken, IL is severe, gas savings matter |

---

## Display Format

```
Position: [Token Pair] — [Fee Tier]
Current Status: OUT OF RANGE (price [above/below] [upper/lower] bound)
Current Range: $[lower] — $[upper]
Current Value: $X,XXX

Option A — Stay and Wait
  Estimated recovery: ~X days (based on ~$X/day fees)
  Gas cost: $0 (no action)
  Risk: Price may continue drifting

Option B — Rebalance to Current Price ± 20%
  Estimated gas: ~$X (2 txs)
  New position value: $X,XXX
  Recovery time: ~X days
  Best for: [reason]

Option C — Remove Liquidity
  Estimated gas: ~$X
  You receive: X.XX [token0], X.XX [token1] (~$X,XXX)
  Best for: Thesis broken, minimize further IL

Recommendation: [Option X]
Reason: [1–2 sentence rationale]
```

---

## Cross-Skill Routing

- User decides to rebalance — execute `onchainos defi withdraw` then `onchainos defi invest`
- User wants to check gas first — `onchainos gateway gas --chain <chain>`
- User is uncertain about token outlook — route to `whale-signals`
- User wants to verify rebalancing is safe — `onchainos gateway simulate` with the withdraw calldata

---

## Error Handling

- Position is in range — redirect to `position-health`
- `calculate-entry` fails — try `defi prepare` as fallback
- Gas estimation unavailable — rough estimates: Ethereum ~$10–30, Base ~$0.50
- `invest`/`withdraw` not supported for this platform — note limitation, suggest manual alternatives
