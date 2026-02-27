import json
from unittest.mock import mock_open, patch
import pytest

from form_manager.src.services import RulesManager


@pytest.fixture
def mock_rules_data():
    return {"races": {"dwarf": {}}}


def test_load_json_caches_result(mock_rules_data):
    with patch(
        "builtins.open", mock_open(read_data=json.dumps(mock_rules_data))
    ) as mock_file:
        manager = RulesManager("/fake/path")

        data = manager._load_json("test.json")
        assert data == mock_rules_data

        manager._load_json("test.json")
        assert mock_file.call_count == 1


def test_load_json_returns_empty_dict_on_missing_file():
    with patch("builtins.open", side_effect=FileNotFoundError):
        manager = RulesManager("/fake/path")
        data = manager._load_json("missing.json")
        assert data == {}


def test_property_accessors():
    manager = RulesManager("/fake/path")
    with patch.object(manager, "_load_json") as mock_load:
        _ = manager.races
        mock_load.assert_called_with("races/race_data.json")
