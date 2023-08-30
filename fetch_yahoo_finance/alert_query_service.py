"""
Check alert databasae for triggered alerts and contact user asap 
"""
import pandas as pd
import pymysql
import constants
import os
from datetime import datetime

def alert_query_manager(price_row:pd.DataFrame, instrument:str):
    """
    query alert db and get necessary data
    """
    pair_table = '{}_h1'.format(instrument)

    if not isinstance(price_row, pd.DataFrame):
        raise ValueError('Value must be a dataframe with OHLC daeta')
    
    print('test pair_output', instrument)
    print('open', price_row.Close[-1])

    # Connect to the database
    connection = pymysql.connect(
        host=os.environ.get('STORAGE_MYSQL_HOST'),
        user=os.environ.get('STORAGE_MYSQL_USER'),
        password=os.environ.get('STORAGE_MYSQL_PASSWORD'),
        db=os.environ.get('STORAGE_MYSQL_DB')
    )

    
    CONDITION_QUERY_SET = [
        f"""SELECT * FROM {constants.ALERTS_TABLE}
        WHERE {constants.TARGET_COL} < {price_row.Close[-1]}
        AND {constants.CURRENCY_PAIR_COL} = '{instrument}'
        AND {constants.EXPIRATION_COL} <= NOW()
        AND {constants.REPEAT_ALARM_COL} > {constants.ALERT_COUNT};
        """,
    ]

    for query in CONDITION_QUERY_SET:
        print(query)
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                response = cursor.fetchall()
                print(response)
                print(type(response))
                # for data in response:
                #     print(data[4]) # candle time determines when to send message
                #     get_alert_details()
                #     send_message(condition=data[2], email )
                #     update_alertcount_col(alert_id=data[0])

        except Exception as e:
            print(f'Query_failed for {instrument}: {e}')


def get_alert_details(alert_id:int):
    """ query user's alert_detail with the given alert_id"""
    pass