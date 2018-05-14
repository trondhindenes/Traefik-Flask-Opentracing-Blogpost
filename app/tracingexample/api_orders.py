from flask_restful import Resource
from tracingexample import api, tracer_helper

class ApiOrders(Resource):
    def get(self):
        #special wrapper that sends the trace headers with the request
        return tracer_helper.tracerequest_get('http://localhost:19000/service2/ordersbackend', trace_name='GetOrders').json()

api.add_resource(ApiOrders, '/orders')