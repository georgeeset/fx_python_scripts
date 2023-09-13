'''
connect and extract price data form yf
'''
import requests_cache
import yfinance as yf
import pandas as pd
# import requests_cache
from requests import Session
from requests_cache import CacheMixin, SQLiteCache
from requests_ratelimiter import LimiterMixin, MemoryQueueBucket
from pyrate_limiter import Duration, RequestRate, Limiter
# import pymysql
import constants
from datetime import datetime, timedelta
from db_storage_service import store_in_db
from alert_query_service import alert_query_manager


# enable debug mode
# yf.enable_debug_mode()

# get timezone at catch
yf.set_tz_cache_location("yfinance_timezone.catch")


# class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
#     pass

def get_yf_data():
    # # No caching for now all data needed to run
    # session = requests_cache.CachedSession('yfinance.cache')
    # session.headers['User-agent'] = 'user-program/1.0'


    # # Dont need sessions since the script will be run once every hour
    # session = CachedLimiterSession(
    # limiter=Limiter(RequestRate(2, Duration.SECOND*5)),  # max 2 requests per 5 seconds
    # bucket_class=MemoryQueueBucket,
    # backend=SQLiteCache("yfinance.cache"),
    # expire_after=datetime.now() - timedelta(minutes=60)
    # )

    data = pd.DataFrame()
    try:
        data = yf.download(tickers=constants.tickers, period='1d', interval='60m') # , session=session)
    except Exception as e:
        print('failed collecting data: {}'.format(e))
    data_dict={}

    # print(data['Open'][constants.tickers[0]])
    # print(len(data))

    for item in constants.tickers:
        price_data = pd.DataFrame(
            {constants.open: data[constants.open][item],
            constants.high: data[constants.high][item],
            constants.low: data[constants.low][item],
            constants.close: data[constants.close][item],
            })

        # print(len(price_data))
        if len(price_data) == 0:
            print('No data received for {}'.format(item))
            continue
        data_dict[item] = price_data

    for key, value in data_dict.items():
        # print(constants.tickers[i])
        # print(type(data_list[i].iloc[-1]))
        print('====================={}================'.format(key))
        # print(value)
        store_in_db(value, pair=f'{key[:-2]}_h1', store_rows=-2)
        alert_query_manager(value, instrument=key[:-2]) # remove the _h1

    # print(len(data_dict))

if __name__ == '__main__':
    get_yf_data()

exit()