# Autonomous Alpha - Glass Box Trading Agent

A production-ready, deterministic trading agent with full transparency and accountability. Built for Apple M4 silicon with Python 3.12.

## Architecture

**Deterministic State Machine**: `FETCH → ANALYZE → VALIDATE → EXECUTE`

Every transition is logged with complete reasoning transparency (Glass Box design).

## Key Features

- ✅ **Glass Box Logging**: All decisions logged to `logs/reasoning_trace.jsonl`
- ✅ **Strict Type Safety**: Full Pydantic validation on all data structures
- ✅ **Risk Management**: Multi-layer validation before execution
- ✅ **Stateless Strategy Engine**: Pure functional signal generation
- ✅ **MCP Integration**: Ready for Model Context Protocol servers
- ✅ **Dry-Run Mode**: Safe testing with simulated execution (default)

## System Components

### Core Modules

- **`src/models.py`**: Pydantic models for strict typing
- **`src/mcp_client.py`**: MCP server wrapper for AlphaVantage + Alpaca
- **`src/market_observer.py`**: Fetch market data and calculate RSI
- **`src/strategy_engine.py`**: Mean reversion strategy (RSI-based)
- **`src/risk_manager.py`**: Multi-factor risk validation
- **`src/execution_gateway.py`**: Order execution interface
- **`src/audit_logger.py`**: Glass Box JSONL logging

### Configuration

- **`config/mcp_config.json`**: MCP server endpoints and credentials
- **`config/risk_limits.json`**: Trading risk parameters
- **`config/trading_universe.csv`**: List of symbols to trade

### Governance

- **`CLAUDE.md`**: Three Laws of Autonomous Alpha (read this!)

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` (already done) and verify credentials:

```bash
cat .env
```

### 3. Run in Dry-Run Mode (Safe)

```bash
python main.py
```

This will:
- Fetch market data for AAPL, TSLA, GOOGL
- Generate trading signals using RSI(14)
- Validate against risk limits
- **Simulate** execution (no real orders)
- Log everything to `logs/reasoning_trace.jsonl`

### 4. Monitor Logs

```bash
# Watch live logs
tail -f logs/reasoning_trace.jsonl | jq .

# Query specific states
cat logs/reasoning_trace.jsonl | jq 'select(.state=="EXECUTE")'
```

## Strategy Details

### Mean Reversion (RSI-based)

**Rules**:
- RSI(14) < 30 → **BUY** signal (oversold)
- RSI(14) > 70 → **SELL** signal (overbought)
- Otherwise → **HOLD**

**Parameters**:
- Position size: 10 shares
- Confidence: Scaled by distance from threshold

## Risk Management

All trades validated against:

1. **Max Trade Value**: $1,000 per trade
2. **Position Size Limit**: 5% of total equity
3. **Buying Power Check**: Sufficient cash for BUY orders
4. **Position Validation**: Sufficient shares for SELL orders

Risk limits defined in `config/risk_limits.json`.

## Glass Box Transparency

Every state transition creates a log entry:

```json
{
  "timestamp": "2025-01-14T12:00:00Z",
  "state": "ANALYZE",
  "inputs": { "market_data": {...} },
  "outputs": { "signal": {...} },
  "rationale": "RSI(28.5) < 30 indicates oversold...",
  "duration_ms": 1.23
}
```

**Key Principle**: No hidden decisions. All reasoning is auditable.

## Safety Features

### Default: Dry-Run Mode

```bash
python main.py              # Safe simulation
python main.py --dry-run    # Explicit dry-run
```

### Live Trading (Use with Caution)

```bash
python main.py --dry-run=False  # Requires confirmation
```

### Emergency Stop

Press `Ctrl+C` to trigger graceful shutdown with logged termination.

## Governance (Three Laws)

See `CLAUDE.md` for complete governance rules:

1. **Law of Verification**: Never execute without validation
2. **Law of Transparency**: All reasoning must be observable
3. **Law of Isolation**: Stateless components, no side effects

## Development

### Run Tests

```bash
pytest tests/
```

### Add New Strategy

1. Create new class in `src/strategy_engine.py`
2. Implement `generate_signal(market_data) -> TradeSignal`
3. Ensure stateless design
4. Update `main.py` to use new strategy

### Modify Risk Limits

Edit `config/risk_limits.json` (requires review per CLAUDE.md).

## Project Structure

```
AutonomousAlpha/
├── main.py                    # Main orchestrator
├── CLAUDE.md                  # Governance rules
├── README.md                  # This file
├── requirements.txt           # Dependencies
├── .env                       # API credentials (not in git)
├── config/
│   ├── mcp_config.json       # MCP server config
│   ├── risk_limits.json      # Risk parameters
│   └── trading_universe.csv  # Symbols to trade
├── logs/
│   └── reasoning_trace.jsonl # Glass Box audit log
├── src/
│   ├── models.py             # Pydantic models
│   ├── mcp_client.py         # MCP wrapper
│   ├── market_observer.py    # Data fetching
│   ├── strategy_engine.py    # Signal generation
│   ├── risk_manager.py       # Risk validation
│   ├── execution_gateway.py  # Order execution
│   └── audit_logger.py       # Glass Box logger
└── tests/                    # Test suite

```

## API Credentials

This system requires:

- **Alpaca API** (paper trading): Get keys at [alpaca.markets](https://alpaca.markets)
- **AlphaVantage API**: Get key at [alphavantage.co](https://www.alphavantage.co)

Already configured in `.env` file.

## Compliance Notice

This system is designed for:
- 📊 Paper trading and backtesting
- 🎓 Educational purposes
- 🔬 Algorithmic trading research

**NOT for**:
- ❌ Production use without extensive testing
- ❌ Unmonitored autonomous trading
- ❌ Real money without proper risk management

## License

Proprietary - For authorized use only.

## Support

For issues or questions, review:
1. `CLAUDE.md` for governance rules
2. `logs/reasoning_trace.jsonl` for system behavior
3. This README for usage instructions

---

**Built with Glass Box principles: Transparent, Auditable, Deterministic**
