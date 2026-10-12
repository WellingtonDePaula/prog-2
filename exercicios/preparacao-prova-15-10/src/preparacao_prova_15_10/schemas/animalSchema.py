from marshmallow import Schema, fields, validate

class AnimalSchema(Schema):
     id = fields.Int(dump_only=True)
     nome = fields.Str(required=True, validate=validate.Length(1, 100))
     raca = fields.Str(required=True, validate=validate.Length(min=1))
     peso = fields.Float(required=True, validate=validate.Range(min=0))
     sexo = fields.Str(required=True, validate=validate.Length(1, 1))