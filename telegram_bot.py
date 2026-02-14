"""
Autonomous Alpha - Telegram Trading Bot
Run this alongside your trading system for mobile notifications
"""
import asyncio
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, os.path.dirname(__file__))

from src.telegram_notifier import TelegramTradingBot
from src.mcp_client import MCPClient
from src.market_observer import MarketObserver
from src.strategy_engine import MeanReversionStrategy
from src.risk_manager import RiskManager
from src.execution_gateway import ExecutionGateway
from src.audit_logger import AuditLogger
from src.ai_advisor import AITradingAdvisor
from src.news_fetcher import NewsFetcher

load_dotenv()


class AutonomousAlphaBot:
    """
    Autonomous trading system with Telegram notifications.
    Runs trading loop, sends signals to phone, waits for approval.
    """

    def __init__(self, dry_run: bool = True):
        # Load credentials
        telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
        telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")

        if not telegram_token or not telegram_chat_id:
            raise ValueError(
                "Missing Telegram credentials!\n"
                "Add to .env:\n"
                "TELEGRAM_BOT_TOKEN=your_token\n"
                "TELEGRAM_CHAT_ID=your_chat_id"
            )

        # Initialize components
        self.telegram = TelegramTradingBot(telegram_token, telegram_chat_id)
        self.mcp_client = MCPClient("config/mcp_config.json")
        self.market_observer = MarketObserver(self.mcp_client)
        self.strategy = MeanReversionStrategy()
        self.risk_manager = RiskManager(self.mcp_client, "config/risk_limits.json")
        self.executor = ExecutionGateway(self.mcp_client, dry_run=dry_run)
        self.auditor = AuditLogger("logs/reasoning_trace.jsonl")
        self.ai_advisor = AITradingAdvisor()
        self.news_fetcher = NewsFetcher()

        self.dry_run = dry_run
        self.universe = ["AAPL", "MSFT", "AMZN"]  # Can load from config

    async def start(self):
        """Start the bot and trading system."""
        print("🤖 Initializing Telegram bot...")
        await self.telegram.initialize()

        print("✅ Bot initialized!")
        print(f"📱 Notifications will be sent to chat ID: {os.getenv('TELEGRAM_CHAT_ID')}")
        print(f"🎯 Mode: {'DRY RUN (Simulation)' if self.dry_run else 'LIVE TRADING'}")
        print()

        # Send startup message
        await self.telegram.send_message(
            f"🚀 **Autonomous Alpha Started**\n\n"
            f"Mode: {'DRY RUN' if self.dry_run else 'LIVE'}\n"
            f"Monitoring: {', '.join(self.universe)}\n"
            f"Status: Active 🟢"
        )

        # Start trading loop
        await self.trading_loop()

    async def process_symbol(self, symbol: str):
        """Process one symbol through the trading pipeline."""
        try:
            # Check if trading is paused
            if self.telegram.trading_paused:
                return

            # FETCH - Get market data
            print(f"\n📊 Fetching data for {symbol}...")
            market_data = await self.market_observer.fetch_market_data(symbol)

            self.auditor.log_transition(
                state="FETCH",
                inputs={"symbol": symbol},
                outputs={"market_data": market_data},
                rationale=f"Fetched market data for {symbol}"
            )

            # ANALYZE - Generate signal
            print(f"🔍 Analyzing {symbol}...")
            signal = self.strategy.generate_signal(market_data)

            if not signal:
                print(f"⚪ {symbol}: HOLD (no signal)")
                return

            print(f"🎯 {symbol}: {signal.action} signal generated!")

            # Get news sentiment
            news = self.news_fetcher.get_stock_news(symbol, limit=3)
            headlines = [item['title'] for item in news] if news else []

            sentiment_analysis = self.ai_advisor.analyze_news(symbol, headlines) if headlines else {
                "sentiment": "Neutral",
                "analysis": "No recent news available"
            }

            sentiment = sentiment_analysis['sentiment']

            self.auditor.log_transition(
                state="ANALYZE",
                inputs={"market_data": market_data},
                outputs={"signal": signal, "sentiment": sentiment},
                rationale=signal.rationale
            )

            # VALIDATE - Risk check
            print(f"🛡️ Running risk checks...")
            risk_result = await self.risk_manager.validate_signal(signal, market_data.price)

            self.auditor.log_transition(
                state="VALIDATE",
                inputs={"signal": signal},
                outputs={"risk_result": risk_result},
                rationale=f"Risk validation: {'approved' if risk_result.approved else 'rejected'}"
            )

            if not risk_result.approved:
                print(f"❌ {symbol}: Risk rejected - {', '.join(risk_result.violations)}")

                # Send rejection notification
                await self.telegram.send_risk_rejection(
                    symbol=symbol,
                    action=signal.action,
                    violations=risk_result.violations
                )
                return

            # APPROVE - Send to Telegram and wait for approval
            print(f"📱 Sending approval request to Telegram...")

            # Get enhanced explanation from Claude
            enhanced_rationale = self.ai_advisor.explain_signal({
                'symbol': symbol,
                'action': signal.action,
                'rsi': market_data.rsi_14,
                'price': float(market_data.price),
                'confidence': signal.confidence
            })

            # Send notification and wait for approval
            approved = await self.telegram.send_trade_signal(
                symbol=symbol,
                action=signal.action,
                quantity=signal.quantity,
                price=float(market_data.price),
                rsi=market_data.rsi_14,
                confidence=signal.confidence,
                rationale=enhanced_rationale[:500],  # Limit length
                sentiment=sentiment,
                timeout=300  # 5 minutes
            )

            if approved is None:
                print(f"⏰ {symbol}: Approval timeout")
                return
            elif not approved:
                print(f"❌ {symbol}: User rejected")
                return

            print(f"✅ {symbol}: User approved! Executing...")

            # EXECUTE - Place order
            order_result = await self.executor.execute_signal(signal, market_data.price)

            self.auditor.log_transition(
                state="EXECUTE",
                inputs={"signal": signal, "approved": True},
                outputs={"order_result": order_result},
                rationale=f"Executed {signal.action} order after user approval"
            )

            # Send confirmation
            await self.telegram.send_trade_confirmation(
                symbol=symbol,
                action=signal.action,
                quantity=signal.quantity,
                price=float(market_data.price),
                order_id=order_result.order_id,
                status=order_result.status
            )

            print(f"🎉 {symbol}: Trade complete!")

        except Exception as e:
            print(f"❌ Error processing {symbol}: {e}")
            await self.telegram.send_message(f"⚠️ Error with {symbol}: {str(e)}")

    async def trading_loop(self):
        """Main trading loop."""
        cycle = 0

        try:
            while True:
                cycle += 1
                print(f"\n{'='*60}")
                print(f"📈 Trading Cycle #{cycle} - {datetime.now().strftime('%H:%M:%S')}")
                print(f"{'='*60}")

                # Process each symbol
                for symbol in self.universe:
                    await self.process_symbol(symbol)

                # Wait before next cycle
                print(f"\n⏰ Cycle complete. Next cycle in 60 seconds...")
                await asyncio.sleep(60)

        except KeyboardInterrupt:
            print("\n\n🛑 Shutting down...")
            await self.telegram.send_message("🛑 **Bot Stopped**\n\nTrading system shut down.")
            await self.telegram.shutdown()


async def main():
    """Entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Autonomous Alpha Telegram Bot")
    parser.add_argument(
        '--dry-run',
        type=lambda x: x.lower() != 'false',
        default=True,
        help='Run in dry-run mode (default: True)'
    )

    args = parser.parse_args()

    print("="*60)
    print("  🤖 AUTONOMOUS ALPHA - TELEGRAM BOT")
    print("="*60)
    print(f"Mode: {'DRY RUN (Safe)' if args.dry_run else 'LIVE TRADING ⚠️'}")
    print("="*60)
    print()

    if not args.dry_run:
        response = input("⚠️  WARNING: Live trading enabled. Continue? (yes/no): ")
        if response.lower() != 'yes':
            print("Exiting...")
            return

    bot = AutonomousAlphaBot(dry_run=args.dry_run)
    await bot.start()


if __name__ == "__main__":
    asyncio.run(main())
