import pytest
from pytest_bdd import scenarios, given, then, parsers
from form_manager.src.models import Item


scenarios("../features/encumbrance.feature")

@given(parsers.parse('the user has a "{ability}" score of {score:d}'))
def set_ability_score(session_context, ability, score):
    char = session_context['character']
    char.stats[ability.lower()] = score


@given(parsers.parse('the user size is set to "{size_name}"'))
def set_size(session_context, size_name):
    char = session_context['character']
    try:
        from form_manager.src.models.character import Character
        char.size = Character.Size(size_name.title()) # Ensure Title Case
    except ValueError:
        pytest.fail(f"Invalid size: {size_name}")


@given("the variant encumbrance rule is enabled")
def enable_variant_rules(session_context):
    char = session_context['character']
    char.use_variant_encumbrance = True


@given(parsers.parse('the user has items weighing {weight:d} lbs'))
def add_weighted_items(session_context, weight):
    char = session_context['character']
    item = Item(name="Heavy Rock", base_weight=weight)
    char.inventory.add_item(item)


@then(parsers.parse('the carrying capacity should be {expected:d} lbs'))
def check_capacity(session_context, expected):
    char = session_context['character']
    assert char.carrying_capacity == expected


@then(parsers.parse('the max push, drag, or lift capacity should be {expected:d} lbs'))
def check_push_capacity(session_context, expected):
    char = session_context['character']
    assert char.max_push_drag_lift == expected


@then(parsers.parse('the encumbrance status should be "{status}"'))
def check_status(session_context, status):
    char = session_context['character']
    assert char.encumbrance_status.value == status, \
        f"Expected status '{status}', got '{char.encumbrance_status.value}' (Weight: {char.current_weight})"


@then(parsers.parse('the effective speed should be {speed:d} ft'))
def check_speed(session_context, speed):
    char = session_context['character']
    assert char.effective_speed == speed, \
        f"Expected speed {speed}, got {char.effective_speed}"