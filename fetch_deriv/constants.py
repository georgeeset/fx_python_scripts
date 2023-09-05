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

MESSAGE_TITLE = """PRICE ALERT {pair} on {tf}"""
MESSAGE_BODY = """
Hi,

Your alert condition has been satisfied before your alert expiration time,
kindly check your trading chart
and confirm your plan before trading. below are details of the alert

Condition: {cdt}
Target price: {tgt}
Expiration: {crtd}
Reminder Note: {note}

Note: The alert will be repeated for {rpt} times if condition is still valid
Alert will be automatically terminated on {exp}

TRADE WISELY !!!

Disclaimer
fx-price-watch is not a financial advicer and will not be held accountable for
your trading decitions

You are receiving this message because you subscribed to {am} alert on
fx-price watch website. to unsubscribe to this message,
delete the alert on your profile
"""
