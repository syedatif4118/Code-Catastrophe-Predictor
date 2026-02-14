from alpaca.trading.client import TradingClient

client = TradingClient('PKHVZ4XK4MGAMP3QRCBL3FEYDN', 'EMxY4vS4gzCLsrhA2Wd9r3tsbJNcpn7xj9egZjJG8Gjp', paper=True)
account = client.get_account()
print(f"Buying Power: {account.buying_power}")
print(f"Equity: {account.equity}")