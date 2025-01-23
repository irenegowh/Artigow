# Usa una imagen base de Python
FROM python:3.12-slim

# Instalar dependencias para `psql` (client de PostgreSQL)
RUN apt-get update && apt-get install -y postgresql-client

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY Pipfile Pipfile.lock requirements.txt /app/
COPY app/ /app/app
COPY config.py /app/config.py

# Copiar el script de inicialización para el usuario administrador
COPY init_admin.py /app/

# Instalar las dependencias de Python
RUN pip install pipenv && pipenv install --system --deploy
RUN pip install -r requirements.txt

# Instalar Flask-Migrate y psycopg2-binary si no están ya en requirements.txt
RUN pip install flask-migrate psycopg2-binary

# Migraciones
RUN if [ ! -d "/app/migrations" ]; then flask db init; fi
RUN flask db migrate -m "Initial migration"
RUN flask db upgrade

# Copiar el script de espera para la base de datos
COPY wait-for-db.sh /wait-for-db.sh
RUN chmod +x /wait-for-db.sh

# Asegurarse de que el directorio /app está en el PYTHONPATH
ENV PYTHONPATH=/app:$PYTHONPATH

# Expón el puerto en el que se ejecuta la app
EXPOSE 5000

# Comando de inicio: primero espera que la base de datos esté lista, luego aplica migraciones, ejecuta el script de admin y finalmente inicia la app
CMD ["sh", "-c", "/wait-for-db.sh && flask db upgrade || echo 'No migrations to apply' && python -m app.run & python /app/init_admin.py"]

