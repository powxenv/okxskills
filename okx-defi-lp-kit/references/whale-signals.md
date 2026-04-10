# Whale Signals Workflow

Track what smart money, KOLs, and whales are doing in the tokens where you hold LP positions.

## Two Modes

- **Mode A** — User provides token pair directly
- **Mode B** — Discover from wallet: pull LP positions, extract token pairs, check signals for each

## Workflow

### Step 1: Discover LP Tokens (Mode B)

```
onchainos defi positions --address <addr> --chains <chains>
```

Extract token pair from `investName` (e.g. "ETH-USDC" from "Uniswap V3 ETH-USDC 0.30%").

### Step 2: Query Signals

```
onchainos signal list --chain ethereum
```

Key signal fields:

| Field | Description |
|---|---|
| `walletType` | 1=Smart Money, 2=KOL, 4=Whale |
| `token.symbol` | Token traded |
| `soldRatioPercent` | % of trade that was a sell (>60% = bearish, <40% = bullish) |
| `amountUsd` | USD value of the activity |
| `timestamp` | When the signal fired (ms since epoch) |

### Step 3: Cross-Reference with Trader Tags

```
onchainos token trades --address <tokenAddr> --chain ethereum --tag-filter 3
onchainos tracker activities --tracker-type smart_money --chain ethereum
```

### Step 4: Sentiment Scoring

Focus on signals from the last 7 days.

```
Bullish:   >60% buy signals by USD volume
Neutral:   mixed signals
Bearish:   >60% sell signals by USD volume
```

---

## Display Format

```
Smart Money Activity for [Token Pair]
Recent Signals (7d):
  [BUY]  @smart_money bought $XX,XXX of [TOKEN] — Xh ago
  [SELL] @kol sold $XX,XXX of [TOKEN] — Xd ago
  [BUY]  @whale bought $XX,XXX of [TOKEN] — Xd ago

Summary: X buy signals, X sell signals in the past 7 days
Sentiment: [Bullish/Neutral/Bearish]

For Your LP: [Token Pair] shows [Bullish/Neutral/Bearish] sentiment
→ [1-sentence interpretation]
```

---

## Alert Generation

| Sentiment | Implication for LP |
|---|---|
| Bullish | KOLs/whales accumulating — favorable for pool volume, stay deployed |
| Neutral | No strong signal — monitor, no urgent action |
| Bearish | Smart money selling — could mean reduced pool volume, monitor IL closely |

---

## Cross-Skill Routing

- Unusual activity detected — run `onchainos token advanced-info` and `onchainos token cluster-overview`
- User wants to follow a whale wallet — `onchainos tracker activities --tracker-type multi_address --wallet-address <addr>`
- User wants to exit based on signal — `onchainos defi withdraw --investment-id <id> --address <addr> --chain <chain> --ratio 1.0`

---

## Limitations

- Point-in-time snapshot only — no persistent subscriptions
- Signals indicate recent activity, not a guarantee of future direction

---

## Error Handling

- No LP positions found — prompt user to provide token addresses
- No signals found for token pair — "No recent signals" (not necessarily bearish, just quiet)
- Signal API fails — fall back to `token trades --tag-filter` for direct activity
