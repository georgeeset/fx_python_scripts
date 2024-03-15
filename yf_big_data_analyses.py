"""
module used to download daily data from their api and store in database,
analize the data and store key support and resistance levels in database.
recommended to run every 10-15 days
"""
from datetime import datetime, timedelta
import pandas as pd
import logging
import os
from price_data_scripts.utils import constants

from price_data_scripts.data_source.yf import fetch_yf
from price_data_scripts.utils.db_storage_service import MysqlOperations
from price_data_scripts.data_source.sr_collector import SRCollector
from price_data_scripts.data_source.alpha_vantage import AlphaVantage
from price_data_scripts.utils.pattern_detector import PatternDetector

def request_big_data() -> pd.DataFrame:
    """
    Get data from cloud to database.
    2 years daily data or 1 month daily data
    """
    my_scan_window = constants.SR_SCAN_WINDOW# sr scan window for analyses
    sr_history_limit = constants.SR_HISTORY_LIMIT

    my_db = MysqlOperations()
    sr_collector = SRCollector(scan_window=my_scan_window)
    fx = AlphaVantage()
    pattern_detector =PatternDetector()

    for pair in constants.VANTAGE_FX_TICKERS:

        big_pair = pair+'_'+constants.D1 # format text to suit table format
        all = False
        sr_table = pair+'_sr'

        response = pd.DataFrame()
        if not my_db.table_exists(big_pair) or not my_db.table_exists(sr_table):
            logging.warning(f"One or more required tables does not exist")
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
            data = my_db.get_recent_price(big_pair, 500)    #500 candles max for analyses
        else:
            data = my_db.get_recent_price(big_pair, round(my_scan_window + (my_scan_window/2)))
        
        sr_df = sr_collector.find_sr(data)

        if not sr_df.empty:
            my_db.store_sr(sr_df, pair)   # add data received to database
        else:
            logging.error(f"No support/Resistance found: {pair}")
            print(f"nothing found on support/resistance: {pair}")

        # #TODO move the below block to daily activity as it is needed there
        # try:
        #     pattern_detector.check_patterns(data, pair)
        # except Exception as e:
        #     logging.error(f"pattern detection failed: {e}")
        #     print(f"error detecting pattern {e}")
    
        # delete old data from support/resistance history
        my_db.delete_old_data(table_name=pair+'_sr', years=sr_history_limit)

    my_db.disconnect()

if __name__ == "__main__":

    # Get the script's absolute path
    script_dir = os.path.dirname(os.path.abspath(__file__))

    logging.basicConfig(
    level = logging.INFO,
    filemode = 'a',
    filename = os.path.join(script_dir, 'logs/big_YF_data.log'),
    format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',    
    datefmt='%Y-%m-%d %H:%M:%S',
    force = True
    )

    request_big_data()

exit()