"""
module used to download daily data from their api and store in database,
analize the data and store key support and resistance levels in database.
recommended to run every 10-15 days
"""
import pandas as pd
import logging
import os
from price_data_scripts import constants
from price_data_scripts.data_source.yf import fetch_yf

def request_big_data() -> pd.DataFrame:
    """
    Get data from cloud to database.
    only run for one time only
    """
    period = '2y'
    interval = '1d'

    for pair in constants.YF_TICKERS:
        response = fetch_yf(pair, period, interval)
        if not response.any():
            logging.error("Failed to fetch big data {}".format(pair))
            continue
        
    

if __name__ == "__main__":

    # Get the script's absolute path
    script_dir = os.path.dirname(os.path.abspath(__file__))

    logging.basicConfig(
    level = logging.INFO,
    filemode = 'a',
    filename = os.path.join(script_dir, 'price_data_scripts/logs/big_YF_data.log'),
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    force = True
    )