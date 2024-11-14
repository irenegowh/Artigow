# Configuración del gestor de tareas para ejecutar pruebas.

Como se explicó en el apartado anterior ([2. Configuración del gestor de tareas para ejecutar pruebas.](./GestorTareas.md)
), se ha elegido **Pytest** como biblioteca de pruebas debido a su popularidad en proyectos Python y su simplicidad para escribir pruebas concisas y claras. Con **Pytest**, puedes validar que las funcionalidades del proyecto se comporten como se espera.

A continuación, se detallan los pasos para configurar las pruebas iniciales:

## 1. Activación del entorno de desarrollo

Primero, se activó el entorno virtual para asegurar que todas las pruebas se ejecuten con las dependencias instaladas en el proyecto. Desde el directorio del repositorio, se utilizó el siguiente comando:

```bash
pipenv shell
```

## 2. Configuracion biblioteca de pruebas:

Para organizar las pruebas del proyecto, se creó un directorio específico llamado tests, donde se guardarán todos los archivos de prueba. Además, se añadió un archivo __init__.py dentro del directorio tests para que se reconozca como un paquete de Python, lo cual facilita las importaciones.

```bash
mkdir tests
touch tests/test_app.py
```

## 3. Prueba inicial

Se añadió una prueba inicial en el archivo test_app.py para validar que Pytest esté configurado correctamente. Esta prueba sencilla verifica que la aplicación puede devolver un mensaje de bienvenida:

La aplicación fue configurada para retornar un mensaje de bienvenida, como se muestra en la siguiente captura:

![App inicial](./imagenes/AppInicial.jpg)

![Test inicial](./imagenes/TestInicial.jpg)

##4. Ejecución y resolución de errores de importación

Al ejecutar la prueba inicial, surgió un error de importación. Este problema se solucionó añadiendo el archivo __init__.py en el directorio tests, permitiendo que Pytest reconozca el directorio como un paquete Python.

![Error de importación solucionado con __init__.py](./imagenes/TestNotPassed1.jpg)

## 5. Ejecución exitosa de la prueba

Finalmente, la prueba fue ejecutada correctamente y se mostró el mensaje "1 passed" en los resultados, indicando que el entorno de pruebas y la configuración inicial son funcionales:

![Test pasado exitosamente](./imagenes/TestPassed1.jpg)
