"""
module for detecting common candlestick patterns
"""
import pandas_ta as ta
import pandas as pd
import constants
from db_storage_service import MysqlOperations

class PatternDetector(MysqlOperations):
    """
    detect candle pattern
    """
    def __init__(self):
        """ initialization """
        super().__init__()


    def check_patterns(self, data:pd.DataFrame, pair: str):
        """
        check a given dataframe for approved candlestick pattern
        only checks for last row of dataframe

        args:
            data: dataframe of ohlc of price
            pair: currency pair/ instrumet

        returns: dataframe containing details of pattern detected
                and price range history 
        """
        patterns = []
        details = {}
        result = data.ta.cdl_pattern(name = constants.APPROVED_PATTERNS)
        target_value = 0
        target_index = -1
        # Create a boolean mask to identify columns with the
        # target value in the specified row
        mask = (result.iloc[target_index] != target_value)
        # print(data)

        # get column names
        spotted_list = result.columns[mask].to_list()
        print(patterns)
        # for item in spotted_list:
        #     patterns.append({"name":item, "value": result[item].iloc[-1]})

        # send price to get the location
        self.__query_location(data[constants.CLOSE].iloc[target_index], pair) 
    
    def __query_location(self, price:float, pair) -> map:
        """
        perform a query to database to get repeated
        sr positions
        """
        print(self.query_sr(price, pair))

