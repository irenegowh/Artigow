# Usa una imagen base de Python
FROM python:3.12-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /templates_service

# Copia los archivos necesarios dentro del contenedor
COPY . /templates_service

# Instalar las dependencias de la aplicación
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Exponer el puerto que Flask usará
EXPOSE 5006

# Establecer las variables de entorno necesarias para Flask
ENV FLASK_APP=templates_service.run
ENV FLASK_ENV=development

# Comando para ejecutar la app cuando se inicie el contenedor
CMD ["python", "-m", "templates_service.run"]
