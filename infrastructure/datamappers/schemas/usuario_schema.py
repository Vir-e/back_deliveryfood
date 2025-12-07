from marshmallow import Schema, fields

class UsuarioSchema(Schema):
    id = fields.Int()
    nombre = fields.Str()
    apellidos = fields.Str()
    username = fields.Str()
    password = fields.Str()
    email = fields.Str()
    admin = fields.Bool()