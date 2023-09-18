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
from ...abstract_equipement_view import EquipementAbstractView
from .....api import soteria_web
from ......schemas.weapon_infos_schema import WeaponPayloadSchema
from ......config import config

logger = logging.getLogger('console')

class EquipResponseSchema(Schema):
    status = fields.String()

@soteria_web.view('/characters/{character_id}/equipement/weapon/{weapon_id}/equip')
class WeaponEquipView(EquipementAbstractView):
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
        summary="Equip Weapon",
        description="Equip a weapon for a character",
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
        weapon_id = self.weapon_id
        access_token = str(self.request.headers['X-Access-Token'])
        bungie_user_id = int(self.request.headers['X-Bungie-Userid'])

        membership_type = await self.get_membership_type(bungie_user_id)
        character_equipment = await self.get_character_equipement(bungie_user_id, character_id)

        if character_equipment.get("inventory", None) is None:
            raise HTTPNotFound(text="Character not found")

        if character_equipment["inventory"].get("data", None) is None:
            raise HTTPNotFound(text="The inventory is private")

        weapon_equipped = await self.equip_weapon(
            access_token,
            weapon_id,
            character_equipment,
            character_id,
            membership_type
        )

        if not weapon_equipped:
            raise HTTPNotFound(text="The weapon is already equipped or is not in the equipment")
                    
        return json_response(data={
            "status": "OK",
        })
