from aiohttp import web
from aiohttp.web import json_response
from aiohttp_apispec import (
    docs,
    response_schema
)

import logging
from ..abstract_equipement_view import EquipementAbstractView
from ....api import soteria_web
from .....schemas.items_schemas import ItemInfoResponseSchema
from .....helpers.errors_handler import NotFound

logger = logging.getLogger('console')

@soteria_web.view('/characters/{character_id}/equipement/{item_id}')
class ItemInfoView(EquipementAbstractView):
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
        summary="Check infos of one item",
        description="Check the infos of one item (weapon or armor) for a character",
        responses={
            200: {"description": "Success reponse"},
            400: {"description": "Invalid request"},
            401: {"description": "Unauthorized"},
            404: {"description": "Weapon or armor not found"},
            500: {"description": "Server error"},
            503: {"description": "Too many requests, wait a bit"},
        },
    )
    @response_schema(ItemInfoResponseSchema, 200, description="Success reponse")
    async def get(self) -> web.Response:
        self.check_auth(self.request)
        
        item_id = self.item_id
        bungie_user_id = int(self.request.headers['X-Bungie-Userid'])

        membership_id = await self.get_membership_id(bungie_user_id)
        membership_type = await self.get_membership_type(bungie_user_id)

        item = await self.get_item_infos(
            item_id,
            membership_id,
            membership_type
        )
                    
        return json_response(data=item)
