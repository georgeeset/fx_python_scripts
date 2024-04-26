
import pandas as pd

def wvf(data, lookback=22):
  """
  This function calculates the Williams VIX Fix for a given forex price dataframe.

  Args:
      data (pandas.DataFrame): Dataframe containing columns 'Open', 'High', 'Low', 'Close'
      lookback (int, optional): Lookback period for the highest price. Defaults to 22.

  Returns:
      pandas.DataFrame: Dataframe with additional column 'Williams VIX Fix'
  """

  # Calculate Highest closing price in lookback period
  data['Highest Close'] = data['Close'].rolling(window=lookback).max()

  # Calculate Williams VIX Fix
  data['Wvf'] = (data['Highest Close'] - data['Low']) / data['Highest Close'] * 100

  # Drop unnecessary column
  data = data.drop('Highest Close', axis=1)

  return data