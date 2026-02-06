from form_manager.src.models.character import Character


class RaceService:
    def __init__(self, race_data_path: str, traits_data_path: str) -> None:
        pass
    
    def apply_race(self, character: Character, race_key: str) -> Character:
        return Character()