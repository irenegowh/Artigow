import os

class Config:
    """Configuración base para la aplicación."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')  # Valor por defecto si no está definido
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'app/static/images'

class LocalConfig(Config):
    """Configuración para entorno local."""
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'LOCAL_DATABASE_URL',
        'postgresql://user:password@localhost:5432/artigow_db'
    )

class RenderConfig(Config):
    """Configuración para Render (Producción)."""
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://user:2ydBw1MGaHyvqbXYUiIWcweUsh5257SB@dpg-cu8g8elsvqrc73baddcg-a.frankfurt-postgres.render.com:5432/artigow_logs_db'
    )

class TestConfig(Config):
    """Configuración para pruebas."""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True

def get_config():
    """Seleccionar configuración según el entorno."""
    environment = os.getenv('FLASK_ENV', 'local').lower()
    if environment == 'production':
        return RenderConfig
    elif environment == 'testing':
        return TestConfig
    else:
        return LocalConfig
