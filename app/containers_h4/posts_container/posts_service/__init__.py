from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Inicializar la base de datos
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Cargar la configuración desde el archivo config.py
    app.config.from_object('config.Config')

    # Inicializar las extensiones
    db.init_app(app)
    migrate.init_app(app, db)

    # Registrar los Blueprints
    from posts_service.routes.posts import posts_bp
    app.register_blueprint(posts_bp, url_prefix='/posts')

    return app
