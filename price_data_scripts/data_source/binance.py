"""
module used to download historical price data from binance api
"""

import pandas as pd
import constants
from binance.spot import Spot
from datetime import datetime

class BinanceData:
    """
    Manage bianance api connection and download spot price data

    
    """

    def __init__(self) -> None:
        """
        Initailize binance spot client
        """
        self.client = Spot()

    def fetch_candles(self, ticker:str, timeframe:str, limit:int) -> pd.DataFrame:
        """
        Request price data from binance api

        Args:
            ticker: currency pair
            timeframe: chart timeframe. eg; 1h, 4h, 1d ...
            limit: number of historical candles to request

        Returns: pandas dataframe

        Throws: ConnectionError
        """
        try:
            response = self.client.klines(symbol=ticker, interval=timeframe, limit=limit)
        except Exception as ex:
            raise ValueError("Failed to download from server: ", ex)

        if response is None:
            raise ConnectionError("unable to get data for ticker {}".format(ticker))

        data = self._convert_data(response)
        # print(type(data[constants.CLOSE].iloc[-1])) # its a fucking string
        return data
    
    def _convert_data(self, payload:list) -> pd.DataFrame:
        """
        Clean up payload message and return ohlcv dataframe

        Args:
            payload: list of raw data received from server

        Return: pandas dataframed cleaned up for processing
        """
        price_data = pd.DataFrame(payload, columns=constants.KLINE_COLUMN_NAMES)
        price_data[constants.DATETIME] = pd.to_datetime(
            price_data['close_time'], unit='ms', utc=False
            ).round('1s')
        
        price_data.drop(['open_time','close_time','qav','num_trades',
                        'taker_base_vol','taker_quote_vol', 'ignore'
                        ],axis=1,inplace=True)
        price_data.set_index(constants.DATETIME,inplace=True)

        # due to deriv api is not a complete timeframe
        price_data.drop(price_data.index[-1], axis=0, inplace=True)

        return price_data
