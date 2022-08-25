import math
import websocket
import json

class Instrument:
    def __init__(self, symbol):
        self.symbol = symbol
        self.size = 100 # default values
        self.ticksize = 0.01 
        self.tickround = 2
        self.stopLoss_enabled = True
        self.stoploss = 0.1
        self.trailing_enabled = True
        self.callbackRate = 0.2
        self.streamToApp = True
        

    def request_ticksize(self, symbol, client):
        try:            
            request = client.get_symbol_info(symbol)
            self.ticksize = float((request['filters'][0]['tickSize']))
            self.tickround = int(math.log10(self.ticksize)*-1)
            print(f"{symbol}, ticksize: {self.tickround}")
        except:
            print(f"Failed to get {symbol} ticksize. Check Connection.")
