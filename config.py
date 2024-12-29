# config.py

class Config:
    SECRET_KEY = 'xxxxyyyyyzzzzz'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data/artigow.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'app/static/images'

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Para pruebas
    TESTING = True  # Indicador para el entorno de pruebas