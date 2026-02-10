import pytest
from pytest_bdd import given, scenarios, parsers, then, when

from form_manager.src.models import Character, Item


scenarios("../features/inventory_management.feature")
    

@given("the user inventory is empty")
def inventory_is_empty(session_context):
    char = session_context['character']
    assert len(char.inventory.items) == 0
    

@given(parsers.parse('the user has {count:d} "{item_name}" in their inventory'))
def user_has_items(session_context, count, item_name):
    char = session_context['character']
    item = Item(name=item_name, 
                stackable=True)
    char.inventory.add_item(item, count)
    

@when(parsers.parse('the user adds a "{item_name}" to their inventory'))
def add_single_item(session_context, item_name):
    char = session_context['character']
    item = Item(name=item_name)
    char.inventory.add_item(item)
    

@when(parsers.parse('the user adds {count:d} "{item_name}" to their inventory'))
def add_multiple_items(session_context, count, item_name):
    char = session_context['character']
    item = Item(name=item_name, stackable=True)
    char.inventory.add_item(item, count)
    

@when(parsers.parse('the user removes {count:d} "{item_name}"'))
def remove_items(session_context, count, item_name):
    char = session_context['character']
    char.inventory.remove_item(item_name, count)
    
    
@when(parsers.parse('the user creates a custom item named "{item_name}"'))
def create_custom_item(session_context, item_name):
    session_context['custom_item'] = Item(name=item_name)
    
    
@when("the user sets the item as non-stackable")
def set_non_stackabale(session_context):
    item = session_context.get('custom_item')
    item.stackable = False
    session_context['character'].inventory.add_item(item)
    
    
@then(parsers.parse('the inventory should contain {count:d} "{item_name}"'))
def check_inventory_count(session_context, count, item_name):
    char = session_context['character']
    found_count = char.inventory.get_item_count(item_name)
    assert found_count == count, f"Expected {count} of {item_name}, found {found_count}"
    
    
@then(parsers.parse('the inventory should contain "{item_name}"'))
def check_inventory_contains(session_context, item_name):
    char = session_context['character']
    assert char.inventory.has_item(item_name)
    

@then(parsers.parse('the item "{item_name}" should not be stackable'))
def check_not_stackable(session_context, item_name):
    char = session_context['character']
    item = char.inventory.get_item(item_name)
    assert item.stackable is False
    
    
@then(parsers.parse('the "{item_name}" entry should be marked as stackable'))
def check_stackable(session_context, item_name):
    char = session_context['character']
    item = char.inventory.get_item(item_name)
    assert item.stackable is True
    

@then(parsers.parse('the inventory should still have only {entry_count:d} entry for "{item_name}"'))
def check_inventory_entries(session_context, entry_count, item_name):
    char = session_context['character']
    entries = [i for i in char.inventory.items if i.name == item_name]
    assert len(entries) == entry_count


@then(parsers.parse('"{item_name}" should be removed from the inventory list'))
def check_item_removed(session_context, item_name):
    char = session_context['character']
    assert not char.inventory.has_item(item_name)
    

@then(parsers.parse('the inventory should not contain "{item_name}"'))
def check_inventory_does_not_contain(session_context, item_name):
    char = session_context['character']
    assert not char.inventory.has_item(item_name), f"Inventory should not contain '{item_name}', but it was found."
