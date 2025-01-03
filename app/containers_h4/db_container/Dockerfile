# Usa una imagen base de Python
FROM python:3.12-slim

# Instalar PostgreSQL y las herramientas necesarias
RUN apt-get update && apt-get install -y \
    postgresql \
    postgresql-contrib \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo
WORKDIR /db_service

# Copia el código fuente al contenedor
COPY . /db_service

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Expón el puerto 5002 para el servicio
EXPOSE 5002

# Establece variables de entorno para Flask
ENV FLASK_APP=run.py
ENV FLASK_ENV=development

# Inicia PostgreSQL en segundo plano (background)
CMD service postgresql start && python -m db_service.run

# Configuración de Healthcheck
HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
  CMD pg_isready -U user -d artigow_db || exit 1
