# app/routes/user.py
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user
from app.services.user_service import get_user_by_id
import logging

logger = logging.getLogger("app_logger")

users_bp = Blueprint('users', __name__)

@users_bp.route('/profile')
def profile():
    try:
        logger.info(f"Usuario {current_user.username} accediendo a su perfil.")
        user = get_user_by_id(current_user.id)
        return render_template('profile.html', user=user)
    except ValueError as e:
        flash(str(e), 'danger')
        return redirect(url_for('main.welcome'))
    except Exception as e:
        logger.error(f"Error inesperado al cargar el perfil: {e}")
        flash('Hubo un error al cargar tu perfil, por favor inténtalo de nuevo.', 'danger')
        return redirect(url_for('main.welcome'))
