import os

class Config:
    SECRET_KEY = 'supersecretkey'
    SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@db_service:5432/artigow_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
