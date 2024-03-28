"""
module used to download daily data from their api and store in database,
analize the data and store key support and resistance levels in database.
recommended to run every 10-15 days
"""
import logging
import price_data_scripts.utils.constants as constants
import pandas as pd
import os
import sys

from price_data_scripts.utils.db_storage_service import MysqlOperations
from price_data_scripts.data_source.sr_collector import SRCollector
from price_data_scripts.data_source.binance import BinanceData
from price_data_scripts.utils.pattern_detector import PatternDetector


def request_big_data(argv) -> None:
    """
    Get data from cloud to database.
    2 years daily data or 1 month daily data
    """
    interval = '1d'
    period = None
    my_scan_window = constants.SR_SCAN_WINDOW # sr scan window for analyses
    sr_history_limit = constants.SR_HISTORY_LIMIT

    my_db = MysqlOperations()
    sr_collector = SRCollector(scan_window=my_scan_window)
    data_source = BinanceData()

    for arg in argv:
        print(arg)

    for pair in constants.CRYPTO_TICKERS:

        d1_table = pair+'_'+constants.D1 # format text to suit table name
        sr_table = pair+'_sr' # formated to sr table name
        candles = 0
        response = pd.DataFrame()   # empty dataframe
        if not my_db.table_exists(d1_table) or not my_db.table_exists(sr_table):
            logging.warning(f"One or more required tables does not exist")
            candles = 550
        else:
            candles = my_scan_window

        print(f'getting data for {d1_table}')
        try:
            response = data_source.fetch_candles(pair, interval, candles )
        except Exception as e:
            logging.error(f"Failed to collect data {pair}: {e}")
            continue

        if response.empty:
            logging.error("Failed to fetch big data {}".format(pair))
            print('data download failed')
            continue

        try:
            my_db.store_data(response, d1_table)
        except Exception as ex:
            logging.error(f"{d1_table} {ex}")
            continue

        print(f'finding sr points for {d1_table}')
        if candles > my_scan_window:
            # sr_df = sr_collector.find_sr(response)
            data = my_db.get_recent_price(d1_table, candles)
        else:
            data = my_db.get_recent_price(d1_table, round(my_scan_window + (my_scan_window/2)))
        
        sr_df = sr_collector.find_sr(data)
            
        # add data received to database
        if not sr_df.empty:
            my_db.store_sr(sr_df, pair)
        else:
            logging.info(f"No support/Resistance found: {d1_table}")
            # print(f"nothing found on support/resistance: {big_pair}")

        # #TODO move the below block to daily activity as it is needed there
        # try:
        #     pattern_detector.check_patterns(data, pair)
        # except Exception as e:
        #     logging.error(f"pattern detection failed: {e}")
        #     print(f"error detecting pattern {e}")
        
        # delete old data from support/resistance history
        my_db.delete_old_data(table_name=sr_table, years=sr_history_limit)

    my_db.disconnect()

if __name__ == "__main__":

    # Get the script's absolute path
    script_dir = os.path.dirname(os.path.abspath(__file__))

    logging.basicConfig(
    level = logging.WARNING,
    filemode = 'a',
    filename = os.path.join(script_dir, 'logs/big_crypto.log'),
    format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',    
    datefmt='%Y-%m-%d %H:%M:%S',
    force = True
    )

    # for arg in sys.argv:
    #     print(arg)

    request_big_data(sys.argv)

exit()