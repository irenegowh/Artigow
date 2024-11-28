# app/routes/__init__py

from .main import main_bp
from .auth import auth_bp
from .posts import posts_bp
from .votes import votes_bp
from .user import users_bp

# Exportar todos los Blueprints para que sean fácilmente importables
__all__ = ['main_bp', 'auth_bp', 'posts_bp', 'votes_bp', 'users_bp']
