from typing import Dict, List
from aiohttp.web_exceptions import HTTPNotFound
import aiobungie
import logging

from ...helpers.clean_characters_data import clean_characters_data
from .. import AbstractView

logger = logging.getLogger('console')


class CharacterAbstractView(AbstractView):
    async def get_characters_ids(self, bungie_user_id: int) -> List[str]:
        # cf https://github.com/Bungie-net/api/issues/147#issuecomment-330367099
        # Bungie ID != Destiny ID
        # Get membershipId to search list of characters
        membership_id = await self.get_membership_id(bungie_user_id)
        membership_type = await self.get_membership_type(bungie_user_id)

        # Get profile with characters infos
        async with self.bungie.client.acquire() as rest:
            user = await rest.fetch_profile(membership_id, membership_type, [aiobungie.ComponentType.PROFILE])

        # Get every character ID
        try:
            list_characters: List = user["profile"]["data"]["characterIds"]
        except KeyError:
            logger.warning("No character found for this profil...")
            raise HTTPNotFound(text="Character not found")

        return list_characters
    

    async def get_one_character_infos(self, bungie_user_id: int, character_id: List[int]) -> Dict:
        membership_id = await self.get_membership_id(bungie_user_id)
        membership_type = await self.get_membership_type(bungie_user_id)
        
        character = {}
        async with self.bungie.client.acquire() as rest:
            character_data = await rest.fetch_character(
                membership_id,
                membership_type,
                character_id,
                [aiobungie.ComponentType.CHARACTERS],
            )
            character[character_id] = clean_characters_data(character_data)

        return character


    async def get_characters_infos(self, bungie_user_id: int, characters_ids: List[int]) -> Dict:
        membership_id = await self.get_membership_id(bungie_user_id)
        membership_type = await self.get_membership_type(bungie_user_id)
        
        characters = {}
        for one_character_id in characters_ids:
            async with self.bungie.client.acquire() as rest:
                character_data = await rest.fetch_character(
                    membership_id,
                    membership_type,
                    one_character_id,
                    [aiobungie.ComponentType.CHARACTERS],
                )
                characters[one_character_id] = clean_characters_data(character_data)

        return characters
    

    async def get_character_equipement(self, bungie_user_id: int, character_id: int) -> Dict:
        membership_id = await self.get_membership_id(bungie_user_id)
        membership_type = await self.get_membership_type(bungie_user_id)
        
        async with self.bungie.client.acquire() as rest:
            character_equipement = await rest.fetch_character(
                membership_id,
                membership_type,
                character_id,
                [aiobungie.ComponentType.CHARACTER_INVENTORY],
            )

        return character_equipement
