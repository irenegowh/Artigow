#app/admin.py: Microservicio gestión de administradores
import os
from . import create_app, db
from .models import Post, Vote

app = create_app()

@app.route('/delete_all_posts', methods=['GET'])
def delete_all_posts():
    with app.app_context():
        posts = Post.query.all()
        votes = Vote.query.all()

        # Eliminar imágenes asociadas a los posts
        for post in posts:
            if post.image_url:
                image_path = os.path.join(app.root_path, 'static', post.image_url)
                try:
                    if os.path.exists(image_path):
                        os.remove(image_path)
                        print(f"Imagen {image_path} eliminada correctamente.")
                    else:
                        print(f"Imagen no encontrada: {image_path}")
                except Exception as e:
                    print(f"Error al eliminar {image_path}: {e}")

        # Eliminar todos los registros de la tabla 'posts' y 'votes'
        Post.query.delete()
        Vote.query.delete()
        db.session.commit()
        return "Todos los posts han sido eliminados.", 200
