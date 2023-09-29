from typing import Dict
import logging
import json

from .. import AbstractView
from ...helpers.errors_handler import NotFound, ReasonError

logger = logging.getLogger('console')


class ManifestAbstractView(AbstractView):
    def set_manifest_version(self, manifest_version: str):
        with open('./manifest-data/version.txt', 'w') as file:
            file.write(manifest_version)


    def get_manifest_version(self) -> str:
        data = ""
        try:
            with open('./manifest-data/version.txt', 'r') as file:
                data = file.read()
        except FileNotFoundError:
            logger.warning("Manifest version not found, proceed...")
        return data
    

    def read_one_manifest_data(self, manifest_name: str):
        try:
            with open(f'./manifest-data/{manifest_name}.json', 'r') as file:
                manifest_data: Dict = json.loads(file.read())
        except FileNotFoundError:
            raise NotFound(ReasonError.MANIFEST_NOT_FOUND.value)
        
        return manifest_data
    

    def get_data_of_one_entity(self, entity_id: int, manifest_data: Dict) -> Dict:
        entity = {}
        entity["entity_id"] = entity_id
        entity_data = manifest_data.get(entity_id, None)
        entity_data = json.loads(entity_data) if entity_data is not None else None
        entity["entity_data"] = entity_data
        return entity
