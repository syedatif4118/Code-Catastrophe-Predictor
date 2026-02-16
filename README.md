# 💀 Code Catastrophe Predictor

> **Built for Anthropic Claude Code Hackathon 2026**
> Because the worst bugs are the ones you didn't think to test for.

[![Demo](https://img.shields.io/badge/Demo-Live-brightgreen)]()
[![Claude](https://img.shields.io/badge/Claude-Opus%204.6-purple)]()

---

## 🎯 The Problem

In 2012, Knight Capital lost **$440 million in 45 minutes**. A single bug.

In 2020, a typo brought down **AWS S3**, taking half the internet with it.

In 2019, **Disney+ collapsed** on launch day. Eight hours. Gone.

**Traditional testing finds what you look for. But production failures? They're creative. Multi-step. Cascading. They exploit the gaps between your tests.**

---

## 💡 The Solution

**Code Catastrophe Predictor** uses Claude Opus 4.6 to imagine how your code fails in production:

✅ **Creative Production Disasters** - Not "null pointer exception" - multi-step cascade failures
✅ **Historical Proof** - Cites real incidents that match the failure pattern
✅ **Multi-Agent Review** - 3 AI experts debate and validate each scenario
✅ **Production-Ready** - CLI tool, web interface, CI/CD integration

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements_catastrophe.txt
```

### 2. Set Your API Key

```bash
export ANTHROPIC_API_KEY="your-key-here"
```

### 3. Run the Demo

#### Web Interface (Recommended)
```bash
streamlit run catastrophe_demo.py
```

#### Command Line
```bash
python catastrophe_cli.py examples/stripe_payments.architecture.md --scenarios 5
```

---

## 🎬 Demo Video

[![Watch Demo](https://img.shields.io/badge/▶️-Watch%20Demo-red)]()

3-minute walkthrough showing real catastrophe prediction on Stripe's payment architecture.

---

## 🔥 How It Works

### 1. **Catastrophe Generation** (Opus 4.6 Adaptive Thinking)

```python
from code_catastrophe_predictor import CatastropheGenerator

generator = CatastropheGenerator()
catastrophes = generator.generate_catastrophes(
    code_description="Stripe payment processing system...",
    num_scenarios=5
)
```

**What it generates:**
- Scenario name (e.g., "The Black Friday Database Collapse")
- Step-by-step failure cascade
- Impact estimation (revenue, users, duration)
- Probability assessment
- Historical precedent (real incidents that match)

### 2. **Multi-Agent Review** (Adversarial Validation)

Three AI experts review each scenario:

🔴 **Paranoid Engineer** - Makes it worse, finds edge cases
🔧 **Debugger** - Proposes fixes and mitigations
🏆 **Production Veteran** - Validates with real-world experience

### 3. **Risk Analysis**

Automatic risk scoring based on:
- Probability distribution (high/medium/low)
- Impact severity (system-wide vs isolated)
- Historical precedent strength

---

## 📊 Real Examples

### Stripe Payment System

**Generated Scenario:** "The Black Friday Database Collapse"

**Failure Cascade:**
1. PostgreSQL hits IOPS limits during Black Friday surge
2. Write latency spikes from 50ms to 5 seconds
3. Payment processing slows to 10+ seconds
4. Cart abandonment jumps 300%
5. **$5-10M revenue loss in 2 hours**

**Historical Proof:** Cites actual 2023 Black Friday database incident

---

## 🛠️ Use Cases

### 1. Pre-Launch Review
```bash
python catastrophe_cli.py my_architecture.md --scenarios 10
```

### 2. CI/CD Integration
```yaml
# .github/workflows/catastrophe-check.yml
- name: Check for Production Catastrophes
  run: python catastrophe_cli.py architecture.md --threshold 8
```

### 3. Architecture Design Review
Run the web demo during design reviews to explore failure modes interactively.

---

## 📁 What to Test

Works best with:
- ✅ **Architecture documents** (microservices, databases, APIs)
- ✅ **Production code** (payment processing, auth systems, real-time features)
- ✅ **Infrastructure** (deployment scripts, k8s configs)

Test with our examples:
- `examples/stripe_payments.architecture.md` - Payment processing
- `examples/netflix_microservices.architecture.md` - Video streaming
- `examples/uber_realtime_pipeline.architecture.md` - Real-time GPS tracking

---

## 🎯 Why This Wins

### Novel Capability Discovery

We discovered Opus 4.6 can:
- Generate **genuinely creative** failure scenarios (not generic bugs)
- Understand **production system context** (traffic patterns, data volumes)
- Imagine **multi-step cascades** (not isolated errors)
- Think **adversarially** about edge cases

### Real-World Value

This isn't a toy demo:
- ✅ Production-ready CLI tool
- ✅ CI/CD integration ready
- ✅ Works on real architectures
- ✅ Multi-agent validation prevents false positives

---

## 📋 Requirements

- Python 3.11+
- Anthropic API key (Claude Opus 4.6)
- Streamlit (for web demo)

---

## 🏗️ Architecture

```
code_catastrophe_predictor.py  # Core engine
├── CatastropheGenerator       # Opus 4.6 scenario generation
├── CodeReviewAgents           # Multi-agent adversarial review
└── CodeCatastrophePredictor   # Main orchestrator

catastrophe_demo.py            # Streamlit web interface
catastrophe_cli.py             # Command-line tool
examples/                      # Real architecture examples
```

---

## 🚦 CLI Reference

```bash
# Generate 5 catastrophes
python catastrophe_cli.py my_code.py --scenarios 5

# With multi-agent review
python catastrophe_cli.py my_code.py --scenarios 3 --review

# Output to JSON
python catastrophe_cli.py my_code.py --scenarios 5 --output results.json

# Set minimum risk score
python catastrophe_cli.py my_code.py --threshold 7
```

---

## 📖 Documentation

- [**Quick Start**](QUICKSTART.md) - Get running in 5 minutes
- [**How It Works**](HOW_IT_WORKS.md) - Deep dive into the system
- [**CLI Guide**](CLI_GUIDE.md) - Command-line usage
- [**Integration Guide**](INTEGRATION_GUIDE.md) - CI/CD setup
- [**Code Examples**](CODE_EXAMPLES.md) - Python API usage
- [**Real World Examples**](REAL_WORLD_EXAMPLES.md) - Production architectures tested

---

## 🤝 Contributing

Built with Claude Sonnet 4.5 during the Anthropic Claude Code Hackathon 2026.

For questions or issues, open a GitHub issue.


---

## 🙏 Acknowledgments

- Anthropic for Claude Opus 4.6 and the hackathon
- Claude Sonnet 4.5 for helping build this
- Real production failures for inspiring the scenarios

---

**The worst bugs are the ones you didn't think to test for. Until now.**

💀 **Code Catastrophe Predictor** - Because production doesn't wait for your tests to be perfect.
