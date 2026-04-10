# OKX X Layer Skills

Three independent agent skills for on-chain trading, automation, and Uniswap integration on X Layer. Each one works on its own — install whichever you need.

## Install

Pick one:

```bash
# Using skills.sh (https://skills.sh)
npx skills add powxenv/okx-agent-skills

# Using flins (https://flins.tech)
npx flins add powxenv/okx-agent-skills
```

Or clone manually and place the skill folder in your agent's skills directory:

```bash
git clone https://github.com/powxenv/okx-agent-skills.git
# Copy the skill folder(s) you need into your agent's skills directory
# e.g. .agents/skills/, .cursor/skills/, .claude/skills/
```

Each skill is self-contained — no cross-skill dependencies. Install one, two, or all three.

## Skills

### okx-trading

Full-lifecycle on-chain trading. 30+ CLI commands covering token analysis, security scanning, market data, smart money tracking, DEX swaps, DeFi yield, meme trenches, portfolio management, and wallet operations.

- Research tokens, check security, pull prices, track smart money
- Execute swaps with MEV protection across 500+ DEX sources
- Deposit, withdraw, and claim rewards in DeFi products
- Scan meme tokens, check developer reputation, detect bundle/sniper activity
- Step-by-step workflows for buy, sell, research, DeFi yield, and meme trading
- Built-in risk framework, trading strategies, and decision checklists

### okx-xlayer-agent

Automation framework for autonomous agents on X Layer. Leverages X Layer's near-zero gas ($0.0005/tx) and 1-second finality so agents can run continuously without burning through capital.

- Sense → Decide → Act loop with mandatory security gates on every trade
- Four ready-made agent patterns: DCA, smart money follower, DeFi auto-compounder, x402 self-funding
- Configurable risk limits: per-trade caps, portfolio heat, daily trade/loss limits, stop-losses
- WebSocket monitoring for real-time price and signal data
- Silent mode for production agents — heartbeat logging, action-only output
- x402 payment integration so agents can pay for services and receive payments
- All 30+ onchainos commands, trading workflows, risk framework, and decision checklists included

### okx-uniswap

Direct Uniswap protocol integration for agents — V3 concentrated liquidity, Trading API swaps, x402 payments, and LP rebalancing on X Layer and EVM chains.

- Swap via OKX aggregator (best price across 500+ DEXes) or Uniswap Trading API (direct protocol)
- Full V3 LP lifecycle: mint, monitor, rebalance, collect fees using `cast` (Foundry)
- X Layer makes active LP profitable — rebalancing every 5 minutes costs ~$4.32/day
- Compare routes: quote both OKX aggregator and Uniswap, pick the better price
- Pay for API access via x402 or Tempo CLI with auto-swap funding
- Five agent patterns: auto-rebalancing LP, fee harvesting, yield farming, cross-chain arbitrage, smart money + Uniswap
- Complete Trading API reference with Permit2, routing types, and error handling
- V3 position lifecycle with tick math and impermanent loss calculator

**Prerequisites**: OnchainOS CLI for all operations. Foundry (`cast`) for V3 LP management. Uniswap API key ([developers.uniswap.org/dashboard](https://developers.uniswap.org/dashboard)) for Trading API.

## Why X Layer

X Layer makes agent strategies viable that would be impractical on Ethereum:

| | X Layer | Ethereum |
|---|---|---|
| Gas per tx | ~$0.0005 | ~$2–50 |
| Block time | ~1 second | ~12 seconds |
| Rebalancing daily | $0.015/day | $300/day |
| Rebalancing hourly | $0.36/day | $7,200/day |
| Rebalancing every 5 min | $4.32/day | Impractical |
| Auto-compounding | Profitable | Gas > rewards |

## File Structure

```
skills/
├── okx-trading/          # 27 files — full trading lifecycle
├── okx-xlayer-agent/     # 18 files — autonomous agent framework
└── okx-uniswap/          # 13 files — Uniswap protocol integration
```

Each skill has its own `SKILL.md`, `agents/openai.yaml`, `_shared/`, and `references/`.

## License

MIT