from enum import Enum

from aiohttp.web_exceptions import HTTPBadRequest, HTTPNotFound, HTTPUnauthorized

class BadRequest(HTTPBadRequest):
    def __init__(self, message: str = None) -> None:
        super().__init__(
            reason=f"BadRequest : {message}"
        )


class NotFound(HTTPNotFound):
    def __init__(self, message: str = None) -> None:
        super().__init__(
            reason=f"NotFound : {message}"
        )


class Unauthorized(HTTPUnauthorized):
    def __init__(self, message: str = None) -> None:
        super().__init__(
            reason=f"Unauthorized : {message}"
        )


class ReasonError(Enum):
    PROFILE_NOT_FOUND = "Profile not found"
    NOT_AUTHENTICATED = "Not Authenticated"
    CHARACTER_NOT_FOUND = "Character not found"
    ITEM_NOT_FOUND = "This item doesn't exist"
    ITEM_NOT_IN_CHARACTER = "The item is not on this character"
    ITEM_NOT_FOUND_IN_INVENTORY = "Item not found in the inventory"
    EQUIPMENT_CANNOT_BE_TRANSFERED = "This equipment cannot be transfered"
    EQUIPMENT_ALREADY_EQUIPED = "You can't transfert because it's already equip"
    NO_SPACE_REMAINING = "There is no space remaining for the item you want to tranfert"
    BUNGIE_API_ERROR = "Something went wrong, please try again"
    EQUIP_TWO_EXOTIC = "You can't equip more than two exotic weapon or two exotic armor"
    ITEM_ALREADY_EQUIPPED = "This item is already equipped or is not in the equipment"
    ITEM_NOT_IN_VAULT = "The item is not on in the Vault"
    ITEM_CANNOT_BE_STORED_IN_VAULT = "The item is not on this character or is equiped"
    MANIFEST_NOT_FOUND = "Manifest not found"
    REDIRECT_ERROR = "Code not found, aborting..."
    VENDOR_NOT_FOUND = "Vendor not found"
