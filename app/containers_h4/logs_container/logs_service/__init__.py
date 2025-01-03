from flask import Flask
from logs_service.logs import setup_logging, logger
from logs_service.logs import logs_bp

def create_app():
    # Inicializa Flask
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Configura logs
    setup_logging()
    logger.info("Logs Service iniciado.")

    # Registra las rutas
    app.register_blueprint(logs_bp)

    return app
