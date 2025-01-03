class Config:
    SECRET_KEY = 'xxxxyyyyyzzzzz'
    SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@db_service:5432/artigow_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'app/static/images'

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Para pruebas locales
    TESTING = True  # Indicador para el entorno de pruebas
