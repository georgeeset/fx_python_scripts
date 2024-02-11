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
from datetime import datetime
import asyncio

def tfQueryManager(instrument:str, source_table:str):
    """
        query price data form hourly data and compile higher timeframe.
        args:
            instrument: currency pair
            source_table: table name for the database table
    """

    now_time = datetime.now()

    if now_time.hour % 4 == 0:
        pass
    if now_time.hour == 0:
        pass
    if now_time.weekday == 0:
        pass
    if now_time.day == 1:
        pass

    CONDITION_QUERY_SET = [
        # SELECT Datetime, Open, High, Low, Close
        # FROM Jump_100_Index_h1
        # WHERE Datetime >= '2024-02-11 10:00:00';
    
        # 'Query for 4 hour data',
        f"""SELECT * FROM {constants.ALERTS_TABLE}
        WHERE {constants.TARGET_COL} < {price_row.iloc[-1][constants.CLOSE]}
        AND {constants.CURRENCY_PAIR_COL} = '{instrument}'
        AND {constants.EXPIRATION_COL} >= NOW()
        AND {constants.REPEAT_ALARM_COL} > {constants.ALERT_COUNT}
        AND {constants.SETUP_CONDITION_COL} = 'CLOSING PRICE IS GREATER THAN SETPOINT';
        """,

        # 'CLOSING PRICE IS LESS THAN SETPOINT'
        f"""SELECT * FROM {constants.ALERTS_TABLE}
        WHERE {constants.TARGET_COL} > {price_row.iloc[-1][constants.CLOSE]}
        AND {constants.CURRENCY_PAIR_COL} = '{instrument}'
        AND {constants.EXPIRATION_COL} >= NOW()
        AND {constants.REPEAT_ALARM_COL} > {constants.ALERT_COUNT}
        AND {constants.SETUP_CONDITION_COL} = 'CLOSING PRICE IS LESS THAN SETPOINT';
        """
        ]