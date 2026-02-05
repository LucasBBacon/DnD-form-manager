from typing import Dict
import pytest
from pytest_bdd import given, scenarios, parsers, then, when


scenarios("../features/racial_modifiers.feature")


@pytest.fixture
def session_context() -> Dict:
    return {}


@given("a new character session is started with default stats")
def new_character(session_context):
    # new character instantiated and session context passed in
    pass


@when(parsers.parse('the user selects "{race_name}" as their race'))
def select_race(session_context, race_name):
    # character is selected and applied through race applicator
    pass


@then(parsers.parse('the user "{ability}" score should increase by {amount:d}'))
def check_ability_score_increase(session_context, ability, amount):
    # assertions about the increase in ability score
    pass