# app/services/vote_service.py
from sqlalchemy import func
from app import db
from app.models.votes import Vote
from app.models.posts import Post
import logging

logger = logging.getLogger("app_logger")

def add_vote(post_id, user):
    try:
        # Verifica si ya existe un voto del usuario para el post
        existing_vote = Vote.query.filter_by(post_id=post_id, user_id=user.id).first()
        if existing_vote:
            raise ValueError("Ya has votado por este post.")

        # Crea un nuevo voto
        vote = Vote(post_id=post_id, user_id=user.id)
        db.session.add(vote)
        db.session.commit()
        logger.info(f"Voto agregado para el post {post_id} por el usuario {user.username}.")
    except ValueError:
        raise
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error al registrar el voto para el post {post_id}: {e}")
        raise ValueError("Error al registrar el voto.")


def get_ranking():
    try:
        # Obtén los posts ordenados por la cantidad de votos
        ranking_data = (
            Post.query.outerjoin(Post.votes)
            .group_by(Post.id)
            .order_by(func.count(Post.votes).desc())
            .all()
        )
        logger.info("Ranking de publicaciones obtenido correctamente.")
        return ranking_data
    except Exception as e:
        logger.error(f"Error al obtener el ranking de publicaciones: {e}")
        raise ValueError("Error al obtener el ranking de publicaciones.")