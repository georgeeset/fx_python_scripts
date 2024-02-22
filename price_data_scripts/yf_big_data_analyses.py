"""
module used to download daily data from their api and store in database,
analize the data and store key support and resistance levels in database.
recommended to run every 10-15 days
"""
import pandas as pd
import logging
import os
import constants
from data_source.yf import fetch_yf
from db_storage_service import MysqlOperations

def store_sr():
    """
    find key support and resistance and stor in database
    """
    

def request_big_data() -> pd.DataFrame:
    """
    Get data from cloud to database.
    2 years daily data or 1 month daily data
    """
    interval = '1d'
    period = None

    my_db = MysqlOperations()
    my_db.connect()

    for pair in constants.YF_TICKERS:

        big_pair = pair[:-2]+'_big' # format text to suit table format

        if my_db.table_exists(big_pair):
            logging.warning(f"table {big_pair} is new table")
            period = '2y'
        else:
            period = '1m'

        response = fetch_yf(pair, period, interval)
        if response.empty:
            logging.error("Failed to fetch big data {}".format(pair))
            continue

        print(response.head(10))
        print(response.tail(10))

        try:
            my_db.store_data(response, big_pair)
        except Exception as ex:
            logging.error(f"{pair} {ex}")

def update_data():
    """update data table for currency pairs"""
    
if __name__ == "__main__":

    # Get the script's absolute path
    script_dir = os.path.dirname(os.path.abspath(__file__))

    logging.basicConfig(
    level = logging.INFO,
    filemode = 'a',
    filename = os.path.join(script_dir, 'logs/big_YF_data.log'),
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    force = True
    )

    request_big_data()