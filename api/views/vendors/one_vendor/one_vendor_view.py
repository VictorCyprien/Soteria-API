from aiohttp import web
from aiohttp.web import json_response
from aiohttp_apispec import (
    docs,
    response_schema,
)
from aiohttp_cache import cache

import logging
from ..abstract_vendor_view import VendorAbstractView
from ...api import soteria_web
from ....config import config
from ....helpers.errors_handler import NotFound

logger = logging.getLogger('console')

@soteria_web.view('/vendors/{vendor_id}')
@cache(expires=config.CACHE_TIME_EXPIRE)
class OneVendorView(VendorAbstractView):

    @property
    def vendor_id(self) -> int:
        vendor_id = self.request.match_info.get('vendor_id', "None")
        #We raise a NotFound when the number is not a positive number
        if not vendor_id.isdigit():
            raise NotFound(text=f"The vendor ID #{vendor_id} is not valid !")
        return int(vendor_id)

    @docs(
        summary="One Vendor route",
        description="Get the informations of one vendor",
        responses={
            200: {"description": "OK"},
            400: {"description": "Invalid request"},
            401: {"description": "Unauthorized"},
            500: {"description": "Server error"},
            503: {"description": "Too many requests, wait a bit"},
        },
    )
    #@response_schema(ReponseGetSchema(), 200, description="Success reponse")
    async def get(self) -> web.Response:
        self.check_auth(self.request)
        
        access_token = self.request.headers['X-Access-Token']
        bungie_user_id = self.request.headers['X-Bungie-UserId']
        vendor_id = self.vendor_id

        membership_id = await self.get_membership_id(bungie_user_id)
        membership_type = await self.get_membership_type(bungie_user_id)
        character_id = await self.get_characters_ids(membership_id, membership_type)

        vendor = await self.get_one_vendor(
            access_token,
            character_id[0],
            membership_id,
            membership_type,
            vendor_id
        )

        return json_response(data=vendor)
