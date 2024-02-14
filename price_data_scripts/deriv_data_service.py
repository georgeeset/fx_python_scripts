#!/usr/bin/env python3
"""Module used to fetch price from deriv,
update database and send alerts
"""
from deriv_api import DerivAPI
import asyncio
from datetime import datetime, timedelta
import constants
import logging
import os
import pandas as pd
from db_storage_service import store_in_db
from alert_query_service import alert_query_manager


def make_dataframe(candles: map) -> pd.DataFrame:
    """ Convert map data to pandas Dataframe with
    all fields named with first later capitalized.
    e.g: Open Low...
    Args:
        candles: ohlc data from candlestick data
    """
    dict_data = {constants.DATETIME: [],
                            constants.OPEN: [],
                            constants.HIGH: [],
                            constants.LOW: [],
                            constants.CLOSE: []
                            }

    # Fill data into dataframe
    for candle in candles.get(constants.CANDLES):
        dict_data[constants.DATETIME].append(datetime.fromtimestamp(candle.get(constants.EPOCH)))
        dict_data[constants.OPEN].append(candle.get(constants.OPEN.lower()))
        dict_data[constants.HIGH].append(candle.get(constants.HIGH.lower()))
        dict_data[constants.LOW].append(candle.get(constants.LOW.lower()))
        dict_data[constants.CLOSE].append(candle.get(constants.CLOSE.lower()))
        # No volume

    candles_data = pd.DataFrame.from_dict(dict_data)
    candles_data.set_index(constants.DATETIME, inplace=True)
    # print(candles_data)
    return candles_data


async def connect_attempt() -> None:
    # Define your API key
    # api_key = os.environ.get('DERIV_API_KEY')
    api_id = '1089'
    now = datetime.now()
    epoch_time = int(now.timestamp())
    # print(epoch_time)

    # add timeout to terminate function when task gets stuck on connection
    timeout = timedelta(minutes=5)


    chart_type = "candles"
    granularity = 3600 #seconds = 1 hour
    count = 10  # Number of hourly candles you want to retrieve
    api = None
    task = asyncio.create_task(DerivAPI(app_id=api_id))
    #connect to derif api socket
    try:
        api = await asyncio.wait_for (task, timeout=timeout)
    except TimeoutError:
        task.cancel()   # Attempt to cancel if timed out
        return
    query_async_tasks = []
    print(type(api))

    # Make the API request to get candles data
    for value in constants.DERIV_TICKERS:
        
        logging.info(f"starting  data collection for {value.get('table')}")

        candles = await api.ticks_history(
            {'ticks_history': value[constants.ID], 'style': chart_type,
            'granularity': granularity, 'count': count,
            'end': str(epoch_time)
            })

        if candles.get(constants.CANDLES):
            
            candles_data = make_dataframe(candles)

            store_in_db(data=candles_data,
                        pair=f'{value[constants.TABLE]}_h1',
                        store_rows=-1,
                        )
            
            # TODO QUERY db to get h4 d1 w1 and m1 data
            # then store in separate tables using store_in_db function

            #first rename the df column to help enable simless dataformat
            # candles_data.rename({'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close'}, axis=1, inplace=True)
            query_task = asyncio.create_task(alert_query_manager(candles_data, instrument=value[constants.TABLE]))
            query_async_tasks.append(query_task)

        logging.info(f"=========End Query for {value.get('table')}==================")

    await asyncio.gather(*query_async_tasks)

    # disconnect when done
    api.disconnect()


if __name__  == "__main__":
    # Get the script's absolute path
    script_dir = os.path.dirname(os.path.abspath(__file__))

    logging.basicConfig(
    level = logging.INFO,
    filemode = 'a',
    filename = os.path.join(script_dir, 'logs/deriv_log.log'),
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    force = True
    )

    logging.warning("first attempt to run file")

    asyncio.run(connect_attempt())

exit()
