# tests/test_app.py
import pytest
from app import create_app, db
from app.models.posts import Post
from app.models.votes import Vote
from app.models.userprof import UserProf
from flask_login import FlaskLoginClient
from config import TestConfig
import requests
import time

########################################################
#                 APLICACIÓN MONOLÍTICA                #
########################################################

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

########################################################
#                   ENTORNO DOCKERIZADO                #
########################################################

# URLS base de cada servicio en el entorno Docker
BASE_URL_APP = "http://localhost:5000"
BASE_URL_LOGS = "http://localhost:5003"

@pytest.fixture(scope="session")
def wait_for_services():
    max_retries = 10
    for attempt in range(max_retries):
        try:
            app_response = requests.get(BASE_URL_APP)
            logs_response = requests.get(f"{BASE_URL_LOGS}/health")
            if app_response.status_code == 200 and logs_response.status_code == 200:
                return
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(5)
    pytest.fail("Los servicios no están disponibles después de varios intentos.")


def test_db_connection(client):
    with client.application.app_context():
        # Verificar que se pueda conectar a la base de datos
        result = db.session.execute('SELECT 1')
        assert result.scalar() == 1  # Verifica que la consulta devuelve 1

def test_logs_service():
    # Enviar una solicitud al servicio de logs con datos válidos
    log_data = {
        "level": "INFO",
        "module": "test_module",
        "message": "Esto es un mensaje de prueba"
    }
    response = requests.post(f"{BASE_URL_LOGS}/log", json=log_data)
    assert response.status_code == 201
    assert response.json()["status"] == "Log almacenado"

def test_connectivity_to_logs_service(wait_for_services):
    response = requests.get(f"{BASE_URL_LOGS}/health")
    assert response.status_code == 200
    assert response.json()["status"] == "Logs Service is running"

# Fixtures para entorno Docker
@pytest.fixture(scope="session")
def wait_for_services():
    """
    Espera a que los servicios en Docker estén disponibles.
    """
    max_retries = 10
    for attempt in range(max_retries):
        try:
            app_response = requests.get(BASE_URL_APP)
            logs_response = requests.get(f"{BASE_URL_LOGS}/health")  # Supongamos que logs_service tiene un endpoint de salud
            if app_response.status_code == 200 and logs_response.status_code == 200:
                print("Todos los servicios están disponibles.")
                return
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(5)
    pytest.fail("Los servicios no están disponibles después de varios intentos.")

# Tests de conectividad entre contenedores
def test_connectivity_to_app_service(wait_for_services):
    # Verifica que el servicio principal (app_service) responde correctamente.
    response = requests.get(BASE_URL_APP)
    assert response.status_code == 200
    assert b'Bienvenido a Artigow!' in response.content

def test_connectivity_to_logs_service(wait_for_services):  
    # Verifica que el servicio de logs responde correctamente.   
    response = requests.get(f"{BASE_URL_LOGS}/health")
    assert response.status_code == 200
    assert b'Logs Service is running' in response.content

# Tests funcionales en contenedores
def test_user_registration_and_login(wait_for_services):   
    # Prueba el flujo de registro e inicio de sesión en el entorno Docker.   
    # Registro
    registration_data = {
        'username': 'dockeruser',
        'email': 'docker@example.com',
        'password': 'password'
    }
    register_response = requests.post(
        f"{BASE_URL_APP}/auth/register",
        data=registration_data
    )
    assert register_response.status_code == 200

    # Login
    login_data = {
        'email': 'docker@example.com',
        'password': 'password'
    }
    login_response = requests.post(
        f"{BASE_URL_APP}/auth/login",
        data=login_data
    )
    assert login_response.status_code == 200


def test_create_and_vote_post(wait_for_services):
    # Prueba la creación de un post y la votación en el entorno Docker.
    # Datos de registro y login
    registration_data = {
        'username': 'dockeruser',
        'email': 'docker@example.com',
        'password': 'password'
    }
    requests.post(f"{BASE_URL_APP}/auth/register", data=registration_data)
    login_response = requests.post(
        f"{BASE_URL_APP}/auth/login",
        data={'email': 'docker@example.com', 'password': 'password'}
    )
    assert login_response.status_code == 200

    # Crear un nuevo post
    cookies = login_response.cookies  # Reutilizar cookies de autenticación
    post_data = {
        'title': 'Docker Post',
        'content': 'Este es un post de prueba en Docker.',
        'image': None
    }
    create_post_response = requests.post(
        f"{BASE_URL_APP}/posts/new_post",
        data=post_data,
        cookies=cookies
    )
    assert create_post_response.status_code == 200

    # Votar por el post (supongamos que conocemos el ID del post)
    post_id = 1  # Cambia según tu lógica
    vote_response = requests.post(
        f"{BASE_URL_APP}/votes/vote_post/{post_id}",
        cookies=cookies
    )
    assert vote_response.status_code == 200
    assert b'Voto registrado correctamente.' in vote_response.content

def test_user_registration_and_login(wait_for_services):
    # Registro
    registration_data = {
        "username": "dockeruser",
        "email": "docker@example.com",
        "password": "password"
    }
    register_response = requests.post(
        f"{BASE_URL_APP}/auth/register",
        json=registration_data
    )
    assert register_response.status_code == 200

    # Login
    login_data = {"email": "docker@example.com", "password": "password"}
    login_response = requests.post(f"{BASE_URL_APP}/auth/login", json=login_data)
    assert login_response.status_code == 200

