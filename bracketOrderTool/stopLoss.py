#https://pypi.org/project/websocket_client/
# import websocket
import asyncio
import concurrent.futures
from datetime import datetime, timedelta
import json
from json.tool import main
from nis import cat
import time
import math
import os


from datetime import datetime
from pytz import timezone
import logging
import requests, sys
sys.path.append(os.path.abspath("model"))
from OrderDatabase import OrderDatabase

# Nasdaq timezone
tz = timezone('EST')
# Import decimal module
from decimal import Decimal

import alpaca_trade_api as tradeapi

api = tradeapi.REST()

# logging.basicConfig(filename='/home/ec2-user/projects/backend/logs/2real-'+ symbolOrder +'-' +datetime.now().strftime("%d-%m-%Y_%H-%M-%S")+ '.log', encoding='utf-8', level=logging.INFO)
logging.basicConfig( level=logging.INFO)

logging.basicConfig(format='%(asctime)s %(message)s')


############################################################
############################################################

def isMarketOpen():
    clock = api.get_clock()
    if clock.is_open:
        return True
    else:
        return False
    
def getPositions():
    # Get a list of all of our positions.
    portfolio = api.list_positions()

    # Print the quantity of shares for each position.
    for position in portfolio:
        print("{} shares of {} | P&L {} | Average cost per stock {} | Stock Current Price {} | Cost when buying {} | Current value {}".
            format(position.qty, position.symbol, position.unrealized_pl, position.avg_entry_price, position.current_price, position.cost_basis, position.market_value))
    


def put_stop_loss_order(symbol, p_profit, p_stop, quant, extended_hours):
    global stop_loss_order,symbolOrder
   
    # Limit order
    stop_loss_order = api.submit_order(
                        order_class='bracket',
                        symbol=symbol,
                        extended_hours=extended_hours,
                        type='market',
                        qty=round(quant,0),
                        side='buy',
                        time_in_force='gtc',
                        take_profit={
                            'limit_price':round(float(p_profit),2)
                        },
                        stop_loss={
                            'stop_price':round(float(p_stop),2)
                            # 'limit_price':round(float(p_stop_limit),2)
                        }
                ) 
    logging.info('stop_loss_order')
    logging.info(stop_loss_order)
    return stop_loss_order

def commitOrder(symbol, side, p_profit, p_stop, quant, extended_hours):
    count = 0
    order = put_stop_loss_order(symbol, p_profit, p_stop, quant, extended_hours)

    while(order.status != 'filled'):
        order = api.get_order_by_client_order_id(str(order.client_order_id))
        time.sleep(2)
        count = count + 1
        if(count >=4):
            api.cancel_order(str(order.id))
            logging.info('orderCancelled')
            #cancelOrder(str(limit_order.id))
            return None
    return order

def getAccount():
     accountInfo = api.get_account()
    #  print(accountInfo)
     return accountInfo

def getAvailableCash():
    return getAccount().cash

def test():
    symbol = 'COIN'
    profit_price = '260'
    loss_price = '240'
    quant = 1
    extended_hours = None

    main_order = commitOrder(symbol, 'buy', profit_price, loss_price, quant, extended_hours)
    order_db = (main_order.id, main_order.legs[0].id, main_order.legs[1].id,datetime.now(), None, None)

    db = OrderDatabase()
    db.create_order(order_db)

    print('--------------- Main  --------------------')
    print(main_order.symbol)
    print(main_order.id)
    print(main_order.qty)
    print(main_order.status)
    print('--------------- Profit  --------------------')
    print(main_order.legs[0].side)
    print(main_order.legs[0].id)
    print(main_order.legs[0].limit_price)
    print(main_order.legs[0].status)

    print('--------------- Loss  --------------------')
    print(main_order.legs[1].side)
    print(main_order.legs[1].id)
    print(main_order.legs[1].stop_price)
    print(main_order.legs[1].status)
