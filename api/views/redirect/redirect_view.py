from typing import Dict
from aiohttp import web
from aiohttp.web import json_response
from aiohttp_apispec import docs, querystring_schema

import logging

from marshmallow import Schema, fields

from .abstract_redirect_view import RedirectAbstractView
from ..api import soteria_web

logger = logging.getLogger('console')


class RedirectParamsSchema(Schema):
    code = fields.String(load_default=None)
    state = fields.String()


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
    async def get(self) -> web.Response:
        params: Dict = self.request['querystring']
        code = params.get("code")

        if code is None:
            raise web.HTTPNotFound(text="Code not found, aborting...")
        
        tokens = await self.get_tokens(code)

        return json_response({
            "access_token": tokens.access_token
        })
