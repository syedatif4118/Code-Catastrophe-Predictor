from dotenv import load_dotenv
import os

load_dotenv()

print("ANTHROPIC_API_KEY:", bool(os.getenv("ANTHROPIC_API_KEY")))
print("ALPACA_API_KEY:", bool(os.getenv("ALPACA_API_KEY")))
print("ALPACA_SECRET_KEY:", bool(os.getenv("ALPACA_SECRET_KEY")))