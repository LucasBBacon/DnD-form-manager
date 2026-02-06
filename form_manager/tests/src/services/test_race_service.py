import os
import pytest

from form_manager.src.models import Character
from form_manager.src.services import RaceService


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RACE_DATA_PATH = os.path.join(BASE_DIR, '../../../src/resources/races/race_data.json')
TRAITS_DATA_PATH = os.path.join(BASE_DIR, '../../../src/resources/races/traits_data.json')

def test_race_service_missing_race_data_path_returns_empty_dict():
    service = RaceService("fake_path.json", TRAITS_DATA_PATH)
    assert service.race_data == {}
    assert service.traits_data != {}
    

def test_race_service_missing_traits_data_path_returns_empty_dict():
    service = RaceService(RACE_DATA_PATH, "fake_path.json")
    assert service.traits_data == {}
    assert service.race_data != {}
    

def test_apply_race_throws_value_error_if_race_does_not_exist():
    service = RaceService(RACE_DATA_PATH, TRAITS_DATA_PATH)
    with pytest.raises(ValueError):
        service.apply_race(Character(), "steven")