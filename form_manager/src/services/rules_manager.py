import json
import os
from typing import Any, Dict


class RulesManager:
    def __init__(self, resources_dir: str) -> None:
        self.resources_dir = resources_dir
        self.__cache = {}
        
    def _load_json(self, relative_path: str) -> Dict[str, Any]:
        if relative_path in self.__cache:
            return self.__cache[relative_path]
        
        full_path = os.path.join(self.resources_dir, relative_path)
        try:
            with open(full_path, 'r') as f:
                data = json.load(f)
                self.__cache[relative_path] = data
                return data
        except FileNotFoundError:
            print(f"Warning: Resource not found at {full_path}")
            return {}
        
    @property
    def races(self) -> Dict:
        return self._load_json('races/race_data.json')
    
    @property
    def traits(self) -> Dict:
        return self._load_json('races/traits_data.json')
    
    @property
    def languages(self) -> Dict:
        return self._load_json('rules/languages.json')
    
    @property
    def spells(self) -> Dict:
        return self._load_json('spells/spell_list.json')
    
    @property
    def draconic_ancestry(self) -> Dict:
        return self._load_json('rules/draconic_ancestry.json')
    
    @property
    def skills(self) -> Dict:
        return self._load_json('rules/skills.json')
    
    @property
    def weapons(self) -> Dict:
        return self._load_json('rules/weapons.json')
    
    @property
    def armor(self) -> Dict:
        return self._load_json('rules/armors.json')
    
    @property
    def adventuring_gear(self) -> Dict:
        return self._load_json('items/adventuring_gear.json')
    
    @property
    def currency(self) -> Dict:
        return self._load_json('rules/currency.json')
    
    def get_item_template(self, name: str) -> Dict:
        key = name.lower().replace(" ", "_").replace("'", "")
        if key in self.weapons:
            return self.weapons[key]
        
        if key in self.armor:
            return self.armor[key]
        
        return {}
        