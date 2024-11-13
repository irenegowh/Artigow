from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# Crear la instancia de la base de datos
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configuración de la base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./artigow.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desactivar la advertencia

    # Definir el directorio donde se guardarán las imágenes
    UPLOAD_FOLDER = 'app/static/images'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # Inicializar la base de datos
    db.init_app(app)
    migrate = Migrate(app, db)  # Esto configura Flask-Migrate

    # Importar el blueprint después de inicializar db
    from .main import main_bp
    app.register_blueprint(main_bp)

    return app
