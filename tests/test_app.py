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