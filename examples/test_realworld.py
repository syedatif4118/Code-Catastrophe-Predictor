"""
Test the 3 real-world architectures with the CLI

Run these commands to test:

1. Netflix Microservices:
   python catastrophe_cli.py examples/netflix_microservices.architecture.md --scenarios 3

2. Uber Real-Time Pipeline:
   python catastrophe_cli.py examples/uber_realtime_pipeline.architecture.md --scenarios 3

3. Stripe Payment Processing:
   python catastrophe_cli.py examples/stripe_payments.architecture.md --scenarios 3
"""

# For Streamlit demo, paste these code descriptions:

NETFLIX_CODE = """
Netflix Video Streaming Service - Microservices Architecture

Component: Playback Service Chain
- User Authentication Service
- Playback Service (orchestrates 4 sub-services)
- User Profile Service
- Viewing History Service
- Recommendation Service (ML-powered, often slow)
- CDN Selection Service
- DRM License Service

Tech Stack:
- Java Spring Boot (700+ microservices)
- Cassandra (2700 nodes, user data, watch history)
- AWS multi-region deployment
- Hystrix circuit breakers
- Chaos Monkey in production 24/7

Scale:
- 260 million subscribers globally
- 125 million hours watched per day
- 2200+ device types supported
- Peak traffic: 6-11 PM local time each timezone

Critical Flow (Video Playback):
1. User clicks Play
2. Authentication (100ms)
3. Playback Service queries 4 services in parallel (200ms total)
4. CDN Selection (20ms)
5. DRM License (150ms)
6. Stream video

Total latency: 470ms typical, 2000ms p99

Known Issues:
- Service chains up to 8 hops deep
- Recommendation Service frequently slow (200ms+)
- Cassandra compaction causes 20% perf drop weekly
- Cache stampede during deployments
- Thundering herd: All 700 services restart after deployment
"""

UBER_CODE = """
Uber Real-Time Data Pipeline - Surge Pricing System

Component: Kappa+ Streaming Architecture
- Apache Kafka (4000+ clusters, 500B events/day)
- Apache Flink (10,000+ jobs processing streams)
- Apache Pinot (100K queries/sec, real-time analytics)
- Presto (distributed SQL query interface)

Critical Feature: Surge Pricing
- Recalculated every 5 minutes per geographic zone
- Requires real-time data: Supply (drivers), Demand (riders)
- Latency requirement: <30 seconds from event to price update
- Failure = $100K-500K revenue loss per minute

Tech Stack:
- Kafka: Message ingestion (5.7M events/sec average)
- Flink: Stream processing with 100+ TB state per large job
- Pinot: Sub-second queries on 5 PB of data
- HDFS: Exabyte-scale data lake

Scale:
- 500 billion events per day
- 70+ countries, 10,000+ cities
- 8,000+ microservices producing data
- Peak: 10M+ events/second (Friday nights)

Data Flow (Surge Pricing):
1. Rider opens app → GPS event to Kafka
2. Flink aggregates demand (counts riders per zone)
3. Flink aggregates supply (counts available drivers)
4. ML model calculates surge multiplier
5. Write to Pinot
6. Rider sees price
Total: 5 seconds target, 15-30 seconds under load

Known Issues:
- Kafka consumer lag grows to 5-10 minutes under load
- Flink checkpoint failures = lost state = lost revenue data
- Pinot query overload crashes cluster (no rate limiting)
- Cross-datacenter replication lag: 5-10 seconds (30+ during issues)
- No end-to-end testing at production scale
- State explosion in large Flink jobs (100+ TB)
"""

STRIPE_CODE = """
Stripe Payment Processing Platform

Component: PaymentIntent Processing Pipeline
- 3-Layer Architecture: Frontend → Middleware → Transaction Layer
- 15+ card processors (Visa, Mastercard, Amex, etc.)
- Circuit breaker per processor with automatic failover
- Fraud detection (Stripe Radar) in <100ms
- Double-entry ledger system (PostgreSQL)

Tech Stack:
- Ruby on Rails (API layer)
- Go (performance-critical services)
- PostgreSQL (100+ shards, 1000+ replicas)
- Redis (500+ clusters for caching)
- Apache Kafka (event streaming)
- Webhooks for merchant notifications

Scale:
- $1 trillion+ annual payment volume
- 10,000+ API requests/second average
- 100,000+ RPS during Black Friday
- 99.999% uptime SLA (5.26 min downtime/year)
- 100+ countries, 135+ currencies

Payment Flow:
1. Merchant calls Create PaymentIntent API
2. Authenticate API key (10ms)
3. Fraud detection / Radar ML scoring (80ms)
4. Create PaymentIntent in PostgreSQL (20ms)
5. Call card processor (Visa: 800ms authorization)
6. Update status in database (20ms)
7. Publish Kafka event, queue webhook
8. Merchant receives webhook (2-5 seconds)

Total: 1.4 seconds typical, 5+ seconds p99

Known Issues:
- Idempotency key conflicts = double charging risk
- Processor circuit breaker cascade (Visa down → all fail to Mastercard → overwhelm)
- Database connection pool exhaustion under high load
- Read replica lag (1-5s normal, 30+ under load)
- Webhook retry storms overwhelm merchant endpoints
- Fraud model false positives block legit payments
- Black Friday surge: 10x volume = database IOPS limits
- Uncaptured authorizations expire (7 days) = lost revenue
"""

# To use in CLI:
# The .architecture.md files contain all the detail
# Just run: python catastrophe_cli.py examples/netflix_microservices.architecture.md

print("Ready to test real-world architectures!")
print("\nCLI Commands:")
print("1. python catastrophe_cli.py examples/netflix_microservices.architecture.md --scenarios 3")
print("2. python catastrophe_cli.py examples/uber_realtime_pipeline.architecture.md --scenarios 3")
print("3. python catastrophe_cli.py examples/stripe_payments.architecture.md --scenarios 3")
print("\nFor Streamlit: Copy NETFLIX_CODE, UBER_CODE, or STRIPE_CODE above")
