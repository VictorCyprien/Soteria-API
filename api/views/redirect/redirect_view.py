from typing import Dict
from aiohttp import web
from aiohttp.web import json_response
from aiohttp_apispec import docs, querystring_schema, response_schema

import logging

from marshmallow import Schema, fields

from .abstract_redirect_view import RedirectAbstractView
from ..api import soteria_web
from ...helpers.errors_handler import NotFound, ReasonError

logger = logging.getLogger('console')


class RedirectParamsSchema(Schema):
    code = fields.String(load_default=None)
    state = fields.String()


class RedirectResponseSchema(Schema):
    access_token = fields.String()
    user_id = fields.Integer()


@soteria_web.view('/redirect')
class RedirectView(RedirectAbstractView):

    @docs(
        summary="This route is used by BungieAPI to retrive user's information",
        description="Get the informations of users",
        responses={
            200: {"description": "OK"},
            400: {"description": "Invalid request"},
            500: {"description": "Server error"},
        },
    )
    @querystring_schema(RedirectParamsSchema)
    @response_schema(RedirectResponseSchema, 200, description="Return a new access token and current user_id")
    async def get(self) -> web.Response:
        params: Dict = self.request['querystring']
        code = params.get("code")

        if code is None:
            raise NotFound(ReasonError.REDIRECT_ERROR.value)
        
        tokens = await self.get_tokens(code)
        user_id = await self.bungie.get_user_infos(tokens.access_token)

        return json_response({
            "access_token": tokens.access_token,
            "user_id": user_id["bungieNetUser"]["membershipId"]
        })
