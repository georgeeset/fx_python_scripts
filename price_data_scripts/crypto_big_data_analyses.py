"""
module used to download daily data from their api and store in database,
analize the data and store key support and resistance levels in database.
recommended to run every 10-15 days
"""
import logging
import constants
import pandas as pd
import os

from db_storage_service import MysqlOperations
from data_source.sr_collector import SRCollector
from data_source.binance import BinanceData


def request_big_data() -> pd.DataFrame:
    """
    Get data from cloud to database.
    2 years daily data or 1 month daily data
    """
    interval = '1d'
    period = None
    my_scan_window = 12 # sr scan window for analyses

    my_db = MysqlOperations()
    my_db.connect()
    sr_collector = SRCollector(scan_window=my_scan_window)
    data_source = BinanceData()

    for pair in constants.CRYPTO_TICKERS:

        big_pair = pair+'_big' # format text to suit table format
        candles = 0
        response = pd.DataFrame()   # empty dataframe
        if not my_db.table_exists(big_pair):
            logging.warning(f"table {big_pair} is new table")
            candles = 550
        else:
            candles = 20

        try:
            response = data_source.fetch_candles(pair, '1d', candles )
        except Exception as e:
            logging.error(f"Failed to collect data {pair}", e)

        if response.empty:
            logging.error("Failed to fetch big data {}".format(pair))
            continue

        # print(response.head(10))
        # print(response.tail(10))

        try:
            my_db.store_data(response, big_pair)
        except Exception as ex:
            logging.error(f"{pair} {ex}")
            continue

        if len(response) > my_scan_window:
            sr_df = sr_collector.find_sr(response)
        else:
            data = my_db.get_recent_price(big_pair, round(my_scan_window + (my_scan_window/2)))
            sr_df = sr_collector.find_sr(data)

        my_db.store_sr(sr_df, big_pair)   # add data received to database

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