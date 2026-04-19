# Weather Traders Leaderboard

A web dashboard for tracking and analyzing the top performing traders in Polymarket weather prediction markets.

## Features

- **Top 20 Leaderboard**: Track the highest performing weather traders ranked by Sharpe ratio
- **Detailed Performance Metrics**: Win rate, ROI, total volume, average bet size, and more
- **Order History**: Click any trader to view their complete trading history (lazy-loaded for performance)
- **Performance Analytics**: Win rate distribution, key insights, and trend analysis
- **Clean UI**: Bootstrap 5-based responsive design with gradient styling

## Screenshots

### Main Leaderboard
The leaderboard shows top 20 traders with gold/silver/bronze badges for top 3 performers.

### Trader Detail Page
Click any wallet address to view:
- Complete trading statistics
- Full order history (last 100 orders)
- PnL breakdown
- Win/loss analysis

## Installation

1. Clone or download this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the dashboard:
```bash
python dashboard.py
```

4. Open your browser and visit:
```
http://localhost:5000
```

## Project Structure

```
Weather-top-Traders-scanner/
├── dashboard.py                      # Flask web application
├── requirements.txt                  # Python dependencies
├── trader_analysis/
│   ├── scan_wallet_orders.py        # Order history scanner (lazy-loaded)
│   ├── generate_trader_stats.py     # Demo trader data generator
│   └── top_traders_demo.json        # Demo trader statistics
└── templates/
    ├── traders.html                  # Main leaderboard page
    └── trader_detail.html            # Trader detail page
```

## How It Works

### Lazy Loading for Performance
Order history is **only scanned when you click on a trader's detail page**, not when viewing the leaderboard. This minimizes resource usage and keeps the dashboard fast.

### Demo Data
This dashboard uses demo data for illustration purposes. In a production environment, you would:
- Connect to Polymarket CLOB API to fetch real order history
- Implement authentication for private wallet tracking
- Store trader statistics in a database
- Set up scheduled jobs to update rankings

## Metrics Explained

- **Sharpe Ratio**: Risk-adjusted return metric (higher is better)
  - 2.0+: Excellent
  - 1.0-2.0: Good
  - <1.0: Average

- **Win Rate**: Percentage of winning trades (60%+ is strong)

- **ROI**: Return on investment percentage

- **Total Volume**: Sum of all trade sizes in USD

- **Average Bet Size**: Mean position size per trade

## Customization

### Change Port
Edit `dashboard.py` line 82:
```python
app.run(debug=True, host='0.0.0.0', port=5000)  # Change 5000 to your port
```

### Modify Rankings
Traders are ranked by Sharpe ratio by default. To change the ranking metric, edit `generate_trader_stats.py`:
```python
traders.sort(key=lambda x: -x["sharpe_ratio"])  # Change to -x["win_rate"] or -x["roi"]
```

### Update Demo Data
Run the trader stats generator:
```bash
cd trader_analysis
python generate_trader_stats.py
```

## API Access (Future)

To connect to real Polymarket data, you'll need:
1. Polymarket CLOB API credentials
2. Update `scan_wallet_orders.py` to fetch real order history
3. Implement wallet scanning logic to find top traders
4. Add database storage for persistent tracking

## License

This project is for educational and demonstration purposes.

## Support

For issues or questions, please open an issue on the GitHub repository.

---

**Note**: This dashboard displays demo data for illustration. Real trader tracking requires authenticated API access to Polymarket CLOB.
