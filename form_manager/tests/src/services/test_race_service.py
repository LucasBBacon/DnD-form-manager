import os
import pytest

from form_manager.src.models import Character
from form_manager.src.services import RaceService
from form_manager.src.services.rules_manager import RulesManager


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(BASE_DIR, '../../../src/resources')
    

def test_apply_race_throws_value_error_if_race_does_not_exist():
    rules_manager = RulesManager(RESOURCES_DIR)
    service = RaceService(rules_manager)
    with pytest.raises(ValueError):
        service.apply_race(Character(), "steven")