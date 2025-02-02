import os

# Configuración base
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'xxxxyyyyyzzzzz')  # Puedes establecer SECRET_KEY como una variable de entorno
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'app/static/images'

# Configuración para entorno local
class LocalConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@db_service:5432/artigow_db'

# Configuración para Render (Producción)
class RenderConfig(Config):
    DATABASE_URL_SQLALCHEMY = os.getenv('DATABASE_URL_SQLALCHEMY')
    print(f"DATABASE_URL_SQLALCHEMY: {DATABASE_URL_SQLALCHEMY}")  # Verificar si DATABASE_URL tiene un valor correcto    
    SQLALCHEMY_DATABASE_URI = str(DATABASE_URL_SQLALCHEMY)
    print(f"{os.getenv('FLASK_ENV')}")

# Configuración para prebas
class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True

# Seleccionar configuración según el entorno
def get_config():
    environment = os.getenv('FLASK_ENV', 'local')  # Por defecto, asumimos un entorno local
    if environment == 'production':
        return RenderConfig
    elif environment == 'testing':
        return TestConfig
    else:
        return LocalConfig
