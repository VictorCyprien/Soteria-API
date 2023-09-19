from typing import List
from aiohttp import web
import aiobungie
from aiohttp.web import json_response
from aiohttp_apispec import (
    docs,
    response_schema,
)

from marshmallow import Schema, fields

import logging
from .abstract_vendor_view import VendorAbstractView
from ..api import soteria_web

logger = logging.getLogger('console')

@soteria_web.view('/vendors')
class VendorsView(VendorAbstractView):

    @docs(
        summary="Vendors route",
        description="Get the list of vendors available in Destiny 2",
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
        access_token = self.request.headers['X-Access-Token']
        bungie_user_id = self.request.headers['X-Bungie-UserId']

        membership_id = await self.get_membership_id(bungie_user_id)
        membership_type = await self.get_membership_type(bungie_user_id)
        character_id = await self.get_characters_ids(membership_id, membership_type)

        list_vendors = await self.get_list_vendors(
            access_token,
            character_id[0],
            membership_id,
            membership_type
        )

        return json_response(data=list_vendors)
