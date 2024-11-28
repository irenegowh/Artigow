# app/routes/votes.py
from flask import Blueprint, redirect, url_for, render_template, flash
from flask_login import login_required, current_user
from app.services.votes_service import add_vote, get_ranking
import logging

logger = logging.getLogger("app_logger")

votes_bp = Blueprint('votes', __name__)

@votes_bp.route('/vote_post/<int:post_id>', methods=['POST'])
@login_required
def vote_post(post_id):
    try:
        logger.info(f"Usuario {current_user.username} está votando por el post {post_id}.")
        # Usa el servicio para manejar la lógica de agregar votos
        add_vote(post_id, current_user)
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
        return render_template('list_votes.html', order_posts=order_posts)
    except Exception as e:
        logger.error(f"Error inesperado al obtener el ranking: {e}")
        flash('Hubo un error al obtener el ranking, por favor inténtalo de nuevo.', 'danger')
        return redirect(url_for('main.welcome'))