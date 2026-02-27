"""
Defines the Inventory class, which manages a character's inventory of items,
including adding, removing, equipping, and calculating total weight and value.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from form_manager.src.models.item import Item


@dataclass
class Inventory:
    """Represents a character's inventory, managing items and their interactions."""

    items: Dict[str, Item] = field(default_factory=dict)
    top_level_ids: List[str] = field(default_factory=list)

    def get_item(self, name_or_id: str) -> Optional[Item]:
        """
        Deep search. Finds an item by UUID first, fallback to Name.

        :param name_or_id: The name of the item to retrieve.
        :type name_or_id: str
        :return: The item if found, otherwise None.
        :rtype: Item | None
        """
        if name_or_id in self.items:
            return self.items[name_or_id]
        name_lower = name_or_id.lower()
        for item in self.items.values():
            if item.name.lower() == name_lower:
                return item
        return None

    def add_item(self, item: Item, count: int = 1) -> str:
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
            existing_id = next(
                (
                    i_id
                    for i_id in self.top_level_ids
                    if self.items[i_id].name.lower() == item.name.lower()
                ),
                None,
            )
            if existing_id:
                self.items[existing_id].quantity += item.quantity
                return existing_id

        self.items[item.id] = item
        self.top_level_ids.append(item.id)
        return item.id

    def remove_item(self, name_or_id: str, count: int = 1) -> None:
        """
        Removes an item from the inventory, handling stackable items and quantities appropriately.

        :param name_or_id: The name of the item to be removed from the inventory.
        :type name_or_id: str
        :param count: The number of items to be removed (default is 1).
        :type count: int
        """
        item = self.get_item(name_or_id)
        if not item:
            raise ValueError(f"Item '{name_or_id}' not found in inventory.")

        if item.stackable and item.quantity > count:
            item.quantity -= count
            return

        if item.id in self.top_level_ids:
            self.top_level_ids.remove(item.id)

        for parent in self.items.values():
            if item.id in parent.content_ids:
                parent.content_ids.remove(item.id)

        del self.items[item.id]

    def get_item_total_weight(self, item_id: str) -> float:
        item = self.items.get(item_id)
        if not item:
            return 0.0

        total = item.weight
        if item.is_container:
            for child_id in item.content_ids:
                total += self.get_item_total_weight(child_id)
        return total

    def unpack_container(self, container_name: str) -> None:
        """Dumps container contents to the top-level inventory."""
        container = self.get_item(container_name)
        if not container:
            raise ValueError("Container not found.")
        if not container.is_container:
            raise ValueError(f"'{container.name}' is not a container.")
        for child_id in list(container.content_ids):
            container.content_ids.remove(child_id)
            self.top_level_ids.append(child_id)

    def move_item_to_container(
        self, item_name_or_id: str, container_name_or_id: str, count: int = 1
    ) -> None:
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
        item = self.get_item(item_name_or_id)
        container = self.get_item(container_name_or_id)

        if not item:
            raise ValueError("Item not found.")
        if not container:
            raise ValueError("Container not found.")
        if not container.is_container:
            raise ValueError(f"'{container.name}' is not a container.")

        current_contents_weight = sum(
            self.get_item_total_weight(cid) for cid in container.content_ids
        )
        added_weight = self.get_item_total_weight(item.id)
        if (current_contents_weight + added_weight) > container.capacity_weight:
            raise ValueError(f"Exceeds capacity of '{container.name}'.")

        if item.id in self.top_level_ids:
            self.top_level_ids.remove(item.id)

        if item.stackable:
            existing_id = next(
                (
                    c_id
                    for c_id in container.content_ids
                    if self.items[c_id].name.lower() == item.name.lower()
                ),
                None,
            )
            if existing_id:
                self.items[existing_id].quantity += item.quantity
                del self.items[item.id]
                return

        container.content_ids.append(item.id)

    def remove_item_from_container(
        self, item_name_or_id: str, container_name_or_id: str, count: int = 1
    ):
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

        item = self.get_item(item_name_or_id)
        container = self.get_item(container_name_or_id)

        if not item:
            raise ValueError("Item not found.")
        if not container:
            raise ValueError("Container not found.")
        if not container.is_container:
            raise ValueError(f"'{container.name}' is not a container.")

        container.content_ids.remove(item.id)
        self.add_item(item, count)

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

    def get_total_weight(self) -> float:
        """
        Gets the total weight of all items in the inventory.

        :return: The total weight of all items in the inventory.
        :rtype: float
        """
        return sum(self.get_item_total_weight(i_id) for i_id in self.top_level_ids)

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
