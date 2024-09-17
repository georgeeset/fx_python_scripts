from .base import BaseModel


class BaseQuoteAsset(BaseModel):
    def __init__(self, asset: str, borrowEnabled: bool, borrowed: str, free: str, interest: str, locked: str, netAsset: str, netAssetOfBtc: str, repayEnabled: bool, totalAsset: str):
        self.asset = asset
        self.borrowEnabled = borrowEnabled
        self.borrowed = borrowed
        self.free = free
        self.interest = interest
        self.locked = locked
        self.netAsset = netAsset
        self.netAssetOfBtc = netAssetOfBtc
        self.repayEnabled = repayEnabled
        self.totalAsset = totalAsset



class Asset(BaseModel):
    def __init__(self, baseAsset: dict, quoteAsset: dict, symbol: str, isolatedCreated: bool, marginLevel: str, marginLevelStatus: str, marginRatio: str, indexPrice: str, liquidatePrice: str, liquidateRate: str, tradeEnabled: bool, enabled: bool):
        self.baseAsset = BaseQuoteAsset.from_dict(baseAsset)
        self.quoteAsset = BaseQuoteAsset.from_dict(quoteAsset)
        self.symbol = symbol
        self.isolatedCreated = isolatedCreated
        self.marginLevel = marginLevel
        self.marginLevelStatus = marginLevelStatus
        self.marginRatio = marginRatio
        self.indexPrice = indexPrice
        self.liquidatePrice = liquidatePrice
        self.liquidateRate = liquidateRate
        self.tradeEnabled = tradeEnabled
        self.enabled = enabled



class IsolatedAcct(BaseModel):
    """
    Isolated Margin Account detail
    """
    def __init__(self, assets: list[dict], totalAssetOfBtc: str, totalLiabilityOfBtc: str, totalNetAssetOfBtc: str):
        self.assets = [Asset.from_dict(asset) for asset in assets]
        self.totalAssetOfBtc = totalAssetOfBtc
        self.totalLiabilityOfBtc = totalLiabilityOfBtc
        self.totalNetAssetOfBtc = totalNetAssetOfBtc