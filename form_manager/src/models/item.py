from dataclasses import dataclass


@dataclass
class Item:
    name: str
    stackable: bool = False
    