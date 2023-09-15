from typing import Dict, List
from aiohttp import web
from aiohttp.web_exceptions import HTTPNotFound
import aiobungie
import logging

from ..client.bungie_api import BungieClient

logger = logging.getLogger('console')

class AbstractView(web.View):
    bungie = BungieClient()

    async def get_membership_with_id(self, bungie_user_id):
        async with self.bungie.client.acquire() as rest:
            user = await rest.fetch_membership_from_id(bungie_user_id)

        return user

    async def get_membership_id(self, bungie_user_id):
        user = await self.get_membership_with_id(bungie_user_id)
        try:
            membership_id = user["destinyMemberships"][0]["membershipId"]
        except (TypeError, KeyError):
            logger.warning("No profil info found...")
            raise HTTPNotFound(text="Profile not found")
        
        return membership_id
    

    async def get_membership_type(self, bungie_user_id):
        user = await self.get_membership_with_id(bungie_user_id)
        try:
            membership_type = user["destinyMemberships"][0]["membershipType"]
        except (TypeError, KeyError):
            logger.warning("No profil info found...")
            raise HTTPNotFound(text="Profile not found")
        
        return membership_type


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
        
        async with self.bungie.client.acquire() as rest:
            character = await rest.fetch_character(
                membership_id,
                membership_type,
                character_id,
                [aiobungie.ComponentType.CHARACTERS],
            )

        return character

    async def get_characters_infos(self, bungie_user_id: int, characters_ids: List[int]) -> Dict:
        membership_id = await self.get_membership_id(bungie_user_id)
        membership_type = await self.get_membership_type(bungie_user_id)
        
        characters = {}
        for one_character_id in characters_ids:
            async with self.bungie.client.acquire() as rest:
                characters[one_character_id] = await rest.fetch_character(
                    membership_id,
                    membership_type,
                    one_character_id,
                    [aiobungie.ComponentType.CHARACTERS],
                )

        return characters
    

    async def get_character_equipement(self, bungie_user_id: int, character_id: List[int]):
        membership_id = await self.get_membership_id(bungie_user_id)
        membership_type = await self.get_membership_type(bungie_user_id)
        
        async with self.bungie.client.acquire() as rest:
            character_equipement = await rest.fetch_character(
                membership_id,
                membership_type,
                character_id,
                [aiobungie.ComponentType.CHARACTER_EQUIPMENT],
            )

        return character_equipement
    

    def set_manifest_version(self, manifest_version: str):
        with open('./manifest-data/version.txt', 'w') as file:
            file.write(manifest_version)


    def get_manifest_version(self) -> str:
        data = ""
        try:
            with open('./manifest-data/version.txt', 'r') as file:
                data = file.read()
        except FileNotFoundError:
            logger.warning("Manifest version not found, proceed...")
        return data


    async def get_list_vendors(self, access_token: str, bungie_user_id: int) -> Dict:
        membership_id = await self.get_membership_id(bungie_user_id)
        membership_type = await self.get_membership_type(bungie_user_id)
        character_id = await self.get_characters_ids(bungie_user_id)

        async with self.bungie.client.acquire() as rest:
            list_vendors = await rest.fetch_vendors(
                access_token,
                character_id[0],
                membership_id,
                membership_type,
                [aiobungie.ComponentType.VENDORS]
            )

        return list_vendors
    

    async def get_one_vendor(self, access_token: str, bungie_user_id: int, vendor_id: int):
        membership_id = await self.get_membership_id(bungie_user_id)
        membership_type = await self.get_membership_type(bungie_user_id)
        character_id = await self.get_characters_ids(bungie_user_id)

        async with self.bungie.client.acquire() as rest:
            try:
                vendor = await rest.fetch_vendor(
                    access_token,
                    character_id[0],
                    membership_id,
                    membership_type,
                    vendor_id,
                    [aiobungie.ComponentType.VENDOR_SALES, aiobungie.ComponentType.VENDOR_RECEIPTS]
                )
            except aiobungie.HTTPError:
                raise HTTPNotFound(text="Vendor not found")


        return vendor
    