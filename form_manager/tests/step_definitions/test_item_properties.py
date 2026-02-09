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
    

@then(parsers.parse('the item "{item_name}" should have properties "{properties_str}"'))
def check_item_properties(session_context, item_name, properties_str):
    char = session_context['character']
    item = char.invetory.get_item(item_name)
    assert item is not None, f"Item {item_name} not found in inventory"
    
    expected_props = [p.strip() for p in properties_str.split(',')]
    
    for prop in expected_props:
        assert prop in item.properties, f"Expecte property '{prop}' not found in {item.properties}"
