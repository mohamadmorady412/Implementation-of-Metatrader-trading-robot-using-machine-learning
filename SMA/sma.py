from information import login, password
from Server import server

import MetaTrader5 as mt5
import pandas as pd
import time
from datetime import datetime


def Maket_order(symbol, volume, order_type, **kwargs):
    tick = mt5.symbol_info_tick(symbol)

    order_dict = {'buy': 0, 'sell': 1}
    price_dict = {'buy': tick.ask, 'sell': tick.bid}

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": order_dict[order_type],
        "price": price_dict[order_type],
        "deviation": DEVIATION,
        "magic": 100,
        "comment": 'python market order',
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC
    }

    order_result = mt5.order_send(request)
    print(order_result)
    return order_result

def Cloas_order(ticket):
    positions = mt5.positions_get()

    type_dict = {0:1, 1:0}
    for pos in positions:
        tick = mt5.symbol_info_tick(pos.symbol)
        price_dict = {0:tick.ask, 1:tick.bid}

        if pos.ticket == ticket:
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "positions": pos.ticket,
                "symbol": "EURUSD",
                "volume": tick.volume,
                "type": type_dict[pos.type],
                "price": price_dict[pos.type],
                "magic": 100,
                "comment": 'python cloas order',
                "type_time": mt5.ORDER_FILLING_IOC
            }

            order_result = mt5.order_send(request)
            print(order_result)
            return order_result
        return 'Ticket does not exist'

def get_exposure(symbol):
    positions = mt5.positions_get(symbol=symbol)
    if positions:
        pos_df = pd.DataFrame(positions, columns=positions[0]._asdict().keys())
        exposure = pos_df['volume'].sum()

        return exposure

def signal(symbol, timeframe, sma_period):
    bars = mt5.copy_rates_from_pos(symbol, timeframe, 1, sma_period)
    bars_df = pd.DataFrame(bars)
    last_cloas = bars_df.iloc[-1].close
    sma = bars_df.close.mean()
    direction = 'flat'

    direction = 'buy' if last_cloas > sma else 'sell'

    return last_cloas, sma, direction

if __name__ == '__main__':
    SYMBOL = "EURUSD"
    VOLUME = 1.0
    TIMEFRAME = mt5.TIMEFRAME_M1
    SMA_PERIOD = 10
    DEVIATION = 20

    mt5.initialize()
    mt5.login(login, password, server)

    while True:
        exposure = get_exposure(SYMBOL)

        last_close, sma, direction = signal(SYMBOL, TIMEFRAME, SMA_PERIOD)

        if direction == 'buy':
            for pos in mt5.positions_get():
                if pos.type == 1:
                    Cloas_order(pos.ticket)

            if not mt5.positions_total():
                Maket_order(SYMBOL, VOLUME, direction)
        
        else:
            for pos in mt5.positions_get():
                if pos.type == 0:
                    Cloas_order(pos.ticket)
            
            if not mt5.positions_total():
                Maket_order(SYMBOL, VOLUME, direction)
            
        print(f'''
                time: {datetime.now()}
                exposure: {exposure}
                last cloas: {last_close}
                sma: {sma}
                signal: {signal}
                -----------\n
              ''')
        
        time.sleep(1)

mt5.shotdown()