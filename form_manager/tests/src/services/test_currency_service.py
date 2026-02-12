import pytest
from unittest.mock import Mock
from form_manager.src.services.currency_service import CurrencyService
from form_manager.src.services.rules_manager import RulesManager

@pytest.fixture
def mock_rules_manager():
    manager = Mock(spec=RulesManager)
    manager.currency = {
        "cp": {"value": 1, "aliases": ["copper", "cp"]},
        "sp": {"value": 10, "aliases": ["silver", "sp"]},
        "ep": {"value": 50, "aliases": ["electrum", "ep"]},
        "gp": {"value": 100, "aliases": ["gold", "gp"]},
        "pp": {"value": 1000, "aliases": ["platinum", "pp"]}
    }
    return manager

@pytest.fixture
def service(mock_rules_manager):
    return CurrencyService(mock_rules_manager)

def test_normalize_currency(service):
    assert service.normalize_currency("Gold") == "gp"
    assert service.normalize_currency("cp") == "cp"
    assert service.normalize_currency("silver") == "sp"
    assert service.normalize_currency("Unknown") is None

def test_convert_purse_to_cp(service):
    purse = {
        "gp": 1,  # 100 cp
        "sp": 5,  # 50 cp
        "cp": 3   # 3 cp
    }
    assert service.convert_purse_to_cp(purse) == 153

def test_optimize_purse_simple(service):
    # 150 cp -> 1 gp (100), 5 sp (50)
    total_cp = 150
    optimized = service.optimize_purse(total_cp)
    
    assert optimized["gp"] == 1
    assert optimized["sp"] == 5
    assert optimized["cp"] == 0
    assert optimized["pp"] == 0

def test_optimize_purse_complex(service):
    # 1105 cp -> 1 pp (1000), 1 gp (100), 5 cp (5)
    # Note: EP (50) is usually skipped in standard optimization logic 
    # unless specifically requested, based on your implementation that skips 'ep'.
    total_cp = 1105
    optimized = service.optimize_purse(total_cp)
    
    assert optimized["pp"] == 1
    assert optimized["gp"] == 1
    assert optimized["sp"] == 0
    assert optimized["cp"] == 5
    assert optimized["ep"] == 0