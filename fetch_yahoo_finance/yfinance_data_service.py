'''
connect and extract price data form yf
'''
import logging
import os
import yfinance as yf
import pandas as pd
# import requests_cache
# import pymysql
import constants
import asyncio
from db_storage_service import store_in_db
from alert_query_service import alert_query_manager


async def get_yf_data():

    data = pd.DataFrame()
    # try:
    #     data = yf.download(tickers=constants.tickers, period='1d', interval='60m') # , session=session)
    # except Exception as e:
    #     print('failed collecting data: {}'.format(e))


    # print(data['Open'][constants.tickers[0]])
    # print(len(data))

    for item in constants.tickers:

        data = await asyncio.to_thread(yf.download, tickers=item, period='1d', interval='60m' )

        # print(data)

        # price_data = pd.DataFrame(
        #     {constants.open: data[constants.open][item],
        #     constants.high: data[constants.high][item],
        #     constants.low: data[constants.low][item],
        #     constants.close: data[constants.close][item],
        #     })



        # print(len(price_data))
        if not any(data):
            print('No data received for {}'.format(item))
            continue

        store_in_db(data, pair=f'{item[:-2]}_h1')

        # remove the -X1 from item
        asyncio.create_task(alert_query_manager(data, instrument=item[:-2]))

        logging.info(f"+++++++done with ticker {item}=======")

    # for key, value in data_dict.items():
    #     # print(constants.tickers[i])
    #     # print(type(data_list[i].iloc[-1]))
    #     print('====================={}================'.format(key))
    #     # print(value)
    #     store_in_db(value, pair=f'{key[:-2]}_h1', store_rows=-2)
    #     alert_query_manager(value, instrument=key[:-2]) # remove the _h1

    # print(len(data_dict))

if __name__ == '__main__':
    # Get the script's absolute path
    script_dir = os.path.dirname(os.path.abspath(__file__))

    logging.basicConfig(
    level = logging.WARNING,
    filemode = 'a',
    filename = os.path.join(script_dir, 'YF_log.log'),
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    force = True
    )

    asyncio.run(get_yf_data())

exit()