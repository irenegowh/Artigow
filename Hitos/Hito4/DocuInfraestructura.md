# Documentación y justificación de la estructura del clúster de contenedores
## Introducción

El diseño del clúster de contenedores para la aplicación Artigow busca 
abordar las necesidades de modularidad, escalabilidad y separación de 
responsabilidades, utilizando Docker Compose para su configuración. 
Este enfoque permite desplegar y gestionar la infraestructura de 
manera reproducible en entornos de desarrollo y pruebas.

El clúster está compuesto por tres servicios principales:
1. app_service: Contenedor principal que implementa la lógica de 
negocio de la aplicación Artigow.
2. db_service: Contenedor que gestiona dos bases de datos, una para 
los datos principales de la aplicación y otra para los logs.
3. logs_service: Microservicio para el procesamiento y visualización 
de logs.

Los archivos de los contenedores se han guardado en el repositorio en un directorio especifico [Directorio contenedores](../../app/container_h4_Simple/)


![](imagenes/tree1.png)

![](imagenes/tree2.png)

## Justificación de la estructura
La estructura de este clúster ha sido diseñada teniendo en cuenta 
principios clave de arquitectura basada en contenedores:
 
- Separación de responsabilidades
1. app_service: Encapsula las funcionalidades principales de la aplicación Artigow, incluyendo la gestión de usuarios, subida de obras de arte, votaciones y rankings. Este servicio interactúa tanto con la base de datos como con el servicio de logs.
2. db_service: Proporciona un almacenamiento centralizado y persistente para los datos de la aplicación y los logs. La utilización de un único contenedor para ambas bases de datos simplifica la gestión mientras se mantiene una separación lógica mediante bases de datos independientes.
3. logs_service: Gestiona los registros de eventos y errores generados por app_service, procesándolos antes de almacenarlos en la base de datos específica para logs y ofreciendo una interfaz para su consulta desde el navegador.

- Escalabilidad
Si el tráfico hacia la aplicación aumenta, se pueden añadir réplicas de app_service.
En caso de un alto volumen de logs, se puede escalar el servicio de logs para manejar un mayor flujo de datos antes de enviarlos a la base de datos. Sin embargo, el almacenamiento de los logs sigue dependiendo de la capacidad del servicio de base de datos (db_service ), que puede escalarse mediante volúmenes persistentes y configuraciones de alta disponibilidad.

- Reutilización de imágenes y despliegue reproducible
Las imágenes de Docker de cada servicio están almacenadas en GitHub Container Registry (ghcr.io), lo que garantiza un acceso centralizado y la posibilidad de reutilizar configuraciones en diferentes entornos.
El archivo docker-compose.yaml define todas las configuraciones necesarias para el despliegue del clúster, haciendo que el entorno sea fácilmente replicable.

- Aislamiento y Seguridad
Cada contenedor se ejecuta en una red de tipo en el bridge definida [docker-compose.yaml ](../../app/container_h4_Simple/docker-compose.yaml ), lo que asegura una comunicación interna eficiente y restringe el acceso externo no autorizado.
Los secretos sensibles, como las credenciales de la base de datos, están gestionados a través de variables de entorno, minimizando la exposición de datos sensibles.

- Facilidad de Desarrollo y Pruebas
El uso de Docker Compose permite a los desarrolladores levantar el clúster completo con un solo comando, eliminando configuraciones manuales y facilitando pruebas locales.

La configuración de dependencias, mediante depends_on ,asegura que los servicios críticos, como la base de datos, estén disponibles antes de que los servicios dependientes inicien.

