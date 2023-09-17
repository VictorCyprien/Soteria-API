from typing import Dict
from aiohttp.web_exceptions import HTTPNotFound
import aiobungie
import logging

from .. import CharacterAbstractView

logger = logging.getLogger('console')


class VendorAbstractView(CharacterAbstractView):
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
    