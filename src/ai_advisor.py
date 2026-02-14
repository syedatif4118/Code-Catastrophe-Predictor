"""
AI Trading Advisor - Claude-powered conversational trading assistant
"""
import os
from anthropic import Anthropic


class AITradingAdvisor:
    """
    Conversational AI advisor powered by Claude 4.6
    Explains trading decisions, answers questions, provides education
    """

    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.conversation_history = []

    def ask(self, question: str, context: dict = None) -> str:
        """
        Ask the AI advisor a question about trading

        Args:
            question: User's question
            context: Additional context (market data, signals, etc.)

        Returns:
            AI advisor's response
        """
        # Build context-aware prompt
        system_prompt = """You are an expert AI trading advisor for the Autonomous Alpha system.
        You help users understand trading decisions, learn about markets, and make informed choices.

        Your style:
        - Clear and educational
        - Use analogies for complex concepts
        - Provide specific, actionable insights
        - Always mention risks
        - Reference actual data when available

        You have access to:
        - Real-time market data (prices, RSI indicators)
        - Trading signals and their rationale
        - Risk management data
        - Historical performance
        """

        # Add context to the message
        context_str = ""
        if context:
            context_str = f"\n\nCurrent Context:\n{self._format_context(context)}"

        user_message = f"{question}{context_str}"

        # Call Claude API
        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_message}
                ]
            )

            answer = response.content[0].text

            # Store in conversation history
            self.conversation_history.append({
                "question": question,
                "answer": answer
            })

            return answer

        except Exception as e:
            return f"I apologize, but I'm having trouble connecting to my AI brain right now. Error: {str(e)}"

    def explain_signal(self, signal_data: dict) -> str:
        """
        Explain why a trading signal was generated

        Args:
            signal_data: Signal information (symbol, action, RSI, price, etc.)

        Returns:
            Detailed explanation
        """
        symbol = signal_data.get('symbol', 'N/A')
        action = signal_data.get('action', 'N/A')
        rsi = signal_data.get('rsi', 'N/A')
        price = signal_data.get('price', 'N/A')
        confidence = signal_data.get('confidence', 0)

        question = f"""
        Explain in detail why we generated a {action} signal for {symbol}.

        Current metrics:
        - RSI(14): {rsi}
        - Price: ${price}
        - Signal Confidence: {confidence:.1%}

        Please explain:
        1. What RSI tells us about this stock
        2. Why {action} makes sense right now
        3. What risks should traders be aware of
        4. What to watch for next

        Keep it educational and actionable.
        """

        return self.ask(question)

    def explain_concept(self, concept: str) -> str:
        """
        Explain a trading concept in simple terms

        Args:
            concept: Trading concept (e.g., "RSI", "Mean Reversion")

        Returns:
            Simple explanation
        """
        question = f"""
        Explain '{concept}' in simple terms that a beginner can understand.

        Use:
        - An analogy or real-world example
        - Simple language (no jargon)
        - Why it matters for trading
        - How our system uses it

        Keep it under 150 words.
        """

        return self.ask(question)

    def analyze_news(self, symbol: str, news_items: list) -> dict:
        """
        Analyze news sentiment for a stock

        Args:
            symbol: Stock symbol
            news_items: List of news headlines/descriptions

        Returns:
            Sentiment analysis with reasoning
        """
        news_text = "\n".join([f"- {item}" for item in news_items[:5]])

        question = f"""
        Analyze the sentiment of recent news for {symbol}:

        {news_text}

        Provide:
        1. Overall sentiment (Bullish/Neutral/Bearish) with confidence %
        2. Key themes in the news
        3. How this might affect the stock price short-term
        4. Any red flags or opportunities

        Format your response as:
        SENTIMENT: [Bullish/Neutral/Bearish] (X% confidence)
        KEY THEMES: [themes]
        IMPACT: [likely impact]
        RECOMMENDATION: [trading implication]
        """

        response = self.ask(question)

        # Parse response
        sentiment = "Neutral"
        if "Bullish" in response:
            sentiment = "Bullish"
        elif "Bearish" in response:
            sentiment = "Bearish"

        return {
            "sentiment": sentiment,
            "analysis": response,
            "news_count": len(news_items)
        }

    def what_if_scenario(self, scenario: str, portfolio_data: dict) -> str:
        """
        Simulate "what-if" scenarios

        Args:
            scenario: Scenario description (e.g., "market drops 20%")
            portfolio_data: Current portfolio information

        Returns:
            Impact analysis and recommendations
        """
        question = f"""
        Analyze this scenario: "{scenario}"

        Current portfolio:
        {self._format_context(portfolio_data)}

        Please provide:
        1. Immediate impact on portfolio value (estimate %)
        2. Which positions are most at risk
        3. What actions to take (hedge, reduce exposure, etc.)
        4. Historical context (what happened in similar scenarios)
        5. Recovery timeline (if applicable)

        Be specific and actionable.
        """

        return self.ask(question)

    def generate_strategy_from_nlp(self, description: str) -> dict:
        """
        Generate trading strategy code from natural language

        Args:
            description: Plain English strategy description

        Returns:
            Strategy parameters and Python code
        """
        question = f"""
        User wants to create a trading strategy: "{description}"

        Generate a Python strategy implementation following this format:

        1. STRATEGY NAME: [descriptive name]
        2. PARAMETERS: [list key parameters like thresholds, periods]
        3. LOGIC: [explain the buy/sell logic]
        4. RISKS: [what could go wrong]

        Then provide Python code for a strategy class similar to MeanReversionStrategy.

        Include:
        - Clear variable names
        - Comments explaining each step
        - Proper risk checks
        """

        response = self.ask(question)

        return {
            "description": description,
            "implementation": response,
            "status": "generated"
        }

    def _format_context(self, context: dict) -> str:
        """Format context dictionary for Claude"""
        lines = []
        for key, value in context.items():
            lines.append(f"- {key}: {value}")
        return "\n".join(lines)

    def get_educational_tip(self) -> str:
        """Get a random educational trading tip"""
        question = """
        Provide ONE short trading tip for beginners.

        Format:
        💡 TIP: [tip title]
        [2-3 sentence explanation]

        Topics: risk management, patience, diversification, emotions, research

        Make it practical and memorable.
        """

        return self.ask(question)
