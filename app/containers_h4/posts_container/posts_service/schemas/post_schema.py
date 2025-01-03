from marshmallow import Schema, fields, post_load
from datetime import datetime

class PostSchema(Schema):
    title = fields.String(required=True, error_messages={"required": "Título es obligatorio"})
    content = fields.String(required=True, error_messages={"required": "Contenido es obligatorio"})
    image = fields.Raw(allow_none=True)  # Permitir valores nulos para la imagen
    user_name = fields.String(required=True, error_messages={"required": "Nombre de usuario es obligatorio"})
    date_posted = fields.DateTime(format="iso", default=datetime.utcnow)  # Fecha en formato ISO 8601

    @post_load
    def make_post(self, data, **kwargs):
        """Aquí puedes hacer la conversión de datos o realizar modificaciones antes de la creación del objeto"""
        return data

# Instancia global para usar el esquema
post_schema = PostSchema()
