"""
RaceService is responsible for applying the traits of a specified race or subrace to a character, 
including handling any choices that arise from those traits.
"""

from typing import Dict, List, Optional
from form_manager.src.models.character import Character, PendingChoice
from form_manager.src.services.rules_manager import RulesManager


class RaceService:
    """Service for applying race and subrace traits to characters."""

    def __init__(self, rules_manager: RulesManager) -> None:
        self.rules = rules_manager

    def apply_race(self, character: Character, race_name: str) -> Character:
        """
        Applies the traits of a specified race or subrace to a character.

        :param character: The character to apply the race traits to.
        :type character: Character
        :param race_name: The name of the race or subrace to apply.
        :type race_name: str
        :return: The character with the applied race traits.
        :rtype: Character
        """
        race_key = race_name.lower().replace(" ", "_")
        race_node = self.__find_race_node(race_key)
        if not race_node:
            raise ValueError(f"Race or Subrace '{race_name}' not found.")

        self.__apply_traits(character, race_node)

        return character

    def __find_race_node(self, key: str) -> Optional[Dict]:
        if key in self.rules.races:
            return self.rules.races[key]

        for race_val in self.rules.races.values():
            subraces = race_val.get('subraces', {})
            if key in subraces:
                return subraces[key]

        return None

    def __apply_traits(self, character: Character, race_node: Dict) -> None:
        for trait_entry in race_node.get('traits', []):
            trait_id = trait_entry.get('id')
            base_trait = self.rules.traits.get(trait_id, {})
            label = (trait_entry.get('overrides', {}).get('label')
                     or base_trait.get('label')
                     or trait_id.replace('_', ' ').title())
            if trait_id not in ['ability_score_increase',
                                'speed',
                                'size',
                                'languages',
                                'age',
                                'alignment']:
                character.features.append(label)

            modifiers = trait_entry.get('overrides', {}).get('modifiers')
            if not modifiers:
                modifiers = base_trait.get('modifiers', [])

            self.__apply_modifiers(character, modifiers)

    def __apply_modifiers(self, character: Character, modifiers) -> None:
        fixed_bonuses = []
        for mod in modifiers:
            if mod.get('type') == 'ability_bonus':
                target = mod.get('target')
                if target and target != 'all':
                    fixed_bonuses.append(target)

        for mod in modifiers:
            m_type = mod.get('type')
            match m_type:
                case 'ability_bonus':
                    target = mod.get('target')
                    value = mod.get('value')
                    if target in character.stats:
                        character.stats[target] += value
                    elif target == 'all':
                        for stat in character.stats.keys():
                            character.stats[stat] += value
                case 'size':
                    character.size = mod.get('value').title()
                case 'speed':
                    character.speed = mod.get('value')
                case 'language_grant':
                    lang = mod.get('language').title()
                    if lang not in character.languages:
                        character.languages.append(lang)
                case 'sense':
                    target = mod.get('target')
                    if target:
                        character.features.append(target.capitalize())
            if 'choice' in str(m_type):
                self.__resolve_choices(character, mod, m_type, fixed_bonuses)

    def __resolve_choices(self, character: Character,
                          mod,
                          m_type,
                          fixed_bonuses: Optional[List[str]] = None) -> None:
        choice = None
        match m_type:
            case 'language_choice':
                language_options = [lang.get('label', "").lower()
                                    for lang in self.rules.languages.values()]
                choice_options = mod.get('pool', language_options)
                choice_options = language_options if choice_options == 'any' else choice_options
                choice = PendingChoice(label='Language',
                                       options=choice_options,
                                       count=mod.get('count', 1),
                                       target_type='language')
            case 'tool_proficiency_choice':
                choice = PendingChoice(label='Tool Proficiency',
                                       options=mod.get('list', []),
                                       count=mod.get('count', 1),
                                       target_type='tool')
            case 'spell_choice':
                class_key = mod.get('list')
                level = mod.get('level', 0)
                available_spells = []
                class_spells = self.rules.spells.get(class_key)
                if class_spells and len(class_spells) > level:
                    available_spells = class_spells[level]
                choice = PendingChoice(label=f"{class_key.capitalize()} Spell",
                                       options=available_spells,
                                       count=mod.get('count', 1),
                                       target_type='spell',
                                       level=level)
            case "choice_trigger":
                trigger_id = mod.get('choice_id')
                if trigger_id == 'draconic_ancestry':
                    options_list = list(self.rules.draconic_ancestry.keys())
                    choice = PendingChoice(label="Draconic Ancestry",
                                           options=options_list,
                                           count=1,
                                           target_type="draconic_ancestry",
                                           choice_map=self.rules.draconic_ancestry)
            case 'skill_choice':
                all_skills = []
                for cat_skills in self.rules.skills.values():
                    all_skills.extend(cat_skills)
                options = mod.get('list', all_skills)
                if mod.get('pool') == 'any':
                    options = all_skills
                choice = PendingChoice(label="Skill Choice",
                                       options=options,
                                       count=mod.get('count', 1),
                                       target_type="skill")
            case 'ability_bonus_choice':
                options = list(character.stats.keys())
                if fixed_bonuses:
                    for fb in fixed_bonuses:
                        if fb in options:
                            options.remove(fb)
                choice = PendingChoice(label="Ability Bonus",
                                       options=options,
                                       count=mod.get('count', 1),
                                       target_type="ability_bonus",
                                       level=mod.get('amount', 1),
                                       unique=True)
        if choice:
            character.pending_choices.append(choice)
