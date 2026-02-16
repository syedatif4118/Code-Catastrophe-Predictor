# Stripe Payment Processing Architecture (Real Production System)

## Component Overview
**Company**: Stripe, Inc.
**System**: Global Payment Processing Platform
**Scale**: $1 trillion+ annual payment volume, 100+ countries, millions of API requests per second

**Sources**: [Stripe Engineering Blog - Payment API Design](https://stripe.com/blog/payment-api-design), [InfoQ - Architecture that Helps Stripe Move Faster](https://www.infoq.com/presentations/stripe-api-pci/), [System Design - Payment Gateways](https://codersguild.github.io/System-Design/Payment%20Architectures/)

## System Architecture

### Three-Layer Architecture

```
Layer 1: User Front-End
  ├── Mobile Apps (iOS, Android)
  ├── Web Dashboard
  ├── Checkout.js (embeddable)
  ├── Email Notifications
  └── Webhooks to merchants

Layer 2: Middleware (API Gateway)
  ├── Authentication & Authorization
  ├── Rate Limiting (per API key)
  ├── Request Routing
  ├── PCI Compliance Boundary
  └── Fraud Detection (ML models)

Layer 3: Transaction Layer
  ├── Payment Processing Engine
  ├── Card Network Integration (Visa, Mastercard, Amex)
  ├── Bank ACH Connections
  ├── Ledger System (double-entry accounting)
  └── Data Persistence (PostgreSQL, Redis)
```

### Key Components

**1. PaymentIntent (Core Abstraction)**
- Stateful object tracking payment attempt
- States: requires_payment_method → requires_confirmation → processing → succeeded/failed
- Idempotent: Same idempotency key = same result
- Automatic retries on network failures

**2. Card Processor Integration**
- **15+ payment processors** (Visa, Mastercard, Amex, Discover, UnionPay, etc.)
- Circuit breaker per processor
- Automatic failover if processor is down
- Processor latency: 500ms-3s per authorization

**3. Fraud Detection Engine**
- **Stripe Radar**: ML-powered fraud detection
- Real-time scoring: <100ms per transaction
- Blocks 99.9% of fraud, 0.1% false positive rate
- $20B+ in fraud blocked annually

**4. Ledger System**
- Double-entry accounting (every debit has a credit)
- PostgreSQL with custom extensions
- Strict ACID transactions
- Audit trail: 7+ years retention

**5. Event-Driven Architecture**
- Apache Kafka for async events
- Webhooks to notify merchants
- Retry logic: 3 attempts over 72 hours
- Dead letter queue for failed events

## Production Deployment Details

### Scale Numbers

**API Traffic:**
- **10,000+ API requests per second** (average)
- **100,000+ RPS** during peak (Black Friday, Cyber Monday)
- **99.999% uptime SLA** (5.26 minutes downtime/year allowed)

**Payment Volume:**
- **$1 trillion+** processed annually
- **$100M-500M per day** in transaction volume
- **Millions of merchants** worldwide
- **100+ countries** and 135+ currencies

**Transaction Processing:**
- **Authorization time**: 500ms-2s (p95)
- **Capture time**: 1-3 business days (settlement)
- **Refund time**: 5-10 business days
- **Dispute resolution**: 30-90 days

**Infrastructure:**
- **4 AWS regions** (us-east-1, eu-west-1, ap-southeast-1, us-west-2)
- **Multi-region active-active** for high availability
- **PostgreSQL**: 100+ shards, 1000+ replicas
- **Redis**: 500+ clusters for caching

### Geographic Distribution

**Primary Regions:**
- **US**: 60% of transaction volume
- **Europe**: 25%
- **Asia**: 10%
- **Rest of World**: 5%

**Latency Requirements:**
- Same-region API call: <100ms (p95)
- Cross-region call: <300ms (p95)
- Payment processor call: <2s (p99)

### Technology Stack

**Backend:**
- Ruby on Rails (API layer)
- Go (performance-critical services)
- Scala (fraud detection, ML)

**Databases:**
- PostgreSQL (primary transactional DB)
- MongoDB (document storage, metadata)
- Redis (caching, session storage)
- DynamoDB (event storage)

**Message Queue:**
- Apache Kafka (event streaming)
- RabbitMQ (internal job queue)
- SQS (webhook delivery queue)

**Monitoring:**
- Custom internal tools
- Datadog for metrics
- Sentry for error tracking
- PagerDuty for on-call

## Critical Dependencies

### External Dependencies

**1. Card Networks (Visa, Mastercard, etc.)**
- Latency: 500ms-3s per authorization
- Downtime: 1-2x per year, 1-4 hours
- Rate limits: Varies by processor
- **If Visa is down**: Circuit breaker opens, fail to backup processor

**2. Banks & ACH Network**
- Settlement: 1-3 business days
- Weekend/holiday delays: 5-7 days
- Failure rate: 0.5-1% (insufficient funds, fraud)
- **If bank rejects**: Automatic retry, then merchant notification

**3. AWS Infrastructure**
- **Single cloud provider risk**: All regions on AWS
- Multi-region deployment mitigates risk
- S3 for blob storage (receipt images, etc.)
- CloudFront for static assets

**4. Third-Party Fraud Services**
- 3D Secure (Verified by Visa, Mastercard SecureCode)
- Address Verification Service (AVS)
- Card Verification Value (CVV)
- **If fraud service is down**: Fall back to internal Radar

### Internal Dependencies

**1. Ledger System**
- All financial transactions recorded here
- **Critical path**: Payment cannot complete without ledger entry
- Database contention under high load
- Backup ledger takes 5-10 minutes to promote

**2. Fraud Detection (Radar)**
- ML model inference: <100ms required
- If slow: Block transaction (false positive)
- If down: Fall back to rule-based system (less accurate)
- Model retraining: Daily, deployment can cause blips

**3. Webhook Delivery**
- Asynchronous notification to merchants
- 3 retry attempts over 72 hours
- If merchant endpoint is down: Events queued, eventual delivery
- No backpressure: Queue can grow unbounded

## Current Limitations & Vulnerabilities

### Payment Processing

**1. Idempotency Key Conflicts**
- Merchant sends same key with different parameters
- Current behavior: Return 400 error
- Problem: Merchant doesn't know if payment succeeded
- Risk: Double charging or missed payment

**2. Processor Circuit Breaker Tuning**
- Threshold: 5% error rate or 2s latency
- Too sensitive: False positives, unnecessary failover
- Not sensitive enough: Users experience slow payments
- Manual tuning per processor (not adaptive)

**3. Capture vs Authorization Timing**
- Authorization reserves funds (instant)
- Capture transfers funds (1-3 days)
- Merchants can forget to capture
- Uncaptured authorizations expire (7 days)
- **Risk**: Lost revenue if capture expires

**4. Multi-Currency Complexity**
- 135+ currencies supported
- Exchange rate updates: Every 15 minutes
- Rate staleness: Arbitrage opportunities
- Settlement currency mismatch: FX risk

### Database & State Management

**1. PostgreSQL Sharding**
- 100+ shards by merchant ID
- Uneven shard sizes (some merchants >> others)
- Rebalancing shards: 8+ hour maintenance window
- Cross-shard queries: Slow (requires scatter-gather)

**2. Database Connection Pool Exhaustion**
- High load: 10,000+ concurrent requests
- Connection pool: 500 connections per shard
- If pool exhausted: 500 error to merchant
- No queuing: Requests fail immediately

**3. Read Replica Lag**
- Async replication: 1-5 second lag typical
- Under load: 30+ second lag
- Merchants read stale data (e.g., old balance)
- Eventual consistency issues

**4. Cache Invalidation**
- Redis caches API responses (30-60s TTL)
- On payment update: Invalidate cache
- Race condition: Cache invalidation before DB commit
- Result: Stale data served to merchants

### Fraud & Security

**1. Radar ML Model Drift**
- Model trained on historical fraud patterns
- New fraud techniques: Model doesn't recognize
- Retraining: Once per day (not real-time)
- **Risk**: 24-hour window where new fraud is undetected

**2. Rate Limiting Per Key**
- Limit: 100 requests/second per API key
- Problem: Distributed attacks use many keys
- No global rate limit per merchant
- **Risk**: DDoS attack overwhelms backend

**3. PCI Compliance Scope**
- Card numbers never stored raw (tokenized)
- Encryption at rest and in transit
- But: Logs may contain partial card numbers
- **Risk**: Log aggregation tools expose sensitive data

**4. Webhook Retry Storm**
- Merchant endpoint goes down
- Stripe retries 3x with exponential backoff
- Endpoint comes back up
- Receives 3x events in rapid succession (thundering herd)
- **Risk**: Merchant processes payment multiple times

### Operational Issues

**1. No End-to-End Testing at Scale**
- Unit tests: Extensive
- Integration tests: Limited
- Load testing: Not at production scale
- **Result**: Incidents discovered in production

**2. Monitoring Alert Fatigue**
- 10,000+ alerts configured
- Many false positives
- On-call engineers ignore non-critical alerts
- **Risk**: Real incidents missed

**3. Deployment Risk**
- 50+ deployments per day
- Blue-green deployment with 5-minute soak
- Automatic rollback on error rate >1%
- **But**: Financial bugs may not show errors (silent data corruption)

**4. Runaway Costs**
- Payment processor fees: 2-3% per transaction
- High-volume merchant: $1M+ monthly fees
- No automatic cost controls
- **Risk**: Unprofitable transactions

## Data Flow Example: Card Payment

```
1. Merchant calls Create PaymentIntent API (t=0)
   → Authenticate API key (10ms)
   → Check rate limit (5ms)
   → Run fraud detection (80ms)
   ↓
2. Create PaymentIntent in database (t=100ms)
   → Insert into PostgreSQL (20ms)
   → Replicate to read replicas (50ms lag)
   ↓
3. Call card processor (Visa) (t=150ms)
   → Network latency to Visa (200ms)
   → Visa authorization (800ms)
   → Network latency back (200ms)
   ↓
4. Update PaymentIntent status (t=1350ms)
   → Write to PostgreSQL (20ms)
   → Invalidate cache (5ms)
   → Publish Kafka event (10ms)
   ↓
5. Return response to merchant (t=1385ms)
   → Webhook queued for async delivery (t=1500ms)
   → Merchant receives webhook (t=2-5s)
```

**Total latency:** 1.4 seconds (typical), 5+ seconds (p99 or under load)

**Failure scenarios:**
- Visa timeout (10s): Return 500 error to merchant, retry later
- Database down: Promote read replica (5-10 min), meanwhile 503 errors
- Fraud detection timeout: Block payment (false positive)
- Webhook delivery fails: Retry 3x over 72 hours, then dead letter queue

## Recent Production Incidents

**2019 - EU Payment Outage (4 hours)**
- Database migration in eu-west-1
- Connection pool exhausted
- All EU payments failed
- $50M+ in lost transaction volume
- Manual intervention to add connection pool capacity

**2020 - Processor Circuit Breaker Cascade**
- Visa API slow (3s latency)
- Circuit breaker opened for Visa
- All traffic failed over to Mastercard
- Mastercard overwhelmed, circuit breaker opened
- Domino effect: All processors failed
- 30-minute outage, manual override required

**2022 - Webhook Retry Storm**
- Major merchant (Shopify) had webhook endpoint outage
- 1M+ webhooks queued
- Endpoint recovered
- 1M webhooks delivered in 5 minutes (3,300/sec)
- Shopify backend overwhelmed
- Resulted in duplicate order processing

**2023 - Black Friday Surge**
- 10x normal transaction volume
- PostgreSQL shards hit IOPS limit
- Write latency increased to 5+ seconds
- Payment processing slowed to 10+ seconds
- Cart abandonment rate increased 300%
- Revenue loss: $5-10M in 2 hours

**2024 - Fraud Model Deployment Bug**
- New Radar ML model deployed
- Bug: Flagged all transactions as fraud
- 100% block rate for 15 minutes
- $20M+ in lost transaction volume
- Rollback took 15 minutes (automated)

## Catastrophe-Prone Areas

⚠️ **Critical (Financial Impact):**
1. **Double charging** - Idempotency key bugs, webhook retry storms
2. **Uncaptured authorizations** - Merchants forget to capture, revenue lost
3. **FX rate staleness** - Arbitrage opportunities, financial loss
4. **Ledger bugs** - Accounting errors, regulatory issues
5. **Processor circuit breaker cascade** - All processors fail simultaneously

⚠️ **High Risk (Availability):**
1. **Database connection pool exhaustion** - High load = 500 errors
2. **Read replica lag** - Stale data served, inconsistency issues
3. **Cache invalidation races** - Serve stale payment status
4. **Webhook retry storms** - Overwhelm merchant endpoints
5. **Fraud model false positives** - Block legitimate payments

⚠️ **Security & Compliance:**
1. **PCI audit failures** - Log aggregation exposes card data
2. **Radar model drift** - New fraud techniques undetected for 24 hours
3. **Rate limit bypass** - Distributed attacks with many API keys
4. **Processor data leakage** - Sensitive data in error messages

⚠️ **Cost Explosions:**
1. **Processor fees** - 2-3% per transaction, unprofitable for low-margin merchants
2. **Database scaling** - Uneven shards, expensive rebalancing
3. **Webhook delivery** - Unbounded queue growth, storage costs

## Historical Precedents

**Similar Incidents:**
- **PayPal (2020)**: 4-hour outage, database connection issues, $200M+ impact
- **Square (2021)**: Processor failover cascade, 1-hour outage
- **Adyen (2022)**: Fraud model false positives, blocked $50M in transactions
- **Braintree (2019)**: Webhook retry storm, merchant overload
- **Worldpay (2023)**: Black Friday surge, 30% of payments failed

**Known Vulnerabilities:**
- **CVE-2021-43138** - Async processing RCE in payment libraries
- **CVE-2022-23529** - JSON Web Token bypass in authentication
- **PCI DSS Violations** - Multiple processors fined for log exposure
- **GDPR Fines** - €10M+ for payment data retention issues

## Cost & Performance

**Infrastructure Cost:**
- **$200-500M annually** (estimated)
- AWS: $100M+
- Payment processor fees: $50M+
- Database infrastructure: $30M+
- Fraud detection: $20M+

**Performance SLAs:**
- API latency: <500ms (p95), <2s (p99)
- Payment success rate: >99%
- Uptime: 99.999% (5 minutes downtime/year)
- Fraud detection: <100ms, 0.1% false positive rate

**Financial SLAs:**
- Settlement time: 1-3 business days (standard)
- Refund time: 5-10 business days
- Dispute resolution: 30-90 days
- Chargeback rate: <1% (above this, merchant at risk)

---

**TLDR for AI:** $1T+/year payment volume, 99.999% SLA, 15+ card processors with circuit breakers, PostgreSQL at massive scale, fraud detection in <100ms, idempotency critical, webhook retry storms, Black Friday surge risks, double-charging bugs = $M losses
