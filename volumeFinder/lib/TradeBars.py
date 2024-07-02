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
logging.basicConfig( level=logging.CRITICAL)

import finnhub
import sys, os, time
sys.path.append(os.path.abspath("model"))
from StockDatabase import StockDatabase
db = StockDatabase()


finnhub_client = finnhub.Client(api_key="cotql7pr01qr7r8ge7u0cotql7pr01qr7r8ge7ug")


from pandas_datareader import data as pdr

import yfinance as yf
yf.pdr_override()
import datetime as dt

end = dt.datetime.now()
interval='1m'
rangeDays=5
range=str(rangeDays)+'d'


# todo: number of trades should be taken into account, similar to volume, 100 trades of 1k shares each means more than 1 trade of 100k shares
# symbol='INOD'
factor=10 # high number is 100 less risk and more profit around 10%, low number is 20 usually miore risk and less profit around 5%
#sellValue= close * profitPerc # profitPerc increases with factor increase
window=3 # high number less risk

def whenVolumeChanged(symbol,factor):
    try:
        url='https://query1.finance.yahoo.com/v8/finance/chart/'+symbol+'?metrics=high&interval='+interval+'&range='+range

        df = yf.download(symbol, interval=interval, period=range,progress=False)

        if(shared._ERRORS != {} ):
            return None
        stock = (symbol,datetime.now(), None, None )
        id=db.create_stock(stock)
        logging.info('stock added')
        i=rangeDays
        previousVol =0


        while(i!=-1):
            delta = dt.timedelta(days=i+1)
            start = end-delta
            volMean = df.loc[str(start.year)+'-'+str(start.month)+'-'+str(start.day)]['Volume'].mean()
            logging.info('stock added')
            if( not math.isnan(volMean)):   
                stock_day=(str(start.year)+'-'+str(start.month)+'-'+str(start.day), id, volMean, datetime.now(), None, None )
                sid=db.create_stock_day(stock_day)
                logging.info('day stock added')
                logging.info(volMean + ' : '+str(start.year)+'-'+str(start.month)+'-'+str(start.day))

            if( not math.isnan(volMean) and previousVol!=0 and volMean > previousVol*factor):
                df2=df.loc[str(start.year)+'-'+str(start.month)+'-'+str(start.day)]
                df["Mean_Close"]=df2.iloc[:,3].rolling(window=window).mean()
                df["Mean_Open"]=df2.iloc[:,0].rolling(window=window).mean()
                df["Mean_Volume"]=df2.iloc[:,5].rolling(window=window).mean()
                df2=df.loc[str(start.year)+'-'+str(start.month)+'-'+str(start.day)]

                for row in df2.iterrows():
                    if( not math.isnan(row[1]['Mean_Volume'])):
                        try:
                            if(row[1]['Mean_Close']>row[1]['Mean_Open'] and row[1]['Mean_Volume']>previousVol*factor):
                                print('--------------------------------------------')
                                print('--------------------------------------------')
                                print(symbol + ' big up --- ' + str(row[1]['Mean_Volume']))
                                print(row[1])
                                print('--------------------------------------------')
                                print('--------------------------------------------')
                                break
                                # return row
                        except:
                            continue
            previousVol=volMean
            i=i-1
    except:
        print('??????????????????????')
        return None

def populateSymbols():
    db.delete_all_stocks_day()
    db.delete_all_stocks()
    
    if(db.get_all_stocks_active() == []):
        symbols = finnhub_client.stock_symbols('US')
        for symbol in symbols:
            logging.info(symbol)
            res = whenVolumeChanged(symbol['symbol'],factor)
            if(res != None):
                print(res)

    # logging.info(db.get_all_stocks_active())

