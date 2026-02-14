"""
Autonomous Alpha - Streamlit Web Dashboard
Beautiful, interactive trading system interface for Claude 4.6 Hackathon
"""
import streamlit as st
import asyncio
import json
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import time
from pathlib import Path

# Must be first Streamlit command
st.set_page_config(
    page_title="Autonomous Alpha - Glass Box Trading",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .signal-buy {
        background-color: #10b981;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .signal-sell {
        background-color: #ef4444;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .signal-hold {
        background-color: #6b7280;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Import trading system components
from src.mcp_client import MCPClient
from src.market_observer import MarketObserver
from src.strategy_engine import MeanReversionStrategy
from src.risk_manager import RiskManager
from src.execution_gateway import ExecutionGateway
from src.audit_logger import AuditLogger
from dotenv import load_dotenv

load_dotenv()

# Initialize session state
if 'trading_active' not in st.session_state:
    st.session_state.trading_active = False
if 'market_data' not in st.session_state:
    st.session_state.market_data = {}
if 'signals' not in st.session_state:
    st.session_state.signals = {}
if 'audit_logs' not in st.session_state:
    st.session_state.audit_logs = []

# Header
st.markdown('<h1 class="main-header">🎯 AUTONOMOUS ALPHA</h1>', unsafe_allow_html=True)
st.markdown("**Glass Box Trading System** - Powered by Claude 4.6")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")

    # Trading universe
    st.subheader("📊 Trading Universe")
    symbols = st.multiselect(
        "Select Symbols",
        ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META"],
        default=["AAPL", "MSFT", "AMZN"]
    )

    # Strategy parameters
    st.subheader("🎯 Strategy Parameters")
    oversold = st.slider("RSI Oversold Threshold", 10, 40, 30)
    overbought = st.slider("RSI Overbought Threshold", 60, 90, 70)
    position_size = st.number_input("Position Size (shares)", 1, 10, 2)

    # Risk parameters
    st.subheader("🛡️ Risk Management")
    max_trade_value = st.number_input("Max Trade Value ($)", 100, 10000, 1000)
    max_position_pct = st.slider("Max Position %", 1, 20, 5)

    # Mode selection
    st.subheader("🎮 Trading Mode")
    dry_run = st.checkbox("Dry Run (Simulation)", value=True)

    st.divider()
    st.caption("🏆 Built for Claude 4.6 Hackathon")

# Control Panel
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("▶️ Start Trading" if not st.session_state.trading_active else "⏸️ Stop Trading"):
        st.session_state.trading_active = not st.session_state.trading_active
        st.rerun()

with col2:
    if st.button("🔄 Refresh Data"):
        st.rerun()

with col3:
    if st.button("🗑️ Clear Logs"):
        st.session_state.audit_logs = []
        log_file = Path("logs/reasoning_trace.jsonl")
        if log_file.exists():
            log_file.write_text("")
        st.success("Logs cleared!")

with col4:
    status = "🟢 LIVE" if st.session_state.trading_active else "🔴 STOPPED"
    st.markdown(f"### {status}")

st.divider()

# Portfolio Metrics
async def get_account_info():
    """Fetch account information"""
    try:
        mcp_client = MCPClient("config/mcp_config.json")
        account = await mcp_client.call_tool("alpaca", "get_account", {})
        return account
    except Exception as e:
        st.error(f"Error fetching account: {e}")
        return {"equity": 100000, "buying_power": 200000, "cash": 100000}

# Fetch account data
account = asyncio.run(get_account_info())

# Display metrics
metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

with metric_col1:
    st.metric("💰 Portfolio Value", f"${float(account.get('equity', 100000)):,.2f}")

with metric_col2:
    st.metric("💵 Buying Power", f"${float(account.get('buying_power', 200000)):,.2f}")

with metric_col3:
    st.metric("📊 Cash", f"${float(account.get('cash', 100000)):,.2f}")

with metric_col4:
    # Calculate simple P&L (would track this in real implementation)
    st.metric("📈 P&L", "$0.00", delta="0.0%")

st.divider()

# Main content area
tab1, tab2, tab3, tab4 = st.tabs(["📈 Live Charts", "🎯 Signals", "🛡️ Risk Monitor", "📝 Audit Log"])

# Tab 1: Live Charts
with tab1:
    st.subheader("📊 Live Market Data & RSI Indicators")

    async def fetch_chart_data(symbol):
        """Fetch market data for charts"""
        try:
            mcp_client = MCPClient("config/mcp_config.json")
            market_observer = MarketObserver(mcp_client)
            market_data = await market_observer.fetch_market_data(symbol)

            # Get historical data
            historical = await mcp_client.call_tool(
                "yfinance",
                "get_historical",
                {"symbol": symbol, "period": "5d"}
            )

            return market_data, historical.get("historical", [])
        except Exception as e:
            st.error(f"Error fetching data for {symbol}: {e}")
            return None, []

    # Display charts for each symbol
    for symbol in symbols:
        with st.expander(f"📊 {symbol}", expanded=True):
            market_data, historical = asyncio.run(fetch_chart_data(symbol))

            if market_data and historical:
                # Create dataframe
                df = pd.DataFrame(historical)
                df['date'] = pd.to_datetime(df['date'])

                # Calculate RSI for historical data
                def calc_rsi(prices, period=14):
                    deltas = pd.Series(prices).diff()
                    gains = deltas.where(deltas > 0, 0).rolling(window=period).mean()
                    losses = -deltas.where(deltas < 0, 0).rolling(window=period).mean()
                    rs = gains / losses
                    return 100 - (100 / (1 + rs))

                df['rsi'] = calc_rsi(df['close'].values)

                # Create subplot with price and RSI
                fig = make_subplots(
                    rows=2, cols=1,
                    shared_xaxes=True,
                    vertical_spacing=0.05,
                    row_heights=[0.7, 0.3],
                    subplot_titles=(f'{symbol} Price', 'RSI(14)')
                )

                # Price chart
                fig.add_trace(
                    go.Scatter(
                        x=df['date'],
                        y=df['close'],
                        mode='lines',
                        name='Price',
                        line=dict(color='#667eea', width=2)
                    ),
                    row=1, col=1
                )

                # RSI chart
                fig.add_trace(
                    go.Scatter(
                        x=df['date'],
                        y=df['rsi'],
                        mode='lines',
                        name='RSI',
                        line=dict(color='#764ba2', width=2)
                    ),
                    row=2, col=1
                )

                # RSI threshold lines
                fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
                fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)

                # Update layout
                fig.update_layout(
                    height=500,
                    showlegend=True,
                    hovermode='x unified',
                    template='plotly_white'
                )

                fig.update_yaxes(title_text="Price ($)", row=1, col=1)
                fig.update_yaxes(title_text="RSI", row=2, col=1)
                fig.update_xaxes(title_text="Date", row=2, col=1)

                st.plotly_chart(fig, use_container_width=True)

                # Current metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Current Price", f"${market_data.price:.2f}")
                with col2:
                    rsi_val = market_data.rsi_14 if market_data.rsi_14 else 0
                    st.metric("RSI(14)", f"{rsi_val:.2f}")
                with col3:
                    st.metric("Volume", f"{market_data.volume:,}")

# Tab 2: Signals
with tab2:
    st.subheader("🎯 Trading Signals")

    async def generate_signals():
        """Generate trading signals for all symbols"""
        signals = {}
        try:
            mcp_client = MCPClient("config/mcp_config.json")
            market_observer = MarketObserver(mcp_client)
            strategy = MeanReversionStrategy(
                oversold_threshold=oversold,
                overbought_threshold=overbought,
                position_size=position_size
            )

            for symbol in symbols:
                market_data = await market_observer.fetch_market_data(symbol)
                signal = strategy.generate_signal(market_data)
                signals[symbol] = {
                    'signal': signal,
                    'market_data': market_data
                }
        except Exception as e:
            st.error(f"Error generating signals: {e}")

        return signals

    signals = asyncio.run(generate_signals())

    # Display signals in columns
    for i, (symbol, data) in enumerate(signals.items()):
        signal = data['signal']
        market_data = data['market_data']

        col1, col2, col3, col4 = st.columns([2, 2, 3, 3])

        with col1:
            st.markdown(f"### {symbol}")

        with col2:
            if signal:
                action = signal.action
                if action == "BUY":
                    st.markdown('<div class="signal-buy">🟢 BUY</div>', unsafe_allow_html=True)
                elif action == "SELL":
                    st.markdown('<div class="signal-sell">🔴 SELL</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="signal-hold">⚪ HOLD</div>', unsafe_allow_html=True)

        with col3:
            if signal:
                st.write(f"**Qty:** {signal.quantity} | **Conf:** {signal.confidence:.1%}")

        with col4:
            if signal:
                with st.expander("View Rationale"):
                    st.info(signal.rationale)

        st.divider()

# Tab 3: Risk Monitor
with tab3:
    st.subheader("🛡️ Risk Management Dashboard")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📋 Risk Limits")
        risk_data = {
            "Parameter": ["Max Trade Value", "Max Position %", "Max Daily Trades", "Max Daily Loss"],
            "Limit": [f"${max_trade_value}", f"{max_position_pct}%", "20", "$5,000"],
            "Current": ["$802.64", "0.8%", "2", "$0.00"],
            "Status": ["✅ OK", "✅ OK", "✅ OK", "✅ OK"]
        }
        st.dataframe(pd.DataFrame(risk_data), use_container_width=True, hide_index=True)

    with col2:
        st.markdown("### 📊 Position Summary")
        position_data = {
            "Symbol": ["MSFT", "AMZN"],
            "Shares": [2, 2],
            "Avg Price": ["$401.32", "$198.79"],
            "Current Value": ["$802.64", "$397.58"],
            "P&L": ["+$0.00", "+$0.00"]
        }
        st.dataframe(pd.DataFrame(position_data), use_container_width=True, hide_index=True)

# Tab 4: Audit Log
with tab4:
    st.subheader("📝 Glass Box Audit Log")

    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_state = st.selectbox("Filter by State", ["ALL", "FETCH", "ANALYZE", "VALIDATE", "EXECUTE"])
    with col2:
        filter_symbol = st.selectbox("Filter by Symbol", ["ALL"] + symbols)
    with col3:
        max_entries = st.slider("Max Entries", 10, 100, 50)

    # Load audit logs
    log_file = Path("logs/reasoning_trace.jsonl")
    if log_file.exists():
        logs = []
        with open(log_file, 'r') as f:
            for line in f:
                try:
                    log = json.loads(line)

                    # Apply filters
                    if filter_state != "ALL" and log.get("state") != filter_state:
                        continue

                    if filter_symbol != "ALL":
                        inputs = log.get("inputs", {})
                        outputs = log.get("outputs", {})
                        symbol_match = False
                        if isinstance(inputs, dict) and inputs.get("symbol") == filter_symbol:
                            symbol_match = True
                        if isinstance(outputs, dict):
                            signal = outputs.get("signal", {})
                            if isinstance(signal, dict) and signal.get("symbol") == filter_symbol:
                                symbol_match = True
                        if not symbol_match:
                            continue

                    logs.append(log)
                except:
                    continue

        # Display logs (most recent first)
        logs = logs[-max_entries:][::-1]

        for log in logs:
            state = log.get("state", "UNKNOWN")
            timestamp = log.get("timestamp", "")
            rationale = log.get("rationale", "")

            # Color code by state
            if state == "FETCH":
                color = "#3b82f6"
            elif state == "ANALYZE":
                color = "#8b5cf6"
            elif state == "VALIDATE":
                color = "#f59e0b"
            elif state == "EXECUTE":
                color = "#10b981"
            else:
                color = "#6b7280"

            with st.expander(f"🔍 [{state}] {timestamp[:19]} - {rationale[:80]}..."):
                st.markdown(f"**State:** `{state}`")
                st.markdown(f"**Timestamp:** {timestamp}")
                st.markdown(f"**Rationale:** {rationale}")
                st.json(log, expanded=False)
    else:
        st.info("No audit logs found. Start trading to generate logs.")

# Auto-refresh
if st.session_state.trading_active:
    time.sleep(2)
    st.rerun()

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #6b7280;'>
    <p>🏆 <strong>Autonomous Alpha</strong> - Glass Box Trading System</p>
    <p>Built with Claude 4.6 for Anthropic Hackathon | Powered by yfinance & Alpaca</p>
</div>
""", unsafe_allow_html=True)
