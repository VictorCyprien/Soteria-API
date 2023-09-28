import logging
import logging.config
import ssl

from aiohttp import web
from aiohttp_apispec import (
    setup_aiohttp_apispec,
    validation_middleware
)

from aiohttp_swagger import setup_swagger
import aiohttp_cors
from aiohttp_cache import setup_cache


logger: logging.Logger = logging.getLogger('console')

logger.info(".--------------------------------------.")
logger.info("|              Soteria API             |")
logger.info(".--------------------------------------.")

app = web.Application()

logging.basicConfig(level=logging.DEBUG)

# Add cache
setup_cache(app)

# Add Web views
from .views import soteria_web
app.add_routes(soteria_web)

app.middlewares.append(validation_middleware)

ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH, cafile="./certs/certificate.pem")
ctx.load_cert_chain("./certs/certificate.pem", "./certs/key.pem")

# Add swagger docs

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

# Add cors for each route

cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
})

for route in app.router.routes():
    cors.add(route)
