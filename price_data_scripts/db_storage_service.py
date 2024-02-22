"""receive process and store data from Deriv"""

import pandas as pd
import pymysql
import constants
import os
import logging


class MysqlOperations:

    def __init__(self):
        pass

    def connect(self) -> None:
        """
        connects to mysql database
        """
        # Connect to the database
        self.connection = pymysql.connect(
            host=os.environ.get('STORAGE_MYSQL_HOST'),
            user=os.environ.get('STORAGE_MYSQL_USER'),
            password=os.environ.get('STORAGE_MYSQL_PASSWORD'),
            db=os.environ.get('STORAGE_MYSQL_DB')
        )

        self.cursor = self.connection.cursor()

    def is_connected(self) -> bool:
        """
        Confirm status of connection
        """
        if self.connection:
            return True
        return False
    
    def disconnect(self):
        """
        close database connection
        """
        self.cursor.close()
        self.connection.close()
    
    def table_exists(self, table_name) -> bool:
        """
        check if a table exists in the database
        """
        try:
            self.cursor.execute("SHOW TABLES")
            tables = self.cursor.fetchall()

            exists = table_name in [row[0] for row in tables]

            return exists
        
        except pymysql.Error as e:
                raise ValueError("Error connecting to MySQL:", e)

    def __create_table(self, pair) -> None:
        """
        creates a database table for curency pair
        if it doesn't already exist

        args: 
            pair: currency pair or instrument
        
        throws:
            valueErrr if operation fails
        """
        # create data table if not exist
        create_query = f"""CREATE TABLE IF NOT EXISTS {pair} (
                {constants.DATETIME} DATETIME PRIMARY KEY,
                {constants.OPEN} FLOAT,
                {constants.HIGH} FLOAT,
                {constants.LOW} FLOAT,
                {constants.CLOSE} FLOAT,
                {constants.VOLUME} FLOAT
                );"""
        
        # Create a cursor object to execute the CREATE TABLE statement
        
        try:
            self.cursor.execute(create_query)
        except Exception as err:
            raise ValueError("Error while creating table {pair}=> {er}")

    def store_data(self, data:pd.DataFrame, pair:str) -> None:
        """
        receive map of currency prices data and store in database.
        with ohlcv data

        args:
            data: dataframe of price of the currency pair trim before sending
                all data in dataframe will be stored in db
            pair: currency pair or instrument eg EURUSD_h1
        returns: None
        """
        if not self.is_connected:
            raise ValueError("db is not connected")
        
        self.__create_table(pair)

       

        for item in data.index:

            add_query = f"""REPLACE INTO {pair} (
                {constants.DATETIME},{constants.OPEN},
                {constants.HIGH},{constants.LOW},
                {constants.CLOSE}, {constants.VOLUME})
                VALUES ('{item}', {data[constants.OPEN][item]},
                {data[constants.HIGH][item]},
                {data[constants.LOW][item]}, 
                {data[constants.CLOSE][item]},
                {data[constants.VOLUME][item]
                if constants.VOLUME in data.columns else 0});
                """
             
            try:
                self.cursor.execute(add_query)
                self.connection.commit()
            except Exception as e:
                raise ValueError(f'error loading file => {pair}: {e}')
    
    def delete_table(self, table_name:str) -> None:
        """ 
        delete a database table

        args:
            table_name: name of table to be emtied
        """
        queryX = f"""DROP TABLE {table_name} """

        try:
            self.cursor.execute(queryX),
        except Exception as e:
            raise ValueError(f'DELETING TABLE ERROR occured: ==> {e}')
