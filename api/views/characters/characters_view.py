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

@soteria_web.view('/characters')
class CharacterView(AbstractView):

    @docs(
        summary="Characters route",
        description="Get the characters of the current destiny 2 account",
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
        bungie_user_id = int(self.request.headers['X-Bungie-Userid'])
        
        # Retrive list of characters
        characters_ids = await self.get_characters_ids(bungie_user_id)
        
        # Get every character infos
        characters = await self.get_characters_infos(
            bungie_user_id,
            characters_ids
        )

        return json_response(data=characters)
