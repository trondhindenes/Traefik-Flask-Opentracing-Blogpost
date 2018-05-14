import requests
import opentracing


class TracerHelper2(object):
    def __init__(self, tracer):
        self.tracer = tracer

    def inject_trace_headers(self, span, headers=None):
        text_carrier = {}
        self.tracer._tracer.inject(span.context, opentracing.Format.HTTP_HEADERS, text_carrier)
        if headers is None:
            return text_carrier
        else:
            for k, v in text_carrier.iteritems():
                headers[k] = v
            return headers

    def tracerequest_get(self, url, trace_name=None, headers=None):
        current_span = self.tracer.get_span()
        if trace_name is None:
            trace_name = 'requests.get'
        with opentracing.tracer.start_span(trace_name, child_of=current_span) as span:


            headers = self.inject_trace_headers(span, headers)
            r = requests.get(url, headers=headers)
            return r
