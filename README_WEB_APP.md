# 🎯 Autonomous Alpha - Web Dashboard

Beautiful, interactive web interface for the Glass Box Trading System.

## 🚀 Quick Start

```bash
# Install dependencies (if not already installed)
pip install streamlit plotly

# Run the web app
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`

## ✨ Features

### 📊 Live Charts Tab
- Real-time price charts for all symbols
- RSI(14) indicator overlay
- Interactive Plotly charts with zoom/pan
- Historical data visualization (5 days)
- Current price, RSI, and volume metrics

### 🎯 Signals Tab
- Live trading signals (BUY/SELL/HOLD)
- Signal confidence scores
- Detailed rationale for each signal
- Color-coded signal indicators

### 🛡️ Risk Monitor Tab
- Real-time risk limit tracking
- Position summary with P&L
- Risk compliance status
- Portfolio allocation breakdown

### 📝 Audit Log Tab
- Complete Glass Box transparency
- Filter by state (FETCH/ANALYZE/VALIDATE/EXECUTE)
- Filter by symbol
- JSON log viewer
- Timestamped decision trail

## ⚙️ Configuration

### Sidebar Controls:
- **Trading Universe**: Select stocks to trade
- **Strategy Parameters**:
  - RSI Oversold Threshold (default: 30)
  - RSI Overbought Threshold (default: 70)
  - Position Size (default: 2 shares)
- **Risk Management**:
  - Max Trade Value (default: $1,000)
  - Max Position % (default: 5%)
- **Trading Mode**: Dry Run / Live Trading

### Control Panel:
- ▶️ **Start/Stop Trading**: Toggle autonomous trading
- 🔄 **Refresh Data**: Manual refresh
- 🗑️ **Clear Logs**: Reset audit trail
- 🟢/🔴 **Status Indicator**: Live/Stopped

## 🎨 UI Features

### Design Elements:
- ✨ Gradient headers
- 📊 Interactive Plotly charts
- 🎨 Color-coded signals (Green=BUY, Red=SELL, Gray=HOLD)
- 📱 Responsive layout
- 🌙 Clean, modern aesthetic

### Real-Time Updates:
- Auto-refreshes when trading is active
- Live market data updates
- Real-time signal generation
- Streaming audit logs

## 🏆 Hackathon Demo Tips

### For Live Demo:
1. Start the dashboard: `streamlit run app.py`
2. Enable "Start Trading" to show real-time updates
3. Navigate through tabs to show different features
4. Highlight the Glass Box transparency in Audit Log tab
5. Show risk management in action

### Key Talking Points:
- **Transparency**: Every decision is logged and explainable
- **Risk Management**: Multi-layer validation prevents bad trades
- **Real-Time**: Live updates with actual market data
- **User Control**: Full configurability via sidebar
- **Glass Box**: Complete audit trail for accountability

## 📊 Demo Data Flow

```
User → Streamlit UI → Trading System → yfinance/Alpaca
         ↓               ↓                    ↓
    Config Panel → Strategy Engine → Market Data
         ↓               ↓                    ↓
    Risk Limits  → Risk Manager   → Validation
         ↓               ↓                    ↓
    Start/Stop   → Execution     → Orders (Simulated)
         ↓               ↓                    ↓
    Dashboard ← Audit Logger ← Glass Box Logs
```

## 🎮 Usage Examples

### Example 1: Monitor Live Signals
1. Select symbols: AAPL, MSFT, GOOGL
2. Adjust RSI thresholds if needed
3. Click "Start Trading"
4. Watch signals appear in real-time
5. Check Audit Log for full transparency

### Example 2: Backtest Strategy
1. Set dry_run = True (default)
2. Configure strategy parameters
3. Monitor performance in Risk Monitor
4. Adjust thresholds based on results

### Example 3: Risk Management Demo
1. Set low max_trade_value (e.g., $500)
2. Try to trade expensive stocks
3. Watch risk manager reject trades
4. Show violations in Audit Log

## 🐛 Troubleshooting

### App won't start:
```bash
pip install --upgrade streamlit plotly
```

### Data not loading:
- Check internet connection (yfinance needs access)
- Verify .env file has correct API keys
- Check logs/reasoning_trace.jsonl exists

### Charts not showing:
- Ensure plotly is installed
- Try refreshing the page
- Check browser console for errors

## 📱 Mobile Support

The dashboard is responsive and works on:
- 💻 Desktop (recommended)
- 📱 Tablets
- 📱 Mobile phones (limited features)

## 🎯 Next Steps

After the hackathon, consider adding:
- [ ] WebSocket for true real-time updates
- [ ] Historical performance charts
- [ ] Strategy backtesting interface
- [ ] Multi-strategy comparison
- [ ] Email/SMS alerts
- [ ] Trade execution history
- [ ] Portfolio analytics dashboard

## 📝 License

Built for Claude 4.6 Hackathon - See main project README.

---

**Happy Trading! 🚀**
