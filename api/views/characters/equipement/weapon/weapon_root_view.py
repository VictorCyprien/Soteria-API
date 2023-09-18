from aiohttp import web
from aiohttp.web import json_response
from aiohttp.web_exceptions import HTTPNotFound
from aiohttp_apispec import (
    docs,
    response_schema,
    request_schema
)

from marshmallow import Schema, fields

import logging
from ....api import soteria_web
from ....abstract_view import AbstractView
from .....schemas.weapon_infos_schema import WeaponPayloadSchema

logger = logging.getLogger('console')

@soteria_web.view('/characters/{character_id}/equipement/weapon')
class WeaponView(AbstractView):
    @property
    def character_id(self) -> int:
        character_id = self.request.match_info.get('character_id', "None")
        #We raise a NotFound when the number is not a positive number
        if not character_id.isdigit():
            raise HTTPNotFound(text=f"The character ID #{character_id} is not valid !")
        return int(character_id)


    @docs(
        summary="Weapon route",
        description="Equip a weapon for a character",
        responses={
            200: {"description": "OK"},
            400: {"description": "Invalid request"},
            401: {"description": "Unauthorized"},
            500: {"description": "Server error"},
            503: {"description": "Too many requests, wait a bit"},
        },
    )
    @request_schema(WeaponPayloadSchema())
    #@response_schema(ReponseGetSchema(), 200, description="Success reponse")
    async def post(self) -> web.Response:
        character_id = self.character_id
        access_token = str(self.request.headers['X-Access-Token'])
        bungie_user_id = int(self.request.headers['X-Bungie-Userid'])
        data = self.request["data"]
        weapon_id = data["weapon_id"]
        membership_type = await self.get_membership_type(bungie_user_id)

        async with self.bungie.client.acquire() as rest:
            await rest.transfer_item(
                access_token,
                3,
                character_id,
                -1
            )
