

class BaseModel:

    def __repr__(self):
        class_name = self.__class__.__name__
        properties = ', '.join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{class_name}({properties})"

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
    


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
