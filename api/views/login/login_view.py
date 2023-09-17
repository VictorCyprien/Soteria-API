from aiohttp import web
from aiohttp_apispec import (
    docs,
    response_schema
)

from marshmallow import Schema, fields

import logging
from .abstract_login_view import LoginAbstractView
from ..api import soteria_web

logger = logging.getLogger('console')

class ReponseGetSchema(Schema):
    status = fields.String()

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
    @response_schema(ReponseGetSchema(), 302, description="Redirection to OAuth login")
    async def get(self) -> web.Response:
        await self.login()
