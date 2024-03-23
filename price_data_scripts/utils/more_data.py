"""
module is to compile more data such as h4 d1, w1
and m1 data to be store d in separate table
"""

import calendar
import pandas as pd
import pymysql

from price_data_scripts.utils.trading_time import fx_week_start_end, is_last_daty_of_month
from . import  constants
import os
import logging
from datetime import datetime

from .db_storage_service import MysqlOperations

def measure_time(now_datetime:datetime, expected:str) -> str | None:
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

def fx_measure_time(now_datetime:datetime, expected:str) -> str | None:
    """
        checks the given time if it is right for next candle stick to start
        args:
            now_datetime: datetime to be checked
            expected: expected result to to avoid returning only first correct value
        return: String expected or none
    """
    # Allow h4 operations at last hour of trading week (fri, 8pm)
    if (expected == constants.H4 and (now_datetime.hour % 4 == 0)) or (expected == constants.H4 and fx_week_start_end(now_datetime) == 0): # 4 hourly
        # dont allow h4 operation at first hour of trading week (Mon, 12am)
        if fx_week_start_end(now_datetime) != 1:
            return expected
    
    # Allow D1 operations at last hour of trading week (fri, 8pm)
    if (expected == constants.D1 and (now_datetime.hour == 0)) or (expected == constants.D1 and fx_week_start_end(now_datetime) == 0): # daily
        if fx_week_start_end(now_datetime) != 1:
            return expected

     # Allow W1 operations at last hour of trading week (fri, 8pm)
    if expected == constants.W1 and fx_week_start_end == 0: # weekly
        # a week in forex is 5 days (monday to friday)
        return expected

    # allow M1 if it is first day of new month and time is midnight
    if expected == constants.M1 and (now_datetime.day == 1) and (now_datetime.hour == 0): # monthly
        return expected

    # allow M1 if friday is last day of the month
    if expected == constants.M1 and is_last_daty_of_month(now_datetime) and fx_week_start_end(now_datetime) == 0:
        return expected
    
    # allow M1 if Monday is the first week day of the month
    if expected == constants.M1 and (now_datetime.day <= 2) and (now_datetime.weekday == 0):
        return expected

    return None

def tf_query_manager(source_table:str):
    """
        query price data form hourly data and compile higher timeframe.
        args:
            source_table: table name for the database table
    """

    now_datetime = datetime.now()
   
    if measure_time(now_datetime, constants.H4) == constants.H4: # 4 hourly
        upadte_table(source_table, source_table[:-2] + constants.H4, number=4, period=constants.HOUR)
        logging.info("H4 row added")
        # print(target_time.strftime("%Y-%m-%d %H:%M:%S"))

    if measure_time(now_datetime, constants.D1) == constants.D1: # daily
        upadte_table(source_table, source_table[:-2] + constants.D1, number=1, period=constants.DAY)
        logging.info("D1 row added")

    if measure_time(now_datetime, constants.W1) == constants.W1: # weekly
        upadte_table(source_table, source_table[:-2] + constants.W1, number=7, period=constants.DAY)
        logging.info("W1 row added")

    if measure_time(now_datetime, constants.M1) == constants.M1: # monthly
        # subtract one month from current date
        upadte_table(source_table, source_table[:-2] + constants.M1, number=1, period=constants.MONTH)
        logging.info("M1 row added")

def fx_tf_query_manager(source_table:str) -> None:
    """
        query price data form hourly data and compile higher timeframe.
        with focus on forex data, taking weekneds and market open/close
        time into consideration

        args:
            source_table: table name for the database table
    """

    now_datetime = datetime.now()
   
    if fx_measure_time(now_datetime, constants.H4) == constants.H4: # 4 hourly
        upadte_table(source_table, source_table[:-2] + constants.H4, number=4, period=constants.HOUR)
        logging.info("H4 row added")

    if fx_measure_time(now_datetime, constants.D1) == constants.D1: # daily
        if now_datetime.day == 4: # friday doesn't have 24hrs
            upadte_table(source_table, source_table[:-2] + constants.D1, number=21, period=constants.HOUR)
        else:
            upadte_table(source_table, source_table[:-2] + constants.D1, number=1, period=constants.DAY)
            logging.info("D1 row added")

    if fx_measure_time(now_datetime, constants.W1) == constants.W1: # weekly forex = 5 days
        upadte_table(source_table, source_table[:-2] + constants.W1, number=5, period=constants.DAY)
        logging.info("W1 row added")

    if fx_measure_time(now_datetime, constants.M1) == constants.M1: # monthly
        # subtract one month from current date
        upadte_table(source_table, source_table[:-2] + constants.M1, number=1, period=constants.MONTH)
        logging.info("M1 row added")

def upadte_table(source_table: str, new_table: str, number:int, period:str ):
    """
        query hourly data table amd make a new table from it

        args:
            source_table: table name containing source of data
            new_table: name of destination table after compiling new data
            number: number of candle period
            period: DAY, MONTH, HOUR
    """

    my_sql_operations = MysqlOperations()
    
    # Connect to the database
    connection = pymysql.connect(
        host=os.environ.get('STORAGE_MYSQL_HOST'),
        user=os.environ.get('STORAGE_MYSQL_USER'),
        password=os.environ.get('STORAGE_MYSQL_PASSWORD') or "",
        db=os.environ.get('STORAGE_MYSQL_DB')
    )

    cursor = connection.cursor()

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
            now = datetime.now()
            month:int = now.month - 1 # previous month
            year = now.year
            num_days = calendar.monthrange(year, month)[1]
            if len(df_result) < (number * 24 * num_days):
                show_error = True
        case _:
            logging.info(f"everything complete for {period}: table {source_table}")
    
    if show_error:
        logging.warning(f"required data length for {period} is not complete: {len(df_result)} {source_table}")
    else:
        logging.info(f"everything complete for {period}: table {source_table}")

    if len(df_result) == 0:
        logging.error("no data found on database. for {}".format(new_table))
        return

    open = df_result.iloc[0][constants.OPEN]
    high = df_result[constants.HIGH].max()
    low = df_result[constants.LOW].min()
    close = df_result.iloc[-1][constants.CLOSE]
    close_datetime = datetime.now().replace(microsecond=0, second=0, minute=0)

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
