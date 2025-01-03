from app import db  # Importa la instancia de SQLAlchemy desde app.py
from flask import request, jsonify  # Asegúrate de importar request y jsonify
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime  # Importa Column y tipos necesarios
from sqlalchemy.orm import relationship 

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    user_name = db.Column(db.String(255), nullable=False) 
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))

    # Relación con los votos
    votes = relationship("Vote", back_populates="post", lazy=True)
    def __repr__(self):
        return f'<Post {self.title}>'

    @staticmethod
    def create_post():
        # Obtener datos del formulario o del cuerpo JSON de la solicitud
        data = request.get_json()
        title = data.get('title')
        content = data.get('content')
        image_url = data.get('image_url', None)  # Opcional
        user_name = data.get('user_name')

        # Crear y guardar el nuevo Post
        new_post = Post(title=title, content=content, image_url=image_url, user_name=user_name)
        db.session.add(new_post)
        db.session.commit()

        return jsonify({'message': 'Publicación creada', 'post': {
            'title': new_post.title,
            'content': new_post.content,
            'image_url': new_post.image_url,
            'user_name': new_post.user_name,
            'date_posted': new_post.date_posted
        }}), 201

