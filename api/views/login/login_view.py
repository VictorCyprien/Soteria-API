from aiohttp import web
from aiohttp.web import json_response
from aiohttp_apispec import (
    docs,
    response_schema
)

from marshmallow import Schema, fields

import logging
from .abstract_login_view import LoginAbstractView
from ..api import soteria_web

logger = logging.getLogger('console')

class ReponseLoginSchema(Schema):
    url = fields.String()

@soteria_web.view('/login')
class LoginView(LoginAbstractView):

    @docs(
        summary="Login route",
        description="Login route",
        responses={
            200: {"description": "OK"},
            400: {"description": "Invalid request"},
            500: {"description": "Server error"},
        },
    )
    @response_schema(ReponseLoginSchema(), 200, description="Generate a new OAuth link")
    async def get(self) -> web.Response:
        url = await self.generate_oauth_url()
        res = {
            "url": url.url
        }
        return json_response(data=res)
