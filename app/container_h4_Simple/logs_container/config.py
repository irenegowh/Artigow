import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://user:2ydBw1MGaHyvqbXYUiIWcweUsh5257SB@dpg-cu8g8elsvqrc73baddcg-a.frankfurt-postgres.render.com:5432/artigow_logs_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
