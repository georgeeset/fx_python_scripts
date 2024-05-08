import logging
from price_data_scripts.trade_strategy_1.super_trend import super_trend
from price_data_scripts.trade_strategy_1.vix_fix import wvf
from price_data_scripts.trade_strategy_1.derivative_oscilator import derivative_oscillator
from price_data_scripts.utils import constants
from price_data_scripts.data_source.deriv import DerivManager
from price_data_scripts.utils.messenger import Messenger
from datetime import datetime
import pandas as pd
import asyncio
import os


async def strategy_task(data_source:DerivManager, item:dict, epoch_time:int, messenger:Messenger):
    try:

        data:pd.DataFrame = await data_source.fetch_candles(item[constants.ID], 86400, 50, epoch_time)
    except Exception as e:
        logging.error(f'Price request failed. Symbol:{item[constants.TABLE]}, Message: {e}')

    response = super_trend(data.copy())
    # print(response)
    response.drop(['StShort', 'StLong'], axis=1, inplace=True)

    new_data = wvf(response)

    complete_data = derivative_oscillator(new_data)
    complete_data.dropna(inplace=True)

    # print(complete_data)
    # print(type(complete_data.iloc[-1]['StDirection']))
    message:str = ''

    if complete_data.iloc[-1]['StDirection'] == 1 and complete_data.iloc[-1]['Wvf'] >= 2.0 and complete_data.iloc[-1]['Buy Signal'] == 1:
        message = f'Strategy1\nBuy signal {item[constants.TABLE]}'
        print(message)
    elif complete_data.iloc[-1]['StDirection'] == -1 and complete_data.iloc[-1]['Wvf'] >= 2.0 and complete_data.iloc[-1]['Sell Signal'] == 1:
        message = f'Strategy1\nSell signal {item[constants.TABLE]}'
        print(message)
    
    if message != '':
        await messenger.send_telegram_async(message, chat_id=5413877579)
    else:
        print('no trade')



    
async def main() -> None:

    data_source = DerivManager()
    await data_source.connect()
    epoch_time:int = int(datetime.now().timestamp())
    my_messenger = Messenger()

    

    task_list:list = []

    for item in constants.STRATEGY_TICKERS:
      my_task = asyncio.create_task(strategy_task(data_source=data_source, item=item, epoch_time=epoch_time, messenger = my_messenger))
      task_list.append(my_task)

    await asyncio.gather(*task_list)
    await data_source.disconnect()

if __name__ == "__main__":

    # Get the script's absolute path
    script_dir = os.path.dirname(os.path.abspath(__file__))

    logging.basicConfig(
    level = logging.WARNING,
    filemode = 'a',
    filename = os.path.join(script_dir, 'logs/strategy1.log'),
    format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',    
    datefmt='%Y-%m-%d %H:%M:%S',
    force = True
    )

    asyncio.run(main())

exit()
