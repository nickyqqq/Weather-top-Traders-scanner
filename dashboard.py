#!/usr/bin/env python
"""Weather Traders Leaderboard - Track Top Performing Weather Traders on Polymarket.

A web dashboard for analyzing and tracking the most successful traders
in Polymarket weather prediction markets.

Usage:
    python dashboard.py
    Then visit: http://localhost:5000
"""
from __future__ import annotations

import json
import logging
from datetime import date
from pathlib import Path

from flask import Flask, render_template

from trader_analysis.scan_wallet_orders import generate_order_history, get_wallet_summary

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

app = Flask(__name__)


def load_trader_stats():
    """Load top trader statistics."""
    trader_file = "trader_analysis/top_traders_demo.json"
    if not Path(trader_file).exists():
        return []

    with open(trader_file, 'r') as f:
        return json.load(f)


@app.route('/')
def index():
    """Main leaderboard page - redirects to traders."""
    traders_data = load_trader_stats()

    return render_template('traders.html',
                         traders=traders_data,
                         total_traders=len(traders_data),
                         today=date.today().strftime('%Y-%m-%d'))


@app.route('/traders')
def traders():
    """Top traders leaderboard page."""
    traders_data = load_trader_stats()

    return render_template('traders.html',
                         traders=traders_data,
                         total_traders=len(traders_data),
                         today=date.today().strftime('%Y-%m-%d'))


@app.route('/traders/<address>')
def trader_detail(address):
    """Trader detail page with order history (lazy loaded).

    This only scans/generates order history when the page is accessed,
    minimizing resource usage.
    """
    # Find trader in our database
    traders_data = load_trader_stats()
    trader = next((t for t in traders_data if t["address"] == address), None)

    if not trader:
        return "Trader not found", 404

    # LAZY LOAD: Only fetch order history when page is accessed
    logger.info("Scanning order history for %s...", address)
    orders = generate_order_history(address, num_orders=100)
    summary = get_wallet_summary(orders)

    return render_template('trader_detail.html',
                         trader=trader,
                         orders=orders,
                         summary=summary,
                         polymarket_url=f"https://polymarket.com/profile/{address}",
                         today=date.today().strftime('%Y-%m-%d'))


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("👥 WEATHER TRADERS LEADERBOARD")
    print("=" * 60)
    print("\nStarting dashboard server...")
    print("Visit: http://localhost:5000")
    print("\nPress Ctrl+C to stop\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
