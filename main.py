from ast import If
from http import client
import tkinter
from ib.ext.Contract import Contract
from ib.ext.Order import Order
from ib.opt import Connection, message
from tkinter import *
from tkinter import ttk
import threading
import websocket
import json
import requests
from binance import AsyncClient, BinanceSocketManager
import keys
import instrument
from binance.client import Client
from binance.enums import *
import math
import time
import pickle
import functions

class Application(Frame):
    
    def __init__(self, master):
        """Initialize the Frame"""
        ttk.Frame.__init__(self, master)
        self.grid()
        # import instruments dictionary
        try:
            with open('instruments.pkl', 'rb') as f:
                self.instruments = pickle.load(f)
        except:
            self.instruments = {}
        self.create_widgets()
        self.symbol = ''
        self.client = None
        self.stoploss_orders = []
        self.websockets = {}
        self.rp = 0
        self.com = 0
        
    def create_widgets(self):
        myFont = ('Lucida Grande', 12)
        #create connect button widget
        self.btnConnect = ttk.Button(self, text='Connect', command=self.connect_to_binance)
        self.btnConnect.grid(row=0, column=0)
        self.btnDisconnect = ttk.Button(self, text='Disconnect', command=self.disconnect_it).grid(row=0, column=1, sticky=W)

        #notebook
        n = ttk.Notebook(root, width=550, height=350)
        f1 = ttk.Frame(n) #first page, which would get widgets gridded into it
        f2 = ttk.Frame(n) # second page
        n.add(f1, text='One')
        n.add(f2, text='Two')
        n.grid(row=3, column=0, padx=5, pady=5, sticky=W)
        
        #create listbox
        self.listbox = Listbox(f1, font=('Lucida Grande', 12), width=10, selectmode='browse', exportselection=False, height=8)
        for i in self.instruments.keys():
            self.listbox.insert(END, i)
        #self.listbox1.bind('<Double-Button-1>', self.OnDoubleClick_listbox)
        self.listbox.bind('<<ListboxSelect>>', self.listbox_onSelect)
        self.listbox.grid(row=0, rowspan=5, column=0, padx=5)

        self.enNewItem = Entry(f1, font=myFont, width=10)
        self.enNewItem.bind('<Return>', self.add_to_list)
        self.enNewItem.grid(row=6, column=0, padx=5)
        self.btnAddItem = Button(f1, text="Add Symbol", command=self.add_to_list)
        self.btnAddItem.grid(row=7, column=0, pady=2)
        self.btnRemoveItem = Button(f1, text="Remove Symbol", command=self.remove_from_list)
        self.btnRemoveItem.grid(row=8, column=0, pady=2)
        self.btnSaveSymbol = Button(f1, text="Save Symbol", command=self.save_symbol)
        self.btnSaveSymbol.grid(row=9, column=0, pady=2)

        self.label4 = Label(f1, font=myFont, text="Symbol").grid(row=0, column=1)
        self.label5 = Label(f1, font=myFont, text="Quantity").grid(row=0, column=2)
        self.label6 = Label(f1, font=myFont, text="Limit Price").grid(row=0, column=3)
        self.label7 = Label(f1, font=myFont, text="Order Type").grid(row=0, column=4)
        self.label8 = Label(f1, font=myFont, text="Ticksize").grid(row=2, column =1)
        self.label9 = Label(f1, font=myFont, text="Trailing (%)").grid(row=2, column =3)
        self.labe21 = Label(f1, font=myFont, text="Stop Loss (%)").grid(row=2, column =4)

        #create combo box for the Symbol
        self.cbSymbol = ttk.Entry(f1, font=myFont, width=10, textvariable = varSymbol)
        #self.cbSymbol.bind("<Return>", self.cbSymbol_onEnter) #when the enter key is pressed an event happens
        #self.cbSymbol.bind('<<ComboboxSelected>>',self.cbSymbol_onEnter)
        #self.cbSymbol['values'] = ('SOLUSDT','BTCUSDT','ETHUSDT')
        self.cbSymbol.grid(row=1, column=1, sticky=W)    

        #create spinbox (numericUpDown) for Limit Price
        #self.spinQuantity = Spinbox(f1, font=myFont, increment=100, from_=0, to=10000, width=7, textvariable=varQuantity)
        self.entQuantity = Entry(f1, font=myFont, width=7, textvariable=varQuantity)
        self.entQuantity.grid(row=1, column=2)
        #create spinbox (numericUpDown) for Limit Price
        #self.spinLimitPrice = Spinbox(f1,font=myFont, format='%8.5f', increment=.01, from_=0.0, to=100000.0, width=10, textvariable=varLimitPrice)
        self.spinLimitPrice = Spinbox(f1,font=myFont, increment=0.01, from_=0.0, to=100000.0, width=10, textvariable=varLimitPrice)
        # when control and up or down arrow are pressed call spenLimitDime()
        #self.spinLimitPrice.bind('<Control-Button-1>', self.spinLimitDime)
        # when Alt and up or down arrow are pressed call spenLimitPenny()
        #self.spinLimitPrice.bind('<Alt-Button-1>', self.spinLimitPenny) 
        self.spinLimitPrice.grid(row=1, column=3)

        #create textbox(Entry box) for the Order Type ****4****
        self.cbOrderType = ttk.Combobox(f1, font=myFont, width=6, textvariable=varOrderType)
        self.cbOrderType['values'] = ('ACTIV', 'LIMIT','MARKET', 'STP') 
        self.cbOrderType.grid(row=1, column =4)

        self.spTicksize = Spinbox(f1,font=myFont, increment=1, from_=-1, to=10, width=7, textvariable=varTicksize)
        self.spTicksize.grid(row=3, column=1)
                
        #create textbox(SpinBox) for the Trailing Stop Callback Rate
        self.trailing_enabled = tkinter.BooleanVar(self)
        self.chboxTrailingStop = ttk.Checkbutton(f1, text="Trailing Stop", variable=self.trailing_enabled)
        self.trailing_enabled.set(True)
        self.chboxTrailingStop.grid(row=2, column=2)
        self.spCRate = Spinbox(f1, font=myFont, increment=0.1, from_=0.1, to=5, width=6, textvariable=varCallbackRate).grid(row=3, column=3)
        
        #create textbox(SpinBox) for the StopLoss Rate
        self.stopLoss_enabled = tkinter.BooleanVar(self)
        self.chboxStopLoss = ttk.Checkbutton(f1, text="Stop Loss", variable=self.stopLoss_enabled)
        self.stopLoss_enabled.set(True)
        self.chboxStopLoss.grid(row=3, column=2)
        self.spStopLoss = Spinbox(f1, font=myFont, increment=0.01, from_=0.01, to=5, width=6, textvariable=varStopLoss)
        self.spStopLoss.grid(row=3, column=4)
        
        self.btnSell = Button(f1, font=('Lucida Grande',10,'bold'), text="SHORT", width=9, bg="red", fg="white", command=self.sell)
        self.btnSell.grid(row=5, column=3)
        self.btnBuy = Button(f1, font=('Lucida Grande',10,'bold'), text="LONG", width=9, bg="green", fg="white", command= self.buy)
        self.btnBuy.grid(row=5, column=4)
        self.btnSLShort = Button(f1, font=('Lucida Grande',10,'bold'), text="MOVE SL", width=9, bg="red", fg="white", command=lambda: self.place_stoploss_order(positionSide='SHORT'))
        self.btnSLShort.grid(row=6, column=3, pady= 5)
        self.btnSLLong = Button(f1, font=('Lucida Grande',10,'bold'), text="MOVE SL", width=9, bg="green", fg="white", command=lambda: self.place_stoploss_order(positionSide='LONG'))
        self.btnSLLong.grid(row=6, column=4)

        #create Label
        self.label1 = Label(f1, font=myFont, width=8, text="Last").grid(row=6, column =1)
        #create textbox(Entry box) for the last price 
        self.tbLast = Entry(f1, font=myFont, width=10, textvariable = varLast)
        self.tbLast.grid(row=6, column =2,sticky = W)
        self.tbLast.bind("<Button-1>", self.last_to_limit)

        # create button for Cancell All
        self.btnCancelAll = Button(f1, font= ('Lucida Grande', 10), text= 'Cancel All',
                                width=8, bg="grey", fg="white", command=self.cancel_all)
        self.btnCancelAll.grid(row=7, column=2)

    def check_connection(self):
        try:
            res = self.client.get_server_time()
            if "serverTime" in res.keys():
                print("logged in")
        except:
            print("logged out")
    
    def get_listenKey(self, binance_api_key):
        url = 'https://fapi.binance.com/fapi/v1/listenKey'
        response = requests.post(url, headers={'X-MBX-APIKEY': binance_api_key}) 
        try:
            json = response.json()
            self.ping = True
            print('listenKey obtained')
            return json['listenKey']
        except:
            print('Error in getting listenKey')

    def keepalive_user_data(self, binance_api_key):
        url = 'https://fapi.binance.com/fapi/v1/listenKey'
        time.sleep(1800)
        while self.ping:
            ping = requests.put(url, headers={'X-MBX-APIKEY': binance_api_key}) 
            print("ping sent")
            time.sleep(1800)
        
    def connect_to_binance(self):
        # initialize the client
        self.client = Client(keys.API_KEY, keys.API_SECRET, tld='com')
        self.check_connection()
        self.listenKey = self.get_listenKey(keys.API_KEY)
        for i in self.instruments.keys():
                threading.Thread(target=self.request_market_data, args=[i]).start()
        threading.Thread(target=self.request_user_data, args=[self.listenKey]).start()
        threading.Thread(target=self.keepalive_user_data, args=[keys.API_KEY]).start()
        
    def disconnect_it(self):
        self.client = None
        self.check_connection()

    def request_user_data(self, listenKey):
        def on_message(ws, message):
            json_message = json.loads(message)
            symbol = json_message['o']['s']
            positionSide = json_message['o']['ps']
            side = json_message['o']['S']
            state = json_message['o']['X']
            ex_type = json_message['o']['x']

            if state == 'FILLED' and ((side == 'BUY' and positionSide == 'LONG') or (side == 'SELL' and positionSide == 'SHORT')):
                print(f"--- TRADE OPENED in {symbol}---")
                if self.instruments[symbol].stopLoss_enabled:
                    self.place_stoploss_order(positionSide=positionSide, symbol=symbol)
            
            elif ((side == 'BUY' and positionSide == 'SHORT') or (side == 'SELL' and positionSide == 'LONG')) and ex_type == 'TRADE':
                rp = float(json_message['o']['rp'])
                com = float(json_message['o']['n'])
                comc = json_message['o']['N']
                if state == 'PARTIALLY_FILLED':
                    self.com += com
                    self.rp += rp
                elif state == 'FILLED':
                    
                    self.com += com
                    self.rp += rp
                    print(f"--- TRADE CLOSED in {symbol}---")
                    print(f"PnL: {round(self.rp,2)}. Fees: {round((self.com * 2), 2)} {comc}")
                    threading.Thread(target=self.get_orders_to_cancel, args=[positionSide, symbol]).start()
                    self.rp = 0
                    self.com = 0
                               
        def on_error(ws, error):
            print(error)

        def on_close(close_msg):
            print("### closed ###" + close_msg)

        def streamUserdata(listenKey):
            websocket.enableTrace(False)
            socket = f'wss://fstream.binance.com/ws/{listenKey}'
            ws_userData = websocket.WebSocketApp(socket,on_message=on_message,on_error=on_error,on_close=on_close)
            print(f"UserData Stream opened")    
            ws_userData.run_forever()
            return
        streamUserdata(self.listenKey)

    def cancel_all(self):
        self.client.futures_cancel_all_open_orders(symbol= self.symbol)
        self.stoploss_orders = []
        print("All orders cancelled")

    def get_orders_to_cancel(self, positionSide, symbol):
        print("Getting hanging orders")
        orders = self.client.futures_get_open_orders(symbol=symbol)
        
        for order in orders:
            if order['symbol'] == symbol and order['positionSide'] == positionSide and order['status'] == 'NEW' and order['reduceOnly'] == True:
                if order['type'] == 'TRAILING_STOP_MARKET':
                    if (order['positionSide'] == 'LONG' and float(order['activatePrice']) < float(varLast.get())*1.002) or (order['positionSide'] == 'SHORT' and float(order['activatePrice']) > float(varLast.get())*0.998): 
                        print(f"Cancelling {order['type']} order, positionSide: {order['positionSide']}, symbol: {order['symbol']}, orderId: {order['orderId']}.")
                        threading.Thread(target=self.cancel_order, args=[order['symbol'], order['orderId']]).start()
                elif order['type'] != 'TRAILING_STOP_MARKET':
                    print(f"Cancelling {order['type']} order, positionSide: {order['positionSide']}, symbol: {order['symbol']}, orderId: {order['orderId']}.")
                    threading.Thread(target=self.cancel_order, args=[order['symbol'], order['orderId']]).start()

    def cancel_order(self, symbol, orderId):
        try:
            time.sleep(0.5)
            self.client.futures_cancel_order(symbol=symbol, orderId=orderId)
        except:
            print("Error in cancelling order")

    def add_to_list(self, event=None):
        symbol = self.enNewItem.get().upper()
        if symbol == "":
            print("Insert symbol name")
            pass
        else:
            self.listbox.insert(END, symbol)
            self.enNewItem.delete(0, END)
            index = self.listbox.size()
            self.create_instrument(symbol=symbol)
            self.select_symbol(index=index-1)

    def create_instrument(self, symbol):
        ticker = instrument.Instrument(symbol=symbol)
        self.instruments[symbol]=ticker
        ticker.request_ticksize(symbol=symbol, client=self.client)
        threading.Thread(target=self.request_market_data, args=[symbol]).start()
        print(f"Instrumento {symbol} creado")
        
    def remove_from_list(self):
        symbol = self.listbox.get(self.listbox.curselection()[0])
        del self.instruments[symbol]
        self.cancel_market_data(symbol=symbol)
        self.listbox.delete(self.listbox.curselection())
        self.select_symbol(0)
        print(self.instruments)

    def save_symbol(self):
        symbol = self.listbox.get(self.listbox.curselection()[0])
        self.instruments[symbol].size = varQuantity.get()
        self.instruments[symbol].stopLoss_enabled = self.stopLoss_enabled.get()
        self.instruments[symbol].stoploss = varStopLoss.get()
        self.instruments[symbol].trailing_enabled = self.trailing_enabled.get()
        self.instruments[symbol].callbackRate = varCallbackRate.get()
        self.instruments[symbol].tickround = varTicksize.get()
        self.save_instruments_dictionary()

    def save_instruments_dictionary(self):
        with open('instruments.pkl', 'wb') as f:
            pickle.dump(self.instruments, f)
        print("Instruments Saved")

    def select_symbol(self, index):
        self.listbox.selection_clear(0, END)
        self.listbox.selection_set(index)
        self.listbox.event_generate("<<ListboxSelect>>")

    def listbox_onSelect(self, event):
        index = int(self.listbox.curselection()[0])
        symbol = self.listbox.get(index)
        try:
            varLast.set(self.websockets[symbol]['last'])
            varSymbol.set(symbol)
            varQuantity.set(self.instruments[symbol].size)
            self.last_to_limit()
            varTicksize.set(self.instruments[symbol].tickround)
            varStopLoss.set(self.instruments[symbol].stoploss)
            self.stopLoss_enabled.set(self.instruments[symbol].stopLoss_enabled)
            varCallbackRate.set(self.instruments[symbol].callbackRate)
            self.trailing_enabled.set(self.instruments[symbol].trailing_enabled)
            self.spinLimitPrice['increment'] = self.instruments[symbol].ticksize
        except:
            print("Failed to retrieve symbol data")
            
    def request_market_data(self, symbol):
        lower = symbol.lower()
        def on_message(ws, message):
            json_message = json.loads(message)
            last = json_message['k']['c']
            if varSymbol.get() == symbol:
                varLast.set(last)
            else:
                self.websockets[symbol]['last'] = last
        
        def on_error(ws, error):
            print(error)

        def on_close(close_msg):
            print("### closed ###" + close_msg)

        def streamKline(lower):
            websocket.enableTrace(False)
            socket = f'wss://fstream.binance.com/ws/{lower}@kline_1m'
            self.websockets[symbol] = {}
            self.websockets[symbol]['ws'] = websocket.WebSocketApp(socket,
                                        on_message=on_message,
                                        on_error=on_error,
                                        on_close=on_close)
        
            self.websockets[symbol]['ws'].run_forever()
            return
        print(f"Opening Stream Market Data: {symbol}")
        streamKline(lower)
        
    def cancel_market_data(self, symbol):
        try:
            self.websockets[symbol]['ws'].close()
            print("websocket closed")
        except:
            pass

    def buy(self):
        self.symbol = varSymbol.get()  # gets the symbol string from the symbol combo box
        self.quantity = float(varQuantity.get())  # gets the share size from the quantity spinbox
        self.order_type = varOrderType.get()  # gets the order type for the order type combobox
        self.limit_price = float(varLimitPrice.get())  # gets the limit price from the limit price spinbox
        self.place_order(self.symbol, self.quantity, self.order_type, True, self.limit_price)
    
    def sell(self):
        self.symbol = varSymbol.get()
        self.quantity = float(varQuantity.get())
        self.order_type = varOrderType.get()
        self.limit_price = float(varLimitPrice.get())
        self.place_order(self.symbol, self.quantity, self.order_type, False, self.limit_price)
    
    def place_order(self, symbol, quantity, order_type, is_buy, limit_price):
        if is_buy == True:
            orderSide = 'BUY'
            slSide = 'SELL'
            positionSide= 'LONG'
        else:
            orderSide = 'SELL'
            slSide = 'BUY'
            positionSide= 'SHORT'
        if order_type == 'STP':
            self.place_stoploss_order(positionSide=positionSide)
        elif order_type == 'ACTIV':
            activ_order = self.client.futures_create_order(symbol=symbol, side=orderSide, positionSide=positionSide, type='STOP_MARKET',  quantity=quantity,stopPrice=limit_price)
        elif order_type == 'LIMIT':
            limitorder = self.client.futures_create_order(symbol=symbol, side=orderSide, positionSide=positionSide, type=order_type, quantity=quantity,price=limit_price, 
            timeInForce='GTC')
        elif order_type == 'MARKET':
            market_order = self.client.futures_create_order(symbol=symbol, side=orderSide, positionSide=positionSide, type=order_type, quantity=quantity)
            limit_price = varLast.get()
        print(f"{order_type} order placed in {symbol}. Position: {positionSide}, Price: {limit_price}")
        if self.trailing_enabled.get():
            trailing_order = self.client.futures_create_order(symbol=symbol, side=slSide, positionSide= positionSide, type='TRAILING_STOP_MARKET', quantity=quantity, activationPrice= limit_price, callbackRate=varCallbackRate.get(), timeInForce='GTC')
            print("Trailing order placed")     
                
    def place_stoploss_order(self, positionSide, symbol=""):
        if symbol == "":
            symbol = varSymbol.get()
        """if varTicksize.get() > -1:
            self.tickround = varTicksize.get()"""
        tickround = self.instruments[symbol].tickround
        if symbol == varSymbol.get():
            stoplossRate = varStopLoss.get() # get stoploss rate from spinbox in case it was changed and NOT saved to instrument object
        else:
            stoplossRate = self.instruments[symbol].stoploss
        if positionSide == 'LONG':
            stopPrice = round(varLast.get()*(1-stoplossRate/100),tickround)
            slSide = 'SELL'
        else:
            stopPrice = round(varLast.get()*(1+stoplossRate/100),tickround)
            slSide = 'BUY'
        for sl in self.stoploss_orders:
            if symbol == sl['symbol'] and positionSide == sl['positionSide']:
                #chequear si el stopLoss es mejor
                threading.Thread(target=self.cancel_order, args=[symbol, sl['orderId']]).start()
                self.stoploss_orders.remove(sl)
        sl_order = self.client.futures_create_order(symbol=symbol, side=slSide, positionSide=positionSide, type='STOP_MARKET', stopPrice=stopPrice, closePosition=True)
        self.stoploss_orders.append({'symbol': symbol, 'positionSide': positionSide, 'stopPrice': stopPrice, 'orderId': sl_order.get('orderId')})
        print(f"StopLoss order placed in {symbol}. Position: {positionSide}, StopPrice: {stopPrice}")

    def focus_to_qty(self):
        self.entQuantity.focus_set()
        self.entQuantity.selection_range(0, END)
        self.entQuantity.icursor(END)

    def focus_to_limit_price(self):
        self.spinLimitPrice.focus_set()
        self.spinLimitPrice.selection_range(0, END)
        self.spinLimitPrice.icursor(END)

    def focus_to_stoploss(self):
        self.spStopLoss.focus_set()
        self.spStopLoss.icursor(END)

    def last_to_limit(self, event=None):
        varLimitPrice.set(varLast.get())
        self.focus_to_limit_price()

    
root = Tk()
root.title("Conexion a Binance")
root.geometry('600x480')
root.attributes('-topmost', True)
varSymbol = StringVar()
varQuantity = StringVar(root, value='100')
varLimitPrice = DoubleVar(root, value='1')
varOrderType = StringVar(root, value='ACTIV')
varTicksize = IntVar(root, value='0')
varCallbackRate = StringVar(root, value='0.2')
varStopLoss = DoubleVar(root, value='0.1')
varLast = DoubleVar()

app = Application(root)
app.select_symbol(0)

# ShortCuts
root.bind('<F1>', lambda event: varOrderType.set('ACTIV'))
root.bind('<F2>', lambda event: varOrderType.set('LIMIT'))
root.bind('<F3>', lambda event: varOrderType.set('MARKET'))
root.bind('<F4>', lambda event: varOrderType.set('STP'))
root.bind('<F5>', lambda event: app.select_symbol(0))
root.bind('<F6>', lambda event: app.select_symbol(1))
root.bind('<F7>', lambda event: app.select_symbol(2))
root.bind('<F8>', lambda event: app.select_symbol(3))
root.bind('<Control-q>', lambda event: app.focus_to_qty())
root.bind('<Control-w>', lambda event: app.last_to_limit())
root.bind('<Control-e>', lambda event: app.focus_to_limit_price())
root.bind('<Control-f>', lambda event: app.focus_to_stoploss())
root.bind('<Control-r>', lambda event: app.cancel_all())
root.bind('<Control-a>', lambda event: functions.get_slippage(client=app.client, symbol=varSymbol.get(), size=int(varQuantity.get())))
root.bind('<Home>', lambda event: app.sell())
root.bind('<Prior>', lambda event: app.buy()) # PageUp
root.bind('<End>', lambda event: app.place_stoploss_order(positionSide='SHORT'))
root.bind('<Next>', lambda event: app.place_stoploss_order(positionSide='LONG')) # PageDown

root.mainloop()
