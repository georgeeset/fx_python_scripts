from  .base import Base

class PriceIndex(Base):
    """
    Price model.

        arguments:
            symbol: string symbol
            price: current exchange price
            calcTime: calculated time
    """

    def __init__(self, symbol:str, price:float, calcTime:int):

        super().__init__(name="PriceIndex")

        self.symbol = symbol
        self.price = price
        self.calcTime = calcTime
    