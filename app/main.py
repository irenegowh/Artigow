import os
from flask import render_template, request, Blueprint, current_app, jsonify, session, redirect, url_for
from werkzeug.utils import secure_filename
from app import db  
from app.models.posts import Post
from sqlalchemy import func

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

@main_bp.route('/vote_post/<int:post_id>', methods=['POST'])
def vote_post(post_id):
    from app.models.votes import Vote  # Crear una instancia de la clase Post
    from app.models.posts import Post 
    # user_id = get_current_user_id()  # Reemplazar con la lógica para obtener el ID del usuario
    #existing_vote = Vote.query.filter_by(user_id=user_id, post_id=post_id).first()
    #existing_vote = Vote.query.filter_by(post_id=post_id).first()
    votes = Vote.query.all()
    #if existing_vote:
    #    num_votes = len(votes)
    #    return {"message": f"Ya has votado este post {num_votes} "}, 400  # Devuelve un error si ya existe

    new_vote = Vote(post_id=post_id)
    db.session.add(new_vote)
    db.session.commit()   

    posts = Post.query.all() 
    return redirect(url_for('main.ranking'))

@main_bp.route('/ranking', methods=['GET'])
def ranking():
    from app import db  # Import db here, as the app is now fully created
    from app.models.posts import Post  # Import Post model
    from app.models.votes import Vote  # Import Vote model

    # Perform an outer join between posts and votes, counting votes for each post
    #order_posts = Post.query.all()
    order_posts = Post.query.outerjoin(Post.votes).group_by(Post.id).order_by(func.count(Post.votes).desc()).all()

    return render_template('list_votes.html', order_posts=order_posts)


@main_bp.route('/show_post/<int:post_id>', methods=['POST'])
def show_post(post_id):

    post = Post.query.filter_by(id=post_id).first()  # .first() para obtener un solo resultado o None si no existe
    
    if not post:
        # Si el post no existe, redirige o muestra un error
        return "Post no encontrado", 404
    return render_template('show_post.html', post=post)

    