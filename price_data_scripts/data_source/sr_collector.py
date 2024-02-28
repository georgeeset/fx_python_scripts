"""
module that determine support and resistance of price
"""
import pandas as pd
import numpy as np
import constants


class SRCollector:
    """
    collect list of support and resistance
    """

    def __init__(self,scan_window:int) -> None:
        """
        initialize the class with needed data

        args:
            scan_window: howmany candles must be considered before picking the
                    highest / lowest price
        """
        self.__scan_window = scan_window

    def find_sr(self, data:pd.DataFrame) -> pd.DataFrame:
        length=self.__scan_window
        compiled = []
        for row in range(len(data)-length):
            point=self.__is_sr(data.iloc[row:row+length])
            if point:
                compiled.append(point)

        if len(compiled) > 0:
            compiled_df = pd.DataFrame(compiled)
            compiled_df.set_index(constants.DATETIME, inplace=True)
            return compiled_df
        return pd.DataFrame()

    def __is_sr (self, data) -> map:
        """
        compare a given dataframe slice for highest and lowest value

        args:
            data: slice of price dataframe should be same size as window

        returns: map containing value, bool support or not support, datetime
        """
        center = round(self.__scan_window/2)

        # if(len(df)!= (center*2)):
        #     print('Data length does not put center at {c}'.format(c=center))
        #     return None 
        highestHigh=data[constants.CLOSE].max()
        lowestLow=data[constants.CLOSE].min()
       
        # find max and appriximate if any
        if(highestHigh==data[constants.CLOSE].iloc[center]):
            data_found = {constants.LEVEL: highestHigh,
                          constants.ISSUPPORT: False,
                          constants.DATETIME: data.index[center]
                          }
            # print(data_found)
            return data_found
        
        elif(lowestLow==data[constants.CLOSE].iloc[center]):
            # print(f'Min found: {lowestLow}')
            data_found = {constants.LEVEL: lowestLow,
                          constants.ISSUPPORT: True,
                          constants.DATETIME: data.index[center]
                          }
            # print(data_found)
            return data_found
        else:
            return None
