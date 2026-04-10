#!/usr/bin/env python3
"""
Impermanent Loss (IL) calculator for Uniswap V3 LP positions.

Usage:
  python3 compute_il.py <entry_price> <current_price> [tick_lower] [tick_upper] [fee_tier]

  python3 compute_il.py --prices <entry_price> <current_price> --range <lower_price> <upper_price>

fee_tier examples: 0.0005 (0.05%), 0.003 (0.30%), 0.01 (1%)
"""

import math
import sys

# Fee tier -> tick spacing for Uniswap V3
_FEE_TICK_SPACING = {
    0.0001: 1,    # 0.01% -- 1 tick
    0.0005: 10,   # 0.05% -- 10 ticks
    0.003: 60,    # 0.30% -- 60 ticks
    0.01: 200,    # 1.00% -- 200 ticks
}

def get_tick_spacing(fee_tier: float) -> int:
    """Return tick spacing for a given fee tier. Default: 60."""
    return _FEE_TICK_SPACING.get(fee_tier, 60)


def compute_il_simple(entry_price: float, current_price: float) -> float:
    """
    IL for a standard 50/50 LP (entry and current prices as floats).
    Returns IL as a percentage. Negative IL means losses vs HODL.
    """
    if entry_price <= 0 or current_price <= 0:
        return 0.0
    price_ratio = current_price / entry_price
    il = 1 - (2 * math.sqrt(price_ratio) / (1 + price_ratio))
    return il * 100


def tick_to_price(tick: int, fee_tier: float = 0.003) -> float:
    """
    Convert a Uniswap V3 tick index to a price (token1/token0).
    Uses fee tier to determine tick spacing.
    price = 1.0001 ^ (tick * tick_spacing)
    """
    spacing = get_tick_spacing(fee_tier)
    effective_tick = tick * spacing
    return 1.0001 ** effective_tick


def price_to_tick(price: float, fee_tier: float = 0.003) -> int:
    """
    Convert a price (token1/token0) to a tick index.
    Returns the floor of the tick index.
    """
    spacing = get_tick_spacing(fee_tier)
    return int(math.log(price) / math.log(1.0001) / spacing)


def compute_il_concentrated(entry_price: float, current_price: float,
                             tick_lower: int, tick_upper: int,
                             fee_tier: float = 0.003) -> dict:
    """
    Compute IL using raw Uniswap V3 tick values from the position API.

    The API returns tickLower/tickUpper values that are already scaled by
    the pool's tick spacing. For price conversion, use:
      price_at_tick = 1.0001 ^ (tick / spacing)

    IMPORTANT: Many APIs store the effective tick directly. If tick values
    don't produce sensible prices, use compute_il_from_prices() instead.
    """
    if entry_price <= 0 or current_price <= 0:
        return {"il": 0.0, "status": "unknown"}

    spacing = get_tick_spacing(fee_tier)
    effective_lower = tick_lower / spacing
    effective_upper = tick_upper / spacing

    price_at_lower = 1.0001 ** effective_lower
    price_at_upper = 1.0001 ** effective_upper
    price_ratio = current_price / entry_price

    if current_price < price_at_lower:
        status = "below_range"
        il = (1 - (2 / (1 + price_ratio))) * 100
    elif current_price > price_at_upper:
        status = "above_range"
        il = (1 - (2 / (1 + price_ratio))) * 100
    else:
        status = "in_range"
        il = (1 - (2 * math.sqrt(price_ratio) / (1 + price_ratio))) * 100

    return {
        "il": round(il, 3),
        "status": status,
        "fee_tier": fee_tier,
        "tick_spacing": spacing,
        "price_at_lower": round(price_at_lower, 4),
        "price_at_upper": round(price_at_upper, 4),
        "price_ratio": round(price_ratio, 4)
    }


def compute_il_from_prices(entry_price: float, current_price: float,
                            range_lower_price: float, range_upper_price: float) -> dict:
    """
    Compute IL when you have direct price values (from rangeInfo).
    This avoids tick conversion ambiguity.

    IL formula for 50/50 LP at entry:
      In range:    IL = (1 - 2*sqrt(P) / (1+P)) * 100
      Out of range: IL = (1 - 2 / (1+P)) * 100
      where P = current_price / entry_price

    Both out-of-range cases (above and below) use the same formula
    because being all-in on one asset means you lost the diversification benefit.
    """
    if entry_price <= 0 or current_price <= 0:
        return {"il": 0.0, "status": "unknown"}

    price_ratio = current_price / entry_price

    if current_price < range_lower_price:
        status = "below_range"
        il = (1 - (2 / (1 + price_ratio))) * 100
    elif current_price > range_upper_price:
        status = "above_range"
        il = (1 - (2 / (1 + price_ratio))) * 100
    else:
        status = "in_range"
        il = (1 - (2 * math.sqrt(price_ratio) / (1 + price_ratio))) * 100

    return {
        "il": round(il, 3),
        "status": status,
        "price_at_lower": round(range_lower_price, 4),
        "price_at_upper": round(range_upper_price, 4),
        "price_ratio": round(price_ratio, 4)
    }


def compute_recovery_hours(il_pct: float, tvl_usd: float, fee_tier: float,
                            daily_volume_usd: float) -> float:
    """
    Estimate hours to recover IL through fee earnings.

    fee_tier: e.g. 0.003 for 0.30% pool
    daily_volume_usd: estimated daily trading volume in the pool
    """
    if tvl_usd <= 0 or fee_tier <= 0:
        return float('inf')

    daily_fees = daily_volume_usd * fee_tier
    daily_il_cost = abs(il_pct / 100) * tvl_usd

    if daily_fees <= 0 or daily_il_cost <= 0:
        return 0.0 if daily_il_cost <= 0 else float('inf')

    return round(daily_il_cost / daily_fees * 24, 1)


def main():
    if len(sys.argv) < 3:
        print("Usage: compute_il.py <entry_price> <current_price> [tick_lower] [tick_upper] [fee_tier]")
        print("  Standard 50/50 IL:")
        print("    compute_il.py 100 150")
        print("  Concentrated position (0.05% fee tier, 10-tick spacing):")
        print("    compute_il.py 1274 2184 204670 204970 0.0005")
        print("  Using direct price bounds:")
        print("    compute_il.py --prices 1274 2184 --range 1255.19 1293.41")
        sys.exit(1)

    if sys.argv[1] == "--prices":
        entry = float(sys.argv[2])
        current = float(sys.argv[3])
        lower = float(sys.argv[5])
        upper = float(sys.argv[6])
        result = compute_il_from_prices(entry, current, lower, upper)
        print(f"Entry: ${entry} | Current: ${current}")
        print(f"Range: ${lower} -- ${upper} (USDC/WETH)")
        print(f"Price Ratio: {result['price_ratio']}x")
        print(f"Status: {result['status']}")
        print(f"Impermanent Loss: {result['il']:.3f}%")
        return

    entry_price = float(sys.argv[1])
    current_price = float(sys.argv[2])

    if len(sys.argv) >= 5:
        tick_lower = int(sys.argv[3])
        tick_upper = int(sys.argv[4])
        fee_tier = float(sys.argv[5]) if len(sys.argv) >= 6 else 0.003
        result = compute_il_concentrated(entry_price, current_price, tick_lower, tick_upper, fee_tier)
        print(f"Entry: ${entry_price} | Current: ${current_price}")
        print(f"Fee tier: {fee_tier*100}% | Tick spacing: {result['tick_spacing']}")
        print(f"Tick Range: [{tick_lower}, {tick_upper}]")
        print(f"Price at Lower Tick: ${result['price_at_lower']}")
        print(f"Price at Upper Tick: ${result['price_at_upper']}")
        print(f"Status: {result['status']}")
        print(f"Price Ratio: {result['price_ratio']}x")
        print(f"Impermanent Loss: {result['il']:.3f}%")
    else:
        il = compute_il_simple(entry_price, current_price)
        print(f"Entry: ${entry_price} | Current: ${current_price}")
        print(f"Impermanent Loss: {il:.3f}%")


if __name__ == "__main__":
    main()
