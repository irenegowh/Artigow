# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from app.logs import setup_logging
from flask import jsonify
import logging
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=None):
    app = Flask(__name__)
    # Si no se pasa un config_class, carga la configuración según el entorno
    if config_class:
        app.config.from_object(config_class)
    else:
        environment = os.getenv('FLASK_ENV', 'local')
        if environment == 'production':
            app.config.from_object('config.RenderConfig')  # Cargar la configuración de producción
        elif environment == 'testing':
            app.config.from_object('config.TestConfig')  # Cargar la configuración de prueba
        else:
            app.config.from_object('config.LocalConfig')  # Cargar la configuración local


    @app.errorhandler(Exception)
    def handle_exception(e):
        logging.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

    @app.errorhandler(404)
    def not_found_error(e):
        logging.warning(f"Recurso no encontrado: {e}")
        return jsonify({"error": "Recurso no encontrado"}), 404

    return app

@login_manager.user_loader
def load_user(user_id):
    from app.models import UserProf
    return UserProf.query.get(int(user_id))  # Carga el usuario por IDs

