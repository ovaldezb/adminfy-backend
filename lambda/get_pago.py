import os
import json
from pymongo import MongoClient
from bson import ObjectId
from bson.json_util import dumps

def get_ingresos_collection():
    """Obtiene la colección de ingresos"""
    mongodb_uri = os.environ.get('MONGODB_URI')
    print(f"MONGODB_URI: {mongodb_uri}")  # Debug log
    
    if not mongodb_uri:
        raise ValueError("MONGODB_URI no está configurada en las variables de entorno")
    
    try:
        client = MongoClient(mongodb_uri)
        #print(f"Client: {client}")  # Debug log
        db = client.get_database('medici_dev')
        #print(f"DB: {db}")  # Debug log
        #print(f"Ingresos: {db['ingresos']}")  # Debug log
        return db['sucursals']
    except Exception as e:
        print(f"Error conectando a MongoDB: {str(e)}")  # Debug log
        raise

def handler(event, context):
    try:
        print(f"Event: {event}")  # Debug log
        #print(f"Environment variables: {dict(os.environ)}")  # Debug log
        
        # Obtener la colección de ingresos
        #print("Obteniendo la colección de ingresos")  # Debug log
        collection = get_ingresos_collection()
        print(f"parameters: {event.get('pathParameters', {})}")  # Debug log
        
        # Verificar si se solicita un ingreso específico por ID
        #pago_id = event.get('pathParameters', {}).get('id') if event.get('pathParameters', {}) != None else None:  
        if event.get('pathParameters', {}) :
            pago_id = event.get('pathParameters', {}).get('id')
        else:
            pago_id = None
        print(f"Pago ID: {pago_id}")  # Debug log
        
        if pago_id:
            # Obtener un ingreso específico por ID
            try:
                object_id = ObjectId(pago_id)
                ingreso = collection.find_one({"_id": object_id})
                
                if not ingreso:
                    return {
                        'statusCode': 404,
                        'headers': {
                            'Content-Type': 'application/json',
                            'Access-Control-Allow-Origin': '*'
                        },
                        'body': json.dumps({'error': 'Ingreso no encontrado'})
                    }
                
                # Convertir ObjectId a string para JSON serialization
                ingreso['_id'] = str(ingreso['_id'])
                
                return {
                    'statusCode': 200,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps(ingreso, default=str)
                }
                
            except Exception as e:
                return {
                    'statusCode': 400,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps({'error': f'ID inválido: {str(e)}'})
                }
        else:
            print("Iniciando consulta de ingresos")  # Debug log
            print(f"Ingresos: {collection.count_documents({})}")  # Debug log
            cursor = collection.find({})
            ingreso_dump = dumps([transformar(doc) for doc in cursor])
            ingresos_lista = json.loads(ingreso_dump)
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps(ingresos_lista)
            }
            
    except Exception as e:
        print(f"Error en handler: {str(e)}")  # Debug log
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': f'Error interno del servidor: {str(e)}'})
        } 

def transformar(doc):
    doc['_id'] = str(doc['_id'])
    return doc