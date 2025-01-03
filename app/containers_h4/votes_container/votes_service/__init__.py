from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging

# Inicializa la base de datos
db = SQLAlchemy()
migrate = Migrate()

# Inicializa el logger
logger = logging.getLogger('app_logger')

def create_app():
    # Crea la instancia de la aplicación Flask
    app = Flask(__name__)

    # Configura la aplicación con las variables de entorno o un archivo de configuración
    app.config.from_object('config.Config')

    # Inicializa la base de datos y la migración
    db.init_app(app)
    migrate.init_app(app, db)

    # Registra los blueprints del servicio
    from votes_service.routes.votes import votes_bp
    app.register_blueprint(votes_bp, url_prefix='/votes')

    # Otras configuraciones como CORS, logging, etc. pueden ir aquí.
    
    # Configurar logger (opcional, si deseas personalizar el log)
    logging.basicConfig(level=logging.INFO)
    logger.info("Votes Service iniciado.")

    return app
