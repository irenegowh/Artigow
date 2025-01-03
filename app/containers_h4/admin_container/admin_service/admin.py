import os
import requests
from flask import Blueprint, current_app as app

# Definir URLs de servicios
DB_SERVICE_URL = 'http://db_service:5002'  # URL del servicio de base de datos
LOGS_SERVICE_URL = 'http://logs_service:5003/log'  # URL del servicio de logging

admin_bp = Blueprint('admin', __name__)

def log_to_service(level, message):
    """Enviar logs al servicio logs_service."""
    try:
        log_data = {'level': level, 'message': message}
        response = requests.post(LOGS_SERVICE_URL, json=log_data)

        # Verificar si el log fue registrado correctamente
        if response.status_code != 200:
            print(f"Error al enviar log: {response.text}")
    except Exception as e:
        print(f"Error al comunicarse con logs_service: {e}")


@admin_bp.route('/delete_all_posts', methods=['GET'])
def delete_all_posts():
    try:
        # Registrar log: inicio del proceso
        log_to_service('INFO', 'Iniciando eliminación de todos los posts.')

        # Solicitar todos los posts desde db_service
        response = requests.get(f'{DB_SERVICE_URL}/posts')
        
        if response.status_code != 200:
            log_to_service('ERROR', 'Error al obtener los posts desde db_service.')
            return "Error al obtener los posts.", 500
        
        posts = response.json()

        # Eliminar imágenes asociadas a los posts
        for post in posts:
            if post['image_url']:
                image_path = os.path.join(app.root_path, 'static', post['image_url'])
                try:
                    if os.path.exists(image_path):
                        os.remove(image_path)
                        log_to_service('INFO', f"Imagen {image_path} eliminada correctamente.")
                    else:
                        log_to_service('WARNING', f"Imagen no encontrada: {image_path}")
                except Exception as e:
                    log_to_service('ERROR', f"Error al eliminar {image_path}: {e}")

        # Solicitar la eliminación de todos los posts desde db_service
        delete_response = requests.delete(f'{DB_SERVICE_URL}/posts')

        if delete_response.status_code == 200:
            log_to_service('INFO', 'Todos los posts han sido eliminados correctamente.')

            # Solicitar la eliminación de todos los votos
            vote_delete_response = requests.delete(f'{DB_SERVICE_URL}/votes')
            if vote_delete_response.status_code == 200:
                log_to_service('INFO', 'Todos los votos han sido eliminados correctamente.')
                return "Todos los posts y votos han sido eliminados.", 200
            else:
                log_to_service('ERROR', 'Error al eliminar los votos.')
                return "Error al eliminar los votos.", 500
        else:
            log_to_service('ERROR', 'Error al eliminar los posts.')
            return "Error al eliminar los posts.", 500

    except requests.exceptions.RequestException as e:
        log_to_service('ERROR', f"Error de comunicación con db_service: {e}")
        return "Error de comunicación con el servicio de base de datos.", 500
