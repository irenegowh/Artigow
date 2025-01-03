from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import logging
from flask import render_template

# Inicializar las extensiones
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    
    # Cargar configuración
    app.config.from_object(config_class)

    # Inicializar las extensiones con la app
    db.init_app(app)
    Migrate(app, db)
    login_manager.init_app(app)
    
    # Configuración de login
    #login_manager.login_view = 'auth.login'

    # Registrar Blueprints
    from auth_service.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

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


@login_manager.user_loader
def load_user(user_id):
    # Asegúrate de importar correctamente el modelo desde el módulo correspondiente
    from auth_service.models.userprof import UserProf
    return UserProf.query.get(int(user_id))
