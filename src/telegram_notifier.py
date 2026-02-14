"""
Telegram Trading Bot - Mobile notifications with approval workflow
Sends trading signals to your phone, gets approval, executes trades
"""
import asyncio
import os
from datetime import datetime
from typing import Optional, Dict
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes


class TelegramTradingBot:
    """
    Telegram bot for autonomous trading with human approval.

    Features:
    - Real-time trade notifications
    - Interactive approve/reject buttons
    - Claude's reasoning in each notification
    - Portfolio status commands
    - Pause/resume trading
    """

    def __init__(self, token: str, chat_id: str):
        """
        Initialize Telegram bot.

        Args:
            token: Bot token from @BotFather
            chat_id: Your Telegram chat ID from @userinfobot
        """
        self.token = token
        self.chat_id = chat_id
        self.bot = Bot(token=token)
        self.app = None
        self.pending_approvals: Dict[str, dict] = {}
        self.trading_paused = False

    async def initialize(self):
        """Initialize the bot application."""
        self.app = Application.builder().token(self.token).build()

        # Add command handlers
        self.app.add_handler(CommandHandler("start", self._cmd_start))
        self.app.add_handler(CommandHandler("help", self._cmd_help))
        self.app.add_handler(CommandHandler("status", self._cmd_status))
        self.app.add_handler(CommandHandler("pause", self._cmd_pause))
        self.app.add_handler(CommandHandler("resume", self._cmd_resume))

        # Add callback handler for buttons
        self.app.add_handler(CallbackQueryHandler(self._handle_approval))

        # Start the bot
        await self.app.initialize()
        await self.app.start()

    async def send_trade_signal(
        self,
        symbol: str,
        action: str,
        quantity: int,
        price: float,
        rsi: float,
        confidence: float,
        rationale: str,
        sentiment: str = "Neutral",
        timeout: int = 300  # 5 minutes
    ) -> Optional[bool]:
        """
        Send trade signal notification and wait for approval.

        Args:
            symbol: Stock symbol
            action: BUY or SELL
            quantity: Number of shares
            price: Current price
            rsi: RSI value
            confidence: Signal confidence (0-1)
            rationale: Claude's explanation
            sentiment: News sentiment
            timeout: Seconds to wait for approval

        Returns:
            True if approved, False if rejected, None if timeout
        """
        # Create unique ID for this trade
        trade_id = f"{symbol}_{action}_{datetime.now().timestamp()}"

        # Action emoji
        action_emoji = "🟢" if action == "BUY" else "🔴"

        # Format message
        message = f"""
{action_emoji} **{action} SIGNAL: {symbol}**

📊 **Market Data:**
• Price: ${price:.2f}
• RSI(14): {rsi:.1f}
• Sentiment: {sentiment}
• Confidence: {confidence:.0%}

🤖 **Claude's Analysis:**
_{rationale}_

💰 **Trade Details:**
• Action: {action} {quantity} shares
• Est. Value: ${price * quantity:.2f}

⏰ Auto-reject in {timeout // 60} minutes
        """

        # Create approval buttons
        keyboard = [
            [
                InlineKeyboardButton("✅ Approve", callback_data=f"approve_{trade_id}"),
                InlineKeyboardButton("❌ Reject", callback_data=f"reject_{trade_id}")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Send message
        await self.bot.send_message(
            chat_id=self.chat_id,
            text=message,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )

        # Store pending approval
        self.pending_approvals[trade_id] = {
            'symbol': symbol,
            'action': action,
            'quantity': quantity,
            'price': price,
            'approved': None,
            'timestamp': datetime.now()
        }

        # Wait for approval with timeout
        start_time = asyncio.get_event_loop().time()
        while True:
            await asyncio.sleep(1)

            # Check if approved/rejected
            if self.pending_approvals[trade_id]['approved'] is not None:
                result = self.pending_approvals[trade_id]['approved']
                del self.pending_approvals[trade_id]
                return result

            # Check timeout
            if asyncio.get_event_loop().time() - start_time > timeout:
                await self.send_message(
                    f"⏰ Trade timeout: {symbol} {action} auto-rejected"
                )
                del self.pending_approvals[trade_id]
                return None

    async def send_trade_confirmation(
        self,
        symbol: str,
        action: str,
        quantity: int,
        price: float,
        order_id: str,
        status: str
    ):
        """Send trade execution confirmation."""
        emoji = "✅" if status == "filled" or status == "simulated" else "⚠️"

        message = f"""
{emoji} **TRADE EXECUTED**

**{symbol}**: {action} {quantity} shares
💰 Price: ${price:.2f}
📝 Order ID: {order_id}
✓ Status: {status.upper()}

Total Value: ${price * quantity:.2f}
        """

        await self.bot.send_message(
            chat_id=self.chat_id,
            text=message,
            parse_mode='Markdown'
        )

    async def send_risk_rejection(
        self,
        symbol: str,
        action: str,
        violations: list
    ):
        """Send risk management rejection notification."""
        message = f"""
🛡️ **RISK REJECTION**

**{symbol}**: {action} signal blocked

⚠️ **Violations:**
{chr(10).join(['• ' + v for v in violations])}

Trade automatically rejected for safety.
        """

        await self.bot.send_message(
            chat_id=self.chat_id,
            text=message,
            parse_mode='Markdown'
        )

    async def send_message(self, text: str):
        """Send a simple text message."""
        await self.bot.send_message(
            chat_id=self.chat_id,
            text=text,
            parse_mode='Markdown'
        )

    async def send_daily_summary(self, summary: dict):
        """Send end-of-day portfolio summary."""
        message = f"""
📊 **DAILY SUMMARY**

💰 Portfolio: ${summary.get('equity', 0):,.2f}
📈 P&L Today: ${summary.get('pnl', 0):,.2f} ({summary.get('pnl_pct', 0):.2f}%)
📊 Trades: {summary.get('trades', 0)}

**Top Performers:**
{summary.get('top_performers', 'N/A')}

**Positions:**
{summary.get('positions', 'None')}
        """

        await self.bot.send_message(
            chat_id=self.chat_id,
            text=message,
            parse_mode='Markdown'
        )

    async def _handle_approval(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle approve/reject button clicks."""
        query = update.callback_query
        await query.answer()

        # Parse callback data
        data = query.data
        action, trade_id = data.split('_', 1)

        if trade_id in self.pending_approvals:
            if action == "approve":
                self.pending_approvals[trade_id]['approved'] = True
                await query.edit_message_text(
                    text=query.message.text + "\n\n✅ **APPROVED** - Executing trade...",
                    parse_mode='Markdown'
                )
            elif action == "reject":
                self.pending_approvals[trade_id]['approved'] = False
                await query.edit_message_text(
                    text=query.message.text + "\n\n❌ **REJECTED** - Trade cancelled",
                    parse_mode='Markdown'
                )

    # Command Handlers

    async def _cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        message = """
🎯 **Autonomous Alpha Trading Bot**

I'll send you trade signals with Claude's analysis.
You approve or reject each trade.

**Commands:**
/status - Portfolio summary
/pause - Pause trading
/resume - Resume trading
/help - Show this message

Ready to trade! 🚀
        """
        await update.message.reply_text(message, parse_mode='Markdown')

    async def _cmd_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        message = """
📚 **Available Commands**

/status - View portfolio & positions
/pause - Pause all trading
/resume - Resume trading
/help - Show this help

**How it works:**
1. System detects trading signal
2. Claude analyzes the opportunity
3. You get notification with [Approve] [Reject]
4. Click to confirm or deny
5. Trade executes automatically

🛡️ **Safety:**
• All trades require your approval
• Risk checks before every trade
• Auto-reject after 5 minutes
• Pause anytime with /pause
        """
        await update.message.reply_text(message, parse_mode='Markdown')

    async def _cmd_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command."""
        # This would fetch real portfolio data
        message = """
📊 **Portfolio Status**

💰 Value: $100,000
💵 Buying Power: $200,000
📈 Today's P&L: +$0.00 (0.00%)

**Active Positions:**
• MSFT: 2 shares @ $401.32
• AMZN: 2 shares @ $198.79

**Status:** {'⏸️ PAUSED' if self.trading_paused else '🟢 ACTIVE'}

Use /pause or /resume to control trading.
        """
        await update.message.reply_text(message, parse_mode='Markdown')

    async def _cmd_pause(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /pause command."""
        self.trading_paused = True
        await update.message.reply_text(
            "⏸️ **Trading Paused**\n\nNo new trades will be initiated.\nUse /resume to continue.",
            parse_mode='Markdown'
        )

    async def _cmd_resume(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /resume command."""
        self.trading_paused = False
        await update.message.reply_text(
            "🟢 **Trading Resumed**\n\nSystem is now active and monitoring markets.",
            parse_mode='Markdown'
        )

    async def shutdown(self):
        """Gracefully shutdown the bot."""
        if self.app:
            await self.app.stop()
            await self.app.shutdown()
