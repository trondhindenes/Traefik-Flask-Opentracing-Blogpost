from flask_restful import Resource
from tracingexample import api, flask_tracer, tracer_helper
import opentracing

class ApiOrdersBackend(Resource):
    def get(self):
        parent_span = flask_tracer.get_span()
        with opentracing.tracer.start_span('SuperAdvancedOrderGetter', child_of=parent_span) as span:
            orders = ['order1', 'order2']
            span.log_kv(
                {'orders_count': len(orders)}
            ) 
            return orders

api.add_resource(ApiOrdersBackend, '/ordersbackend')