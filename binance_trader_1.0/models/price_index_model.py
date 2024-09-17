from  .base import BaseModel

class PriceIndex(BaseModel):
    """
    Price model.

        arguments:
            symbol: string symbol
            price: current exchange price
            calcTime: calculated time
    """

    def __init__(self, symbol:str, price:float, calcTime:int):

        self.symbol = symbol
        self.price = price
        self.calcTime = calcTime
    