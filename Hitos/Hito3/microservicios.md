# Microservicios y estructura de la API

Para este hito se ha hecho una división de las funcionalidades en microservicios.

Estos microservicios son:

1. Microservicio de autenticación

2. Microservicio de gestión de logs**

3. Microservicio de gestión de roles

4. Microservicio de publicaciones

1. Microservicio de gestión de votos

## 1. **Microservicio de autenticación**
El microservicio de autenticación se encarga de gestionar el registro, inicio de sesión y protección de rutas mediante la autenticación de usuarios. Este microservicio utiliza Flask-Login para manejar sesiones y bcrypt para cifrar contraseñas.
**Rutas principales**:
    ◦ **`POST /auth/register`**: Permite a los usuarios registrarse proporcionando **`username`**, **`email`** y **`password`**.
    ◦ **`POST /auth/login`**: Autentica a los usuarios y establece una sesión segura.
    ◦ **`GET /auth/logout`**: Cierra la sesión del usuario autenticado.
**Dependencias**:
    ◦ **`flask-login`** para la gestión de sesiones.
    ◦ **`bcrypt`** para hashing seguro de contraseñas.
**Protección de rutas**: Se utilizan decoradores como **`@login_required`** para restringir el acceso a rutas específicas únicamente a usuarios autenticados.

## **2. Microservicio de gestión de logs**
El microservicio de logs centraliza el registro de actividades, errores y eventos del sistema utilizando el módulo **`logging`** de Python. Permite mantener trazabilidad y depuración en tiempo de ejecución. Esta funcionalidad se está utilizando para identificar problemas de validación en tiempo de ejecución y para proporcionar un historial de acciones realizadas por los usuarios.
**Uso en el proyecto**:
    ◦ **Nivel de logs**: Configurado para registrar información (**`INFO`**) y errores (**`ERROR`**) importantes.
    ◦ **Ejemplo**:
        ▪ Log de acceso: **`logger.info(f"Usuario {current_user.username} accedió a crear un nuevo post.")`**
        ▪ Log de error: **`logger.error(f"Errores de validación al crear el post: {e.messages}")`**

    ◦ 
## **3. Microservicio de gestión de roles**
En un principio, se quería implementar este microservicio para gestionar los roles de los usuarios, permitiendo distinguir entre administradores y usuarios regulares. En la implementación actual no se distingue entre rol administrador y usuarios regulares, pero si que se distingue entre usuarios autenticados y no autenticados, mediante el uso de Flask-login:

Los métodos descritos proporcionan las siguientes funcionalidades clave:

- **Rutas (`users.py`)**: Gestionan el acceso a las acciones relacionadas con usuarios (perfil, actualización, eliminación).
- **Servicios (`user_service.py`)**: Encapsulan la lógica de negocio para registrar, actualizar y eliminar usuarios.
- **Repositorio (`user_repository.py`)**: Actúa como la capa de acceso a datos, interactuando directamente con la base de datos.
- **Modelo (`userprof.py`)**: Define la estructura de los usuarios en la base de datos y proporciona métodos auxiliares para la gestión de contraseñas.

## **4. Microservicio de publicaciones**
Este microservicio permite a los usuarios crear, listar y eliminar publicaciones. También implementa validaciones para garantizar que los datos de entrada sean correctos.
**Rutas principales**:
    ◦ **`GET /posts/new_post`**: Muestra el formulario para crear una nueva publicación.
    ◦ **`POST /posts/new_post`**: Procesa los datos enviados por el formulario y crea una publicación.
    ◦ **`GET /posts/list_posts`**: Muestra una lista de todas las publicaciones.
    ◦ **`GET /posts/delete_all_posts`**: Elimina todas las publicaciones del usuario actual.

**Validaciones**:
    ◦ Se utiliza Marshmallow para validar los datos enviados en las solicitudes (**`title`**, **`content`**, **`image`**).
    ◦ Los errores de validación devuelven un código de estado **`400`** con los detalles en formato JSON.

## **5. Microservicio de gestión de votos**
Permite a los usuarios votar por las publicaciones y calcular rankings basados en las votaciones.
**Rutas principales**:
    ◦ **`POST /votes/vote_post/<post_id>`**: Permite a un usuario votar por una publicación específica.
    ◦ **`GET /votes/ranking`**: Devuelve el ranking de publicaciones basado en los votos.
**Lógica del ranking**:
    ◦ Cada voto se almacena con un puntaje asignado.
    ◦ Las publicaciones se ordenan por la suma de los votos para generar el ranking.
