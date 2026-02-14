"""
Autonomous Alpha - Risk Manager
Validates trade signals against risk limits and account constraints.
"""
import json
from decimal import Decimal
from pathlib import Path
from typing import Optional

from src.models import TradeSignal, RiskCheckResult, TradingAction
from src.mcp_client import MCPClient


class RiskManager:
    """Validate trades against risk limits."""

    def __init__(self, mcp_client: MCPClient, risk_config_path: str):
        self.mcp_client = mcp_client
        self.risk_config_path = Path(risk_config_path)
        self.limits = self._load_risk_limits()

    def _load_risk_limits(self) -> dict:
        """Load risk limits from config file."""
        with open(self.risk_config_path, 'r') as f:
            return json.load(f)

    async def validate_signal(self, signal: TradeSignal, current_price: Decimal) -> RiskCheckResult:
        """
        Validate trade signal against risk limits.

        Checks:
        1. Trade value <= max_trade_value
        2. Position size <= max_position_percent of equity
        3. Sufficient buying power for BUY orders

        Args:
            signal: Trade signal to validate
            current_price: Current market price

        Returns:
            RiskCheckResult with approval status and violations
        """
        violations = []

        # Get account info
        account = await self.mcp_client.call_tool("alpaca", "get_account", {})
        buying_power = Decimal(str(account["buying_power"]))
        equity = Decimal(str(account["equity"]))

        # Get current position
        position = await self.mcp_client.call_tool(
            "alpaca",
            "get_position",
            {"symbol": signal.symbol}
        )
        current_position_qty = position.get("qty", 0)

        # Calculate trade value
        trade_value = current_price * signal.quantity

        # Check 1: Max trade value
        max_trade_value = Decimal(str(self.limits["max_trade_value"]))
        if trade_value > max_trade_value:
            violations.append(
                f"Trade value ${trade_value:.2f} exceeds limit ${max_trade_value:.2f}"
            )

        # Check 2: Position size limit
        max_position_percent = self.limits["max_position_percent"] / 100

        if signal.action == TradingAction.BUY:
            new_position_value = (current_position_qty + signal.quantity) * current_price
        elif signal.action == TradingAction.SELL:
            new_position_value = max(0, current_position_qty - signal.quantity) * current_price
        else:
            new_position_value = Decimal(0)

        position_percent = float(new_position_value / equity) if equity > 0 else 0

        if position_percent > max_position_percent:
            violations.append(
                f"Position size {position_percent:.2%} exceeds limit {max_position_percent:.2%}"
            )

        # Check 3: Buying power (for BUY orders)
        if signal.action == TradingAction.BUY:
            if trade_value > buying_power:
                violations.append(
                    f"Insufficient buying power: need ${trade_value:.2f}, have ${buying_power:.2f}"
                )

        # Check 4: Position exists for SELL orders
        if signal.action == TradingAction.SELL:
            if current_position_qty < signal.quantity:
                violations.append(
                    f"Insufficient position: trying to sell {signal.quantity}, only have {current_position_qty}"
                )

        approved = len(violations) == 0

        return RiskCheckResult(
            approved=approved,
            signal=signal,
            violations=violations,
            buying_power_available=buying_power,
            position_size_percent=position_percent,
        )
