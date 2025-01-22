#*************************#
# Configuracion en local  #
#*************************
class Config:
    SECRET_KEY = 'xxxxyyyyyzzzzz'
    SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@db_service:5432/artigow_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'app/static/images'

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Para pruebas locales
    TESTING = True  # Indicador para el entorno de pruebas

#*************************#
# Configuracion en Render #
#*************************#
#class Config:
#    SECRET_KEY = 'xxxxyyyyyzzzzz'
#    # Usar la URL externa de la base de datos proporcionada por Render
#    SQLALCHEMY_DATABASE_URI = 'postgresql://artigowdb_user:hOZs4UHZpYxNlCPtVX2Pr4kMCRA96X9M@dpg-cu816b8gph6c7397vs6g-a:5432/artigowdb'
#    SQLALCHEMY_TRACK_MODIFICATIONS = False
#    UPLOAD_FOLDER = 'app/static/images'

#class TestConfig(Config):
#    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Para pruebas locales
#    TESTING = True  # Indicador para el entorno de pruebas
