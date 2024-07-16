login = 5027070331
password = "5q+mVpSy"
server = "MetaQuotes-Demo"

import MetaTrader5 as mt5

mt5.initialize()
mt5.login(login, password, server)

symbol = "EURUSD"
tick = mt5.symbol_info_tick(symbol)

request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volom": 2.0,
    "type": mt5.ORDER_TYPE_SELL,
    "position": mt5.positions_get(),
    "price": tick.bid,
    "sl": 0.0,
    "tp": 0.0,
    "devition": 20,
    "magic": 234000,
    "comment": "python script open",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_IOC
}
mt5.order_send(request)

mt5.shutdown()
print(5)