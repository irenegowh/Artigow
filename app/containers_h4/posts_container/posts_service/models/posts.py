from posts_service import db  # Importa la instancia de SQLAlchemy desde app.py
from flask import request, jsonify, current_app  # Asegúrate de importar request y jsonify
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime  # Importa Column y tipos necesarios
from sqlalchemy.orm import relationship
import requests  # Para interactuar con logs_service
from flask_login import current_user  # Para obtener al usuario actual (autenticación)

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    user_name = db.Column(db.String(255), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))

    # Relación con los votos
    votes = db.relationship('Vote', back_populates='post')

    def __repr__(self):
        return f'<Post {self.title}>'

    @staticmethod
    def create_post():
        """
        Crea un nuevo post y guarda los logs en logs_service.
        """
        data = request.get_json()

        # Verificar que los campos necesarios están presentes en la solicitud
        title = data.get('title')
        content = data.get('content')
        image_url = data.get('image_url', None)  # Opcional
        user_name = data.get('user_name')

        if not title or not content or not user_name:
            return jsonify({'message': 'Título, contenido y nombre de usuario son requeridos.'}), 400

        # Crear y guardar el nuevo Post
        new_post = Post(title=title, content=content, image_url=image_url, user_name=user_name)
        db.session.add(new_post)
        db.session.commit()

        # Enviar un log al logs_service
        try:
            log_data = {
                'level': 'INFO',
                'message': f'Publicación creada por {user_name}: {title}',
                'user_name': user_name
            }
            # Enviar un mensaje al logs_service para registrar la creación de la publicación
            logs_service_url = current_app.config.get('LOGS_SERVICE_URL')
            if logs_service_url:
                requests.post(logs_service_url + "/log", json=log_data)
        except Exception as e:
            return jsonify({'message': f'Error al registrar el log: {str(e)}'}), 500

        return jsonify({'message': 'Publicación creada', 'post': {
            'title': new_post.title,
            'content': new_post.content,
            'image_url': new_post.image_url,
            'user_name': new_post.user_name,
            'date_posted': new_post.date_posted
        }}), 201
