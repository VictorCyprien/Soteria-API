from marshmallow import Schema, fields

class CharacterDataSchema(Schema):
    dateLastPlayed = fields.String()
    minutesPlayedThisSession = fields.String()
    minutesPlayedTotal = fields.String()
    light = fields.String()
    stats = fields.Dict()
    raceType = fields.Integer()
    classType = fields.Integer()
    genderType = fields.Integer()
    emblemPath = fields.String()
    emblemBackgroundPath = fields.String()

    class Meta:
        ordered = True


class CharactersResponseSchema(Schema):
    data = fields.Dict(
        keys=fields.Integer, 
        values=fields.Nested(CharacterDataSchema),
        metadata={"description": "The information of one or multiples characters"}
    )

    class Meta:
        ordered = True


class OneCharacterResponseSchema(Schema):
    data = fields.Dict(
        keys=fields.Integer, 
        values=fields.Nested(CharacterDataSchema),
        metadata={"description": "The information of one character"}
    )

    class Meta:
        ordered = True
