from typing import Dict, List
import logging
import aiobungie
from aiobungie import HTTPError, InternalServerError, NotFound
from aiohttp.web_exceptions import HTTPBadRequest, HTTPNotFound

from ... import CharacterAbstractView

logger = logging.getLogger('console')


class EquipementAbstractView(CharacterAbstractView):

    async def get_equipment_object(
        self, 
        equipment_id: int,
        membership_id: int,
        membership_type: int
    ):
        async with self.bungie.client.acquire() as rest:
            try:
                item = await rest.fetch_item(
                    membership_id,
                    equipment_id,
                    membership_type,
                    [aiobungie.ComponentType.ALL_ITEMS]
                )
                logger.info(item)
            except NotFound as error:
                logger.exception(error)
                if error.error_status == "DestinyItemNotFound":
                    raise HTTPNotFound(text="This item doesn't exist")
        return item
    
    async def transfert_weapon(
        self, 
        access_token: str,
        weapon_id: int,
        character_equipment: Dict, 
        character_id_from: int, 
        character_id_to: int,
        membership_type: int
    ) -> bool:
        weapon_transfered = False
        for item in character_equipment["inventory"]["data"]["items"]:
            # Check the hash (ID) of the weapon payload and equipment
            item_instance_id = int(item.get("itemInstanceId", 0))
            if item_instance_id == weapon_id:
                # 0 : Can be tranfered
                # 1 : You can't transfert because it's already equip
                # 2 : Cannot be transfered
                # 4 : There is no space remaining for the item you want to tranfert
                if not item["transferStatus"] == 0:
                    if item["transferStatus"] == 1:
                        raise HTTPBadRequest(text="You can't transfert because it's already equip")
                    if item["transferStatus"] == 2:
                        raise HTTPBadRequest(text="This weapon cannot be transfered")
                    if item["transferStatus"] == 4:
                        raise HTTPBadRequest(text="There is no space remaining for the item you want to tranfert")
                
                async with self.bungie.client.acquire() as rest:
                    try:
                        await rest.transfer_item(
                            access_token,
                            item["itemInstanceId"],
                            item["itemHash"],
                            character_id_from,
                            membership_type,
                            vault=True
                        )
                        await rest.transfer_item(
                            access_token,
                            item["itemInstanceId"],
                            item["itemHash"],
                            character_id_to,
                            membership_type,
                        )
                        weapon_transfered = True
                    except HTTPError as error:
                        logger.warning(error)
                        raise HTTPNotFound(text="Something went wrong")
        return weapon_transfered


    async def equip_weapon(
        self, 
        access_token: str, 
        weapon_id: int, 
        character_equipment: Dict,
        character_id: int,
        membership_type: int
    ) -> bool:
        weapon_equipped = False
        for item in character_equipment["inventory"]["data"]["items"]:
            # Check the hash (ID) of the weapon payload and equipment
            item_instance_id = int(item.get("itemInstanceId", 0))
            if item_instance_id == weapon_id:
                async with self.bungie.client.acquire() as rest:
                    try:
                        await rest.equip_item(
                            access_token,
                            item["itemInstanceId"],
                            character_id,
                            membership_type
                        )
                        weapon_equipped = True
                    except InternalServerError as error:
                        if error.error_status == "DestinyItemUniqueEquipRestricted":
                            raise HTTPBadRequest(text="You can't equip more than two exotic weapon")
                        if error.error_status == "DestinyItemNotFound":
                            raise HTTPNotFound(text="This item doesn't exist")
        return weapon_equipped


    async def store_weapon_to_vault(
        self, 
        access_token: str, 
        weapon_id: int, 
        character_equipment: Dict,
        character_id: int,
        membership_type: int
    ):
        weapon_stored = False
        for item in character_equipment["inventory"]["data"]["items"]:
            # Check the hash (ID) of the weapon payload and equipment
            item_instance_id = int(item.get("itemInstanceId", 0))
            if item_instance_id == weapon_id:
                async with self.bungie.client.acquire() as rest:
                    try:
                        await rest.transfer_item(
                            access_token,
                            item["itemInstanceId"],
                            item["itemHash"],
                            character_id,
                            membership_type,
                            vault=True
                        )
                        weapon_stored = True
                    except InternalServerError as error:
                        logger.exception(error)
                        if error.error_status == "DestinyItemNotFound":
                            raise HTTPNotFound(text="This item doesn't exist")
        return weapon_stored
    

    async def retrieve_weapon_from_vault(
        self, 
        access_token: str, 
        weapon_id: int, 
        weapon_hash: int,
        character_id: int,
        membership_type: int
    ):
        weapon_retrieved = False
        async with self.bungie.client.acquire() as rest:
            try:
                await rest.transfer_item(
                    access_token,
                    weapon_id,
                    weapon_hash,
                    character_id,
                    membership_type,
                )
                weapon_retrieved = True
            except HTTPError as error:
                logger.warning(error)
                raise HTTPNotFound(text="Something went wrong")
            return weapon_retrieved