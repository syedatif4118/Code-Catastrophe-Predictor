"""
Autonomous Alpha - Strategy Engine
Stateless, side-effect free signal generation.
"""
from datetime import datetime
from typing import Optional

from src.models import MarketData, TradeSignal, TradingAction


class MeanReversionStrategy:
    """
    Mean Reversion Strategy using RSI(14).

    Rules:
    - RSI < 30: Oversold → BUY signal
    - RSI > 70: Overbought → SELL signal
    - Otherwise: HOLD
    """

    def __init__(
        self,
        name: str = "MeanReversion_RSI14",
        oversold_threshold: float = 30.0,
        overbought_threshold: float = 70.0,
        position_size: int = 2,
    ):
        self.name = name
        self.oversold_threshold = oversold_threshold
        self.overbought_threshold = overbought_threshold
        self.position_size = position_size

    def generate_signal(self, market_data: MarketData) -> Optional[TradeSignal]:
        """
        Generate trading signal based on RSI indicator.

        Args:
            market_data: Current market data with RSI

        Returns:
            TradeSignal if action required, None for HOLD
        """
        if market_data.rsi_14 is None:
            return None

        rsi = market_data.rsi_14
        action = TradingAction.HOLD
        rationale = ""
        confidence = 0.0

        # Mean Reversion Logic
        if rsi < self.oversold_threshold:
            action = TradingAction.BUY
            rationale = (
                f"RSI({rsi:.2f}) < {self.oversold_threshold} indicates oversold condition. "
                f"Mean reversion suggests price will rise. Initiating BUY."
            )
            confidence = (self.oversold_threshold - rsi) / self.oversold_threshold

        elif rsi > self.overbought_threshold:
            action = TradingAction.SELL
            rationale = (
                f"RSI({rsi:.2f}) > {self.overbought_threshold} indicates overbought condition. "
                f"Mean reversion suggests price will fall. Initiating SELL."
            )
            confidence = (rsi - self.overbought_threshold) / (100 - self.overbought_threshold)

        else:
            # HOLD - no signal
            return None

        # Cap confidence at 1.0
        confidence = min(confidence, 1.0)

        return TradeSignal(
            symbol=market_data.symbol,
            action=action,
            quantity=self.position_size,
            rationale=rationale,
            confidence=confidence,
            timestamp=datetime.utcnow(),
            strategy_name=self.name,
            indicators={
                "rsi_14": rsi,
                "price": float(market_data.price),
            }
        )
