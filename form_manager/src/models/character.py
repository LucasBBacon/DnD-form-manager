from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List


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
    pending_choices: List[str] = field(default_factory=list)