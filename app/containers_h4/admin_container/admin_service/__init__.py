from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging

# Inicializar las extensiones
db = SQLAlchemy()

def create_app(config_class='config.Config'):
    app = Flask(__name__)

    # Cargar configuración
    app.config.from_object(config_class)

    # Inicializar las extensiones con la app
    db.init_app(app)
    Migrate(app, db)
    
    # Registrar Blueprints
    from admin_service.admin import admin_bp  # Importar el Blueprint desde admin_service.admin
    app.register_blueprint(admin_bp, url_prefix='/admin')  # Registrar el Blueprint con el prefijo '/admin'

    # Configurar manejo de errores dentro de la función
    @app.errorhandler(404)
    def not_found_error(e):
        logging.warning(f"Recurso no encontrado: {e}")
        return jsonify({"error": "Recurso no encontrado"}), 404

    @app.errorhandler(500)
    def internal_error(e):
        logging.error(f"Error interno del servidor: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

    return app
