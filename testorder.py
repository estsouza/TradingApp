symbol=GMTUSDT, side=BUY, positionSide=LONG, type='STOP_MARKET',  quantity=100,stopPrice=1.09

symbol=GMTUSDT, side=BUY, positionSide=LONG, type='STOP_MARKET',  quantity=100,stopPrice=   1.0420


logged in
symbol=GMTUSDT, side=BUY, positionSide=LONG, type='STOP_MARKET',  quantity=100,limitPrice=   1.089
Exception in Tkinter callback
Traceback (most recent call last):
  File "C:\Users\estso\AppData\Local\Programs\Python\Python310\lib\tkinter\__init__.py", line 1921, in __call__
    return self.func(*args)
  File "c:\Users\estso\Documents\Python Scripts\TradingApp\TradingApp\main.py", line 343, in <lambda>
    root.bind('<Control-d>', lambda event: app.buy())
  File "c:\Users\estso\Documents\Python Scripts\TradingApp\TradingApp\main.py", line 163, in buy
    self.place_order(self.symbol, self.quantity, self.order_type, True, self.limit_price)
  File "c:\Users\estso\Documents\Python Scripts\TradingApp\TradingApp\main.py", line 257, in place_order
    activ_order = self.client.futures_create_order(symbol=symbol, side=orderSide, positionSide=positionSide, type='STOP_MARKET',  quantity=quantity,stopPrice=limit_price)
  File "C:\Users\estso\AppData\Local\Programs\Python\Python310\lib\site-packages\binance\client.py", line 5985, in futures_create_order
    return self._request_futures_api('post', 'order', True, data=params)
  File "C:\Users\estso\AppData\Local\Programs\Python\Python310\lib\site-packages\binance\client.py", line 339, in _request_futures_api
    return self._request(method, uri, signed, True, **kwargs)
  File "C:\Users\estso\AppData\Local\Programs\Python\Python310\lib\site-packages\binance\client.py", line 315, in _request
    return self._handle_response(self.response)
  File "C:\Users\estso\AppData\Local\Programs\Python\Python310\lib\site-packages\binance\client.py", line 324, in _handle_response
    raise BinanceAPIException(response, response.status_code, response.text)
binance.exceptions.BinanceAPIException: APIError(code=-1022): Signature for this request is not valid.
symbol=GMTUSDT, side=BUY, positionSide=LONG, type='STOP_MARKET',  quantity=100,limitPrice=.089
Exception in Tkinter callback
Traceback (most recent call last):
  File "C:\Users\estso\AppData\Local\Programs\Python\Python310\lib\tkinter\__init__.py", line 1921, in __call__
    return self.func(*args)
  File "c:\Users\estso\Documents\Python Scripts\TradingApp\TradingApp\main.py", line 343, in <lambda>
    root.bind('<Control-d>', lambda event: app.buy())
  File "c:\Users\estso\Documents\Python Scripts\TradingApp\TradingApp\main.py", line 163, in buy
    self.place_order(self.symbol, self.quantity, self.order_type, True, self.limit_price)
  File "c:\Users\estso\Documents\Python Scripts\TradingApp\TradingApp\main.py", line 257, in place_order
    activ_order = self.client.futures_create_order(symbol=symbol, side=orderSide, positionSide=positionSide, type='STOP_MARKET',  quantity=quantity,stopPrice=limit_price)
  File "C:\Users\estso\AppData\Local\Programs\Python\Python310\lib\site-packages\binance\client.py", line 5985, in futures_create_order
    return self._request_futures_api('post', 'order', True, data=params)
  File "C:\Users\estso\AppData\Local\Programs\Python\Python310\lib\site-packages\binance\client.py", line 339, in _request_futures_api
    return self._request(method, uri, signed, True, **kwargs)
  File "C:\Users\estso\AppData\Local\Programs\Python\Python310\lib\site-packages\binance\client.py", line 315, in _request
    return self._handle_response(self.response)
  File "C:\Users\estso\AppData\Local\Programs\Python\Python310\lib\site-packages\binance\client.py", line 324, in _handle_response
    raise BinanceAPIException(response, response.status_code, response.text)
binance.exceptions.BinanceAPIException: APIError(code=-1102): Mandatory parameter 'stopPrice' was not sent, was empty/null, or malformed.
symbol=GMTUSDT, side=BUY, positionSide=LONG, type='STOP_MARKET',  quantity=100,limitPrice=1089
StopLoss order placed in GMTUSDT. Position: LONG, Price: 1089
symbol=GMTUSDT, side=BUY, positionSide=LONG, type='STOP_MARKET',  quantity=100,limitPrice=1.89
StopLoss order placed in GMTUSDT. Position: LONG, Price: 1.89
symbol=GMTUSDT, side=BUY, positionSide=LONG, type='STOP_MARKET',  quantity=100,limitPrice=1.09
StopLoss order placed in GMTUSDT. Position: LONG, Price: 1.09