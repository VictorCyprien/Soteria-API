from aiohttp import web
from aiohttp.web import json_response
from aiohttp.web_exceptions import HTTPBadRequest
from aiohttp_apispec import (
    docs,
    querystring_schema,
    response_schema,
)

from marshmallow import Schema, fields

import logging
from ..abstract_manifest_view import ManifestAbstractView
from ...api import soteria_web
from ...root_abstract_view import AbstractView
from ....helpers.list_to_dict import convert_list_to_dict

logger = logging.getLogger('console')

class ManifestParamsSchema(Schema):
    id = fields.Integer(
        load_default=None,
        metadata={"description": "The ID of the entity data we want"}
    )


@soteria_web.view('/manifest/{manifest_name}')
class OneManifestView(ManifestAbstractView):

    @property
    def manifest_name(self) -> int:
        manifest_name = self.request.match_info.get('manifest_name', "None")
        if manifest_name is None:
            raise HTTPBadRequest(text=f"The name of the manifest is required !")
        return str(manifest_name)

    @docs(
        summary="Get the entity of one manifest",
        description="Get the entity id and data of one manifest",
        responses={
            200: {"description": "OK"},
            400: {"description": "Invalid request"},
            401: {"description": "Unauthorized"},
            500: {"description": "Server error"},
            503: {"description": "Too many requests, wait a bit"},
        },
    )
    @querystring_schema(ManifestParamsSchema)
    #@response_schema(ReponseGetSchema(), 200, description="Success reponse")
    async def get(self) -> web.Response:
        self.check_auth(self.request)
        
        manifest_name = self.manifest_name
        params = self.request['querystring']
        entity_id = params.get("id", None)

        if entity_id is None:
            raise HTTPBadRequest(text="No ID filled for entity data !")
        
        manifest_data = self.read_one_manifest_data(manifest_name)
        manifest_data_dict = convert_list_to_dict(manifest_data)
        entity = self.get_data_of_one_entity(entity_id, manifest_data_dict)

        return json_response(data=entity)
