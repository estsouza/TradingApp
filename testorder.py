from binance.client import Client
import websocket
import json
import keys
import requests

client = Client(keys.API_KEY, keys.API_SECRET, tld='com')

positionSide = 'LONG'
stopLoss = 1.036
takeProfit = 1.048
symbol = 'GMTUSDT'
side = 'BUY'
slSide = 'SELL'
lastPrice = 1.03

def get_listen_key_by_REST(binance_api_key):
    url = 'https://fapi.binance.com/fapi/v1/listenKey'
    response = requests.post(url, headers={'X-MBX-APIKEY': binance_api_key}) 
    json = response.json()
    return json['listenKey']

listenKey = get_listen_key_by_REST(keys.API_KEY)

def on_message(ws, message):
    json_message = json.loads(message)
    positionSide = json_message['o']['ps']
    side = json_message['o']['S']
    state = json_message['o']['X']
    if state == 'FILLED' and ((side == 'BUY' and positionSide == 'LONG') or (side == 'SELL' and positionSide == 'SHORT')):
        print(f"side: {side}, positionSide: {positionSide}, state: {state}")
        place_stoploss_order(positionSide)


    #print(json_message)
        
def on_error(ws, error):
    print(error)

def on_close(close_msg):
    print("### closed ###" + close_msg)

def streamUserdata():
    websocket.enableTrace(False)
    socket = f'wss://fstream.binance.com/ws/{listenKey}'
    ws = websocket.WebSocketApp(socket,on_message=on_message,on_error=on_error,on_close=on_close)
        
    ws.run_forever()

def place_stoploss_order(positionSide):
    print("pedido de SL")
    if positionSide == 'LONG':
        stopPrice = 1.015
        slSide = 'SELL'
    else:
        stopPrice = 1.03
        slSide = 'BUY'
    """for sl in self.stoploss_orders:
            if symbol == sl['symbol'] and positionSide == sl['positionSide']:
                #chequear si el stopLoss es mejor
                threading.Thread(target=self.cancel_order, args=[symbol, sl['orderId']]).start()
                self.stoploss_orders.remove(sl)"""
    sl_order = client.futures_create_order(symbol=symbol, side=slSide, positionSide=positionSide, type='STOP_MARKET', stopPrice=stopPrice, closePosition=True)
        #self.stoploss_orders.append({'symbol': symbol, 'positionSide': positionSide, 'stopPrice': stopPrice, 'orderId': sl_order.get('orderId')})
    print(f"StopLoss order placed in {symbol}. Position: {positionSide}, StopPrice: {stopPrice}")

streamUserdata()