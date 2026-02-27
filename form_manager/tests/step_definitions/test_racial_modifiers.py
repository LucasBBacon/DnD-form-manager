import os
from pytest_bdd import given, scenarios, parsers, then, when

from form_manager.src.models.character import Character
from form_manager.src.services import RaceService


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(BASE_DIR, '../../src/resources')

scenarios("../features/racial_modifiers.feature")


def normalize_text(raw_input: str) -> str:
    return raw_input.lower().replace(" ", "_").replace("'", "")


@when(parsers.parse('the user selects "{race_name}" as their race'))
def select_race(session_context, rules_manager, race_name):
    # character is selected and applied through race applicator
    applicator = RaceService(rules_manager)
    character = session_context['character']
    applicator.apply_race(character, race_name)


@when(parsers.parse('the user selects "{subrace_name}" as their subrace'))
def select_subrace(session_context, rules_manager, subrace_name):
    applicator = RaceService(rules_manager)
    character = session_context['character']
    applicator.apply_race(character, subrace_name)


@then(parsers.parse('the user "{ability}" score should increase by {amount:d}'))
def check_ability_score_increase(session_context, ability, amount):
    # assertions about the increase in ability score
    char = session_context['character']
    base_stats = session_context['base_stats']
    ability_key = ability.lower()
    
    actual_increase = char.stats[ability_key] - base_stats[ability_key]
    assert actual_increase == amount, f"Expected {ability} to increase by {amount}, but increased by {actual_increase}."


@then(parsers.parse('the user size should be set to "{size}"'))
def check_size(session_context, size):
    # assertions about the character size
    char = session_context['character']
    assert char.size == size


@then(parsers.parse('the user speed should be set to {speed:d} ft'))
def check_speed(session_context, speed):
    # assert character speed
    char = session_context['character']
    assert char.speed == speed


@then(parsers.parse('"{feature}" should be added to the user feature list'))
def check_feature_list(session_context, feature):
    # assertions of item inside feature list
    char = session_context['character']
    assert feature in char.features, f"Feature '{feature}' not found in {char.features}"


@then(parsers.parse('"{item}" should be added to the user pending choices'))
def check_pending_choices(session_context, item):
    # checks if the pending item exists
    char = session_context['character']
    choice_labels = [c.label for c in char.pending_choices]
    assert item in choice_labels, f"Choice '{item}' not found in {choice_labels}"


@when(parsers.parse('the user selects "{choice}" from "{pending_category}" pending choice'))
def resolve_pending_choice(session_context, choice, pending_category):
    choice_normalized = normalize_text(choice)
    char = session_context['character']
    choice_labels = [c.label for c in char.pending_choices]
    assert pending_category in choice_labels, f"Character does not have a pending choice for '{pending_category}'"
    char.choose(pending_category, choice_normalized)


@then(parsers.parse('"{pending_category}" should be removed from the user pending choices'))
def check_choice_removed(session_context, pending_category):
    char = session_context['character']
    choice_labels = [c.label for c in char.pending_choices]
    assert pending_category not in choice_labels, f"Character still has pending choice for '{pending_category}'"


@then(parsers.parse('the user should not be able to select "{ability}" again'))
def check_option_removed(session_context, ability):
    char = session_context['character']
    choice = next((c for c in char.pending_choices if c.label == "Ability Bonus"), None)
    ability_normalized = normalize_text(ability)
    if choice:
        assert ability_normalized not in choice.options


@then(parsers.parse('"{language}" should be added to the user languages'))
def check_languages(session_context, language):
    char = session_context['character']
    assert language in char.languages, f"Language '{language}' not found in {char.languages}"


@then(parsers.parse('"{spell}" should be added to the user "{level}" spells'))
def check_spells(session_context, spell, level):
    level_map = {
        "Cantrip": "0",
        "1st Level": "1",
        "2nd Level": "2"
    }
    target_level = level_map.get(level)
    if not target_level:
        raise ValueError(f"Unknown spell level label: {level}")

    char = session_context['character']
    spell_normalized = normalize_text(spell)

    assert spell_normalized in char.spells[target_level], f"Spell '{spell_normalized}' not found in level {target_level} spells: {char.spells[target_level]}"


@then(parsers.parse('"{item}" should be added to the "{category}" proficiencies of the user'))
def check_categorized_proficiency(session_context, item, category):
    char = session_context['character']
    item_normalized = normalize_text(item)
    assert category in char.proficiencies, f"Proficiency category '{category}' does not exist on Character."
    assert item_normalized in char.proficiencies[category], f"Expected '{item_normalized}' in '{category}' proficiencies, but got: {char.proficiencies[category]}"


@then(parsers.parse('"{damage_type}" should be added to the user draconic damage type'))
def check_draconic_damage(session_context, damage_type):
    char = session_context['character']
    damage_type_normalized = normalize_text(damage_type)
    assert damage_type_normalized in char.resistances, f"Expected {damage_type} in resistances: {char.resistances}"


@then(parsers.parse('"{ability}" should be the ability save for user breath weapon'))
def check_breath_save(session_context, ability):
    char = session_context['character']
    ability_normalized = normalize_text(ability)
    actual = char.breath_weapon.get('save')
    assert actual == ability_normalized, f"Expected breath save {ability}, got {actual}"


@then(parsers.parse('"{area}" should be the area for user breath weapon'))
def check_breath_area(session_context, area):
    char = session_context['character']
    actual = char.breath_weapon.get('area', "").lower()
    assert actual == area, f"Expected breath area {area}, got {actual}"
