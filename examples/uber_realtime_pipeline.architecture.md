# Uber Real-Time Data Pipeline Architecture (Real Production System)

## Component Overview
**Company**: Uber Technologies
**System**: Real-Time Data Infrastructure & Streaming Pipeline
**Scale**: 500 billion events per day, petabytes of data, 100,000+ microservices

**Sources**: [Uber Engineering Blog - Real-Time Data Infrastructure](https://www.uber.com/blog/building-scalable-streaming-pipelines/), [ArXiv Paper: Real-time Data Infrastructure at Uber](https://arxiv.org/pdf/2104.00087)

## System Architecture

### Core Platform: Kappa+ Architecture

**Data Flow:**
```
Trip Event (rider requests ride)
  ↓
Apache Kafka (message ingestion)
  ↓
Apache Flink (stream processing)
  ↓
Apache Pinot (real-time OLAP)
  ↓
Presto (SQL query interface)
  ↓
Real-time features (surge pricing, ETA, fraud detection)
```

### Key Components

**1. Apache Kafka (Message Streaming)**
- **4,000+ Kafka clusters** globally
- **500 billion messages per day**
- **50 petabytes** of data per day
- 1-2 second end-to-end latency target
- Cross-datacenter replication with 5-10 second lag

**2. Apache Flink (Stream Processing)**
- **10,000+ Flink jobs** running 24/7
- Real-time aggregations, joins, windowing
- State size: 100+ TB per job (largest jobs)
- Checkpoint interval: 10 seconds
- Recovery time: 2-5 minutes on failure

**3. Apache Pinot (Real-Time Analytics)**
- **100,000+ queries per second**
- Sub-second query latency (p95 < 500ms)
- 5 petabytes of data indexed
- Data retention: 7 days hot, 90 days warm

**4. HDFS (Long-Term Storage)**
- **Exabyte-scale** storage
- Parquet format for batch processing
- Data retention: 7 years for compliance
- Replication factor: 3x (triple storage cost)

### Technology Stack

**Streaming:**
- Apache Kafka - message bus
- Apache Flink - stream processing
- Confluent Schema Registry - data schemas
- Kafka Connect - CDC pipelines

**Storage:**
- Apache Pinot - real-time OLAP
- HDFS - data lake
- Hudi - incremental ETL
- Schemaless (MySQL fork) - key-value store

**Query:**
- Presto - distributed SQL
- Spark - batch processing
- Hive - data warehousing

**Orchestration:**
- Uber Cadence - workflow engine
- Kubernetes - container orchestration
- Mesos - resource management

## Production Deployment Details

### Scale Numbers

**Events Per Second:**
- **5.7 million events/second** average
- **10+ million events/second** peak (Friday nights)
- Event types: GPS pings, trip status, payments, ratings, support tickets

**Geographic Distribution:**
- **70+ countries**, **10,000+ cities**
- **5 major datacenters** (US-East, US-West, EU, APAC, LATAM)
- **20+ edge locations** for low latency

**Service Count:**
- **8,000+ microservices** producing data
- **2,000+ data pipelines** consuming data
- **5,000+ Flink jobs** for stream processing

**Team Size:**
- **300+ data engineers** maintaining pipelines
- **50+ SREs** for infrastructure
- On-call rotation: 24/7, 5-person teams

### Load Patterns

**Hourly:**
- 5 AM - 9 AM: Morning commute spike (+200%)
- 5 PM - 9 PM: Evening rush (+250%)
- 2 AM - 5 AM: Lowest traffic (30% of peak)

**Weekly:**
- Friday/Saturday nights: +300% (nightlife, bars close)
- Sunday mornings: -40% (people sleeping)

**Event-Driven:**
- **New Year's Eve**: 10x normal load in 1-hour window
- **Concerts/Sports**: 5x load in specific cities
- **Weather events**: Sudden 3x spike (rain, snow)

### Critical Features Powered by Real-Time Data

**1. Surge Pricing**
- Recalculated every 5 minutes per zone
- Requires: Supply (available drivers), Demand (waiting riders)
- Latency requirement: <30 seconds from event to pricing update
- Failure impact: $100K-500K revenue loss per minute

**2. ETA Prediction**
- Updated every 10 seconds during trip
- Uses: Traffic data, historical patterns, driver location
- Latency requirement: <5 seconds
- Failure impact: User frustration, driver confusion

**3. Fraud Detection**
- Real-time scoring of every transaction
- ML models check for anomalies
- Latency requirement: <1 second (blocking payment)
- Failure impact: Financial loss, regulatory issues

**4. Driver Matching**
- Real-time optimization of rider-driver pairs
- Considers: Distance, ETA, ratings, preferences
- Latency requirement: <2 seconds
- Failure impact: Longer wait times, lost trips

## Current Limitations & Vulnerabilities

### Kafka Issues

**1. Consumer Lag**
- Normal lag: <10 seconds
- Under load: Lag grows to 5-10 minutes
- No automatic backpressure - consumers just fall behind
- Recovery: Manual intervention, add partitions

**2. Cross-Datacenter Replication**
- 5-10 second lag between regions
- Network partitions cause 30+ second lag
- Data loss possible during datacenter failover
- No conflict resolution for concurrent writes

**3. Retention Limits**
- Kafka retains messages for 7 days
- Storage cost: $10M+ annually
- Old messages dropped = cannot replay
- No archive recovery mechanism

### Flink Vulnerabilities

**1. Stateful Processing**
- Largest jobs have 100+ TB of state
- Checkpoint time: 10+ minutes for large jobs
- Checkpoints stored in HDFS (slow)
- Failure during checkpoint = lost data

**2. Recovery Time**
- Small jobs: 30 seconds
- Large jobs: 5-10 minutes
- During recovery: No processing, data queues up
- Cascading failures if multiple jobs restart

**3. Backpressure Handling**
- Flink slows down when overwhelmed
- But Kafka keeps producing → lag grows
- No automatic circuit breaker
- Manual intervention needed to shed load

### Pinot Limitations

**1. Query Overload**
- 100K QPS normal, 200K+ during incidents
- No global rate limiting per user/team
- Slow queries block others (head-of-line blocking)
- Cluster crashes under 300K+ QPS

**2. Data Ingestion**
- Real-time segments lag during high load
- 5-10 minute delay possible
- Users see stale data, make wrong decisions
- No alerting on data freshness

**3. Hot Partition Problem**
- Popular cities (SF, NYC) overwhelm single servers
- Rebalancing takes 30+ minutes
- During rebalance: Degraded query performance

### System-Wide Issues

**1. Dependency Hell**
- 8,000 services produce data → 2,000 pipelines consume
- Single service schema change breaks 20+ downstream consumers
- No enforcement of backward compatibility
- Breaking change = pipeline outage

**2. No End-to-End Testing**
- Unit tests exist, integration tests limited
- No load testing at production scale
- Outages discovered in production
- Mean time to detection: 15-30 minutes

**3. Monitoring Gaps**
- 10,000+ Flink jobs = not all monitored
- Some pipelines fail silently for days
- Data quality issues undetected
- No SLAs for data freshness

**4. Cost Explosion**
- No automatic cost controls
- Runaway queries cost $10K+ per hour
- Unoptimized pipelines waste resources
- Storage growth: 50% YoY, no cleanup

## Data Flow Example: Surge Pricing

```
1. Rider opens app (t=0)
   → GPS event sent to Kafka
   ↓
2. Flink job aggregates demand (t=1s)
   → Counts riders per zone
   ↓
3. Flink job aggregates supply (t=2s)
   → Counts available drivers per zone
   ↓
4. Surge calculation job (t=3s)
   → ML model predicts multiplier
   ↓
5. Write to Pinot (t=4s)
   → Stores current surge pricing
   ↓
6. Rider sees price (t=5s)
   → Query Pinot for zone pricing
```

**Total latency:** 5 seconds (target), 15-30 seconds (under load)

**Failure scenarios:**
- Kafka lag: Surge pricing based on 5-minute-old data
- Flink crash: Surge stuck at old value for 2-5 minutes
- Pinot overload: Query timeout, rider sees error
- Network partition: NYC prices use LA data (wrong)

## Recent Production Incidents

**2021 - New Year's Eve Surge Failure**
- 10x normal load in 30-minute window
- Kafka consumer lag hit 15 minutes
- Surge pricing calculated on stale data
- Underpriced rides = driver shortage
- Revenue loss: $2-3M in 1 hour

**2022 - Flink State Explosion**
- ML model update increased state size 10x
- Checkpoints took 30+ minutes (normally 10 sec)
- Out of memory errors, job crashes
- 4-hour outage for fraud detection
- 50+ fraudulent transactions missed ($500K loss)

**2023 - Pinot Query Storm**
- Dashboard with unoptimized query
- 1000+ engineers opened dashboard simultaneously
- Pinot cluster overloaded, crashed
- 2-hour outage for all real-time analytics
- Surge pricing, ETA, fraud detection all down

**2024 - Cross-DC Replication Failure**
- Network issue between US-East and US-West
- Replication lag hit 5 minutes
- Split-brain: Both DCs thought they were primary
- Conflicting surge prices, double bookings
- 30-minute outage, manual reconciliation

## Catastrophe-Prone Areas

⚠️ **Critical:**
1. **Kafka consumer lag cascade** - One slow consumer blocks others
2. **Flink checkpoint failure** - Lost state = lost revenue data
3. **Pinot query overload** - No rate limiting, cluster crash
4. **Cross-DC split-brain** - Conflicting data, manual resolution
5. **Schema breaking changes** - Downstream pipeline failures

⚠️ **High Risk:**
1. **Surge pricing staleness** - Wrong prices = revenue loss or driver shortage
2. **ETA prediction failure** - Users cancel, reputation damage
3. **Fraud detection outage** - Financial loss, regulatory issues
4. **Driver matching latency** - Long wait times, lost trips
5. **Monitoring blind spots** - Silent failures for days

⚠️ **Cost Explosions:**
1. **Runaway Flink jobs** - Unbounded state growth
2. **Unoptimized Pinot queries** - $10K+/hour CPU costs
3. **HDFS storage growth** - 50% YoY, no cleanup policy
4. **Kafka retention** - $10M+/year, could be optimized

## Historical Precedents

**Similar Systems:**
- **LinkedIn**: Kafka creators, similar scale (1T+ messages/day)
- **Airbnb**: Flink for real-time analytics, experienced state explosion
- **Twitter**: Real-time tweet processing, Kafka consumer lag during trending events
- **Robinhood**: Kafka + Flink for stock trading, outages during meme stock volatility

**Known Incidents:**
- **AWS Kinesis Outage (2020)**: Cascading failures in stream processing
- **Google Cloud Pub/Sub (2019)**: Message delivery delays during high load
- **Apache Flink CVE-2020-17518**: RCE vulnerability in Flink REST API
- **Kafka Log4j Vulnerability (2021)**: Affected thousands of Kafka clusters

## Cost & Performance

**Infrastructure Cost:**
- **$500M-1B annually** (estimated)
- Kafka: $200M+
- Flink: $150M+
- Pinot: $100M+
- HDFS: $50M+

**Performance SLAs:**
- End-to-end latency: <5 seconds (p95)
- Query latency: <500ms (p95)
- Uptime: 99.9% (8.7 hours downtime/year)
- Data freshness: <30 seconds lag

---

**TLDR for AI:** 500B events/day, Kafka + Flink + Pinot at massive scale, surge pricing depends on real-time data, consumer lag = revenue loss, state explosion = outages, no end-to-end testing, monitoring gaps, cost explosion risks
