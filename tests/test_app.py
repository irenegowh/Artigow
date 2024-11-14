# tests/test_app.py
import pytest
import os
from app import create_app, db
from app.models.posts import Post


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Base de datos en memoria
    app.config['UPLOAD_FOLDER'] = 'app/static/images'

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client

def test_welcome_message(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Bienvenido a Artigow!' in response.data

def test_create_new_post(client):
    # Datos para el nuevo post
    data = {
        'title': 'Mi primer post',
        'content': 'Usa tus ojos y decide por ti mismo.',
        'user_id': 'Prueba0'
    }

    response = client.post('/new_post', data=data)
    assert response.status_code == 200
    assert b'Mi primer post' in response.data

def test_list_posts(client):
    # Agregar un post de prueba a la base de datos
    with client.application.app_context():
        post = Post(title='Test Post', content='Contenido de prueba', user_id='user123')
        db.session.add(post)
        db.session.commit()

        # Verificar la respuesta de la lista de posts
        response = client.get('/list_posts')
        assert response.status_code == 200
        assert b'Test Post' in response.data

def test_vote_post(client):
    from app.models.votes import Vote
    post = Post(title="Test Post", content="Test Content", user_id=1)
    db.session.add(post)
    db.session.commit()

    # Simular un voto a la publicación
    response = client.post(f'/vote_post/{post.id}')
    
    # Verificar que la respuesta redirige a la página de ranking
    assert response.status_code == 302  # Redirección (status 302)
    assert response.location == '/ranking'

    # Verificar que el voto fue guardado en la base de datos
    assert Vote.query.count() == 1  # Debe haber un voto registrado

def test_list_votes(client):
    from app.models.votes import Vote  # Importar el modelo Vote

    post1 = Post(title="Post 1", content="Content 1", user_id=1)
    post2 = Post(title="Post 2", content="Content 2", user_id=2)

    db.session.add(post1)
    db.session.add(post2)
    db.session.commit()

     # Realizar votos para las publicaciones
    vote1 = Vote(post_id=post1.id)
    vote2 = Vote(post_id=post2.id)
    db.session.add(vote1)
    db.session.add(vote2)
    db.session.commit()

    # Simular solicitud GET para obtener el ranking
    response = client.get('/ranking')


    # Verificar que la respuesta se recibe correctamente
    assert response.status_code == 200
    assert b'Post 1' in response.data  # Verificar que el título del post 1 aparece
    assert b'Post 2' in response.data  # Verificar que el título del post 2 aparece

def test_show_post(client):
    post = Post(title="Test Post", content="Test Content", user_id=1)
    db.session.add(post)
    db.session.commit()

    response = client.post(f'/show_post/{post.id}')

    # Verificar que la respuesta se recibe correctamente
    assert response.status_code == 200
    assert b'Test Post' in response.data  # Verificar que el título de la publicación aparece
    assert b'Test Content' in response.data  # Verificar que el contenido de la publicación aparece

    # Verificar que no se recibe error 404
    assert b'Post no encontrado' not in response.data

