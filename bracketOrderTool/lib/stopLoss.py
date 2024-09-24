## DISCLAIMER
# Trading leveraged products carries a high degree of risk and you could lose more than your initial deposit. Any code,opinions, chats, messages, news, research, analyses, prices, or other information contained on this repository are provided as general market information for educational and entertainment purposes only, and do not constitute investment advice neither investment assurance. The code in this repository should not be relied upon as a substitute for extensive independent market research before making your actual trading decisions.

# THE AUTHOR OF THIS REPOSITORY will not accept liability for any loss or damage, including without limitation any loss of profit, which may arise directly or indirectly from use of THE CODE SOFTWARE WITHIN THIS REPOSITORY.

# THE AUTHOR OF THIS REPOSITORY do not recommend the use of technical analysis as a sole means of trading decisions. THE AUTHOR OF THIS REPOSITORY do not recommend making hurried trading decisions. You should always understand that PAST PERFORMANCE IS NOT NECESSARILY INDICATIVE OF FUTURE RESULTS.

## LICENSE
# This file is part of tradingTools.

# tradingTools is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# tradingTools is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with tradingTools. If not, see <https://www.gnu.org/licenses/>.

# Author: Miguel Espiga


# Copyright 2024 to the author Miguel Espiga. All Rights Reserved

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

trading_hours_token="sdZRsMb34qMYFuFtXxmqtOO5EfvsbzyMHa96ugkkd75e7b51"

logging.basicConfig( level=logging.INFO)

logging.basicConfig(format='%(asctime)s %(message)s')


############################################################
############################################################

def isAfterHoursOpen():
    if(isPreMarketOpen()):
        return True
    elif(isPostMarketOpen()):
        return True
    else:
        return False

def isMarketOpen():
    clock = api.get_clock()
    if clock.is_open:
        return True
    else:
        return False

def isPreMarketOpen():
    date = datetime.today().strftime('%Y-%m-%d')
   
    d = requests.get("https://api.tradinghours.com/v3/markets/hours?fin_id=us.nyse&api_token="+trading_hours_token+"&date="+date).json()
    if("Pre-Trading Session" in d['data']['schedule'][0]['phase_type']):
        if("Closed" in d['data']['schedule'][0]['status']):
            return False
    return True

def isPostMarketOpen():
    date = datetime.today().strftime('%Y-%m-%d')
   
    d = requests.get("https://api.tradinghours.com/v3/markets/hours?fin_id=us.nyse&api_token="+trading_hours_token+"&date="+date).json()
    if("Post-Trading Session" in d['data']['schedule'][5]['phase_type']):
        if("Closed" in d['data']['schedule'][5]['status']):
            return False
    return True
    
def getPositions():
    # Get a list of all of our positions.
    portfolio = api.list_positions()

    # Print the quantity of shares for each position.
    for position in portfolio:
        logging.info("{} shares of {} | P&L {} | Average cost per stock {} | Stock Current Price {} | Cost when buying {} | Current value {}".
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
    loss_price = '220'
    quant = 1
    extended_hours = None

    main_order = commitOrder(symbol, 'buy', profit_price, loss_price, quant, extended_hours)
    order_db = (main_order.id, main_order.legs[0].id, main_order.legs[1].id,datetime.now(), None, None)

    db = OrderDatabase()
    db.create_order(order_db)

    logging.info('--------------- Main  --------------------')
    logging.info(main_order.symbol)
    logging.info(main_order.id)
    logging.info(main_order.qty)
    logging.info(main_order.status)
    logging.info('--------------- Profit  --------------------')
    logging.info(main_order.legs[0].side)
    logging.info(main_order.legs[0].id)
    logging.info(main_order.legs[0].limit_price)
    logging.info(main_order.legs[0].status)

    logging.info('--------------- Loss  --------------------')
    logging.info(main_order.legs[1].side)
    logging.info(main_order.legs[1].id)
    logging.info(main_order.legs[1].stop_price)
    logging.info(main_order.legs[1].status)

