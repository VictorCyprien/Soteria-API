from typing import Dict
from aiohttp import web
from aiohttp.web import json_response
from aiohttp_apispec import (
    docs,
    response_schema
)
from aiohttp_cache import cache

from marshmallow import Schema, fields

import logging
from .api import soteria_web
from .root_abstract_view import AbstractView
from ..config import config

logger = logging.getLogger('console')


class IndexResponseSchema(Schema):
    name = fields.String()
    user = fields.String()
    user_id = fields.Integer(required=False)


@soteria_web.view('/')
@cache(expires=config.CACHE_TIME_EXPIRE)
class IndexView(AbstractView):

    @docs(
        summary="Index route",
        description="Index route",
        responses={
            200: {"description": "OK"},
            400: {"description": "Invalid request"},
            500: {"description": "Server error"},
        },
    )
    @response_schema(IndexResponseSchema(), 200, description="Success reponse")
    async def get(self) -> web.Response:
        res = {}
        res['name'] = config.SERVICE_NAME

        access_token = self.request.headers.get('X-Access-Token', None)
        if access_token is None:
            bungie_user = "Not Logged"
        else:
            access_token = str(access_token)
            bungie_user = await self.bungie.get_bungie_user(access_token)

        if isinstance(bungie_user, Dict):
            res["user"] = bungie_user["bungieNetUser"]["uniqueName"]
            res["user_id"] = bungie_user["bungieNetUser"]["membershipId"]
        else:
            res["user"] = bungie_user
        return json_response(data=res)
