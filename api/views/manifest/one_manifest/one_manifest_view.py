from typing import List
from aiohttp import web
import json
from aiohttp.web import json_response
from aiohttp.web_exceptions import HTTPNotFound, HTTPBadRequest
from aiohttp_apispec import (
    docs,
    response_schema,
)

from marshmallow import Schema, fields

import logging
from ...api import soteria_web
from ...abstract_view import AbstractView

logger = logging.getLogger('console')

@soteria_web.view('/manifest/{manifest_name}')
class OneManifestView(AbstractView):

    @property
    def manifest_name(self) -> int:
        manifest_name = self.request.match_info.get('manifest_name', "None")
        #We raise a NotFound when the number is not a positive number
        if manifest_name is None:
            raise HTTPBadRequest(text=f"The name of the manifest is required !")
        return str(manifest_name)

    @docs(
        summary="Download the manifest",
        description="Download the one manifest table of Destiny 2",
        responses={
            200: {"description": "OK"},
            400: {"description": "Invalid request"},
            401: {"description": "Unauthorized"},
            500: {"description": "Server error"},
            503: {"description": "Too many requests, wait a bit"},
        },
    )
    #@response_schema(ReponseGetSchema(), 200, description="Success reponse")
    async def get(self) -> web.Response:
        manifest_name = self.manifest_name

        try:
            with open(f'./manifest-data/{manifest_name}.json', 'r') as file:
                data = file.read()
        except FileNotFoundError:
            raise HTTPNotFound(text="Manifest not found !")

        return json_response(data=json.loads(data))
