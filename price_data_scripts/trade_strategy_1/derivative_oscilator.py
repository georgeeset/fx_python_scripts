import talib as ta
import numpy as np


def derivative_oscillator(data, rsi_period=14, signal_period=9):
  """
  This function calculates the derivative oscillator for a given forex price dataframe using TA-Lib.

  Args:
      data (pandas.DataFrame): Dataframe containing columns 'Open', 'High', 'Low', 'Close'
      rsi_period (int, optional): RSI calculation period. Defaults to 14.
      signal_period (int, optional): Signal line period (SMA over RSI). Defaults to 9.

  Returns:
      pandas.DataFrame: Dataframe with additional columns 'RSI', 'Signal Line', 'Derivative Oscillator'
  """

  # Ensure TA-Lib is installed (use 'pip install TA-Lib' if not)

  # Convert data to TA-Lib compatible format (numpy arrays)
  close_prices = data['Close'].to_numpy()

  # Calculate RSI using TA-Lib
  rsi = ta.RSI(close_prices, timeperiod=rsi_period)

  # Calculate Signal Line (SMA of RSI) using TA-Lib
  signal_line = ta.SMA(rsi, timeperiod=signal_period)

  # Calculate Derivative Oscillator
  derivative_oscillator = rsi - signal_line

  # Add new columns to dataframe
  data['Derivative Oscillator'] = derivative_oscillator

   # Buy/Sell Signals based on zero line crossovers
  data['Buy Signal'] = np.where(data['Derivative Oscillator'].diff() > 0, 1, 0)
  data['Sell Signal'] = np.where(data['Derivative Oscillator'].diff() < 0, 1, 0)


  return data