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
import time
import math
import os
import sqlite3
from sqlite3 import Error


from datetime import datetime
from pytz import timezone
import logging
import requests

from decimal import Decimal

class OrderDatabase(object):
    DB_FILE = r"/Users/miguelespiga/Documents/workspace/xcode/trading/backend/dailyMoves/model/pythonsqlite.db"
    conn = None

    # logging.basicConfig(filename='/home/ec2-user/projects/backend/logs/2real-'+ symbolOrder +'-' +datetime.now().strftime("%d-%m-%Y_%H-%M-%S")+ '.log', encoding='utf-8', level=logging.INFO)
    logging.basicConfig( level=logging.INFO)

    logging.basicConfig(format='%(asctime)s %(message)s')

    sql_create_orders_table = """ CREATE TABLE IF NOT EXISTS orders (
                                            id integer PRIMARY KEY,
                                            orderId text NOT NULL,
                                            orderSellLimitId text,
                                            orderStopLimitId text,
                                            created_at text,
                                            updated_at text,
                                            archived_at text
                                        ); """


    ############################################################
    ############################################################

    def __init__(self):
        """ create a database connection to the SQLite database
            specified by the db_file
        :param db_file: database file
        :return: Connection object or None
        """
        try:
            self.conn = sqlite3.connect(OrderDatabase.DB_FILE)
            self.cur = self.conn.cursor()
            self.create_table()
        except Error as e:
            print(e)

    def close(self):
        """close sqlite3 connection"""
        self.conn.close()


    def update_order(self, order):
        """
        :param conn:
        :param order:
        :return: order id
        """
        sql = ''' UPDATE orders
                SET orderId = ? ,
                    orderSellLimitId = ? ,
                    orderStopLimitId = ? ,
                    created_at = ? ,
                    updated_at = ? ,
                    archived_at = ?  
                WHERE id = ?'''
        cur = self.conn.cursor()
        cur.execute(sql, order)
        self.conn.commit()
        return self.cur.lastrowid

    def create_table(self):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            self.cur = self.conn.cursor()
            self.cur.execute(OrderDatabase.sql_create_orders_table)
        except Error as e:
            print(e)



    def create_order(self, order):
        """
        Create a new order
        :param conn:
        :param order:
        :return:
        """
        sql = ''' INSERT INTO orders(orderId,orderSellLimitId,orderStopLimitId,created_at,updated_at,archived_at)
                VALUES(?,?,?,?,?,?) '''
        self.cur = self.conn.cursor()
        self.cur.execute(sql, order)
        self.conn.commit()
        return self.cur.lastrowid
    
    def delete_all_rows(self):
        """
        delete all rows from table orders
        :param conn:
        :param order:
        :return:
        """
        sql = ''' DELETE from orders '''
        self.cur = self.conn.cursor()
        self.cur.execute(sql)
        self.conn.commit()

    def get_all_active(self):
        """
        get all active rows from table orders
        :param conn:
        :param order:
        :return:
        """
        try:
            sql = ''' SELECT * from orders where archived_at is null '''
            self.cur = self.conn.cursor()
            self.cur.execute(sql)
            self.conn.commit()
            return self.cur.fetchall()
        except Error as e:
            print(e)
    
    def get_all_archived(self):
        """
        get all active rows from table orders
        :param conn:
        :param order:
        :return:
        """
        sql = ''' SELECT * from orders where archived_at is not null '''
        self.cur = self.conn.cursor()
        self.cur.execute(sql)
        self.conn.commit()
        rows = self.cur.fetchall()
        
        return rows
    
    def archive_order_by_order_id(self, orderId):
        order = (str(datetime.now()),str(datetime.now()),orderId)
        """
        :param conn:
        :param order:
        :return: order id
        """
        sql = ''' UPDATE orders
                SET updated_at = ?,
                    archived_at = ? 
                WHERE orderId = ? '''
        cur = self.conn.cursor()
        cur.execute(sql,order)
        self.conn.commit()
        return self.cur.lastrowid


    # test database creation, insert and delete            
    def test(self):
        order = ( '1', '1', '1','1', None, None )
        id=self.create_order(order)
        print(id)
        print(self.get_all_active())
        order = (id, '2', '1', '1','1', '1', '1' )
        print(self.update_order(order))
        print(self.get_all_archived())
        print(self.delete_all_rows())




# db = OrderDatabase()
# db.test()

