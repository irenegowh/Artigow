# Usa una imagen base de Python
FROM python:3.9-slim

# Instalar dependencias necesarias para ejecutar psql (cliente de PostgreSQL)
RUN apt-get update && apt-get install -y postgresql-client

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /logs_container

# Copiar el archivo requirements.txt
COPY requirements.txt /logs_container/

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación (directorio app)
COPY app/ /logs_container/app/

# Copiar el archivo de configuración
COPY config.py /logs_container/config.py

# Copiar el script wait-for-db.sh y darle permisos de ejecución
COPY wait-for-db.sh /logs_container/wait-for-db.sh
RUN chmod +x /logs_container/wait-for-db.sh

# Exponer el puerto 5003 para la aplicación Flask
EXPOSE 5003

# Comando para ejecutar la aplicación de logs, usando wait-for-db.sh para esperar a la base de datos
CMD ["sh", "-c", "./wait-for-db.sh && python app/app.py"]
