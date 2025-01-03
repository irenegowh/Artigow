import requests
import logging

# Configurar el logger
logger = logging.getLogger("app_logger")

# Definir la URL del servicio db_service
DB_SERVICE_URL = 'http://db_service:5002'  # URL del servicio de base de datos

def get_user_by_id(user_id):
    """
    Obtiene un usuario por su ID a través de una solicitud HTTP al servicio db_service.
    """
    try:
        # Realizar una solicitud HTTP al servicio db_service para obtener al usuario por su ID
        response = requests.get(f'{DB_SERVICE_URL}/users/{user_id}')

        if response.status_code == 200:
            user = response.json()  # Obtener los datos del usuario desde db_service
            logger.info(f"Usuario con ID {user_id} obtenido correctamente.")
            return user
        else:
            logger.warning(f"Usuario con ID {user_id} no encontrado.")
            raise ValueError("Usuario no encontrado.")
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error de comunicación con db_service: {e}")
        raise ValueError("Error al conectar con el servicio de base de datos.")
    
    except Exception as e:
        logger.error(f"Error al obtener usuario con ID {user_id}: {e}")
        raise ValueError("Error al obtener usuario.")
