from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConfigurationError
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

if not MONGODB_URI:
    raise ValueError("La URI de MongoDB no está configurada en las variables de entorno.")

try:
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=10000)
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
    db = client["floristeria_db"]
except ServerSelectionTimeoutError:
    print("Error de conexión a MongoDB Atlas: No se pudo conectar al servidor.")
except ConfigurationError as e:
    print(f"Error de configuración en MongoDB Atlas: {e}")
except Exception as e:
    print(f"Error inesperado: {e}")

def get_db():
    return db
