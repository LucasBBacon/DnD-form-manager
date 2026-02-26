import pytest
from pytest_bdd import given, scenarios, parsers, then, when

from form_manager.src.models import Item
from form_manager.src.services import CurrencyService


scenarios("../features/shop.feature")


CURRENCY_MAP = {
    "copper piece": "cp",
    "copper pieces": "cp",
    "cp": "cp",
    "silver piece": "sp",
    "silver pieces": "sp",
    "sp": "sp",
    "electrum piece": "ep",
    "electrum pieces": "ep",
    "ep": "ep",
    "gold piece": "gp",
    "gold pieces": "gp",
    "gp": "gp",
    "platinum piece": "pp",
    "platinum pieces": "pp",
    "pp": "pp",
}


def get_currency_key(name: str) -> str:
    key = CURRENCY_MAP.get(name.lower())
    if not key:
        raise ValueError(f"Unknown currency: {name}")
    return key


def normalize_text(raw_input: str) -> str:
    return raw_input.lower().replace(" ", "_").replace("'", "")


@given(parsers.parse('the user has {amount:d} "{currency_name}" in their purse'))
def add_coinage_to_inventory(session_context, amount, currency_name):
    char = session_context["character"]
    currency = get_currency_key(currency_name)
    char.purse.update({currency: amount})


@given(parsers.parse('the user has a "{item_name}" in their inventory'))
def user_has_specific_item(session_context, rules_manager, item_name):
    char = session_context["character"]
    item = Item(name=item_name)
    template = rules_manager.get_item_template(item_name)
    if template:
        item.apply_template(template)
    char.inventory.add_item(item)


@given(
    parsers.parse('the user has a "{item_name}" worth "{cost_str}" in their inventory')
)
def given_user_has_item_worth(session_context, item_name, cost_str):
    char = session_context["character"]
    item = Item(name=item_name)
    value = Item.parse_cost(cost_str)
    item.cost.update(value)
    char.inventory.add_item(item)


@when(parsers.parse('the user buys a "{item_name}"'))
def buy_single_item(session_context, rules_manager, item_name):
    char = session_context["character"]

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


@when(parsers.parse('the user buys {count:d} "{item_name}"'))
def buy_multiple_items(session_context, rules_manager, count, item_name):
    char = session_context["character"]

    template = rules_manager.get_item_template(item_name)
    assert template, f"Item '{item_name}' not found in rules."

    item = Item(name=item_name)
    item.apply_template(template)

    total_cost = {currency: amount * count for currency, amount in item.cost.items()}

    currency_service = CurrencyService(rules_manager)
    success = char.pay_cost(total_cost, currency_service)

    if success:
        char.inventory.add_item(item, count)
    else:
        pytest.fail(f"Failed to buy '{item_name}' due to insufficient funds.")


@when(parsers.parse('the user attempts to buy "{item_name}"'))
def attempt_buy_items(session_context, rules_manager, item_name):
    char = session_context["character"]

    template = rules_manager.get_item_template(item_name)
    if not template and " armor" in item_name.lower():
        short_name = item_name.lower().replace(" armor", "")
        template = rules_manager.get_item_template(short_name)

    assert template, f"Item '{item_name}' not found in rules."

    item = Item(name=template.get("name", item_name))
    item.apply_template(template)

    currency_service = CurrencyService(rules_manager)
    success = char.pay_cost(item.cost, currency_service)

    session_context["last_transaction_success"] = success
    if success:
        char.inventory.add_item(item)


@when(parsers.parse('the user sells the "{item_name}"'))
def sell_item_standard(session_context, rules_manager, item_name):
    char = session_context["character"]
    currency_service = CurrencyService(rules_manager)

    item = char.inventory.get_item(item_name)
    assert item is not None, f"Cannot sell '{item_name}': Item not found in inventory."

    total_cost_cp = currency_service.convert_purse_to_cp(item.cost)
    sell_value_cp = total_cost_cp // 2

    currency_wealth_cp = currency_service.convert_purse_to_cp(char.purse)
    new_wealth_cp = currency_wealth_cp + sell_value_cp

    char.purse = currency_service.optimize_purse(new_wealth_cp, use_pp=False)
    char.inventory.remove_item(item_name)


@when(parsers.parse('the user sells the "{item_name}" for "{cost_str}"'))
def sell_item_for_specific_value(session_context, rules_manager, item_name, cost_str):
    char = session_context["character"]
    currency_service = CurrencyService(rules_manager)

    item = char.inventory.get_item(item_name)
    assert item is not None, f"Cannot sell '{item_name}': Item not found in inventory."

    sell_cost_dict = Item.parse_cost(cost_str)
    sell_value_cp = currency_service.convert_purse_to_cp(sell_cost_dict)
    current_wealth_cp = currency_service.convert_purse_to_cp(char.purse)

    new_wealth_cp = current_wealth_cp + sell_value_cp

    char.purse = currency_service.optimize_purse(new_wealth_cp, use_pp=False)

    char.inventory.remove_item(item_name)


@then(parsers.parse('the inventory should contain {count:d} "{item_name}"'))
def check_inventory_count(session_context, count, item_name):
    char = session_context["character"]
    found_count = char.inventory.get_item_count(item_name)
    assert found_count == count, f"Expected {count} of {item_name}, found {found_count}"


@then(parsers.parse('the inventory should not contain "{item_name}"'))
def check_inventory_does_not_contain(session_context, item_name):
    char = session_context["character"]
    assert not char.inventory.has_item(
        item_name
    ), f"Inventory should not contain '{item_name}', but it was found."


@then(parsers.parse("the character funds should show {gp:d} gp and {sp:d} sp"))
def check_funds_specific(session_context, gp, sp):
    char = session_context["character"]
    assert char.purse["gp"] == gp
    assert char.purse["sp"] == sp


@then("the transaction should fail")
def check_transaction_failed(session_context):
    success = session_context.get("last_transaction_success")
    assert success is False, "Expected transaction to fail, but it succeeded."
