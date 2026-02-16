import pytest

from form_manager.src.models import Inventory, Item


@pytest.fixture
def inventory():
    return Inventory()


def test_add_item_non_stackable(inventory):
    sword1 = Item(name="Sword", stackable=False)
    sword2 = Item(name="Sword", stackable=False)
    
    inventory.add_item(sword1)
    inventory.add_item(sword2)
    
    assert len(inventory.items) == 2
    assert inventory.get_item_count("Sword") == 1
    

def test_add_item_stackable(inventory):
    potion = Item(name="Potion", stackable=True)
    inventory.add_item(potion, count=5)
    
    potion_more = Item(name="Potion", stackable=True)
    inventory.add_item(potion_more, count=3)
    
    assert len(inventory.items) == 1
    assert inventory.items[0].quantity == 8
    

def test_remove_item_partial_stack(inventory):
    potion = Item(name="Potion", stackable=True, quantity=10)
    inventory.items.append(potion)
    
    inventory.remove_item("Potion", count=3)
    
    assert len(inventory.items) == 1
    assert inventory.items[0].quantity == 7

def test_remove_item_full_removal(inventory):
    sword = Item(name="Sword")
    inventory.add_item(sword)
    
    inventory.remove_item("Sword")
    
    assert len(inventory.items) == 0

def test_remove_missing_item_raises_error(inventory):
    with pytest.raises(ValueError, match="not found"):
        inventory.remove_item("NonExistent")

def test_get_total_weight(inventory):
    # 2 items @ 5lbs each + 1 item @ 10lbs
    item1 = Item(name="Heavy Thing", base_weight=5.0, stackable=True, quantity=2)
    item2 = Item(name="Big Thing", base_weight=10.0)
    
    inventory.items.append(item1)
    inventory.items.append(item2)
    
    assert inventory.get_total_weight() == 20.0

def test_total_value_calculation(inventory):
    item1 = Item(name="Gold Bar")
    item1.cost = {"cp": 0, "sp": 0, "ep": 0, "gp": 1, "pp": 0}
    
    item2 = Item(name="Silver Bar")
    item2.cost = {"cp": 0, "sp": 5, "ep": 0, "gp": 0, "pp": 0}
    
    inventory.add_item(item1)
    inventory.add_item(item2)
    
    assert inventory.get_total_value_in_cp() == 150