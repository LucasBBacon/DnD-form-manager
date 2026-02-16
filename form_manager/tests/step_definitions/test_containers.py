from pytest_bdd import given, parsers, scenarios, then, when

from form_manager.src.models import Item


scenarios('../features/containers.feature')


@given(parsers.parse('the user has a "{item_name}" in their inventory'))
def define_item_inventory(session_context, item_name):
    char = session_context['character']
    item = Item(name=item_name, is_container=True)
    char.inventory.add_item(item)
    assert item is not None


@given(parsers.parse('the item "{item_name}" is a container with capacity {capacity:f} lbs and base weight {weight:f} lbs'))
def define_container_stats(session_context, item_name, capacity, weight):
    char = session_context['character']
    container = char.inventory.get_item(item_name)
    assert container is not None
    
    container.is_container = True
    container.capacity_weight = capacity
    container.base_weight = weight


@given(parsers.parse('the user has {item_quantity:d} "{item_name}" weighing {item_weight:f} lbs in their inventory'))
def define_item_by_quantity_weight(session_context, item_quantity, item_name, item_weight):
    char = session_context['character']
    item = Item(name=item_name, base_weight=item_weight)
    char.inventory.add_item(item, item_quantity)


@when(parsers.parse('the user moves {item_quantity:d} "{item_name}" into "{container_name}"'))
def move_item_to_container(session_context, item_quantity, item_name, container_name):
    char = session_context['character']
    char.inventory.move_item_to_container(item_name, container_name, item_quantity)
    

@then(parsers.parse('the inventory should not contain "{item_name}" at the top level'))
def check_missing_top_level(session_context, item_name):
    char = session_context['character']
    found = any(i.name == item_name for i in char.inventory.items)
    assert not found, f"Item '{item_name}' found at top level of inventory."


@then(parsers.parse('the "{container_name}" should contain "{item_name}"'))
def check_container_content(session_context, container_name, item_name):
    char = session_context['character']
    container = char.inventory.get_item(container_name)
    assert container is not None
    
    found = any(i.name == item_name for i in container.contents)
    assert found, f"Container '{container_name}' does not contain '{item_name}'"
    
    
@then(parsers.parse('the "{container_name}" total weight should be {weight:f} lbs'))
def check_container_weight(session_context, container_name, weight):
    char = session_context['character']
    container = char.inventory.get_item(container_name)
    assert container.weight == weight
