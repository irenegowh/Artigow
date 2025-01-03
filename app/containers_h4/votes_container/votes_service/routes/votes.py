from flask import Blueprint, request, jsonify, redirect, url_for, render_template, flash
from flask_login import login_required, current_user
from votes_service.services.votes_service import add_vote, get_ranking, get_user_votes
import logging
import requests
import os

logger = logging.getLogger("app_logger")

votes_bp = Blueprint('votes', __name__)

# Variables de entorno para conectar con otros servicios
POSTS_SERVICE_URL = os.getenv('POSTS_SERVICE_URL', 'http://posts_service:5004')
LOGS_SERVICE_URL = os.getenv('LOGS_SERVICE_URL', 'http://logs_service:5003')


@votes_bp.route('/vote_post/<int:post_id>', methods=['POST'])
@login_required
def vote_post(post_id):
    try:
        logger.info(f"Usuario {current_user.username} está votando por el post {post_id}.")

        # Verifica si el post existe en el posts_service
        post_response = requests.get(f"{POSTS_SERVICE_URL}/posts/{post_id}")
        if post_response.status_code != 200:
            flash('El post especificado no existe.', 'danger')
            return redirect(url_for('votes.ranking'))

        # Usa el servicio para manejar la lógica de agregar votos
        add_vote(post_id, current_user)

        # Registra el voto en logs_service
        log_data = {
            "action": "vote",
            "user_id": current_user.id,
            "post_id": post_id,
            "message": f"Voto agregado por el usuario {current_user.username}."
        }
        requests.post(f"{LOGS_SERVICE_URL}/logs", json=log_data)

        flash('Voto registrado correctamente.', 'success')
    except ValueError as e:
        logger.warning(f"Error al votar por el post {post_id}: {e}")
        flash(str(e), 'danger')
    except Exception as e:
        logger.error(f"Error inesperado al votar por el post {post_id}: {e}")
        flash('Hubo un error al registrar tu voto, por favor inténtalo de nuevo.', 'danger')

    return redirect(url_for('votes.ranking'))  # Redirige al ranking después de votar


@votes_bp.route('/ranking', methods=['GET'])
def ranking():
    try:
        logger.info("Accediendo a la página de ranking de votos.")

        # Usa el servicio para obtener los posts ordenados por votos
        order_posts = get_ranking()

        # Renderiza la plantilla con los datos
        return render_template('list_votes.html', order_posts=order_posts)
    except Exception as e:
        logger.error(f"Error inesperado al obtener el ranking: {e}")
        flash('Hubo un error al obtener el ranking, por favor inténtalo de nuevo.', 'danger')
        return redirect(url_for('main.welcome'))


@votes_bp.route('/user_votes/<int:user_id>', methods=['GET'])
@login_required
def user_votes(user_id):
    try:
        # Verificar si el ID coincide con el usuario actual
        if user_id != current_user.id:
            flash('No tienes permisos para ver esta información.', 'danger')
            return redirect(url_for('votes.ranking'))

        logger.info(f"Obteniendo votos del usuario {user_id}.")
        user_votes_data = get_user_votes(user_id)

        # Devuelve los votos en formato JSON
        return jsonify(user_votes_data), 200
    except Exception as e:
        logger.error(f"Error inesperado al obtener los votos del usuario {user_id}: {e}")
        flash('Hubo un error al obtener tus votos, por favor inténtalo de nuevo.', 'danger')
        return redirect(url_for('votes.ranking'))
