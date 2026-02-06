import os
from typing import Dict
import pytest
from pytest_bdd import given, scenarios, parsers, then, when

from form_manager.src.models.character import Character
from form_manager.src.services.race_service import RaceService


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RACE_DATA_PATH = os.path.join(BASE_DIR, '../../src/resources/races/race_data.json')
TRAITS_DATA_PATH = os.path.join(BASE_DIR, '../../src/resources/races/traits_data.json')

scenarios("../features/racial_modifiers.feature")


@pytest.fixture
def session_context() -> Dict:
    return {}


@given("a new character session is started with default stats")
def new_character(session_context):
    # new character instantiated and session context passed in
    session_context['character'] = Character()
    session_context['base_stats'] = session_context['character'].stats.copy()


@given(parsers.parse(''))


@when(parsers.parse('the user selects "{race_name}" as their race'))
def select_race(session_context, race_name):
    # character is selected and applied through race applicator
    applicator = RaceService(RACE_DATA_PATH, TRAITS_DATA_PATH)
    character = session_context['character']
    applicator.apply_race(character, race_name)
    

@when(parsers.parse('the user selects "{subrace_name}" as their subrace'))
def select_subrace(session_context, subrace_name):
    applicator = RaceService(RACE_DATA_PATH, TRAITS_DATA_PATH)
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
    assert item in char.pending_choices, f"Choice '{item}' not found in {char.pending_choices}"


@when(parsers.parse('the user selects "{choice}" from "{pending_category}" pending choice'))
def resolve_pending_choice(session_context, choice, pending_category):
    pass


@then(parsers.parse('"{language}" should be added to the user languages'))
def check_languages(session_context, language):
    char = session_context['character']
    assert language in char.languages, f"Language '{language}' not found in {char.languages}"


@then(parsers.parse('"{item}" should be added to the "{category}" proficiencies of the user'))
def check_categorized_proficiency(session_context, item, category):
    pass
