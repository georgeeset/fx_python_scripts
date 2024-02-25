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
        self.__sr_dataframe = pd.DataFrame(columns=[
            constants.LEVEL, constants.ISSUPPORT, constants.DATETIME, constants.FREQUENCY
            ])

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
        df=data.copy()
        center = round(self.__scan_window/2)

        # if(len(df)!= (center*2)):
        #     print('Data length does not put center at {c}'.format(c=center))
        #     return None 
        highestHigh=df[constants.CLOSE].max()
        lowestLow=df[constants.CLOSE].min()
        
        # find max and appriximate if any
        if(highestHigh==df.iloc[center][constants.CLOSE]):
            data_found = {constants.LEVEL: highestHigh,
                          constants.ISSUPPORT: False,
                          constants.DATETIME: df.index[center]
                          }
            # print(data_found)
            return data_found
        
        elif(lowestLow==df.iloc[center][constants.CLOSE]):
            # print(f'Min found: {lowestLow}')
            data_found = {constants.LEVEL: lowestLow,
                          constants.ISSUPPORT: True,
                          constants.DATETIME: df.index[center]
                          }
            # print(data_found)
            return data_found
        else:
            return None
