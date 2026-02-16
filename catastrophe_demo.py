"""
Code Catastrophe Predictor - Demo Interface
Developer-focused UI for hackathon demo
"""
import streamlit as st
import json
from code_catastrophe_predictor import CodeCatastrophePredictor, CatastropheGenerator, CodeReviewAgents
from datetime import datetime
import time

# Page config
st.set_page_config(
    page_title="Code Catastrophe Predictor - Find Production Nightmares",
    page_icon="💀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - darker, developer theme with animations
st.markdown("""
<style>
    @keyframes pulse-red {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
    }

    @keyframes slide-in {
        from { transform: translateY(20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }

    .main-header {
        font-size: 3.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 0.5rem;
        background: linear-gradient(90deg, #ff0000 0%, #ff6b6b 50%, #ff0000 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(255,0,0,0.5);
        animation: pulse-red 3s ease-in-out infinite;
    }
    .sub-header {
        font-size: 1.3rem;
        text-align: center;
        color: #888;
        margin-bottom: 2rem;
    }
    .catastrophe-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d1f1f 100%);
        border-left: 4px solid #ff0000;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 0.5rem;
        box-shadow: 0 4px 6px rgba(255,0,0,0.1);
        animation: slide-in 0.5s ease-out;
        transition: transform 0.2s, box-shadow 0.2s;
    }

    .catastrophe-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(255,0,0,0.2);
    }
    .metric-card {
        background: linear-gradient(135deg, #ff0000 0%, #cc0000 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .danger-box {
        background: #3d1f1f;
        border-left: 4px solid #ff0000;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.5rem;
    }
    .warning-box {
        background: #3d2f1f;
        border-left: 4px solid #ff6b00;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.5rem;
    }
    .success-box {
        background: #1f3d1f;
        border-left: 4px solid #00ff00;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.5rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #2d2d2d;
        border-radius: 4px 4px 0 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">💀 CODE CATASTROPHE PREDICTOR</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Because the worst bugs are the ones you didn\'t think to test for | Built with Claude Opus 4.6</div>', unsafe_allow_html=True)

st.markdown("---")

# Initialize session state
if 'catastrophes' not in st.session_state:
    st.session_state.catastrophes = None
if 'code_input' not in st.session_state:
    st.session_state.code_input = ""

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")

    st.subheader("💀 What This Does")
    st.markdown("""
    **Traditional testing** finds bugs you thought to test for.

    **Code Catastrophe Predictor** uses AI to imagine:
    - 🔥 Multi-step cascade failures
    - 💥 Edge cases you missed
    - 🐛 Production nightmares
    - 💀 Creative failure scenarios
    """)

    st.markdown("---")

    st.subheader("🎬 Examples")
    demo_code = st.selectbox(
        "Load example:",
        [
            "Custom",
            "--- Real-World Systems ---",
            "🎬 Netflix Microservices",
            "🚗 Uber Real-Time Pipeline",
            "💳 Stripe Payment Processing",
            "--- Generic Examples ---",
            "Authentication API (No Rate Limiting)",
            "Payment Processing System",
            "File Upload Service",
            "Microservices Architecture",
            "Caching Layer"
        ]
    )

    if demo_code == "🎬 Netflix Microservices":
        default_code = """Netflix Video Streaming - Microservices Architecture

System Overview:
- 700+ independent microservices
- 260 million subscribers globally
- 125 million hours watched per day
- 2200+ device types supported

Video Playback Service Chain:
1. Authentication Service (100ms)
2. Playback Service orchestrates:
   - User Profile Service (30ms)
   - Viewing History Service (40ms)
   - Recommendation Service (200ms) ← OFTEN SLOW
3. CDN Selection Service (20ms)
4. DRM License Service (150ms)
5. Netflix Open Connect streams video

Tech Stack:
- Java Spring Boot (majority of services)
- Cassandra: 2700 nodes, user data
- AWS multi-region deployment
- Hystrix circuit breakers
- Chaos Monkey terminates instances 24/7

Scale & Load:
- Peak hours: 6-11 PM local time
- Service chains: Up to 8 hops deep
- Latency: 550ms average, 2000ms p99
- Popular releases: +40% traffic spike

Known Issues:
- Recommendation Service slow under load
- Cache stampede during deployments
- Cassandra compaction weekly (20% perf drop)
- Thundering herd on restarts"""

    elif demo_code == "🚗 Uber Real-Time Pipeline":
        default_code = """Uber Real-Time Data Pipeline - Surge Pricing

System Overview:
- 500 billion events per day
- Kafka: 4000+ clusters
- Flink: 10,000+ stream processing jobs
- Pinot: 100K queries/second

Surge Pricing Architecture:
1. Rider opens app → GPS event to Kafka
2. Flink aggregates demand (riders per zone)
3. Flink aggregates supply (drivers per zone)
4. ML model calculates surge multiplier
5. Write to Pinot (real-time OLAP)
6. Rider sees price in app

Tech Stack:
- Apache Kafka (message streaming)
- Apache Flink (stream processing, 100+ TB state)
- Apache Pinot (real-time analytics, 5 PB data)
- HDFS (exabyte-scale data lake)

Scale & Load:
- 5.7M events/second average
- 10M+ events/second peak (Friday nights)
- 70+ countries, 10,000+ cities
- Surge recalculated every 5 minutes

Known Issues:
- Kafka consumer lag: 5-10 min under load
- Flink checkpoint failures (10+ min recovery)
- Pinot query overload (no rate limiting)
- Cross-DC replication lag: 5-10 seconds
- No end-to-end testing at scale
- Failure = $100K-500K/min revenue loss"""

    elif demo_code == "💳 Stripe Payment Processing":
        default_code = """Stripe Payment Processing Platform

System Overview:
- $1 trillion+ annual payment volume
- 99.999% uptime SLA (5 min downtime/year)
- 10,000+ API requests/second (100K+ peak)
- 100+ countries, 135+ currencies

PaymentIntent Processing Pipeline:
1. Merchant calls API
2. Authentication & rate limiting (15ms)
3. Fraud detection / Stripe Radar ML (80ms)
4. Create PaymentIntent in PostgreSQL (20ms)
5. Call card processor (Visa/Mastercard: 800ms)
6. Update database status (20ms)
7. Publish event, queue webhook (10ms)
8. Merchant receives webhook (2-5 seconds)

Tech Stack:
- Ruby on Rails (API layer)
- Go (performance-critical services)
- PostgreSQL: 100+ shards, 1000+ replicas
- Redis: 500+ clusters for caching
- Apache Kafka (event streaming)

Architecture:
- 15+ payment processors with circuit breakers
- Double-entry ledger system (ACID)
- Multi-region active-active (4 AWS regions)
- Automatic failover between processors

Scale & Load:
- Total latency: 1.4s typical, 5+ seconds p99
- Black Friday: 10x normal volume
- $100M-500M per day transaction volume

Known Issues:
- Idempotency key conflicts = double charging
- Database connection pool exhaustion
- Processor circuit breaker cascade
- Webhook retry storms overwhelm merchants
- Read replica lag: 1-5s (30+ under load)
- Fraud model false positives block payments"""

    elif demo_code == "Authentication API (No Rate Limiting)":
        default_code = """API Endpoint: User Authentication

POST /api/login
- Accepts username + password in JSON
- Queries PostgreSQL database for user
- Uses bcrypt for password verification
- Generates JWT token (24h expiry)
- Returns token to client
- Stores active sessions in Redis cache
- NO rate limiting
- NO account lockout after failed attempts
- Single database instance (no replication)
- Deployed on 3 load-balanced servers
- 50,000 daily active users
- Peak load: 500 req/sec"""

    elif demo_code == "Payment Processing System":
        default_code = """Payment Processing Service:

- Accepts credit card payments via Stripe API
- Stores transaction records in MySQL
- Sends confirmation emails via SendGrid
- Updates inventory in real-time
- No transaction retry logic
- No idempotency keys
- Synchronous processing (client waits)
- Single points of failure: Stripe, SendGrid, MySQL
- Average 1000 transactions/day
- Black Friday: 10,000+ transactions/day"""

    elif demo_code == "File Upload Service":
        default_code = """File Upload API:

POST /api/upload
- Accepts files up to 100MB
- No file type validation (accepts all types)
- Stores files in S3 bucket (public read)
- Generates unique filename using timestamp + random
- No virus scanning
- No duplicate detection
- Synchronous upload (blocks during S3 upload)
- Uses ImageMagick for image processing
- 10,000 uploads per day"""

    elif demo_code == "Microservices Architecture":
        default_code = """E-commerce Microservices:

Services:
- User Service (Node.js, MongoDB)
- Product Service (Python, PostgreSQL)
- Order Service (Go, PostgreSQL)
- Payment Service (Java, MySQL)
- Notification Service (Node.js, Redis)

Communication:
- REST APIs between services
- No circuit breakers
- No retries (single attempt)
- Synchronous calls (chain: A → B → C → D)
- No saga pattern for distributed transactions"""

    elif demo_code == "Caching Layer":
        default_code = """Redis Caching Implementation:

- Cache user sessions (24h TTL)
- Cache product catalog (1h TTL)
- Single Redis instance (no replica)
- No fallback to database on cache miss
- Cache keys use user input (not sanitized)
- Cache size limit: 4GB
- 1 million cache operations per day
- Deployed in US-East-1
- Application in US-East-1, EU-West-1, Asia-Pacific-1"""
    else:
        default_code = ""

    num_scenarios = st.slider("Number of catastrophes", 1, 5, 3)

    st.markdown("---")
    st.markdown("**🏆 Built for Anthropic Hackathon**")
    st.markdown("*Showcasing Opus 4.6 creative failure imagination*")

# Main content
tab1, tab2, tab3 = st.tabs(["💻 Code Input", "💀 Catastrophe Scenarios", "📊 Risk Assessment"])

with tab1:
    st.header("💻 Define Your Code/Architecture")

    col1, col2 = st.columns([2, 1])

    with col1:
        code_input = st.text_area(
            "Code/Architecture Description",
            value=default_code,
            height=300,
            placeholder="""Describe your code, API, or system architecture...

Include:
- What it does
- Tech stack
- Scale/load
- Dependencies
- Known weaknesses

The more specific, the better the catastrophes!"""
        )

        # Optional architecture context
        with st.expander("📚 Optional: Add Detailed Architecture Context (Recommended)", expanded=False):
            st.markdown("""
            **Add production deployment details for hyper-realistic predictions:**
            - Current scale (users, requests/day, peak times)
            - External dependencies (APIs, databases, services)
            - Missing safeguards (no rate limiting, no retries, etc.)
            - In-memory vs persistent state
            - Single points of failure
            - Historical incidents or known vulnerabilities

            *Example: See `src/*.architecture.md` files for templates*
            """)

            # Quick load buttons - Your Project Architectures
            st.markdown("**📂 Your Project:**")
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("📥 Load AI Advisor Architecture", use_container_width=True):
                    try:
                        with open('src/ai_advisor.architecture.md', 'r') as f:
                            content = f.read()
                        st.session_state.arch_context = content
                        st.session_state.arch_loaded = "AI Advisor"
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error loading AI Advisor architecture: {str(e)}")

            with col_b:
                if st.button("📥 Load Telegram Bot Architecture", use_container_width=True):
                    try:
                        with open('src/telegram_notifier.architecture.md', 'r') as f:
                            content = f.read()
                        st.session_state.arch_context = content
                        st.session_state.arch_loaded = "Telegram Bot"
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error loading Telegram Bot architecture: {str(e)}")

            # Real-world architecture examples
            st.markdown("---")
            st.markdown("**🌎 Real-World Production Systems:**")
            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button("🎬 Netflix\n(700 services)", use_container_width=True, key="netflix_btn"):
                    try:
                        with open('examples/netflix_microservices.architecture.md', 'r') as f:
                            content = f.read()
                        st.session_state.arch_context = content
                        st.session_state.arch_loaded = "Netflix (260M users, 700 microservices)"
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")

            with col2:
                if st.button("🚗 Uber\n(500B events/day)", use_container_width=True, key="uber_btn"):
                    try:
                        with open('examples/uber_realtime_pipeline.architecture.md', 'r') as f:
                            content = f.read()
                        st.session_state.arch_context = content
                        st.session_state.arch_loaded = "Uber Real-Time Pipeline"
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")

            with col3:
                if st.button("💳 Stripe\n($1T/year)", use_container_width=True, key="stripe_btn"):
                    try:
                        with open('examples/stripe_payments.architecture.md', 'r') as f:
                            content = f.read()
                        st.session_state.arch_context = content
                        st.session_state.arch_loaded = "Stripe Payment Processing"
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")

            # Show success message if architecture was just loaded
            if 'arch_loaded' in st.session_state and st.session_state.arch_loaded:
                st.success(f"✅ Loaded {st.session_state.arch_loaded} architecture!")
                st.session_state.arch_loaded = None

            arch_context = st.text_area(
                "Architecture & Deployment Details",
                height=200,
                value=st.session_state.get('arch_context', ''),
                placeholder="""Production Deployment:
- 50,000 daily active users
- Peak load: 500 req/sec at 9:30 AM ET
- Single Redis instance (no replica)
- No rate limiting implemented
- In-memory session storage (lost on restart)
- Telegram Bot API dependency (20 msg/min limit)
- No monitoring or alerting configured

Known Issues:
- Conversation history grows unbounded
- No fallback if external API fails
- Race condition in approval workflow""",
                key="arch_context"
            )

        if st.button("💀 Predict Production Catastrophes", type="primary", use_container_width=True):
            if not code_input.strip():
                st.error("Please describe your code/architecture")
            else:
                # Combine code input with architecture context
                full_description = code_input
                if 'arch_context' in st.session_state and st.session_state.arch_context.strip():
                    full_description += f"\n\n--- DETAILED ARCHITECTURE & DEPLOYMENT INFO ---\n{st.session_state.arch_context}"

                # Better loading experience
                progress_bar = st.progress(0)
                status_text = st.empty()

                status_text.text("🧠 Opus 4.6 adaptive thinking initializing...")
                progress_bar.progress(20)
                time.sleep(0.5)

                status_text.text("💀 Imagining creative failure scenarios...")
                progress_bar.progress(40)

                # Generate catastrophes
                gen = CatastropheGenerator()
                catastrophes = gen.generate_catastrophes(full_description, num_scenarios=num_scenarios)

                progress_bar.progress(80)
                status_text.text("✅ Multi-step cascades generated...")
                time.sleep(0.3)

                progress_bar.progress(100)
                status_text.empty()
                progress_bar.empty()

                if catastrophes:
                    st.session_state.catastrophes = catastrophes
                    st.session_state.code_input = code_input

                    st.success(f"✅ Generated {len(catastrophes)} production failure scenarios!")
                    st.balloons()
                else:
                    st.error("Failed to generate catastrophes. Please try again.")

    with col2:
        st.markdown("### 💡 Pro Tips")
        st.markdown("""
        **Good descriptions include:**
        - Specific tech stack
        - Load/scale numbers
        - Single points of failure
        - Missing safeguards
        - Production details

        **Examples:**
        - "No rate limiting"
        - "Single database instance"
        - "50K users, 500 req/sec"
        - "No retries configured"
        """)

with tab2:
    st.header("💀 AI-Generated Production Catastrophes")

    if st.session_state.catastrophes is None:
        st.info("👈 Generate catastrophes in the 'Code Input' tab first")
    else:
        catastrophes = st.session_state.catastrophes

        st.markdown(f"### {len(catastrophes)} Ways Your Code Could Fail in Production")
        st.markdown("*These scenarios don't exist in your test suite - Opus 4.6 imagined them*")

        for i, catastrophe in enumerate(catastrophes, 1):
            # Color code by probability
            if catastrophe['probability'] == 'high':
                icon = "🔴"
                color = "#ff0000"
            elif catastrophe['probability'] == 'medium':
                icon = "🟡"
                color = "#ff6b00"
            else:
                icon = "🟢"
                color = "#00ff00"

            with st.expander(f"{icon} CATASTROPHE {i}: {catastrophe['name']}", expanded=(i==1)):
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.markdown(f"**Probability:** {catastrophe['probability'].upper()}")
                with col2:
                    st.markdown(f"**Blast Radius:** {catastrophe['blast_radius']}")
                with col3:
                    st.markdown(f"**Detection:** {catastrophe['detection_difficulty']}")
                with col4:
                    impact = catastrophe.get('impact_metrics', {})
                    st.markdown(f"**Downtime:** {impact.get('downtime_hours', 'N/A')}h")

                st.markdown("---")

                st.markdown("**💀 How It Fails:**")
                st.markdown(catastrophe['description'])

                st.markdown("**🎯 Why Your Code Is Vulnerable:**")
                st.markdown(catastrophe['vulnerability'])

                st.markdown("**⚡ Example Trigger:**")
                st.markdown(f"`{catastrophe['example_trigger']}`")

                # VALIDATION - Historical precedent
                if catastrophe.get('historical_precedent'):
                    st.markdown("---")
                    st.markdown("**📚 Historical Precedent (This Has Happened Before):**")
                    st.markdown('<div class="success-box">' + catastrophe['historical_precedent'] + '</div>', unsafe_allow_html=True)

                # VALIDATION - Why realistic
                if catastrophe.get('why_realistic'):
                    st.markdown("**✅ Why This Is Realistic:**")
                    st.markdown(catastrophe['why_realistic'])

                if catastrophe.get('impact_metrics'):
                    metrics = catastrophe['impact_metrics']
                    st.markdown("**💰 Business Impact:**")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Revenue Impact", metrics.get('revenue_impact', 'Unknown'))
                    with col2:
                        st.metric("Data Loss", metrics.get('data_loss', 'Unknown'))
                    with col3:
                        st.metric("Recovery Time", metrics.get('recovery_time', 'Unknown'))

                if catastrophe.get('warning_signs'):
                    st.markdown("**⚠️ Warning Signs:**")
                    for sign in catastrophe['warning_signs']:
                        st.markdown(f"- {sign}")

        st.markdown("---")

        # Multi-agent review
        if st.button("👥 Run Multi-Agent Code Review", type="primary", use_container_width=True):
            with st.spinner("Running expert review (Paranoid Engineer, Debugger, Production Veteran)..."):
                agents = CodeReviewAgents()
                top_catastrophe = catastrophes[0]

                st.markdown("### 👥 Expert Panel Review")
                st.markdown(f"**Analyzing:** {top_catastrophe['name']}")

                # Paranoid Engineer
                with st.spinner("😰 Paranoid Engineer finding more ways it fails..."):
                    paranoid_view = agents.paranoid_review(top_catastrophe)
                    time.sleep(1)

                with st.expander("😰 Paranoid Engineer's Nightmare", expanded=True):
                    st.markdown(paranoid_view)

                # Debugger
                with st.spinner("🔧 Debugger finding fixes..."):
                    debugger_view = agents.debugger_review(top_catastrophe)
                    time.sleep(1)

                with st.expander("🔧 Debugger's Fix", expanded=True):
                    st.markdown(debugger_view)

                # Veteran
                with st.spinner("⚡ Production Veteran checking realism..."):
                    veteran_view = agents.veteran_review(top_catastrophe)
                    time.sleep(1)

                with st.expander("⚡ Production Veteran's Assessment", expanded=True):
                    st.markdown(veteran_view['analysis'])
                    st.markdown(f"**Realism Score:** {veteran_view['realism_score']}/10")

                st.success("✅ Multi-agent review complete!")

with tab3:
    st.header("📊 Production Risk Assessment")

    if st.session_state.catastrophes is None:
        st.info("👈 Generate catastrophes first")
    else:
        catastrophes = st.session_state.catastrophes

        # Calculate risk metrics (case-insensitive and flexible)
        high_prob = sum(1 for c in catastrophes if 'high' in c.get('probability', '').lower())
        med_prob = sum(1 for c in catastrophes if 'medium' in c.get('probability', '').lower() or 'med' in c.get('probability', '').lower())
        low_prob = sum(1 for c in catastrophes if 'low' in c.get('probability', '').lower())

        system_wide = sum(1 for c in catastrophes if any(term in c.get('blast_radius', '').lower() for term in ['system', 'company', 'wide']))

        # Header metrics
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f'<div class="metric-card"><h3>High Probability</h3><h1>{high_prob}</h1><p>catastrophes</p></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-card"><h3>System-Wide Impact</h3><h1>{system_wide}</h1><p>catastrophes</p></div>', unsafe_allow_html=True)
        with col3:
            total_risk = (high_prob * 3) + (med_prob * 2) + (low_prob * 1)
            risk_score = min(10, total_risk)
            st.markdown(f'<div class="metric-card"><h3>Risk Score</h3><h1>{risk_score}/10</h1></div>', unsafe_allow_html=True)

        st.markdown("---")

        # Risk assessment
        st.markdown("### 🎯 Assessment")

        if high_prob >= 2 or risk_score >= 7:
            st.markdown('<div class="danger-box"><h3>🚨 HIGH RISK</h3><p>Your code has multiple high-probability failure modes. <strong>Do not deploy without addressing these issues.</strong></p></div>', unsafe_allow_html=True)
            recommendation = "HIGH RISK - Do not deploy"
        elif high_prob >= 1 or risk_score >= 4:
            st.markdown('<div class="warning-box"><h3>⚠️ MEDIUM RISK</h3><p>Significant failure scenarios exist. <strong>Implement safeguards before production.</strong></p></div>', unsafe_allow_html=True)
            recommendation = "MEDIUM RISK - Add safeguards"
        else:
            st.markdown('<div class="success-box"><h3>✅ ACCEPTABLE RISK</h3><p>Low probability failures only. <strong>Monitor and maintain defensive practices.</strong></p></div>', unsafe_allow_html=True)
            recommendation = "ACCEPTABLE RISK"

        st.markdown("---")

        # Catastrophes by severity
        st.markdown("### 📋 Catastrophes Ranked by Severity")

        # Sort by probability then blast radius
        priority_map = {'high': 3, 'medium': 2, 'low': 1}
        blast_map = {'company-wide': 4, 'system': 3, 'service': 2, 'local': 1}

        sorted_catastrophes = sorted(
            catastrophes,
            key=lambda c: (priority_map.get(c['probability'], 0), blast_map.get(c['blast_radius'], 0)),
            reverse=True
        )

        for i, catastrophe in enumerate(sorted_catastrophes, 1):
            icon = "🔴" if catastrophe['probability'] == 'high' else "🟡" if catastrophe['probability'] == 'medium' else "🟢"
            st.markdown(f"{i}. {icon} **{catastrophe['name']}** → {catastrophe['probability']} probability, {catastrophe['blast_radius']} impact")

        st.markdown("---")

        # Export report
        st.markdown("### 📥 Export Report")

        report = {
            "timestamp": datetime.now().isoformat(),
            "code": st.session_state.code_input,
            "catastrophes_found": len(catastrophes),
            "risk_score": risk_score,
            "recommendation": recommendation,
            "catastrophes": [
                {
                    "name": c['name'],
                    "probability": c['probability'],
                    "blast_radius": c['blast_radius'],
                    "detection_difficulty": c['detection_difficulty']
                }
                for c in sorted_catastrophes
            ]
        }

        report_json = json.dumps(report, indent=2)

        st.download_button(
            label="📄 Download Catastrophe Report (JSON)",
            data=report_json,
            file_name=f"catastrophe_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

        st.markdown("---")
        st.markdown("### 🏆 Built with Claude Opus 4.6")
        st.markdown("""
        **Novel Capabilities:**
        - 💀 Creative failure imagination
        - 👥 Multi-agent code review
        - 🎯 Production-realistic scenarios
        - 📊 Risk assessment

        *This tool imagines bugs you didn't think to test for.*
        """)

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #666;'>💀 Built for Anthropic Claude Code Hackathon 2026 | Opus 4.6 Production Nightmare Generator</div>", unsafe_allow_html=True)
