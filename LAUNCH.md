# 🚀 Launch Your Dashboard

## Quick Start

```bash
streamlit run app.py
```

The dashboard will open automatically at: **http://localhost:8501**

## 🎯 Demo Flow for Hackathon

### 1. Initial Setup (30 seconds)
```bash
cd AutonomousAlpha
streamlit run app.py
```

### 2. Walkthrough Script (2-3 minutes)

**Opening:**
> "Welcome to Autonomous Alpha - a Glass Box trading system built with Claude 4.6.
> What makes this unique is complete transparency - every decision is logged and explainable."

**Tab 1 - Live Charts:**
> "Here we have real-time market data with RSI indicators.
> The system uses mean reversion - buying when RSI < 30 (oversold),
> selling when RSI > 70 (overbought)."

**Tab 2 - Signals:**
> "The system generates trading signals in real-time.
> See here - [point to signal] - it's identified MSFT as oversold with 37% confidence.
> The rationale is fully explainable: 'RSI below 30 indicates oversold condition.'"

**Tab 3 - Risk Monitor:**
> "Before any trade executes, it goes through multi-layer risk validation.
> Notice how trades are rejected if they exceed our $1000 limit -
> this is the safety layer in action."

**Tab 4 - Audit Log:**
> "This is the Glass Box feature - complete transparency.
> Every state transition is logged with inputs, outputs, and rationale.
> You can filter by state or symbol to trace any decision."

**Sidebar Configuration:**
> "Everything is configurable - RSI thresholds, position sizes, risk limits.
> And it's in dry-run mode by default for safety."

**Live Demo:**
> "Let me start the trading system... [Click Start Trading]
> Watch as it cycles through symbols, generates signals, validates risk,
> and logs everything - all in real-time."

### 3. Key Talking Points

✅ **Transparency**: Every decision logged and explainable (Glass Box)
✅ **Safety**: Multi-layer risk management prevents bad trades
✅ **Real-Time**: Live market data from yfinance
✅ **Configurability**: Full control via UI
✅ **Production-Ready**: Integrates with Alpaca for real trading

### 4. Questions & Answers

**Q: How is this different from other trading bots?**
> A: Glass Box architecture - complete transparency and explainability.
> Most trading systems are black boxes. We log every decision with rationale.

**Q: Is it safe to use?**
> A: Yes! Multi-layer risk management, dry-run mode by default,
> and you control all parameters. Plus, it uses paper trading accounts.

**Q: How does Claude 4.6 help?**
> A: The system architecture and Glass Box logging approach
> were designed using Claude 4.6's advanced reasoning capabilities.
> The audit logs provide human-readable explanations of every decision.

**Q: Can it trade other strategies?**
> A: Absolutely! The strategy engine is modular.
> You can add new strategies by implementing a simple interface.

## 🎬 Screen Recording Tips

1. **Show the full cycle:**
   - Start with config in sidebar
   - Click "Start Trading"
   - Show signals being generated
   - Show risk validation
   - Show audit logs populating

2. **Highlight key features:**
   - Zoom into a chart
   - Expand a signal rationale
   - Filter audit logs by state
   - Show risk rejection in action

3. **End with impact:**
   - Show total positions
   - Show complete audit trail
   - Emphasize Glass Box transparency

## 🐛 Quick Fixes

### If app won't start:
```bash
pip install --upgrade streamlit plotly pandas
```

### If charts don't load:
- Check internet connection
- Verify symbols in sidebar
- Try refreshing (🔄 button)

### If data is stale:
- Click 🔄 Refresh Data button
- Or toggle Start/Stop trading

## 🎨 Customization

### Change theme:
Create `.streamlit/config.toml`:
```toml
[theme]
primaryColor="#667eea"
backgroundColor="#0e1117"
secondaryBackgroundColor="#262730"
textColor="#fafafa"
```

### Adjust refresh rate:
In `app.py`, change:
```python
time.sleep(2)  # Change this number
```

## 📝 Backup Commands

```bash
# Save current logs
cp logs/reasoning_trace.jsonl logs/backup_$(date +%Y%m%d_%H%M%S).jsonl

# Clear logs before demo
rm logs/reasoning_trace.jsonl

# Kill streamlit if stuck
pkill -f streamlit
```

## 🏆 Good Luck!

Remember: The judges care about:
1. **Innovation** - Glass Box transparency is unique
2. **Execution** - Show it working in real-time
3. **Impact** - Explainable AI in finance is huge
4. **Claude 4.6 Integration** - Highlight the design process

**You've got this! 🚀**
