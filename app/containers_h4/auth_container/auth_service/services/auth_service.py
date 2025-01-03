# auth_service.py
import logging
import requests
import os
from flask_login import login_user, logout_user
from requests.exceptions import RequestException

logger = logging.getLogger("app_logger")
# DB_SERVICE_URL = os.getenv('DB_SERVICE_URL', 'http://db_service:5002/users')
DB_SERVICE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@db_service:5432/artigow_db')

if not DB_SERVICE_URL:
    logger.critical("La URL del servicio de base de datos no está configurada. Revisa las variables de entorno.")
    raise SystemExit("DB_SERVICE_URL no está configurada.")

def register_user(data):
    try:
        if not data.get('username') or not data.get('email') or not data.get('password'):
            raise ValueError("Campos requeridos faltantes")

        response = requests.post(DB_SERVICE_URL, json=data, timeout=10)
        if response.status_code == 201:
            logger.info(f"Usuario {data['username']} registrado correctamente.")
            return {"message": "Usuario registrado correctamente."}
        else:
            try:
                error_detail = response.json().get('error', 'Detalle no disponible')
            except ValueError:
                error_detail = 'Respuesta no válida del servicio de base de datos'
            
            logger.error(f"Error al registrar usuario: {error_detail}")
            raise ValueError(f"Error al registrar usuario: {error_detail}")

    except requests.ConnectionError:
        logger.error("No se pudo conectar al servicio de base de datos.")
        raise ValueError("Servicio de base de datos no disponible.")
    except requests.Timeout:
        logger.error("La solicitud al servicio de base de datos superó el tiempo de espera.")
        raise ValueError("Tiempo de espera excedido al conectar con el servicio de base de datos.")
    except requests.RequestException as e:
        logger.error(f"Error en la solicitud HTTP: {e}")
        raise ValueError("Ocurrió un error inesperado al conectar con el servicio de base de datos.")
    except Exception as e:
        logger.error(f"Error inesperado: {e}")
        raise ValueError("Error inesperado al registrar al usuario.")

    
def login_user_service(data):
    """
    Maneja el inicio de sesión del usuario.
    """
    try:
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise ValueError("Campos requeridos faltantes")

        # Buscar al usuario por email en la base de datos (deberías hacer la búsqueda en db_service)
        user = db_service_query_user_by_email(email)

        if user and user.check_password(password):  # Verificar la contraseña
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
    """
    Maneja el cierre de sesión de un usuario autenticado.
    """
    try:
        logger.info(f"El usuario {user.username} está cerrando sesión.")
        logout_user()
        return {"message": "Sesión cerrada correctamente."}
    except Exception as e:
        logger.error(f"Error al cerrar sesión: {e}")
        raise ValueError("Error al cerrar sesión.")
