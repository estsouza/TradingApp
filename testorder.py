from binance.client import Client
import keys

client = Client(keys.API_KEY, keys.API_SECRET)

buylimitorder = client.futures_create_order(symbol='BTCUSDT', side='BUY', type='LIMIT', quantity=0.001, price=20000, timeInForce='GTC')
print(buylimitorder)