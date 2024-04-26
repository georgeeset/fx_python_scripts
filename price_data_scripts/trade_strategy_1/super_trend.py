import pandas_ta as ta
import pandas as pd

def super_trend(data: pd.DataFrame, atr_length:int = 20, multiplier:int = 3) -> pd.DataFrame:
    data[['St', 'StDirection', 'StLong','StShort']]= data.ta.supertrend(length=atr_length, multiplier=multiplier)
    return data