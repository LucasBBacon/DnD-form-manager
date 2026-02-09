from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Item:
    name: str
    stackable: bool = False
    quantity: int = 1
    category: Optional[str] = None
    properties: List[str] = field(default_factory=list)
    equipped: bool = False
    
    def __post_init__(self):
        pass
    