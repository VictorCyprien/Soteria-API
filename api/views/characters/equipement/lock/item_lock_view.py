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
from .....schemas.items_schemas import ItemLockSchema, EquipItemResponseSchema
from .....helpers.errors_handler import NotFound

logger = logging.getLogger('console')

@soteria_web.view('/characters/{character_id}/equipement/{item_id}/lock')
class ItemLockView(EquipementAbstractView):
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
        summary="Lock an item",
        description="Lock an item (weapon or armor)",
        responses={
            201: {"description": "Success reponse"},
            400: {"description": "Invalid request"},
            401: {"description": "Unauthorized"},
            404: {"description": "Weapon or armor not found"},
            500: {"description": "Server error"},
            503: {"description": "Too many requests, wait a bit"},
        },
    )
    @request_schema(ItemLockSchema())
    @response_schema(EquipItemResponseSchema, 201, description="Success reponse")
    async def post(self) -> web.Response:
        self.check_auth(self.request)
        
        character_id = self.character_id
        item_id = self.item_id
        access_token = str(self.request.headers['X-Access-Token'])
        bungie_user_id = int(self.request.headers['X-Bungie-Userid'])

        data = self.request["data"]
        lock_state = data["lock_state"]

        membership_type = await self.get_membership_type(bungie_user_id)

        await self.lock_item(
            access_token,
            lock_state,
            item_id,
            character_id,
            membership_type
        )
                    
        return json_response(data={
            "status": "OK",
        })
