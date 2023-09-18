from aiohttp import web
from aiohttp.web import json_response
from aiohttp.web_exceptions import HTTPNotFound
from aiohttp_apispec import (
    docs,
    response_schema
)

import logging
from ...abstract_equipement_view import EquipementAbstractView
from .....api import soteria_web
from ......schemas.communs_schemas import EquipResponseSchema

logger = logging.getLogger('console')

@soteria_web.view('/characters/{character_id}/equipement/armor/{armor_id}/equip')
class ArmorEquipView(EquipementAbstractView):
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
        summary="Equip armor",
        description="Equip a armor for a character",
        responses={
            201: {"description": "Success reponse"},
            400: {"description": "Invalid request"},
            401: {"description": "Unauthorized"},
            404: {"description": "Inventory or weapon not found"},
            500: {"description": "Server error"},
            503: {"description": "Too many requests, wait a bit"},
        },
    )
    @response_schema(EquipResponseSchema, 201, description="Success reponse")
    async def post(self) -> web.Response:
        character_id = self.character_id
        armor_id = self.armor_id
        access_token = str(self.request.headers['X-Access-Token'])
        bungie_user_id = int(self.request.headers['X-Bungie-Userid'])

        membership_id = await self.get_membership_id(bungie_user_id)
        membership_type = await self.get_membership_type(bungie_user_id)

        character_equipment = await self.get_character_equipement(
            character_id,
            membership_id,
            membership_type
        )

        armor_equipped = await self.equip_weapon(
            access_token,
            armor_id,
            character_equipment,
            character_id,
            membership_type
        )

        if not armor_equipped:
            raise HTTPNotFound(text="The armor is already equipped or is not in the equipment")
                    
        return json_response(data={
            "status": "OK",
        })
