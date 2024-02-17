#!/usr/bin/env python3
"""connect and extract price data form yf
"""
import logging
import os
import yfinance as yf
import pandas as pd
import constants
import asyncio
from datetime import datetime
from db_storage_service import store_in_db
from alert_query_service import alert_query_manager
from more_data import tf_query_manager, measured_time


async def get_yf_data():

    data = pd.DataFrame()
    query_async_tasks = []
    now = datetime.now()
    # try:
    #     data = yf.download(tickers=constants.tickers, period='1d', interval='60m') # , session=session)
    # except Exception as e:
    #     print('failed collecting data: {}'.format(e))


    # print(data['Open'][constants.tickers[0]])
    # print(len(data))

    for item in constants.YF_TICKERS:

        data = await asyncio.to_thread(yf.download, tickers=item, period='1d', interval='60m' )

        # print(data)

        # price_data = pd.DataFrame(
        #     {constants.open: data[constants.open][item],
        #     constants.high: data[constants.high][item],
        #     constants.low: data[constants.low][item],
        #     constants.close: data[constants.close][item],
        #     })

        # print(len(price_data))
        if not any(data) or data.empty:
            logging.error('No data received for {}'.format(item))
            continue

        current_pair = f'{item[:-2]}_h1'

        store_in_db(data, pair=current_pair)

        # QUERY db to get h4 d1 w1 and m1 data
        # then store in separate tables using store_in_db function
        tf_query_manager(current_pair)

        # Query for H1 alerts only and send emails
        query_task = asyncio.create_task(alert_query_manager(data, instrument=item[:-2], timeframe=constants.H1))
        query_async_tasks.append(query_task)

        # Query for other timeframe alerts and send emails also
        # TODO for other timeframe, check if time is right before querying the other timeframe
        if measured_time(now) == constants.H4:
            query_task = asyncio.create_task(alert_query_manager(pd.DataFrame(), instrument=item[:-2], timeframe=constants.H4))
            query_async_tasks.append(query_task)
        if measured_time(now) == constants.D1:
            query_task = asyncio.create_task(alert_query_manager(pd.DataFrame(), instrument=item[:-2], timeframe=constants.D1))
            query_async_tasks.append(query_task)
        if measured_time(now) == constants.W1:  
            query_task = asyncio.create_task(alert_query_manager(pd.DataFrame(), instrument=item[:-2], timeframe=constants.W1))
            query_async_tasks.append(query_task)
        if measured_time(now) == constants.M1:  
            query_task = asyncio.create_task(alert_query_manager(pd.DataFrame(), instrument=item[:-2], timeframe=constants.M1))
            query_async_tasks.append(query_task)

        logging.info(f"+++++++done with ticker {item}=======")

    await asyncio.gather(*query_async_tasks)


if __name__ == '__main__':

    # Exit if weekend
    week_num = datetime.today().weekday()
    if week_num > 4:
        exit()

    # Get the script's absolute path
    script_dir = os.path.dirname(os.path.abspath(__file__))

    logging.basicConfig(
    level = logging.INFO,
    filemode = 'a',
    filename = os.path.join(script_dir, 'logs/YF_log.log'),
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    force = True
    )

    asyncio.run(get_yf_data())

exit()