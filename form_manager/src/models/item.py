from dataclasses import dataclass


@dataclass
class Item:
    name: str
    stackable: bool = False
    quantity: int = 1
    
    def __post_init__(self):
        pass
    