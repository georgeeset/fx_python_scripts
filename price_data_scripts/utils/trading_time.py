"""
module for determining if market is close or open
"""
import calendar
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
    is_open:bool = True

    week_num = my_time.weekday()
    current_hour = my_time.hour

    if week_num == 4 and current_hour > 21:
        # 1hr added to enable us collect 20:00 data at 21:00
        return False
    
    if week_num > 4:
        return False

    if week_num == 0 and current_hour == 0:
        # no need to check for data when candle of the day has not formed
        return False

    return True

def fx_week_start_end(my_time:datetime) -> int | None :
    """
    Indicate if at trading week just started or ended.
    will be used to determine when to start or stop
    gathering data

    args:
        my_time: datetime data

    returns:
        int "1" or "0" representing first (1)
        and last (0) trading hour of the week
    """
    week_num = my_time.weekday()
    current_hour = my_time.hour

    if week_num == 4 and current_hour == 21:
        # last hour of the week
        return 0
    
    if week_num == 0 and current_hour == 1:
        # fiest hour of trading week
        return 1
    return None

def is_last_daty_of_month(my_date:datetime) -> bool:
    """
    determine if a given date is the last day of the month
    """

    last_day_of_month = calendar.monthrange(my_date.year, my_date.month)[1]

    if my_date.day == last_day_of_month:
        return True
    return False
