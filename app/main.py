import os
from flask import render_template, request, Blueprint, current_app, jsonify
from werkzeug.utils import secure_filename
from app import db  
from app.models.posts import Post

# Crear un Blueprint para las rutas
main_bp = Blueprint('main', __name__)

# Función para verificar si la extensión del archivo es permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

# Ruta de bienvenida
@main_bp.route('/')
def welcome():
    # return 'Bienvenido a Artigow!'
    return render_template('bienvenida.html')

# Ruta para listar publicaciones
@main_bp.route('/list_posts')
def list_posts():
    from app import db  # Importar db aquí, ya que ahora la app está completamente creada
    from app.models.posts import Post  # Crear una instancia de la clase Post
    posts = Post.query.all()
    return render_template('list_posts.html', posts=posts)

# Ruta para crear una nueva publicación
@main_bp.route('/new_post', methods=['GET', 'POST'])
def new_post():
    from app import db  # Importar db aquí para evitar la circularidad
    from app.models.posts import Post # Crear una instancia de la clase Post

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        user_id = request.form['user_id']
        
        # Verificar si se subió una imagen
        image = request.files.get('image')
        image_url = None
        
        if image and allowed_file(image.filename):
            # Guardar la imagen en el directorio especificado
            filename = secure_filename(image.filename)
            image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            image_url = f"images/{filename}"  # Guardar solo la ruta relativa a la imagen

        # Crear la publicación en la base de datos
        new_post = Post(title=title, content=content, image_url=image_url, user_id=user_id)
        db.session.add(new_post)
        db.session.commit()

        posts = Post.query.all()
        return render_template('list_posts.html', posts=posts)

    return render_template('new_post.html')
