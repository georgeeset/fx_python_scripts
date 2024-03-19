"""
module for fetching yf data from cloud
"""
from datetime import timedelta
import yfinance as yf
import pandas as pd
from price_data_scripts.utils import constants

def fetch_yf(pair: str, period:str = '1d', interval:str = '60m') -> pd.DataFrame:
    """
    scrape data from yf
    
    args:
        pair: currency pair requested
        period: timeframe of data request
        intercal: time range form current time
    """
    data = pd.DataFrame()
    data = yf.download(tickers=pair, period=period, interval= interval)
    

    if not any(data) or data.empty:
        return pd.DataFrame()   # pandas dataframe
    
    data.reset_index(inplace = True)
    
    # add 1hr to every column to enable us record closing time for each candlestick
    # and make uniform candlestick data 
    data[constants.DATETIME] = data[constants.DATETIME] + timedelta(hours = 1)

    # drop the last redoundant row of dataframe
    data.drop(data.tail(1).index, inplace=True)
    data.set_index(data[constants.DATETIME], inplace = True, drop = True)
    data.drop(columns = [constants.DATETIME], inplace = True)
    # print(data)
    return data
