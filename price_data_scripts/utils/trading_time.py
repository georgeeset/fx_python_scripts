"""
module for determining if market is close or open
"""
from datetime import datetime

def fx_is_open(my_time:datetime) -> bool:
    """ Use date time to check status

    args:
        my_time: current datetime
    
    returns: True if market is open
            or False if market is close
    """

    # fx closes 20:00  on Fridays
    # fx Opens 00:00 on Monday
    open:bool = True

    week_num = my_time.weekday()
    current_hour = my_time.hour

    if week_num == 4 and current_hour >20:
        # 1hr added to enable us collect 20:00 data
        open = False
    
    if week_num > 4:
        open = False
    
    return open

def fx_no_multi_timeframe(my_time:datetime):
    """ determine if h4, d1 tim"""
    pass