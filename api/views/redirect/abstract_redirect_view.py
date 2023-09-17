from aiohttp import web
from aiohttp.web_exceptions import HTTPNotFound
import logging

from .. import AbstractView

logger = logging.getLogger('console')

class RedirectAbstractView(AbstractView):

    async def get_tokens(self, code: str):
        async with self.bungie.client.acquire() as rest:
            tokens = await rest.fetch_oauth2_tokens(code)

        return tokens
