from ib.ext.Contract import Contract
from ib.ext.Order import Order
from ib.opt import Connection, message
from tkinter import *
from tkinter import ttk
import threading
import websocket
import json
from binance import AsyncClient, BinanceSocketManager
import keys
from binance.client import Client
from binance.enums import *
import math
import time

class Application(Frame):
    
    def __init__(self, master):
        """Initialize the Frame"""
        ttk.Frame.__init__(self, master)

        self.grid()
        self.create_widgets()
        self.symbol_id, self.symbol = 0, 'BTCUSDT'
        self.client = None
        self.stoploss_orders = []

    def create_widgets(self):
        """ create the window layout. """

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
        self.listbox1 = Listbox(f1, font=('Lucida Grande', 9), width=7)
        #self.listbox1.bind('<Double-Button-1>', self.OnDoubleClick_listbox)
        self.listbox1.insert(1, 'SOLUSDT')
        self.listbox1.insert(2, 'BTCUSDT')
        self.listbox1.insert(3, 'ETHUSDT')
        self.listbox1.grid(row=0, rowspan=5, column=0, padx=5)

        self.label4 = Label(f1, font=myFont, text="Symbol").grid(row=0, column=1)
        self.label5 = Label(f1, font=myFont, text="Quantity").grid(row=0, column=2)
        self.label6 = Label(f1, font=myFont, text="Limit Price").grid(row=0, column=3)
        self.label7 = Label(f1, font=myFont, text="Market").grid(row=0, column=4)
        self.label8 = Label(f1, font=myFont, text="OrderType").grid(row=2, column =1, sticky=W)
        self.label9 = Label(f1, font=myFont, text="Trailing (%)").grid(row=2, column =2)
        self.labe20 = Label(f1, font=myFont, text="Stop Loss (%)").grid(row=2, column =3)
        self.labe21 = Label(f1, font=myFont, text="TIF").grid(row=2, column =4)

        #create combo box for the Symbol
        self.cbSymbol = ttk.Combobox(f1, font=myFont, width=10, textvariable = varSymbol)
        self.cbSymbol.bind("<Return>", self.cbSymbol_onEnter) #when the enter key is pressed an event happens
        self.cbSymbol.bind('<<ComboboxSelected>>',self.cbSymbol_onEnter)
        self.cbSymbol['values'] = ('SOLUSDT','BTCUSDT','ETHUSDT')
        self.cbSymbol.grid(row=1, column=1, sticky=W)    

        #create spinbox (numericUpDown) for Limit Price
        #self.spinQuantity = Spinbox(f1, font=myFont, increment=100, from_=0, to=10000, width=7, textvariable=varQuantity)
        self.quantity = Entry(f1, font=myFont, width=7, textvariable=varQuantity)
        self.quantity.grid(row=1, column=2)
        #create spinbox (numericUpDown) for Limit Price
        self.spinLimitPrice = Spinbox(f1,font=myFont, format='%10.5f', increment=.01, from_=0.0, to=100000.0, width=10, textvariable=varLimitPrice)
        # when control and up or down arrow are pressed call spenLimitDime()
        #self.spinLimitPrice.bind('<Control-Button-1>', self.spinLimitDime)
        # when Alt and up or down arrow are pressed call spenLimitPenny()
        #self.spinLimitPrice.bind('<Alt-Button-1>', self.spinLimitPenny) 
        self.spinLimitPrice.grid(row=1, column=3)

        #create textbox(Entry box) for the Order Type ****4****
        self.cbOrderType = ttk.Combobox(f1, font=myFont, width=6, textvariable=varOrderType)
        self.cbOrderType['values'] = ('A+T','ACTIV', 'LIMIT','MARKET', 'STP') 
        self.cbOrderType.grid(row=3, column =1,sticky = W)
                
        #create textbox(SpinBox) for the Trailing Stop Callback Rate
        self.spCRate = Spinbox(f1, font=myFont, increment=0.1, from_=0.1, to=5, width=6, textvariable=varCallbackRate).grid(row=3, column=2)
        
        #create textbox(SpinBox) for the StopLoss Rate
        self.spStopLoss = Spinbox(f1, font=myFont, increment=0.01, from_=0.01, to=5, width=6, textvariable=varStopLoss).grid(row=3, column=3)
        """
        #create textbox(Entry box) for the Primary Exchange
        self.tbPrimaryEx = Entry(f1, font=myFont, width=8, textvariable=varPrimaryEx).grid(row=3, column =3,sticky = W)

        #create textbox(Entry box) for the Time in Force
        self.cbTIF = ttk.Combobox(f1, font=myFont, width=7, textvariable=varTIF)
        self.cbTIF['values'] = ('DAY','GTC')
        self.cbTIF.grid(row=3, column =4,sticky = W)
        """
        """
        #create Bid Label
        self.label2 = Label(f1, font=myFont, text="Bid", width=7).grid(row=4, column=2)
        #create Ask Label
        self.label3 = Label(f1, font=myFont, text="Ask", width=7).grid(row=4, column=3)
        
        #create textbox(Entry box) for the Bid price
        self.tbBid = Entry(f1, font=myFont, width=7, textvariable = varBid)
        #self.tbBid.bind("<Button-1>", self.tbBid_Click)
        self.tbBid.grid(row=5, column =2, sticky=E)
        
        #create textbox(Entry box) for the Ask price
        self.tbAsk = Entry(f1, font=myFont, width=7, textvariable = varAsk)
        #self.tbAsk.bind("<Button-1>", self.tbAsk_Click)
        self.tbAsk.grid(row=5, column=3)
        """

        #create a sell button ***
        self.btnSell = Button(f1, font=('Lucida Grande',10,'bold'), text="SHORT", width=9, bg="red", fg="white", command=self.sell)
        self.btnSell.grid(row=5, column=1, sticky=W)

        #create a buy button ***
        self.btnBuy = Button(f1, font=('Lucida Grande',10,'bold'), text="LONG", width=9, bg="green", fg="white", command= self.buy)
        self.btnBuy.grid(row=5, column=4, sticky=E)

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

    def connect_to_binance(self):
        # initialize the client
        self.client = Client(keys.API_KEY, keys.API_SECRET, tld='com')
        self.check_connection()
        
    def disconnect_it(self):
        self.client = None
        self.check_connection()

    def buy(self):
        self.symbol = varSymbol.get()  # gets the symbol string from the symbol combo box
        self.quantity = varQuantity.get()  # gets the share size from the quantity spinbox
        self.order_type = varOrderType.get()  # gets the order type for the order type combobox
        self.limit_price = varLimitPrice.get()  # gets the limit price from the limit price spinbox
        # calls the function place_market order passes variables
        # symbol, quantity, order type, buy or sell represeted by true or false, and limit price
        self.place_order(self.symbol, self.quantity, self.order_type, True, self.limit_price)
    
    def sell(self):
        self.symbol = varSymbol.get()
        self.quantity = varQuantity.get()
        self.order_type = varOrderType.get()
        self.limit_price = varLimitPrice.get()
        self.place_order(self.symbol, self.quantity, self.order_type, False, self.limit_price)

    def cancel_all(self):
        self.client.futures_cancel_all_open_orders(symbol= self.symbol)
        self.stoploss_orders = []
        print("All orders cancelled")

    def cbSymbol_onEnter(self, event):
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
            
    def request_market_data(self, symbol):

        def on_message(ws, message):
            
            json_message = json.loads(message)
            varLast.set(json_message['k']['c']) 
        
        def on_error(ws, error):
            print(error)

        def on_close(close_msg):
            print("### closed ###" + close_msg)

        def streamKline(currency):
            websocket.enableTrace(False)
            socket = f'wss://fstream.binance.com/ws/{currency}@kline_1m'

            self.ws = websocket.WebSocketApp(socket,
                                        on_message=on_message,
                                        on_error=on_error,
                                        on_close=on_close)
        
            self.ws.run_forever()
            return
        streamKline(self.symbol)
    
    def request_ticksize(self, symbol):
        try:
            request = self.client.get_symbol_info(self.symbol)
            self.ticksize = float((request['filters'][0]['tickSize']))
        except:
            self.check_connection()

    def cancel_order(self, symbol, orderId):
        try:
            time.sleep(0.5)
            self.client.futures_cancel_order(symbol=symbol, orderId=orderId)
        except:
            print("Error in cancelling order")

    def cancel_market_data(self):
        try:
            self.ws.close()
        except:
            pass
    
    def place_order(self, symbol, quantity, order_type, is_buy, limit_price):
        tickround = int(math.log10(self.ticksize)*-1)
        if is_buy == True:
            orderSide = 'BUY'
            slSide = 'SELL'
            positionSide= 'LONG'
        else:
            orderSide = 'SELL'
            slSide = 'BUY'
            positionSide= 'SHORT'
        if order_type == 'STP':
            if positionSide == 'LONG':
                stopPrice = round(varLast.get()*(1-varStopLoss.get()/100),tickround)
            else:
                stopPrice = round(varLast.get()*(1+varStopLoss.get()/100),tickround)
            for sl in self.stoploss_orders:
                if symbol == sl['symbol'] and positionSide == sl['positionSide']:
                    #chequear si el stopLoss es mejor
                    threading.Thread(target=self.cancel_order, args=[symbol, sl['orderId']]).start()
                    #self.client.futures_cancel_order(symbol=symbol, orderId=sl['orderId'])
                    self.stoploss_orders.remove(sl)
            sl_order = self.client.futures_create_order(symbol=symbol, side=slSide, positionSide=positionSide, type='STOP_MARKET', stopPrice=stopPrice, closePosition=True)
            self.stoploss_orders.append({'symbol': symbol, 'positionSide': positionSide, 'stopPrice': stopPrice, 'orderId': sl_order.get('orderId')})
            print(self.stoploss_orders)
        elif order_type == 'A+T':
            activ_order = self.client.futures_create_order(symbol=symbol, side=orderSide, positionSide=positionSide, type='STOP_MARKET',  quantity=quantity,stopPrice=limit_price, closePosition=False)
            trailing_order = self.client.futures_create_order(symbol=symbol, side=slSide, positionSide= positionSide, type='TRAILING_STOP_MARKET', quantity=quantity, activationPrice= limit_price, callbackRate=varCallbackRate.get(), timeInForce='GTC')
            """sl_order = self.client.futures_create_order(symbol=symbol, side='SELL', positionSide=positionSide, type='STOP_MARKET', stopPrice='{:.8f}'.format(round(float(limit_price)*0.998,8)), closePosition=True, timeInForce='GTE_GTC')"""
        elif order_type == 'LIMIT':
            limitorder = self.client.futures_create_order(symbol=symbol, side=orderSide, positionSide=positionSide, type=order_type, quantity=quantity,price=limit_price, 
            timeInForce='GTC')
        elif order_type == 'MARKET':
            market_order = self.client.futures_create_order(symbol=symbol, side=orderSide, positionSide=positionSide, type=order_type, quantity=quantity)
        try:
            print(f"{order_type} order placed in {symbol}. Position: {positionSide}, StopPrice: {stopPrice}")
        except:    
            print(f"{order_type} order placed in {symbol}. Position: {positionSide}, Price: {limit_price}")
        
    def focus_to_qty(self):
        self.quantity.focus_set()
        self.quantity.selection_range(0, END)
        self.quantity.icursor(END)

    def focus_to_limit_price(self):
        self.spinLimitPrice.focus_set()
        self.spinLimitPrice.selection_range(0, END)
        self.spinLimitPrice.icursor(END)

    def last_to_limit(self, event=None):
        varLimitPrice.set(varLast.get())
        self.focus_to_limit_price()

"""
    def server_handler(self, msg):
        if msg.typeName == "nextValidId":
            self.order_id = msg.orderId
        elif msg.typeName == "managedAccounts":
            self.account_code = msg.accountsList
        elif msg.typeName == "updatePortfolio" \
                and msg.contract.m_symbol == self.symbol \
                and msg.contract.m_secType == 'STK':  # added this to my code not shown in video ******
            self.unrealized_pnl = msg.unrealizedPNL
            self.realized_pnl = msg.realizedPNL
            self.position = msg.position
            self.average_price = msg.averageCost
        elif msg.typeName == "error" and msg.id != -1:
            return#
            """
"""    
    def error_handler(self, msg):
        if msg.typeName == 'error'and msg.id != -1:
            print ('Server Error:', msg)
    """

root = Tk()
root.title("Conexion a Binance")
root.geometry('600x480')
root.attributes('-topmost', True)
varSymbol = StringVar(root, value='BTCUSDT')
varQuantity = StringVar(root, value='100')
varLimitPrice = StringVar()
varOrderType = StringVar(root, value='A+T')
varCallbackRate = StringVar(root, value='0.1')
varStopLoss = DoubleVar(root, value='0.1')
varLast = DoubleVar()

app = Application(root)

# ShortCuts
root.bind('<F1>', lambda event: varOrderType.set('A+T'))
root.bind('<F2>', lambda event: varOrderType.set('ACTIV'))
root.bind('<F3>', lambda event: varOrderType.set('LIMIT'))
root.bind('<F4>', lambda event: varOrderType.set('MARKET'))
root.bind('<F5>', lambda event: varOrderType.set('STP'))
root.bind('<Control-w>', lambda event: app.focus_to_qty())
root.bind('<Control-e>', lambda event: app.focus_to_limit_price())
root.bind('<Control-r>', lambda event: app.cancel_all())
root.bind('<Control-s>', lambda event: app.sell())
root.bind('<Control-d>', lambda event: app.buy())
root.bind('<Control-q>', lambda event: app.last_to_limit())

root.mainloop()
