class Instrument:
    def __init__(self, symbol):
        self.symbol = symbol
        self.size = 100
        self.ticksize = 2
        self.stoploss = 0.1


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