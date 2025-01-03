# votes.py
from db_service import db
from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from datetime import datetime, timezone
from flask import request, jsonify
from sqlalchemy.orm import relationship


class Vote(db.Model):
    __tablename__ = 'votes'
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    user_id = db.Column(db.Integer, ForeignKey("userprof.id"), nullable=False)  # Referencia a UserProf
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    # Relación con Post
    post = relationship("Post", back_populates="votes", lazy=True)

    # Relación con UserProf (la importación se hace aquí para evitar problemas)
    user = relationship("UserProf", back_populates="votes", lazy=True)

    __table_args__ = (UniqueConstraint('post_id', 'user_id', name='uq_post_user_vote'),)

    def __repr__(self):
        return f'<Vote {self.id}>'

    @staticmethod
    def create_vote():
        # Obtener datos del cuerpo JSON de la solicitud
        data = request.get_json()
        post_id = data.get('post_id')
        user_id = data.get('user_id')
        created_at = data.get('created_at', datetime.utcnow())

        existing_vote = Vote.query.filter_by(post_id=post_id, user_id=user_id).first()
        if existing_vote:
            return jsonify({'message': 'Ya has votado por este post.'}), 400

        # Crear y guardar el nuevo Voto
        new_vote = Vote(post_id=post_id, user_id=user_id, created_at=created_at)
        db.session.add(new_vote)
        db.session.commit()

        return jsonify({'message': 'Voto creado', 'vote': {
            'post_id': new_vote.post_id,
            'user_id': new_vote.user_id,
            'created_at': new_vote.created_at
        }}), 201
