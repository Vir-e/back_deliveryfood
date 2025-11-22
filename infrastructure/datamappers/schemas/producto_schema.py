from marshmallow import Schema, fields

class ProductoSchema(Schema):
    id = fields.Int()
    nombre = fields.Str()
    precio_kg = fields.Float()
    stock = fields.Int()

