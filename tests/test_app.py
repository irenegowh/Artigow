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
BASE_URL_LOGS = "http://localhost:5003"  # Asegúrate de que la URL es la correcta

#******************************************************#
#                   contenedor de logs                 #
#******************************************************#
def test_connectivity_to_logs_service():
    try:
        # Verificar que el servicio de logs responde en el endpoint principal '/'
        response = requests.get(BASE_URL_LOGS)
        assert response.status_code == 200
        assert "formulario" in response.text.lower()  # Verifica si la palabra "formulario" está en la respuesta HTML
        print("El servicio de logs está disponible y funcionando.")
    except requests.exceptions.RequestException as e:
        pytest.fail(f"No se pudo conectar al servicio de logs: {e}")

def test_receive_log():
    log_data = {
        "level": "INFO",
        "module": "test_module",
        "message": "Este es un mensaje de prueba"
    }

    try:
        response = requests.post(f"{BASE_URL_LOGS}/log", json=log_data)
        assert response.status_code == 201
        assert response.json()["status"] == "Log almacenado"
        print("Log recibido y almacenado correctamente.")
    except requests.exceptions.RequestException as e:
        pytest.fail(f"No se pudo enviar el log: {e}")

def test_run_query():
    query_data = {
        "query": "SELECT * FROM application_logs LIMIT 1;"  # Asegúrate de que la tabla tiene datos
    }

    try:
        response = requests.post(f"{BASE_URL_LOGS}/query", json=query_data)
        assert response.status_code == 200
        result = response.json()
        assert isinstance(result, list)  # Debería devolver una lista de resultados
        print("Consulta SQL ejecutada correctamente.")
    except requests.exceptions.RequestException as e:
        pytest.fail(f"No se pudo ejecutar la consulta SQL: {e}")

def test_receive_log_incomplete_data():
    # Enviar un log incompleto (sin mensaje)
    log_data = {
        "level": "INFO",
        "module": "test_module"
    }

    try:
        response = requests.post(f"{BASE_URL_LOGS}/log", json=log_data)
        assert response.status_code == 400
        assert "Datos incompletos" in response.json()["error"]
        print("Respuesta correcta ante datos incompletos.")
    except requests.exceptions.RequestException as e:
        pytest.fail(f"No se manejó correctamente el error de datos incompletos: {e}")

def test_run_invalid_query():
    query_data = {
        "query": "SELECT * FROM non_existent_table;"  # Tabla inexistente
    }

    try:
        response = requests.post(f"{BASE_URL_LOGS}/query", json=query_data)
        assert response.status_code == 500
        assert "error" in response.json()
        print("Error manejado correctamente por consulta inválida.")
    except requests.exceptions.RequestException as e:
        pytest.fail(f"No se manejó correctamente el error de consulta inválida: {e}")

def test_retrieve_stored_logs():
    query_data = {
        "query": "SELECT * FROM application_logs LIMIT 1;"  # Suponiendo que hay al menos un log en la base de datos
    }

    try:
        response = requests.post(f"{BASE_URL_LOGS}/query", json=query_data)
        assert response.status_code == 200
        result = response.json()
        assert len(result) > 0  # Asegúrate de que se obtienen registros
        print("Logs recuperados correctamente.")
    except requests.exceptions.RequestException as e:
        pytest.fail(f"No se pudo recuperar los logs almacenados: {e}")


#******************************************************#
#                   contenedor de app                  #
#******************************************************#
BASE_URL_APP = "http://localhost:5000"  # Cambia si tu aplicación está en otra URL

def test_register_login_logout_user():
    # Paso 1: Generar un nombre de usuario único utilizando el timestamp actual
    unique_suffix = str(int(time.time()))  # Utilizamos el tiempo actual como sufijo único
    username = f"testuser_{unique_suffix}"
    
    registration_data = {
        "username": username,
        "email": f"{username}@example.com",
        "password": "securepassword"
    }

    # Enviar una solicitud POST al endpoint de registro
    response = requests.post(f"{BASE_URL_APP}/auth/register", data=registration_data)

    # Verificar que la respuesta de registro sea exitosa (código 200)
    assert response.status_code == 200, f"Expected 200, but got {response.status_code}"

    # Verificar que la respuesta contiene un mensaje de éxito (puedes modificar esto según el formato de tu respuesta)
    assert "Usuario registrado correctamente" in response.text, "Registration success message not found"

    # Paso 2: Intentar hacer login con las credenciales del usuario registrado
    login_data = {
        "email": f"{username}@example.com",
        "password": "securepassword"
    }
    
    # Enviar solicitud POST al endpoint de login
    login_response = requests.post(f"{BASE_URL_APP}/auth/login", data=login_data, cookies=response.cookies)

    # Verificar que la respuesta del login sea exitosa (código 302)
    assert login_response.status_code == 200, f"Expected 302, but got {login_response.status_code}"
    
    # Paso 3: Hacer logout
    logout_response = requests.get(f"{BASE_URL_APP}/auth/logout", cookies=login_response.cookies)

    # Verificar que el logout redirige a la página de login (código 302)
    assert logout_response.status_code == 200, f"Expected 302, but got {logout_response.status_code}"

def test_list_posts_container():
    # Enviar una solicitud GET al endpoint de listado de publicaciones
    response = requests.get(f"{BASE_URL_APP}/posts/list_posts")

    # Verificar que la respuesta sea exitosa (código 200)
    assert response.status_code == 200, f"Expected 200, but got {response.status_code}"

    # Verificar que la respuesta contiene información sobre las publicaciones
    assert "posts" in response.text, "No posts found in the response"

def test_create_new_post():
    # Autenticación (necesitarías una sesión activa de usuario)
    login_data = {"email": "testuser@example.com", "password": "securepassword"}
    login_response = requests.post(f"{BASE_URL_APP}/auth/login", data=login_data)

    # Verificar que el login fue exitoso (redirección a la página de bienvenida)
    assert login_response.status_code == 200

    unique_suffix = str(int(time.time()))
    # Crear un nuevo post
    post_data = {
        "title": "Nuevo Post de Test {unique_suffix}",
        "content": "Este es un post de prueba.",
    }

    # Enviar solicitud POST para crear el post
    create_post_response = requests.post(f"{BASE_URL_APP}/posts/new_post", data=post_data, cookies=login_response.cookies)

    # Verificar que la respuesta de la creación del post sea exitosa (redirección)
    assert create_post_response.status_code == 200, f"Expected 200, but got {create_post_response.status_code}"

    # Enviar solicitud GET para eliminar todos los posts
    delete_response = requests.get(f"{BASE_URL_APP}/posts/delete_all_posts", cookies=login_response.cookies)

    # Verificar que la respuesta de eliminación sea exitosa (código 200)
    assert delete_response.status_code == 200, f"Expected 200, but got {delete_response.status_code}"

    # Verificar que el mensaje de éxito se encuentra en la respuesta
    assert "Todas las publicaciones han sido eliminadas" in delete_response.json()["message"], "Delete all posts message not found"
