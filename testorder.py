from warnings import filters
from binance.client import Client
import keys

client = Client(keys.API_KEY, keys.API_SECRET)

info = client.get_exchange_info()
infoMatic= client.get_symbol_info('MATICUSDT')

print(infoMatic['filters'][0]['tickSize'])