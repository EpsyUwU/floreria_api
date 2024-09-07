from pymongo import MongoClient
from pymongo.errors import ConfigurationError, ServerSelectionTimeoutError
import os
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()

# URI de conexión a MongoDB desde las variables de entorno
MONGODB_URI = os.getenv("MONGODB_URI")

# Verificar que la URI está disponible
if not MONGODB_URI:
    raise ValueError("La URI de MongoDB no está configurada en las variables de entorno.")

# Conectar a MongoDB
try:
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)  # Agregar timeout
    # Enviar un ping para confirmar la conexión exitosa
    client.admin.command('ping')
    db = client["floristeria_db"]  # Nombre de la base de datos

    # Crear colecciones
    productos_collection = db["productos"]
    pedidos_collection = db["pedidos"]

    # Insertar productos iniciales (ejemplo)
    productos_collection.insert_many([
        {"nombre": "Rosa Roja", "precio": 10.00, "stock": 100},
        {"nombre": "Tulipán Amarillo", "precio": 12.00, "stock": 150}
    ])

    print("Base de datos inicializada correctamente.")

except ServerSelectionTimeoutError:
    print("Error de conexión a MongoDB Atlas: No se pudo conectar al servidor.")
except ConfigurationError as e:
    print(f"Error de configuración en MongoDB Atlas: {e}")
except Exception as e:
    print(f"Error inesperado: {e}")
