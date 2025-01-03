from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging

# Inicializar la base de datos
db = SQLAlchemy()

def create_app(config_class='config.Config'):
    # Crear la aplicación Flask
    app = Flask(__name__)

    # Cargar configuración desde config.py
    app.config.from_object(config_class)

    # Registrar el Blueprint con el prefijo '/user_routes'
    # Importar aquí para evitar importación circular
    from db_service.routes.user_routes import user_routes  # Asegúrate de importar correctamente el Blueprint
    app.register_blueprint(user_routes, url_prefix='/user_routes')

    # Inicializar extensiones
    db.init_app(app)
    Migrate(app, db)

    # Manejadores de errores (opcional)
    @app.errorhandler(404)
    def not_found_error(e):
        logging.warning(f"Recurso no encontrado: {e}")
        return jsonify({"error": "Recurso no encontrado"}), 404

    @app.errorhandler(500)
    def internal_error(e):
        logging.error(f"Error interno del servidor: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

    return app
