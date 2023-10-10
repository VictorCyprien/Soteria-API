from aiohttp import web
from aiohttp.web import json_response
from aiohttp_apispec import (
    docs,
    response_schema,
)

import logging
from .abstract_manifest_view import ManifestAbstractView
from ..api import soteria_web
from ...helpers.convert_sqlite_to_json import sqliteToJson
from ...schemas.manifest_schemas import ManifestVersionResponseSchema

logger = logging.getLogger('console')

@soteria_web.view('/manifest')
class ManifestView(ManifestAbstractView):

    @docs(
        summary="Get and Download the manifest",
        description="Get and Download the last manifest of Destiny 2 and build JSON file for each table",
        responses={
            200: {"description": "OK"},
            400: {"description": "Invalid request"},
            401: {"description": "Unauthorized"},
            500: {"description": "Server error"},
            503: {"description": "Too many requests, wait a bit"},
        },
    )
    @response_schema(ManifestVersionResponseSchema(), 200, description="Success reponse")
    async def get(self) -> web.Response:
        self.check_auth(self.request)
        
        async with self.bungie.client.acquire() as rest:
            last_manifest_version = await rest.fetch_manifest_version()
            current_manifest_version = self.get_manifest_version()
            
            # Download the last manifest version if the current version in the API in not the right one
            if current_manifest_version != last_manifest_version:
                await rest.download_manifest("fr", path="./manifest-data", force=True)
                sqliteToJson("./manifest-data/manifest.sqlite3")
                self.set_manifest_version(manifest_version=last_manifest_version)

        return json_response(data={
            "manifest_version": last_manifest_version,
        })
