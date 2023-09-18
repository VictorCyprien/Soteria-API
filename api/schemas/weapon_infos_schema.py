from marshmallow import Schema, fields


class WeaponPayloadSchema(Schema):
    character_id_pull_equipment = fields.Integer(
        required=True,
        metadata={"description": "The ID of the character we want to get the weapon"}
    )
