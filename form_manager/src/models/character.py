from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List

from form_manager.src.models.inventory import Inventory


class TargetType(str, Enum):
    TOOL = "tool"
    SKILL = "skill"
    LANGUAGE = "language"
    SPELL = "spell"
    ABILITY_BONUS = "ability_bonus"
    DRACONIC_ANCESTRY = "draconic_ancestry"


@dataclass
class PendingChoice:
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
        SMALL = "Small"
        MEDIUM = "Medium"
        LARGE = "Large"

    stats: Dict[str, int] = field(default_factory=lambda: {
        "strength": 10, "dexterity": 10, "constitution": 10, 
        "intelligence": 10, "wisdom": 10, "charisma": 10
    })
    size: Size = Size.MEDIUM
    speed: int = 30
    languages: List[str] = field(default_factory=list)
    features: List[str] = field(default_factory=list)
    pending_choices: List[PendingChoice] = field(default_factory=list)
    
    proficiencies: Dict[str, List[str]] = field(default_factory=lambda: {
        "armor": [], "weapon": [], "tool": [], "skill": []
    })
    resistances: List[str] = field(default_factory=list)
    
    inventory: Inventory = field(default_factory=Inventory)
    purse: Dict[str, int] = field(default_factory=lambda: {
        "cp": 0, "sp": 0, "ep": 0, "gp": 0, "pp": 0
    })
    
    spells: Dict[str, List[str]] = field(default_factory=lambda: {
        "0": [], "1": [], "2": [], "3": [], "4": [], 
        "5": [], "6": [], "7": [], "8": [], "9": [] 
    })
    breath_weapon: Dict[str, str] = field(default_factory=dict)
    
    def choose(self, choice_label: str, selection: str) -> 'Character':
        choice_obj = next((c for c in self.pending_choices if c.label == choice_label), None)
        print(choice_obj)          
        if not choice_obj:
            raise ValueError(f"No pending choice found for '{choice_label}'")
        
        # Validation
        selection = selection.lower()
        if choice_obj.options and selection not in choice_obj.options:
            raise ValueError(f"'{selection}' is not a valid option for {choice_label}")    
        
        # Logic
        match choice_obj.target_type:
            case TargetType.TOOL:
                self.proficiencies['tool'].append(selection)
                
            case TargetType.SKILL:
                self.proficiencies['skill'].append(selection)
                
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
        
        # Optional Comsumption
        if choice_obj.unique and selection in choice_obj.options:
            choice_obj.options.remove(selection)
            
        # Counter
        choice_obj.count -= 1
        if choice_obj.count <= 0:
            self.pending_choices.remove(choice_obj)
        
        return self
    
    def _calculate_purse_total_cp(self) -> int:
        return (
            self.purse.get('cp', 0) +
            self.purse.get('sp', 0) * 10 +
            self.purse.get('ep', 0) * 50 +
            self.purse.get('gp', 0) * 100 +
            self.purse.get('pp', 0) * 1000
        )
    
    def pay_cost(self, cost: Dict[str , int]) -> bool:
        total_cp = self._calculate_purse_total_cp()
        
        cost_cp = (
            cost.get('cp', 0) +
            cost.get('sp', 0) * 10 +
            cost.get('ep', 0) * 50 +
            cost.get('gp', 0) * 100 +
            cost.get('pp', 0) * 1000
        )
        
        if total_cp < cost_cp:
            return False
        
        remaining_cp = total_cp - cost_cp
        new_purse = {
           "cp": 0, "sp": 0, "ep": 0, "gp": 0, "pp": 0
        }
        new_purse['pp'] = remaining_cp // 1000
        remaining_cp %= 1000
        new_purse['gp'] = remaining_cp // 100
        remaining_cp %= 100
        new_purse['sp'] = remaining_cp // 10
        remaining_cp %= 10
        new_purse['cp'] = remaining_cp 
        remaining_cp %= 1000
        
        self.purse = new_purse
        return True
        
        