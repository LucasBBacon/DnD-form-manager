import pytest
from pytest_bdd import given, scenarios, then, when, parsers

from form_manager.src.models import Character, Item


scenarios("../features/item_properties.feature")


@pytest.fixture
def session_context():
    return {}


@given("a new character session is started")
def new_character(session_context):
    session_context['character'] = Character()
    
    
@given(parsers.parse('the user has a "{item_name}" in their inventory'))
def user_has_specific_item(session_context, item_name):
    char = session_context['character']
    item = Item(name=item_name)
    char.inventory.add_item(item)
    
    
@given(parsers.parse('the item "{item_name}" is currently unequipped'))
def check_item_is_unequipped(session_context, item_name):
    char = session_context['character']
    item = char.inventory.get_item(item_name)
    assert item is not None
    item.equipped = False
    assert item.equipped is False


@given(parsers.parse('the item "{item_name}" is currently equipped'))
def check_item_is_equipped(session_context, item_name):
    char = session_context['character']
    item = char.inventory.get_item(item_name)
    assert item is not None
    item.equipped = True
    assert item.equipped is True


@given(parsers.parse('the user has {count:d} "{item_name}" weighing {weight:f} lbs in their inventory'))
def user_has_weighted_items(session_context, count, item_name, weight):
    char = session_context['character']
    item = Item(name=item_name, weight=weight, stackable=True)
    char.inventory.add_item(item, count)


@when(parsers.parse('the user creates a custom item named "{item_name}"'))
def create_custom_item(session_context, item_name):
    item = Item(name=item_name)
    session_context['custom_item'] = item
    session_context['character'].inventory.add_item(item)
    

@when(parsers.parse('the user sets the item category to "{category}"'))
def set_item_category(session_context, category):
    item = session_context.get('custom_item')
    assert item is not None, "No custom item found in context to modify"
    item.category = category
    

@when(parsers.parse('the user adds the property "{property_name}" to the item'))
def add_item_property(session_context, property_name):
    item = session_context.get('custom_item')
    assert item is not None, "No custom item found in context to modify"
    item.properties.append(property_name)
    

@when(parsers.parse('the user equips the "{item_name}"'))
def user_equips_item(session_context, item_name):
    char = session_context['character']
    char.inventory.equip_item(item_name)
    

@when(parsers.parse('the user unequips the "{item_name}"'))
def user_unequips_item(session_context, item_name):
    char = session_context['character']
    char.inventory.unequip_item(item_name)
    
    
@when(parsers.parse('the user checks their total inventory weight'))
def check_inventory_weight(session_context):
    char = session_context['character']
    session_context['calculated_weight'] = char.inventory.get_total_weight()


@then(parsers.parse('the item "{item_name}" should have properties "{properties_str}"'))
def check_item_properties(session_context, item_name, properties_str):
    char = session_context['character']
    item = char.inventory.get_item(item_name)
    assert item is not None, f"Item {item_name} not found in inventory"
    
    expected_props = [p.strip() for p in properties_str.split(',')]
    
    for prop in expected_props:
        assert prop in item.properties, f"Expecte property '{prop}' not found in {item.properties}"


@then(parsers.parse('the item "{item_name}" should be marked as equipped'))
def assert_item_equipped(session_context, item_name):
    char = session_context['character']
    item = char.inventory.get_item(item_name)
    assert item.equipped is True, f"Item {item_name} should be equipped"
    
    
@then(parsers.parse('the item "{item_name}" should be marked as unequipped'))
def assert_item_unequipped(session_context, item_name):
    char = session_context['character']
    item = char.inventory.get_item(item_name)
    assert item.equipped is False, f"Item {item_name} should be unequipped"


@then(parsers.parse('the total weight should be {expected_weight:f} lbs'))
def assert_total_weight(session_context, expected_weight):
    actual_weight = session_context['calculated_weight']
    assert actual_weight == expected_weight, f"Expected weight {expected_weight} lbs, but calculated {actual_weight} lbs"
