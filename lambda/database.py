import os
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection

def get_database() -> Database:
    """Obtiene la conexión a la base de datos MongoDB"""
    mongodb_uri = os.environ.get('MONGODB_URI')
    if not mongodb_uri:
        raise ValueError("MONGODB_URI no está configurada en las variables de entorno")
    
    client = MongoClient(mongodb_uri)
    return client.ce-skill-stack  # Nombre de la base de datos

def get_ingresos_collection() -> Collection:
    """Obtiene la colección de ingresos"""
    db = get_database()
    return db.ingresos 