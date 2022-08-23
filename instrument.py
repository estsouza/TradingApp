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
    
    """
    def request_market_data(self, lastFieldVariable):
        def on_message(ws, message):
            json_message = json.loads(message)
            print(json_message['k']['c'])
            while self.streamToApp:
                lastFieldVariable.set(json_message['k']['c']) 
        
        def on_error(ws, error):
            print(error)

        def on_close(close_msg):
            print("### closed ###" + close_msg)

        def streamKline():
            lower = self.symbol.lower()
            websocket.enableTrace(False)
            socket = f'wss://fstream.binance.com/ws/{lower}@kline_1m'
            self.ws = websocket.WebSocketApp(socket,
                                        on_message=on_message,
                                        on_error=on_error,
                                        on_close=on_close)
        
            self.ws.run_forever()
            return
        print(f"Opening Stream Market Data: {self.symbol}")
        streamKline()"""
        

"""
varSymbol.set(varSymbol.get().upper())
        mytext = varSymbol.get()
        vals = self.cbSymbol.cget('values')
        self.cbSymbol.select_range(0, END)
        if not vals:
            self.cbSymbol.configure(values = (mytext, ))
        elif mytext not in vals: 
            self.cbSymbol.configure(values = vals + (mytext, ))
        mySymbol = varSymbol.get()
        self.symbol = mySymbol.lower()
        self.cancel_market_data()
        #varPosition.set('0')
        #varAvgPrice.set('0.00')
        self.ticksize = 0.01
        threading.Thread(target=self.request_market_data, args=[self.symbol]).start()
        threading.Thread(target=self.request_ticksize, args=[self.symbol]).start()
        # calls method to request account updates
        #self.request_account_updates(self.account_code)

"""