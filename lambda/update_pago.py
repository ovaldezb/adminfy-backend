import os

def handler(event, context):
    # Aquí iría la lógica para actualizar un pago en MongoDB
    mongodb_uri = os.environ.get('MONGODB_URI')
    pago_id = event.get('pathParameters', {}).get('id')
    # payload = event.get('body')
    return {
        'statusCode': 200,
        'body': f'Pago actualizado (mock), id: {pago_id}'
    } 