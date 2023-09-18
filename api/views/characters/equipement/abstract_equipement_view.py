from typing import Dict, List
import logging
import aiobungie
from aiobungie import HTTPError, InternalServerError, NotFound
from aiohttp.web_exceptions import HTTPBadRequest, HTTPNotFound

from ... import CharacterAbstractView

logger = logging.getLogger('console')


class EquipementAbstractView(CharacterAbstractView):

    def get_item_in_equipment(self, character_equipment: Dict, item_id: int, isVault: bool = False) -> Dict:
        item_searched = {}
        items = character_equipment["inventory"]["data"]["items"] if not isVault else \
            character_equipment["profileInventory"]["data"]["items"]
        for item in items:
            # Check the hash (ID) of the weapon payload and equipment
            item_instance_id = int(item.get("itemInstanceId", 0))
            if item_instance_id == item_id:
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
                item_searched = item
        return item_searched
    

    async def get_item(
        self, 
        item_id: int,
        membership_id: int,
        membership_type: int
    ):
        async with self.bungie.client.acquire() as rest:
            try:
                item = await rest.fetch_item(
                    membership_id,
                    item_id,
                    membership_type,
                    [aiobungie.ComponentType.ALL_ITEMS]
                )
                logger.info(item)
            except NotFound as error:
                logger.exception(error)
                if error.error_status == "DestinyItemNotFound":
                    raise HTTPNotFound(text="This item doesn't exist")
        return item
    
    async def transfert_item(
        self, 
        access_token: str,
        item_id: int,
        character_equipment: Dict, 
        character_id_from: int, 
        character_id_to: int,
        membership_type: int
    ) -> bool:
        item_transfered = False
        item = self.get_item_in_equipment(character_equipment, item_id)
        if item:
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
                    item_transfered = True
                except HTTPError as error:
                    logger.warning(error)
                    raise HTTPNotFound(text="Something went wrong")
        return item_transfered


    async def equip_item(
        self, 
        access_token: str, 
        item_id: int, 
        character_equipment: Dict,
        character_id: int,
        membership_type: int
    ) -> bool:
        item_equipped = False
        item = self.get_item_in_equipment(character_equipment, item_id)
        if item:
            async with self.bungie.client.acquire() as rest:
                try:
                    await rest.equip_item(
                        access_token,
                        item["itemInstanceId"],
                        character_id,
                        membership_type
                    )
                    item_equipped = True
                except InternalServerError as error:
                    if error.error_status == "DestinyItemUniqueEquipRestricted":
                        raise HTTPBadRequest(text="You can't equip more than two exotic weapon")
                    if error.error_status == "DestinyItemNotFound":
                        raise HTTPNotFound(text="This item doesn't exist")
        return item_equipped


    async def store_item_to_vault(
        self, 
        access_token: str, 
        item_id: int, 
        character_equipment: Dict,
        character_id: int,
        membership_type: int
    ):
        item_stored = False
        item = self.get_item_in_equipment(character_equipment, item_id)
        if item:
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
                    item_stored = True
                except InternalServerError as error:
                    logger.exception(error)
                    if error.error_status == "DestinyItemNotFound":
                        raise HTTPNotFound(text="This item doesn't exist")
        return item_stored
    

    async def retrieve_item_from_vault(
        self, 
        access_token: str, 
        item_id: int,
        character_id: int,
        membership_id: int,
        membership_type: int
    ):
        item_retrieved = False

        # Get vault content
        async with self.bungie.client.acquire() as rest:
            vault_content = await rest.fetch_profile(
                membership_id,
                membership_type,
                [aiobungie.ComponentType.PROFILE_INVENTORIES],
                access_token
            )
        
        item = self.get_item_in_equipment(vault_content, item_id, isVault=True)
        if item:
            async with self.bungie.client.acquire() as rest:
                try:
                    await rest.transfer_item(
                        access_token,
                        item["itemInstanceId"],
                        item["itemHash"],
                        character_id,
                        membership_type,
                    )
                    item_retrieved = True
                except HTTPError as error:
                    logger.warning(error)
                    raise HTTPNotFound(text="Something went wrong")

        return item_retrieved


    async def lock_item(
        self, 
        access_token: str,
        lock_state: bool,
        item_id: int, 
        character_id: int,
        membership_type: int
    ) -> bool:
        item_locked = False
        async with self.bungie.client.acquire() as rest:
            try:
                await rest.set_item_lock_state(
                    access_token,
                    lock_state,
                    item_id,
                    character_id,
                    membership_type
                )
                item_locked = True
            except InternalServerError as error:
                logger.exception(error)
                assert False
                if error.error_status == "DestinyItemNotFound":
                    raise HTTPNotFound(text="This item doesn't exist")
        return item_locked
