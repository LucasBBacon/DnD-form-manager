"""
Defines the Character class, which represents a character's attributes, inventory, and mechanics
such as encumbrance and pending choices. The Character class includes methods for calculating
carrying capacity, encumbrance status, effective speed, resolving pending choices, and paying costs.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List

from form_manager.src.models.inventory import Inventory
from form_manager.src.models.item import Item
from form_manager.src.services.currency_service import CurrencyService


class TargetType(str, Enum):
    """
    Enumeration of possible target types for pending choices.
    This helps to determine how to apply the user's selection when resolving a pending choice.
    """

    TOOL = "tool"
    SKILL = "skill"
    LANGUAGE = "language"
    SPELL = "spell"
    ABILITY_BONUS = "ability_bonus"
    DRACONIC_ANCESTRY = "draconic_ancestry"


@dataclass
class PendingChoice:
    """
    Represents a pending choice that the user must resolve,
    such as selecting a proficiency, language, or spell.
    """

    label: str
    options: List[str]
    count: int
    target_type: str
    level: int = 0
    choice_map: Dict[str, Any] = field(default_factory=dict)
    unique: bool = True


@dataclass
class Character:
    """
    Representation of a character and their attributes in memory.
    """

    class Size(str, Enum):
        """
        Enumeration of possible character sizes,
        which can affect carrying capacity and other mechanics.
        """

        SMALL = "Small"
        MEDIUM = "Medium"
        LARGE = "Large"

    class Encumbrance(str, Enum):
        """
        Enumeration of possible encumbrance statuses,
        which determine how much the character is encumbered based on their current weight
        and carrying capacity.
        """

        UNENCUMBERED = "Unencumbered"
        ENCUMBERED = "Encumbered"
        HEAVILY_ENCUMBERED = "Heavily Encumbered"
        OVER_CAPACITY = "Over Capacity"

    stats: Dict[str, int] = field(
        default_factory=lambda: {
            "strength": 10,
            "dexterity": 10,
            "constitution": 10,
            "intelligence": 10,
            "wisdom": 10,
            "charisma": 10,
        }
    )
    size: Size = Size.MEDIUM
    speed: int = 30
    languages: List[str] = field(default_factory=list)
    features: List[str] = field(default_factory=list)
    pending_choices: List[PendingChoice] = field(default_factory=list)

    proficiencies: Dict[str, List[str]] = field(
        default_factory=lambda: {"armor": [], "weapon": [], "tool": [], "skill": []}
    )
    resistances: List[str] = field(default_factory=list)

    inventory: Inventory = field(default_factory=Inventory)
    purse: Dict[str, int] = field(
        default_factory=lambda: {"cp": 0, "sp": 0, "ep": 0, "gp": 0, "pp": 0}
    )

    spells: Dict[str, List[str]] = field(
        default_factory=lambda: {
            "0": [],
            "1": [],
            "2": [],
            "3": [],
            "4": [],
            "5": [],
            "6": [],
            "7": [],
            "8": [],
            "9": [],
        }
    )
    breath_weapon: Dict[str, str] = field(default_factory=dict)

    use_variant_encumbrance: bool = False

    @property
    def size_multiplier(self) -> float:
        """
        Gets the size multiplier based on the character's size,
        which affects carrying capacity and encumbrance calculations.
        """
        if self.size == self.Size.LARGE:
            return 2.0
        return 1.0

    @property
    def carrying_capacity(self) -> float:
        """
        Calculates the character's carrying capacity based on their strength score,
        size multiplier, and the standard 15 lbs per point of strength.
        This is used to determine how much weight the character can carry before
        becoming encumbered.
        """
        strength_score = self.stats.get("strength", 10)
        return strength_score * 15 * self.size_multiplier

    @property
    def max_push_drag_lift(self) -> float:
        """
        Calculates the maximum weight the character can push, drag, or lift,
        which is typically double the carrying capacity.
        """
        return self.carrying_capacity * 2

    @property
    def current_weight(self) -> float:
        """
        Calculates the current total weight the character is carrying,
        including all items in the inventory and the weight of any coins
        in the purse (with a standard conversion of 50 cp = 1 lb).
        """
        total = self.inventory.get_total_weight()
        total_coins = sum(self.purse.values())
        total += total_coins / 50.0
        return total

    @property
    def encumbrance_status(self) -> "Encumbrance":
        """
        Determines the character's encumbrance status based on their current weight
        and carrying capacity, as well as whether the variant encumbrance rules are in use.
        """
        weight = self.current_weight
        cap = self.carrying_capacity
        strength = self.stats.get("strength", 10)
        size_multiplier = self.size_multiplier

        if weight > cap:
            return self.Encumbrance.OVER_CAPACITY

        if not self.use_variant_encumbrance:
            return self.Encumbrance.UNENCUMBERED

        if weight > (10 * strength * size_multiplier):
            return self.Encumbrance.HEAVILY_ENCUMBERED

        if weight > (5 * strength * size_multiplier):
            return self.Encumbrance.ENCUMBERED

        return self.Encumbrance.UNENCUMBERED

    @property
    def effective_speed(self) -> int:
        """
        Calculates the character's effective speed based on
        their base speed and encumbrance status.
        Encumbrance can reduce speed by 10 or 20 feet, or reduce it to 5 feet if over capacity.
        """
        status = self.encumbrance_status
        base = self.speed

        if status == self.Encumbrance.OVER_CAPACITY:
            return 5

        if status == self.Encumbrance.HEAVILY_ENCUMBERED:
            return max(0, base - 20)

        if status == self.Encumbrance.ENCUMBERED:
            return max(0, base - 10)

        return base

    @property
    def attuned_items(self) -> List["Item"]:
        """Returns a list of all currently attuned items in teh inventory."""
        return [
            item for item in self.inventory.items if getattr(item, "is_attuned", False)
        ]

    @property
    def attunement_slots_remaining(self) -> int:
        """Calculates remaining attunement slots (Base limit 3)"""
        return max(0, 3 - len(self.attuned_items))

    def choose(self, choice_label: str, selection: str) -> "Character":
        """
        Resolves a pending choice for the character based on the user's selection,
        applying the appropriate effects to the character's attributes, proficiencies, or spells.

        :param choice_label: The label of the pending choice to resolve.
        :type choice_label: str
        :param selection: The user's selection for the choice.
        :type selection: str
        :return: The character instance with the choice applied.
        :rtype: Character
        """
        choice_obj = next(
            (c for c in self.pending_choices if c.label == choice_label), None
        )
        if not choice_obj:
            raise ValueError(f"No pending choice found for '{choice_label}'")

        # Validation
        selection = selection.lower()
        if choice_obj.options and selection not in choice_obj.options:
            raise ValueError(f"'{selection}' is not a valid option for {choice_label}")

        # Logic
        match choice_obj.target_type:
            case TargetType.TOOL:
                self.proficiencies["tool"].append(selection)

            case TargetType.SKILL:
                self.proficiencies["skill"].append(selection)

            case TargetType.LANGUAGE:
                self.languages.append(selection.title())

            case TargetType.SPELL:
                level = str(getattr(choice_obj, "level", "0"))
                self.spells[level].append(selection)

            case TargetType.ABILITY_BONUS:
                bonus = choice_obj.level if choice_obj.level else 1
                if selection in self.stats:
                    self.stats[selection] += bonus
                else:
                    raise ValueError(f"Invalid ability score: {selection}")

            case TargetType.DRACONIC_ANCESTRY:
                payload = choice_obj.choice_map.get(selection, {})
                if "damage_type" in payload:
                    self.resistances.append(payload["damage_type"])
                if "breath_weapon" in payload:
                    self.breath_weapon = payload["breath_weapon"]
                    self.breath_weapon["damage_type"] = payload.get("damage_type")

            case _:
                return self

        # Optional Consumption
        if choice_obj.unique and selection in choice_obj.options:
            choice_obj.options.remove(selection)

        # Counter
        choice_obj.count -= 1
        if choice_obj.count <= 0:
            self.pending_choices.remove(choice_obj)

        return self

    def pay_cost(self, cost: Dict[str, int], currency_service: CurrencyService) -> bool:
        """
        Pays a specified cost from the character's purse, if they have sufficient funds.

        :param cost: The cost to be paid,
        represented as a dictionary of currency types and their values.
        :type cost: Dict[str, int]
        :param currency_service: The service used to convert and manage currency.
        :type currency_service: CurrencyService
        :return: True if the cost was successfully paid, False otherwise.
        :rtype: bool
        """
        current_wealth = currency_service.convert_purse_to_cp(self.purse)
        cost_value = currency_service.convert_purse_to_cp(cost)

        if current_wealth < cost_value:
            return False

        remaining_wealth = current_wealth - cost_value
        self.purse = currency_service.optimize_purse(remaining_wealth)
        return True

    def attune_item(self, item_name: str) -> None:
        """Attempts to attune to an item. Raises ValueError if rules violated."""
        matching_items = [
            i for i in self.inventory.items if i.name.lower() == item_name.lower()
        ]
        if not matching_items:
            raise ValueError(f"Cannot attune: '{item_name}' not found in inventory.")

        item = next(
            (i for i in matching_items if not getattr(i, "is_attuned", False)),
            matching_items[0],
        )

        if not getattr(item, "requires_attunement", False):
            raise ValueError(f"'{item_name}' does not require attunement.")

        if getattr(item, "is_attuned", False):
            return

        if any(i.name == item.name for i in self.attuned_items):
            raise ValueError(f"Already attuned to an item named '{item_name}'.")

        if self.attunement_slots_remaining <= 0:
            raise ValueError("No attunement slots remaining.")

        item.is_attuned = True

    def unattune_item(self, item_name: str) -> None:
        item = self.inventory.get_item(item_name)
        if not item:
            raise ValueError(f"Cannot unattune: '{item_name}' not found in inventory.")

        item.is_attuned = False
