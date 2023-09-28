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
    # TODO : Add error here...
    PROFILE_NOT_FOUND = "Profile not found"
    NOT_AUTHENTICATED = "Not Authenticated"