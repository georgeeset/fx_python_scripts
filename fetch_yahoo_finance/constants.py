""" consstants file for cleaner code"""

tickers =   [  
    'EURUSD=X',
    'EURJPY=X',
    # 'USDJPY=X',
    # 'GBPUSD=X',
    # 'AUDUSD=X',
    # 'USDCAD=X',
    # 'USDCHF=X',

    # 'CADCHF=X',
    # 'USDCNY=X',
    # 'USDHKD=X',
    # 'EURGBP=X',
    ]

deriv_tickers = {
    'id':'frxAUDUSD', 'table': 'AUDUSD',
    'id':'frxEURGBP', 'table': 'EURGBP',
    'id':'frxEURJPY', 'table': 'EURJPY',
    'id':'frxEURUSD', 'table': 'EURUSD',
    'id':'frxGBPUSD', 'table': 'GBPUSD',
    'id':'frxUSDCAD', 'table': 'USDCAD',
    'id':'frxUSDCHF', 'table': 'USDCHF',
    'id':'frxUSDJPY', 'table': 'USDJPY',
    'id':'frxXAUUSD', 'table': 'GoldUSD',
    'id': 'R_50', 'table': 'Volatility_50_Index',
    'id': 'R_75', 'table': 'Volatility_75_Index',
    'id': 'R_100', 'table': 'Volatility_100_Index',
    'id': 'stpRNG', 'table': 'Step_Index',
    'id': 'BOOM500', 'table': 'Boom_500_Index',
    'id': 'BOOM1000', 'table': 'Boom_1000_Index',
    'id': 'CRASH500', 'table': 'Crash_500_Index',
    'id': 'CRASH1000', 'table': 'Crash_1000_Index',
    'id': 'JD50', 'table': 'Jump_50_Index',
    'id': 'JD75', 'table': 'Jump_75_Index',
    'id': 'JD100', 'table':'Jump_100_Index',
    }

open = 'Open'
high = 'High'
low = 'Low'
close = 'Close'
volume = 'Volume'
datetime='datetime'

CONDITION_CHOICES = [
    'CLOSING PRICE IS GREATER THAN SETPOINT',
    'CLOSING PRICE IS LESS THAN SETPOINT',
    'OPENING PRICE IS GREATER THAN SETPOINT',
    'OPENING PRICE IS LESS THAN SETPOINT',
    'HIGHEST PRICE IS GREATER THAN SETPOINT',
    'HIGHEST PRICE IS LESS THAN SETPOINT',
    'LOWEST PRICE IS GREATER THAN SETPOINT',
    'LOWEST PRICE IS LESS THAN SETPOINT'
]

ALERTS_TABLE = 'fxmktwatch_alerts'
CURRENCY_PAIR_COL = 'currency_pair'
TARGET_COL = 'target_price'
EXPIRATION_COL = 'expiration'
REPEAT_ALARM_COL = 'repeat_alarm'
ALERT_COUNT = 'alertcount'
ALERT_MEDIUM_ID_COL = 'alert_medium_id'
NOTE_COL = 'note'
CONDITION_COL = 'condition'
ALERT_MEDIUM_TABLE = 'fxmktwatch_alertmedium'
ID = 'id'
CHAT_ID = 'chat_id'
ALERT_ID = 'alert_id'
ALERT_TYPE = 'alert_type'
USER_ID_COL = 'user_id'
EMAIL = 'email'
TELEGRAM = 'telegram'
