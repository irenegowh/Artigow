# app/routes/posts.py
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, abort
from flask_login import login_required, current_user
from app.services.post_service import create_post, list_all_posts, delete_all_user_posts, get_post_by_id
import logging
from marshmallow import ValidationError
from app.schemas.post_schema import PostSchema

logger = logging.getLogger("app_logger")

posts_bp = Blueprint('posts', __name__)

post_schema = PostSchema()

@posts_bp.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    logger.info(f"Usuario {current_user.username} accedió a crear un nuevo post.")
    if request.method == 'POST':
        data = {
            'title': request.form.get('title'),
            'content': request.form.get('content'),
            'image': request.files.get('image')
        }
        try:
            post_schema.load(data)  # Validar datos
            create_post(data['title'], data['content'], data['image'], current_user.username)
            return redirect(url_for('posts.list_posts'))
        except ValidationError as e:
            logger.error(f"Errores de validación al crear el post: {e.messages}")
            return jsonify({"errors": e.messages}), 400  # Respuesta con código 400
        except Exception as e:
            logger.error(f"Error inesperado al crear el post: {e}")
            abort(500)
    return render_template('new_post.html')


@posts_bp.route('/list_posts')
def list_posts():
    logger.info("Acceso al listado de publicaciones.")
    try:
        posts = list_all_posts()
        return render_template('list_posts.html', posts=posts)
    except ValueError as e:
        logger.error(f"Error al listar publicaciones: {e}")
        abort(500)

@posts_bp.route('/delete_all_posts/<string:username>', methods=['GET'])
@login_required
def delete_all_posts(username):
    logger.info(f"Usuario {username} accedió a borrar sus publicaciones.")
    try:
        # Llamar al servicio para eliminar todas las publicaciones del usuario proporcionado
        delete_all_user_posts(username)
        return jsonify({"message": f"Todas las publicaciones del usuario {username} han sido eliminadas."}), 200
    except ValueError as e:
        logger.error(f"Error al eliminar publicaciones para el usuario {username}: {e}")
        abort(500)

@posts_bp.route('/show_post/<int:post_id>', methods=['POST'])
def show_post(post_id):
    logger.info(f"Acceso al post con ID: {post_id}.")
    try:
        post = get_post_by_id(post_id)
        return render_template('show_post.html', post=post)
    except ValueError as e:
        logger.error(f"Error al mostrar publicación: {e}")
        abort(404)
