"""
Autonomous Alpha - MCP Client Wrapper
Async client for communicating with local MCP servers (yfinance, Alpaca).
"""
import asyncio
import json
import os
from typing import Any, Optional
from pathlib import Path


class MCPClient:
    """
    Wrapper for MCP servers defined in config/mcp_config.json.
    In a real implementation, this would use the MCP protocol.
    For this prototype, we'll use direct API calls via the installed libraries.
    """

    def __init__(self, config_path: str):
        self.config_path = Path(config_path)
        self.config: dict[str, Any] = {}
        self._load_config()

    def _load_config(self):
        """Load and interpolate environment variables in MCP config."""
        with open(self.config_path, 'r') as f:
            raw_config = json.load(f)

        # Interpolate ${VAR} placeholders with environment variables
        self.config = self._interpolate_env_vars(raw_config)

    def _interpolate_env_vars(self, obj: Any) -> Any:
        """Recursively interpolate ${VAR} with environment variables."""
        if isinstance(obj, dict):
            return {k: self._interpolate_env_vars(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._interpolate_env_vars(item) for item in obj]
        elif isinstance(obj, str):
            # Simple ${VAR} replacement
            if obj.startswith('${') and obj.endswith('}'):
                var_name = obj[2:-1]
                return os.getenv(var_name, obj)
            return obj
        return obj

    async def call_tool(self, server_name: str, tool_name: str, arguments: dict) -> dict:
        """
        Call a tool on an MCP server.

        Args:
            server_name: Name of MCP server (e.g., 'yfinance', 'alpaca')
            tool_name: Tool to invoke (e.g., 'get_quote', 'place_order')
            arguments: Tool arguments

        Returns:
            Tool response as dictionary
        """
        # In production, this would use MCP protocol
        # For now, we'll delegate to the appropriate API wrapper

        if server_name == "yfinance":
            return await self._call_yfinance(tool_name, arguments)
        elif server_name == "alpaca":
            return await self._call_alpaca(tool_name, arguments)
        else:
            raise ValueError(f"Unknown MCP server: {server_name}")

    async def _call_yfinance(self, tool_name: str, arguments: dict) -> dict:
        """Call yfinance (Yahoo Finance) - Free, no API key needed."""
        import yfinance as yf

        if tool_name == "get_quote":
            symbol = arguments.get('symbol')

            loop = asyncio.get_event_loop()

            def fetch_quote():
                ticker = yf.Ticker(symbol)
                info = ticker.info
                hist = ticker.history(period="1d")

                if hist.empty:
                    raise Exception(f"No data available for {symbol}")

                current_price = hist['Close'].iloc[-1]
                volume = hist['Volume'].iloc[-1]

                return {
                    "symbol": symbol,
                    "price": float(current_price),
                    "volume": int(volume),
                    "change": float(info.get('regularMarketChange', 0)),
                    "changesPercentage": float(info.get('regularMarketChangePercent', 0)),
                }

            return await loop.run_in_executor(None, fetch_quote)

        elif tool_name == "get_historical":
            symbol = arguments.get('symbol')
            period = arguments.get('period', '1mo')  # 1 month default

            loop = asyncio.get_event_loop()

            def fetch_historical():
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period=period)

                if hist.empty:
                    raise Exception(f"No historical data for {symbol}")

                historical = []
                for date, row in hist.iterrows():
                    historical.append({
                        "date": date.strftime("%Y-%m-%d"),
                        "close": float(row['Close']),
                        "volume": int(row['Volume']),
                        "open": float(row['Open']),
                        "high": float(row['High']),
                        "low": float(row['Low']),
                    })

                return {
                    "symbol": symbol,
                    "historical": historical
                }

            return await loop.run_in_executor(None, fetch_historical)

        raise ValueError(f"Unknown yfinance tool: {tool_name}")

    async def _call_alpaca(self, tool_name: str, arguments: dict) -> dict:
        """Call Alpaca API via alpaca-py library."""
        from alpaca.trading.client import TradingClient
        from alpaca.trading.requests import MarketOrderRequest
        from alpaca.trading.enums import OrderSide, TimeInForce

        api_key = self.config.get('mcpServers', {}).get('alpaca', {}).get('env', {}).get('ALPACA_API_KEY')
        secret_key = self.config.get('mcpServers', {}).get('alpaca', {}).get('env', {}).get('ALPACA_SECRET_KEY')

        client = TradingClient(api_key, secret_key, paper=True)

        if tool_name == "get_account":
            account = client.get_account()
            return {
                "buying_power": float(account.buying_power),
                "equity": float(account.equity),
                "cash": float(account.cash),
            }

        elif tool_name == "get_position":
            symbol = arguments.get('symbol')
            try:
                position = client.get_open_position(symbol)
                return {
                    "symbol": symbol,
                    "qty": int(position.qty),
                    "market_value": float(position.market_value),
                    "avg_entry_price": float(position.avg_entry_price),
                }
            except Exception:
                return {
                    "symbol": symbol,
                    "qty": 0,
                    "market_value": 0.0,
                    "avg_entry_price": 0.0,
                }

        elif tool_name == "place_order":
            symbol = arguments.get('symbol')
            side = OrderSide.BUY if arguments.get('side') == 'BUY' else OrderSide.SELL
            qty = arguments.get('qty')

            order_data = MarketOrderRequest(
                symbol=symbol,
                qty=qty,
                side=side,
                time_in_force=TimeInForce.DAY
            )

            order = client.submit_order(order_data)
            return {
                "order_id": str(order.id),
                "symbol": order.symbol,
                "qty": int(order.qty),
                "side": order.side.value,
                "status": order.status.value,
            }

        raise ValueError(f"Unknown Alpaca tool: {tool_name}")
