from flask import Flask
from templates_service.main import main_bp
from flask_sqlalchemy import SQLAlchemy

# Inicializa la base de datos fuera de la app para evitar la importación circular
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  # Configuración de la app
    
    # Registrar blueprint
    app.register_blueprint(main_bp)
    
    # Inicializa la base de datos con la app
    db.init_app(app)

    return app
