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
class Item:
    name: str
    stackable: bool = False
    quantity: int = 1
    
    category: Optional[str] = None
    equipped: bool = False
    weight: float = 0.0
    
    properties: List[str] = field(default_factory=list)
    
    damage_dice: Optional[str] = None
    damage_type: Optional[DamageType] = None
    range: Optional[str] = None
    
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
    