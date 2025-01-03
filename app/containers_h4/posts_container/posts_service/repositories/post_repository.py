# app/repositories/post_repository.py

from post_service import db  # Para interactuar con la base de datos a través de SQLAlchemy
from post_service.models.posts import Post  # Importar el modelo de Post
from sqlalchemy.exc import SQLAlchemyError  # Para manejar errores en las consultas SQLAlchemy

class PostRepository:
    def __init__(self):
        # Usar la sesión global de SQLAlchemy proporcionada por Flask
        self.session = db.session

    def get_all_posts(self):
        try:
            # Recupera todos los posts
            return self.session.query(Post).all()
        except SQLAlchemyError as e:
            # Manejo de errores en la base de datos
            print(f"Error al obtener los posts: {e}")
            return []

    def get_post_by_id(self, post_id: int):
        try:
            # Recupera un post por su ID
            return self.session.query(Post).filter(Post.id == post_id).first()
        except SQLAlchemyError as e:
            # Manejo de errores en la base de datos
            print(f"Error al obtener el post con ID {post_id}: {e}")
            return None

    def create_post(self, title: str, content: str, image_url: str, user_name: str):
        try:
            # Crea un nuevo post en la base de datos
            new_post = Post(title=title, content=content, image_url=image_url, user_name=user_name)
            self.session.add(new_post)
            self.session.commit()  # Realiza la transacción
            return new_post
        except SQLAlchemyError as e:
            # Manejo de errores en la base de datos
            print(f"Error al crear el post: {e}")
            self.session.rollback()  # En caso de error, se revierte la transacción
            return None

    def delete_post(self, post: Post):
        try:
            # Elimina un post de la base de datos
            self.session.delete(post)
            self.session.commit()  # Realiza la transacción
        except SQLAlchemyError as e:
            # Manejo de errores en la base de datos
            print(f"Error al eliminar el post: {e}")
            self.session.rollback()  # En caso de error, se revierte la transacción
