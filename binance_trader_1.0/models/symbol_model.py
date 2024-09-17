from dataclasses import dataclass
from .base import BaseModel


class Symbol(BaseModel):

    def __init__(self, symbol:str, base:str, quote:str, isMarginTrade:bool, isBuyAllowed:bool, isSellAllowed:bool):
        
        self.symbol = symbol
        self.base = base
        self.quote = quote
        self.isMarginTrade = isMarginTrade
        self.isBuyAllowed = isBuyAllowed
        self.isSellAllowed = isSellAllowed

       