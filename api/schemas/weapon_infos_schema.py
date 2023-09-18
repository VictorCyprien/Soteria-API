from marshmallow import Schema, fields


class WeaponPayloadSchema(Schema):
    weapon_id = fields.Integer(
        required=True,
        metadata={"description": "The ID of the weapon"}
    )
