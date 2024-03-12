from price_data_scripts.utils import constants
from .messenger import Messenger
import pandas as pd
import asyncio

class AlertComposer:

    def __init__(self):
        pass

    async def compile_send_messages(self, data:pd.DataFrame, timeframe:str, pair:str, pattern:dict) -> None:
        my_message = Messenger()
        pattern_list = str([item[4:] for item in pattern[constants.PATTERNS]])
        mail_async_task = []

        email_subject = f'PRICE PATTERN ALERT on {timeframe}'

        email_list = []
        telegram_list = []
        # print(data)

        for index, receiver in data.iterrows() :
            
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

            # print(msg)
            if receiver[constants.ALERT_TYPE] == constants.EMAIL:
                # simply avoid sending same message more than once. incase of duplicate alert set
                if receiver[constants.ALERT_ID] in email_list:
                    continue
                email_list.append(receiver[constants.ALERT_ID])

                email_task = my_message.send_email_async(receiver[constants.ALERT_ID], email_subject, msg)
                mail_async_task.append(email_task)

            elif receiver[constants.ALERT_TYPE] == constants.TELEGRAM:
                # simply avoid sending same message more than once. incase of duplicate alert set
                if receiver[constants.CHAT_ID] in telegram_list:
                    continue
                email_list.append(receiver[constants.CHAT_ID])

                telegram_task = my_message.send_telegram_async(email_subject+'\n\n'+msg, receiver[constants.CHAT_ID])
                mail_async_task.append(telegram_task)
            else:
                raise ValueError('wahala dey o: not email not telegram')
            
        
        await asyncio.gather(*mail_async_task)