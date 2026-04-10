---
name: okx-defi-lp
description: >
  Use this skill for managing Uniswap V3 liquidity provider (LP) positions end-to-end:
  checking position health and in-range status, computing impermanent loss (IL),
  finding the best LP pools by APY and risk, tracking whale/KOL activity in your
  token pairs, and deciding whether to rebalance an out-of-range position.

  Triggers: 'check my LP position', 'is my position in range', 'impermanent loss',
  'find LP pools', 'best APY pools', 'whale activity on my token', 'smart money',
  'rebalance my position', 'out of range what to do', 'LP监控', '流动性管理',
  '要不要调仓', '大户动态'.

  This skill is the single entry point for the OKX DeFi LP kit. It delegates to
  the appropriate workflow based on the user's question. Use the reference files
  for detailed workflows, API patterns, IL formulas, and display formats.
tags: [uniswap-v3, liquidity, impermanent-loss, lp-management, defi, okx-build-x, apy, whale-tracking, rebalancing]
references:
  - il-formula
  - position-health
  - pool-scouting
  - whale-signals
  - rebalance-decisions
---

# OKX DeFi LP

Unified Uniswap V3 liquidity management skill for the OKX Build X Hackathon — Agent Track.

## At a Glance

This skill covers 4 LP management scenarios. Read the reference files to understand each workflow:

| Scenario | Reference | Key Question |
|---|---|---|
| Is my position in range? Am I losing money? | `position-health` | IL, tick range, drift, health score |
| Where should I provide liquidity? | `pool-scouting` | APY ranking, TVL, token risk |
| What are whales/KOLs doing in my token pair? | `whale-signals` | Smart money sentiment, buy/sell pressure |
| My position is out of range — stay or rebalance? | `rebalance-decisions` | Gas cost, recovery time, exit value |

## Quick Reference

### IL Formulas

```
price_ratio = current_price / entry_price

# IN-RANGE position (earning fees on both tokens):
il = (1 - 2 * sqrt(price_ratio) / (1 + price_ratio)) * 100

# OUT-OF-RANGE position (100% one token — 7-10x worse):
il = (1 - 2 / (1 + price_ratio)) * 100
```

⚠️ Do NOT use the sqrt formula for out-of-range positions. Out-of-range IL is 7–10x worse than it looks.

### Tick Data

- Use `rangeInfo.lowerPrice` / `rangeInfo.upperPrice` directly from the API
- Do NOT convert `tickLower`/`tickUpper` via `1.0001^tick` — the API tick values are already scaled
- `rangeInfo` lives inside `positionList[]` in the `position-detail` response, NOT at the top level

### Supported Chains

ethereum, base, bsc, polygon, arbitrum, avalanche, optimism

⚠️ Sepolia is NOT supported for position queries — returns `Parameter error` or HTTP 500.

## Skill Router

Based on the user's question, use the matching workflow:

```
"is my position in range" / "am I losing money" / "check my LP"
  → onchainos defi positions --address <addr> --chains <chains>
  → onchainos defi position-detail --address <addr> --chain <chain> --platform-id <platformId>
  → compute IL using out-of-range or in-range formula
  → display health score

"find LP pools" / "best APY" / "where to provide liquidity"
  → onchainos defi search --token <token> --chain <chain>
  → onchainos defi list --chain <chain>
  → enrich with token risk data
  → score by APY * TVL_weight - risk_penalty

"whale" / "smart money" / "KOL" signals
  → onchainos signal list --chain <chain>
  → filter by token pair from user's positions
  → sentiment: >60% buy = Bullish, >60% sell = Bearish

"out of range" / "should I rebalance" / "what do I do"
  → onchainos defi position-detail (confirm out-of-range)
  → estimate exit value, rebalance cost, recovery time
  → compare options: Stay / Rebalance / Exit
```

## Chain-to-Platform ID Map (for position-detail)

| Platform | Platform ID |
|---|---|
| Uniswap V3 | 68 |
| PancakeSwap V3 | 279 |
| SushiSwap V3 | 306 |
| Uniswap V2 | 1 |

## Wallet Requirements

| Operation | Wallet Required? |
|---|---|
| Position health check | Provide address (read-only) |
| Pool scouting | No |
| Whale signals | No |
| Executing rebalances | Yes (`okx-agentic-wallet` login) |

## Limitations

- **No persistent subscriptions** — whale signals are a point-in-time snapshot
- **IL requires entry price** — without it, display as estimate and note what's needed
- **Sepolia unsupported** for position queries — use mainnet chains only
