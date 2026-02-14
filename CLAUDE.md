# Autonomous Alpha - Governance Prompt

This document defines the Three Laws governing the Autonomous Alpha trading agent to ensure safe, transparent, and accountable autonomous operation.

## The Three Laws of Autonomous Alpha

### 1. Law of Verification
**"Never execute without validation"**

- Every trade signal MUST pass through the RiskManager validation layer
- No order shall be placed without explicit approval from risk checks
- All trades must comply with limits defined in `config/risk_limits.json`
- Position sizes, trade values, and account constraints must be verified
- In case of validation failure, the system MUST halt execution and log the violation

### 2. Law of Transparency
**"All reasoning must be observable"**

- Every state transition MUST be logged to `logs/reasoning_trace.jsonl`
- Each log entry must include: timestamp, state, inputs, outputs, and rationale
- The system operates as a Glass Box: no hidden decisions, no black box logic
- Human operators must be able to audit and understand every action taken
- Print human-readable thought process to STDOUT for real-time monitoring

### 3. Law of Isolation
**"Separate concerns, eliminate side effects"**

- StrategyEngine must be stateless and side-effect free
- Pure signal generation: market data in → trade signal out
- Risk management, execution, and data fetching are separate concerns
- Each component operates in isolation with clear interfaces
- State machine flow is deterministic: FETCH → ANALYZE → VALIDATE → EXECUTE

## Operational Constraints

### Safety Mechanisms
- Default mode: `--dry-run=True` (simulation only)
- Live trading requires explicit `--dry-run=False` flag and confirmation
- Paper trading account enforced via Alpaca configuration
- Emergency shutdown: Ctrl+C logs graceful termination

### Code Modifications
When modifying this codebase:
1. Preserve the state machine architecture
2. Maintain Glass Box logging for all new features
3. Add risk checks for any new trade logic
4. Keep components stateless where specified
5. Update audit logs when changing state transitions
6. Never bypass the RiskManager validation layer

### Monitoring
- Monitor `logs/reasoning_trace.jsonl` for audit trail
- Each JSONL entry is a complete record of a state transition
- Use tools like `jq` to query and analyze decision logs
- Example: `cat logs/reasoning_trace.jsonl | jq 'select(.state=="EXECUTE")'`

## Risk Limits Reference

Current configuration in `config/risk_limits.json`:
- Max trade value: $1,000
- Max position size: 5% of equity
- Max daily trades: 20
- Max daily loss: $5,000

**WARNING**: Modifying risk limits requires explicit review and approval.

## Strategy Configuration

### Mean Reversion Strategy (RSI-based)
- Oversold threshold: RSI < 30 → BUY signal
- Overbought threshold: RSI > 70 → SELL signal
- Position size: 10 shares (configurable)
- Indicator: 14-period RSI

To add new strategies:
1. Extend `src/strategy_engine.py` with new class
2. Ensure stateless design (no instance variables that track state)
3. Return `TradeSignal` with clear `rationale` field
4. Update main.py to use new strategy

## Emergency Procedures

### If System Misbehaves
1. Press Ctrl+C to trigger graceful shutdown
2. Review `logs/reasoning_trace.jsonl` for last known state
3. Check for risk violations or execution errors
4. Verify account status via Alpaca dashboard

### If Unauthorized Trades Occur
1. Immediately halt the system (Ctrl+C)
2. Manually close positions via Alpaca dashboard if needed
3. Review audit logs to identify root cause
4. Do not restart until issue is resolved and verified

## Compliance

This system is designed for:
- Paper trading and backtesting
- Educational purposes
- Algorithmic trading research

**NOT for:**
- Production use without extensive testing
- Unmonitored autonomous trading
- Real money without proper risk management
- Regulatory-unsupervised deployment

---

*These governance rules are binding. Any code changes must preserve these principles.*
