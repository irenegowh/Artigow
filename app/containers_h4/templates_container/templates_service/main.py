from flask import Blueprint, render_template, flash
from flask_login import current_user, login_required  # Importar current_user y login_required
import logging

# Definir blueprint para la página principal
main_bp = Blueprint('main', __name__)

# Configuración básica de logging
logger = logging.getLogger("app_logger")

@main_bp.route('/')
def welcome():
    try:
        logger.info("Accediendo a la página principal (bienvenida).")
        return render_template('bienvenida.html')
    except Exception as e:
        logger.error(f"Error al cargar la página de bienvenida: {e}")
        flash('Hubo un error al cargar la página principal, por favor inténtalo de nuevo.', 'danger')
        return render_template('error.html')  # Página de error personalizada

@main_bp.route('/templates/register.html')
def register():
    try:
        return render_template('register.html')  # Devuelve el template de registro
    except Exception as e:
        logger.error(f"Error al cargar la página de registro: {e}")
        return render_template('error.html')

@main_bp.route('/templates/login.html')
def login():
    try:
        return render_template('login.html')  # Devuelve el template de login
    except Exception as e:
        logger.error(f"Error al cargar la página de login: {e}")
        return render_template('error.html')

@main_bp.route('/static/<path:filename>')
def static_files(filename):
    try:
        # Sirve archivos desde el directorio 'static'
        return send_from_directory('static', filename)
    except Exception as e:
        logger.error(f"Error al servir el archivo estático {filename}: {e}")
        return "Error al cargar el archivo estático.", 500