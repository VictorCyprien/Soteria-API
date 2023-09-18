from typing import Dict, List
from aiohttp.web_exceptions import HTTPNotFound
import aiobungie
import logging

from ...helpers.clean_characters_data import clean_characters_data
from .. import AbstractView

logger = logging.getLogger('console')


class VaultAbstractView(AbstractView):
    async def get_vault_content(self, access_token: str, membership_id: int, membership_type: int) -> Dict:
        async with self.bungie.client.acquire() as rest:
            vault = await rest.fetch_profile(
                membership_id,
                membership_type,
                [aiobungie.ComponentType.PROFILE_INVENTORIES],
                access_token
            )

        return vault
