# app/services/post_service.py
import os
from werkzeug.utils import secure_filename
from app import db
from app.models.posts import Post
from app.models.votes import Vote

from flask import current_app
import logging

logger = logging.getLogger("app_logger")

def allowed_file(filename):
# Verifica si el archivo tiene una extensión permitida.
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

def create_post(title, content, image, username):
# Crea una nueva publicación.
    try:
        image_url = None
        if image and allowed_file(image.filename):
            # Guardar la imagen
            filename = secure_filename(image.filename)
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            image_url = f"images/{filename}"
            logger.info(f"Imagen guardada en: {image_url}")

        # Crear la publicación
        new_post = Post(title=title, content=content, image_url=image_url, user_name=username)
        db.session.add(new_post)
        db.session.commit()
        logger.info(f"Publicación '{title}' creada por {username}")
        return new_post
    except Exception as e:
        logger.error(f"Error al crear la publicación: {e}")
        db.session.rollback()
        raise ValueError("No se pudo crear la publicación.")

def list_all_posts():
# Devuelve todas las publicaciones.
    try:
        posts = Post.query.all()
        logger.info("Consulta de publicaciones realizada correctamente.")
        return posts
    except Exception as e:
        logger.error(f"Error al consultar publicaciones: {e}")
        raise ValueError("No se pudo obtener la lista de publicaciones.")

def delete_all_user_posts(username):
# Elimina todas las publicaciones de un usuario.
    try:
        posts = Post.query.filter_by(user_name=username).all()
        if not posts:
            logger.warning(f"No se encontraron publicaciones para el usuario {username}.")
            raise ValueError("No se encontraron publicaciones para eliminar.")

        # Eliminar imágenes asociadas
        for post in posts:
            if post.image_url:
                image_path = os.path.join(current_app.root_path, 'static', post.image_url)
                if os.path.exists(image_path):
                    os.remove(image_path)
                    logger.info(f"Imagen eliminada: {image_path}")

        # Eliminar publicaciones
        for post in posts:
            db.session.delete(post)
        db.session.commit()
        logger.info(f"Publicaciones del usuario {username} eliminadas correctamente.")
    except Exception as e:
        logger.error(f"Error al eliminar publicaciones: {e}")
        db.session.rollback()
        raise ValueError("Error al eliminar publicaciones.")

def get_post_by_id(post_id):
# Obtiene una publicación por ID.
    try:
        post = db.session.get(Post, post_id)
        if not post:
            logger.warning(f"Publicación con ID {post_id} no encontrada.")
            raise ValueError("Publicación no encontrada.")
        return post
    except Exception as e:
        logger.error(f"Error al obtener la publicación: {e}")
        raise ValueError("Error al obtener la publicación.")


def delete_votes_by_post(username):
    try:
        # Obtén los posts del usuario
        posts = Post.query.filter_by(username=username).all()
        for post in posts:
            # Elimina los votos relacionados con este post
            votes = Vote.query.filter_by(post_id=post.id).all()
            for vote in votes:
                db.session.delete(vote)
        db.session.commit()  # Guarda los cambios
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Error al eliminar votos asociados: {str(e)}")

def delete_votes_by_user(user_id):
    try:
        # Eliminar todos los votos asociados al usuario
        votes = Vote.query.filter_by(user_id=user_id).all()
        for vote in votes:
            db.session.delete(vote)
        db.session.commit()
        logger.info(f"Votos relacionados con el usuario {user_id} eliminados.")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error al eliminar votos: {e}")
        raise ValueError("Error al eliminar votos relacionados.")

def delete_all_user_posts(user_name):
    try:
        # Obtén todas las publicaciones del usuario
        posts = Post.query.filter_by(user_name=user_name).all()
        if not posts:
            logger.warning(f"No se encontraron publicaciones para el usuario {user_name}.")
            raise ValueError("No se encontraron publicaciones para eliminar.")

        # Eliminar imágenes asociadas
        for post in posts:
            if post.image_url:
                image_path = os.path.join(current_app.root_path, 'static', post.image_url)
                if os.path.exists(image_path):
                    os.remove(image_path)
                    logger.info(f"Imagen eliminada: {image_path}")

        # Eliminar publicaciones
        for post in posts:
            db.session.delete(post)
        db.session.commit()
        logger.info(f"Publicaciones del usuario {user_name} eliminadas correctamente.")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error al eliminar publicaciones: {e}")
        raise ValueError("Error al eliminar publicaciones.")
