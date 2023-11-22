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


def data_handler(payload: list) -> pd.DataFrame:
    """
    Clean up payload message and return ohlcv dataframe
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

    for ticker in constants.CRYPTO_TICKERS:
        response = my_client.klines(ticker, "1h", limit=10)
        # my_client.klines("ETHUSDT", "1h", limit=10)
        # my_client.exchange_info()
        # print(response)
        if response is None:
            print("unable to get data for ticker {}".format(ticker))

        candles_data = data_handler(response)
        store_in_db(candles_data, f'{ticker}_h1', -1, False)

        query_task = asyncio.create_task(alert_query_manager(candles_data, instrument=ticker))
        query_async_tasks.append(query_task)

        print(f"=========End data_colleciton for {ticker}==================")
    await asyncio.gather(*query_async_tasks)


if __name__ == '__main__':
    # Get the script's absolute path
    script_dir = os.path.dirname(os.path.abspath(__file__))

    logging.basicConfig(
    level = logging.INFO,
    filemode = 'a',
    filename = os.path.join(script_dir, 'logs/cryto_log.log'),
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    force = True
    )

    asyncio.run(crypto_data_service())

exit()
