"""
CurrencyService is responsible for handling currency-related operations,
such as normalization, conversion, and optimization of purses.
"""

from typing import Dict, Optional

from form_manager.src.models.inventory import Inventory
from form_manager.src.services.rules_manager import RulesManager


class CurrencyService:
    """Service for handling currency-related operations."""

    def __init__(self, rules_manager: RulesManager) -> None:
        self.data = rules_manager.currency
        self._alias_map = {}
        for code, info in self.data.items():
            for alias in info.get("aliases", []):
                self._alias_map[alias.lower()] = code

    def normalize_currency(self, name: str) -> Optional[str]:
        """
        Normalizes a currency name to its standard code using aliases.

        :param name: The name or alias of the currency to normalize.
        :type name: str
        :return: The standard currency code if found, otherwise None.
        :rtype: str | None
        """
        return self._alias_map.get(name.lower())

    def get_value_in_cp(self, currency_node: str) -> int:
        """
        Retrieves the value of a currency in copper pieces (cp).

        :param currency_node: The currency node (e.g., 'gp', 'sp') to get the value for.
        :type currency_node: str
        :return: The value of the currency in copper pieces.
        :rtype: int
        """
        return self.data.get(currency_node, {}).get("value", 0)

    def convert_purse_to_cp(self, purse: Dict[str, int]) -> int:
        """
        Converts a purse of various currencies into its total value in copper pieces (cp).

        :param purse: A dictionary mapping currency codes to their amounts.
        :type purse: Dict[str, int]
        :return: The total value of the purse in copper pieces.
        :rtype: int
        """
        total = 0
        for currency, amount in purse.items():
            total += amount * self.get_value_in_cp(currency_node=currency)
        return total

    def optimize_purse(self, total_cp: int, use_pp: bool = False) -> Dict[str, int]:
        """
        Optimizes a purse to contain the least number of coins
        for a given total value in copper pieces (cp).

        :param total_cp: The total value in copper pieces to optimize into a purse.
        :type total_cp: int
        :param use_pp: If True, allows auto-conversion into Platinum Pieces (pp).
        :type use_pp: bool
        :return: A dictionary mapping currency codes to their optimized amounts.
        :rtype: Dict[str, int]
        """
        sorted_currencies = sorted(
            self.data.keys(), key=lambda k: self.data[k]["value"], reverse=True
        )

        new_purse = {k: 0 for k in self.data}
        remaining = total_cp

        for code in sorted_currencies:
            if code == "ep" or (code == "pp" and not use_pp):
                continue

            value = self.data[code]["value"]
            if value > 0:
                count = remaining // value
                new_purse[code] = count
                remaining %= value

        return new_purse
    
    def calculate_inventory_value(self, inventory: 'Inventory') -> int:
        """Calculates the total value of all items in the inventory in CP."""
        total_cp = 0
        for item in inventory.items.values():
            item_cp = self.convert_purse_to_cp(item.cost)
            total_cp += (item_cp * item.quantity)
        return total_cp
