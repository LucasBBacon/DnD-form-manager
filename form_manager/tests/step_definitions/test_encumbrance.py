from pytest_bdd import given, parsers, scenarios, then


scenarios('../features/encumbrance.feature')


@given(parsers.parse('the user has a "{ability}" score of {score:d}'))
def set_ability_score(session_context, ability, score):
    char = session_context['character']
    key = ability.lower()
    if key not in char.stats:
        raise ValueError(f"Invalid ability: {ability}")
    char.stats[key] = score


@then(parsers.parse('the carrying capacity should be {expected_capacity:d} lbs'))
def check_carrying_capacity(session_context, expected_capacity):
    char = session_context['character']
    assert char.carrying_capacity == expected_capacity, f"Expected capacity {expected_capacity}, but got {char.carrying_capacity}"
    

@then(parsers.parse('the max push, drag, or lift capacity should be {expected_capacity:d} lbs'))
def check_push_drag_lift(session_context, expected_capacity):
    char = session_context['character']
    assert char.max_push_drag_lift == expected_capacity, f"Expected push/drag/lift {expected_capacity}, but got {char.max_push_drag_lift}"
    