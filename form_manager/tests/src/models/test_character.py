import pytest

from form_manager.src.models import Character, PendingChoice, TargetType


@pytest.fixture
def character() -> Character:
    return Character()


def test_choose_consumes_option_if_unique(character):
    choice = PendingChoice(label="Stat Boost",
                           options=["strength", "dexterity"],
                           count=2,
                           target_type=TargetType.ABILITY_BONUS,
                           unique=True)
    character.pending_choices.append(choice)
    
    character.choose("Stat Boost", "strength")
    
    remaining_choice = character.pending_choices[0]
    assert "strength" not in remaining_choice.options
    assert "dexterity" in remaining_choice.options
    assert remaining_choice.count == 1
    
    
def test_choose_removes_choice_when_count_zero(character):
    choice = PendingChoice(label="Skill",
                           options=["athletics"],
                           count=1,
                           target_type=TargetType.SKILL)
    character.pending_choices.append(choice)
    
    character.choose("Skill", "athletics")
    
    assert len(character.pending_choices) == 0
    assert "athletics" in character.proficiencies["skill"]
    

def test_choose_validates_selection_against_options(character):
    choice = PendingChoice(label="Language",
                           options=["elvish"],
                           count=1,
                           target_type=TargetType.LANGUAGE)
    character.pending_choices.append(choice)
    
    with pytest.raises(ValueError, match="not a valid option"):
        character.choose("Language", "dwarvish")
        

def test_choose_raises_error_if_choice_label_missing(character):
    with pytest.raises(ValueError, match="No pending choice"):
        character.choose("Non Existent Choice", "anything")
        

def test_choose_draconic_ancestry_applies_complex_payload(character):
    choice = PendingChoice(label="Dragon",
                           options=["red"],
                           count=1,
                           target_type=TargetType.DRACONIC_ANCESTRY,
                           choice_map={
                               "red": {
                                   "damage_type": "fire",
                                   "breath_weapon": {
                                       "area": "cone"
                                   }
                               }
                           })
    character.pending_choices.append(choice)
    
    character.choose("Dragon", "red")
    
    assert "fire" in character.resistances
    assert character.breath_weapon["area"] == "cone"
    assert character.breath_weapon["damage_type"] == "fire"
    