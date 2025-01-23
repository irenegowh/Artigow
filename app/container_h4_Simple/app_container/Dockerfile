# Usa una imagen base de Python
FROM python:3.12-slim

# Instalar dependencias para `psql` (cliente de PostgreSQL)
RUN apt-get update && apt-get install -y postgresql-client

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY Pipfile Pipfile.lock requirements.txt /app/
COPY app/ /app/app
COPY config.py /app/config.py
COPY init_admin.py /app/

# Instalar las dependencias de Python
RUN pip install pipenv && pipenv install --system --deploy
RUN pip install -r requirements.txt

# Instalar Flask-Migrate y psycopg2-binary si no están ya en requirements.txt
RUN pip install flask-migrate psycopg2-binary

# Copiar el script de espera para la base de datos
COPY wait-for-db.sh /wait-for-db.sh
RUN chmod +x /wait-for-db.sh

# Asegurar que el directorio /app está en el PYTHONPATH
ENV PYTHONPATH=/app:$PYTHONPATH

# Expón el puerto en el que se ejecuta la app
EXPOSE 5000

# Modifica el comando de inicio para verificar si las migraciones existen y crearlas si es necesario
CMD ["sh", "-c", "/wait-for-db.sh && flask db init || echo 'Migrations already initialized' && flask db upgrade && python /app/init_admin.py && flask run --host=0.0.0.0"]

