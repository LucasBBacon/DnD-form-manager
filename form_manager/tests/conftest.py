import os
import pytest

from form_manager.src.services import RulesManager
from form_manager.src.models import Character


@pytest.fixture(scope="function")
def session_context():
    return {}


@pytest.fixture(scope="session")
def rules_manager():
    base_directory = os.path.dirname(os.path.abspath(__file__))
    resources_directory = os.path.join(base_directory, '../src/resources')
    return RulesManager(resources_directory)


@pytest.fixture
def new_character_session(session_context):
    session_context['character'] = Character()