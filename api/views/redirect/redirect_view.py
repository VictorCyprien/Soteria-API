from typing import Dict
from aiohttp import web
from aiohttp.web import json_response
from aiohttp_apispec import docs, querystring_schema

import logging

from marshmallow import Schema, fields

from ..api import soteria_web
from ..abstract_view import AbstractView

logger = logging.getLogger('console')


class RedirectParamsSchema(Schema):
    code = fields.String(load_default=None)
    state = fields.String()


@soteria_web.view('/redirect')
class RedirectView(AbstractView):

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
        
        async with self.bungie.client.acquire() as rest:
            tokens = await rest.fetch_oauth2_tokens(code)
            self.bungie.client.metadata["token"] = tokens.access_token


        # TODO : Return the token to client

        return json_response({
            "access_token": tokens.access_token
        })
