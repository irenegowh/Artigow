import requests
import os

# URL de los servicios
DB_SERVICE_URL = os.getenv('DB_SERVICE_URL', 'http://db_service:5002')  # Servicio de la base de datos
POSTS_SERVICE_URL = os.getenv('POSTS_SERVICE_URL', 'http://posts_service:5004')  # Servicio de publicaciones


class VoteRepository:
    @staticmethod
    def add_vote(post_id, user_id):
        """
        Agrega un nuevo voto para un post dado.
        Realiza una consulta HTTP al db_service para registrar el voto.
        """
        try:
            # Realiza la solicitud HTTP al servicio de base de datos para agregar el voto
            response = requests.post(
                f"{DB_SERVICE_URL}/votes",
                json={"post_id": post_id, "user_id": user_id}
            )

            if response.status_code == 201:
                return response.json()
            else:
                raise ValueError(f"Error al registrar el voto: {response.text}")
        except Exception as e:
            raise ValueError(f"Error de conexión con db_service: {str(e)}")

    @staticmethod
    def get_votes_for_post(post_id):
        """
        Obtiene todos los votos para un post específico.
        Hace una consulta HTTP al db_service para obtener los votos.
        """
        try:
            response = requests.get(f"{DB_SERVICE_URL}/votes/{post_id}")
            if response.status_code == 200:
                return response.json()
            else:
                raise ValueError(f"Error al obtener los votos: {response.text}")
        except Exception as e:
            raise ValueError(f"Error de conexión con db_service: {str(e)}")

    @staticmethod
    def get_ranking():
        """
        Devuelve el ranking de publicaciones basado en los votos.
        Se hace una consulta HTTP al db_service para obtener los votos.
        """
        try:
            # Primero, obtenemos los votos desde el db_service
            response = requests.get(f"{DB_SERVICE_URL}/votes/ranking")
            if response.status_code != 200:
                raise ValueError(f"Error al obtener el ranking: {response.text}")

            ranking_data = response.json()

            # Crear un diccionario para almacenar el resultado enriquecido
            enriched_ranking = []

            for post in ranking_data:
                post_id = post["post_id"]
                vote_count = post["vote_count"]

                # Consultar los detalles del post desde el posts_service
                post_response = requests.get(f"{POSTS_SERVICE_URL}/posts/{post_id}")
                if post_response.status_code == 200:
                    post_data = post_response.json()
                    enriched_ranking.append({
                        "post_id": post_id,
                        "title": post_data.get("title", "Sin título"),
                        "author": post_data.get("author", "Desconocido"),
                        "vote_count": vote_count
                    })
                else:
                    enriched_ranking.append({
                        "post_id": post_id,
                        "title": "Post eliminado o no disponible",
                        "author": "Desconocido",
                        "vote_count": vote_count
                    })

            return enriched_ranking

        except Exception as e:
            raise ValueError(f"Error al obtener el ranking: {str(e)}")

    @staticmethod
    def get_user_votes(user_id):
        """
        Obtiene todos los votos de un usuario específico.
        Se hace una consulta HTTP al db_service para obtener los votos.
        """
        try:
            response = requests.get(f"{DB_SERVICE_URL}/user_votes/{user_id}")
            if response.status_code == 200:
                return response.json()
            else:
                raise ValueError(f"Error al obtener los votos del usuario: {response.text}")
        except Exception as e:
            raise ValueError(f"Error de conexión con db_service: {str(e)}")
