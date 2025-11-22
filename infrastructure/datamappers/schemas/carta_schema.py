from marshmallow import Schema, fields

class CartaSchema(Schema):
    id = fields.Int()
    nombre = fields.Str()
    precio = fields.Float()

