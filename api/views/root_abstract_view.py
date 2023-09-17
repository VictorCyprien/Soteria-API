from aiohttp import web
from aiohttp.web_exceptions import HTTPNotFound
import logging

from ..client.bungie_api import BungieClient

logger = logging.getLogger('console')

class AbstractView(web.View):
    bungie = BungieClient()

    async def get_membership_with_id(self, bungie_user_id):
        #TODO : Add try/except when ID is wrong...
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
