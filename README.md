# PARQUEO_USERS_MS


## CONTENIDO DE ESTE ARCHIVO

* Introducción
* Requerimientos
* Recomendaciones
* Instalación
* Configuración
* Ejecución
* FAQ
* contacto


## INTRODUCCIÓN

Este proyecto es una serie de microservicios para el front-end del aplicativo web Parqueo,
esta desarrollado con FastAPI que utiliza Uvicorn como servidor ASGI y SQLAlchemy para la gestion de la base de datos.


## REQUERIMIENTOS

Este proyecto requiere los siguientes módulos:

* Uvicorn (https://www.uvicorn.org/)
* FastAPI (https://fastapi.tiangolo.com/)
* SQLAlchemy (https://www.sqlalchemy.org/)

## RECOMENDACIONES

Se recomiendan las siguientes herramientas para un mejor desarrollo y mantenimiento:

* Python 3.10+

## INSTALACIÓN

1. Clonar el repositorio:
    git clone https://github.com/sojoko/parqueo_users_ms.git
    cd tu_proyecto

2. Crear y activar un entorno virtual:
    python -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`

3. Instalar las dependencias desde el archivo requirements.txt:
    pip install -r requirements.txt

4. Crear un archivo .env en el directorio raíz del proyecto y agregar las variables de entorno necesarias:
    touch .env

* Añadir el siguiente contenido al archivo .env:
    DATABASE_URL=sqlite:///./test.db  # O usa tu URL de base de datos

## EJECUCIÓN

Para ejecutar el proyecto:
    uvicorn main:app --reload
    
## FAQ

P: ¿Cómo puedo cambiar la configuración de la base de datos?
R: Puedes cambiar la URL de la base de datos en el archivo .env.

## CONTACTO

Si tienes alguna duda al respecto por favor comunicate a los siguientes correos electronicos:
- jonhathansojo@gmail.com
- chop052009@gmail.com
