# Justificacion framework

Para el desarrollo de esta aplicación, Artigow, se ha optado por utilizar Flask como framework principal para implementar la API REST, como se mencionó brevemente en el Hito 2: Integración continua. 
Se ha considerado este framework frente a otros porque se alinea de manera sencilla con los objetivos planteados de modularidad, flexibilidad y escalabilidad del proyecto, así como permitir el desarrollo de las funcionalidades de manera sencilla con el lenguaje de programación Python para poder finalizar el proyecto en el tiempo estimado de la asignatura.

A continuación, detallo de manera un poco más concreta que características he tenido en cuenta para elegir Flask para el desarrollo de la API REST.

## 1. Ligereza y flexibliidad:
La primera razón por la que se ha escogido este framework es por su carácter minimalista, y las opciones que ofrece para personalizar su configuración según las necesidades específicas, que en este caso es muy conveniente para el diseño de un sistema basado en microservicios como se plantea en este hito.
   
## 2. Soporte para APIs REST: 
Entre otras razones, Flask ofrece muchas extensiones entre las que está Flask-RESTful, que proporciona herramientas sencillas y a su vez robusta para el desarrollo de APIs bien estructuradas de manera modular separando endpoints, middleware, la gestión de errores y la gestión de logs.
   
## 3. Facilidad de integración: 
Otra de las razones es que puede integrarse fácilmente con diversas bibliotecas y herramientas, lo que he considaro para el desarrollo se hace uso de otra librerias como SQLAlchemy para el manejo de bases de datos y en próximos se puede extender para dar soporte a contenedores con Docker.

Estos han sido los principales motivos por los que se ha escogido frente a otras alternativas como FastAPI o Django, pues estas opciones son más complejas de implementar y tiene una curva de aprendizaje menor que he considera esencial para el tiempo estimado.
