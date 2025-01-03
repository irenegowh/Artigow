import requests
from sqlalchemy import func
from votes_service import db
from votes_service.models.votes import Vote
import logging
import os

logger = logging.getLogger("app_logger")

# URLs de los otros servicios
DB_SERVICE_URL = os.getenv('DATABASE_URL', 'http://db_service:5002')
POSTS_SERVICE_URL = os.getenv('POSTS_SERVICE_URL', 'http://posts_service:5004')
LOGS_SERVICE_URL = os.getenv('LOGS_SERVICE_URL', 'http://logs_service:5003')


def add_vote(post_id, user):
    try:
        # Verificar si el post existe en el servicio posts_service
        post_response = requests.get(f"{POSTS_SERVICE_URL}/posts/{post_id}")
        if post_response.status_code != 200:
            raise ValueError("El post especificado no existe.")

        # Verifica si ya existe un voto del usuario para el post
        existing_vote = Vote.query.filter_by(post_id=post_id, user_id=user.id).first()
        if existing_vote:
            raise ValueError("Ya has votado por este post.")

        # Crea un nuevo voto
        vote = Vote(post_id=post_id, user_id=user.id)
        db.session.add(vote)
        db.session.commit()

        # Registrar el voto en el servicio de logs
        log_data = {
            "action": "add_vote",
            "user_id": user.id,
            "post_id": post_id,
            "message": f"Voto agregado para el post {post_id} por el usuario {user.username}."
        }
        requests.post(f"{LOGS_SERVICE_URL}/logs", json=log_data)

        logger.info(f"Voto agregado para el post {post_id} por el usuario {user.username}.")
    except ValueError as e:
        raise
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error al registrar el voto para el post {post_id}: {e}")
        raise ValueError("Error al registrar el voto.")


def get_ranking():
    try:
        # Obtener los posts ordenados por cantidad de votos
        ranking_data = (
            Post.query.outerjoin(Post.votes)
            .group_by(Post.id)
            .order_by(func.count(Post.votes).desc())
            .all()
        )

        # Consultar la información detallada de los posts desde posts_service
        detailed_ranking = []
        for post in ranking_data:
            post_response = requests.get(f"{POSTS_SERVICE_URL}/posts/{post.id}")
            if post_response.status_code == 200:
                post_data = post_response.json()
                detailed_ranking.append({
                    "post_id": post.id,
                    "title": post_data.get("title"),
                    "content": post_data.get("content"),
                    "vote_count": len(post.votes)
                })

        logger.info("Ranking de publicaciones obtenido correctamente.")
        return detailed_ranking
    except Exception as e:
        logger.error(f"Error al obtener el ranking de publicaciones: {e}")
        raise ValueError("Error al obtener el ranking de publicaciones.")


def get_user_votes(user_id):
    """Consulta los votos de un usuario usando db_service"""
    try:
        response = requests.get(f"{DB_SERVICE_URL}/users/{user_id}/votes")
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError("No se encontraron votos para este usuario.")
    except Exception as e:
        logger.error(f"Error al consultar los votos del usuario {user_id}: {e}")
        raise ValueError("Error al consultar los votos del usuario.")
