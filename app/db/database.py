from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConfigurationError
import os
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()

# URI de conexión a MongoDB desde las variables de entorno
MONGODB_URI = os.getenv("MONGODB_URI")

# Verificar que la URI está disponible
if not MONGODB_URI:
    raise ValueError("La URI de MongoDB no está configurada en las variables de entorno.")

# Crear un nuevo cliente y conectar al servidor
try:
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)  # Agregar timeout
    # Enviar un ping para confirmar la conexión exitosa
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
    db = client["floristeria_db"]  # Nombre de la base de datos
except ServerSelectionTimeoutError:
    print("Error de conexión a MongoDB Atlas: No se pudo conectar al servidor.")
except ConfigurationError as e:
    print(f"Error de configuración en MongoDB Atlas: {e}")
except Exception as e:
    print(f"Error inesperado: {e}")

def get_db():
    return db
