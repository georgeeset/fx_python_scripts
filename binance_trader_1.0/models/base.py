
from dataclasses import dataclass
import time


@dataclass
class Base:
    """
    Base model class.

    Attributes:
        id (int): The unique identifier.
        name (str): The name of the model.
    """

    def __init__(self, name:str, id:int = 0):
        self.id = id or time.time()
        self.name = name
