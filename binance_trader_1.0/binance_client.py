import asyncio
import json
import os
from binance import AsyncClient

from models.symbol_model import Symbol
from models.price_index_model import PriceIndex
from models.assets_model import Asset, Account
from models.loan_details_model import Transaction, RepayDetails

async def main():
    api_key = os.environ.get('BINANCE_API_KEY')
    secret_key = os.environ.get('SECRET_KEY')

    client = await AsyncClient.create(
        api_key=api_key,
        api_secret=secret_key,
    )

    #===============================client margin asset========================
    # info = client.get_margin_asset(asset='BNB')
    # print(info)
    # fetch exchange info

    try: # Allmargin orders
        orders = await client.get_all_margin_orders(symbol='BNBBTC', limit=10)
    except Exception as e:
        print(e)
    print(orders)

    # res = await client.get_exchange_info()
    # # print(json.dumps(res, indent=2))
    # for item in res:
    #     print(item)
    # print (res['rateLimits'])
    # for rs in res['symbols']:
    #     print(rs)


    # #Get isolated margin symbol info
    # info = await client.get_isolated_margin_symbol(symbol='BTCUSDT')
    # print(info)
    # # {'symbol': 'BTCUSDT', 'base': 'BTC', 'quote': 'USDT', 'isMarginTrade': True, 'isBuyAllowed': True, 'isSellAllowed': True}
    

    # # Get cross-margin magin symbolinfo
    # info = await client.get_margin_symbol(symbol='BTCUSDT')
    # symbol = Symbol(**info)
    # print(symbol.name)

    # #Get all isolated margin symbol info
    # info = await client.get_all_isolated_margin_symbols()
    # for item in info:
    #     symbol = Symbol(** item)
    #     print(symbol.symbol)


    # #Get margin price index
    # info = await client.get_margin_price_index(symbol='BTCUSDT')
    # my_price = PriceIndex(**info)
    # print(my_price.price)


    print("=================Order validation=======================")
    

    #==================================================================================
    # Place a margin order
    # Use the create_margin_order function to have full control over creating an order


    # #from binance.enums import *
    # order = client.create_margin_order(
    # symbol='BNBBTC',
    # side=SIDE_BUY,
    # type=ORDER_TYPE_LIMIT,
    # timeInForce=TIME_IN_FORCE_GTC,
    # quantity=100,
    # price='0.00001')

    #==================================================================================

    # Check order status
   
    # order = client.get_margin_order(
    # symbol='BNBBTC',
    # orderId='orderId')
    # await client.close_connection()
    

    #==================================================================================

    # Cancel a margin order
    # result = client.cancel_margin_order(
    # symbol='BNBBTC',
    # orderId='orderId')

    #==================================================================================

    # Get all open margin orders
    # orders = client.get_open_margin_orders(symbol='BNBBTC')
    # For isolated margin, add the isIsolated='TRUE' parameter.
    #==================================================================================

    # Get all margin orders
    # orders = client.get_all_margin_orders(symbol='BNBBTC')
    # For isolated margin, add the isIsolated='TRUE' parameter.


    print("==========================Account Management ============================")

    # # Get cross-margin account info
    # info = await client.get_margin_account()
    # account = Account.from_dict(info)
    # print(account.totalAssetOfBtc)

    # try:
    #     # Transfer spot to cross-margin account
    #     transaction = await client.transfer_spot_to_margin(asset='USDT', amount='1.0')
    #     print(type(transaction))
    #     print(transaction)
    # except Exception as e:
    #     print (e)

    # Transfer cross-margin account to spot
    #transaction = await client.transfer_margin_to_spot(asset='BTC', amount='1.1')

    print("====================Trades=========================")
    # Get all margin trades
    trades = await client.get_margin_trades(symbol='BNBBTC')
    # For isolated margin trades, add the isIsolated='TRUE' parameter.
    print(trades)

    # print("====================Loans=========================")

    # try:
    #     # Create loan
    #     transaction = await client.create_margin_loan(asset='USDT', amount='1.1')
    #     # This for the cross-margin account by default. For isolated margin, add
    #     # the isIsolated='TRUE' and the symbol=symbol_name parameters.
    #     print(transaction) #{'tranId': 191733908051, 'clientTag': ''}
    # except Exception as e:
    #     print(e)


    # Get cross-margin account info
    info = await client.get_margin_account()
    account = Account.from_dict(info)
    print(account.totalAssetOfBtc)

    try:
        print("=====================Get Loan Details-ALL or ONE=================")
        details = await client.get_margin_loan_details() # (asset='BTC', ttxId='100001')
        # For isolated margin records, add the isolatedSymbol=symbol_name parameter.
        transactionList = [Transaction.from_dict(trx) for trx in details['rows']]
        print([transaction.txId for transaction in transactionList])
    except Exception as e:
        print(e)

    try:
        print("====================Get repay details===================")
        # Get repay details
        details = await client.get_margin_repay_details() # (asset='USDT', amount='1.1' )
        # For isolated margin records, add the isolatedSymbol=symbol_name parameter.
        repay_details = [RepayDetails.from_dict(detail) for detail in details['rows']]
        print([f"total repay => {float(repay.amount) + float(repay.interest)} {type(repay.amount)}" for repay in repay_details])
    except Exception as e:
        print(e)


    # print("=============Repay Loan =====================")
    # try:
    #     # Repay loan
    #     transaction = await client.repay_margin_loan(asset='USDT', amount=1.10000693)
    #     print(transaction) # {'tranId': 191737724149, 'clientTag': ''}
    # except Exception as e:
    #     print(e)











    await client.close_connection()
if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())