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
from .....config import config

logger = logging.getLogger('console')

@soteria_web.view('/characters/{character_id}/equipement/armor/{armor_id}')
class ArmorView(EquipementAbstractView):
    @property
    def character_id(self) -> int:
        character_id = self.request.match_info.get('character_id', "None")
        #We raise a NotFound when the number is not a positive number
        if not character_id.isdigit():
            raise HTTPNotFound(text=f"The character ID #{character_id} is not valid !")
        return int(character_id)
    

    @property
    def armor_id(self) -> int:
        armor_id = self.request.match_info.get('armor_id', "None")
        #We raise a NotFound when the number is not a positive number
        if not armor_id.isdigit():
            raise HTTPNotFound(text=f"The armor ID #{armor_id} is not valid !")
        return int(armor_id)


    @docs(
        summary="Armor route",
        description="Get data armor for a character",
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
        armor_id = self.armor_id
        bungie_user_id = int(self.request.headers['X-Bungie-Userid'])
        membership_id = await self.get_membership_id(bungie_user_id)
        membership_type = await self.get_membership_type(bungie_user_id)
        
        character = await self.get_character_equipement(
            character_id,
            membership_id,
            membership_type
        )
        
        armor = {}
        for item in character["inventory"]["data"]["items"]:
            # Check the ID of the armor payload and equipment
            # (NOT THE HASH)
            item_instance_id = int(item.get("itemInstanceId", 0))
            if item_instance_id == armor_id:
                armor = await self.get_equipment_object(
                    armor_id,
                    membership_id,
                    membership_type
                )
                    
        return json_response(data=armor)
