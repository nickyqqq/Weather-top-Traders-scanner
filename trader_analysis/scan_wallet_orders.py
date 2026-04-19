#!/usr/bin/env python
"""Scan order history for a specific wallet address.

This generates demo order data. In production, this would call Polymarket CLOB API
to fetch real order history for a wallet.
"""
import random
from datetime import date, datetime, timedelta


def generate_order_history(wallet_address: str, num_orders: int = 50):
    """Generate realistic order history for a wallet.

    Args:
        wallet_address: Wallet address to generate history for
        num_orders: Number of orders to generate

    Returns:
        List of order dictionaries with timestamps, markets, outcomes, etc.
    """
    cities = ["Paris", "Seoul", "London", "Madrid", "Chicago", "Dallas", "Shanghai", "Miami"]
    order_types = ["BUY", "SELL"]
    statuses = ["FILLED", "FILLED", "FILLED", "FILLED", "PARTIALLY_FILLED", "CANCELLED"]

    orders = []

    for i in range(num_orders):
        days_ago = random.randint(0, 90)
        order_date = date.today() - timedelta(days=days_ago)
        order_time = datetime.combine(order_date, datetime.min.time()) + timedelta(
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )

        city = random.choice(cities)
        temp = random.randint(10, 30)
        outcome = f"{temp}°C"

        order_type = random.choice(order_types)
        status = random.choice(statuses)

        size = random.uniform(10, 500)
        price = random.uniform(0.10, 0.90)

        # Calculate if won (simplified)
        won = None
        pnl = None
        if status == "FILLED":
            won = random.choice([True, True, True, False])  # 75% win rate for demo
            if won:
                pnl = size * (1.0 - price) if order_type == "BUY" else size * price
            else:
                pnl = -size * price if order_type == "BUY" else -size * (1.0 - price)

        orders.append({
            "order_id": f"0x{random.randint(10**15, 10**16-1):016x}",
            "timestamp": order_time.strftime("%Y-%m-%d %H:%M:%S"),
            "city": city,
            "outcome": outcome,
            "order_type": order_type,
            "status": status,
            "size": size,
            "price": price,
            "won": won,
            "pnl": pnl,
            "market_url": f"https://polymarket.com/event/highest-temperature-in-{city.lower()}-on-{order_date.strftime('%B-%d-%Y').lower()}",
        })

    # Sort by timestamp descending (newest first)
    orders.sort(key=lambda x: x["timestamp"], reverse=True)

    return orders


def get_wallet_summary(orders):
    """Calculate summary statistics from order history."""
    if not orders:
        return {}

    filled_orders = [o for o in orders if o["status"] == "FILLED"]

    if not filled_orders:
        return {
            "total_orders": len(orders),
            "filled_orders": 0,
        }

    won_orders = [o for o in filled_orders if o["won"]]
    lost_orders = [o for o in filled_orders if o["won"] is False]

    total_pnl = sum(o["pnl"] for o in filled_orders if o["pnl"] is not None)
    total_volume = sum(o["size"] for o in filled_orders)

    return {
        "total_orders": len(orders),
        "filled_orders": len(filled_orders),
        "won_orders": len(won_orders),
        "lost_orders": len(lost_orders),
        "win_rate": len(won_orders) / len(filled_orders) if filled_orders else 0,
        "total_pnl": total_pnl,
        "total_volume": total_volume,
        "avg_order_size": total_volume / len(filled_orders) if filled_orders else 0,
        "best_trade": max((o["pnl"] for o in filled_orders if o["pnl"]), default=0),
        "worst_trade": min((o["pnl"] for o in filled_orders if o["pnl"]), default=0),
    }


if __name__ == "__main__":
    # Test
    address = "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
    orders = generate_order_history(address, 50)
    summary = get_wallet_summary(orders)

    print(f"Generated {len(orders)} orders for {address}")
    print(f"Summary: {summary['filled_orders']} filled, {summary['won_orders']}W / {summary['lost_orders']}L")
    print(f"Win Rate: {summary['win_rate']*100:.1f}%")
    print(f"Total PnL: ${summary['total_pnl']:.2f}")
