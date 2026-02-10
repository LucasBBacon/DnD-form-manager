from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class DamageType(str, Enum):
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
    base: int = 0
    dex_bonus: bool = False
    max_dex_bonus: int = 0


@dataclass
class Item:
    name: str
    stackable: bool = False
    quantity: int = 1
    
    cost: Dict[str, int] = field(default_factory=lambda: {
        "cp": 0, "sp": 0, "ep": 0, "gp": 0, "pp": 0
    })
    
    category: Optional[str] = None
    equipped: bool = False
    weight: float = 0.0
    
    properties: List[str] = field(default_factory=list)
    
    damage_dice: Optional[str] = None
    damage_type: Optional[DamageType] = None
    range: Optional[str] = None
    armor_class: Optional[ArmorClass] = None
    
    def __post_init__(self):
        pass
    
    def make_improvised(self) -> None:
        self.damage_dice = "1d4"
        self.range = "20/60"
    
    def apply_weapon_stats(self, weapon_data: Dict) -> None:
        if 'damage_dice' in weapon_data: 
            self.damage_dice = weapon_data['damage_dice']
            
        if 'damage_type' in weapon_data:
            dtype_str = weapon_data['damage_type'].lower()
            try:
                self.damage_type = DamageType(dtype_str)
            except ValueError:
                pass
            
        if 'properties' in weapon_data:
            self.properties = weapon_data['properties']
            
        if 'range' in weapon_data:
            self.range = weapon_data['range']
            
        if 'category' in weapon_data:
            self.category = weapon_data['category']
    
    def apply_template(self, template_data: Dict) -> None:
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
            
        if 'range' in template_data:
            self.range = template_data['range']
            
        if 'category' in template_data:
            self.category = template_data['category']
            
        if 'cost' in template_data:
            self.cost = template_data['cost']
            
        if 'armor_class' in template_data:
            armor_class_data = template_data['armor_class']
            base = 0
            dex_bonus = False
            max_dex_bonus = 0
            if 'base' in armor_class_data:
                base = armor_class_data['base']
            if 'dex_bonus' in armor_class_data:
                dex_bonus = bool(armor_class_data['dex_bonus'])
            if 'max_dex_bonus' in armor_class_data:
                max_dex_bonus = armor_class_data['max_dex_bonus']
            armor_class = ArmorClass(base=base,
                                     dex_bonus=dex_bonus,
                                     max_dex_bonus=max_dex_bonus)
            self.armor_class = armor_class
            
        if 'strength_requirement' in template_data:
            self.strength_requirement = template_data['strength_requirement']
        
        if 'stealth_disadvantage' in template_data:
            self.stealth_disadvantage = template_data['stealth_disadvantage']
        