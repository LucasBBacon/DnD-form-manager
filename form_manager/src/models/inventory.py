from dataclasses import dataclass, field
from typing import List, Optional

from form_manager.src.models.item import Item


@dataclass
class Inventory:
    items: List[Item] = field(default_factory=list)
    
    def add_item(self, item: Item, count: int = 1):
        if count > 1:
            item.quantity = count
        
        if item.stackable:
            existing_item = self.get_item(item.name)
            if existing_item:
                existing_item.quantity += count
        
        item.quantity = count
        self.items.append(item)
        
    def remove_item(self, item_name: str, count: int = 1):
        item = self.get_item(item_name)
        if not item:
            raise ValueError(f"Item '{item_name}' not found in inventory.")
        
        if item.stackable:
            item.quantity -= count
            if item.quantity <= 0:
                self.items.remove(item)
                
        else:
            self.items.remove(item)
        
    def get_item(self, name: str) -> Optional[Item]:
        name_lower = name.lower()
        return next((i for i in self.items if i.name.lower() == name_lower), None)
    
    def has_item(self, name: str) -> bool:
        return self.get_item(name) is not None
    
    def get_item_count(self, name: str) -> int:
        item = self.get_item(name)
        return item.quantity if item else 0