"""
module for detecting common candlestick patterns
"""
import pandas_ta as ta
import pandas as pd
from . import constants
from .db_storage_service import MysqlOperations

class PatternDetector(MysqlOperations):
    """
    detect candle pattern
    """

    def __init__(self):
        """ initialization """
        super().__init__()

    def check_patterns(self, data:pd.DataFrame, pair: str) -> dict | None:
        """
        check a given dataframe for approved candlestick pattern
        only checks for last row of dataframe

        args:
            data: dataframe of ohlc of price
            pair: currency pair/ instrumet

        returns: dataframe containing details of pattern detected
                and price range history 
        """

        result = data.ta.cdl_pattern(name = constants.APPROVED_PATTERNS)
        target_value = 0
        target_index = -1
        # Create a boolean mask to identify columns with the
        # target value in the specified row
        mask = (result.iloc[target_index] != target_value)
        # print(data)

        # get column names
        spotted_list = result.columns[mask].to_list()
        # print(spotted_list)
        if len(spotted_list) > 0:
            observation = self.__query_zone(data[constants.CLOSE].iloc[target_index], pair)
            
            if observation:
                observation[constants.PATTERNS] = spotted_list
                return observation
        
        return None
  
    def __query_zone(self, price:float, pair) -> dict:
        """
        perform a query to get repeated
        support and resistance around that price zine
        """
        response = self.query_sr(price, pair)
        if response.empty:
            return {}
        # print(response)
        observation = {"frequency": len(response),
                       "last_used": response.index[-1],
                       "recent_status": "Support" if response[constants.ISSUPPORT].iloc[-1] == 1 else "Resistance"}

        return observation

    def compile_mailing_list(self, pair, timeframe) -> pd.DataFrame:
        """
        query the pattern alert databaase for user's alert to get their alert info
        """
        limit = 100 if timeframe == constants.D1 else 1
        return self.query_pattern_table(pair, timeframe, limit)

    def update_message_count(self, data:pd.DataFrame) -> None:
        """increment alert count"""
        for item in data.itertuples:
            self.increment_alert_count(constants.PATTERN_ALERT_TBL,
                                       constants.ALERT_COUNT,
                                       item[constants.id]
                                       )

    def clean(self) -> None:
        self.disconnect()

    dispose = close = disconnect = clean
