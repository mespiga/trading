#https://pypi.org/project/websocket_client/
# import websocket

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

class StockDatabase(object):
    DB_FILE = r"/Users/miguelespiga/Documents/workspace/xcode/trading/backend/dailyMoves/model/pythonsqlite.db"
    conn = None

    # logging.basicConfig(filename='/home/ec2-user/projects/backend/logs/2real-'+ symbolOrder +'-' +datetime.now().strftime("%d-%m-%Y_%H-%M-%S")+ '.log', encoding='utf-8', level=logging.INFO)
    logging.basicConfig( level=logging.INFO)

    logging.basicConfig(format='%(asctime)s %(message)s')

    sql_create_stock_table = """ CREATE TABLE IF NOT EXISTS stock (
                                            id integer PRIMARY KEY AUTOINCREMENT,
                                            symbol text NOT NULL,
                                            created_at text,
                                            updated_at text,
                                            archived_at text
                                        ); """

    sql_create_stock_day_table = """ CREATE TABLE IF NOT EXISTS stock_day (
                                            id integer PRIMARY KEY AUTOINCREMENT,
                                            date text NOT NULL,
                                            stock_id integer NÕT NULL,
                                            vol_mean float,
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
            self.conn = sqlite3.connect(StockDatabase.DB_FILE)
            self.cur = self.conn.cursor()
            self.create_table_stock()
            self.create_table_stock_day()
        except Error as e:
            print(e)

    def close(self):
        """close sqlite3 connection"""
        self.conn.close()


    def update_stock(self, stock):
        """
        :param conn:
        :param order:
        :return: order id
        """
        sql = ''' UPDATE stock
                SET symbol = ? ,
                    created_at = ? ,
                    updated_at = ? ,
                    archived_at = ?  
                WHERE id = ?'''
        cur = self.conn.cursor()
        cur.execute(sql, stock)
        self.conn.commit()
        return self.cur.lastrowid

    def update_stock_day(self, stock_day):
        """
        :param conn:
        :param stock_day:
        :return: stock_day id
        """
        sql = ''' UPDATE stock_day
                SET date = ? ,
                    stock_id = ?,
                    vol_mean = ?,
                    created_at = ? ,
                    updated_at = ? ,
                    archived_at = ?  
                WHERE id = ?'''
        cur = self.conn.cursor()
        cur.execute(sql, stock_day)
        self.conn.commit()
        return self.cur.lastrowid

    def create_table_stock(self):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            self.cur = self.conn.cursor()
            self.cur.execute(StockDatabase.sql_create_stock_table)
        except Error as e:
            print(e)

    def create_table_stock_day(self):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            self.cur = self.conn.cursor()
            self.cur.execute(StockDatabase.sql_create_stock_day_table)
        except Error as e:
            print(e)



    def create_stock(self, stock):
        """
        Create a new stock
        :param conn:
        :param order:
        :return:
        """
        sql = ''' INSERT INTO stock(symbol,created_at,updated_at,archived_at)
                VALUES(?,?,?,?) '''
        self.cur = self.conn.cursor()
        self.cur.execute(sql, stock)
        self.conn.commit()
        return self.cur.lastrowid
    
    def delete_all_stocks(self):
        """
        delete all rows from table stock
        :param conn:
        :param order:
        :return:
        """
        sql = ''' DELETE from stock '''
        self.cur = self.conn.cursor()
        self.cur.execute(sql)
        self.conn.commit()

    def create_stock_day(self, stock_day):
        """
        Create a new stock_day
        :param conn:
        :param order:
        :return:
        """
        sql = ''' INSERT INTO stock_day(date,stock_id,vol_mean,created_at,updated_at,archived_at)
                VALUES(?,?,?,?,?,?) '''
        self.cur = self.conn.cursor()
        self.cur.execute(sql, stock_day)
        self.conn.commit()
        return self.cur.lastrowid
    
    def delete_all_stocks_day(self):
        """
        delete all rows from table stock_day
        :param conn:
        :param order:
        :return:
        """
        sql = ''' DELETE from stock_day '''
        self.cur = self.conn.cursor()
        self.cur.execute(sql)
        self.conn.commit()

    def get_all_stocks_active(self):
        """
        get all active rows from table stock
        :param conn:
        :return:
        """
        sql = ''' SELECT * from stock where archived_at is null '''
        self.cur = self.conn.cursor()
        self.cur.execute(sql)
        self.conn.commit()
        return self.cur.fetchall()

    def get_all_stocks_days_active(self):
        """
        get all active rows from table stock
        :param conn:
        :return:
        """
        sql = ''' SELECT * from stock s left join stock_day sd on s.id=sd.stock_id where sd.archived_at is null '''
        self.cur = self.conn.cursor()
        self.cur.execute(sql)
        self.conn.commit()
        return self.cur.fetchall()
    
    def get_all_stocks_days_active_groupby(self):
        """
        get all active rows from table stock
        :param conn:
        :return:
        """
        sql = ''' SELECT s.symbol,sd.stock_id, sd.date from stock s left join stock_day sd on s.id=sd.stock_id where sd.archived_at is null group by sd.stock_id'''
        self.cur = self.conn.cursor()
        self.cur.execute(sql)
        self.conn.commit()
        return self.cur.fetchall()

    def get_all_stocks_archived(self):
        """
        get all active rows from table stock
        :param conn:
        :return:
        """
        sql = ''' SELECT * from stock where archived_at is not null '''
        self.cur = self.conn.cursor()
        self.cur.execute(sql)
        self.conn.commit()
        rows = self.cur.fetchall()
        
        return rows
    


    # test database creation, insert and delete            
    def test(self):
        print(self.get_all_stocks_active())
        print(self.get_all_stocks_days_active())
        stock = ('FLGC','1', None, None )
        id=self.create_stock(stock)
        print(id)
        print(self.get_all_stocks_active())
        stock = ( 'FLGC','1', '1', '1',id )
        print(self.update_stock(stock))
        print(self.get_all_stocks_archived())
        stock_day=('2024-01-01', id, 123.1, '1', None, None )
        sid=self.create_stock_day(stock_day)
        print(sid)
        print(self.get_all_stocks_days_active())
        stock_day=('2024-01-02', id, 124.1, '1', None, None, sid )
        print(self.update_stock_day(stock_day))
        print(self.get_all_stocks_days_active())
        print(self.delete_all_stocks_day())
        print(self.delete_all_stocks())




# db = StockDatabase()
# db.test()

