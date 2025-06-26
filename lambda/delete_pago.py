import os

def handler(event, context):
    # Aquí iría la lógica para eliminar un pago en MongoDB
    mongodb_uri = os.environ.get('MONGODB_URI')
    pago_id = event.get('pathParameters', {}).get('id')
    return {
        'statusCode': 204,
        'body': f'Pago eliminado (mock), id: {pago_id}'
    } 