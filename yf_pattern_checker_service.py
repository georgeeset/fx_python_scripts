
import asyncio
from price_data_scripts.utils.more_data import measured_time
from price_data_scripts.utils.pattern_detector import PatternDetector
import logging
import os
from price_data_scripts.utils.db_storage_service import MysqlOperations
from price_data_scripts.utils import constants
from price_data_scripts.utils.messenger import Messenger
import pandas as pd
from datetime import datetime
from price_data_scripts.utils.alert_composer import AlertComposer


async def check_pattern(timeframe:str='h1'):
    """
    organize candlestick pattern detection
    """
    candles:int = 4
    composer = AlertComposer()
    pattern_detector = PatternDetector()

    logging.info(f'checking pattern for {timeframe}')

    for item in constants.VANTAGE_FX_TICKERS:

        tbl_name = item+'_'+timeframe
        my_db = MysqlOperations()
        # grab data from db
        data = my_db.get_recent_price(tbl_name, candles)
        # print(data)
        pattern = {}
        try:
            pattern = pattern_detector.check_patterns(data, item)
        except Exception as e:
            logging.error(f"pattern detection failed > {tbl_name}: {e}")
            # print(f"error detecting pattern {e}")

        if not pattern:
            logging.info(f"no pattern seen: {tbl_name}")
            continue
        logging.info(f"pattern found {tbl_name}: {pattern}")

        mailing_list:pd.DataFrame = pattern_detector.compile_mailing_list(item, timeframe)

        if mailing_list.empty:
            logging.info('mailing list is empty')
            print('mailing list is empty')
            continue

        # print(mailing_list)
        try:
            await composer.compile_send_messages(mailing_list, timeframe, item, pattern)
            pattern_detector.update_message_count(mailing_list)
        except Exception as e:
            logging.error(f"Message sending failed {tbl_name}: {e}")

    pattern_detector.clean()
    logging.info(f"pattern check complte for {timeframe}")

async def time_base_checker():
    now_datetime = datetime.now()
    task_list = []
    
    checker = check_pattern()
    task_list.append(checker)

    if measured_time(now_datetime, constants.H4) == constants.H4: # 4 hourly
       checker = check_pattern(constants.H4)
       task_list.append(checker)

    if measured_time(now_datetime, constants.D1) == constants.D1: # daily
        checker = check_pattern(constants.D1)
        task_list.append(checker)

    if measured_time(now_datetime, constants.W1) == constants.W1: # weekly
        checker = check_pattern(constants.W1)
        task_list.append(checker)

    if measured_time(now_datetime, constants.M1) == constants.M1: # monthly
        checker = check_pattern(constants.M1)
        task_list.append(checker)


    await asyncio.gather(*task_list)


if __name__ == "__main__":

    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Exit if weekend 
    week_num = datetime.today().weekday()
    current_hour = datetime.now().hour
    if week_num > 4 and current_hour > 0:
        exit()

    # monday morning, 1AM
    if week_num == 0 and current_hour == 0: 
        print("wait for one more hour")
        exit()


    logging.basicConfig(
    level = logging.INFO,
    filemode = 'a',
    filename = os.path.join(script_dir, 'logs/pattern_yf.log'),
    format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',    
    datefmt='%Y-%m-%d %H:%M:%S',
    force = True
    )

    logging.info('pattern checking for yf')
    asyncio.run(time_base_checker())

exit()
