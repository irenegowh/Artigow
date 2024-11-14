# votes.py
from app import db  # Importa la instancia de SQLAlchemy desde app.py
from sqlalchemy.orm import relationship 
from flask import request, jsonify  # Asegúrate de importar request y jsonify
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship 
from datetime import datetime, timezone
class Vote(db.Model):
    __tablename__ = 'votes'
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    # Relacion con la clase Post
    post = relationship("Post", back_populates="votes", lazy=True)
    
    def __repr__(self):
        return f'<Vote {self.id}>'

    @staticmethod
    def create_vote():
        # Obtener datos del cuerpo JSON de la solicitud
        data = request.get_json()
        post_id = data.get('post_id')
        created_at = data.get('created_at', datetime.utcnow())

        # Crear y guardar el nuevo Voto
        new_vote = Vote(post_id=post_id, created_at=created_at)
        db.session.add(new_vote)
        db.session.commit()

        return jsonify({'message': 'Voto creado', 'vote': {
            'post_id': new_vote.post_id,
            'created_at': new_vote.created_at
        }}), 201