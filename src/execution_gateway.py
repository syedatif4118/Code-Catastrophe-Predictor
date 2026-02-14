"""
Autonomous Alpha - Execution Gateway
Places orders via MCP client to Alpaca.
"""
from decimal import Decimal
from typing import Optional

from src.models import TradeSignal, OrderResult, TradingAction
from src.mcp_client import MCPClient


class ExecutionGateway:
    """Execute trades via Alpaca MCP server."""

    def __init__(self, mcp_client: MCPClient, dry_run: bool = True):
        self.mcp_client = mcp_client
        self.dry_run = dry_run

    async def execute_signal(self, signal: TradeSignal, current_price: Decimal) -> OrderResult:
        """
        Execute approved trade signal.

        Args:
            signal: Approved trade signal
            current_price: Current market price

        Returns:
            OrderResult with execution details
        """
        if self.dry_run:
            return self._simulate_order(signal, current_price)

        try:
            # Place market order via Alpaca MCP
            order_response = await self.mcp_client.call_tool(
                "alpaca",
                "place_order",
                {
                    "symbol": signal.symbol,
                    "side": signal.action.value,
                    "qty": signal.quantity,
                }
            )

            return OrderResult(
                order_id=order_response.get("order_id"),
                symbol=signal.symbol,
                action=signal.action,
                quantity=signal.quantity,
                filled_price=current_price,
                status=order_response.get("status", "submitted"),
            )

        except Exception as e:
            return OrderResult(
                order_id=None,
                symbol=signal.symbol,
                action=signal.action,
                quantity=signal.quantity,
                filled_price=None,
                status="failed",
                error=str(e),
            )

    def _simulate_order(self, signal: TradeSignal, current_price: Decimal) -> OrderResult:
        """Simulate order execution for dry-run mode."""
        return OrderResult(
            order_id=f"DRY_RUN_{signal.symbol}_{signal.timestamp.timestamp()}",
            symbol=signal.symbol,
            action=signal.action,
            quantity=signal.quantity,
            filled_price=current_price,
            status="simulated",
        )
