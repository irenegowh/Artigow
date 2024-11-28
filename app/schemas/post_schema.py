from marshmallow import Schema, fields

class PostSchema(Schema):
    title = fields.String(required=True, error_messages={"required": "Título es obligatorio"})
    content = fields.String(required=True, error_messages={"required": "Contenido es obligatorio"})
    image = fields.Raw(allow_none=True)  # Permitir valores nulos para la imagen
    
post_schema = PostSchema()
