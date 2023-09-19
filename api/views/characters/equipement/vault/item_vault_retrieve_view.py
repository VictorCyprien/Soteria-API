from aiohttp import web
from aiohttp.web import json_response
from aiohttp.web_exceptions import HTTPNotFound
from aiohttp_apispec import (
    docs,
    response_schema
)

import logging
from ..abstract_equipement_view import EquipementAbstractView
from ....api import soteria_web
from .....schemas.items_schemas import TransfertItemResponseSchema

logger = logging.getLogger('console')


@soteria_web.view('/characters/{character_id}/equipement/{item_id}/retrieve')
class VaultRetrieveItemView(EquipementAbstractView):
    @property
    def character_id(self) -> int:
        character_id = self.request.match_info.get('character_id', "None")
        #We raise a NotFound when the number is not a positive number
        if not character_id.isdigit():
            raise HTTPNotFound(text=f"The character ID #{character_id} is not valid !")
        return int(character_id)


    @property
    def item_id(self) -> int:
        item_id = self.request.match_info.get('item_id', "None")
        #We raise a NotFound when the number is not a positive number
        if not item_id.isdigit():
            raise HTTPNotFound(text=f"The item ID #{item_id} is not valid !")
        return int(item_id)


    @docs(
        summary="Retrieve an item",
        description="Retrieve an item (weapon, armor or other) from the vault for a character",
        responses={
            201: {"description": "Success response"},
            400: {"description": "Invalid request"},
            401: {"description": "Unauthorized"},
            404: {"description": "Item not found"},
            500: {"description": "Server error"},
            503: {"description": "Too many requests, wait a bit"},
        },
    )
    @response_schema(TransfertItemResponseSchema, 201, description="Success reponse")
    async def post(self) -> web.Response:
        character_id = self.character_id
        item_id = self.item_id
        access_token = str(self.request.headers['X-Access-Token'])
        bungie_user_id = int(self.request.headers['X-Bungie-Userid'])
    
        membership_id = await self.get_membership_id(bungie_user_id)
        membership_type = await self.get_membership_type(bungie_user_id)
    
        item_retrieved = await self.retrieve_item_from_vault(
            access_token,
            item_id,
            character_id,
            membership_id,
            membership_type
        )

        if not item_retrieved:
            raise HTTPNotFound(text="The item is not on in the Vault")

        return json_response(data={
            "status": "OK",
        })
