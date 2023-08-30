from metaapi_cloud_sdk import MetaApi
import asyncio


token = 'eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiIwNWU1NDJiMjk2ZjFmZTAwMjM3M2RlMmQ3YmEwMGVjMSIsInBlcm1pc3Npb25zIjpbXSwiYWNjZXNzUnVsZXMiOlt7ImlkIjoidHJhZGluZy1hY2NvdW50LW1hbmFnZW1lbnQtYXBpIiwibWV0aG9kcyI6WyJ0cmFkaW5nLWFjY291bnQtbWFuYWdlbWVudC1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1yZXN0LWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1ycGMtYXBpIiwibWV0aG9kcyI6WyJtZXRhYXBpLWFwaTp3czpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibWV0YWFwaS1yZWFsLXRpbWUtc3RyZWFtaW5nLWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6d3M6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFzdGF0cy1hcGkiLCJtZXRob2RzIjpbIm1ldGFzdGF0cy1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoicmlzay1tYW5hZ2VtZW50LWFwaSIsIm1ldGhvZHMiOlsicmlzay1tYW5hZ2VtZW50LWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJjb3B5ZmFjdG9yeS1hcGkiLCJtZXRob2RzIjpbImNvcHlmYWN0b3J5LWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJtdC1tYW5hZ2VyLWFwaSIsIm1ldGhvZHMiOlsibXQtbWFuYWdlci1hcGk6cmVzdDpkZWFsaW5nOio6KiIsIm10LW1hbmFnZXItYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX1dLCJ0b2tlbklkIjoiMjAyMTAyMTMiLCJpbXBlcnNvbmF0ZWQiOmZhbHNlLCJyZWFsVXNlcklkIjoiMDVlNTQyYjI5NmYxZmUwMDIzNzNkZTJkN2JhMDBlYzEiLCJpYXQiOjE2OTI2NTY3MjYsImV4cCI6MTcwMDQzMjcyNn0.Lmv0_eiTvrbQ10ZXCvfrqg-LCYuRRz1EaMKyjHeC997SnvGTWzU2DTXyckq_JCZetO7_ZhfEF1U4U1g4hkNlvGPYhHhJlkoTln95Ntbmet7hXEBmZ5uYGuaDjwc32yShd11P2Xck53U0M4I9_eF251FwSXfW5A5D4TtB2nMlyzuDfxcXIV8riR0YVD0V4G5FOsLigw_XWiZlPlYTfMC_OtF6yFQDPYmyLf7dtxul3yYc_6qaZj4yCGNCEmsRbsuXPfMG9ctmvU1rtSbD5yg68IBM5gbWX4IsU6dfew-QC0QlEqrCNCtMKNGIkj8o-beCwGA_tLI-SmsysmqF7eOl0PT6k-MusJQy09jk4Isos366nfniwhx-CCDBJwPN28zq10NXxiSxkU0mhzvsWJd8c4h1qxFnMqV3lh69MEtaCbvNQ5hMhbuE4QADXNa6jGGNLzslxh7P7_N9mPqA_J9kjffwS4NYaL8nw52ZmQGdBPgD5UyVxj98wx6vQbiQjFWTrPCE-8Iidn45vJuCsp00vxxC7d1HHjdvI6vhoT8Oz2NQGCeh1mB0_8YkhdUvgHQ_dP65CDtcEvTh27KEOkM67qMH_iHDbGhq6fG6Rs80ae0TeZoOVOcVpe4q1K-QVokZeioQ1pftrsvuINXHDCgxJfuqg6q8IkP0Jou_jMy8JTQ'
# params = {'auth-token':key,}
account_id = 'f83d0c2b-7b7e-49cf-a9e4-37868bcbfb2f'
# symbol = 'EURUSD'
# timeframe = '30m'
# limit = 100
# url = 'https://mt-market-data-client-api-v1.new-york.agiliumtrade.ai/users/current/accounts/f83d0c2b-7b7e-49cf-a9e4-37868bcbfb2f/historical-market-data/symbols/EURUSD/timeframes/30m/candles?limit=100'
# header= {'auth-token':key}
# mt_response = requests.get(url, headers=header)
# print(mt_response.content)

# sio = socketio.Client()

# @sio.event
# async def connect():
#     print('connection established')

# @sio.event
# async def my_message(data):
#     print('message received with ', data)
#     sio.emit('my response', {'response': 'my response'})

# @sio.event
# async def disconnect():
#     print('disconnected')

# async def main():
#     sio.connect('https://mt-client-api-v1.agiliumtrade.agiliumtrade.ai', headers={'type':'synchronize', 'accountId':account_id, 'requestId':'534425-636-asdfa-sa'}, auth=key, socketio_path='/ws')
#     sio.wait()

import os
import asyncio
from metaapi_cloud_sdk import MetaApi
# from metaapi_cloud_sdk.clients.metaApi.tradeException import TradeException
from datetime import datetime

# Note: for information on how to use this example code please read https://metaapi.cloud/docs/client/usingCodeExamples

token = os.getenv('TOKEN') or 'eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiIwNWU1NDJiMjk2ZjFmZTAwMjM3M2RlMmQ3YmEwMGVjMSIsInBlcm1pc3Npb25zIjpbXSwidG9rZW5JZCI6IjIwMjEwMjEzIiwiaW1wZXJzb25hdGVkIjpmYWxzZSwicmVhbFVzZXJJZCI6IjA1ZTU0MmIyOTZmMWZlMDAyMzczZGUyZDdiYTAwZWMxIiwiaWF0IjoxNjkyNjkzMTc0fQ.NVnimC0uvf3U3vJMunGCml03J-wwXpvaGS91Fo9UmuCozLbs4Hc6C-yD8dXV-1qNcmPg2ctT3nxoz2M3ga9Lhov0PhXzscDxKRUpWPIhhc4Lue_b4YOxdqhqDa0LxUMZeKK0TPxH12HUh7jIiIpOBRL5eO0Vug8kDVBpXZwE1fniXUyYvJLkzy6WFJBKOY6uGJZjrYtmHHOcIfqfXkGoLaFXlEusJ4Q1S15BW81BiGJngtMu_GB61sqPP9UK6U7IN3PlDOmUa_ZozEjDZq9N7doG7-mrhuH3Pd4zIAyaL22ykLZarpRsqV1D6W8PXNGA6ZLI_UjIetkXxpR5V1TTah9gqVVJjBANKNTKsBE7elWqRrzXed7tvwfuOgBXrel9tuTOMbzjxUjDPzq_EorV2Wc12XtuX89vpN4SYbKZCbmxmWg-aTgFhzB0Z0xPGpEi1C-GTmRM0YZEooj5csEZ7DQe5pEEl_5ZEcs9y6KT5pxfhe7-J6FrQ5uv9xx5E0OygV6ZKtLILiL5zBIKuTabiLPyUNMptQVBljJtS4lWaZ-BMS0EZnWrSEHCkckRPjzQuxIXCUADdigD8ATSyKH2Fdb_DOid60Ze4Xey37gc2QG1ps845BWPMnhktQjUSdp-Ih6VYmOEWJpH8Vvh4OOGCow6t6itw1rOFVHTQoz58W0'
accountId = os.getenv('ACCOUNT_ID') or 'f83d0c2b-7b7e-49cf-a9e4-37868bcbfb2f'


async def test_meta_api_synchronization():
    api = MetaApi(token)
    try:
        account = await api.metatrader_account_api.get_account(accountId)
        initial_state = account.state
        deployed_states = ['DEPLOYING', 'DEPLOYED']

        if initial_state not in deployed_states:
            #  wait until account is deployed and connected to broker
            print('Deploying account')
            await account.deploy()

        print('Waiting for API server to connect to broker (may take couple of minutes)')
        await account.wait_connected()

        # connect to MetaApi API
        connection = account.get_streaming_connection()
        await connection.connect()

        # wait until terminal state synchronized to the local state
        print('Waiting for SDK to synchronize to terminal state (may take some time depending on your history size)')
        await connection.wait_synchronized()

        # # access local copy of terminal state
        # print('Testing terminal state access')
        # terminal_state = connection.terminal_state
        # print('connected:', terminal_state.connected)
        # print('connected to broker:', terminal_state.connected_to_broker)
        # print('account information:', terminal_state.account_information)
        # print('positions:', terminal_state.positions)
        # print('orders:', terminal_state.orders)
        # print('specifications:', terminal_state.specifications)
        # print('EURUSD specification:', terminal_state.specification('EURUSD'))
        # print('EURUSD price:', terminal_state.price('EURUSD'))


        # # access history storage
        # history_storage = connection.history_storage
        # print('deals:', history_storage.deals[-5:])
        # print('deals with id=1:', history_storage.get_deals_by_ticket('1'))
        # print('deals with positionId=1:', history_storage.get_deals_by_position('1'))
        # print('deals for the last day:', history_storage.get_deals_by_time_range(
        #     datetime.fromtimestamp(datetime.now().timestamp() - 24 * 60 * 60), datetime.now()))


        # print('history orders:', history_storage.history_orders[-5:])
        # print('history orders with id=1:', history_storage.get_history_orders_by_ticket('1'))
        # print('history orders with positionId=1:', history_storage.get_history_orders_by_position('1'))
        # print('history orders for the last day:', history_storage.get_history_orders_by_time_range(
        #     datetime.fromtimestamp(datetime.now().timestamp() - 24 * 60 * 60), datetime.now()))

        # calculate margin required for trade
        print('margin required for trade', await connection.calculate_margin({
            'symbol': 'GBPUSD',
            'type': 'ORDER_TYPE_BUY',
            'volume': 0.01,
            'openPrice': 1.1
        }))

        print('price subscription', await connection.subscribe_to_market_data(symbol='EURUSD', timeout_in_seconds=2))

        # # trade
        # print('Submitting pending order')
        # try:
        #     result = await connection.create_limit_buy_order('GBPUSD', 0.07, 1.0, 0.9, 2.0,
        #                                                      {'comment': 'comm', 'clientId': 'TE_GBPUSD_7hyINWqAlE'})
        #     print('Trade successful, result code is ' + result['stringCode'])
        # except Exception as err:
        #     print('Trade failed with error:')
        #     print(api.format_error(err))

        if initial_state not in deployed_states:
            # undeploy account if it was undeployed
            print('Undeploying account')
            await account.undeploy()

    except Exception as err:
        print(api.format_error(err))
    exit()

loop = asyncio.get_event_loop()
loop.run_until_complete(test_meta_api_synchronization())

# asyncio.run(test_meta_api_synchronization())