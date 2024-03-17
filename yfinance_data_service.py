#!/usr/bin/env python3
"""connect and extract price data form yf
"""
import logging
import os
import pandas as pd
from price_data_scripts.utils import constants
import asyncio
from datetime import datetime
from price_data_scripts.utils.db_storage_service import MysqlOperations
from price_data_scripts.utils.alert_query_service import alert_query_manager
from price_data_scripts.utils.more_data import tf_query_manager, measured_time
from price_data_scripts.data_source.yf import fetch_yf


async def get_yf_data():

    
    query_async_tasks = []
    now = datetime.now()
    my_sql_operations = MysqlOperations()

    for item in constants.YF_TICKERS:
        data = fetch_yf(item, period='1d', interval='60m' )

        # print(len(price_data))
        if data.empty:
            logging.error(f"faild to download data for {item} - 60m")
            continue

        current_pair = f'{item[:-2]}_h1'

        my_sql_operations.store_data(data, pair=current_pair)

        # QUERY db to get h4 d1 w1 and m1 data
        # then store in separate tables using store_in_db function
        tf_query_manager(current_pair)

        # Query for H1 alerts only and send emails
        query_task = asyncio.create_task(alert_query_manager(data, instrument=item[:-2], timeframe=constants.H1))
        query_async_tasks.append(query_task)

        # Query for other timeframe alerts and send emails also
        # TODO for other timeframe, check if time is right before querying the other timeframe
        if measured_time(now, constants.H4) == constants.H4:
            query_task = asyncio.create_task(alert_query_manager(pd.DataFrame(), instrument=item[:-2], timeframe=constants.H4))
            query_async_tasks.append(query_task)
        if measured_time(now, constants.D1) == constants.D1:
            query_task = asyncio.create_task(alert_query_manager(pd.DataFrame(), instrument=item[:-2], timeframe=constants.D1))
            query_async_tasks.append(query_task)
        if measured_time(now, constants.W1) == constants.W1:  
            query_task = asyncio.create_task(alert_query_manager(pd.DataFrame(), instrument=item[:-2], timeframe=constants.W1))
            query_async_tasks.append(query_task)
        if measured_time(now, constants.M1) == constants.M1:  
            query_task = asyncio.create_task(alert_query_manager(pd.DataFrame(), instrument=item[:-2], timeframe=constants.M1))
            query_async_tasks.append(query_task)

        logging.info(f"+++++++done with ticker {item}=======")

    await asyncio.gather(*query_async_tasks)


if __name__ == '__main__':

    # Exit if weekend 
    week_num = datetime.today().weekday()
    current_hour = datetime.now().hour
    
    if week_num > 4:
        exit()

    # Get the script's absolute path
    script_dir = os.path.dirname(os.path.abspath(__file__))

    logging.basicConfig(
    level = logging.INFO,
    filemode = 'a',
    filename = os.path.join(script_dir, 'logs/YF_log.log'),
    format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',    
    datefmt='%Y-%m-%d %H:%M:%S',
    force = True
    )

    asyncio.run(get_yf_data())

exit()