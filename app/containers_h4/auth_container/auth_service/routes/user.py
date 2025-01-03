import requests
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user
import logging
from sqlalchemy import create_engine, text
import os  # Asegúrate de importar 'os' para las variables de entorno


# Configurar el logger
logger = logging.getLogger("app_logger")

# Definir la URL del servicio db_service
DB_SERVICE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@db_service:5432/artigow_db')

users_bp = Blueprint('users', __name__)

@users_bp.route('/profile')
def profile():
    try:
        logger.info(f"Usuario {current_user.username} accediendo a su perfil.")
        
        # Realizar una solicitud HTTP al servicio db_service para obtener los datos del usuario
        response = requests.get(f'{DB_SERVICE_URL}/users/{current_user.id}')
        
        if response.status_code == 200:
            user = response.json()  # Obtener la información del usuario desde db_service
            return render_template('profile.html', user=user)
        else:
            flash('Usuario no encontrado, por favor verifica tu sesión.', 'danger')
            return redirect(url_for('main.welcome'))

    except requests.exceptions.RequestException as e:
        logger.error(f"Error de comunicación con db_service: {e}")
        flash('Hubo un problema al cargar tu perfil, por favor inténtalo de nuevo.', 'danger')
        return redirect(url_for('main.welcome'))
    
    except Exception as e:
        logger.error(f"Error inesperado al cargar el perfil: {e}")
        flash('Hubo un error al cargar tu perfil, por favor inténtalo de nuevo.', 'danger')
        return redirect(url_for('main.welcome'))
