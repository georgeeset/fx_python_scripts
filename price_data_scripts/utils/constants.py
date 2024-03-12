""" consstants file for cleaner code"""

CONDITION_CHOICES:list[tuple] = [
    ('C>TP','CLOSES ABOVE target price'),
    ('C<TP', 'CLOSES BELOW target price'),
    ('H>TP', 'HIGHEST price is ABOVE target price'),
    ('H<TP', 'HIGHEST price is BELOW target price'),
    ('L>TP', 'LOWEST price is ABOVE target price'),
    ('L<TP', 'LOWEST price is BELOW target price'),
]

""" id and table name map for easy represnetation of
database table name and api reference id for each currency pair
"""
DERIV_TICKERS = [
    # {'id':'frxAUDUSD', 'table': 'AUDUSD'},
    # {'id':'frxEURGBP', 'table': 'EURGBP'},
    # {'id':'frxEURJPY', 'table': 'EURJPY'},
    # {'id':'frxEURUSD', 'table': 'EURUSD'},
    # {'id':'frxGBPUSD', 'table': 'GBPUSD'},
    # {'id':'frxUSDCAD', 'table': 'USDCAD'},
    # {'id':'frxUSDCHF', 'table': 'USDCHF'},
    # {'id':'frxUSDJPY', 'table': 'USDJPY'},-------------------
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

""" forex ticker list for yf query
"""
YF_TICKERS =   [  
    'EURUSD=X',
    'AUDJPY=X',
    'EURCHF=X',
    'EURJPY=X',
    'USDJPY=X',
    'GBPUSD=X',
    'AUDUSD=X',
    'USDCAD=X',
    'USDCHF=X',
    'CADCHF=X',
    'CHFJPY=X',
    'USDHKD=X',
    'EURGBP=X',
    ]

VANTAGE_FX_TICKERS = [
    'EURUSD',
    'AUDJPY',
    'EURCHF',
    'EURJPY',
    'USDJPY',
    'GBPUSD',
    'AUDUSD',
    'USDCAD',
    'USDCHF',
    'CADCHF',
    'CHFJPY',
    'USDHKD',
    'EURGBP',
]

CRYPTO_TICKERS = [
    'ETHUSDT',
    'BTCUSDT',
    'SOLUSDT',
    'FTTUSDT',
    'XRPUSDT',
    'BNBUSDT',
    'LINKUSDT',
    'FTTUSDT',
    'AVAXUSDT',
    'TIAUSDT',
    'AVAXUSDT'
    ]

KLINE_COLUMN_NAMES= ['open_time','Open',
               'High', 'Low', 'Close',
               'Volume','close_time',
               'qav','num_trades','taker_base_vol',
               'taker_quote_vol', 'ignore'
               ]

RESULT = 'result'
PATTERNS = 'patterns'
LASTUSED = 'last_used'
Frequency = 'frequency'
RECENT_STATUS = 'recent_status'
PATTERN_ALERT_TBL = 'fxmktwatch_patternalert'


OPEN = 'Open'
HIGH = 'High'
LOW = 'Low'
CLOSE = 'Close'
DATETIME ='Datetime'
CANDLES = 'candles'
EPOCH = 'epoch'

VOLUME = 'Volume'
TABLE = 'table'
ID = 'id'
SECSINHR = 36000 # seconds in one hour

QUERY = 'query'

ALERTS_TABLE = 'fxmktwatch_alerts'
CURRENCY_PAIR_COL = 'currency_pair'
TARGET_COL = 'target_price'
EXPIRATION_COL = 'expiration'
REPEAT_ALARM_COL = 'repeat_alarm'
ALERT_COUNT = 'alertcount'
ALERT_MEDIUM_ID_COL = 'alert_medium_id'
NOTE_COL = 'note'
SETUP_CONDITION_COL = 'setup_condition'
ALERT_MEDIUM_TABLE = 'fxmktwatch_alertmedium'
TIMEFRAME = 'timeframe'
ID = 'id'
CHAT_ID = 'chat_id'
ALERT_ID = 'alert_id'
ALERT_TYPE = 'alert_type'
USER_ID_COL = 'user_id'
EMAIL = 'email'
TELEGRAM = 'telegram'

H1 = 'H1'
H4 = 'H4'
D1 = 'D1'
W1 = 'W1'
M1 = 'M1'

# Approved candlestick chart patterns
APPROVED_PATTERNS = ['engulfing', 'morningstar', 'morningdojistar', '3blackcrows',
                     'abandonedbaby',  'dojistar', 'dragonflydoji', 'eveningdojistar',
                     'gravestonedoji', 'longleggeddoji', 'kicking', 'kickingbylength',
                     'hammer', 'invertedhammer', '3whitesoldiers', 'haramicross', 
                     'spinningtop', 'piercing', 'darkcloudcover', 'risefall3methods',
                     'xsidegap3methods', 'shootingstar', 'hangingman', 'harami',
                     ]
LEVEL = 'Level'
FREQUENCY = 'Frequency'
ISSUPPORT = 'is_support'

MESSAGE_TITLE = """PRICE ALERT {pair} on {tf}"""
MESSAGE_BODY = """
Hi,

Your alert condition has been satisfied before your alert expiration time,
kindly check your trading chart to confirm your trading plan.

Instrument: {pair}

Timeframe: {tmf}

Alert Condition: {cdt}

Target price: {tgt}

Expiration: {crtd}

Alert sending status: {cnt} / {rpt}

Alert Expirex on: {exp}

Prefered Alert Medium: {am}

Reminder Note: {note}


TRADE WISELY !!!

"""

PATTERN_ALERT_MESSAGE = """Hi,
Your Pattern Alert have been traggered,
Kindly check your chart to analyze the market.
details:

Candlestick pattern(s): {patterns}

Instrument: {c_pair}

Served as support/resistance {used} times

Recently served as: {recent_status} on {last_used}

Alert Counter: {alert_count}

Reminder Note: {note}

NB: 
Consult an expart for fiancial advice
"""

HTML_MESSAGE = """
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FX Market Watch</title>
</head>
<body>
    {}
</body>
</html>
"""
