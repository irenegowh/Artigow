# Documentación y justificación de la configuración de cada uno de los 
contenedores

## DB_SERVICE
###  Descripción del servicio
El contenedor db_service utiliza una configuración personalizada para implementar un servidor PostgreSQL que administra dos bases de datos específicas:
1. Base de datos principal (artigow_db): Usada por el servicio principal de la aplicación (app_service) para manejar sus datos.
2. Base de datos de logs (artigow_logs_db): Usada por el servicio de logs (logs_service) para almacenar los registros generados por la aplicación.
