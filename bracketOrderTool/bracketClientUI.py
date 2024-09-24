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

from guizero import App, Text, Box, PushButton, TextBox
import sys, os, time
from datetime import datetime
from model.OrderDatabase import OrderDatabase
from lib.stopLoss import commitOrder, isAfterHoursOpen
import alpaca_trade_api as tradeapi
import requests

import logging
logging.basicConfig( level=logging.CRITICAL)

api = tradeapi.REST()

a               = []
b               = []
order_content    = []
texto_estrelas   = []
colors           = ["#20ff00", "#228b22", "#00ff00", "#228b22", "#00ff00"]
app = App(layout="grid", width=1400, height=500, bg="#feffa3")
db = OrderDatabase()
extendedHours = ''
checkMarketTimer = 10000

def fetchOrders():
    order_content = []
    try:
        orders = db.get_all_active()
        for order in orders:
            aux = api.get_order(order_id=order[1], nested=True)
            order_content.append(aux)
    except Exception as err:
            print(err)
            app.error("Uh oh!", "Submitting Bracket Order error: " + str(err))
            return []
    return order_content

def drawExtendedHoursNotice():
    global extendedHours, app
    extendedHours = Text(app, text="Market Open", grid=[0,0], align="left")

def drawBracketForm(): 
    global app, extendedHours
    # Create Bracket order form
    symbol = Text(app, text="Symbol", grid=[0,0], align="left")
    symbolVal = TextBox(app, text="", grid=[1,0])
    symbolVal.text_color = "black"

    qty = Text(app, text="Quantity", grid=[2,0], align="left")
    qtyVal = TextBox(app, text="", grid=[3,0])
    qtyVal.text_color = "black"

    stopLoss = Text(app, text="Stop Loss", grid=[4,0], align="left")
    stopLossVal = TextBox(app, text="", grid=[5,0])
    stopLossVal.text_color = "black"

    limitProfit = Text(app, text="Limit Profit", grid=[6,0], align="left")
    limitProfitVal = TextBox(app, text="", grid=[7,0])
    limitProfitVal.text_color = "black"

    extended_hours = isAfterHoursOpen()

    bracket_order_button = PushButton(app, text="Submit Bracket Order", grid=[11,0], command=bracket_order, args=[symbolVal, qtyVal, stopLossVal, limitProfitVal, extended_hours])
    bracket_order_button.bg = "Orange"

    new_line = Text(app, text="", grid=[0,1,11,1], align="left")

    # Extended hours
    extendedHours = Text(app, text="Loading...", grid=[0,1], align="left")
    extendedHours.repeat(checkMarketTimer, counter)

    PushButton(app, text="Refresh Table", grid=[0,2], command=refreshTableContent)

    new_line = Text(app, text="", grid=[0,3,11,1], align="left")


def drawTableHeader(): 
    global app
    # Table Header
    symbol = Text(app, text="Symbol", grid=[0,4], align="left")
    qty = Text(app, text="Filled_qty", grid=[1,4], align="left")
    status = Text(app, text="Status", grid=[2,4], align="left")
    filled_avg_price = Text(app, text="Filled_avg_price", grid=[3,4], align="left")
    loss = Text(app, text="loss", grid=[4,4])
    loss.text_color = "black"
    loss_status = Text(app, text=("Side - status"), grid=[5,4])
    profit = Text(app, text="Profit", grid=[6,4])
    profit.text_color = "black"
    profit_status = Text(app, text=("Side - status"), grid=[7,4])
    

def drawTableContent():
    global app
    orders = fetchOrders()

    i=5
    for order in orders:
        print(order)
        symbol = Text(app, text=order.symbol, grid=[0,i], align="left")
        qty = Text(app, text=order.filled_qty, grid=[1,i], align="left")
        status = Text(app, text=order.status, grid=[2,i], align="left")
        filled_avg_price = Text(app, text=order.filled_avg_price, grid=[3,i], align="left")
        if(order.legs[0].status == 'filled' or order.legs[1].status == 'filled' or order.legs[0].status == 'canceled' or order.legs[1].status == 'canceled'):
            loss = Text(app, text=order.legs[1].stop_price, grid=[4,i])
            loss_status = Text(app, text=(order.legs[1].side + " - " + order.legs[1].status), grid=[5,i])
            profit = Text(app, text=order.legs[0].limit_price, grid=[6,i])
            profit_status = Text(app, text=(order.legs[0].side + " - " + order.legs[0].status), grid=[7,i])
            refresh_button = PushButton(app, text="Archive", grid=[8,i], command=archive, args=[order.id])
            refresh_button.bg = "Orange"
        else:
            loss = TextBox(app, text=order.legs[1].stop_price, grid=[4,i])
            loss.text_color = "black"
            loss_status = Text(app, text=(order.legs[1].side + " - " + order.legs[1].status), grid=[5,i])
            profit = TextBox(app, text=order.legs[0].limit_price, grid=[6,i])
            profit.text_color = "black"
            profit_status = Text(app, text=(order.legs[0].side + " - " + order.legs[0].status), grid=[7,i])
            loss_button = PushButton(app, text="Update Loss", grid=[8,i], command=update_loss, args=[order.legs[1],loss.value,loss])
            loss_button.bg = "Orange"
            profit_button = PushButton(app, text="Update Profit", grid=[9,i], command=update_profit, args=[order.legs[0],profit.value,profit])
            profit_button.bg = "Orange"

            cancel_sell_button = PushButton(app, text="Cancel P&L and Sell Now", grid=[11,i], command=cancel_sell_now, args=[order])
            cancel_sell_button.bg = "Orange"
        new_line = Text(app, text="", grid=[0,i+1,11,1], align="left")

        i=i+2


def cleanTableContent():
    global app
    app.destroy()
    app = App(layout="grid", width=1400, height=500, bg="#feffa3")
    drawBracketForm()
    drawTableHeader()
    app.display()



def refreshTableContent():
    global app
    app.destroy()
    app = App(layout="grid", width=1400, height=500, bg="#feffa3")
    draw()

def draw():
    drawBracketForm()
    drawTableHeader()
    drawTableContent()
    app.display()

def archive(orderId):
    db.archive_order_by_order_id(orderId)
    app.info("Archive", "Order archived successfuly!")
    refreshTableContent()

def bracket_order(symbolVal, qtyVal, stopLossVal, limitProfitVal, extended_hours):
    try:
        print(str(symbolVal.value) + ' | ' + str(qtyVal.value) + ' | ' + str(stopLossVal.value) + ' | ' + str(limitProfitVal.value) )
        # validate if all fields are filled
        if(str(symbolVal.value) == "" or str(qtyVal.value) == "" or str(stopLossVal.value) == "" or str(limitProfitVal.value) == ""):
            app.warn("Uh oh!", "All form values but be filled")
            return
        # caps symbol
        symbolVal.value = str(symbolVal.value).upper()
        # validate numbers
        if(validateNumber(qtyVal.value) is False or validateNumber(stopLossVal.value) is False or validateNumber(limitProfitVal.value) is False):
            return
        # validate limit profit is higher than stop loss
        if(float(stopLossVal.value) > float(limitProfitVal.value)):
            app.warn("Uh oh!", "Change Stop Loss/Limit Profit values. Stop Loss " +stopLossVal.value +  " value must be less than Profit Limit value " + limitProfitVal.value)
            return
        #buy
        
        main_order = commitOrder(symbolVal.value, 'buy', float(limitProfitVal.value), float(stopLossVal.value), float(qtyVal.value), extended_hours)
        print("main_order")
        print(main_order)
        if(main_order == None):
            print("Bracket create order cancelled.")
            app.warn("Create Bracket Order", "Bracket create order cancelled. Try again at market hours")
            return
        else:
            print("Bracket order filled successfully")
        # update database
        db = OrderDatabase()
        order_db = (main_order.id, main_order.legs[0].id, main_order.legs[1].id,datetime.now(), None, None)
        db.create_order(order_db)
        print("Local Database updated")

        app.info("Create Bracket Order", "Bracket Order created successfuly!")
        refreshTableContent()
    except Exception as err:
        app.error("Uh oh!", "Submitting Bracket Order error: " + str(err))


def update_profit(ord, old_p, new_p):
    if(validateNumberPair(old_p, new_p.value) is False):
        new_p.value=old_p
        return
    
    profit_dialog = app.yesno("Sell Profit change...", "Do you wanto to change sell Profit from "+old_p+" to " + new_p.value + " ?")
    if profit_dialog == True:
        ord = api.replace_order(order_id=ord.id, limit_price=new_p.value)
        app.info("Profit", "Profit changed to " + new_p.value + "!")
        refreshTableContent()
    else:
        app.info("Profit", "Okay bye...")
        new_p.value=old_p
        return
    
def update_loss(ord, old_p, new_p):
    if(validateNumberPair(old_p, new_p.value) is False):
        new_p.value=old_p
        return
    if(float(new_p.value)<=float(old_p)):
        app.warn("Uh oh!", new_p.value + " is less than the current stop loss of " + old_p + ". You only can increase stop loss value.")
        new_p.value=old_p
        return

    loss_dialog = app.yesno("Sell Loss change...", "Do you wanto to change sell Loss from "+old_p+" to " + new_p.value + " ?")
    if loss_dialog == True:
        ord = api.replace_order(order_id=ord.id, stop_price=new_p.value)
        app.info("Loss", "Loss changed to " + new_p.value + "!")
        refreshTableContent()
    else:
        app.info("Loss", "Okay bye...")
        new_p.value=old_p
        return


def cancel_sell_now(ord):
    # todo
    cancel_dialog = app.yesno("Cancel & Sell...", "Do you wanto to Cancel & Sell " + ord.filled_qty + " stocks of " +ord.symbol + " ?")
    if cancel_dialog == True:
        print(ord.filled_qty)
        api.cancel_order(order_id=ord.legs[0].id)
        print("Order cancelled successfully: " + ord.filled_qty + " stocks of " +ord.symbol)
        if(ord == None or float(ord.filled_qty) == 0):
            print("Order cancelled successfully of " +ord.symbol)
            app.error("Cancel", "Order cancelled successfully of " +ord.symbol)
            return
        else:    
            sell_order = api.submit_order(
                            symbol=ord.symbol,
                            type='market',
                            qty=ord.filled_qty,
                            side='sell',
                            time_in_force='gtc'
                        )
            count=0
            while(sell_order.status != 'filled'):
                sell_order = api.get_order_by_client_order_id(str(sell_order.client_order_id))
                time.sleep(2)
                count = count + 1
                if(count >=8):
                    api.cancel_order(str(sell_order.id))
                    print("Limit profit order canceled. However it wasn't possible to sell the order " + ord.filled_qty + " stocks of " +ord.symbol + " Please try again manually in your broker system.")
                    app.info("Cancel", "Limit profit order canceled. However it wasn't possible to sell the order " + ord.filled_qty + " stocks of " +ord.symbol + " Please try again manually in your broker system.")
            print("Order cancelled and sold successfully: " + ord.filled_qty + " stocks of " +ord.symbol)
            app.info("Cancel", "Order cancelled and sold successfully: " + ord.filled_qty + " stocks of " +ord.symbol)
            refreshTableContent()
    else:
        app.info("Cancel", "Okay bye...")
        return

def validateNumberPair(old_num, new_num):
    try:
        float(new_num)
    except:
        app.warn("Uh oh!", new_num + " is not a number. Valid examples are 20.3 or 20")
        return False
    if(float(new_num)==float(old_num)):
        app.warn("Uh oh!", new_num + " is equal than the current stop loss of " + old_num + ". No action needed.")
        return False

def validateNumber(num):
    try:
        float(num)
    except:
        app.warn("Uh oh!", num + " is not a number. Valid examples are 20.3 or 20")
        return False
    
def counter():
    global extendedHours, app

    if(isAfterHoursOpen()):
        extendedHours.value = "After Hours Open"
    else:
        extendedHours.value = "Market Close"

draw()