from marshmallow import Schema, fields

class CartaSchema(Schema):
    id = fields.Int()
    nombre = fields.Str()
    precio = fields.Float()
    sin_gluten = fields.Bool()
    sin_huevo = fields.Bool()
    vegano = fields.Bool()
