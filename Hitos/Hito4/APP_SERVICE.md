## APP_SERVICE

###  Descripción del servicio
El contenedor app_service contiene la lógica principal de la aplicación. Es responsable de procesar las solicitudes de los usuarios y comunicarse con los otros servicios (bases de datos y servicio de logs) para gestionar las publicaciones y registrar eventos.

### Configuración del contenedor [Dockerfile de db_service](../../app/container_h4_Simple/app_container/Dockerfile)
1. Imagen base:
```yaml
FROM python:3.12-slim
```
Utiliza una imagen ligera de Python 3.12 para optimizar recursos.
2. Instalación de dependencias:
```yaml
RUN apt-get update && apt-get install -y postgresql-client
```
Instala el cliente de PostgreSQL para realizar conexiones con las bases de datos.
3. Dependencias Python:
```yaml
RUN pip install pipenv && pipenv install --system --deploy
RUN pip install -r requirements.txt
```
Instala las dependencias necesarias para la aplicación, incluidas bibliotecas como Flask, Flask-SQLAlchemy, Marshmallow, etc.
4. Exposición del puerto:
```yaml
EXPOSE 5000
```
Se expone el puerto 5000 para que el servicio pueda ser accedido desde el exterior (host).
5. Comando de inicio:
```yaml
CMD ["sh", "-c", "/wait-for-db.sh && flask db upgrade || echo 'No migrations to apply' && python /app/init_admin.py && python -m app.run"]
```
Este comando realiza: Espera que la base de datos principal esté disponible (wait-for-db.sh). Aplica migraciones a la base de datos (flask db upgrade). Crea un usuario administrador (init_admin.py). Inicia la aplicación. 
6. Configuración personalizada
- Conexión a la base de datos principal: En el archivo config.py, se configura la URI de conexión a PostgreSQL:
```yaml
SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@db_service:5432/artigow_db'
```
Esto indica que APP_SERVICE se conecta al contenedor db_service para interactuar con la base de datos artigow_db.
- Servicio de logs:
La URL del servicio de logs se define mediante una variable de entorno:
```yaml
LOG_SERVICE_URL = "http://logs_service:5003/log"
```
Esto establece la conexión con el contenedor logs_service.
- Inicialización del administrador: El script init_admin.py crea automáticamente un usuario administrador si no existe.
7. Comunicación con otros contenedores
- Base de datos principal (db_service): La conexión a la base de datos se realiza mediante la URI configurada en SQLALCHEMY_DATABASE_URI. Un ejemplo es la función create_post en el servicio post_service.py:
```python
def create_post(title, content, image, username):
new_post = Post(title=title, content=content, image_url=image_url, user_name=username)
db.session.add(new_post)
db.session.commit()
```
Este código usa SQLAlchemy para interactuar con artigow_db y registrar una nueva publicación.
- Servicio de logs (logs_service): La comunicación se realiza enviando solicitudes HTTP con el manejador HTTPLogHandler:
```python
class HTTPLogHandler(logging.Handler):
 def emit(self, record):
   log_entry = {
     "level": record.levelname,
     "module": record.module,
     "message": self.format(record)
   }
   requests.post(self.url, json=log_entry)
```
Por ejemplo, al registrar un evento en la función new_post:
```python
logger.info(f"Usuario {current_user.username} accedió a crear un nuevo post.")
```
El mensaje se envía al servicio de logs a través de:
```python
POST http://logs_service:5003/log Content-Type: application/json
{
  "level": "INFO",
   "module": "posts",
   "message": "Usuario admin accedió a crear un nuevo post."
}
```
8. Ejemplo de flujo completo de comunicación
- Usuario crea un post desde 
Ruta: /new_post .
APP_SERVICE: Se valida y guarda la información en la base de datos artigow_db .
- Se registra un log:
Se envía un mensaje al servicio de logs con detalles del evento.
- El servicio de logs guarda el evento:
Registra la información en la base de datos de logs artigow_logs_db .

### Justificación de la configuración personalizada
1. Conexión a la Base de Datos: Se utiliza PostgreSQL como base de datos principal, conectándose al servicio db_service para garantizar la integridad y centralización de los datos en un entorno Dockerizado.
2. Manejo de Logs Externos: Los logs se envían al servicio logs_service , permitiendo un monitoreo centralizado y en tiempo real, lo que facilita la depuración y el seguimiento de eventos críticos de la aplicación.
3. Inicialización Automática de Usuarios: Se implementa un script para crear automáticamente un usuario administrador si no existe, asegurando que siempre haya un punto de acceso inicial con privilegios para gestionar la aplicación.
4. Dependencia de Servicios Externos: Un script de espera asegura que el servicio no intente conectarse a la base de datos antes de que esta esté lista, mejorando la estabilidad en entornos con múltiples contenedores.
5. Estructura Modular y Validación de Datos: La aplicación está organizada en módulos para facilitar su mantenimiento, y se utiliza Marshmallow para validar los datos ingresados, asegurando su consistencia y fiabilidad.
6. Gestión de Recursos Estáticos: Los archivos subidos, como imágenes, se almacenan de manera segura en un directorio dedicado, con validaciones que previenen el manejo de archivos maliciosos.
7. Automatización del Inicio: El comando de inicio aplica migraciones, crea usuarios clave y lanza la aplicación, eliminando tareas manuales y garantizando que el contenedor esté listo para operar en cualquier entorno.

### Puerto expuesto y justificación
En el contenedor app_service, se expone el puerto 5000 al host. Esto se define en el archivo docker-compose.yml con la configuración ports: - "5000:5000" , donde el primer valor corresponde al puerto del host y el segundo al puerto interno del contenedor donde la aplicación Flask está escuchando.
