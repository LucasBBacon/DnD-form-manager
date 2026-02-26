"""
Defines the Item class, which represents an item in the inventory, 
with properties such as name, weight, cost, and any special attributes.
The Item class also includes methods for calculating weight, 
applying templates, and handling container contents.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class DamageType(str, Enum):
    """
    Enumeration of possible damage types.
    """
    BLUDGEONING = "bludgeoning"
    PIERCING = "piercing"
    SLASHING = "slashing"
    ACID = "acid"
    COLD = "cold"
    FIRE = "fire"
    FORCE = "force"
    LIGHTNING = "lightning"
    NECROTIC = "necrotic"
    POISON = "poison"
    PSYCHIC = "psychic"
    RADIANT = "radiant"
    THUNDER = "thunder"


@dataclass
class ArmorClass:
    """
    Represents the armor class of an item, including base AC, 
    dexterity bonus, and any additional bonuses.
    """
    base: int = 0
    dex_bonus: bool = False
    max_dex_bonus: int = 0
    bonus: int = 0


@dataclass
class Item:
    """
    Represents an item in the inventory, with properties such as name, 
    weight, cost, and any special attributes.
    """
    name: str
    stackable: bool = False
    quantity: int = 1

    cost: Dict[str, int] = field(default_factory=lambda: {
        "cp": 0, "sp": 0, "ep": 0, "gp": 0, "pp": 0
    })

    category: Optional[str] = None
    equipped: bool = False
    base_weight: float = 0.0

    is_container: bool = False
    capacity_weight: float = 0.0
    contents: List['Item'] = field(default_factory=list)

    properties: List[str] = field(default_factory=list)

    damage_dice: Optional[str] = None
    damage_type: Optional[DamageType] = None
    range: Optional[str] = None
    armor_class: Optional[ArmorClass] = None
    strength_requirement: int = 0
    stealth_disadvantage: bool = False

    def __post_init__(self):
        pass

    @property
    def weight(self) -> float:
        """
        Calculates the total weight of the item, including any contents if it is a container.
        """
        total = self.base_weight
        if self.is_container:
            for item in self.contents:
                total += (item.weight * item.quantity)
        return total

    @weight.setter
    def weight(self, value: float) -> None:
        """
        Sets the base weight of the item.
        For containers, the total weight will be calculated dynamically based on contents.
        """
        self.base_weight = value

    @property
    def content_weight(self) -> float:
        """Calculates the total weight of the contents if this item is a container."""
        if not self.is_container:
            return 0.0
        return sum(item.weight * item.quantity for item in self.contents)

    def add_content(self, item: 'Item', count: int = 1) -> None:
        """
        Adds an item to the container, ensuring that the total weight does not exceed capacity.

        :param item: The item to be added to the container.
        :type item: 'Item'
        :param count: The number of items to be added (default is 1).
        :type count: int
        """
        if not self.is_container:
            raise ValueError(f"'{self.name}' is not a container.")

        added_weight = item.weight * item.quantity * count
        if (self.content_weight + added_weight) > self.capacity_weight:
            raise ValueError(
                f"Cannot add '{item.name}': Exceeds capacity of '{self.name}'")

        for _ in range(count):
            self.contents.append(item)

    def remove_content(self, item_name: str, count: int = 1) -> 'Item':
        """
        Removes an item from the container, 
        ensuring that the item exists and handling quantities appropriately.

        :param item_name: The name of the item to be removed from the container.
        :type item_name: str
        :param count: The number of items to be removed (default is 1).
        :type count: int
        :return: The item that was removed from the container.
        :rtype: Item
        """
        if not self.is_container:
            raise ValueError(f"'{self.name}' is not a container.")

        item = next((i for i in self.contents if i.name.strip(
        ).lower() == item_name.strip().lower()), None)
        if not item:
            raise ValueError(f"'{item_name}' was not found in '{self.name}'.")

        for _ in range(count):
            self.contents.remove(item)
        return item

    @staticmethod
    def parse_cost(cost_str: str) -> Dict[str, int]:
        """
        Parses a cost string into a dictionary of currency types and their amounts.

        :param cost_str: The cost string to be parsed (e.g., "10 gp").
        :type cost_str: str
        :return: A dictionary mapping currency types to their amounts.
        :rtype: Dict[str, int]
        """
        if not cost_str:
            return {}
        try:
            parts = cost_str.strip().split(' ')
            if len(parts) != 2:
                return {}

            amount = int(parts[0])
            currency = parts[1].lower()

            valid_currencies = ["cp", "sp", "ep", "gp", "pp"]
            if currency not in valid_currencies:
                return {}

            return {currency: amount}

        except (IndexError, ValueError):
            return {}

    def make_improvised(self) -> None:
        """Converts the item into an improvised thrown weapon, setting appropriate properties."""
        self.damage_dice = "1d4"
        self.range = "20/60"

    def apply_template(self, template_data: Dict) -> None:
        """
        Applies a template of properties to the item, 
        allowing for bulk updates of attributes based on predefined templates.

        :param template_data: The template data to be applied to the item.
        :type template_data: Dict
        """
        if 'weight' in template_data:
            self.weight = template_data['weight']

        if 'damage_dice' in template_data:
            self.damage_dice = template_data['damage_dice']

        if 'damage_type' in template_data:
            dtype_str = template_data['damage_type'].lower()
            try:
                self.damage_type = DamageType(dtype_str)
            except ValueError:
                pass

        if 'properties' in template_data:
            self.properties = template_data['properties']
            
        if 'stackable' in template_data:
            self.stackable = template_data['stackable']

        if 'range' in template_data:
            self.range = template_data['range']

        if 'category' in template_data:
            self.category = template_data['category']

        if 'cost' in template_data:
            if isinstance(template_data['cost'], str):
                parsed = self.parse_cost(template_data['cost'])
                print(parsed)
                self.cost.update(parsed)
            else:
                self.cost = template_data['cost']

        if 'armor_class' in template_data:
            ac_data = template_data['armor_class']
            self.armor_class = ArmorClass(
                base=ac_data.get('base', 0),
                dex_bonus=bool(ac_data.get('dex_bonus', False)),
                max_dex_bonus=ac_data.get('max_dex_bonus', 0),
                bonus=ac_data.get('bonus', 0)
            )

        if 'strength_requirement' in template_data:
            self.strength_requirement = template_data['strength_requirement']

        if 'stealth_disadvantage' in template_data:
            self.stealth_disadvantage = template_data['stealth_disadvantage']
