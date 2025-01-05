## DB_SERVICE
###  Descripción del servicio
El contenedor db_service utiliza una configuración personalizada para implementar un servidor PostgreSQL que administra dos bases de datos específicas:
1. Base de datos principal (artigow_db): Usada por el servicio principal de la aplicación (app_service) para manejar sus datos.
2. Base de datos de logs (artigow_logs_db): Usada por el servicio de logs (logs_service) para almacenar los registros generados por la aplicación.

### Configuración del contenedor [Dockerfile de db_service](../../app/container_h4_Simple/db_container/Dockerfile)

- Contenedor base:
Utiliza una imagen de PostgreSQL específica (ghcr.io/irenegowh/artigow/db_service:latest), que se basa en la imagen oficial de PostgreSQL.
Se utiliza una imagen oficial de PostgreSQL (postgres:latest) como base.
Esta imagen personalizada incluye un script de inicialización 
para configurar automáticamente las bases de datos al 
arrancar el contenedor.
- Justificación del contenedor base:
PostgreSQL es una base de datos relacional robusta, ampliamente utilizada en aplicaciones modernas.
- Configuración personalizada
Se utilizan algunas variables de entorno que configuran las credenciales del servidor PostgreSQL:
1. POSTGRES_USER: Nombre del usuario administrador.
2. POSTGRES_PASSWORD: Contraseña del usuario administrador.
3. POSTGRES_DB: Define la creación inicial de la base de datos artigow_db .
```yaml
environment:
 POSTGRES_USER: user
 POSTGRES_PASSWORD: password
 POSTGRES_DB: artigow_db
```
- Script de Inicialización:
```yaml
volumes:- ./init.sql:/docker-entrypoint-initdb.d/init.s
```
Monta un archivo SQL llamado init.sql , que se encuentra en el host, dentro del directorio predeterminado de inicialización del contenedor (/docker-entrypoint-initdb.d/).
Este archivo ejecuta el siguiente comando al arrancar el contenedor:
```yaml
CREATE DATABASE artigow_logs_db;
```
Se crea la segunda base de datos requerida, artigow_logs_db.
-  Persistencia de Datos:
```yaml
volumes:
  - postgres_data:/var/lib/postgresql/data
```
- Red de Aplicación:
```yaml
networks:
  - app_network
```
Configura al contenedor para que se conecte a una red personalizada llamada 
app_network , permitiendo la comunicación con los demás servicios (logs_service).

### Justificación de la configuración personalizada
- Gestión de Múltiples Bases de Datos: PostgreSQL se usa para gestionar las bases de datos principales de la aplicación (artigow_db ) y de los registros de logs (artigow_logs_db ).
La separación en dos bases de datos permite aislar los datos de la aplicación de los logs, mejorando la organización y la seguridad.
- Inicialización Automática: El archivo init.sql simplifica la creación de la base de datos de logs al inicializar automáticamente artigow_logs_db.
- Persistencia de Datos: El volumen postgres_data asegura que los datos de ambas 
bases de datos se conserven entre reinicios del contenedor.
- Flexibilidad en Entornos Multi-Servicio: Al usar app_network , todos los servicios pueden comunicarse de manera eficiente dentro del entorno Docker, mientras que los servicios externos necesitan permisos explícitos.

### Puerto expuesto y justificación
1. Puerto Configurado:
```yaml
 ports:- "5433:5432"
```
- Puerto interno: 5432 (Puerto predeterminado de PostgreSQL dentro del contenedor).
- Puerto externo: 5433 (Puerto asignado en la máquina host para acceder al servicio).
  
2. Justificación del Puerto Expuesto:
Cambiar el puerto externo a 5433 evita conflictos si otro servicio de PostgreSQL ya está en ejecución en el host en el puerto predeterminado (5432).
El puerto externo permite pruebas y depuración desde herramientas locales (como clientes de PostgreSQL) conectándose a localhost:5433.
