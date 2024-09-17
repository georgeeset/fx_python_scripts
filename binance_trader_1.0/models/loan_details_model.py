from .base import BaseModel
    


class Transaction(BaseModel):
    """
    handles details about loan
    """
    def __init__(self, timestamp: int, txId: int, asset: str, principal: float, status: str, clientTag: str):
        self.timestamp = timestamp
        self.txId = txId
        self.asset = asset
        self.principal = principal
        self.status = status    # CONFIRMED
        self.clientTag = clientTag


class RepayDetails(BaseModel):
    def __init__(self, timestamp: int, txId: int, asset: str, amount: str, principal: float, interest: float, status: str, clientTag: str):
        self.timestamp = timestamp
        self.txId = txId
        self.asset = asset
        self.amount = amount
        self.principal = principal
        self.interest = interest
        self.status = status
        self.clientTag = clientTag
