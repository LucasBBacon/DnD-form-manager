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
                return
        
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
        name_lower = name.lower().lower()
        return next((i for i in self.items if i.name.strip().lower() == name_lower), None)
    
    def has_item(self, name: str) -> bool:
        return self.get_item(name) is not None
    
    def get_item_count(self, name: str) -> int:
        item = self.get_item(name)
        return item.quantity if item else 0
    
    def equip_item(self, item_name: str) -> None:
        item = self.get_item(item_name)
        if not item:
            raise ValueError(f"Cannot equip: Item '{item_name}' not found.")
        item.equipped = True
        
    def unequip_item(self, item_name: str) -> None:
        item = self.get_item(item_name)
        if not item:
            raise ValueError(f"Cannot unequip: Item '{item_name}' not found.")
        item.equipped = False
        
    def get_total_weight(self) -> float:
        return sum(item.weight * item.quantity for item in self.items)
    
    def get_total_value_in_cp(self) -> int:
        total_cp = 0
        for item in self.items:
            item_value = 0
            item_value += item.cost.get('cp', 0)
            item_value += item.cost.get('sp', 0) * 10
            item_value += item.cost.get('ep', 0) * 50
            item_value += item.cost.get('gp', 0) * 100
            item_value += item.cost.get('pp', 0) * 1000

            total_cp += (item_value * item.quantity)
        
        return total_cp