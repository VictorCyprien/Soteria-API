from typing import Dict
import aiobungie
import logging

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
