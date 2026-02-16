# 🏗️ Architecture - Code Catastrophe Predictor

**Complete system architecture, data flows, and component diagrams**

---

## 📋 Table of Contents

1. [System Overview](#system-overview)
2. [High-Level Architecture](#high-level-architecture)
3. [Core Components](#core-components)
4. [Data Flow](#data-flow)
5. [Multi-Agent System](#multi-agent-system)
6. [Catastrophe Generation Pipeline](#catastrophe-generation-pipeline)
7. [API & Interfaces](#api--interfaces)
8. [Deployment Architecture](#deployment-architecture)

---

## System Overview

Code Catastrophe Predictor is a production failure prediction system powered by Claude Opus 4.6. It analyzes code/architecture descriptions and generates creative, multi-step cascade failure scenarios using adaptive thinking and multi-agent adversarial review.

### Key Capabilities

- **Creative Scenario Generation**: Opus 4.6 imagines novel failure modes
- **Multi-Agent Validation**: Three AI experts debate scenario realism
- **Historical Precedent Matching**: Links predictions to real incidents
- **Risk Analysis**: Automatic scoring and prioritization
- **Multiple Interfaces**: CLI tool, web demo, Python API

---

## High-Level Architecture

```mermaid
graph TB
    subgraph "User Interfaces"
        CLI[CLI Tool<br/>catastrophe_cli.py]
        WEB[Web Demo<br/>catastrophe_demo.py]
        API[Python API]
    end

    subgraph "Core Engine"
        PRED[CodeCatastrophePredictor<br/>Main Orchestrator]
        GEN[CatastropheGenerator<br/>Opus 4.6 Scenario Generation]
        AGENTS[CodeReviewAgents<br/>Multi-Agent Review]
    end

    subgraph "Anthropic API"
        OPUS[Claude Opus 4.6<br/>Adaptive Thinking Mode]
    end

    subgraph "Data"
        ARCH[Architecture Files<br/>examples/*.md]
        RESULTS[Results<br/>JSON Output]
    end

    CLI --> PRED
    WEB --> PRED
    API --> PRED

    PRED --> GEN
    PRED --> AGENTS

    GEN --> OPUS
    AGENTS --> OPUS

    ARCH --> PRED
    PRED --> RESULTS

    style OPUS fill:#8b5cf6,stroke:#7c3aed,color:#fff
    style GEN fill:#ef4444,stroke:#dc2626,color:#fff
    style AGENTS fill:#f59e0b,stroke:#d97706,color:#fff
```

---

## Core Components

### 1. CatastropheGenerator

**Responsibility**: Generate creative production failure scenarios using Opus 4.6

```mermaid
classDiagram
    class CatastropheGenerator {
        -Anthropic client
        +generate_catastrophes(code_description, num_scenarios)
        -_build_prompt(code_description, num_scenarios)
        -_parse_response(response)
        -_extract_json(response_text)
    }

    class Catastrophe {
        +string scenario_name
        +list~string~ failure_steps
        +string probability
        +string impact_assessment
        +string revenue_impact
        +string historical_precedent
    }

    CatastropheGenerator --> Catastrophe : generates
```

**Key Features**:
- Uses Opus 4.6 with `thinking` parameter for adaptive reasoning
- Handles multi-content block responses (thinking + text)
- Parses structured JSON from natural language
- Validates scenario completeness

### 2. CodeReviewAgents

**Responsibility**: Multi-agent adversarial review of scenarios

```mermaid
classDiagram
    class CodeReviewAgents {
        -Anthropic client
        +paranoid_review(code, scenario)
        +debugger_review(code, scenario)
        +veteran_review(code, scenario)
        -_call_agent(role, prompt)
    }

    class AgentReview {
        +string agent_role
        +string critique
        +list~string~ additional_concerns
        +list~string~ suggested_fixes
        +string validation
    }

    CodeReviewAgents --> AgentReview : produces
```

**Three Agents**:
- **Paranoid Engineer**: Finds edge cases, makes scenarios worse
- **Debugger**: Proposes fixes and mitigations
- **Production Veteran**: Validates with real-world experience

### 3. CodeCatastrophePredictor

**Responsibility**: Main orchestrator coordinating generation and review

```mermaid
classDiagram
    class CodeCatastrophePredictor {
        -CatastropheGenerator generator
        -CodeReviewAgents agents
        +predict(code_description, num_scenarios)
        +predict_with_review(code_description, num_scenarios)
        +analyze_risk(catastrophes)
        -_calculate_risk_score(catastrophes)
    }

    class PredictionResult {
        +list~Catastrophe~ catastrophes
        +dict agent_reviews
        +dict risk_analysis
        +datetime timestamp
    }

    CodeCatastrophePredictor --> CatastropheGenerator : uses
    CodeCatastrophePredictor --> CodeReviewAgents : uses
    CodeCatastrophePredictor --> PredictionResult : produces
```

---

## Data Flow

### End-to-End Prediction Flow

```mermaid
sequenceDiagram
    participant User
    participant Interface as CLI/Web
    participant Predictor as CodeCatastrophePredictor
    participant Generator as CatastropheGenerator
    participant Opus as Claude Opus 4.6
    participant Agents as CodeReviewAgents
    participant Risk as Risk Analyzer

    User->>Interface: Submit architecture/code
    Interface->>Predictor: predict_with_review()

    rect rgb(239, 68, 68, 0.1)
        Note over Predictor,Opus: Phase 1: Catastrophe Generation
        Predictor->>Generator: generate_catastrophes(code, n=5)
        Generator->>Opus: Prompt with code context
        Opus-->>Opus: Adaptive thinking mode
        Opus-->>Generator: JSON catastrophe scenarios
        Generator-->>Predictor: List[Catastrophe]
    end

    rect rgb(245, 158, 11, 0.1)
        Note over Predictor,Agents: Phase 2: Multi-Agent Review
        loop For each catastrophe
            Predictor->>Agents: paranoid_review(scenario)
            Agents->>Opus: "Make it worse" prompt
            Opus-->>Agents: Edge cases found

            Predictor->>Agents: debugger_review(scenario)
            Agents->>Opus: "Find fixes" prompt
            Opus-->>Agents: Mitigation strategies

            Predictor->>Agents: veteran_review(scenario)
            Agents->>Opus: "Validate realism" prompt
            Opus-->>Agents: Real-world validation
        end
        Agents-->>Predictor: Agent reviews
    end

    rect rgb(34, 197, 94, 0.1)
        Note over Predictor,Risk: Phase 3: Risk Analysis
        Predictor->>Risk: analyze_risk(catastrophes)
        Risk-->>Risk: Calculate probability distribution
        Risk-->>Risk: Assess impact severity
        Risk-->>Risk: Validate historical precedent
        Risk-->>Predictor: Risk scores & metrics
    end

    Predictor-->>Interface: Complete results
    Interface-->>User: Display catastrophes + reviews + risk
```

---

## Multi-Agent System

### Agent Interaction Architecture

```mermaid
graph TB
    subgraph "Input"
        CODE[Code/Architecture<br/>Description]
        SCENARIO[Generated<br/>Catastrophe]
    end

    subgraph "Agent Committee"
        PARANOID[🔴 Paranoid Engineer<br/>Makes scenarios worse<br/>Finds edge cases]
        DEBUGGER[🔧 Debugger<br/>Proposes fixes<br/>Suggests mitigations]
        VETERAN[🏆 Production Veteran<br/>Validates realism<br/>Cites real incidents]
    end

    subgraph "Consensus"
        MERGE[Merge Reviews<br/>Aggregate Insights]
        VALIDATE[Validation Score<br/>High/Medium/Low]
    end

    subgraph "Output"
        ENHANCED[Enhanced Catastrophe<br/>+ Agent Reviews<br/>+ Risk Score]
    end

    CODE --> PARANOID
    CODE --> DEBUGGER
    CODE --> VETERAN

    SCENARIO --> PARANOID
    SCENARIO --> DEBUGGER
    SCENARIO --> VETERAN

    PARANOID --> MERGE
    DEBUGGER --> MERGE
    VETERAN --> MERGE

    MERGE --> VALIDATE
    VALIDATE --> ENHANCED

    style PARANOID fill:#ef4444,stroke:#dc2626,color:#fff
    style DEBUGGER fill:#3b82f6,stroke:#2563eb,color:#fff
    style VETERAN fill:#10b981,stroke:#059669,color:#fff
```

### Agent Prompting Strategy

```mermaid
flowchart LR
    subgraph "Paranoid Engineer Prompt"
        P1[Base Scenario]
        P2[Find what could<br/>make it worse]
        P3[Identify edge cases]
        P4[Estimate worst-case<br/>impact]
    end

    subgraph "Debugger Prompt"
        D1[Base Scenario]
        D2[Identify root causes]
        D3[Propose fixes]
        D4[Suggest monitoring]
    end

    subgraph "Veteran Prompt"
        V1[Base Scenario]
        V2[Match to real<br/>incidents]
        V3[Assess likelihood]
        V4[Validate technical<br/>accuracy]
    end

    P1 --> P2 --> P3 --> P4
    D1 --> D2 --> D3 --> D4
    V1 --> V2 --> V3 --> V4

    P4 --> CONSENSUS{Consensus<br/>Mechanism}
    D4 --> CONSENSUS
    V4 --> CONSENSUS

    CONSENSUS --> OUTPUT[Final Validated<br/>Catastrophe]
```

---

## Catastrophe Generation Pipeline

### Opus 4.6 Adaptive Thinking Flow

```mermaid
stateDiagram-v2
    [*] --> ReceiveCode: Architecture input

    ReceiveCode --> ContextAnalysis: Opus 4.6 Adaptive Thinking

    state ContextAnalysis {
        [*] --> UnderstandSystem
        UnderstandSystem --> IdentifyComponents
        IdentifyComponents --> MapDependencies
        MapDependencies --> FindBottlenecks
        FindBottlenecks --> [*]
    }

    ContextAnalysis --> ScenarioGeneration: System understanding complete

    state ScenarioGeneration {
        [*] --> ImaginFailure
        ImaginFailure --> BuildCascade
        BuildCascade --> EstimateImpact
        EstimateImpact --> FindPrecedent
        FindPrecedent --> [*]
    }

    ScenarioGeneration --> FormatJSON: Scenarios generated

    FormatJSON --> ParseResponse: Return JSON

    state ParseResponse {
        [*] --> ExtractBlocks
        ExtractBlocks --> FindJSON
        FindJSON --> ValidateSchema
        ValidateSchema --> [*]
    }

    ParseResponse --> [*]: Catastrophes ready
```

### Content Block Handling

```mermaid
flowchart TD
    START[API Response Received] --> CHECK{Check<br/>Content Type}

    CHECK -->|Single Text Block| DIRECT[Extract text directly]
    CHECK -->|Multiple Blocks| ITERATE[Iterate through blocks]

    ITERATE --> BLOCK1{Block Type?}

    BLOCK1 -->|thinking| SKIP[Skip thinking block]
    BLOCK1 -->|text| EXTRACT[Extract text content]

    SKIP --> NEXT{More blocks?}
    EXTRACT --> CONCAT[Concatenate text]
    CONCAT --> NEXT

    NEXT -->|Yes| BLOCK1
    NEXT -->|No| COMPLETE[Complete text ready]

    DIRECT --> COMPLETE
    COMPLETE --> PARSE[Parse JSON]
    PARSE --> VALIDATE{Valid JSON?}

    VALIDATE -->|Yes| SUCCESS[Return catastrophes]
    VALIDATE -->|No| RETRY[Retry with stricter prompt]

    RETRY --> START

    style CHECK fill:#8b5cf6,color:#fff
    style ITERATE fill:#ef4444,color:#fff
    style SUCCESS fill:#10b981,color:#fff
```

---

## API & Interfaces

### CLI Tool Architecture

```mermaid
graph LR
    subgraph "CLI Entry Point"
        ARGS[argparse<br/>Command Arguments]
        VALIDATE[Validate Inputs]
    end

    subgraph "File Handling"
        READ[Read Architecture File]
        DETECT[Detect File Type<br/>.py .md .txt]
    end

    subgraph "Prediction Engine"
        PRED[CodeCatastrophePredictor]
        OPTS[Apply Options<br/>--scenarios --review]
    end

    subgraph "Output Formatting"
        CONSOLE[Console Display<br/>Rich Text]
        JSON_OUT[JSON Export<br/>--output flag]
    end

    ARGS --> VALIDATE
    VALIDATE --> READ
    READ --> DETECT
    DETECT --> PRED
    PRED --> OPTS
    OPTS --> CONSOLE
    OPTS --> JSON_OUT

    style ARGS fill:#3b82f6,color:#fff
    style PRED fill:#ef4444,color:#fff
```

### Web Demo Architecture

```mermaid
graph TB
    subgraph "Streamlit Frontend"
        UI[User Interface]
        INPUT[Text Input Area]
        SCENARIOS[Scenario Selector]
        BUTTON[Predict Button]
    end

    subgraph "Session State"
        CACHE[st.cache_data]
        STATE[st.session_state]
    end

    subgraph "Backend Processing"
        PREDICTOR[CodeCatastrophePredictor]
        SPINNER[Progress Indicator]
    end

    subgraph "Results Display"
        CARDS[Catastrophe Cards]
        METRICS[Risk Metrics]
        AGENTS_UI[Agent Reviews]
        EXPORT[Download JSON]
    end

    UI --> INPUT
    UI --> SCENARIOS
    INPUT --> BUTTON
    SCENARIOS --> BUTTON

    BUTTON --> STATE
    STATE --> PREDICTOR
    PREDICTOR --> SPINNER

    SPINNER --> CACHE
    CACHE --> CARDS
    CACHE --> METRICS
    CACHE --> AGENTS_UI
    CACHE --> EXPORT

    style UI fill:#3b82f6,color:#fff
    style PREDICTOR fill:#ef4444,color:#fff
    style CARDS fill:#10b981,color:#fff
```

### Python API Usage

```python
# Simple usage
from code_catastrophe_predictor import CodeCatastrophePredictor

predictor = CodeCatastrophePredictor()
results = predictor.predict(
    code_description="Your architecture here...",
    num_scenarios=5
)

# With multi-agent review
results = predictor.predict_with_review(
    code_description="Your architecture here...",
    num_scenarios=3
)

# Access results
for catastrophe in results['catastrophes']:
    print(f"Scenario: {catastrophe['scenario_name']}")
    print(f"Impact: {catastrophe['revenue_impact']}")
    print(f"Steps: {catastrophe['failure_steps']}")

# Risk analysis
risk = predictor.analyze_risk(results['catastrophes'])
print(f"Risk Score: {risk['risk_score']}/10")
```

---

## Deployment Architecture

### Local Development Setup

```mermaid
graph TB
    subgraph "Developer Machine"
        CODE[Source Code]
        VENV[Virtual Environment<br/>Python 3.11+]
        ENV[.env File<br/>ANTHROPIC_API_KEY]
    end

    subgraph "Dependencies"
        ANTHROPIC[anthropic>=0.39.0]
        STREAMLIT[streamlit>=1.39.0]
        DOTENV[python-dotenv>=1.0.0]
    end

    subgraph "Runtime"
        CLI_RUN[CLI Execution<br/>python catastrophe_cli.py]
        WEB_RUN[Web Demo<br/>streamlit run]
    end

    CODE --> VENV
    ENV --> VENV

    VENV --> ANTHROPIC
    VENV --> STREAMLIT
    VENV --> DOTENV

    VENV --> CLI_RUN
    VENV --> WEB_RUN

    style VENV fill:#3b82f6,color:#fff
    style ANTHROPIC fill:#8b5cf6,color:#fff
```

### CI/CD Integration

```mermaid
graph LR
    subgraph "Git Repository"
        COMMIT[Git Commit]
        PUSH[Git Push]
    end

    subgraph "CI Pipeline"
        TRIGGER[GitHub Actions Trigger]
        INSTALL[Install Dependencies]
        ANALYZE[Run Catastrophe Check]
    end

    subgraph "Analysis"
        READ[Read architecture.md]
        PREDICT[Generate Scenarios]
        THRESHOLD[Check Risk Score]
    end

    subgraph "Results"
        PASS[✅ Pass: Low Risk]
        WARN[⚠️ Warning: Medium Risk]
        FAIL[❌ Fail: High Risk]
        COMMENT[Post PR Comment]
    end

    COMMIT --> PUSH
    PUSH --> TRIGGER
    TRIGGER --> INSTALL
    INSTALL --> ANALYZE

    ANALYZE --> READ
    READ --> PREDICT
    PREDICT --> THRESHOLD

    THRESHOLD --> PASS
    THRESHOLD --> WARN
    THRESHOLD --> FAIL

    PASS --> COMMENT
    WARN --> COMMENT
    FAIL --> COMMENT

    style ANALYZE fill:#ef4444,color:#fff
    style PASS fill:#10b981,color:#fff
    style FAIL fill:#dc2626,color:#fff
```

### Example GitHub Action

```yaml
name: Catastrophe Check

on:
  pull_request:
    paths:
      - 'architecture/**'
      - 'src/**'

jobs:
  catastrophe-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -r requirements_catastrophe.txt

      - name: Run Catastrophe Predictor
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          python catastrophe_cli.py architecture/system.md \
            --scenarios 5 \
            --threshold 7 \
            --output results.json

      - name: Post PR Comment
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const results = JSON.parse(fs.readFileSync('results.json'));
            const comment = `## 💀 Catastrophe Analysis\n\n${results.summary}`;
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: comment
            });
```

---

## Data Structures

### Catastrophe Schema

```json
{
  "scenario_name": "The Black Friday Database Collapse",
  "failure_steps": [
    "PostgreSQL hits IOPS limits at 10K writes/sec",
    "Write latency spikes from 50ms to 5 seconds",
    "Payment timeout rate jumps from 0.1% to 40%",
    "Cart abandonment increases by 300%",
    "Revenue loss: $5-10M in 2 hours"
  ],
  "probability": "medium-high",
  "impact_assessment": "catastrophic - system-wide payment failures",
  "revenue_impact": "$5M-$10M in 2 hours",
  "users_affected": "All active users (500K+ concurrent)",
  "duration": "2-4 hours until emergency read-only mode deployed",
  "historical_precedent": "Similar to 2023 Black Friday Shopify incident..."
}
```

### Agent Review Schema

```json
{
  "paranoid_engineer": {
    "additional_concerns": [
      "Cache invalidation storm could amplify the issue",
      "Retry logic might create thundering herd"
    ],
    "edge_cases": [
      "What if database failover also fails?",
      "Dead letter queue overflow"
    ]
  },
  "debugger": {
    "root_causes": ["Insufficient IOPS provisioning", "No rate limiting"],
    "suggested_fixes": [
      "Implement queue-based write buffering",
      "Add circuit breaker pattern"
    ],
    "monitoring": ["Track write latency p99", "Alert on IOPS > 80%"]
  },
  "production_veteran": {
    "validation": "Highly realistic - matches common patterns",
    "real_incidents": ["Shopify 2023", "Stripe 2022"],
    "likelihood": "7/10 - very possible during peak traffic"
  }
}
```

### Risk Analysis Schema

```json
{
  "risk_score": 8,
  "probability_distribution": {
    "high": 2,
    "medium": 2,
    "low": 1
  },
  "impact_summary": {
    "system_wide": 3,
    "isolated": 2
  },
  "top_concerns": [
    "Database IOPS exhaustion",
    "Payment processing cascade failure"
  ],
  "recommended_actions": [
    "Conduct load testing at 3x peak traffic",
    "Implement circuit breaker on payment flow"
  ]
}
```

---

## Performance Considerations

### Opus 4.6 API Usage

```mermaid
graph LR
    subgraph "Single Catastrophe Generation"
        GEN1[Generate 5 scenarios<br/>~15-20 seconds]
    end

    subgraph "Multi-Agent Review"
        REV1[Paranoid: ~8s]
        REV2[Debugger: ~8s]
        REV3[Veteran: ~8s]
    end

    subgraph "Total Time"
        TOTAL[Total: ~40-45 seconds<br/>for full analysis]
    end

    GEN1 --> REV1
    REV1 --> REV2
    REV2 --> REV3
    REV3 --> TOTAL

    style GEN1 fill:#ef4444,color:#fff
    style TOTAL fill:#10b981,color:#fff
```

### Optimization Strategies

1. **Batch Processing**: Generate multiple scenarios in one API call (current implementation)
2. **Caching**: Cache results for identical architecture descriptions
3. **Parallel Agent Calls**: Run 3 agents concurrently (future enhancement)
4. **Streaming**: Stream results as they're generated (future enhancement)

### Cost Estimation

```python
# Approximate costs (as of 2026)
OPUS_INPUT_COST = 0.015  # per 1K tokens
OPUS_OUTPUT_COST = 0.075  # per 1K tokens

# Typical usage per analysis:
# - Input: ~2K tokens (architecture) * 4 calls = 8K tokens
# - Output: ~3K tokens per call * 4 = 12K tokens
# Total: ~$0.90-$1.20 per full analysis with multi-agent review
```

---

## Security Considerations

### API Key Management

```mermaid
graph TB
    subgraph "Environment Variables"
        ENV[.env file<br/>ANTHROPIC_API_KEY]
        GITIGNORE[.gitignore<br/>excludes .env]
    end

    subgraph "CI/CD Secrets"
        GITHUB[GitHub Secrets<br/>Encrypted storage]
    end

    subgraph "Application"
        DOTENV[python-dotenv<br/>Loads at runtime]
        CLIENT[Anthropic Client<br/>Authenticated calls]
    end

    ENV --> GITIGNORE
    ENV --> DOTENV
    GITHUB --> DOTENV
    DOTENV --> CLIENT

    style GITIGNORE fill:#10b981,color:#fff
    style GITHUB fill:#3b82f6,color:#fff
```

### Input Validation

- Architecture descriptions limited to 50KB
- Number of scenarios capped at 10 per request
- Rate limiting to prevent API abuse
- No execution of generated code (read-only analysis)

---

## Future Enhancements

```mermaid
mindmap
  root((Future<br/>Enhancements))
    Performance
      Parallel agent execution
      Streaming results
      Result caching layer
    Features
      Integration with GitHub PRs
      Slack notifications
      Custom agent personalities
      Historical incident database
    Scalability
      API service deployment
      Multi-tenant support
      Analytics dashboard
    Intelligence
      Learn from validated catastrophes
      Auto-prioritize by codebase context
      Suggest proactive fixes
```

---

## Conclusion

The Code Catastrophe Predictor architecture is designed for:

✅ **Modularity** - Clear separation between generation, review, and analysis
✅ **Extensibility** - Easy to add new agents or interfaces
✅ **Performance** - Optimized API usage with batching
✅ **Reliability** - Multi-agent validation prevents false positives
✅ **Usability** - Multiple interfaces (CLI, Web, API) for different workflows

The system leverages Opus 4.6's unique adaptive thinking capability to discover failure modes that traditional testing cannot imagine, making it a powerful tool for production readiness assessment.

---

**Built with Claude Opus 4.6 | Anthropic Claude Code Hackathon 2026**
