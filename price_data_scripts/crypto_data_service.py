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
from db_storage_service import store_in_db
from alert_query_service import alert_query_manager
from more_data import tf_query_manager, measured_time


def data_handler(payload: list) -> pd.DataFrame:
    """
    Clean up payload message and return ohlcv dataframe
    args:
        payload: list of raw data received from server
    return: pandas dataframed cleaned up for processing
    """
    price_data = pd.DataFrame(payload, columns=constants.KLINE_COLUMN_NAMES)
    price_data[constants.DATETIME] = pd.to_datetime(
        price_data['close_time'], unit='ms', utc=False
        ).round('1s')
    
    price_data.drop(['open_time','close_time','qav','num_trades',
                     'taker_base_vol','taker_quote_vol', 'ignore'
                     ],axis=1,inplace=True)
    price_data.set_index(constants.DATETIME,inplace=True)
    # due to deriv api hourly agregation, the last row is not a complete hour.
    if price_data.index[-1].hour == datetime.now().hour:
        # print(price_data.index[-1])
        # print("hour is same as current hour")
        price_data.drop(price_data.index[-1], axis=0, inplace=True)
    return price_data

async def crypto_data_service():
    """ extract crypto prices and query alerts
    send alerts to users based on request
    """
    my_client = Spot()
    query_async_tasks = []
    now = datetime.now()

    for ticker in constants.CRYPTO_TICKERS:
        response = my_client.klines(ticker, "1h", limit=10)
        # my_client.klines("ETHUSDT", "1h", limit=10)
        # my_client.exchange_info()
        # print(response)
        if response is None:
            logging.error("unable to get data for ticker {}".format(ticker))

        current_pair = f'{ticker}_h1'
        candles_data = data_handler(response)
        store_in_db(candles_data, current_pair, -1, False)

        # QUERY db to get h4 d1 w1 and m1 data
        # then store in separate tables using store_in_db function
        tf_query_manager(current_pair)


        # Query for H1 alerts only and send emails
        query_task = asyncio.create_task(alert_query_manager(candles_data, instrument=ticker, timeframe=constants.H1))
        query_async_tasks.append(query_task)

        # Query for other timeframe alerts and send emails also
        # TODO for other timeframe, check if time is right before querying the other timeframe
        if measured_time(now) == constants.H4:
            query_task = asyncio.create_task(alert_query_manager(pd.DataFrame(), instrument=value[constants.TABLE], timeframe=constants.H4))
            query_async_tasks.append(query_task)
        if measured_time(now) == constants.D1:
            query_task = asyncio.create_task(alert_query_manager(pd.DataFrame(), instrument=value[constants.TABLE], timeframe=constants.D1))
            query_async_tasks.append(query_task)
        if measured_time(now) == constants.W1:  
            query_task = asyncio.create_task(alert_query_manager(pd.DataFrame(), instrument=value[constants.TABLE], timeframe=constants.W1))
            query_async_tasks.append(query_task)
        if measured_time(now) == constants.M1:  
            query_task = asyncio.create_task(alert_query_manager(pd.DataFrame(), instrument=value[constants.TABLE], timeframe=constants.M1))
            query_async_tasks.append(query_task)

        print(f"=========End data_colleciton for {ticker}==================")
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
