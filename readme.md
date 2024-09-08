# Floristería API

## Descripción

Esta es una API RESTful para la gestión de productos y pedidos en una floristería. Permite a los usuarios consultar el catálogo de productos, realizar pedidos y gestionar el inventario de flores.

## Tecnologías

- **Backend**: FastAPI
- **Base de Datos**: MongoDB (Atlas)
- **Servidor ASGI**: Uvicorn
- **Cliente MongoDB**: Motor
- **Validación y Serialización**: Pydantic
- **Configuración de Entorno**: Python-dotenv

## Instalación

1. **Clonar el repositorio:**

   ```bash
   https://github.com/EpsyUwU/floreria_api.git
   cd floristeria-api
   
2. **Instalar las dependencias específicas:**

    ```bash
    pip install fastapi==0.114.0 uvicorn==0.30.6 motor==3.5.1 pydantic==2.9.0 python-dotenv==1.0.1 pymongo==4.8.0
   
3. **Crear base de datos:**


   Debes acceder a https://cloud.mongodb.com/ craerte una cuenta, crea un cluster revisa que sea la capa gratuita,selecciona un provedor, su region, dale un nombre al cluster en mi caso Floreria-api, una vez creado te abrira una ventanita donde te explica como conectarte sigue los pasos.


4. **Configurar las variables de entorno:**
   La URI te la proporciona Atlas
    ```bash
    MONGODB_URI=mongodb+srv://<usuario>:<contrasena>@<cluster>.mongodb.net/?retryWrites=true&w=majority&appName=<nombre_db>

5. **Ejecuta el script para llenar la DB**
   
   ```bash
   cd scripts/
   python init_db.py
   
6. **Ejecuta main**
   ```bash
   cd app/
   python main.py

## Documentacion

   La docuementacion de la api se encuentra en Swagger y ReDoc una vez corrido el proyecto puedes acceder a cualquira de estos dos atravez de los siguientes links
   ```bash
   http://127.0.0.1:8000/docs
   http://127.0.0.1:8000/redoc
   

    

