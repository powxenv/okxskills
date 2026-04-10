# Position Health Workflow

Check whether a Uniswap V3 LP position is in-range, compute IL, and generate a health score.

## Workflow

### Step 1: Discover Positions

```
onchainos defi positions --address <addr> --chains ethereum,base,bsc,polygon,arbitrum,avalanche,optimism
```

For each platform with `investmentCount > 0`, get detailed position data:

```
onchainos defi position-detail --address <addr> --chain <chain> --platform-id <platformId>
```

Filter for Uniswap V3 positions: `platformName` contains "Uniswap V3".

### Step 2: Parse Position Data

Key fields from `position-detail`:

```
positionList[].positionStatus        # "INACTIVE" = out of range, "ACTIVE" = in range
positionList[].rangeInfo.lowerPrice  # lower price bound (USDC per WETH, etc.)
positionList[].rangeInfo.upperPrice  # upper price bound
positionList[].totalValue            # current USD value
positionList[].assetsTokenList[].tokenSymbol
positionList[].assetsTokenList[].coinAmount   # string, not float
positionList[].assetsTokenList[].currencyAmount
```

### Step 3: Get Current Price

```
onchainos token price-info --address <tokenAddr>
```

For a WETH-USDC pool, get the current WETH price.

### Step 4: Determine In-Range Status

```
if currentPrice >= lowerPrice and currentPrice < upperPrice:
    status = "IN_RANGE"
elif currentPrice < lowerPrice:
    status = "BELOW_RANGE"
else:
    status = "ABOVE_RANGE"
```

### Step 5: Compute IL (if entry price available)

Use the `il-formula` reference. If entry price is unavailable, compute drift only and label IL as `[ESTIMATE]`.

### Step 6: Generate Health Score

| Status | IL | Score | Message |
|---|---|---|---|
| In range | IL > -1% | healthy | Position is in range and not experiencing meaningful IL |
| In range | -1% <= IL < -5% | moderate | In range but minor IL — monitor |
| In range | -5% >= IL > -15% | at_risk | Significant IL — consider rebalancing |
| In range | IL <= -15% | critical | Severe IL — review position thesis |
| Below range | — | out_of_range | Price has dropped below your lower bound |
| Above range | — | out_of_range | Price has rallied above your upper bound |

---

## Display Format

For each position found:

```
[Protocol] [Token Pair] [Fee Tier]
TVL: $XX,XXX | In Range: Yes/No | IL: X.X%
Current: [token0] = $XXX | [token1] = $XXX
Price Range: $[lower] — $[upper] | Current: $[N]
Health: [score] [message]
```

---

## Cross-Skill Routing

- **Position is out of range** → suggest rebalancing: "Want to know your options? I can run the rebalance advisor."
- **User wants to find new LP opportunities** → route to `pool-scouting`
- **User wants whale/KOL signals for their token pair** → route to `whale-signals`
- **User wants to exit** → `onchainos defi withdraw --investment-id <id> --address <addr> --chain <chain> --ratio 1.0`

---

## Error Handling

- `defi positions` returns empty list — user has no DeFi positions
- `position-detail` fails — retry `defi positions` to confirm platform IDs
- Token price lookup fails — note which token price is unavailable
- `rangeInfo` missing — position may be V2 or a different pool type; skip IL calculation and note it
- No wallet address provided — ask user to provide one
