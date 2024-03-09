"""
module for fetching yf data from cloud
"""
import yfinance as yf
import pandas as pd

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
    return data
