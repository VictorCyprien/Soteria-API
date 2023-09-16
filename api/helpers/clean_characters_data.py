from typing import Dict
import logging

logger = logging.getLogger('console')

def clean_characters_data(character_data: Dict) -> Dict:
    clean_data = {}
    try:
        clean_data = character_data["character"]["data"]
    except KeyError:
        logger.warning("No character data found, abort cleaning...")
        return clean_data

    clean_data.pop("membershipId", None)
    clean_data.pop("membershipType", None)
    clean_data.pop("characterId", None)
    clean_data.pop("raceHash", None)
    clean_data.pop("genderHash", None)
    clean_data.pop("classHash", None)
    clean_data.pop("emblemColor", None)
    clean_data.pop("levelProgression", None)
    clean_data.pop("baseCharacterLevel", None)
    clean_data.pop("percentToNextLevel", None)

    return clean_data
