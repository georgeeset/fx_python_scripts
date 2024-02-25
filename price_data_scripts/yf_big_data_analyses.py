"""
module used to download daily data from their api and store in database,
analize the data and store key support and resistance levels in database.
recommended to run every 10-15 days
"""
from datetime import datetime, timedelta
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
    my_scan_window = 12 # sr scan window for analyses

    my_db = MysqlOperations()
    sr_collector = SRCollector(scan_window=12)
    fx = AlphaVantage()

    for pair in constants.VANTAGE_FX_TICKERS:

        big_pair = pair+'_'+constants.D1 # format text to suit table format
        all = False
        response = pd.DataFrame()
        if not my_db.table_exists(big_pair):
            logging.warning(f"table {big_pair} is new table")
            all = True

        print(f'getting data for {big_pair}')
        try:
            response = fx.fx_daily(pair, all)
        except Exception as e:
            logging.error(f"data downloading failed {big_pair}: {e}")
            continue
        
        if response.empty:
            logging.error("Failed to fetch big data {}".format(pair))
            continue

        try:
            my_db.store_data(response, big_pair)
        except Exception as ex:
            logging.error(f"{pair} {ex}")
            continue

        print(f'finding sr points for {big_pair}')
        if all:
            sr_df = sr_collector.find_sr(response)
            print(len(response))
        else:
            data = my_db.get_recent_price(big_pair, round(my_scan_window + (my_scan_window/2)))
            print(data)
            sr_df = sr_collector.find_sr(data)

        if not sr_df.empty:
            my_db.store_sr(sr_df, pair)   # add data received to database
        else:
            logging.error(f"No support/Resistance found: {pair}")
            print(f"nothing found on support/resistance: {pair}")

        # delete old data from support/resistance history
        my_db.delete_old_data(table_name=pair+'_sr', years=2)

    my_db.disconnect()

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

exit()