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
from more_data import tf_query_manager


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
    """
        Connect to deriv socketio api, download data
        store in database, query for user alert set,
        send email to users whose alerts are triggered
    """
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

    #connect to derif api socket
    api = DerivAPI(app_id=api_id)

    query_async_tasks = []

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
            current_pair = f'{value[constants.TABLE]}_h1'

            store_in_db(data=candles_data,
                        pair=current_pair,
                        store_rows=-1,
                        )
            
            # QUERY db to get h4 d1 w1 and m1 data
            # then store in separate tables using store_in_db function
            tf_query_manager(current_pair)
            
            #first rename the df column to help enable simless dataformat
            # candles_data.rename({'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close'}, axis=1, inplace=True)
            query_task = asyncio.create_task(alert_query_manager(candles_data, instrument=value[constants.TABLE]))
            query_async_tasks.append(query_task)

        logging.info(f"=========End Query for {value.get('table')}==================")

    await asyncio.gather(*query_async_tasks)

    # disconnect when done
    await api.disconnect()

async def task_function() -> None:
    """
    this functio is basically to manage the connection attempt function
    it does not have timeout exception so I had to make a asymcio task
    to manage the process and cancle it when it gets stuck due to network
    faulure or server issues.
    Note: it is hardcoded to terminate in 100 seconds which is sufficient for now
    """

    task = asyncio.create_task(connect_attempt())

    try:
        await asyncio.wait_for(task, timeout=100)
    except asyncio.TimeoutError:
        logging.error("Task timed out!")
        task.cancel()  # Attempt to cancel if timed out
        
    else:
        # Task completed successfully (can do cleanup here)
        pass

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

    asyncio.run(task_function())

exit()
