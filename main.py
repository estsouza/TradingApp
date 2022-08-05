from ib.ext.Contract import Contract
from ib.ext.Order import Order
from ib.opt import Connection, message
from tkinter import *
from tkinter import ttk
import time
import keys
from binance.client import Client
from binance.enums import *



class Application(Frame):

    def __init__(self, master):
        """Initialize the Frame"""
        ttk.Frame.__init__(self, master)

        self.port=7496
        self.grid()
        self.create_widgets()
        self.account_code = None
        self.symbol_id, self.symbol = 0, 'AAPL'

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
        self.listbox1.insert(1, 'NFLX')
        self.listbox1.insert(2, 'AAPL')
        self.listbox1.insert(3, 'FB')
        self.listbox1.grid(row=0, rowspan=5, column=0, padx=5)


        #create Label Symbol
        self.label4 = Label(f1, font=myFont, text="Symbol").grid(row=0, column=1)

        #create Label Quantity
        self.label5 = Label(f1, font=myFont, text="Quantity").grid(row=0, column=2)

        #create Label Limit Price
        self.label6 = Label(f1, font=myFont, text="Limit Price").grid(row=0, column=3)

        #create Limit Market
        self.label7 = Label(f1, font=myFont, text="Market").grid(row=0, column=4)

        #create combo box for the Symbol
        self.cbSymbol = ttk.Combobox(f1, font=myFont, width=6, textvariable = varSymbol)
        self.cbSymbol.bind("<Return>", self.cbSymbol_onEnter) #when the enter key is pressed an event happens
        self.cbSymbol.bind('<<ComboboxSelected>>',self.cbSymbol_onEnter)
        self.cbSymbol['values'] = ('AAPL','FB','NFLX')
        self.cbSymbol.grid(row=1, column=1, sticky=W)    

        #create spinbox (numericUpDown) for Limit Price
        self.spinQuantity = Spinbox(f1, font=myFont, increment=100, from_=0, to=10000, width=7, textvariable=varQuantity).grid(row=1, column=2)

        #create spinbox (numericUpDown) for Limit Price
        self.spinLimitPrice = Spinbox(f1,font=myFont, format='%8.2f', increment=.01, from_=0.0, to=1000.0, width=7, textvariable=varLimitPrice)
        # when control and up or down arrow are pressed call spenLimitDime()
        #self.spinLimitPrice.bind('<Control-Button-1>', self.spinLimitDime)
        # when Alt and up or down arrow are pressed call spenLimitPenny()
        #self.spinLimitPrice.bind('<Alt-Button-1>', self.spinLimitPenny) 
        self.spinLimitPrice.grid(row=1, column=3)
                                       
        #create textbox(Entry box) for the Market
        self.cbMarket = ttk.Combobox(f1, font=myFont, width=7, textvariable=varMarket).grid(row=1, column=4, sticky = W)

        #create Label OrderType ********-3-****
        self.label8 = Label(f1, font=myFont, text="OrderType").grid(row=2, column =1, sticky=W)

        #create Label Visible 
        self.label9 = Label(f1, font=myFont, text="Visible").grid(row=2, column =2)

        #create Label Primary Exchange
        self.labe20 = Label(f1, font=myFont, text="Primary Ex.").grid(row=2, column =3)

        #create Label Time in Force
        self.labe21 = Label(f1, font=myFont, text="TIF").grid(row=2, column =4)

        #create textbox(Entry box) for the Order Type ****4****
        self.cbOrderType = ttk.Combobox(f1, font=myFont, width=6, textvariable=varOrderType)
        self.cbOrderType['values'] = ('LMT','MKT','STP', 'STP LMT', 'TRAIL', 'MOC','LOC')
        self.cbOrderType.grid(row=3, column =1,sticky = W)

        #create textbox(Entry box) for the Primary Exchange
        self.tbPrimaryEx = Entry(f1, font=myFont, width=8, textvariable=varPrimaryEx).grid(row=3, column =3,sticky = W)

        #create textbox(Entry box) for the Time in Force
        self.cbTIF = ttk.Combobox(f1, font=myFont, width=7, textvariable=varTIF)
        self.cbTIF['values'] = ('DAY','GTC')
        self.cbTIF.grid(row=3, column =4,sticky = W)

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

        #create a sell button ***
        self.btnSell = Button(f1, font=('Lucida Grande',10,'bold'), text="SELL", width=9, bg="red", fg="white")
        self.btnSell.grid(row=5, column=1, sticky=W)

        #create a buy button ***
        self.btnBuy = Button(f1, font=('Lucida Grande',10,'bold'), text="BUY", width=9, bg="green", fg="white")
        self.btnBuy.grid(row=5, column=4, sticky=E)

        #create Label
        self.label1 = Label(f1, font=myFont, width=8, text="Last").grid(row=6, column =1)

        #create textbox(Entry box) for the last price 
        self.tbLast = Entry(f1, font=myFont, width=8, textvariable = varLast).grid(row=6, column =2,sticky = W)



    def check_connection(self):
        try:
            res = self.client.get_server_time()
            if "serverTime" in res.keys():
                varAsk.set('1')
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
        

    def cbSymbol_onEnter(self, event):
        # cancels Account updates
        self.tws_conn.reqAccountUpdates(False, self.account_code)
        # changes characters to upper case
        varSymbol.set(varSymbol.get().upper())
        # gets the value of the text from the combobox. cbSymbol
        # and adds it to the variable mytext
        mytext = varSymbol.get()
        # gets list of values from dropdwn list of
        # cbSymbol combobox
        vals = self.cbSymbol.cget('values')
        # selects all in the combobox. cbSymbol
        self.cbSymbol.select_range(0, END)
        # checks if symbol exists in the combobox if not it adds it
        # to the dropdown list
        if not vals:
            self.cbSymbol.configure(values = (mytext, ))
        elif mytext not in vals: 
            self.cbSymbol.configure(values = vals + (mytext, ))
        mySymbol = varSymbol.get()
        self.symbol = mySymbol
       
        # calls the cancel_market_data() method   
        self.cancel_market_data()
        # sets the text boxes for position and average price to zero
        #varPosition.set('0')
        #varAvgPrice.set('0.00')
        # calls the method to request streaming data
        self.request_market_data(self.symbol_id, self.symbol)
        # calls method to request account updates
        self.request_account_updates(self.account_code)
        # sets bid and ask price to zero
        varBid.set('0.00')
        varAsk.set('0.00')    
    
    def request_account_updates(self, account_code):  
        self.tws_conn.reqAccountUpdates(True, self.account_code)
    def cancel_market_data(self):
        self.tws_conn.cancelMktData(self.symbol_id)
    
    def request_market_data(self, symbol_id, symbol): 
        contract = self.create_contract(symbol,
                                        'STK',
                                        'SMART',
                                        'NASDAQ',
                                        'USD')
        self.tws_conn.reqMktData(symbol_id, contract, '', False)
        #time.sleep(1)
 
    def tick_event(self, msg):
        if msg.tickerId == 0: # added this to the code not shown in video ********* 
            if msg.field == 1: # 1 is for the bid price
                self.bid_price = msg.price
            elif msg.field == 2:  # 2 is for the ask price
                self.ask_price = msg.price
            elif msg.field == 4:  # 4 represents the last price
                self.last_prices = msg.price
                self.monitor_position(msg)

    def create_contract(self, symbol, sec_type, exch, prim_exch, curr):#*
        contract = Contract()
        contract.m_symbol = symbol
        contract.m_secType = sec_type
        contract.m_exchange = exch
        contract.m_primaryExch = prim_exch
        contract.m_currency = curr
        return contract

    def register_callback_functions(self):
        # Assign server messages handling function.
        self.tws_conn.registerAll(self.server_handler)

        # Assign error handling function.
        self.tws_conn.register(self.error_handler, 'Error')

        # Register market data events.
        self.tws_conn.register(self.tick_event,
                               message.tickPrice,
                               message.tickSize)

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
            return
        
    def error_handler(self, msg):
        if msg.typeName == 'error'and msg.id != -1:
            print ('Server Error:', msg)

    def monitor_position(self, msg): #*
        print ('Last Price = %s' % (self.last_prices))
        varLast.set(self.last_prices)
        varBid.set(self.bid_price)
        varAsk.set(self.ask_price)


root = Tk()
root.title("Conexion a Binance")
root.geometry('600x480')
root.attributes('-topmost', True)
varSymbol = StringVar(root, value='NFLX')
varQuantity = StringVar(root, value='100')
varLimitPrice = StringVar()
varMarket = StringVar(root, value='SMART')
varOrderType = StringVar(root, value='LMT')
varPrimaryEx = StringVar(root, value='NASDAQ')
varTIF = StringVar(root, value='DAY')
varLast = StringVar()
varBid = StringVar()
varAsk = StringVar()
app = Application(root)


root.mainloop()
