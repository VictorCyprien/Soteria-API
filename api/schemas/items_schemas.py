from marshmallow import fields, Schema


class ItemPayloadSchema(Schema):
    character_id_pull_item = fields.Integer(
        required=True,
        metadata={"description": "The ID of the character we want to get the item"}
    )


class EquipItemResponseSchema(Schema):
    status = fields.String()


class TransfertItemResponseSchema(Schema):
    status = fields.String()
