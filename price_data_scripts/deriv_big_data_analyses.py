"""
module used to download daily data from their api and store in database,
analize the data and store key support and resistance levels in database.
recommended to run every 10-15 days
"""
import asyncio
import logging
import constants
import pandas as pd
import os
import sys

from datetime import datetime, timedelta
from db_storage_service import MysqlOperations
from data_source.sr_collector import SRCollector
from data_source.deriv import DerivManager


async def request_big_data() -> pd.DataFrame:
    """
    Get data from cloud to database.
    2 years daily data or 1 month daily data
    """
    interval = 86400
    period = None
    my_scan_window = 12 # sr scan window for analyses

    my_db = MysqlOperations()
    sr_collector = SRCollector(scan_window=my_scan_window)
    data_source = DerivManager()
    await data_source.connect()

    now = datetime.now()
    epoch_time = int(now.timestamp())


    for pair in constants.DERIV_TICKERS:

        tbl_name = pair[constants.TABLE]+'_'+constants.D1 # table name
        big_id= pair[constants.ID]   # id for fetching data from api
        candles = 0
        response = pd.DataFrame()   # empty dataframe
        if not my_db.table_exists(tbl_name) :
            logging.warning(f"table {tbl_name} is new table")
            candles = 550
        else:
            candles = my_scan_window

        print(f'getting data for {tbl_name}')
        try:
            response = await data_source.fetch_candles(pair=big_id, frame=interval,
                                                 size = candles, end_time=epoch_time
                                                 )
        except Exception as e:
            logging.error(f"Failed to collect data {tbl_name}: {e}")

        if response.empty:
            logging.error("Failed to fetch big data {}".format(tbl_name))
            continue

        try:
            my_db.store_data(response, tbl_name)
        except Exception as ex:
            logging.error(f"{tbl_name} {ex}")
            continue

        print(f'finding sr points for {tbl_name}')
        if len(response) > my_scan_window:
            sr_df = sr_collector.find_sr(response)
        else:
            data = my_db.get_recent_price(tbl_name, round(my_scan_window + (my_scan_window/2)))
            sr_df = sr_collector.find_sr(data)

        if not sr_df.empty:
            my_db.store_sr(sr_df, pair[constants.TABLE])   # add data received to database
        else:
            logging.info(f"No support/Resistance found: {tbl_name}")
            # print(f"nothing found on support/resistance: {big_pair}")

        # delete old data from support/resistance history
        my_db.delete_old_data(table_name=pair[constants.TABLE]+'_sr', years=2)

    await data_source.disconnect()
    my_db.disconnect()


if __name__ == "__main__":

    # Get the script's absolute path
    script_dir = os.path.dirname(os.path.abspath(__file__))

    logging.basicConfig(
    level = logging.INFO,
    filemode = 'a',
    filename = os.path.join(script_dir, 'logs/big_deriv.log'),
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    force = True
    )

    # for arg in sys.argv:
    #     print(arg)

    asyncio.run(request_big_data())

exit()
