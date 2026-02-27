from pytest_bdd import given, parsers, scenarios, then, when

from form_manager.src.models.item import Item


scenarios("../features/attunement.feature")


@given(parsers.parse('the user has a "{item_name}" in their inventory'))
def define_item_inventory(session_context, item_name):
    """Ensures the specified item exists in the user's inventory."""
    char = session_context["character"]
    item = Item(name=item_name)
    char.inventory.add_item(item)
    assert item is not None


@given(parsers.parse('the item "{item_name}" requires attunement'))
def set_item_requires_attunement(session_context, item_name):
    char = session_context["character"]
    item = char.inventory.get_item(item_name)
    assert (
        item is not None
    ), f"Item '{item_name}' not found to set attunement requirements."
    item.requires_attunement = True


@given(parsers.parse('the item "{item_name}" does not require attunement'))
def set_item_does_not_require_attunement(session_context, item_name):
    char = session_context["character"]
    item = char.inventory.get_item(item_name)
    assert (
        item is not None
    ), f"Item '{item_name}' not found to set attunement requirements."
    item.requires_attunement = False


@given(parsers.parse("the user has attuned to {count:d} items"))
def set_attuned_items(session_context, count):
    char = session_context["character"]
    item_a = Item(name="Item a", requires_attunement=True)
    item_b = Item(name="Item b", requires_attunement=True)
    item_c = Item(name="Item c", requires_attunement=True)
    for item in [item_a, item_b, item_c]:
        char.inventory.add_item(item)
        char.attune_item(item.name)
    number_of_items = len(char.attuned_items)
    assert (
        number_of_items == count
    ), f"Expected {count} attuned items, but was {number_of_items}."


@given(parsers.parse('the user attunes to "{item_name}"'))
def set_attuned_to_item(session_context, item_name):
    char = session_context["character"]
    char.attune_item(item_name)


@given(parsers.parse('the user has another "{item_name}" in their inventory'))
def add_another_item_item_inventory(session_context, item_name):
    char = session_context["character"]

    existing_item = char.inventory.get_item(item_name)
    requires_attunement = existing_item.requires_attunement if existing_item else False

    new_item = Item(name=item_name)
    new_item.requires_attunement = requires_attunement
    char.inventory.add_item(new_item)


@when(parsers.parse('the user attunes to "{item_name}"'))
def attune_to_item(session_context, item_name):
    char = session_context["character"]
    char.attune_item(item_name)


@when(parsers.parse('the user attempts to attune to "{item_name}"'))
def attempt_attune_to_item(session_context, item_name):
    char = session_context["character"]
    try:
        char.attune_item(item_name)
        session_context["last_err"] = None
    except ValueError as e:
        session_context["last_err"] = str(e)


@when(parsers.parse('the user attempts to attune to the second "{item_name}"'))
def attempts_attune_second_item(session_context, item_name):
    char = session_context["character"]
    try:
        char.attune_item(item_name)
        session_context["last_err"] = None
    except ValueError as e:
        session_context["last_err"] = str(e)


@when(parsers.parse('the user unattunes from "{item_name}"'))
def unattune_to_item(session_context, item_name):
    char = session_context["character"]
    char.unattune_item(item_name)


@then(parsers.parse('the item "{item_name}" should be attuned'))
def check_item_is_attuned(session_context, item_name):
    char = session_context["character"]
    item = char.inventory.get_item(item_name)
    assert item is not None
    assert (
        item.is_attuned is True
    ), f"Expected {item_name} to be attuned, but it was not."


@then(parsers.parse('the item "{item_name}" should not be attuned'))
def check_item_is_not_attuned(session_context, item_name):
    char = session_context["character"]
    item = char.inventory.get_item(item_name)
    assert item is not None
    assert (
        item.is_attuned is False
    ), f"Expected {item_name} to not be attuned, but it was."


@then(parsers.re(r"the user should have (?P<count>\d+) attuned item(s)?"))
def check_attuned_item_count(session_context, count):
    char = session_context["character"]
    expected_count = int(count)
    actual_count = len(char.attuned_items)
    assert (
        actual_count == expected_count
    ), f"Expected {expected_count} attuned items, found {actual_count}."


@then(parsers.parse("the user should have {count:d} attunement slots remaining"))
def check_attunement_slots(session_context, count):
    char = session_context["character"]
    assert (
        char.attunement_slots_remaining == count
    ), f"Expected {count} slots remaining, but got {char.attunement_slots_remaining}."


@then("the action should fail")
def check_failed_action(session_context):
    last_error = session_context["last_err"]
    assert last_error is not None, "Action should have failed, but did not."
