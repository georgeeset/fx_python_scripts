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
from data_source.sr_collector import SRCollector
from data_source.alpha_vantage import AlphaVantage

def request_big_data() -> pd.DataFrame:
    """
    Get data from cloud to database.
    2 years daily data or 1 month daily data
    """
    interval = '1d'
    period = None

    my_db = MysqlOperations()
    my_db.connect()
    sr_collector = SRCollector(scan_window=12)
    fx = AlphaVantage()

    for pair in constants.VANTAGE_FX_TICKERS:

        big_pair = pair[:-2]+'_big' # format text to suit table format
        all = False
        if not my_db.table_exists(big_pair):
            logging.warning(f"table {big_pair} is new table")
            all = True
        else:
            all = False

        response = fx.fx_daily(pair, all)
        if response.empty:
            logging.error("Failed to fetch big data {}".format(pair))
            continue

        print(response.head(10))
        print(response.tail(10))

        try:
            my_db.store_data(response, big_pair)
        except Exception as ex:
            logging.error(f"{pair} {ex}")

        sr_df = sr_collector.find_sr(response)
        my_db.store_sr(sr_df, pair+'_sr')   # add data received to database

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