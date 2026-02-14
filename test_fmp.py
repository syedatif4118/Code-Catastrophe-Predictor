"""
Test yfinance (Yahoo Finance) API integration
"""
import asyncio
from dotenv import load_dotenv
from src.mcp_client import MCPClient
from src.market_observer import MarketObserver

async def test_yfinance():
    """Test yfinance API calls."""
    load_dotenv()

    print("=" * 60)
    print("Testing yfinance (Yahoo Finance) Integration")
    print("=" * 60)

    # Initialize MCP client
    mcp_client = MCPClient("config/mcp_config.json")
    market_observer = MarketObserver(mcp_client)

    # Test symbols
    symbols = ["AAPL", "TSLA", "GOOGL"]

    for symbol in symbols:
        print(f"\n{'─' * 60}")
        print(f"Testing: {symbol}")
        print(f"{'─' * 60}")

        try:
            # Test quote endpoint
            quote = await mcp_client.call_tool("yfinance", "get_quote", {"symbol": symbol})
            print(f"✓ Quote retrieved:")
            print(f"  Price: ${quote['price']:.2f}")
            print(f"  Volume: {quote['volume']:,}")
            print(f"  Change: ${quote.get('change', 0):.2f} ({quote.get('changesPercentage', 0):.2f}%)")

            # Test market data with RSI
            market_data = await market_observer.fetch_market_data(symbol)
            print(f"\n✓ Market data with RSI:")
            print(f"  Symbol: {market_data.symbol}")
            print(f"  Price: ${market_data.price}")
            print(f"  Volume: {market_data.volume:,}")
            print(f"  RSI(14): {market_data.rsi_14:.2f}" if market_data.rsi_14 else "  RSI(14): Calculating...")

        except Exception as e:
            print(f"✗ Error: {e}")
            import traceback
            traceback.print_exc()

    print(f"\n{'=' * 60}")
    print("yfinance API Test Complete")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_yfinance())
