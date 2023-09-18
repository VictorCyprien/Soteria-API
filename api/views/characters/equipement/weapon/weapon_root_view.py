from aiohttp import web
from aiohttp.web import json_response
from aiobungie import HTTPError, InternalServerError
from aiohttp.web_exceptions import HTTPNotFound
from aiohttp_apispec import (
    docs,
    response_schema,
    request_schema
)

from marshmallow import Schema, fields

import logging
from ..abstract_equipement_view import EquipementAbstractView
from ....api import soteria_web
from .....schemas.weapon_infos_schema import WeaponPayloadSchema
from .....config import config

logger = logging.getLogger('console')

@soteria_web.view('/characters/{character_id}/equipement/weapon/{weapon_id}')
class WeaponView(EquipementAbstractView):
    @property
    def character_id(self) -> int:
        character_id = self.request.match_info.get('character_id', "None")
        #We raise a NotFound when the number is not a positive number
        if not character_id.isdigit():
            raise HTTPNotFound(text=f"The character ID #{character_id} is not valid !")
        return int(character_id)
    

    @property
    def weapon_id(self) -> int:
        weapon_id = self.request.match_info.get('weapon_id', "None")
        #We raise a NotFound when the number is not a positive number
        if not weapon_id.isdigit():
            raise HTTPNotFound(text=f"The weapon ID #{weapon_id} is not valid !")
        return int(weapon_id)


    @docs(
        summary="Weapon route",
        description="Get data weapon for a character",
        responses={
            200: {"description": "OK"},
            400: {"description": "Invalid request"},
            401: {"description": "Unauthorized"},
            500: {"description": "Server error"},
            503: {"description": "Too many requests, wait a bit"},
        },
    )
    #@request_schema(WeaponPayloadSchema())
    #@response_schema(ReponseGetSchema(), 200, description="Success reponse")
    async def get(self) -> web.Response:
        character_id = self.character_id
        weapon_id = self.weapon_id
        bungie_user_id = int(self.request.headers['X-Bungie-Userid'])

        character = await self.get_character_equipement(bungie_user_id, character_id)
        if character.get("inventory", None).get("data", None) is None:
            raise HTTPNotFound("The inventory is private")
        
        weapon = {}
        for item in character["inventory"]["data"]["items"]:
            # Check the hash (ID) of the weapon payload and equipment
            if item["itemHash"] == weapon_id:
                assert item.get("itemInstanceId", None) is not None, "The instance ID of the item is None..."
                weapon = item
                    
        return json_response(data=weapon)
