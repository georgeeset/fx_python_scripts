"""
collects data form alpha vantage api
"""
import os
import constants
import time
import pandas as pd
from alpha_vantage.timeseries import TimeSeries

class AlphaVantage:
    """
    collect information form api
    """
    __api_limit = 5

    def __init__(self):
        key = os.environ.get("ALPHA_VANTAGE_KEY")
        self.ts = TimeSeries(key=key, output_format='pandas', indexing_type='date')
        self.__api_call_count = 1
        self.__start_time = time.time()
        

    def fx_intraday(self, symbol)-> pd.DataFrame:
        if(self.__api_call_count >= self.__api_limit):
            self.__wait_api()
        try:
            data = self.ts.get_intraday(symbol=symbol, interval='1min', outputsize='all' if all else 'compact')[0]
        except Exception as ex:
            raise ValueError("data download railed: ", ex)
        if not data.any:
            raise ValueError("Got nothing from API")
        
        data.columns = [constants.OPEN,constants.HIGH,constants.LOW,constants.CLOSE,constants.VOLUME]
        data = data.iloc[::-1]  # sort in reverse order
        self.__api_call_count += 1
        return data

    def fx_daily(self, symbol:str, all:bool=False) -> pd.DataFrame:
        """
        download daily candlestick from api
        """
        if(self.__api_call_count >= self.__api_limit):
            self.__wait_api()
        
        try:
            data = self.ts.get_daily(symbol=symbol, outputsize='full' if all else 'compact')[0]
        except Exception as ex:
            raise ValueError("data download railed: ", ex)
        if not data.any:
            raise ValueError("Got nothing from API")
            
        data.columns = [constants.OPEN,constants.HIGH,constants.LOW,constants.CLOSE,constants.VOLUME]
        data = data.iloc[::-1]  # sort in reverse order
        self.__api_call_count += 1
        return data
    
    def __wait_api(self):
        self.__api_call_count = 0
        print("waiting for nex batch of 5 per minute")
        time.sleep(60 - ((time.time() - self.__start_time) % 60.0))
