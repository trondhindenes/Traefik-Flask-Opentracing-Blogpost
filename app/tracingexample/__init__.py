import os
import logging
from flask import Flask
from flask_restful import Api
from jaeger_client import Config
from flask_opentracing import FlaskTracer
from tracingexample.tracer_helper2 import TracerHelper2

logging.getLogger('').handlers = []
logging.basicConfig(format='%(message)s', level=logging.DEBUG)

flask_app_name = os.getenv('FLASK_APP_NAME')
app = Flask(flask_app_name)

api = Api(app)
config = Config(
    config={
        'enabled': True,
        'sampler': {
            'type': 'const',
            'param': 1
        },
        'logging': True,
    },
    service_name=flask_app_name,
)
jaeger_tracer = config.initialize_tracer
flask_tracer = FlaskTracer(jaeger_tracer, True, app, ['url', 'url_rule', 'environ.HTTP_X_REAL_IP', 'path'])

#tracer_helper contains some small helper functions
tracer_helper = TracerHelper2(flask_tracer)

print('wiring up routes')
from tracingexample.api_customers import ApiCustomers
from tracingexample.api_customersbackend import ApiCustomersBackend
from tracingexample.api_orders import ApiOrders
from tracingexample.api_ordersbackend import ApiOrdersBackend