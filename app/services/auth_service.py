# app/services/auth_service.py (Lógica de negocio de la autenticación y manejo de usuarios)
# app/services/auth_service.py

from app.repositories.auth_repository import AuthRepository
from flask_login import login_user, logout_user
import logging

logger = logging.getLogger("app_logger")

def register_user(data):
# Registra un nuevo usuario utilizando los datos proporcionados
    try:
        AuthRepository.add_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        logger.info(f"Usuario {data['username']} registrado correctamente.")
        return {"message": "Usuario registrado correctamente."}
    except Exception as e:
        logger.error(f"Error al registrar al usuario: {e}")
        raise ValueError("Error al registrar al usuario.")

def login_user_service(data):
    """
    Maneja el inicio de sesión del usuario.
    """
    try:
        email = data['email']
        password = data['password']

        user = AuthRepository.get_user_by_email(email)
        if user and user.check_password(password):
            login_user(user)
            logger.info(f"Usuario {email} inició sesión correctamente.")
            return {"message": "Inicio de sesión exitoso."}
        else:
            logger.warning(f"Intento de conexión fallido para el email: {email}.")
            raise ValueError("Credenciales inválidas.")
    except Exception as e:
        logger.error(f"Error al intentar iniciar sesión con el email {email}: {e}")
        raise ValueError("Error al iniciar sesión.")

def logout_user_service(user):
# Maneja el cierre de sesión de un usuario autenticado.
	try:
		logger.info(f"El usuario {user.username} está cerrando sesión.")
		logout_user()
		return {"message": "Sesión cerrada correctamente."}
	except Exception as e:
		logger.error(f"Error al cerrar sesión: {e}")
		raise ValueError("Error al cerrar sesión.")
