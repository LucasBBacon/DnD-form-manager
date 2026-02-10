from pytest_bdd import scenarios, parsers, when


scenarios("../features/custom_items.feature")

@when(parsers.parse('the user renames "{old_name}" to "{new_name}"'))
def rename_item(session_context, old_name, new_name):
    char = session_context['character']
    item = char.inventory.get_item(old_name)
    assert item is not None, f"Cannot rename: Item '{old_name}' no found."
    
    item.name = new_name
