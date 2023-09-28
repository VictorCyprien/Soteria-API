from aiohttp import web
from aiohttp.web import json_response
from aiohttp_apispec import (
    docs,
    response_schema,
)
from aiohttp_cache import cache

import logging
from .abstract_vault_view import VaultAbstractView
from ..api import soteria_web
from ...config import config

logger = logging.getLogger('console')

@soteria_web.view('/vault')
@cache(expires=config.CACHE_TIME_EXPIRE)
class VaultView(VaultAbstractView):

    @docs(
        summary="Vault route",
        description="Get the of the Vault for the current destiny 2 account",
        responses={
            200: {"description": "OK"},
            400: {"description": "Invalid request"},
            401: {"description": "Unauthorized"},
            500: {"description": "Server error"},
            503: {"description": "Too many requests, wait a bit"},
        },
    )
    async def get(self) -> web.Response:
        access_token = self.request.headers['X-Access-Token']
        bungie_user_id = int(self.request.headers['X-Bungie-Userid'])

        membership_id = await self.get_membership_id(bungie_user_id)
        membership_type = await self.get_membership_type(bungie_user_id)

        vault = await self.get_vault_content(
            access_token, 
            membership_id, 
            membership_type
        )

        return json_response(data=vault)
