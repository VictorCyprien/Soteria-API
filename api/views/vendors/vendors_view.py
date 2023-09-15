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
from ..api import soteria_web
from ..abstract_view import AbstractView

logger = logging.getLogger('console')

@soteria_web.view('/vendors')
class VendorsView(AbstractView):

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

        list_vendors = await self.get_list_vendors(
            access_token,
            bungie_user_id
        )

        return json_response(data=list_vendors)
