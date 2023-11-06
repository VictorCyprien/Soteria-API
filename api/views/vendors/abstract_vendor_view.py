from typing import Dict
import aiobungie
import logging

from .. import CharacterAbstractView
from ...helpers.errors_handler import NotFound, ReasonError

logger = logging.getLogger('console')


class VendorAbstractView(CharacterAbstractView):
    async def get_list_vendors(
        self, 
        access_token: str, 
        character_id: int, 
        membership_id: int, 
        membership_type: int
    ) -> Dict:

        async with self.bungie.client.acquire() as rest:
            list_vendors = await rest.fetch_vendors(
                access_token,
                character_id,
                membership_id,
                membership_type,
                [
                    aiobungie.ComponentType.VENDORS,
                    aiobungie.ComponentType.VENDOR_CATEGORIES,
                ]
            )

        return list_vendors
    

    async def get_one_vendor(
        self, 
        access_token: str,
        character_id: int, 
        membership_id: int, 
        membership_type: int, 
        vendor_id: int
    ) -> Dict:
        
        async with self.bungie.client.acquire() as rest:
            try:
                vendor = await rest.fetch_vendor(
                    access_token,
                    character_id,
                    membership_id,
                    membership_type,
                    vendor_id,
                    [
                        aiobungie.ComponentType.VENDORS,
                        aiobungie.ComponentType.VENDOR_SALES
                    ]
                )
            except aiobungie.HTTPError:
                raise NotFound(ReasonError.VENDOR_NOT_FOUND.value)

        return vendor
    