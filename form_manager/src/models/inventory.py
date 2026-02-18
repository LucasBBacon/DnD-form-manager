"""
Defines the Inventory class, which manages a character's inventory of items, 
including adding, removing, equipping, and calculating total weight and value.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from form_manager.src.models.item import Item


@dataclass
class Inventory:
    """Represents a character's inventory, managing items and their interactions."""

    items: List[Item] = field(default_factory=list)

    def add_item(self, item: Item, count: int = 1) -> None:
        """
        Adds an item to the inventory, handling stackable items and quantities appropriately.
        
        :param item: The item to be added to the inventory.
        :type item: Item
        :param count: The number of items to be added (default is 1).
        :type count: int
        """
        if count > 1:
            item.quantity = count

        if item.stackable:
            existing_item = self.get_item(item.name)
            if existing_item:
                existing_item.quantity += count
                return

        item.quantity = count
        self.items.append(item)

    def remove_item(self, item_name: str, count: int = 1) -> None:
        """
        Removes an item from the inventory, handling stackable items and quantities appropriately.
        
        :param item_name: The name of the item to be removed from the inventory.
        :type item_name: str
        :param count: The number of items to be removed (default is 1).
        :type count: int
        """
        item = self.get_item(item_name)
        if not item:
            raise ValueError(f"Item '{item_name}' not found in inventory.")

        if item.stackable:
            item.quantity -= count
            if item.quantity <= 0:
                self.items.remove(item)
        else:
            self.items.remove(item)

    def move_item_to_container(self, item_name: str, container_name: str, count: int = 1) -> None:
        """
        Moves an item from the top-level inventory into a specified container, 
        handling stackable items and quantities appropriately.
        
        :param item_name: The name of the item to be moved.
        :type item_name: str
        :param container_name: The name of the container to move the item into.
        :type container_name: str
        :param count: The number of items to be moved (default is 1).
        :type count: int
        """
        item = self.get_item(item_name)
        if not item:
            raise ValueError(f"Item '{item_name}' not found in inventory.")

        container = self.get_item(container_name)
        if not container:
            raise ValueError(f"Container '{container_name}' not found.")

        container.add_content(item)

        if item.stackable:
            item.quantity -= count
            if item.quantity <= 0:
                self.items.remove(item)
        else:
            self.items.remove(item)

    def remove_item_from_container(self, item_name: str, container_name: str, count: int = 1):
        """
        Removes an item from a container in the inventory, 
        handling stackable items and quantities appropriately.
        
        :param item_name: The name of the item to be removed from the container.
        :type item_name: str
        :param container_name: The name of the container from which the item is to be removed.
        :type container_name: str
        :param count: The number of items to be removed (default is 1).
        :type count: int
        """
        container = self.get_item(container_name)
        if not container:
            raise ValueError(f"Container '{container_name}' not found.")
        item_removed = container.remove_content(item_name, count)
        self.add_item(item_removed, count)

    def get_item(self, name: str) -> Optional[Item]:
        """
        Gets an item from the inventory by name, case-insensitively.
        
        :param name: The name of the item to retrieve.
        :type name: str
        :return: The item if found, otherwise None.
        :rtype: Item | None
        """
        name_lower = name.lower().strip()
        return next((i for i in self.items if i.name.strip().lower() == name_lower), None)

    def has_item(self, name: str) -> bool:
        """
        Checks if an item exists in the inventory by name, case-insensitively.
        
        :param name: The name of the item to check for.
        :type name: str
        :return: True if the item exists, otherwise False.
        :rtype: bool
        """
        return self.get_item(name) is not None

    def get_item_count(self, name: str) -> int:
        """
        Gets the quantity of a specified item in the inventory, 
        handling stackable items appropriately.
        
        :param name: The name of the item to count.
        :type name: str
        :return: The quantity of the item if found, otherwise 0.
        :rtype: int
        """
        item = self.get_item(name)
        return item.quantity if item else 0

    def equip_item(self, item_name: str) -> None:
        """
        Equips an item in the inventory.
        
        :param item_name: The name of the item to equip.
        :type item_name: str
        """
        item = self.get_item(item_name)
        if not item:
            raise ValueError(f"Cannot equip: Item '{item_name}' not found.")
        item.equipped = True

    def unequip_item(self, item_name: str) -> None:
        """
        Unequips an item in the inventory.
        
        :param item_name: The name of the item to unequip.
        :type item_name: str
        """
        item = self.get_item(item_name)
        if not item:
            raise ValueError(f"Cannot unequip: Item '{item_name}' not found.")
        item.equipped = False

    def get_total_weight(self) -> float:
        """
        Gets the total weight of all items in the inventory.
        
        :return: The total weight of all items in the inventory.
        :rtype: float
        """
        return sum(item.weight * item.quantity for item in self.items)

    def get_total_value_in_cp(self) -> int:
        """
        Calculates the total value of all items in the inventory, 
        converting all currency types to copper pieces (cp) for a unified total.
        
        :return: The total value of all items in the inventory, in copper pieces.
        :rtype: int
        """
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
