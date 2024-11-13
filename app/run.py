import os
from app import create_app, db
from app.models import Post  # Asegúrate de importar el modelo Post

app = create_app()

# Crear todas las tablas en la base de datos
with app.app_context():
    db.create_all()

@app.route('/delete_all_posts', methods=['GET'])
def delete_all_posts():
    with app.app_context():  # Usa el contexto de la aplicación
        posts = Post.query.all()

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


        # Eliminar todos los registros de la tabla 'posts'
        Post.query.delete()
        db.session.commit()
        return "Todos los posts han sido eliminados.", 200

if __name__ == '__main__':  
    app.run(debug=True)
