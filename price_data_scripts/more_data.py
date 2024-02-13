"""
module is to compile more data such as h4 d1, w1
and m1 data to be store d in separate table
"""

import pandas as pd
import pymysql
import constants
import os
import logging
import aiosmtplib
import requests
from datetime import datetime, timedelta
import asyncio

def tf_query_manager(instrument:str, source_table:str):
    """
        query price data form hourly data and compile higher timeframe.
        args:
            instrument: currency pair
            source_table: table name for the database table
    """

    now_datetime = datetime.now()
    queryStr = None
    target_time = None
    print(now_datetime)
   
    if now_datetime.hour % 4 != 0:
        window = timedelta(hours=4)
        target_time = now_datetime - window
        print(target_time.strftime("%Y-%m-%d %H:%M:%S"))
        
    if now_datetime.hour == 0:
        pass
    if now_datetime.weekday == 0:
        pass
    if now_datetime.day == 1:
        pass

    # print(os.environ.get('STORAGE_MYSQL_USER'))
    
    # Connect to the database
    connection = pymysql.connect(
        host=os.environ.get('STORAGE_MYSQL_HOST'),
        user=os.environ.get('STORAGE_MYSQL_USER'),
        password=os.environ.get('STORAGE_MYSQL_PASSWORD'),
        db=os.environ.get('STORAGE_MYSQL_DB')
    )

    cursor = connection.cursor()
    type(target_time.strftime("%Y-%m-%d %H:%M:%S"))

    query_str = f"""
        SELECT {constants.DATETIME}, {constants.OPEN}, {constants.HIGH}, {constants.LOW}, {constants.CLOSE}
        FROM Jump_100_Index_h1
        WHERE {constants.DATETIME} >= '{target_time.strftime("%Y-%m-%d %H:%M:%S")}'
        ORDER BY {constants.DATETIME} ASC;
        """
    
    cursor.execute(query_str)
    data = cursor.fetchall()

    df = pd.DataFrame(data, columns=[
        constants.DATETIME,
        constants.OPEN,
        constants.HIGH,
        constants.LOW,
        constants.CLOSE]
        )
    
    cursor.close()

    print(df.head())

    # CONDITION_QUERY_SET = [
    #     # SELECT Datetime, Open, High, Low, Close
    #     # FROM Jump_100_Index_h1
    #     # WHERE Datetime >= '2024-02-11 10:00:00'
    #     # ORDER BY Datetime ASC;
    
    #     # 'Query for 4 hour data',
    #     f"""SELECT * FROM {constants.ALERTS_TABLE}
    #     WHERE {constants.TARGET_COL} < {price_row.iloc[-1][constants.CLOSE]}
    #     AND {constants.CURRENCY_PAIR_COL} = '{instrument}'
    #     AND {constants.EXPIRATION_COL} >= NOW()
    #     AND {constants.REPEAT_ALARM_COL} > {constants.ALERT_COUNT}
    #     AND {constants.SETUP_CONDITION_COL} = 'CLOSING PRICE IS GREATER THAN SETPOINT';
    #     """,

    #     # 'CLOSING PRICE IS LESS THAN SETPOINT'
    #     f"""SELECT * FROM {constants.ALERTS_TABLE}
    #     WHERE {constants.TARGET_COL} > {price_row.iloc[-1][constants.CLOSE]}
    #     AND {constants.CURRENCY_PAIR_COL} = '{instrument}'
    #     AND {constants.EXPIRATION_COL} >= NOW()
    #     AND {constants.REPEAT_ALARM_COL} > {constants.ALERT_COUNT}
    #     AND {constants.SETUP_CONDITION_COL} = 'CLOSING PRICE IS LESS THAN SETPOINT';
    #     """
    #     ]

tf_query_manager("EURUSD", "h1")