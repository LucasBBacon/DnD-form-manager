import pytest
from pytest_bdd import given, scenarios, parsers, then, when

from form_manager.src.models import Item
from form_manager.src.services import CurrencyService


scenarios("../features/shop.feature")


CURRENCY_MAP = {
    "copper piece": "cp", "copper pieces": "cp", "cp": "cp",
    "silver piece": "sp", "silver pieces": "sp", "sp": "sp",
    "electrum piece": "ep", "electrum pieces": "ep", "ep": "ep",
    "gold piece": "gp", "gold pieces": "gp", "gp": "gp",
    "platinum piece": "pp", "platinum pieces": "pp", "pp": "pp",
}

def get_currency_key(name: str) -> str:
    key = CURRENCY_MAP.get(name.lower())
    if not key:
        raise ValueError(f"Unknown currency: {name}")
    return key


@given(parsers.parse('the user has {amount:d} "{currency_name}" in their purse'))
def add_coinage_to_inventory(session_context, amount, currency_name):
    char = session_context['character']
    currency = get_currency_key(currency_name)
    char.purse.update({currency: amount})


@when(parsers.parse('the user buys a "{item_name}"'))
def buy_single_item(session_context, rules_manager, item_name):
    char = session_context['character']

    template = rules_manager.get_item_template(item_name)
    assert template, f"Item '{item_name}' not found in rules."

    item = Item(name=item_name)
    item.apply_template(template)

    currency_service = CurrencyService(rules_manager)
    success = char.pay_cost(item.cost, currency_service)

    if success:
        char.inventory.add_item(item)
    else:
        pytest.fail(f"Failed to buy '{item_name}' due to insufficient funds.")


@then(parsers.parse('the inventory should contain {count:d} "{item_name}"'))
def check_inventory_count(session_context, count, item_name):
    char = session_context['character']
    found_count = char.inventory.get_item_count(item_name)
    assert found_count == count, f"Expected {count} of {item_name}, found {found_count}"


@then(parsers.parse('the character funds should show {gp:d} gp and {sp:d} sp'))
def check_funds_specific(session_context, gp, sp):
    char = session_context['character']
    assert char.purse['gp'] == gp
    assert char.purse['sp'] == sp
