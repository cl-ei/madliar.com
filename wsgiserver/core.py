import re

from wsgiref.headers import Headers
from .middleware import HttpResponse, WSGIRequest, static_files_response, Http404Response
from etc.config import *
from application.urls import url as user_url_map


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

    def route_distributing(self, request, url_map=user_url_map):
        for url, view_func in url_map.items():
            m = re.match(url, request.route_path)
            if m:
                if isinstance(view_func, dict):
                    request.route_path = request.route_path[len(m.group()):] or "/"
                    return self.route_distributing(request, url_map=view_func)
                else:
                    return view_func(request, *m.groups())
        # Not hit
        if DEBUG:
            for url, static_path in STATICS_URL_MAP.items():
                m = re.match(url, request.path_info)
                if m:
                    request.route_path = request.path_info[len(m.group()):] or "/"
                    return static_files_response(request, static_path)
        return Http404Response()

    def get_response(self, request):
        self._load_middleware(request)
        return self.route_distributing(request)


def get_application():
    return WSGIHandler()

