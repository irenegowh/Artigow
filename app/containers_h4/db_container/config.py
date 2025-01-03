import os

class Config:
    SECRET_KEY = 'supersecretkey'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://user:password@db:5433/artigow_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
