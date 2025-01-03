import os

class Config:
    SECRET_KEY = 'supersecretkey'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://user:password@db_service:5432/artigow_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = '/path/to/uploads'  # Cambia esta ruta según la ubicación en el contenedor
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
