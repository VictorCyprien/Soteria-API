import logging
import logging.config
import ssl

from aiohttp import web
from aiohttp_apispec import (
    setup_aiohttp_apispec,
    validation_middleware
)
from aiohttp_swagger import setup_swagger

from .helpers.check_auth import auth_middleware

logger: logging.Logger = logging.getLogger('console')

logger.info(".--------------------------------------.")
logger.info("|              Soteria API             |")
logger.info(".--------------------------------------.")

app = web.Application()
logging.basicConfig(level=logging.DEBUG)

from .views import soteria_web
app.add_routes(soteria_web)

app.middlewares.append(validation_middleware)
app.middlewares.append(auth_middleware)

ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH, cafile="./certs/certificate.pem")
ctx.load_cert_chain("./certs/certificate.pem", "./certs/key.pem")

setup_aiohttp_apispec(
    app=app, 
    title="Soteria API : API that manage interaction from BungieAPI", 
    version="v1",
    url="/_schema/swagger.json",
    swagger_path="/_schema",
    in_place=True,
)

async def swagger(app):
    setup_swagger(
        app=app, swagger_url='/api/docs', swagger_info=app['swagger_dict']
    )

app.on_startup.append(swagger)
