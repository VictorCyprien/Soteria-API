from aiohttp import web
from aiohttp_apispec import (
    docs,
    response_schema
)

from marshmallow import Schema, fields

import logging
from ..api import soteria_web
from ..abstract_view import AbstractView

logger = logging.getLogger('console')

class ReponseGetSchema(Schema):
    status = fields.String()

@soteria_web.view('/login')
class LoginView(AbstractView):

    @docs(
        summary="Login route",
        description="Login route",
        responses={
            200: {"description": "OK"},
            400: {"description": "Invalid request"},
            500: {"description": "Server error"},
        },
    )
    @response_schema(ReponseGetSchema(), 200, description="Success reponse")
    async def get(self) -> web.Response:
        async with self.bungie.client.acquire() as rest:
            oauth_url = rest.build_oauth2_url()

            assert oauth_url is not None, "Make sure client ID and secret are set AND correct !"
            raise web.HTTPFound(location=oauth_url.url)
