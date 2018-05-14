from flask_restful import Resource
from tracingexample import api

class ApiCustomersBackend(Resource):
    def get(self):
        return ['mommi', 'papi']

api.add_resource(ApiCustomersBackend, '/customersbackend')