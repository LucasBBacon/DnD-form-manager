"""Step definitions for testing container functionality in the inventory system."""

from pytest_bdd import given, parsers, scenarios, then, when

from form_manager.src.models import Item, Character


scenarios("../features/containers.feature")


@given(parsers.parse('the user has a "{item_name}" in their inventory'))
def define_item_inventory(session_context, item_name):
    """Ensures the specified item exists in the user's inventory."""
    char = session_context["character"]
    item = Item(name=item_name, is_container=True)
    char.inventory.add_item(item)
    assert item is not None


@given(
    parsers.parse(
        (
            'the item "{item_name}" is a container with '
            "capacity {capacity:f} lbs and base weight {weight:f} lbs"
        )
    )
)
def define_container_stats(session_context, item_name, capacity, weight):
    """Configures the specified item as a container with given capacity and weight."""
    char = session_context["character"]
    container = char.inventory.get_item(item_name)
    assert container is not None

    container.is_container = True
    container.capacity_weight = capacity
    container.base_weight = weight


@given(
    parsers.parse(
        (
            'the user has {item_quantity:d} "{item_name}" '
            "weighing {item_weight:f} lbs in their inventory"
        )
    )
)
def define_item_by_quantity_weight(
    session_context, item_quantity, item_name, item_weight
):
    """Adds a specified quantity of an item with a given weight to the user's inventory."""
    char = session_context["character"]
    item = Item(name=item_name, base_weight=item_weight)
    char.inventory.add_item(item, item_quantity)


@given(parsers.parse('the "{container_name}" contains items weighing {weight:f} lbs'))
def define_container_with_items(session_context, container_name, weight):
    """Adds an item with a specified weight into the container."""
    char = session_context["character"]
    container = char.inventory.get_item(container_name)
    assert container is not None

    item = Item(name="Heavy rock", base_weight=weight)
    char.inventory.add_item(item)
    char.inventory.move_item_to_container("Heavy rock", container_name)


@given(parsers.parse('the "{container_name}" contains "{item_name}"'))
def define_container_with_item(session_context, container_name, item_name):
    """Adds a specified item into the container."""
    char = session_context["character"]
    container = char.inventory.get_item(container_name)
    assert container is not None

    item = Item(name=item_name)
    char.inventory.add_item(item)
    char.inventory.move_item_to_container(item_name, container_name)


@given(parsers.parse("the user total weight is {weight:f} lbs"))
def define_total_inventory_weight(session_context, weight):
    """Adds an item to the inventory to ensure the total weight matches the specified value."""
    char: Character = session_context["character"]
    missing_weight = weight - char.inventory.get_total_weight()
    item = Item(name="Heavy rock", base_weight=missing_weight)
    char.inventory.add_item(item)
    actual_weight = char.inventory.get_total_weight()
    assert (
        actual_weight == weight
    ), f"Weight {actual_weight} lbs, does not match expected weight {weight} lbs."


@when(
    parsers.parse(
        'the user moves {item_quantity:d} "{item_name}" into "{container_name}"'
    )
)
def move_item_to_container(session_context, item_quantity, item_name, container_name):
    """Moves a specified quantity of an item into a container."""
    char = session_context["character"]
    char.inventory.move_item_to_container(item_name, container_name, item_quantity)


@when("the user checks their total inventory weight")
def calculate_total_inventory_weight(session_context):
    """Calculates the total weight of all items in the user's inventory."""
    char = session_context["character"]
    session_context["total_inv_weight"] = char.inventory.get_total_weight()


@when(parsers.parse('the user attempts to move "{item_name}" into "{container_name}"'))
def attempt_move_item_to_container(session_context, item_name, container_name):
    """Attempts to move an item into a container, expecting failure if it exceeds capacity."""
    char = session_context["character"]
    try:
        char.inventory.move_item_to_container(item_name, container_name)
        session_context["last_err"] = None
    except ValueError as e:
        session_context["last_err"] = str(e)


@when(parsers.parse('the user retrieves "{item_name}" from "{container_name}"'))
def remove_item_from_container(session_context, item_name, container_name):
    """Removes a specified item from a container and adds it back to the top-level inventory."""
    char = session_context["character"]
    char.inventory.remove_item_from_container(item_name, container_name)


@when(parsers.parse('the user drops the "{container_name}"'))
def remove_container_from_inventory(session_context, container_name):
    """Removes the specified container from the user's inventory."""
    char: Character = session_context["character"]
    char.inventory.remove_item(container_name)


@then(parsers.parse('the inventory should contain "{item_name}" at the top level'))
def check_item_in_top_level(session_context, item_name):
    """Checks that the specified item exists at the top level of the inventory (not inside a container)."""
    char = session_context["character"]
    found = any(char.inventory.items[c_id].name == item_name for c_id in char.inventory.top_level_ids)
    assert found, f"Item '{item_name}' not found at top level of inventory."


@then(parsers.parse('the inventory should not contain "{item_name}" at the top level'))
def check_missing_top_level(session_context, item_name):
    """Checks that the specified item does not exist at the top level of the inventory
    (it may be inside a container)."""
    char = session_context["character"]
    found = any(char.inventory.items[c_id].name == item_name for c_id in char.inventory.top_level_ids)
    assert not found, f"Item '{item_name}' found at top level of inventory."


@then(parsers.parse('the "{container_name}" should contain "{item_name}"'))
def check_container_content(session_context, container_name, item_name):
    """Checks that the specified item exists within the specified container."""
    char = session_context["character"]
    container = char.inventory.get_item(container_name)
    assert container is not None

    found = any(char.inventory.items[c_id].name == item_name for c_id in container.content_ids)
    assert found, f"Container '{container_name}' does not contain '{item_name}'"


@then(parsers.parse('the "{container_name}" should not contain "{item_name}"'))
def check_container_content_missing(session_context, container_name, item_name):
    """Checks that the specified item does not exist within the specified container."""
    char = session_context["character"]
    container = char.inventory.get_item(container_name)
    assert container is not None

    found = any(char.inventory.items[c_id].name == item_name for c_id in container.content_ids)
    assert not found, f"Container '{container_name}' contains '{item_name}'"


@then(parsers.parse('the "{container_name}" total weight should be {weight:f} lbs'))
def check_container_weight(session_context, container_name, weight):
    """Checks that the total weight of the specified container
    (including its contents) matches the expected value."""
    char = session_context["character"]
    container = char.inventory.get_item(container_name)
    actual_weight = char.inventory.get_item_total_weight(container.id)
    assert actual_weight == weight, f"Expected {weight} lbs, got {actual_weight} lbs."


@then(parsers.parse("the total weight should be {weight:f} lbs"))
def check_total_inventory_weight(session_context, weight):
    """Checks that the total weight of all items in the inventory matches the expected value."""
    actual_weight = session_context["total_inv_weight"]
    assert (
        actual_weight == weight
    ), f"Expected total inventory weight of {weight}, got {actual_weight}"


@then("the action should fail")
def check_action_failed(session_context):
    """Checks that the last attempted action resulted in an error, indicating failure."""
    error = session_context["last_err"]
    assert error is not None, "Expected action to fail, but it succeeded"
    assert "Exceeds capacity" in error
