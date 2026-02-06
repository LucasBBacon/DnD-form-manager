import json
from typing import Dict
from form_manager.src.models.character import Character


class RaceService:
    def __init__(self, race_data_path: str, traits_data_path: str) -> None:
        self.race_data = self.__load(race_data_path)
        self.traits_data = self.__load(traits_data_path)
    
    def __load(self, path: str) -> Dict:
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: {path} not found.")
            return {}
    
    def apply_race(self, character: Character, race_key: str) -> Character:
        race_key = race_key.lower()
        if race_key not in self.race_data:
            raise ValueError(f"Race '{race_key} not found.'")
        
        race = self.race_data[race_key]
        
        for trait_entry in race.get('traits', []):
            trait_id = trait_entry.get('id')
            print(trait_id)
            base_trait = self.traits_data.get(trait_id, {})
            label = trait_entry.get('overrides', {}).get('label') or base_trait.get('label') or trait_id.replace('_', ' ').title()
            if trait_id not in ['ability_score_increase', 'speed', 'size', 'languages', 'age', 'alignment']:
                character.features.append(label)
                
            modifiers = trait_entry.get('overrides', {}).get('modifiers')
            if not modifiers:
                modifiers = base_trait.get('modifiers', [])
            
            self.__apply_modifiers(character, modifiers)
        
        return character
            
    def __apply_modifiers(self, character: Character, modifiers):
        print(modifiers)
        for mod in modifiers:
            m_type = mod.get('type')
            
            if m_type == 'ability_bonus':
                target = mod.get('target')
                value = mod.get('value')
                if target in character.stats:
                    character.stats[target] += value
            
            elif m_type == 'size':
                character.size = mod.get('value').title()
                
            elif m_type == 'speed':
                character.speed = mod.get('value')
                
            elif m_type == 'language_grant':
                lang = mod.get('language').title()
                if lang not in character.languages:
                    character.languages.append(lang)
                    
            elif m_type == 'tool_proficiency_choice':
                options = mod.get('list', [])
                choice_name = 'Tool Proficiency'
                character.pending_choices.append(choice_name)
                
            elif m_type == 'sense':
                target = mod.get('target')
                if target:
                    character.features.append(target.capitalize())
    