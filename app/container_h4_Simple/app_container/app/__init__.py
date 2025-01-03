# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from app.logs import setup_logging
from flask import jsonify
import logging


db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=None):
    app = Flask(__name__)
    if config_class:
        app.config.from_object(config_class)
    elif app.config['TESTING']:
        app.config.from_object('config.TestConfig')
    else:
        app.config.from_object('config.Config')
   
    setup_logging()  # Inicializa el sistema de logging
    logger = logging.getLogger("app_logger")
    logger.info("Aplicación inicializada")
    
    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
        
    # Registrar Blueprints
    from app.routes import main_bp, auth_bp, posts_bp, votes_bp, users_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(posts_bp, url_prefix='/posts')
    app.register_blueprint(votes_bp, url_prefix='/votes')
    app.register_blueprint(users_bp, url_prefix='/user')

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

