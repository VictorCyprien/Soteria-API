import logging

from .. import AbstractView

logger = logging.getLogger('console')

class LoginAbstractView(AbstractView):

    async def generate_oauth_url(self):
        async with self.bungie.client.acquire() as rest:
            oauth_url = rest.build_oauth2_url()

            assert oauth_url is not None, "Make sure client ID and secret are set AND correct !"
            return oauth_url
