from marshmallow import fields, Schema


class EquipResponseSchema(Schema):
    status = fields.String()


class TransfertResponseSchema(Schema):
    status = fields.String()
