from flask_restful import Resource
from tracingexample import api, flask_tracer
import requests
import opentracing

def inject_trace_headers(span, headers=None):
    text_carrier = {}
    flask_tracer._tracer.inject(span.context, opentracing.Format.HTTP_HEADERS, text_carrier)
    if headers is None:
        return text_carrier
    else:
        for k in text_carrier.keys():
            headers[k] = text_carrier[k]
        return headers

class ApiCustomers(Resource):
    def get(self):
        return requests.get('http://localhost:19000/service2/customersbackend').json()

api.add_resource(ApiCustomers, '/customers')