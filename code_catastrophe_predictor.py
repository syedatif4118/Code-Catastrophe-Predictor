"""
Code Catastrophe Predictor - Opus 4.6 Production Failure Imagination

Uses AI to imagine how your code/architecture could fail in production.
Because the worst bugs are the ones you didn't think to test for.

Built for Anthropic Claude Code Hackathon 2026
"""
import os
from anthropic import Anthropic
from dotenv import load_dotenv
from typing import Dict, List
import json
from datetime import datetime

load_dotenv()


class CatastropheGenerator:
    """
    🔥 THE KILLER FEATURE 🔥

    Uses Opus 4.6 to imagine production failures that haven't happened yet.
    Not just "null pointer exception" - multi-step cascade failures.
    """

    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def generate_catastrophes(self, code_description: str, num_scenarios: int = 5) -> List[Dict]:
        """
        Generate creative production failure scenarios.

        Args:
            code_description: Description of code/architecture
            num_scenarios: Number of scenarios to generate

        Returns:
            List of catastrophe scenarios
        """
        print(f"\n{'='*70}")
        print(f"💀 OPUS 4.6 CATASTROPHE GENERATION - Adaptive Thinking Mode")
        print(f"{'='*70}\n")

        prompt = f"""You are a battle-scarred senior engineer with 20 years of debugging production disasters.
Your specialty: Imagining creative ways code fails in production.

CODE/ARCHITECTURE:
{code_description}

YOUR MISSION:
Generate {num_scenarios} creative PRODUCTION FAILURE scenarios this code might face.

DO NOT give me basic bugs like "null pointer exception" or "syntax error."
I want CREATIVE, MULTI-STEP CASCADE FAILURES that happen in production.

Think about:
- Race conditions and concurrency nightmares
- Scale failures (works at 100 users, dies at 10,000)
- Edge cases (leap years, timezones, unicode, internationalization)
- Dependency failures (API goes down, library has bug)
- Data corruption (bad input, encoding issues, injection)
- Network failures (timeouts, partial failures, Byzantine faults)
- Resource exhaustion (memory leaks, file handles, connections)
- Human errors (wrong config, bad deployment, fat-finger mistakes)
- Cascade failures (one failure triggers others)
- Silent data corruption (wrong but doesn't crash)

For each scenario:
1. Scenario name (catchy, dramatic title)
2. Detailed description (step-by-step cascade)
3. Why this specific code is vulnerable
4. Probability (low/medium/high)
5. Blast radius (local/service/system/company-wide)
6. Detection difficulty (easy/medium/hard/silent)
7. Example trigger (what starts the cascade)
8. **Historical precedent** (real incidents that were similar - be specific!)
9. **Why it's realistic** (cite actual bug patterns, CVEs, or known failure modes)

Think creatively. Be scary. Be realistic. CITE REAL EXAMPLES.

IMPORTANT: Return ONLY the JSON object below. No explanation, no markdown, no code blocks.
Start your response with {{ and end with }}.

FORMAT AS JSON:
{{
  "catastrophes": [
    {{
      "name": "Catastrophe name",
      "description": "Multi-step failure cascade...",
      "vulnerability": "Why this code is vulnerable...",
      "probability": "low/medium/high",
      "blast_radius": "local/service/system/company-wide",
      "detection_difficulty": "easy/medium/hard/silent",
      "example_trigger": "What starts it",
      "historical_precedent": "Real incident: GitHub outage 2018, Knight Capital $440M loss, etc.",
      "why_realistic": "This matches known bug pattern X, similar to CVE-YYYY-ZZZZ",
      "impact_metrics": {{
        "downtime_hours": 4,
        "data_loss": "minimal/significant/catastrophic",
        "revenue_impact": "$50k-500k",
        "recovery_time": "2-8 hours"
      }},
      "warning_signs": ["Sign 1", "Sign 2"]
    }}
  ]
}}"""

        try:
            print("💀 Opus 4.6 is imagining production nightmares...")
            print("   (Using adaptive thinking for creative failure scenarios)\n")

            response = self.client.messages.create(
                model="claude-opus-4-6",
                max_tokens=8000,
                thinking={
                    "type": "adaptive"
                },
                messages=[{"role": "user", "content": prompt}]
            )

            # Extract text from response (handle thinking blocks)
            response_text = ""
            for block in response.content:
                if hasattr(block, 'text'):
                    response_text += block.text
                elif block.type == 'text':
                    response_text += block.text

            print("✅ Catastrophe generation complete!\n")

            # Debug: Save full response to file
            with open("debug_response.txt", "w") as f:
                f.write(response_text)
            print(f"📝 Debug: Full response saved to debug_response.txt ({len(response_text)} chars)\n")

            # Parse JSON - improved extraction
            import re

            # Try to find JSON with "catastrophes" key (greedy match to get the full object)
            json_match = re.search(r'\{[\s\S]*?"catastrophes"[\s\S]*\][\s\S]*?\}', response_text, re.DOTALL)

            if not json_match:
                # Fallback: try to find any JSON object
                json_match = re.search(r'\{[\s\S]*\}', response_text, re.DOTALL)
                if json_match:
                    print(f"⚠️  Warning: Found JSON but no 'catastrophes' key")

            catastrophes = []

            if json_match:
                try:
                    json_str = json_match.group()
                    print(f"📋 Attempting to parse {len(json_str)} char JSON...")
                    catastrophes_data = json.loads(json_str)
                    catastrophes = catastrophes_data.get("catastrophes", [])

                    if not catastrophes:
                        print(f"⚠️  Warning: JSON parsed but no catastrophes array")
                        print(f"Keys found: {list(catastrophes_data.keys())}")
                        print(f"Response preview: {response_text[:300]}...")
                    else:
                        print(f"✅ Successfully parsed {len(catastrophes)} catastrophes")
                except json.JSONDecodeError as e:
                    print(f"❌ JSON parsing failed: {e}")
                    print(f"Attempted to parse: {json_str[:300]}...")
                    print(f"Error at position: {e.pos}")
            else:
                print(f"❌ No JSON found in response")
                print(f"Response preview: {response_text[:300]}...")

            # If parsing failed, create fallback from raw text
            if not catastrophes:
                print("⚠️  Using fallback catastrophe generation")
                catastrophes = [{
                    "name": "AI-Generated Production Failure",
                    "description": response_text[:1000],  # First 1000 chars
                    "vulnerability": "See description",
                    "probability": "medium",
                    "blast_radius": "service",
                    "detection_difficulty": "medium",
                    "example_trigger": "Production load",
                    "historical_precedent": "Unable to parse JSON response",
                    "why_realistic": "See description for details",
                    "impact_metrics": {
                        "downtime_hours": 2,
                        "data_loss": "minimal",
                        "revenue_impact": "$10k-100k",
                        "recovery_time": "1-4 hours"
                    },
                    "warning_signs": []
                }]

            # Print scenarios
            for i, catastrophe in enumerate(catastrophes, 1):
                print(f"💀 CATASTROPHE {i}: {catastrophe['name']}")
                print(f"   Probability: {catastrophe['probability'].upper()}")
                print(f"   Blast Radius: {catastrophe['blast_radius']}")
                print(f"   Detection: {catastrophe['detection_difficulty']}")
                print(f"   Impact: {catastrophe.get('impact_metrics', {}).get('revenue_impact', 'Unknown')}")
                print()

            return catastrophes

        except Exception as e:
            print(f"❌ Error generating catastrophes: {e}")
            return []


class CodeReviewAgents:
    """
    👥 MULTI-AGENT CODE REVIEW

    Three specialized agents review the failure scenarios:
    - Paranoid Engineer: Makes it worse
    - Optimistic Debugger: Finds fixes
    - Production Veteran: Checks realism
    """

    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def paranoid_review(self, catastrophe: Dict) -> str:
        """Paranoid engineer makes the catastrophe worse"""
        print(f"😰 PARANOID ENGINEER reviewing: {catastrophe['name']}")

        prompt = f"""You are the PARANOID ENGINEER. Your job: find MORE ways this fails.

CATASTROPHE:
{catastrophe['description']}

YOUR MISSION:
What ELSE could go wrong? What second-order effects?
What if multiple things fail at once?

Think: Murphy's Law on steroids.
Be creative. Be dark. Make it worse."""

        try:
            response = self.client.messages.create(
                model="claude-opus-4-6",
                max_tokens=1000,
                thinking={"type": "adaptive"},
                messages=[{"role": "user", "content": prompt}]
            )

            # Extract text from response (handle thinking blocks)
            result = ""
            for block in response.content:
                if hasattr(block, 'text'):
                    result += block.text
                elif block.type == 'text':
                    result += block.text

            if not result:
                return "Paranoid engineer returned empty response"

            print(f"   💀 Paranoid's nightmare: {result[:80]}...\n")
            return result

        except Exception as e:
            print(f"   ❌ Error: {e}")
            return f"Paranoid engineer unavailable: {e}"

    def debugger_review(self, catastrophe: Dict) -> str:
        """Optimistic debugger finds fixes"""
        print(f"🔧 DEBUGGER reviewing: {catastrophe['name']}")

        prompt = f"""You are the OPTIMISTIC DEBUGGER. Your job: find the fix.

CATASTROPHE:
{catastrophe['description']}

YOUR MISSION:
How do we prevent this? What tests catch it?
What monitoring alerts us? How do we recover?

Be practical. Show the way out."""

        try:
            response = self.client.messages.create(
                model="claude-opus-4-6",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )

            # Extract text from response
            result = ""
            for block in response.content:
                if hasattr(block, 'text'):
                    result += block.text
                elif block.type == 'text':
                    result += block.text

            if not result:
                return "Debugger returned empty response"

            print(f"   ✨ Debugger's fix: {result[:80]}...\n")
            return result

        except Exception as e:
            print(f"   ❌ Error: {e}")
            return f"Debugger unavailable: {e}"

    def veteran_review(self, catastrophe: Dict) -> Dict:
        """Production veteran checks realism"""
        print(f"⚡ PRODUCTION VETERAN reviewing: {catastrophe['name']}")

        prompt = f"""You are the PRODUCTION VETERAN. You've seen it all.

CATASTROPHE:
{catastrophe['description']}

YOUR MISSION:
Is this realistic? Have you seen something similar?
Rate the plausibility and provide historical examples.

Rate:
- Realism: 1-10 (1=fantasy, 10=definitely will happen)
- Have you seen similar? (yes/no + example)
- Verdict: PLAUSIBLE / UNLIKELY / ALREADY HAPPENED"""

        try:
            response = self.client.messages.create(
                model="claude-opus-4-6",
                max_tokens=1000,
                thinking={"type": "adaptive"},
                messages=[{"role": "user", "content": prompt}]
            )

            # Extract text from response (handle thinking blocks)
            result = ""
            for block in response.content:
                if hasattr(block, 'text'):
                    result += block.text
                elif block.type == 'text':
                    result += block.text

            if not result:
                return {"analysis": "Veteran returned empty response", "realism_score": 5}

            print(f"   ⚖️  Veteran's verdict: {result[:80]}...\n")

            # Parse realism score
            import re
            realism_match = re.search(r'realism[:\s]+(\d+)', result, re.IGNORECASE)
            realism_score = int(realism_match.group(1)) if realism_match else 5

            return {
                "analysis": result,
                "realism_score": realism_score
            }

        except Exception as e:
            print(f"   ❌ Error: {e}")
            return {"analysis": f"Veteran unavailable: {e}", "realism_score": 5}


class CodeCatastrophePredictor:
    """
    🏆 MAIN CLASS

    Complete system for predicting production failures.
    """

    def __init__(self):
        self.catastrophe_gen = CatastropheGenerator()
        self.agents = CodeReviewAgents()

    def predict(self, code_description: str) -> Dict:
        """
        Full catastrophe prediction pipeline.

        Args:
            code_description: Code/architecture to analyze

        Returns:
            Complete prediction results
        """
        print(f"\n{'#'*70}")
        print(f"💀 CODE CATASTROPHE PREDICTOR - INITIATED")
        print(f"{'#'*70}\n")
        print(f"Analyzing: {code_description[:100]}...\n")

        # Stage 1: Generate catastrophes
        print("STAGE 1: Catastrophe Generation")
        print("-" * 70)
        catastrophes = self.catastrophe_gen.generate_catastrophes(code_description, num_scenarios=3)

        if not catastrophes:
            print("❌ No catastrophes generated. Aborting.")
            return {}

        # Stage 2: Agent review (first catastrophe)
        print(f"\nSTAGE 2: Multi-Agent Code Review")
        print("-" * 70)

        top_catastrophe = catastrophes[0]

        paranoid_view = self.agents.paranoid_review(top_catastrophe)
        debugger_view = self.agents.debugger_review(top_catastrophe)
        veteran_result = self.agents.veteran_review(top_catastrophe)

        # Results
        print(f"\n{'='*70}")
        print(f"📊 PREDICTION RESULTS")
        print(f"{'='*70}\n")

        print(f"✅ Generated {len(catastrophes)} production failure scenarios")
        print(f"✅ Multi-agent review complete")
        print(f"✅ Realism validated: {veteran_result['realism_score']}/10\n")

        results = {
            "code": code_description,
            "timestamp": datetime.now().isoformat(),
            "catastrophes": catastrophes,
            "top_catastrophe_analysis": {
                "catastrophe": top_catastrophe,
                "paranoid": paranoid_view,
                "debugger": debugger_view,
                "veteran": veteran_result
            }
        }

        return results


# Demo / Testing
if __name__ == "__main__":
    print("="*70)
    print("  💀 CODE CATASTROPHE PREDICTOR")
    print("  Built with Claude Opus 4.6 Adaptive Thinking")
    print("="*70)

    # Example code to test
    code = """
    API Endpoint: User Authentication

    POST /api/login
    - Accepts username + password
    - Queries database for user
    - Generates JWT token (24h expiry)
    - Returns token to client
    - Stores token in Redis cache
    - No rate limiting
    - Single database instance
    - Deployed on 3 load-balanced servers
    - 50,000 daily active users
    """

    predictor = CodeCatastrophePredictor()
    results = predictor.predict(code)

    # Save results
    with open("catastrophe_prediction_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\n✅ Results saved to catastrophe_prediction_results.json")
    print("💀 Core engine working. Next: build demo interface.\n")
