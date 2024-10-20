from binance import AsyncClient
from binance.enums import *
from models.symbol_model import Symbol
from models.assets_model import CrossAcct
from models.isolated_account_info_model import IsolatedAcct
from models.loan_details_model import Loan, RepayDetails


class BinanceMargin:
    """
    class handles cross and isolated margin opteraions
    """
    def __init__ (self, is_isolated):
        self.is_isolated = is_isolated
        self.client = None

    async def initialize_client(self, api_key:str, api_secret:str):
         """must initialize client """
         self.client = await AsyncClient.create(
            api_key=api_key,
            api_secret=api_secret,
            testnet=True
    )

    async def get_all_open_margin_orders(self, symbol:str, limit:int=10) -> dict:
        """
        get all open cross margin order

        args:
            symbol: currency symbol
            limit: result limit default is 10
        returns: List of Orders
        """
        try: # Allmargin orders
            orders = await self.client.get_open_margin_orders(symbol=symbol, isIsolated = self.is_isolated, limit=limit)
            return orders
        except Exception as e:
            raise ValueError(f"failed to get all cross margin orders {e}")

    async def get_margin_symbol_info(self, symbol:str):
        """
        Get margin symbol information
        """
        info = None
        if self.is_isolated:
            info = await self.client.get_isolated_margin_symbol(symbol=symbol)
        else:
            info = await self.client.get_margin_symbol(symbol=symbol)
        return Symbol(**info)
    
    async def get_cross_margin_account_info(self, symbol:str):
        """
        get margin account information
        """

        info = await self.client.get_margin_account(symbol = symbol, isIsolated=self.is_isolated)
        return info

    async def place_margin_limit_order(self, symbol:str, side:str, entry_price:float, quantity:float,order_type:str):
        """
         Use the create_margin_order function to have full
         control over creating an order
         for both isolated and cross margin
        """
        try:
            order = await self.client.create_margin_order(
            symbol= symbol,
            side=side,
            type=ORDER_TYPE_LIMIT,
            timeInForce=TIME_IN_FORCE_GTC,
            quantity=quantity,
            price=entry_price,
            isIsolated=self.is_isolated,
            sideEffectType=AUTO_REPAY_TYPE
            )
            return order
        except Exception as e:
            raise ValueError(f"failed to place margin Limit order: {e}")

    async def place_margin_stop_order(self, symbol:str, side:str, limit_price:float, stop_price:float, quantity:float):
        """
        Use the create a stop_limit order function to have full
        control over creating an order
        """
        try:
            order = await self.client.create_margin_order(
            symbol= symbol,
            side=side,
            type=ORDER_TYPE_STOP_LOSS_LIMIT,
            timeInForce=TIME_IN_FORCE_GTC,
            quantity=quantity,
            price=limit_price,
            stopPrice=stop_price,
            isIsolated=self.is_isolated,
            sideEffectType=AUTO_REPAY_TYPE
            )
            return order
        except Exception as e:
            raise ValueError(f"failed to place margin Stop order: {e}")

    async def check_order_status(self, symbol:str, order_id:int):
        """ 
        Check order status

        args:
            orderid: id or order
        """
        order = await self.client.get_margin_order(
        symbol=symbol,
        orderId= order_id)

        return order

    async def cancle_order(self, symbol:str, order_id:int):
        """
        Cancel a margin order
        """
        result = await self.client.cancel_margin_order(
        symbol=symbol,
        orderId=order_id
        )
        return result

    async def create_oco_order(self, symbol:str, side:str, quantity:float, tp:float, sl:float, sl2:float):
        """
        Createe an oco order for sl and tp

        args:
            side: you SELL if you already bought and you want a sell order
                you BUY if you already  sold and you want a buy order
        """

        try:
            order = await self.client.create_margin_oco_order(
                symbol = symbol,
                side = side,
                quantity = quantity,
                price = tp,
                stopPrice = sl,
                stopLimitPrice = sl2,
                stopLimitTimeInForce = 'GTC'
            )
        except Exception as e:
            print(f"Error creating oco {e}")

        return order

    async def symbol_allow_orders(self, symbol):
        """
        check symbol information and confirm if the symbol supports orders or not
        """

        info = await self.client.get_symbol_info(symbol=symbol)
        return info

    async def transfer_spot_to_margin(self, asset:str, amount:float, symbol=None):
        """
            Transfer spot to margin account

            args:
                symbol: Is necessary for isolated margin
                asset: asset to be transfered
                amount: cash to be transfered
        """
        try:
            if self.is_isolated:
                if symbol is None:
                    raise ValueError("transfer spot to margin failed: Symbol is needed")
                response = await self.client.transfer_spot_to_isolated_margin(asset=asset,  amount=2.0, symbol=symbol)
                return response
            else:
                transaction = await self.client.transfer_spot_to_margin(asset=asset, amount=amount)
                return transaction

        except Exception as e:
            raise ValueError(f"failed to transfer sport to cross margin: {e}")

    async def transfer_margin_to_sport(self, symbol:str, amount:float):
        """
        Transfer cross-margin account to spot
        """
        if self.is_isolated:
            response = await self.client.transfer_isolated_margin_to_spot(asset=symbol,  amount=amount)
            return response
        else:
            response = await self.client.transfer_margin_to_spot(asset=symbol, amount=amount)
            return response

    async def open_market_position(self, symbol:str, side:str, quantity:float):
        """
        Open position
        """
        try:
            # Place the margin order
            order = await self.client.create_margin_order(
            symbol=symbol,
            side=side,
            type= ORDER_TYPE_MARKET,
            quantity=quantity,
            isIsolated=self.is_isolated,  # Important for isolated margin
            sideEffectType='AUTO_BORROW_REPAY'
            )
            print(order)
        except Exception as e:
            print(e)

    async def get_all_margin_trades(self, symbol:str):
        """
        Get all margin trades
        For isolated margin trades, add the isIsolated='TRUE' parameter.
        """
        trades = await self.client.get_margin_trades(symbol=symbol, isIsolated=self.is_isolated)
        return trades

    async def get_loan_details(self)->list:
        """
        For isolated margin records, add the isolatedSymbol parameter.
        """
        try:
            details = await self.client.get_margin_loan_details(isIsolated = self.is_isolated) # (asset='BTC', ttxId='100001')
            transactionList = [Loan.from_dict(trx) for trx in details['rows']]
            return [transaction for transaction in transactionList]
        except Exception as e:
            raise ValueError(f"get loan details failed: {e}")

    async def get_repay_details(self)->list:
        """
        Get repay details
        For isolated margin records,
        add the isolatedSymbol=True.
        """
        try:
            details = await self.client.get_margin_repay_details(isIsolated=self.is_isolated)
            repay_details = [RepayDetails.from_dict(detail) for detail in details['rows']]
            return repay_details
        except Exception as e:
            raise ValueError(f"failed to get repay details: {e}")

    async def repay_loan(self, asset:str, amount:float):
        """
        Repay loan
        """
        try:
            transaction = await self.client.repay_margin_loan(asset=asset, amount=amount, isIsolated = self.is_isolated)
            return transaction # {'tranId': 191737724149, 'clientTag': ''}
        except Exception as e:
            raise ValueError(f"failed to repay loan: {e}")

    async def max_loan_amount(self, symbol:str):
        """
        Get max loan amount
        For isolated margin records, add the isolatedSymbol=symbol_name parameter.
        """
        details = await self.client.get_max_margin_loan(asset=symbol, isIsolated = self.is_isolated)
        return details

    async def close(self):
        """
        close connection
        """
        await self.client.close_connection()

    def helper(self):
        """
        view help for you functions here
        """
        help(self.client.create_margin)
