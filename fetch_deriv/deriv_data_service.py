from deriv_api import DerivAPI
import asyncio
from datetime import datetime
import constants
import pandas as pd
from deriv_storage_service import store_in_db
from alert_query_service import alert_query_manager
# import os

async def connect_attempt():
    # Define your API key
    # api_key = os.environ.get('DERIV_API_KEY')
    api_id = '1089'


    now = datetime.now()
    epoch_time = int(now.timestamp())
    print(epoch_time)
    

    chart_type = "candles"
    granularity = 3600 #seconds = 1 hour
    count = 10  # Number of hourly candles you want to retrieve


    api = DerivAPI(app_id=api_id)
    # response = await api.ping({'ping': 1})
    # print(response)

    # authorize = await api.authorize(api_key)
    # print(authorize)

    # # GET LIST OF SUPPORTED ASSETS
    # assets = await api.cache.asset_index()
    # for item in assets.get('asset_index'):
    #     print(f'{item[0]} => {item[1]}')

    # Make the API request to get candles data
    for value in constants.DERIV_TICKERS:
        try:
            # ticks = await api.ticks('R_100')
            # print(ticks)
            
            print(value)
            candles = await api.ticks_history(
                {'ticks_history': value[constants.ID], 'style': chart_type,
                'granularity': granularity, 'count': count,
                'end': str(epoch_time)
                })
            
            if candles.get(constants.CANDLES):
                dict_data = {constants.DATETIME: [],
                             constants.OPEN: [],
                             constants.HIGH: [],
                             constants.LOW: [],
                             constants.CLOSE: []
                             }

                for candle in candles.get(constants.CANDLES):
                    dict_data[constants.DATETIME].append(datetime.fromtimestamp(candle.get(constants.EPOCH)))
                    dict_data[constants.OPEN].append(candle.get(constants.OPEN))
                    dict_data[constants.HIGH].append(candle.get(constants.HIGH))
                    dict_data[constants.LOW].append(candle.get(constants.LOW))    
                    dict_data[constants.CLOSE].append(candle.get(constants.CLOSE))
                    # No volume

                candles_data = pd.DataFrame.from_dict(dict_data)
                candles_data.set_index(constants.DATETIME, inplace=True)
                print(candles_data)

                store_in_db(data=candles_data,
                            pair=f'{value[constants.TABLE]}_h1',
                            store_rows=-1,
                            )
                
                #first rename the df column to help enable simless dataformat
                candles_data.rename({'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close'}, axis=1, inplace=True)
                alert_query_manager(candles_data, instrument=value[constants.TABLE])
                # break
            ## Print the candle data
            # for candle in candles.get('candles'):
            #     print(f"""{datetime.fromtimestamp(candle.get('epoch'))} => {candle.get('open')} => {candle.get('high')} => {candle.get('low')} => {candle.get('close')}""")

            print("============================================")

        except Exception as e:
            print(f"An error occurred: {e}")


asyncio.run(connect_attempt())