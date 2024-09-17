


from typing import List


class Asset:
    """
    Cross Margin trading asset
    """
    def __init__(self, asset:str, free:float, locked:float, borrowed:float, interest:float, netAsset:float):

        self.asset = asset
        self.free = free
        self.locked = locked
        self.borrowed = borrowed
        self.interest = interest
        self.netAsset = netAsset


    def __repr__(self):
        return f"Asset(id={self.asset} free='{self.free}', locked ={self.locked}, borrowed = {self.borrowed}, interest = {self.interest}, net asset = {self.netAsset})"

    @classmethod
    def from_dict(cls, data: dict):
        return cls(asset=data['asset'], free=data['free'],
                   locked=data['locked'], borrowed=data['borrowed'],
                   interest = data['interest'], netAsset = data['netAsset']
                   )


class CrossAcct:

    """
    Account information
    cross margin
    """

    def __init__(self, tradeEnabled:bool, transferEnabled:bool,
                 transferInEnabled:bool, transferOutEnabled:bool,
                 borrowEnabled:bool, marginLevel:float, totalAssetOfBtc:float,
                 totalLiabilityOfBtc:float, totalNetAssetOfBtc:float, userAssets:List[Asset]):
        self.tradeEnabled = tradeEnabled
        self.transferEnabled = transferEnabled
        self.transferInEnabled = transferInEnabled
        self.transferOutEnabled = transferOutEnabled
        self.borrowEnabled = borrowEnabled
        self.marginLevel = marginLevel
        self.totalAssetOfBtc = totalAssetOfBtc
        self.totalLiabilityOfBtc = totalLiabilityOfBtc
        self.totalNetAssetOfBtc = totalNetAssetOfBtc
        self.userAssets = userAssets if userAssets is not None else []

    @classmethod
    def from_dict(cls, data:dict):
        assets = [Asset.from_dict(asset) for asset in data.get('assets', [])]
        return cls(tradeEnabled=data['tradeEnabled'], transferEnabled = data['transferEnabled'], transferInEnabled = data['transferInEnabled'],
                   transferOutEnabled=data['transferOutEnabled'], borrowEnabled=data['borrowEnabled'], totalNetAssetOfBtc = data['totalNetAssetOfBtc'],
                   marginLevel = data['marginLevel'], totalAssetOfBtc = data['totalAssetOfBtc'],
                    totalLiabilityOfBtc = data['totalLiabilityOfBtc'],   userAssets=assets)

    def add_asset(self, asset: Asset):
        self.userAssets.append(asset)

    def __repr__(self):
        return f"Account(id={self.id}, owner='{self.owner}', assets="