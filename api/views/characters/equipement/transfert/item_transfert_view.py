from aiohttp import web
from aiohttp.web import json_response
from aiohttp_apispec import (
    docs,
    response_schema,
    request_schema
)

import logging
from ..abstract_equipement_view import EquipementAbstractView
from ....api import soteria_web
from .....schemas.items_schemas import TransfertItemResponseSchema
from .....schemas.items_schemas import ItemPayloadSchema
from .....helpers.errors_handler import NotFound, ReasonError

logger = logging.getLogger('console')


@soteria_web.view('/characters/{character_id}/equipement/{item_id}/transfert')
class ItemTransfertView(EquipementAbstractView):
    @property
    def character_id(self) -> int:
        character_id = self.request.match_info.get('character_id', "None")
        #We raise a NotFound when the number is not a positive number
        if not character_id.isdigit():
            raise NotFound(f"The character ID #{character_id} is not valid !")
        return int(character_id)


    @property
    def item_id(self) -> int:
        item_id = self.request.match_info.get('item_id', "None")
        #We raise a NotFound when the number is not a positive number
        if not item_id.isdigit():
            raise NotFound(f"The item ID #{item_id} is not valid !")
        return int(item_id)


    @docs(
        summary="Transfert an item",
        description="Transfert an item (weapon or armor) to a character",
        responses={
            201: {"description": "Success response"},
            400: {"description": "Invalid request"},
            401: {"description": "Unauthorized"},
            404: {"description": "Weapon or armor not found"},
            500: {"description": "Server error"},
            503: {"description": "Too many requests, wait a bit"},
        },
    )
    @request_schema(ItemPayloadSchema())
    @response_schema(TransfertItemResponseSchema, 201, description="Success reponse")
    async def post(self) -> web.Response:
        self.check_auth(self.request)
        
        character_id = self.character_id
        item_id = self.item_id
        access_token = str(self.request.headers['X-Access-Token'])
        bungie_user_id = int(self.request.headers['X-Bungie-Userid'])

        membership_id = await self.get_membership_id(bungie_user_id)
        membership_type = await self.get_membership_type(bungie_user_id)
        
        data = self.request["data"]
        character_id_pull_item = data["character_id_pull_item"]
        character_equipment = await self.get_character_equipement(
            character_id_pull_item,
            membership_id,
            membership_type
        )
        
        membership_type = await self.get_membership_type(bungie_user_id)
        item_transfered = await self.transfert_item(
            access_token,
            item_id,
            character_equipment,
            character_id_pull_item,
            character_id,
            membership_type
        )

        if not item_transfered:
            raise NotFound(ReasonError.ITEM_NOT_IN_CHARACTER.value)

        return json_response(data={
            "status": "OK",
        })
