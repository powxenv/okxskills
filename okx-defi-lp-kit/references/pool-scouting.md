# Pool Scouting Workflow

Find the best LP pool opportunities across Uniswap V3, PancakeSwap V3, and SushiSwap V3 — ranked by APY, TVL, and token risk.

## Workflow

### Step 1: Discover Pools

**For a specific token pair:**
```
onchainos defi search --token ETH --chain ethereum
onchainos defi search --token USDC --chain ethereum
```

**Top pools by APY on a chain:**
```
onchainos defi list --chain ethereum
```

Filter for `productGroup == 'DEX_POOL'` platforms: Uniswap V3 (68), PancakeSwap V3 (279), SushiSwap V3 (306).

### Step 2: Enrich Pool Data

```
onchainos defi detail --investment-id <investmentId>
```

Extract: `apyDetailInfo.totalValue`, `feeRate`, `tvl`, `isExistTradingFee`, `investType`.

### Step 3: Assess Token Risk

```
onchainos token advanced-info --address <tokenAddress> --chain ethereum
onchainos token cluster-overview --address <tokenAddress> --chain ethereum
```

Flag if: `rugPullPercentage > 20%` or `newAddressHoldPercentage > 30%`.

### Step 4: Score and Rank

```
score = APY * TVL_weight - risk_penalty
```

Present top 3 recommendations with APY, TVL, risk, and holder count.

---

## Entry Point Variations

| User Provides | Action |
|---|---|
| Token pair (e.g. ETH-USDC) | Search pools for both tokens, intersect results |
| Single token | Find pools where that token is base or quote |
| Neither | Ask which chain and optionally which token |

---

## Display Format

```
[Rank 1] [Platform] — [Token Pair] ([Fee Tier])
  APY: X.XX% | TVL: $X,XXX,XXX
  Risk: [Low/Medium/High] | Holders: X,XXX
  Pool Health: [Good/Concerning] — [reason]
  Investment Thesis: [1 sentence why this pool]
```

---

## Cross-Skill Routing

- User wants to deposit — `onchainos defi invest --investment-id <id> --address <addr> --token <sym> --amount <amt>`
- User wants IL estimate before entering — route to `il-formula`
- User is unsure about token safety — run token advanced-info and token cluster-overview
