"""receive process and store data from Deriv"""

import pandas as pd
import pymysql
import constants
import os
import logging

def store_in_db(data:pd.DataFrame, pair:str, store_rows:int = -1, clear_tables:bool = False) -> bool:
    """
    receive map of Deriv prices data and store in database.
    args:
        data: must be in this format -> {'pair': 'EURUSD', 'data': pandas dataframe:}
        store_rows: the number of rows to store. starting from the bottom.
                    the value must be nagative. e.g -2 ->[-2:]
    return: bool of update status success = True failed = False
    """
    # Connect to the database
    connection = pymysql.connect(
        host=os.environ.get('STORAGE_MYSQL_HOST'),
        user=os.environ.get('STORAGE_MYSQL_USER'),
        password=os.environ.get('STORAGE_MYSQL_PASSWORD'),
        db=os.environ.get('STORAGE_MYSQL_DB')
    )

    if not isinstance(data, pd.DataFrame):
        raise ValueError('data argument must be a dataframe')

    if not isinstance(store_rows, int) or store_rows > 0:
        raise ValueError('Store_rows arg must be negative number')

    if not isinstance(pair, str) or pair == None:
        raise ValueError('pair arg must be a String')

    if not isinstance(clear_tables, bool):
         raise ValueError('clear table arg must be boolean')

    # print('store data', f'{pair}-> {data.iloc[store_rows:]}')
    # Store the dataframe in MySQL
    trimed_data = data[store_rows:]
    # print(trimed_data)

    # print(constants.CLOSE.capitalize())

    # clear table if it is marked for deletion
    if clear_tables == True:
        queryX = f"""DROP TABLE {pair} """

        try:
            with connection.cursor() as cursor:
                    cursor.execute(queryX),
        except Exception as e:
         logging.error(f'DELETING TABLE ERROR occured: ==> {e}')

        logging.info('table deleted')

    query = f"""CREATE TABLE IF NOT EXISTS {pair} (
            {constants.DATETIME} DATETIME PRIMARY KEY,
            {constants.OPEN} FLOAT,
            {constants.HIGH} FLOAT,
            {constants.LOW} FLOAT,
            {constants.CLOSE} FLOAT,
            {constants.VOLUME} FLOAT
            );"""

    try:
        with connection.cursor() as cursor:
                cursor.execute(query),
    except Exception as e:
        logging.error('creating TABLE error has occured: ==', e)
        return False

    for item in trimed_data.index:
        # print(item)
        # print(trimed_data[constants.OPEN][item])
        # print(trimed_data.index[0])
        try:
            db_query = f"""REPLACE INTO {pair} (
                {constants.DATETIME},{constants.OPEN},
                {constants.HIGH},{constants.LOW},
                {constants.CLOSE})
                VALUES ('{item}', {trimed_data[constants.OPEN][item]},
                {trimed_data[constants.HIGH][item]}, 
                {trimed_data[constants.LOW][item]}, 
                {trimed_data[constants.CLOSE][item]});
                """
            with connection.cursor() as cursor:
                cursor.execute(db_query)
                connection.commit()
        except Exception as e:
             logging.error(f'error loading file => {pair}', e)

    connection.close()
