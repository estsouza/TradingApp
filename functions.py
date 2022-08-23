def get_slippage(client, symbol, size):
    depth = client.futures_order_book(symbol=symbol, limit=10)
    acumSize = 0
    acumAmount = 0
    for i in depth['bids']:
        price = float(i[0])
        qty = float(i[1])
        if qty > (size - acumSize):
            acumAmount += (size - acumSize) * price
            acumSize = size
            break
        else:
            acumSize += qty
            acumAmount += qty * price
    sellap = acumAmount/acumSize

    acumSize = 0
    acumAmount = 0
    for i in depth['asks']:
        price = float(i[0])
        qty = float(i[1])
        if qty > (size - acumSize):
            acumAmount += (size - acumSize) * price
            acumSize = size
            break
        else:
            acumSize += qty
            acumAmount += qty * price
    buyap = acumAmount/acumSize

    buyslip = round((buyap/float(depth['asks'][0][0]) -1)*1000, 2)
    sellslip = round((sellap/float(depth['bids'][0][0]) -1)*-1000, 2)
    print(f"Buying slippage {buyslip} %o @ {symbol}")
    print(f"Selling slippage {sellslip} %o @ {symbol}")
    return buyslip, sellslip

def calculate_size(lastPrice, symbol):
    print(f"2000 USD: {round(2000/lastPrice, 1)} {symbol}")
    print(f"4000 USD: {round(4000/lastPrice, 1)} {symbol}")
    print(f"6000 USD: {round(6000/lastPrice, 1)} {symbol}")
    print(f"8000 USD: {round(8000/lastPrice, 1)} {symbol}")
    print(f"10000 USD: {round(10000/lastPrice, 1)} {symbol}")

