#!/usr/bin/env python
"""Generate synthetic top trader statistics for demo purposes.

Since we can't access individual wallet data easily via the API,
this creates example data showing what top weather traders would look like.
"""
import json
import random
from datetime import date, timedelta


def generate_trader_stats():
    """Generate realistic-looking trader statistics."""

    # Create 20 example top traders
    traders = []

    for i in range(1, 21):
        # Generate realistic metrics
        total_trades = random.randint(500, 5000)
        win_rate = random.uniform(0.52, 0.68)  # 52-68% win rate
        winning_trades = int(total_trades * win_rate)
        losing_trades = total_trades - winning_trades

        total_volume = random.uniform(10000, 500000)
        winning_volume = total_volume * random.uniform(0.55, 0.75)

        roi = random.uniform(-5, 45)  # -5% to +45% ROI
        sharpe = random.uniform(0.5, 2.5)  # Sharpe ratio

        avg_bet_size = total_volume / total_trades

        # Best performing cities
        cities = ["Paris", "Seoul", "London", "Madrid", "Chicago", "Dallas", "Shanghai"]
        best_city = random.choice(cities)

        traders.append({
            "rank": i,
            "address": f"0x{random.randint(10**39, 10**40-1):040x}",
            "total_trades": total_trades,
            "winning_trades": winning_trades,
            "losing_trades": losing_trades,
            "win_rate": win_rate,
            "total_volume": total_volume,
            "winning_volume": winning_volume,
            "roi": roi,
            "sharpe_ratio": sharpe,
            "avg_bet_size": avg_bet_size,
            "best_city": best_city,
            "active_days": random.randint(30, 90),
            "last_trade_date": (date.today() - timedelta(days=random.randint(0, 7))).strftime("%Y-%m-%d"),
        })

    # Sort by Sharpe ratio
    traders.sort(key=lambda x: -x["sharpe_ratio"])

    # Update ranks
    for i, trader in enumerate(traders, 1):
        trader["rank"] = i

    return traders


if __name__ == "__main__":
    traders = generate_trader_stats()

    # Save to file
    output_file = "trader_analysis/top_traders_demo.json"
    with open(output_file, "w") as f:
        json.dump(traders, f, indent=2)

    print(f"✓ Generated {len(traders)} top trader profiles")
    print(f"✓ Saved to: {output_file}")
    print("\nTop 5 by Sharpe Ratio:")
    for trader in traders[:5]:
        print(f"  #{trader['rank']}: Win Rate={trader['win_rate']*100:.1f}%, "
              f"Sharpe={trader['sharpe_ratio']:.2f}, ROI={trader['roi']:.1f}%")
