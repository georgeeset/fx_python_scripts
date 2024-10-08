"""
Module for extracting price data from Deriv API server.

This module defines a `DerivManager` class for managing API connections and retrieving
candle data.
"""

from price_data_scripts.utils import constants
import pandas as pd
from datetime import datetime, timedelta
from deriv_api import DerivAPI

class DerivManager:
    """
    Manages Deriv API connections and data requests.

    Attributes:
        api_id (str): The Deriv API ID used for authentication.
        api (DerivAPI, optional): The DerivAPI instance.
    """

    def __init__(self):
        """
        Initializes a DerivManager object.
        """
        pass

    @property
    def is_connected(self) -> bool:
        """
        Returns True if the manager is connected to the Deriv API, False otherwise.
        """
        return self.api is not None and self.api.connected

    async def connect(self,):
        """
        Connects to the Deriv API.
        """
        self.api = DerivAPI(app_id = 1234)

    async def fetch_candles(self, pair: str, frame: int, size: int, end_time: int) -> pd.DataFrame:
        """
        Fetches candle data from the Deriv API.

        Args:
            pair (str): The currency pair or index.
            frame (str): The timeframe granularity in seconds.
            size (int): The number of candles to retrieve.
            end_time (str): The datetime epoch time of the last candle.

        Returns:
            pd.DataFrame: A DataFrame containing the candle data.

        Raises:
            ValueError: If invalid parameters are provided.
            DerivAPIError: If an error occurs during data retrieval.
        """

        if not self.is_connected:
            raise RuntimeError("Not connected to the Deriv API. Call connect() first.")

        try:
            data = await self.api.ticks_history(
                {
                    'ticks_history': pair,
                    'style': constants.CANDLES,
                    'granularity': frame,
                    'count': size,
                    'end': str(end_time)
                }
            )
        except Exception as e:
            raise ConnectionError(f"Failed to fetch candle data {pair}: {e}") from e

        # validate data received
        if data.get(constants.CANDLES):
            # Convert raw data to a DataFrame
            candles_data = self._make_dataframe(data)
            candles_data.drop(candles_data.index[-1], axis=0, inplace=True)
            # print(candles_data)
            return candles_data

        return pd.DataFrame()

    def _make_dataframe(self, candles: dict) -> pd.DataFrame:
        """ Convert map data to pandas Dataframe with
        all fields named with first later capitalized.
        e.g: Open Low...

        Args:
            candles: ohlc data from candlestick data

        Returns: pandas DataFrame
        """

        dict_data:dict = {constants.DATETIME: [],
                                constants.OPEN: [],
                                constants.HIGH: [],
                                constants.LOW: [],
                                constants.CLOSE: []
                                }

        # Fill data into dataframe add 1h to time to make each candle carry closing time
        # customize for deriv data which is usually made with candle open time
        for candle in candles.get(constants.CANDLES) or []:
            dict_data[constants.DATETIME].append(datetime.fromtimestamp(candle.get(constants.EPOCH)) + timedelta(hours = 1)) # add timezone if you wish
            dict_data[constants.OPEN].append(candle.get(constants.OPEN.lower()))
            dict_data[constants.HIGH].append(candle.get(constants.HIGH.lower()))
            dict_data[constants.LOW].append(candle.get(constants.LOW.lower()))
            dict_data[constants.CLOSE].append(candle.get(constants.CLOSE.lower()))
            # No volume

        candles_data = pd.DataFrame.from_dict(dict_data)
        candles_data.set_index(constants.DATETIME, inplace=True)
        # print(candles_data)
        return candles_data

    async def disconnect(self):
        """
        Disconnects from the Deriv API.
        """
        if self.api is not None:
            await self.api.disconnect()
            self.api = None
