""" consstants file for cleaner code"""

DERIV_TICKERS = [
    # {'id':'frxAUDUSD', 'table': 'AUDUSD'},
    # {'id':'frxEURGBP', 'table': 'EURGBP'},
    # {'id':'frxEURJPY', 'table': 'EURJPY'},
    # {'id':'frxEURUSD', 'table': 'EURUSD'},
    # {'id':'frxGBPUSD', 'table': 'GBPUSD'},
    # {'id':'frxUSDCAD', 'table': 'USDCAD'},
    # {'id':'frxUSDCHF', 'table': 'USDCHF'},
    # {'id':'frxUSDJPY', 'table': 'USDJPY'},
    {'id':'frxXAUUSD', 'table': 'GoldUSD'},
    {'id': 'R_50', 'table': 'Volatility_50_Index'},
    {'id': 'R_75', 'table': 'Volatility_75_Index'},
    {'id': 'R_100', 'table': 'Volatility_100_Index'},
    {'id': 'stpRNG', 'table': 'Step_Index'},
    {'id': 'BOOM500', 'table': 'Boom_500_Index'},
    {'id': 'BOOM1000', 'table': 'Boom_1000_Index'},
    {'id': 'CRASH500', 'table': 'Crash_500_Index'},
    {'id': 'CRASH1000', 'table': 'Crash_1000_Index'},
    {'id': 'JD50', 'table': 'Jump_50_Index'},
    {'id': 'JD75', 'table': 'Jump_75_Index'},
    {'id': 'JD100', 'table':'Jump_100_Index'},
]

OPEN = 'open'
HIGH = 'high'
LOW = 'low'
CLOSE = 'close'
DATETIME ='datetime'
CANDLES = 'candles'
EPOCH = 'epoch'

VOLUME = 'volume'
TABLE = 'table'
ID = 'id'