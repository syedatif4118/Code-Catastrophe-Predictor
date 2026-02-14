"""
Autonomous Alpha - Enhanced Streamlit Dashboard
With AI Advisor, News Analysis, Education Mode, NLP Strategy Builder, What-If Simulator
Built for Claude 4.6 Hackathon
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
    page_title="Autonomous Alpha - AI-Powered Trading",
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
    }
    .tooltip-box {
        background-color: #f3f4f6;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
        color: #1f2937;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        color: #1f2937;
    }
    .user-message {
        background-color: #e0e7ff;
        text-align: right;
        color: #1e40af;
    }
    .ai-message {
        background-color: #f3f4f6;
        color: #374151;
    }
    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
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
from src.ai_advisor import AITradingAdvisor
from src.news_fetcher import NewsFetcher
from src.education_helper import get_tooltip, get_onboarding_steps, get_feature_highlights
from dotenv import load_dotenv

load_dotenv()

# Initialize session state
if 'trading_active' not in st.session_state:
    st.session_state.trading_active = False
if 'market_data' not in st.session_state:
    st.session_state.market_data = {}
if 'signals' not in st.session_state:
    st.session_state.signals = {}
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'show_onboarding' not in st.session_state:
    st.session_state.show_onboarding = True
if 'onboarding_step' not in st.session_state:
    st.session_state.onboarding_step = 0
if 'ai_advisor' not in st.session_state:
    st.session_state.ai_advisor = AITradingAdvisor()
if 'news_fetcher' not in st.session_state:
    st.session_state.news_fetcher = NewsFetcher()

# Header
st.markdown('<h1 class="main-header">🎯 AUTONOMOUS ALPHA</h1>', unsafe_allow_html=True)
st.markdown("**AI-Powered Glass Box Trading System** - Built with Claude 4.6")

# Onboarding Tutorial
if st.session_state.show_onboarding and st.session_state.onboarding_step < 5:
    steps = get_onboarding_steps()
    current_step = steps[st.session_state.onboarding_step]

    with st.container():
        st.info(f"""
        ### {current_step['title']}
        {current_step['content']}

        **{current_step['action']}**
        """)

        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            if st.button("⏭️ Next" if st.session_state.onboarding_step < 4 else "🚀 Get Started"):
                st.session_state.onboarding_step += 1
                if st.session_state.onboarding_step >= 5:
                    st.session_state.show_onboarding = False
                st.rerun()
        with col2:
            if st.button("Skip Tutorial"):
                st.session_state.show_onboarding = False
                st.rerun()

    st.divider()

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
    oversold = st.slider("RSI Oversold Threshold", 10, 40, 30, help="Buy when RSI falls below this level")
    overbought = st.slider("RSI Overbought Threshold", 60, 90, 70, help="Sell when RSI rises above this level")
    position_size = st.number_input("Position Size (shares)", 1, 10, 2)

    # Risk parameters
    st.subheader("🛡️ Risk Management")
    max_trade_value = st.number_input("Max Trade Value ($)", 100, 10000, 1000)
    max_position_pct = st.slider("Max Position %", 1, 20, 5)

    # Mode selection
    st.subheader("🎮 Trading Mode")
    dry_run = st.checkbox("Dry Run (Simulation)", value=True)

    st.divider()

    # Educational Tooltips Section
    st.subheader("📚 Learn")
    concept = st.selectbox(
        "Explain a concept:",
        ["RSI", "Mean Reversion", "Position Size", "Buying Power", "Dry Run", "Signal", "Risk Management", "Confidence"]
    )

    if st.button("📖 Explain"):
        tooltip = get_tooltip(concept)
        st.markdown(f"""
        <div class="tooltip-box">
        <h4>{tooltip['name']}</h4>
        <p><strong>Simple:</strong> {tooltip['simple']}</p>
        <p><strong>Details:</strong> {tooltip['explanation']}</p>
        <p><strong>Example:</strong> {tooltip['example']}</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.caption("🏆 Built for Claude 4.6 Hackathon")

# Control Panel
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("▶️ Start" if not st.session_state.trading_active else "⏸️ Stop"):
        st.session_state.trading_active = not st.session_state.trading_active
        st.rerun()

with col2:
    if st.button("🔄 Refresh"):
        st.rerun()

with col3:
    if st.button("🗑️ Clear Logs"):
        st.session_state.chat_history = []
        log_file = Path("logs/reasoning_trace.jsonl")
        if log_file.exists():
            log_file.write_text("")
        st.success("Cleared!")

with col4:
    if st.button("🎓 Tutorial"):
        st.session_state.show_onboarding = True
        st.session_state.onboarding_step = 0
        st.rerun()

with col5:
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
        return {"equity": 100000, "buying_power": 200000, "cash": 100000}

account = asyncio.run(get_account_info())

metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
with metric_col1:
    st.metric("💰 Portfolio", f"${float(account.get('equity', 100000)):,.2f}")
with metric_col2:
    st.metric("💵 Buying Power", f"${float(account.get('buying_power', 200000)):,.2f}")
with metric_col3:
    st.metric("📊 Cash", f"${float(account.get('cash', 100000)):,.2f}")
with metric_col4:
    st.metric("📈 P&L", "$0.00", delta="0.0%")

st.divider()

# Main Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 Live Charts",
    "🎯 Signals & News",
    "🤖 AI Advisor Chat",
    "🗣️ Strategy Builder",
    "🎮 What-If Scenarios",
    "📝 Audit Log"
])

# Tab 1: Live Charts
with tab1:
    st.subheader("📊 Live Market Data & RSI Indicators")

    async def fetch_chart_data(symbol):
        try:
            mcp_client = MCPClient("config/mcp_config.json")
            market_observer = MarketObserver(mcp_client)
            market_data = await market_observer.fetch_market_data(symbol)
            historical = await mcp_client.call_tool("yfinance", "get_historical", {"symbol": symbol, "period": "5d"})
            return market_data, historical.get("historical", [])
        except Exception as e:
            st.error(f"Error: {e}")
            return None, []

    for symbol in symbols:
        with st.expander(f"📊 {symbol}", expanded=True):
            market_data, historical = asyncio.run(fetch_chart_data(symbol))

            if market_data and historical:
                df = pd.DataFrame(historical)
                df['date'] = pd.to_datetime(df['date'])

                def calc_rsi(prices, period=14):
                    deltas = pd.Series(prices).diff()
                    gains = deltas.where(deltas > 0, 0).rolling(window=period).mean()
                    losses = -deltas.where(deltas < 0, 0).rolling(window=period).mean()
                    rs = gains / losses
                    return 100 - (100 / (1 + rs))

                df['rsi'] = calc_rsi(df['close'].values)

                fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05,
                                    row_heights=[0.7, 0.3], subplot_titles=(f'{symbol} Price', 'RSI(14)'))

                fig.add_trace(go.Scatter(x=df['date'], y=df['close'], mode='lines',
                                        name='Price', line=dict(color='#667eea', width=2)), row=1, col=1)
                fig.add_trace(go.Scatter(x=df['date'], y=df['rsi'], mode='lines',
                                        name='RSI', line=dict(color='#764ba2', width=2)), row=2, col=1)

                fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
                fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)

                fig.update_layout(height=500, showlegend=True, hovermode='x unified', template='plotly_white')
                fig.update_yaxes(title_text="Price ($)", row=1, col=1)
                fig.update_yaxes(title_text="RSI", row=2, col=1)

                st.plotly_chart(fig, use_container_width=True)

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Current Price", f"${market_data.price:.2f}")
                with col2:
                    rsi_val = market_data.rsi_14 if market_data.rsi_14 else 0
                    st.metric("RSI(14)", f"{rsi_val:.2f}")
                with col3:
                    st.metric("Volume", f"{market_data.volume:,}")

# Tab 2: Signals & News
with tab2:
    st.subheader("🎯 Trading Signals with News Sentiment")

    async def generate_signals_with_news():
        signals = {}
        try:
            mcp_client = MCPClient("config/mcp_config.json")
            market_observer = MarketObserver(mcp_client)
            strategy = MeanReversionStrategy(oversold_threshold=oversold, overbought_threshold=overbought, position_size=position_size)

            for symbol in symbols:
                market_data = await market_observer.fetch_market_data(symbol)
                signal = strategy.generate_signal(market_data)

                # Fetch news
                news_items = st.session_state.news_fetcher.get_stock_news(symbol, limit=3)
                headlines = [item['title'] for item in news_items]

                # Analyze sentiment with Claude
                if headlines:
                    sentiment_analysis = st.session_state.ai_advisor.analyze_news(symbol, headlines)
                else:
                    sentiment_analysis = {"sentiment": "Neutral", "analysis": "No recent news", "news_count": 0}

                signals[symbol] = {
                    'signal': signal,
                    'market_data': market_data,
                    'news': news_items,
                    'sentiment': sentiment_analysis
                }
        except Exception as e:
            st.error(f"Error: {e}")

        return signals

    with st.spinner("Analyzing markets and news..."):
        signals = asyncio.run(generate_signals_with_news())

    for symbol, data in signals.items():
        signal = data['signal']
        market_data = data['market_data']
        news = data['news']
        sentiment = data['sentiment']

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
            sent_color = "🟢" if sentiment['sentiment'] == "Bullish" else "🔴" if sentiment['sentiment'] == "Bearish" else "⚪"
            st.write(f"{sent_color} Sentiment: **{sentiment['sentiment']}**")

        with col4:
            if signal:
                st.write(f"**Conf:** {signal.confidence:.1%}")

        # Expandable details
        with st.expander(f"📰 View News & Analysis for {symbol}"):
            col_a, col_b = st.columns(2)

            with col_a:
                st.markdown("**Recent News:**")
                for item in news[:3]:
                    st.markdown(f"• {item['title']}")

            with col_b:
                st.markdown("**AI Sentiment Analysis:**")
                st.info(sentiment['analysis'][:300] + "...")

            if signal:
                st.markdown("**Signal Rationale:**")
                st.success(signal.rationale)

        st.divider()

# Tab 3: AI Advisor Chat
with tab3:
    st.subheader("🤖 AI Trading Advisor - Chat with Claude 4.6")

    st.info("💡 **Ask me anything!** Try: 'Why did you buy MSFT?' or 'Explain RSI' or 'What if interest rates rise?'")

    # Chat interface
    user_question = st.text_input("Your question:", placeholder="e.g., Why did you generate that signal?", key="chat_input")

    if st.button("Ask AI Advisor") and user_question:
        with st.spinner("Claude is thinking..."):
            # Get context
            context = {
                "symbols": ", ".join(symbols),
                "mode": "Dry Run" if dry_run else "Live Trading"
            }

            answer = st.session_state.ai_advisor.ask(user_question, context)
            st.session_state.chat_history.append({"question": user_question, "answer": answer})

    # Display chat history
    for i, chat in enumerate(reversed(st.session_state.chat_history[-10:])):
        st.markdown(f"""
        <div class="chat-message user-message">
        <strong>You:</strong> {chat['question']}
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="chat-message ai-message">
        <strong>🤖 Claude:</strong> {chat['answer']}
        </div>
        """, unsafe_allow_html=True)

    # Quick questions
    st.markdown("### 🚀 Quick Questions")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📚 Explain RSI"):
            answer = st.session_state.ai_advisor.explain_concept("RSI")
            st.info(answer)

    with col2:
        if st.button("🎯 Why this strategy?"):
            answer = st.session_state.ai_advisor.explain_concept("Mean Reversion")
            st.info(answer)

    with col3:
        if st.button("💡 Trading Tip"):
            tip = st.session_state.ai_advisor.get_educational_tip()
            st.success(tip)

# Tab 4: NLP Strategy Builder
with tab4:
    st.subheader("🗣️ Natural Language Strategy Builder")

    st.markdown("""
    **Describe your trading strategy in plain English**, and Claude will generate the code for you!

    Examples:
    - "Buy stocks when they're oversold and have positive momentum"
    - "Sell when price breaks below 50-day moving average"
    - "Buy value stocks with strong fundamentals"
    """)

    strategy_description = st.text_area(
        "Describe your strategy:",
        placeholder="e.g., Buy stocks that have been falling for 3 days but have strong fundamentals...",
        height=100
    )

    if st.button("🚀 Generate Strategy") and strategy_description:
        with st.spinner("Claude is generating your strategy..."):
            result = st.session_state.ai_advisor.generate_strategy_from_nlp(strategy_description)

            st.success("✅ Strategy Generated!")
            st.markdown("### Implementation")
            st.code(result['implementation'], language='python')

            st.info("💡 **Next Steps:** Copy this code to `src/strategy_engine.py` and test it in dry-run mode!")

# Tab 5: What-If Scenarios
with tab5:
    st.subheader("🎮 What-If Scenario Simulator")

    st.markdown("**Ask Claude to simulate market scenarios and analyze their impact on your portfolio.**")

    scenario_templates = [
        "Market drops 20% tomorrow",
        "Interest rates rise by 2%",
        "Tech sector crashes 30%",
        "AAPL announces bad earnings",
        "Global recession starts",
        "Custom scenario..."
    ]

    scenario_choice = st.selectbox("Select a scenario:", scenario_templates)

    if scenario_choice == "Custom scenario...":
        scenario = st.text_input("Describe your scenario:")
    else:
        scenario = scenario_choice

    if st.button("🎯 Analyze Scenario") and scenario:
        with st.spinner("Claude is analyzing the scenario..."):
            portfolio_context = {
                "equity": float(account.get('equity', 100000)),
                "positions": ", ".join(symbols),
                "strategy": "Mean Reversion (RSI-based)"
            }

            analysis = st.session_state.ai_advisor.what_if_scenario(scenario, portfolio_context)

            st.markdown("### 📊 Scenario Analysis")
            st.info(analysis)

    st.markdown("### 💡 Popular Scenarios")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("📉 Market Crash (-20%)"):
            analysis = st.session_state.ai_advisor.what_if_scenario(
                "Market drops 20% across all sectors",
                {"equity": float(account.get('equity', 100000)), "positions": ", ".join(symbols)}
            )
            st.warning(analysis)

    with col2:
        if st.button("📈 Bull Run (+15%)"):
            analysis = st.session_state.ai_advisor.what_if_scenario(
                "Market rallies 15% driven by tech stocks",
                {"equity": float(account.get('equity', 100000)), "positions": ", ".join(symbols)}
            )
            st.success(analysis)

# Tab 6: Audit Log
with tab6:
    st.subheader("📝 Glass Box Audit Log")

    col1, col2, col3 = st.columns(3)
    with col1:
        filter_state = st.selectbox("Filter by State", ["ALL", "FETCH", "ANALYZE", "VALIDATE", "EXECUTE"])
    with col2:
        filter_symbol = st.selectbox("Filter by Symbol", ["ALL"] + symbols)
    with col3:
        max_entries = st.slider("Max Entries", 10, 100, 50)

    log_file = Path("logs/reasoning_trace.jsonl")
    if log_file.exists():
        logs = []
        with open(log_file, 'r') as f:
            for line in f:
                try:
                    log = json.loads(line)
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

        logs = logs[-max_entries:][::-1]

        for log in logs:
            state = log.get("state", "UNKNOWN")
            timestamp = log.get("timestamp", "")
            rationale = log.get("rationale", "")

            with st.expander(f"🔍 [{state}] {timestamp[:19]} - {rationale[:80]}..."):
                st.markdown(f"**State:** `{state}`")
                st.markdown(f"**Rationale:** {rationale}")
                st.json(log, expanded=False)
    else:
        st.info("No logs yet. Start trading to generate audit trail!")

# Auto-refresh
if st.session_state.trading_active:
    time.sleep(2)
    st.rerun()

# Footer
st.divider()
highlights = get_feature_highlights()
cols = st.columns(len(highlights))
for i, feature in enumerate(highlights):
    with cols[i]:
        st.markdown(f"""
        <div style='text-align: center;'>
        <h1>{feature['icon']}</h1>
        <h4>{feature['title']}</h4>
        <p style='font-size: 0.9rem;'>{feature['description']}</p>
        </div>
        """, unsafe_allow_html=True)

st.divider()
st.markdown("""
<div style='text-align: center; color: #6b7280;'>
    <p>🏆 <strong>Autonomous Alpha</strong> - AI-Powered Glass Box Trading System</p>
    <p>Built with Claude 4.6 for Anthropic Hackathon | Powered by yfinance & Alpaca</p>
</div>
""", unsafe_allow_html=True)
