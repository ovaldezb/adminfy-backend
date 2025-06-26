from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
)
from constructs import Construct
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

class AdminfyBackendStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Ruta base para los handlers
        lambda_path = os.path.join(os.path.dirname(__file__), '..', 'lambda')

        # Variables de entorno comunes
        env_vars = {
            'MONGODB_URI': os.getenv('MONGODB_URI'),
        }

        # Crear Lambdas para CRUD de pagos
        create_pago_lambda = _lambda.Function(
            self, 'CreatePagoHandler',
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler='create_pago.handler',
            code=_lambda.Code.from_asset(os.path.join(lambda_path)),
            environment=env_vars
        )
        get_pago_lambda = _lambda.Function(
            self, 'GetPagoHandler',
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler='get_pago.handler',
            code=_lambda.Code.from_asset(os.path.join(lambda_path)),
            environment=env_vars
        )
        update_pago_lambda = _lambda.Function(
            self, 'UpdatePagoHandler',
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler='update_pago.handler',
            code=_lambda.Code.from_asset(os.path.join(lambda_path)),
            environment=env_vars
        )
        delete_pago_lambda = _lambda.Function(
            self, 'DeletePagoHandler',
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler='delete_pago.handler',
            code=_lambda.Code.from_asset(os.path.join(lambda_path)),
            environment=env_vars
        )

        # API Gateway REST API con CORS habilitado
        api = apigateway.RestApi(self, 'PagosApi',
            rest_api_name='Pagos Service',
            description='API para CRUD de pagos.',
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=apigateway.Cors.ALL_ORIGINS,
                allow_methods=apigateway.Cors.ALL_METHODS,
                allow_headers=apigateway.Cors.DEFAULT_HEADERS,
                allow_credentials=True
            )
        )

        pagos = api.root.add_resource('pagos')
        pagos.add_method('POST', apigateway.LambdaIntegration(create_pago_lambda))  # Crear pago
        pagos.add_method('GET', apigateway.LambdaIntegration(get_pago_lambda))      # Listar pagos

        pago = pagos.add_resource('{id}')
        pago.add_method('GET', apigateway.LambdaIntegration(get_pago_lambda))       # Obtener pago por id
        pago.add_method('PUT', apigateway.LambdaIntegration(update_pago_lambda))    # Actualizar pago
        pago.add_method('DELETE', apigateway.LambdaIntegration(delete_pago_lambda)) # Eliminar pago
