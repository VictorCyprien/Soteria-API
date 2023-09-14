from typing import Dict
import aiobungie
from aiohttp.client_exceptions import ClientConnectionError
import json
import logging
from types import SimpleNamespace

from ..config import config

logger: logging.Logger = logging.getLogger('console')

class BungieClient():
    
    def __init__(self) -> None:
        self.client = aiobungie.RESTPool(
            config.BUNGIE_API_KEY, 
            client_secret=config.BUNGIE_API_CLIENT_SECRET, 
            client_id=config.BUNGIE_API_CLIENT_ID
        )


    async def get_user_infos(self, access_token: str):
        try:
            async with self.client.acquire() as rest:
                user_data = await rest.fetch_current_user_memberships(access_token)
        except aiobungie.HTTPError:
            logger.warning("No user found for this access token, abort...")
            return "Not Logged"
        except ClientConnectionError:
            logger.warning("Unabled to connect to Bungie API, please try again...")
            return "Not Logged"
        return user_data if isinstance(user_data, Dict) else await user_data
    


    async def get_bungie_user(self, access_token: str):
        user_data = self.get_user_infos(access_token)
        return user_data if isinstance(user_data, Dict) else await user_data
