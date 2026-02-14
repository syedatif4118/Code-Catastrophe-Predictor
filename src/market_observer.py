"""
Autonomous Alpha - Market Observer
Fetches market data via MCP client and calculates technical indicators.
"""
import asyncio
from datetime import datetime
from decimal import Decimal
from typing import Optional
import pandas as pd
import numpy as np

from src.models import MarketData
from src.mcp_client import MCPClient


class MarketObserver:
    """Fetch market data and compute indicators."""

    def __init__(self, mcp_client: MCPClient):
        self.mcp_client = mcp_client
        self._price_history: dict[str, list[float]] = {}

    async def fetch_market_data(self, symbol: str) -> MarketData:
        """
        Fetch current market data for a symbol and compute RSI.

        Args:
            symbol: Stock symbol

        Returns:
            MarketData with price, volume, and RSI indicator
        """
        # Get current quote from yfinance
        quote = await self.mcp_client.call_tool(
            "yfinance",
            "get_quote",
            {"symbol": symbol}
        )

        price = quote.get("price", 0)
        volume = quote.get("volume", 0)

        # Get historical data for better RSI calculation
        if symbol not in self._price_history or len(self._price_history[symbol]) < 20:
            try:
                historical = await self.mcp_client.call_tool(
                    "yfinance",
                    "get_historical",
                    {"symbol": symbol, "period": "1mo"}
                )

                # Extract closing prices from historical data
                hist_data = historical.get("historical", [])
                if hist_data:
                    # yfinance returns oldest to newest, so use directly
                    self._price_history[symbol] = [float(d.get("close", 0)) for d in hist_data]
            except Exception as e:
                # Fallback to building history incrementally
                if symbol not in self._price_history:
                    self._price_history[symbol] = []

        # Update with current price
        if symbol in self._price_history:
            self._price_history[symbol].append(price)
            # Keep last 50 prices for RSI calculation
            if len(self._price_history[symbol]) > 50:
                self._price_history[symbol] = self._price_history[symbol][-50:]
        else:
            self._price_history[symbol] = [price]

        # Calculate RSI(14)
        rsi = self._calculate_rsi(self._price_history[symbol], period=14)

        return MarketData(
            symbol=symbol,
            timestamp=datetime.utcnow(),
            price=Decimal(str(price)),
            volume=volume,
            rsi_14=rsi
        )

    def _calculate_rsi(self, prices: list[float], period: int = 14) -> Optional[float]:
        """
        Calculate RSI (Relative Strength Index).

        Args:
            prices: List of historical prices
            period: RSI period (default 14)

        Returns:
            RSI value (0-100) or None if insufficient data
        """
        if len(prices) < period + 1:
            return None

        prices_array = np.array(prices)
        deltas = np.diff(prices_array)

        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)

        avg_gain = np.mean(gains[-period:])
        avg_loss = np.mean(losses[-period:])

        if avg_loss == 0:
            return 100.0

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        return float(rsi)
