# app/services/user_service.py

from app.models.userprof import UserProf as User
import logging

logger = logging.getLogger("app_logger")

def get_user_by_id(user_id):
    """
    Obtiene un usuario por su ID.
    """
    try:
        user = User.query.get(user_id)
        if not user:
            logger.warning(f"Usuario con ID {user_id} no encontrado.")
            raise ValueError("Usuario no encontrado.")
        logger.info(f"Usuario con ID {user_id} obtenido correctamente.")
        return user
    except Exception as e:
        logger.error(f"Error al obtener usuario con ID {user_id}: {e}")
        raise ValueError("Error al obtener usuario.")
