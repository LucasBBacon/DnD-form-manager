from pytest_bdd import given, scenarios, parsers, then, when

from form_manager.src.models import Item


scenarios("../features/custom_items.feature")


def normalize_text(raw_input: str) -> str:
    return raw_input.lower().replace(" ", "_").replace("'", "")

def find_item(context, item_name):
    char = context['character']
    item = char.inventory.get_item(item_name)
    assert item is not None, f"Item {item_name} not found"
    return item


@given(parsers.parse('the user has a "{item_name}" in their inventory'))
def user_has_specific_item(session_context, rules_manager, item_name):
    char = session_context['character']
    item = Item(name=item_name)
    weapon_key = normalize_text(item_name)
    if weapon_data := rules_manager.weapons.get(weapon_key):
        item.apply_weapon_stats(weapon_data)
    char.inventory.add_item(item)


@when(parsers.parse('the user renames "{old_name}" to "{new_name}"'))
def rename_item(session_context, old_name, new_name):
    char = session_context['character']
    item = char.inventory.get_item(old_name)
    assert item is not None, f"Cannot rename: Item '{old_name}' no found."
    
    item.name = new_name
    

@when(parsers.parse('the user creates an item "{item_name}" using the "{template_name}" template'))
def create_item_from_template(session_context, rules_manager, item_name, template_name):
    char = session_context['character']
    item = Item(name=item_name)
    template_data = rules_manager.get_item_template(template_name)
    assert template_data is not None, f"Template '{template_name}' not found."
    item.apply_template(template_data)
    char.inventory.add_item(item)
    session_context['custom_item'] = item


@when(parsers.parse('the user sets the item weight to {new_weight} lbs'))
def set_item_weight(session_context, new_weight):
    item = session_context['custom_item']
    item.weight = float(new_weight)


@then(parsers.parse('the inventory should contain "{item_name}"'))
def check_inventory_contains(session_context, item_name):
    char = session_context['character']
    assert char.inventory.has_item(item_name)
    

@then(parsers.parse('the inventory should not contain "{item_name}"'))
def check_inventory_does_not_contain(session_context, item_name):
    char = session_context['character']
    assert not char.inventory.has_item(item_name), f"Inventory should not contain '{item_name}', but it was found."
    

@then(parsers.parse('the item "{item_name}" should have a damage die of "{dice}"'))
def check_item_damage_die(session_context, item_name, dice):
    char = session_context['character']
    item = char.inventory.get_item(item_name)
    assert item.damage_dice == dice, f"Expected damage die {dice}, but got {item.damage_dice}"


@then(parsers.parse('the item "{item_name}" should have properties "{properties_str}"'))
def check_item_properties(session_context, item_name, properties_str):
    char = session_context['character']
    item = char.inventory.get_item(item_name)
    assert item is not None, f"Item {item_name} not found in inventory"
    
    expected_props = [p.strip().lower() for p in properties_str.split(',')]
    
    for prop in expected_props:
        assert prop in item.properties, f"Expected property '{prop}' not found in {item.properties}"


@then(parsers.parse('the item "{item_name}" should have a weight of {expected_weight} lbs'))
def assert_total_weight(session_context, item_name, expected_weight):
    expected_weight = float(expected_weight)
    actual_weight = find_item(session_context, item_name).weight
    assert actual_weight == expected_weight, f"Expected weight {expected_weight} lbs, but actual weight is {actual_weight} lbs"
    

@then(parsers.parse('the item "{item_name}" should be Category "{category_name}"'))
def check_item_category(session_context, item_name, category_name):
    expected_category = category_name
    actual_category = find_item(session_context, item_name).category
    assert actual_category == expected_category, f"Expected item category of {expected_category}, but was {actual_category}"
