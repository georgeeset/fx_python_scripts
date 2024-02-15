"""
module is to compile more data such as h4 d1, w1
and m1 data to be store d in separate table
"""

from calendar import calendar
import pandas as pd
import pymysql
import constants
import os
import logging
from datetime import datetime, timedelta

from db_storage_service import store_in_db

def monthdelta(date, delta):
    m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
    if not m: m = 12
    d = d = min(date.day, calendar.monthrange(y, m)[1])
    return date.replace(day=d,month=m, year=y)


def tf_query_manager(source_table:str):
    """
        query price data form hourly data and compile higher timeframe.
        args:
            source_table: table name for the database table
    """

    now_datetime = datetime.now()
    queryStr = None
    target_time = None
   
    if now_datetime.hour % 4 == 0: # 4 hourly
        window = timedelta(hours=4)
        target_time = now_datetime - window
        upadte_table(source_table, f"{source_table[:-2]}h4", target_time)
        logging.info("h4 row added")
        # print(target_time.strftime("%Y-%m-%d %H:%M:%S"))
        
    if now_datetime.hour == 0: # daily
        window = timedelta(days=1)
        target_time = now_datetime - window
        upadte_table(source_table, f"{source_table[:-2]}d1", target_time)
        logging.info("d1 row added")

    if now_datetime.weekday == 0: # weekly
        window = timedelta(weeks=1)
        target_time = now_datetime - window
        upadte_table(source_table, f"{source_table[:-2]}w1", target_time)
        logging.info("w1 row added")

    if now_datetime.day == 1: # monthly
        # subtract one month from current date
        target_ts = now_datetime - pd.DateOffset(months=1) 
        target_time = target_ts.to_pydatetime()
        upadte_table(source_table, f"{source_table[:-2]}m1", target_time)
        logging.info("m1 row added")
    
    if not target_time:
        logging.info("not yet time")

def upadte_table(source_table: str, new_table: str, target_time: datetime ):
    """
        query hourly data table amd make a new table from it
        args:
            source_table:
            new_table:
            target_time:
    """

     # Connect to the database
    connection = pymysql.connect(
        host=os.environ.get('STORAGE_MYSQL_HOST'),
        user=os.environ.get('STORAGE_MYSQL_USER'),
        password=os.environ.get('STORAGE_MYSQL_PASSWORD'),
        db=os.environ.get('STORAGE_MYSQL_DB')
    )

    cursor = connection.cursor()
    # type(target_time.strftime("%Y-%m-%d %H:%M:%S"))

    if not isinstance(target_time, datetime):
        raise(TypeError, "target_time must be datetime datatype")
    if not isinstance(source_table, str) or not isinstance(new_table, str):
        raise(TypeError, "source_table and new_table must be string")

    query_str = f"""
        SELECT {constants.DATETIME}, {constants.OPEN}, {constants.HIGH}, {constants.LOW}, {constants.CLOSE}
        FROM {source_table}
        WHERE {constants.DATETIME} >= '{target_time}'
        ORDER BY {constants.DATETIME} ASC;
        """
    cursor.execute(query_str)
    data = cursor.fetchall()

    # convert query response to pandas dataframe
    df_result = pd.DataFrame(data, columns=[
        constants.DATETIME,
        constants.OPEN,
        constants.HIGH,
        constants.LOW,
        constants.CLOSE]
        )
    
    cursor.close()

    print(df_result)

    if len(df_result) == 0:
        logging.error("no data found on database. for {}".format(new_table))
        return
    
    open = df_result.iloc[0][constants.OPEN]
    high = df_result[constants.HIGH].max()
    low = df_result[constants.LOW].min()
    close = df_result.iloc[-1][constants.CLOSE]
    close_datetime = df_result.iloc[-1][constants.DATETIME]

    # print(close_datetime)

    new_data = pd.DataFrame(data = {
        constants.DATETIME: [close_datetime],
        constants.OPEN: [open],
        constants.HIGH: [high],
        constants.LOW: [low],
        constants.CLOSE: [close],
        constants.VOLUME: [0],
        }
    )

    new_data.set_index(constants.DATETIME, inplace=True)

    for i in new_data.index:
        print (i)
    # print(type(new_data))
    store_in_db(data=new_data,
                pair=new_table
                )

if __name__ == "__main__":
    tf_query_manager("Jump_100_Index_h1") # testing only
