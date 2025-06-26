import os

def handler(event, context):
    print(event)
    # Aquí iría la lógica para crear un pago en MongoDB
    mongodb_uri = os.environ.get('MONGODB_URI')
    # payload = event.get('body')
    return {
        'statusCode': 201,
        'body': 'Pago creado (mock)'
    } 