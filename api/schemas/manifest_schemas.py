from marshmallow import fields, Schema


class ManifestVersionResponseSchema(Schema):
    manifest_version = fields.String(metadata={"description": "The current version of the manifest"})

