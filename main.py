"""
Autonomous Alpha - Main Orchestrator
Deterministic state machine: Fetch → Analyze → Validate → Execute
Glass Box logging with full transparency.
"""
import argparse
import asyncio
import csv
import time
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

from src.mcp_client import MCPClient
from src.market_observer import MarketObserver
from src.strategy_engine import MeanReversionStrategy
from src.risk_manager import RiskManager
from src.execution_gateway import ExecutionGateway
from src.audit_logger import AuditLogger


class AutonomousAlpha:
    """
    Glass Box Trading Agent with deterministic state machine.

    State Flow: FETCH → ANALYZE → VALIDATE → EXECUTE
    """

    def __init__(self, dry_run: bool = True):
        # Load environment variables
        load_dotenv()

        # Initialize components
        self.mcp_client = MCPClient("config/mcp_config.json")
        self.market_observer = MarketObserver(self.mcp_client)
        self.strategy = MeanReversionStrategy()
        self.risk_manager = RiskManager(self.mcp_client, "config/risk_limits.json")
        self.executor = ExecutionGateway(self.mcp_client, dry_run=dry_run)
        self.auditor = AuditLogger("logs/reasoning_trace.jsonl")

        # Load trading universe
        self.universe = self._load_trading_universe("config/trading_universe.csv")

        self.dry_run = dry_run

    def _load_trading_universe(self, path: str) -> list[str]:
        """Load list of symbols to trade."""
        symbols = []
        with open(Path(path), 'r') as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header if exists
            for row in reader:
                if row:
                    symbols.append(row[0].strip())
        return symbols

    async def process_symbol(self, symbol: str):
        """
        Process one symbol through the full state machine.

        States: FETCH → ANALYZE → VALIDATE → EXECUTE
        """
        print(f"\n{'='*60}")
        print(f"Processing: {symbol}")
        print(f"{'='*60}")

        # STATE 1: FETCH
        start_time = time.time()
        try:
            market_data = await self.market_observer.fetch_market_data(symbol)
            duration_ms = (time.time() - start_time) * 1000

            print(f"\n[FETCH] Retrieved market data for {symbol}")
            print(f"  Price: ${market_data.price}")
            rsi_display = f"{market_data.rsi_14:.2f}" if market_data.rsi_14 else "N/A"
            print(f"  RSI(14): {rsi_display}")

            self.auditor.log_transition(
                state="FETCH",
                inputs={"symbol": symbol},
                outputs={"market_data": market_data},
                rationale=f"Fetched market data for {symbol}: price=${market_data.price}, RSI={market_data.rsi_14}",
                duration_ms=duration_ms,
            )

        except Exception as e:
            print(f"[FETCH] ERROR: {e}")
            self.auditor.log_transition(
                state="FETCH",
                inputs={"symbol": symbol},
                outputs={"error": str(e)},
                rationale=f"Failed to fetch data for {symbol}: {e}",
            )
            return

        # STATE 2: ANALYZE
        start_time = time.time()
        signal = self.strategy.generate_signal(market_data)
        duration_ms = (time.time() - start_time) * 1000

        if signal is None:
            print(f"[ANALYZE] No signal generated (HOLD)")
            self.auditor.log_transition(
                state="ANALYZE",
                inputs={"market_data": market_data},
                outputs={"action": "HOLD"},
                rationale=f"RSI({market_data.rsi_14:.2f}) in neutral zone. No action required.",
                duration_ms=duration_ms,
            )
            return

        print(f"\n[ANALYZE] Signal Generated: {signal.action}")
        print(f"  Action: {signal.action}")
        print(f"  Quantity: {signal.quantity}")
        print(f"  Confidence: {signal.confidence:.2%}")
        print(f"  Rationale: {signal.rationale}")

        self.auditor.log_transition(
            state="ANALYZE",
            inputs={"market_data": market_data},
            outputs={"signal": signal},
            rationale=signal.rationale,
            duration_ms=duration_ms,
        )

        # STATE 3: VALIDATE
        start_time = time.time()
        risk_result = await self.risk_manager.validate_signal(signal, market_data.price)
        duration_ms = (time.time() - start_time) * 1000

        print(f"\n[VALIDATE] Risk Check: {'✓ APPROVED' if risk_result.approved else '✗ REJECTED'}")
        print(f"  Buying Power: ${risk_result.buying_power_available}")
        print(f"  Position Size: {risk_result.position_size_percent:.2%}")

        if risk_result.violations:
            print(f"  Violations:")
            for violation in risk_result.violations:
                print(f"    - {violation}")

        self.auditor.log_transition(
            state="VALIDATE",
            inputs={"signal": signal},
            outputs={"risk_result": risk_result},
            rationale=f"Risk validation {'approved' if risk_result.approved else 'rejected'}: {', '.join(risk_result.violations) if risk_result.violations else 'All checks passed'}",
            duration_ms=duration_ms,
        )

        if not risk_result.approved:
            print(f"[VALIDATE] Trade rejected due to risk violations")
            return

        # STATE 4: EXECUTE
        start_time = time.time()
        order_result = await self.executor.execute_signal(signal, market_data.price)
        duration_ms = (time.time() - start_time) * 1000

        print(f"\n[EXECUTE] Order Status: {order_result.status}")
        if self.dry_run:
            print(f"  🔍 DRY RUN MODE - No real orders placed")
        print(f"  Order ID: {order_result.order_id}")
        print(f"  Symbol: {order_result.symbol}")
        print(f"  Action: {order_result.action}")
        print(f"  Quantity: {order_result.quantity}")
        print(f"  Price: ${order_result.filled_price}")

        self.auditor.log_transition(
            state="EXECUTE",
            inputs={"signal": signal, "dry_run": self.dry_run},
            outputs={"order_result": order_result},
            rationale=f"{'Simulated' if self.dry_run else 'Executed'} {order_result.action} order for {order_result.quantity} shares of {order_result.symbol} at ${order_result.filled_price}",
            duration_ms=duration_ms,
        )

    async def run_cycle(self):
        """Run one complete trading cycle across all symbols."""
        print(f"\n{'#'*60}")
        print(f"Starting Trading Cycle - {datetime.utcnow().isoformat()}")
        print(f"Mode: {'DRY RUN' if self.dry_run else 'LIVE TRADING'}")
        print(f"Universe: {', '.join(self.universe)}")
        print(f"{'#'*60}")

        for symbol in self.universe:
            await self.process_symbol(symbol)

        print(f"\n{'#'*60}")
        print(f"Cycle Complete - Next cycle in 60 seconds")
        print(f"{'#'*60}\n")

    async def run(self):
        """Main event loop - tick every 60 seconds."""
        try:
            while True:
                await self.run_cycle()
                await asyncio.sleep(60)
        except KeyboardInterrupt:
            print("\n\nShutting down Autonomous Alpha...")
            self.auditor.log_transition(
                state="SHUTDOWN",
                inputs={},
                outputs={},
                rationale="System shutdown via keyboard interrupt",
            )


def main():
    """Entry point with CLI argument parsing."""
    parser = argparse.ArgumentParser(
        description="Autonomous Alpha - Glass Box Trading Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Run in dry-run mode (default)
  python main.py --dry-run=False    # Run with live trading (USE WITH CAUTION)
        """
    )

    parser.add_argument(
        '--dry-run',
        type=lambda x: x.lower() != 'false',
        default=True,
        help='Run in dry-run mode (default: True). Set to False for live trading.',
    )

    args = parser.parse_args()

    print("="*60)
    print("  AUTONOMOUS ALPHA - Glass Box Trading Agent")
    print("="*60)
    print(f"Mode: {'DRY RUN (Simulation)' if args.dry_run else 'LIVE TRADING ⚠️'}")
    print(f"Logging: logs/reasoning_trace.jsonl")
    print("="*60)

    if not args.dry_run:
        response = input("\n⚠️  WARNING: Live trading mode enabled. Continue? (yes/no): ")
        if response.lower() != 'yes':
            print("Exiting...")
            return

    agent = AutonomousAlpha(dry_run=args.dry_run)
    asyncio.run(agent.run())


if __name__ == "__main__":
    main()
