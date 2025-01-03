from .auth import auth_bp
from .user import users_bp

# Exportar todos los Blueprints necesarios para el microservicio
__all__ = ['auth_bp', 'users_bp']
