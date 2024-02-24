#!/usr/bin/env python3
""" Module for retrieving crypto exchange rate
check for user alerts and send reminder email
"""
import asyncio
import logging
import os
import pandas as pd
import constants
from datetime import datetime
from binance.spot import Spot
from db_storage_service import MysqlOperations
from alert_query_service import alert_query_manager
from more_data import tf_query_manager, measured_time
from data_source.binance import BinanceData

async def crypto_data_service():
    """ extract crypto prices and query alerts
    send alerts to users based on request
    """
    # my_client = Spot()
    binance_data = BinanceData()
    query_async_tasks = []
    now = datetime.now()

    for ticker in constants.CRYPTO_TICKERS:
        current_pair = f'{ticker}_h1'

        try:
            candles_data = binance_data.fetch_candles(ticker, "1h", limit=10)
        except Exception as e:
            logging.error(str(e))
            continue
        else:
            # candles_data = data_handler(response)
            store_in_db(candles_data, current_pair, -1, False)

            # QUERY db to get h4 d1 w1 and m1 data
            # then store in separate tables using store_in_db function
            tf_query_manager(current_pair)

            # Query for H1 alerts only and send emails
            query_task = asyncio.create_task(alert_query_manager(candles_data, instrument=ticker, timeframe=constants.H1))
            query_async_tasks.append(query_task)

        # Query for other timeframe alerts and send emails also
        # TODO for other timeframe, check if time is right before querying the other timeframe
        if measured_time(now, constants.H4) == constants.H4:
            query_task = asyncio.create_task(alert_query_manager(pd.DataFrame(), instrument=ticker, timeframe=constants.H4))
            query_async_tasks.append(query_task)
        if measured_time(now, constants.D1) == constants.D1:
            query_task = asyncio.create_task(alert_query_manager(pd.DataFrame(), instrument=ticker, timeframe=constants.D1))
            query_async_tasks.append(query_task)
        if measured_time(now, constants.W1) == constants.W1:  
            query_task = asyncio.create_task(alert_query_manager(pd.DataFrame(), instrument=ticker, timeframe=constants.W1))
            query_async_tasks.append(query_task)
        if measured_time(now, constants.M1) == constants.M1:
            query_task = asyncio.create_task(alert_query_manager(pd.DataFrame(), instrument=ticker, timeframe=constants.M1))
            query_async_tasks.append(query_task)

        # print(f"=========End data_colleciton for {ticker}==================")
    await asyncio.gather(*query_async_tasks)

if __name__ == '__main__':
    # Get the script's absolute path
    script_dir = os.path.dirname(os.path.abspath(__file__))

    logging.basicConfig(
    level = logging.INFO,
    filemode = 'a',
    filename = os.path.join(script_dir, 'logs/crypto_log.log'),
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    force = True
    )

    asyncio.run(crypto_data_service())

exit()
