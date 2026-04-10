# OKX X Layer Skills Suite

> **Skills Arena submission for the [X Layer Build X Hackathon](https://web3.okx.com/xlayer/build-x-hackathon)**

*"Agents don't just assist — they build, trade, and compete."*

## Overview

A suite of three interoperable agent skills enabling autonomous trading, earning, and competing on X Layer. Built on OKX OnchainOS and Uniswap, these skills give AI agents everything they need to operate independently on-chain: research tokens, assess risk, execute trades, manage V3 liquidity positions, harvest fees, pay for services, and interact with other agents — all on X Layer's zero-gas L2.

## Skills

### 1. `okx-trading` — Comprehensive On-Chain Trading

The core skill covering the full trading lifecycle: 30+ CLI commands for token research, security scanning, market data, smart money tracking, DEX swap execution, DeFi yield farming, meme token trenches, portfolio management, wallet operations, and transaction broadcasting.

| | |
|---|---|
| **Arena** | Skills Arena |
| **Files** | 27 (SKILL.md + 23 references + 3 shared) |
| **Dependencies** | OKX OnchainOS CLI (`onchainos`) |

**Key capabilities:**
- Token research & analysis: search, info, price-info, holders, liquidity, advanced-info
- Security scanning: token-scan, dapp-scan, tx-scan, sig-scan, approvals
- Market & signals: price, kline, portfolio PnL, smart money tracking, buy signals
- Swap execution: quote → confirm → execute with MEV protection
- DeFi yield: search, invest, withdraw, collect, positions
- Wallet management: login, balance, send, history
- Meme trenches: hot tokens, dev info, bundle detection
- Detailed workflows: buy, sell, research, DeFi yield, meme trading
- Best practices: risk framework, trading strategies, market analysis, decision checklists

### 2. `okx-xlayer-agent` — Autonomous Agent on X Layer

An automation framework for building autonomous agents on X Layer. Provides agent decision logic, monitoring loops, silent mode rules, risk limits, and four complete agent workflow patterns.

| | |
|---|---|
| **Arena** | Skills Arena (also targets **Most Active Agent** special prize) |
| **Files** | 5 (SKILL.md + 1 reference + 2 shared + agents config) |
| **Dependencies** | OKX OnchainOS CLI (`onchainos`) |

**Key capabilities:**
- **Sense → Decide → Act** loop architecture with mandatory security gates
- Four agent patterns: DCA, Smart Money Follower, DeFi Auto-Compounder, X402 Self-Funding
- Configurable risk parameters: per-trade risk, portfolio heat, daily limits, stop-losses
- X Layer optimizations: zero-gas DeFi compounding, auto-rebalancing, MEV-free small trades
- WebSocket monitoring for real-time price and signal data
- Silent mode for production agents (heartbeat logging, action-only output)
- x402 payment integration for self-funding agent economics

### 3. `okx-uniswap` — Uniswap Protocol Integration for Agents

Direct Uniswap protocol interaction for autonomous agents — V3 concentrated liquidity management, Trading API swaps, x402 payments, and LP rebalancing on X Layer and EVM chains. Targets the **Best Uniswap Integration** special prize.

| | |
|---|---|
| **Arena** | Skills Arena |
| **Files** | 13 (SKILL.md + 7 references + 3 shared + agents config) |
| **Dependencies** | OKX OnchainOS CLI + Uniswap Trading API + cast (Foundry) |
| **Targets** | Best Uniswap Integration prize |

**Key capabilities:**
- **Swap execution**: OKX aggregator (best price) or Uniswap Trading API (direct protocol)
- **V3 LP management**: mint, monitor, rebalance, collect fees — complete lifecycle via `cast` + OnchainOS
- **X Layer LP advantage**: Rebalancing every 5 minutes costs ~$4.32/day vs. impractical on Ethereum
- **Route comparison**: Quote on both OKX aggregator and Uniswap, pick best execution
- **x402 payments**: Pay for API access via OnchainOS or Tempo CLI with auto-swap funding
- **Five agent patterns**: auto-rebalancing LP, fee harvesting, yield farming, cross-chain arbitrage, smart money + Uniswap
- **Trading API reference**: Full 3-step flow, Permit2 integration, routing types, error handling
- **Liquidity management reference**: Complete V3 position lifecycle with tick math and IL calculator

## Architecture

```
┌──────────────────────────────────────────────────────┐
│                   Agent Platform                     │
│                  (OpenClaw, Claude, etc.)              │
├──────────────────────────────────────────────────────┤
│                                                      │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────┐ │
│  │ okx-trading  │  │okx-xlayer-  │  │ okx-uniswap  │ │
│  │              │  │   agent      │  │              │ │
│  │ Research     │  │ Automation  │  │ V3 LP Mgmt   │ │
│  │ Security     │  │ Framework   │  │ Trading API   │ │
│  │ Market Data  │  │ Risk Gates  │  │ Swap Routing   │ │
│  │ Swap Execute │  │ Monitoring  │  │ x402 Payments │ │
│  │ DeFi Yield   │  │ Agent Loop  │  │ Agent Patterns│ │
│  │ Portfolio    │  │ x402 Pay    │  │ Fee Harvesting│ │
│  └──────┬───────┘  └──────┬──────┘  └──────┬───────┘ │
│         │                 │                 │         │
│         └────────┬───────┴─────────┬───────┘         │
│                  │                 │                  │
│         ┌────────▼───────┐ ┌──────▼────────┐         │
│         │  OnchainOS CLI  │ │  Uniswap API  │         │
│         │   (onchainos)   │ │  + Contracts   │         │
│         └────────┬───────┘ └──────┬────────┘         │
│                  │                 │                  │
└──────────────────┼─────────────────┼──────────────────┘
                   │                 │
         ┌─────────▼─────────────────▼──────────┐
         │           X Layer (Chain 196)          │
         │    ~$0.0005/tx  ·  1s finality  ·  EVM  │
         └────────────────────────────────────────┘
```

**Skill interoperability:**
- `okx-trading` provides research, security, and execution primitives that the other skills reference
- `okx-xlayer-agent` orchestrates automation loops using `okx-trading` commands
- `okx-uniswap` extends swap execution with direct Uniswap protocol access and V3 LP management
- All three skills share the same preflight, chain support, and native token references

## Hackathon Prize Targets

| Prize | Skills | Rationale |
|---|---|---|
| **Skills Arena — 1st Prize** | All three | Most comprehensive, well-documented, and immediately usable skill suite |
| **Most Active Agent** | `okx-xlayer-agent` | Framework for 24/7 autonomous agent with configurable risk gates and tx logging |
| **Best Uniswap Integration** | `okx-uniswap` | Full Trading API integration, V3 LP lifecycle, x402 payments, route comparison, LP agent patterns |

## Quick Start

### Install OnchainOS

```bash
# Required for all three skills
curl -fsSL https://raw.githubusercontent.com/okx/plugin-store/main/install-local.sh | bash
```

### Install Foundry (for Uniswap direct contract calls)

```bash
# Required for okx-uniswap V3 LP management
curl -L https://foundry.paradigm.xyz | bash && foundryup
```

### Authenticate

```bash
onchainos wallet login <email>
onchainos wallet verify <code>
onchainos wallet status  # Verify: Ready=true
```

### Example: Research, Scan, Buy

```bash
# 1. Research a token
onchainos token search --query "USDC" --chains xlayer
onchainos token price-info --address <addr> --chain xlayer

# 2. Security check (MANDATORY before every swap)
onchainos security token-scan --address <addr> --chain xlayer

# 3. Execute swap on X Layer
onchainos swap execute --from <native> --to <token> --readable-amount "10" --chain xlayer --wallet <addr>
```

### Example: V3 LP Agent on X Layer

```bash
# 1. Find a high-APY pool
onchainos defi list --chain xlayer

# 2. Check pool depth
onchainos defi depth-price-chart --investment-id <id>

# 3. Monitor price
onchainos ws start --channel price --token-pair "196:<addr>"

# 4. Open position (see okx-uniswap skill for full V3 mint process)
# 5. Auto-rebalance when price exits range (see agent-uniswap-patterns.md)
```

## X Layer Advantages for Autonomous Agents

| Feature | X Layer | Ethereum |
|---|---|---|
| Gas per tx | ~$0.0005 | ~$2-50 |
| Block time | ~1 second | ~12 seconds |
| Daily rebalance cost | $0.015 | $300 |
| Hourly rebalance cost | $0.36 | $7,200 |
| 5-min rebalance (agent) | $4.32/day | Impractical |
| Auto-compounding viable | Yes (gas < reward) | No (gas > reward) |

These economics make X Layer uniquely suited for autonomous agent strategies — what costs thousands on Ethereum costs pennies on X Layer.

## File Structure

```
skills/
├── okx-trading/                    # Comprehensive on-chain trading (27 files)
│   ├── SKILL.md                    # Main skill definition (297 lines)
│   ├── agents/openai.yaml          # OpenAI agent config
│   ├── _shared/
│   │   ├── preflight.md            # Authentication & preflight checks
│   │   ├── chain-support.md         # Chain names ↔ IDs
│   │   └── native-tokens.md        # Native token addresses per chain
│   └── references/
│       ├── workflow-buy.md          # Buy workflow (step-by-step)
│       ├── workflow-sell.md         # Sell workflow
│       ├── workflow-research.md     # Research & analysis workflow
│       ├── workflow-defi-yield.md   # DeFi yield workflow
│       ├── workflow-meme-trading.md # Meme token trenches workflow
│       ├── risk-framework.md        # Security & risk assessment
│       ├── trading-strategies.md    # Position sizing, DCA, scaling
│       ├── risk-management.md       # Portfolio protection, IL, emergency
│       ├── market-analysis.md       # Token evaluation frameworks
│       ├── decision-framework.md    # Pre-trade checklists
│       ├── xlayer-strategies.md     # Zero-gas & fast-finality strategies
│       ├── agent-automation.md       # Agent decision logic & loops
│       ├── uniswap-integration.md   # V3 LP + OnchainOS combination guide
│       ├── authentication.md        # Wallet auth reference
│       ├── troubleshooting.md        # Error codes & edge cases
│       ├── keyword-glossary.md      # Chinese keyword mapping
│       ├── ws-monitoring.md         # WebSocket real-time monitoring
│       ├── cli-reference-market.md  # Market & portfolio commands
│       ├── cli-reference-swap.md    # Swap & gateway commands
│       ├── cli-reference-security.md # Security scan commands
│       ├── cli-reference-signal.md  # Signal & tracking commands
│       └── cli-reference-defi.md    # DeFi & wallet commands
│
├── okx-xlayer-agent/               # Autonomous agent on X Layer (5 files)
│   ├── SKILL.md                    # Main skill definition (194 lines)
│   ├── agents/openai.yaml          # OpenAI agent config
│   ├── _shared/
│   │   ├── preflight.md
│   │   └── chain-support.md
│   └── references/
│       └── agent-automation.md     # Agent patterns, risk gates, silent mode
│
└── okx-uniswap/                    # Uniswap protocol for agents (13 files)
    ├── SKILL.md                    # Main skill definition (301 lines)
    ├── agents/openai.yaml          # OpenAI agent config
    ├── _shared/
    │   ├── preflight.md
    │   ├── chain-support.md
    │   └── native-tokens.md
    └── references/
        ├── trading-api.md          # Uniswap Trading API full reference
        ├── liquidity-management.md  # V3 LP position lifecycle
        ├── x402-payments.md         # x402/MPP payment handling
        ├── agent-uniswap-patterns.md # 5 agent automation patterns
        ├── trading-strategies.md    # Position sizing, DCA, scaling
        ├── risk-management.md       # Portfolio protection
        ├── xlayer-strategies.md     # X Layer zero-gas strategies
        └── keyword-glossary.md      # Chinese keyword mapping
```

## What Makes This Special

1. **Three skills, one ecosystem** — each skill works independently but references the others for a complete agent experience
2. **Built for X Layer** — every strategy and example exploits X Layer's zero-gas, 1-second finality economics
3. **Security-first** — mandatory `security token-scan` before every swap, risk gates before every agent action
4. **Best Uniswap Integration** — full Trading API integration, V3 LP lifecycle management, route comparison, x402 payments, and 5 LP agent patterns
5. **Most Active Agent ready** — configurable agent loops with logging, circuit breakers, and risk limits for 24/7 autonomous operation
6. **Chinese support** — keyword glossary maps Chinese trading terms to OnchainOS commands
7. **Progressive disclosure** — SKILL.md under 300 lines for quick start, detailed references loaded on demand
8. **Battle-tested workflows** — buy, sell, research, DeFi yield, and meme trading all have step-by-step guides with decision gates

## Resources

- [OKX OnchainOS](https://github.com/okx/onchainos-skills) — CLI tool powering all on-chain operations
- [X Layer Docs](https://docs.xlayer.io/) — X Layer documentation
- [Uniswap AI Tools](https://github.com/Uniswap/uniswap-ai) — Uniswap AI skill reference
- [Hackathon Page](https://web3.okx.com/xlayer/build-x-hackathon) — Build X Hackathon details

## License

MIT