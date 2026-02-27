"""
RulesManager is responsible for loading and providing access to game
rules and data from JSON files,
such as races, traits, languages, spells, and more.
"""

import json
import os
from typing import Any, Dict


class RulesManager:
    """
    Manager for loading and providing access to game rules
    and data from JSON files.
    """

    def __init__(self, resources_dir: str) -> None:
        self.resources_dir = resources_dir
        self.__cache = {}

    def _load_json(self, relative_path: str) -> Dict[str, Any]:
        if relative_path in self.__cache:
            return self.__cache[relative_path]

        full_path = os.path.join(self.resources_dir, relative_path)
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.__cache[relative_path] = data
                return data
        except FileNotFoundError:
            print(f"Warning: Resource not found at {full_path}")
            return {}

    @property
    def races(self) -> Dict:
        """Loads and returns the race data from the JSON file."""
        return self._load_json("races/race_data.json")

    @property
    def traits(self) -> Dict:
        """Loads and returns the trait data from the JSON file."""
        return self._load_json("races/traits_data.json")

    @property
    def languages(self) -> Dict:
        """Loads and returns the language data from the JSON file."""
        return self._load_json("rules/languages.json")

    @property
    def spells(self) -> Dict:
        """Loads and returns the spell data from the JSON file."""
        return self._load_json("spells/spell_list.json")

    @property
    def draconic_ancestry(self) -> Dict:
        """Loads and returns the draconic ancestry data from the JSON file."""
        return self._load_json("rules/draconic_ancestry.json")

    @property
    def skills(self) -> Dict:
        """Loads and returns the skill data from the JSON file."""
        return self._load_json("rules/skills.json")

    @property
    def weapons(self) -> Dict:
        """Loads and returns the weapon data from the JSON file."""
        return self._load_json("rules/weapons.json")

    @property
    def armor(self) -> Dict:
        """Loads and returns the armor data from the JSON file."""
        return self._load_json("rules/armors.json")

    @property
    def adventuring_gear(self) -> Dict:
        """Loads and returns the adventuring gear data from the JSON file."""
        return self._load_json("items/adventuring_gear.json")

    @property
    def currency(self) -> Dict:
        """Loads and returns the currency data from the JSON file."""
        return self._load_json("rules/currency.json")

    def get_item_template(self, name: str) -> Dict:
        """
        Retrieves the item template for a given item name,
        searching through weapons, armor, and adventuring gear.

        :param name: The name of the item to retrieve the template for.
        :type name: str
        :return: The item template if found, otherwise an empty dictionary.
        :rtype: Dict[Any, Any]
        """
        key = name.lower().replace(" ", "_").replace("'", "")
        sources = [self.weapons, self.armor, self.adventuring_gear]
        
        for source in sources:
            if key in source:
                template = dict(source[key])
                if 'cost' in template and isinstance(template['cost'], str):
                    print(self._parse_cost_string(template['cost']))
                    template['cost'] = self._parse_cost_string(template['cost'])
                return template
        return {}

    def _parse_cost_string(self, cost_str: str) -> Dict[str, int]:
        if not cost_str:
            return {}

        try:
            parts = cost_str.strip().split(" ")
            if len(parts) != 2:
                return {}
            amount = int(parts[0])
            currency_code = parts[1].lower()
            valid_currencies = [code.lower() for code in self.currency.keys()]
            if currency_code in valid_currencies:
                return {currency_code: amount}
        except (IndexError, ValueError):
            pass
        return {}
