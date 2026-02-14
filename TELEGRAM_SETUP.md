# 📱 Telegram Bot Setup - Complete Guide

## 🚀 What You're Building

A **mobile-first autonomous trading bot** that:
- 📱 Sends trade signals to your phone
- 🤖 Includes Claude's AI analysis
- ✅ Waits for your approval before trading
- 🔔 Real-time notifications
- 💬 Interactive commands

---

## ⚡ Quick Setup (10 Minutes)

### Step 1: Create Your Bot (5 minutes)

**On your phone (Telegram app):**

1. **Open Telegram**
2. **Search:** `@BotFather`
3. **Send:** `/newbot`
4. **Bot Name:** `Autonomous Alpha Trading Bot`
5. **Bot Username:** `autonomous_alpha_bot` (or any name ending in `_bot`)
6. **COPY THE TOKEN** (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

📝 **Save this token!**

---

### Step 2: Get Your Chat ID (2 minutes)

**Still on your phone:**

1. **Search:** `@userinfobot`
2. **Start chat** (click Start)
3. It will show your **Chat ID** (example: `123456789`)
4. **COPY THIS NUMBER**

📝 **Save this chat ID!**

---

### Step 3: Add to .env File (1 minute)

Open `/Users/atif/Desktop/AutonomousAlpha/.env`

Add these lines at the end:

```bash
# Telegram Bot
TELEGRAM_BOT_TOKEN="paste_your_token_here"
TELEGRAM_CHAT_ID="paste_your_chat_id_here"
```

**Example:**
```bash
TELEGRAM_BOT_TOKEN="7891234560:AAFdB1cxyz_abcDEFghiJKLmnoPQRstuvWX"
TELEGRAM_CHAT_ID="987654321"
```

---

### Step 4: Test It! (2 minutes)

```bash
python telegram_bot.py
```

**You should see:**
```
✅ Bot initialized!
📱 Notifications will be sent to chat ID: 987654321
🎯 Mode: DRY RUN (Simulation)
```

**On your phone:** You'll get a message: "🚀 Autonomous Alpha Started"

---

## 🎮 How to Use

### Start the Bot

```bash
# Dry run (safe, simulated trades)
python telegram_bot.py

# Live trading (real money - be careful!)
python telegram_bot.py --dry-run=False
```

### Commands (In Telegram)

Send these commands to your bot:

- `/start` - Initialize bot
- `/help` - Show all commands
- `/status` - Portfolio summary
- `/pause` - Pause trading
- `/resume` - Resume trading

---

## 📱 What Happens When Trading

### 1. Signal Detected

System detects opportunity (e.g., AAPL RSI < 30)

### 2. You Get Notification

**On your phone:**

```
🟢 BUY SIGNAL: AAPL

📊 Market Data:
• Price: $255.78
• RSI(14): 21.5
• Sentiment: Bullish
• Confidence: 85%

🤖 Claude's Analysis:
AAPL has dropped significantly below its mean.
RSI at 21.5 indicates extreme oversold conditions.
Historical data shows 78% probability of rebound
within 3-5 days. Current market sentiment remains
positive with strong fundamentals...

💰 Trade Details:
• Action: BUY 2 shares
• Est. Value: $511.56

⏰ Auto-reject in 5 minutes

[✅ Approve]  [❌ Reject]
```

### 3. You Decide

**Tap ✅ Approve** → Trade executes
**Tap ❌ Reject** → Trade cancelled
**Do nothing** → Auto-rejects after 5 minutes

### 4. Confirmation

**After approving:**

```
✅ TRADE EXECUTED

AAPL: BUY 2 shares
💰 Price: $255.78
📝 Order ID: DRY_RUN_AAPL_1234567
✓ Status: SIMULATED

Total Value: $511.56
```

---

## 🎯 Features

### Real-Time Notifications
- ✅ Trade signals with AI analysis
- ✅ Risk rejections
- ✅ Trade confirmations
- ✅ Portfolio updates

### Interactive Buttons
- ✅ Approve trades instantly
- ✅ Reject trades with one tap
- ✅ No typing required

### Smart Commands
- `/status` - Check portfolio anytime
- `/pause` - Stop trading while away
- `/resume` - Start trading again

### Safety Features
- ✅ All trades require approval
- ✅ 5-minute auto-reject timeout
- ✅ Risk checks before notifications
- ✅ Pause trading anytime

---

## 🎨 Example Workflow

**Morning:**
```
You: /start
Bot: 🚀 Autonomous Alpha Started
```

**10:30 AM:**
```
Bot: 🟢 BUY Signal for MSFT
     [Claude's analysis...]
You: *taps ✅ Approve*
Bot: ✅ Trade Executed
```

**Lunch:**
```
You: /pause
Bot: ⏸️ Trading Paused
```

**Afternoon:**
```
You: /resume
Bot: 🟢 Trading Resumed
```

**Evening:**
```
You: /status
Bot: 📊 Portfolio Summary
     💰 Value: $100,523
     📈 P&L: +$523 (0.52%)
```

---

## 🐛 Troubleshooting

### Bot doesn't respond to commands

**Problem:** Bot token is wrong
**Fix:**
1. Go to @BotFather on Telegram
2. Send `/mybots`
3. Select your bot
4. Click "API Token"
5. Copy the correct token to `.env`

### Bot sends to wrong person

**Problem:** Chat ID is wrong
**Fix:**
1. Message @userinfobot on Telegram
2. Copy YOUR chat ID (not someone else's!)
3. Update in `.env`

### "Missing Telegram credentials" error

**Problem:** .env file not updated
**Fix:**
```bash
# Check if credentials are loaded
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('Token:', os.getenv('TELEGRAM_BOT_TOKEN')[:10])
print('Chat ID:', os.getenv('TELEGRAM_CHAT_ID'))
"
```

Should show your token and chat ID. If not, check `.env` file.

### Bot sends but no response to buttons

**Problem:** Callback handler not working
**Fix:** Make sure bot is running (don't stop the script)

---

## 🎯 Pro Tips

1. **Test First:** Always start with dry-run mode
2. **Check Phone:** Make sure Telegram notifications are enabled
3. **Be Responsive:** Approvals timeout after 5 minutes
4. **Use Commands:** `/status` keeps you updated
5. **Pause When Away:** Use `/pause` if you can't approve trades

---

## 🏆 Demo This at Hackathon

**Opening:**
> "I can control this trading system from my phone. Watch..."

**Live Demo:**
1. Show your phone screen
2. Bot sends a notification
3. Tap Approve
4. Trade executes
5. Confirmation appears

**Judges:** 🤯 "That's amazing!"

---

## 🚀 You're Ready!

**Test it now:**
```bash
python telegram_bot.py
```

**Then check your phone!** 📱

You should see:
```
🚀 Autonomous Alpha Started

Mode: DRY RUN
Monitoring: AAPL, MSFT, AMZN
Status: Active 🟢
```

---

**Questions? Issues? Let me know!**

Happy trading! 📈🤖📱
