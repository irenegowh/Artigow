# tests/test_app.py
import pytest
from app import create_app, db
from app.models.posts import Post
from app.models.votes import Vote
from app.models.userprof import UserProf
from flask_login import FlaskLoginClient
from config import TestConfig


@pytest.fixture
def app():
    app = create_app(config_class=TestConfig)
    app.test_client_class = FlaskLoginClient
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


@pytest.fixture
def authenticated_client(client):
    # Registrar un nuevo usuario
    registration_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password'
    }
    register_response = client.post(
        '/auth/register',
        data=registration_data,
        follow_redirects=True  # Sigue las redirecciones para verificar el flujo
    )
    assert register_response.status_code == 200  # Asegura que el registro fue exitoso

    # Iniciar sesión con las credenciales recién creadas
    login_response = client.post(
        '/auth/login',
        data={'email': 'test@example.com', 'password': 'password'},
        follow_redirects=True
    )
    assert login_response.status_code == 200  # Asegura que el login fue exitoso

    yield client



def test_welcome_message(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Bienvenido a Artigow!' in response.data


def test_create_new_post(authenticated_client):
    # Acceder al formulario de nuevo post
    response = authenticated_client.get('/posts/new_post')
    assert response.status_code == 200

    # Datos para el post
    data = {
        'title': 'Mi primer post',
        'content': 'Las rosas son rojas, las violetas azules.',
        'image': None
    }

    # Enviar el formulario
    response = authenticated_client.post('/posts/new_post', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Mi primer post' in response.data


def test_list_posts(client):
    # Crear datos de prueba
    with client.application.app_context():
        post = Post(title='Test Post', content='Contenido de prueba', user_name='user123')
        db.session.add(post)
        db.session.commit()

    # Verificar la lista de posts
    response = client.get('/posts/list_posts')
    assert response.status_code == 200
    assert b'Test Post' in response.data


def test_vote_post(authenticated_client):
    # Crear un post de prueba
    with authenticated_client.application.app_context():
        post = Post(title="Post de prueba", content="Contenido de prueba", user_name="testuser")
        db.session.add(post)
        db.session.commit()
        post_id = post.id  # Extraer el ID mientras la sesión está activa

    # Votar por el post usando el ID extraído
    response = authenticated_client.post(f'/votes/vote_post/{post_id}', follow_redirects=True)
    assert response.status_code == 200
    assert b'Voto registrado correctamente.' in response.data


def test_ranking(authenticated_client):
    # Crear posts y votos de prueba
    with authenticated_client.application.app_context():
        user = UserProf.query.filter_by(username="testuser").first()
        assert user is not None, "El usuario testuser no se encontró"

        post1 = Post(title="Post 1", content="Content 1", user_name=user.username)
        post2 = Post(title="Post 2", content="Content 2", user_name=user.username)
        db.session.add(post1)
        db.session.add(post2)
        db.session.commit()

        vote1 = Vote(post_id=post1.id, user_id=user.id)
        vote2 = Vote(post_id=post2.id, user_id=user.id)
        db.session.add(vote1)
        db.session.add(vote2)
        db.session.commit()

    # Consultar el ranking
    response = authenticated_client.get('/votes/ranking', follow_redirects=True)
    assert response.status_code == 200
    assert b'Post 1' in response.data
    assert b'Post 2' in response.data

def test_404_not_found(client):
    response = client.get('/ruta/inexistente')
    assert response.status_code == 404
    assert 'Recurso no encontrado'.encode('utf-8') in response.data  # Cambiar el texto a lo que la API devuelve
