from marshmallow import fields, Schema


class VaultItems(Schema):
    itemHash = fields.Integer(),
    quantity = fields.Integer(),
    bindStatus = fields.Integer(),
    location = fields.Integer(),
    bucketHash = fields.Integer(),
    transferStatus = fields.Integer(),
    lockable = fields.Boolean(),
    state = fields.Integer(),
    dismantlePermission = fields.Integer(),
    isWrapper = fields.String(),
    tooltipNotificationIndexes = fields.List(fields.Integer())


class VaultData(Schema):
    data = fields.Nested(VaultItems, many=True)


class VaultResponseSchema(Schema):
    responseMintedTimestamp = fields.String(metadata={"description": "The time at which the response was received"})
    profileInventory = fields.Nested(VaultData)
