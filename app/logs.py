#app/logs.py (Microservicio de gestión de logs)
import logging
from logging.handlers import RotatingFileHandler
from logging.config import dictConfig
import os

# Configuración del logger
def setup_logging():
    # Crear el directorio de logs si no existe
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Configuración central de logging con dictConfig
    dictConfig(
        {
            "version": 1,
            "formatters": {
                "default": {
                    "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "stream": "ext://sys.stdout",
                },
                "file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "formatter": "default",
                    "filename": "logs/app.log",
                    "maxBytes": 1000000,
                    "backupCount": 5,
                    "level": "INFO",
                },
            },
            "root": {
                "level": "INFO",
                "handlers": ["console", "file"],
            },
            "loggers": {
                "app_logger": {
                    "level": "INFO",
                    "handlers": ["console", "file"],
                    "propagate": False,
                },
            },
        }
    )

# Inicializa el logger para ser usado en toda la aplicación
logger = logging.getLogger("app_logger")