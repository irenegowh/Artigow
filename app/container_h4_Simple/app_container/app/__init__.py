from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask import jsonify
import logging
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=None):
    app = Flask(__name__)

    # Configuración de la app (esto lo tienes bien)
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
    db.init_app(app)  # Aquí es donde se registra SQLAlchemy con la app
    login_manager.init_app(app)
    Migrate(app, db)  # Inicializa Flask-Migrate para manejar las migraciones de la base de datos

    # Imprimir todas las rutas registradas
    with app.app_context():
    print("Rutas registradas en la aplicación:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule.rule}")

    @app.errorhandler(Exception)
    def handle_exception(e):
        logging.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

    @app.errorhandler(404)
    def not_found_error(e):
        logging.warning(f"Recurso no encontrado: {e}")
        return jsonify({"error": "Recurso no encontrado"}), 404

    return app
