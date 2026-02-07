from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List


@dataclass
class PendingChoice:
    label: str
    options: List[str]
    count: int
    target_type: str


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
    
    spells: List[List[str]] = field(default_factory=list)
    
    def choose(self, choice_label: str, selection: str) -> 'Character':
        choice_obj = next((c for c in self.pending_choices if c.label == choice_label))
        selection = selection.lower()
            
        if not choice_obj:
            raise ValueError(f"No pending choice found for '{choice_label}'")
        if choice_obj.options and selection not in choice_obj.options:
            raise ValueError(f"'{selection}' is not a valid option for {choice_label}")    
        
        if choice_obj.target_type == "tool":
            self.proficiencies['tool'].append(selection)
        elif choice_obj.target_type == "skill":
            self.proficiencies['skill'].append(selection)
        elif choice_obj.target_type == "language":
            self.languages.append(selection.title())
            
        choice_obj.count -= 1
        if choice_obj.count <= 0:
            self.pending_choices.remove(choice_obj)
        
        return self