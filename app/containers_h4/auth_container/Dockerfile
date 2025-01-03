# Usa una imagen base de Python
FROM python:3.12-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /auth_service

# Copia los archivos necesarios dentro del contenedor
COPY . /auth_service

# Instalar las dependencias de la aplicación
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expón el puerto en el que se ejecuta la app
EXPOSE 5000

# Establece las variables de entorno necesarias para Flask
ENV FLASK_APP=auth_service.run
ENV FLASK_ENV=development

# Comando para ejecutar la app cuando se inicie el contenedor
CMD ["python", "-m", "auth_service.run"]
