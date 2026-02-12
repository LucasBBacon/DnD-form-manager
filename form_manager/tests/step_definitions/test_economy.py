import pytest
from pytest_bdd import given, scenarios, parsers, then, when

from form_manager.src.models import Item
from form_manager.src.services import CurrencyService


scenarios("../features/economy.feature")


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


@given(parsers.parse('the user adds a "{item_name}" worth "{cost_str}" to their inventory'))
def add_item_worth_cost(session_context, item_name, cost_str):
    char = session_context['character']
    item = Item(name=item_name)
    value = Item.parse_cost(cost_str)
    item.cost.update(value)
    char.inventory.add_item(item)


@given(parsers.parse('the user has {amount:d} "{currency_name}" in their purse'))
def add_coinage_to_inventory(session_context, amount, currency_name):
    char = session_context['character']
    currency = get_currency_key(currency_name)
    char.purse.update({currency: amount})


@when(parsers.parse('the user adds {amount:d} "{currency_name}" to their purse'))
def add_coinage(session_context, amount, currency_name):
    char = session_context['character']
    key = get_currency_key(currency_name)
    char.purse[key] += amount
    
    
@when(parsers.parse('the user removes {amount:d} "{currency_name}"'))
def remove_coinage(session_context, amount, currency_name):
    char = session_context['character']
    key = get_currency_key(currency_name)
    if char.purse[key] < amount:
        pytest.fail(f"Not enough {key} to remove {amount}")
    char.purse[key] -= amount


@when('the user checks their total inventory value')
def calculate_inventory_value(session_context):
    char = session_context['character']
    session_context['inventory_value'] = char.inventory.get_total_value_in_cp()
    

@when(parsers.parse('the user attempts to buy an item costing {amount:d} "{currency_name}"'))    
def buy_item_costing(session_context, rules_manager, amount, currency_name):
    char = session_context['character']
    key = get_currency_key(currency_name)
    cost = {key: amount}
    success = char.pay_cost(cost, CurrencyService(rules_manager))
    session_context['purchase_success'] = success

    
@then(parsers.parse('the character funds should show {gp:d} gp and {sp:d} sp'))
def check_funds_specific(session_context, gp, sp):
    char = session_context['character']
    assert char.purse['gp'] == gp
    assert char.purse['sp'] == sp
    
    
@then(parsers.parse('the character funds should show {amount:d} {currency_key}'))
def check_single_fund(session_context, amount, currency_key):
    char = session_context['character']
    key = get_currency_key(currency_key)
    assert char.purse[key] == amount


@then(parsers.parse('the total value should be "{expected_value_str}"'))
def check_inventory_value(session_context, expected_value_str):
    actual_cp = session_context['inventory_value']
    parsed_expected = Item.parse_cost(expected_value_str)
    
    expected_cp = 0
    expected_cp += parsed_expected.get('cp', 0)
    expected_cp += parsed_expected.get('sp', 0) * 10
    expected_cp += parsed_expected.get('ep', 0) * 50
    expected_cp += parsed_expected.get('gp', 0) * 100
    expected_cp += parsed_expected.get('pp', 0) * 1000
    
    assert actual_cp == expected_cp, f"Expected value {expected_value_str} ({expected_cp} cp), but got {actual_cp} cp"


@then("the purchase should be successful")
def check_purchase_sucess(session_context):
    assert session_context.get('purchase_success') is True, "Purchase failed unexpectedly"
    

@then(parsers.parse('the purse should contain {amount:d} "{currency_name}"'))
def check_purse_contains(session_context, amount, currency_name):
    char = session_context['character']
    key = get_currency_key(currency_name)
    assert char.purse[key] == amount, f"Expected purse to contain {amount} {key}, but found {char.purse[key]} {key}"
