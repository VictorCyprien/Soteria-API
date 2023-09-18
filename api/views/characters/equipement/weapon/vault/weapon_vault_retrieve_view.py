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
from ......schemas.communs_schemas import TransfertResponseSchema

logger = logging.getLogger('console')


@soteria_web.view('/characters/{character_id}/equipement/weapon/{weapon_id}/retrieve')
class WeaponVaultRetrieveView(EquipementAbstractView):
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
        summary="Retrieve Weapon",
        description="Retrieve a weapon from the vault for a character",
        responses={
            201: {"description": "Success response"},
            400: {"description": "Invalid request"},
            401: {"description": "Unauthorized"},
            404: {"description": "Inventory or weapon not found"},
            500: {"description": "Server error"},
            503: {"description": "Too many requests, wait a bit"},
        },
    )
    @response_schema(TransfertResponseSchema, 201, description="Success reponse")
    async def post(self) -> web.Response:
        character_id = self.character_id
        weapon_id = self.weapon_id
        access_token = str(self.request.headers['X-Access-Token'])
        bungie_user_id = int(self.request.headers['X-Bungie-Userid'])
    
        membership_id = await self.get_membership_id(bungie_user_id)
        membership_type = await self.get_membership_type(bungie_user_id)
    
        weapon_retrieved = await self.retrieve_weapon_from_vault(
            access_token,
            weapon_id,
            character_id,
            membership_id,
            membership_type
        )

        if not weapon_retrieved:
            raise HTTPNotFound(text="The weapon is not on in the Vault")

        return json_response(data={
            "status": "OK",
        })
