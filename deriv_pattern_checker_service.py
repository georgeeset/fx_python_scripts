
import asyncio
from price_data_scripts.utils.pattern_detector import PatternDetector
import logging
import os
from price_data_scripts.utils.db_storage_service import MysqlOperations
from price_data_scripts.utils import constants
from price_data_scripts.utils.messenger import Messenger
import pandas as pd


async def check_pattern(timeframe:str='h1'):
    """
    organize candlestick pattern detection
    """
    candles:int = 4

    for item in constants.DERIV_TICKERS:

        tbl_name = item[constants.TABLE]+'_'+timeframe # table name
        pattern_detector = PatternDetector()
        my_db = MysqlOperations()
        # grab data from db
        data = my_db.get_recent_price(tbl_name, candles)

        try:
            pattern = pattern_detector.check_patterns(data, item[constants.TABLE])
        except Exception as e:
            logging.error(f"pattern detection failed: {e}")
            # print(f"error detecting pattern {e}")

        if not pattern:
            print("no pattern seen")
            continue
        
        print(tbl_name)
        print(pattern)
        mailing_list:pd.DataFrame = pattern_detector.compile_mailing_list(item[constants.TABLE], timeframe)

        if mailing_list.empty:
            print('mailing list is empty')
            continue

        print(mailing_list)

        await compile_send_messages(mailing_list, timeframe, item[constants.TABLE], pattern)
        pattern_detector.update_message_count(mailing_list)

        pattern_detector.close()

async def compile_send_messages(data:pd.DataFrame, timeframe:str, pair:str, pattern:dict) -> None:
    my_message = Messenger()

    # email_list = data.loc[data[constants.ALERT_TYPE] == constants.EMAIL][constants.ALERT_ID]

    # telegram_list = data.loc[data[constants.ALERT_TYPE] == constants.TELEGRAM][constants.ALERT_ID]

    # email_list = set(email_list)
    # telegram_list = set(telegram_list)
    pattern_list = str([item[4:] for item in pattern[constants.PATTERNS]])
    mail_async_task = []

    email_subject = f'PRICE PATTERN ALERT on {timeframe}'

    email_list = []
    telegram_list = []
    
    for receiver in data.itertuples():

        # prepare message to be sent
        msg = constants.PATTERN_ALERT_MESSAGE.format(
            patterns = pattern_list,
            c_pair = pair,
            recent_status = pattern[constants.RECENT_STATUS],
            last_used = pattern[constants.LASTUSED],
            alert_count = receiver[constants.ALERT_COUNT] + 1,
            used = pattern[constants.Frequency],
            note = receiver[constants.NOTE_COL]
        )

        print(msg)
        if receiver[constants.ALERT_TYPE] == constants.EMAIL:
            # simply avoid sending same message more than once. incase of duplicate alert set
            if receiver[constants.ALERT_ID] in email_list:
                continue
            email_list.add(receiver[constants.ALERT_ID])

            email_task = my_message.send_email_async(receiver[constants.ALERT_ID], email_subject, msg)
            mail_async_task.append(email_task)

        elif receiver[constants.ALERT_TYPE] == constants.TELEGRAM:
            # simply avoid sending same message more than once. incase of duplicate alert set
            if receiver[constants.CHAT_ID] in telegram_list:
                continue
            email_list.add(receiver[constants.ALERT_ID])

            telegram_task = my_message.send_telegram_async(email_subject+'\n\n'+msg, receiver[constants.CHAT_ID])
            mail_async_task.append(telegram_task)
        else:
            raise ValueError('wahala dey o: not email not telegram')
        
    
    result = await asyncio.gather(*mail_async_task)
    print('message sent', result)


if __name__ == "__main__":

    script_dir = os.path.dirname(os.path.abspath(__file__))

    logging.basicConfig(
    level = logging.INFO,
    filemode = 'a',
    filename = os.path.join(script_dir, 'logs/pattern_deriv.log'),
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    force = True
    )
    asyncio.run(check_pattern())

exit()
