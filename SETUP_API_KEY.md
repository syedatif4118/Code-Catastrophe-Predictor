# 🔑 Get Your Anthropic API Key

## Quick Start (2 minutes)

### Step 1: Get API Key

1. **Go to:** https://console.anthropic.com/
2. **Sign up** or **Log in** (use Google/GitHub for fastest signup)
3. Click **"API Keys"** in the left sidebar
4. Click **"Create Key"**
5. **Name it:** "Autonomous Alpha" (or anything)
6. **Copy the key** (starts with `sk-ant-`)

⚠️ **Important:** Copy it NOW - you won't see it again!

### Step 2: Add to .env File

Open `/Users/atif/Desktop/AutonomousAlpha/.env` and replace:

```bash
ANTHROPIC_API_KEY="EMxY4vS4gzCLsrhA2Wd9r3tsbJNcpn7xj9egZjJG8Gjp"
```

With your real key:

```bash
ANTHROPIC_API_KEY="sk-ant-api03-YOUR_ACTUAL_KEY_HERE"
```

### Step 3: Test It

```bash
python -c "
import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

response = client.messages.create(
    model='claude-sonnet-4-20250514',
    max_tokens=100,
    messages=[{'role': 'user', 'content': 'Say hello in 5 words'}]
)

print('✅ API Key Working!')
print('Claude says:', response.content[0].text)
"
```

If you see "✅ API Key Working!" - you're all set!

### Step 4: Restart Streamlit

```bash
streamlit run app_enhanced.py
```

Now all AI features will work! 🎉

---

## 💰 Pricing (Don't Worry, It's Cheap!)

**Claude Sonnet 4 Pricing:**
- **Input:** $3 per 1M tokens (~750k words)
- **Output:** $15 per 1M tokens (~750k words)

**Your demo will cost:** ~$0.01-0.05 (basically free!)

**Free Credits:**
- New accounts get **$5 free credits**
- Plenty for hackathon demo + testing

---

## 🎯 What Works Now

With a valid API key, these features activate:

✅ **AI Trading Advisor Chat** (Tab 3)
- Ask any question about trading
- Get detailed explanations

✅ **News Sentiment Analysis** (Tab 2)
- Claude analyzes news headlines
- Provides trading implications

✅ **Strategy Builder** (Tab 4)
- Describe strategies in plain English
- Claude generates code

✅ **What-If Simulator** (Tab 5)
- Simulate market scenarios
- Get impact analysis

✅ **Educational Explanations** (Sidebar)
- "Explain" button works
- Trading tips from Claude

---

## 🚨 Troubleshooting

### Error: "authentication_error"
❌ **Problem:** API key is wrong or missing
✅ **Fix:** Double-check you copied the full key (starts with `sk-ant-`)

### Error: "rate_limit_error"
❌ **Problem:** Too many requests too fast
✅ **Fix:** Wait 10 seconds and try again

### Error: "insufficient_credits"
❌ **Problem:** Used up free credits
✅ **Fix:** Add payment method at console.anthropic.com (you'll get charged ~$0.01)

### Still not working?
```bash
# Check if key is loaded
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('ANTHROPIC_API_KEY')[:20])"

# Should show: sk-ant-api03-xxxxx
```

---

## 🎮 Demo Without API Key (Backup Plan)

If you can't get an API key in time for demo, you can:

**Option 1:** Use original app (no AI features)
```bash
streamlit run app.py
```

**Option 2:** Mock the responses
- Show the UI
- Say "Claude would analyze this..."
- Walk through what AI would do
- Show code instead

**Option 3:** Pre-record demo
- Get API key working
- Record video of AI responses
- Show recording during demo

---

## 💡 Pro Tips

1. **Test before demo:** Ask 2-3 questions to verify it works
2. **Have backup:** Keep original `app.py` working
3. **Monitor usage:** Check console.anthropic.com/usage
4. **Clear cache:** If weird behavior, restart Streamlit

---

**Need help? The AI features are awesome but not critical - your base system is already impressive! 🚀**
