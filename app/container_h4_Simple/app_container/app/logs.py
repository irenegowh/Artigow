import logging
import logging.config
from logging.handlers import RotatingFileHandler
import requests
import os
import json


class HTTPLogHandler(logging.Handler):
    """Manejador personalizado para enviar logs al microservicio de logs."""
    def __init__(self, url):
        super().__init__()
        self.url = url

    def emit(self, record):
        log_entry = {
            "level": record.levelname,
            "module": record.module,
            "message": self.format(record)
        }
        try:
            print("Enviando log:", log_entry)  # Verifica que se está enviando el log
            requests.post(self.url, json=log_entry)
        except Exception as e:
            print(f"Error enviando log: {e}")


# Configuración del logger
def setup_logging():
    if not os.path.exists('logs'):
        os.makedirs('logs')

    log_url = os.getenv('LOG_SERVICE_URL')
    print(f"URL del servicio de logs: {log_url}")

    logging_config = {
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
            "http": {
                "()": HTTPLogHandler,
                "url": log_url,
            }
        },
        "root": {
            "level": "INFO",
            "handlers": ["console", "file", "http"],
        },
        "loggers": {
            "app_logger": {
                "level": "INFO",
                "handlers": ["console", "file", "http"],
                "propagate": False,
            },
        },
    }

    logging.config.dictConfig(logging_config)


logger = logging.getLogger("app_logger")
