# Contenedor log_service

## Descripción del servicio
El contenedor logs_service implementa un microservicio basado en Flask, diseñado para recibir y gestionar logs de aplicaciones en una base de datos PostgreSQL. Este servicio se encuentra integrado dentro de una arquitectura de microservicios, interactuando con los otros componentes, como la base de datos en el contenedor db_services y el servicio de la aplicación (app_service).

## Configuración del contenedor
La configuración del contenedor para logs_service incluye varios aspectos clave que garantizan su correcto funcionamiento y su integración en una arquitectura basada en microservicios. Estas configuraciones están cuidadosamente estructuradas en el Dockerfile y el archivo docker-compose.yml.
- Contenedor base: python:3.9-slim. Es una imagen ligera con soporte completo para Python 3.9, ideal para reducir el tamaño del contenedor mientras asegura un entorno funcional para la aplicación.
- Instalación de Dependencias del Sistema:
Dependencia clave: postgresql-client.
Propósito: Este cliente permite probar y gestionar la conexión con la base de datos PostgreSQL desde el contenedor, crucial para el script wait-for-db.sh.
- Configuración del Directorio de Trabajo:
Directorio: /logs_container: Establece un espacio lógico donde se organiza todo el código, configuraciones y scripts necesarios para el servicio.
- Instalación de Dependencias de Python:
Se utiliza pip install para instalar paquetes desde requirements.txt y la opción --no-cache-dir optimiza el tamaño del contenedor eliminando archivos temporales.
- Copiado de Archivos Esenciales:
Archivos clave: app/, config.py, wait-for-db.sh. Estos archivos contienen la lógica de la aplicación, la configuración de la base de datos y scripts para garantizar la disponibilidad de servicios dependientes.
- Comando de Inicio: Combina el script (wait-for-db.sh) con el arranque de Flask (app.py), asegurando la disponibilidad de la base de datos antes de iniciar la aplicación.
El script wait-for-db.sh tiene como propósito principal asegurar que el servicio de base de datos PostgreSQL esté completamente operativo antes de iniciar la aplicación que depende de ella. Esto evita errores relacionados con la conexión a la base de datos durante el arranque del contenedor.
![](imagenes/waitsh.png)

## Justificacion de la configuración personalizada
El contenedor ha sido personalizado para cumplir con los requisitos específicos de un servicio de gestión de logs en una arquitectura de microservicios:
1. Resiliencia ante dependencias externas:
El script wait-for-db.sh sincroniza el arranque del servicio con la disponibilidad de la base de datos, mitigando errores comunes en despliegues con contenedores.
2. Optimización del Tamaño: 
El uso de una imagen slim y la eliminación de cachés innecesarios minimizan los recursos consumidos por el contenedor.
3. Compatibilidad y Modularidad:
La configuración separa la lógica del servicio (app/) de las configuraciones (config.py), facilitando la modificación y reutilización en diferentes entornos.
4. Estandarización:
La ubicación de archivos y el uso de variables de entorno para la configuración de la base de datos garantizan un comportamiento predecible y un fácil mantenimiento.
5. Portabilidad:
Todo el código y la configuración están encapsulados en el contenedor, lo que permite desplegar el servicio en cualquier entorno compatible con Docker.

## Puerto expuesto y justificación
- Puerto expuesto: El microservicio está configurado para escuchar en el puerto 5003, tanto en el contenedor como en el host, lo que permite la comunicación entre servicios y el acceso desde herramientas externas para pruebas.
- Evitar conflictos de puertos: El puerto 5003 se seleccionó para distinguir este servicio del resto de los servicios en la arquitectura, como el app_service (puerto 5000).
- Estandarización: Mantener un puerto fijo para este microservicio simplifica el despliegue, la configuración y el mantenimiento.
- Visibilidad y depuración: La exposición del puerto en el host permite interactuar directamente con el servicio durante el desarrollo y realizar pruebas manuales con herramientas como curl o Postman, o directamente como una peticcion HTTP desde el navegador.
- Compatibilidad interna: Dentro de la red app_network, otros servicios pueden comunicarse con este microservicio utilizando su hostname (logs_service) y el puerto expuesto 5003, facilitando la integración.
