import re

from wsgiref.headers import Headers
from .middleware import HttpResponse, WSGIRequest
from application import urls


class BaseHandler(object):
    def __init__(self):
        pass


class WSGIHandler(BaseHandler):
    request_class = WSGIRequest

    def __init__(self, *args, **kwargs):
        super(WSGIHandler, self).__init__(*args, **kwargs)
        self._handler = None

    def __call__(self, environ, start_response):

        request = self.request_class(environ)
        response = self.get_response(request)

        response._handler_class = self.__class__

        status = '%d %s' % (response.status_code, response.reason_phrase)
        start_response(str(status), response.headers.items())

        if getattr(response, 'file_to_stream', None) is not None and environ.get('wsgi.file_wrapper'):
            response = environ['wsgi.file_wrapper'](response.file_to_stream)
        return response

    def _load_middleware(self, request):
        pass

    def route_distributing(self, request):
        print request.GET

        return HttpResponse("Test")

    def get_response(self, request):
        self._load_middleware(request)
        return self.route_distributing(request)


def get_application():
    return WSGIHandler()

