En este hito, se ha reestructurado la aplicación para adoptar un diseño basado en microservicios, aplicando principios de modularidad y desacoplamiento. El objetivo principal ha sido crear una API REST consistente, con una arquitectura organizada en capas que separa claramente la lógica de negocio, la gestión de rutas, y el acceso a datos.

Además, se han incorporado elementos clave para garantizar la calidad y robustez de la aplicación, como:

Modularidad con Blueprints: Las rutas de la API se han organizado en blueprints, asignando cada funcionalidad (autenticación, gestión de publicaciones, votos, etc.) a módulos independientes.

Lógica de Negocio en Servicios: Se ha encapsulado la lógica de negocio en servicios que procesan los datos y realizan validaciones antes de interactuar con los repositorios.

Acceso a Datos con Repositorios: Se ha implementado el patrón Repository para centralizar las operaciones con la base de datos, manteniendo una única fuente de acceso a los datos.

Sistema de Logging: Se ha configurado un sistema de logs para registrar las actividades de la API, incluyendo eventos importantes como errores, accesos y acciones de los usuarios.

Pruebas Automatizadas: Se han diseñado y ejecutado pruebas exhaustivas para verificar la funcionalidad de las rutas, asegurando que la API responde correctamente ante diferentes escenarios.

Esta reestructuración no solo mejora la mantenibilidad y escalabilidad de la aplicación, sino que también la prepara para integrarse en entornos de producción y soportar un flujo de trabajo basado en CI/CD.

