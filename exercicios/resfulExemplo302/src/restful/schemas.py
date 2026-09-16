from marshmallow import Schema, fields

class ItemQueryArgsSchema(Schema):
    nome = fields.String()

class ItemSchema(Schema):
    id = fields.Integer(dump_only=True)
    nome = fields.String()
    quantidade = fields.Integer()
    valor = fields.Float()