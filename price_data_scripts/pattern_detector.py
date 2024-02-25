"""
module for detecting common candlestick patterns
"""
import pandas_ta as ta
import pandas as pd
import constants

class PatternDetector:
    """
    detect candle pattern
    """
    def __init__(self):
        pass

    def check_patterns(self, data):
        
        result = data.ta.cdl_pattern(name = constants.APPROVED_PATTERNS)
        target_value = 0
        target_index = -1
        # Create a boolean mask to identify columns with the
        # target value in the specified row
        mask = (result.iloc[target_index] != target_value)
        print(data)
        # Print the column names
        print(result.columns[mask].to_list())