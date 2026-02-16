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
    bonus: int = 0


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
        total = self.base_weight
        if self.is_container:
            for item in self.contents:
                total += (item.weight * item.quantity)
        return total
    
    @weight.setter
    def weight(self, value: float) -> None:
        self.base_weight = value
        
    @property
    def content_weight(self) -> float:
        if not self.is_container:
            return 0.0
        return sum(item.weight * item.quantity for item in self.contents)
    
    def add_content(self, item: 'Item', count: int = 1) -> None:
        if not self.is_container:
            raise ValueError(f"'{self.name}' is not a container.")
        
        added_weight = item.weight * item.quantity * count
        if (self.content_weight + added_weight) > self.capacity_weight:
            raise ValueError(f"Cannot add '{item.name}': Exceeds capacity of '{self.name}'")
        
        for _ in range(count):
            self.contents.append(item)
    
    @staticmethod
    def parse_cost(cost_str: str) -> Dict[str, int]:
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
        self.damage_dice = "1d4"
        self.range = "20/60"
    
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
        