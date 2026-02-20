import os
import pytest
from unittest.mock import Mock

from form_manager.src.models import Character, TargetType
from form_manager.src.services import RaceService, RulesManager


@pytest.fixture
def mock_rules():
    rules = Mock(spec=RulesManager)
    rules.races = {
        "human": {
            "traits": [
                {
                    "id": "ability_score_increase"
                }
            ]
        }
    }
    rules.traits = {
        "ability_score_increase": {
            "modifiers": [
                {
                    "type": "ability_bonus",
                    "target": "all",
                    "value": 1
                }
            ]
        }
    }
    return rules


def test_apply_race_normalizes_input(mock_rules):
    service = RaceService(mock_rules)
    char = Character()
    
    service.apply_race(char, "Human")
    assert char.stats["strength"] == 11
    

def test_apply_race_finds_subraces(mock_rules):
    mock_rules.races = {
        "elf": {
            "subraces": {
                "high_elf": {
                    "traits": [
                        {
                            "id": "cantrip"
                        }
                    ]
                }
            }
        }
    }
    mock_rules.traits = {
        "cantrip": {
            "modifiers": [
                {
                    "type": "spell_choice",
                    "list": "wizard",
                    "level": 0
                }
            ]
        }
    }
    mock_rules.spells = {
        "wizard": [
            [
                "fire_bolt"
            ]
        ]
    }
    service = RaceService(mock_rules)
    char = Character()
    
    service.apply_race(char, "High Elf")
    
    assert len(char.pending_choices) == 1
    choice = char.pending_choices[0]
    assert choice.target_type == TargetType.SPELL
    assert "fire_bolt" in choice.options
    

def test_ability_bonus_choice_filters_fixed_stats(mock_rules):
    mock_rules.races = {
        "half_elf": {
            "traits": [
                {
                    "id": "stat_boost"
                }
            ]
        }
    }
    mock_rules.traits = {
        "stat_boost": {
            "modifiers": [
                {
                    "type": "ability_bonus",
                    "target": "charisma",
                    "value": 2
                },
                {
                    "type": "ability_bonus_choice",
                    "count": 2,
                    "amount": 1
                }
            ]
        }
    }
    service = RaceService(mock_rules)
    char = Character()
    
    service.apply_race(char, "Half Elf")
    
    assert char.stats["charisma"] == 12
    
    choice = char.pending_choices[0]
    assert choice.target_type == TargetType.ABILITY_BONUS
    
    assert "charisma" not in choice.options
    assert "strength" in choice.options
