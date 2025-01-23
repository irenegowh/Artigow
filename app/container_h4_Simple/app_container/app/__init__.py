from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from .routes import main_bp, auth_bp, posts_bp, votes_bp, users_bp  # Importar los blueprints
import logging
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=None):
    app = Flask(__name__)

    # Configuración de la app
    if config_class:
        app.config.from_object(config_class)
    else:
        environment = os.getenv('FLASK_ENV', 'local')
        if environment == 'production':
            app.config.from_object('config.RenderConfig')
        elif environment == 'testing':
            app.config.from_object('config.TestConfig')
        else:
            app.config.from_object('config.LocalConfig')

    # Inicializar las extensiones
    db.init_app(app)
    login_manager.init_app(app)
    Migrate(app, db)

    # Registrar los blueprints
    app.register_blueprint(main_bp)  # Ruta raíz
    app.register_blueprint(auth_bp, url_prefix='/auth')  # Autenticación
    app.register_blueprint(posts_bp, url_prefix='/posts')  # Publicaciones
    app.register_blueprint(votes_bp, url_prefix='/votes')  # Votaciones
    app.register_blueprint(users_bp, url_prefix='/users')  # Usuarios

    # Registrar manejadores de errores
    @app.errorhandler(Exception)
    def handle_exception(e):
        logging.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

    @app.errorhandler(404)
    def not_found_error(e):
        logging.warning(f"Recurso no encontrado: {e}")
        return jsonify({"error": "Recurso no encontrado"}), 404

    return app
