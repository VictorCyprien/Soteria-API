from typing import List
from aiohttp import web
import aiobungie
from aiohttp.web import json_response
from aiohttp_apispec import (
    docs,
    response_schema,
)

import logging
from .abstract_character_view import CharacterAbstractView
from ..api import soteria_web
from ...schemas.characters_infos_schema import CharactersResponseSchema

logger = logging.getLogger('console')

@soteria_web.view('/characters')
class CharacterView(CharacterAbstractView):

    @docs(
        summary="Characters route",
        description="Get the list characters ids of the current destiny 2 account",
        responses={
            200: {"description": "OK"},
            400: {"description": "Invalid request"},
            401: {"description": "Unauthorized"},
            500: {"description": "Server error"},
            503: {"description": "Too many requests, wait a bit"},
        },
    )
    @response_schema(CharactersResponseSchema, 200, description="Success reponse")
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
