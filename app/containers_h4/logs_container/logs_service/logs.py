import logging
from logging.handlers import RotatingFileHandler
from logging.config import dictConfig
import os
from flask import Flask, Blueprint, request, jsonify
import requests

# --- CONFIGURACIÓN DEL LOGGER ---

def setup_logging():
    # Crear el directorio de logs si no existe
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Configuración central de logging con dictConfig
    dictConfig(
        {
            "version": 1,
            "formatters": {
                "default": {
                    "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "stream": "ext://sys.stdout",
                },
                "file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "formatter": "default",
                    "filename": "logs/app.log",
                    "maxBytes": 1000000,
                    "backupCount": 5,
                    "level": "INFO",
                },
            },
            "root": {
                "level": "INFO",
                "handlers": ["console", "file"],
            },
            "loggers": {
                "app_logger": {
                    "level": "INFO",
                    "handlers": ["console", "file"],
                    "propagate": False,
                },
            },
        }
    )

# Inicializa el logger para ser usado en toda la aplicación
logger = logging.getLogger("app_logger")

# Configura el logging al cargar el módulo
setup_logging()

# --- BLUEPRINT ---
logs_bp = Blueprint('logs', __name__)

# --- RUTAS (Endpoints HTTP) ---

@logs_bp.route('/log', methods=['POST'])
def log_message():
    """Endpoint para registrar logs con diferentes niveles."""
    try:
        data = request.json
        level = data.get('level', 'INFO').upper()
        message = data.get('message', 'Log vacío')

        # Registrar el log según el nivel
        if level == 'INFO':
            logger.info(message)
            return jsonify({'message': 'Log registrado exitosamente'}), 200
        elif level == 'ERROR':
            logger.error(message)
            return jsonify({'message': 'Log registrado exitosamente'}), 200
        elif level == 'WARNING':
            logger.warning(message)
            return jsonify({'message': 'Log registrado exitosamente'}), 200
        else:
            return jsonify({'error': 'Nivel de log no soportado'}), 400
        
    except Exception as e:
        logger.error(f"Error al registrar el log: {str(e)}")
        return jsonify({'error': str(e)}), 500


@logs_bp.route('/check_auth_service', methods=['GET'])
def check_auth_service():
    """Comprueba la conectividad con auth_service."""
    try:
        response = requests.get(os.getenv('AUTH_SERVICE_URL', 'http://auth_service:5000') + '/auth/register')
        if response.status_code == 200:
            return jsonify({'message': 'Conectado a auth_service'}), 200
        return jsonify({'error': 'No se pudo conectar a auth_service'}), 500
    except Exception as e:
        logger.error(f"Error al conectar con auth_service: {str(e)}")
        return jsonify({'error': f"No se pudo conectar: {str(e)}"}), 500


@logs_bp.route('/check_db_service', methods=['GET'])
def check_db_service():
    """Comprueba la conectividad con db_service."""
    try:
        response = requests.get(os.getenv('DB_SERVICE_URL', 'http://db_service:5002') + '/status')
        if response.status_code == 200:
            return jsonify({'message': 'Conectado a db_service'}), 200
        return jsonify({'error': 'No se pudo conectar a db_service'}), 500
    except Exception as e:
        logger.error(f"Error al conectar con db_service: {str(e)}")
        return jsonify({'error': f"No se pudo conectar: {str(e)}"}), 500

@logs_bp.route('/check_post_service', methods=['GET'])
def check_post_service():
    """Comprueba la conectividad con post_service."""
    try:
        # Usamos un endpoint de post_service para verificar si está activo
        post_service_url = os.getenv('POST_SERVICE_URL', 'http://post_service:5003')
        response = requests.get(f'{post_service_url}/status')
        if response.status_code == 200:
            logger.info("Conectado a post_service")
            return jsonify({'message': 'Conectado a post_service'}), 200
        else:
            logger.error(f"No se pudo conectar a post_service. Código de respuesta: {response.status_code}")
            return jsonify({'error': 'No se pudo conectar a post_service'}), 500
    except Exception as e:
        logger.error(f"Error al conectar con post_service: {str(e)}")
        return jsonify({'error': f"No se pudo conectar a post_service: {str(e)}"}), 500

# --- EXPORTAR BLUEPRINT ---
__all__ = ['logs_bp', 'logger', 'setup_logging']
