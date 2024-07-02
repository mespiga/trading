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


import json
import math
from tokenize import Number
import alpaca_trade_api as tradeapi
import  pandas                  as pd
from datetime import datetime
import yfinance as yf
from yfinance import shared
import logging
logging.basicConfig( level=logging.INFO)

import finnhub
import sys, os, time
sys.path.append(os.path.abspath("model"))
from StockDatabase import StockDatabase
from lib.TradeBars import populateSymbols

from pandas_datareader import data as pdr
import yfinance as yf
import datetime as dt

logging.basicConfig( level=logging.INFO)
logging.basicConfig(format='%(asctime)s %(message)s')

def findBullish(df, sDate, symbol):
    ret=False
    arr =[]
    df2 = df.loc[str(sDate)]
    df["Mean_Close"]=df2.iloc[:,3].rolling(window=window).mean()
    df["Mean_Open"]=df2.iloc[:,0].rolling(window=window).mean()
    df2 = df.loc[str(sDate)]
    i=0
    for row in df2.iterrows():
        i=i+1
        if(i==len(df2)):
            break
        try:
            if(row[1]['Mean_Close']>row[1]['Mean_Open']*profit):
                arr.append(row[0])
                ret = True
        except:
            continue
    # print(arr)
    if ret and (str(arr[-1])[8:10] == str(dt.datetime.now())[8:10]):
        logging.info('--------------------------------------------')
        logging.info('------------------- buy: '+symbol+ ' -------------------------')
        logging.info('------------------- BUY TODAY TODAY TODAY '+str(arr[-1])+' -------------------------')
        logging.info('--------------------------------------------')
    return ret

def findGold(symbol):
    try:
        df = yf.download(symbol, interval=interval, period=str(rangeDays)+'d',progress=False)
        # logging.info(df)
        if(shared._ERRORS != {}):
            return None
        startDate = df.index[0]
        prevVolSum = 0
        for i in range(0, (rangeDays+2)):
            delta = dt.timedelta(days=i)
            nextDate = str(df.index[0]+delta)[0:10]
            # logging.info(nextDate)
            volSum=df.loc[str(nextDate)]['Volume'].sum()
            # logging.info('volume '+str(volSum) +' previousVol '+str(prevVolSum))
            # if(prevVolSum==0):
            #     prevVolSum=volSum
            #     continue
            if(volSum > prevVolSum*factor and i==(rangeDays)):
                # logging.info(nextDate)
                if(findBullish(df, nextDate, symbol)):
                    return
                else:
                    logging.info('************ not 2 ***************')
            elif( i==(rangeDays-1)):
                logging.info('************ not ***************')
            prevVolSum=volSum
    except:
        pass

yf.pdr_override()
db = StockDatabase()
finnhub_client = finnhub.Client(api_key="cotql7pr01qr7r8ge7u0cotql7pr01qr7r8ge7ug")
interval='1m'
rangeDays=7
# todo: number of trades should be taken into account, similar to volume, 100 trades of 1k shares each means more than 1 trade of 100k shares
factor=5 # high number is 100 less risk and more profit around 10%, low number is 20 usually miore risk and less profit around 5%
window=3 # high number less risk
profit=1.005

# findGold('TSRI')


stocks = db.get_all_stocks_active()
if(stocks == []):
    populateSymbols()

for stock in stocks:
    logging.info(stock[1])
    findGold(stock[1])
    