import pytest

from form_manager.src.models import Item, DamageType, ArmorClass


def test_apply_template_full_weapon():
    item = Item(name="Test Sword")
    template = {
        "damage_dice": "1d8",
        "damage_type": "slashing",
        "properties": ["light", "finesse"],
        "weight": 2.5,
        "cost": {
            "cp": 0,
            "sp": 0,
            "ep": 0,
            "gp": 15,
            "pp": 0,
        },
    }

    item.apply_template(template)

    assert item.damage_dice == "1d8"
    assert item.damage_type == DamageType.SLASHING
    assert "light" in item.properties
    assert item.weight == 2.5
    assert item.cost == {"cp": 0, "sp": 0, "ep": 0, "gp": 15, "pp": 0}


def test_apply_template_armor_creation():
    item = Item(name="Test Armor")
    template = {
        "category": "Heavy Armor",
        "armor_class": {"base": 16, "dex_bonus": False, "max_dex_bonus": 0},
        "stealth_disadvantage": True,
    }

    item.apply_template(template)

    assert item.category == "Heavy Armor"
    assert isinstance(item.armor_class, ArmorClass)
    assert item.armor_class.base == 16
    assert item.armor_class.dex_bonus is False
    assert item.stealth_disadvantage is True


def test_make_improvised_overrides_stats():
    item = Item(name="Chair Leg", damage_dice="1d10", range="5")
    item.make_improvised()

    assert item.damage_dice == "1d4"
    assert item.range == "20/60"
