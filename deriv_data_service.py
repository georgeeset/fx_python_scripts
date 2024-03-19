#!/usr/bin/env python3
"""Module used to fetch price from deriv,
update database and send alerts
"""
import asyncio
from datetime import datetime, timedelta
from price_data_scripts.utils import constants
import logging
import os
import pandas as pd
from price_data_scripts.utils.db_storage_service import MysqlOperations
from price_data_scripts.utils.alert_query_service import alert_query_manager
from price_data_scripts.utils.more_data import tf_query_manager, measure_time
from price_data_scripts.data_source.deriv import DerivManager

# print(os.getcwd())  # Should output the project root path

async def connect_attempt() -> None:
    """
        Connect to deriv socketio api, download data
        store in database, query for user alert set,
        send email to users whose alerts are triggered
    """
    # Define your API key
    # api_key = os.environ.get('DERIV_API_KEY')
    api_id = 1089
    now = datetime.now()
    epoch_time = int(now.timestamp())
    # print(epoch_time)

    my_sql_operations = MysqlOperations()

    chart_type = "candles"
    granularity = 3600 #seconds = 1 hour
    count = 10  # Number of hourly candles you want to retrieve

    #connect to derif api socket
    # api = DerivAPI(app_id=api_id)

    deriv_data = DerivManager()
    await deriv_data.connect()
    query_async_tasks = []

    # Make the API request to get candles data
    for value in constants.DERIV_TICKERS:

        logging.info(f"starting  data collection for {value.get('table')}")

        try:
            candles = await deriv_data.fetch_candles(pair = value[constants.ID],
                                                        frame = granularity,
                                                        size = count,
                                                        end_time =str(epoch_time)
                                                        )
        except Exception as e:
            logging.error(str(e))
            continue
        else:
            if not candles.empty:
                # candles_data = make_dataframe(candles)
                current_pair = f'{value[constants.TABLE]}_h1'

                my_sql_operations.store_data(data=candles.iloc[-4:],
                            pair=current_pair
                            )

                # QUERY db to get h4 d1 w1 and m1 data
                # then store in separate tables using store_in_db function
                # print(current_pair)
                tf_query_manager(current_pair)

                #first rename the df column to help enable simless dataformat
                # candles_data.rename({'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close'}, axis=1, inplace=True)
                query_task = asyncio.create_task(alert_query_manager(candles, instrument=value[constants.TABLE], timeframe=constants.H1))
                query_async_tasks.append(query_task)

                # TODO for other timeframe, check if time is right before querying the other timeframe
                if measure_time(now, constants.H4) == constants.H4:
                    query_task = asyncio.create_task(alert_query_manager(pd.DataFrame(), instrument=value[constants.TABLE], timeframe=constants.H4))
                    query_async_tasks.append(query_task)
                if measure_time(now, constants.D1) == constants.D1:
                    query_task = asyncio.create_task(alert_query_manager(pd.DataFrame(), instrument=value[constants.TABLE], timeframe=constants.D1))
                    query_async_tasks.append(query_task)
                if measure_time(now, constants.W1) == constants.W1:  
                    query_task = asyncio.create_task(alert_query_manager(pd.DataFrame(), instrument=value[constants.TABLE], timeframe=constants.W1))
                    query_async_tasks.append(query_task)
                if measure_time(now, constants.M1) == constants.M1:  
                    query_task = asyncio.create_task(alert_query_manager(pd.DataFrame(), instrument=value[constants.TABLE], timeframe=constants.M1))
                    query_async_tasks.append(query_task)

        logging.info(f"=========End Query for {value.get('table')}==================")

    await asyncio.gather(*query_async_tasks)

    # disconnect when done
    await deriv_data.disconnect()

async def task_function() -> None:
    """
    this function is basically to manage the connection attempt function
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
    format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',    
    datefmt='%Y-%m-%d %H:%M:%S',
    force = True
    )

    asyncio.run(task_function())

exit()
