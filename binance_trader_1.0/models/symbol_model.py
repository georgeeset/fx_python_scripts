from dataclasses import dataclass
from .base import Base


@dataclass
class Symbol(Base):

    def __init__(self,symbol:str, base:str, quote:str, isMarginTrade:bool, isBuyAllowed:bool, isSellAllowed:bool, id:int = 0, ):
        
        super().__init__(id, name='Symbol')

        self.symbol = symbol
        self.base = base
        self.quote = quote
        self.isMarginTrade = isMarginTrade
        self.isBuyAllowed = isBuyAllowed
        self.isSellAllowed = isSellAllowed

       