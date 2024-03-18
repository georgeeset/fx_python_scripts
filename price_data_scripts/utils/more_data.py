"""
module is to compile more data such as h4 d1, w1
and m1 data to be store d in separate table
"""

from calendar import calendar
import pandas as pd
import pymysql
from . import  constants
import os
import logging
from datetime import datetime, timedelta

from .db_storage_service import MysqlOperations

def monthdelta(date, delta):
    m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
    if not m: m = 12
    d = d = min(date.day, calendar.monthrange(y, m)[1])
    return date.replace(day=d,month=m, year=y)

def measured_time(now_datetime:datetime, expected:str) -> str:
    """
        checks the given time if it is right for next candle stick to start
        args:
            now_datetime: datetime to be checked
            expected: expected result to to avoid returning only first correct value
        return: String expected or none
    """

    if expected == constants.H4 and (now_datetime.hour % 4 == 0): # 4 hourly
        return expected
    if expected == constants.D1 and (now_datetime.hour == 0): # daily
        return expected
    if expected == constants.W1 and (now_datetime.weekday == 0): # weekly
        return expected
    if expected == constants.M1 and (now_datetime.day == 1) and (now_datetime.hour == 0): # monthly
        return expected
    return None


def tf_query_manager(source_table:str):
    """
        query price data form hourly data and compile higher timeframe.
        args:
            source_table: table name for the database table
    """

    now_datetime = datetime.now()


    target_time = None
   
    if measured_time(now_datetime, constants.H4) == constants.H4: # 4 hourly
        upadte_table(source_table, source_table[:-2] + constants.H4, number=4, period=constants.HOUR)
        logging.info("H4 row added")
        # print(target_time.strftime("%Y-%m-%d %H:%M:%S"))

    if measured_time(now_datetime, constants.D1) == constants.D1: # daily
        upadte_table(source_table, source_table[:-2] + constants.D1, number=1, period=constants.DAY)
        logging.info("D1 row added")

    if measured_time(now_datetime, constants.W1) == constants.W1: # weekly
        upadte_table(source_table, source_table[:-2] + constants.W1, number=7, period=constants.DAY)
        logging.info("W1 row added")

    if measured_time(now_datetime, constants.M1) == constants.M1: # monthly
        # subtract one month from current date
        upadte_table(source_table, source_table[:-2] + constants.M1, number=1, period=constants.MONTH)
        logging.info("M1 row added")

def upadte_table(source_table: str, new_table: str, number:int, period:str ):
    """
        query hourly data table amd make a new table from it
        args:
            source_table:
            new_table:
            target_time:
    """

    my_sql_operations = MysqlOperations()
    
    # Connect to the database
    connection = pymysql.connect(
        host=os.environ.get('STORAGE_MYSQL_HOST'),
        user=os.environ.get('STORAGE_MYSQL_USER'),
        password=os.environ.get('STORAGE_MYSQL_PASSWORD'),
        db=os.environ.get('STORAGE_MYSQL_DB')
    )

    cursor = connection.cursor()
    # type(target_time.strftime("%Y-%m-%d %H:%M:%S"))

    if not isinstance(source_table, str) or not isinstance(new_table, str):
        raise(TypeError, "source_table and new_table must be string")

    query_str = f"""
        SELECT {constants.DATETIME}, {constants.OPEN}, {constants.HIGH}, {constants.LOW}, {constants.CLOSE}
        FROM {source_table}
        WHERE {constants.DATETIME} >= DATE_SUB(NOW(), INTERVAL {number} {period})
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

    show_error = False
    # log worning if data is not complete:
    match period:
        case constants.HOUR:
            if len(df_result) < number:
                show_error = True
        case constants.DAY: # weekely and daily
            if len(df_result) < (number * 24):
                show_error = True
        case constants.MONTH:
            if len(df_result) < (number * )
    
    if show_error:
        logging.warning(f"required data length for {period} is not complete: {len(df_result)} {source_table}")

    # print(df_result)

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

    # for i in new_data.index:
    #     print (i)

    # print(type(new_data))
    my_sql_operations.store_data(data=new_data,
                pair=new_table
                )

if __name__ == "__main__":
    tf_query_manager("Jump_100_Index_h1") # testing only
