from marshmallow import fields, Schema


class OneItemEquipment(Schema):
    itemHash = fields.Integer()
    itemInstanceId = fields.String()
    quantity = fields.Integer()
    location = fields.Integer()
    bucketHash = fields.Integer()
    transferStatus = fields.Integer()
    lockable = fields.Boolean()
    state = fields.Integer()
    dismantlePermission = fields.Integer()
    isWrapper = fields.Boolean()
    versionNumber = fields.Integer()


class ItemEquipment(Schema):
    items = fields.Nested(OneItemEquipment, many=True)


class DataEquipment(Schema):
    data = fields.Nested(ItemEquipment)
    privacy = fields.Integer()


class EquipmentResponseSchema(Schema):
    inventory = fields.Nested(DataEquipment)
    loadouts = fields.Dict()


class ItemInfoResponseSchema(Schema):
    characterId = fields.String(metadata={"description": "The ID of the character we get the item"})
    instance = fields.Dict(metadata={"description": "Data of the instance's item"})
    objectives = fields.Dict()
    perks = fields.Dict(metadata={"description": "Perks of the instance's item"})
    renderData = fields.Dict()
    stats = fields.Dict(metadata={"description": "Stats of the instance's item"})
    talentGrid = fields.Dict()
    sockets = fields.Dict(metadata={"description": "Sockets of the instance's item"})
    reusablePlugs = fields.Dict()
    plugObjectives = fields.Dict()



class ItemPayloadSchema(Schema):
    character_id_pull_item = fields.Integer(
        required=True,
        metadata={"description": "The ID of the character we want to get the item"}
    )


class ItemLockSchema(Schema):
    lock_state = fields.Boolean(
        required=True,
        metadata={"description": "The state of the lock we want. If True, we lock the item, else, we unlock it."}
    )


class EquipItemResponseSchema(Schema):
    status = fields.String()


class TransfertItemResponseSchema(Schema):
    status = fields.String()
