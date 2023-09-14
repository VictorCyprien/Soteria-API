from aiohttp import web
from aiohttp.web import json_response
from aiohttp.web_exceptions import HTTPNotFound
from aiohttp_apispec import (
    docs,
    response_schema,
)

from marshmallow import Schema, fields

import logging
from ...api import soteria_web
from ...abstract_view import AbstractView

logger = logging.getLogger('console')

@soteria_web.view('/characters/{character_id}')
class OneCharacterView(AbstractView):

    @property
    def character_id(self) -> int:
        character_id = self.request.match_info.get('character_id', "None")
        #We raise a NotFound when the number is not a positive number
        if not character_id.isdigit():
            raise HTTPNotFound(text=f"The character ID #{character_id} is not valid !")
        return int(character_id)

    @docs(
        summary="One character route",
        description="Get the information of one character of the current destiny 2 account",
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
        character_id = self.character_id
        bungie_user_id = int(self.request.headers['X-Bungie-Userid'])
        
        # Get character info
        character = await self.get_one_character_infos(
            bungie_user_id,
            character_id
        )

        return json_response(data=character)
